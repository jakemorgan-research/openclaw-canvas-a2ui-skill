# Choose a compatible surface

[Home](../README.md) · [Contract](payload-contract.md)

| Observed capability | Route | Evidence required |
| --- | --- | --- |
| `show_widget` in the active session | Small HTML widget | Installed argument schema and visible output |
| Registered dashboard A2UI kind | Dashboard A2UI | Plugin availability and its current payload contract |
| Native widget-panel support | `show_widget` with `presentation.target: "node_panel"` | Eligible presenter and authorized presentation |
| Only node `canvas.a2ui.*` names are advertised | Stop; historical comparison only | Action names do not establish a renderer, dashboard route, or visible output |
| None of these | Explain unavailability | Do not invent a fallback action |

The old direct-push pattern is retained only for interpreting historical traces. The `legacy-node` JSON files are non-executable teaching records; a PASS from their syntax validator is never permission to push or reset a live node. If a separately maintained old installation must be reproduced, require its pinned documentation, a non-sensitive disposable surface, an actual non-`none` renderer, and visible output. Keep that acceptance outside the current dashboard workflow.

Run `python scripts/check_capabilities.py <report.json>` on a sanitized report when the fields are available. `legacyActions: true` alone returns `stop`; `renderer: "none"` can never select a render route.

Current routing evidence: [OpenClaw nodes](https://github.com/openclaw/openclaw/blob/main/docs/nodes/index.md#macos-widget-panel) and [dashboard A2UI](https://github.com/openclaw/openclaw/blob/main/docs/web/dashboards.md#a2ui-widgets). Rechecked 2026-09-04.
