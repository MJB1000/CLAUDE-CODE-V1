// api/summarize.js
// AI-powered promo summarization via Claude API
// POST { "text": "raw promo text", "brand": "Brand Name", "market": "AU" }
// Returns { "summary": "One-line summary" }

const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY || "";
const SECRET = process.env.WIPER_INTEL_SECRET || "changeme";

async function callClaude(prompt) {
  const payload = JSON.stringify({
    model: "claude-haiku-4-5-20251001",
    max_tokens: 150,
    messages: [{ role: "user", content: prompt }],
  });

  const resp = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
    },
    body: payload,
  });

  if (!resp.ok) {
    const err = await resp.text();
    throw new Error(`Claude API ${resp.status}: ${err}`);
  }

  const data = await resp.json();
  return data.content?.[0]?.text || "";
}

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, X-API-Key");
  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });

  const apiKey = req.headers["x-api-key"] || req.query.key;
  if (apiKey !== SECRET) return res.status(401).json({ error: "Unauthorized" });

  if (!ANTHROPIC_API_KEY) {
    return res.status(503).json({ error: "ANTHROPIC_API_KEY not configured" });
  }

  let body;
  try { body = typeof req.body === "string" ? JSON.parse(req.body) : req.body; }
  catch { return res.status(400).json({ error: "Invalid JSON" }); }

  const { text, brand, market } = body;
  if (!text) return res.status(400).json({ error: "Missing 'text' field" });

  const prompt = `You are a competitive intelligence analyst for an Australian wiper blade company.
Summarize this competitor promotion in ONE concise sentence (max 80 chars).
Focus on: discount amount, what's included, any codes, urgency.

Brand: ${brand || "Unknown"}
Market: ${market || "AU"}
Raw promo text:
${text.substring(0, 500)}

One-line summary:`;

  try {
    const summary = await callClaude(prompt);
    return res.status(200).json({ ok: true, summary: summary.trim() });
  } catch (err) {
    console.error("[summarize] Claude API error:", err.message);
    return res.status(500).json({ error: "AI summary failed", detail: err.message });
  }
};
