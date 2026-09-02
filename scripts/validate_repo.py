#!/usr/bin/env python3
"""Run lightweight privacy and repository-readiness checks."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml", ".txt"}
REQUIRED = {
    "SKILL.md",
    "README.md",
    "LICENSE",
    "SECURITY.md",
    "agents/openai.yaml",
    "scripts/validate_sequence.py",
    "tests/test_validate_sequence.py",
    "examples/a2ui-reset-good.json",
    "examples/url-good.json",
}
PATTERNS = {
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "Chinese mobile number": re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    "private IPv4 range": re.compile(r"\b(?:10\.|192\.168\.|172\.(?:1[6-9]|2\d|3[01])\.)\d{1,3}(?:\.\d{1,3}){1,2}\b"),
    "Windows user path": re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+", re.I),
    "Unix home path": re.compile(r"/home/[^/\s]+", re.I),
    "secret assignment": re.compile(r"(?i)(?:api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}"),
}


def main() -> int:
    failures: list[str] = []
    for required in sorted(REQUIRED):
        if not (ROOT / required).is_file():
            failures.append(f"missing required file: {required}")

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if path.name == "validate_repo.py":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        relative = path.relative_to(ROOT)
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                failures.append(f"{relative}: possible {label}")

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: required files present; no configured privacy pattern matched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
