# Preflight contract

This validator checks a small **teaching-plan format**, not full API correctness.

| Input | Expected |
| --- | --- |
| `widget-good.json` | PASS: current HTML plan |
| `a2ui-good.json` | PASS: historical syntax only; not executable |
| `a2ui-reset-good.json` | PASS: historical syntax only; not executable |
| `url-good.json` | PASS: historical syntax only; not executable |
| `a2ui-bad-present-first.json` | FAIL: lab's minimal-order convention |
| Wrong root type, unknown action/profile, missing widget fields | FAIL |

```text
python scripts/validate_sequence.py examples/widget-good.json
python scripts/validate_sequence.py examples/a2ui-good.json
python scripts/validate_sequence.py examples/a2ui-reset-good.json
python scripts/validate_sequence.py examples/url-good.json
python -m unittest discover -s tests -v
```

The above commands should pass. Run this negative example separately; **exit code 1 is expected**:

```text
python scripts/validate_sequence.py examples/a2ui-bad-present-first.json
```

CLI exits: 0 accepted plan; 1 rejected plan; 2 usage, encoding, size, or JSON input error. Maximum input is 1 MiB. Error output omits file contents. This tool does not connect to OpenClaw, execute HTML, or verify renderer/schema compatibility.

For `check_capabilities.py`, exit 0 means a current route was selected, exit 1 means `stop`, and exit 2 means invalid or unreadable input. A route selection is still preflight evidence, not proof of visible output.
