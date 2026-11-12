---
name: animated-video-production
description: "The stylized 3D animation layer for a short-form Google Flow video (Disney/Pixar-style or DreamWorks-style feature-animation CG; default: warm, jewel-toned Pixar look). It adds the look, the character, place and product sheets, the scene-still and clip prompt templates, product mascots, characters speaking on camera and the animated failure locks, on top of the shared video-production pipeline (layout, make.py, gates), which it loads. Use when a video plan's style is 3D feature animation, when continuing a project whose AGENTS.md names this skill, or for a single animated sheet, scene still or clip prompt. Not for claymation (clay-video-production), photoreal ads (photoreal-video-production) or UGC talking heads."
---

# Animated Video Production

Stylized 3D feature-animation CG, 9:16, made with Google Flow.

**Load `video-production` first.** It holds the pipeline: who runs which batch, the gates, the project layout, `init-project.sh` and every `make.py` command. This skill adds only what is specific to animation. Start a project with:

```bash
bash <video-production-dir>/scripts/init-project.sh <client-folder> video-N --style animated
```

Files, loaded only when a phase needs them:

| File | Load it for |
|---|---|
| [references/characters.md](references/characters.md) | Character sheets in animation (phase 2) |
| [references/places.md](references/places.md) | Place sheets in animation (phase 2) |
| [references/product.md](references/product.md) | The product sheet and product mascots (phase 2) |
| [references/scene-still.md](references/scene-still.md) | Writing any still prompt (phase 3) |
| [references/clip-prompt.md](references/clip-prompt.md) | Writing any clip prompt (phase 4), including characters who speak on camera |
| [references/failure-locks.md](references/failure-locks.md) | Before writing prompts, and whenever a result is rejected, with `video-production/references/failure-locks.md` |
| [references/look/](references/look/) | Before writing the first still of any project: nine approved stills from the Mysa song ad (video-6) at the quality bar, each with the exact prompt that made it (`<name>.jpg` + `<name>.md`). Open the images, read the prompts, and match their level of detail |

## Reference sheets

The layouts are shared (`video-production/references/sheets/`); the files above say what changes for animation: one landscape image, stylized CG, neutral light, and no grey studio backdrop leaking into scenes.

- **Sheets only, never scene stills.** Every still takes only the environment, character and product sheets as ingredients, never an earlier scene still: reusing stills degraded quality on video-13. Consistency comes from the environment sheet plus the same Light line for that place in every prompt.
- **Product mascots** (a real product with a face and limbs): edit the client's real product photo, never generate the product or its logo from a description (`product.md`).

## Visual direction

The quality bar is `references/look/`: open those images before the first still of a project. The default look, unless the brief or the user asks for something else, is the one the user loved in the Mysa song ad:

- **Render:** high-end Disney/Pixar-style feature-animation CG, polished like a theatrical release. Sculpted, appealing, slightly stylized characters with big glossy expressive eyes and catch-lights, soft subsurface glow on skin, big sculpted groomed hair (clumped curls), detailed fabric weave and stitching. Never 2D or outlined, never photoreal, never plastic, toy-like or game-like.
- **Colour:** rich, saturated jewel tones in every frame: mustard, magenta, emerald, lavender, burgundy, navy, peach. Bold patterned clothes and set dressing.
- **Light:** warm and motivated by real sources: golden window light, soft warm rim light on hair and shoulders, warm practical lamps, candles, string lights, glowing bokeh. Sad or tense moments stay rich and warm and get a darker, moodier key (one lamp on a rainy night), never grey, desaturated or cold. No cold blue or fluorescent light, no flat light.
- **Sets:** detailed and lived-in: patterned wallpaper, plants, framed photos, brass lamps, throws, wood floors, warm clutter; stores stocked with real-looking products carrying readable fictional labels. Big moments get a magical setting (a terrace under string lights, bougainvillea).
- **Depth in every frame:** a sharp FOREGROUND layer (a table with props, a hand, a product), the subject in the MIDGROUND, a soft lived-in BACKGROUND with bokeh. Shallow depth of field, stated camera height and distance.
- **Acting:** every still is a moment with a specific, strong expression described muscle by muscle ("brows knitted and raised in the middle, she bites her lower lip, shoulders hunched"). Background people are doing something real (reading a label, laughing over wine), never just standing.
- **Science or "inside the body" cutaways:** a cosy fantasy world (warm glowing caves, cute builder creatures, lanterns), never anatomy, organs or diagrams.
- **Product shots:** the client's real pack photo as the reference, the label never redrawn, at real scale (about a fifth of the frame next to a glass), in a warm scene with shallow depth of field; softgels glow amber where light passes through them.

Describe these visible qualities in every prompt instead of relying on a studio name. When a brief asks for a different look (a neutral daylight DreamWorks look, a cold palette), write that instead and keep the light motivated: image models drift into sunset and orange haze when "warm" isn't anchored to a source.

- Keep identity, wardrobe, proportions, scale, location layout and light consistent from sheets through stills to clips. Put relative scale in every prompt with more than one character (for example: the cat's back is at the man's shin).
- 9:16 unless the brief says otherwise. Keep the action in the central 70% of the frame, clear of the bottom and right edges where short-video apps put their buttons.
- Clips: see `clip-prompt.md` for when the frame stays locked and when the camera makes one gentle move.

## Review additions

On top of the shared checklist: the render is 3D CG like the sheets (not 2D or outlined, not photoreal), and a talking clip says its whole line, each word once, with no gaps.
