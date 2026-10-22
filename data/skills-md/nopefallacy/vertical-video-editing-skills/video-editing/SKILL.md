---
name: video-editing
description: Turn an approved script, provided talking-head/voiceover media, and gathered assets into a polished, creator-grade vertical (9:16) short rendered with HyperFrames. Encodes a non-negotiable init→preview→lint→render→verify workflow; a reusable editorial house look (mixed serif/sans headlines, paper-stage and dark-grid grounds, stacked splits with seam captions, highlight-bar supers, name pills, headline cards, UI-card stacks); engineered hooks; A-roll/B-roll spine; non-metronomic cuts down to 0.2s; split-screen layouts with deliberate full-frame transitions; eased camera moves (zoom/push) with explicit anti-jitter rules; kinetic captions/keyword emphasis; themed motion graphics (number/spec/poster/callout cards); logo animation; layered SFX mixed under voice; visual theming derived from a style pack (styles/<style>/FRAME.md); asset integration via a manifest; and required verification (preview screenshots + ffprobe + frame spot-checks + a render gate script). Adopts hyperframes-helper conventions (GSAP power-eases, glow captions, lint gotchas) and extends them with an editorial look, a camera-motion system, style theming, SFX synthesis, and a verification gate. Use when you have a script and media and need a finished short.
---

# video-editing

Use this skill when you have an approved script, provided voice/talking-head media, and gathered assets, and need to turn them into a finished vertical (9:16) short. You are the **main editor**, not a clip-stitcher. The bar is creator-grade shorts (Kallaway / Varun Mayya density): every beat earns attention. Generic AI-tool output — uniform 1s cuts, default fonts, linear/jittery transforms, a stock-template look — is a **failure**, not a deliverable.

> Default ratio is **9:16 (1080×1920)**. The style packs also define 16:9 and 1:1 behavior, so the same look can be retargeted — but this skill's pacing and hook grammar are written for vertical short-form first.

## The non-negotiable workflow (never skip, never reorder)

Authoring `index.html` by hand from nothing breaks live-reload and project structure. Always:

1. **`npx hyperframes init edit`** inside your project's `edit/` folder — creates the scaffold (`index.html`, `meta.json`, `hyperframes.json`, `CLAUDE.md`, `package.json`).
2. **`cd edit`** and modify the generated project files to build the actual edit. Add `fonts/`, `assets/sfx/`, sub-compositions under `compositions/`.
3. **`npx hyperframes preview`** (long-running — run in background) — verify in the browser with live reload. Use a browser tool to inspect and screenshot. Confirm pacing, layout, text timing, and animation smoothness **before** rendering.
4. **`npx hyperframes lint` / `npm run check`** — fix every error; review warnings.
5. **`npx hyperframes render`** — final MP4.
6. **Verify**: `ffprobe` (9:16 dimensions, duration, codec) + `ffmpeg` frame spot-checks against a contact sheet. Run the bundled gate script (below).

Use the **hyperframes** docs (`npx hyperframes docs`) for API/feature reference and the references in this skill for the editing standard. If HyperFrames tooling is missing or broken, stop and tell the user rather than hand-authoring a generic edit.

## Requirements

- **HyperFrames** — the rendering engine, run via `npx hyperframes`. This skill is the editing standard *on top of* HyperFrames; it does not replace it.
- **Node.js** (for `npx` and the verification script).
- **ffmpeg / ffprobe** on PATH — for SFX synthesis, audio mixing, and render verification.
- A **style pack** under `styles/<style>/FRAME.md` (this skill ships `vibe-life` as a worked example and `_template` as a starting point — see `styles/README.md`).

## Inputs

Work from one project folder. A recommended layout (adapt to yours):

```
your-project/
├── script.md            # approved script with beats/timestamps, supers, energy cues — THE SPINE
├── voiceover/           # provided voice / talking-head media (the A-roll)
├── avatar/              # optional talking-head media
├── assets/
│   ├── manifest.json    # gathered B-roll + per-beat asset map + rights notes
│   └── ...              # the gathered media
└── edit/                # YOUR output (created by `npx hyperframes init edit`)
```

Read (do not edit) the script, the voice/avatar media, and the asset manifest. Pick the **style pack** the video should use (`styles/<style>/FRAME.md`).

## Outputs

Write everything under your project's `edit/` folder:

- The HyperFrames project (`index.html` + `compositions/` + `fonts/` + `assets/sfx/` + `assets/master_audio.*`).
- The final rendered **MP4** (9:16), verified.
- `edit-report.md` — a handoff note: per-beat edit decisions, assets used (with manifest references), SFX/music used, preview/render verification notes, and anything you flagged for final review. Template in `references/edit-report-template.md` (appended below).

## Editing grammar (what "professional" means here)

Each item below is a quality gate, not a suggestion.

