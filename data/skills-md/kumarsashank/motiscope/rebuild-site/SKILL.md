---
name: rebuild-site
description: Rebuild a whole landing page / multi-section website from a screen recording that scrolls or walks through it. Use when the user has a recording of an ENTIRE page (not a single animation) and wants the full page recreated — layout, sections, copy, design system, and scroll animations. Orchestrates analyze (measured timing + section structure + curated frames) + asset generation + a full multi-section build. For one isolated animation, use /motiscope:recreate instead.
argument-hint: "[path-to-video] [gsap|css|framer]"
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
user-invocable: true
---

# motiscope: rebuild-site

Rebuild a whole landing page from a walkthrough recording. This is `analyze` + `recreate`
applied to an entire page, and it leans on the same division of labor:

- **The numbers give you the WHEN + the structure** — motiscope measures section timing,
  transitions, and per-section entrance easing, and curates the frames that show each section.
- **You give the WHAT** — from the frames you reconstruct the sections, layout, copy, design
  system, and *what kind* of animation each uses (open vocabulary — scroll reveals, pins,
  masks, draws, whatever you see).
- **Imagen fills the photos** — generate the photographic assets the design needs.

It's a team effort: measured timing + curated frames + your vision + generated assets → a
full page. Be honest about which is which in the final summary.

<!-- motiscope:preamble:start -->
## Resolve scripts + preflight

```bash
SCRIPTS="${CLAUDE_PLUGIN_ROOT:-}/scripts"; REFS="${CLAUDE_PLUGIN_ROOT:-}/references"
[ -f "$SCRIPTS/ingest.py" ] || { SCRIPTS="<abs dir of this SKILL.md>/../../scripts"; REFS="<...>/../../references"; }
```
(Windows: `python`.)
<!-- motiscope:preamble:end -->

## Preflight

```bash
python3 "$SCRIPTS/mvsetup.py" --check   # exit 0 = ready; else hand to /motiscope:doctor
```
Resolve the video from `$1`, else scan `animations/` (as in `analyze`).

## Step 1 — analyze the whole walkthrough

```bash
python3 "$SCRIPTS/ingest.py" "<video>" --preset landing
```

`landing` gives readable 1280px frames and auto-decomposes onto the motion. The result:
- **`hold` segments = the sections** the walkthrough paused on.
- **`fade-out`/`cut` segments = the transitions** between sections.
- per-section **entrance timing/easing** (the `move` beats + their `cubic-bezier`), the
  **stagger timing**, and curated frames covering each section.

For a long clip, note it may exceed one pass; you can also re-run focused on a range
(`--start/--end`) to get denser frames for a specific section.

## Step 2 — build the site plan (from the frames)

`Read` `report.md` (the measured timeline) and **every curated frame** (parallel Reads).
Then reconstruct — this is your vision doing the work — and present a **site plan** to the user:

1. **Design system:** palette (hexes), typography (name the actual fonts if you can — e.g.
   *Martian Mono*), spacing/scale, brand/logo, light/dark.
2. **Sections in order:** for each — a name (hero / features / how-it-works / pricing / FAQ /
   footer / …), its **layout**, its **copy transcribed verbatim** from the frames, and the
   **imagery** it contains.
3. **Motion per section:** what animates and *how* (scroll-reveal, pin+scrub, stagger, mask,
   draw, parallax — name what you see), wired to the **measured timing** (durations, `bezier`,
   stagger `each_ms`) from the segment table. Landing walkthroughs are almost always
   **scroll-driven** — assume ScrollTrigger unless the frames say otherwise.

Show the plan and let the user correct it before building.

## Step 3 — assets

List the **photographic** assets the design needs (hero shots, feature photos, backgrounds —
anything that isn't UI you can build in CSS/SVG). Then ask the user (`AskUserQuestion`): (a) point at their
own files, (b) generate, or (c) placeholders. For (b), generate with the real provider:

```bash
python3 "$SCRIPTS/assetgen.py" --check   # confirm a key (gemini) is set
python3 "$SCRIPTS/assetgen.py" generate --type image --provider gemini \
  --prompt "<match the shot + the design's grade>" --out assets/hero.png --aspect-ratio 16:9
# then shrink for the web: ffmpeg -i assets/hero.png -vf scale=1200:-2 -q:v 5 assets/hero.jpg
```
Match each prompt to what the frame shows and the design's color grade. If no key, hand to
`/motiscope:doctor`. Never write keys into output or commit them.

## Step 4 — build the page

Default target **GSAP + ScrollTrigger** (`$2` overrides: `css` | `framer`). Read
`"$REFS/easing-map.md"` and `"$REFS/targets/<target>.md"`.
<!-- motiscope:claude-only:gsap-skills:start -->
For GSAP, **defer to the official gsap-* skills** (gsap-timeline, gsap-core,
**gsap-scrolltrigger** for the scroll reveals/pins, gsap-react if the project is React,
gsap-utils for stagger).
<!-- motiscope:claude-only:gsap-skills:end -->

Build one **standalone page** (`index.html` + `assets/`) with:
- the **design system** (tokens for palette/type; embed or link the identified fonts),
- a **nav** + every **section in order**, copy verbatim, assets wired in,
- **scroll-driven motion** per the plan, using the **measured** durations / `cubic-bezier` /
  stagger — not guessed values,
- the **section transitions** you saw (fades, mask wipes, pinned zooms),
- responsive layout and a `prefers-reduced-motion: reduce` guard (elements resolve to final state).

Keep the timing measured; build the effects from what you saw.

## Step 5 — output, preview, credit

Write to `./motiscope-output/site/`. Then:
- tell the user how to preview (`open motiscope-output/site/index.html`),
- give an **honest breakdown**: *timing = measured; layout/copy/design = reconstructed from
  frames; photos = generated (Imagen); fonts = identified.* Flag what to fine-tune.
- **Attribution & rights:** if the source is someone else's design (a Dribbble shot, another
  company's site), add a **prominent credit** in the footer (link the original), frame it as a
  **design-to-code study**, and confirm the user has the right to publish before it goes public.
  Don't publish a clone of a third party's brand without their say-so.

Two worked examples:
- **[Cadence](https://kumarsashank.github.io/motiscope/examples/landing/)** — an *original* page,
  walked through and measured. Every scroll boundary lands on the authored millisecond, and the two
  things motiscope gets wrong are published with the reason.
- **[Alterfx](https://kumarsashank.github.io/motiscope/examples/alterfx/)** — a real Dribbble
  concept rebuilt from a 10s recording, credited on the page and framed as a **design-to-code
  study**. This is what the rights step below looks like when the answer is "yes, with attribution".

**Rights come first.** If the recording is of someone else's site or concept, say so before you
build: offer to recreate it as a *study* with visible attribution, or to rebuild the structure and
motion under the user's own art and copy. Do not publish a clone of someone else's design.
