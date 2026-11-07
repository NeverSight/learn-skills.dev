---
name: motion-assets
description: Source, generate, and prepare the real assets that keep a motion-graphics edit from looking generated — sampling the palette from the footage, collecting style references, pulling 3D models/Lottie/SVG/textures/SFX, generating AI stills and b-roll, and the mandatory conform pass that grades every asset into one palette. Use when a scene needs an icon, logo, 3D object, texture, background, screenshot, chart source, sound effect, or generated image/video, and whenever output "looks flat", "looks stocky", "looks AI", or assets came from different places and no longer match.
---

# motion-assets

An animation is only as good as what is in it. Three shapes and a font is a template no matter how well it is eased.

**The rule that governs this whole skill: nothing enters the edit at the color, scale, or texture it arrived in.** Every asset gets conformed. An un-conformed stock asset is the fastest way to make a frame read as assembled rather than designed.

## 1. Sample the palette before sourcing anything

Do this first. Every later decision depends on it.

1. Pull 3–5 stills from the A-roll (`ffmpeg -ss <t> -i in.mp4 -frames:v 1 out.png`).
2. Find the strongest non-skin, non-neutral hue — practical light, wall wash, jacket, product, set dressing.
3. That hue is the accent. Build ground / surface / accent from it per `motion-design`.
4. Write `04-design/tokens.css` **and** `palette.json`. Everything downstream reads these files.

If there is no footage (pure motion piece), take the palette from the brand kit, or from the single strongest reference image — still sampled, never invented.

## 2. Collect references before generating anything

References are the highest-leverage input in the entire pipeline. Two or three images beat any amount of prose.

Ask the user for them. If they have none, go and find them: search the look by name ("Apple-style product animation", "editorial data documentary", "retro terminal UI"), pull frames from videos whose look matches, screenshot competitor sites.

Save each into `03-assets/refs/` **named for what it teaches**:

```
refs/
  glass-transparency.png      ← how transparent the panels should be
  type-pairing.png            ← the display/body relationship
  grain-and-vignette.png      ← the texture treatment
  camera-move.mp4             ← the pacing of the push
```

Naming them this way matters: at design time you attach the one that answers the current question, instead of dumping five images and hoping.

**When a generated result is wrong, attach a reference and say what specifically differs.** "Make it nicer" produces drift. "The glass in ref-1 is more transparent and has a visible edge highlight; match that" produces a fix.

## 3. Source the concrete assets

Per shot, the `assets[]` list in `plan.json` must resolve to real files. Categories and where they come from — full link catalogue in Appendix A.

| Need | Get it from |
|---|---|
| Brand logo | the client, as **SVG**. Never trace a PNG, never let a model redraw a logo. |
| Real product/company logos | official brand/press kits. Models draw outdated or wrong logos — this is a frequent, visible error. |
| Icons | one icon set only, matched to the type weight. Mixing sets is instantly visible. |
| UI screenshots | capture the real thing (Playwright MCP, or a manual screen record). A mocked-up UI that differs from the product is worse than no UI. |
| 3D models | Sketchfab, Poly Haven, NASA's model library, or generate (Meshy, Hunyuan3D, Rodin) |
| PBR textures / HDRIs | Poly Haven, Adobe Substance 3D assets |
| Vector animations | LottieFiles (`.json` / `.lottie`) |
| Maps / globes | Mapbox (needs a token), or a 3D globe in Three.js |
| Charts | real data. If the number is on screen, it must be the true number — verify it, cite the source in `NOTES.md`. |
| Photoreal stills | Midjourney / Nano Banana / GPT Image / Freepik-Magnific, always with a style reference |
| Photoreal motion b-roll | image-to-video (Seedance, Veo, Kling, Luma Ray, Runway) |
| Consistent recurring character/product | train a LoRA (see Appendix A) — reference images alone drift across angles |
| Voiceover | ElevenLabs or a cloned voice; feed it more source audio than feels necessary |
| SFX | a proper library, or generated. Sparse and mixed low. |
| Music | licensed library. Check the license before it reaches a client render. |
| Fonts | licensed and self-hosted. Confirm the license permits video embedding. |

### Generating stills that do not look generated

- Attach a **style reference** and keep the prompt short. A long prompt with no reference produces the model's average taste; a short prompt with a strong reference produces yours.
- Generate the whole set from **one anchor image** rather than prompting each independently — independent prompts are why palettes drift between shots.
- For any subject that recurs, build a **reference sheet** (multiple angles from one identity) and generate from that.
- Upscale before compositing, not after.
- **Check every generated image for text.** Garbled type is the single most recognizable artifact. Crop it out, cover it with real type, or regenerate.

