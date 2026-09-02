# OpenClaw Canvas A2UI Skill

An installable companion Skill for creating and diagnosing OpenClaw Canvas/A2UI flows without the common empty-Canvas ordering mistake.

> Status: private preview. The repository is intentionally not released or promoted yet.

## Choose the mode in 30 seconds

```text
A2UI payload?  yes -> optional reset only for stale state -> push -> verify
               no  -> URL/HTML surface -> present -> verify
```

## The one rule that prevents most confusion

```text
Incorrect A2UI flow                 Recommended A2UI flow

canvas.present                     canvas.a2ui.push / pushJSONL
      |                                      |
      v                                      v
empty or waiting surface            verify returned result
      |                                      |
      v                                      v
push A2UI later                     snapshot only when needed
```

`canvas.present` remains correct for URL or HTML surfaces. The problem is using it as a preparatory step for an A2UI payload.

## What developers get

- A focused `SKILL.md` that guides agents toward a minimal command sequence.
- A preflight validator for A2UI and URL-mode sequences.
- A known-good example and a deliberately bad example.
- A short reproduction guide for empty, waiting, or Unknown results.
- Privacy checks designed to catch common personal and secret-like data before sharing.

## Install

Project-level install:

```powershell
openclaw skills install git:jakemorgan-research/openclaw-canvas-a2ui-skill@main
```

While this preview is private, Git must already have access to the repository. A checked-out copy can be installed with `openclaw skills install .`.

Global install:

```powershell
openclaw skills install git:jakemorgan-research/openclaw-canvas-a2ui-skill@main --global
```

Then ask your agent to create or diagnose an OpenClaw Canvas/A2UI flow. The skill should activate for empty Canvas, waiting, Unknown, action-ordering, JSONL, and node-selection questions.

## Validate before use

```powershell
python scripts/validate_repo.py
python scripts/validate_sequence.py examples/a2ui-good.json
python scripts/validate_sequence.py examples/a2ui-reset-good.json
python scripts/validate_sequence.py examples/url-good.json
python scripts/validate_sequence.py examples/a2ui-bad-present-first.json
python -m unittest discover -s tests -v
```

The final command should fail by design.

## Repository map

```text
SKILL.md                    Agent instructions
agents/openai.yaml          Display metadata
scripts/                    Local validation tools
examples/                   Good and bad teaching sequences
tests/                      Ordering and mode-separation regression tests
references/                 Mode choice, reproduction, and validation notes
```

## Scope and limitations

This repository documents and checks command ordering; it is not an OpenClaw fork and does not replace upstream Canvas code. Actual command availability depends on the connected node, platform, permissions, and installed OpenClaw version. A passing local sequence check does not prove that a remote node rendered successfully.

## Official references

- [OpenClaw Nodes documentation](https://github.com/openclaw/openclaw/blob/main/docs/nodes/index.md)
- [OpenClaw Skills documentation](https://github.com/openclaw/openclaw/blob/main/docs/tools/skills.md)
- [OpenClaw FAQ](https://github.com/openclaw/openclaw/blob/main/docs/help/faq.md)

## Contributing and security

Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing a change. Report security or privacy problems using the private process in [SECURITY.md](SECURITY.md); do not place secrets or personal information in a public issue.

## License

MIT. See [LICENSE](LICENSE).
