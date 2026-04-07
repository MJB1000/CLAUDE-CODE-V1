/**
 * TDD Round 2 — Coverage gap tests.
 * RED phase: rate limiting, anomaly detection, sale state, price-tracker edges, brand defaults.
 *
 * Run: cd dashboard && npx jest --config jest.config.js __tests__/coverage-gaps.test.js
 */

// ── Mock KV store ───────────────────────────────────────────────────────────────

const mockKvStore = {};

const mockKv = {
  get: jest.fn(async (key) => mockKvStore[key] ?? null),
  set: jest.fn(async (key, value) => { mockKvStore[key] = value; return "OK"; }),
  del: jest.fn(async (key) => { delete mockKvStore[key]; return 1; }),
  incr: jest.fn(async (key) => {
    mockKvStore[key] = (mockKvStore[key] || 0) + 1;
    return mockKvStore[key];
  }),
  expire: jest.fn(async () => 1),
};

jest.mock("../api/_kv", () => ({ kv: mockKv }));

const mockAppend = jest.fn(async () => ({ data: { updates: { updatedRows: 1 } } }));
jest.mock("../api/_sheets", () => ({ appendRow: mockAppend }));

const mockSendMail = jest.fn(async () => ({ messageId: "test-123" }));
jest.mock("nodemailer", () => ({
  createTransport: jest.fn(() => ({ sendMail: mockSendMail })),
}));

// ── Helpers ─────────────────────────────────────────────────────────────────────

function createReq(overrides = {}) {
  return {
    method: "POST",
    headers: { "x-api-key": "changeme", "x-forwarded-for": "1.2.3.4" },
    query: {},
    body: {},
    ...overrides,
  };
}

function createRes() {
  const res = {
    _status: null, _body: null, _headers: {},
    setHeader: jest.fn((k, v) => { res._headers[k] = v; }),
    status: jest.fn((code) => { res._status = code; return res; }),
    json: jest.fn((data) => { res._body = data; return res; }),
    send: jest.fn((data) => { res._body = data; return res; }),
    end: jest.fn(() => res),
  };
  return res;
}

function resetAll() {
  Object.keys(mockKvStore).forEach(k => delete mockKvStore[k]);
  [mockKv.get, mockKv.set, mockKv.del, mockKv.incr, mockKv.expire, mockAppend].forEach(m => m.mockClear());
}

// ═══════════════════════════════════════════════════════════════════════════════
// 1. RATE LIMITING (ingest.js lines 14-24)
// ═══════════════════════════════════════════════════════════════════════════════

