// api/export.js
// Export current dashboard data as CSV or JSON
// GET /api/export?format=csv  (default)
// GET /api/export?format=json

const { kv } = require("@vercel/kv");

const SECRET = process.env.WIPER_INTEL_SECRET || "changeme";

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");

  // Require auth for exports
  const apiKey = req.headers["x-api-key"] || req.query.key;
  if (apiKey !== SECRET) return res.status(401).json({ error: "Unauthorized" });

  if (req.method !== "GET") return res.status(405).json({ error: "GET only" });

  const format = (req.query.format || "csv").toLowerCase();
  if (!["csv", "json"].includes(format)) {
    return res.status(400).json({ error: "format must be 'csv' or 'json'" });
  }

  try {
    const [latest, alerts, shopping, saleState] = await Promise.all([
      kv.get("wiper:latest").catch(() => null),
      kv.get("wiper:alerts").catch(() => []),
      kv.get("wiper:shopping:latest").catch(() => null),
      kv.get("wiper:sale_state").catch(() => {}),
    ]);

    const sites = latest?.sites || [];
    const date = latest?.date || new Date().toISOString().slice(0, 10);

    if (format === "json") {
      res.setHeader("Content-Type", "application/json");
      res.setHeader("Content-Disposition", `attachment; filename="wiper-intel-${date}.json"`);
      return res.status(200).json({
        exported_at: new Date().toISOString(),
        date,
        sites,
        alerts: alerts || [],
        shopping: shopping || {},
        sale_state: saleState || {},
      });
    }

    // CSV format
    const headers = [
      "id", "name", "market", "type", "url",
      "is_on_sale", "promotion_intensity", "sale_duration_days",
      "sale_start_date", "territory_price", "territory_price_url",
      "canary_pass", "http_status", "promo_count",
      "top_promo_text", "top_promo_code", "top_discount_pct",
      "anomaly", "anomaly_zscore", "claude_summary",
    ];

    const rows = sites.map(s => {
      const promo = (s.promos || [])[0];
      const saleDur = (saleState || {})[s.id]?.consecutive_days || s.sale_duration_days || 0;
      return [
        s.id, s.name, s.market || "AU", s.type || "",
        s.url || "",
        s.is_on_sale ? "yes" : "no",
        s.promotion_intensity || 0,
        saleDur,
        s.sale_start_date || "",
        s.territory_price?.price || "",
        s.territory_price?.url || "",
        s.canary_pass === false ? "FAIL" : "ok",
        s.http_status || "",
        (s.promos || []).length,
        (promo?.raw_text || "").replace(/"/g, '""').substring(0, 100),
        promo?.promo_code || "",
        promo?.discount_pct || "",
        s.anomaly ? "yes" : "no",
        s.anomaly_zscore || "",
        (s.claude_summary || "").replace(/"/g, '""'),
      ];
    });

    const csvLines = [
      headers.join(","),
      ...rows.map(r => r.map(v => `"${v}"`).join(",")),
    ];

    res.setHeader("Content-Type", "text/csv; charset=utf-8");
    res.setHeader("Content-Disposition", `attachment; filename="wiper-intel-${date}.csv"`);
    return res.status(200).send(csvLines.join("\n"));

  } catch (err) {
    return res.status(500).json({ error: "Export failed", detail: err.message });
  }
};
