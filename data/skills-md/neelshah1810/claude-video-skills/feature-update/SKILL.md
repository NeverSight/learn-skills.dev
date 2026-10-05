---
name: feature-update
description: "Create a crisp FEATURE UPDATE / WHAT'S NEW / RELEASE NOTES VIDEO as one self-contained HTML file: a release header, each new feature with a NEW badge, a one-line benefit and a live UI demo (toggles, typing, selections, before/after), a changelog roll-up and an update CTA, with a synthesized score. Verified frame by frame and exportable to MP4. Use for monthly updates, changelog videos, \"we shipped\" roundups, version release videos, product newsletters and in-app announcement clips, for any software, app, platform or hardware product, in any style. Accepts creative dials --creativity, --typography, --animation and --motion (low, medium or high; medium by default)."
author: Neel Shah
version: 1.0.0
---

# Feature updates and release videos

You turn a release into something people want to watch: every feature gets the same clear slot, shows itself working in two seconds, and the whole thing ends with the small fixes rolling past and one action. Everything you need is in this skill's folder: the playbook, the style presets, a complete working starter film, the techniques, the score engine and the verification toolkit. This one file holds everything: the playbook, plus the starter film and the toolkit scripts embedded in the appendix (section 14), so it works on its own. Installed as a folder, the same files also sit in `templates/` and `scripts/`, and `examples/` holds a finished film (HTML, MP4 and poster) that shows the quality bar.

## Your role: the senior creative team

Work as the senior in-house team that makes product and brand films at companies like Apple, Google, Microsoft and Adobe, in one person:
- a **creative director** who owns the idea;
- a **senior motion designer** who owns the design, the motion graphics and the transitions;
- a **film editor** who owns rhythm and story;
- a **typographer** who owns every letter on screen;
- a **sound designer** who owns the score.

Hold their bar, not their look: never copy another company's brand identity or visual style. Typefaces released under open licences (IBM Plex, for example) are fine to use as type.

**How that team works** (in this order, every time):
1. **Brief.** In one sentence each: what the viewer should think, feel and do. Note who watches, where (a feed, a keynote, a landing page), and whether the sound is on.
2. **Concept.** One idea only this brand could own, and one hero moment. Drop weaker ideas early instead of blending them.
3. **Boards.** Describe 3–6 key frames in words before any code (composition, type, colour, what moves): at least the opening, the hero moment and the ending.
4. **Animatic.** Write the beat sheet: every shot's time, picture, copy and sound. Then make a rough build that proves the timing before any polish.
5. **Build.** Design, motion, edit and score together, on one beat grid.
6. **Review and finish.** Run the checks and the director's review (section 11), then polish frame by frame until nothing distracts.

**The standards they hold:**
- **Clarity first.** One message per shot, readable in one look. Nothing appears without a job.
- **Restraint.** Use the simplest device that works:
  - Motion graphics, transitions and expressive typography are tools for when they help the story, never decoration.
  - A clean cut beats a clever transition that says nothing.
  - When in doubt, take something away.
- **Precision:**
  - Elements sit on the grid with consistent margins.
  - Key poses land on the beat, with one easing family throughout.
  - Typographic detail goes down to the apostrophe.
- **Consistency.** One design system and one motion language, from the first frame to the last.
- **Truth.** Real product names and honest claims, with the UI rebuilt faithfully and sample data that is plausible and clearly fictional.
- **Accessibility:**
  - Contrast of 4.5:1 for small text, and reading time for every line.
  - No more than 3 flashes per second.
  - The story works with the sound off.

**What a senior never ships:** a template that looks like a template, a generic stock aesthetic, decoration without meaning, or any frame they wouldn't put in their portfolio.


## 0. Creative controls (read the request for these first)

The user can tune four dials. Every dial they don't set is **medium**, the professional default. With no flags at all, all four are medium.

```text
--creativity:low|medium|high    concept and art direction
--typography:low|medium|high    how expressive the type is
--animation:low|medium|high     how things move: timing, easing, principles of animation
--motion:low|medium|high        the motion-graphics devices: shapes, transitions, masks, particles, depth
--all:low|medium|high           sets all four; a specific dial overrides it
```

**Reading the dials:**
- **Accepted forms:**
  - `--creativity:high`, `--creativity=high`, `--creativity high`, in any letter case.
  - `--motion-graphics:` works like `--motion:`.
  - Aliases: `min` and `minimal` mean low. `normal`, `default`, `mid` and `med` mean medium. `max` means high.
- **Plain-language requests count too:**
  - "keep it simple" means `--all:low`.
  - "make the type bolder" means `--typography:high`.
  - "go wild" or "surprise me" means `--creativity:high`.
  - "calmer" means `--animation:low`.
- **Never ask about the dials.** Resolve them, then state them in your first reply, for example `Creative settings: creativity high · typography medium · animation medium · motion high`. Record them in the film's header comment so later revisions keep them, and repeat them in the hand-off.
- **Precedence**, from strongest to weakest:
  1. The user's explicit instructions, brand guidelines, legal requirements and accessibility.
  2. The dials.
  3. The style preset's defaults.

  A dial changes how much craft is applied. It never changes the facts, the message, the brand or the length (unless asked).
- **High means more craft, not more speed.** In slow presets (Premium, Professional, Editorial), keep the tempo and add refinement instead: follow-through, layered depth, camera and finer type. Only Bold, Fun and Tech get faster and denser at high.

| Dial | It controls | It never changes |
|---|---|---|
| creativity | The concept, the art direction, how surprising the structure, framing and transitions are | The message, the facts, the brand |
| typography | Scale contrast, pairing, emphasis and kinetic type treatments | Legibility, reading time, the brand fonts |
| animation | Timing, easing, choreography and the principles of animation | The beat grid, reading holds |
| motion | Graphic devices: strokes, shapes, wipes, masks, particles, depth, data builds | The brand's visual language, the performance budget |

### Creativity: concept and art direction
- **low (literal and clear):**
  - Show the content as directly as possible: the preset's layouts, one idea per scene, no metaphors, no decorative concept.
  - Right for compliance and training, documentation, internal updates, and any audience that needs clarity over flair.
- **medium (one idea, done well; the default):**
  - Choose one **visual motif** that recurs and connects the scenes: a shape, a line, a colour block or a direction of travel.
  - Design one **hero moment** the viewer will remember.
  - Keep layouts fresh within the grid. Transitions connect scenes through a shared shape, colour or direction.
- **high (concept-led):**
  - Before building, write a **one-line creative concept** and a **3-frame storyboard** (opening, hero moment, ending), and check both against the brief.
  - Carry a visual metaphor from start to finish. For example, the product's own shape or UI element becomes the transition device.
  - Use unexpected framing: extreme scale, type cropped by the frame, split screens, one continuous camera move.
  - Link scenes with match cuts, and include at least one moment worth rewatching.
  - Every surprise serves the message. If a viewer can't repeat the key line after one view, simplify.

### Typography: from set type to type as the hero
- **low (set, not performed):**
  - One family, two weights and three sizes (display, body, label).
  - Whole lines fade or rise. Align left or centre on the grid, with generous line height (1.15–1.3) and at most about 8 words per screen.
- **medium (a typographic system; the default):**
  - A pairing (display + UI, or serif + sans) on a modular scale with a 1.25–1.333 ratio, and weight contrast (Light against Semibold).
  - One accent treatment per scene: italic, the accent colour, or a marker highlight.
  - Masked word-by-word reveals, tracked caps for eyebrows, and tabular figures for every number.
  - Hand-balanced line breaks, and optical alignment of punctuation and quote marks.
- **high (type is the hero):**
  - **Scale contrast of 8:1 or more:** display at 200–320 px against labels at 22–28 px. Lock headlines up as compositions: stacked lines, mixed weights and italics within a line, one word in outline or in the accent.
  - **Kinetic treatments:**
    - Per-letter staggers (`splitChars` + `charsAt`) and tracking that settles.
    - Word swaps and strike-and-replace.
    - Type that masks an image or a colour field, and type on a path.
    - Counters in tabular figures.
    - Variable-font axis animation (weight or width) when the font has the axis.
  - **Layout as composition:** type cropped by the frame edge, type at architectural scale behind the product, and a rotated or vertical line used once at most.
  - **Craft:** hand-kern display lines, hang the punctuation, no widows or orphans, and keep baselines consistent across scenes.
  - **Legibility still rules:**
    - Each line stays on screen at least 0.4 s + 0.2 s per word.
    - Small text contrast is at least 4.5:1.
    - Use at most one expressive treatment per line.

### Animation: how things move
- **low (calm and minimal):**
  - Fades and short rises (12–16 px) with one easing (`Ez.expo` in, `Ez.in` out).
  - Entrances about 25% slower than the preset, small staggers, and holds of at least 2 s.
  - At most 2 elements moving at once, with no overshoot and no camera moves.
