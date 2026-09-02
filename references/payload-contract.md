# Payload contract

The examples use two explicit profiles:

- `current-widget`: a synthetic HTML teaching plan whose `arguments` contain `title` and `widget_code`. Only that object can be adapted into a real tool call.
- `legacy-node`: action names only. **No payload is supplied or validated.** These plans are not executable calls and do not claim A2UI v0.8 compatibility.

For current A2UI, inspect the installed registered-source schema. This repository deliberately does not invent an A2UI envelope. [Dashboard A2UI reference](https://github.com/openclaw/openclaw/blob/main/docs/web/dashboards.md#a2ui-widgets).

The current HTML example requests no network, data feeds, prompt bridge, pinning, or automation. Validate it against the installed tool before sending. See [show_widget fields](https://github.com/openclaw/openclaw/blob/main/docs/tools/show-widget.md#use-the-tool).

Checked against upstream default-branch documentation on 2026-09-02, not a guarantee for a particular installed release.
