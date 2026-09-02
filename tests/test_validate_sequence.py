import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_sequence import validate, main, MAX_BYTES


def sequence(mode, *actions):
    return {"profile": "legacy-node", "mode": mode, "actions": [{"action": a} for a in actions]}


class ValidateSequenceTests(unittest.TestCase):
    def test_positive_legacy(self):
        for doc in (sequence("a2ui", "canvas.a2ui.push", "canvas.snapshot"),
                    sequence("a2ui", "canvas.a2ui.reset", "canvas.a2ui.pushJSONL"),
                    sequence("url", "canvas.present", "canvas.snapshot")):
            with self.subTest(doc=doc):
                self.assertEqual(validate(doc), [])

    def test_negative_legacy(self):
        for mode, names in [
            ("a2ui", ["canvas.present", "canvas.a2ui.push"]),
            ("a2ui", ["canvas.a2ui.reset"]),
            ("a2ui", ["canvas.a2ui.push", "canvas.a2ui.reset"]),
            ("a2ui", ["canvas.snapshot", "canvas.a2ui.push"]),
            ("a2ui", ["canvas.a2ui.reset", "canvas.a2ui.reset", "canvas.a2ui.push"]),
            ("url", ["canvas.present", "canvas.a2ui.push"]),
            ("url", ["canvas.snapshot"]),
            ("url", ["canvas.present", "arbitrary.exec"]),
        ]:
            with self.subTest(names=names):
                self.assertTrue(validate(sequence(mode, *names)))

    def test_arbitrary_json_does_not_crash(self):
        for doc in (None, [], 42, "text", True, {}, {"profile": []},
                    {"profile": "legacy-node", "mode": [], "actions": [{"action": []}]}):
            with self.subTest(doc=doc):
                self.assertTrue(validate(doc))

    def test_unknown_fields_and_payload(self):
        doc = sequence("a2ui", "canvas.a2ui.push")
        doc["actions"][0]["payload"] = "not a schema"
        self.assertTrue(validate(doc))
        doc = sequence("url", "canvas.present")
        doc["unexpected"] = True
        self.assertTrue(validate(doc))

    def test_missing_profile(self):
        self.assertTrue(validate({"mode": "a2ui", "actions": [{"action": "canvas.a2ui.push"}]}))

    def test_empty_or_malformed_actions(self):
        for actions in ([], None, ["canvas.present"], [{"action": 2}], [{}]):
            doc = {"profile": "legacy-node", "mode": "url", "actions": actions}
            self.assertTrue(validate(doc))

    def widget(self):
        return {"profile": "current-widget", "mode": "widget",
                "actions": [{"action": "show_widget", "arguments":
                             {"title": "Synthetic card", "widget_code": "<p>Demo</p>"}}]}

    def test_widget(self):
        self.assertEqual(validate(self.widget()), [])

    def test_widget_rejects_capability_request(self):
        doc = self.widget()
        doc["actions"][0]["arguments"]["capabilities"] = {"tools": ["prompt"]}
        self.assertTrue(validate(doc))

    def test_widget_missing_or_bad_fields(self):
        for value in (None, [], {}, {"title": "X", "widget_code": ""}):
            doc = self.widget()
            doc["actions"][0]["arguments"] = value
            self.assertTrue(validate(doc))

    def test_profile_mix(self):
        doc = self.widget()
        doc["mode"] = "a2ui"
        self.assertTrue(validate(doc))

    def test_oversized_widget(self):
        doc = self.widget()
        doc["actions"][0]["arguments"]["widget_code"] = "x" * 48001
        self.assertTrue(validate(doc))

    def test_invalid_unicode_is_rejected(self):
        doc = self.widget()
        doc["actions"][0]["arguments"]["title"] = chr(0xD800)
        self.assertTrue(validate(doc))

    def test_preview_uses_same_card_without_scripts(self):
        root = Path(__file__).resolve().parents[1] / "examples"
        doc = json.loads((root / "widget-good.json").read_text(encoding="utf-8"))
        preview = (root / "widget-preview.html").read_text(encoding="utf-8")
        self.assertIn(doc["actions"][0]["arguments"]["widget_code"], preview)
        self.assertNotIn("<script", preview.lower())
        self.assertIn("default-src 'none'", preview)

    def test_cli_exit_codes(self):
        self.assertEqual(main([]), 2)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "plan.json"
            for data, expected in ((b"null", 1), (b"{", 2), (bytes([255]), 2),
                                   (b"x" * (MAX_BYTES + 1), 2),
                                   (json.dumps(self.widget()).encode(), 0)):
                path.write_bytes(data)
                self.assertEqual(main([str(path)]), expected)

    def test_repository_examples(self):
        root = Path(__file__).resolve().parents[1] / "examples"
        for path in root.glob("*-good.json"):
            with self.subTest(name=path.name):
                self.assertEqual(validate(json.loads(path.read_text(encoding="utf-8"))), [])
        self.assertTrue(validate(json.loads((root / "a2ui-bad-present-first.json").read_text())))
