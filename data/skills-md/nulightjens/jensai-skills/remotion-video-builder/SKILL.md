---
name: remotion-video-builder
description: Build a complete Remotion video composition from a written style guide. Takes a STYLE-GUIDE.md describing canvas, colors, fonts, text animation, cut rhythm, and audio, then produces a renderable composition with new content. Covers script writing, voiceover generation, word-level caption sync, asset collection, and component architecture. Use when asked to "build a video in this style," "create a new reel," "make a video like [reference]," "produce a Remotion video," or any request to create a programmatic video from a style template. Works with any Remotion project and does not assume a particular folder layout.
---

# Remotion Video Builder

Build complete Remotion video compositions from style guides. This skill bridges the gap between a visual style specification, hand-authored or reverse-engineered from a reference video, and a working, renderable Remotion composition with new content.

---

## Prerequisites

Before starting, verify:

1. **Remotion project exists**: either an existing project, or create one:
   ```bash
   npx create-video@latest my-video
   cd my-video
   npm install
   ```
2. **Style guide available**: a STYLE-GUIDE.md covering canvas dimensions, colors, fonts, text animation, cut rhythm, and audio specs. Write it by hand, or derive it from a reference video.
3. **For voiceover**: an ElevenLabs API key in `ELEVENLABS_API_KEY`, or an equivalent TTS service
4. **For transcription**: a Gemini API key in `GEMINI_API_KEY` for word-level timestamps, or whisper.cpp installed locally
5. **For B-roll**: a Pexels API key in `PEXELS_API_KEY` for automated fetching, or manual asset collection

> **Key setup**: export the keys your workflow actually needs before starting, for example `export ELEVENLABS_API_KEY="..."` in your shell profile or a project `.env` file. Only the voiceover step needs ElevenLabs, only the transcription step needs Gemini, and only automated B-roll needs Pexels, so a manual-asset run may need no keys at all.

---

## Workflow

### Step 1: Load & Parse Style Guide

Read the STYLE-GUIDE.md and extract every parameter into a mental model:

**Canvas parameters:**
- Width, height, FPS, typical duration
- Safe zones (top, bottom, left, right padding)

**Visual parameters:**
- Background color (canvas)
- Color palette (primary text, accent colors, color rules)
- Font family, weight, case, letter spacing, line height
- Text sizes (hook vs. main captions)
- Text positioning (vertical %, horizontal alignment, max width)
- Caption styling (pill background vs. bare text, shadows, outlines)

**Animation parameters:**
- Text animation type: karaoke word-reveal, pop-in, typewriter, phrase-swap
- Animation timing: instant reveal, fade duration, scale curves
- Sentence boundary behavior: hard-cut, fade-out, slide-up

**Layout parameters:**
- Layout modes (floating card, full-bleed, split-screen, etc.)
- Layout distribution (% of video in each mode)
- Image treatment: Ken Burns zoom, padding, corners, shadows

**Audio parameters:**
- Voice specs (voice name, stability, similarity, speed, model)
- Music bed volume relative to voice
- SFX inventory (cuts, transitions, reveals)
- Audio format requirements

**Editorial parameters:**
- Storytelling template / beat structure
- Typical word count and WPM
- Vernacular rules (sentence length, pronouns, TTS quirks)
- CTA style

> **Action**: Read the style guide. Summarize the extracted parameters back to the user for confirmation before proceeding. Flag any gaps that need filling.

---

### Step 2: Write the Script

The script drives everything: timing, assets, duration. Write it before anything else.

1. **Select a storytelling template** from the style guide, or load `references/storytelling-templates.md` for options
2. **Ask the user for the topic/story**: what is this video about?
3. **Draft the script** following:
   - The beat structure from the chosen template
   - Word count and WPM targets from the style guide
   - TTS optimization rules (see below)
   - The style guide's vernacular rules (pronoun ratios, sentence length, tone)
4. **Present the script** with beat labels and estimated timing per section
5. **Get user approval** before proceeding. The script is the contract.

**TTS Writing Rules (apply to all scripts):**
- No rhetorical questions unless the style guide explicitly uses them. TTS reads questions with an unnatural rising intonation
- Short sentences (8-15 words) produce better prosody than long ones
- Use concrete nouns over abstract concepts. TTS handles them better
- Spell out numbers for natural reading ("eight hundred" not "800")
- Use em dashes (written `--` in these templates) for punchy pauses, periods for full stops
- ALL CAPS on words that need stress emphasis
- Avoid parenthetical asides. TTS does not handle nested clauses well
- End sentences on strong nouns, not prepositions or weak verbs

---

### Step 3: Generate Voiceover

