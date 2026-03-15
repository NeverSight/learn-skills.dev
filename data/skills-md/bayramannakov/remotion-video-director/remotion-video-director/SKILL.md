---
name: remotion-video-director
description: |
  Interactive guide for creating Remotion videos - from strategic concept to rendered MP4.
  Use when the user wants to create a video, make a Remotion project, build a product demo video,
  generate a launch video, make a recurring content template, create a marketing video,
  or says "I need a video for...", "help me make a video", "video for my product", "remotion video".
  Covers the full creative process: expert deliberation, scenario design, build, and review.
  Works alongside the official remotion-dev/skills for API-level guidance.
version: 2.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
  - WebSearch
  - WebFetch
  - mcp__nanobanana__generate_image
---

# Remotion Video Director

An interactive skill that guides users from "I need a video" to a rendered MP4 with music, through expert deliberation, scenario design, and battle-tested Remotion patterns.

## When to Use

Trigger this skill when the user:
- Wants to create a video using Remotion
- Needs a product demo, launch video, recurring content template, marketing video, or narrative intro
- Says "I need a video", "make a video for...", "create a Remotion video", "video as code"
- Wants help thinking through what video to make or how to structure it
- Has a Remotion project and wants expert review

## Relationship to Official Remotion Skill

The official `remotion-dev/skills` package teaches Claude the Remotion API (37 rule files covering animations, audio, captions, transitions, etc.). This skill handles the **creative and strategic layer** on top:

- Official skill: "How do I use `interpolate()`?" (technical reference)
- Video Director: "What video should I make and how should it flow?" (creative process)

If the official Remotion skill is installed, leverage it for API-specific details. If not, the `references/remotion-patterns.md` and `references/component-library.md` in this skill provide sufficient Remotion knowledge to build production videos.

---

## Four-Phase Workflow

### Phase 1: Strategic Framing

**Goal**: Understand what the user needs through conversation, then assemble expert perspectives.

**CRITICAL**: This phase is INTERACTIVE. Ask questions one at a time and WAIT for answers. Do NOT dump all questions at once or auto-proceed without user input.

#### Step 1 - Discovery (Conversational)

Start with a single open question:

> "What is this video for? Tell me about the idea, who will watch it, and what you want them to do after."

**WAIT** for the user's answer. Then ask targeted follow-ups based on what's missing:

- If audience is unclear: "Who specifically will watch this? (customers, team, investors, social media?)"
- If desired action is unclear: "After watching, what should viewers DO? (sign up, understand something, share?)"
- If no constraints mentioned: "Any constraints I should know? Duration, brand colors, existing assets, deadline?"
- If they mention a product: "Can you share screenshots of the product/interface?"

Do NOT proceed until you understand: purpose, audience, desired action, and constraints.

#### Step 2 - Creative Direction

Present the creative direction options and ask the user to pick:

| Style | Feel | Best For |
|-------|------|----------|
| **Minimal/Jobs** | Black bg, dramatic pauses, one idea per frame, Impact font | Product launches, big ideas, keynotes |
| **Data-Rich/Bloomberg** | Dark navy bg, animated charts, dense but organized | Meeting recaps, reports, dashboards |
| **Warm/Narrative** | Warm tones, personal quotes, serif accents | Course intros, team stories, community |
| **Terminal/Hacker** | Dark code theme, typewriter, monospace everywhere | Technical demos, dev tools, engineering |
| **Custom** | User describes or provides reference screenshots/videos | Anything specific |

> "Which style direction fits your video? Or share screenshots of videos you've seen that you liked."

**WAIT** for answer.

Read `references/video-archetypes.md` for the full spec of the chosen direction (colors, fonts, animation style, timing rules).

#### Step 3 - Reference Input (Optional)

> "Do you have any reference videos, screenshots, or visual styles you'd like me to emulate? (Skip if none)"

If the user provides references, analyze them for: color palette, typography, animation speed, layout density, overall mood. Incorporate these into the creative brief.

**WAIT** for answer or skip confirmation.

#### Step 4 - Expert Panel Assembly

Based on the selected archetype (from `references/video-archetypes.md`) and creative direction, assemble a panel of 3-4 experts from `references/expert-definitions.md`.

**Generate expert perspectives** - for each expert, generate 2-3 sentences:
- One specific recommendation
- One risk to watch for

Keep this concise. Present as a brief roundtable. Highlight only where experts **disagree** (flags a decision the user needs to make).

#### Step 5 - Creative Brief

Synthesize into a structured brief:

