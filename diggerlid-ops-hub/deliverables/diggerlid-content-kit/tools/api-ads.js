/**
 * DiggerLid — Meta TOP ADS WITH COPY, business-as-usual (non-sale) periods only.
 * Deploy alongside the existing feed as  api/ads.js  in the diggerlid-mer project.
 *
 *   /api/ads                                  -> top 30 ads by ROAS across the default BAU windows
 *   /api/ads?sort=purchases&top=50            -> rank by purchases instead, return 50
 *   /api/ads?min_spend=500                    -> ignore ads with less than $500 spend (default 300)
 *   /api/ads?windows=2026-01-05:2026-03-31,2026-07-01:2026-08-22   -> custom BAU windows
 *
 * Default windows skip the sale periods (BFCM 2025 16 Nov–1 Dec, Boxing Day / Christmas,
 * EOFY 2026 15–30 Jun, Father's Day 2026 23 Aug–7 Sep). Edit DEFAULT_WINDOWS if other sales ran.
 *
 * For each ad it returns performance summed across the windows plus the creative copy:
 * body (primary text), title (headline), description, link, and for dynamic / Advantage+
 * creative the full asset_feed_spec text variants. Read-only: ads_read is all it needs.
 *
 * Uses the SAME META_TOKEN / META_ACCOUNT_ID env vars already set on the project.
 * The token never leaves the server.
 *
 * DEPLOY:
 *   cd ~/diggerlid-mer && mkdir -p api
 *   (save this file as api/ads.js)
 *   vercel --prod
 *   curl -s "https://diggerlid-mer.vercel.app/api/ads" > top-ads.json
 */

var DEFAULT_WINDOWS = [
  ['2025-10-01', '2025-11-15'],
  ['2026-01-05', '2026-06-14'],
  ['2026-07-01', '2026-08-22'],
  ['2026-09-08', '2026-10-06']
];

var GRAPH = 'https://graph.facebook.com/v20.0/';

function pick(list, types) {
  var v = 0;
  (list || []).forEach(function (a) {
    if (types.indexOf(a.action_type) !== -1) v = parseFloat(a.value) || v;
  });
  return v;
}

async function getAll(url) {
  var out = [], guard = 0;
  while (url && guard++ < 20) {
    var resp = await fetch(url);
    if (!resp.ok) throw new Error('meta ' + resp.status + ': ' + (await resp.text()).slice(0, 300));
    var j = await resp.json();
    out = out.concat(j.data || []);
    url = (j.paging && j.paging.next) ? j.paging.next : null;
  }
  return out;
}

module.exports = async function (req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 's-maxage=3600, stale-while-revalidate=7200');
  try {
    var token = process.env.META_TOKEN, acct = process.env.META_ACCOUNT_ID;
    if (!token || !acct) return res.status(200).json({ error: 'META_TOKEN / META_ACCOUNT_ID not set' });
    if (!/^act_/.test(acct)) acct = 'act_' + acct;

    var q = req.query || {};
    var top = Math.min(parseInt(q.top || '30', 10) || 30, 100);
    var minSpend = parseFloat(q.min_spend || '300') || 0;
    var sort = ['roas', 'purchases', 'purchase_value', 'spend', 'ctr'].indexOf(q.sort) !== -1 ? q.sort : 'roas';
    var windows = q.windows
      ? String(q.windows).split(',').map(function (w) { return w.split(':'); })
      : DEFAULT_WINDOWS;

    // 1. Ad-level insights per BAU window, summed per ad.
    var byAd = {};
    for (var i = 0; i < windows.length; i++) {
      var url = GRAPH + acct + '/insights?level=ad'
        + '&fields=ad_id,ad_name,adset_name,campaign_name,spend,impressions,clicks,inline_link_clicks,actions,action_values'
        + '&time_range=' + encodeURIComponent(JSON.stringify({ since: windows[i][0], until: windows[i][1] }))
        + '&limit=500&access_token=' + token;
      var rows = await getAll(url);
      rows.forEach(function (d) {
        var a = byAd[d.ad_id] || (byAd[d.ad_id] = {
          ad_id: d.ad_id, ad_name: d.ad_name, adset: d.adset_name, campaign: d.campaign_name,
          spend: 0, impressions: 0, link_clicks: 0, purchases: 0, purchase_value: 0, windows: 0
        });
        a.spend += parseFloat(d.spend) || 0;
        a.impressions += parseInt(d.impressions || 0, 10);
        a.link_clicks += parseInt(d.inline_link_clicks || 0, 10);
        a.purchases += pick(d.actions, ['purchase', 'omni_purchase']);
        a.purchase_value += pick(d.action_values, ['purchase', 'omni_purchase']);
        a.windows++;
      });
    }

    var ads = Object.keys(byAd).map(function (k) { return byAd[k]; })
      .filter(function (a) { return a.spend >= minSpend && a.purchases > 0; });
    ads.forEach(function (a) {
      a.spend = Math.round(a.spend * 100) / 100;
      a.purchase_value = Math.round(a.purchase_value * 100) / 100;
      a.roas = a.spend ? Math.round(a.purchase_value / a.spend * 100) / 100 : 0;
      a.cpa = a.purchases ? Math.round(a.spend / a.purchases * 100) / 100 : null;
      a.ctr = a.impressions ? Math.round(a.link_clicks / a.impressions * 10000) / 100 : 0;
    });
    ads.sort(function (a, b) { return (b[sort] || 0) - (a[sort] || 0); });
    ads = ads.slice(0, top);

    // 2. Creative copy for the winners, 25 ids per batch.
    var fields = 'name,creative{id,name,body,title,link_url,call_to_action_type,object_type,'
      + 'object_story_spec,asset_feed_spec{bodies,titles,descriptions,link_urls,call_to_action_types}}';
    for (var b = 0; b < ads.length; b += 25) {
      var ids = ads.slice(b, b + 25).map(function (a) { return a.ad_id; }).join(',');
      var resp = await fetch(GRAPH + '?ids=' + ids + '&fields=' + encodeURIComponent(fields) + '&access_token=' + token);
      if (!resp.ok) continue;
      var j = await resp.json();
      ads.slice(b, b + 25).forEach(function (a) {
        var c = (j[a.ad_id] || {}).creative || {};
        var oss = c.object_story_spec || {};
        var link = oss.link_data || {}, video = oss.video_data || {};
        var feed = c.asset_feed_spec || {};
        var texts = function (arr) { return (arr || []).map(function (x) { return x.text; }).filter(Boolean); };
        a.copy = {
          format: c.object_type || (oss.video_data ? 'VIDEO' : 'SHARE'),
          body: c.body || link.message || video.message || null,
          title: c.title || link.name || video.title || null,
          description: link.description || video.link_description || null,
          link: c.link_url || link.link || ((video.call_to_action || {}).value || {}).link || null,
          cta: c.call_to_action_type || ((link.call_to_action || video.call_to_action || {}).type) || null,
          bodies: texts(feed.bodies),
          titles: texts(feed.titles),
          descriptions: texts(feed.descriptions)
        };
      });
    }

    res.status(200).json({
      sort: sort, min_spend: minSpend, windows: windows,
      count: ads.length, ads: ads
    });
  } catch (e) {
    res.status(200).json({ error: String(e) });
  }
};