**The house visual language is the editorial look** — see "editorial-look" below. Frames are designed pages, not video with text on top: mixed serif-italic/heavy-sans editorial headlines, paper-stage and dark-grid-interstitial grounds, the **stacked split (B-roll top / talking head bottom) as the default A-roll/B-roll layout**, highlight-bar supers with keyword color emphasis, seam captions and name pills, headline cards, and UI-card stacks. Build every short from those ten patterns, themed per style pack.

- **Engineered hook (first 1–3s):** text supers on top, a pattern interrupt, then a move into frame (e.g. a split panel that grows to full 9:16). Never open on a static talking head.
- **A-roll / B-roll structure:** A-roll (talking head / VO) is the spine; B-roll (clips, screenshots, motion graphics) covers and punctuates it. Cut B-roll over the A-roll's audio, not in silence.
- **Cut granularity:** cuts as fast as **0.2s** when the script's energy demands; **never metronomic 1s cuts**. Pacing follows the script.
- **Split-screen layouts:** side-by-side and stacked compositions, with deliberate transitions in and out of full-frame. The **stacked split with a seam caption is the workhorse** — full-frame B-roll cover is the exception.
- **Face-safe framing:** whenever a person is inside a panel or crop, bias the crop with `object-position` so the **face sits centered in the panel's visible area, eyes in the upper third** — the default `50% 50%` is almost always wrong for talking-head sources and cuts heads off. Camera moves on a person-panel must keep the face in frame for the entire move. An off-center or cropped face is a gate failure. See "editorial-look" §4 "Face-safe framing".
- **Eased camera motion:** zoom-in/out and push left/right pans, **always eased, never linear, never jittery.** See "camera-moves" for the anti-jitter contract.
- **Kinetic text / captions:** animated entrances, keyword emphasis (one accent word), caption supers timed to the voice.
- **Themed motion graphics:** number cards, spec/JSON cards, bounding-box callouts, poster splits, chart builds — designed on the style theme, not generic.
- **Logo / wordmark animation:** animated brand/product marks where the script names them.
- **SFX:** whooshes, clicks, risers, impacts layered on cuts and graphic hits — subtle, mixed under the voice. See "sfx-and-audio".
- **Cohesive aesthetics:** one color theme, consistent typography, eased curves, no default-look elements, no popping. All from the style pack `FRAME.md`.

## Style theming (required, before designing anything)

Derive the visual identity from the style pack first — colors, type, motion personality, and graphic language all come from `styles/<style>/FRAME.md`. **Different style → different look.** See "style-theming" below for turning `FRAME.md` into a concrete `frame.md` design spec (palette tokens, `@font-face` for local fonts, motion personality → easing/cut choices). The shipped `vibe-life` example uses a cream/ink/peach/butter palette; Space Grotesk + Instrument Serif italic + JetBrains Mono; paper-cut motion (hard cuts masked by SFX, not crossfades); one italic-serif accent word per frame in a pill; flat hard ink shadows. Your own style fills the same roles with its own tokens.

## HyperFrames hard rules (break these and the render breaks)

