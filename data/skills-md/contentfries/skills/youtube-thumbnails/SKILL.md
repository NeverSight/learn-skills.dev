---
name: youtube-thumbnails
description: Designs and generates YouTube thumbnails and A/B variants, and reviews existing ones. Use when making a thumbnail, thumbnail variants for Test & compare, or critiquing a thumbnail.
---

# YouTube thumbnails

A thumbnail's job: stand out in the feed, grab attention and open a **curiosity gap** strong enough that people click. The title is the supporting act: it tips the ones still hesitating.

## Image generation

Use the best available model for images with text, today GPT Image 2.5: through Codex CLI's image-gen skill or an API such as fal.ai or OpenAI. Before starting, generate one test image to confirm it works. If the tool doesn't report the model version, note that and carry on.

If nothing works, set it up first: tell the person exactly what to do (install and sign in to Codex CLI, or create an API key and store it in their env or secret manager themselves) and continue once a test image succeeds.

## Steps

To review an existing thumbnail, run the Rules and Checks against it and give 1–3 concrete fixes. To make new ones:

1. **Curiosity gap first.** Get the video's title; with no final title yet, pair each variant with one title candidate. Write one sentence each: the question the viewer should ask, and what they should feel. Every element on the thumbnail serves one of the two.
2. **References: 10–15 from five sources:** the creator's above-average videos; outliers from other channels (far above their channel's median); channels with a similar format but a different topic; the creator's saved inspiration (ask where it is); things outside YouTube (posters, film, ads, album covers). For each, name the mechanism: which question or emotion, created by what. Copy the mechanism, never the content.
3. **Three variants, each a different archetype**, not just a different colour. These are starting points; invent a better archetype when the video calls for it:
   - **Face + hook:** big face with a strong emotion on one side, 2–3 words on the other.
   - **Typography:** text is the main element (50%+ of the frame), smaller face.
   - **Concept:** one absurd or symbolic image that tells the point without words; little or no text.
4. **Generate, run the checks, fix.** Scale or crop each result to exactly 1280×720. Pick up to 3 for YouTube Test & compare, which tests them under one shared title; when replacing a live thumbnail, one of the 3 is the current one, as the control. Describe 1–2 more alternatives (other text, other emotion, no text) in words.

## Rules

- **One main element** the eye finds in 0.3 s. At most 3 elements in total: text, main subject, face; a group of repeated identical figures counts as one. Everything on the canvas carries the point.
- **Text is optional.** Some of the best thumbnails have none. When there is text: short (usually 2–4 words), legible at 120–168 px wide, in the video's language.
- **The thumbnail tells the second half of the story** (question, number, twist), in words and in image alike; the title already tells the first half. If the creator wants the thumbnail to say what the title says, point out once why that usually costs clicks, offer an alternative, then do it their way.
- **2–3 saturated colours** on a flat or simple background. Light backgrounds work; pure white melts into the light-mode feed.
- **Face:** strong emotion, 30–50% of the frame height, looking toward the text or the main element.
- **TV shows the top half first.** Put the point in the top half when that costs the thumbnail nothing. The scene always fills the whole frame.
- **Bottom right holds YouTube's duration badge;** keep that corner plain.
- **Truth:** the thumbnail promises only what the video delivers, and the video pays it off (or promises to) in its first 30–60 s. For an unfilmed video, write down per variant what the video must show to keep that promise.

## Prompt template

When the creator's face is on the thumbnail, attach 1–3 photos of them as identity references. Without photos, recommend the creator send 1–3 sharp photos from different angles, or go faceless: many strong thumbnails have no face.

```
YouTube thumbnail, 16:9, 1280x720, full-bleed.
LAYOUT: <where the main element, text and face sit>.
SUBJECT: <the one main element, concrete>.
PERSON: <identity from the attached photos, emotion, position, plain t-shirt>.
TEXT: "<exact text>", heavy sans-serif, <colour>, readable at 168 px.
BACKGROUND: <flat colour / simple gradient>.
Keep the bottom-right corner plain.
Use the reference photos for the person's identity only; background and props come from this prompt.
Only the elements listed above.
```

To change one part of an image, use a tool with mask support (fal.ai, OpenAI API) so the rest stays untouched.

## Checks before handoff

- **Glance test:** at 120–168 px wide, is there one main element, and is the text readable?
- **Top-half test:** with the bottom half covered, is it clear what this is about (for a no-text concept: does it raise a question), and do I want to see the rest?
- **Pair test:** do thumbnail and title together open a question the video answers?
- **Text** exactly as intended?

When a check fails, remove elements or enlarge the text and regenerate. After 2–3 failed attempts, change the concept.
