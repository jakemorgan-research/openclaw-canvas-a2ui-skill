"""Select a current Canvas/widget route from a sanitized capability report."""
import json
import sys
from pathlib import Path

MAX_BYTES = 64 * 1024
FIELDS = {"showWidget", "dashboardA2UI", "nodePanel", "legacyActions", "renderer"}


def select_route(report):
    if not isinstance(report, dict) or set(report) != FIELDS:
        raise ValueError("report must contain only the five documented fields")
    if any(not isinstance(report[key], bool) for key in FIELDS - {"renderer"}):
        raise ValueError("capability flags must be booleans")
    renderer = report["renderer"]
    if renderer is not None and not isinstance(renderer, str):
        raise ValueError("renderer must be a string or null")
    if isinstance(renderer, str) and (not renderer.strip() or len(renderer) > 80):
        raise ValueError("renderer is empty or oversized")
    renderer_ready = isinstance(renderer, str) and renderer.lower() != "none"
    if report["dashboardA2UI"] and renderer_ready:
        return "dashboard-a2ui"
    if report["showWidget"]:
        return "inline-widget"
    if report["nodePanel"]:
        return "node-panel"
    return "stop"


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("usage: check_capabilities.py <sanitized-report.json>")
        return 2
    try:
        with Path(argv[0]).open("rb") as stream:
            raw = stream.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("oversized")
        route = select_route(json.loads(raw.decode("utf-8-sig")))
    except (OSError, UnicodeError, ValueError, RecursionError):
        print("FAIL: invalid or unreadable capability report (contents withheld)")
        return 2
    if route == "stop":
        print("STOP: no supported render route; advertised legacy actions are historical evidence only")
        return 1
    print("ROUTE: " + route + "; visible output still requires observation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
