"""Serve a synthetic A2UI v0.8 demo with an explicitly selected installed renderer.

No renderer is bundled or downloaded. Binds to loopback; no Gateway, credentials,
model call, private config, directory listing, or automatic browser launch.
"""
import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "examples" / "a2ui-v08-card.jsonl"
MAX_RENDERER = 8 * 1024 * 1024

PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>A2UI renderer acceptance</title>
<style>
body{margin:0;background:#102c43;color:#f3fafc;font:18px/1.6 system-ui,sans-serif}
main{max-width:900px;margin:30px auto;padding:24px}
h1{font-size:32px}p{color:#c6d9e5}
button{padding:12px 20px;font:inherit;border:0;border-radius:8px;background:#7fe0cd;color:#102c43}
button:disabled{opacity:.5}
#frame{margin-top:24px;border:1px solid #426177;border-radius:16px;min-height:260px;padding:20px}
openclaw-a2ui-host{display:block;min-height:220px}
#result{color:#7fe0cd}
</style></head><body><main>
<h1>Real A2UI renderer / synthetic data</h1>
<p>Uses your selected OpenClaw renderer. Not a Gateway session or an agent turn.</p>
<button id="update" disabled>Apply synthetic update</button>
<p id="result" role="status">Loading renderer and sample...</p>
<div id="frame"></div>
<p>No credentials, private configuration, or external service requests.</p>
<script>
(async () => {
  const status = document.getElementById('result');
  try {
    const response = await fetch('/sample.jsonl');
    if (!response.ok) throw new Error('sample unavailable');
    const messages = (await response.text()).trim().split(/\\r?\\n/).map(line => JSON.parse(line));
    globalThis.openclawA2UIBoot = {messages, actionTier:'state'};
    const script = document.createElement('script');
    script.src = '/renderer.js';
    script.onerror = () => {status.textContent='FAIL: renderer could not load';};
    script.onload = async () => {
      try {
      if (!customElements.get('openclaw-a2ui-host')) {
        status.textContent='FAIL: selected bundle does not provide the expected host'; return;
      }
      const host = document.createElement('openclaw-a2ui-host');
      document.getElementById('frame').appendChild(host);
      await host.updateComplete;
      const surfaces = globalThis.openclawA2UI.getSurfaces();
      if (!surfaces.includes('demo')) { status.textContent='FAIL: demo surface was not created'; return; }
      status.textContent='Surface created. Verify the card text below.';
      document.getElementById('update').disabled=false;
      document.getElementById('update').onclick=async()=>{
        try {
        globalThis.openclawA2UI.applyMessages([{dataModelUpdate:{surfaceId:'demo',path:'/',contents:[{key:'message',valueString:'Synthetic update received'}]}}]);
        await host.updateComplete;
        status.textContent='Update submitted. Verify that the card text changed.';
        } catch (_) {status.textContent='FAIL: data update was rejected';}
      };
      } catch (_) {status.textContent='FAIL: renderer initialization failed';}
    };
    document.head.appendChild(script);
  } catch (_) { status.textContent='FAIL: sample could not load'; }
})();
</script></main></body></html>"""


def validate_sample(text):
    messages = [json.loads(line) for line in text.splitlines() if line.strip()]
    if len(messages) != 3:
        raise ValueError("sample requires exactly three messages")
    keys = [list(message) if isinstance(message, dict) else [] for message in messages]
    if keys != [["surfaceUpdate"], ["dataModelUpdate"], ["beginRendering"]]:
        raise ValueError("unexpected sample message order")
    for message in messages:
        payload = next(iter(message.values()))
        if not isinstance(payload, dict) or payload.get("surfaceId") != "demo":
            raise ValueError("sample surface must be demo")
    components = messages[0]["surfaceUpdate"].get("components")
    if not isinstance(components, list) or {c.get("id") for c in components if isinstance(c, dict)} != {"root", "heading", "status"}:
        raise ValueError("sample needs root, heading and status components")
    if messages[2]["beginRendering"].get("root") != "root":
        raise ValueError("sample render root must be root")
    return messages


def make_handler(renderer, sample):
    resources = {
        "/": ("text/html; charset=utf-8", PAGE.encode("utf-8")),
        "/renderer.js": ("text/javascript; charset=utf-8", renderer),
        "/sample.jsonl": ("application/x-ndjson; charset=utf-8", sample),
    }

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            item = resources.get(self.path)
            if item is None:
                self.send_error(404)
                return
            mime, payload = item
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Security-Policy", "default-src 'none'; script-src 'self' 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'self'; base-uri 'none'; form-action 'none'")
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, *_args):
            pass
    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--renderer", required=True, type=Path, help="installed a2ui.bundle.js; never supply a private config file")
    parser.add_argument("--port", type=int, default=8768)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be 1 to 65535")
    if args.renderer.name != "a2ui.bundle.js":
        parser.error("select the installed v0.8 a2ui.bundle.js")
    try:
        if args.renderer.stat().st_size > MAX_RENDERER:
            raise ValueError("oversized")
        renderer = args.renderer.read_bytes()
        sample = SAMPLE.read_bytes()
        validate_sample(sample.decode("utf-8"))
        if b"openclaw-a2ui-host" not in renderer:
            raise ValueError("host missing")
        server = HTTPServer(("localhost", args.port), make_handler(renderer, sample))
    except (OSError, UnicodeError, ValueError):
        parser.exit(1, "Cannot open the selected renderer/sample or bind the port; private paths withheld.\n")
    print(f"Open http://localhost:{args.port}/ ; stop with Ctrl+C.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