1. Every timed element needs `data-start`, `data-duration`, `data-track-index` **and** `class="clip"` (the framework controls visibility via `clip`).
2. **Never GSAP the `.clip` element itself** — the framework owns its visibility/transform. Animate a child wrapper (e.g. `.cam`, `.inner`).
3. Timelines must be `gsap.timeline({ paused: true })` and registered on `window.__timelines["main"]` (id matches `data-composition-id`).
4. **Deterministic only** — no `Math.random()`, no `Date.now()`, no network fetches, no `repeat: -1`. Renders are frame-sampled and must be reproducible.
5. **9:16 = 1080×1920.** Set `#root { container-type: size; }` so `cqw`/`cqh` resolve against the frame (1cqw = 10.8px). Size type/graphics in `cqw`/`cqh`, not `vw`/`vh`.
6. **Adjacent same-track clips must not touch** — float precision makes `3.2 + 0.35 = 3.5500000000000003`, which overlaps a clip starting at `3.55` and trips `overlapping_clips_same_track`. Leave a gap or use durations like `0.34`. (Adopted from hyperframes-helper's lint gotchas.)
7. **Audio:** videos are `muted` with a separate `<audio>` element. Prefer **one pre-mixed master audio track** (VO + SFX mixed via ffmpeg `adelay`+`amix`) over many `<audio>` elements — multiple tracks cause echo/desync. Put it on a high, dedicated `data-track-index`.
8. **Density:** `timeline_track_too_dense` (many timed elements on one track) is advisory for a short pilot but real at scale — split scenes into **sub-compositions** (`data-composition-src="compositions/file.html"`) for production-length edits.

## Workflow

1. **Read the script as the spine.** Build a beat map: each beat/timestamp → A-roll (VO/avatar segment) + B-roll/MG need + on-screen super + intended cut/camera/transition + energy. The script's energy dictates pacing; do not impose a uniform rhythm.
2. **Theme from the style pack.** Read `styles/<style>/FRAME.md`. Produce the concrete design spec: palette tokens, local `@font-face` declarations, motion personality, graphic language. (See "style-theming".)
3. **Reconcile asset coverage.** Cross-reference your asset manifest: which beats are covered by gathered media, which are `build-in-editor` (yours to build as motion graphics), which are `alternate` swaps. Never put placeholder/unlicensed media in a final render — flag gaps in the report.
4. **`npx hyperframes init edit`.** Scaffold first. Then add `fonts/` (local woff2 subsets), `assets/sfx/`, `compositions/`.
5. **Build the edit beat-by-beat** in `index.html` (and sub-compositions for length). Apply the editing grammar: engineered hook, A-roll/B-roll cover, non-metronomic cuts, split-screens, eased camera moves, kinetic text, themed MGs, logo animation. Animate child wrappers, never the `.clip`.
6. **Author SFX + master audio.** Synthesize rights-free SFX with ffmpeg (`anoisesrc`/`aevalsrc`/`sine`) or use cleared assets; mix VO + SFX into one master track. (See "sfx-and-audio".)
7. **Preview and inspect.** `npx hyperframes preview` in background; open in the browser; screenshot key beats; confirm pacing, layout, text timing, and motion smoothness. Fix before rendering.
8. **Lint.** `npm run check` / `npx hyperframes lint --verbose`. Fix all errors; review warnings (note known false positives — e.g. WCAG-contrast warnings sampled at timestamps where a high-contrast card is hidden).
9. **Render.** `npx hyperframes render` → MP4.
10. **Verify with the gate script.** Run `node scripts/verify-render.mjs <path-to-mp4>` — asserts 9:16, expected duration, h264/yuv420p, audio present. Then `ffmpeg` frame spot-checks into a contact sheet and eyeball against the preview.
11. **Write `edit-report.md`** and set disposition (done / in_review / blocked). Attach the MP4 + contact sheet.

Run the verification gate (the script ships in `scripts/verify-render.mjs` next to this file):

```sh
node scripts/verify-render.mjs path/to/edit/<file>.mp4
```

Optionally assert exact specs:

```sh
node scripts/verify-render.mjs <file>.mp4 --duration 12 --tolerance 0.5
```

## Missing assets

If a beat needs an asset your `assets/` doesn't have:

1. Check the manifest for `alternate` or `build-in-editor` rows first — custom motion-graphic beats are **yours to build**, not a blocker.
2. If it is genuinely missing and quick to fetch lawfully and directly, fetch it yourself and record provenance in `edit-report.md`.
3. Otherwise list the exact beat/timestamp, the asset need, and the intended edit action in the report, ask the user to supply it, and continue on beats you can finish. Never render a placeholder you can't license.

## Verification (required before handoff)

- **Preview screenshots:** representative frames captured from the live preview, confirming layout/timing/motion.
- **ffprobe:** dimensions exactly 9:16 (1080×1920), expected duration (±tolerance), `h264` / `yuv420p`, audio stream present. The gate script enforces this.
- **Frame spot-checks:** `ffmpeg` extract frames across the timeline into a contact sheet; confirm each required technique renders on-style and matches the preview.
- **Face check:** on every preview screenshot and contact-sheet frame containing a person, the whole face is visible and centered in its panel (not cropped by a seam, caption, edge, or camera move). Fail the gate and re-frame if not.
- **Rights:** no unlicensed/placeholder media in the render; anything that needs a final license check called out in the report.
- **Design-change log:** any deviation from the style spec or the editorial-look patterns (new layout, changed colors/type, modified motion) must be recorded in `edit-report.md` under "Design decisions", with the reason. Visual changes are fine; silent visual changes are not.

## Credits & provenance

This skill researched the **hyperframes** docs, `github.com/robonuggets/hyperframes-helper`, and reference frames from creator-grade shorts, then went beyond them. See "standard-provenance" below for the breakdown. Summary:

- **Adopted** from hyperframes-helper / HyperFrames: HTML-source-of-truth model; `data-*` timing attributes + `class="clip"`; paused timelines on `window.__timelines`; GSAP `power2/power3.out` eases; white-glow caption styling; SVG underline emphasis; the lint gotcha list (overlap float-precision, deterministic-only, muted-video-plus-audio, etc.).
- **Added** here: a full **eased camera-motion system** with an explicit anti-jitter contract; **9:16 short-form grammar** (engineered hooks, sub-0.2s non-metronomic cutting, split→full-frame transitions); a **style-theming pipeline** from `FRAME.md` → concrete design spec; **rights-free SFX synthesis** + single pre-mixed master-track discipline; and a **render verification gate** (ffprobe assertions + contact-sheet spot-checks).


---

## Appendix — Reference Library (inlined)

The authoring source keeps these as separate files under `references/`; they are inlined here so the skill is a single self-contained SKILL.md.


### Appendix: editorial-look

# The editorial look — reference visual grammar

Distilled from stills of creator-grade shorts (Kallaway / Varun Mayya class) into ten
named patterns. These are the **house layouts**: build every short from them, themed
with your style pack's tokens (`styles/<style>/FRAME.md`). The recipes below show a
mapping for the shipped `vibe-life` example; substitute your own tokens.

The unifying idea: **frames are designed pages, not video with text on top.** Type is
editorial (a heavy grotesque playing against an italic serif), media sits in cards or
panels on a textured ground, and supers are typeset objects (bars, pills, underlines) —
never bare drop-shadowed text.

---

## 1. Editorial headline (mixed serif/sans)

One headline, two voices: heavy sans for the statement, italic serif for the *twist
word(s)*, plus a hand-drawn underline or highlight on the payoff.

```
Claude Just *Changed*        ← serif italic on the verb
SOCIAL MEDIA FOREVER         ← heavy grotesque, tight leading
━━━━━━━━━━━━                 ← accent underline (brand accent)
```

```css
.headline { text-align: center; line-height: 0.95; color: var(--fg); }
.headline .sans  { font: 500 9cqw/0.96 "Space Grotesk"; letter-spacing: -0.32cqw; }
.headline .serif { font: italic 400 9cqw/0.96 "Instrument Serif"; }
.headline .underline {
  display: block; width: 46cqw; height: 0.9cqw; margin: 1.6cqw auto 0;
  background: var(--accent-strong); border-radius: 999px;
  transform-origin: left center;          /* animate scaleX 0→1, power3.out */
}
```

Rules: serif italic on **one or two words max** (the verb or the twist), never the whole
line. Underline draws in with `scaleX` after the words land. Mixed-case serif against
caps/title-case sans is the signature.

## 2. Paper stage (light textured ground)

Full-frame off-white "paper" with a faint grid — media and graphics sit **on** it as
cards. Used for hooks, logo beats, UI-stack beats.

```css
.paper {
  background:
    linear-gradient(var(--line-faint) 1px, transparent 1px),
    linear-gradient(90deg, var(--line-faint) 1px, transparent 1px),
    var(--bg);                                   /* e.g. #f3ecd9 */
  background-size: 6cqw 6cqw, 6cqw 6cqw, auto;
}
/* --line-faint: color-mix(in srgb, var(--fg) 7%, transparent) */
```

Optional grain: a deterministic SVG `feTurbulence` data-URI at 4–6% opacity (fixed seed
— renders must stay reproducible). Never a looping video texture.

## 3. Dark grid interstitial (typographic chapter card)

Full-frame ink wall with a visible grid, a centered mixed-type claim, and **one lit
accent cell** — a typographic pattern interrupt between sections. Hold 0.6–1.2s.

```css
.grid-wall {
  background:
    linear-gradient(rgba(255,255,255,0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.07) 1px, transparent 1px),
    #121110;
  background-size: 4.5cqw 4.5cqw;
}
.grid-wall .cell {           /* the single accent pixel */
  position: absolute; width: 4.5cqw; height: 4.5cqw;
  background: var(--accent-strong); filter: blur(0.15cqw);
}
```

Type on the wall follows pattern 1 (small serif italic line above, heavy sans claim,
serif italic tail below, ragged-right offset). A handful of grid cells may flicker
brighter — animate `opacity` on 2–4 cells, staggered, deterministic.

## 4. Stacked split (the workhorse layout)

B-roll panel top (~52–56cqh), talking-head panel bottom, with the caption at the seam.
This is the default A-roll/B-roll layout — full-frame B-roll cover is the exception,
not the rule.

```html
<div class="stack">
  <div class="panel top"><video class="fill" ...></video></div>
  <div class="seam-caption">For <em>13 years</em></div>
  <div class="panel bottom"><video class="fill" ...></video></div>
</div>
```

```css
.stack .panel { position: absolute; left: 0; right: 0; overflow: hidden; }
.stack .top    { top: 0;    height: 54cqh; }
.stack .bottom { bottom: 0; height: 46cqh; }
.seam-caption {
  position: absolute; top: 54cqh; left: 0; right: 0; z-index: 2;
  transform: translateY(-50%); text-align: center;
}
```

Moves in/out of full frame are deliberate: a panel **grows into the full 9:16** (animate
`height`/`y` on the panel wrapper, `power3.inOut`, 0.45–0.6s, whoosh on the move) or the
top panel slides off and the bottom takes over. Panels can sit inside a dark grid frame
(pattern 3 ground showing at the edges) for a premium "mounted" look.

### Face-safe framing (required whenever a person is in a panel)

A panel crops the source video, and the default crop (`object-position: 50% 50%`) cuts
heads off or pushes the face to a corner. **The face must sit centered in the panel's
visible area, eyes in the upper third.** Never let a seam, caption, or panel edge crop
the face.

```css
.panel video.fill { width: 100%; height: 100%; object-fit: cover; }
.panel.bottom video.fill { object-position: 50% 22%; } /* bias crop toward the face */
```

Procedure:

1. Find the face's position in the **source** clip (preview one frame; faces in 9:16
   talking-head sources usually sit at ~20–35% from the top).