```
## Creative Brief

**Purpose**: [one sentence]
**Audience**: [who, what they care about]
**Core Message**: [the ONE thing viewers should remember]
**Desired Action**: [what viewers should do next]
**Duration**: [seconds] ([frames] frames at 30fps)
**Creative Direction**: [selected style - Minimal/Jobs, Bloomberg, etc.]
**Emotional Arc**: [e.g., curiosity -> proof -> confidence -> action]

## Audio Strategy
- Music: [ambient/upbeat/dramatic/sparse] from Pixabay
- Voice-over: [yes/no]
- Music mood: [description matching creative direction]

## Scene Sequence
| # | Scene | Duration | Purpose |
|---|-------|----------|---------|
| 1 | ...   | Xs       | ...     |

## Data Model (if applicable)
[What's parameterized vs hardcoded - the reusable template structure]

## Visual Style
- Theme: [creative direction name]
- Background: [color]
- Colors: [primary, accent, secondary]
- Typography: [heading font, body font, mono font]
- Animation feel: [snappy/gentle/dramatic/typewriter]
```

> "Here's the creative brief. Want to adjust anything before we design scenes?"

**WAIT** for confirmation or adjustments.

---

### Phase 2: Scenario Design

**Goal**: Turn the brief into a detailed scene-by-scene scenario.

#### Step 6 - Scene Design

For each scene in the sequence, specify:
- **Content**: Exact text, data, visuals
- **Components**: Which reusable components to use (from `references/component-library.md`)
- **Animation**: Entry/exit animations, timing in frames
- **Transitions**: Cross-dissolve between all scenes (8-12 frames)

Read `references/remotion-patterns.md` for critical Remotion constraints and premium styling patterns.

**Scene Focus Rule**: Each scene must serve ONE idea that connects to the core message. If a scene is tangential to the core message, CUT IT. Fewer focused scenes are always better than many scattered ones.

**Frame Budget**: Map out the entire timeline:
```
const TIMING = {
  scene1: { start: 0, dur: 6 },   // Hook
  scene2: { start: 6, dur: 10 },  // ...
  // Total must match composition durationInFrames / fps
};
```

#### Step 7 - Data Architecture

If the video is data-driven (recurring report, multi-variant marketing):
- Design the config object that changes between renders
- Identify what stays constant (visual template) vs what varies (content)
- Show the user the config shape and confirm

Example pattern (from WeeklyIntro):
```typescript
const weekData = {
  weekLabel: "Mar 3 - Mar 9",
  heroNumber: 312,
  heroLabel: "new signups",
  // ... fields that change weekly
};
```

#### Step 8 - User Confirmation

Present the complete scenario.

> "Ready to build, or want to adjust anything?"

**WAIT** for confirmation.

---

### Phase 3: Build

**Goal**: Create the Remotion project and render the first version.

**CRITICAL**: Never run any command that launches an interactive CLI wizard or prompts for input. This includes `npx create-video`, `npx remotion init`, `npm init`, or bare `npx remotion render` without arguments. Always create files manually and pass all arguments explicitly to CLI commands.

#### Step 9 - Scaffold Project

Create the Remotion project structure manually (do NOT use scaffolding wizards - see Phase 3 header):
```
<project>/
├── src/
│   ├── Root.tsx
│   ├── Video.tsx           # or <VideoName>.tsx
│   ├── theme/
│   │   ├── colors.ts
│   │   ├── fonts.ts
│   │   └── springs.ts
│   ├── scenes/
│   │   ├── Scene1Hook.tsx
│   │   └── ...
│   ├── components/
│   │   ├── FadeIn.tsx
│   │   └── ...
│   └── data/
│       └── config.ts       # if data-driven
├── public/
│   ├── music.mp3           # background music
│   └── illustrations/      # if using background images
├── package.json
├── tsconfig.json
└── remotion.config.ts
```

Install dependencies: `pnpm install`

#### Step 10 - Build Scenes

Build each scene component following the scenario from Phase 2. Use components from `references/component-library.md`.

**Critical build rules** (from `references/remotion-patterns.md`):
- All animation via `useCurrentFrame()` + `interpolate()`/`spring()` - NEVER CSS transitions
- Always clamp interpolation: `{ extrapolateLeft: "clamp", extrapolateRight: "clamp" }`
- `useCurrentFrame()` is relative to nearest `<Sequence>`, not global timeline
- Cross-dissolve between every scene (8-12 frame envelope; exception: Terminal/Hacker style where hard cuts fit)
- Every element must animate in - never appear static on a cut

**Premium styling rules** (from `references/remotion-patterns.md`):
- Font variety: mix heading font + body font + mono font (not Inter everywhere)
- Extreme size contrast: headlines 72-96pt, body 20-24pt
- Center important questions/headlines vertically
- Max 15-20 words per body slide, 7 words for headline slides (Jobs-style)
- Keep text in upper 85% of frame
- Minimum 24px font for readability
- Padding 80-120px from edges

#### Step 11 - Audio Integration

Read `references/music-and-audio.md` for the full audio guide.

> "Want to add background music? I recommend browsing pixabay.com/music/ for a royalty-free track that matches the [selected creative direction] style. Share the download link or file and I'll integrate it with proper volume curves."

**WAIT** for user response.

If user provides music:
1. Download/save to `public/music.mp3`
2. Add `<Audio>` component with fade-in/fade-out volume curve
3. Lower music volume during data-heavy scenes (0.30 -> 0.15)
4. If track is longer than video, use `startFrom` to play the ending section

