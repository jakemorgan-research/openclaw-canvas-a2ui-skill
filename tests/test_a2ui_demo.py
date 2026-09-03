import json
import subprocess
import sys
import threading
import unittest
from http.client import HTTPConnection
from http.server import HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from serve_a2ui_demo import SAMPLE, PAGE, make_handler, validate_sample


class A2UIDemoTests(unittest.TestCase):
    def run_cli(self, *args):
        script = Path(__file__).resolve().parents[1] / "scripts" / "serve_a2ui_demo.py"
        return subprocess.run([sys.executable, str(script), *args], capture_output=True,
                              encoding="utf-8", timeout=10)

    def test_invalid_port_stops_without_serving(self):
        result = self.run_cli("--renderer", "a2ui.bundle.js", "--port", "0")
        self.assertEqual(result.returncode, 2)
        self.assertIn("port must be", result.stderr)

    def test_wrong_renderer_name_rejected(self):
        result = self.run_cli("--renderer", "a2ui-v0.9.bundle.js")
        self.assertEqual(result.returncode, 2)
        self.assertIn("select the installed v0.8", result.stderr)

    def test_missing_renderer_hides_path(self):
        missing = str(Path(__file__).resolve().parent / "absent-synthetic-folder" / "a2ui.bundle.js")
        result = self.run_cli("--renderer", missing)
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(missing, result.stderr)
        self.assertIn("private paths withheld", result.stderr)

    def test_real_sample_structure(self):
        self.assertEqual(len(validate_sample(SAMPLE.read_text(encoding="utf-8"))), 3)

    def test_bad_order_rejected(self):
        lines = SAMPLE.read_text(encoding="utf-8").splitlines()
        with self.assertRaises(ValueError):
            validate_sample("\n".join(reversed(lines)))

    def test_wrong_surface_rejected(self):
        with self.assertRaises(ValueError):
            validate_sample(SAMPLE.read_text(encoding="utf-8").replace('"demo"', '"other"'))

    def test_wrong_root_rejected(self):
        lines = SAMPLE.read_text(encoding="utf-8").splitlines()
        last = json.loads(lines[-1])
        last["beginRendering"]["root"] = "absent"
        lines[-1] = json.dumps(last)
        with self.assertRaises(ValueError):
            validate_sample("\n".join(lines))

    def test_http_routes_are_allowlisted(self):
        server = HTTPServer(("localhost", 0), make_handler(b"/* synthetic transport fixture */", b"{}\n"))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            for path, expected in [("/", 200), ("/renderer.js", 200), ("/sample.jsonl", 200),
                                   ("/../SKILL.md", 404), ("/private", 404), ("/?file=secret", 404)]:
                connection = HTTPConnection("localhost", server.server_port, timeout=3)
                connection.request("GET", path)
                response = connection.getresponse()
                self.assertEqual(response.status, expected)
                if expected == 200:
                    self.assertIn("default-src 'none'", response.getheader("Content-Security-Policy"))
                response.read()
                connection.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)

    def test_page_has_no_external_source(self):
        self.assertNotIn("https://", PAGE)
        self.assertIn("applyMessages", PAGE)
        self.assertIn("No credentials", PAGE)
