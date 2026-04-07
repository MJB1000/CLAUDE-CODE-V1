// api/_sheets.js — Google Sheets logging via Sheets API v4
// Appends rows to a configured Google Sheet for audit/record keeping.
//
// Environment variables:
//   GOOGLE_SHEETS_ID          — the spreadsheet ID (or auto-loaded from KV)
//   GOOGLE_SERVICE_ACCOUNT    — JSON string of the service account credentials

const crypto = require("crypto");

let SHEETS_ID = process.env.GOOGLE_SHEETS_ID || "";
const SERVICE_ACCOUNT = process.env.GOOGLE_SERVICE_ACCOUNT || "";

let _cachedToken = null;
let _tokenExpiry = 0;

async function getAccessToken() {
  if (_cachedToken && Date.now() < _tokenExpiry) return _cachedToken;
  if (!SERVICE_ACCOUNT) return null;

  let creds;
  try { creds = JSON.parse(SERVICE_ACCOUNT); } catch { return null; }

  const header = Buffer.from(JSON.stringify({ alg: "RS256", typ: "JWT" })).toString("base64url");
  const now = Math.floor(Date.now() / 1000);
  const payload = Buffer.from(JSON.stringify({
    iss: creds.client_email,
    scope: "https://www.googleapis.com/auth/spreadsheets",
    aud: "https://oauth2.googleapis.com/token",
    iat: now, exp: now + 3600,
  })).toString("base64url");

  const sign = crypto.createSign("RSA-SHA256");
  sign.update(`${header}.${payload}`);
  const signature = sign.sign(creds.private_key, "base64url");
  const jwt = `${header}.${payload}.${signature}`;

  const res = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion=${jwt}`,
  });
  const data = await res.json();

  _cachedToken = data.access_token;
  _tokenExpiry = Date.now() + (data.expires_in - 60) * 1000;
  return _cachedToken;
}

async function appendRow(sheetName, rowData) {
  // Try loading sheet ID from KV if not set as env var
  if (!SHEETS_ID) {
    try {
      const { kv } = require("./_kv");
      SHEETS_ID = await kv.get("sheets:spreadsheet_id") || "";
    } catch { /* ignore */ }
  }
  if (!SHEETS_ID) return; // silently skip if not configured

  const token = await getAccessToken();
  if (!token) return; // no credentials configured

  const range = `${sheetName}!A:Z`;
  const url = `https://sheets.googleapis.com/v4/spreadsheets/${SHEETS_ID}/values/${encodeURIComponent(range)}:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS`;

  await fetch(url, {
    method: "POST",
    headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ values: [rowData] }),
  });
}

module.exports = { appendRow };
