/**
 * DiggerLid Ops Hub — one Google Apps Script that runs the whole daily loop, free & autonomous.
 * Bind it to your EE-model Google Sheet. One daily trigger → pull → compute → email.
 *
 *   F1  dailyImport()      pull yesterday's Shopify sales → "Daily Actuals" tab
 *   F3  computeScorecard() read actuals + CONFIG → write "Scorecard" + "Forecast" tabs
 *   F4  sendDailyBrief()   read those + the /ai calendar → email the brief (from your address)
 *   F2  getMetaSpend()     STUB — returns null today; fill it tomorrow to make MER real
 *   ▶  dailyRun()          orchestrator the trigger calls (import → compute → send)
 *
 * ── SETUP (once, ~15 min — do it signed in as matthew@diggerlid.com so email sends from you) ──
 * 1. Import the EE model xlsx into Google Sheets (Drive → Open with Google Sheets). Set
 *    File → Settings → timezone = Australia/Brisbane.
 * 2. Extensions → Apps Script → paste this file.
 * 3. Shopify admin → Develop apps → create app → scope read_orders → install → copy token.
 * 4. Project Settings → Script properties:
 *       SHOP          = digger-lid.myshopify.com
 *       SHOPIFY_TOKEN = shpat_xxxx            (never in code/chat)
 *       BRIEF_TO      = matthew@diggerlid.com
 * 5. Run backfillThisMonth() once (authorises + fills the month so far).
 * 6. Run dailyRun() once to check the email arrives.
 * 7. Triggers (clock) → Add trigger → dailyRun → Time-driven → Day timer → 6–7am. Done.
 *
 * TOMORROW (F2): create a Meta system-user token (ads_read), add META_TOKEN + META_ACCOUNT_ID
 * to Script properties, and fill getMetaSpend() — MER/GPAM then go fully real, no other change.
 */

// ─────────────────────────── CONFIG (edit freely) ───────────────────────────
var CONFIG = {
  API_VERSION: '2024-10',
  FIXED_MONTHLY: 74831,          // total fixed costs / month (EE Drivers)
  VCR_BAU: 0.46, VCR_SALE: 0.48, // variable cost ratio
  GPAM_TARGET: 0.26, MER_TARGET: 0.25, CVR_TARGET: 0.022,

  // finished months: [net_revenue, realized_MER]  (EE model)
  ACTUALS: {
    'Jan': [239596, 0.20], 'Feb': [298749, 0.28], 'Mar': [301354, 0.32],
    'Apr': [331418, 0.32], 'May': [400329, 0.30], 'Jun': [778275, 0.25]
  },
  // current-month MER until Meta is wired (F2). Keyed yyyy-MM. From EE model Accelerate_4.
  MER_OVERRIDE: { '2026-07': 0.37 },

  // forward scenario: [net_rev, isSale, MER_current, MER_target]
  FORWARD: {
    'Aug': [420000, true,  0.32, 0.27], 'Sep': [340000, false, 0.30, 0.25],
    'Oct': [330000, false, 0.30, 0.25], 'Nov': [580000, true,  0.28, 0.26],
    'Dec': [430000, true,  0.30, 0.26]
  },
  MONTHS: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
  CAL_URL: 'https://diggerlid-calendar-henna.vercel.app/ai'
};

