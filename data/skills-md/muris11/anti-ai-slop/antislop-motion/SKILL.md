---
name: antislop-motion
description: "Animation and interaction rules: motion with a UX reason, a single focal animation, intentional easing and timing, and no template scroll-reveal everywhere. Map to antislop-master section F. Use when adding or auditing motion."
allowed-tools: Read Write Edit Glob Grep
---
# antislop-motion

> Motion rules for anti-ai-slop. Map to **F-1 … F-6** (P2/P3) in `antislop-master`.
>
> Motion is a **magnifier**: it makes the focal element feel important and everything else recede. When everything moves, nothing matters.

---

## The one rule

**Motion serves a decision or a state change.** If an animation doesn't help the user understand *what changed, where to look, or what's next*, it's decoration.

Ask of every animation: *does removing it change what the user understands?* If no — cut it.

## What to avoid

- **Fade-in on every section** as the universal scroll effect. This is the #1 motion tell. (F-1)
- **Scroll-reveal + parallax with no hierarchy** — when all elements animate equally, the page reads as "template". (F-2)
- **Idle float/loop on a hero blob or icon** that loops forever with no signal. (F-3)
- **Pulse-glow on a CTA** that never stops "drawing the eye". (F-4)
- **Micro-animation on every hover** so nothing is special. (F-5)
- **Identical easing/timing on everything** — no sense of weight or purpose. (F-6)

## What to do instead

- **Animate the one thing that matters.** A single entrance, a single state change, a single hover that reveals.
- **Use easing and duration to encode meaning**: fast/snappy for confirmation, slow/purposeful for focus. Make them different by intent, not by accident.
- **Respect reduced-motion.** Any motion system must honor `prefers-reduced-motion` and degrade to instant. (G-9 accessibility)
- **Motion must be interruptible** — a user can leave a state mid-animation without it breaking.

## Honoring purpose

- A **loading shimmer** has a reason (content coming). (G-4)
- A **transition on expand/collapse** has a reason (space is opening).
- A **hover lift on the primary card** has a reason (this is the thing you'd click). (D-6)

---

## Audit checklist

- [ ] Every animation has a UX reason or it is removed. (F-1–F-6)
- [ ] Only the focal element animates. (F-2)
- [ ] Reduced-motion is respected. (G-9)
- [ ] Motion is interruptible.
- [ ] Easing/timing differ by meaning, not by default.

Findings cite the code from `antislop-master` plus one honest reason.
