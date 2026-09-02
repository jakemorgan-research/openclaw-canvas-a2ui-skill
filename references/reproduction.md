# Reproduce without guessing

1. Record sanitized versions and available tool/action names.
2. Select the matching profile. If only current widgets exist, do not test removed legacy commands.
3. Validate the synthetic plan locally.
4. With permission, adapt the minimal payload to the installed schema and render on a non-sensitive surface.
5. Compare the returned status with visible output.

| Observation | Next check |
| --- | --- |
| Tool missing | Check the active client capability and installed version |
| Preflight fails | Fix the plan using the stated profile contract |
| Command accepted, surface empty | Check payload and renderer availability; do not claim success |
| Partial result | Inspect existing state before retrying; avoid duplicate pinning |
| Caller timeout | Check final status before repeating a mutating action |

For legacy installations only, a direct push and an explicitly authorized present-then-push comparison can help test an ordering hypothesis. Change one variable at a time; a single comparison is not a universal root cause.

Keep a short sanitized report with expected/observed results, profile, and remaining uncertainty. Never attach real node identifiers, raw logs, or account screenshots.
