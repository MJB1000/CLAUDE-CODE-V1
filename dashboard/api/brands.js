// api/brands.js
// Brand management — create and list tracked brands with competitors
// POST /api/brands → create brand
// GET  /api/brands → list brands

const { kv } = require("./_kv");
const { appendRow } = require("./_sheets");
const crypto = require("crypto");

const SECRET = process.env.WIPER_INTEL_SECRET || "changeme";

const REQUIRED_FIELDS = ["name", "market", "website", "product_category", "reference_product"];

function generateId(prefix) {
  return `${prefix}_${crypto.randomBytes(6).toString("hex")}`;
}

function slugify(name) {
  return name.toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/(^_|_$)/g, "");
}

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, X-API-Key");
  if (req.method === "OPTIONS") return res.status(200).end();

  // ── GET — list brands ───────────────────────────────────────────────────────
  if (req.method === "GET") {
    const index = (await kv.get("brands:index").catch(() => null)) || [];
    const brands = [];
    for (const id of index) {
      const brand = await kv.get(`brands:${id}`).catch(() => null);
      if (brand) brands.push(brand);
    }
    return res.status(200).json({ brands });
  }

  // ── POST — create brand ─────────────────────────────────────────────────────
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  const apiKey = req.headers["x-api-key"] || req.query.key;
  if (apiKey !== SECRET) return res.status(401).json({ error: "Unauthorized" });

  let body;
  try { body = typeof req.body === "string" ? JSON.parse(req.body) : req.body; }
  catch { return res.status(400).json({ error: "Invalid JSON" }); }

  // Validate required fields
  for (const field of REQUIRED_FIELDS) {
    if (!body[field]) {
      return res.status(400).json({ error: `Missing required field: ${field}` });
    }
  }

  // Validate competitors
  const competitors = body.competitors || [];
  if (!Array.isArray(competitors) || competitors.length === 0) {
    return res.status(400).json({ error: "At least one competitor is required" });
  }

  for (const comp of competitors) {
    if (!comp.url) {
      return res.status(400).json({ error: `Competitor "${comp.name || "unknown"}" is missing url` });
    }
  }

  // Build brand object
  const brandId = generateId("brand");
  const now = new Date().toISOString();

  const brand = {
    id: brandId,
    name: body.name,
    market: body.market,
    website: body.website,
    product_category: body.product_category,
    reference_product: body.reference_product,
    status: "active",
    created_at: now,
    updated_at: now,
    competitors: competitors.map(c => ({
      id: c.id || `${slugify(c.name)}_${body.market.toLowerCase()}`,
      name: c.name,
      url: c.url,
      product_url: c.product_url || null,
      type: c.type || "specialist",
      canary: c.canary || c.name.toLowerCase().split(" ")[0],
      renderer: c.renderer || "http",
    })),
  };

  // Store brand + update index
  const index = (await kv.get("brands:index").catch(() => null)) || [];
  await Promise.all([
    kv.set(`brands:${brandId}`, brand),
    kv.set("brands:index", [...index, brandId]),
  ]);

  // Log to Google Sheets
  try {
    await appendRow("Brands", [
      now, brandId, brand.name, brand.market, brand.website,
      brand.product_category, brand.reference_product,
      brand.competitors.length, brand.competitors.map(c => c.name).join(", "),
    ]);
  } catch { /* sheets logging is best-effort */ }

  return res.status(201).json({ ok: true, brand });
};
