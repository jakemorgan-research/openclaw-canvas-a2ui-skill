"""Validate offline teaching plans, not live OpenClaw API calls."""
from __future__ import annotations
import json
import sys
from pathlib import Path

A2UI_PUSH = {"canvas.a2ui.push", "canvas.a2ui.pushJSONL"}
A2UI_RESET = "canvas.a2ui.reset"
LEGACY_ACTIONS = A2UI_PUSH | {A2UI_RESET, "canvas.present", "canvas.snapshot"}
MAX_BYTES = 1024 * 1024


def validate(document) -> list[str]:
    if not isinstance(document, dict):
        return ["plan must be a JSON object"]
    errors = []
    if set(document) - {"profile", "mode", "actions"}:
        errors.append("unknown plan field")
    profile, mode = document.get("profile"), document.get("mode")
    if not isinstance(profile, str) or profile not in {"legacy-node", "current-widget"}:
        return errors + ["profile must be legacy-node or current-widget"]
    actions = document.get("actions")
    if not isinstance(actions, list) or not actions or len(actions) > 32:
        return errors + ["actions must contain 1 to 32 items"]
    if any(not isinstance(a, dict) or not isinstance(a.get("action"), str) for a in actions):
        return errors + ["each action must be an object with a string action"]
    names = [a["action"] for a in actions]
    if profile == "current-widget":
        if mode != "widget" or names != ["show_widget"]:
            errors.append("current-widget requires widget mode and one show_widget action")
        for action in actions:
            if set(action) - {"action", "arguments"}:
                errors.append("unknown widget action field")
            args = action.get("arguments")
            if not isinstance(args, dict):
                errors.append("widget arguments must be an object")
                continue
            if set(args) != {"title", "widget_code"}:
                errors.append("teaching widget allows only title and widget_code; no capability requests")
            for key, limit in (("title", 80), ("widget_code", 48000)):
                value = args.get(key)
                try:
                    valid = isinstance(value, str) and bool(value.strip()) and len(value.encode("utf-8")) <= limit
                except UnicodeError:
                    valid = False
                if not valid:
                    errors.append(f"invalid or oversized {key}")
        return errors
    if mode not in ("a2ui", "url"):
        errors.append("legacy-node mode must be a2ui or url")
    if any(set(a) != {"action"} for a in actions):
        errors.append("legacy plans are order-only; payloads and arguments are not supported")
    if any(name not in LEGACY_ACTIONS for name in names):
        errors.append("unknown legacy action")
    if mode == "a2ui":
        if "canvas.present" in names:
            errors.append("legacy minimal-order convention excludes canvas.present in A2UI mode")
        push = next((i for i, name in enumerate(names) if name in A2UI_PUSH), None)
        if push is None or not (push == 0 or (push == 1 and names[0] == A2UI_RESET)):
            errors.append("begin with a push, or one reset immediately followed by a push")
        if names.count(A2UI_RESET) > 1 or (A2UI_RESET in names and names[0] != A2UI_RESET):
            errors.append("one reset is allowed only before the first push")
    elif mode == "url":
        if names[0] != "canvas.present" or any(n in A2UI_PUSH or n == A2UI_RESET for n in names):
            errors.append("URL order must start with present and exclude A2UI")
    return errors


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("usage: validate_sequence.py <sequence.json>")
        return 2
    try:
        with Path(argv[0]).open("rb") as stream:
            raw = stream.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("oversized")
        document = json.loads(raw.decode("utf-8-sig"))
    except (OSError, UnicodeError, ValueError, RecursionError):
        print("FAIL: unreadable, oversized, or invalid JSON input (contents withheld)")
        return 2
    errors = validate(document)
    if errors:
        print("FAIL\n" + "\n".join("- " + error for error in errors))
        return 1
    print("PASS: teaching plan only; live rendering and full payload schema are not checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
