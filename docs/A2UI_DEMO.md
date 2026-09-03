# A real card in four steps

[Home](../README.md) · [Recorded acceptance](ACCEPTANCE.md) · [Payload boundary](../references/payload-contract.md)

![Create components, load data, render, then update the visible text](media/a2ui-demo.svg)

## 1 · Select an installed renderer

Requirements: Python 3.9+, a browser, and a trusted OpenClaw installation containing the **v0.8** `a2ui.bundle.js`. Tested with OpenClaw **2026.8.2 (0965053)** in WSL2.

Locate the package directory used by your actual OpenClaw executable. Inside the tested package, the renderer is `dist/canvas-host/a2ui/a2ui.bundle.js`. Custom launchers may use a different package directory than your default package manager. Do not substitute `a2ui-v0.9.bundle.js`: its message contract differs.

The renderer is executable JavaScript: use your trusted installed copy, not a file received in an issue or an arbitrary download. No renderer code is distributed by this repository. If your installation has no matching bundle, stop here and use the [HTML-only preview](../examples/widget-preview.html).

## 2 · Start the demo locally

From this repository, replace the placeholder with the renderer you located:

```text
python scripts/serve_a2ui_demo.py --renderer "<installed-package>/dist/canvas-host/a2ui/a2ui.bundle.js"
```

In WSL, use `python3` if that is your installed Python command. Open `http://localhost:8768/` in your browser. If the port is busy, add `--port 8769` and use the printed URL. If Windows-to-WSL localhost forwarding is unavailable, use a browser in the same environment; do not expose the service to the LAN or disable a firewall to pass this test.

Only the page, renderer, and synthetic sample are served. There is no directory listing, private configuration read, model call, or connection to your Gateway. Stop with **Ctrl+C** when done. Do not use this small development server as public hosting.

## 3 · Observe the initial card

Expected visible result: an **A2UI acceptance card** title and **Synthetic data loaded** text. The renderer may show a Markdown heading marker in this standalone host. The enclosing page is HTML; the card is produced by the installed `openclaw-a2ui-host`, not a hardcoded HTML imitation.

The [JSONL payload](../examples/a2ui-v08-card.jsonl) contains three actual v0.8 messages:

| Message | What it does |
| --- | --- |
| `surfaceUpdate` | Creates a column and two text components on surface `demo` |
| `dataModelUpdate` | Sets the synthetic `/message` data value |
| `beginRendering` | Displays the `root` component |

This order is one tested example, not a universal rule for all clients. Do not add a `version: v0.8` field or mix v0.9 messages into it.

## 4 · Change the bound data

Click **Apply synthetic update**. The card text must change to **Synthetic update received** without reloading. A success message above the card alone is not enough: inspect the actual text in the card.

If the surface is blank or the text does not change, record the OpenClaw version, browser family, and failed step. Do not attach full paths, raw logs, tokens, or account screenshots.

## What this proves

It exercises real v0.8 message processing, surface rendering, and data binding. It does **not** test model-driven tool selection, Gateway routing, dashboard registered-source envelopes, native node delivery, or arbitrary A2UI components. Unit tests check the fixed example and local transport, not the complete A2UI schema or a live renderer.
