# Verification boundary

Review date: 2026-09-03. Distribution: experimental source toolkit; visibility and Release publication require separate approval.

Local review: 38 Python test methods passed. The HTML card was inspected at desktop and narrow widths; original SVG diagrams were visually reviewed. Skill frontmatter and workflow/issue YAML parsed successfully. Repository and local reachable-history privacy scans reported no configured matches. [Recorded acceptance](ACCEPTANCE.md) adds isolated skill installation/discovery and a real v0.8 renderer display/update on OpenClaw 2026.8.2. These are local checks; inspect the current GitHub Actions run for remote CI evidence.

| Layer | Evidence / limit |
| --- | --- |
| Offline plan validation | Positive and negative synthetic cases in unit tests |
| CLI input handling | Wrong JSON types, invalid encoding, size limit, and exit codes covered |
| Documentation | Local link and SVG structure checks |
| HTML example | Separate offline HTML preview; not A2UI |
| A2UI example | Real installed v0.8 renderer displayed the synthetic JSONL card and a visible bound-data update; [reproduce](A2UI_DEMO.md) |
| Skill installation | Local clean source installed and discovered as eligible in isolated OpenClaw 2026.8.2 state |
| Current API guidance | Default-branch docs inspected; installed releases can differ |
| Legacy action plans | Order-only convention; not the new runnable v0.8 payload example |
| Live Gateway / node / dashboard | Not executed by this repository's CI; user acceptance still required |

Capability-gate regression covers a misleading real-world shape: legacy node actions advertised together with `renderer: none`. The expected result is `stop`, not a push attempt. Current upstream routing was rechecked on 2026-09-04. A separate local acceptance found Gateway health but no render-capable Windows node, so no end-to-end success is claimed.

## Before a public release

- Re-run privacy checks on tracked files, assets, and reachable history.
- Review both author/committer identities and any attachments.
- Reproduce the recorded runtime acceptance when changing the payload, supported runtime, or renderer harness.
- Record partial results honestly; model/Gateway/client integration remains outside the tested scope.
- Ensure installation, uninstall/rollback instructions, issue forms, and checks agree.
- Obtain explicit approval for visibility changes and Release creation.

No automatic scanner can certify the absence of all personal information. A quiet scan is supporting evidence, not a guarantee.