// ─────────────────────────── F1: Shopify import ───────────────────────────
function dailyImport() { importRange_(dateNDaysAgo_(1), dateNDaysAgo_(1)); }
function backfillThisMonth() {
  var tz = Session.getScriptTimeZone(), now = new Date();
  var first = new Date(now.getFullYear(), now.getMonth(), 1);
  importRange_(Utilities.formatDate(first, tz, 'yyyy-MM-dd'), dateNDaysAgo_(1));
}
function importRange_(fromDay, toDay) {
  var p = PropertiesService.getScriptProperties();
  var shop = p.getProperty('SHOP'), token = p.getProperty('SHOPIFY_TOKEN');
  if (!shop || !token) throw new Error('Set SHOP and SHOPIFY_TOKEN in Script properties.');
  var sh = tab_('Daily Actuals', ['date','orders','gross','net','aov']);
  var have = sh.getLastRow() > 1 ? sh.getRange(2,1,sh.getLastRow()-1,1).getValues().flat().map(String) : [];

  var d = new Date(fromDay + 'T12:00:00'), end = new Date(toDay + 'T12:00:00');
  while (d <= end) {
    var day = Utilities.formatDate(d, Session.getScriptTimeZone(), 'yyyy-MM-dd');
    var t = dayTotals_(shop, token, day);
    var row = [day, t.orders, t.gross, t.net, t.orders ? t.net/t.orders : 0];
    var idx = have.indexOf(day);
    if (idx === -1) { sh.appendRow(row); have.push(day); }
    else sh.getRange(idx+2, 1, 1, 5).setValues([row]);
    d.setDate(d.getDate()+1);
  }
}
function dayTotals_(shop, token, day) {
  var orders=0, gross=0, net=0;
  var url = 'https://'+shop+'/admin/api/'+CONFIG.API_VERSION+'/orders.json?status=any'
    + '&created_at_min='+day+'T00:00:00&created_at_max='+day+'T23:59:59'
    + '&limit=250&fields=id,total_price,subtotal_price,current_subtotal_price';
  while (url) {
    var res = UrlFetchApp.fetch(url, {headers:{'X-Shopify-Access-Token':token}, muteHttpExceptions:true});
    if (res.getResponseCode() !== 200) throw new Error('Shopify '+res.getResponseCode()+': '+res.getContentText());
    (JSON.parse(res.getContentText()).orders||[]).forEach(function(o){
      orders++; gross += +o.total_price||0; net += +(o.current_subtotal_price||o.subtotal_price||0);
    });
    var link = res.getHeaders()['Link']||res.getHeaders()['link']||'';
    var m = link.match(/<([^>]+)>;\s*rel="next"/); url = m ? m[1] : null;
  }
  return {orders:orders, gross:gross, net:net};
}

// ─────────────────────────── F2: Meta (fill tomorrow) ───────────────────────────
// Return current-month month-to-date ad spend, or null to fall back to MER_OVERRIDE.
function getMetaSpend() {
  var p = PropertiesService.getScriptProperties();
  var token = p.getProperty('META_TOKEN'), acct = p.getProperty('META_ACCOUNT_ID');
  if (!token || !acct) return null;                 // ← F2 not wired yet
  var since = Utilities.formatDate(new Date(new Date().getFullYear(), new Date().getMonth(), 1),
                                   Session.getScriptTimeZone(), 'yyyy-MM-dd');
  var until = dateNDaysAgo_(1);
  var url = 'https://graph.facebook.com/v20.0/'+acct+'/insights?fields=spend'
    + '&time_range={"since":"'+since+'","until":"'+until+'"}&access_token='+token;
  var res = UrlFetchApp.fetch(url, {muteHttpExceptions:true});
  if (res.getResponseCode() !== 200) return null;
  var d = JSON.parse(res.getContentText());
  return (d.data && d.data[0]) ? parseFloat(d.data[0].spend) : null;
}