2. Set `object-position: 50% <face-y>%` per panel so the face lands mid-panel. A 46cqh
   bottom panel showing a 9:16 source needs the y-bias — 50% 50% is almost always wrong.
3. If the panel is narrower than full width (side-by-side split), bias x the same way
   toward the face.
4. Camera moves on a person-panel must keep the face inside the visible area for the
   **entire** move — check the end pose, not just the start.
5. Verify in preview screenshots and again on the render contact sheet: every frame with
   a person shows the whole face, centered in its panel. An off-center or cropped face
   is a gate failure, same severity as jitter.

## 5. Highlight-bar super (the boxed statement)

The big super is type **inside a solid bar**, one or two stacked bars, with the keyword
in the accent color. Black-bar/white-text (newspaper) and accent-bar variants.

```css
.bar-super { text-align: center; }
.bar-super .bar {
  display: inline-block; padding: 0.8cqw 3cqw;
  background: var(--fg); color: var(--bg);              /* ink bar */
  font: 500 7.4cqw/1.18 "Space Grotesk"; letter-spacing: -0.2cqw;
  box-decoration-break: clone; -webkit-box-decoration-break: clone;
}
.bar-super .bar.accent { background: var(--accent-strong); }  /* accent bar variant */
.bar-super .kw { color: var(--butter); }               /* keyword pop inside the bar */
```

