// api/health.js
// Health check endpoint for monitoring and uptime checks
// GET /api/health → { status: "ok", ... }

const { kv } = require("./_kv");

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Cache-Control", "no-store");

  const checks = {
    status: "ok",
    timestamp: new Date().toISOString(),
    kv: "unknown",
    last_scrape: null,
    brands_tracked: 0,
    alerts_count: 0,
  };

  try {
    const latest = await kv.get("intel:latest").catch(() => null);
    checks.kv = "connected";

    if (latest) {
      checks.last_scrape = latest.scraped_at || latest.date;
      checks.brands_tracked = (latest.sites || []).length;
      checks.scrape_date = latest.date;

      // Check if data is stale (>36 hours old)
      const lastScrapeTime = new Date(latest.scraped_at || latest.date).getTime();
      const hoursSince = (Date.now() - lastScrapeTime) / (1000 * 60 * 60);
      checks.hours_since_scrape = Math.round(hoursSince);
      if (hoursSince > 36) {
        checks.status = "degraded";
        checks.warning = "Data may be stale — last scrape was " + Math.round(hoursSince) + "h ago";
      }
    } else {
      checks.status = "no_data";
      checks.warning = "No scrape data found — run the scraper first";
    }

    const alerts = await kv.get("intel:alerts").catch(() => []);
    checks.alerts_count = (alerts || []).length;

  } catch (err) {
    checks.status = "error";
    checks.kv = "disconnected";
    checks.error = err.message;
    return res.status(503).json(checks);
  }

  // Uptime monitoring: include ping-friendly response time
  checks.response_time_ms = Date.now() - Date.parse(checks.timestamp);
  checks.version = "2.0.0";
  checks.endpoints = {
    data: "/api/data",
    ingest: "/api/ingest",
    export: "/api/export",
    health: "/api/health",
    openapi: "/api/openapi",
    summarize: "/api/summarize",
    digest: "/api/weekly-digest",
    own: "/api/wipertech-own",
  };

  const statusCode = checks.status === "ok" ? 200 : checks.status === "degraded" ? 200 : 503;
  return res.status(statusCode).json(checks);
};