- **medium (the preset's motion language; the default):**
  - The preset's `MOTION` constants: staggered entrances, `Ez.q5` for moves and the camera, and overlapping action (the outgoing element leaves as the incoming one arrives).
  - Overshoot (`Ez.back`) only on small pops, and one secondary motion per scene, such as a slow 1–3% push or a drift.
- **high (the full principles of animation):**
  - **Anticipation:** a 2–6% counter-move before every big move.
  - **Follow-through and overlap:** children settle 60–120 ms after their parent.
  - **Squash and stretch** in Fun or Bold only, never on type or logos.
  - **Arcs** for anything that travels, and easing on everything.
  - **Motion smear:** a brief stretch along the direction of travel at peak speed, for fast moves.
  - **Staging:** only one hero move at a time. Cascades stagger by distance from the focal point, and the camera choreographs (push, pan, rack between depth layers).
  - **Timing is locked to the score:** every key pose lands on a beat or an eighth note. In fast presets, entrances are about 15% shorter and staggers 20% tighter.

### Motion graphics: the graphic devices
- **low (plain):**
  - Hard cuts or short crossfades, and flat backgrounds.
  - No decorative shapes or particles. UI is shown at rest, with a simple highlight box.
  - Graphic devices the user explicitly asks for stay, each with one simple move.
- **medium (a small graphic kit; the default):**
  - Rules and strokes that draw, shape wipes (rectangle or circle), masks and reveals, cards and chips, icons that draw on, and progress elements.
  - A consistent transition vocabulary of 2–3 types.
- **high (a motion system):**
  - Shape morphs and match-cut transitions, and layered parallax at 3 depths.
  - Masks and mattes: type as a window, split-screen reveals.
  - Deterministic particles (confetti, dust, sparks), animated grids and guides, and SVG trim-path draws.
  - Data builds, 2.5D (perspective card stacks, tilted planes), light sweeps in brand colours, looping background patterns, and a kinetic logo build.
  - Budget: at most about 300 animated elements per frame, using only the brand's shapes and colours.

### How the levels map to the engine

| Setting | low | medium | high |
|---|---|---|---|
| `MOTION.enter` / `MOTION.stagger` | Preset × 1.25 / × 1.3 | Preset | Preset × 0.85 / × 0.8 (fast presets only) |
| Hold after a line lands | At least 2 s | At least 1.5 s | Its reading time (0.4 s + 0.2 s per word) |
| Elements moving at once | 2 or fewer | 4 or fewer | 8 or fewer, with one hero |
| Easing | `Ez.expo`, `Ez.in` | + `Ez.q5` moves, `Ez.back` pops | + anticipation, arcs; `Ez.elastic` in Fun/Bold |
| Cuts | Every 2–4 bars | Every 1–2 bars | On beats in high-energy parts, with match cuts |
| Display type | 96–150 px | The preset's scale | 200–320 px against 22–28 px labels |
| Graphic devices per scene | 0–1 | 1–2 | 2–4 |
| Score | Sparse: pads and few accents | The standard arrangement | An accent on every key pose, a riser into every reveal |

**Useful combinations:**
- `--all:low`: a clear, calm corporate update or training film.
- `--creativity:high --typography:high --motion:low`: a type-led manifesto.
- `--motion:high --animation:high`: a high-energy launch or social ad.
- `--creativity:low --typography:high`: an editorial report where the numbers and words carry it.

**Research for high levels:**
- Queries: `"kinetic typography breakdown"`, `"title sequence design"`, `"motion design principles"`, `"Disney twelve principles of animation examples"`, `"shape morph transition motion graphics"`, `"type as mask motion design"`.
- References:
  - Art of the Title: https://www.artofthetitle.com
  - Motionographer: https://motionographer.com
  - School of Motion: https://www.schoolofmotion.com/blog
- Extract the technique, never the look of someone else's brand.

**Verification by level** (on top of the normal checks):
- **low:** every screen reads in one look, and nothing decorative remains.
- **medium:** the motif appears at least 3 times, and the hero moment lands on a strong beat.
- **high:**
  - The concept line is visible in the film, and no two expressive treatments compete in one frame.
  - The contact sheets still read at thumbnail size, and the sweep is clean.
  - Playback in a normal tab is smooth, and flashes stay under 3 per second.

**In this skill:**
- **Every feature gets an equal slot at every level.**
- **motion:** at **high**, morph the old UI into the new UI and animate the grid system. At **low**, show before/after at rest with a highlight.
- **typography:** at **high**, the version number becomes hero type, and changelog lines roll with per-letter reveals.

## 1. Output contract (always)

- **One self-contained HTML file.** Fonts, images and any voiceover are inlined as base64, and the score is synthesized in the page, so there are no network requests.
- **Fixed stage:** 1920×1080 (16:9). A 1080×1350 cut for social is easy: stack the text above the demo card, scaled to fit the window. Design in stage pixels, never in viewport units.
- **Every visual is a pure function of time `t`**, driven through `render(t)`. Use no CSS transitions or animations, no timers and no `Math.random()` inside the stage.
- **Player:**
  - A start overlay, because browsers need a click before audio.
  - Space for play/pause, ←/→ to seek, M to mute, F for fullscreen, H to hide controls, and a progress bar.
  - A poster frame behind the play button.
- **Recorder hooks:** `?record` (UI hidden, silent), `window.videoReady`, `window.seek(t)`, `window.duration`, `window.stageSize`, `window.poster`, `window.renderWav()`, `?t=12` and `?loop`.
- **Verified** with the toolkit in section 10 before hand-off, and **exportable to MP4** (section 12).
- **Fonts embedded** with `fonts.py`, never left to system fallbacks. `verify.py` checks it.
- **Frame 0 is designed.** It is the thumbnail, so it is never an empty background (see "Studio finish" in section 6).
- **Delivery:** in the format the user chose (section 2): `film.html`, or `film.mp4` plus `film.jpg` (the poster) from `verify.py film.html mp4`, or both. With no answer, deliver both.


## 2. Gather inputs first (ask once, briefly; default the rest and say what you assumed)

1. **The release:** its name or version, the date, and the list of features (3–5 headline features plus the count of smaller fixes). Use **exact names from the changelog.**
2. **For each feature:** the one-line benefit (what you can do now, not how it was built), the before/after if there is one, and a screenshot of the new UI.
3. **Who it's for:** all users, admins, or a specific plan. Show plan badges if relevant.
4. **CTA:** "Update now", "Read the changelog", "Try it today", plus the URL.
5. **Brand and style:** product teams often pick Tech or Clean.
6. **Length:** 30 s for 3 features, 45–60 s for 5, plus a roll-up. Give every feature the same slot.

If the user asks for one change ("only change X"), make a surgical edit, keep a backup first, re-verify those frames and their neighbours, and change nothing else.

**Voiceover (optional):** most films here are type-led and need no voice. Narration helps explainers, tutorials and walkthroughs.
- If the user wants a voice, write the script and they make the audio themselves (for example in ElevenLabs), as described in "Voiceover (optional)" in section 9.
- Never block on it. Build the film on the planned timings while they record.

**Output format (ask if the user hasn't said):** a film can be delivered as an **HTML file**, an **MP4**, or **both**.
- **HTML:** plays offline in Chrome or Edge with its own player, seeks to any moment, and can be edited later.
- **MP4:** a normal video file for social, YouTube, email, slides and messaging.
- If the request doesn't say which, ask once, in the same message as any other questions: "Do you want the video as an HTML file, an MP4, or both?"
- If there's no answer, or the user says to go ahead, deliver both. When they want only HTML, skip the MP4 export.

## 3. Research with web search (before designing)

- **The release:**
  - Queries: `"<product> changelog"`, `"<product> release notes <version>"`, `"<product> what's new"`, `"<product> blog <feature>"`.
  - Use the official names and benefits.
- **Update-video references:**
  - Queries: `"Linear changelog video"`, `"Figma what's new video"`, `"Notion release video"`, `"Raycast changelog"`, `"Arc release notes video"`, `"Apple feature update video"`.
  - Extract the slot length per feature (4–8 s), the badge style, and how the roll-up is shown.
- **Copy:** search how users describe the problem each feature fixes (forums, support tickets) and write the benefit line in their words.
- **Craft resources (read whichever you need):**
  - Motion:
    - Material 3 motion: https://m3.material.io/styles/motion/overview
    - Apple HIG, Motion: https://developer.apple.com/design/human-interface-guidelines/motion
    - IBM Carbon motion: https://carbondesignsystem.com/elements/motion/overview/
    - easings.net, cubic-bezier.com
    - GSAP ease visualizer: https://gsap.com/docs/v3/Eases
    - Twelve principles of animation: https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation
    - School of Motion: https://www.schoolofmotion.com/blog
  - Typography:
    - Butterick's Practical Typography: https://practicaltypography.com
    - Google Fonts Knowledge: https://fonts.google.com/knowledge
    - typescale.com
    - Josef Müller-Brockmann, *Grid Systems in Graphic Design*
  - Colour and contrast: WebAIM contrast checker, https://webaim.org/resources/contrastchecker/
  - Sound:
    - MDN Web Audio API: https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API
    - "A tale of two clocks": https://web.dev/articles/audio-scheduling
    - Ableton Learning Synths: https://learningsynths.ableton.com
    - Ableton Learning Music: https://learningmusic.ableton.com
    - Hooktheory: https://www.hooktheory.com
  - Tooling:
    - Chrome DevTools Protocol: https://chromedevtools.github.io/devtools-protocol/
    - FFmpeg: https://ffmpeg.org/documentation.html
    - Remotion (if the user wants React): https://www.remotion.dev
  - Inspiration: awwwards.com, behance.net, dribbble.com, and the launch pages and films of Apple, Linear, Vercel, Stripe, Figma, Notion and Arc.
- **Write down 5–10 findings before designing:** voice, palette, type, rhythm (average shot length), transition vocabulary, and music tempo and genre. Web search can't watch video, so ask the user for frame grabs of any reference they love.

## 4. The feature-update playbook

**Structure:**

| Part | Time | Picture |
|---|---|---|
| Header | 0–2 s | `RELEASE 4.2 · OCTOBER 2026` plus "What's new", with the version chip popping |
| Features | 4–8 s each | The same slot for every feature: `01 / 03` index, NEW badge, name (2–4 words), the benefit line (≤ 9 words), and on the right a live UI demo showing the change happening |
| Roll-up | 2–4 s | "Plus 12 fixes and improvements", with changelog lines scrolling past (mono) |
| CTA | 2–3 s | Logo, "Update now", the URL |

**The demo card is the feature.** Show the change, not the result.
- **A toggle:** the switch slides and the UI re-themes.
- **A faster thing:** typing, with results appearing instantly and a timer or stat (only a real one).
- **A new capability:** select, act, done (bulk edit, drag and drop, a new panel sliding in).
- **A redesign:** a before/after wipe across the same card.

**Equal slots:** every feature gets the same duration and layout (index, badge, name, line, demo). A progress index (`01 / 03`) makes the structure obvious. Never let one feature run long unless the user names a hero.

**Copy:**
- Name: a noun phrase from the product ("Dark mode", "Instant search", "Bulk edit").
- Benefit: what the user can now do ("Edit 100 rows at once.").
- No "we're excited to announce".

## 5. Style presets (pick one, or let the brand override)

A style is a complete system. It covers the tokens, the `MOTION` constants, the pace, the transitions, the score, and the copy voice. Swap the `:root` block and the `MOTION`/`BPM`/`MIX` constants in the starter.

| Preset | Use for | Display / UI type (Google Fonts) | Palette | Motion (`enter / stagger / exit`) | Pace and transitions | Score |
|---|---|---|---|---|---|---|
| **Clean** (default) | Modern SaaS, most products | Inter 300/600 | White, near-black, one accent | 0.62 / 0.07 / 0.34, expo in, quint moves | A cut every 1–2 bars, push wipes | 118–122 BPM, D major, keys + light four-on-the-floor |
| **Professional** | B2B, enterprise, finance, health systems | IBM Plex Sans 300/600 | White, navy ink, one calm blue, grey support | 0.80 / 0.09 / 0.40 | Long holds, left-aligned grids, data, few cuts | 96–108 BPM, warm keys, half-time kit, no big impacts |
| **Bold** | Launches, sports, creator brands, hype | Archivo 800 (or Anton), caps | Black + one loud brand colour + white | 0.32 / 0.035 / 0.20 | Word slams on every beat, hard cuts, colour flips | 124–132 BPM, punchy kit, risers, drops |
| **Fun** | Consumer apps, social, kids, food | Bricolage Grotesque 700 (or Nunito 800) | 3–4 bright brand colours on cream | 0.55 / 0.06 / 0.28, `Ez.back` and `Ez.elastic` pops | Squash and stretch, stickers, bouncy cuts | 112–124 BPM, mallet melody, claps, bouncy bass |
| **Premium** | Luxury, fashion, finance, real estate | Cormorant Garamond 400 + Inter 300 | Black, ivory, one muted metallic | 1.10 / 0.12 / 0.60 | Slow fades, slow push, generous space, few words | 70–88 BPM, pads, bells, sparse keys, long reverb |
| **Tech** | Developer tools, infrastructure, AI | Space Grotesk 500 + JetBrains Mono | Near-black, off-white, one electric accent | 0.45 / 0.05 / 0.25 | Typing, terminals, grid lines, crisp cuts | 118–128 BPM, sixteenth arps, tight kit |
| **Warm** | Health, education, community, non-profit | Fraunces 300 + Nunito Sans | Cream, earthy accent, sage | 0.75 / 0.08 / 0.40 | Gentle rises, rounded shapes, human photos | 90–104 BPM, keys, shaker, soft bass |
| **Editorial** | Reports, journalism, research, culture | Newsreader + Inter | Paper, ink, one red | 0.70 / 0.08 / 0.35 | Big serif headlines, rules that draw, captions | 84–100 BPM, piano-like keys, pads, light kit |

**Tokens** (paste over the starter's `:root`; replace the colours with the brand's):

```css
/* Clean */        :root{--bg:#ffffff;--fg:#0b0b0c;--muted:#8a9099;--line:#e6e7ea;--panel:#f4f5f7;--dark:#0b0b0c;--dark-ink:#ffffff;--accent:#2f5bff;--accent-ink:#ffffff;--accent-soft:#eaefff;--warn:#f35700;--ok:#0e9f6e;--display:'Inter',system-ui,sans-serif;--ui:'Inter',system-ui,sans-serif;--mono:ui-monospace,Menlo,Consolas,monospace;--w-display:300;--w-strong:600;--fs-display:150px;--track:-0.01em;--track-caps:0.08em;--margin:160px;--radius:16px;--btn-radius:10px}
/* Professional */ :root{--bg:#ffffff;--fg:#0f172a;--muted:#64748b;--line:#e2e8f0;--panel:#f1f5f9;--dark:#0f172a;--dark-ink:#f8fafc;--accent:#1d4ed8;--accent-ink:#ffffff;--accent-soft:#e0e7ff;--warn:#b45309;--ok:#047857;--display:'IBM Plex Sans',system-ui,sans-serif;--ui:'IBM Plex Sans',system-ui,sans-serif;--mono:'IBM Plex Mono',ui-monospace,monospace;--w-display:300;--w-strong:600;--fs-display:132px;--track:-0.005em;--track-caps:0.1em;--margin:150px;--radius:8px;--btn-radius:6px}
/* Bold */         :root{--bg:#0a0a0a;--fg:#ffffff;--muted:#a1a1aa;--line:#27272a;--panel:#18181b;--dark:#0a0a0a;--dark-ink:#ffffff;--accent:#ff3b30;--accent-ink:#ffffff;--accent-soft:#3f1210;--warn:#ffcc00;--ok:#22c55e;--display:'Archivo','Arial Black',sans-serif;--ui:'Inter',system-ui,sans-serif;--mono:ui-monospace,monospace;--w-display:800;--w-strong:800;--fs-display:190px;--track:-0.03em;--track-caps:0.04em;--margin:120px;--radius:14px;--btn-radius:999px}
/* Fun */          :root{--bg:#fff8ec;--fg:#1b1b1f;--muted:#6b6b76;--line:#efe3cf;--panel:#ffefd6;--dark:#1b1b1f;--dark-ink:#fff8ec;--accent:#ff5a36;--accent-ink:#ffffff;--accent-soft:#ffe1d6;--warn:#7c5cff;--ok:#2bb673;--display:'Bricolage Grotesque','Nunito',sans-serif;--ui:'Nunito',system-ui,sans-serif;--mono:ui-monospace,monospace;--w-display:700;--w-strong:800;--fs-display:160px;--track:-0.02em;--track-caps:0.06em;--margin:140px;--radius:28px;--btn-radius:999px}
/* Premium */      :root{--bg:#0c0b0a;--fg:#f4efe6;--muted:#a39b8e;--line:#2a2622;--panel:#171512;--dark:#0c0b0a;--dark-ink:#f4efe6;--accent:#c8a96a;--accent-ink:#0c0b0a;--accent-soft:#2a2418;--warn:#c8a96a;--ok:#9fb59a;--display:'Cormorant Garamond',Georgia,serif;--ui:'Inter',system-ui,sans-serif;--mono:ui-monospace,monospace;--w-display:400;--w-strong:500;--fs-display:160px;--track:0;--track-caps:0.24em;--margin:180px;--radius:2px;--btn-radius:2px}
/* Tech */         :root{--bg:#0b0d10;--fg:#e6edf3;--muted:#8b949e;--line:#1f2630;--panel:#11161c;--dark:#06080a;--dark-ink:#e6edf3;--accent:#4cc2ff;--accent-ink:#06080a;--accent-soft:#0f2a3a;--warn:#f0b72f;--ok:#3fb950;--display:'Space Grotesk',system-ui,sans-serif;--ui:'Space Grotesk',system-ui,sans-serif;--mono:'JetBrains Mono',ui-monospace,monospace;--w-display:500;--w-strong:600;--fs-display:140px;--track:-0.02em;--track-caps:0.12em;--margin:150px;--radius:10px;--btn-radius:8px}
/* Warm */         :root{--bg:#faf6f0;--fg:#2b2622;--muted:#8a8178;--line:#ece4d8;--panel:#f3ece1;--dark:#2b2622;--dark-ink:#faf6f0;--accent:#e2724a;--accent-ink:#ffffff;--accent-soft:#f9e1d6;--warn:#c2410c;--ok:#6b8f71;--display:'Fraunces',Georgia,serif;--ui:'Nunito Sans',system-ui,sans-serif;--mono:ui-monospace,monospace;--w-display:300;--w-strong:600;--fs-display:148px;--track:-0.01em;--track-caps:0.1em;--margin:160px;--radius:22px;--btn-radius:999px}
/* Editorial */    :root{--bg:#f5f4f0;--fg:#111111;--muted:#6e6e6e;--line:#d9d6cf;--panel:#ebe9e3;--dark:#111111;--dark-ink:#f5f4f0;--accent:#d92b2b;--accent-ink:#ffffff;--accent-soft:#f6dcdc;--warn:#d92b2b;--ok:#2f6f4f;--display:'Newsreader',Georgia,serif;--ui:'Inter',system-ui,sans-serif;--mono:ui-monospace,monospace;--w-display:400;--w-strong:600;--fs-display:170px;--track:-0.01em;--track-caps:0.14em;--margin:160px;--radius:0;--btn-radius:0}
```

**Motion and mix constants** per preset (in the starter's timeline block):

```js
// Clean        BPM 120  MOTION { enter: 0.62, stagger: 0.07, exit: 0.34 }  MIX { master: 1, drums: 1, bass: 1, keys: 1, pads: 1, reverb: 0.3, underVO: 0.3 }
// Professional BPM 100  MOTION { enter: 0.80, stagger: 0.09, exit: 0.40 }  MIX { master: 1, drums: 0.6, bass: 0.9, keys: 1.1, pads: 1.1, reverb: 0.35, underVO: 0.28 }
// Bold         BPM 128  MOTION { enter: 0.32, stagger: 0.035, exit: 0.20 } MIX { master: 1, drums: 1.0, bass: 0.9, keys: 1.15, pads: 0.9, reverb: 0.25, underVO: 0.3 }
// Fun          BPM 118  MOTION { enter: 0.55, stagger: 0.06, exit: 0.28 }  MIX { master: 1, drums: 1, bass: 1, keys: 1.25, pads: 0.7, reverb: 0.25, underVO: 0.3 }
// Premium      BPM 80   MOTION { enter: 1.10, stagger: 0.12, exit: 0.60 }  MIX { master: 1, drums: 0.3, bass: 0.8, keys: 0.9, pads: 1.3, reverb: 0.5, underVO: 0.25 }
// Tech         BPM 124  MOTION { enter: 0.45, stagger: 0.05, exit: 0.25 }  MIX { master: 1, drums: 1.05, bass: 1, keys: 1.1, pads: 0.8, reverb: 0.22, underVO: 0.3 }
// Warm         BPM 96   MOTION { enter: 0.75, stagger: 0.08, exit: 0.40 }  MIX { master: 1, drums: 0.7, bass: 0.9, keys: 1.15, pads: 1, reverb: 0.35, underVO: 0.28 }
// Editorial    BPM 92   MOTION { enter: 0.70, stagger: 0.08, exit: 0.35 }  MIX { master: 1, drums: 0.6, bass: 0.85, keys: 1.1, pads: 1.1, reverb: 0.4, underVO: 0.25 }
```

Fonts are embedded as base64 with `fonts.py` (section 10). Check that the display face has tabular figures (`tnum`) before you set counters in it. Newsreader and Inter do; Instrument Serif, for example, does not, so its counters jitter. Google Fonts are licensed OFL or Apache 2.0, so embedding them is fine; a brand font needs the brand's licence.

**Update-specific style notes:**
- **Tech** (the starter): mono indices and changelog, crisp 0.45 s moves, an electric accent and a dark stage.
- **Clean:** a white stage and soft cards.
- **Fun:** badges bounce (`Ez.back`) and each feature has its own colour.
- **Professional:** no badges, just version tags, with a calmer score.

## 6. Design system (decide it, then never improvise)

- **Grid:**
  - 16:9 is 1920×1080 with side margins of 120–160 px and a top safe line around 90–120 px.
  - 9:16 is 1080×1920 with text kept inside x 90–990 and y 220–1500, clear of the platform UI.
  - Left-align editorial type on the margin; centre lockups and end cards.
- **Type:**
  - Display 150–200 px (on 9:16, 120–170 at 1080 wide), headline 96–130, subline 36–52, eyebrow 18–24 caps; display line height 1.05–1.15.
  - Hierarchy comes from scale and weight, not colour.
- **Colour:**
  - The brand primaries carry the film; accents are for emphasis only (a highlight, a warning, the CTA).
  - Alternate light and dark scenes for pacing, and check contrast.
- **Logo:**
  - Use the official file only; never redraw, outline, glow, rotate or recolour it.
  - For a knockout on a coloured background, use the official path with `fill-rule="evenodd"` and `fill="currentColor"`.
- **Motion:**
  - Use one family: expo-out entrances, quint in-out moves, and ease-in exits faster than the entrances. Stagger 40–90 ms per word.
  - Keep one dominant direction of travel; up reads as growth.
  - Keep holds alive with a 1–3% slow push. Transitions overlap by 0.2 s or less, and elements never collide.
- **Product UI:**
  - Rebuild the real screens in HTML/CSS at native desktop size inside a minimal browser frame, and drive them with `cam()`.
  - Match the screenshots exactly: labels, order, icons and spacing. Data is fictional, plausible and consistent across a series.
- **Never** (it reads as AI-generated):
  - Glowing gradient blobs, lens rays, glow rings, neon, grain, chromatic aberration and glitch.
  - Blur as a transition, random rotations, chaotic floating cards, and fake 3D wobble.
  - Generic purple gradients, everything centred at one size, and stock "futuristic" HUDs.
- **Update specifics:**
  - The left text column (index, badge, name, line) is identical in position for every feature, so only the content changes.
  - The demo card sits on the right at a fixed size.
  - The changelog roll-up uses the mono font at about 28 px, with lines prefixed `fix`, `new` or `improved`.

### Studio finish: made by a studio, not generated

Generated films share a look that viewers feel even when they can't name it:
- every element fades up 24 px on the same ease;
- everything is centred, and every scene lasts the same time;
- the copy fits any brand, the palette is default SaaS blue, and the music is a loop under a slideshow.

Hold every film to these rules. They sit under the user's brand and the dials, and above your own habits.

**Concept and specifics**
- **Own one idea.** Write the concept in one sentence that only this brand could say. "Saves you time" belongs to everyone. "Invoices that chase themselves" belongs to one product.
- **Be specific.** Use real-feeling nouns, names, times and amounts: "Harbor Dental · invoice 0417 · $1,240 · 3 days late", not "Client · Invoice · Amount".
  - Prefer odd, plausible numbers (47, 1,240, 3.8) over round ones (50, 1,000, 4.0).
  - Sample data is fictional but lived-in, and consistent from scene to scene.
- **Write like a person.** Keep copy short, concrete and a little surprising. Delete any line that would fit any brand.
  - Never use: "Introducing", "Elevate", "Unleash", "Empower", "Unlock", "Seamless", "Effortless", "Revolutionize", "Supercharge", "Game-changer", "Next-gen", "In a world where", "The future of", or "AI-powered" as filler.
  - Also avoid adjective triads ("Fast. Simple. Powerful."), rhyming slogans, and more than one rhetorical question per film.

**Rhythm and editing**
- **Vary shot lengths** (long, short, short, long), never every scene at the same 2 bars. Give the film one **breath** (a 2–4 s hold) and one **burst** (3–4 cuts or builds on consecutive beats).
- **Cut on action.** Start the incoming element's move 2–4 frames *before* the cut, so the first frame after it is already in motion. One frame of empty colour after a cut reads as a hiccup, and `verify.py check` flags any frame that is a single flat colour.
- **Design frame 0.** It is the thumbnail on social and the first impression on autoplay. Put the hook on it, never an empty background. The one exception is a deliberate fade from black of at most 0.5 s in a Premium or brand film.
- **Make every paused frame a poster.** Pause anywhere and the frame should be composed, not caught mid-mess. Read the contact sheets with that eye.
- **Give scenes continuity.** Link each scene to the next: a shape becomes the next background, a line keeps travelling, a colour floods the frame, or a word stays while the scene changes around it. Crossfades are the last resort.

**Composition**
- **Use the grid asymmetrically.** Most frames align left on the margin with deliberate negative space. Centre only lockups and end cards.
- **Give each frame one dominant element**, at least 3× the size of the next.
- **Crop with intent.** Type or UI running off the frame edge says "this is bigger than the screen". Accidental near-misses (a line 6 px from the edge) say "mistake".
- **Build depth from overlap and scale**, never from drop shadows, glows or blur.

**Type**
- **Always embed the fonts** (`fonts.py`). A system fallback looks like a default and changes from machine to machine. `verify.py` checks it.
- **Set real typography:**
  - Curly quotes and apostrophes (’ “ ”).
  - En dashes for ranges (9–5) and × for dimensions.
  - Non-breaking spaces in "10 km" and "4 min".
  - Tabular figures for every number that changes.
- **Choose a face for a reason:** a grotesk for engineering, a high-contrast serif for luxury, a humanist sans for care. Inter is a fine UI face but a weak default display face. With no brand font, pick a display face with character.
- **Hang the punctuation.** Put a negative `text-indent` (about −0.42 em) on a quote block, so the opening “ sits outside the text edge. The starter's word masks reset `text-indent`, so the words stay intact.
- **Check special glyphs.** `fonts.py` embeds the `latin` subset, which has no arrows (→) or ticks (✓). Draw those as SVG, or the browser silently uses a system font for them. `verify.py` lists any character outside the embedded subset.
- **Track by size and break by meaning:**
  - Big display type gets tight tracking (−1 to −3%). Small caps get open tracking (+6 to +14%).
  - Break lines by meaning, not by width.

**Colour**
- **Derive the palette** from the brand or the concept, never from a default.
- **Tint the neutrals:** warm paper `#f4f1ea` and ink `#15130f` instead of pure white and black.
- **Use one accent sparingly**, so it means something every time it appears.

**Motion**
- **Give each role its own movement:**
  - Type rises out of masks, and UI travels on a quint.
  - Small badges pop with a little overshoot, and the camera moves slowly.
  - One identical fade-up for everything is the clearest tell of all.
- **Overlap.** The outgoing element leaves while the incoming one arrives, and children trail their parent by 60–120 ms.
- **Swap inside a mask.** When one line of a multi-line headline changes, clip it in its own line mask, so the outgoing words never pass through the line above.
- **Stagger by meaning, not by index.** The important word lands last, on the beat.
- **Keep holds alive** with a 1–3% push or a slow drift. A frame that is dead still for more than 3 s feels frozen (`verify.py` flags it), except the final end-card hold.
- **Never decorate with motion that means nothing:**
  - Floating blobs, particles for their own sake, random wobble.
  - Lens flares, glitch, chromatic aberration, glow rings.
  - Fake 3D tilts and stock HUD graphics.

**Sound**
- **Score this film, not a loop.** Put hits on the cuts, a silence before the reveal, and a note per list item, so the list becomes a melody.
- **Make it feel played:**
  - Velocity variation (`hum(i)`).
  - Parts that change every 4 bars (drop the hats, bring in the arp, open the filter).
  - A fill into each new section.
- **Add width and air.** Pan hats, shakers and arps a little, and let hats, shakers and bells add 4–12 kHz shimmer. `analyze.py` checks both.
- **Treat silence as an instrument.** One bar of near-silence before the biggest moment makes it land.


## 7. The starter film (complete and working; copy it, then build on it)

Unpack `starter.html` (section 10), copy it to `film.html`, open it in Chrome or Edge, and press play. It is a finished 0:18 example of this category. Keep its engine, and replace the content and scenes with yours.

**What's inside the starter** (18.3 s at 118 BPM, Tech style):

| Beats | Scene | Technique |
|---|---|---|
| 0–4 | `RELEASE 4.2 · OCTOBER 2026`, "What's new", the `v4.2` chip pops | Header, back-ease chip |
| 4–28 | Three identical 8-beat slots (`01 / 03`, NEW, name, line, demo card). **Dark mode:** the toggle slides and the card re-themes (`mixC`). **Instant search:** "pricing" types and results stream in, with a timing chip. **Bulk edit:** 3 rows selected on beats, the action bar slides up, every row flips to Done | Equal slots, live UI demos |
| 28–32 | "Plus 12 fixes and improvements" with a mono changelog rolling past | Ticker |
| 32–36 | Lockup "Acme 4.2", "Update now. It's free.", CTA | End card |

**Architecture rules (non-negotiable):**
- `render(t)` calls one renderer per scene, and each renderer starts with `if (!show(scene, inWindow)) return;`. Nothing animates by itself: no CSS transitions or animations in `#stage`, no timers, and no `Math.random()` (use `hash01`).
- Call `splitWords()` and `splitChars()` once at load. Put layout measurements in `measure()`, which runs after fonts load and again on `loadingdone`.
- Times are authored in beats (`b(n)`), and schedules live in arrays (for example `ITEMS`) that the score reads too, so picture and sound can't drift apart.
- If you reuse an existing stylesheet (an app's CSS), prefix every new class and run the collision audit in section 12.
- Keep the player, the recorder hooks and the score engine exactly as they are. Change scenes, tokens, `MOTION`/`MIX`/`BPM` and `score`.

**How to get it:** run the unpack command in section 10 once. It writes `starter.html` and the toolkit next to your film. Then:

```bash
cp starter.html film.html
```

- **Read it once in full before editing.** It is plain HTML, CSS and JS with no embedded assets.
- **The helpers it gives you:**
  - Timing and easing: `P(t, a, b, ease)` (eased progress) and `Ez` (the easings).
  - Element state: `S(el, {x, y, s, r, o})` sets transform and opacity, `st` sets a style, `show` gates a scene by time, `txt` sets text, and `cls` toggles a class.
  - Entrances: `rise`, `wy`, `splitWords`/`wordsAt` and `splitChars`/`charsAt` for masked type reveals, and `stag` for staggers.
  - Movement: `keys` for keyframes, `pathAt` for arced cursor paths, `cam` for the UI camera, and `rel` for element boxes.
  - Cards: `prepCard` and `animCard` drive bars, counters, rings and typing inside a card.
  - Utilities: `typed`, `hash01` (deterministic randomness), `mixC` (colour blends) and `fmtN` (number formatting).
  - The score engine: `one`, `sus`, `harmony` and the instruments (section 9).
- **Change only:** the scenes, the `:root` tokens, `MOTION`/`MIX`/`BPM`, and `score`. The player, the recorder hooks (`window.seek`, `window.duration`, `window.stageSize`, `window.poster`, `window.renderWav`) and the engine stay as they are.
- **The quality bar:** a finished, more ambitious film made with this skill is in **`examples/`** (HTML, MP4 and poster) when the skill is installed as a folder; the skill works without it. Watch the MP4 to see the target. To borrow a technique, search its source with `grep -n`; don't read its embedded font blocks.

## 8. Update techniques

**Equal feature slots:** `FT = [b(4), b(12), b(20)]` with `SLOT = b(8)`. Every slot uses the same elements at the same positions; only the content and the demo change. To add a feature, add a `.ft` block, a time in `FT` and a demo function in `DEMO`.

**Demo patterns** (each a function of `u` = seconds into the slot, finishing by `SLOT - 0.4`):
- **Toggle and re-theme:** slide the knob and blend every colour with `mixC(from, to, k)` (background, text, borders).
- **Typing and results:** `typed()` plus results rising in with a 0.08 s stagger, then a stat chip. Only show real numbers.
- **Select and act:** checkboxes pop on the beat (`Ez.back`), an action bar slides up, and every affected row changes at the same moment (the "at once" is the feature).
- **Before/after:** clip the after layer across the before layer with `clip-path: inset(0 ${(1 - k) * 100}% 0 0)`, plus a divider.
- **New panel:** slide it in from the edge it lives on in the product (`x: 400 * (1 - k)`), never from a random side.

**Changelog roll-up:** a mono list in an overflow-hidden box, translated up linearly at a steady line rate (about 2–3 lines a second). Prefix `fix`, `new` or `improved` in the accent colour.

**Version chip:** a mono label on an accent fill that pops with `Ez.back`. Reuse it on the end card ("Acme 4.2").

## 9. Sound: the score engine

The score is written in `score()` on the same beat grid as the picture.
- `one(t, fn)` schedules a one-shot. `sus(t, dur, fn)` schedules a sustained event, and seeking mid-note still works.
- `pump()` schedules about 0.3 s ahead, every frame.
- `harmony(PROG)` turns a chord timeline into `chords()`, `pads()`, `arp()` and `groove()`.
- The instruments are `kick`, `clap`, `snare`, `hat`, `shaker`, `crash`, `bass`, `ep` (FM keys), `mallet`, `bell`, `pad`, `swell`, `whoosh` and `impact`, plus UI sounds (`click`, `tick`, `pop`).
- `MIX` sets the level of each group. `DUCK` dips the whole score under voiceover segments.
- `KEY` transposes everything.

**Update arrangement:**
- The header gets a chord and a pop on the chip, then a riser.
- An impact starts the groove (tight four-on-the-floor kick, sixteenth arp, light pads).
- Every feature gets a whoosh in, a pop on its NEW badge, and a mallet note climbing through the release.
- Demo actions are audible: a click on the toggle, ticks under typing, clicks on selections, and a two-note "done".
- Ticks while the changelog rolls, and a chord on the CTA.

**Score craft (what stops it sounding like a loop):**
- **Stereo:** `hat`, `shaker`, `ep`, `mallet`, `bell`, `tone` and `noise` take a `pan` argument (−1 is left, 1 is right).
  - Hats default to slightly right and shakers to slightly left. Chords spread their voices, the arp alternates sides, and pad voices sit left and right.
  - Keep kick, bass, claps and the melody in the centre.
- **Feel:** `hum(i, amt)` gives a deterministic velocity variation, for example `hat(w, B, 0.08 * hum(i))`.
  - The groove already uses it.
  - For swing, delay every second 16th note by 8–12 ms at most, so it stays on the grid.
- **Grid:** put every sound on the beat grid: UI clicks, ticks and pops on 16ths, and fast typing on 32nds. Writing a sound as `cue + 0.3` seconds puts it off the grid, and `analyze.py` will flag it.
- **Development:** change something every 4 bars, and add a fill (snare roll, tom-like `tone` drops or a reversed `swell`) into each section. Strip back before the biggest moment.
- **Air:** if `analyze.py` reports air below 3%, raise the hats and shaker, add `bell` accents, or open the pad filter (`cut` 2400–3200). Get air from transients (hat and shaker hits, bell and hammer attacks), not a steady noise bed, which sounds like hiss and masks the soft onsets the analyzer looks for.
- **Voice:** see "Voiceover (optional)" below. Under a voice, keep the bed simple: chords, pads and a soft pulse, with no busy arps.

**Mix targets** (`analyze.py` prints a PASS/WARN verdict for each):
- Peak below 0.9, with no clipping and 0 clicks.
- Music RMS around −22 to −12 dBFS. The MP4 export normalises to −14 LUFS.
- Intentional silences quieter than −35 dB, and an onset on every listed hit.
- Raw energy below 80 Hz under about 45%, with the A-weighted mids (250 Hz–4 kHz) at 55% or more.
- Air (A-weighted 4–12 kHz) at 3% or more, and stereo width (side/mid) between 0.08 and 0.6.
- Synth scores come out bass-heavy, so lower the kick and bass and raise the keys, claps and hats until it works on laptop speakers.

### Voiceover (optional: the user makes the audio, Claude writes and syncs)

Use a voice only when the film needs one: explainers, tutorials, walkthroughs, or a testimonial with no real recording. There is no API and no key. Claude writes the script, the user generates the audio in ElevenLabs (or any TTS, or records it), and pastes the MP3 into the chat. Claude then syncs the film to it.

**1. Write the script for the ear, and save it as `vo_script.txt`:**
- **One line per caption.** Each line is a short sentence or phrase that matches one picture beat.
- **Budget about 2.5 words per second** of speech, plus the pauses. A 30 s film holds about 60 spoken words.
- **Write it the way people say it:**
  - Use contractions, and spell numbers as they are spoken ("forty-eight thousand", "three point eight").
  - Write symbols out ("and", "percent").
  - Spell acronyms the way they sound ("S-Q-L", or "sequel" if that's how the brand says it).
- **Mark pauses** with `<break time="0.6s" />` at the end of a line. Eleven Multilingual v2, Turbo and Flash honour it. For Eleven v3, use a new paragraph or "…" instead, with optional audio tags such as `[warmly]`.

**2. Hand it over in one message, ready to paste:**
- The whole script in a single code block.
- The voice to look for, for example "warm, unhurried, mid-30s, neutral accent".
- Suggested settings:
  - Model: Eleven Multilingual v2.
  - Stability around 50%, Similarity around 75%, Style 0–15%, Speaker boost on, Speed 1.0.
  - Download as MP3 at 44.1 kHz.
- The ask: "Paste the MP3 here, or tell me its path." Re-generate any line that sounds off before sending.

**3. Keep building.** Lay the scenes out on the planned timings (2.5 words per second plus each break), so nothing waits on the audio.

**4. When the audio arrives:**
1. Save it as `vo.mp3` next to the film. If the attachment has no file path, ask the user to drop it in the project folder.
2. Run `python vo_timing.py vo.mp3 --lines vo_script.txt`. It prints `SUBS`, `DUCK`, `VO_LINES` and the minimum `DUR`.
3. Paste `DUCK` into the timeline block, so the score dips to `MIX.underVO` while someone speaks.
4. Pin each scene's key move to its line start, in one of two ways:
   - **Short films (the default):** set the scene times from `VO_LINES`, for example `const T_STEP2 = VO_LINES[3]`, instead of beat numbers. Keep the score as a soft bed (pads, chords, a gentle pulse), so no hit needs to land on a word.
   - **Longer films:** build the scenes in script time, then map voice time to script time with piecewise-linear anchors, as below. `render(t)` calls `renderScript(Ow(t))`, while the voice and the score run in film time.
     ```js
     const ANCH = [[0, 0], [8, 9.3], [20, 22.1]];   // [script time, voice time] at each pinned beat (voice times from VO_LINES)
     const Ow = T => { for (let i = 0; i < ANCH.length - 1; i++) { const [a, A] = ANCH[i], [b, B] = ANCH[i + 1]; if (T < B) return a + (T - A) * (b - a) / (B - A); } const [a, A] = ANCH[ANCH.length - 1]; return a + (T - A); };
     ```
5. Show captions from `SUBS` if the film is captioned.
6. Add `<audio id="vo" src="vo.mp3" preload="auto"></audio>` to the body, then run `inline.py` to embed it.
7. Export with `python verify.py film.html mp4 --vo vo.mp3`.

**5. Check the sync:**
- Every key move lands within 0.1 s of the word that names it.
- The last word ends at least 2 s before the end of the film.
- The voice sits about 10 dB above the bed.
- If the user sends a new take, re-run `vo_timing.py` and re-pin the beats. Never stretch the audio.


## 10. Toolkit: verify, analyse, embed, export

The toolkit and the starter film travel with this skill: they are in the skill's `templates/` and `scripts/` folders when it is installed as a folder, and the same files are embedded in the appendix at the end of this file, so `SKILL.md` on its own is enough. Unpack them next to the film once, so every command in this file works as written:

```bash
python3 - "<path to this SKILL.md>" <<'EOF'
# Writes starter.html and the five toolkit scripts into the current folder: from the skill's
# templates/ and scripts/ folders when they exist, otherwise from the copies embedded in SKILL.md.
import pathlib, re, shutil, sys
skill = pathlib.Path(sys.argv[1]).expanduser().resolve(); root = skill.parent
embedded = dict(re.findall(r'<!-- file: (\S+) -->\n````[a-z]*\n(.*?)\n````', skill.read_text(encoding='utf-8'), re.S))
for n in ['starter.html', 'verify.py', 'analyze.py', 'fonts.py', 'inline.py', 'vo_timing.py']:
    src = root / ('templates' if n.endswith('.html') else 'scripts') / n
    if src.exists():
        shutil.copy(src, n); how = f'copied from {src.parent.name}/'
    elif n in embedded:
        pathlib.Path(n).write_text(embedded[n] + '\n', encoding='utf-8'); how = 'unpacked from SKILL.md'
    else:
        sys.exit(f'{n} not found: re-download the skill')
    print(f'{n:14s} {how}')
EOF
pip install websocket-client pillow numpy    # once (add miniaudio to read MP3s in vo_timing.py)
```

- **The path:** in Claude Code, it is the skill's base directory (shown when the skill loads) plus `/SKILL.md`. In the Claude apps, the uploaded skill is on disk too; use the path it loaded from.
- **No file on disk?** If you can't read this `SKILL.md` as a file, write each file from the appendix out verbatim with your file tool, under the name its marker gives.
- Then start the film from the starter: `cp starter.html film.html`.

You also need Chrome, Chromium or Edge (set `CHROME=/path` if it isn't found), plus FFmpeg for the MP4.

| Command | What it does |
|---|---|
| `python verify.py film.html check` | Sweeps for exceptions every 0.05 s and checks that every font, weight and glyph in use is embedded. It also scans a frame every 0.1 s for **blank frames** and **static holds**. |
| `python verify.py film.html frames 0 30 0.5` | Saves frames and 3-column contact sheets in `verify_out/`. |
| `python verify.py film.html at 7.9 8.0 8.1` | Saves frames at exact moments, such as around every cut. |
| `python verify.py film.html start` | Captures the player's start screen: the poster frame and the overlay. |
| `python verify.py film.html poster [t]` | Saves `poster.jpg` at `window.poster`, or at `t` if given. |
| `python verify.py film.html wav` | Renders the score offline to `verify_out/score.wav`. |
| `python verify.py film.html eval "js" [t]` | Evaluates an expression in the recording page, optionally after `seek(t)`, and prints the JSON result. Use it to debug sizes, styles and state without guessing. |
| `python verify.py film.html mp4 [fps]` | Exports **the finished MP4**: renders the score offline, pipes the frames to FFmpeg, normalises to −14 LUFS, encodes H.264 with `+faststart`, and writes `film.jpg` as the poster. |
| `python analyze.py verify_out/score.wav [a-b …] --bpm N --hits t,t --silent a-b` | Measures loudness, tonal balance, **air** (4–12 kHz), **stereo width**, timing on the grid and clicks, and ends with a **PASS/WARN verdict**. |
| `python fonts.py google "Family" 300,600 [--italic] --into film.html` | Embeds Google Fonts as base64; a variable font is embedded once, with a weight range. For extra axes, pass the axis spec as it is: `google "Archivo" "wdth,wght@62..125,100..900"` (width) or `"opsz,wght@6..72,300..400"` (optical size). Use `local "Brand" Bold.woff2:700 …` for the brand's own files. |
| `python inline.py film.src.html film.html` | Inlines every local image, font, audio, CSS and JS file, so the film is one file. |
| `python vo_timing.py vo.mp3 --lines vo_script.txt` | Syncs a voiceover the user made (for example in ElevenLabs). It finds where each line lands and prints `SUBS`, `DUCK`, `VO_LINES` and the minimum `DUR`. ElevenLabs `<break>` tags and `[audio tags]` in the script are ignored. |

Options for `verify.py`:
- `--out DIR` sets the output folder.
- `--size WxH` overrides the stage size, which is otherwise read from `window.stageSize`.
- `--scale 2` renders at 4K.
- For `mp4`: `--vo vo.mp3` mixes a voiceover over the ducked score, `--audio vo|none` changes the audio, and `--crf 18` and `--lufs -14` set quality and loudness.

**Every `WARNING:` line is a bug unless it is deliberate.** The common ones:
- Fonts not embedded.
- A blank first frame, which makes an empty thumbnail.
- A flat frame after a cut (cut on action instead).
- Nothing moving for 3 s or more.

**Working with embedded fonts:** after `fonts.py --into`, the film contains large base64 blocks.
- Never read the whole file back into context. Search for the code you need (`grep -n`), then read that range.
- Or keep the fonts in a separate file while you build:
  1. Run `python fonts.py google "Inter" 300,600 > fonts.css` and add `<link rel="stylesheet" href="fonts.css">`.
  2. Build `film.src.html` against it.
  3. Publish with `python inline.py film.src.html film.html`.


## 11. Verify (mandatory before you say "done")

```bash
python verify.py film.html check                       # sweep + fonts + blank frames + static holds (fix every WARNING)
python verify.py film.html frames 0 18 0.5          # sweep + a frame every 0.5 s → verify_out/sheet_*.png
python verify.py film.html at 7.9 8.0 8.1 8.2          # exact moments around every transition and cut
python verify.py film.html start                       # poster frame + start overlay
python verify.py film.html wav && python analyze.py verify_out/score.wav 0-2 2-6 6-14 14-18.3 --bpm 118 --hits 2.03,16.27
```

Open every contact sheet and look at it properly. Fix, re-render and re-check until all of this passes:

1. **Sweep:** no exceptions anywhere on the timeline, and no page errors.
2. **Frames:**
   - Nothing clipped, overflowing or colliding during transitions.
   - Margins are consistent, with no orphaned single words (balance lines with `<br>`).
   - Descenders are intact at rest, the logo is untouched, and contrast is fine.
3. **Logic:**
   - Every typing animation, counter, ring and line finishes while fully visible.
   - Reveal order makes sense.
   - Clocks and counters agree.
   - The first and last items get the same time as the others.
4. **Copy:** exact strings, product names spelled right, no invented claims, and sample data clearly fictional.
5. **Audio:**
   - Peak below 0.9 with no clipping, 0 clicks, and music RMS around −22 to −12 dBFS (the MP4 is normalised to −14 LUFS).
   - Air (A-weighted 4–12 kHz) at 3% or more and stereo width between 0.08 and 0.6: read the `analyze.py` verdict.
   - Intentional silences are quieter than −35 dB, and every listed hit shows an onset.
   - Raw energy below 80 Hz stays under about 45%, while the A-weighted mids dominate. Synth scores come out bass-heavy, so lower the kick and bass and raise the keys, claps and hats until it works on laptop speakers.
6. **Update checks:**
   - Every feature has the same slot length and layout, and the names match the changelog.
   - Every demo shows the change happening, not a static screenshot.
   - Demos finish before their slot ends.
   - The roll-up count matches the real number of fixes.
7. **Studio finish:** `verify.py check` prints no `WARNING:` lines (or each one is deliberate and noted), the `analyze.py` verdict is all PASS (or each WARN is explained), and the director's review below scores 4 or more on every line.
8. **Creative settings:** the film matches the resolved dials (section 0), passes that level's checks, and records them in its header comment.

### Director's review (after every check passes)

Open the contact sheets at thumbnail size and watch the film once with sound and once without. Score each line from 1 to 5, honestly, and ship only when every line scores 4 or 5:

1. **Thumbnail:** would frame 0 and the poster frame make someone stop scrolling?
2. **Message:** after one viewing with the sound off, can you repeat the key line?
3. **Specificity:** could a competitor run this film by swapping the logo? If yes, the concept and copy are generic.
4. **Rhythm:** do shot lengths vary, with one breath and one burst? Does every cut land on the grid?
5. **Hierarchy:** in every frame, is it obvious where to look first?
6. **Craft:** fonts embedded, curly quotes, tabular numbers, no widows, nothing touching an edge by accident.
7. **Motion:** does each kind of element move in its own way, with overlap? Does any frame look like a template?
8. **Sound:** does the music follow the picture (hits, a silence, a melody from the items), or is it a loop under slides?
9. **The tells:** no blank frames, no glows, blobs, purple gradients or glitch, no banned copy.

Write the scores in your notes and fix the lowest line first. Re-render the frames you changed and their neighbours.


## 12. Export, collisions and pitfalls

**MP4 (when the user chose MP4 or both):**
```bash
python verify.py film.html mp4                 # → film.mp4 + film.jpg (poster), 30 fps, at the stage size, score at −14 LUFS
python verify.py film.html mp4 60 --scale 2    # 60 fps 4K master
python verify.py film.html mp4 --vo vo.mp3     # a voiceover mixed over the ducked score
```
- `mp4` renders the score in a fresh page load, then streams every frame (seek, screenshot) into FFmpeg. Nothing plays in real time, so the result is frame-accurate on any machine.
- Use −14 LUFS for the web, YouTube and social. The file gets `+faststart`, so it starts playing before it has fully downloaded.
- Check the result: `ffprobe -v error -show_entries stream=codec_name,width,height,duration -of compact film.mp4`, plus a look at `film.jpg`.

**CSS collision audit** (whenever you reuse an existing stylesheet):
```python
import re; base = open('base.css').read(); mine = set(c for m in re.findall(r'class="([^"]+)"', open('film.html').read()) for c in m.split())
for sel, body in re.findall(r'([^{}]+)\{([^{}]*)\}', base):
    hit = [c for c in mine if re.search(r'\.' + re.escape(c) + r'(?![\w-])', sel)]
    if hit: print(hit, '→', sel.strip()[:80])
```

**Hard-won pitfalls:**
- **Silent render crashes.** An exception inside `seek()` doesn't fire page error events. The sweep in `verify.py` catches it, so always read its line.
- **Descenders.** Masked words clip descenders mid-rise. That's fine in motion, but check the at-rest frames.
- **Hidden elements.** `display:none` measures as zero, so `measure()` un-hides before reading sizes.
- **Gated elements and CSS `display:none`.** `show()` clears the inline style, so an element that CSS hides with `display:none` stays hidden for ever. Hide gated elements only through `show()` (or opacity), never in the stylesheet.
- **Line draws.** A zero-length dash with `stroke-linecap: round` still paints a dot, and a `pathLength` dash at offset 1 can leave a sliver. Keep a stroke at opacity 0 until its draw starts.
- **Width overflow.** Long lines overflow; measure them and auto-fit the font size against the real column width.
- **Camera zooms.** New items must appear inside the frame. Pull back in stages, each on a beat.
- **Timing budgets.** An element on screen for 0.66 s must finish all its internal motion inside 0.6 s. Scale the durations (`prepCard(c, stagger, speed)`).
- **Transitions.** Sequence motion so elements never pass through each other: the headline clears the area before the product rises.
- **Sidechain automation.** Put ducking on a separate gain node, never on the envelope gain, and ramp it (never jump) to avoid clicks.
- **Offline vs live audio.** `renderWav()` replaces the live audio context, so run it in its own `?record` page load (which `verify.py wav` does).
- **Edits.** When the user asks for one change ("only change X"), make a surgical edit and keep a backup first. Re-verify those frames and their neighbours, and change nothing else.
- **Asking.** Don't ask what you can decide. Report what you verified, what you assumed (sample data, story devices like a clock), and how to watch it (sound on, Chrome or Edge).
- **Clicks at note starts.** A new GainNode is at gain 1 until its first scheduled event, so one full-level sample leaks through before an envelope begins. Every instrument here sets `g.gain.value = 0.0001` first; do the same in any instrument you add, and check that `analyze.py` reports 0 clicks.
- **Update specifics:**
  - Keep benefit lines under about 9 words, or they wrap and push the layout.
  - If a feature is plan-limited, add a small plan badge next to NEW instead of a footnote.

## 13. Hand-off message

Lead with what to watch and where: the file path, the length, and "sound on, in Chrome or Edge". Then include:
- A scene table (time, picture, copy).
- What the score does.
- How you verified it: frames, sweep and audio numbers.
- The deliverables in the format the user chose: `film.html` (plays offline in Chrome or Edge), and/or `film.mp4` (H.264, −14 LUFS) with `film.jpg` (the poster), with their sizes.
- Assumptions and claims to double-check.
- The creative settings used (for example `creativity medium · typography high · animation medium · motion medium`), and that any dial can be changed with `--creativity`, `--typography`, `--animation` or `--motion` (`low`, `medium` or `high`).
- An invitation to give feedback by timestamp.

## 14. Appendix: embedded files (the starter film and the toolkit)
<!-- appendix: embedded files -->
These are byte-for-byte copies of `templates/starter.html` and `scripts/*.py`, so this file works on its own. The unpack command in section 10 writes them out; you never need to retype them. Each file sits under a `<!-- file: NAME -->` marker, in a four-backtick fence.

### `starter.html`: the starter film (copy it to film.html)

<!-- file: starter.html -->
````html
<!doctype html>
<!--
  Feature update starter (Tech style): a release header, 3 equal feature slots with live UI demos (theme toggle, instant search, bulk edit), a changelog roll-up and an update CTA
  Watch     open in Chrome or Edge, click play. Space play/pause · ←/→ seek · M mute · F fullscreen · H hide controls
  Record    film.html?record → await window.videoReady → window.seek(t) per frame (silent, UI hidden)
  Score     window.renderWav({ rate, mono }) → WAV Blob of the whole score (run it in its own ?record page load)
  Params    ?t=12 opens at 12 s · ?autoplay · ?mute · ?loop
  Rules     every visual is a pure function of time t (render(t)); no CSS transitions/animations inside #stage
  Creative  --creativity:medium --typography:medium --animation:medium --motion:medium  (section 0: record the levels you resolve here)
-->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Acme — What’s new in 4.2</title>
<style>
/* ===================== style tokens: swap for a preset (section 5) or the brand ===================== */
:root{--bg:#0b0d10;--fg:#e6edf3;--muted:#8b949e;--line:#1f2630;--panel:#11161c;--dark:#06080a;--dark-ink:#e6edf3;--accent:#4cc2ff;--accent-ink:#06080a;--accent-soft:#0f2a3a;--warn:#f0b72f;--ok:#3fb950;
  --display:'Space Grotesk','Segoe UI',system-ui,sans-serif;--ui:'Inter','Segoe UI',system-ui,sans-serif;--mono:'JetBrains Mono',ui-monospace,Consolas,monospace;
  --w-display:500;--w-strong:600;--fs-display:140px;--track:-0.02em;--track-caps:0.12em;--margin:150px;--radius:10px;--btn-radius:8px}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:#000;overflow:hidden}
body{font-family:var(--ui);color:var(--fg);-webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}
#stage{position:absolute;left:0;top:0;transform-origin:0 0;overflow:hidden;background:var(--bg);visibility:hidden}
.ready #stage{visibility:visible}
.scene{position:absolute;inset:0;overflow:hidden}
.light{background:var(--bg);color:var(--fg)} .dark{background:var(--dark);color:var(--dark-ink)} .brand{background:var(--accent);color:var(--accent-ink)}
/* masked words and letters: generous padding so descenders survive at rest */
.wm{display:inline-block;overflow:hidden;vertical-align:top;padding:.08em .06em .24em;margin:-.08em -.06em -.24em;text-indent:0}   /* text-indent:0 so a hung quote (text-indent on the block) never shifts words inside their masks */
.w,.ch{display:inline-block}
.h1{position:absolute;left:var(--margin);font-family:var(--display);font-weight:var(--w-display);font-size:var(--fs-display);line-height:1.08;letter-spacing:var(--track);white-space:nowrap;transform-origin:0 50%}
.h1.c{left:0;right:0;text-align:center;transform-origin:50% 50%}
.ln{display:block;white-space:nowrap}
.eb{font-family:var(--display);font-weight:var(--w-strong);font-size:22px;letter-spacing:var(--track-caps);text-transform:uppercase;display:inline-flex;align-items:center;white-space:nowrap}
.sep{display:inline-block;width:2px;height:20px;background:currentColor;opacity:.25;margin:0 16px}
.num{font-variant-numeric:tabular-nums}
.sub{font-family:var(--display);font-weight:var(--w-display);font-size:40px;line-height:1.3;letter-spacing:var(--track)}
.xa{opacity:0}
.caret{display:inline-block;width:2px;height:1.05em;background:var(--accent);margin-left:1px;vertical-align:-.15em}
/* end-card lockup: REPLACE the placeholder mark with the official logo */
.lock{position:absolute;left:0;right:0;display:flex;align-items:center;justify-content:center;gap:40px}
.mk{display:block;width:140px;height:140px;overflow:hidden;flex:none}
.mk svg{display:block;width:100%;height:100%}
.wd{display:inline-block;overflow:hidden;padding:.06em .05em .16em;font-family:var(--display);font-weight:var(--w-strong);font-size:132px;line-height:1;letter-spacing:var(--track)}
.wd > span{display:inline-block}
.cta{display:inline-flex;align-items:center;gap:14px;height:84px;padding:0 38px;border-radius:var(--btn-radius);background:var(--accent);color:var(--accent-ink);font-family:var(--display);font-weight:var(--w-strong);font-size:32px}
/* ---------- player UI (outside the stage) ---------- */
#ui{position:fixed;inset:0;pointer-events:none;font:15px system-ui,sans-serif;color:#fff;z-index:10}
.rec #ui{display:none}
#start{position:absolute;inset:0;display:flex;flex-direction:column;gap:16px;align-items:center;justify-content:center;text-align:center;padding:24px;background:rgba(0,0,0,.55);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);pointer-events:auto;cursor:pointer;transition:opacity .4s}
#start.gone{opacity:0;pointer-events:none}
#start b{width:96px;height:96px;border-radius:50%;background:#fff;color:#000;display:grid;place-items:center;font-size:34px;padding-left:6px}
#start em{font-style:normal;font-size:24px;font-weight:600}
#start small{opacity:.8}
#bar{position:absolute;left:24px;right:24px;bottom:18px;height:22px;display:flex;align-items:center;pointer-events:auto;cursor:pointer;opacity:0;transition:opacity .3s}
.started #bar{opacity:1} .started.idle #bar{opacity:0} .idle{cursor:none}
#bar div{position:relative;width:100%;height:4px;border-radius:2px;background:rgba(255,255,255,.3)}
#bar i{position:absolute;left:0;top:0;height:100%;border-radius:2px;background:#fff;width:0}
/* ===================== this film ===================== */
#gridBg{position:absolute;inset:0;background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:120px 120px;opacity:.55}
#aEb{position:absolute;left:var(--margin);top:390px;font-family:var(--mono);font-weight:500;color:var(--accent)}
#aT{top:440px}
#aChip{position:absolute;left:var(--margin);top:630px;font:600 30px var(--mono);color:var(--accent-ink);background:var(--accent);border-radius:8px;padding:8px 18px;transform-origin:0 50%;opacity:0}
/* feature slots: the same layout for every feature */
.ft{position:absolute;inset:0}
.ft .idx{position:absolute;left:var(--margin);top:330px;font:500 24px var(--mono);color:var(--muted)}
.ft .new{position:absolute;left:var(--margin);top:384px;font:700 18px var(--mono);letter-spacing:.12em;color:var(--accent-ink);background:var(--accent);border-radius:6px;padding:6px 12px;transform-origin:0 50%}
.ft h2{position:absolute;left:var(--margin);top:440px;font-family:var(--display);font-weight:var(--w-display);font-size:104px;letter-spacing:var(--track);line-height:1.05;white-space:nowrap}
.ft p{position:absolute;left:var(--margin);top:580px;width:700px;font:400 36px/1.35 var(--ui);color:var(--muted)}
.ft .h2 .wm,.ft p .wm{padding:.08em .06em .24em;margin:-.08em -.06em -.24em}
.dc{position:absolute;left:1020px;top:220px;width:760px;height:640px;border-radius:18px;background:#fff;color:#111;font-family:var(--ui);overflow:hidden;box-shadow:0 0 0 1px #2a3340}
.dc .bar{height:56px;display:flex;align-items:center;gap:8px;padding:0 20px;border-bottom:1px solid #e5e7eb}
.dc .bar i{width:11px;height:11px;border-radius:50%;background:#d4d4d8}
/* 1 · theme toggle */
#d0 .body{padding:34px}
#d0 .row{display:flex;align-items:center;justify-content:space-between;height:84px;border-bottom:1px solid #e5e7eb;font-size:26px}
#tg{position:relative;width:96px;height:52px;border-radius:26px;background:#d4d4d8}
#tg i{position:absolute;left:6px;top:6px;width:40px;height:40px;border-radius:50%;background:#fff}
#d0 .lines div{height:22px;border-radius:11px;background:#e5e7eb;margin-top:22px}
/* 2 · instant search */
#d1 .body{padding:34px}
#sf{height:72px;border-radius:14px;box-shadow:inset 0 0 0 2px var(--accent);display:flex;align-items:center;padding:0 22px;font-size:30px;color:#111}
#sf .ph{color:#9ca3af}
.res{display:flex;align-items:center;gap:18px;height:84px;padding:0 18px;border-radius:12px;margin-top:10px;font-size:25px}
.res b{font-weight:700}
.res em{margin-left:auto;font-style:normal;font-size:18px;color:#6b7280;font-family:var(--mono)}
.res.top{background:#eff6ff}
#d1 .stat{position:absolute;right:34px;bottom:34px;font:700 24px var(--mono);color:#0b0d10;background:#e0f2fe;border-radius:10px;padding:10px 16px;opacity:0}
/* 3 · bulk edit */
#d2 .body{padding:24px 30px}
.br{display:grid;grid-template-columns:40px 1fr 150px;align-items:center;gap:18px;height:80px;border-bottom:1px solid #eef0f3;font-size:24px}
.cb{position:relative;width:30px;height:30px;border-radius:7px;box-shadow:inset 0 0 0 2px #cbd5e1}
.cb b{position:absolute;inset:0;border-radius:7px;background:var(--accent);transform:scale(0)}
.st{font:600 18px var(--mono);border-radius:999px;padding:6px 12px;width:max-content;background:#f1f5f9;color:#475569}
.st.dn{background:#dcfce7;color:#166534}
#bulk{position:absolute;left:30px;right:30px;bottom:28px;height:76px;border-radius:14px;background:#0b0d10;color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 24px;font-size:24px;opacity:0}
#bulk span:last-child{font:600 20px var(--mono);color:var(--accent-ink);background:var(--accent);border-radius:8px;padding:8px 14px}
/* roll-up */
#cT{top:250px;font-size:96px}
#log{position:absolute;left:var(--margin);top:450px;width:1400px;height:420px;overflow:hidden;font:400 30px/70px var(--mono);color:var(--muted)}
#logIn div b{color:var(--accent);font-weight:500;display:inline-block;width:170px}
/* CTA */
#eIn{position:absolute;inset:0;transform-origin:50% 46%}
#eLock .mk{color:var(--accent)}
#eLet{position:absolute;left:0;right:0;text-align:center}
#eCtaW{position:absolute;left:0;right:0;display:flex;justify-content:center;opacity:0}
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <!-- placeholder mark: REPLACE with the official logo path (fill="currentColor"; fill-rule="evenodd" gives a knockout) -->
  <symbol id="mark" viewBox="0 0 100 100"><path fill="currentColor" fill-rule="evenodd" d="M22 0h56a22 22 0 0 1 22 22v56a22 22 0 0 1-22 22H22A22 22 0 0 1 0 78V22A22 22 0 0 1 22 0ZM50 25 74 75H26Z"/></symbol>
  <symbol id="tick" viewBox="0 0 24 24"><path d="M6.2 12.6l3.9 3.9 7.7-8.4"/></symbol>
  <symbol id="cursor" viewBox="0 0 24 24"><path d="M4 2.5v17.2l4.6-4.4 3 6.7 3.1-1.4-3-6.6 6.3-.2z" fill="#111" stroke="#fff" stroke-width="1.4" stroke-linejoin="round"/></symbol>
</defs></svg>

<div id="stage">
  <div class="scene dark"><div id="gridBg"></div></div>
  <section class="scene" id="sA"><div class="eb" id="aEb">Release 4.2 · October 2026</div><div class="h1" id="aT">What’s new</div><span id="aChip">v4.2</span></section>
  <section class="scene" id="sB">
    <div class="ft" id="f0"><span class="idx">01 / 03</span><span class="new">NEW</span><h2 class="h2">Dark mode</h2><p>Easier on the eyes, everywhere in the app.</p>
      <div class="dc" id="d0"><div class="bar"><i></i><i></i><i></i></div><div class="body"><div class="row"><span>Appearance</span><span id="tg"><i></i></span></div><div class="row"><span>Theme</span><span id="thName">Light</span></div><div class="lines"><div style="width:90%"></div><div style="width:72%"></div><div style="width:84%"></div><div style="width:60%"></div></div></div></div></div>
    <div class="ft" id="f1"><span class="idx">02 / 03</span><span class="new">NEW</span><h2 class="h2">Instant search</h2><p>Find any client, report or task as you type.</p>
      <div class="dc" id="d1"><div class="bar"><i></i><i></i><i></i></div><div class="body"><div id="sf"><span class="ph" id="sfPh">Search everything…</span><span id="sfTx"></span><i class="caret" id="sfCar"></i></div>
        <div class="res top xa"><b>Pricing</b> page · Harbor Dental<em>report</em></div><div class="res xa">Pricing review<em>task</em></div><div class="res xa">Pine &amp; Co. pricing deck<em>file</em></div><div class="res xa">Q4 pricing notes<em>doc</em></div></div><span class="stat" id="stat">results in 40 ms</span></div></div>
    <div class="ft" id="f2"><span class="idx">03 / 03</span><span class="new">NEW</span><h2 class="h2">Bulk edit</h2><p>Select many rows and change them at once.</p>
      <div class="dc" id="d2"><div class="bar"><i></i><i></i><i></i></div><div class="body">
        <div class="br"><span class="cb"><b></b></span><span>Homepage copy</span><span class="st">In review</span></div><div class="br"><span class="cb"><b></b></span><span>Sitemap update</span><span class="st">In review</span></div>
        <div class="br"><span class="cb"><b></b></span><span>GA4 events</span><span class="st">In review</span></div><div class="br"><span class="cb"></span><span>Photo shoot</span><span class="st">Planned</span></div></div>
        <div id="bulk"><span id="bulkN">3 selected</span><span>Mark as done</span></div></div></div>
  </section>
  <section class="scene" id="sC"><div class="h1" id="cT">Plus 12 fixes and improvements</div>
    <div id="log"><div id="logIn"><div><b>improved</b>Reports load 3× faster on large accounts</div><div><b>fix</b>Calendar sync no longer duplicates events</div><div><b>new</b>Export any table to CSV</div><div><b>fix</b>Mentions now notify the right teammate</div><div><b>improved</b>Sharper charts on high-DPI screens</div><div><b>new</b>Keyboard shortcut for search: ⌘K</div><div><b>fix</b>Long names no longer overflow cards</div><div><b>improved</b>Smoother scrolling in tables</div></div></div></section>
  <section class="scene" id="sD"><div id="eIn">
    <div class="lock" id="eLock"><span class="mk" id="eMark"><svg viewBox="0 0 100 100"><use href="#mark"/></svg></span><span class="wd"><span id="eWord">Acme 4.2</span></span></div>
    <div class="sub" id="eLet">Update now. It’s free.</div><div id="eCtaW"><span class="cta">acme.example.com/changelog →</span></div></div></section>
</div>

<div id="ui">
  <div id="start"><b>▶</b><em>Acme — What’s new in 4.2</em><small>0:18 · Sound on · Space play/pause · ←/→ seek · M mute · F fullscreen · H hide controls</small></div>
  <div id="bar"><div><i id="barFill"></i></div></div>
</div>

<script>
(() => {
'use strict';
const Q = new URLSearchParams(location.search), REC = Q.has('record');

/* ===================== timeline: authored in beats, so a tempo change moves everything together ===================== */
const SW = 1920, SH = 1080;
const BPM = 118, BEAT = 60 / BPM, b = n => +(n * BEAT).toFixed(4);
const DUR = b(36), POSTER = b(34);
const MOTION = { enter: 0.45, stagger: 0.05, exit: 0.25 };   // Tech preset
const MIX = { master: 1, drums: 1.05, bass: 1, keys: 1.1, pads: 0.8, reverb: 0.22, underVO: 0.3 };
const DUCK = [];
const FT = [b(4), b(12), b(20)];                             // three equal 8-beat slots
const SLOT = b(8);

/* ===================== helpers: every visual is a pure function of time t ===================== */
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const clamp = (v, a = 0, c = 1) => (v < a ? a : v > c ? c : v), mix = (a, c, k) => a + (c - a) * k;
const Ez = {
  lin: x => x, out: x => 1 - (1 - x) ** 3, out4: x => 1 - (1 - x) ** 4, in: x => x * x * x,
  expo: x => (x >= 1 ? 1 : 1 - 2 ** (-10 * x)),                  // entrances
  q5: x => (x < 0.5 ? 16 * x ** 5 : 1 - (-2 * x + 2) ** 5 / 2),   // moves, wipes, camera
  back: x => 1 + 2.25 * (x - 1) ** 3 + 1.25 * (x - 1) ** 2,       // small pops only
  elastic: x => (x <= 0 ? 0 : x >= 1 ? 1 : 2 ** (-10 * x) * Math.sin((x * 10 - 0.75) * 2.094) + 1),   // fun styles only
};
const P = (t, a, c, e = Ez.out) => e(clamp((t - a) / (c - a)));   // eased 0→1 progress of t through [a, c]
function S(el, { x = 0, y = 0, s = 1, sx = 1, sy = 1, r = 0, o } = {}) {   // transform + opacity, cached (never mix with st(el,'transform'))
  const tf = `translate3d(${x.toFixed(2)}px,${y.toFixed(2)}px,0)` + (r ? ` rotate(${r.toFixed(2)}deg)` : '') + (s !== 1 ? ` scale(${s.toFixed(4)})` : '') + (sx !== 1 || sy !== 1 ? ` scale(${sx.toFixed(4)},${sy.toFixed(4)})` : '');
  if (el._tf !== tf) { el.style.transform = tf; el._tf = tf; }
  if (o != null) { const v = clamp(o).toFixed(3); if (el._op !== v) { el.style.opacity = v; el._op = v; } }
}
const st = (el, p, v) => { if (el['_' + p] !== v) { if (p.startsWith('--')) el.style.setProperty(p, v); else el.style[p] = v; el['_' + p] = v; } };
const show = (el, on) => { st(el, 'display', on ? '' : 'none'); return on; };   // gate every scene by time
const txt = (el, s) => { if (el._tx !== s) { el.textContent = s; el._tx = s; } };
const cls = (el, c, on) => { if (el['_c' + c] !== !!on) { el.classList.toggle(c, !!on); el['_c' + c] = !!on; } };
const typed = (s, t, a, c) => s.slice(0, Math.round(P(t, a, c, Ez.lin) * s.length));
const rise = (el, t, a, z = null, dy = 24, d = 0.6) => { const i = P(t, a, a + d, Ez.expo), o = z == null ? 0 : P(t, z, z + MOTION.exit, Ez.in); S(el, { y: dy * (1 - i) - 16 * o, o: i * (1 - o) }); return i * (1 - o); };
const wy = (el, pct) => { const v = `translate3d(0,${pct.toFixed(2)}%,0)`; if (el._tf !== v) { el.style.transform = v; el._tf = v; } };
const hash01 = (a, c = 0) => { let h = (Math.imul(a + 1, 374761393) + Math.imul(c + 7, 668265263)) | 0; h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967296; };
const pressAt = (t, c) => t > c - 0.06 && t < c + 0.1;   // a click "press" frame window
const fmtN = (v, dec = 0) => dec ? v.toFixed(dec) : Math.round(v).toLocaleString('en-US');
const hexRgb = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
const mixC = (a, c, k) => { const A = hexRgb(a), C = hexRgb(c); return `rgb(${A.map((v, i) => Math.round(mix(v, C[i], clamp(k)))).join(',')})`; };   // blend two #rrggbb colours
function splitWords(el) {   // wrap each word in a mask so it rises from its baseline. Call ONCE, at load.
  const words = [], nodes = [...el.childNodes]; el.textContent = '';
  const add = n => { const m = document.createElement('span'), w = document.createElement('span'); m.className = 'wm'; w.className = 'w'; w.appendChild(n); m.appendChild(w); el.appendChild(m); words.push(w); };
  nodes.forEach(n => {
    if (n.nodeType === 3) n.textContent.split(/(\s+)/).forEach(p => { if (/^\s+$/.test(p)) el.appendChild(document.createTextNode(' ')); else if (p) add(document.createTextNode(p)); });
    else if (n.nodeName === 'BR') el.appendChild(document.createElement('br'));
    else if (n.nodeType === 1 && n.classList.contains('ln')) { el.appendChild(n); words.push(...splitWords(n)); }   // a .ln line keeps its own line, its words split inside it
    else add(n);   // an element (a <b>, a highlight span) moves as one word
  });
  return words;
}
function splitChars(el) {   // one span per letter (spaces kept) for letter-by-letter motion. Call ONCE, at load.
  const s = el.textContent; el.textContent = '';
  return [...s].map(c => { const sp = document.createElement('span'); sp.className = 'ch'; sp.textContent = c === ' ' ? '\u00a0' : c; el.appendChild(sp); return sp; });   // spaces become \u00a0: a plain space collapses inside an inline-block span
}
function wordsAt(ws, t, times, z = null, d = MOTION.enter) {   // word i rises at times[i]; all leave upward from z
  ws.forEach((w, i) => {
    const a = times[Math.min(i, times.length - 1)], k = P(t, a, a + d, Ez.expo);
    const o = z == null ? 0 : P(t, z + i * 0.03, z + i * 0.03 + MOTION.exit, Ez.in);
    wy(w, (1 - k) * 125 - o * 140);
  });
}
const stag = (ws, a, s = MOTION.stagger) => ws.map((_, i) => a + i * s);
function charsAt(cs, t, times, d = MOTION.enter, dy = 40) {   // letters rise and fade in at times[i] (use with splitChars)
  cs.forEach((c, i) => { const a = times[Math.min(i, times.length - 1)], k = P(t, a, a + d, Ez.expo); S(c, { y: dy * (1 - k), o: P(t, a, a + d * 0.4, Ez.lin) }); });
}
function keys(K, t, e = Ez.q5) {   // keyframes [[t, v1, v2, …], …] → eased values at t; two keys at the same t make a hard cut
  if (t <= K[0][0]) return K[0].slice(1);
  for (let i = 0; i < K.length - 1; i++) { const A = K[i], B = K[i + 1]; if (t < B[0]) { const k = B[0] > A[0] ? e(clamp((t - A[0]) / (B[0] - A[0]))) : 1; return A.slice(1).map((v, j) => mix(v, B[j + 1], k)); } }
  return K[K.length - 1].slice(1);
}
function pathAt(K, t) {   // a cursor path [[t, x, y], …] that travels in a gentle arc, like a hand
  if (t <= K[0][0]) return [K[0][1], K[0][2]];
  for (let i = 0; i < K.length - 1; i++) {
    const A = K[i], B = K[i + 1];
    if (t < B[0]) { const k = Ez.q5(clamp((t - A[0]) / (B[0] - A[0]))), dx = B[1] - A[1], dy = B[2] - A[2], bow = Math.sin(Math.PI * k) * 0.08; return [A[1] + dx * k - dy * bow, A[2] + dy * k + dx * bow]; }
  }
  const L = K[K.length - 1]; return [L[1], L[2]];
}
function cam(el, fx, fy, s, A) {   // UI camera: content laid out at A.aw×A.ah, seen through A.vw×A.vh; focus (fx, fy) at zoom s (1 = fit width)
  const k = (A.vw / A.aw) * s;
  const ax = (v, f, a) => (a * k <= v ? (v - a * k) / 2 : clamp(v / 2 - f * k, v - a * k, 0));   // content smaller than the view: centre it, never show an edge
  const tx = ax(A.vw, fx, A.aw), ty = ax(A.vh, fy, A.ah);
  const v = `translate3d(${tx.toFixed(2)}px,${ty.toFixed(2)}px,0) scale(${k.toFixed(5)})`;
  if (el._tf !== v) { el.style.transform = v; el._tf = v; }
}
function rel(el, root) {   // an element's box in root's (unscaled) coordinates
  let x = 0, y = 0, n = el;
  while (n && n !== root) { x += n.offsetLeft; y += n.offsetTop; n = n.offsetParent; }
  return { x, y, w: el.offsetWidth, h: el.offsetHeight, cx: x + el.offsetWidth / 2, cy: y + el.offsetHeight / 2 };
}
/* product cards: one animator for every card (staged .xa reveals, [data-v] bars, [data-num] counters, rings, [data-type] typing) */
function prepCard(c, stg = 0.05, spd = 0.75) {
  c._xa = $$('.xa', c); c._stg = stg; c._spd = spd;
  const at = e => { const j = c._xa.indexOf(e.closest('.xa')); return 0.08 + Math.max(0, j) * stg; };
  c._bars = $$('[data-v]', c).map(e => ({ e, v: +e.dataset.v, a: at(e) }));
  c._nums = $$('[data-num]', c).map(e => ({ e, to: +e.dataset.num, from: +(e.dataset.from || 0), dec: +(e.dataset.dec || 0), pre: e.dataset.pre || '', suf: e.dataset.suf || '', comma: !!e.dataset.comma, a: at(e) }));
  c._rings = $$('circle[data-p]', c).map(e => { const L = 2 * Math.PI * +e.getAttribute('r'); e.style.strokeDasharray = L.toFixed(2); e.style.strokeDashoffset = L.toFixed(2); return { e, L, p: +e.dataset.p, a: at(e) }; });
  c._types = $$('[data-type]', c).map(e => ({ e, full: e.dataset.type, a: e.dataset.a ? +e.dataset.a : at(e) + 0.06, d: +(e.dataset.d || 0.6) }));
  c._car = $('.caret', c);
}
function animCard(c, u) {   // u = seconds since the card's moment
  const k = c._spd;
  c._xa.forEach((e, j) => { const a = 0.05 + j * c._stg; S(e, { y: 16 * (1 - P(u, a, a + 0.5 * k, Ez.expo)), o: P(u, a, a + 0.2 * k, Ez.lin) }); });
  c._bars.forEach(o => st(o.e, 'transform', `scaleX(${(o.v * P(u, o.a, o.a + 0.65 * k, Ez.expo)).toFixed(4)})`));
  c._nums.forEach(o => { const v = mix(o.from, o.to, P(u, o.a, o.a + 0.7 * k, Ez.out4)); txt(o.e, o.pre + (o.comma ? Math.round(v).toLocaleString('en-US') : v.toFixed(o.dec)) + o.suf); });
  c._rings.forEach(o => st(o.e, 'strokeDashoffset', (o.L * (1 - o.p * P(u, o.a, o.a + 0.8 * k, Ez.out4))).toFixed(2)));
  c._types.forEach(o => txt(o.e, typed(o.full, u, o.a, o.a + o.d)));
  if (c._car) { const y = c._types[0], on = u > 0 && (u < (y ? y.a + y.d + 0.1 : 0) || (u * 2.2) % 1 < 0.6); st(c._car, 'opacity', on ? '1' : '0'); }
}
const clock = m => { m = Math.round(m) % 1440; const h = Math.floor(m / 60); return `${((h + 11) % 12) + 1}:${String(m % 60).padStart(2, '0')} ${h < 12 ? 'AM' : 'PM'}`; };

/* ===================== scenes: one renderer per scene, gated by time ===================== */
const M = {};
const aW = splitWords($('#aT')), cW = splitWords($('#cT')), eLetW = splitWords($('#eLet'));
const FH = $$('#sB .ft').map(f => ({ h: splitWords($('.h2', f)), p: splitWords($('p', f)) }));
function rA(t) {
  if (!show(M.sA, t < b(4))) return;
  rise(M.aEb, t, b(0.2), b(3.3), 14); wordsAt(aW, t, stag(aW, b(0.5)), b(3.3));
  S(M.aChip, { s: mix(0.6, 1, P(t, b(1.5), b(1.5) + 0.35, Ez.back)), o: P(t, b(1.5), b(1.6), Ez.lin) * (1 - P(t, b(3.3), b(3.6), Ez.in)) });
}
function rB(t) {
  if (!show(M.sB, t >= b(4) && t < b(28))) return;
  M.fts.forEach((f, i) => {
    const a = FT[i], z = a + SLOT;
    if (!show(f, t >= a - 0.05 && t < z)) return;
    rise(f._idx, t, a, z - 0.3, 12); S(f._new, { s: mix(0.6, 1, P(t, a + 0.1, a + 0.45, Ez.back)), o: P(t, a + 0.1, a + 0.18, Ez.lin) * (1 - P(t, z - 0.3, z - 0.05, Ez.in)) });
    wordsAt(FH[i].h, t, stag(FH[i].h, a + 0.15), z - 0.32); wordsAt(FH[i].p, t, stag(FH[i].p, a + 0.45, 0.025), z - 0.32);
    const k = P(t, a + 0.1, a + 0.6, Ez.expo), ko = P(t, z - 0.3, z - 0.02, Ez.in);
    S(f._dc, { x: 120 * (1 - k) - 120 * ko, o: P(t, a + 0.1, a + 0.3, Ez.lin) * (1 - ko) });
    DEMO[i](t - a);
  });
}
const DEMO = [
  u => {   // dark mode: the toggle slides and the whole card re-themes
    const k = P(u, 1.4, 1.9, Ez.q5);
    S(M.tgDot, { x: 44 * k }); st(M.tg, 'background', mixC('#d4d4d8', '#4cc2ff', k));
    st(M.d0, 'background', mixC('#ffffff', '#0f141a', k)); st(M.d0, 'color', mixC('#111111', '#e6edf3', k));
    M.d0Lines.forEach(e => st(e, 'background', mixC('#e5e7eb', '#232b36', k))); M.d0Rows.forEach(e => st(e, 'borderColor', mixC('#e5e7eb', '#232b36', k)));
    txt(M.thName, k > 0.5 ? 'Dark' : 'Light');
  },
  u => {   // instant search: type, results appear as you type, then the timing
    txt(M.sfTx, typed('pricing', u, 0.9, 1.6)); show(M.sfPh, u < 0.9);
    st(M.sfCar, 'opacity', u > 0.6 && (u < 1.6 || (u * 2.2) % 1 < 0.6) ? '1' : '0');
    M.res.forEach((e, j) => S(e, { y: 14 * (1 - P(u, 1.2 + j * 0.08, 1.6 + j * 0.08, Ez.expo)), o: P(u, 1.2 + j * 0.08, 1.35 + j * 0.08, Ez.lin) }));
    S(M.stat, { y: 10 * (1 - P(u, 2.2, 2.6, Ez.expo)), o: P(u, 2.2, 2.35, Ez.lin) });
  },
  u => {   // bulk edit: select on the beat, the action bar slides up, every row changes at once
    M.cbs.forEach((e, j) => st(e, 'transform', `scale(${P(u, 0.9 + j * BEAT / 2, 0.9 + j * BEAT / 2 + 0.25, Ez.back).toFixed(4)})`));
    const kb = P(u, 2.0, 2.4, Ez.expo); S(M.bulk, { y: 30 * (1 - kb), o: P(u, 2.0, 2.15, Ez.lin) });
    const done = u >= 3.0; M.sts.forEach((e, j) => { if (j < 3) { cls(e, 'dn', done); txt(e, done ? 'Done' : 'In review'); S(e, { s: done ? 1 + 0.15 * (1 - P(u, 3.0, 3.3, Ez.out)) : 1 }); } });
  },
];
function rC(t) {
  if (!show(M.sC, t >= b(28) && t < b(32))) return;
  wordsAt(cW, t, stag(cW, b(28)), b(31.6));
  S(M.logIn, { y: -70 * 3 * P(t, b(29.6), b(31.8), x => x), o: P(t, b(28.4), b(28.8), Ez.lin) * (1 - P(t, b(31.6), b(32), Ez.lin)) });   // the changelog rolls past
}
function rD(t) {
  if (!show(M.sD, t >= b(32))) return;
  S(M.eIn, { s: 1 + 0.02 * P(t, b(32), DUR, Ez.lin) });
  wy(M.eMarkS, (1 - P(t, b(32), b(32) + 0.5, Ez.expo)) * 106); wy(M.eWord, (1 - P(t, b(32.25), b(32.25) + 0.5, Ez.expo)) * 125);
  wordsAt(eLetW, t, stag(eLetW, b(33), 0.06)); rise(M.eCtaW, t, b(33.7), null, 24, 0.6);
}
function render(t) { rA(t); rB(t); rC(t); rD(t); }
function measure() {
  $$('#stage [style*="display: none"]').forEach(e => { e.style.display = ''; e._display = undefined; });
  const g = id => document.getElementById(id);
  Object.assign(M, { sA: g('sA'), aEb: g('aEb'), aChip: g('aChip'), sB: g('sB'), fts: $$('#sB .ft'), d0: g('d0'), tg: g('tg'), tgDot: $('#tg i'), thName: g('thName'), d0Lines: $$('#d0 .lines div'), d0Rows: $$('#d0 .row'),
    sfTx: g('sfTx'), sfPh: g('sfPh'), sfCar: g('sfCar'), res: $$('#d1 .res'), stat: g('stat'), cbs: $$('#d2 .cb b'), bulk: g('bulk'), sts: $$('#d2 .st'),
    sC: g('sC'), logIn: g('logIn'), sD: g('sD'), eIn: g('eIn'), eLock: g('eLock'), eMarkS: $('#eMark svg'), eWord: g('eWord'), eLet: g('eLet'), eCtaW: g('eCtaW') });
  M.fts.forEach(f => { f._idx = $('.idx', f); f._new = $('.new', f); f._dc = $('.dc', f); });
  const el = M.eLock.offsetHeight, et = M.eLet.offsetHeight, e0 = SH / 2 - (el + 50 + et + 44 + 84) / 2;
  M.eLock.style.top = Math.round(e0) + 'px'; M.eLet.style.top = Math.round(e0 + el + 50) + 'px'; M.eCtaW.style.top = Math.round(e0 + el + 50 + et + 44) + 'px';
}

/* ===================== score: Web Audio, scheduled on the film clock ===================== */
const AU = (() => {
  let ctx = null, OFF = false, comp, noiseBuf, irBuf, bus = null, a0 = 0, tFrom = 0, cursor = 0;
  const EV = [], KICKS = [];
  const one = (t, fn) => EV.push({ t, fn }), sus = (t, dur, fn) => EV.push({ t, dur, fn });   // sus: fn(w, B, offset, remaining)
  const W = te => a0 + (te - tFrom);   // film time → audio-clock time
  function setup() {
    comp = ctx.createDynamicsCompressor();
    comp.threshold.value = -18; comp.knee.value = 8; comp.ratio.value = 4; comp.attack.value = 0.003; comp.release.value = 0.18;
    const out = ctx.createGain(); out.gain.value = MIX.master; comp.connect(out).connect(ctx.destination);
    let s = 1234567; const rnd = () => (s = (Math.imul(s, 1103515245) + 12345) >>> 0) / 2147483648 - 1;
    noiseBuf = ctx.createBuffer(1, ctx.sampleRate * 2, ctx.sampleRate); const nd = noiseBuf.getChannelData(0); for (let i = 0; i < nd.length; i++) nd[i] = rnd();
    const len = Math.floor(ctx.sampleRate * 2.4); irBuf = ctx.createBuffer(2, len, ctx.sampleRate);
    for (let c = 0; c < 2; c++) { const d = irBuf.getChannelData(c); for (let i = 0; i < len; i++) d[i] = rnd() * (1 - i / len) ** 3.2; }
  }
  function init() { if (ctx) return true; try { ctx = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { return false; } setup(); return true; }
  function newBus() {
    const B = { nodes: [], out: ctx.createGain(), dry: ctx.createGain(), send: ctx.createGain(), conv: ctx.createConvolver() };
    B.out.connect(comp); B.dry.connect(B.out); B.conv.buffer = irBuf;
    const wet = ctx.createGain(); wet.gain.value = MIX.reverb; B.send.connect(B.conv).connect(wet).connect(B.out);
    if (DUCK.length) duckBus(B);   // under a voiceover, the whole score dips while someone speaks
    return B;
  }
  function duckBus(B) { for (const [s, e] of DUCK) { const a = W(s), z = W(e); if (z < ctx.currentTime) continue; B.out.gain.setValueAtTime(1, Math.max(ctx.currentTime, a - 0.25)); B.out.gain.linearRampToValueAtTime(MIX.underVO, Math.max(ctx.currentTime + 0.01, a)); B.out.gain.setValueAtTime(MIX.underVO, Math.max(ctx.currentTime + 0.02, z)); B.out.gain.linearRampToValueAtTime(1, Math.max(ctx.currentTime + 0.03, z + 0.4)); } }
  function start(from) {
    if (!OFF) { if (!init()) return; if (ctx.state === 'suspended') ctx.resume(); }
    stop(); a0 = ctx.currentTime + 0.05; tFrom = from; bus = newBus();   // 50 ms lead-in (subtract it when analysing)
    for (const e of EV) if (e.dur && e.t < from && e.t + e.dur > from) e.fn(a0, bus, from - e.t, e.t + e.dur - from);
    cursor = 0; while (cursor < EV.length && EV[cursor].t < from) cursor++;
    pump(from);
  }
  function pump(t) {   // schedule ~0.3 s ahead; called every frame while playing
    if (!bus) return;
    while (cursor < EV.length && EV[cursor].t < t + 0.3) {
      const e = EV[cursor++], w = W(e.t);
      if (e.dur) e.fn(Math.max(w, ctx.currentTime), bus, 0, e.dur); else if (w > ctx.currentTime - 0.03) e.fn(w, bus);
    }
  }
  function stop(soft) {
    if (!bus) return; const B = bus; bus = null; const now = ctx.currentTime;
    B.out.gain.cancelScheduledValues(now); B.out.gain.setValueAtTime(B.out.gain.value, now); B.out.gain.linearRampToValueAtTime(0.0001, now + (soft ? 2 : 0.06));
    setTimeout(() => { B.nodes.forEach(n => { try { n.stop(); } catch (e) {} }); B.out.disconnect(); }, soft ? 2200 : 150);
  }
  /* ---- instruments: levels are a balanced starting mix ---- */
  const go = (B, ...n) => B.nodes.push(...n);
  const dest = (B, p) => { if (!p) return B.dry; const n = ctx.createStereoPanner(); n.pan.value = clamp(p, -1, 1); n.connect(B.dry); return n; };   // pan -1 (left) … 1 (right); 0 = centre, no node
  const hum = (i, amt = 0.14) => 1 - amt / 2 + amt * hash01(i, 77);   // deterministic velocity variation: hat(w, B, 0.08 * hum(i)) sounds played, not pasted
  const envG = (w, a, peak, d) => { const g = ctx.createGain(); g.gain.value = 0.0001; g.gain.setValueAtTime(0.0001, w); g.gain.exponentialRampToValueAtTime(Math.max(peak, 0.0002), w + a); g.gain.exponentialRampToValueAtTime(0.0001, w + a + d); return g; };   // starts silent: a new gain is 1 until its first event, which would let one sample click
  function noise(w, B, { f = 2000, type = 'bandpass', q = 1, v = 0.1, a = 0.002, d = 0.1, send = 0, pan = 0 } = {}) {
    const s = ctx.createBufferSource(); s.buffer = noiseBuf;
    const fl = ctx.createBiquadFilter(); fl.type = type; fl.frequency.value = f; fl.Q.value = q;
    const g = envG(w, a, v, d); s.connect(fl).connect(g).connect(dest(B, pan));
    if (send) { const sg = ctx.createGain(); sg.gain.value = send; g.connect(sg).connect(B.send); }
    s.start(w, (w * 7.31) % Math.max(0.05, 1.95 - a - d)); s.stop(w + a + d + 0.05); go(B, s);
  }
  function tone(w, B, { f = 880, f2 = 0, type = 'sine', v = 0.08, a = 0.004, d = 0.3, send = 0, pan = 0 } = {}) {
    const o = ctx.createOscillator(); o.type = type; o.frequency.setValueAtTime(f, w); if (f2) o.frequency.exponentialRampToValueAtTime(f2, w + a + d * 0.5);
    const g = envG(w, a, v, d); o.connect(g).connect(dest(B, pan));
    if (send) { const sg = ctx.createGain(); sg.gain.value = send; g.connect(sg).connect(B.send); }
    o.start(w); o.stop(w + a + d + 0.05); go(B, o);
  }
  function kick(w, B, v = 0.34) {
    v *= MIX.drums; const o = ctx.createOscillator(); o.frequency.setValueAtTime(165, w); o.frequency.exponentialRampToValueAtTime(48, w + 0.085);
    const g = ctx.createGain(); g.gain.value = 0.0001; g.gain.setValueAtTime(0.0001, w); g.gain.exponentialRampToValueAtTime(v, w + 0.003); g.gain.exponentialRampToValueAtTime(v * 0.5, w + 0.11); g.gain.exponentialRampToValueAtTime(0.0001, w + 0.36);
    o.connect(g).connect(B.dry); o.start(w); o.stop(w + 0.4); go(B, o);
    noise(w, B, { type: 'highpass', f: 3200, v: 0.09 * MIX.drums, d: 0.012 });   // the click is what small speakers hear
  }
  const clap = (w, B, v = 0.2) => { v *= MIX.drums; [0, 0.009, 0.019].forEach(o => noise(w + o, B, { f: 1250, q: 0.9, v, d: 0.016 })); noise(w + 0.028, B, { f: 1150, q: 0.7, v: v * 0.75, d: 0.13, send: 0.45 }); };
  const snare = (w, B, v = 0.15) => { v *= MIX.drums; noise(w, B, { f: 1800, q: 0.6, v, d: 0.15, send: 0.35 }); tone(w, B, { f: 196, f2: 150, v: v * 0.6, d: 0.08 }); };
  const hat = (w, B, v = 0.09, pan = 0.18) => noise(w, B, { type: 'highpass', f: 7500, v: v * MIX.drums, d: 0.03, pan });
  const shaker = (w, B, v = 0.05, pan = -0.3) => noise(w, B, { f: 6400, q: 1.1, v: v * MIX.drums, a: 0.01, d: 0.045, pan });
  const crash = (w, B, v = 0.06, d = 1.8) => noise(w, B, { type: 'highpass', f: 5200, v, d, send: 0.45 });
  const click = (w, B, v = 0.12) => { noise(w, B, { f: 3400, q: 2.2, v, d: 0.018 }); tone(w, B, { f: 2300, f2: 1500, v: v * 0.3, d: 0.03 }); };   // UI click
  const tick = (w, B, i = 0, v = 0.05) => noise(w, B, { f: 3800 + hash01(i, 9) * 1600, q: 1.6, v, d: 0.012 });                          // typing / counter
  const pop = (w, B, v = 0.08) => tone(w, B, { f: 520, f2: 900, v, d: 0.12, send: 0.25 });                                              // a badge or chip appears
  function bass(w, B, f, d = 0.2, v = 0.09) {   // sine + octave triangle: the octave is what laptops can play
    v *= MIX.bass; const o1 = ctx.createOscillator(), o2 = ctx.createOscillator(); o1.frequency.value = f; o2.type = 'triangle'; o2.frequency.value = f * 2;
    const g1 = ctx.createGain(), g2 = ctx.createGain(), g = ctx.createGain(); g1.gain.value = 0.75; g2.gain.value = 0.8; g.gain.value = 0.0001;
    g.gain.setValueAtTime(0.0001, w); g.gain.exponentialRampToValueAtTime(v, w + 0.008); g.gain.setValueAtTime(v, w + d * 0.55); g.gain.exponentialRampToValueAtTime(0.0001, w + d);
    o1.connect(g1).connect(g); o2.connect(g2).connect(g); g.connect(B.dry);
    [o1, o2].forEach(o => { o.start(w); o.stop(w + d + 0.05); }); go(B, o1, o2);
  }
  function fm(w, B, f, ratio, idx0, idx1, idxT, v, d, send, pan = 0) {   // two-operator FM voice
    const c = ctx.createOscillator(), m = ctx.createOscillator(), mg = ctx.createGain();
    c.frequency.value = f; m.frequency.value = f * ratio;
    mg.gain.setValueAtTime(f * idx0, w); mg.gain.exponentialRampToValueAtTime(f * idx1, w + idxT); m.connect(mg).connect(c.frequency);
    const g = envG(w, 0.004, v, d); c.connect(g).connect(dest(B, pan));
    const s = ctx.createGain(); s.gain.value = send; g.connect(s).connect(B.send);
    [c, m].forEach(o => { o.start(w); o.stop(w + d + 0.05); }); go(B, c, m);
  }
  const ep = (w, B, f, v = 0.1, d = 1.6, pan = 0) => fm(w, B, f, 1, 1.3, 0.1, 0.5, v * MIX.keys, d, 0.35, pan);        // electric piano: chords, arps
  const mallet = (w, B, f, v = 0.12, d = 0.6, pan = 0) => fm(w, B, f, 4, 1.8, 0.04, 0.09, v * MIX.keys, d, 0.3, pan);  // checks, pings, sparkles
  const bell = (w, B, f, v = 0.06, d = 1.6, pan = 0) => fm(w, B, f, 3.5, 2.4, 0.2, 0.6, v * MIX.keys, d, 0.5, pan);    // glassy accents for premium/brand
  function duck(g, w, end, depth = 0.45) { for (const k of KICKS) { const a = W(k); if (a < w + 0.01) continue; if (a > end) break; g.gain.setValueAtTime(1, a - 0.006); g.gain.linearRampToValueAtTime(depth, a + 0.01); g.gain.linearRampToValueAtTime(1, a + 0.3); } }
  function pad(w, B, freqs, off, rem, lvl = 0.024, cut = 1800, pumpIt = true) {   // use with sus()
    lvl *= MIX.pads; const end = w + rem, att = off > 0 ? 0.05 : 0.35;
    const fl = ctx.createBiquadFilter(); fl.type = 'lowpass'; fl.frequency.value = cut;
    const g = ctx.createGain(), dg = ctx.createGain(); g.gain.value = 0.0001;
    g.gain.setValueAtTime(0.0001, w); g.gain.linearRampToValueAtTime(1, w + att); g.gain.setValueAtTime(1, Math.max(w + att, end - 0.04)); g.gain.linearRampToValueAtTime(0.0001, end + 0.6);
    fl.connect(g).connect(dg).connect(B.dry); const s = ctx.createGain(); s.gain.value = 0.5; dg.connect(s).connect(B.send);
    if (pumpIt) duck(dg, w, end + 0.6);   // sidechain on its own gain node, never on the envelope
    freqs.forEach(f => [-8, 8].forEach(dt => { const o = ctx.createOscillator(); o.type = 'sawtooth'; o.frequency.value = f; o.detune.value = dt; const og = ctx.createGain(); og.gain.value = lvl; const pn = ctx.createStereoPanner(); pn.pan.value = dt < 0 ? -0.45 : 0.45; o.connect(og).connect(pn).connect(fl); o.start(w); o.stop(end + 0.7); go(B, o); }));
  }
  function swell(w, B, off, rem, v = 0.08, top = 6000) {   // reversed-cymbal riser into a downbeat; use with sus()
    const k0 = off / (off + rem), end = w + rem, v0 = 0.0004;
    const s = ctx.createBufferSource(); s.buffer = noiseBuf; s.loop = true;
    const fl = ctx.createBiquadFilter(); fl.type = 'bandpass'; fl.Q.value = 0.8;
    fl.frequency.setValueAtTime(400 * (top / 400) ** k0, w); fl.frequency.exponentialRampToValueAtTime(top, end);
    const g = ctx.createGain(); g.gain.value = 0.0001; g.gain.setValueAtTime(v0 * (v / v0) ** k0, w); g.gain.exponentialRampToValueAtTime(v, end - 0.01); g.gain.linearRampToValueAtTime(0.0001, end + 0.004);
    s.connect(fl).connect(g).connect(B.dry); s.start(w); s.stop(end + 0.05); go(B, s);
  }
  function whoosh(w, B, d = 0.5, v = 0.12) {
    const s = ctx.createBufferSource(); s.buffer = noiseBuf;
    const fl = ctx.createBiquadFilter(); fl.type = 'bandpass'; fl.Q.value = 0.7; fl.frequency.setValueAtTime(320, w); fl.frequency.exponentialRampToValueAtTime(3200, w + d);
    const g = ctx.createGain(); g.gain.value = 0.0001; g.gain.setValueAtTime(0.0001, w); g.gain.exponentialRampToValueAtTime(v, w + d * 0.7); g.gain.exponentialRampToValueAtTime(0.0001, w + d);
    s.connect(fl).connect(g).connect(B.dry); s.start(w, 0.3); s.stop(w + d + 0.05); go(B, s);
  }
  function impact(w, B, k = 1) { kick(w, B, 0.47 * k); tone(w, B, { f: 64, f2: 40, v: 0.18 * k * MIX.bass, d: 0.85 }); noise(w, B, { type: 'lowpass', f: 1700, v: 0.1 * k, d: 0.45, send: 0.6 }); crash(w, B, 0.085 * k, 1.8); }

  /* ---- harmony + groove helpers (D major; set KEY to transpose the whole score) ---- */
  const KEY = 0;
  const hz = m => 440 * 2 ** ((m + KEY - 69) / 12);
  const range = (a, c, s) => { const r = []; for (let x = a; x < c - 1e-6; x += s) r.push(+x.toFixed(4)); return r; };
  const K = (t, v = 0.34) => { KICKS.push(t); one(t, (w, B) => kick(w, B, v)); };
  const CH = { D: [54, 57, 62, 64], Em: [55, 59, 62, 66], 'F#m': [57, 61, 64, 66], G: [55, 59, 62, 66], A: [52, 57, 61, 64], Bm: [54, 57, 59, 62] };   // voicings (MIDI)
  const ROOT = { D: 38, Em: 40, 'F#m': 42, G: 31, A: 33, Bm: 35 };
  const ARP = { D: [62, 66, 69, 74], Em: [64, 67, 71, 76], 'F#m': [66, 69, 73, 78], G: [62, 67, 71, 74], A: [61, 64, 69, 73], Bm: [62, 66, 71, 74] };
  const PENTA = [74, 76, 78, 81, 83, 86, 88, 90, 93];   // D major pentatonic, D5 → A6: one note per item, rising
  function harmony(PROG) {   // PROG = [[t, 'D'], [t, 'A'], …, [tEnd, null]]: chord changes on the film clock
    const chordAt = t => { let c = null; for (const [s, k] of PROG) if (t + 1e-6 >= s) c = k; return c; };
    const segs = (a, c) => PROG.map(([s, k], i) => [s, PROG[i + 1] ? PROG[i + 1][0] : DUR + 4, k]).filter(([s, e, k]) => k && e > a && s < c).map(([s, e, k]) => [Math.max(s, a), Math.min(e, c), k]);
    return {
      chordAt, segs,
      chords: (a, c, v = 0.1, oct = 0) => segs(a, c).forEach(([s, e, k]) => one(s, (w, B) => CH[k].forEach((m, i) => ep(w + i * 0.007, B, hz(m + oct), v, e - s + 0.35, (i - 1.5) * 0.22)))),
      pads: (a, c, lvl = 0.024, cut = 1800, pumpIt = true) => segs(a, c).forEach(([s, e, k]) => sus(s, e - s, (w, B, off, rem) => pad(w, B, CH[k].map(m => hz(m)), off, rem, lvl, cut, pumpIt))),
      arp: (a, c, step = BEAT / 2, v = 0.05, oct = 12, pat = [0, 1, 2, 3, 2, 1, 2, 3]) => range(a, c, step).forEach((x, i) => { const k = chordAt(x); if (k) one(x, (w, B) => ep(w, B, hz(ARP[k][pat[i % pat.length]] + oct), v * hum(i, 0.2), 0.4, i % 2 ? 0.32 : -0.32)); }),
      groove: (a, c, o = {}) => {   // o: { kick, clap, hat, shaker, bass: false to drop a part; half: true for half-time; kv, cv, hv, bv levels }
        const on = p => o[p] !== false;
        range(a, c, BEAT).forEach(x => {
          const n = Math.round(x / BEAT), k = chordAt(x);
          if (on('kick') && (o.half ? n % 4 === 0 : true)) K(x, o.kv || 0.34);
          if (on('clap') && (o.half ? n % 4 === 2 : n % 2 === 1)) one(x, (w, B) => clap(w, B, o.cv || 0.2));
          if (on('hat')) one(x + BEAT / 2, (w, B) => hat(w, B, (o.hv || 0.09) * hum(n)));
          if (on('bass') && k) one(x + BEAT / 2, (w, B) => bass(w, B, hz(ROOT[k]), BEAT * 0.42, o.bv || 0.09));
        });
        if (on('shaker')) range(a, c, BEAT / 4).forEach((x, i) => one(x, (w, B) => shaker(w, B, (i % 2 ? 0.05 : 0.03) * hum(i))));
      },
    };
  }

  /* ---- the score, written on the same beat grid as the picture ---- */
  const H = harmony([[b(0), 'Bm'], [b(4), 'G'], [b(8), 'D'], [b(12), 'A'], [b(16), 'Bm'], [b(20), 'G'], [b(24), 'D'], [b(28), 'A'], [b(32), 'D'], [DUR + 9, null]]);
  // tech groove: tight kit, a sixteenth arp, a bleep and a hit on every feature
  one(b(0), (w, B) => { CH.Bm.forEach((m, i) => ep(w + i * 0.007, B, hz(m), 0.08, 2)); }); one(b(1.5), (w, B) => pop(w, B, 0.09));
  sus(b(3), b(1), (w, B, off, rem) => swell(w, B, off, rem, 0.07, 7000));
  one(b(4), (w, B) => impact(w, B, 0.6)); KICKS.push(b(4));
  H.groove(b(5), b(28)); H.chords(b(4), b(28), 0.075); H.arp(b(4), b(28), BEAT / 4, 0.035, 12, [0, 2, 1, 3, 2, 1, 3, 2]); H.pads(b(4), b(28), 0.016, 1600);
  FT.forEach((x, i) => { one(x - 0.2, (w, B) => whoosh(w, B, 0.22, 0.07)); one(x + 0.1, (w, B) => { pop(w, B, 0.09); mallet(w, B, hz(PENTA[i * 2 + 3]), 0.11); }); });
  one(FT[0] + 1.4, (w, B) => click(w, B));                                                             // the toggle
  range(FT[1] + 0.9, FT[1] + 1.6, 0.1).forEach((x, i) => one(x, (w, B) => tick(w, B, i, 0.05)));      // typing
  [0, 1, 2].forEach(j => one(FT[2] + 0.9 + j * BEAT / 2, (w, B) => click(w, B, 0.09)));               // selections
  one(FT[2] + 3.0, (w, B) => [81, 86].forEach((m, i) => mallet(w + i * 0.07, B, hz(m), 0.1)));        // all done at once
  range(b(29.6), b(31.8), BEAT / 2).forEach((x, i) => one(x, (w, B) => tick(w, B, i + 50, 0.04)));    // the changelog rolling
  one(b(32), (w, B) => { impact(w, B, 0.5); CH.D.forEach((m, i) => ep(w + i * 0.007, B, hz(m), 0.1, 2.6)); });
  sus(b(32), b(4), (w, B, off, rem) => pad(w, B, CH.D.map(hz), off, rem, 0.018, 1500, false));

  KICKS.sort((x, y) => x - y); EV.sort((x, y) => x.t - y.t);

  /* ---- offline render: the whole score as a WAV Blob (analysis, MP4 muxing). Use in a fresh ?record page ---- */
  function wavBlob(buf, mono) {
    const ch = mono ? 1 : 2, n = buf.length, sr = buf.sampleRate, dv = new DataView(new ArrayBuffer(44 + n * ch * 2));
    const ws = (o, s) => { for (let i = 0; i < s.length; i++) dv.setUint8(o + i, s.charCodeAt(i)); };
    ws(0, 'RIFF'); dv.setUint32(4, 36 + n * ch * 2, true); ws(8, 'WAVE'); ws(12, 'fmt '); dv.setUint32(16, 16, true); dv.setUint16(20, 1, true); dv.setUint16(22, ch, true);
    dv.setUint32(24, sr, true); dv.setUint32(28, sr * ch * 2, true); dv.setUint16(32, ch * 2, true); dv.setUint16(34, 16, true); ws(36, 'data'); dv.setUint32(40, n * ch * 2, true);
    const L = buf.getChannelData(0), R = buf.numberOfChannels > 1 ? buf.getChannelData(1) : L, q = v => Math.max(-1, Math.min(1, v)) * 32767;
    for (let i = 0, o = 44; i < n; i++) { if (mono) { dv.setInt16(o, q((L[i] + R[i]) / 2), true); o += 2; } else { dv.setInt16(o, q(L[i]), true); dv.setInt16(o + 2, q(R[i]), true); o += 4; } }
    return new Blob([dv], { type: 'audio/wav' });
  }
  async function renderWav({ rate = 48000, mono = false } = {}) {
    OFF = true; ctx = new OfflineAudioContext(2, Math.ceil(rate * (DUR + 2)), rate); setup(); start(0); pump(DUR + 2);
    return wavBlob(await ctx.startRendering(), mono);
  }
  return { init, start, pump, stop, renderWav };
})();

/* optional voiceover: add an audio element with id="vo" and src="vo.mp3" to the body (inline.py embeds it as a data: URI) */
const VOX = (() => {
  const el = $('#vo'); if (!el || REC) return { start() {}, pump() {}, stop() {} };
  return { start(t) { try { el.currentTime = t; } catch (e) {} el.play().catch(() => {}); }, pump(t) { if (!el.paused && Math.abs(el.currentTime - t) > 0.25) el.currentTime = t; }, stop() { el.pause(); } };
})();

/* ===================== player ===================== */
const stage = $('#stage');
stage.style.width = SW + 'px'; stage.style.height = SH + 'px';
let cur = 0, playing = false, perf0 = 0, cur0 = 0, started = false, sound = !Q.has('mute'), lastMove = 0;
const SND = { start: t => { if (sound) { AU.start(t); VOX.start(t); } }, pump: t => { if (sound) { AU.pump(t); VOX.pump(t); } }, stop: s => { AU.stop(s); VOX.stop(); } };
const fit = () => { const s = Math.min(innerWidth / SW, innerHeight / SH); stage.style.transform = `translate(${((innerWidth - SW * s) / 2).toFixed(2)}px,${((innerHeight - SH * s) / 2).toFixed(2)}px) scale(${s})`; };
addEventListener('resize', fit); fit();
function play() { if (cur >= DUR - 0.05) cur = 0; playing = true; perf0 = performance.now(); cur0 = cur; SND.start(cur); }
function pause() { playing = false; SND.stop(); }
function seekTo(t) { cur = clamp(t, 0, DUR); render(cur); if (playing) { perf0 = performance.now(); cur0 = cur; SND.stop(); SND.start(cur); } }
function frame(now) {
  if (playing) { cur = cur0 + (now - perf0) / 1000; if (cur >= DUR) { cur = DUR; playing = false; SND.stop(true); if (Q.has('loop')) setTimeout(() => { cur = 0; render(0); play(); }, 600); } render(cur); if (playing) SND.pump(cur); }
  if (!REC) { $('#barFill').style.width = (cur / DUR * 100).toFixed(3) + '%'; document.body.classList.toggle('idle', playing && now - lastMove > 2200); }
  requestAnimationFrame(frame);
}
function bindUI() {
  const begin = () => { if (started) return; started = true; document.body.classList.add('started'); $('#start').classList.add('gone'); AU.init(); cur = Q.has('t') ? cur : 0; render(cur); play(); };
  $('#start').addEventListener('click', begin);
  stage.addEventListener('click', () => { if (started) playing ? pause() : play(); });
  $('#bar').addEventListener('pointerdown', e => { const r = $('#bar div').getBoundingClientRect(); seekTo(clamp((e.clientX - r.left) / r.width) * DUR); });
  addEventListener('mousemove', () => { lastMove = performance.now(); });
  addEventListener('keydown', e => {
    const k = e.key.toLowerCase();
    if (k === ' ' || k === 'k') { e.preventDefault(); if (!started) begin(); else playing ? pause() : play(); }
    else if (k === 'arrowright') seekTo(cur + (e.shiftKey ? 5 : 1)); else if (k === 'arrowleft') seekTo(cur - (e.shiftKey ? 5 : 1));
    else if (k === 'm') { sound = !sound; if (!sound) SND.stop(); else if (playing) SND.start(cur); }
    else if (k === 'h') { const u = $('#ui'); u.style.visibility = u.style.visibility === 'hidden' ? '' : 'hidden'; }
    else if (k === 'f') document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen();
  });
  document.addEventListener('visibilitychange', () => { if (document.hidden && playing) pause(); });
  if (Q.has('autoplay')) begin();
}
window.duration = DUR; window.stageSize = [SW, SH]; window.poster = POSTER;   // read by verify.py (stage size, thumbnail frame)
window.seek = t => { cur = clamp(+t || 0, 0, DUR); render(cur); return cur; };
window.renderWav = o => AU.renderWav(o);

/* ===================== boot ===================== */
const fontsReady = Promise.all([...document.fonts].map(f => f.load().catch(() => {}))).then(() => document.fonts.ready);   // every embedded face (display, UI, mono, italics) is ready before the first measure()
window.videoReady = fontsReady.then(() => {
  measure();
  cur = Q.has('t') ? clamp(+Q.get('t') || 0, 0, DUR) : REC ? 0 : POSTER;
  render(cur);
  document.body.classList.add('ready'); if (REC) document.body.classList.add('rec'); else bindUI();
  requestAnimationFrame(frame);
  document.fonts.addEventListener('loadingdone', () => { measure(); render(cur); });
  return true;
});
})();
</script>
</body>
</html>
````

### `verify.py`: sweep, checks, frames, contact sheets, WAV, MP4

<!-- file: verify.py -->
````python
#!/usr/bin/env python3
"""Verify, render and export a motion film in headless Chrome (via the DevTools Protocol).

Every run (except `start`) first sweeps the whole timeline (seek every 0.05 s) and reports any exception
thrown inside seek()/render(), plus page errors, then checks that every font the film uses is embedded.

  python verify.py film.html check                      sweep + fonts + a frame every 0.1 s scanned for blank frames and static holds
  python verify.py film.html sweep                      only the sweep and the font check
  python verify.py film.html frames 0 60 0.5            PNG frames + 3-column contact sheets (12 frames per sheet)
  python verify.py film.html at 3.2 7.95 12             frames at exact times (+ a sheet)
  python verify.py film.html start                      the player's start screen (poster frame + overlay), not ?record
  python verify.py film.html poster [t]                 poster.jpg at window.poster (or t): the thumbnail for the MP4 and README
  python verify.py film.html wav [rate]                 offline render of the score → score.wav (default 48000 Hz)
  python verify.py film.html export [fps]               every frame as PNG → frames/f_00000.png … (for your own ffmpeg)
  python verify.py film.html eval "js" [t]               evaluate an expression in the ?record page (after seek(t)) and print the JSON result,
                                                        e.g. eval "getComputedStyle(document.querySelector('#cT')).fontSize" 9.5
  python verify.py film.html mp4 [fps]                  the finished MP4 in one step: score + frames piped to ffmpeg,
                                                        loudness-normalised, H.264, +faststart (default 30 fps)

Options:
  --out DIR        output folder (default ./verify_out)
  --size WxH       stage size; by default it is read from the film (window.stageSize, else #stage)
  --scale N        device pixel ratio for frames/mp4/poster (2 → 3840×2160 from a 1920×1080 stage)
  --mp4 PATH       where `mp4` writes (default: next to the film, same name, .mp4)
  --vo FILE        a voiceover (mp3/wav) to mix with the score in `mp4`; it starts at film time 0
  --audio MODE     score (default) | vo (voiceover only) | none (silent MP4)
  --crf N          H.264 quality for `mp4` (default 18; lower is better and bigger)
  --lufs N         loudness target for `mp4` (default -14, right for web, YouTube and social)
Needs:  pip install websocket-client pillow numpy · Chrome, Chromium or Edge (set CHROME=/path if not found) · ffmpeg for `mp4`

Warnings this script prints are the usual tells of an unfinished film. Treat each one as a bug unless it is deliberate:
  fonts not embedded    the film renders in a fallback font on any machine without that font installed
  blank frames          a frame that is one flat colour (an empty first frame makes a blank thumbnail)
  static holds          nothing on screen changes for 3 s or more (keep holds alive with a slow push)
"""
import argparse, base64, io, json, os, pathlib, shutil, socket, subprocess, sys, tempfile, time, urllib.request

try:
    import websocket
    from PIL import Image, ImageDraw, ImageStat
except ImportError:
    sys.exit('pip install websocket-client pillow numpy')


def find_chrome():
    cands = [os.environ.get('CHROME'), shutil.which('google-chrome'), shutil.which('google-chrome-stable'), shutil.which('chromium'),
             shutil.which('chromium-browser'), shutil.which('chrome'), shutil.which('msedge'),
             r'C:\Program Files\Google\Chrome\Application\chrome.exe', r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
             r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
             '/Applications/Chromium.app/Contents/MacOS/Chromium', '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge']
    for c in cands:
        if c and os.path.exists(c):
            return c
    sys.exit('Chrome not found: set CHROME=/path/to/chrome')


def free_port():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close(); return p


ap = argparse.ArgumentParser(description='Verify and export a motion film.')
ap.add_argument('film'); ap.add_argument('cmd', choices=['check', 'sweep', 'frames', 'at', 'start', 'poster', 'wav', 'export', 'mp4', 'eval']); ap.add_argument('args', nargs='*')
ap.add_argument('--out', default='verify_out'); ap.add_argument('--size'); ap.add_argument('--scale', type=float, default=1); ap.add_argument('--port', type=int, default=0)
ap.add_argument('--mp4'); ap.add_argument('--vo'); ap.add_argument('--audio', choices=['score', 'vo', 'none'], default='score')
ap.add_argument('--crf', type=int, default=18); ap.add_argument('--lufs', type=float, default=-14)
A = ap.parse_args()
film = pathlib.Path(A.film).resolve(); out = pathlib.Path(A.out); out.mkdir(parents=True, exist_ok=True)
if not film.exists():
    sys.exit(f'no such film: {film}')
if A.cmd == 'mp4' and not shutil.which('ffmpeg'):
    sys.exit('ffmpeg not found: install it (brew install ffmpeg · apt install ffmpeg · winget install ffmpeg)')
if A.audio == 'vo' and not A.vo:
    sys.exit('--audio vo needs --vo FILE')
port = A.port or free_port()
proc = subprocess.Popen([find_chrome(), '--headless=new', '--disable-gpu', '--hide-scrollbars', '--mute-audio', '--force-color-profile=srgb',
                         f'--remote-debugging-port={port}', '--remote-allow-origins=*', f'--user-data-dir={tempfile.mkdtemp(prefix="vf_")}',
                         '--window-size=1920,1080', 'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
errors, warnings, mid, ws = [], [], [0], None
W, H = 1920, 1080


def call(method, params=None):
    mid[0] += 1; ws.send(json.dumps({'id': mid[0], 'method': method, 'params': params or {}}))
    while True:
        m = json.loads(ws.recv())
        if m.get('method') == 'Runtime.exceptionThrown':
            d = m['params']['exceptionDetails']; errors.append('page: ' + d.get('exception', {}).get('description', d.get('text', '?'))[:300])
        elif m.get('method') == 'Runtime.consoleAPICalled' and m['params'].get('type') == 'error':
            errors.append('console.error: ' + ' '.join(str(a.get('value', a.get('description', ''))) for a in m['params'].get('args', []))[:300])
        if m.get('id') == mid[0]:
            if 'error' in m:
                errors.append(f'{method}: ' + m['error'].get('message', '?'))
            return m.get('result', {})


def js(expr, wait=True):
    """Evaluate in the page. Exceptions thrown by seek()/render() land HERE, not in page error events."""
    r = call('Runtime.evaluate', {'expression': expr, 'awaitPromise': wait, 'returnByValue': True})
    if 'exceptionDetails' in r:
        errors.append('eval: ' + r['exceptionDetails'].get('exception', {}).get('description', '?')[:300])
    return r.get('result', {}).get('value')


def metrics(w, h, scale=1):
    call('Emulation.setDeviceMetricsOverride', {'width': w, 'height': h, 'deviceScaleFactor': scale, 'mobile': False})


def load(record=True):
    call('Page.navigate', {'url': film.as_uri() + ('?record' if record else '')})
    time.sleep(0.2)
    for i in range(400):
        if js("!!(window.videoReady && document.body && document.body.classList.contains('ready'))", False):
            js('window.videoReady'); return
        if i > 12 and any(e.startswith('page:') for e in errors):   # a script error during load: the film will never become ready
            sys.exit('the film threw while loading:\n  ' + '\n  '.join(errors))
        time.sleep(0.15)
    sys.exit('film never became ready (window.videoReady / body.ready): check page errors ' + str(errors))


def settle():
    js('new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))')


def shot(fmt='png', q=None):
    p = {'format': fmt}
    if q:
        p['quality'] = q
    return base64.b64decode(call('Page.captureScreenshot', p)['data'])


def frame(t):
    js(f'window.seek({t})'); settle()
    return Image.open(io.BytesIO(shot())).convert('RGB')


def flat(im):
    """A frame that is (almost) one flat colour: no content to look at."""
    st = ImageStat.Stat(im.convert('L').resize((192, 108)))
    return st.stddev[0] < 1.2


def report_flat(ts, step=0.5):
    if not ts:
        return
    runs, a, prev = [], ts[0], ts[0]
    for t in ts[1:] + [None]:
        if t is None or t - prev > step * 1.05:   # flagged frames one scan step apart form one run
            runs.append((a, prev)); a = t
        if t is not None:
            prev = t
    desc = ', '.join(f'{x:.2f} s' if x == y else f'{x:.2f}–{y:.2f} s' for x, y in runs)
    warnings.append(f'blank frames (one flat colour) at {desc}' + ('  ← the FIRST frame is blank: the thumbnail will be empty' if ts[0] == 0 else ''))


def report_static(items, step):
    if step > 0.5 or len(items) < 3:
        return
    import numpy as np
    run0, last = None, None
    for t, im in items:
        a = np.asarray(im.convert('L').resize((192, 108)), dtype=np.float32)
        if last is not None and np.abs(a - last).mean() < 0.06:
            run0 = t - step if run0 is None else run0
        else:
            if run0 is not None and t - step - run0 >= 3:
                warnings.append(f'static hold {run0:.2f}–{t - step:.2f} s: nothing moves (keep holds alive with a 1–3 % push)')
            run0 = None
        last = a
    if run0 is not None and items[-1][0] - run0 >= 3:
        warnings.append(f'static hold {run0:.2f}–{items[-1][0]:.2f} s: nothing moves (fine only for a final end-card hold)')


def sheets(items, tag):
    tw = 640 if W >= H else 300; th = int(tw * H / W)
    for si in range(0, len(items), 12):
        chunk = items[si:si + 12]; rows = (len(chunk) + 2) // 3
        sheet = Image.new('RGB', (3 * (tw + 8) + 8, rows * (th + 26) + 8), (40, 40, 40)); d = ImageDraw.Draw(sheet)
        for k, (t, im) in enumerate(chunk):
            x, y = 8 + k % 3 * (tw + 8), 8 + k // 3 * (th + 26)
            sheet.paste(im.resize((tw, th)), (x, y)); d.text((x + 4, y + th + 6), f't = {t:.2f}', fill='white')
        fn = out / f'sheet_{tag}_{si // 12:02d}.png'; sheet.save(fn); print('sheet', fn)


FONT_CHECK = r"""(() => {
  const norm = s => s.replace(/["']/g, '').trim().toLowerCase();
  const GENERIC = /^(serif|sans-serif|monospace|cursive|fantasy|system-ui|ui-sans-serif|ui-serif|ui-monospace|ui-rounded|-apple-system|blinkmacsystemfont|segoe ui|menlo|consolas|monaco|courier new|georgia|arial|helvetica|helvetica neue|times new roman|arial black|inherit|initial)$/;
  const faces = [...document.fonts];
  const wOk = (f, w) => { const p = String(f.weight).split(/\s+/).map(Number); return p.length > 1 ? w >= p[0] && w <= p[1] : p[0] === w; };
  const need = new Map(), glyphs = new Map();
  const ranges = f => String(f.unicodeRange || 'U+0-10FFFF').split(',').map(r => { r = r.trim().replace(/^u\+/i, '');
    if (r.includes('?')) return [parseInt(r.replace(/\?/g, '0'), 16), parseInt(r.replace(/\?/g, 'F'), 16)];
    const [a, b] = r.split('-'); return [parseInt(a, 16), parseInt(b || a, 16)]; });
  const stage = document.getElementById('stage') || document.body;
  for (const e of stage.querySelectorAll('*')) {
    const own = [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('') + (e.dataset ? e.dataset.type || '' : '');
    if (!own.trim()) continue;   // only elements that render text (data-type: text typed in later)
    const cs = getComputedStyle(e), fam = norm(cs.fontFamily.split(',')[0]);
    if (!fam || GENERIC.test(fam)) continue;
    const fr = faces.filter(f => norm(f.family) === fam).flatMap(ranges);
    if (fr.length) for (const ch of own) { const cp = ch.codePointAt(0); if (cp > 32 && !fr.some(([lo, hi]) => cp >= lo && cp <= hi)) glyphs.set(ch, `${ch} U+${cp.toString(16).toUpperCase().padStart(4, '0')} in ${fam}`); }
    const key = fam + '|' + (+cs.fontWeight) + '|' + (cs.fontStyle === 'italic' ? 'italic' : 'normal');
    if (!need.has(key)) need.set(key, (e.textContent || '').trim().slice(0, 24));
  }
  const missing = [], weights = [];
  for (const [key, sample] of need) {
    const [fam, w, style] = key.split('|');
    const fams = faces.filter(f => norm(f.family) === fam);
    if (!fams.length) { missing.push(fam); continue; }
    if (!fams.some(f => wOk(f, +w) && (f.style === style || (style === 'normal' && f.style !== 'italic')))) weights.push(`${fam} ${w}${style === 'italic' ? ' italic' : ''} ("${sample}")`);
  }
  return { faces: faces.length, missing: [...new Set(missing)], weights: [...new Set(weights)], glyphs: [...glyphs.values()], failed: faces.filter(f => f.status === 'error').map(f => f.family) };
})()"""


def checks(dur):
    bad = js(f"(() => {{ const bad = []; for (let i = 0; i <= {int(dur * 20)}; i++) {{ try {{ window.seek(i / 20); }} catch (e) {{ bad.push((i / 20).toFixed(2) + ' s: ' + e.message); if (bad.length > 12) break; }} }} return bad; }})()", False)
    print(f'timeline sweep (0–{dur:.2f} s every 0.05 s):', 'no exceptions' if not bad else '\n  ' + '\n  '.join(bad))
    if bad:
        errors.append(f'{len(bad)} exception(s) during the sweep')
    fc = js(FONT_CHECK, False) or {}
    if fc.get('missing'):
        warnings.append('fonts not embedded (fallback font on other machines): ' + ', '.join(fc['missing']) + ' → embed them with fonts.py')
    if fc.get('weights'):
        warnings.append('font weights/styles used but not embedded (the browser fakes them): ' + '; '.join(fc['weights'][:8]))
    if fc.get('glyphs'):
        warnings.append('characters outside the embedded font subset (they render in a system font): ' + '; '.join(fc['glyphs'][:10]) + ' → draw them as SVG, or embed a subset that has them (fonts.py --subsets)')
    if fc.get('failed'):
        errors.append('font faces that failed to load: ' + ', '.join(fc['failed']))
    print(f"fonts: {fc.get('faces', 0)} embedded face(s)" + ('' if fc.get('missing') or fc.get('weights') or fc.get('glyphs') else ' · every font, weight and glyph the film uses is embedded'))
    js('window.seek(0)')


def render_wav(rate=48000):
    load(True)
    b64 = js(f"window.renderWav({{ rate: {rate} }}).then(b => b.arrayBuffer()).then(a => {{ const u = new Uint8Array(a); let s = ''; for (let i = 0; i < u.length; i += 32768) s += String.fromCharCode.apply(null, u.subarray(i, i + 32768)); return btoa(s); }})")
    if not b64:
        sys.exit('renderWav() failed: ' + str(errors))
    fn = out / 'score.wav'; fn.write_bytes(base64.b64decode(b64)); print('score', fn, f'({fn.stat().st_size / 1e6:.1f} MB)')
    return fn


try:
    for _ in range(100):
        try:
            tab = next(t for t in json.loads(urllib.request.urlopen(f'http://127.0.0.1:{port}/json', timeout=2).read()) if t['type'] == 'page'); break
        except Exception:
            time.sleep(0.25)
    else:
        sys.exit('could not connect to headless Chrome')
    ws = websocket.create_connection(tab['webSocketDebuggerUrl'], suppress_origin=True, timeout=900)
    call('Runtime.enable'); call('Page.enable')
    metrics(1920, 1080)
    load(A.cmd != 'start')
    dur = float(js('window.duration', False) or 0)
    if A.size:
        W, H = map(int, A.size.lower().split('x'))
    else:
        W, H = js("(() => { if (window.stageSize) return window.stageSize; const s = document.getElementById('stage'); return s ? [s.offsetWidth, s.offsetHeight] : [1920, 1080]; })()", False) or [1920, 1080]
        W, H = int(W), int(H)
    scale = A.scale if A.cmd in ('frames', 'at', 'poster', 'export', 'mp4') else 1
    metrics(W, H, scale); js("dispatchEvent(new Event('resize'))"); settle()
    print(f'{film.name}: {dur:.2f} s · stage {W}×{H}' + (f' · ×{scale:g} → {int(W * scale)}×{int(H * scale)}' if scale != 1 else ''))
    if A.cmd == 'eval':
        if len(A.args) > 1:
            js(f'window.seek({float(A.args[1])})'); settle()
        print(json.dumps(js(A.args[0], True), indent=1, ensure_ascii=False))
    elif A.cmd == 'start':
        time.sleep(1.0); fn = out / 'start.png'; Image.open(io.BytesIO(shot())).save(fn); print('start screen', fn)
    else:
        checks(dur)

    if A.cmd == 'check':
        ts = [round(i * 0.1, 2) for i in range(int(round(dur / 0.1)) + 1)]   # 0.1 s: catches a blank frame right after a cut
        items = [(t, frame(t)) for t in ts]
        report_flat([t for t, im in items if flat(im)], 0.1); report_static(items[::5], 0.5)
        print(f'scanned {len(ts)} frames every 0.1 s for blank frames (static holds judged every 0.5 s)')
    elif A.cmd == 'frames':
        a, c, step = map(float, A.args); ts = [round(a + i * step, 3) for i in range(int(round((c - a) / step)) + 1)]
        items = []
        for t in ts:
            im = frame(t); im.save(out / f'f_{t:07.2f}.png'); items.append((t, im))
        report_flat([t for t, im in items if flat(im)], step); report_static(items, step)
        sheets(items, f'{a:g}-{c:g}')
    elif A.cmd == 'at':
        items = []
        for t in map(float, A.args):
            im = frame(t); im.save(out / f'f_{t:07.2f}.png'); items.append((t, im))
        report_flat([t for t, im in items if flat(im)])
        sheets(items, 'at')
    elif A.cmd == 'poster':
        t = float(A.args[0]) if A.args else (lambda v: float(v) if v is not None else max(0, dur - 1))(js('window.poster', False))
        fn = out / 'poster.jpg'; frame(t).save(fn, quality=92); print(f'poster at {t:.2f} s → {fn}')
    elif A.cmd == 'wav':
        render_wav(int(A.args[0]) if A.args else 48000)
    elif A.cmd == 'export':
        fps = int(A.args[0]) if A.args else 30; fd = out / 'frames'; fd.mkdir(exist_ok=True); n = int(round(dur * fps)); fl = []
        for i in range(n):
            im = frame(i / fps); im.save(fd / f'f_{i:05d}.png')
            if flat(im):
                fl.append(round(i / fps, 2))
            if i % (fps * 5) == 0:
                print(f'  {i}/{n}')
        report_flat(fl, 1 / fps)
        print(f'{n} frames → {fd}')
    elif A.cmd == 'mp4':
        fps = int(A.args[0]) if A.args else 30; n = int(round(dur * fps))
        dst = pathlib.Path(A.mp4).resolve() if A.mp4 else film.with_suffix('.mp4')
        poster_t = (lambda v: float(v) if v is not None else max(0, dur - 1))(js('window.poster', False))
        wav = None
        if A.audio == 'score':
            metrics(W, H, 1); wav = render_wav(48000); load(True); metrics(W, H, scale); js("dispatchEvent(new Event('resize'))"); settle()
        cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(fps), '-c:v', 'png', '-i', '-']
        loud = f'loudnorm=I={A.lufs}:TP=-1.5:LRA=11'
        if A.audio == 'score' and A.vo:
            cmd += ['-i', str(wav), '-i', str(pathlib.Path(A.vo).resolve()), '-filter_complex',
                    f'[1:a]atrim=start=0.05,asetpts=PTS-STARTPTS[m];[2:a]asetpts=PTS-STARTPTS[v];[m][v]amix=inputs=2:normalize=0:duration=first,{loud},aresample=48000[a]',
                    '-map', '0:v', '-map', '[a]']
        elif A.audio == 'score':
            cmd += ['-i', str(wav), '-af', f'atrim=start=0.05,asetpts=PTS-STARTPTS,{loud},aresample=48000', '-map', '0:v', '-map', '1:a']
        elif A.audio == 'vo':
            cmd += ['-i', str(pathlib.Path(A.vo).resolve()), '-af', f'{loud},aresample=48000', '-map', '0:v', '-map', '1:a']
        cmd += ['-c:v', 'libx264', '-preset', 'slow', '-crf', str(A.crf), '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-r', str(fps), '-movflags', '+faststart']
        if A.audio != 'none':
            cmd += ['-c:a', 'aac', '-b:a', '192k', '-t', f'{n / fps:.3f}']
        cmd += [str(dst)]
        ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        fl, t0 = [], time.time()
        for i in range(n):
            js(f'window.seek({i / fps})'); settle(); png = shot()
            ff.stdin.write(png)
            if i % 6 == 0 and flat(Image.open(io.BytesIO(png))):
                fl.append(round(i / fps, 2))
            if i % (fps * 5) == 0:
                print(f'  frame {i}/{n}  ({time.time() - t0:.0f} s)')
        ff.stdin.close(); rc = ff.wait()
        if rc:
            sys.exit(f'ffmpeg failed (exit {rc})')
        report_flat(fl, 6 / fps)
        poster = dst.with_suffix('.jpg'); frame(poster_t).save(poster, quality=92)
        print(f'MP4 → {dst} ({dst.stat().st_size / 1e6:.1f} MB, {n} frames at {fps} fps, {int(W * scale)}×{int(H * scale)})  ·  poster → {poster}')
finally:
    for w_ in warnings:
        print('WARNING:', w_)
    print('errors:', 'none' if not errors else '\n  ' + '\n  '.join(errors))
    if ws:
        ws.close()
    proc.kill()
````

### `analyze.py`: score analysis with a PASS/WARN verdict

<!-- file: analyze.py -->
````python
#!/usr/bin/env python3
"""Measure a film's score (the WAV from `verify.py film.html wav`): loudness, tonal balance, width, timing, clicks.

  python analyze.py score.wav                       whole film in 10 s blocks
  python analyze.py score.wav 0-6 6-8 8-30 30-60    named sections, in film seconds
  options: --bpm 120   --lead 0.05 (the engine's audio lead-in)   --hits 8,30,44 (moments that must carry an onset)
           --silent 6-8 (sections that are meant to be near-silent; checked against -35 dB)

Targets (see the sound section of SKILL.md); the verdict at the end checks each one:
  peak < 0.9, no clipped samples and 0 clicks · music RMS about -22 to -12 dBFS (the MP4 is normalised to -14 LUFS) · intentional silences below -35 dB
  raw energy below 80 Hz under ~45 % · A-weighted: mids (250 Hz–4 kHz) dominate, bass underneath
  air: A-weighted 4–12 kHz at least ~3 % (hats, shakers, bells); below that the score sounds dull and cheap
  width: some stereo (side/mid 0.08–0.6); fully mono sounds small, too wide falls apart on phones
  onsets sit on the 16th-note grid with a small constant offset; every listed hit shows an onset
Needs: pip install numpy
"""
import argparse, wave
import numpy as np

ap = argparse.ArgumentParser(); ap.add_argument('wav'); ap.add_argument('sections', nargs='*')
ap.add_argument('--bpm', type=float, default=120); ap.add_argument('--lead', type=float, default=0.05); ap.add_argument('--hits', default='')
ap.add_argument('--silent', nargs='*', default=[])
A = ap.parse_args()
w = wave.open(A.wav); sr, ch = w.getframerate(), w.getnchannels()
st = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64).reshape(-1, ch) / 32768.0
x = st.mean(1)
dur = len(x) / sr
db = lambda v: 20 * np.log10(v + 1e-9)
verdict = []   # (ok, text)


def aweight(f):
    f2 = f * f
    r = 12194 ** 2 * f2 * f2 / ((f2 + 20.6 ** 2) * np.sqrt((f2 + 107.7 ** 2) * (f2 + 737.9 ** 2)) * (f2 + 12194 ** 2))
    return (r * 1.2589) ** 2


BANDS = [('<80', 20, 80), ('80-250', 80, 250), ('250-1k', 250, 1000), ('1-4k', 1000, 4000), ('4-12k', 4000, min(12000, sr / 2 - 1))]


def spectrum(s):
    sp = np.abs(np.fft.rfft(s * np.hanning(len(s)))) ** 2; f = np.fft.rfftfreq(len(s), 1 / sr)
    raw = np.array([sp[(f >= lo) & (f < hi)].sum() for _, lo, hi in BANDS]); spa = sp * aweight(np.maximum(f, 1))
    per = np.array([spa[(f >= lo) & (f < hi)].sum() for _, lo, hi in BANDS])
    return 100 * raw / max(raw.sum(), 1e-12), 100 * per / max(per.sum(), 1e-12)


peak, clipped = np.abs(st).max(), int((np.abs(st) > 0.99).sum())
print(f'{A.wav}: {dur:.2f} s, {sr} Hz, {ch} ch · peak {peak:.3f} · clipped samples {clipped}')
print('%-13s %8s %7s   %-34s %s' % ('section (s)', 'rms dB', 'peak', 'raw energy  ' + ' '.join(b[0] for b in BANDS), 'A-weighted (what the ear hears)'))
secs = [tuple(map(float, s.split('-'))) for s in A.sections] or [(a, min(a + 10, dur - A.lead)) for a in np.arange(0, dur - A.lead - 0.5, 10)]
fmt = lambda v: ' '.join('%4.0f%%' % q for q in v)
for a, c in secs:
    s = x[int((a + A.lead) * sr):int((c + A.lead) * sr)]
    if len(s) < sr // 10:
        continue
    raw, per = spectrum(s)
    print('%5.1f-%-7.1f %8.1f %7.3f   %-34s %s' % (a, c, db(np.sqrt((s ** 2).mean())), np.abs(s).max(), fmt(raw), fmt(per)))

# whole-film balance, measured where the music actually plays (blocks louder than -30 dB)
blk = int(0.5 * sr); loud = [x[i:i + blk] for i in range(int(A.lead * sr), len(x) - blk, blk) if db(np.sqrt((x[i:i + blk] ** 2).mean())) > -30]
if loud:
    body = np.concatenate(loud); raw, per = spectrum(body); rms = db(np.sqrt((body ** 2).mean()))
    print(f'whole film (music only): rms {rms:.1f} dB · raw {fmt(raw)} · A-weighted {fmt(per)}')
    verdict += [(peak < 0.9 and clipped == 0, f'peak {peak:.2f}, {clipped} clipped (target < 0.9, 0)'),
                (-22 <= rms <= -12, f'music RMS {rms:.1f} dBFS (target about -22 to -12; the MP4 export normalises to -14 LUFS)'),
                (raw[0] <= 45, f'raw energy below 80 Hz {raw[0]:.0f} % (target ≤ 45 %; lower kick/bass if high)'),
                (per[2] + per[3] >= 55, f'A-weighted mids {per[2] + per[3]:.0f} % (target ≥ 55 %: keys, claps, melody carry it)'),
                (per[4] >= 3, f'A-weighted air 4–12 kHz {per[4]:.1f} % (target ≥ 3 %: add hats, shaker, bells, brighter attacks)')]
if ch == 2 and loud:
    L = np.concatenate([st[i:i + blk, 0] for i in range(int(A.lead * sr), len(x) - blk, blk) if db(np.sqrt((x[i:i + blk] ** 2).mean())) > -30])
    R = np.concatenate([st[i:i + blk, 1] for i in range(int(A.lead * sr), len(x) - blk, blk) if db(np.sqrt((x[i:i + blk] ** 2).mean())) > -30])
    side = np.sqrt((((L - R) / 2) ** 2).mean()) / max(np.sqrt((((L + R) / 2) ** 2).mean()), 1e-12)
    verdict.append((0.08 <= side <= 0.6, f'stereo width side/mid {side:.2f} (target 0.08–0.6: pan hats, arps and shakers a little)'))
for sec in A.silent:
    a, c = map(float, sec.split('-')); s = x[int((a + A.lead) * sr):int((c + A.lead) * sr)]
    r = db(np.sqrt((s ** 2).mean())) if len(s) else -99
    verdict.append((r < -35, f'intended silence {a:g}–{c:g} s at {r:.1f} dB (target < -35 dB)'))

# onsets (spectral flux), compared with the 16th-note grid
n, h = 1024, 256; win = np.hanning(n); prev = None; flux = []
for i in range(0, len(x) - n, h):
    m = np.abs(np.fft.rfft(x[i:i + n] * win)); flux.append(0.0 if prev is None else float(np.maximum(m - prev, 0).sum())); prev = m
flux = np.array(flux); Wn = int(0.4 * sr / h)   # adaptive threshold: 3× the local median (±0.4 s), never below 4 % of the loudest onset
thr = np.maximum(np.array([np.median(flux[max(0, i - Wn):i + Wn + 1]) for i in range(len(flux))]) * 3, flux.max() * 0.04)
peaks, gap = [], int(0.06 * sr / h)   # one onset per 60 ms: keep the strongest of a cluster
for i in range(1, len(flux) - 1):
    if flux[i] > thr[i] and flux[i] >= flux[i - 1] and flux[i] > flux[i + 1]:
        if peaks and i - peaks[-1] < gap:
            if flux[i] > flux[peaks[-1]]: peaks[-1] = i
        else: peaks.append(i)
on = np.array([(i * h + n / 2) / sr - A.lead for i in peaks])
if len(on):
    g = 60 / A.bpm / 4; off = (on + g / 2) % g - g / 2; iqr = 1000 * (np.percentile(off, 75) - np.percentile(off, 25))
    print(f'onsets {len(on)} · median offset from the 16th-note grid {1000 * np.median(off):+.0f} ms · spread (IQR) {iqr:.0f} ms')
    verdict.append((round(iqr) <= 25, f'onset spread on the {A.bpm:g} BPM grid {iqr:.0f} ms (target ≤ 25 ms; check --bpm if high)'))
for t0 in [float(v) for v in A.hits.split(',') if v.strip()]:
    near = on[np.abs(on - t0) < 0.08] if len(on) else []
    print(f'  hit at {t0:.2f} s: ' + (', '.join(f'{v:.3f}' for v in near) if len(near) else 'NO ONSET — the moment has no audible accent'))
    verdict.append((len(near) > 0, f'hit at {t0:.2f} s'))
# clicks: isolated one-sample spikes (an envelope that starts above silence). There must be none.
d2 = np.abs(x[1:-1] - (x[:-2] + x[2:]) / 2)
clicks = [i + 1 for i in np.where(d2 > 0.15)[0] if abs(x[i + 1]) > 8 * np.sqrt((np.r_[x[max(0, i - 31):i + 1], x[i + 2:i + 34]] ** 2).mean() + 1e-12)]
print(f'clicks (isolated one-sample spikes) {len(clicks)}' + (' at ' + ', '.join(f'{i / sr - A.lead:.3f} s' for i in clicks[:8]) if clicks else ' · good'))
verdict.append((not clicks, f'{len(clicks)} clicks (target 0)'))
# loudness curve in 0.5 s steps, to spot holes and spikes
hop = int(0.5 * sr); env = [db(np.sqrt((x[i:i + hop] ** 2).mean())) for i in range(int(A.lead * sr), len(x) - hop, hop)]
print('rms every 0.5 s (dB):')
for r in range(0, len(env), 20):
    print('  %5.1f s ' % (r * 0.5) + ' '.join('%4.0f' % v for v in env[r:r + 20]))
print('verdict:')
for ok, t in verdict:
    print(('  PASS  ' if ok else '  WARN  ') + t)
````

### `fonts.py`: embed Google or brand fonts as base64

<!-- file: fonts.py -->
````python
#!/usr/bin/env python3
"""Embed fonts in a film as base64 @font-face rules (no network needed at playback).

  python fonts.py google "Inter" 300,500,700 [--italic] [--subsets latin] [--into film.html] [--as Display]
  python fonts.py google "Archivo" "wdth,wght@62..125,100..900"      a raw axis spec (any Google axes): one variable file
  python fonts.py google "Newsreader" "opsz,wght@6..72,300..400"     with weight and width/optical-size ranges declared
  python fonts.py local "Brand" Light.woff2:300 Medium.woff2:500 Bold.woff2:700 [Italic.woff2:300i] [--into film.html]

google  downloads WOFF2 from the Google Fonts CSS API (only the subsets you ask for; latin by default) — check the licence
        (Google Fonts are OFL/Apache, fine to embed). local embeds files you were given (the brand's own font files).
--into  inserts the @font-face rules at the top of the film's first <style>; otherwise the CSS is printed.
--as    the family name to declare (default: the font's own name). Then use it: --display:'Display', sans-serif
"""
import argparse, base64, pathlib, re, sys, urllib.request

ap = argparse.ArgumentParser()
ap.add_argument('mode', choices=['google', 'local']); ap.add_argument('family'); ap.add_argument('items', nargs='+')
ap.add_argument('--italic', action='store_true'); ap.add_argument('--subsets', default='latin'); ap.add_argument('--into'); ap.add_argument('--as', dest='alias')
A = ap.parse_args()
name = A.alias or A.family
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'   # → WOFF2 responses
rules = []


def face(b64, weight, style, fmt='woff2', urange=None, stretch=None):
    r = f"@font-face{{font-family:'{name}';src:url(data:font/{fmt};base64,{b64}) format('{fmt}');font-weight:{weight};font-style:{style};font-display:block"
    r += f';font-stretch:{stretch}' if stretch else ''
    return r + (f';unicode-range:{urange}' if urange else '') + '}'


if A.mode == 'google':
    raw = '@' in A.items[0]   # "wdth,wght@62..125,100..900": passed to Google as it is
    weights = [] if raw else [w.strip() for w in A.items[0].split(',') if w.strip()]
    axis = A.items[0].replace(' ', '') if raw else 'ital,wght@' + ';'.join([f'0,{w}' for w in weights] + ([f'1,{w}' for w in weights] if A.italic else [])) if A.italic else 'wght@' + ';'.join(weights)
    url = f'https://fonts.googleapis.com/css2?family={A.family.replace(" ", "+")}:{axis}&display=block'
    css = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=30).read().decode()
    want = {s.strip() for s in A.subsets.split(',')}
    seen = {}
    for sub, body in re.findall(r'/\*\s*([\w-]+)\s*\*/\s*@font-face\s*\{([^}]*)\}', css):
        if sub not in want:
            continue
        src = re.search(r'url\((https://[^)]+)\)', body).group(1)
        wm = re.search(r'font-weight:\s*(\d+)(?:\s+(\d+))?', body); wt = wm.group(1) if not wm.group(2) else f'{wm.group(1)} {wm.group(2)}'
        fs = re.search(r'font-stretch:\s*([^;]+)', body); stretch = fs.group(1).strip() if fs else None
        stl = re.search(r'font-style:\s*(\w+)', body).group(1)
        ur = re.search(r'unicode-range:\s*([^;]+)', body)
        key = (src, stl, sub)
        if key in seen:   # a variable font serves every weight from one file: embed it once, as a weight range
            seen[key][1] += [int(w) for w in wt.split()]; continue
        data = urllib.request.urlopen(urllib.request.Request(src, headers={'User-Agent': UA}), timeout=30).read()
        seen[key] = [data, [int(w) for w in wt.split()], stl, ur.group(1).strip() if ur else None, sub, stretch]
    for (src, stl, sub), (data, wts, stl, urange, sub, stretch) in seen.items():
        wt = str(wts[0]) if len(set(wts)) == 1 else f'{min(wts)} {max(wts)}'
        rules.append(face(base64.b64encode(data).decode(), wt, stl, 'woff2', urange, stretch))
        print(f'  {A.family} {wt} {stl} [{sub}] {len(data) / 1e3:.0f} kB' + (' (variable: one file for every weight)' if len(wts) > 1 else ''), file=sys.stderr)
    if not rules:
        sys.exit(f'no faces found for subsets {want} — check the family name / weights: {url}')
else:
    for it in A.items:
        path, _, spec = it.rpartition(':')
        if not path:
            sys.exit(f'use FILE:WEIGHT (e.g. Bold.woff2:700, Italic.woff2:300i), got {it}')
        p = pathlib.Path(path); fmt = {'.woff2': 'woff2', '.woff': 'woff', '.ttf': 'truetype', '.otf': 'opentype'}[p.suffix.lower()]
        rules.append(face(base64.b64encode(p.read_bytes()).decode(), spec.rstrip('i'), 'italic' if spec.endswith('i') else 'normal', fmt))
        print(f'  {p.name} → {name} {spec} ({p.stat().st_size / 1e3:.0f} kB)', file=sys.stderr)

css = '\n'.join(rules) + '\n'
if A.into:
    f = pathlib.Path(A.into); html = f.read_text(encoding='utf-8')
    m = re.search(r'<style\b[^>]*>', html, re.I)
    if not m:
        sys.exit('no <style> in ' + A.into)
    html = html[:m.end()] + '\n' + css + html[m.end():]
    f.write_text(html, encoding='utf-8', newline=''); print(f'inserted {len(rules)} @font-face rules into {f} — now set --display/--ui to \'{name}\'', file=sys.stderr)
else:
    sys.stdout.write(css)
````

### `inline.py`: inline every local asset into one file

<!-- file: inline.py -->
````python
#!/usr/bin/env python3
"""Make a film self-contained: inline every local asset it references.

  python inline.py film.src.html film.html

Inlines (as data URIs or inline text):
  <img|audio|video|source|image|track|link rel=icon|embed|object> src / href / poster / data
  <link rel="stylesheet" href="x.css">  → <style> (its own url(...) refs resolve from the CSS file's folder)
  <script src="x.js"></script>         → inline <script>
  url(...) inside <style> blocks and style="" attributes (fonts, backgrounds)
Kept as they are: http(s)://, //, data:, #fragment and <use href> references (put SVG symbols inline instead).
Prints what was inlined and the final size; warns above 25 MB.
"""
import base64, mimetypes, pathlib, re, sys

MIME = {'.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.otf': 'font/otf', '.svg': 'image/svg+xml', '.png': 'image/png',
        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.avif': 'image/avif', '.gif': 'image/gif', '.mp3': 'audio/mpeg',
        '.m4a': 'audio/mp4', '.wav': 'audio/wav', '.ogg': 'audio/ogg', '.mp4': 'video/mp4', '.webm': 'video/webm', '.json': 'application/json',
        '.vtt': 'text/vtt', '.ico': 'image/x-icon'}
if len(sys.argv) != 3:
    sys.exit(__doc__)
src, dst = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2])
base = src.parent
html = src.read_text(encoding='utf-8')
done = []


def is_local(ref):
    ref = ref.strip()
    return bool(ref) and not re.match(r'^(?:[a-z][a-z0-9+.-]*:|//|#)', ref, re.I)


def data_uri(path):
    p = path.resolve()
    if not p.exists():
        print('  MISSING:', p)
        return None
    mt = MIME.get(p.suffix.lower()) or mimetypes.guess_type(str(p))[0] or 'application/octet-stream'
    done.append(f'{p.name} ({p.stat().st_size / 1e3:.0f} kB)')
    return f'data:{mt};base64,' + base64.b64encode(p.read_bytes()).decode()


def clean(ref):
    return ref.split('#')[0].split('?')[0]


def css_urls(css, folder):
    def rep(m):
        ref = m.group(2)
        if not is_local(ref):
            return m.group(0)
        u = data_uri(folder / clean(ref))
        return f'url({u})' if u else m.group(0)
    return re.sub(r'url\(\s*([\'"]?)([^\'")]+)\1\s*\)', rep, css)


def link_tag(m):
    tag = m.group(0)
    href = re.search(r'\bhref\s*=\s*["\']([^"\']+)["\']', tag, re.I)
    if not href or not is_local(href.group(1)):
        return tag
    if re.search(r'\brel\s*=\s*["\'][^"\']*stylesheet', tag, re.I):
        p = (base / clean(href.group(1))).resolve()
        done.append(p.name)
        return '<style>\n' + css_urls(p.read_text(encoding='utf-8'), p.parent) + '\n</style>'
    u = data_uri(base / clean(href.group(1)))   # icons and other links
    return tag.replace(href.group(1), u) if u else tag


def script_tag(m):
    ref = m.group(1)
    if not is_local(ref):
        return m.group(0)
    p = (base / clean(ref)).resolve()
    done.append(p.name)
    return '<script>\n' + p.read_text(encoding='utf-8').replace('</script', '<\\/script') + '\n</script>'


def media_attr(m):
    full, name, q, ref = m.group(0), m.group(2), m.group(3), m.group(4)
    if not is_local(ref):
        return full
    u = data_uri(base / clean(ref))
    return full.replace(f'{name}={q}{ref}{q}', f'{name}={q}{u}{q}') if u else full


KEEP = []   # HTML comments and inline script bodies are never scanned for assets (a comment that mentions <audio src> is not an asset)


def stash(text):
    KEEP.append(text); return f'\x00KEEP{len(KEEP) - 1}\x00'


def keep(m):
    return stash(m.group(0))


html = re.sub(r'<!--.*?-->', keep, html, flags=re.S)
html = re.sub(r'<link\b[^>]*>', link_tag, html, flags=re.I)
html = re.sub(r'<script\b[^>]*?\bsrc\s*=\s*["\']([^"\']+)["\'][^>]*>\s*</script>', script_tag, html, flags=re.I)
html = re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + css_urls(m.group(2), base) + m.group(3), html, flags=re.S | re.I)
html = re.sub(r'\bstyle\s*=\s*"([^"]*url\([^"]*)"', lambda m: 'style="' + css_urls(m.group(1), base).replace('"', "'") + '"', html, flags=re.I)
html = re.sub(r'(<script\b[^>]*>)(.*?)(</script>)', lambda m: m.group(1) + stash(m.group(2)) + m.group(3), html, flags=re.S | re.I)
for _ in range(3):   # a tag can carry several refs (e.g. <video poster src>); inlined ones start with data:, so this converges
    html = re.sub(r'<(img|audio|video|source|image|track|embed|object)\b[^>]*?\b(src|href|xlink:href|poster|data)\s*=\s*(["\'])((?!data:|https?:|//|#)[^"\']+)\3',
                  media_attr, html, flags=re.I)
for _ in range(2):   # restore protected blocks (a kept script may itself contain a kept marker)
    html = re.sub(r'\x00KEEP(\d+)\x00', lambda m: KEEP[int(m.group(1))], html)
dst.write_text(html, encoding='utf-8', newline='')
size = dst.stat().st_size / 1e6
print('inlined:', ', '.join(done) if done else 'nothing (already self-contained)')
print(f'wrote {dst} · {size:.2f} MB' + ('  WARNING: over 25 MB, compress images/audio first' if size > 25 else ''))
````

### `vo_timing.py`: sync a voiceover the user made

<!-- file: vo_timing.py -->
````python
#!/usr/bin/env python3
"""Find where each line of a voiceover actually lands, so picture beats can be pinned to it.

  python vo_timing.py vo.mp3                         speech segments (start, end) in seconds
  python vo_timing.py vo.mp3 --lines script.txt      map script lines (one per line) to segments → SUBS, DUCK, line starts
  script.txt may be the exact ElevenLabs script: <break time="0.6s" /> tags, [audio tags] and # comment lines are ignored
  options: --silence -35 (dB below the loudest speech that counts as a pause)   --min-gap 0.28 (s)   --json out.json

Decoding: WAV natively; MP3/M4A/OGG/FLAC via `pip install miniaudio` (no ffmpeg needed), else ffmpeg if it is on PATH.
When the script has fewer lines than segments, the shortest pauses are merged first (a sentence with a comma can split in two).
Check the result by ear-free means too: the printed segment list should match the script's sentence count and rhythm.
"""
import argparse, json, pathlib, shutil, subprocess, sys, wave
import numpy as np

ap = argparse.ArgumentParser(); ap.add_argument('audio'); ap.add_argument('--lines'); ap.add_argument('--silence', type=float, default=-35)
ap.add_argument('--min-gap', type=float, default=0.28); ap.add_argument('--min-speech', type=float, default=0.15); ap.add_argument('--json')
A = ap.parse_args()
p = pathlib.Path(A.audio)


def decode(path):
    if path.suffix.lower() == '.wav':
        w = wave.open(str(path)); sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
        raw = np.frombuffer(w.readframes(w.getnframes()), {1: np.int8, 2: np.int16, 4: np.int32}[sw]).astype(np.float64)
        return raw.reshape(-1, ch).mean(1) / float(2 ** (8 * sw - 1)), sr
    try:
        import miniaudio
        d = miniaudio.decode_file(str(path), output_format=miniaudio.SampleFormat.SIGNED16, nchannels=1, sample_rate=22050)
        return np.frombuffer(d.samples, np.int16).astype(np.float64) / 32768.0, 22050
    except ImportError:
        pass
    if shutil.which('ffmpeg'):
        raw = subprocess.run(['ffmpeg', '-v', 'quiet', '-i', str(path), '-ac', '1', '-ar', '22050', '-f', 's16le', '-'], capture_output=True, check=True).stdout
        return np.frombuffer(raw, np.int16).astype(np.float64) / 32768.0, 22050
    sys.exit('cannot decode ' + path.suffix + ': pip install miniaudio (or install ffmpeg), or pass a WAV')


x, sr = decode(p)
hop = int(0.02 * sr); n = len(x) // hop
env = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
thr = np.percentile(env, 95) + A.silence
voiced = env > thr
segs, i = [], 0
while i < n:   # runs of voiced frames, with short dips bridged
    if voiced[i]:
        j = i
        while j < n and (voiced[j] or voiced[j:j + int(A.min_gap / 0.02)].any()):
            j += 1
        if (j - i) * 0.02 >= A.min_speech:
            segs.append([round(i * 0.02, 2), round(j * 0.02, 2)])
        i = j
    else:
        i += 1
print(f'{p.name}: {len(x) / sr:.2f} s · threshold {thr:.1f} dB · {len(segs)} speech segments')
import re
def clean(l):   # drop ElevenLabs markup: <break time="0.6s" /> tags and [audio tags] such as [warmly]
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]*>|\[[^\]]*\]', ' ', l)).strip()
lines = [clean(l) for l in pathlib.Path(A.lines).read_text(encoding='utf-8').splitlines() if l.strip() and not l.strip().startswith('#')] if A.lines else None
lines = [l for l in lines if l] if lines else lines
if lines and len(segs) > len(lines):
    while len(segs) > len(lines):   # merge across the shortest pause
        k = min(range(len(segs) - 1), key=lambda q: segs[q + 1][0] - segs[q][1]); segs[k][1] = segs[k + 1][1]; del segs[k + 1]
if lines and len(segs) < len(lines):
    print(f'WARNING: {len(lines)} script lines but only {len(segs)} segments: lower --min-gap or check the take')
for k, (a, c) in enumerate(segs):
    print(f'  {k + 1:2d}  {a:6.2f} → {c:6.2f}  ({c - a:4.2f} s)' + (f'   {lines[k]}' if lines and k < len(lines) else ''))
if lines:
    m = min(len(lines), len(segs))
    print('\nconst SUBS = [ // [start, end, text] in voiceover time')
    for k in range(m):
        print(f"  [{segs[k][0]}, {segs[k][1]}, {json.dumps(lines[k], ensure_ascii=False)}],")
    print('];\n// pin each scene beat to the line that names it: ANCH = [[scriptTime, voTime], ...] with voTime from the starts above')
if segs:
    duck = []
    for a, c in segs:
        if duck and a - duck[-1][1] < 0.35: duck[-1][1] = c
        else: duck.append([a, c])
    print('const DUCK = [' + ', '.join(f'[{a}, {c}]' for a, c in duck) + '];   // paste into the timeline block: the score dips under speech')
    print('const VO_LINES = [' + ', '.join(str(a) for a, _ in segs) + '];   // line starts: land each scene\'s key move on these')
    print(f'// the voice ends at {segs[-1][1]:.2f} s: make DUR at least {segs[-1][1] + 2.5:.1f} s so the end card holds after the last word')
if A.json:
    pathlib.Path(A.json).write_text(json.dumps({'segments': segs, 'lines': lines}, indent=1), encoding='utf-8')
````
