// api/openapi.js
// Serves the OpenAPI 3.0 specification for the Wiper Intel API
// GET /api/openapi → JSON spec

const spec = {
  openapi: "3.0.3",
  info: {
    title: "Wiper Intel API",
    version: "2.0.0",
    description: "Competitive intelligence API for tracking wiper blade competitor pricing, promotions, and sales across AU and NZ markets.",
    contact: { email: "matthew@wipertech.com.au" },
  },
  servers: [
    { url: "https://dashboard-theta-five-15.vercel.app", description: "Production" },
    { url: "http://localhost:3000", description: "Local development" },
  ],
  paths: {
    "/api/data": {
      get: {
        summary: "Get latest dashboard data",
        description: "Returns latest scrape data, alerts, shopping data, and sale state. Optionally includes 30-day history.",
        parameters: [
          { name: "history", in: "query", schema: { type: "string", enum: ["0", "1"] }, description: "Set to '1' to include 30-day history" },
        ],
        responses: {
          200: { description: "Dashboard data", content: { "application/json": { schema: { type: "object", properties: {
            latest: { type: "object", description: "Most recent scrape snapshot" },
            alerts: { type: "array", items: { "$ref": "#/components/schemas/Alert" } },
            history: { type: "array", description: "Historical snapshots (if requested)" },
            shopping: { type: "object", description: "Google Shopping data" },
            sale_state: { type: "object", description: "Per-brand sale duration state" },
          }}}}},
        },
        tags: ["Data"],
      },
    },
    "/api/ingest": {
      post: {
        summary: "Ingest scraper data",
        description: "Accepts scraped brand data, runs anomaly detection, sale tracking, and generates alerts.",
        security: [{ apiKey: [] }],
        requestBody: { required: true, content: { "application/json": { schema: { "$ref": "#/components/schemas/IngestPayload" } } } },
        responses: {
          200: { description: "Data processed", content: { "application/json": { schema: { type: "object", properties: {
            ok: { type: "boolean" }, date: { type: "string" },
            brands_processed: { type: "integer" }, new_alerts: { type: "integer" },
            alerts: { type: "array", items: { "$ref": "#/components/schemas/Alert" } },
          }}}}},
          401: { description: "Unauthorized" },
          429: { description: "Rate limit exceeded" },
        },
        tags: ["Ingest"],
      },
    },
    "/api/health": {
      get: {
        summary: "Health check",
        description: "Returns system health: KV connectivity, data freshness, brand/alert counts.",
        responses: {
          200: { description: "Healthy or degraded", content: { "application/json": { schema: { type: "object", properties: {
            status: { type: "string", enum: ["ok", "degraded", "no_data"] },
            kv: { type: "string" }, brands_tracked: { type: "integer" },
            hours_since_scrape: { type: "integer" },
          }}}}},
          503: { description: "Service unavailable" },
        },
        tags: ["Monitoring"],
      },
    },
    "/api/export": {
      get: {
        summary: "Export data",
        description: "Download current brand data as CSV or JSON.",
        security: [{ apiKey: [] }],
        parameters: [
          { name: "format", in: "query", schema: { type: "string", enum: ["csv", "json"], default: "csv" } },
        ],
        responses: {
          200: { description: "Exported file" },
          401: { description: "Unauthorized" },
        },
        tags: ["Data"],
      },
    },
    "/api/summarize": {
      post: {
        summary: "AI promo summary",
        description: "Uses Claude API to generate a one-line summary of competitor promotion text.",
        security: [{ apiKey: [] }],
        requestBody: { required: true, content: { "application/json": { schema: { type: "object", required: ["text"], properties: {
          text: { type: "string", description: "Raw promotion text" },
          brand: { type: "string" }, market: { type: "string", enum: ["AU", "NZ"] },
        }}}}},
        responses: {
          200: { description: "Summary generated", content: { "application/json": { schema: { type: "object", properties: {
            ok: { type: "boolean" }, summary: { type: "string" },
          }}}}},
          503: { description: "ANTHROPIC_API_KEY not configured" },
        },
        tags: ["AI"],
      },
    },
    "/api/wipertech-own": {
      get: {
        summary: "Get Wipertech position",
        description: "Returns Wipertech's own active promotion state.",
        responses: { 200: { description: "Own data" } },
        tags: ["Data"],
      },
      post: {
        summary: "Update Wipertech position",
        description: "Set Wipertech's own promotion state (active/inactive, promo details).",
        security: [{ apiKey: [] }],
        requestBody: { required: true, content: { "application/json": { schema: { type: "object", properties: {
          market: { type: "string", enum: ["AU", "NZ", "both"] },
          active: { type: "boolean" },
          promo: { type: "object", properties: {
            raw_text: { type: "string" }, discount_pct: { type: "number" },
            promo_code: { type: "string" }, dollar_off: { type: "number" },
          }},
          note: { type: "string" },
        }}}}},
        responses: { 200: { description: "Updated" }, 401: { description: "Unauthorized" } },
        tags: ["Data"],
      },
    },
    "/api/weekly-digest": {
      get: {
        summary: "Weekly digest",
        description: "Generates and sends the weekly intelligence email digest. Triggered by Vercel Cron or manually with API key.",
        security: [{ apiKey: [] }],
        responses: { 200: { description: "Digest sent or HTML returned" } },
        tags: ["Digest"],
      },
    },
  },
  components: {
    securitySchemes: {
      apiKey: { type: "apiKey", in: "header", name: "X-API-Key", description: "WIPER_INTEL_SECRET" },
    },
    schemas: {
      Alert: { type: "object", properties: {
        type: { type: "string", enum: ["sale_started", "sale_ended", "price_change", "new_promo_code", "anomaly", "canary_fail", "price_found"] },
        ts: { type: "string", format: "date-time" },
        brand: { type: "string" }, market: { type: "string" },
        message: { type: "string" }, detail: { type: "string" },
      }},
      IngestPayload: { type: "object", required: ["date", "sites"], properties: {
        date: { type: "string", format: "date", example: "2025-03-21" },
        day_of_week: { type: "integer", minimum: 0, maximum: 6 },
        is_weekend: { type: "boolean" },
        sites: { type: "array", items: { "$ref": "#/components/schemas/Site" } },
        google_shopping: { type: "object" },
      }},
      Site: { type: "object", properties: {
        id: { type: "string" }, name: { type: "string" },
        market: { type: "string", enum: ["AU", "NZ"] },
        type: { type: "string", enum: ["specialist", "retailer", "oem"] },
        url: { type: "string", format: "uri" },
        http_status: { type: "integer" },
        canary_pass: { type: "boolean" },
        is_on_sale: { type: "boolean" },
        promotion_intensity: { type: "integer", minimum: 0, maximum: 100 },
        promos: { type: "array", items: { type: "object" } },
        territory_price: { type: "object", properties: {
          price: { type: "number" }, url: { type: "string" },
        }},
      }},
    },
  },
};

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Cache-Control", "public, max-age=3600");
  return res.status(200).json(spec);
};
