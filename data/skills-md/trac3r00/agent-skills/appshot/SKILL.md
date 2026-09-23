---
name: appshot
description: Takes screenshots of any macOS app window, the full screen, or an interactive region using the native screencapture command — zero dependencies. Capture a browser, Notes, a desktop agent app, or anything with a window. Use for visual QA evidence, app-state documentation, or "show me what X looks like right now".
when_to_use: Any macOS task that needs visual evidence of an app's current state — QA captures, documenting a bug, comparing before/after states, feeding a screenshot to a vision-capable agent. NOT a screen recorder (video) or an OCR tool; it captures PNG stills.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [screenshot, macos, capture, visual-qa, evidence]
---

# AppShot

"Show me what it looks like right now" — for any app on the machine.

## Commands

```bash
python3 scripts/appshot.py --screen --out shot.png
python3 scripts/appshot.py --app "Google Chrome" --out chrome.png
python3 scripts/appshot.py --app Notes --out notes.png
python3 scripts/appshot.py --region --out region.png
python3 scripts/appshot.py --list --json
```

## Modes

| Mode | What it captures |
|---|---|
| `--screen` | Full screen, no interaction |
| `--app NAME` | Front window of the named app (activates it first) |
| `--region` | Interactive click-drag selection |
| `--list` | All visible apps with capturable windows |

## Evidence workflow

1. `--list` to see what's capturable
2. `--app "Target App" --out before.png`
3. Make the change
4. `--app "Target App" --out after.png`
5. Compare (visually or with the visual-qa workflow)

## Pairs with

`visual-qa` (the verdict workflow these captures feed),
`webapp-testing` (browser-level captures for web surfaces),
`session-finder` (find the agent app, then screenshot it).
