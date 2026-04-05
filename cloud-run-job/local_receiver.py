#!/usr/bin/env python3
"""Minimal HTTP server that captures POST payloads for dry-run testing."""
import json, os, sys
from http.server import HTTPServer, BaseHTTPRequestHandler

CAPTURE_FILE = os.path.join(os.path.dirname(__file__), "output", "last_payload.json")

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
            os.makedirs(os.path.dirname(CAPTURE_FILE), exist_ok=True)
            with open(CAPTURE_FILE, "w") as f:
                json.dump(data, f, indent=2)
            sites = data.get("sites", [])
            print(f"\n{'='*60}")
            print(f"CAPTURED: {len(sites)} brands, date={data.get('date')}")
            for s in sites:
                flag = "SALE" if s.get("is_on_sale") else "    "
                dur = f"{s.get('fetch_duration_ms',0)}ms"
                rend = s.get("renderer", "http")
                print(f"  [{flag}] {s['name']:25s} intensity={s.get('promotion_intensity',0):3d}  {dur:>7s}  ({rend})")
            summary = data.get("landscape_summary", "")
            if summary:
                print(f"\nAI Analysis: {summary}")
            print(f"{'='*60}")
            print(f"Payload saved to {CAPTURE_FILE}")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "date": data.get("date"), "brands_processed": len(sites), "new_alerts": 0, "alerts": []}).encode())
        except Exception as e:
            print(f"ERROR: {e}", file=sys.stderr)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'{"error":"capture failed"}')

    def log_message(self, fmt, *args):
        pass  # Suppress default logging

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
    print(f"Local ingest receiver listening on http://localhost:{port}/api/ingest")
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
