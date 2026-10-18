---
name: explain-with-section-clips
description: Use when asked to explain visually with section clips
---

# Explain with Section Clips

A traditional page of grouped sections, where each section's visual is a short looping animation ("clip") in a
small player frame. Each clip shows exactly one idea.

## Use this skill when

- The user asks for a visual explanation of changes with section clips.
- Used by an orchestrator to explain changes visually with section clips.

## Sections

- 3–6 sections. Each: a one-sentence takeaway → one clip → 2–3 short lines → one `ev-more` toggle that names its
  contents (e.g. "The new code · Files touched").
- Group related information inside the toggles: highlighted code, grouped items, status chips, compact tables.

## Clips

- 5–12 seconds, looping, showing one idea: something counting up, a value flowing through steps, a request
  being stopped, a change spreading to its consumers.
- Play only while visible; pause when scrolled away. Play / pause / replay controls and a progress bar.
- At rest (before playing, under reduced motion, in thumbnails) show the **end frame**, which must state the
  result on its own.
- Text inside a clip must stay legible on phones (≥ 13 px at desktop size, scaled up for narrow frames).

## Building it

- Build it as a fragment with the `explainer-kit` skill and draw clips with `EV.clip(el, {duration, setup, draw})`,
  where `draw(t)` sets the whole frame from the time alone (makes seeking, looping and the poster frame free).
- Give each section `id` + `data-toc` so it appears in the chapter list.
