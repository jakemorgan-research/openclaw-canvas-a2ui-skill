# Safe skill customization

The narrow behavior change is:

> When the requested output is A2UI, push the A2UI payload directly and do not use `canvas.present` as a preparatory step.

Keep this as a small companion skill when possible. A companion is easier to inspect, update, remove, and compare with upstream behavior.

If a managed override is necessary:

1. Read the installed upstream skill and current OpenClaw documentation.
2. Copy only the minimum instructions required by the override policy.
3. Record the upstream version or commit.
4. Apply the ordering constraint above.
5. Validate a known-good and known-bad sequence.
6. Keep a rollback copy outside any public repository.

Never silently replace bundled files. Never include a user's complete local configuration or backup in a reusable skill.

