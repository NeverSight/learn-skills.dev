---
name: cat-sticker-sheet
description: >-
  Turn one supplied cat photo or clear cat illustration into a finished 3:5
  retro-pop photographic collage sticker sheet with nine head-dominant, face-led
  cat stickers using familiar human props through one simple displacement, plus
  six micro-stickers and 2–3 graphic face-in-cover portrait accents. Use for 猫头贴纸,
  猫咪表情贴纸, pet sticker sheets, or lightly absurd anthropomorphic cat sticker
  generation. Preserve visible breed/type and identity
  anchors; keep human actions optional, and increase visual interest without
  inferring the cat's personality or inventing fantasy lore.
---

<!--
[INPUT]: 依赖一张清晰单猫主体图、references/ 的身份/日常错位/少量 face-in-cover 视觉规则、优先使用的原生生图工具，以及仅在原生生图工具缺席时启用的 GD CLI 兜底
[OUTPUT]: 对外提供一张 3:5 复古摄影拼贴猫咪贴纸版及其可点击绝对文件地址
[POS]: cat-sticker-sheet 的单一执行入口；以「真实猫头 + 普通人类道具 + 一个轻微错位」为主体，用微表情变化和少量图形化套壳肖像提升趣味，防止身体泄露、性格臆测、复杂世界观和过度荒诞
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
-->

# Cat Sticker Sheet

Turn one real cat into a retro-pop photographic sticker family. The cat stays recognizable; ordinary human props create the gentle mismatch, while a few graphic face-in-cover portraits give the sheet memorable visual peaks.

## Hold The Contract

- Produce one flat 3:5 portrait sheet: exactly **9 main stickers + 6 micro-stickers**.
- Arrange the main stickers as **2 large + 4 medium + 3 small** with six separated micro-stickers in the gaps.
- Show the same source cat exactly once in every main sticker and nowhere in the micro-stickers. Make the photographic cat head the dominant subject every time. Hide the neck and body completely behind the primary prop or crop cleanly at the jawline. Show no shoulders, chest, torso, belly, arms, or legs.
- Default to no paws. Only when a held or operated object would otherwise be unreadable, allow one or two small partial front paws. Keep them secondary and never connect them into a visible body or humanoid pose. Head-only does not mean face-in-cover: reserve the clean face-window shell for the specified 2–3 accents.
- Preserve visible breed/type, coat relationships, face markings, ear silhouette, eye colors and orientation, nose, muzzle, and distinctive marks. Never guess pedigree or promise biometric identity.
- Do not infer whether the cat is cute, goofy, obedient, clever, aloof, or any other personality. Use only subtle micro-expressions as temporary acting directions: small changes in eyelid openness, gaze, ear angle, muzzle tension, or head tilt. Change at most two cues per sticker; never alter facial proportions or turn the cues into character diagnosis.
- Build each main sticker from one familiar primary object, one credible cat interaction, and one simple displacement. A recognizable human action may sharpen the idea but is optional. If the joke needs more than one sentence to explain, simplify it.
- Keep the object recognizable, normally constructed, and materially believable. For a face-in-cover accent, it may be enlarged, wrapped, or reshaped into an oversized shell while remaining identifiable at a glance. Do not add an unexpected material, second prop, fantasy role, or secondary gag unless the user explicitly asks.
- Let most props be worn, held, or operated. Use **2–3 face-in-cover portraits** as visual accents: center the photographic cat face in one clean opening of an exaggerated shell that hides or replaces the body. Do not turn all nine pieces into the same face-window construction.
- Treat telephone calls, a black plastic bag used as a hood, a baseball cap, a bath towel, or drinking coffee as calibration examples, never a mandatory inventory.
- Use deliberate low-fi photomontage, high-saturation late-1990s/early-2000s poster energy, one flat sky-blue background near `#279DDA`, and one pure-white die-cut contour around every piece. Make the face-in-cover accents obvious, graphic, and close to surreal portraiture without changing the sheet into a fantasy world. Honor an explicit user color exactly; allow no scenery, gradient, vignette, glow, grain, or lighting falloff.
- Permit zero to two short labels. Quote approved text exactly and allow no other words, logos, watermarks, signatures, account names, or gibberish.
- Use a callable native image-generation tool whenever one is available. Use GD CLI only when the runtime exposes no native image-generation tool at all; a failed, slow, rate-limited, or unsatisfactory native call does not count as tool absence.

