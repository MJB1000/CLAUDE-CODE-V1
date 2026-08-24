/**
 * DiggerLid — daily sales export into the Ecommerce Equation model (Google Sheets).
 * Free & autonomous: runs on a Google time-trigger, no server, no cost.
 * Appends yesterday's Shopify actuals to a "Daily Actuals" tab; your model reads from it.
 *
 * ── SETUP (once, ~10 min) ─────────────────────────────────────────────
 * 1. Shopify admin → Settings → Apps → Develop apps → Create app "DL Daily Export".
 *    Admin API access scopes: read_orders  (add read_reports too if you later want ShopifyQL).
 *    Install app → reveal & copy the Admin API access token (starts shpat_...).
 * 2. Open your EE model Google Sheet → Extensions → Apps Script → paste this file.
 * 3. Project Settings (gear) → Script properties → add two:
 *       SHOP           = digger-lid.myshopify.com
 *       SHOPIFY_TOKEN  = shpat_xxxxxxxx      (NEVER put the token in the code or in chat)
 * 4. Set the Sheet's timezone: File → Settings → Australia/Brisbane.
 * 5. Run dailyExport once → authorize when prompted.
 * 6. Triggers (clock icon) → Add trigger → function dailyExport → Time-driven →
 *    Day timer → 6–7am. Done — it now runs every morning by itself.
 *
 * Note: "net" here = sum of order subtotals (after discounts, before tax/shipping/returns).
 * It tracks Shopify's net_sales closely and consistently day-over-day, but isn't identical
 * (ShopifyQL also nets out returns). Good enough to drive the model; swap to the Analytics
 * API later if you want an exact match.
 */

var API_VERSION = '2024-10';

function dailyExport() {
  var props = PropertiesService.getScriptProperties();
  var shop  = props.getProperty('SHOP');
  var token = props.getProperty('SHOPIFY_TOKEN');
  if (!shop || !token) throw new Error('Set SHOP and SHOPIFY_TOKEN in Script Properties first.');

  var tz  = Session.getScriptTimeZone();               // set the Sheet tz to Australia/Brisbane
  var d   = new Date(); d.setDate(d.getDate() - 1);    // yesterday
  var day = Utilities.formatDate(d, tz, 'yyyy-MM-dd');
  var min = day + 'T00:00:00';
  var max = day + 'T23:59:59';

  var orders = 0, gross = 0, net = 0;
  var url = 'https://' + shop + '/admin/api/' + API_VERSION +
            '/orders.json?status=any&created_at_min=' + min + '&created_at_max=' + max +
            '&limit=250&fields=id,created_at,total_price,subtotal_price,current_subtotal_price';

  while (url) {
    var res  = UrlFetchApp.fetch(url, {headers: {'X-Shopify-Access-Token': token}, muteHttpExceptions: true});
    if (res.getResponseCode() !== 200) throw new Error('Shopify API ' + res.getResponseCode() + ': ' + res.getContentText());
    var data = JSON.parse(res.getContentText());
    (data.orders || []).forEach(function (o) {
      orders++;
      gross += parseFloat(o.total_price || 0);
      net   += parseFloat(o.current_subtotal_price || o.subtotal_price || 0);
    });
    var link = res.getHeaders()['Link'] || res.getHeaders()['link'] || '';
    var m = link.match(/<([^>]+)>;\s*rel="next"/);
    url = m ? m[1] : null;
  }

  var aov = orders ? net / orders : 0;

  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName('Daily Actuals');
  if (!sh) { sh = ss.insertSheet('Daily Actuals'); sh.appendRow(['date', 'orders', 'gross', 'net', 'aov']); }

  var existing = sh.getLastRow() > 1
    ? sh.getRange(2, 1, sh.getLastRow() - 1, 1).getValues().flat().map(String)
    : [];
  if (existing.indexOf(day) === -1) {
    sh.appendRow([day, orders, gross, net, aov]);
  } else {
    // idempotent: overwrite the existing row for that day (in case of a re-run)
    var row = existing.indexOf(day) + 2;
    sh.getRange(row, 1, 1, 5).setValues([[day, orders, gross, net, aov]]);
  }
}