Two-line bars are staggered (second bar lands 0.08–0.12s after the first, `y: 30 → 0`,
`power3.out`). Numbers get the keyword color: `**1** out of 3 employees`.

## 6. Name pill / seam pill

Small rounded pill identifying who/what is on screen, or carrying the serif accent word
at a panel seam. Enters with `scale: 0 → 1, back.out(2)`, a click SFX, sits for the beat,
exits before the panel changes.

## 7. Headline card (newspaper beat)

A "clipping" for news/announcement beats: serif headline with an ink highlight bar over
the key phrase, photo cut-outs below separated by a jagged divider (lightning-bolt SVG
path), all on the paper stage.

```css
.clipping h1 { font: italic 400 6.4cqw/1.15 "Instrument Serif"; color: var(--fg); }
.clipping h1 mark { background: var(--fg); color: var(--bg); padding: 0 1cqw; }
.clipping .photos { display: grid; grid-template-columns: 1fr 1fr; gap: 0.6cqw; }
```

Animate like a build: headline types/slides in, highlight `mark` wipes across
(`scaleX`, origin left), photos drop in 0.1s apart with the divider flash.

## 8. UI-card stack (receipts)

Real screenshots (profiles, posts, dashboards, JSON) presented as a **stack of rounded
cards** with borders/shadows on the paper stage — evidence, typeset. Cards cascade in
(y-offset + stagger 0.1–0.14s, `power3.out`), slightly overlapping, ±1–2° rotation on
alternating cards. One small word super beneath ("connect") in heavy sans.

## 9. Display word with glow/outline (sparingly)

For a single hype word over B-roll: script/serif word small above, the big word in heavy
caps with an outlined-glow twin behind it (`-webkit-text-stroke` + soft `text-shadow` in
the accent). **At most once per short** — it is the loudest element in the kit.

## 10. The seam caption

Captions live at layout seams (between stacked panels) or in the scrim band over the
talking head — small serif italic phrases (`For 13 years`, `order sunlight`) in the
accent or paper color. One short phrase at a time, timed to the VO clause, fade or
rise 20–30px in. Never paragraph captions; never full-sentence karaoke captions in this
look.

---

## Composition rules (how the patterns combine)

- **Every frame is grounded**: paper stage, dark grid, or media panel edge-to-edge.
  No floating type over raw video without a scrim, bar, or pill.
- **Hook recipe** (refs 1, 3, 5): editorial headline (pattern 1) on paper or over the
  top panel → stacked split (4) with the talking head entering the bottom panel →
  seam pill (6) → a panel grows to full frame as the body starts.
- **Section turns** use the dark grid interstitial (3) or a headline card (7) — never
  a bare jump cut between topics.
- **Emphasis ladder** (quiet → loud): seam caption (10) → name pill (6) → highlight bar
  (5) → editorial headline (1) → glow word (9). Pick the lowest rung that does the job;
  do not stack two loud patterns in the same frame.
