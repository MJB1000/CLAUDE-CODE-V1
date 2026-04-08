// api/weekly-digest.js
// Triggered by Vercel Cron every Monday 07:00 AEST (21:00 UTC Sunday)
// Composes a full weekly intelligence briefing email

const { kv } = require("./_kv");
const nodemailer = require("nodemailer");

const SECRET     = process.env.WIPER_INTEL_SECRET || "changeme";
const ALERT_TO   = process.env.ALERT_TO   || "matthew@wipertech.com.au";
const ALERT_FROM = process.env.ALERT_FROM || "alerts@wipertech.com.au";
const SMTP_HOST  = process.env.SMTP_HOST  || "smtp.gmail.com";
const SMTP_PORT  = parseInt(process.env.SMTP_PORT || "587");
const SMTP_USER  = process.env.SMTP_USER  || "";
const SMTP_PASS  = process.env.SMTP_PASS  || "";

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");

  // Allow manual trigger with secret, or Vercel Cron (no auth header)
  const apiKey = req.headers["x-api-key"] || req.query.key;
  const isCron = req.headers["x-vercel-cron"] === "1";
  if (!isCron && apiKey !== SECRET)
    return res.status(401).json({ error: "Unauthorized" });

  try {
    // Load last 7 days of history
    const histKeys = (await kv.get("intel:history_keys").catch(() => [])) || [];
    const last7    = histKeys.slice(-7);
    const snaps    = await Promise.all(
      last7.map(k => kv.get(`intel:history:${k}`).catch(() => null))
    );
    const history  = snaps.filter(Boolean);
    const alerts   = (await kv.get("intel:alerts").catch(() => [])) || [];
    const latest   = await kv.get("intel:latest").catch(() => null);
    const shopping = await kv.get("intel:shopping:latest").catch(() => null);
    const ownData  = await kv.get("intel:own_data").catch(() => null);
    const saleState = (await kv.get("intel:sale_state").catch(() => {})) || {};

    if (!history.length) {
      return res.status(200).json({ ok: false, reason: "No history available yet" });
    }

    const landscape = await kv.get("intel:landscape_summary").catch(() => null);
    const digestHtml = buildDigestHtml(history, alerts, latest, shopping, ownData, saleState, landscape);
    const digestText = buildDigestText(history, alerts, latest, shopping, ownData, landscape);

    if (SMTP_USER && SMTP_PASS) {
      const transporter = nodemailer.createTransport({
        host: SMTP_HOST, port: SMTP_PORT, secure: false,
        auth: { user: SMTP_USER, pass: SMTP_PASS },
      });

      const weekStart = last7[0] || "—";
      const weekEnd   = last7[last7.length - 1] || "—";

      await transporter.sendMail({
        from:    `"Wiper Intel" <${ALERT_FROM}>`,
        to:      ALERT_TO,
        subject: `[Wiper Intel] Weekly Digest — ${weekStart} to ${weekEnd}`,
        text:    digestText,
        html:    digestHtml,
      });

      return res.status(200).json({ ok: true, sent_to: ALERT_TO, days_covered: history.length });
    } else {
      // Return HTML for testing if no SMTP configured
      return res.status(200).send(digestHtml);
    }
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: err.message });
  }
};

// ── Build digest HTML ──────────────────────────────────────────────────────────