describe("Ingest — Rate limiting", () => {
  let handler;

  beforeEach(() => {
    resetAll();
    jest.resetModules();
    jest.mock("../api/_kv", () => ({ kv: mockKv }));
    jest.mock("../api/_sheets", () => ({ appendRow: mockAppend }));
    handler = require("../api/ingest.js");
  });

  test("sets rate limit headers on successful request", async () => {
    const req = createReq({
      body: { date: "2026-04-07", sites: [], day_of_week: 2, is_weekend: false },
    });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(200);
    expect(res._headers["X-RateLimit-Limit"]).toBeDefined();
    expect(res._headers["X-RateLimit-Remaining"]).toBeDefined();
  });

  test("returns 429 when rate limit exceeded", async () => {
    // Pre-fill the rate limit counter to be at the limit
    mockKvStore["ratelimit:ingest:1.2.3.4"] = 10;

    const req = createReq({
      body: { date: "2026-04-07", sites: [], day_of_week: 2, is_weekend: false },
    });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(429);
    expect(res._body.error).toMatch(/rate limit/i);
  });

  test("rate limit uses x-forwarded-for IP", async () => {
    const req = createReq({
      headers: { "x-api-key": "changeme", "x-forwarded-for": "10.0.0.1, 10.0.0.2" },
      body: { date: "2026-04-07", sites: [], day_of_week: 2, is_weekend: false },
    });
    const res = createRes();
    await handler(req, res);

    expect(mockKv.incr).toHaveBeenCalledWith("ratelimit:ingest:10.0.0.1");
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// 2. ANOMALY DETECTION (ingest.js lines 171-188)
// ═══════════════════════════════════════════════════════════════════════════════

describe("Ingest — Anomaly detection", () => {
  let handler;

  beforeEach(() => {
    resetAll();
    jest.resetModules();
    jest.mock("../api/_kv", () => ({ kv: mockKv }));
    jest.mock("../api/_sheets", () => ({ appendRow: mockAppend }));
    handler = require("../api/ingest.js");
  });

  test("detects anomaly when intensity spikes above 2σ", async () => {
    // Build 14 days of low-intensity history (with slight variation so stddev > 0)
    const historyKeys = [];
    for (let i = 1; i <= 14; i++) {
      const d = `2026-03-${String(i).padStart(2, "0")}`;
      historyKeys.push(d);
      mockKvStore[`wiper:history:${d}`] = {
        date: d, sites: [{ id: "comp_1", promotion_intensity: 3 + (i % 3) }],
      };
    }
    mockKvStore["wiper:history_keys"] = historyKeys;
    mockKvStore["wiper:alerts"] = [];

    const req = createReq({
      body: {
        date: "2026-04-07",
        day_of_week: 2,
        is_weekend: false,
        sites: [{
          id: "comp_1", name: "Test Comp", market: "AU",
          is_on_sale: true, promotion_intensity: 85,
          promos: [{ raw_text: "80% OFF EVERYTHING" }],
        }],
      },
    });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(200);
    // Should generate an anomaly alert
    const anomalyAlerts = res._body.alerts.filter(a => a.type === "anomaly");
    expect(anomalyAlerts.length).toBe(1);
    expect(anomalyAlerts[0].brand).toBe("Test Comp");
  });

  test("does NOT flag anomaly when history < 14 days", async () => {
    const historyKeys = [];
    for (let i = 1; i <= 5; i++) {
      const d = `2026-03-${String(i).padStart(2, "0")}`;
      historyKeys.push(d);
      mockKvStore[`wiper:history:${d}`] = {
        date: d, sites: [{ id: "comp_1", promotion_intensity: 5 }],
      };
    }
    mockKvStore["wiper:history_keys"] = historyKeys;
    mockKvStore["wiper:alerts"] = [];

    const req = createReq({
      body: {
        date: "2026-04-07", day_of_week: 2, is_weekend: false,
        sites: [{ id: "comp_1", name: "Test", market: "AU", is_on_sale: true, promotion_intensity: 85, promos: [] }],
      },
    });
    const res = createRes();
    await handler(req, res);

    const anomalyAlerts = res._body.alerts.filter(a => a.type === "anomaly");
    expect(anomalyAlerts.length).toBe(0);
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// 3. SALE STATE TRANSITIONS (ingest.js lines 96-128)
// ═══════════════════════════════════════════════════════════════════════════════

describe("Ingest — Sale state transitions", () => {
  let handler;

  beforeEach(() => {
    resetAll();
    jest.resetModules();
    jest.mock("../api/_kv", () => ({ kv: mockKv }));
    jest.mock("../api/_sheets", () => ({ appendRow: mockAppend }));
    handler = require("../api/ingest.js");
  });

  test("tracks consecutive sale days", async () => {
    // Day 1 — sale starts
    mockKvStore["wiper:sale_state"] = {
      comp_1: { start_date: "2026-04-05", consecutive_days: 2, last_intensity: 30, market: "AU" },
    };
    mockKvStore["wiper:latest"] = {
      sites: [{ id: "comp_1", is_on_sale: true, promotion_intensity: 30 }],
    };
    mockKvStore["wiper:history_keys"] = [];
    mockKvStore["wiper:alerts"] = [];

    const req = createReq({
      body: {
        date: "2026-04-07", day_of_week: 2, is_weekend: false,
        sites: [{ id: "comp_1", name: "Test", market: "AU", is_on_sale: true, promotion_intensity: 35, promos: [] }],
      },
    });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(200);
    // Sale state should show consecutive_days = 3
    const updatedState = mockKvStore["wiper:sale_state"];
    expect(updatedState.comp_1.consecutive_days).toBe(3);
  });

  test("records sale end with duration", async () => {
    mockKvStore["wiper:sale_state"] = {
      comp_1: { start_date: "2026-04-01", consecutive_days: 5, last_intensity: 40, market: "AU" },
    };
    mockKvStore["wiper:latest"] = {
      sites: [{ id: "comp_1", is_on_sale: true }],
    };
    mockKvStore["wiper:history_keys"] = [];
    mockKvStore["wiper:alerts"] = [];

    const req = createReq({
      body: {
        date: "2026-04-07", day_of_week: 2, is_weekend: false,
        sites: [{ id: "comp_1", name: "Test", market: "AU", is_on_sale: false, promotion_intensity: 0, promos: [] }],
      },
    });
    const res = createRes();
    await handler(req, res);

    // Should generate sale_ended alert with duration
    const endAlerts = res._body.alerts.filter(a => a.type === "sale_ended");
    expect(endAlerts.length).toBe(1);
    expect(endAlerts[0].message).toContain("5 days");
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// 4. PRICE TRACKER — edge cases
// ═══════════════════════════════════════════════════════════════════════════════

describe("Price tracker — edge cases", () => {
  let handler;

  beforeEach(() => {
    resetAll();
    jest.resetModules();
    jest.mock("../api/_kv", () => ({ kv: mockKv }));
    jest.mock("../api/_sheets", () => ({ appendRow: mockAppend }));
    handler = require("../api/price-tracker.js");
  });

  test("rejects non-GET methods", async () => {
    const req = createReq({ method: "POST", query: { brand_id: "x" } });
    const res = createRes();
    await handler(req, res);
    expect(res._status).toBe(405);
  });

  test("returns 400 when brand_id is missing", async () => {
    const req = createReq({ method: "GET", query: {} });
    const res = createRes();
    await handler(req, res);
    expect(res._status).toBe(400);
  });

  test("handles zero BAU price without division by zero", async () => {
    mockKvStore["brands:brand_1"] = { id: "brand_1", name: "Test", status: "active", competitors: [] };
    mockKvStore["prices:brand_1"] = [
      { date: "2026-04-01", competitor_id: "c1", price: 0, period_type: "bau" },
      { date: "2026-04-05", competitor_id: "c1", price: 10, period_type: "sale" },
    ];

    const req = createReq({ method: "GET", query: { brand_id: "brand_1" } });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(200);
    // Should not be Infinity or NaN
    const discount = res._body.summary.sale_discount_pct;
    expect(Number.isFinite(discount) || discount === null).toBe(true);
  });

  test("returns correct summary with only BAU data (no sales)", async () => {
    mockKvStore["brands:brand_1"] = { id: "brand_1", name: "Test", status: "active", competitors: [] };
    mockKvStore["prices:brand_1"] = [
      { date: "2026-04-01", competitor_id: "c1", price: 30, period_type: "bau" },
      { date: "2026-04-02", competitor_id: "c1", price: 32, period_type: "bau" },
    ];

    const req = createReq({ method: "GET", query: { brand_id: "brand_1" } });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(200);
    expect(res._body.summary.bau_avg_price).toBeCloseTo(31.0);
    expect(res._body.summary.sale_avg_price).toBeNull();
    expect(res._body.summary.sale_discount_pct).toBeNull();
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// 5. BRANDS — competitor defaults
// ═══════════════════════════════════════════════════════════════════════════════

describe("Brands — competitor defaults", () => {
  let handler;

  beforeEach(() => {
    resetAll();
    jest.resetModules();
    jest.mock("../api/_kv", () => ({ kv: mockKv }));
    jest.mock("../api/_sheets", () => ({ appendRow: mockAppend }));
    handler = require("../api/brands.js");
  });

  test("assigns default type=specialist when not provided", async () => {
    const req = createReq({
      body: {
        name: "Defaults Test", market: "AU", website: "https://test.com",
        product_category: "wipers", reference_product: "Test",
        competitors: [{ name: "Bare Minimum", url: "https://bare.com" }],
      },
    });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(201);
    expect(res._body.brand.competitors[0].type).toBe("specialist");
  });

  test("assigns default renderer=http when not provided", async () => {
    const req = createReq({
      body: {
        name: "Renderer Test", market: "NZ", website: "https://test.co.nz",
        product_category: "wipers", reference_product: "Test",
        competitors: [{ name: "Basic Co", url: "https://basic.co.nz", type: "retailer" }],
      },
    });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(201);
    expect(res._body.brand.competitors[0].renderer).toBe("http");
  });

  test("auto-generates canary from competitor name", async () => {
    const req = createReq({
      body: {
        name: "Canary Test", market: "AU", website: "https://test.com",
        product_category: "wipers", reference_product: "Test",
        competitors: [{ name: "Super Cheap Auto", url: "https://sca.com.au", type: "retailer" }],
      },
    });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(201);
    expect(res._body.brand.competitors[0].canary).toBe("super");
  });

  test("auto-generates competitor ID from name and market", async () => {
    const req = createReq({
      body: {
        name: "ID Test", market: "AU", website: "https://test.com",
        product_category: "wipers", reference_product: "Test",
        competitors: [{ name: "Repco Australia", url: "https://repco.com.au", type: "retailer" }],
      },
    });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(201);
    expect(res._body.brand.competitors[0].id).toBe("repco_australia_au");
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// 6. INGEST — Sheets price logging + period tagging
// ═══════════════════════════════════════════════════════════════════════════════

describe("Ingest — price history + period tagging", () => {
  let handler;

  beforeEach(() => {
    resetAll();
    jest.resetModules();
    jest.mock("../api/_kv", () => ({ kv: mockKv }));
    jest.mock("../api/_sheets", () => ({ appendRow: mockAppend }));
    handler = require("../api/ingest.js");
  });

  test("stores price history keyed by brand_id", async () => {
    mockKvStore["wiper:history_keys"] = [];
    mockKvStore["wiper:alerts"] = [];
    mockKvStore["periods:brand_x"] = [
      { id: "p1", brand_id: "brand_x", type: "sale", start_date: "2026-04-01", end_date: "2026-04-30" },
    ];

    const req = createReq({
      body: {
        date: "2026-04-07", brand_id: "brand_x", day_of_week: 2, is_weekend: false,
        sites: [{
          id: "c1", name: "Comp", market: "AU", is_on_sale: true,
          promotion_intensity: 25, promos: [],
          territory_price: { price: 19.99 },
        }],
      },
    });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(200);
    // Should have stored price record in KV
    const prices = mockKvStore["prices:brand_x"];
    expect(prices).toBeDefined();
    expect(prices.length).toBe(1);
    expect(prices[0].price).toBe(19.99);
    expect(prices[0].period_type).toBe("sale");
  });

  test("defaults to BAU when no matching period", async () => {
    mockKvStore["wiper:history_keys"] = [];
    mockKvStore["wiper:alerts"] = [];
    // No periods defined

    const req = createReq({
      body: {
        date: "2026-04-07", brand_id: "brand_y", day_of_week: 2, is_weekend: false,
        sites: [{
          id: "c1", name: "Comp", market: "AU", is_on_sale: false,
          promotion_intensity: 0, promos: [],
          territory_price: { price: 34.99 },
        }],
      },
    });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(200);
    const prices = mockKvStore["prices:brand_y"];
    expect(prices[0].period_type).toBe("bau");
  });

  test("skips price logging when no territory_price", async () => {
    mockKvStore["wiper:history_keys"] = [];
    mockKvStore["wiper:alerts"] = [];

    const req = createReq({
      body: {
        date: "2026-04-07", brand_id: "brand_z", day_of_week: 2, is_weekend: false,
        sites: [{
          id: "c1", name: "Comp", market: "AU", is_on_sale: false,
          promotion_intensity: 0, promos: [],
          // no territory_price
        }],
      },
    });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(200);
    // Should NOT have created price records
    expect(mockKvStore["prices:brand_z"]).toBeUndefined();
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// 7. INGEST — MAX_ALERTS limit
// ═══════════════════════════════════════════════════════════════════════════════

describe("Ingest — alert limits", () => {
  let handler;

  beforeEach(() => {
    resetAll();
    jest.resetModules();
    jest.mock("../api/_kv", () => ({ kv: mockKv }));
    jest.mock("../api/_sheets", () => ({ appendRow: mockAppend }));
    handler = require("../api/ingest.js");
  });

  test("caps stored alerts at MAX_ALERTS (200)", async () => {
    // Pre-fill 199 existing alerts
    mockKvStore["wiper:alerts"] = Array.from({ length: 199 }, (_, i) => ({
      type: "old", ts: "2026-01-01", brand: `Brand ${i}`, message: `Alert ${i}`,
    }));
    mockKvStore["wiper:history_keys"] = [];
    mockKvStore["wiper:latest"] = { sites: [] };

    // Ingest with 5 new sale_started alerts
    const sites = Array.from({ length: 5 }, (_, i) => ({
      id: `comp_${i}`, name: `Comp ${i}`, market: "AU",
      is_on_sale: true, promotion_intensity: 20,
      promos: [{ raw_text: "Sale!" }],
    }));

    const req = createReq({
      body: { date: "2026-04-07", day_of_week: 2, is_weekend: false, sites },
    });
    const res = createRes();
    await handler(req, res);

    expect(res._status).toBe(200);
    // Total should be capped at 200
    const storedAlerts = mockKvStore["wiper:alerts"];
    expect(storedAlerts.length).toBeLessThanOrEqual(200);
    // New alerts should be at the front
    expect(storedAlerts[0].type).toBe("sale_started");
  });
});