If user wants voice-over:
1. Generate narration script from scene content (~3 words/second)
2. User records or uses ElevenLabs
3. Integrate with music ducking (music drops to 0.10-0.12 during narration)

If user skips audio: render with `--muted` flag.

#### Step 12 - Render and Preview

**CRITICAL: Always pass the entry point file to avoid interactive prompts.** Never run bare `npx remotion render` - it may launch an interactive composition picker. Always specify the entry file and composition ID explicitly:

```bash
# Render final MP4 - always specify entry point + composition ID
npx remotion render src/Root.tsx <CompositionId> out/<name>.mp4 --codec=h264 --crf=18

# If no audio:
npx remotion render src/Root.tsx <CompositionId> out/<name>.mp4 --codec=h264 --crf=18 --muted
```

Open the video for the user to review.

---

### Phase 4: Review

**Goal**: Refine the video through expert review and user feedback until it's ready to ship.

#### Step 13 - Multi-Expert Review

After the user has seen the video, run the review protocol from `references/expert-definitions.md`.

Generate a scorecard (see `references/expert-definitions.md` for the full template):
```
| Dimension              | Priority | Score |
|------------------------|----------|-------|
| Hook clarity (first 3-5s) | Critical | ?/5   |
| Core message landed    | Critical | ?/5   |
| Pacing / dynamism      | High     | ?/5   |
| Visual readability     | High     | ?/5   |
| Target action clear    | High     | ?/5   |
| Audience fit           | Medium   | ?/5   |
```

Add 2-3 type-specific dimensions (e.g., "Visual premium feel" for Minimal/Jobs, "Audio-visual harmony" if music was added, "Config reusability" for data reports).

Each expert reviews from their angle, including the **Cinematographer** on visual composition and the **Music Director** on audio (if music was added). Synthesize into:
1. **Strengths** - what works well
2. **Improvements** - specific, actionable changes
3. **Verdict** - ship as-is, needs one more pass, or needs significant rework

Ask the user which improvements to apply.

#### Step 14 - User Review & Iteration

The expert review catches technical issues, but only the user knows if the video *feels right*.

> "Now that you've seen the video and the expert review - what's your take?
> 1. Which scenes work well?
> 2. Which scenes need changes? (screenshot specific frames if possible)
> 3. Any text, timing, or visual issues?
> 4. Anything missing or that should be cut?"

**WAIT** for the user's feedback.

When the user provides feedback:
1. **Acknowledge** what they liked (reinforces the direction)
2. **List** the specific changes you'll make based on their notes
3. **Make the changes** - edit scene components, adjust timing, fix text
4. **Re-render** and present the updated video
5. **Ask again**: "Better? Anything else to adjust?"

Repeat this loop until the user is satisfied. Typical videos need 1-3 rounds of refinement.

Common feedback patterns and how to handle them:
- "Too fast" → Increase scene durations by 30-50%, add more dramatic pauses
- "Too much text" → Split scenes, reduce to 7 words per frame (Jobs-style)
- "Doesn't feel premium" → Switch to Minimal/Jobs direction, add negative space
- "Music doesn't fit" → Try a different Pixabay track, adjust volume curve
- "Wrong tone" → Revisit creative direction, adjust color palette and animation speed
- "Scene X is confusing" → Simplify to ONE idea, add visual hierarchy

---

## Adaptation Guidelines

### When the user already has a Remotion project
Skip Phase 1-2 scaffolding. Focus on reviewing existing code, suggesting improvements, or adding new scenes/compositions.

### When the user wants a quick video (no deliberation)
Compress Phase 1 to: ask for video type + creative direction in one question. Pick top 2 experts, generate a brief scenario. Move to build quickly. Still ask about music.

### When the user wants only the concept (no code)
Run Phase 1-2 fully. Output the creative brief and scenario as a document. Skip Phase 3.

### When the user wants multi-variant videos
Use the Growth Marketing archetype. Design the variant matrix (what changes per variant). Build one base video, then show how to parameterize for N variants via config objects.

### When the user says "make it premium" / "more expensive"
Switch to Minimal/Jobs creative direction: black background, Impact font, extreme size contrast, one idea per frame, dramatic pauses (60+ frame holds), lots of negative space. Add background music.

---

## Quality Checklist (before declaring done)

- [ ] Video renders without errors
- [ ] No text overlapping other text
- [ ] No text in bottom 15% of frame
- [ ] Key headlines/questions are vertically centered
- [ ] Max 15-20 words per frame (7 for headline slides)
- [ ] All animations use frame-driven timing (no CSS transitions)
- [ ] Every element animates in (no static cuts)
- [ ] Cross-dissolve between all scenes
- [ ] Font variety used (not just Inter everywhere)
- [ ] Music fades in/out smoothly (if present)
- [ ] Music volume lowers during data-heavy scenes (if present)
- [ ] Duration matches the creative brief
- [ ] Core message is clear within first 5 seconds
- [ ] CTA or closing is memorable
- [ ] Data model is clean and reusable (if data-driven)
- [ ] User has reviewed and approved the final version