- **Style mapping is mandatory**: reference-frame red/yellow are *roles* (accent-strong /
  emphasis), not colors to copy. Fill the same roles from your own `FRAME.md`.
- All entrances obey the anti-jitter contract ("camera-moves"); every bar/pill/card
  landing gets a click or thock under the voice ("sfx-and-audio").


### Appendix: style-theming

# Style theming — FRAME.md → concrete design spec

Before designing anything, turn your style pack's `styles/<style>/FRAME.md` into a
concrete, usable design spec for the edit. **Different style → different look.** Never
ship a generic theme.

## What to extract from FRAME.md

1. **Palette → CSS custom properties.** Pull every named color and define tokens on
   `:root` so every scene references the same source of truth:

   ```css
   :root {
     --cream: #f4efe6;  --ink: #1a1714;  --peach: #f2a07a;
     --butter: #f5cf6a; --moss: #8a9b6e;  --sky: #8fb3c4;  --plum: #9a7aa0;
   }
   ```

2. **Typography → local `@font-face`.** Renders must be deterministic and offline —
   **never rely on a font CDN at render time.** Download woff2 subsets into `fonts/` and
   declare them locally:

   ```css
   @font-face { font-family: "Space Grotesk"; src: url("fonts/spacegrotesk.woff2") format("woff2"); }
   @font-face { font-family: "Instrument Serif"; src: url("fonts/instrumentserif.woff2") format("woff2"); font-style: italic; }
   @font-face { font-family: "JetBrains Mono"; src: url("fonts/jetbrainsmono.woff2") format("woff2"); }
   ```

   Fetch the **latin subset, largest woff2** per family (a too-small file is usually a
   wrong/partial subset). Map each face to its role: display sans for headlines, italic
   serif for the accent word, mono for spec/number/code cards.

3. **Motion personality → easing & cut style.** FRAME.md describes how the style *moves*.
   Translate it:
   - "Paper-cut / calm" → **hard cuts masked by SFX**, not crossfades; eased
     `power1.inOut` drifts; no bouncy `back`/`elastic` on the spine.
   - "Energetic / punchy" → faster cuts, `power3.out` arrivals, occasional `back.out`
     accents.
   Reconcile a calm personality with short-form energy by keeping *transitions* on-style
   (hard cuts) while letting *pacing* (cut frequency) carry the energy.

4. **Graphic language → MG recipes.** FRAME.md's signature devices become reusable motion
   graphics: e.g. one italic-serif accent word per frame in an accent pill; flat hard ink
   shadows (offset solid, never blurred); number/ledger cards on a paper stage.

## The frame.md design spec (lowercase, preferred)

HyperFrames prefers a lowercase `frame.md` as the per-project design spec. Produce one in
`edit/` capturing: the token palette, the three font roles, the motion-personality
decision, and the graphic devices you'll reuse. This keeps every scene coherent and gives
the next editor a single reference.

## Container units for fidelity

Set `#root { container-type: size; }` and size type/graphics in `cqw`/`cqh` (1cqw = 10.8px
at 1080 wide). This keeps proportions identical between preview and render and lets spacing
scale cleanly. Avoid `vw`/`vh` — they resolve against the viewport, not the frame.


### Appendix: camera-moves

# Camera moves & the anti-jitter contract

HyperFrames renders by seeking a paused GSAP timeline to sampled frame times and
screenshotting. Camera motion that looks fine in a live preview can **stutter or shimmer**
in the render if the transform isn't GPU-promoted and sub-pixel-stable. This is the single
biggest gap between "AI-tool output" and creator-grade. hyperframes-helper has **no camera
system** — this is added by this skill and mandatory.

## The rules

1. **Never animate the `.clip` element.** The framework owns its visibility and base
   transform. Put a `.cam` wrapper *inside* the clip and animate that.

   ```html
   <div class="clip" data-start="5.0" data-duration="2.6" data-track-index="1">
     <div class="cam"> ... scene content ... </div>
   </div>
   ```

2. **GPU-promote the moving layer** so the compositor (not layout) handles the transform —
   this is what kills jitter:

   ```css
   .cam {
     will-change: transform;
     backface-visibility: hidden;
     transform: translateZ(0);   /* forces its own compositor layer */
   }
   ```

3. **Force 3D on the tween** so GSAP writes `matrix3d`, not `matrix`:

   ```js
   gsap.set(".cam", { force3D: true });
   ```

4. **Ease, never linear.** Linear camera moves read as robotic. Use `power1.inOut` for
   slow drifts, `power2.out`/`power3.out` for arrivals. Reserve `expo`/`back` for accents,
   not the base camera.