1. **Match voice to style guide specs**: use the exact voice name, model, and settings specified
2. **If using ElevenLabs MCP tools**: use `mcp__elevenlabs__text_to_speech` with:
   - Voice ID from style guide (or search with `mcp__elevenlabs__search_voices`)
   - Model ID (e.g., `eleven_multilingual_v2`)
   - Stability, similarity, style, speed settings from style guide
3. **If using ElevenLabs API directly**: format the script following the ElevenLabs formatting guide (em dashes for pauses, ALL CAPS for emphasis, phoneme tags for mispronunciations)
4. **Save audio** to the project's `public/` directory (e.g., `public/voiceover.mp3`)
5. **Get the audio duration**:
   ```bash
   ffprobe -v error -show_entries format=duration -of csv=p=0 public/voiceover.mp3
   ```

> **Checkpoint**: Play the audio back or confirm with user before proceeding to transcription.

---

### Step 4: Transcribe with Word-Level Timestamps

Word-level timestamps are the backbone of caption sync and scene timing.

**Option A: Gemini API (preferred for accuracy)**
- Upload the audio file to Gemini with a prompt requesting word-level timestamps
- Parse the response into the standard format

**Option B: whisper.cpp (local, no API needed)**
```bash
./whisper.cpp/main -m models/ggml-medium.en.bin -f public/voiceover.mp3 --output-json --max-len 1 --word-timestamps true
```

**Output format**, saved as `public/captions.json`:
```json
[
  { "word": "this", "start": 0.4 },
  { "word": "company", "start": 0.72 },
  { "word": "changed", "start": 1.14 },
  { "word": "everything", "start": 1.52 }
]
```

**Post-processing:**
- Verify first and last word timestamps align with audible speech start/end
- Calculate total duration: last word start + ~0.5s buffer
- Calculate total frames: `Math.ceil(audioDurationSeconds * fps)`
- Group words into sentences/phrases based on punctuation and pause gaps (>500ms = sentence break)

---

### Step 5: Collect Assets

Based on the script, identify and collect visual assets.

1. **Create an asset list**: for each sentence or scene in the script, describe the ideal B-roll image or clip:
   ```
   Scene 1 (0:00-0:03): "Company X changed logistics forever" → warehouse/logistics footage
   Scene 2 (0:03-0:07): "They started with a simple idea" → founder portrait or early office
   ```
2. **Source assets**:
   - **Pexels API**: If the project has a `fetch-broll.ts` script, use it. Otherwise, use the Pexels API directly with search terms from the asset list. Request portrait orientation (9:16) and minimum 1080px width.
   - **Manual collection**: Ask the user to provide specific images/clips
   - **Web search**: For brand-specific assets (logos, product shots), search and download
3. **Save to project**: `public/broll/broll-01-description.jpg` (or `.mp4` for video clips)
4. **Create a manifest** if the project pattern uses one:
   ```json
   [
     { "file": "broll-01-warehouse.jpg", "description": "Warehouse logistics", "source": "pexels", "id": "12345" },
     { "file": "broll-02-founder.jpg", "description": "Company founder", "source": "manual" }
   ]
   ```

**Asset quality checklist:**
- Minimum 1080px wide (for 1080x1920 canvas)
- No watermarks
- Appropriate aspect ratio (portrait preferred, landscape can be cropped)
- Visual variety: a mix of close-ups, wide shots, abstract, concrete

---

### Step 6: Build Remotion Components

**IMPORTANT**: Before creating any components, read the existing project structure thoroughly. Follow existing patterns for file organization, naming conventions, imports, and prop types.

Load `references/component-patterns.md` for reusable component templates.

#### 6a. Canvas / Theme Setup

Create or update the theme/token file based on the style guide:

```typescript
// theme.ts or tokens.ts
export const theme = {
  canvas: { width: 1080, height: 1920 },
  colors: {
    background: '#FFFFFF',
    primaryText: '#000000',
    accent: '#FFD700', // from style guide
  },
  fonts: {
    primary: { family: 'Inter', weight: '900' },
  },
  text: {
    hookSize: 110,
    captionSize: 75,
    case: 'lowercase' as const,
    letterSpacing: '-0.02em',
    lineHeight: 1.2,
    maxWidth: 0.8, // fraction of canvas width
    verticalPosition: 0.72, // fraction of canvas height
  },
  safeZones: {
    top: 120, bottom: 270, left: 40, right: 40,
  },
};
```

#### 6b. Load Fonts

