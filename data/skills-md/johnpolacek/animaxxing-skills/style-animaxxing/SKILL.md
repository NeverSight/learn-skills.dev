---
name: style-animaxxing
description: "Apply the Animaxxing art direction: monochrome editorial design, Rethink Sans and JetBrains Mono, poster type, hairlines, and a curated motion treatment. Use for 'animaxx it', the Animaxxing aesthetic, or a requested Swiss-style monochrome redesign. Use animaxxing for reusable effects while preserving another brand. Not for framework routing or isolated GSAP API questions."
license: MIT
metadata:
  short-description: The Animaxxing look and its motion art direction
---

# Animaxxing Style

The look of [Animaxxing](https://github.com/johnpolacek/animaxxing): black, white, neutral gray, oversized sans against small uppercase mono, hairline rules, scattering letters, and particle-assembled controls.

This skill owns visual design and selects how motion supports it. `animaxxing` supplies the reusable vanilla TypeScript and GSAP recipes. The matching `gsap-<framework>` skill (including `gsap-vanilla`) owns **mount → initial state → intro → settled → outro → end state → unmount**, navigation, interruption, and cleanup timing.

## Choose the scope

- Apply a full restyle only when the request authorizes it; preserve an existing brand otherwise. An explicit Animaxxing redesign needs no further confirmation.
- For the full treatment, install and load `animaxxing` and the matching framework skill, then use the surface choices below. If either is unavailable, identify the missing skill; do not invent its recipes or lifecycle guidance.
- For the design with minimal or no animation, apply the tokens and layout and reduce or omit display effects. Do not require a motion skill or GSAP for a static restyle.
- For effects on another brand, use `animaxxing` directly without applying these fonts, colors, or layout rules.

## Apply and load progressively

For a full restyle, work in this order; for a focused change, load only the relevant reference.

| Task | Reference |
|---|---|
| Colors, fonts, scales, spacing, focus, light/dark themes | [Tokens](references/tokens.md) |
| Poster/Statement/Label/Annotation/BodyCopy roles; header, grid, rail, ledgers, cards | [Typography and layout](references/typography-and-layout.md) |
| Choose effects, map them to surfaces, set the Animaxxing pacing | [Motion art direction](references/motion-vocabulary.md), then the selected references in `animaxxing` |
| Check the changed look | [Verification](references/verification.md); for motion, also use the motion and framework skills' relevant checks |

## Design constraints

- Load variable Rethink Sans (400–800) and JetBrains Mono (100–800) through the project's font pipeline. Use plain CSS tokens, or their Tailwind v4 mapping if the project uses it.
- Neutral token colors only; no decorative shadows or gradients. Use hairlines by default, 2px borders for controls/cards, and tight radii.
- Flush left, ragged right. Poster type may crop deliberately; reading text and annotations never crop. Annotations stay at least 11px; uppercase mono is for metadata, not body copy.
- Reading text stays still. Display text can scatter, split, or wave; the hero subhead is the speak-in exception for the full treatment.
- Ordinary UI motion uses the duration/ease/distance values in the tokens reference; display effects deliberately use larger moves. The motion skill owns implementation and text stability checks.
- Motion is part of this art direction, but the requested intensity takes precedence. Keep the composition readable with all effects omitted and under reduced motion.

## Composition boundary

Select and configure effects; do not copy their implementations into this skill. Load recipe files from the installed `animaxxing` skill by name, without assuming skill folders are siblings on disk. The framework controller calls the selected builders and owns their phase state and cleanup handles. This skill never installs routing hooks, owns a navigation wait, or decides mount, unmount, or replay timing.

## Readable design

Static styles keep meaningful content readable. Invisible entrances use the matching installed framework skill’s `references/initialization.md`; effect rollback belongs to `animaxxing`’s `references/effect-restoration.md`. Do not add unconditional hiding, readiness timers, or route recovery to this style. Preserve the selected choreography when initialization succeeds.
