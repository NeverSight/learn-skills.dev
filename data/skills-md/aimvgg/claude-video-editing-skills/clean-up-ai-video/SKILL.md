---
name: clean-up-ai-video
description: "Finishes AI-generated and real footage one shot at a time. Paints a logo, sign or object out of a moving shot, upscales soft shots, changes the frame rate, adds a film look, and grades and blurs a generated shot until it matches the real footage around it. Use when a shot needs finishing before the final cut, for 'upscale this AI video', 'make it look less AI', 'the generated shots look too clean', 'take the logo off the wall', 'remove the watermark from my own clip', 'sharpen this soft shot', 'convert this to 60 fps' or 'give this a film look'. To put a person into a shot, use v2v-video-to-video-swap instead."
license: Apache-2.0
compatibility: "Needs ffmpeg, network access and Python 3 with numpy and opencv-python-headless. Clean plates need an image API such as OpenRouter and a person matte (MediaPipe, or Apple Vision on macOS). Upscales need a datacenter GPU such as an H100 or H200 rented on Modal. Interpolation needs rife-ncnn-vulkan."
---

# Clean up AI video

Each technique below takes one shot in and gives one out. The upscale and frame rate notes carry measured results from the example. The worked example is the Dylan Patel hype video ([zealous1/dylan-patel-hype-video](https://github.com/zealous1/dylan-patel-hype-video), `RECIPE.md` and `code/`). Its scripts are named below by path. Pick the ones the video needs. `restyle-reference-video` calls into this skill; it also works alone. To put a person into a shot, use `v2v-video-to-video-swap`. Before choosing a model for a transform, check the current leaders on https://aimv.gg/generators. The models named here won in October 2026.

Run every command from the user's project folder, and write every output there. Upscales on a rented GPU and clean plates from an image model are paid runs. Name the model, the price per shot and the shot count, and get a yes before each batch.

## Clean an object, sign or logo out of a moving shot

Only clean footage the user owns or has the right to edit. Never remove a watermark, credit or channel logo from someone else's footage. A visible watermark or content credential that an AI generator put on the user's own output stays unless the generator's terms allow removing it, so check them first, and keep any AI label the posting platform asks for. When the user asks to remove a watermark, ask whose it is before doing anything.

Pick one sharp frame with the object fully in view, usually the first, and ask an image model to remove only the object and change nothing else (the example used GPT Image 2.5 Sunburst, about $0.06 an image). Align the plate to every frame with OpenCV `findTransformECC`, using `MOTION_AFFINE`, or `MOTION_HOMOGRAPHY` when the camera moves in depth, and pass a mask that leaves the subject out so the subject's motion does not pull the fit. Composite the warped plate only inside a feathered box around the object, minus a per-frame person matte from MediaPipe person segmentation, or Apple Vision on macOS. One plate is cheaper and steadier than generating the shot again. Step through every frame where the subject crosses the box. The script is `code/shots/datacenter/post/designify.py` in the example.

## Upscale

Upscale only the softest shots. SeedVR2 7B with the sharp weights (`seedvr2_ema_7b_sharp_fp16`), run through `inference_cli.py` from ComfyUI-SeedVR2_VideoUpscaler at a 1440 short side, then Lanczos down to 1080. At 1080 the model pads to 1088 and leaves a seam on the bottom row. A 90-frame shot at 1080 fits an H100. At 1440, or past 100 frames, use an H200. Test shots took 200 to 280 s each on an H100. The six shipped shots and their tests cost $11.24 of Modal GPU time. A local Apple-silicon run ran out of memory. Measure the win as the variance of the Laplacian per shot at delivery size, before and after. In the example it rose 2x to 2.6x. The script is `code/shots/upscale-sweep/modal_seedvr2.py` in the example.

## Frame rate

RIFE in-betweens (rife-ncnn-vulkan) halve detail on whips, morph across cuts (doubled tags and hands) and melt flashes. If you need 60 fps, render code graphics natively at 60 and interpolate only frame pairs inside one shot. Find the cuts with ffmpeg `scdet` at threshold 7, and repeat the frame at each cut instead of interpolating across it. Compare full exports of both rates side by side before deciding. The example rendered 60 and shipped 30.

## Film look

Measure the reference's per-frame mean luma and borrow its frame-to-frame flicker instead of inventing one. With no reference, use the classic preset without borrowed flicker. Apply an S-curve before lifting blacks, because a lift alone washes the picture out. Scratches live 3 to 14 frames, and dust and hairs one frame. Leave the last 3 frames clean. Values are 8-bit. Floor is the black level out of 255, grain is the noise strength in levels, and weave is in pixels. The script is `code/shots/film/film.py` in the example. Pick a preset from full exports side by side. The example shipped worn.

- match. Borrowed flicker, floor 22, dust 8, scratches 0.35.
- classic. Borrowed flicker, floor 20, dust 10, scratches 0.35, grain 7, weave 1, halation 0.35, vignette 0.35.
- worn. Borrowed flicker plus about 5% random flicker, floor 26, dust 22, scratches 0.6, grain 12, weave 2, halation 0.5, vignette 0.5.

## Look match a generated shot

Grade and blur a generated shot until it measures like the real footage, in three steps from `code/shots/lookmatch.py` in the example. First, per-channel quantile curves. Second, a coarse per-channel gain grid for vignette and light falloff, smoothed over time. Third, the blur (Gaussian, radial zoom or directional motion) whose detail on a 4x4 tile grid best matches the reference. When the generated shot replaces a span of a source clip, use the source frame at the same time as the reference. When it is a new shot with nothing under it, pool frames from the shots on either side, match curves on luma only so the generated hues survive, and skip the gain grid. `v2v-video-to-video-swap` runs the same pass on swapped shots.

## After each transform

Run `check-video-render` on the shot when that skill is installed. Without it, confirm with ffprobe that the frame count and frame rate match the input, and step through the last frames. Record the tool, model, settings and cost per shot in the project, for `write-aimv-recipe` if it is installed.

## About

Made free and open source by [Arcmira](https://arcmira.com), the search engine for what people say in podcasts and videos. This skill is one of the [Claude video editing skills](https://github.com/aimvgg/claude-video-editing-skills), written while making real hype videos and AI music videos. Shipped by [Zeal](https://x.com/zealcaiden).
