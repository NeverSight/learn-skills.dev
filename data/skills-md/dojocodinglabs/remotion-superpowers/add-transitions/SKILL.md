---
name: add-transitions
description: Add professional scene transitions to your Remotion video. Choose from fade, slide, wipe, flip, clock-wipe and light-leak overlays — with spring or linear timing.
---

# Add Transitions — Scene Transition Wizard

You are helping the user add professional transitions between scenes in their Remotion composition. This skill is the Q&A and the creative call (which transition fits which cut). **For the API, follow the official `remotion-markup` skill**: `transitions.md` for `TransitionSeries`, presentations, timing, overlays and duration math, and `light-leaks.md` for light-leak overlays. Don't write transition code from memory.

## Workflow

### 1. Check the Preview Is Running

Studio should already be open (`npx remotion studio`, or `npx remotion studio --no-open` with an in-app browser; open the URL it prints). If not, start it now so the user sees each transition as you add it.

### 2. Audit Current Scenes

Look at the current composition and identify the cut points:

```bash
grep -rlE "Sequence|TransitionSeries|Track" src/ --include="*.tsx" --include="*.ts"
```

List the scenes and ask where the user wants transitions. If the scenes are still a chain of `<Sequence from>` hard cuts, they move into `<TransitionSeries>` with one `<TransitionSeries.Sequence>` per scene, as official transitions.md shows (install `@remotion/transitions` with `npx remotion add @remotion/transitions`).

### 3. Choose Transition Types

Ask about the mood of each cut, then suggest:

| Transition | Effect | Best For |
|---|---|---|
| `fade` | Cross-dissolve between scenes | Universal, subtle; intros, outros, time passing |
| `slide` | Scene slides in from a direction | Energetic, modern; lists, step-by-step, social carousels |
| `wipe` | New scene wipes over old | Dramatic, reveals; before/after |
| `flip` | 3D card flip | Playful, eye-catching; product variants, surprises |
| `clockWipe` | Clock-hand reveal | Creative, unique; countdowns, "later that day" |
| **Light leak** (overlay) | Warm flash of light over a hard cut | Cinematic energy without shortening the video; music drops, montages |

**Slide directions:** `from-left`, `from-right`, `from-top`, `from-bottom`. Slides should follow the visual flow (reading direction, or the direction something on screen is moving).

A light leak isn't a transition between scenes: it's a `<TransitionSeries.Overlay>` placed at the cut, which draws on top of the cut point and **doesn't** shorten the timeline. Build it as official light-leaks.md shows.

### 4. Choose Timing

| Timing | Feel | When |
|---|---|---|
| Linear (`linearTiming`) | Constant speed, mechanical | Wipes, clock wipes, slides that should feel "mechanical" |
| Spring (`springTiming`, `damping: 200`) | Smooth ease-in/ease-out, **no bounce** | Most fades and slides; feels natural |
| Spring with low damping (e.g. 10-20) | Overshoots and settles: a visible bounce | Playful content only, used sparingly |

**Recommended:** spring timing with `damping: 200` for most transitions, at 15-25 frames (0.5-0.8s at 30 fps). Shorts: 8-15 frames.

### 5. Apply and Fix the Duration

Write the `TransitionSeries` exactly as official transitions.md shows, with a `name` on each sequence so the user can edit it in Studio.

**Important:** transitions overlap adjacent scenes, so the total shrinks by the sum of the transition durations (overlays don't change it). Compute it with `getDurationInFrames({ fps })` on each timing object, as official transitions.md shows, and update the `<Composition>` duration or its `calculateMetadata`.

### 6. Common Patterns

- **All fade (cinematic):** the same fade everywhere, clean and professional
- **Slide carousel (social media):** every scene slides in from the right, like swiping
- **Mixed (dynamic):** fade for intro/outro, slide for body scenes, wipe for reveals, a light-leak overlay on the biggest beat. Match the energy of each cut.
- **Beat-synced:** for music videos, land each cut on a beat and keep transitions short

### 7. Check in the Preview

Ask the user to scrub each cut in Studio. Pay attention to:
- Transition speed — too fast feels jarring, too slow feels sluggish
- Direction — slides should follow the visual flow
- Consistency — don't use too many different transitions (2-3 types max)
- Voiceover — a transition shouldn't land in the middle of a spoken word

Adjust `durationInFrames` and `damping` until it feels right. Don't render unless the user asks.