5. **Keep magnitudes small.** A push is `scale 1.0 → 1.12` over 2–3s, a pan is
   `xPercent ±1.5` — not `±20`. Big fast moves amplify sampling stutter and read as cheap.
   Slow, subtle, eased.

6. **Anchor the zoom.** Set `transform-origin` deliberately (`center`, or toward the
   subject) so a zoom pushes *into* the point of interest, not the geometric center by
   accident.

## Patterns

**Eased zoom-in push:**

```js
tl.set("#s4 .cam", { force3D: true });
tl.fromTo("#s4 .cam",
  { scale: 1.0, xPercent: -1.5 },
  { scale: 1.12, xPercent: 1.5, duration: 2.6, ease: "power1.inOut" },
  5.0
);
```

**Push left/right pan:** animate `xPercent` only, small magnitude, `power1.inOut`. Combine
with a tiny `scale: 1.04` so edges never reveal the frame boundary.

**Split → full-frame grow:** a panel starts as half-frame (`width: 50cqw`) and grows to
full (`100cqw`) with `power3.out`, while the sibling panel slides out. This is the
"character grows into the full 9:16 frame" hook move — eased arrival, masked by a whoosh
SFX on the cut.

## Verify motion in the render, not just the preview

Live preview interpolates smoothly; the render samples discrete frames. After rendering,
extract 3–5 frames across the camera move with `ffmpeg` and check for: shimmer on text
edges, sub-pixel jutter, or a "pop" at the start/end (usually a missing `fromTo` start
state or animating the clip instead of the wrapper).


### Appendix: sfx-and-audio

# SFX & audio — synthesis and the single master-track discipline

SFX separate creator-grade edits from silent slideshows: whooshes on camera moves, clicks
on text entrances, risers into reveals, impacts on graphic hits — all **subtle, mixed
under the voice.** Two hard problems: getting rights-free SFX, and avoiding echo/desync
from multiple audio elements.

## Rights-free SFX via ffmpeg synthesis

No licensing, no provenance burden — synthesize SFX deterministically. Generate each into
`assets/sfx/`:

**Whoosh** (cut / camera move) — filtered pink noise with a fast envelope:
```sh
ffmpeg -f lavfi -i "anoisesrc=duration=0.45:color=pink:sample_rate=48000:amplitude=0.5" \
  -af "afade=t=in:st=0:d=0.05,afade=t=out:st=0.2:d=0.25,highpass=f=300,lowpass=f=6000" \
  assets/sfx/whoosh.wav
```
> Gotcha: always **quote** the lavfi arg. An unquoted `*` elsewhere in the command can
> glob and shift ffmpeg's positional args, mis-parsing `r=$SR` etc.

**Click** (text/UI entrance) — short high sine blip:
```sh
ffmpeg -f lavfi -i "sine=frequency=2200:duration=0.04:sample_rate=48000" \
  -af "afade=t=out:st=0.01:d=0.03" assets/sfx/click.wav
```

**Riser** (build into a reveal) — rising sweep via `aevalsrc`/`sine` with frequency ramp,
~0.6–1.0s, fade in.

**Impact** (graphic hit / landing) — low sine (~80–120Hz) + short noise burst, fast decay.

Keep SFX **−18 to −12 dB under the voice**. They punctuate; they don't compete.

## One pre-mixed master track (not many `<audio>` elements)

Multiple simultaneous `<audio>` elements cause echo, drift, and desync in the render.
Instead, mix **VO + all SFX into one master track** offline with ffmpeg, placing each SFX
at its cut time via `adelay`, then `amix`:

```sh
ffmpeg \
  -i voiceover/vo.wav \
  -i assets/sfx/whoosh.wav -i assets/sfx/click.wav -i assets/sfx/riser.wav -i assets/sfx/impact.wav \
  -filter_complex "\
    [1]adelay=2200|2200,volume=0.5[w]; \
    [2]adelay=3200|3200,volume=0.4[c]; \
    [3]adelay=7000|7000,volume=0.45[r]; \
    [4]adelay=7600|7600,volume=0.6[i]; \
    [0][w][c][r][i]amix=inputs=5:duration=longest:normalize=0[mix]" \
  -map "[mix]" -ar 48000 -ac 2 assets/master_audio.wav
```

`adelay` is in **milliseconds per channel** (`ms|ms` for stereo). `normalize=0` keeps the
VO from being attenuated by the mixer. Then encode to `.m4a` (AAC) for the render and
reference the single file from one `<audio>` element on a dedicated high `data-track-index`:

```sh
ffmpeg -i assets/master_audio.wav -c:a aac -b:a 192k assets/master_audio.m4a
```

```html
<audio class="clip" data-start="0" data-duration="12" data-track-index="9"
       src="assets/master_audio.m4a"></audio>
```

Videos stay `muted`; their audio (if any) is pre-mixed into the master too. Keep the master
length == composition duration so the gate script's audio + duration checks pass.