// ─────────────────────────── F3: compute scorecard + forecast ───────────────────────────
function computeScorecard() {
  var tz = Session.getScriptTimeZone(), now = new Date();
  var mName = CONFIG.MONTHS[now.getMonth()], ym = Utilities.formatDate(now, tz, 'yyyy-MM');
  var dim = new Date(now.getFullYear(), now.getMonth()+1, 0).getDate();

  // current-month actuals from Daily Actuals
  var da = tab_('Daily Actuals', ['date','orders','gross','net','aov']);
  var rows = da.getLastRow()>1 ? da.getRange(2,1,da.getLastRow()-1,5).getValues() : [];
  var mtdNet=0, mtdOrders=0, days=0, lastDay=null, lastNet=0, lastAov=0;
  rows.forEach(function(r){
    if (String(r[0]).indexOf(ym)===0) {
      mtdNet += +r[3]; mtdOrders += +r[1]; days++;
      if (!lastDay || String(r[0])>lastDay) { lastDay=String(r[0]); lastNet=+r[3]; lastAov=+r[4]; }
    }
  });
  var fullRev = days ? Math.round(mtdNet/days*dim) : 0;
  var spend = getMetaSpend();
  var mer = spend && mtdNet ? spend/mtdNet : (CONFIG.MER_OVERRIDE[ym] || 0.30);
  var merSrc = spend ? 'real (Meta MTD)' : (CONFIG.MER_OVERRIDE[ym] ? 'model (EE)' : 'assumed');
  var vcr = CONFIG.VCR_BAU;
  var g = gp_(mer, vcr), gpamDollar = fullRev*g, netProfit = gpamDollar - CONFIG.FIXED_MONTHLY;
  var mtdAov = mtdOrders ? mtdNet/mtdOrders : 0;

  // write Scorecard tab
  var sc = tab_('Scorecard', ['metric','value','target','status']);
  sc.clearContents(); sc.appendRow(['metric','value','target','status']);
  sc.appendRow([mName+' net (MTD)', money_(mtdNet)+' ('+days+'d) → ~'+money_(fullRev), '', '']);
  sc.appendRow(['MER ('+merSrc+')', pct_(mer), '≤25%', mer<=0.25?'OK':'MISS']);
  sc.appendRow(['GPAM %', pct_(g), '≥26%', g>=CONFIG.GPAM_TARGET?'OK':'MISS']);
  sc.appendRow(['GPAM $ (month)', money_(gpamDollar), '> '+money_(CONFIG.FIXED_MONTHLY), gpamDollar>CONFIG.FIXED_MONTHLY?'OK':'LOSS']);
  sc.appendRow(['Net profit (month)', money_(netProfit), '> 0', netProfit>0?'OK':'LOSS']);
  sc.appendRow(['AOV (MTD)', money_(mtdAov), '', '']);
  sc.appendRow(['Last day '+(lastDay||''), money_(lastNet)+'  AOV '+money_(lastAov), '', '']);
  sc.appendRow(['Updated', Utilities.formatDate(now, tz, 'yyyy-MM-dd HH:mm'), '', '']);

  // write Forecast tab (both scenarios)
  writeForecast_(mName, fullRev, mer, vcr);
  return {mName:mName, mtdNet:mtdNet, days:days, fullRev:fullRev, mer:mer, merSrc:merSrc,
          gpam:g, gpamDollar:gpamDollar, netProfit:netProfit, mtdAov:mtdAov,
          lastDay:lastDay, lastNet:lastNet, lastAov:lastAov};
}
function writeForecast_(curName, curRev, curMer, curVcr) {
  var f = tab_('Forecast', []); f.clearContents();
  f.appendRow(['DiggerLid H2 forecast — GPAM target 26%. Two scenarios differ only on spend discipline.']);
  [['current','CURRENT TRAJECTORY',2],['target','TARGET DISCIPLINE',3]].forEach(function(sc){
    f.appendRow(['']); f.appendRow([sc[1]]);
    f.appendRow(['Mon','Rev(net)','MER','GPAM%','GPAM$','Net']);
    var tr=0,tg=0,tn=0, cg=gp_(curMer,curVcr);
    f.appendRow([curName, curRev, pct_(curMer), pct_(cg), Math.round(curRev*cg), Math.round(curRev*cg-CONFIG.FIXED_MONTHLY)]);
    tr+=curRev; tg+=curRev*cg; tn+=curRev*cg-CONFIG.FIXED_MONTHLY;
    Object.keys(CONFIG.FORWARD).forEach(function(m){
      var d=CONFIG.FORWARD[m], vcr=d[1]?CONFIG.VCR_SALE:CONFIG.VCR_BAU, mer=d[sc[2]], gg=gp_(mer,vcr);
      f.appendRow([m, d[0], pct_(mer), pct_(gg), Math.round(d[0]*gg), Math.round(d[0]*gg-CONFIG.FIXED_MONTHLY)]);
      tr+=d[0]; tg+=d[0]*gg; tn+=d[0]*gg-CONFIG.FIXED_MONTHLY;
    });
    f.appendRow(['H2', tr, '', pct_(tg/tr), Math.round(tg), Math.round(tn)]);
  });
}

