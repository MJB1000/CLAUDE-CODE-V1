// api/_sheets.js — Google Sheets logging via Sheets API v4
// Appends rows to a configured Google Sheet for audit/record keeping.
//
// Environment variables:
//   GOOGLE_SHEETS_ID          — the spreadsheet ID from the URL
//   GOOGLE_SERVICE_ACCOUNT    — JSON string of the service account credentials
//
// Each sheet tab (Brands, Prices, Alerts) is auto-created if needed.

const https = require("https");

const SHEETS_ID = process.env.GOOGLE_SHEETS_ID || "";
const SERVICE_ACCOUNT = process.env.GOOGLE_SERVICE_ACCOUNT || "";

let _cachedToken = null;
let _tokenExpiry = 0;

async function getAccessToken() {
  if (_cachedToken && Date.now() < _tokenExpiry) return _cachedToken;
  if (!SERVICE_ACCOUNT) return null;

  let creds;
  try { creds = JSON.parse(SERVICE_ACCOUNT); }
  catch { return null; }

  // Build JWT
  const header = Buffer.from(JSON.stringify({ alg: "RS256", typ: "JWT" })).toString("base64url");
  const now = Math.floor(Date.now() / 1000);
  const payload = Buffer.from(JSON.stringify({
    iss: creds.client_email,
    scope: "https://www.googleapis.com/auth/spreadsheets",
    aud: "https://oauth2.googleapis.com/token",
    iat: now,
    exp: now + 3600,
  })).toString("base64url");

  const crypto = require("crypto");
  const sign = crypto.createSign("RSA-SHA256");
  sign.update(`${header}.${payload}`);
  const signature = sign.sign(creds.private_key, "base64url");

  const jwt = `${header}.${payload}.${signature}`;

  // Exchange JWT for access token
  const tokenData = await postJSON("https://oauth2.googleapis.com/token", {
    grant_type: "urn:ietf:params:oauth:grant-type:jwt-bearer",
    assertion: jwt,
  });

  _cachedToken = tokenData.access_token;
  _tokenExpiry = Date.now() + (tokenData.expires_in - 60) * 1000;
  return _cachedToken;
}

function postJSON(url, data) {
  return new Promise((resolve, reject) => {
    const body = new URLSearchParams(data).toString();
    const parsed = new URL(url);
    const options = {
      hostname: parsed.hostname,
      path: parsed.pathname,
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded", "Content-Length": body.length },
    };
    const req = https.request(options, (res) => {
      let raw = "";
      res.on("data", d => raw += d);
      res.on("end", () => {
        try { resolve(JSON.parse(raw)); }
        catch { reject(new Error(raw)); }
      });
    });
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

async function appendRow(sheetName, rowData) {
  if (!SHEETS_ID) return; // silently skip if not configured

  const token = await getAccessToken();
  if (!token) return; // no credentials configured

  const range = `${sheetName}!A:Z`;
  const url = `https://sheets.googleapis.com/v4/spreadsheets/${SHEETS_ID}/values/${encodeURIComponent(range)}:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS`;

  return new Promise((resolve, reject) => {
    const body = JSON.stringify({ values: [rowData] });
    const parsed = new URL(url);
    const options = {
      hostname: parsed.hostname,
      path: `${parsed.pathname}${parsed.search}`,
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
        "Content-Length": Buffer.byteLength(body),
      },
    };
    const req = https.request(options, (res) => {
      let raw = "";
      res.on("data", d => raw += d);
      res.on("end", () => {
        try { resolve(JSON.parse(raw)); }
        catch { reject(new Error(raw)); }
      });
    });
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

module.exports = { appendRow };
