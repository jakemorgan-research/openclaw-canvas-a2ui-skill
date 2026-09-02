# Reproduce an empty or waiting Canvas

## Minimal comparison

Run two controlled tests against the same Canvas-capable node.

### Control: direct A2UI push

1. Send a small valid payload with `canvas.a2ui.push` or `canvas.a2ui.pushJSONL`.
2. Record the returned status.
3. Capture one snapshot only if the command reports success but the surface looks wrong.

### Suspect sequence: present before push

1. Start with `canvas.present` without a URL or HTML surface.
2. Push the same A2UI payload.
3. Compare the returned status and visual state with the control.

If the control succeeds and the suspect sequence does not, treat action ordering as the leading cause. If both fail, check node selection, advertised capabilities, payload validity, and version compatibility before changing the skill.

## Evidence to keep

- OpenClaw version
- Selected node and advertised capability, with private identifiers removed
- Ordered action names
- Sanitized result codes
- One redacted snapshot when it materially helps diagnosis

Do not publish raw logs or screenshots containing account, network, device, or session details.

