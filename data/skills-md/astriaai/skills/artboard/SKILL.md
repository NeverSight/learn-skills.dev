---
name: artboard
description: Legacy alias for the storyboard skill. Use when someone invokes /artboard or asks for the former artboard workflow; explain that it is now Storyboard, then create a text-only cinematic video storyboard in video_prompt and clear the image prompt without generating a grid image.
---

# Artboard is now Storyboard

Tell the user briefly that Artboard is now called Storyboard, then fulfill the
request directly. Do not ask them to restart with another command.

Create a text-only cinematic storyboard from the current draft and references.
Never generate a 4x4 artboard, storyboard image, contact sheet, or first-frame
image.

Write 16 numbered cinematic shots, varying camera scale and angle while keeping
the same references, subject, wardrobe, location, lighting, and grade. Preserve
every `<lora:...>` and `<faceid:...>` token exactly. Give each shot one filmable
action and do not repeat a camera scale twice in a row.

Call `present_generation` exactly once with the complete current generation
draft. Put the completed sequence in `video_prompt`, set `text` to the empty
string, and preserve every other current field, including ordered
`image_reference_urls`. If the current prompt already
contains the completed storyboard or the user asks to generate video from it,
copy that prompt into the video prompt verbatim and omit image prompt text
entirely. Do not emit an `ASTRIA_PROMPT` or `ASTRIA_VIDEO_PROMPT` command.

When the user explicitly asks to generate, use `astria video` with the exact
approved content as `--video-prompt`, omit `--text`, and never create or pass an
artboard image. If the content is still in `prompt.text`, move it byte-for-byte
into `video_prompt` and clear `prompt.text`; do not rewrite it during the
generation step. Pass each raw reference as a repeated `--image-reference` in
its original order.
