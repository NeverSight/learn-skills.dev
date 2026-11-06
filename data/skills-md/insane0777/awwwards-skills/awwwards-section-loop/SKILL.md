---
name: awwwards-section-loop
description: Use when recreating or rebuilding a multi-section page from a reference site — build section by section instead of all at once. Teaches the loop map (analyze_page_structure bands → capture_component per section → build → section gate from captured geometry and screenshots → lock → next), selector fallback rules learned from real captures, when a page must be treated as one unit (shared WebGL canvas), and the lock-before-next discipline that stops compounding drift. Pairs with awwwards-motion-study (motion recipe per section) and verify_build (aggregate evidence, not a per-section score).
---

# Awwwards Section Loop — build section by section, verify each, lock it

Building a whole page in one pass loses: attention splits across eight
sections, an early mistake silently propagates into every later one, and
feedback arrives only when everything is finished — too late to trace the
drift to the decision that caused it. The section loop fixes all three:
**one section gets full attention; each section is verified and locked
before the next starts; drift is caught where it began.**

The tools to run this loop already exist. This skill is the order to run
them in, and the judgment calls the tool outputs don't make for you.

> **Profile note:** this skill's tools are `analyze_page_structure`,
> `capture_component`, `analyze_stack`, `capture_pose_3d`,
> `analyze_scroll_map`, `analyze_hover_census`, `audit_url`, `analyze_bundle`,
> `build_gsap_stub` and retained `build_project` / `verify_build`. Examples
> below use 1.x names (default `full`). On `AWWWARDS_MCP_PROFILE=v2`, use
> `inspect_page {request:{kind:"structure", url}}`,
> `capture_page {request:{kind:"component", url}}`,
> `inspect_page {request:{kind:"stack", url}}`,
> `capture_page {request:{kind:"pose", url}}`,
> `analyze_motion {request:{kind:"scroll", url}}`,
> `analyze_motion {request:{kind:"hover", url}}`,
> `audit_page {request:{kind:"performance", url, compact:true}}`,
> `audit_page {request:{kind:"bundle", url}}` and
> `build_motion {request:{kind:"gsap_stub", scrollCensus}}`; `build_project`
> and `verify_build` stay flat. Feed `build_motion` a `compact:false` scroll
> census. Full mapping: [v2-routing.md](v2-routing.md).

## The loop

```
PLAN          analyze_page_structure(reference)   → band map = section plan
FOR EACH      capture_component(section selector) → section pack (recipe)
              build that section                  → in your output, fully
              gate that section                   → geometry + screenshots + checks
              iterate until every check passes    → then LOCK it
NEXT SECTION  (do not touch locked sections again)
FINALLY       whole-page verify_build             → aggregate + coherence pass
```

### Step 0 — Plan from the band map

`analyze_stack` first (one call): the site's framework, CSS framework, and
marker libs. A Webflow or WordPress source means conventions you re-skin;
a Next source means you can mirror component shapes. Then
`analyze_page_structure` returns ordered bands with `top`, `height`,
`bg`, and a text sniff. Treat the band list as the build order:

- **Small count, sane heights** (≤ ~3,000 px each) → bands map 1:1 to
  build sections.
- **One giant band** (5,000 px+) → the band collapsed multiple real
  sections (repeated `<section class="…">` siblings do this). Do not
  build it as one giant component. Drop to the raw page HTML and pick
  **explicit selectors** for the real sections (`.section`, `[role=…]`,
  `header`, `footer`, or `#id`s), one per logical section. Real-capture
  finding: a 20,631 px band held an entire main content area; the four
  real sections inside it captured fine by class.
- **Shared canvas / WebGL hero** spanning many bands → **the page does
  not slice.** Treat that canvas region as ONE unit: `capture_pose_3d`
  for canvas frames + synthesized camera guidance, rebuild as a single
  component, then loop normally for everything after it. For a Three.js
  scene, `capture_scene_3d` with `adapters:["three"]` adds only reachable
  nodes/cameras/lights; `build_scene_stub` recreates the supported primitive
  subset and exact captured camera matrix, while parent transforms are lost and
  controls are never recreated. For shader evidence, `adapters:["spector"]`
  captures one drawing frame with command counts and capped shader source — not
  arguments, state or raw capture. Slicing a shared-canvas page into
  per-section captures produces sections that each reference a canvas
  none of them own.

### Step 1 — Capture per section

`capture_component(selector)` per section, in band order. Selector
discipline (learned from real captures, in priority order):