### Generating b-roll that does not look generated

- Prefer **one longer continuous shot** over chaining short clips. Chained first-frame/last-frame joins produce a visible stutter at every seam.
- If you must chain, use the true last frame as the next first frame, then **delete one duplicated frame** at the seam.
- Match the camera language of your real footage — if the A-roll is locked off, do not hand back a drifting orbit.
- Keep generated clips short and cutaway-sized. The longer a generated shot holds, the more the viewer inspects it.

## 4. Conform — the pass nobody does

Every asset, without exception, before it enters a scene:

- [ ] **Re-grade into the palette.** Hue-shift, duotone, or overlay-tint stock and generated images toward `tokens.css`. A stock photo at its original color temperature is visible from across the room.
- [ ] **Match black level and contrast** to the plate.
- [ ] **Add the same grain/texture** the rest of the edit carries.
- [ ] **Normalize scale** — icons on one optical size, logos on one clear-space rule.
- [ ] **Cut out the background** where it should sit in the scene (u2net / `hyperframes remove-background` / Runway), then give it a contact shadow.
- [ ] **Clean the edges** — no white halo from a bad key, no JPEG mush on a logo.
- [ ] **3D**: render with the scene's light direction, matching the shadow direction used everywhere else.
- [ ] **Audio**: normalize, trim the head, and duck under dialogue.

Log the conform in `NOTES.md` for anything non-obvious, so a re-render reproduces it.

## 5. Store it so the next agent can find it

```
03-assets/
  brand/     logo.svg, fonts/, brand.json (hexes, clear-space, don'ts)
  refs/      named-for-what-they-teach.png
  gen/       image.png + prompt.txt beside it (model, seed, style ref)
  3d/        model.glb + renders/
  lottie/    name.json
  sfx/       impact-01.wav
```

`prompt.txt` beside every generated file is not optional. Without it you cannot regenerate a matching variant three weeks later, and the whole set drifts.

## 6. Licensing

Before anything reaches a client deliverable, confirm: fonts licensed for video, music licensed for the platform and territory, stock licensed for commercial use, 3D model license permits redistribution in a render, and no real person's likeness is generated without permission. Record it in `NOTES.md`. This is a client-facing risk, not a technicality.

## When assets are the actual problem

If a frame is well designed and well animated and still looks generated, it is almost always one of these:

1. Flat solid background — no gradient, no texture, no depth layer.
2. Icons from a different family than the type.
3. A stock or generated image left at its original color.
4. A logo the model drew instead of the real SVG.
5. Every asset centered at the same scale on a symmetric grid.

Fix the assets before touching the animation.

---

# Appendix A · Asset source catalogue


Verify pricing and licensing at the source — both change. Links are canonical homepages; anything marked `~` is a search target rather than a URL to trust blindly.

## 3D models and scenes

| Source | URL | Notes |
|---|---|---|
| Sketchfab | https://sketchfab.com | Huge library; filter to **Downloadable + free license**. Check the license per model. |
| Poly Haven | https://polyhaven.com | CC0 models, HDRIs, PBR textures. No attribution required. Best default. |
| NASA 3D Resources | https://science.nasa.gov/3d-resources/ | Free spacecraft, terrain, mission assets. Often split into many parts — parent them to one null before animating. |
| Adobe Substance 3D Assets | https://substance3d.adobe.com/assets | Materials; a large free tier. Drops straight into After Effects' 3D layers. |
| Meshy | https://meshy.ai | Text-to-3D and image-to-3D, plus texturing and humanoid/quadruped rigging with a stock animation library. |
| Hunyuan3D (Tencent) | https://huggingface.co/tencent | Open-weights image-to-3D. Geometry is good; texturing is the weak point. |
| Hyper3D / Rodin | https://hyper3d.ai | Text/image to 3D, available as an MCP inside the Blender integration. |
| Mesh-to-Motion | ~ search "mesh to motion rig" | Rigging for non-humanoid meshes (birds, creatures) that humanoid riggers refuse. |

**Multi-view trick:** a single front image produces a wrong back. Generate 90°/180° turns of the subject first, then feed the model 3–4 views. This is the difference between a usable asset and one you can only shoot from one angle.

## Textures, HDRIs, backgrounds

- Poly Haven — https://polyhaven.com (CC0 HDRIs + PBR)
- ambientCG — https://ambientcg.com (CC0 materials)
- Unsplash / Pexels — https://unsplash.com , https://pexels.com (free photos; still re-grade them)

