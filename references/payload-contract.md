# Payload and version boundary

This Skill intentionally validates command order, not the complete A2UI schema.

Before relying on a payload in production:

1. Confirm the connected node advertises Canvas capability.
2. Check the current OpenClaw node documentation for the supported A2UI version and action names.
3. Validate the payload against the component/schema rules used by that OpenClaw version.
4. Run one small render before sending a complex surface.
5. Treat a local validator pass as preflight evidence only; the node result is the rendering evidence.

The repository examples target the current documented A2UI v0.8 action family as of 2026-08-31. Recheck upstream documentation when OpenClaw or the node changes.

