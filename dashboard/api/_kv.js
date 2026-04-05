// Shared KV client — uses @upstash/redis (replaces deprecated @vercel/kv)
const { Redis } = require("@upstash/redis");

const kv = new Redis({
  url: process.env.KV_REST_API_URL,
  token: process.env.KV_REST_API_TOKEN,
});

module.exports = { kv };