## Vector animation

- LottieFiles — https://lottiefiles.com (browse), https://app.lottiefiles.com (editor)
- Remotion Lottie support: `npx remotion lottie` / `@remotion/lottie`
- HyperFrames: the `lottie` adapter skill covers deterministic seeking

Lotties are tiny, resolution-independent, and re-colorable — recolor them to `tokens.css` rather than using them as shipped.

## Icons and fonts

| Source | URL |
|---|---|
| Google Fonts | https://fonts.google.com |
| Fontshare | https://fontshare.com (free for commercial use) |
| Lucide icons | https://lucide.dev |
| Phosphor icons | https://phosphoricons.com |
| Simple Icons (brand marks) | https://simpleicons.org |

Use **one** icon family per project, matched to the type weight. For real company logos use the company's own brand kit — never a model's redraw.

## AI images

| Tool | URL | Best at |
|---|---|---|
| Midjourney | https://midjourney.com | Aesthetic quality; style references are its superpower (`--sref`) |
| Google AI Studio / Gemini image | https://aistudio.google.com | Strong prompt adherence, character/subject consistency, editing |
| Freepik + Magnific | https://freepik.com , https://magnific.ai | Many models side by side, upscaling, camera-angle change, spaces/node canvas |
| Higgsfield | https://higgsfield.ai | Multi-model image + video, MCP integration into agents |
| Replicate | https://replicate.com | API access to most open models |
| fal.ai | https://fal.ai | Fast serverless inference; also runs LoRA training |
| ComfyUI | https://comfy.org , https://github.com/comfyanonymous/ComfyUI | Local, free, node-based, full control; runs your own LoRAs |

## AI video

| Tool | URL | Notes |
|---|---|---|
| Runway | https://runwayml.com | Video-to-video restyling, object replacement, background removal, multi-shot edits |
| Luma Dream Machine | https://lumalabs.ai/dream-machine | Start-frame + end-frame interpolation |
| Kling | https://klingai.com | Image-to-video |
| Google Veo | via https://aistudio.google.com / https://labs.google | Native audio generation |
| Seedance | via Higgsfield / fal / Replicate | Long single-take shots — fewer seams than chaining |

**Always prefer one long take over stitched clips.** Every stitch is a visible hitch.

## Audio

| Need | Source |
|---|---|
| Voiceover / cloning | ElevenLabs — https://elevenlabs.io |
| Local TTS | `npx hyperframes tts` (Kokoro), or Piper |
| Music (licensed) | Epidemic Sound https://epidemicsound.com , Artlist https://artlist.io |
| SFX (free) | Freesound https://freesound.org (check per-file license) |
| Transcription | Whisper — https://github.com/openai/whisper , whisper.cpp — https://github.com/ggerganov/whisper.cpp , or `npx hyperframes transcribe` |

## Data and web capture

| Need | Tool |
|---|---|
| Real screenshots of a live site/app | Playwright MCP — https://github.com/microsoft/playwright-mcp |
| Maps, satellite, 3D city fly-throughs | Mapbox — https://mapbox.com (free token tier) |
| Charts | real source data; render with Remotion + a chart lib, or the `dataviz` skill |

## Utilities

| Need | Tool |
|---|---|
| Anything video, on the command line | FFmpeg — https://ffmpeg.org |
| Background removal | u2net / rembg — https://github.com/danielgatis/rembg , `npx hyperframes remove-background`, or Runway |
| Upscaling | Topaz — https://topazlabs.com , or Magnific |

## Consistent subjects: train a LoRA

When a face, product, or style must be identical across dozens of shots, reference images are not enough — they drift the moment the angle or lighting changes. Train a small LoRA instead.

**Shape of the job:**
1. Collect 15–35 varied, high-quality images of the subject (angles, lighting, distances). Quality and variety beat count.
2. Pick a **rare trigger word** — never a common word like `face` or `style`, or the model will fire on ordinary prompts. Use something like `mkxr_person`.
3. Train against a base model (Flux, SDXL, Qwen-Image and similar). Roughly 1000 steps for a subject is a normal starting point.
4. Train on rented GPU (fal.ai, Replicate) rather than locally unless you have the hardware — minutes and a couple of dollars versus hours.
5. Output is a `.safetensors` file. Drop it in ComfyUI's `models/loras/`, load it in the workflow, set strength ~0.8–1.0, and include the trigger word in the prompt.

**Where it pays off:** thumbnails with your own face, a client's product across a campaign, one illustration style across a series, a recurring character in a short-form series.
