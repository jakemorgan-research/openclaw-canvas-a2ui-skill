# Choose the rendering mode first

| Intended result | First Canvas action | Avoid |
| --- | --- | --- |
| A2UI text payload | `canvas.a2ui.push` | Opening an empty Canvas first |
| A2UI JSONL payload | `canvas.a2ui.pushJSONL` | Calling `canvas.present` afterward just to display it |
| Clear demonstrated stale A2UI state | `canvas.a2ui.reset`, then push | Resetting every successful render |
| URL or HTML surface | `canvas.present` | Mixing URL mode with an A2UI sequence |

```text
Need a Canvas result
        |
        v
Is the payload A2UI? -- no --> Present URL/HTML
        |
       yes
        |
        v
Optional reset --> push payload --> inspect result --> snapshot only if needed
```

The important constraint is mode consistency. `canvas.present` is a valid action, but it is not the opening step for an A2UI render. A reset is an exception only when stale state or an explicit clean-surface request justifies it, and it must be followed immediately by a push.
