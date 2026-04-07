// api/price-tracker.js
// Price history aggregation for brands — sale vs BAU analysis
// GET /api/price-tracker?brand_id=xxx → price history + summary
// GET /api/price-tracker?brand_id=xxx&period=sale → filtered by period type

const { kv } = require("./_kv");

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "GET") return res.status(405).json({ error: "GET only" });

  const { brand_id, period } = req.query;
  if (!brand_id) return res.status(400).json({ error: "Missing brand_id" });

  const brand = await kv.get(`brands:${brand_id}`).catch(() => null);
  if (!brand) return res.status(404).json({ error: "Brand not found" });

  let prices = (await kv.get(`prices:${brand_id}`).catch(() => null)) || [];

  // Filter by period type if requested
  if (period) {
    prices = prices.filter(p => p.period_type === period);
  }

  // Calculate summary
  const bauPrices = prices.filter(p => p.period_type === "bau").map(p => p.price);
  const salePrices = prices.filter(p => p.period_type === "sale").map(p => p.price);

  const avg = arr => arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : null;
  const bauAvg = avg(bauPrices);
  const saleAvg = avg(salePrices);

  const summary = {
    bau_avg_price: bauAvg,
    sale_avg_price: saleAvg,
    sale_discount_pct: bauAvg && saleAvg ? ((bauAvg - saleAvg) / bauAvg) * 100 : null,
    total_records: prices.length,
    bau_records: bauPrices.length,
    sale_records: salePrices.length,
  };

  return res.status(200).json({ brand, prices, summary });
};
