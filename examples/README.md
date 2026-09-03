# Try the smallest artifact

[Home](../README.md)

1. Download or clone the repository with any required access permission.
2. Open `widget-preview.html` in a browser. You should see a card with three readiness checks.
3. Run `python scripts/validate_sequence.py examples/widget-good.json` from the repository root.
4. In an authorized widget-capable OpenClaw session, inspect the installed tool schema.
5. Supply only `actions[0].arguments` to `show_widget`. Do not paste the outer plan as a tool call.
6. Inspect the result and visible card. This final integration step is not automated or claimed as tested here.

The preview shares the exact card markup with the current widget plan, but uses its own preview stylesheet. It is **not an A2UI rendering sample**.

The four legacy JSON plans contain no payload. They teach the lab's action-order contract only. The bad-present-first plan must fail locally; that does not establish a universal upstream bug.

## Ready for real A2UI?

Use [a2ui-v08-card.jsonl](a2ui-v08-card.jsonl) with the [four-step renderer demo](../docs/A2UI_DEMO.md). Unlike the legacy plans, this file contains real v0.8 component/data/render messages. The demo was observed displaying and updating with the installed OpenClaw 2026.8.2 renderer. No renderer is bundled and no model or Gateway is required.
