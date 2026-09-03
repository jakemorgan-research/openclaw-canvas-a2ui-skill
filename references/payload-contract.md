# Payload contract

The `.json` teaching plans use two explicit profiles:

- `current-widget`: a synthetic HTML teaching plan whose `arguments` contain `title` and `widget_code`. Only that object can be adapted into a real tool call.
- `legacy-node`: action names only. **No payload is supplied or validated.** These plans are not executable calls and do not claim A2UI v0.8 compatibility.

For current A2UI, inspect the installed registered-source schema. This repository deliberately does not invent an A2UI envelope. [Dashboard A2UI reference](https://github.com/openclaw/openclaw/blob/main/docs/web/dashboards.md#a2ui-widgets).

Separately, [a2ui-v08-card.jsonl](../examples/a2ui-v08-card.jsonl) contains real v0.8 messages for the [standalone renderer demo](../docs/A2UI_DEMO.md). `surfaceUpdate`, `dataModelUpdate`, and `beginRendering` were exercised with the installed OpenClaw 2026.8.2 renderer. A later `dataModelUpdate` changes a bound text field. These messages have no version field; they are not v0.9 messages and are not a complete dashboard registration envelope. The existing sequence validator does not accept this JSONL format; the demo's tests check the fixed sample only.

The current HTML example requests no network, data feeds, prompt bridge, pinning, or automation. Validate it against the installed tool before sending. See [show_widget fields](https://github.com/openclaw/openclaw/blob/main/docs/tools/show-widget.md#use-the-tool).

Checked against upstream default-branch documentation on 2026-09-02, not a guarantee for a particular installed release.