1. Section class or id from the band/HTML (`.process`, `.pricing`,
   `.footer`) — most reliable.
2. `role` attributes (`[role="banner"]`, `[role="contentinfo"]`).
3. Tag names (`header`, `footer`, `nav`) — **last resort**: real sites
   frequently have no `<header>` element at all (a real capture of a
   Webflow site returned `selector not found: header` while `nav` and
   `.footer` worked).

If a selector misses, try the alternatives before shrinking the plan.
A failed capture with `selector not found` is a selector problem, not
a missing section.

### Step 2 — Build one section, completely

Build the section against its pack: layout from the pack's geometry,
tokens (fonts/colors/spacing) from its captured computed styles, motion
from the census (`analyze_scroll_map` + `analyze_hover_census` scoped to
the section, per awwwards-motion-study). Content is yours — structure,
motion, and tokens are what you're matching.

**Finish it.** A half-built section pollutes the next verify. No
placeholder blocks left "for later" inside a section you're about to
lock.

### Step 3 — Gate the section against its capture

Do not wait on `verify_build` for a per-section verdict. It compares the two
**whole pages** and returns one aggregate band score —
`bands: { score, matched, refOnly, buildOnly }` — not a score per band. It
cannot isolate section N, and running it after every section mostly measures
the sections you have not built yet.

Gate section N with evidence that is local to section N:

- **Geometry:** the band map (`analyze_page_structure`) gives the section's
  `offsetTop`, `height` and `background`; the section pack
  (`capture_component`) gives the root and child `rect` (`x`, `y`, `w`, `h`)
  plus computed styles. Measure the same nodes in your build (Playwright
  `getBoundingClientRect` / `evaluate`) and assert them within tolerance —
  e.g. section height ±2 %, child positions and column counts exact. This
  catches the 3×-height and collapsed-band bugs a whole-page average hides.
- **Screenshots:** capture the reference section and your build at the same
  viewport, pinned to the section center, and compare them side by side. A
  uniform page-fraction shot lands mid-transition and proves nothing.
- **Tokens and motion:** check the captured computed styles (fonts, colors,
  spacing) and the section-scoped census values (trigger, duration, easing,
  stagger) you built from.
- **Explicit checks:** write the pass conditions for this section before
  building it (height tolerance, columns, visible children, motion beats),
  then mark each pass/fail. "Looks close" is not a gate.

Only when every local check passes is section N locked. Use `verify_build` as
**aggregate evidence** after a few sections and at the end: its `bands.score`
shows whole-page similarity, `matched` / `refOnly` / `buildOnly` name which
band labels matched or are missing, and its motion score, `perf:` line
(`fps=… dropped=… longTasks=…`) and `anti-patterns:` count are page-level
evidence. If perf shows dropped frames, animation weight is the usual cause —
transitioning `filter: blur`, infinite loops, or animating layout properties.
Fix the prop, not the score. A good aggregate score never proves section N
locally; a local pass never proves the page is coherent.

**Why the section gate matters:** section-by-section without a gate is just
chunked guessing. Per-section geometry and screenshots turn "looks close" into
named numbers and a yes/no per section; `verify_build` then supplies a
page-level number without pretending to localize it.

### Step 4 — Lock before next

Locking = this section's markup/styles/motion are frozen. If a later
section reveals a problem that truly requires changing a locked section,
make the change **as an explicit re-open**: fix, re-run that section's
gate, re-lock. Never silently fudge a locked section while building another.

### Step 5 — Final coherence pass

After the last section locks: run whole-page `verify_build` as the
aggregate evidence pass — `bands.score` plus `matched` / `refOnly` /
`buildOnly`, the motion score, perf and anti-pattern lines. It does not
report per-band scores; use your per-section geometry and screenshots to
locate any section the aggregate comparison flags. Also run
`analyze_page_structure` once with `compare: "mobile"`: `mobileBands` +
`diff` (`bandsAdded`, `bandsRemoved`, `reordered`, `heightDelta`) name the
sections that only exist at 390×844 or changed order — a desktop-only
rebuild shows up here before the mobile smoke. You're now checking
cross-section things the per-section loop can't see: shared spacing
rhythm, consistent header behavior, scroll continuity, one easing family
across sections (or an intentional break). Fix coherence issues at the
page level (tokens, shared CSS), not by re-opening sections unless the
aggregate band comparison shows a regression — then use its
`refOnly`/`buildOnly` labels plus your own geometry to find the section.