## Route The Request

- **Generate:** inspect the cat, write the final prompt internally, generate once, run the minimal delivery check, persist the result, and return only the image preview plus its absolute file path. Never trigger another paid generation from visual review alone.
- **Missing source:** ask for the cat image when the request points to “this cat” but no usable image exists.
- **Multiple cats:** ask which cat should lead when the source does not have one unambiguous subject. Never mix several cats on one sheet.
- **Batch:** make one independent sheet per supplied single-cat image.

Assign every input one role:

- **Subject source:** the only authority for cat identity and the only cat included in generation.
- **User style reference:** may supply medium, palette, or layout cues, never another subject or copied inventory.

## Load Only What Is Needed

- Read `references/style-system.md` for every request.
- Read `references/subject-identity.md` when an image is supplied.
- Read `references/one-step-concepts.md` before writing the nine concepts.
- Read `references/quality-gate.md` before returning a generated result; it is a minimal broken-output check, not an aesthetic scorecard.
- Read `references/gd-cli.md` only after confirming that the runtime exposes no callable native image-generation tool. Do not load or use it while a native tool is available.

Resolve bundled paths relative to this `SKILL.md`.

## Generate

1. **Inspect the source.** Record one subject count and four to eight robust identity anchors. Treat unreadable or hidden traits as unknown.
2. **Write the final prompt.** State the identity anchors, head-first body rule, default flat sky-blue background near `#279DDA` or the user's exact color, palette, 3:5 format, 2/4/3 scale rhythm, nine distinct object-interaction-displacement-micro-expression concepts, each concept's `body treatment: fully hidden behind the prop / clean jawline crop`, optional human actions where useful, 2–3 graphic face-in-cover accents, six cat-free micro-stickers, single white contour, and text boundary. Explicitly forbid scenery, gradients, vignettes, glow, grain, and lighting falloff. Keep it backend-neutral and placeholder-free; do not create a separate plan artifact.
3. **Choose the renderer.** Apply the native-first rule above; use `references/gd-cli.md` only for fallback.
4. **Generate from the real source.** Pass only user-provided or task-required images, with the subject first. On the native route, use `referenced_image_paths` for local inputs or the smallest sufficient `num_last_images_to_include` for conversation-only inputs; never use both mechanisms. On the GD CLI fallback route, follow `references/gd-cli.md`. Never pass the bundled anchor to any renderer.
5. **Check delivery, not taste.** Apply only the three catastrophic checks in `references/quality-gate.md`. Do not enumerate stickers, score prompt adherence, grade style details, compare candidate aesthetics, or regenerate automatically. Renderer variation is acceptable.
6. **Persist and return compactly.** Save the generated image under the active project's `output/cat-sticker-sheets/`, never inside the installed Skill. Return only the image preview and a clickable absolute path to that file. Do not include the internal final prompt, mode, identity summary, review status, or routine quality explanation. Add one brief limitation only when the file is broken, the hero subject is wrong, or the result is severely incomplete; never substitute the internal prompt for a missing image.

## Return Shape

````markdown
**猫咪贴纸排版图**

![Cat sticker sheet](absolute-image-path-or-rendered-image)

**输出文件**

[cat-sticker-sheet.png](/absolute/path/to/output/cat-sticker-sheets/cat-sticker-sheet.png)
````

## Non-negotiable Outcome

Use this as the generation target, not a post-generation rejection checklist: the same real cat, nine photographic cat-head human-prop situations with subtle micro-expressions and no visible bodies, one gentle wrongness per piece, two or three graphic face-in-cover accents, six small accents, and one cohesive flat sticker sheet. Accept normal renderer variation unless one of the three catastrophic delivery checks fails.
