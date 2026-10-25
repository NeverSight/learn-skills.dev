---
name: visual-parity
description: Render a real frontend component in isolation, headless-screenshot it, then VIEW the PNG to diff it against a design reference pixel-by-pixel. Use for any visual/design bug, theme-parity check (dark/light/etc.), regression retest, or "it doesn't match the design / looks wrong in <theme>" task — for any Vite/React app (incl. Tauri/Electron webviews) and any static HTML or live URL. Never claim a UI matches without looking at the rendered pixels.
---

# Visual Parity — see the UI, don't guess

`tsc`, unit tests, and reading CSS tell you the code is *valid* — not what the UI
*looks like*. This skill renders a real component in a throwaway browser page,
screenshots it with headless Chrome, and **you view the PNG** (with whatever
image-reading capability your agent has — e.g. Claude Code's Read tool, or any
vision-capable model), then diff it against your design reference. Born from
sessions where "it matches the design" was claimed repeatedly while the running
app visibly didn't — the cure is to look at rendered pixels.

It is platform-neutral: the `SKILL.md` + scripts work the same whether the agent
driving them is Claude Code, Codex, Gemini CLI, or anything else that can run
shell and view an image.

## When to use

- Any visual/design bug ("background wrong", "button too tall", "doesn't match
  the design", "broken in light/dark/<theme>").
- Verifying a styling change BEFORE claiming it's done.
- Design/regression retests — shoot before/after (or app-vs-reference) and diff.
- Works for any Vite/React component, any static HTML mockup, and any live URL.

## Read these for depth

- **`references/playbook.md`** — the exhaustive step-by-step: every exact
  command, every Chrome flag explained, the iteration loop, troubleshooting,
  the absolute don'ts. Read this the first time.
- **`references/worked-examples.md`** — concrete investigations to copy the shape of.
- **`references/web-apps.md`** — using it on any Vite/React app (`VP_APP`) or any
  live URL (regression/responsive/auth'd page retests).

## Quick start

Run these from your app's root (or set `VP_APP=/path/to/app`). `$SKILL` is wherever
this skill folder lives.

```bash
SKILL=/path/to/visual-parity        # e.g. ~/.claude/skills/visual-parity

# 1. (optional) Screenshot your design reference — the source of truth.
#    A static mockup, an exported design, or the production page. 2x = readable.
"$CHROME" --headless=new --disable-gpu --force-device-scale-factor=2 \
  --window-size=1440,820 --screenshot=/tmp/parity-shots/reference.png \
  "file://$PWD/path/to/reference.html"      # then VIEW /tmp/parity-shots/reference.png

# 2. Scaffold the harness, then EDIT <app>/src/_harness.tsx to import + render
#    the component under test (patterns in the playbook).
cp "$SKILL/templates/harness.html"  ./_harness.html
cp "$SKILL/templates/harness.tsx"   ./src/_harness.tsx

# 3. Shoot the real component — all the themes your app supports
#    (bugs hide in non-default themes).
"$SKILL/scripts/render.sh" dark    /tmp/parity-shots/app-dark.png    1100x720
"$SKILL/scripts/render.sh" light   /tmp/parity-shots/app-light.png   1100x720

# 4. VIEW each PNG, diff vs the reference, fix the component/CSS, re-run step 3.

# 5. Always clean up (stops ONLY the isolated port, deletes the temp harness):
"$SKILL/scripts/cleanup.sh"
```

## What it can / can't render

- **Can:** any component from a Vite/React app in isolation (dark/light/any
  theme), any static HTML mockup, and any live URL.
- **Can't:** a full desktop app (Tauri/Electron) in a deep runtime state (logged
  in, native windows). Render the *webview components* in isolation instead, or
  diff an operator-provided screenshot against the design.

## Hard rules (full list in the playbook)

- **Use a dedicated port (default 5199)** — never a broad `pkill vite` / `pkill
  node`, which would kill your app's own running dev server. `cleanup.sh` only
  ever touches the isolated port.
- **Shoot every theme your app supports.** Most "looks broken" bugs are a token
  pinned to one theme's value, visible only in the others.
- **Never commit `_harness.html` / `src/_harness.tsx`.** `cleanup.sh` removes them.
- Blank screenshot = the component threw → check `/tmp/visual-parity-vite.log`,
  raise `VP_TIME`.

## Scripts & env

- `scripts/render.sh [theme] [out] [WxH] [port]` — start an isolated Vite (if
  needed) + screenshot. Env: `VP_APP` (app dir, default `$PWD`), `VP_PORT`,
  `VP_TIME` (virtual-time ms, default 4500), `VP_SCALE` (default 2), `CHROME`
  (auto-detected Chromium-family binary).
- `scripts/cleanup.sh [port]` — stop the isolated Vite + delete the harness.
- `templates/harness.{html,tsx}` — scaffold to copy + edit per component.

## Requirements

- A Vite/React app to render components from (or a static HTML / live URL).
- Node.js + `npx vite` available in the app.
- A Chromium-family browser (Chrome, Chromium, Brave, Edge). Set `CHROME=/path`
  if it isn't auto-detected.