```typescript
// fonts.ts
import { loadFont } from '@remotion/fonts';

export const fontFamily = loadFont({
  family: 'Inter',
  url: 'https://fonts.gstatic.com/s/inter/v18/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuBWYAZ9hiA.woff2',
  weight: '900',
}).fontFamily;
```

#### 6c. Build Components Based on Style Guide

Select and build components matching the style guide's layout modes and animation types. Common patterns (see `references/component-patterns.md` for full implementations):

| Component | Use When Style Guide Specifies |
|-----------|-------------------------------|
| **FloatingCard** | Images on colored/white canvas with padding, optional Ken Burns |
| **KaraokeCaption** | Word-by-word reveal synced to timestamps |
| **PhraseCaptions** | Phrase-based captions (dark pill or bare text) |
| **HardCutSequencer** | Scene manager for asset switching at frame boundaries |
| **MusicBed** | Looped background audio at configurable volume |
| **HookScene** | Colored background + hero asset + large text for opening |
| **SplitLayout** | Multiple images or top/bottom split on canvas |

**Component rules:**
- One component per file, under 200 lines
- All timing derived from audio timestamps and FPS, never hard-coded frame numbers
- Use `useCurrentFrame()` and `useVideoConfig()` from Remotion
- Use `interpolate()` and `spring()` for all animations
- Props should be typed with Zod schemas when the project uses them

#### 6d. Register the Composition

In `Root.tsx` (or wherever compositions are registered):

```typescript
import { Composition } from 'remotion';

export const Root: React.FC = () => {
  return (
    <Composition
      id="new-video-name"
      component={MainComposition}
      durationInFrames={totalFrames} // from audio duration * fps
      fps={30}
      width={1080}
      height={1920}
      defaultProps={clipConfig}
    />
  );
};
```

---

### Step 7: Configure Scene Sequence

Map every script sentence to a scene with precise timing.

```typescript
const clips = [
  {
    file: 'broll/broll-01-warehouse.jpg',
    startFrame: 0,
    endFrame: 90, // 3 seconds at 30fps
    layout: 'floating-card',
    words: [
      { word: 'this', start: 0.4 },
      { word: 'company', start: 0.72 },
      { word: 'changed', start: 1.14 },
      { word: 'everything', start: 1.52 },
    ],
  },
  {
    file: 'broll/broll-02-founder.jpg',
    startFrame: 90,
    endFrame: 210, // next 4 seconds
    layout: 'floating-card',
    words: [ /* ... */ ],
  },
  // ... one entry per scene
];
```

**Scene timing rules:**
- Each scene boundary should align with a sentence break in the voiceover
- Scene duration should match the style guide's cut rhythm (e.g., 2-4s for fast cuts, 4-6s for split-screen)
- The first scene is the hook, so use the hook-specific styling from the style guide
- The last scene may need special treatment (CTA overlay, end card, etc.)

**Frame number calculation:**
```
startFrame = Math.round(firstWordTimestamp * fps)
endFrame = Math.round(lastWordTimestamp * fps) + paddingFrames
```

---

### Step 8: Preview & Iterate

1. **Start the preview server**:
   ```bash
   npx remotion preview
   ```
2. **Visual checks against style guide:**
   - [ ] Canvas dimensions and background color match
   - [ ] Font family, weight, size, and case match
   - [ ] Text position (vertical %) matches
   - [ ] Caption animation type matches (karaoke vs. phrase-swap vs. pop-in)
   - [ ] First word of each scene syncs with audio
   - [ ] Last word of each scene syncs before cut
   - [ ] Asset layout matches (floating card padding, Ken Burns zoom range)
   - [ ] Cut rhythm feels right (not too fast, not too slow)
   - [ ] Music bed volume is subordinate to voice
   - [ ] Safe zones respected (no text behind platform chrome)
3. **Use Playwright MCP** for automated screenshot comparison if available:
   - Navigate to `http://localhost:3000` and take screenshots at key frames
   - Compare against style guide reference screenshots
4. **Fix discrepancies** in a tight build-check-fix loop
5. **If recreating from a reference video** (not just a written style guide), use the **graded recreation loop** instead of eyeballing:
   - Work **one scene at a time**: recreate, gate, then advance. Whole-video passes do not converge.
   - Build a **contact sheet** per scene (grid collage of source frames, start → end) so you can "read" the motion arc as one image; feed it plus source frames alongside the style guide.
   - Render frames at timestamps matching the source (`npx remotion still`), Read them side-by-side with the ground-truth source frames, and grade the match /10 (layout fidelity, animation smoothness). Iterate until ≥9 before moving to the next scene.
   - Watch for the two known failure modes: missed **layering** (image behind text) and **animation overlap at scene boundaries**.
