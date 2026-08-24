/**
 * DiggerLid — Meta spend TIME-SERIES feed.  Deploy as a Vercel serverless function at /api/campaigns
 *
 * Companion to /api/mer (which returns only current-month MTD). This one returns a spend SERIES
 * over an arbitrary date range at a chosen increment, so the hub can plot RPV-vs-spend, weekly MER,
 * and cost-efficiency curves. Secrets stay server-side (same model as /api/mer).
 *
 * ── DEPLOY (once) ─────────────────────────────────────────────────────────
 * 1. Drop this file into the diggerlid-mer Vercel project as  api/campaigns.js
 *    (the repo behind diggerlid-mer.vercel.app). Vercel exposes it at /api/campaigns.
 * 2. It reuses the SAME env vars already set for /api/mer:  META_TOKEN, META_ACCOUNT_ID.
 * 3. Redeploy. Test:
 *      https://diggerlid-mer.vercel.app/api/campaigns?since=2026-01-01&until=2026-08-19&increment=1
 *    → JSON: { account, since, until, increment, total, series:[{date_start,date_stop,spend}, ...] }
 *
 * PARAMS
 *   since, until  YYYY-MM-DD (required-ish; default = last 90 days)
 *   increment     Meta time_increment: 1 (daily, default — most flexible; the hub buckets to ISO weeks),
 *                 7 (weekly), or "monthly". Daily is recommended so weeks align to Shopify's Mon–Sun.
 *   level         (optional) "account" (default) or "campaign" to break spend out per campaign.
 *
 * SECURITY: returns spend numbers only; META_TOKEN never leaves the server. No spreadsheet touched.
 */

async function metaSeries(since, until, increment, level) {
  var token = process.env.META_TOKEN, acct = process.env.META_ACCOUNT_ID;
  if (!token || !acct) return { error: 'META_TOKEN / META_ACCOUNT_ID not set' };
  var tr = encodeURIComponent(JSON.stringify({ since: since, until: until }));
  var fields = level === 'campaign' ? 'campaign_id,campaign_name,spend' : 'spend';
  var base = 'https://graph.facebook.com/v20.0/' + acct + '/insights' +
             '?fields=' + fields +
             '&time_range=' + tr +
             '&time_increment=' + increment +
             (level === 'campaign' ? '&level=campaign' : '') +
             '&limit=500&access_token=' + token;
  var out = [], url = base, guard = 0;
  while (url && guard++ < 50) {
    var r = await fetch(url);
    if (!r.ok) return { error: 'meta ' + r.status + ' ' + (await r.text()).slice(0, 300) };
    var j = await r.json();
    (j.data || []).forEach(function (d) {
      out.push({
        date_start: d.date_start, date_stop: d.date_stop,
        spend: parseFloat(d.spend || 0),
        campaign_id: d.campaign_id, campaign_name: d.campaign_name
      });
    });
    url = (j.paging && j.paging.next) ? j.paging.next : null;
  }
  return { series: out };
}

module.exports = async function (req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 's-maxage=3600, stale-while-revalidate=86400'); // 1h edge cache
  try {
    var q = req.query || {};
    var pad = function (n) { return String(n).padStart(2, '0'); };
    var d = new Date(), def = new Date(d.getTime() - 90 * 864e5);
    var iso = function (x) { return x.getFullYear() + '-' + pad(x.getMonth() + 1) + '-' + pad(x.getDate()); };
    var since = q.since || iso(def), until = q.until || iso(d);
    var increment = q.increment || '1';
    var level = q.level === 'campaign' ? 'campaign' : 'account';

    var r = await metaSeries(since, until, increment, level);
    if (r.error) return res.status(200).json({ source: 'error', error: r.error, since: since, until: until });

    var total = r.series.reduce(function (a, b) { return a + b.spend; }, 0);
    res.status(200).json({
      account: process.env.META_ACCOUNT_ID, since: since, until: until,
      increment: increment, level: level,
      total: Math.round(total * 100) / 100, points: r.series.length,
      series: r.series, updated: new Date().toISOString(),
      note: 'Meta spend series; token stays server-side. Bucket daily -> ISO weeks in the hub to align with Shopify.'
    });
  } catch (e) {
    res.status(200).json({ source: 'error', error: String(e) });
  }
};
