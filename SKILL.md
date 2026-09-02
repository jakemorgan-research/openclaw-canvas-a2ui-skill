---
name: openclaw-canvas-a2ui-skill
description: Select and diagnose OpenClaw Canvas, dashboard A2UI, and widget flows using installed capabilities and version-specific contracts. Use for empty or unavailable surfaces, legacy push ordering, payload compatibility, or Canvas node selection; not general web development.
---

# OpenClaw Canvas and A2UI

Check the installed surface and tool schema before selecting a command. Do not turn a historical empty-Canvas case into a universal ordering rule.

## Decision flow

1. Record component versions and advertised tool/action names without personal or device identifiers.
2. Use [mode selection](references/mode-selection.md) to distinguish current session widgets, dashboard A2UI, native node panels, and legacy node A2UI.
3. For current HTML widgets, adapt the synthetic arguments in `examples/widget-good.json` to the installed `show_widget` schema. The outer plan is not tool input.
4. For current A2UI, read [payload contract](references/payload-contract.md). Do not send legacy node pushes to a dashboard or invent the registered-source envelope.
5. Only if the installed node advertises the legacy actions, use the legacy plans as order-only comparisons. Direct push is this lab's minimal convention, not an upstream ban on `canvas.present`.
6. Inspect the tool result and, when useful, the visible surface. A preflight pass, receipt, or timeout alone does not prove rendering. Diagnose using [reproduction](references/reproduction.md).

## Boundaries

- Never export private paths, identifiers, credentials, raw logs, or unredacted screenshots.
- Do not install/enable plugins, change permissions, reset surfaces, replace skills, or pin persistent widgets without authorization for that action.
- If a tool or capability is absent, stop at that boundary and explain the supported alternative; do not bypass it.
- Ask before a legacy reset that would remove existing content. A blank surface is not by itself proof that reset is needed.
- Offline validators check teaching contracts, not arbitrary-code security or complete A2UI schemas.
- For skill overrides read [safe customization](references/skill-design.md); preserve the user's chosen runtime.

## Completion

Report chosen surface, verified capability, preflight result, observed render (or unverified), and one bounded next check. Use [validation](references/validation.md) for expected outcomes.
