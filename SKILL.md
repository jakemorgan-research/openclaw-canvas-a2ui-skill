---
name: openclaw-canvas-a2ui-skill
description: Select and diagnose OpenClaw Canvas, dashboard A2UI, and widget flows using installed capabilities and version-specific contracts. Use for empty or unavailable surfaces, historical A2UI traces, payload compatibility, or widget-panel selection; not general web development.
---

# OpenClaw Canvas and A2UI

Check the installed surface and tool schema before selecting a command. Do not turn a historical empty-Canvas case into a universal ordering rule.

## Decision flow

1. Record component versions and advertised tool/action names without personal or device identifiers.
2. Use [mode selection](references/mode-selection.md) to distinguish current session widgets, dashboard A2UI, native widget panels, and historical node-action traces. When given a sanitized capability report, run `python scripts/check_capabilities.py <report.json>` before choosing a route.
3. For current HTML widgets, adapt the synthetic arguments in `examples/widget-good.json` to the installed `show_widget` schema. The outer plan is not tool input.
4. For current A2UI, read [payload contract](references/payload-contract.md). For an authorized synthetic-only renderer test, follow [the runnable v0.8 demo](docs/A2UI_DEMO.md); it is tested with OpenClaw 2026.8.2, not proof of Gateway or agent integration. Do not send legacy node pushes to a dashboard or invent the registered-source envelope.
5. Treat the legacy JSON plans as offline historical-trace comparisons only. Never invoke node `canvas.a2ui.*` because those names are advertised: action discovery is not renderer evidence. Current upstream routing puts A2UI on session dashboards and uses `show_widget` with `presentation.target: "node_panel"` for an eligible native widget panel.
6. Inspect the tool result and, when useful, the visible surface. A preflight pass, receipt, or timeout alone does not prove rendering. Diagnose using [reproduction](references/reproduction.md).

## Boundaries

- Never export private paths, identifiers, credentials, raw logs, or unredacted screenshots.
- Do not install/enable plugins, change permissions, reset surfaces, replace skills, or pin persistent widgets without authorization for that action.
- If a tool or capability is absent, stop at that boundary and explain the supported alternative; do not bypass it.
- For an A2UI request, if capability evidence reports `renderer: none` or a missing dashboard A2UI registration, stop or offer a genuinely supported HTML-widget route. If no eligible widget presenter exists, do not target a native panel. A push receipt cannot upgrade any unsupported state into a visible render.
- Ask before a legacy reset that would remove existing content. A blank surface is not by itself proof that reset is needed.
- Offline validators check teaching contracts, not arbitrary-code security or complete A2UI schemas.
- For skill overrides read [safe customization](references/skill-design.md); preserve the user's chosen runtime.

## Completion

Report chosen surface, verified capability, preflight result, observed render (or unverified), and one bounded next check. Use [validation](references/validation.md) for expected outcomes.
