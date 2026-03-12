---
name: motion-graphic-director
description: "Creative direction and design intelligence for Remotion motion graphic videos. Use when an agent needs to (1) convert a script or SRT into a shot-by-shot visual design document, (2) ideate motion graphics with editorial intent for each scene, (3) produce a design brief for user approval before writing Remotion code. Always use before generating any Remotion video code from a script."
---

# Motion Graphic Director

This skill makes you think like a professional motion graphic director and video editor before
touching any code. The output quality of the final Remotion video is entirely determined by the
quality of the design decisions made here — and by whether those decisions were translated into
exact frame numbers before implementation began.

## The Pipeline

Every video follows this exact sequence. Do not skip steps.

```
1. SRT/Script Input
2. Script Analysis       →  script-[name].md
3. Visual Ideation       →  video-design-[name].md   (shown to user for approval)
4. User Approves Design
5. Frame Timing          →  frame-timing-[name].md   (calculator + beat table for every scene)
6. User Approves Timing
7. Remotion Build        →  uses remotion-best-practices skill
```

Steps 3 and 5 both require user approval before proceeding. Step 5 is not optional —
it is where every timing bug, dead-air problem, spring misconfiguration, and transition
conflict is caught on paper instead of in a render.

---

## Step 1: Parse the Script

If given an SRT file, run the bundled converter script:

```bash
python scripts/srt_to_script.py <input.srt> "<Video Title>" [output.md]
```

This produces a `script-[name].md` with one segment per SRT cue and exact voiceover text —
matching the format of the example scripts in `examples/`. The segment names will be generic
placeholders ("Segment 1", etc.) — rename them to meaningful scene names during Step 2 analysis.

If given raw voiceover text instead of an SRT, structure it manually into the same format.
See `references/design-doc-format.md` for the exact format and `examples/video-script-1.md`
as a reference.

---

## Step 2: Analyze Before Ideating

Before designing anything, extract from the script:

- **Core thesis** — what is the single idea being proven?
- **Emotional arc** — where does tension rise? where is relief? where is the climax?
- **Key terms** — which words/concepts deserve a dedicated visual metaphor?
- **Target viewer** — tech-savvy? general? what is their assumed anxiety or curiosity?
- **Video duration** — determines pacing budget per segment

This analysis drives every design decision. Never skip it.

---

## Step 3: Ideate the Design

This is the most important creative step. Think like a director, not a programmer.

### Core Design Decisions (make these first)

**1. Visual Identity**
- Choose a 2-3 color palette. Typically: 1 dark/neutral background + 1 blazing accent +
  1 secondary accent for "error/wrong" states
- Every color must have a *meaning* — train the viewer to associate it with an emotion
  (e.g., green = correct/progress, red = wrong/warning)
- Choose a single dominant typographic style (monospace/hacker, bold serif/editorial, clean sans)

**2. Dominant Visual Metaphor**
- What is the ONE central metaphor that visualizes the core thesis?
- This metaphor must be introduced in the hook and returned to at the resolution

**3. Pacing Architecture**
- These videos are relentlessly fast-paced — constant motion, no dead air, visuals always
  serving the voiceover rhythm. Study the example files to calibrate your instincts.
- No single static element should sit idle for more than ~22 frames (~0.73s at 30fps) without
  purpose. If nothing is moving, there must be a deliberate reason.
- Plan the tension curve: Hook → Build → Pattern Interrupt → Teach → Climax → Resolution → CTA
- See `references/editorial-patterns.md` for tension/relief patterns

**4. Motion Graphic Vocabulary**
- Decide on 2-3 signature animation moves that repeat
- Read `references/motion-graphic-prompts.md` as an idea library

### Per-Segment Design Rules

For each segment, answer these questions in order:

1. What is the viewer's mental state entering this segment?
2. What single concept must they understand by the end?
3. What is the strongest visual metaphor for that concept?
4. What is the background/environment doing?
5. What exactly animates in, and how?
6. How does this segment transition out, and why that specific transition type?
7. Why did you make these choices? (the editorial intent — always write it)

---

## Step 4: Document the Design

Output a `video-design-[name].md` file with one section per segment.

Each segment follows the **exact same 4-subsection format** as the video-example files:

```
## [timestamp] | [Scene Name]

**Backgrounds & Tints:** ...

**Motion Graphics & Typography:** ...

**Transitions & Pacing:** ...

**Editorial Thinking/Intent:** ...
```

