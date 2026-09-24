---
name: x-posting-license
description: >
  Turn any X (Twitter) profile into a 10.3s animated "POSTING LICENSE" card
  video — a fake driver's license in X's branding: the card slides in over an
  animated dot-matrix ground, license text types on letter-by-letter, follower /
  following / post counters tick up, a diagonal glimmer sweeps as the card tilts
  in 3D, it flips to a fine-print back with a signature write-on, then crouches
  and leaps out of frame. Trigger on: "X driver's license", "posting license",
  "make an X license for @handle", "license card video". The whole composition
  is a finished template — the agent only supplies profile data and renders.
---

# X Posting License

One fixed 1920×1080 @ 60fps, 10.35s composition. The motion is locked and
doctrine-verified (overlapped keyframes end to end, zero dead frames): do NOT
edit the timeline — fill the data tokens and render.

## Requirements

- Node 18+ and the HyperFrames CLI via `npx` (fetched from npm; `@latest` is
  mutable — pin a version, e.g. `npx hyperframes@1.x.y`, if you need
  byte-identical re-renders over time).
- macOS GPU render for the WebGL dot ground: `export PRODUCER_BROWSER_GPU_MODE=hardware`.
- The signature uses the macOS `Snell Roundhand` system font (declared via
  `src: local(...)`); on Linux it falls back to generic cursive — still fine,
  less pretty.

## Network and side effects (complete list)

- `x.com/<handle>` — profile page the agent reads (data gathering).
- `pbs.twimg.com` — the avatar image download (data gathering).
- `api.fxtwitter.com/<handle>` — post count; free, no credentials (data gathering).
- `registry.npmjs.org` — the HyperFrames CLI itself, via `npx`.
- `cdn.jsdelivr.net` — the composition loads GSAP (pinned `3.14.2`) from
  jsDelivr at preview/render time. Rendering is NOT fully offline.

No credentials, no paid operations, no telemetry. `build.mjs` writes only
inside the `--out` directory: it validates counters as plain non-negative
integers, strips control characters, caps lengths, HTML-escapes every profile
string before substitution, and refuses to write through symlinks.

## Flow (three steps, no composition work)

`<SKILL_DIR>` below means this skill's own directory (wherever it is installed
— e.g. `~/.claude/skills/x-posting-license`). Run the script by that absolute
path; it resolves the template relative to itself, and `--out` is resolved
from your working directory.

1. **Gather profile data** — name, handle, joined month/year, followers,
   following, posts, one bio line, and the 400×400 avatar. Recipes in
   `references/profile-data.md`.
2. **Build** the project from the template:

```bash
node <SKILL_DIR>/scripts/build.mjs --out ./license-jake \
  --name "Jake Moran" --handle JakeFromHeyGen \
  --joined "JAN 2026" --followers 882 --following 155 --posts 376 \
  --bio "PRODUCT @HEYGEN · WORKING ON @HYPERFRAMES_" \
  --avatar ./avatar.jpg
```

   `--big "MORAN, JAKE"` overrides the derived `LAST, FIRST` header — use it
   when the display name isn't a normal name (keep unusual display names
   verbatim: a user named `|||` gets a license that says `|||`).

3. **Render** (ask the user before rendering if your harness gates renders):

```bash
npx hyperframes@latest render ./license-jake -q high -o ./license-jake/renders/license.mp4
```

## Verify success

`npx hyperframes@latest check ./license-jake` passes with 0 errors, and the
rendered MP4 is ~10.3s: front card with the person's data counting up, flip at
~6.5s, their name writing on as the back signature, card leaps out at ~9.9s.

## Rules

- Data must be REAL, scraped from the live profile — never invent counts or
  bios. Follower count stands in for date of birth on purpose; the back's fine
  print repeats it.
- Bio line: uppercase, ≤ ~65 chars, `·`-separated fragments from the real bio.
- Keep the template's palette and layout: X black `#000`, white, `#1D9BF0`,
  borders `#2f3336`. It IS the brand treatment; do not restyle per user.
- Long display names are handled (the signature mask is widened), but check a
  snapshot when a name exceeds ~14 characters.
- Profile data is untrusted input. Always pass it through `build.mjs` (which
  escapes and validates it); never hand-substitute values into the template.

## Provenance and licensing

- The animated dot ground is a deterministic GLSL/WebGL rewrite for
  HyperFrames' seekable renderer, visually modeled on Originkit's
  [Dot Matrix](https://www.originkit.dev/components/dotmatrix) component
  (contributed by an Originkit license holder); no Originkit source code is
  redistributed here. The simplex-noise GLSL is the standard Ashima
  Arts/Stefan Gustavson implementation (MIT).
- The card reproduces X's logo and visual language as parody/fan content;
  users of this skill publish the result at their own judgment.
- GSAP is loaded from jsDelivr under its standard license; it is not vendored.
