---
name: replica
description: Rebuild a web page, section, component or interaction from a reference (a live URL, a local HTML file, a screenshot or design export, or a screen recording or GIF) inside the user's own codebase. Then measure the rebuild against the reference (element boxes, computed styles, pixels, motion timing and easing) and iterate until a numeric Replica Score passes. Use when the user wants to clone, replicate, recreate, copy, port or match a site, landing page, hero, navbar, pricing table, card, modal, footer, hover effect, scroll reveal, page-load animation or any other UI, or to "make it look/feel/move like" one. Also use when they say "pixel-perfect", "1:1", "exactly like this" or "same as <url>", or hand over a screenshot, Figma export or video and ask to build it, including when they want their own copy, brand or extra features on top.
---

# Replica

Rebuild what the user points at, then prove it. `capture` turns the reference into a **blueprint** of measured facts. You build from the blueprint. `compare` scores the build on four axes (layout, style, pixels, motion) and tells you which fix is worth the most points. You are done when `compare` exits 0, not when the build looks right to you.

`<skill>` below means the directory this SKILL.md is in.

## Rules

1. **Measure, don't guess.** Take every size, colour, font, spacing, duration and easing from `blueprint.md`, `blueprint.json` or a report. Don't use your memory of how sites like this usually look.
2. **Never game the score.** Don't embed screenshots or video frames of the reference, iframe or proxy the reference, paste its rendered HTML wholesale, edit anything under `.replica/`, or lower `--level` to get a pass. Build real UI in the user's stack.
3. **Use the project's stack.** Read `package.json` and the nearest existing components first. Match the framework, styling approach and animation library already in use. Add a dependency only when the reference needs something the project cannot do.
4. **Fix in report order, a few at a time.** Items at the top often cause items lower down: one cascade fix can move dozens of elements. Re-run `compare` after each batch. Never stack ten speculative changes.
5. **Respect ownership.** The reference's fonts, images, icons and copy belong to their owners. Use the user's own assets and copy where they have them. Otherwise ask, or use placeholders with the same dimensions, marked `data-replica="placeholder"`: `compare` still checks their boxes but leaves their pixels out of the pixel score (whatever is painted in front of them still counts). Say in the final message which reference assets you reused.

## 0. Scope

Decide these and state them in your first message:

- **Target**: the URL or file, plus which part: a CSS selector for a section or component, or a time range for a video.
- **Destination**: the file or route in the user's project, and the stack.
- **Level**, which sets the bar `compare` holds you to:

  | level | when the user says | gates (all must pass) |
  |---|---|---|
  | `structure` | "same layout/feel but our brand", "like X with our content" | layout ≥ 90, motion ≥ 85 |
  | `faithful` (default) | "clone this", "recreate", "make it look like" | layout ≥ 95, style ≥ 95, pixels ≥ 85, motion ≥ 90 |
  | `exact` | "pixel-perfect", "1:1", "exactly" | layout ≥ 98, style ≥ 98, pixels ≥ 97, motion ≥ 95 |

- **Trigger**: what starts the motion (page load, hover, click, scroll into view, scroll-scrubbing). This becomes `--action`.

Infer what you can from the request and the repo. Ask only when two readings would lead to different work.

## 1. Setup (once per machine)

```bash
npm install --prefix <skill>/scripts
node <skill>/scripts/replica.mjs doctor
```

If `doctor` reports no browser, run the install command it prints. If Google Chrome is installed, Replica uses it as a fallback. Video and GIF references also need `ffmpeg` on PATH.

## 2. Capture the reference

Keep everything in `.replica/<name>/` inside the user's project, and add `.replica/` to `.gitignore`.

```bash
node <skill>/scripts/replica.mjs capture <url|file.html|image|video> --out .replica/<name>/ref \
  --selector "<css of the part>" --viewports 1440x900,390x844 --action load --motion 1500
```

- `--selector`: scope the capture to the part you are cloning. Whole pages produce huge blueprints.
- `--viewports`: the widths you will ship. The first one is primary; motion is recorded there.
- `--action` and `--motion <ms>`: only when there is motion to clone. Make the recording long enough to cover all of it; `capture` prints a note if something was still moving at the end.
- `--hide "<css>"`: hide cookie banners, chat widgets and dev overlays. This applies to both sides.

Recipes for images, videos, login-walled pages, iframes, canvas and dark mode are in [references/sources.md](references/sources.md).

Then **read `ref/blueprint.md` in full**. **Look at** `ref/<viewport>/shot.png` and `ref/motion/filmstrip.png` with your image viewer. The blueprint syntax is explained in [references/blueprint.md](references/blueprint.md). Image and video references have no blueprint, so build from the shots and frames.

## 3. Build

Work in this order: tokens → layout skeleton → typography → boxes and paint → media → responsive → motion.

- **Tokens**: put the blueprint's colours, type scale, radii, shadows and CSS variables into the project's token system (CSS variables or the Tailwind theme) with their exact values.
- **Layout**: reproduce each outline line's `flex …` / `grid cols[…]`, `gap` and `pad` values, and the widths of containers.
- **Typography**: match the family, weight, size/line-height and letter-spacing exactly. If a font is unavailable or licensed, use the closest available one and record it as a known difference.
- **Motion**: when the blueprint has "Declared animations", copy their duration, delay, easing and keyframes exactly. Otherwise use the timeline's start, duration and easing, or its spring parameters.
- **Serve it**: make the clone reachable at a URL or HTML file that renders the same state (a dev-server route, a story, or a static file). If its root element needs a different selector than the reference's, pass `--selector` to `compare`.

Notes for each stack (CSS, Tailwind, Framer Motion, GSAP) are in [references/building.md](references/building.md).

## 4. Compare, fix, repeat

```bash
node <skill>/scripts/replica.mjs compare .replica/<name>/ref <clone url|file> [--selector "<clone root css>"]
```

It writes `round-N/` with `report.md`, `issues.json`, `score.json` and `sheets/`. Exit code 0 means pass, 1 means not yet, and 2 means an error.

1. Read `round-N/report.md`: the score table, then **Fix next**. Each item shows how many points fixing it is worth.
2. Look at `round-N/sheets/*.png`: the reference | yours | diff overview, zoomed hotspots, and the motion strip.
3. Fix the top 3–5 items, always including any **"Likely cause"** item. Then run `compare` again.

- If the report shows ▼ (the score went down), undo your last change before trying anything else.
- If two rounds in a row gain less than 1 point, stop patching. Re-read the blueprint for the failing area, and check that fonts loaded and that you are comparing the right selector, state and viewport.
- Stop after 8 rounds, and report what is left and why.

[references/fixing.md](references/fixing.md) covers what each kind of finding means and the change that usually resolves it.

## 5. Deliver

End with this, filled in:

```
Replica · <target> → <files changed>
Level <level> · round <N> · score <overall> — PASS | NOT YET
layout <n> · style <n> · pixels <n> · motion <n>
Known differences: <each one, with its reason (licensed font, user's own copy, …)>
Reference assets reused: <list, or none> · placeholders: <list, or none>
Evidence: .replica/<name>/round-<N>/report.md and sheets/
```

If it did not pass, say so plainly and list the remaining top findings.
