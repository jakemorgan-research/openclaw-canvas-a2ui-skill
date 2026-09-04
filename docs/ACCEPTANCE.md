# Recorded runtime acceptance

[Home](../README.md) · [Reproduce the renderer demo](A2UI_DEMO.md) · [Verification boundary](VERIFICATION.md)

Date: **2026-09-03**. Runtime: **OpenClaw 2026.8.2 (0965053)**, Node **24.15.0**, WSL2 on Windows. Browser: Codex in-app browser. No runtime upgrade, personal Gateway changes, model credentials, or account data were needed.

| Stage | Observed result |
| --- | --- |
| Clean source installation | Local tracked-files-only snapshot installed using `skills install <checkout> --global`; exit 0 |
| Skill discovery | `skills info openclaw-canvas-a2ui-skill --json`; exit 0, `eligible: true`, `disabled: false`, `source: openclaw-managed` |
| Real renderer | Used the installed v0.8 bundle; the `demo` surface and synthetic card appeared in the browser |
| Initial data | The card displayed `Synthetic data loaded` |
| Data update | Clicking the page button changed the card to `Synthetic update received` |
| Automated regression | 38 local Python test methods passed after adding the fail-closed capability gate; fixture and transport tests do not substitute for the observed renderer test |

Installation used fresh state, configuration, and workspace directories. The subprocess received only minimal runtime environment variables and isolated `OPENCLAW_STATE_DIR` / `OPENCLAW_CONFIG_PATH` values. The test did not read the user's normal configuration or sessions. Raw installation output can contain local paths and is deliberately not included here.

## Reproduce installation safely

1. Review the source and select a pinned commit. Use a disposable environment or your runtime's documented isolated state/configuration options, not a private production workspace.
2. With that isolation active, run `openclaw --version`, then `openclaw skills install . --global` from the reviewed checkout. `--global` refers to the managed skills area of the selected state; verify the destination before installing. Stop if a different skill would be overwritten.
3. Run `openclaw skills info openclaw-canvas-a2ui-skill --json`. Confirm the name, eligibility, enabled status, and expected installation source. Do not post raw output containing paths.
4. Run the [four-step renderer demo](A2UI_DEMO.md), then stop its server. Keep any screenshots synthetic-only.

Local source installation was tested. Authentication to a private Git source, model/agent invocation, Gateway-to-client delivery, full dashboard integration, and native Windows OpenClaw execution were **not** tested. This is an experimental skill and renderer lab, not a certified production integration. See [removal and rollback](DEVELOPER_GUIDE.md#delivery-boundary).
