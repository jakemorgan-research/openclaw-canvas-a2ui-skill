# Choose a compatible surface

[Home](../README.md) · [Contract](payload-contract.md)

| Observed capability | Route | Evidence required |
| --- | --- | --- |
| `show_widget` in the active session | Small HTML widget | Installed argument schema and visible output |
| Registered dashboard A2UI kind | Dashboard A2UI | Plugin availability and its current payload contract |
| Native node panel support | Current node-panel route | Eligible device and authorized presentation |
| Legacy `canvas.a2ui.push` / `pushJSONL` | Legacy order comparison | Those exact actions advertised by the installed version |
| None of these | Explain unavailability | Do not invent a fallback action |

The old direct-push pattern is retained only for diagnosing older installations. In this lab's **legacy-node** profile, push first (or one authorized reset followed by push); `canvas.present` belongs to the separate URL plan. Failing that profile means the plan violates the lab convention, not that upstream forbids the sequence.

Current routing evidence: [OpenClaw nodes](https://github.com/openclaw/openclaw/blob/main/docs/nodes/index.md#macos-widget-panel).
