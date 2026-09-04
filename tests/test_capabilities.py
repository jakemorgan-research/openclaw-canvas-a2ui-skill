import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_capabilities import main, select_route


class CapabilityGateTests(unittest.TestCase):
    def report(self, **changes):
        value = {"showWidget": False, "dashboardA2UI": False, "nodePanel": False,
                 "legacyActions": False, "renderer": None}
        value.update(changes)
        return value

    def test_dashboard_requires_renderer(self):
        self.assertEqual(select_route(self.report(dashboardA2UI=True, renderer="a2ui-v0.8")), "dashboard-a2ui")
        self.assertEqual(select_route(self.report(dashboardA2UI=True, renderer="none")), "stop")

    def test_legacy_actions_alone_stop(self):
        self.assertEqual(select_route(self.report(legacyActions=True, renderer="none")), "stop")

    def test_current_widget_routes_remain_separate(self):
        self.assertEqual(select_route(self.report(showWidget=True)), "inline-widget")
        self.assertEqual(select_route(self.report(nodePanel=True)), "node-panel")

    def test_unknown_or_bad_fields_fail_closed(self):
        for value in (None, [], {}, {**self.report(), "nodeId": "private"}, self.report(showWidget="yes")):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    select_route(value)

    def test_repository_examples(self):
        root = Path(__file__).resolve().parents[1] / "examples"
        dashboard = json.loads((root / "capability-dashboard.json").read_text(encoding="utf-8"))
        no_renderer = json.loads((root / "capability-node-no-renderer.json").read_text(encoding="utf-8"))
        self.assertEqual(select_route(dashboard), "dashboard-a2ui")
        self.assertEqual(select_route(no_renderer), "stop")

    def test_cli_exit_codes(self):
        self.assertEqual(main([]), 2)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "report.json"
            path.write_text(json.dumps(self.report(legacyActions=True, renderer="none")), encoding="utf-8")
            self.assertEqual(main([str(path)]), 1)
            path.write_text("{", encoding="utf-8")
            self.assertEqual(main([str(path)]), 2)
