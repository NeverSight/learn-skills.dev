---
name: awwwards-web-design
description: "Evidence-grounded web UI/UX design and build skill for Awwwards-level sites (Site of the Day / Month / Year quality). Use when building or redesigning a landing page, portfolio, product or launch site, brand or campaign site, e-commerce storefront, or an immersive 3D/WebGL or scroll-storytelling site; when choosing a design direction, signature idea, typography, color, layout, motion, imagery or 3D approach; or when auditing a site against award standards. Built from a 732-site Awwwards corpus, 51 audited teardowns, a 554-site font census and 7 cited research files. If an anti-slop design law (for example pols.dev/slop.md) is installed, it outranks this skill."
license: MIT
compatibility: Instructions work in any agent. Scripts need Python 3.10+; scripts/site_probe.py and the recipe tests also need uv (or pip), Playwright and a one-time Chromium download, plus network access. Scripts will not run in sandboxes without network (claude.ai, Skills API).
metadata:
  version: "1.0.0"
  author: owenisas
  homepage: https://github.com/owenisas/awwwards-web-design
---

# Awwwards web design

Last updated: 2026-09-25

This skill teaches the language award juries reward: one owned idea, rendered live, on a tight system, with usability that holds up. Every rule traces to measured evidence in `data/`. Take the design language from the winners, never their content.

**Precedence:** the user's explicit instruction > an anti-slop design law if your setup has one (for example `deslop-law`, from https://pols.dev/slop.md) > this skill > your defaults. The references are written to stand on their own: every place where award habits conflict with anti-slop craft already gives the crafted version. Where winners use a slop tell (hidden-until-revealed content, underline-fill hovers, hover lifts, saturated accent chips, cream grounds, grain over text), the references give the crafted version. Build that.

All paths in this skill are relative to this skill's directory (the folder that contains this SKILL.md). Run scripts from there, for example `uv run scripts/site_probe.py https://example.com`. First run only, for the Playwright browser: `uvx --from playwright==1.63.0 playwright install chromium`.

## Works with (optional)