function buildDigestHtml(history, alerts, latest, shopping, ownData, saleState, landscape) {
  const sites    = latest?.sites || [];
  const auSites  = sites.filter(s => s.market === "AU" || !s.market);
  const nzSites  = sites.filter(s => s.market === "NZ");
  const weekAlerts = alerts.slice(0, 20);

  // Weekly stats
  const allIntensities = history.flatMap(d => (d.sites || []).map(s => s.promotion_intensity || 0));
  const avgIntensity   = allIntensities.length
    ? Math.round(allIntensities.reduce((a, x) => a + x, 0) / allIntensities.length) : 0;

  // Brands on sale today
  const onSaleToday = sites.filter(s => s.is_on_sale);

  // Price leader (lowest Territory price AU)
  const auPrices = auSites.map(s => ({ name: s.name, price: s.product_price?.price }))
    .filter(s => s.price).sort((a, b) => a.price - b.price);

  // Anomalies this week
  const anomalyAlerts = weekAlerts.filter(a => a.type === "anomaly");

  // Sale durations
  const longSales = sites
    .filter(s => (saleState[s.id]?.consecutive_days || 0) >= 3)
    .sort((a, b) => (saleState[b.id]?.consecutive_days || 0) - (saleState[a.id]?.consecutive_days || 0));

  const weekRange = history.length >= 2
    ? `${history[0].date} – ${history[history.length - 1].date}`
    : history[0]?.date || "—";

  const S = (text, color = "#1a1a1a") => `<span style="color:${color}">${text}</span>`;

  const tableRow = (cells, header = false) => {
    const tag = header ? "th" : "td";
    const style = header
      ? `style="text-align:left;padding:8px 12px;font-size:11px;color:#888;text-transform:uppercase;border-bottom:2px solid #eee;font-weight:400"`
      : `style="padding:8px 12px;border-bottom:1px solid #f0f0f0;font-size:13px;vertical-align:middle"`;
    return `<tr>${cells.map(c => `<${tag} ${style}>${c}</${tag}>`).join("")}</tr>`;
  };

  return `<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  body{margin:0;padding:0;background:#f5f5f0;font-family:'Helvetica Neue',Arial,sans-serif;color:#1a1a1a}
  .wrap{max-width:680px;margin:0 auto;padding:32px 16px}
  .card{background:#fff;border-radius:12px;padding:28px;margin-bottom:20px;box-shadow:0 1px 4px rgba(0,0,0,.06)}
  .header{background:#111;border-radius:12px;padding:28px;margin-bottom:20px;color:#f0ede8}
  .logo{font-family:monospace;font-size:13px;color:#c8f135;letter-spacing:.1em;margin-bottom:12px}
  .h1{font-size:22px;font-weight:600;margin:0 0 6px}
  .sub{font-size:13px;color:#888;margin:0}
  .stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:0}
  .stat{background:#f9f9f7;border-radius:8px;padding:14px}
  .stat-label{font-size:11px;color:#888;text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px}
  .stat-val{font-size:22px;font-weight:600}
  .section-title{font-size:14px;font-weight:600;margin:0 0 14px;padding-bottom:10px;border-bottom:1px solid #f0f0f0}
  table{width:100%;border-collapse:collapse}
  .badge{display:inline-block;font-size:10px;padding:2px 7px;border-radius:4px;font-family:monospace}
  .badge-live{background:#eafce3;color:#2a7a1e}
  .badge-off{background:#f5f5f5;color:#888}
  .badge-alert{background:#fff3e0;color:#b45309}
  .badge-nz{background:#e8f0ff;color:#2a4db5}
  .price-lo{color:#2a7a1e;font-weight:600}
  .alert-row{padding:8px 0;border-bottom:1px solid #f5f5f5;font-size:13px;display:flex;gap:10px}
  .alert-ts{font-size:11px;color:#aaa;min-width:60px;flex-shrink:0;margin-top:1px}
  .footer{text-align:center;font-size:11px;color:#aaa;padding:20px 0}
  a{color:#2563eb}
</style></head><body>
<div class="wrap">

  <div class="header">
    <div class="logo">WT / WIPER INTEL</div>
    <div class="h1">Weekly Digest</div>
    <div class="sub">${weekRange} · AU + NZ · ${sites.length} brands tracked</div>
  </div>

  <!-- Stats -->
  <div class="card">
    <div class="stat-grid">
      <div class="stat">
        <div class="stat-label">On sale today</div>
        <div class="stat-val" style="color:${onSaleToday.length > 0 ? '#c8a800' : '#1a1a1a'}">${onSaleToday.length}</div>
        <div style="font-size:11px;color:#888;margin-top:3px">of ${sites.length} brands</div>
      </div>
      <div class="stat">
        <div class="stat-label">Avg intensity (7d)</div>
        <div class="stat-val">${avgIntensity}</div>
        <div style="font-size:11px;color:#888;margin-top:3px">/ 100 scale</div>
      </div>
      <div class="stat">
        <div class="stat-label">Lowest AU price</div>
        <div class="stat-val price-lo">${auPrices.length ? "$" + auPrices[0].price.toFixed(2) : "—"}</div>
        <div style="font-size:11px;color:#888;margin-top:3px">${auPrices.length ? auPrices[0].name : "no data"}</div>
      </div>
    </div>
  </div>

  ${landscape?.summary ? `
  <!-- AI Landscape Analysis -->
  <div class="card" style="border-left:3px solid #c8f135">
    <div class="section-title">AI Competitive Analysis</div>
    <div style="font-size:13px;line-height:1.6;color:#333">${landscape.summary}</div>
  </div>` : ""}

  ${ownData ? `
  <!-- Own position -->
  <div class="card">
    <div class="section-title">Wipertech Position</div>
    <div style="display:flex;align-items:center;gap:12px">
      <span class="badge ${ownData.active ? 'badge-live' : 'badge-off'}">${ownData.active ? "SALE ACTIVE" : "NO SALE"}</span>
      ${ownData.active && ownData.promo ? `
        <span style="font-size:13px">${ownData.promo.raw_text}</span>
        ${ownData.promo.promo_code ? `<span style="font-family:monospace;font-size:11px;background:#fff3cd;padding:2px 6px;border-radius:3px">${ownData.promo.promo_code}</span>` : ""}
      ` : `<span style="font-size:13px;color:#888">No active promotion this week</span>`}
    </div>
    ${ownData.note ? `<div style="margin-top:8px;font-size:12px;color:#666">${ownData.note}</div>` : ""}
  </div>` : ""}

  <!-- Active sales -->
  ${onSaleToday.length > 0 ? `
  <div class="card">
    <div class="section-title">Active Sales Right Now</div>
    <table>
      ${tableRow(["Brand", "Market", "Deal", "Intensity", "Duration"], true)}
      ${onSaleToday.map(s => {
        const promo = (s.promos || [])[0];
        const dur   = saleState[s.id]?.consecutive_days || s.sale_duration_days || 1;
        const dealText = s.claude_summary || promo?.raw_text?.substring(0, 55) || "—";
        const mktBadge = s.market === "NZ" ? `<span class="badge badge-nz">NZ</span>` : "";
        return tableRow([
          `<strong>${s.name}</strong>`,
          mktBadge || "AU",
          `<span style="font-size:12px;color:#444">${dealText}</span>`,
          `<span style="font-family:monospace;color:${s.promotion_intensity >= 40 ? '#b45309' : '#555'}">${s.promotion_intensity}</span>`,
          `<span style="color:#888;font-size:12px">${dur}d</span>`,
        ]);
      }).join("")}
    </table>
  </div>` : ""}

  <!-- Territory pricing -->
  ${auPrices.length > 0 ? `
  <div class="card">
    <div class="section-title">Ford Territory 2009 — AU Price Comparison</div>
    <table>
      ${tableRow(["Brand", "Price", "Type", "Change?"], true)}
      ${auPrices.slice(0, 8).map((item, i) => {
        const site = auSites.find(s => s.name === item.name);
        return tableRow([
          `${i === 0 ? "🏆 " : ""}<strong>${item.name}</strong>`,
          `<span class="${i === 0 ? "price-lo" : ""}" style="font-family:monospace">$${item.price.toFixed(2)}</span>`,
          `<span style="font-size:11px;color:#888">${site?.type || ""}</span>`,
          "—",
        ]);
      }).join("")}
    </table>
  </div>` : ""}

  ${shopping && (shopping.AU?.listings?.length || shopping.NZ?.listings?.length) ? `
  <!-- Google Shopping -->
  <div class="card">
    <div class="section-title">Google Shopping — Ford Territory 2009</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
      ${["AU","NZ"].map(mkt => {
        const s = shopping[mkt];
        if (!s || !s.listings?.length) return `<div><strong>${mkt}</strong><br><span style="color:#aaa;font-size:12px">No data</span></div>`;
        return `<div>
          <div style="font-weight:600;margin-bottom:8px">${mkt}</div>
          <div style="font-size:13px"><span style="color:#2a7a1e">Low: <strong>$${s.min_price?.toFixed(2)}</strong></span> &nbsp;·&nbsp; High: $${s.max_price?.toFixed(2)}</div>
          <div style="font-size:11px;color:#888;margin-top:4px">${s.listing_count} listings found</div>
        </div>`;
      }).join("")}
    </div>
  </div>` : ""}

  ${anomalyAlerts.length > 0 ? `
  <!-- Anomalies -->
  <div class="card" style="border-left:3px solid #f59e0b">
    <div class="section-title">⚡ Anomalies Detected This Week</div>
    ${anomalyAlerts.map(a => `
      <div class="alert-row">
        <span class="alert-ts">${new Date(a.ts).toLocaleDateString("en-AU",{day:"2-digit",month:"short"})}</span>
        <span><strong>${a.brand}</strong> [${a.market}] — ${a.message}</span>
      </div>`).join("")}
  </div>` : ""}

  <!-- All alerts -->
  ${weekAlerts.length > 0 ? `
  <div class="card">
    <div class="section-title">All Alerts This Week (${Math.min(weekAlerts.length, 20)})</div>
    ${weekAlerts.slice(0, 20).map(a => {
      const ICONS = {sale_started:"▲",sale_ended:"▼",price_change:"$",new_promo_code:"★",anomaly:"⚡",canary_fail:"⚠",price_found:"+"};
      return `<div class="alert-row">
        <span class="alert-ts">${new Date(a.ts).toLocaleDateString("en-AU",{day:"2-digit",month:"short"})}</span>
        <span>${ICONS[a.type]||"·"} <strong>${a.brand}</strong> [${a.market||"AU"}] — ${a.message}${a.detail ? " · " + a.detail.substring(0,60) : ""}</span>
      </div>`;
    }).join("")}
  </div>` : ""}

  <!-- CTA -->
  <div class="card" style="text-align:center;background:#111">
    <a href="https://dashboard-theta-five-15.vercel.app/wiper-intel" style="display:inline-block;background:#c8f135;color:#111;padding:12px 28px;border-radius:8px;text-decoration:none;font-weight:600;font-size:14px">Open Live Dashboard →</a>
  </div>

  <div class="footer">
    Wiper Intel · Competitive Intelligence for Wipertech AU<br>
    Generated ${new Date().toLocaleString("en-AU", {timeZone:"Australia/Melbourne",day:"2-digit",month:"short",year:"numeric",hour:"2-digit",minute:"2-digit"})} AEST
  </div>

</div></body></html>`;
}

