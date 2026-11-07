---
name: thumbnail
description: Generate and edit finished YouTube thumbnail images from video topics, titles, scripts, and reference photos. Use for thumbnail creation, redesigns, and A/B variants with strong visual hooks and readable composition. Excludes downloading existing thumbnails and fixing thumbnail-saving extensions.
---

# YouTube Thumbnail

Deliver a real image using the built-in image-generation tool. A successful thumbnail communicates the video's specific promise at a glance, fits its audience, and survives a small preview. Concepts or prompts alone are deliverables only when the user asks for them.

## Get enough context to act

Use the conversation's topic, title, audience, payoff, and supplied assets. A clear topic is enough to begin. Ask only for missing information that prevents a truthful, useful image; if there is no topic, ask what the video is about. Do not replace it with a generic "My Next Video."

Respect exact copy, requested style, brand conventions, no-text requests, and variant count. For a video link, inspect accessible title/transcript information before claiming to know its contents. If inaccessible, use an already supplied summary or ask for the topic. Do not invent results or imply that you watched footage you could not access.

Inspect local images with the image-viewing tool before generation. Assign each a clear role: identity/subject, product, style, composition, or edit target. If the user says "use my face" and no portrait is available, request it; do not generate a substitute identity. A reference thumbnail supplies design cues, not permission to invent its subjects or claims for the user's video.

## Choose the hook before styling

For a new design with creative latitude, briefly consider two or three visual ideas internally and choose the strongest. Do not make the user approve a concept unless they asked for that step. For a precise edit, preserve the existing design and change only what was requested.

Evaluate candidate ideas by:

- **Specificity:** Could the same image describe dozens of unrelated videos? Add a concrete object, transformation, tension, or result from this video.
- **Immediate reading:** Can the subject and hook be understood without reading the full title?
- **Title partnership:** Let the title explain context while the image shows evidence or creates an honest unanswered question. Do not repeat the entire title.
- **Visual credibility:** Depict claims supported by the brief. Avoid invented numbers, false before/after results, endorsements, or fake evidence.

When choosing a composition or generating variants, consult [references/art-direction.md](references/art-direction.md). A requested style takes precedence over these defaults.

## Art direct for the feed

Create a clear hierarchy: dominant subject, one supporting clue when useful, optional headline. Favor an unmistakable silhouette, intentional crop, separated foreground/background, and a palette chosen for this topic. Remove small decorations that disappear at preview size.

If text adds information, usually use two to four words in large, heavy, simple lettering. Quote the exact wording in the generation prompt. Prefer one short line or a deliberate two-line stack. Use solid negative space behind text; add an outline or shadow only when needed for contrast. Never override the user's exact copy to meet a word-count preference.

Start with roughly 5% outer breathing room and keep essential content clear of the lower-right duration badge. These are composition defaults, not measured YouTube safe-area rules. Keep faces, hands, product geometry, and logos faithful to supplied references. Avoid automatic shocked faces, neon outlines, arrows, circles, and split screens; use them only when they explain the idea.

## Generate, don't simulate

Use built-in image generation by default and follow its current schema. Read the installed imagegen skill when available. Do not replace a requested image with HTML, SVG, ASCII, or a prompt. Built-in generation does not require an API key; use a CLI/API fallback only if the user explicitly chooses it.

Translate the selected idea into a compact production brief:

```text
Asset: finished YouTube video thumbnail, landscape 16:9.
Video promise: [specific topic and supported payoff].
Visual hook: [one immediately readable idea].
Subject and action: [concrete appearance, gesture, object or transformation].
Composition: [placement, relative scale, crop, depth, text area].
Art direction: [appropriate medium, light, background and palette].
Exact text: "[verbatim headline]", [position and type treatment]; or no text.
Reference roles: [what each image supplies and what must stay faithful].
Preserve/avoid: [user constraints and edit invariants].
Finish: clear at small preview size, generous margins, clear duration area,
no unintended lettering, watermarks, or extraneous objects.
```

One image is the default. Generate each requested variant separately, sequentially; a contact sheet is not a set of usable thumbnails. For controlled A/B variants change one meaningful variable, hold the rest steady, and label files clearly. For exploration, make concepts meaningfully different instead of merely changing colors.

For reference-based generation or edits, use `referenced_image_paths` when all needed images have local paths and the tool supports it, after inspecting them. Otherwise use the smallest `num_last_images_to_include` that includes every needed conversation image within the tool limit. Never use both mechanisms. Omit both for a new image without references. Request missing images again if they cannot all be included.

State edit invariants explicitly, such as "change only the background; preserve face, expression, clothing, headline, and layout." Use the selected result as the edit target. If generation fails, report the failure; never describe an unexecuted prompt as a generated asset.

## Review the actual result

Inspect the output before calling it finished. Check both the full image and its small-preview appearance, around 320 x 180 for landscape, when the viewer supports it. If reduced-size inspection is unavailable, say so when relevant rather than claiming it was tested.

Review in this order:

1. **Meaning:** The image communicates the selected hook and matches the video's promise.
2. **Hierarchy:** One clear focal point; subject and optional text remain readable at small size.
3. **Accuracy:** Exact spelling, numbers and requested copy; faithful identity, anatomy and product details.
4. **Composition:** No accidental cropping, crowded margins, badge collision, or distracting background objects.
5. **Finish:** Clean edges, coherent light and perspective, no unintended lettering or watermark.

Fix an observable defect with a targeted generation edit, preserving what already works. Avoid polishing into a new concept. After two unsuccessful correction attempts, explain the remaining issue and deliver the best available result instead of looping indefinitely. Do not claim improved click-through rate or a winning variant without actual analytics.

## Deliver usable files

Use 16:9 JPG or PNG for ordinary video thumbnails; aim for 3840 x 2160 when supported and honor requested smaller sizes. Shorts and podcast artwork need their own format when requested. Check [YouTube's current thumbnail guidance](https://support.google.com/youtube/answer/72431?hl=en) for upload-specific dimensions and device-dependent size limits rather than treating historical limits as universal.

Read actual file dimensions, format, and byte size with lightweight metadata inspection before calling an export upload-ready. A requested size is not proof of output size. Use image generation for visual corrections; separate image-processing tools require the user's explicit request for that workflow. If exact export constraints cannot be met, disclose the mismatch.

Show the actual returned image with the environment's image-result mechanism. Copy the real output to the user's requested destination or the active project's output folder when project-bound. Use descriptive, versioned filenames such as `desk-setup-thumbnail-v1.png`; preserve originals and earlier versions. Preview-only output may remain at the generator's default location. Never invent paths or save placeholders as finished images.

Keep the final response short: image, saved-file link when available, and any material limitation. For variants, add a brief label identifying the difference. Uploading or changing a live YouTube video requires a user request for that action.