If an anti-slop design law skill is available (for example `deslop-law`, from https://pols.dev/slop.md), load it first; where the two conflict, it wins. If none is installed, continue with this skill alone.

## The loop

Work through these steps in order. Each step has an output. Do not skip to code.

| # | Step | Load | Output |
|---|------|------|--------|
| 1 | **Brief** | [content-voice](references/content-voice.md) | What the brand really has: an object, a place, footage, text, a body of work, a service. List its real specifics (names, numbers, dates). No lorem. |
| 2 | **Jury lens** | [jury-lens](references/jury-lens.md) | Target band (SOTD ≈ 7.4, SOTM ≈ 7.7) and where points are cheapest for this brief. |
| 3 | **Direction** | [directions](references/directions.md) | One primary direction from the ten, plus at most one secondary layer, chosen with the direction picker. |
| 4 | **Signature** | [directions § Inventing the signature](references/directions.md) | One sentence: the brand's own object, material or process, which the visitor *plays*. It must survive with motion off, and it must recur at 3+ touchpoints (loader, nav, transition, footer). |
| 5 | **System** | [typography](references/typography.md), [color](references/color.md), [layout](references/layout.md), [motion](references/motion.md) | Named faces with sizes at 1440 and 390; ground/ink/accent tokens; grid and section rhythm; one ease family and one duration ladder (use `recipes/tokens.css` names). |
| 6 | **Imagery and 3D** | [imagery](references/imagery.md), [webgl-3d](references/webgl-3d.md) | Media archetype and art-direction rules; a 3D decision from the tree (none, video/sequence, Spline, three.js, R3F, shaders), with its budget and fallback. |
| 7 | **Interaction** | [interaction](references/interaction.md) | Nav/menu, hover language, cursor (native kept), loader, transitions, footer, 404, sound (opt-in). |
| 8 | **Build** | [recipes/](recipes/README.md) | Code on the visible-by-default contract: content renders with no JS, no WebGL and no CDN. Motion inside `gsap.matchMedia` no-preference only. |
| 9 | **QA gates** | [quality-gates](references/quality-gates.md) | Probe your build at 1440 and 390, view each screenshot on its own, and run the no-JS, reduced-motion, no-WebGL and CDN-blocked scenarios. |
| 10 | **Self-score** | [jury-lens § rubric](references/jury-lens.md) | A score per criterion with evidence. Anything below its band goes on the fix list, and a house-law failure blocks shipping. |

For worked examples, [casebook](references/casebook.md) has all 51 winners: signature, stack, type, color, motion and what to steal. Open `data/teardowns/<slug>.json` for the full evidence.

## The ten directions (step 3)

Each of the 51 teardowns has one primary direction. The full recipes, exemplars and slop versions are in [directions](references/directions.md).

| Direction | First screen owned by | Display type | Palette | Motion clock | Pick it when the brief has |
|---|---|---|---|---|---|
| **Flown world** (10) | a lit scene flown by an authored camera | DOM 30-82px; a giant word on 4/10 | 75-92% scene or void, one emissive hue | camera leads; world 4-7s, DOM 0.3-0.7s | an abstract or invisible offer (platform, protocol, holding) |
| **Playable toy** (5) | a toy you operate | UI 13-20px, one statement 48-162px | one saturated field | springs and held poses | a creative-dev portfolio or campaign where the visit is the product |
| **Object hero** (6) | one lit product | 110-350px, occluded by the object | studio field, color from the material | the object moves first and alone | a physical product whose form or mechanism is the pitch |
| **Reel as interface** (4) | full-bleed footage | credit ~40px or wordmark 90-175px | black or white shell, no UI accent | little moves at once | work that is moving image |
| **Editorial catalogue** (4) | type on a visible grid | 137-231px | paper, ink, one full field | masked rises 1.0-1.3s | an archive, museum, research or long-form text |
| **Kinetic poster** (3) | condensed caps plus one figure | 180-317px | a duotone pair per section | snappy, 16-22ms char stagger | a loud youth, sport, drink or gaming brand with owned colors |
| **Illustrated story** (4) | commissioned characters | 144-293px | section color = chapter | Rive/Lottie characters, plain UI | a warm human service or nonprofit with no photogenic product |
| **Material calm** (5) | a material in soft light | 48-58px (one monument allowed) | material neutral, deep ink, accent near 0 | slow; a 400/800/1200ms ladder | a place (residence, resort, venue) or a high-consideration material |
| **Process filter** (5) | every image through one render grammar | 80-194px | a strict pair forced through the filter | shader leads, stepped time | mixed media that must read as one voice |
| **Archive index** (5) | the body of work itself | 16-250px | neutral chrome; the work brings color | one scroll value drives everything | a portfolio where range is the proof |

Tie-breakers:
- Task-first pages (checkout, catalogue, lead form) keep native scroll and DOM content, so use object, calm, editorial or index there.
- With no 3D budget (under about 1.5 MB compressed before first interaction on mobile), step down to a 2D direction.
- Before designing, write the decision as one line:

`<Direction> (+ <secondary>) for <brand>: <signature sentence>. Ground <hex>, ink <hex>, accent <hex or none>. Display <face> at <px>. Clock <ease family>, ladder <ms>.`

## Crafted vs slop (the crosswalk)

Winners often ship the left column. Build the right one.

| Award habit | Slop version | Crafted version |
|---|---|---|
| Scroll reveals | sections authored at `opacity: 0` waiting for an observer (45/51 winners) | content at rest in CSS; a small y-settle or clip created in the frame its tween starts ([recipes/motion-core.js](recipes/motion-core.js)) |
| Preloader | a timed 0-100 counter over the whole site | honest progress on real promises, intro ≤ 1.5s, skippable, once per session |
| Link and button hover | an underline that wipes in; a button that lifts or scales | a tonal fill or ink change, or an icon sliding inside a static box ([recipes/magnetic.js](recipes/magnetic.js)) |
| Accent color | one neon splashed on chips, dots and CTAs | one owned hue as a whole field or the object's material; everything else in tonal steps |
| Luxury ground | cream or oat plus a letterspaced Didone | a ground sampled from the material (plaster grey, stone, fog) and a serif chosen for a detail of the place |
| Texture | grain over the whole page, including text | grain or dither on the substrate or inside one display word only |
| Background canvas | a fixed field trailing behind every section and the nav | a field that reacts (cursor, per-section color) and ends where its chapter ends |
| Footer wordmark | a giant word, clipped and floating | anchored flush to the bottom edge, bleeding off it on purpose, above any texture, never shaved |
| Custom cursor | the native cursor hidden, a blob follower | the native cursor kept; a follower only on fine pointers with full motion, used as a label |
| Type | Inter, Space Grotesk, Syne or Fraunces carrying the brand | a licensed or distinctive display face with a truly neutral body ([typography](references/typography.md)) |
| Text in WebGL | headings drawn only in the canvas | the DOM owns every word; the canvas is `aria-hidden` decoration |

## Pre-ship checklist (condensed)

Tick a line only when you have the evidence for it. The full checklist is in [quality-gates §6](references/quality-gates.md).

- [ ] No-JS, no-WebGL and CDN-blocked screenshots of every route show all text, images and links.
- [ ] Reduced motion: no transforms, Lenis off, WebGL still, video paused, and the page still composed. The OS setting can flip live.
- [ ] Every loop longer than 5s has a pause control. Sound is opt-in. Nothing flashes more than 3 times a second.
- [ ] The skip link comes first, focus is visible (2px, 3:1) and never under the sticky header, Esc returns focus, and anchors plus find-in-page work under smooth scroll.
- [ ] Text contrast is ≥ 4.5:1 (3:1 at 24px and up) on the worst frame behind it. Targets are ≥ 24px, and primary targets ≥ 44px.
- [ ] Mobile p75: LCP ≤ 2.5s on DOM text or a poster, CLS ≤ 0.1, INP ≤ 200ms. The budgets in quality-gates §3 are met.
- [ ] One server-rendered `h1`, landmarks, `lang`, title, description and OG per route. No console errors, debug GUIs, localhost URLs or trial fonts.
- [ ] The 390px first screen, loader, footer and 404 are designed, not leftovers.
- [ ] Every screenshot was viewed on its own at full size, with clipped edges zoom-checked.
- [ ] The jury-lens rubric is scored with evidence, there are zero house-law failures, and the signature survives with motion off.

## Numbers card (measured)

| Fact | Value | Source |
|---|---|---|
| Score formula | 0.4 Design + 0.3 Usability + 0.2 Creativity + 0.1 Content | jury-lens |
| Recent SOTD median / SOTM median | 7.38 / 7.73 | `data/stats.md`, awwwards-editorial |
| Lowest sub-score | Usability on 47/51 teardowns; Accessibility lowest dev score (mean 6.83 vs Animations 8.01) | stats, teardowns |
| Display type at 1440 | median 80px, p75 ≈ 150px, max 346px | `data/probe_summary.json` |
| Display type at 390 | median ≈ 47px (p25 32, p75 80) | probe_summary |
| Display tracking / line-height | median −0.023em (p25 −0.04) / 0.83–1.0 | probe_summary |
| Body size | median 14.4px (p75 16.7) | probe_summary |
| Font families per site | median 2; ~10% load Google Fonts; top family (Inter) on only 11% | `data/font_census.json` |
| Palette | 1–2 recorded colors; near-black and near-white dominate; accents are unique per brand | stats (2024+ cut) |
| Canvas | webgl2 on 43/51; 3D asset files on 26–28/51 (.glb, .ktx2, .exr/.hdr) | probe_summary |
| Motion stack | Lenis 85/117 and ScrollTrigger 84/117 recent SOTDs; gsap 3.15.0, lenis 1.3.26, three r186 | motion-stack research |
| Top CSS easings | `cubic-bezier(0.4,0,0.2,1)`, `(0.19,1,0.22,1)` expo-out, `(0.215,0.61,0.355,1)` cubic-out | probe_summary |
| Durations | hover 200ms, menus/cards 600ms, a reveal 1000ms, hero intro ≤ 1400ms | motion, tokens.css |
| Reduced-motion rules shipped | 11/51 winners (cheap differentiation) | probe_summary |

## Hard rules

1. **Content is visible by default.** No text, image or control waits on JS, a CDN, WebGL or a scroll trigger. Hidden start states are set by JS in the same frame the tween starts.
2. **One owned idea, rendered live, that the visitor completes.** Not ten effects. The signature comes from the brand itself and recurs.
3. **Commit to one direction.** It fixes what owns the first screen, the motion clock and the palette structure. A secondary direction adds one layer only.
4. **Palette: one ground, one ink, at most one owned hue** at 5% of the area or less, or as a whole field or object color. Everything else is a tonal step.
5. **Licensed or distinctive display type** that is deliberate and measured. It never carries the signature in a Google-shelf default. Pair it with a truly neutral body face.
6. **One ease family, one duration ladder.** Duration scales with distance. Stagger follows reading order, with a total spread of at most 0.6s. Overlap beats; do not queue them.
7. **One hero moment per viewport.** World or object moves first, type second, chrome last.
8. **Hover never moves the box and never animates an underline.** State changes are tonal or typographic, or happen inside a static box.
9. **3D only when it carries the subject.** Budget it first: DPR clamp, on-demand frames, init after LCP, pause offscreen, poster fallback. The canvas is `aria-hidden` and the DOM owns every word.
10. **Reduced motion is a designed state.** CSS, GSAP, Lenis, WebGL and video all follow it. Anything that moves on its own for more than 5s gets a pause control.
11. **Usability is where points are left.** Clear orientation, a skip link, visible focus, 4.5:1 contrast on the worst frame, 24px minimum targets, and a mobile input model of its own.
12. **Core Web Vitals at mobile p75:** LCP ≤ 2.5s (DOM text or a poster, never a canvas), INP ≤ 200ms, CLS ≤ 0.1. A loader must earn its place and end within 1.5s.
13. **Design the 390px first screen, loader, footer and 404** as deliberately as the hero. Jurors look at all of them.
14. **Real content only.** Specific names, numbers and stories; no lorem, no stock filler, no template demos.
15. **Dead is a fail too.** Every page ships a hero intro, one signature moment that responds to scroll, pointer or state, a nav that enters and responds, and crafted hovers.

## Reference map

| File | Load when |
|---|---|
| [jury-lens](references/jury-lens.md) | Setting targets; self-scoring; deciding where effort pays |
| [directions](references/directions.md) | Choosing the art direction and inventing the signature |
| [typography](references/typography.md) | Picking faces, sizes, tracking, type moves, font loading |
| [color](references/color.md) | Building palette tokens, section color shifts, texture, contrast |
| [layout](references/layout.md) | Grids, first-screen ownership, section rhythm, mobile re-composition |
| [motion](references/motion.md) | Smooth scroll, easing/duration tokens, reveals, pins, transitions, reduced motion |
| [imagery](references/imagery.md) | Photography, CGI, illustration, video, treatments, asset pipeline |
| [webgl-3d](references/webgl-3d.md) | Any 3D or shader decision, asset pipeline, budgets, fallbacks |
| [interaction](references/interaction.md) | Nav, menus, cursors, hovers, loaders, galleries, 404, sound |
| [content-voice](references/content-voice.md) | Headlines, voice, narrative arc, microcopy |
| [quality-gates](references/quality-gates.md) | Accessibility, performance budgets, QA procedure, pre-ship checklist |
| [casebook](references/casebook.md) | Concrete exemplars for any decision |
| [recipes/](recipes/README.md) | Tested code: tokens, motion core, transitions, WebGL image hover, three.js hero |
| `data/research/*.md` | Deep, cited background: editorial, motion stack, WebGL stack, typography, elements catalog, a11y/perf, imagery |

## Audit mode (scoring an existing site)

1. `uv run scripts/site_probe.py <url> --out <dir> --name <slug>` writes eight 1440px scroll screenshots, two 390px shots and `probe.json` (libraries, canvas contexts, 3D assets, fonts, type scale, easings, CSS features, reduced-motion rules).
2. View every screenshot individually. Never build a montage.
3. Fill in `data/teardowns/_TEMPLATE.json` for the site, separating observed from inferred.
4. Score it with the jury-lens rubric and list slop tells from the house law. Report the gaps as a fix list, with numbers.

## Refresh mode (rebuilding the evidence)

Run these from the skill directory. Each step is resumable.

```bash
python3 scripts/awwwards_corpus.py all --out data --cache <cache-dir>
```
```bash
python3 scripts/select_sample.py --corpus data/corpus.jsonl --out data/sample.json --since 2024
```
```bash
python3 scripts/gather_evidence.py --sample data/sample.json --out evidence --jobs 5
```

Then write and audit the teardowns (one JSON per site, following `_TEMPLATE.json`), and regenerate the derived files with `build_digests.py`, `build_casebook.py`, `probe_summary.py --sample data/sample.json` and `font_census.py`.

Probing notes:
- `site_probe.py` uses the real GPU (`--gpu metal`) and a desktop Chrome user agent. Sites that gate on GPU tier (for example Active Theory) reject SwiftShader and headless user-agent strings; use `--gpu swiftshader` only on Linux or CI.
- Some sites need `--settle 12` to get past preloaders.
- Awwwards listing pages serve plain HTML to a desktop user agent. The palette presets from before 2022 (#2779A7, #D14836, #ECD06F) skew the all-time stats, so use the 2024+ cut.
