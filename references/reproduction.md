# Reproduce without guessing

1. Record sanitized versions and available tool/action names.
2. Select the current supported surface. Do not execute legacy node A2UI commands from action discovery alone.
3. Validate the synthetic plan locally.
4. With permission, adapt the minimal payload to the installed schema and render on a non-sensitive surface.
5. Compare the returned status with visible output.

| Observation | Next check |
| --- | --- |
| Tool missing | Check the active client capability and installed version |
| Preflight fails | Fix the plan using the stated profile contract |
| Legacy actions advertised, renderer `none` | Stop; this is not a render-capable route |
| Command accepted, surface empty | Check the current dashboard/presenter route and renderer availability; do not claim success |
| Partial result | Inspect existing state before retrying; avoid duplicate pinning |
| Caller timeout | Check final status before repeating a mutating action |

The legacy plans can compare archived traces offline. They do not authorize direct push, reset, or present operations. Reproducing a pinned old installation is a separate acceptance exercise and still requires a disposable surface plus visible renderer evidence.

Keep a short sanitized report with expected/observed results, profile, and remaining uncertainty. Never attach real node identifiers, raw logs, or account screenshots.
