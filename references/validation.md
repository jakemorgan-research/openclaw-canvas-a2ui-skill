# Validation matrix

| Case | Expected result |
| --- | --- |
| A2UI mode begins with `canvas.a2ui.push` | Pass |
| A2UI mode begins with `canvas.a2ui.pushJSONL` | Pass |
| A2UI mode begins with one reset, then a push | Pass |
| A2UI mode contains `canvas.present` | Fail |
| URL mode begins with `canvas.present` | Pass |
| URL mode mixes in A2UI actions | Fail |
| Unknown mode or empty sequence | Fail |

Run locally:

```powershell
python scripts/validate_sequence.py examples/a2ui-good.json
python scripts/validate_sequence.py examples/a2ui-reset-good.json
python scripts/validate_sequence.py examples/url-good.json
python scripts/validate_sequence.py examples/a2ui-bad-present-first.json
```

The second command is expected to fail. That failure proves the guard catches the problematic ordering.

The validator checks ordering and mode separation. It does not connect to a node, validate every A2UI component field, or prove that a render occurred.