6. **Render final video**:
   ```bash
   npx remotion render MainComposition out/video.mp4
   ```

---

## Component Architecture Patterns

These are the core reusable patterns for Remotion video styles. Full implementations with TypeScript code are in `references/component-patterns.md`.

### 1. Floating Card
Image centered on canvas with configurable padding. Optional Ken Burns zoom (scale interpolation over scene duration). Sharp or rounded corners. Drop shadow optional. Used for documentary-style B-roll presentation on clean backgrounds.

### 2. Karaoke Caption
Word-by-word reveal synced to audio timestamps. Each word transitions from invisible to visible at its exact timestamp. Words accumulate to form phrases, then hard-cut on sentence boundaries. Config: font, size, weight, case, color, position, maxWidth, shadow.

### 3. Hard Cut Sequencer
Scene manager that maps an array of scene configs (with startFrame/endFrame) to Remotion `<Sequence>` components. Only the active scene renders at any given frame. Handles scene transitions (hard cut only, no dissolves unless the style guide specifies otherwise).

### 4. Music Bed
`<Audio>` component with loop enabled and configurable volume. Typically set to 0.05-0.1 (about -20dB relative to voice). Starts at frame 0, runs full duration. Can include fade-in/fade-out at composition boundaries.

### 5. Split Layout
Canvas divided into regions (top/bottom, left/right, grid). Each region renders a different asset or component. Used for talking-head + B-roll splits, multi-image showcases, before/after comparisons.

### 6. Hook Scene
The opening 2-4 seconds. Colored or branded background with a hero asset (scaled, centered) and large text overlay. May include entrance animation (zoom-in, scale-up). Sets the visual tone for the entire video.

---

## Key Rules

1. **Read the existing project structure first**, then follow its patterns for file organization, naming, imports, and prop typing. Never impose a foreign architecture.
2. **Never hard-code timing**: all frame numbers must be derived from `audioTimestamp * fps`. If the voiceover is re-recorded, the video should re-sync automatically.
3. **One component per file, under 200 lines.** Split large components into focused sub-components.
4. **The style guide is the source of truth**: every visual decision (color, font, position, animation) must reference a specific value from it. If the style guide does not specify something, ask the user.
5. **Test audio sync at boundaries**: check the first word and last word of every scene. If they are off by more than 2 frames, adjust.
6. **Use the project's existing theme system**: if the project has `theme.ts`, design tokens, or a shared config, extend it rather than creating a parallel system.
7. **Check the Remotion docs for API questions** (animations, sequencing, fonts, audio). <https://www.remotion.dev/docs> is authoritative; a Remotion API reference skill, if you have one installed, is a faster lookup.
8. **Assets go in `public/`.** Never import assets from `src/`. Remotion serves from `public/` via `staticFile()`.
9. **Reference-driven beats prompt-driven for complex motion.** Do not try to describe intricate animation in prose. Give a reference video or image, a contact sheet, or a start image plus an end image (generate the end state if needed) and let the agent reason from those. Attach an "art of the possible" reference too, such as an existing Remotion project full of complex animation or the official Remotion examples, so the model knows what the library can actually do.

---

## Quick Reference: File Outputs

At the end of the workflow, the project should contain:

```
project/
  src/
    Root.tsx                    # Updated with new composition registration
    components/
      [VideoName].tsx           # Main orchestrator component
      [AssetLayer].tsx          # B-roll / image rendering
      [CaptionLayer].tsx        # Text animation component
      [HookScene].tsx           # Opening scene (if style uses one)
      theme.ts                  # Design tokens from style guide
      fonts.ts                  # Font loader
  public/
    voiceover.mp3               # Generated TTS audio
    captions.json               # Word-level timestamps
    broll/
      broll-01-*.jpg            # B-roll assets
      broll-02-*.jpg
      ...
    sfx/
      music.mp3                 # Background music (if style uses one)
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Captions out of sync | Check that `captions.json` timestamps are in seconds (not ms). Verify FPS matches between transcription assumption and composition config. |
| Font not rendering | Ensure font is loaded via `@remotion/fonts` or `@remotion/google-fonts`. Check that `fontFamily` is passed to the text component's style. |
| Audio not playing in preview | Use `staticFile('voiceover.mp3')` not a relative path. Ensure file is in `public/`. |
| Ken Burns jittery | Use `interpolate()` with `Easing.inOut(Easing.ease)`, not spring, for slow zoom. |
| White flash between scenes | Ensure scene endFrame equals next scene startFrame (no gap). Use the sequencer pattern. |
| Video too long/short | Recalculate `durationInFrames` from actual audio duration: `Math.ceil(duration * fps)`. |