function buildDigestText(history, alerts, latest, shopping, ownData, landscape) {
  const sites       = latest?.sites || [];
  const onSale      = sites.filter(s => s.is_on_sale);
  const weekRange   = history.length >= 2
    ? `${history[0].date} to ${history[history.length - 1].date}` : "this week";
  const auPrices    = sites.filter(s => (s.market === "AU" || !s.market) && s.product_price?.price)
    .sort((a, b) => a.product_price.price - b.product_price.price);

  return [
    `WIPER INTEL — Weekly Digest (${weekRange})`,
    "=".repeat(50),
    "",
    `Brands on sale: ${onSale.length} of ${sites.length}`,
    `Lowest AU Territory price: ${auPrices.length ? "$" + auPrices[0].product_price.price.toFixed(2) + " (" + auPrices[0].name + ")" : "—"}`,
    "",
    landscape?.summary ? `AI Analysis: ${landscape.summary}` : "",
    "",
    ownData ? `Own position: ${ownData.active ? "SALE ACTIVE — " + (ownData.promo?.raw_text || "") : "No active promotion"}` : "",
    "",
    "Active sales:",
    ...onSale.map(s => `  ${s.name} [${s.market || "AU"}]: ${(s.promos || [])[0]?.raw_text?.substring(0, 60) || "—"}`),
    "",
    "Recent alerts:",
    ...alerts.slice(0, 10).map(a => `  ${a.brand} — ${a.message}`),
    "",
    "Dashboard: https://dashboard-theta-five-15.vercel.app/wiper-intel",
  ].filter(l => l !== undefined && l !== null).join("\n");
}
