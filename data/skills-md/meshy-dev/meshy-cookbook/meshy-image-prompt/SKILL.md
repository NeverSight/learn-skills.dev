---
name: meshy-image-prompt
description: Write the prompt and parameters for a Meshy Text to Image (or Image to Image) task whose output will feed Image to 3D, including A-pose and T-pose characters for rigging and the three-call rig-ready pipeline. Use this skill whenever the user wants a 3D model to start from a generated image, asks for a Meshy image prompt, a concept or reference image "for 3D", a character they can rig or animate, an A-pose or T-pose, a multi-view image set, or asks why an Image to 3D result invented a front, fused the arms or baked shadows into the texture. It covers the subject-first image formula (full object, front or three-quarter view, even lighting, plain background), when to use pose_mode versus pose words, remove_background, generate_multi_view and aspect_ratio, and the Image to 3D settings that produced a riggable mesh. Not for Text to 3D preview prompts (meshy-text-to-3d-prompt), texture or retexture prompts (meshy-texture-prompt), or Meshy Edit (meshy-edit-prompt); it writes prompts and parameters, it does not call the API.
license: MIT
metadata:
  author: meshy-dev
  version: "0.2.0"
---

# Meshy image prompts for Image to 3D

Image to 3D reconstructs what the picture shows and invents the rest, so a good input image shows the whole object, from an angle that exposes the most surface, lit evenly, alone on a plain background. The Text to Image prompt describes that picture. This is also the only route that gives a standard A-pose for rigging: Text to 3D did not produce one in 18 tries, while Text to Image with `pose_mode` followed by Image to 3D did in 3 of 3.

The rules below come from live runs on 2026-10-07 with `nano-banana-pro` for images and `ai_model: "latest"` (Meshy 7.1) for 3D. The formula and `pose_mode` were rechecked on six more image models on 2026-10-16 (see the `ai_model` row). The formula was also run on six props on 2026-10-20 with `gpt-image-2-5-flare` (see "Props"). The rig-ready pipeline was rerun on 2026-11-08 on Smart Topology (`meshy-t2.5`) with the Meshy 7 texture model, and that is now the recommended route (see "Rig-ready characters in three calls"). T-pose was tested on 2026-11-11 through every step, from the image to the animated rig (see "Pose"). [references/evidence.md](references/evidence.md) has the runs; [references/rig-ready-characters.md](references/rig-ready-characters.md) has the full rigging pipeline with costs.

## Workflow