This document is what the user reviews and approves. It must be detailed enough that a
skilled developer could implement it without asking questions.

See `references/design-doc-format.md` for a fully worked example.

---

## Step 5: Frame Timing Document

This step happens **after design approval** and **before writing any Remotion code**.

The frame timing document (`frame-timing-[name].md`) translates every creative decision from
the design doc into exact frame numbers. It is the engineering specification. Frame is the unit
of everything here — not seconds, not "about halfway through." Every animation beat, every
transition window, every hold gets an explicit frame range.

This is where the following problems are caught on paper — before they are rendered:
- Dead air (scenes holding idle for too long after the last animation)
- Spring misconfiguration (underdamped springs that oscillate instead of popping)
- Transition conflicts (scene-level entry animations that fight TransitionSeries)
- Frame math errors (TOTAL off because transition overlap wasn't subtracted)
- Phase sequencing errors (Phase 2 firing before Phase 1 finishes)

### Substep A — Run the frame calculator

```bash
python scripts/frame_calculator.py \
  --fps 30 \
  --durations <S1_dur> <S2_dur> ... <SN_dur> \
  --transition <T_dur> \
  --names "Scene 1 Name" "Scene 2 Name" ... \
  --last-anim <last_anim_local_1> <last_anim_local_2> ... \
  --springs "springLabel:damping:stiffness[:mass]" ...
```

The calculator outputs:
- Absolute start/end frame for every scene and every transition window
- Local ↔ absolute frame conversion for every scene
- Dead air warnings per scene (flags if idle > 22f before transition exit)
- Spring ζ (damping ratio) and settle time for every config

**Do not compute these numbers by hand.** Off-by-one arithmetic propagates silently into
code. Run the calculator, paste its output verbatim into the frame timing document header.

Example invocation for a 6-scene video with spring analysis:
```bash
python scripts/frame_calculator.py \
  --fps 30 \
  --durations 150 180 150 210 200 120 \
  --transition 15 \
  --names "Hook" "Definition" "Solution" "Demo" "Processing" "Dialogue" \
  --last-anim 125 150 110 178 177 95 \
  --springs "errorStamp:10:300" "staccatoPop:28:400" "cardEntrance:12:200"
```

### Substep B — Write the per-scene beat table

For every scene, produce a table of frame ranges covering every distinct animation beat.
Ranges must be contiguous — no gap, no unexplained jump. Both local and absolute frame
columns are required in every row.

| Frame Range (local) | Absolute Range | What Happens | Notes / Risks |
|---------------------|----------------|--------------|---------------|
| 0–44                | 0–44           | ... | ... |
| 45–52               | 45–52          | ... | ... |
| ...                 | ...            | ... | ... |

Any range that has no authored animation must still appear in the table as a named hold:
"Hold — [what is still visible, what micro-animation keeps it alive]." Never leave a gap.

### Substep C — Write a dedicated section for every transition

Each transition gets its own section. Do not summarize transitions inside the scene table.
Every transition section must answer:

1. **What presentation is used** — exact import path and function call
2. **What timing is used** — `linearTiming` vs `springTiming` and why
3. **Editorial intent** — why this specific transition at this narrative beat; what would be
   wrong about using a different type here
4. **What each scene is doing during the overlap window** — what is visible/animating in the
   exiting scene during its last T frames, and what the entering scene shows during its first
   T frames
5. **Specific risks** — anything that can go wrong at this exact transition point

### Substep D — Verify frame math

Manually verify the total before committing to code:

```
TOTAL = sum(all scene durations) - (num_transitions × transition_duration)
```

Write this calculation explicitly in the document. If `TOTAL` does not match what you put in
`SCENE_TIMING.TOTAL` and `Root.tsx durationInFrames`, the video will cut early or have a
blank tail. This is a non-negotiable check.

See `references/frame-timing-format.md` for the complete format spec and a fully worked
example covering all 6 scenes of the VibeCodingPRD video.

---

## Step 6: Wait for Approval

Present the frame timing document to the user. Do not start writing Remotion code until they
approve. If they request changes, revise the frame timing document — not the code.

If the user requests changes to the design doc at this stage, rerun the calculator with
the updated durations before proceeding. Duration changes ripple into every absolute frame
number downstream.

---

## Step 7: Build with Remotion

Once both the design doc and frame timing document are approved, use the
`remotion-best-practices` skill to implement. The frame timing document is your spec.

**Key implementation principles:**
- Every animation is driven by `useCurrentFrame()` — no CSS transitions
- Scene timing constants derive from the frame timing document — no magic numbers in components
- `SCENE_X_START` values are not needed when using `TransitionSeries` — positions are
  auto-calculated. Only duration constants are needed.
- Color values from your chosen palette must be defined as constants, not inline
- Every visual metaphor described in the design doc must be present in the code
- Phase N start frames must be derived from Phase N-1 end frames, not hardcoded:
  ```ts
  const PHASE2_START = PHASE1_END + HOLD_DURATION; // NOT a literal number
  ```

---

## Quality Bar

Before finalizing a design doc, check every segment against this list:

- [ ] Background is doing something — it has a color/texture with intent, not default grey
- [ ] There is at least one visual metaphor (not just text on screen)
- [ ] Transitions use specific easing descriptions (not just "fades in")
- [ ] The editorial intent explains viewer psychology, not just what happens visually
- [ ] Color is used consistently — same color means same thing throughout
- [ ] The hook grabs attention in the first 2 seconds
- [ ] There is at least one pattern interrupt (tonal shift, meme, unexpected visual)
- [ ] The final segment creates a visual vacuum — strips everything to focus on CTA or punchline
- [ ] Pacing varies — not every segment is the same visual density
- [ ] Every scene has a micro-animation in its hold period (no pure-static frames)

Before finalizing a frame timing document, check every scene against this list:

- [ ] Every frame range is accounted for — no unexplained gaps
- [ ] Both local and absolute frame numbers are shown for every range
- [ ] Dead air idle frames are within budget (≤ 22f) or explicitly justified
- [ ] Every spring config has been run through the calculator and ζ is in the intended range
- [ ] Every transition has its own dedicated section with intent and risk
- [ ] Frame math total is verified with the explicit arithmetic written out
- [ ] Phase start frames are derived values, not literals

---

## What Can Go Wrong

These are the failure modes encountered in real production. Each one destroyed renders that
looked correct in code review. Know them before writing a single line.

---

### 1. Dead Air — The Static Tail

**What it looks like:** The last animation in a scene finishes and the scene sits frozen for
1–3 seconds before the transition fires. The viewer disengages. Watch time drops.

**Why it happens:** Scene duration was set generously ("give it some breathing room") without
accounting for when the last animation actually ends. A scene with duration 180f where the
last animation ends at local frame 120 has a 60-frame static tail (2 seconds of nothing).

**How to catch it:** Run `--last-anim` flags in the calculator. Any scene reporting
`idle > 22f` has a static tail.

**How to fix it:**
- Shorten the scene duration so `scene_duration ≈ last_animation_end + 20f hold + transition_duration`.
- If you cannot shorten (design reasons), add a micro-animation — glow pulse, cursor blink,
  ambient particle — to bridge the hold. The frame must never be fully static.

**Budget:** ≤ 22 idle frames between last authored animation and start of transition exit.
This is ~0.73s at 30fps — enough for the viewer to absorb the final state without disengaging.

---

### 2. Spring Misconfiguration — Continuous Oscillation

**What it looks like:** Elements that should "pop" in with a single snappy overshoot instead
bounce back and forth repeatedly. Pill cards, checkmarks, and icon entrances all look jittery
and amateurish. The animation never settles cleanly.

**Why it happens:** The spring damping ratio ζ is below 0.5. With `damping: 8, stiffness: 400`,
ζ = 0.2 — heavily underdamped. The element oscillates for 3+ seconds. With `damping: 28, stiffness: 400`,
ζ = 0.7 — lightly underdamped, single clean overshoot to ~105%, settles in 12 frames.

**The formula:**
```
ζ = damping / (2 × sqrt(stiffness × mass))
ζ < 0.5  →  wrong. Will oscillate.
0.5–0.85 →  correct for pops. Single overshoot, snappy settle.
0.85–1.0 →  correct for slides and magnetic clicks. Near-critical, smooth.
> 1.0    →  overdamped. Slow creep, no overshoot. Use for deliberate heavy entrances.
```

**How to catch it:** Run `--springs "label:damping:stiffness"` in the calculator. Any config
with ζ < 0.5 is flagged. Do this before writing the component.

**How to fix it:** Increase damping. For stiffness 400, damping 28 gives ζ = 0.70. For
stiffness 200, damping 20 gives ζ = 0.71. Rule of thumb: target ζ ∈ [0.65, 0.80] for pops.

**Common misconfigured presets to avoid:**
```ts
// WRONG — ζ = 0.20, will bounce for 3 seconds
spring({ damping: 8, stiffness: 400 })

// WRONG — ζ = 0.25, same problem
spring({ damping: 10, stiffness: 400 })

// CORRECT — ζ = 0.70, single pop
spring({ damping: 28, stiffness: 400 })
```

---

### 3. DIY Entry Animation Conflicting With TransitionSeries

**What it looks like:** A scene that enters via TransitionSeries slide or wipe appears as a
blank panel sliding in, then the content snaps into existence partway through the transition.
Or the content is clipped during the slide and only becomes visible when the slide completes.

**Why it happens:** The scene component's outermost `AbsoluteFill` has a `clipPath`,
`transform`, or `opacity` entry animation applied to it. TransitionSeries wraps each scene
in its own container and applies the transition transform to *that wrapper*. Any clip-path or
transform on the inner `AbsoluteFill` composites on top of the wrapper transform, producing:
- Clip-path on inner element → content is invisible during slide (clip at 0%)
- Transform on inner element → double-transformed, moves incorrectly
- Opacity on inner element → fades independently of the slide, creates ghost effect

**Classic example:** A radial circle-wipe clip-path on the outermost `AbsoluteFill`:
```tsx
// WRONG — clip-path at frame 0 is 0%, so scene slides in blank
<AbsoluteFill style={{ clipPath: `circle(0% at 50% 50%)` }}>
```

**How to catch it:** In the frame timing document, the transition risk section must
explicitly state whether the entering scene has any entry animation on its outermost element.
If it does, it must be removed before the TransitionSeries transition is applied.

**How to fix it:** Move all entry animations to child elements inside the outermost
`AbsoluteFill`. The outermost element must be a plain container with no transform, clip-path,
or animated opacity. Let TransitionSeries own the container motion.

---

### 4. Frame Math Errors — Wrong TOTAL

**What it looks like:** The video cuts off before the last scene ends, or there is a blank
black tail after the CTA. Or the timeline preview in Remotion Studio shows 1010 frames when
the video should be 935.

**Why it happens:** `TOTAL` was set to the sum of scene durations without subtracting the
transition overlaps. For N scenes with shared transition duration T:
```
TOTAL = sum(durations) - (N - 1) × T
```
Every transition overlaps the adjacent scenes by T frames. Forgetting this makes TOTAL
larger than the actual composition length.

**How to catch it:** The frame calculator prints the explicit arithmetic:
```
Verify: 150+180+150+210+200+120 - (5×15) = 1010 - 75 = 935
```
Write this in the frame timing document. If `SCENE_TIMING.TOTAL` does not match, fix it
before Root.tsx picks up the wrong value.

**How to fix it:** Set `TOTAL = sum(durations) - (N-1) × transition_duration` in constants.
If transition durations vary per-transition, subtract each individually.

---

### 5. Phase Sequencing — Phase 2 Fires Mid-Sentence

**What it looks like:** In a scene with a typewriter transcript followed by UI elements
(pills, cards, checkmarks), the UI elements begin appearing while the transcript is still
being typed. The typewriter and the UI fight for attention.

**Why it happens:** `PHASE2_START` was hardcoded to a literal number instead of being
derived from the actual transcript end frame. The transcript length varies (the designer
wrote 60 characters but the VO was later updated to 74 characters), and the hardcoded
constant no longer matches.

**How to fix it:** Always derive phase start frames from the actual animation end of the
previous phase:
```ts
const TRANSCRIPT_END = TRANSCRIPT_START + Math.ceil(TRANSCRIPT.length / CHARS_PER_FRAME);
const PHASE2_START   = TRANSCRIPT_END + HOLD_FRAMES; // HOLD_FRAMES = 12
```
Never write `const PHASE2_START = 113;`. It will break the moment the content changes.

---

### 6. Abrupt Cuts — State Changes Without Transitions

**What it looks like:** An element disappears or changes color in a single frame. The viewer
flinches. It reads as a bug, not an effect.

**Why it happens:** A conditional like `{frame >= PHASE2_START && <NewElement />}` renders
the element at full opacity on the exact frame it becomes true. No entrance animation was
planned.

**Examples of abrupt cuts that must always be avoided:**
- REC indicator: `{frame < PHASE2_START && <RecDot />}` — disappears in one frame. Fix:
  fade out over 10 frames using `interpolate`.
- Scene-to-scene: hard cut between scenes instead of using TransitionSeries. Fix: every
  scene transition must be a TransitionSeries transition, even if it's just `fade()`.
- Void vacuum: instant jump from dark scene to pure white. Fix: the white background must
  fade in over ≥6 frames. A single-frame white flash reads as a render artifact.
- State color snap: chaos lines are one color and snap to red in a single frame. This
  specific case is intentional (the freeze is the effect) — but document it explicitly in
  the beat table so no future developer "fixes" it.

---

### 7. Sizing and Scale — Elements Too Small at 1080×1920

**What it looks like:** Text is technically readable in Remotion Studio but becomes illegible
on a phone screen. Cards look like UI chrome, not bold statements. The video feels like a
shrunken desktop website, not a native vertical video.

**Why it happens:** Sizes were chosen while looking at a scaled-down preview, or sizes were
copied from a 1080×1080 or 16:9 layout and never recalibrated for 9:16.

**Minimum size rules at 1080×1920 (30fps):**

| Element type | Minimum size | Recommended |
|---|---|---|
| Hero / central concept text | 80px | 100–140px |
| Scene heading / key label | 40px | 48–60px |
| Body text / explanatory | 28px | 32–36px |
| Terminal / code / mono | 22px | 26–30px |
| UI label / caption | 18px | 20–24px |
| Do-not-go-below | 16px | — |

**Padding rules:**
- Side padding on a 1080px wide frame: minimum 80px each side. Effective content width: 920px.
- Top/bottom safe zones: 80px each. Content should not start in the top 80px or end in the
  bottom 80px.
- Cards / pills: minimum 16px internal padding. Border must be visible (≥ 1.5px stroke).

**Common mistakes:**
- `maxWidth: 800` on a centered container — fine, but add `width: '100%'` so it fills the
  available space on narrower containers.
- `fontSize: 18` for terminal lines — readable on desktop, invisible on mobile. Use 26+.
- Card borders: `border: '1px solid ...'` — too thin at 1080px. Use 1.5px minimum.

**Before writing layout code:** Write explicit pixel widths and font sizes into the frame
timing document's "Notes / Risks" column for every element that carries critical information.
If you cannot read it at arms-length in preview, the viewer cannot read it on a phone.

---

### 8. Color Meaning Drift

**What it looks like:** The accent color appears on elements that are neutral or negative,
which confuses the viewer's trained color associations. Or the error/state color is used for
decoration without intent.

**Examples:**
- Green accent on a cursor in a scene showing a problem. The cursor reads as "correct" when
  the scene is about wrongness.
- Red state color on a decorative border because "it looks good." Now the viewer subconsciously
  reads the border as a warning.
- Green checkmarks on every list item including items that are still "pending." Uses up the
  semantic weight of green before the real success moment.

**Rule:** Green = solved / correct / progress. Red = broken / wrong / missing. These meanings
are established in frame 0 and must never drift. If you need a third color for "neutral" or
"pending" state, use the text-dim muted color (`#4A4A5A` in the dark system). Never use the
accent as a decorative color.

---

### 9. Local vs Absolute Frame Confusion

**What it looks like:** An animation trigger like `frame > 500` inside a scene component
never fires because `useCurrentFrame()` returns local frames (0 to scene_duration-1), and
this scene's duration is only 200 frames. The condition is unreachable.

**Why it happens:** The developer reasoned about the animation in absolute frame terms but
wrote the condition in local frame terms (or vice versa).

**Rule:** Inside any scene component, `useCurrentFrame()` returns local frames starting from
0. Absolute frame numbers from the frame timing document must be converted to local before
use:
```ts
// In the component — always local
const GLITCH_START = 73; // local frame 73 = absolute 73 (Scene 1 starts at absolute 0)

// For Scene 2 (absolute start = 135):
const WIPE_START = 10; // local — absolute equivalent is 135 + 10 = 145
// Never write: const WIPE_START = 145; // WRONG inside Scene 2 component
```

Label every timing constant in the component with a comment showing both the local value
and its absolute equivalent for the first time a reader needs to cross-reference:
```ts
const TYPE_START = 99; // local 99 = absolute 99 (Scene 1 starts at 0)
```

---

### 10. Transition Entry Content Flash

**What it looks like:** During a slide or wipe transition, the entering scene momentarily
shows content (text, glows, UI elements) that should not be visible until after the
transition completes. The viewer sees a jumbled mix of Scene N exiting and Scene N+1 content
arriving simultaneously.

**Why it happens:** Scene N+1 has authored animations that start at local frame 0, which is
the same frame as the transition start. So for a 15f slide transition, Scene N+1 is running
local frames 0–14 while the slide is still in progress. If Scene N+1's opening animation
(e.g., a heading typewriter) starts at local 0, it will be visible and actively animating
while the container is still mid-slide.

**How to fix it:** Design Scene N+1's first authored animation to start at or after
`TRANSITION_DURATION` (e.g., local frame 15 for a 15f transition). Use this buffer window
to show only the background/environment entering, letting the transition settle cleanly before
content appears. The `WIPE_DURATION` pattern in Scene 2 (`WIPE_DURATION = 10`) is exactly
this: a deliberate buffer so lines don't start drawing during the incoming slide.

---

## Bundled Files — Read These

### scripts/

- `scripts/srt_to_script.py` — Converts an SRT subtitle file into a structured
  `script-[name].md`. Usage: `python scripts/srt_to_script.py <input.srt> "<Title>" [output.md]`

- `scripts/frame_calculator.py` — **Read the docstring at the top of this file.** Computes
  absolute frame ranges for all scenes and transitions, detects dead air, and analyses spring
  damping ratios. Run this in Step 5 before writing any frame timing document. Usage:
  `python scripts/frame_calculator.py --fps 30 --durations ... --transition ... --names ... --last-anim ... --springs ...`

### examples/ — The quality benchmark. Read these before designing anything.

These are real shot-by-shot breakdowns of high-performing motion graphic videos, paired with
their exact voiceover scripts. Every design decision you make should be measured against the
standard they demonstrate.

- `examples/video-example-1.md` + `examples/video-script-1.md` — Claude Code tips video (~54s).
  Study: dark hacker aesthetic, neon mint accent, glitch hook, staccato checkmark pops,
  context window slider metaphor, liquid alpha matte wipe, visual vacuum CTA.
- `examples/video-example-2.md` + `examples/video-script-2.md` — ZIP compression explainer (~56s).
  Study: warm beige palette, safety orange accent, retro computing metaphor, Pac-Man
  gamification, flowchart line-drawing, lossless reversal proof, AI pivot climax.
- `examples/video-example-3.md` + `examples/video-script-3.md` — Brand Gravity marketing video (~80s).
  Study: mint-green monochromatic world, funnel-to-tombstone morph hook, spacetime grid
  metaphor, authority anchor cut, corporate facade shatter, orbital customer resolution.

**When to read:** Read ALL six files at the start of Step 2 (Script Analysis). Internalize
the level of editorial depth in the "Editorial Thinking/Intent" sections — that depth is what
you must match in your own design doc. The scripts show you exactly how timestamps map to
voiceover density.

### references/ — Design rules and format specs.

- `references/design-doc-format.md` — Exact format for `script-[name].md` and
  `video-design-[name].md`, with a fully worked example and anti-patterns to avoid.
  Read during Step 4.

- `references/frame-timing-format.md` — **The most important reference for Step 5.**
  Exact format for `frame-timing-[name].md`, with a fully worked example covering all 6
  scenes and 5 transitions of the VibeCodingPRD video. Every future video's frame timing
  document must meet the detail level demonstrated here. Read during Step 5.

- `references/design-system.md` — Color architecture, typography registers, easing as
  emotional language, scene density calibration, background depth rules. Read during Step 3.

- `references/editorial-patterns.md` — Tension curve architecture, pattern interrupt
  techniques, cognitive relief design, visual metaphor construction formula, hook types,
  CTA vacuum mechanics, narrative arc patterns. Read during Step 3.

- `references/motion-graphic-prompts.md` — Library of 75 motion graphic concepts across
  5 categories. Read during Step 3 when brainstorming animation vocabulary for a segment.
