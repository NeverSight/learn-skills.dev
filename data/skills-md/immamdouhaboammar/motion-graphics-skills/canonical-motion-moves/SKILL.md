---
name: canonical-motion-moves
description: Choreograph the 10 canonical motion graphics moves with tested GSAP easing curves and durations. Use when animating UI elements, cards, and data callouts with standard moves such as rise, pop, count-up, checklist tick, typewriter, slide-in, blur-in, punch-in, reframe, and bar fill.
---

# The 10 Canonical Motion Moves

Standardized choreography library for motion design with pre-tuned physics and easing equations.

## The Moves Catalog

| Index | Move Name | Visual Description | GSAP Easing | Duration | Typical Usage |
|---|---|---|---|---|---|
| 01 | Rise | Card fades in while moving up 30 to 40 pixels | `power3.out` | 0.60s | Introducing primary UI cards |
| 02 | Pop | Scales up from 0.6 to 1.0 with subtle overshoot | `back.out(2.5)` | 0.45s | Success badges, icons, stickers |
| 03 | Count-up | Numbers roll smoothly from zero to target value | `power2.out` | 1.80s | Financial metrics and counters |
| 04 | Checklist tick | Items appear sequentially with green check marks | `power2.out` | 0.35s stagger | Feature verification lists |
| 05 | Typewriter | Sentence types itself character by character | `steps(n)` | 0.04s per char | Search inputs and terminal logs |
| 06 | Slide-in | Element slides in horizontally from viewport edge | `power4.out` | 0.40s | Notifications and side sheets |
| 07 | Blur-in | Element sharpens from 20px blur to crystal clarity | `power2.inOut` | 0.50s | Background shifts and titles |
| 08 | Punch-in | Whole viewport zooms in 15 percent suddenly | `expo.out` | 0.25s | Climax phrases and key quotes |
| 09 | Reframe | Full frame shrinks to card while new element rises | `power3.inOut` | 0.80s | Multi-step feature demos |
| 10 | Bar fill | Horizontal progress bar fills from 0 to 100 percent | `power1.inOut` | 1.20s | Loading bars and analytics stats |

## Composing Combined Moves

Combine moves to create visual hierarchy:
- Primary hero elements use Pop or Punch-in to capture attention.
- Secondary supporting metadata uses Rise or Slide-in.
- Background atmospheric elements use Blur-in or gentle continuous drifts.

## Code Examples and Recipes

- [references/gsap-recipes.md](references/gsap-recipes.md) for ready-to-run GSAP timeline code snippets.
