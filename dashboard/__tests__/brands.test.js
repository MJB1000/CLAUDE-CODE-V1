/**
 * TDD tests for Brand Management + Price Tracking + Google Sheets logging.
 * RED phase — these tests should FAIL until the APIs are implemented.
 *
 * Run: cd dashboard && npx jest --config jest.config.js __tests__/brands.test.js
 */

// ── Mock KV store ───────────────────────────────────────────────────────────────

const mockKvStore = {};

const mockKv = {
  get: jest.fn(async (key) => {
    if (key in mockKvStore) return mockKvStore[key];
    return null;
  }),
  set: jest.fn(async (key, value) => {
    mockKvStore[key] = value;
    return "OK";
  }),
  del: jest.fn(async (key) => {
    delete mockKvStore[key];
    return 1;
  }),
};

jest.mock("../api/_kv", () => ({ kv: mockKv }));

// ── Mock Google Sheets ─────────────────────────────────────────────────────────

const mockAppend = jest.fn(async () => ({ data: { updates: { updatedRows: 1 } } }));
jest.mock("../api/_sheets", () => ({
  appendRow: mockAppend,
}));

// ── Helpers ─────────────────────────────────────────────────────────────────────

function createReq(overrides = {}) {
  return {
    method: "POST",
    headers: { "x-api-key": "changeme" },
    query: {},
    body: {},
    ...overrides,
  };
}

function createRes() {
  const res = {
    _status: null,
    _body: null,
    _headers: {},
    setHeader: jest.fn((k, v) => { res._headers[k] = v; }),
    status: jest.fn((code) => { res._status = code; return res; }),
    json: jest.fn((data) => { res._body = data; return res; }),
    send: jest.fn((data) => { res._body = data; return res; }),
    end: jest.fn(() => res),
  };
  return res;
}

function resetKvStore() {
  Object.keys(mockKvStore).forEach(k => delete mockKvStore[k]);
  mockKv.get.mockClear();
  mockKv.set.mockClear();
  mockKv.del.mockClear();
  mockAppend.mockClear();
}

// ═══════════════════════════════════════════════════════════════════════════════
// 1. BRAND CRUD — POST /api/brands, GET /api/brands
// ═══════════════════════════════════════════════════════════════════════════════