### Appendix: edit-report-template

# edit-report.md template

Write this to your project's `edit/edit-report.md`. It is the editor→reviewer handoff.
Fill every section; do not leave placeholders.

```markdown
# Edit report — {project}: {title}

**Disposition:** done | in_review | blocked
**Output:** edit/{file}.mp4 — {WxH}, {duration}s, {codec}, audio {present/absent}
**Style:** {style} (theme from styles/{style}/FRAME.md)

## Beat-by-beat edit decisions
| Beat / ts | A-roll | B-roll / MG | Cut & camera | On-screen super | SFX |
|-----------|--------|-------------|--------------|-----------------|-----|
| S1 0–2.2s | VO hook | — | kinetic text in | "..." (accent word) | click |
| ... | | | | | |

## Assets used
- {manifest file} → beat {S#}: {how used in the cut}. status: {gathered/alternate}.
- Built-in-editor MGs: {list} (no stock equivalent — designed on the style theme).
- Self-fetched (if any): {file} ← {source URL}, {tool}, {license}.

## Audio
- Voiceover: {voiceover/file}
- SFX: {list} — synthesized via ffmpeg (rights-free) | cleared asset {provenance}
- Mixed to single master: assets/master_audio.m4a ({duration}s, 48kHz stereo)

## Design decisions
- {any deviation from the style spec or editorial-look patterns: what changed, why.
  "None" if the edit is fully on-pattern.}

## Verification
- Preview: {beats screenshotted; pacing/layout/timing confirmed}
- Face check: {every person-frame shows the whole face centered in its panel — confirmed}
- Lint: {errors fixed}; warnings: {list + which are known false positives and why}
- ffprobe: {WxH} / {codec} / {fps} / {frames} / {duration} / {audio}
- Frame spot-checks: contact sheet at {path}; all required techniques render on-style.
- Gate script: PASS

## Rights flags
- needs-final-review: {assets, if any — confirm a license before publish}
- missing: {NONE in render — listed here if a beat still wants an official file}

## Gaps / next steps
- {anything deferred, any follow-up needed from the user}
```

Keep it readable: decisions and evidence, not narration. If blocked, the disposition line
and the gaps section must make the blocker and the next action unambiguous.


### Appendix: standard-provenance

# Standard provenance — adopted vs. added

Recorded so anyone reading the skill can see what is reused convention vs. added here.

## Sources researched
- The **hyperframes** docs (`npx hyperframes docs`, `llms.txt` index).
- **github.com/robonuggets/hyperframes-helper** — a HyperFrames helper repo.
- Reference stills from creator-grade shorts (Kallaway / Varun Mayya class).

## Adopted (industry / framework convention — reused as-is)
- **HTML-source-of-truth** composition model; `data-start`/`data-duration`/
  `data-track-index`/`data-media-start` timing; `class="clip"` for framework visibility
  control.
- **Paused GSAP timelines** registered on `window.__timelines["<composition-id>"]`;
  deterministic-only constraint (no random/now/fetch/`repeat:-1`).
- **GSAP easing vocabulary** — `power2.out` / `power3.out` for arrivals, `power1.inOut`
  for drifts.
- **Caption styling** — white text with a soft glow/stroke for legibility over any
  footage; SVG underline as a keyword-emphasis device.
- **The lint gotcha list** — notably the float-precision `overlapping_clips_same_track`
  trap, `muted` video + separate `<audio>`, and the self-attribute-selector warning.

## Added here (beyond hyperframes-helper)
- **Eased camera-motion system** with an explicit **anti-jitter contract**
  (`will-change`/`backface-visibility`/`translateZ(0)`/`force3D`, animate-the-wrapper-not-
  the-clip, small eased magnitudes, verify-in-render). hyperframes-helper has **no camera
  system at all**.
- **9:16 short-form grammar.** hyperframes-helper is **16:9-only**. This skill defines
  vertical-native engineered hooks, split→full-frame transitions, and **non-metronomic
  cutting down to 0.2s** tied to script energy.
- **Style-theming pipeline:** `styles/<style>/FRAME.md` → concrete `frame.md` design spec
  (palette tokens, local `@font-face` for offline-deterministic renders, motion-personality
  → easing/cut mapping, graphic devices).
- **SFX synthesis + master-track discipline:** rights-free ffmpeg-synthesized SFX and a
  single pre-mixed master audio track to avoid multi-`<audio>` echo/desync.
- **Render verification gate:** `scripts/verify-render.mjs` — ffprobe assertions (9:16,
  duration±tol, h264/yuv420p, audio present) plus contact-sheet frame spot-checks. Turns
  "looks fine in preview" into a hard, scriptable acceptance check.
- **Container-unit fidelity:** `container-type: size` on `#root` + `cqw`/`cqh` sizing so
  preview and render match exactly at 1080×1920.
