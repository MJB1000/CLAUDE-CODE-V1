// api/data.js  v2
// Serves AU+NZ data, Google Shopping, sale duration, anomaly flags, alerts

const { kv } = require("@vercel/kv");

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Cache-Control", "no-store");

  try {
    const [latest, alerts, shopping, saleState] = await Promise.all([
      kv.get("wiper:latest").catch(() => null),
      kv.get("wiper:alerts").catch(() => []),
      kv.get("wiper:shopping:latest").catch(() => null),
      kv.get("wiper:sale_state").catch(() => {}),
    ]);

    // Enrich sites with sale duration from state
    if (latest?.sites && saleState) {
      latest.sites = latest.sites.map(s => ({
        ...s,
        sale_duration_days: saleState[s.id]?.consecutive_days || s.sale_duration_days || 0,
        sale_start_date:    saleState[s.id]?.start_date || s.sale_start_date || null,
      }));
    }

    // Optional: pull history for charting
    let history = [];
    if (req.query.history === "1") {
      const histKeys = (await kv.get("wiper:history_keys").catch(() => [])) || [];
      const last30   = histKeys.slice(-30);
      const snaps    = await Promise.all(
        last30.map(k => kv.get(`wiper:history:${k}`).catch(() => null))
      );
      history = snaps.filter(Boolean);
    }

    return res.status(200).json({
      latest, alerts, history, shopping,
      sale_state: saleState,
    });
  } catch (err) {
    return res.status(500).json({ error: "KV error", detail: err.message });
  }
};
