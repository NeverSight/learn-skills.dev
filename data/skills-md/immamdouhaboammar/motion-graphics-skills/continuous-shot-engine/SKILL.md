---
name: continuous-shot-engine
description: Plan and build seamless continuous single shot videos with zero hard cuts. Use when creating unbroken cinematic ads, continuous single shot promos, or when connecting scenes with a single shared visual motif or light filament.
---

# Continuous Shot Engine

Builds unbroken single shot motion graphics where scenes transition seamlessly without traditional hard cuts. Inspired by high-end brand spec ads and code-driven 2.5D visual storytelling.

## Core Principles

1. **The Shared Function Invariant**: Every scene hands the exact same visual element to the next scene. Whether it is an orange line of light, a particle thread, a metallic ribbon, or a floating camera tracker, the element is drawn through one shared mathematical function so it remains identical across the entire timeline.
2. **One Shot Visual Flow**: Traditional video edits hide transitions in cuts. The continuous shot engine hides transitions in camera moves: a push-in through a screen, a whip around a corner, a dive into defocus, or a camera swoop from aerial to three-quarter view.
3. **Physical Believability**: Objects that land in the scene must exhibit real physical interaction. Surfaces show bevelled edges, packaging shows tape and soft dents, and contact shadows grow as objects approach the ground plane.

## Beat Sheet Structure (Frame-Exact Timing)

A continuous shot ad must follow a strict beat sheet with microsecond precision. The canonical 21-second structure:

| Scene | Timestamp | Visual Action | Sound Event |
|---|---|---|---|
| S1 | 0.00 to 1.60s | The slam. The light thread rushes toward the camera and slams into place, revealing the primary logo | Deep sub bass hit, glass particle crack, settled ring |
| S2 | 1.60 to 4.80s | Search interface. The logo lifts away, phone arrives on the beat, text types itself, result cards fan out in 3D depth | Keystroke ticks, card fanning whoosh, subtle click |
| S3 | 4.80 to 7.20s | One tap action. Camera glides to the primary action button, line fills the button shape, tap triggers confirmation | Soft button tap, success chime, camera fly-through |
| S4 | 7.20 to 10.00s | Route animation. Drop hits, environment becomes a top-down night scene, line traces transit route to destination pin | Musical drop, low synth riser, destination pin drop |
| S5 | 10.00 to 13.30s | The doorstep. Physical package hovers, light line wraps the package and cools into printed ink, package touches down | Cardboard contact thud, subtle tape stretch, push notification pop |
| S6 | 13.30 to 16.50s | Narrative transformation. Core typography forms, letters filled with product imagery, arrow hooks into the brand smile | Light shimmer, gentle chord swell, reverse sweep |
| S7 | 16.50 to 19.20s | Hero lock. Music cuts to silence for 60ms breath, hero hit triggers logo reveal, slow ambient glow passes beneath | Solo hero hit with isolated frequency space, low resonant ring |
| S8 | 19.20 to 21.20s | End card. Defocus into solitary pinpoint of light, clean creator signature and disclaimer | Final chime tail fading naturally |

## Code Implementation Blueprint

For detailed implementation guidelines and renderer setups, read:
- [references/light-filament-math.md](references/light-filament-math.md) for continuous Bezier interpolation math.
- [references/scene-handovers.md](references/scene-handovers.md) for techniques connecting consecutive scenes without cuts.
