---
name: eli5
description: Create a self-contained HTML picture explainer for beginners. Use for /eli5, modules, tradeoffs, incidents, or big-visual explanations.
argument-hint: "<topic or question>"
---

Explain the topic to someone who knows nothing about it. The request or `$ARGUMENTS` is authoritative.

## Contract

1. Ground the explanation in evidence. Inspect source material for a module, tradeoff, or incident; prefer current primary sources for external facts. Never invent causality. Separate facts and inference, including material uncertainty.
2. Choose one truthful mental model. Remove jargon or define unavoidable jargon beside the picture.
3. Create one self-contained HTML picture explainer: big pictures, few words, no icon-decorated essay.
4. Verify it against evidence and inspect wide and narrow viewports.

## Audience

Assume no background, not low intelligence. Use familiar objects, concrete verbs, and a calm adult tone; never be childish or patronizing. Keep conclusion-changing detail. Ask once only when wrong scope would mislead; otherwise choose the smallest useful scope.

## Visual grammar

- Prefer 3-6 scenes; give each scene or panel one idea and a clear reading order.
- Use diagrams, space, motion, timelines, scales, or before/after states; decoration does not count.
- Use short headings and labels; visuals carry sequence, quantity, ownership, and cause.
- Module: input -> transformation -> output. Tradeoff: gains and losses. Incident: trigger -> propagation -> impact -> recovery, distinguishing facts from inference.
- End with one picture and sentence restating the model.

## HTML artifact

- Use semantic HTML with inline CSS and SVG. Embed assets; no CDN, remote font, hotlink, or build.
- Escape untrusted text. Make it responsive, high-contrast, zoom-safe, and not color-only; honor `prefers-reduced-motion`.
- At narrow widths, recompose horizontal diagrams into stacked scenes; never shrink labels unreadably.
- Give each meaningful visual a text alternative or accessible description using visible labels, `aria-labelledby`, `<figcaption>`, or equivalent.
- Put citations, paths, assumptions, and nuance in "Sources and assumptions" `<details>`.
- Add JavaScript only when interaction teaches more; static content must retain the core explanation.

Use the host HTML artifact surface or a temporary directory such as `mktemp -d "${TMPDIR:-/tmp}/eli5.XXXXXX"`; never add one-shot explainers to the repo.

## Verify and return

Open it in an isolated browser or host preview. Check comprehension, clipping, narrow-screen legibility, and claims; repair defects.

Return the artifact or absolute path, one-sentence takeaway, and material uncertainty. Do not repeat the full explanation in chat.
