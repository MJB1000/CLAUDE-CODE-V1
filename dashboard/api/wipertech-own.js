// api/wipertech-own.js
// Accepts POST of Wipertech's own active promotion schedule
// Call this whenever you start/end a Klaviyo campaign or site promo
//
// POST body: {
//   "secret": "your_secret",
//   "market": "AU" | "NZ" | "both",
//   "active": true | false,
//   "promo": {
//     "raw_text": "20% off sitewide — use SPRING20",
//     "discount_pct": 20,
//     "promo_code": "SPRING20",
//     "deal_type": null,
//     "dollar_off": null
//   },
//   "note": "Spring sale 2025"
// }

const { kv } = require("@vercel/kv");

const SECRET = process.env.WIPER_INTEL_SECRET || "changeme";

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, X-API-Key");
  if (req.method === "OPTIONS") return res.status(200).end();

  // GET — read current own-data state
  if (req.method === "GET") {
    const own = await kv.get("wiper:own_data").catch(() => null);
    return res.status(200).json({ own_data: own });
  }

  if (req.method !== "POST") return res.status(405).end();

  const apiKey = req.headers["x-api-key"] || req.query.key;
  if (apiKey !== SECRET) return res.status(401).json({ error: "Unauthorized" });

  let body;
  try { body = typeof req.body === "string" ? JSON.parse(req.body) : req.body; }
  catch { return res.status(400).json({ error: "Invalid JSON" }); }

  const { market, active, promo, note } = body;

  const ownData = {
    updated_at: new Date().toISOString(),
    market: market || "AU",
    active: !!active,
    promo: active ? (promo || null) : null,
    promotion_intensity: active && promo?.discount_pct ? Math.min(promo.discount_pct + 15, 100) : 0,
    note: note || "",
  };

  await kv.set("wiper:own_data", ownData);

  return res.status(200).json({ ok: true, own_data: ownData });
};