1. **Decide what the image is for.** Feeding Image to 3D (this skill), or a final 2D image (drop the view, background and single-object slots and write composition, camera and lighting mood instead). For a character the user will rig or animate, follow the rig-ready pipeline in step 5.
2. **Write the prompt with the formula.** Subject first, then pose only when it is not set by `pose_mode`, then framing, materials and colors per part, style, and the fixed closing phrase.
3. **Set the parameters** from the table below. Never set `pose_mode` and describe a different pose in the same request. Default to `gpt-image-2-5-flare`, which works on every Meshy plan; suggest `nano-banana-pro` only when the user says they have a Pro plan or above.
4. **Check it.** Run `python3 scripts/check_prompt.py --kind image [--pose-mode a-pose] "…"` (path relative to this skill's directory). It flags missing framing, lighting or background phrases, thin or dense parts, clear glass, pose words that conflict with `pose_mode`, and length.
5. **Say what happens next.** For a rig-ready character: Image to 3D with `model_type: "smart-topology"`, `ai_model: "meshy-t2.5"`, a `target_polycount` from 5,000 to 30,000, `texture_model: "meshy-7"`, `enable_pbr: true`, `texture_resolution: "2k"` and `pose_mode` set to the pose in the image, then Rigging with that task id. For anything else: Image to 3D (textured or mesh-only as the user needs). When the model goes into a game engine, a web viewer or AR, give it a face count: Smart Topology (`model_type: "smart-topology"`, `ai_model: "meshy-t2.5"`, `target_polycount`) generates the mesh at that count, or a standard model takes `should_remesh: true` and a `target_polycount`; otherwise leave them out.
6. **Deliver prompt, parameters, next step and assumptions** in the output format at the end.

## The formula

```
[Subject], [pose, only if not using pose_mode], [full object or full body], [front view or three-quarter front view], centered with space around it, [material and color per part], [style], soft even studio lighting, plain white background, single object, no props, no text
```

Why each slot is there:

- **Full object in view.** A part cropped out of the frame has to be guessed.
- **Front view for characters, three-quarter front view for props.** These angles show the most surface. A single image that showed a rear three-quarter view of a toy robot left Image to 3D to invent the front, and it put a blob inside the glass dome. The image model sometimes draws a prop almost straight on anyway (a lantern and a sword in the prop test); both still converted cleanly.
- **Centered with space around it, at an aspect ratio that fits the object.** At 1:1, a delivery van's cargo box ran off the right edge despite this phrase; at 4:3 the whole van fit.
- **Soft even lighting, plain white background.** Hard shadows and highlights in the image are painted into the model's texture; a cast shadow on the ground becomes part of the model.
- **Single object, no props, no text.** The bare prompt "a knight's helmet" produced a feather plume, a grey background, a cast shadow and a tilted pose. A plume is a dense thin structure that converts badly. Other bare prompts added a lit flame to a lantern, a cartoon face to a car, bushes and a potted plant to a house, and a grey background with a diagonal angle to a sword.
- **Materials and colors per part.** Unlike the Text to 3D preview, this image carries the colors: Image to 3D textures from it.

Tested examples:

- Prop: `A medieval knight's helmet, full object, three-quarter front view, centered with space around it, dark hammered iron dome with a narrow eye slit and a pointed visor, brass rivets, polished steel ridge along the top, light rust in the dents, realistic style, soft even studio lighting, plain white background, single object, no props, no text` (with `aspect_ratio: "1:1"`)
- Prop with thin parts: `A farmhouse dining chair, full object, three-quarter front view, centered with space around it, upright back with five vertical spindles under a curved top rail, square seat, four slightly splayed legs joined by stretcher bars, honey-colored oak with visible grain and a satin finish, realistic style, soft even studio lighting, plain white background, single object, no props, no text` (with `aspect_ratio: "1:1"`; every spindle and stretcher survived Image to 3D)
- Wide prop: `A cartoon delivery van, full object, three-quarter front view, centered with space around it, short boxy body with an oversized rounded cab, glossy mint-green paint, white cargo box at the back, large round headlights, chunky black tires, chrome front bumper, roof rack, stylized style, soft even studio lighting, plain white background, single object, no props, no text` (with `aspect_ratio: "4:3"`)
- Character for rigging, with `pose_mode: "a-pose"`: `A stocky dwarf blacksmith, braided grey beard reaching the belt, leather apron over a red tunic, heavy brown boots, full body, front view, centered with space around it, stylized proportions, soft even studio lighting, plain white background, single character, no props, no text`

## Parameters

| Parameter | Use | Notes |
|---|---|---|
| `ai_model` | `gpt-image-2-5-flare`, `gpt-image-2`, `gpt-image-2-5-sunburst` or `nano-banana-pro` (9 credits) for the final image; `nano-banana-2` (6), `nano-banana-2-lite` or `nano-banana` (3) for drafts | Tested on 2026-10-16 with the two example prompts above, one sample per model. The three GPT Image models followed the formula best: pure white background, little or no shadow, every requested material, nothing added. `nano-banana-pro` and `nano-banana-2` passed, but with light grey backgrounds and soft shadows. `nano-banana` missed two requested details, and `nano-banana-2-lite` added a chainmail neck guard draped onto the floor. Untested: `nano-banana-2-1` on these prompts, and Image to Image or multi-view on any model except `nano-banana-pro`. `gpt-image-2-6-flare` and `gpt-image-2-6-sunburst` (9 credits, added 2026-11-06) followed the formula like the other GPT Image models in the 2026-11-11 T-pose test. The rig-ready pipeline has run end to end from `nano-banana-pro` (2026-10-07) and `gpt-image-2-5-flare` (2026-11-08). `nano-banana-pro` needs a Pro plan or above; the GPT Image models and the other nano-banana models do not. |
| `pose_mode: "a-pose"` or `"t-pose"` | Characters you will rig | Leave pose words out of the prompt. `"a-pose"` gave a clean A-pose with the hands clear for every model requested, and mesh-only Image to 3D kept the arms clear of the torso on every one tested (2026-10-16, one sample each). `"t-pose"` gave a clean T-pose, arms level and palms down, on all five GPT Image models and on `nano-banana-pro`, but `nano-banana-2`, `nano-banana-2-lite` and `nano-banana-2-1` returned the arms angled about 40° down instead (2026-11-11, one sample per model, three on `gpt-image-2-5-flare`); use a GPT Image model or `nano-banana-pro` for a T-pose. On the nano-banana models it fixes the aspect ratio to 3:4 and ignores `aspect_ratio`. `pose_mode` needs a Pro plan only on `nano-banana` and `nano-banana-pro`: a posed `nano-banana` request is generated by `nano-banana-pro`. `nano-banana-2`, `nano-banana-2-lite`, `nano-banana-2-1` and the GPT Image models keep the requested model and work on any plan. The GPT Image models also keep your `aspect_ratio` (`"3:4"` on `gpt-image-2-5-flare` returned a 3:4 A-pose on 2026-11-08); with none set they return square images, so send `"3:4"` for a standing character in an A-pose and `"1:1"` for a T-pose. A T-pose is about as wide as it is tall: at 3:4 the fingertips came within 6 to 23 pixels of the side edges on every GPT image, against 85 to 184 for an A-pose. Nothing was cut off, but at 1:1 there was room around the hands and the mesh came out the same. |
| `aspect_ratio` | `"3:4"` for a standing character, `"4:3"` for a wide object such as a vehicle or a bench, `"1:1"` for anything else | At 1:1 a van was cut off at the right edge; 4:3 fit it (one sample each). Cannot be combined with `generate_multi_view`. |
| `remove_background: true` | Returns a transparent PNG | Only when the user asks; the plain white background in the prompt already converts cleanly. |
| `generate_multi_view: true` | Three cropped views for Multi-Image to 3D | Same 9 credits as one image, 66 to 97 s instead of 24. See the multi-view finding below before choosing it. |

For Image to Image (cleaning up a user's photo, or making multi-views from a single generated image), the same prompt rules apply and `reference_image_urls` or `input_task_id` carries the source. `gpt-image-2-5-sunburst` is the editing-precision model for "change X, keep the rest" edits.

## Pose

For A-pose or T-pose use `pose_mode` and leave pose words out; for any other pose write it in the prompt and leave `pose_mode` unset; never let the two disagree.

- The parameter and the prompt gave equally clean A-poses (arms about 45 degrees from the body, hands clear), and both rigged with no forearm or hand weighted to the torso. The parameter's advantage is length: it leaves the 800 characters for the character. The tested A-pose wording, for when `pose_mode` is not used: "standing in an A-pose, arms straight and angled down about 45 degrees away from the body, hands open and clear of the body, legs slightly apart, facing forward".
- Using both added nothing and drifted the style (photoreal, smaller in frame, a floor shadow).
- T-pose in words, when `pose_mode` is not used, gave a clean T-pose on `gpt-image-2-5-flare` (one run): "standing in a T-pose, arms straight out to the sides at shoulder height, palms facing down, fingers together, legs slightly apart, facing forward".
- On Image to 3D, set `pose_mode` to the pose in the image, or leave it out. Image to 3D re-poses the mesh to its `pose_mode`: a T-pose image with `"a-pose"` came out in an A-pose, and an A-pose image with `"t-pose"` came out with the arms raised partway, about 25° below level. Without `pose_mode` the mesh kept the image's T-pose (2026-11-11, one run each).
- A conflict, `pose_mode: "a-pose"` with "sitting on a stool" in the prompt, produced a blend: A-pose arms, straight legs and a stool between the legs.
- Statues, figurines and 3D prints in a specific pose: describe it body part by body part, body position, then arms, then hands, then head. "Kneeling on one knee, left hand on the knee, right hand holding a staff upright, head turned slightly left" works; "heroic pose" does not.
- Any pose that will go through Image to 3D: keep limbs clear of the body, hands away from the face and torso, and the weight on both feet or on a visible base. Arms against the body are the usual cause of a forearm fused to the torso after rigging.

## Rig-ready characters in three calls

1. Text to Image with `pose_mode: "a-pose"`, `aspect_ratio: "3:4"` and `ai_model: "gpt-image-2-5-flare"` (any plan) or `"nano-banana-pro"` (Pro plan or above): 9 credits. The GPT Image models keep the aspect ratio; the nano-banana models return 3:4 whatever you send.
2. Image to 3D with `model_type: "smart-topology"`, `ai_model: "meshy-t2.5"`, `target_polycount: 30000`, `texture_model: "meshy-7"`, `enable_pbr: true`, `texture_resolution: "2k"` and `pose_mode: "a-pose"`: 15 credits. Meshy T2.5 generates the mesh at the count you set (100 to 30,000, triangles only), so nothing needs remeshing. Use 5,000 for crowds and mobile, 20,000 for a side character, 30,000 for a lead. The tested run (2026-11-08) came out at 31,472 triangles for a 30,000 target in 55 seconds, with base color, metallic, roughness and normal maps at 2K in an 8.3 MB GLB and no non-manifold edges.
3. Rigging with that task id as `input_task_id`, plus `height_meters` for the character's height (default 1.7): 5 credits. Includes walking and running animations.

Total 29 credits, about two minutes. The tested rig had 24 bones, walked and ran cleanly, and had no forearm, hand or other limb fused to the torso. Ask for clothing that ends above the knee or splits between the legs: a long apron or skirt is weighted to both legs and stretches when they separate.

**Which texture model.** Step 2 can paint with Meshy 7 or Meshy N1 at the same 15 credits; the texture model does not change the price. On 2026-11-08 the same A-pose dwarf image went through step 2 once with each (Smart Topology `meshy-t2.5` at 30,000), and both rigged:

| | `texture_model: "meshy-7"`, `enable_pbr: true` | `texture_model: "meshy-n1"` |
|---|---|---|
| Maps | Base color, metallic, roughness and normal at 2K | Base color only, at 2K |
| What it textures from | The input image, plus an optional `texture_prompt` | The input image, or `texture_image_url` as the front view; no `texture_prompt` |
| Tested run | 55 s, 0 non-manifold edges, 8.3 MB GLB | 96 s, 8 non-manifold edges, 4.7 MB GLB |
| Rig | 24 bones, clean walk and run | 24 bones, clean walk and run |
| Use it for | Scenes with real lights, where metal, leather and cloth should look different | Unlit or toon-shaded games, or when file size matters |

Leaving out `texture_model` on `meshy-t2.5` gives Meshy 7, but `enable_pbr` defaults to `false`, so without `enable_pbr: true` you get the base color only. Meshy N1 returns `400` for `enable_pbr: true`, `texture_prompt`, `4k` and `8k`. Meshy N1 has not been tested on a T-pose model; the 2026-11-11 T-pose runs all used Meshy 7.

**A-pose or T-pose.** Both rig cleanly. On 2026-11-11 the same three characters went through this pipeline in each pose: all six rigs had 24 bones and no forearm or hand weighted to the torso, and all six walked and ran. Each rig deforms best near the pose it was made in. In the walk and run, with the arms down, the T-pose rigs stretched the shoulders more and held the arms a little wider. In Jumping Jacks, with the arms overhead, the A-pose rigs stretched the shoulders more. Use A-pose (the default) for characters that mostly walk, run and idle, and T-pose for characters whose animations keep the arms raised. For a T-pose, send `pose_mode: "t-pose"` with `aspect_ratio: "1:1"` in step 1 and `pose_mode: "t-pose"` in step 2. `skeleton_template` (such as `mixamo` or `ue5_mannequin`) and `include_fingers` rigged both poses, and the template keeps the model's pose rather than converting it to the template's, so a template is no reason to choose one pose over the other. The measurements are in [references/rig-ready-characters.md](references/rig-ready-characters.md).

The earlier route still works: a standard model (`ai_model: "latest"`, Meshy 7.1) with `should_texture: true`, `should_remesh: true`, `target_polycount: 30000`, `enable_pbr: true` and `pose_mode: "a-pose"` is 30 credits, 44 in all. From the same image on the same day it rigged just as cleanly, but the model took 127 seconds against 55, had 29 non-manifold edges and came in a 12 MB GLB. Without remesh a standard mesh is 600,000 to 1.4 million faces, over Rigging's limit of 380,000 triangles. Keep it for a character that needs Meshy 7.1's denser surface detail. Rigged GLB and FBX files carry an armature scaled 0.01, so check the height on import. The side-by-side numbers, the other routes and the rig measurements are in [references/rig-ready-characters.md](references/rig-ready-characters.md).

## Props

Six props were tested on 2026-10-20: a lantern, a chair, a longsword, a potted plant, a cottage and a cartoon van. Each formula image (`gpt-image-2-5-flare`) went through textured Image to 3D on `latest`, one sample each. The runs are in [references/evidence.md](references/evidence.md).

- **The 3D followed the image on all six props,** including thin parts that are part of the object's structure: six chair spindles and the stretcher bars, the lantern's loop handle, the van's roof rack and the monstera leaves. The same six ideas on Text to 3D lost the cartoon style, some proportions and some part counts (see `meshy-text-to-3d-prompt`). Prefer this route when a prop's look matters. The image costs 9 credits and shows the design before any 3D is paid for; with textured Image to 3D the total is 39 credits, against 30 for a Text to 3D preview and refine.
- **Leave out dense clusters, not every thin part.** Feathers, plumes, chains and netting are the parts Meshy's error documentation names, and a plume was the problem in the helmet test. A handle, spindles, a rack and leaves converted fine here.
- **Glass.** "Clear glass panes" came out as an open frame with no panes, and the burner seen through the glass was modeled inside. "Frosted glass panes" came out as solid panes with the burner's outline painted on them. A clear glass dome on an earlier toy robot came out opaque white. Image to 3D makes no transparent material, so ask for frosted or tinted glass when the panes should be there.
- **Face counts.** Raw textured meshes ran from 47,804 faces (sword) to 1.6 million (van), and the thatched cottage reached 7.7 million faces in a 303 MB GLB, taking 821 seconds against 47 to 152 for the others. The same cottage image with `should_remesh: true` and `target_polycount: 30000` gave 30,028 faces, a 6.6 MB file, in 195 seconds, at the same 30 credits, and looked the same at viewing size. For a game engine, a web viewer or AR, set both, or generate on Smart Topology (next bullet).
- **Smart Topology props.** On 2026-11-08 a prop image went through Image to 3D with `model_type: "smart-topology"`, `ai_model: "meshy-t2.5"` and `target_polycount: 5000`: 5,111 triangles, no non-manifold edges, 51 seconds, 15 credits. With `texture_model: "meshy-7"` and `enable_pbr: true` it came with base color, metallic, roughness and normal maps at 2K in a 5.9 MB GLB; with `texture_model: "meshy-n1"` (base color only, same price) the GLB was 2.7 MB, which suits an unlit or toon-shaded game. A set piece on `ai_model: "meshy-t2"` at 2,000 faces held its shape too. Every Smart Topology count landed within 2.5% of its target. Static models come back about 1 m on the longest side with the origin at the centre of the bounding box; Resize with `resize_height` (or `resize_longest_side`) and `origin_at: "bottom"` (1 credit, 2 seconds) sets the real size and a base pivot and keeps the PBR maps.

## Single image or multi-view

One image shows one side; everything on the far side is inferred. When the back matters (a backpack, a key, a logo), the tested order of results was:

1. **Best:** generate one image, then Image to Image with `generate_multi_view: true` from it, then Multi-Image to 3D. The views kept the design and the orientation of the back parts consistent.
2. Text to Image with `generate_multi_view: true` directly: the three views disagreed on where a wind-up key sat, and the 3D put it on the wrong side.
3. A single image from an angle that hides the front: Image to 3D invented the hidden side.

Multi-view output is three cropped transparent PNGs (about 340 to 450 by 610 to 690 pixels) rather than one 1024-square image, at the same credit cost. A glass dome came out opaque white in every arm; transparent materials do not survive the conversion.

## Output format

```
Prompt: <the image prompt, under 800 characters>
Parameters: {"ai_model":"gpt-image-2-5-flare","aspect_ratio":"1:1"}   plus pose_mode / remove_background / generate_multi_view when they apply
Next step: Image to 3D   or, for a game engine, web viewer or AR, Image to 3D with model_type smart-topology, ai_model meshy-t2.5 and a target_polycount   or, for rigging, Image to 3D with model_type smart-topology, ai_model meshy-t2.5, target_polycount 30000, texture_model meshy-7, enable_pbr true and pose_mode a-pose, then Rigging
Assumptions: <values you chose that the idea did not give>
```

Keep the prompt itself under 800 characters; two of five long ideas ran over in testing when no length rule was applied.

## Resources

| File | Use it when |
|---|---|
| [references/evidence.md](references/evidence.md) | You need the runs behind a rule: pose test arms, the T-pose test, multi-view test, bare versus formula images, the six-prop test |
| [references/rig-ready-characters.md](references/rig-ready-characters.md) | The user wants a character to rig or animate: the pipeline, costs, the three Image to 3D settings compared, what the rig files contain, rig measurements, clothing advice |
| [assets/meta-prompt-code.txt](assets/meta-prompt-code.txt) | The user is building an app that turns ideas into image prompts with a language model; returns one line of JSON |
| [assets/meta-prompt-plain.txt](assets/meta-prompt-plain.txt) | Same, for a person who will read and paste the result |
| `scripts/check_prompt.py` | Lint a drafted prompt: `python3 scripts/check_prompt.py --kind image --pose-mode a-pose "<prompt>"` |

To run it in code, these Meshy Cookbook recipes take an image or a description and run the steps in Python or TypeScript:

- [Create a textured 3D prop from a text prompt](https://www.meshy.ai/developers/cookbook/recipes/create-textured-3d-prop/): Text to Image, then textured Image to 3D.
- [Generate a 3D character from concept art](https://www.meshy.ai/developers/cookbook/recipes/generate-3d-character/) and [Generate low-poly props with Smart Topology](https://www.meshy.ai/developers/cookbook/recipes/generate-low-poly-props/): Image to 3D from an image you already have.
- [Rig a 3D character with walk and run animations](https://www.meshy.ai/developers/cookbook/recipes/rig-3d-character/), [Animate a 3D character with idle, jump and attack clips](https://www.meshy.ai/developers/cookbook/recipes/animate-3d-character/) and [Play an animated 3D character in a three.js game](https://www.meshy.ai/developers/cookbook/recipes/animate-character-in-threejs/): they rig on the standard route (`latest` with `should_remesh`), not the Smart Topology route recommended above.
- [Make a rigged game character for Unreal with your coding agent](https://www.meshy.ai/developers/cookbook/recipes/game-character-for-unreal/): the Smart Topology route above, run by a coding agent with the Meshy CLI and imported into Unreal Engine.
- [Make low-poly props that match your concept art](https://www.meshy.ai/developers/cookbook/recipes/match-props-to-concept-art/): Image to Image from a style reference, then Smart Topology and Meshy N1.

Related skills: `meshy-text-to-3d-prompt` when the model should come straight from text, `meshy-texture-prompt` for retexturing the result, `meshy-edit-prompt` for changing one part afterwards, `meshy-3d-generation` to run the tasks.
