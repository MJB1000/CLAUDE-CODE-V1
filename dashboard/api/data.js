// api/data.js  v2
// Serves AU+NZ data, Google Shopping, sale duration, anomaly flags, alerts

const { kv } = require("./_kv");

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Cache-Control", "no-store");

  try {
    const [latest, alerts, shopping, saleState] = await Promise.all([
      kv.get("intel:latest").catch(() => null),
      kv.get("intel:alerts").catch(() => []),
      kv.get("intel:shopping:latest").catch(() => null),
      kv.get("intel:sale_state").catch(() => {}),
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
      const histKeys = (await kv.get("intel:history_keys").catch(() => [])) || [];
      const last30   = histKeys.slice(-30);
      const snaps    = await Promise.all(
        last30.map(k => kv.get(`intel:history:${k}`).catch(() => null))
      );
      history = snaps.filter(Boolean);
    }

    const landscape = await kv.get("intel:landscape_summary").catch(() => null);
    const ownData   = await kv.get("intel:own_data").catch(() => null);

    return res.status(200).json({
      latest, alerts, history, shopping,
      sale_state: saleState,
      landscape_summary: landscape,
      own_data: ownData,
    });
  } catch (err) {
    return res.status(500).json({ error: "KV error", detail: err.message });
  }
};
