// api/periods.js
// Sale/BAU period management — define time windows for price tracking
// POST /api/periods → create period
// GET  /api/periods?brand_id=xxx → list periods (+ active_period for date)

const { kv } = require("./_kv");
const crypto = require("crypto");

const SECRET = process.env.WIPER_INTEL_SECRET || "changeme";
const VALID_TYPES = ["sale", "bau"];

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, X-API-Key");
  if (req.method === "OPTIONS") return res.status(200).end();

  // ── GET — list periods for a brand ──────────────────────────────────────────
  if (req.method === "GET") {
    const { brand_id, date } = req.query;
    if (!brand_id) return res.status(400).json({ error: "Missing brand_id" });

    const periods = (await kv.get(`periods:${brand_id}`).catch(() => null)) || [];

    let active_period = null;
    if (date) {
      active_period = periods.find(p => date >= p.start_date && date <= p.end_date) || null;
    }

    return res.status(200).json({ periods, active_period });
  }

  // ── POST — create period ────────────────────────────────────────────────────
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  const apiKey = req.headers["x-api-key"] || req.query.key;
  if (apiKey !== SECRET) return res.status(401).json({ error: "Unauthorized" });

  let body;
  try { body = typeof req.body === "string" ? JSON.parse(req.body) : req.body; }
  catch { return res.status(400).json({ error: "Invalid JSON" }); }

  const { brand_id, label, type, start_date, end_date } = body;

  if (!brand_id || !label || !type || !start_date || !end_date) {
    return res.status(400).json({ error: "Missing required fields: brand_id, label, type, start_date, end_date" });
  }

  if (!VALID_TYPES.includes(type)) {
    return res.status(400).json({ error: `Invalid type: must be one of ${VALID_TYPES.join(", ")}` });
  }

  if (end_date < start_date) {
    return res.status(400).json({ error: "end_date must be after start_date" });
  }

  const period = {
    id: `period_${crypto.randomBytes(6).toString("hex")}`,
    brand_id,
    label,
    type,
    start_date,
    end_date,
    created_at: new Date().toISOString(),
  };

  const existing = (await kv.get(`periods:${brand_id}`).catch(() => null)) || [];
  await kv.set(`periods:${brand_id}`, [...existing, period]);

  return res.status(201).json({ ok: true, period });
};
