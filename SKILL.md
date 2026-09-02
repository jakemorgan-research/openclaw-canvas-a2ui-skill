---
name: openclaw-canvas-a2ui-skill
description: Create and diagnose OpenClaw Canvas/A2UI flows with capability checks, minimal rendering sequences, and evidence-based validation. Use for empty Canvas, waiting, Unknown, push/present ordering, A2UI JSONL, or Canvas node-selection problems; do not use for unrelated web UI development.
---

# OpenClaw Canvas A2UI

Use the smallest valid Canvas command sequence. Decide the rendering mode before issuing any Canvas action.

## Workflow

1. Confirm that the selected node advertises Canvas capability.
2. Choose exactly one rendering mode:
   - A2UI text: `canvas.a2ui.push`
   - A2UI JSONL: `canvas.a2ui.pushJSONL`
   - URL or HTML surface: `canvas.present`
3. For A2UI, send the payload first. Do not open an empty Canvas with `canvas.present`.
4. Use `canvas.a2ui.reset` only when the user requests a clean surface or stale state is demonstrated; follow it immediately with a push.
5. Check the command result. Take a snapshot only when visual evidence is necessary.
6. If the result is waiting, Unknown, or empty, compare the actual sequence with [references/mode-selection.md](references/mode-selection.md) and [references/validation.md](references/validation.md).

## Safety boundaries

- Never expose tokens, local paths, device names, IP addresses, session identifiers, logs, or private screenshots.
- Do not overwrite OpenClaw's bundled Canvas skill automatically. Prefer this companion skill or a reviewed managed override.
- Do not invent successful rendering. Report the returned command status and label anything not observed as unverified.
- Ask before changing node configuration or replacing an existing managed skill.

## Included resources

- `scripts/validate_sequence.py`: checks a proposed command sequence before execution.
- `examples/a2ui-good.json`: minimal valid A2UI example.
- `examples/a2ui-bad-present-first.json`: intentionally invalid teaching example.
- `references/reproduction.md`: short reproduction and diagnosis flow.
- `references/skill-design.md`: safe customization guidance.
- `references/payload-contract.md`: payload/version boundaries and what must still be verified upstream.
