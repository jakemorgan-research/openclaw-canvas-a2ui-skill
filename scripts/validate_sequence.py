#!/usr/bin/env python3
"""Validate a proposed OpenClaw Canvas command sequence."""

from __future__ import annotations

import json
import sys
from pathlib import Path


A2UI_PUSH = {"canvas.a2ui.push", "canvas.a2ui.pushJSONL"}
A2UI_RESET = "canvas.a2ui.reset"


def validate(document: dict) -> list[str]:
    errors: list[str] = []
    mode = document.get("mode")
    actions = document.get("actions")

    if mode not in {"a2ui", "url"}:
        errors.append("mode must be 'a2ui' or 'url'")
    if not isinstance(actions, list) or not actions:
        errors.append("actions must be a non-empty list")
        return errors

    names = [item.get("action") if isinstance(item, dict) else None for item in actions]
    if any(not isinstance(name, str) or not name for name in names):
        errors.append("every action must have a non-empty action name")
        return errors

    if mode == "a2ui":
        if "canvas.present" in names:
            errors.append("A2UI mode must not contain canvas.present")
        first_push = next((index for index, name in enumerate(names) if name in A2UI_PUSH), None)
        if first_push is None:
            errors.append("A2UI mode requires canvas.a2ui.push or canvas.a2ui.pushJSONL")
        elif first_push == 0:
            pass
        elif first_push == 1 and names[0] == A2UI_RESET:
            pass
        else:
            errors.append("A2UI mode must begin with a push, or one reset followed immediately by a push")
        if names.count(A2UI_RESET) > 1:
            errors.append("A2UI mode allows at most one reset in a minimal sequence")
        if A2UI_RESET in names and names.index(A2UI_RESET) != 0:
            errors.append("canvas.a2ui.reset must appear before the first push")
        if "canvas.snapshot" in names and first_push is not None and names.index("canvas.snapshot") < first_push:
            errors.append("canvas.snapshot must not appear before the first A2UI push")
    elif mode == "url":
        if names[0] != "canvas.present":
            errors.append("URL mode must begin with canvas.present")
        if any(name in A2UI_PUSH or name == A2UI_RESET for name in names):
            errors.append("URL mode must not mix in A2UI push or reset actions")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_sequence.py <sequence.json>")
        return 2

    path = Path(sys.argv[1])
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot read valid JSON: {exc}")
        return 2

    errors = validate(document)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS: {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
