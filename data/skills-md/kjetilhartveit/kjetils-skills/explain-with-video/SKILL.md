---
name: explain-with-video
description: Use when asked to explain visually with video.
---

# Explain with Video

A short, concise animated explainer, about 60 seconds, played in a large video-like player. By default it is a
live HTML/SVG animation, not a video file: it follows the theme, its text can be searched and copied, and
editing it needs no re-render.

## Use this skill when

- The user asks for a visual explanation of changes with video.
- Used by an orchestrator to explain changes visually with video.

## The video

- About 60 seconds, brisk pacing. 4–7 chapters, each one takeaway with one moving visual.
- Large stage: the full content width, 16:9 on desktop; switch to a taller layout and larger text on phones.
- Captions as real text in a strip under the stage.
- Keep the stage clean: no chapter labels, timestamps or tooltips inside the video or on the scrubber.
- Player controls: play/pause (Space), scrubber, speed, captions toggle, fullscreen.
- Before playing, show a meaningful poster frame (the strongest frame), not an empty stage. Pausing always
  leaves a clean, readable frame.

## Below the player

- One row of chapter names directly under the player: click to jump, the current one highlighted while playing.
- Then a compact details area: a few `ev-more` toggles that name their contents, with visual content
  (highlighted code, chips, compact tables). Keep it small.

## Building it

- Build it with the `explainer-kit` skill (theme tokens, `ev-more`, code blocks).
- Draw every frame with one function `render(t)` that sets the whole picture from the time alone, driven by
  `requestAnimationFrame`. Seeking, speed changes and the poster frame then come for free.
- Only render a real video file (e.g. frames with Python PIL piped to ffmpeg) when the user needs a file to share
  outside the page.