// ─────────────────────────── F4: email the brief ───────────────────────────
function sendDailyBrief() {
  var s = computeScorecard();
  var to = PropertiesService.getScriptProperties().getProperty('BRIEF_TO');
  if (!to) throw new Error('Set BRIEF_TO in Script properties.');
  var cal = calendarDigest_();
  var flag = function(ok, warn){ return ok?'#1f8f52':(warn?'#b9790a':'#c23b3b'); };

  var html = '<div style="font-family:system-ui,Arial,sans-serif;max-width:640px;color:#15181c;line-height:1.5">'
    + '<p style="font:600 12px ui-monospace;letter-spacing:.1em;text-transform:uppercase;color:#888;margin:0">DiggerLid · daily brief</p>'
    + '<h2 style="margin:2px 0 12px">'+s.mName+' scorecard</h2>'
    + '<table style="border-collapse:collapse;width:100%;margin-bottom:16px">'
    + row_('Net sales (MTD)', money_(s.mtdNet)+' ('+s.days+'d) → ~'+money_(s.fullRev), '#15181c')
    + row_('MER ('+s.merSrc+')', pct_(s.mer), flag(s.mer<=0.25,true))
    + row_('GPAM %', pct_(s.gpam), flag(s.gpam>=CONFIG.GPAM_TARGET,true))
    + row_('GPAM $ (month)', money_(s.gpamDollar), flag(s.netProfit>0,true))
    + row_('Net profit (month)', money_(s.netProfit), flag(s.netProfit>0,true))
    + row_('AOV (MTD)', money_(s.mtdAov), '#15181c')
    + row_('Yesterday '+(s.lastDay||''), money_(s.lastNet)+' · AOV '+money_(s.lastAov), '#15181c')
    + '</table>'
    + '<p style="font:600 11px ui-monospace;letter-spacing:.08em;text-transform:uppercase;color:#888;margin:0 0 4px">Calendar</p>'
    + cal
    + '<p style="font-size:12px;color:#888;border-top:1px solid #ddd;padding-top:10px;margin-top:14px">'
    + 'Auto-generated from the live model + Shopify + /ai. MER source: '+s.merSrc
    + (s.merSrc==='model (EE)' ? ' — wire Meta (F2) to make it real.' : '.') + '</p></div>';

  MailApp.sendEmail({ to: to, subject: 'DiggerLid daily brief — '+s.mName+' '+(s.lastDay||''),
                      htmlBody: html, name: 'DiggerLid Ops Hub' });
}
function calendarDigest_() {
  try {
    var plan = JSON.parse(UrlFetchApp.fetch(CONFIG.CAL_URL, {muteHttpExceptions:true}).getContentText());
    var today = new Date(), soon = new Date(); soon.setDate(today.getDate()+7);
    var iso = function(d){ return Utilities.formatDate(d, Session.getScriptTimeZone(), 'yyyy-MM-dd'); };
    var up=[], next=null;
    (plan.calendar||[]).sort(function(a,b){return a.date<b.date?-1:1;}).forEach(function(x){
      if (x.date>=iso(today) && x.date<=iso(soon) && x.status!=='Done') up.push(x.date+' — '+x.name);
      if (!next && (x.tier==='major' || x.status==='In Progress') && x.date>=iso(today)) next=x;
    });
    var out='<div style="font-size:13.5px;margin-bottom:12px">';
    up.slice(0,6).forEach(function(u){ out+='• '+u+'<br>'; });
    if (next){ var t=Math.round((new Date(next.date)-today)/86400000); out+='<b>Next launch:</b> '+next.name+' — T-'+t+'d ('+next.date+')'; }
    return out+'</div>';
  } catch(e){ return '<div style="font-size:13px;color:#888">calendar feed unavailable</div>'; }
}

// ─────────────────────────── orchestrator + helpers ───────────────────────────
function dailyRun(){ dailyImport(); sendDailyBrief(); }   // compute runs inside sendDailyBrief

function gp_(mer,vcr){ return (1-vcr)-mer; }
function money_(n){ return 'A$'+Math.round(n).toLocaleString('en-AU'); }
function pct_(n){ return (n*100).toFixed(1)+'%'; }
function row_(k,v,color){ return '<tr><td style="padding:5px 0;border-bottom:1px solid #eee">'+k
  +'</td><td style="padding:5px 0;border-bottom:1px solid #eee;text-align:right;font-weight:600;color:'+color+'">'+v+'</td></tr>'; }
function dateNDaysAgo_(n){ var d=new Date(); d.setDate(d.getDate()-n);
  return Utilities.formatDate(d, Session.getScriptTimeZone(), 'yyyy-MM-dd'); }
function tab_(name, header){
  var ss=SpreadsheetApp.getActiveSpreadsheet(), sh=ss.getSheetByName(name);
  if (!sh){ sh=ss.insertSheet(name); if (header && header.length) sh.appendRow(header); }
  return sh;
}