### Step 6 — Convert only if the user asks

The single-file rebuild is a valid handoff. When the user asks for a project (or
picks a framework), convert: locked sections are exactly what `build_project
--target vite|astro|next` needs — the band split becomes components. If they also
want authored motion, add `--authored --motion census.json` and author per section
(see `motion-authoring`), keeping the same lock discipline: author section N,
re-run its section gate, lock, next. Whole-page desktop + 390 mobile parity last.

## Failure modes this skill prevents

| Failure | What you'd see | The rule that prevents it |
|---|---|---|
| Giant collapsed band built as one component | One "section" with 6 sub-layouts, all mediocre | Step 0 explicit-selector split |
| Selector miss treated as missing section | Whole region skipped in the rebuild | Step 1 alternatives ladder |
| Sliced shared-canvas page | Sections that each expect a canvas nobody renders | Step 0 one-unit rule |
| Placeholder left inside a "finished" section | Section gate never passes | Step 2 finish-it rule |
| Drift compounding through the page | Every section slightly worse than the last | Steps 3–4 gate+lock |
| Lock-fudging | Locked section regresses unnoticed | Step 4 explicit re-open |
| Per-section sections that don't rhyme | Page reads as stitched screenshots | Step 5 coherence pass |

## Companion tools

- `awwwards-motion-study` — the per-section motion recipe (record →
  inventory → build → re-record).
- `verify_build` — aggregate evidence (steps 3 and 5), **not** a per-section
  gate: one whole-page band score (`bands.score` + `matched`/`refOnly`/
  `buildOnly` labels) and a motion score, plus measured perf (fps, dropped
  frames, long tasks) and anti-pattern counts from instrumented live probes.
  Runs a real browser — expect ~2 min per call. For a shared WebGL canvas,
  opt-in `scene3d` replays a
  `capture_scene_3d` pack on the build canvas as a separate gate with its own
  status/verdict; it never upgrades the legacy band pass, unstable capture
  frames are rejected, and its build URL must resolve publicly (loopback is
  refused). It preflights both URLs before the legacy scans and makes zero
  requests when either is private; the deadline is the replayed checkpoint
  waits + 10 s headroom (floor 15 s, cap 45 s), and the canvas gets a per-run
  marker so duplicate or pre-marked decoys are refused.
- `audit_url compact:true` — quick perf and anti-pattern checks when you only
  need the summary, not the full evidence.
- `capture_pose_3d` - canvas frames + synthesized camera guidance for
  shared-canvas units (step 0); no camera transforms are recovered, and the
  generated stub dedupes same-index frame loads and discards stale decodes.
- `capture_scene_3d` + `build_scene_stub` - opt-in Three.js adapter for
  shared canvases: reachable globals only, with primitives, standard/basic
  materials and a perspective camera from its exact matrix reconstructed.
  Captured controls are never recreated and stay unresolved. Module-local
  scenes, parent transforms and unbound textures are lost, and `scene.json`
  frame references are basenames extracted from either Windows or POSIX paths.
- `capture_scene_3d` spector adapter - optional `spectorjs@0.9.33`; captures one
  WebGL frame with command counts/statuses and capped shader source. It needs a
  drawing frame, transfers no arguments/state/raw capture, and a missing package
  only degrades the adapter.
- `analyze_scroll_map` / `analyze_hover_census` - per-section motion
  census to build from. `analyze_scroll_map` rows now carry keyframe
  value-pairs and a site-level `gsapTriggers` list (numeric pixel
  start/end, live progress, tween vars) — build from measured values,
  not invented ones. Hover samples include animations captured DURING
  the hover (`activeAnims`), which is how event-driven tweens get seen.
- `build_gsap_stub` - turns the captured censuses into a runnable
  GSAP+ScrollTrigger stub (durations, easings, scrub/pin, synthesized
  camera guidance from `capture_pose_3d`, reduced-motion guard) - step 2's
  motion wiring, generated.
- `build_project` — build → convert → own the motion: `--target vite|astro|next`
  gives native structure (section components, shell, split CSS, ordered libs);
  `--authored --motion census.json` drops site logic and emits
  `motion.manifest.json` + per-section/page motion hooks to author against (pair
  with `motion-authoring`); always re-verify after conversion.
- `analyze_bundle` - mechanism recovery (step 2 escape hatch): when a
  section's effect can't be explained from the census evidence, grep the
  section site's script bundle for mechanism keywords; the censuses say
  WHAT animates, the bundle says HOW.
