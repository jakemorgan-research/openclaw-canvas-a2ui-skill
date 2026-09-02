from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_sequence import validate  # noqa: E402


def sequence(mode: str, *actions: str) -> dict:
    return {"mode": mode, "actions": [{"action": action} for action in actions]}


class ValidateSequenceTests(unittest.TestCase):
    def test_direct_push_is_valid(self):
        self.assertEqual(validate(sequence("a2ui", "canvas.a2ui.push", "canvas.snapshot")), [])

    def test_reset_then_push_is_valid(self):
        self.assertEqual(validate(sequence("a2ui", "canvas.a2ui.reset", "canvas.a2ui.pushJSONL")), [])

    def test_present_before_push_is_rejected(self):
        self.assertTrue(validate(sequence("a2ui", "canvas.present", "canvas.a2ui.push")))

    def test_reset_without_push_is_rejected(self):
        self.assertTrue(validate(sequence("a2ui", "canvas.a2ui.reset")))

    def test_late_reset_is_rejected(self):
        self.assertTrue(validate(sequence("a2ui", "canvas.a2ui.push", "canvas.a2ui.reset")))

    def test_snapshot_before_push_is_rejected(self):
        self.assertTrue(validate(sequence("a2ui", "canvas.snapshot", "canvas.a2ui.push")))

    def test_url_present_is_valid(self):
        self.assertEqual(validate(sequence("url", "canvas.present", "canvas.snapshot")), [])

    def test_url_and_a2ui_mix_is_rejected(self):
        self.assertTrue(validate(sequence("url", "canvas.present", "canvas.a2ui.push")))


if __name__ == "__main__":
    unittest.main()