describe("api/brands.js — Brand CRUD", () => {
  let handler;

  beforeEach(() => {
    resetKvStore();
    jest.resetModules();
    jest.mock("../api/_kv", () => ({ kv: mockKv }));
    jest.mock("../api/_sheets", () => ({ appendRow: mockAppend }));
    handler = require("../api/brands.js");
  });

  // ── Auth ─────────────────────────────────────────────────────────────────────

  test("rejects unauthenticated POST", async () => {
    const req = createReq({ headers: {} });
    const res = createRes();
    await handler(req, res);
    expect(res._status).toBe(401);
  });

  test("allows OPTIONS for CORS preflight", async () => {
    const req = createReq({ method: "OPTIONS" });
    const res = createRes();
    await handler(req, res);
    expect(res._status).toBe(200);
  });

  // ── CREATE brand ────────────────────────────────────────────────────────────

  test("creates a new brand with required fields", async () => {
    const req = createReq({
      body: {
        name: "Acme Wipers",
        market: "AU",
        website: "https://acme.com.au",
        product_category: "wiper blades",
        reference_product: "Ford Territory 2009",
        competitors: [
          {
            name: "Rival Co",
            url: "https://rival.com.au",
            product_url: "https://rival.com.au/ford-territory",
            type: "specialist",
          },
        ],
      },
    });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(201);
    expect(res._body.ok).toBe(true);
    expect(res._body.brand.id).toBeDefined();
    expect(res._body.brand.name).toBe("Acme Wipers");
    expect(res._body.brand.competitors).toHaveLength(1);
    expect(res._body.brand.competitors[0].id).toBeDefined(); // auto-generated
    expect(res._body.brand.status).toBe("active");
    expect(res._body.brand.created_at).toBeDefined();
  });

  test("rejects brand missing required fields", async () => {
    const req = createReq({ body: { name: "Incomplete" } });
    const res = createRes();
    await handler(req, res);
    expect(res._status).toBe(400);
    expect(res._body.error).toMatch(/market/i);
  });

  test("rejects brand with no competitors", async () => {
    const req = createReq({
      body: {
        name: "Lonely Brand",
        market: "AU",
        website: "https://lonely.com",
        product_category: "wipers",
        reference_product: "Test Product",
        competitors: [],
      },
    });
    const res = createRes();
    await handler(req, res);
    expect(res._status).toBe(400);
    expect(res._body.error).toMatch(/competitor/i);
  });

  test("rejects competitor missing URL", async () => {
    const req = createReq({
      body: {
        name: "Bad Competitor Brand",
        market: "AU",
        website: "https://bc.com",
        product_category: "wipers",
        reference_product: "Test",
        competitors: [{ name: "No URL Co", type: "specialist" }],
      },
    });
    const res = createRes();
    await handler(req, res);
    expect(res._status).toBe(400);
    expect(res._body.error).toMatch(/url/i);
  });

  test("stores brand in KV with correct key", async () => {
    const req = createReq({
      body: {
        name: "KV Test Brand",
        market: "NZ",
        website: "https://kvtest.co.nz",
        product_category: "wipers",
        reference_product: "Test",
        competitors: [
          { name: "Comp A", url: "https://compa.co.nz", type: "retailer" },
        ],
      },
    });
    const res = createRes();
    await handler(req, res);

    const brandId = res._body.brand.id;
    // Should store individual brand
    expect(mockKvStore[`brands:${brandId}`]).toBeDefined();
    expect(mockKvStore[`brands:${brandId}`].name).toBe("KV Test Brand");
    // Should update brand index
    expect(mockKvStore["brands:index"]).toContain(brandId);
  });

  // ── LIST brands ────────────────────────────────────────────────────────────

  test("lists all brands via GET", async () => {
    // Seed two brands
    mockKvStore["brands:index"] = ["brand_1", "brand_2"];
    mockKvStore["brands:brand_1"] = { id: "brand_1", name: "Alpha", status: "active" };
    mockKvStore["brands:brand_2"] = { id: "brand_2", name: "Beta", status: "active" };

    const req = createReq({ method: "GET" });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(200);
    expect(res._body.brands).toHaveLength(2);
    expect(res._body.brands[0].name).toBe("Alpha");
  });

  test("returns empty array when no brands exist", async () => {
    const req = createReq({ method: "GET" });
    const res = createRes();
    await handler(req, res);
    expect(res._status).toBe(200);
    expect(res._body.brands).toEqual([]);
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// 2. PRICE PERIODS — Sale vs BAU tagging
// ═══════════════════════════════════════════════════════════════════════════════

describe("api/periods.js — Sale/BAU period management", () => {
  let handler;

  beforeEach(() => {
    resetKvStore();
    jest.resetModules();
    jest.mock("../api/_kv", () => ({ kv: mockKv }));
    jest.mock("../api/_sheets", () => ({ appendRow: mockAppend }));
    handler = require("../api/periods.js");
  });

  test("creates a sale period for a brand", async () => {
    const req = createReq({
      body: {
        brand_id: "brand_1",
        label: "Winter Sale 2026",
        type: "sale",
        start_date: "2026-06-01",
        end_date: "2026-06-30",
      },
    });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(201);
    expect(res._body.period.id).toBeDefined();
    expect(res._body.period.type).toBe("sale");
    expect(res._body.period.label).toBe("Winter Sale 2026");
  });

  test("creates a BAU period", async () => {
    const req = createReq({
      body: {
        brand_id: "brand_1",
        label: "Q1 BAU",
        type: "bau",
        start_date: "2026-01-01",
        end_date: "2026-03-31",
      },
    });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(201);
    expect(res._body.period.type).toBe("bau");
  });

  test("rejects period with invalid type", async () => {
    const req = createReq({
      body: {
        brand_id: "brand_1",
        label: "Bad Type",
        type: "promo",
        start_date: "2026-01-01",
        end_date: "2026-01-31",
      },
    });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(400);
    expect(res._body.error).toMatch(/type/i);
  });

  test("rejects period with end before start", async () => {
    const req = createReq({
      body: {
        brand_id: "brand_1",
        label: "Backwards",
        type: "sale",
        start_date: "2026-06-30",
        end_date: "2026-06-01",
      },
    });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(400);
    expect(res._body.error).toMatch(/date/i);
  });

  test("lists periods for a brand via GET", async () => {
    mockKvStore["periods:brand_1"] = [
      { id: "p1", brand_id: "brand_1", label: "Sale", type: "sale", start_date: "2026-06-01", end_date: "2026-06-30" },
      { id: "p2", brand_id: "brand_1", label: "BAU", type: "bau", start_date: "2026-07-01", end_date: "2026-09-30" },
    ];

    const req = createReq({ method: "GET", query: { brand_id: "brand_1" } });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(200);
    expect(res._body.periods).toHaveLength(2);
  });

  test("tags current date with active period", async () => {
    mockKvStore["periods:brand_1"] = [
      { id: "p1", brand_id: "brand_1", label: "Winter Sale", type: "sale", start_date: "2026-04-01", end_date: "2026-04-30" },
    ];

    const req = createReq({
      method: "GET",
      query: { brand_id: "brand_1", date: "2026-04-15" },
    });
    const res = createRes();
    await handler(req, res);

    expect(res._body.active_period).toBeDefined();
    expect(res._body.active_period.type).toBe("sale");
    expect(res._body.active_period.label).toBe("Winter Sale");
  });

  test("returns null active_period when date is outside all periods", async () => {
    mockKvStore["periods:brand_1"] = [
      { id: "p1", brand_id: "brand_1", label: "Winter Sale", type: "sale", start_date: "2026-06-01", end_date: "2026-06-30" },
    ];

    const req = createReq({
      method: "GET",
      query: { brand_id: "brand_1", date: "2026-04-15" },
    });
    const res = createRes();
    await handler(req, res);

    expect(res._body.active_period).toBeNull();
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// 3. GOOGLE SHEETS LOGGING — append row on ingest
// ═══════════════════════════════════════════════════════════════════════════════

describe("api/_sheets.js — Google Sheets logging", () => {
  test("sheets module exports appendRow function", () => {
    // We mock it above, but the real module should exist and export appendRow
    jest.resetModules();
    jest.mock("../api/_kv", () => ({ kv: mockKv }));
    // This will fail until _sheets.js exists
    const sheets = jest.requireActual("../api/_sheets.js");
    expect(typeof sheets.appendRow).toBe("function");
  });
});

describe("api/brands.js — Sheets logging on brand create", () => {
  let handler;

  beforeEach(() => {
    resetKvStore();
    jest.resetModules();
    jest.mock("../api/_kv", () => ({ kv: mockKv }));
    jest.mock("../api/_sheets", () => ({ appendRow: mockAppend }));
    handler = require("../api/brands.js");
  });

  test("logs brand creation to Google Sheets", async () => {
    const req = createReq({
      body: {
        name: "Sheet Test Brand",
        market: "AU",
        website: "https://sheet.com.au",
        product_category: "wipers",
        reference_product: "Ford Territory",
        competitors: [
          { name: "Comp X", url: "https://compx.com.au", type: "specialist" },
        ],
      },
    });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(201);
    expect(mockAppend).toHaveBeenCalledTimes(1);

    const appendArgs = mockAppend.mock.calls[0];
    expect(appendArgs[0]).toBe("Brands"); // sheet name
    expect(appendArgs[1]).toContain("Sheet Test Brand"); // row data includes brand name
    expect(appendArgs[1]).toContain("AU"); // row data includes market
  });
});

describe("Ingest + Sheets integration", () => {
  let ingestHandler;

  beforeEach(() => {
    resetKvStore();
    jest.resetModules();
    jest.mock("../api/_kv", () => ({ kv: mockKv }));
    jest.mock("../api/_sheets", () => ({ appendRow: mockAppend }));
    ingestHandler = require("../api/ingest.js");
  });

  test("logs price data to Google Sheets on ingest", async () => {
    // Set up a brand first
    mockKvStore["brands:index"] = ["brand_1"];
    mockKvStore["brands:brand_1"] = {
      id: "brand_1",
      name: "Test Brand",
      market: "AU",
      status: "active",
      competitors: [{ id: "comp_1", name: "Comp 1" }],
    };
    mockKvStore["periods:brand_1"] = [
      { id: "p1", brand_id: "brand_1", type: "sale", label: "Sale", start_date: "2026-04-01", end_date: "2026-04-30" },
    ];

    const req = createReq({
      body: {
        date: "2026-04-07",
        brand_id: "brand_1",
        sites: [
          {
            id: "comp_1",
            name: "Comp 1",
            market: "AU",
            is_on_sale: true,
            promotion_intensity: 35,
            promos: [{ raw_text: "20% off", discount_pct: 20 }],
            territory_price: { price: 29.99, url: "https://comp.com/product" },
          },
        ],
        day_of_week: 2,
        is_weekend: false,
      },
    });
    const res = createRes();
    await ingestHandler(req, res);

    expect(res._status).toBe(200);
    // Should have logged to the Prices sheet
    const sheetsCalls = mockAppend.mock.calls.filter(c => c[0] === "Prices");
    expect(sheetsCalls.length).toBeGreaterThanOrEqual(1);

    // Row should contain date, brand, price, period type
    const row = sheetsCalls[0][1];
    expect(row).toContain("2026-04-07");
    expect(row).toContain(29.99);
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// 4. PRICE TRACKER DATA — aggregated view for dashboard
// ═══════════════════════════════════════════════════════════════════════════════

describe("api/price-tracker.js — Price history by period", () => {
  let handler;

  beforeEach(() => {
    resetKvStore();
    jest.resetModules();
    jest.mock("../api/_kv", () => ({ kv: mockKv }));
    jest.mock("../api/_sheets", () => ({ appendRow: mockAppend }));
    handler = require("../api/price-tracker.js");
  });

  test("returns price history for a brand", async () => {
    mockKvStore["brands:brand_1"] = {
      id: "brand_1", name: "Test Brand", market: "AU", status: "active",
      competitors: [{ id: "comp_1", name: "Comp 1" }],
    };
    mockKvStore["prices:brand_1"] = [
      { date: "2026-04-01", competitor_id: "comp_1", price: 32.00, period_type: "bau" },
      { date: "2026-04-05", competitor_id: "comp_1", price: 24.00, period_type: "sale" },
      { date: "2026-04-06", competitor_id: "comp_1", price: 24.00, period_type: "sale" },
    ];

    const req = createReq({ method: "GET", query: { brand_id: "brand_1" } });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(200);
    expect(res._body.brand.name).toBe("Test Brand");
    expect(res._body.prices).toHaveLength(3);
    expect(res._body.summary.bau_avg_price).toBeCloseTo(32.0);
    expect(res._body.summary.sale_avg_price).toBeCloseTo(24.0);
    expect(res._body.summary.sale_discount_pct).toBeCloseTo(25.0);
  });

  test("returns 404 for unknown brand", async () => {
    const req = createReq({ method: "GET", query: { brand_id: "nonexistent" } });
    const res = createRes();
    await handler(req, res);
    expect(res._status).toBe(404);
  });

  test("returns empty prices for brand with no history", async () => {
    mockKvStore["brands:brand_1"] = {
      id: "brand_1", name: "New Brand", market: "AU", status: "active",
      competitors: [],
    };

    const req = createReq({ method: "GET", query: { brand_id: "brand_1" } });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(200);
    expect(res._body.prices).toEqual([]);
    expect(res._body.summary.bau_avg_price).toBeNull();
    expect(res._body.summary.sale_avg_price).toBeNull();
  });

  test("filters prices by period type", async () => {
    mockKvStore["brands:brand_1"] = {
      id: "brand_1", name: "Test", market: "AU", status: "active",
      competitors: [{ id: "c1", name: "C1" }],
    };
    mockKvStore["prices:brand_1"] = [
      { date: "2026-04-01", competitor_id: "c1", price: 30, period_type: "bau" },
      { date: "2026-04-10", competitor_id: "c1", price: 22, period_type: "sale" },
    ];

    const req = createReq({ method: "GET", query: { brand_id: "brand_1", period: "sale" } });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(200);
    expect(res._body.prices).toHaveLength(1);
    expect(res._body.prices[0].period_type).toBe("sale");
  });
});
