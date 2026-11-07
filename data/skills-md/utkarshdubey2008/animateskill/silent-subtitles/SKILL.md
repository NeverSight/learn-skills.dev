---
name: silent-subtitles
description: >
  Burn the user's script in as subtitles and keep the film silent. Use whenever a historical
  animation is rendered or a script line is placed on screen. Never add narration, music, or effects.
---

# Silent subtitles

## Overview

Subtitles are strictly mandatory on every scene. The user's script is the soundtrack and narrative: it is burned directly into the lower 20% of the video frame. The video has no audio speech, music, or sound effects (silent AAC track muxed). Do not draw placeholder badges such as "CAPTIONS ONLY" on screen.

## When to use

Use when cutting scenes from a script and again at render time.

## Steps

1. Read `docs/house-rules.md`.
2. One script line is one scene `narration`, in the user's spelling. Do not paraphrase. Split a line only when it needs a second subtitle line to fit the frame width.
3. Put a non-empty ASCII string in `speech` so the loader accepts the file. The default render does not speak it.
4. Keep icons and portrait labels out of the bottom 20 percent. The disclaimer sits under the subtitle in smaller type.
5. Render from `docs/renderer.md` without `--no-silence`.
6. In the log, confirm you do not see `flite`. Confirm each still shows that scene's line.

## Checks

- Subtitle text matches the script line for that scene.
- No `audio_file` is set.
- The validator still reports an AAC stream. That stream is the silent track the encoder muxes. It is not narration.

## See also

- `docs/renderer.md`
- `docs/house-rules.md`
