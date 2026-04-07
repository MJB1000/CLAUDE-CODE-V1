// api/sheets-setup.js
// One-time setup: creates the Google Sheet with tabs + headers in the user's Drive
// POST /api/sheets-setup → creates sheet, stores ID, returns URL
// GET  /api/sheets-setup → returns current sheet ID/URL

const { kv } = require("./_kv");
const crypto = require("crypto");

const SECRET = process.env.WIPER_INTEL_SECRET || "changeme";
const SERVICE_ACCOUNT = process.env.GOOGLE_SERVICE_ACCOUNT || "";
const SHARE_WITH = process.env.GOOGLE_SHEETS_SHARE_EMAIL || "";

async function getAccessToken() {
  if (!SERVICE_ACCOUNT) return null;
  let creds;
  try { creds = JSON.parse(SERVICE_ACCOUNT); } catch { return null; }

  const header = Buffer.from(JSON.stringify({ alg: "RS256", typ: "JWT" })).toString("base64url");
  const now = Math.floor(Date.now() / 1000);
  const payload = Buffer.from(JSON.stringify({
    iss: creds.client_email,
    scope: "https://www.googleapis.com/auth/spreadsheets https://www.googleapis.com/auth/drive",
    aud: "https://oauth2.googleapis.com/token",
    iat: now, exp: now + 3600,
  })).toString("base64url");

  const sign = crypto.createSign("RSA-SHA256");
  sign.update(`${header}.${payload}`);
  const signature = sign.sign(creds.private_key, "base64url");
  const jwt = `${header}.${payload}.${signature}`;

  const tokenRes = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion=${jwt}`,
  });
  const tokenData = await tokenRes.json();
  return tokenData.access_token;
}

async function gapi(method, url, token, body) {
  const res = await fetch(url, {
    method,
    headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  return res.json();
}

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, X-API-Key");
  if (req.method === "OPTIONS") return res.status(200).end();

  const apiKey = req.headers["x-api-key"] || req.query.key;
  if (apiKey !== SECRET) return res.status(401).json({ error: "Unauthorized" });

  // GET — check status
  if (req.method === "GET") {
    const sheetId = await kv.get("sheets:spreadsheet_id").catch(() => null);
    return res.status(200).json({ configured: !!sheetId, spreadsheet_id: sheetId });
  }

  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });

  if (!SERVICE_ACCOUNT) {
    return res.status(400).json({ error: "GOOGLE_SERVICE_ACCOUNT env var not set" });
  }

  // Check if already set up
  const existing = await kv.get("sheets:spreadsheet_id").catch(() => null);
  if (existing) {
    return res.status(200).json({ ok: true, already_exists: true, spreadsheet_id: existing,
      url: `https://docs.google.com/spreadsheets/d/${existing}` });
  }

  try {
    const token = await getAccessToken();
    if (!token) return res.status(500).json({ error: "Failed to get access token", sa_email: (() => { try { return JSON.parse(SERVICE_ACCOUNT).client_email } catch { return "parse_failed" } })(), sa_len: SERVICE_ACCOUNT.length });

    // Create spreadsheet
    const spreadsheet = await gapi("POST", "https://sheets.googleapis.com/v4/spreadsheets", token, {
      properties: { title: "Wiper Intel — Price Tracker" },
      sheets: [
        { properties: { title: "Brands", index: 0 } },
        { properties: { title: "Prices", index: 1 } },
        { properties: { title: "Alerts", index: 2 } },
      ],
    });

    const sheetId = spreadsheet.spreadsheetId;
    if (!sheetId) return res.status(500).json({ error: "Failed to create spreadsheet", detail: spreadsheet });

    // Add header rows
    const headers = {
      Brands: ["Timestamp", "Brand ID", "Brand Name", "Market", "Website", "Category", "Reference Product", "Competitors Count", "Competitors"],
      Prices: ["Date", "Brand ID", "Competitor ID", "Competitor Name", "Market", "Price", "Period Type", "Period Label", "On Sale", "Intensity"],
      Alerts: ["Timestamp", "Type", "Brand", "Market", "Message", "Detail"],
    };
    for (const [tab, row] of Object.entries(headers)) {
      await gapi("POST",
        `https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/values/${tab}!A1:append?valueInputOption=USER_ENTERED&insertDataOption=OVERWRITE`,
        token, { values: [row] });
    }

    // Share with user if email configured
    if (SHARE_WITH) {
      await gapi("POST", `https://www.googleapis.com/drive/v3/files/${sheetId}/permissions`, token, {
        type: "user", role: "writer", emailAddress: SHARE_WITH,
      });
    }

    // Store the sheet ID
    await kv.set("sheets:spreadsheet_id", sheetId);

    return res.status(201).json({
      ok: true,
      spreadsheet_id: sheetId,
      url: `https://docs.google.com/spreadsheets/d/${sheetId}`,
      shared_with: SHARE_WITH || null,
    });
  } catch (err) {
    return res.status(500).json({ error: err.message || "Failed to create sheet" });
  }
};
