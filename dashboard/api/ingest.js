// api/ingest.js  v2
// Handles AU + NZ data, anomaly detection, sale duration tracking,
// day-of-week normalisation, canary failure alerts, Wipertech own data

const { kv } = require("@vercel/kv");

const SECRET      = process.env.WIPER_INTEL_SECRET || "changeme";
const MAX_ALERTS  = 200;
const MAX_HISTORY = 90;
const RATE_LIMIT_MAX     = parseInt(process.env.RATE_LIMIT_MAX || "10");
const RATE_LIMIT_WINDOW  = parseInt(process.env.RATE_LIMIT_WINDOW || "60"); // seconds

async function checkRateLimit(req) {
  const ip = req.headers["x-forwarded-for"]?.split(",")[0]?.trim() || "unknown";
  const key = `ratelimit:ingest:${ip}`;
  try {
    const count = await kv.incr(key);
    if (count === 1) await kv.expire(key, RATE_LIMIT_WINDOW);
    return { allowed: count <= RATE_LIMIT_MAX, count, limit: RATE_LIMIT_MAX };
  } catch {
    return { allowed: true, count: 0, limit: RATE_LIMIT_MAX };
  }
}

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, X-API-Key");
  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST")    return res.status(405).json({ error: "POST only" });

  const apiKey = req.headers["x-api-key"] || req.query.key;
  if (apiKey !== SECRET) return res.status(401).json({ error: "Unauthorized" });

  // Rate limiting
  const rl = await checkRateLimit(req);
  res.setHeader("X-RateLimit-Limit", rl.limit);
  res.setHeader("X-RateLimit-Remaining", Math.max(0, rl.limit - rl.count));
  if (!rl.allowed) {
    return res.status(429).json({ error: "Rate limit exceeded", retry_after: RATE_LIMIT_WINDOW });
  }

  let body;
  try { body = typeof req.body === "string" ? JSON.parse(req.body) : req.body; }
  catch { return res.status(400).json({ error: "Invalid JSON" }); }

  const { date, sites, google_shopping, day_of_week, is_weekend } = body;
  if (!date || !Array.isArray(sites))
    return res.status(400).json({ error: "Missing date or sites array" });

  const now = new Date().toISOString();

  // ── Load state ─────────────────────────────────────────────────────────────
  const [prevSnapshot, saleState, historyKeys, existingAlerts] = await Promise.all([
    kv.get("wiper:latest").catch(() => null),
    kv.get("wiper:sale_state").catch(() => ({})),
    kv.get("wiper:history_keys").catch(() => []),
    kv.get("wiper:alerts").catch(() => []),
  ]);

  const prevMap   = Object.fromEntries(((prevSnapshot || {}).sites || []).map(s => [s.id, s]));
  const saleMap   = saleState || {};  // {site_id: {start_date, consecutive_days, last_intensity}}
  const newAlerts = [];

  // ── Load rolling history for anomaly detection ────────────────────────────
  const histKeys = historyKeys.slice(-30);
  const histSnapshots = histKeys.length > 0
    ? await Promise.all(histKeys.map(k => kv.get(`wiper:history:${k}`).catch(() => null)))
    : [];
  const validHistory = histSnapshots.filter(Boolean);

  // Build per-brand intensity history for anomaly detection
  const brandHistoryMap = {};
  for (const snap of validHistory) {
    const dow = snap.day_of_week ?? new Date(snap.date).getDay();
    for (const site of (snap.sites || [])) {
      if (!brandHistoryMap[site.id]) brandHistoryMap[site.id] = { all: [], byDow: {} };
      brandHistoryMap[site.id].all.push(site.promotion_intensity || 0);
      if (!brandHistoryMap[site.id].byDow[dow]) brandHistoryMap[site.id].byDow[dow] = [];
      brandHistoryMap[site.id].byDow[dow].push(site.promotion_intensity || 0);
    }
  }

  function mean(arr)   { return arr.length ? arr.reduce((a, x) => a + x, 0) / arr.length : 0; }
  function stddev(arr) {
    if (arr.length < 2) return 0;
    const m = mean(arr);
    return Math.sqrt(arr.reduce((a, x) => a + (x - m) ** 2, 0) / arr.length);
  }

  // ── Process each site ─────────────────────────────────────────────────────
  const updatedSaleMap = { ...saleMap };

  for (const site of sites) {
    const prev     = prevMap[site.id];
    const isOnSale = site.is_on_sale || false;
    const wasOnSale = prev?.is_on_sale || false;
    const intensity = site.promotion_intensity || 0;
    const market   = site.market || "AU";

    // ── Sale duration tracking ──────────────────────────────────────────────
    if (isOnSale) {
      if (!updatedSaleMap[site.id] || !wasOnSale) {
        // Sale just started
        updatedSaleMap[site.id] = {
          start_date: date, consecutive_days: 1,
          last_intensity: intensity, market,
        };
      } else {
        // Sale continuing
        updatedSaleMap[site.id].consecutive_days = (updatedSaleMap[site.id].consecutive_days || 0) + 1;
        updatedSaleMap[site.id].last_intensity   = intensity;
      }
      // Annotate site with duration
      site.sale_duration_days = updatedSaleMap[site.id].consecutive_days;
      site.sale_start_date    = updatedSaleMap[site.id].start_date;
    } else {
      if (updatedSaleMap[site.id]) {
        // Record ended sale for recurrence analysis
        updatedSaleMap[site.id] = {
          ...updatedSaleMap[site.id],
          end_date: date, active: false,
        };
      }
      site.sale_duration_days = 0;
    }

    // ── Promo alerts ────────────────────────────────────────────────────────
    const currCodes = new Set((site.promos || []).map(p => p.promo_code).filter(Boolean));
    const prevCodes = new Set((prev?.promos || []).map(p => p.promo_code).filter(Boolean));
    const newCodes  = [...currCodes].filter(c => !prevCodes.has(c));

    if (newCodes.length) {
      const detail = (site.promos || []).find(p => newCodes.includes(p.promo_code))?.raw_text || "";
      newAlerts.push({ type: "new_promo_code", ts: now, brand: site.name, market,
        message: `New promo code: ${newCodes.join(", ")}`, detail });
    }
    if (isOnSale && !wasOnSale) {
      const detail = (site.promos || [])[0]?.raw_text || "";
      const summary = site.claude_summary || detail;
      newAlerts.push({ type: "sale_started", ts: now, brand: site.name, market,
        message: "Sale started", detail: summary });
    }
    if (!isOnSale && wasOnSale) {
      const dur = updatedSaleMap[site.id]?.consecutive_days || 1;
      newAlerts.push({ type: "sale_ended", ts: now, brand: site.name, market,
        message: `Sale ended after ${dur} day${dur !== 1 ? "s" : ""}`, detail: "" });
    }

    // ── Price alerts ────────────────────────────────────────────────────────
    const currPrice = site.territory_price?.price;
    const prevPrice = prev?.territory_price?.price;
    const threshold = parseFloat(process.env.PRICE_ALERT_THRESHOLD || "1.00");

    if (currPrice && prevPrice && Math.abs(currPrice - prevPrice) >= threshold) {
      const dir   = currPrice < prevPrice ? "decreased" : "increased";
      const delta = Math.abs(currPrice - prevPrice).toFixed(2);
      newAlerts.push({ type: "price_change", ts: now, brand: site.name, market,
        message: `Territory price ${dir} by $${delta}`,
        detail: `$${prevPrice.toFixed(2)} → $${currPrice.toFixed(2)}`,
        prev_price: prevPrice, new_price: currPrice });
    }
    if (currPrice && !prevPrice) {
      newAlerts.push({ type: "price_found", ts: now, brand: site.name, market,
        message: `Territory price now tracked: $${currPrice.toFixed(2)}`,
        detail: site.territory_price?.url || "" });
    }

    // ── Anomaly detection ───────────────────────────────────────────────────
    const hist = brandHistoryMap[site.id];
    const dow  = day_of_week ?? new Date(date).getDay();
    const minHistory = parseInt(process.env.MIN_HISTORY_FOR_ANOMALY || "14");
    const sigma      = parseFloat(process.env.ANOMALY_SIGMA || "2.0");

    if (hist && hist.all.length >= minHistory) {
      // Use day-of-week normalised history if available (7+ samples), else global
      const series = (hist.byDow[dow]?.length >= 7) ? hist.byDow[dow] : hist.all;
      const m = mean(series), sd = stddev(series);
      if (sd > 0 && intensity > m + sigma * sd && intensity > 20) {
        site.anomaly = true;
        site.anomaly_zscore = ((intensity - m) / sd).toFixed(1);
        newAlerts.push({ type: "anomaly", ts: now, brand: site.name, market,
          message: `Anomaly: intensity ${intensity} is ${site.anomaly_zscore}σ above their norm (avg=${Math.round(m)})`,
          detail: (site.promos || [])[0]?.raw_text || "" });
      }
    }

    // ── Canary failure alert ────────────────────────────────────────────────
    if (site.canary_pass === false && !site.error?.includes("canary")) {
      newAlerts.push({ type: "canary_fail", ts: now, brand: site.name, market,
        message: "Canary check failed — parser may be broken",
        detail: `Site returned ${site.http_status} but brand name not found in HTML` });
    }

    // ── Slow fetch alert ──────────────────────────────────────────────────
    if (site.fetch_duration_ms && site.fetch_duration_ms > 10000) {
      newAlerts.push({ type: "slow_fetch", ts: now, brand: site.name, market,
        message: `Slow fetch: ${(site.fetch_duration_ms / 1000).toFixed(1)}s`,
        detail: `Renderer: ${site.renderer || "http"}, status: ${site.http_status}` });
    }
  }

  // ── Persist ────────────────────────────────────────────────────────────────
  const snapshot = {
    date, scraped_at: now, day_of_week, is_weekend, sites,
    google_shopping: google_shopping || {},
  };

  // Update history keys list
  const allKeys = [...new Set([...historyKeys, date])].sort().slice(-MAX_HISTORY);

  await Promise.all([
    kv.set("wiper:latest",           snapshot),
    kv.set(`wiper:history:${date}`,  snapshot),
    kv.set("wiper:history_keys",     allKeys),
    kv.set("wiper:sale_state",       updatedSaleMap),
    kv.set("wiper:alerts",           [...newAlerts, ...existingAlerts].slice(0, MAX_ALERTS)),
  ]);

  // Store Google Shopping separately for easy access
  if (google_shopping) {
    await kv.set(`wiper:shopping:${date}`, google_shopping);
    await kv.set("wiper:shopping:latest",  google_shopping);
  }

  // Store landscape summary if provided
  if (body.landscape_summary) {
    await kv.set("wiper:landscape_summary", {
      date, summary: body.landscape_summary, target_brand: body.target_brand || "",
    });
  }

  return res.status(200).json({
    ok: true, date,
    brands_processed: sites.length,
    new_alerts: newAlerts.length,
    alerts: newAlerts,
  });
};
