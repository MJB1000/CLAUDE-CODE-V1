/**
 * DiggerLid — live MER / GPAM feed.  Deploy as a Vercel serverless function at  /api/mer
 *
 * WHY THIS EXISTS: a Meta token is a secret and must NOT sit in the dashboard (client-side =
 * exposed) or in any spreadsheet. This function holds the secrets in Vercel env vars, calls
 * Meta + Shopify server-side, and returns ONLY computed numbers. The dashboard fetches this.
 * It reads/writes NO Google Sheet.
 *
 * ── DEPLOY (once) ─────────────────────────────────────────────────────────
 * 1. Drop this file into your Vercel calendar project as  api/mer.js  (the repo behind
 *    diggerlid-calendar-henna.vercel.app). Vercel auto-exposes it at /api/mer.
 * 2. Vercel → Project → Settings → Environment Variables (values only you ever see):
 *       META_TOKEN        Meta system-user token, scope: ads_read
 *       META_ACCOUNT_ID   e.g.  act_1234567890
 *       SHOPIFY_SHOP      digger-lid.myshopify.com
 *       SHOPIFY_TOKEN     shpat_...            (Admin API, scope: read_orders)
 *       VCR               (optional) default 0.46
 *       GPAM_TARGET       (optional) default 0.26
 *       FIXED_MONTHLY     (optional) default 74831
 * 3. Redeploy. Test: open  https://<your-app>.vercel.app/api/mer  → you should see JSON.
 * 4. Paste that URL into the dashboard (FEED_URL) and it goes live.
 *
 * If SHOPIFY_TOKEN isn't set, pass revenue in as  /api/mer?rev=264093  and it still computes MER.
 */

const API = '2024-10';

function monthRange(tz) {
  var now = new Date(new Date().toLocaleString('en-US', { timeZone: tz || 'Australia/Brisbane' }));
  var y = now.getFullYear(), m = now.getMonth();
  var pad = function (n) { return String(n).padStart(2, '0'); };
  return { first: y + '-' + pad(m + 1) + '-01', today: y + '-' + pad(m + 1) + '-' + pad(now.getDate()) };
}

async function metaSpend(since, until) {
  var token = process.env.META_TOKEN, acct = process.env.META_ACCOUNT_ID;
  if (!token || !acct) return null;
  var tr = encodeURIComponent(JSON.stringify({ since: since, until: until }));
  var url = 'https://graph.facebook.com/v20.0/' + acct + '/insights?fields=spend&time_range=' + tr +
            '&access_token=' + token;
  var r = await fetch(url);
  if (!r.ok) return null;
  var j = await r.json();
  return (j.data && j.data[0]) ? parseFloat(j.data[0].spend) : 0;
}

async function shopifyNet(first, today) {
  var shop = process.env.SHOPIFY_SHOP, token = process.env.SHOPIFY_TOKEN;
  if (!shop || !token) return null;
  var orders = 0, net = 0;
  var url = 'https://' + shop + '/admin/api/' + API + '/orders.json?status=any' +
            '&created_at_min=' + first + 'T00:00:00&created_at_max=' + today + 'T23:59:59' +
            '&limit=250&fields=id,subtotal_price,current_subtotal_price';
  while (url) {
    var r = await fetch(url, { headers: { 'X-Shopify-Access-Token': token } });
    if (!r.ok) break;
    var j = await r.json();
    (j.orders || []).forEach(function (o) {
      orders++; net += parseFloat(o.current_subtotal_price || o.subtotal_price || 0);
    });
    var link = r.headers.get('link') || '';
    var m = link.match(/<([^>]+)>;\s*rel="next"/);
    url = m ? m[1] : null;
  }
  return { orders: orders, net: net };
}

module.exports = async function (req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');                 // dashboard may live elsewhere
  res.setHeader('Cache-Control', 's-maxage=900, stale-while-revalidate=1800'); // 15-min edge cache
  try {
    var r = monthRange();
    var vcr = parseFloat(process.env.VCR || '0.46');
    var target = parseFloat(process.env.GPAM_TARGET || '0.26');
    var fixed = parseFloat(process.env.FIXED_MONTHLY || '74831');

    var pair = await Promise.all([metaSpend(r.first, r.today), shopifyNet(r.first, r.today)]);
    var spend = pair[0], shop = pair[1];
    var qRev = (req.query && req.query.rev) ? parseFloat(req.query.rev) : null;
    var net = (shop && shop.net) || qRev || null;

    var mer = null, gpam = null, gpamDollar = null, netProfit = null, source = 'unavailable';
    if (spend != null && net) {
      mer = spend / net;
      gpam = (1 - vcr) - mer;
      gpamDollar = net * gpam;
      netProfit = gpamDollar - fixed;
      source = 'live (Meta' + (shop ? '+Shopify' : '+rev param') + ')';
    } else if (spend == null) {
      source = 'META_TOKEN not set';
    }

    res.status(200).json({
      month: r.first.slice(0, 7),
      updated: new Date().toISOString(),
      mtd_net: net, mtd_spend: spend, orders: shop ? shop.orders : null,
      aov: (shop && shop.orders) ? net / shop.orders : null,
      mer: mer, vcr: vcr, gpam: gpam, gpam_target: target,
      gpam_dollar: gpamDollar, net_profit: netProfit,
      source: source,
      note: 'Computed server-side; secrets stay in Vercel env. No spreadsheet read or written.'
    });
  } catch (e) {
    res.status(200).json({ source: 'error', error: String(e) });
  }
};
