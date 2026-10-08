/**
 * DiggerLid — Meta REACH and VIDEO feed.  Deploy as  api/reach.js  in the diggerlid-mer Vercel project.
 *
 * Why: /api/campaigns returns spend, impressions, clicks and purchases only. Reach, frequency and
 * video views are separate insight fields. This endpoint returns account-level totals for a date
 * range so year-on-year media facts can be pulled without the token leaving the server.
 *
 *   /api/reach?since=2025-09-23&until=2026-09-22
 *   /api/reach?since=...&until=...&increment=monthly     (one row per month)
 *
 * Reuses META_TOKEN + META_ACCOUNT_ID. Deploy: save this file as api/reach.js, then `vercel --prod`.
 * Returns: reach (unique accounts, de-duplicated across the whole range when no increment is set),
 * impressions, frequency, spend, video_3s (3-second plays), video_thruplay, video_p25/p50/p100.
 */
module.exports = async function (req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 's-maxage=3600, stale-while-revalidate=86400');
  try {
    var token = process.env.META_TOKEN, acct = process.env.META_ACCOUNT_ID;
    if (!token || !acct) return res.status(200).json({ error: 'META_TOKEN / META_ACCOUNT_ID not set' });
    if (!/^act_/.test(acct)) acct = 'act_' + acct;
    var q = req.query || {};
    if (!q.since || !q.until) return res.status(200).json({ error: 'since and until (YYYY-MM-DD) required' });
    var fields = 'spend,impressions,reach,frequency,actions,video_play_actions,video_thruplay_watched_actions,' +
                 'video_p25_watched_actions,video_p50_watched_actions,video_p100_watched_actions';
    var url = 'https://graph.facebook.com/v20.0/' + acct + '/insights?fields=' + fields +
              '&time_range=' + encodeURIComponent(JSON.stringify({ since: q.since, until: q.until })) +
              (q.increment ? '&time_increment=' + q.increment : '') + '&limit=500&access_token=' + token;
    var pick = function (arr, type) {
      var v = 0; (arr || []).forEach(function (a) { if (a.action_type === type) v = parseFloat(a.value) || v; }); return v;
    };
    var rows = [], guard = 0;
    while (url && guard++ < 20) {
      var r = await fetch(url);
      if (!r.ok) return res.status(200).json({ error: 'meta ' + r.status + ': ' + (await r.text()).slice(0, 300) });
      var j = await r.json();
      (j.data || []).forEach(function (d) {
        rows.push({
          date_start: d.date_start, date_stop: d.date_stop,
          spend: parseFloat(d.spend || 0), impressions: parseInt(d.impressions || 0, 10),
          reach: parseInt(d.reach || 0, 10), frequency: parseFloat(d.frequency || 0),
          video_3s: pick(d.actions, 'video_view'),
          video_plays: pick(d.video_play_actions, 'video_view'),
          video_thruplay: pick(d.video_thruplay_watched_actions, 'video_view'),
          video_p25: pick(d.video_p25_watched_actions, 'video_view'),
          video_p50: pick(d.video_p50_watched_actions, 'video_view'),
          video_p100: pick(d.video_p100_watched_actions, 'video_view')
        });
      });
      url = (j.paging && j.paging.next) ? j.paging.next : null;
    }
    res.status(200).json({ since: q.since, until: q.until, increment: q.increment || 'range', rows: rows });
  } catch (e) { res.status(200).json({ error: String(e) }); }
};
