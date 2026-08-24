/**
 * DiggerLid — Meta spend BY CAMPAIGN and BY AD SET.
 * Deploy alongside the existing feed as  api/campaigns.js  in the diggerlid-mer project.
 *
 *   /api/campaigns                    -> campaign-level spend, this month to date
 *   /api/campaigns?level=adset        -> ad-set level (ad set names usually carry the product)
 *   /api/campaigns?since=2026-07-01&until=2026-07-31   -> explicit range
 *
 * Uses the SAME META_TOKEN / META_ACCOUNT_ID env vars already set on the project.
 * Returns spend, impressions, clicks, purchases and purchase value per campaign/ad set,
 * plus a derived CPA and ROAS, so spend can be attributed to product categories.
 *
 * DEPLOY:
 *   cd ~/diggerlid-mer && mkdir -p api
 *   (save this file as api/campaigns.js)
 *   vercel --prod
 *   curl -s "https://diggerlid-mer.vercel.app/api/campaigns?level=adset"
 */

function monthRange() {
  var now = new Date(new Date().toLocaleString('en-US', { timeZone: 'Australia/Brisbane' }));
  var y = now.getFullYear(), m = now.getMonth();
  var pad = function (n) { return String(n).padStart(2, '0'); };
  return { since: y + '-' + pad(m + 1) + '-01', until: y + '-' + pad(m + 1) + '-' + pad(now.getDate()) };
}

module.exports = async function (req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 's-maxage=900, stale-while-revalidate=1800');
  try {
    var token = process.env.META_TOKEN, acct = process.env.META_ACCOUNT_ID;
    if (!token || !acct) return res.status(200).json({ error: 'META_TOKEN / META_ACCOUNT_ID not set' });
    if (!/^act_/.test(acct)) acct = 'act_' + acct;

    var q = req.query || {};
    var level = (q.level === 'adset') ? 'adset' : 'campaign';
    var r = monthRange();
    var since = q.since || r.since, until = q.until || r.until;

    var fields = level === 'adset'
      ? 'adset_name,campaign_name,spend,impressions,clicks,actions,action_values'
      : 'campaign_name,spend,impressions,clicks,actions,action_values';

    var url = 'https://graph.facebook.com/v20.0/' + acct + '/insights'
      + '?level=' + level
      + '&fields=' + fields
      + '&time_range=' + encodeURIComponent(JSON.stringify({ since: since, until: until }))
      + '&limit=500&access_token=' + token;

    var rows = [], guard = 0;
    while (url && guard++ < 10) {
      var resp = await fetch(url);
      if (!resp.ok) {
        return res.status(200).json({ error: 'meta ' + resp.status + ': ' + (await resp.text()).slice(0, 300) });
      }
      var j = await resp.json();
      (j.data || []).forEach(function (d) {
        var purch = 0, val = 0;
        (d.actions || []).forEach(function (a) {
          if (a.action_type === 'purchase' || a.action_type === 'omni_purchase') purch = parseFloat(a.value) || purch;
        });
        (d.action_values || []).forEach(function (a) {
          if (a.action_type === 'purchase' || a.action_type === 'omni_purchase') val = parseFloat(a.value) || val;
        });
        var spend = parseFloat(d.spend) || 0;
        rows.push({
          name: d.adset_name || d.campaign_name,
          campaign: d.campaign_name,
          spend: Math.round(spend * 100) / 100,
          impressions: parseInt(d.impressions || 0, 10),
          clicks: parseInt(d.clicks || 0, 10),
          purchases: purch,
          purchase_value: Math.round(val * 100) / 100,
          cpa: purch ? Math.round(spend / purch * 100) / 100 : null,
          roas: spend ? Math.round(val / spend * 100) / 100 : null
        });
      });
      url = (j.paging && j.paging.next) ? j.paging.next : null;
    }

    rows.sort(function (a, b) { return b.spend - a.spend; });
    var total = rows.reduce(function (s, x) { return s + x.spend; }, 0);
    rows.forEach(function (x) { x.share = total ? Math.round(x.spend / total * 1000) / 10 : 0; });

    res.status(200).json({
      level: level, since: since, until: until,
      total_spend: Math.round(total * 100) / 100,
      count: rows.length,
      rows: rows
    });
  } catch (e) {
    res.status(200).json({ error: String(e) });
  }
};
