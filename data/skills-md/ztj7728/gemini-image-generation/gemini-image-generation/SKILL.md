---
name: gemini-image-generation
description: 'Generate or edit images with Gemini using the Google GenAI SDK. Use when the user asks to create, transform, render, or save one or more images in an OpenClaw skill workflow.'
argument-hint: 'prompt="<image prompt>" output="outputs/image.png" [input="assets/source.png"] [input="assets/source-2.png"] [aspectRatio="16:9"] [imageSize="2K"]'
metadata: {"openclaw":{"emoji":"🎨","requires":{"bins":["node","npm"],"env":["GEMINI_API_KEY","GEMINI_MODEL_ID"]},"primaryEnv":"GEMINI_API_KEY","optionalEnv":"GEMINI_BASE_URL"}}
---

# Image Generation

Use this skill when you need to create one or more image files from a text prompt, or edit one or more existing images with Gemini.

## Requirements


- `~/.openclaw/openclaw.json` must include `$.skills.entries["gemini-image-generation"].enabled` set to `true`.
- `~/.openclaw/openclaw.json` must include `$.skills.entries["gemini-image-generation"].env` with the following keys and values:
- `GEMINI_API_KEY` required
- `GEMINI_MODEL_ID` required
- `GEMINI_BASE_URL` optional

- example `~/.openclaw/openclaw.json`:
```json
{
  ......,
  "skills": {
    "entries": {
      "gemini-image-generation": {
        "enabled": true,
        "env": {
          "GEMINI_API_KEY": "sk-xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
          "GEMINI_MODEL_ID": "gemini-3.1-flash-image-preview",
          "GEMINI_BASE_URL": "https://custom-endpoint.com"
        }
      }
    }
  },
  ......
}
```
- Node.js must be installed in the workspace environment.
- Install dependencies once with `npm install` from the skill root.

## When To Use

- The user asks to generate a new image from a text prompt.
- The user asks to modify, restyle, extend, or otherwise edit one or more existing images.
- The user wants the generated image saved to a workspace file.
- The task should be handled through a reusable OpenClaw skill instead of ad hoc SDK code.

## Procedure

1. Convert the user request into a single clear image prompt.
2. If the user supplied source images, choose or confirm the input file path or paths inside the workspace.
3. If the user specified a target aspect ratio or size, pass them through as `--aspectRatio` and `--imageSize`.
4. Choose an output path inside the workspace unless the user already provided one.
5. For text-to-image, run [generate-image.mjs](./scripts/generate-image.mjs) with `--prompt`, `--output`, and optional image config arguments.
6. For image editing, run [edit-image.mjs](./scripts/edit-image.mjs) with `--prompt`, one or more `--input` values, `--output`, and optional image config arguments.
7. Read the api key from `GEMINI_API_KEY` and the model ID from `GEMINI_MODEL_ID` in the environment.
8. Optionally, read the base URL from `GEMINI_BASE_URL` in the environment for custom endpoints.
9. Return the saved image path or paths to the user.

## Commands

```powershell
node ./.claude/skills/gemini-image-generation/scripts/generate-image.mjs --prompt "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme" --output "outputs/gemini-native-image.png"
```

```powershell
node ./.claude/skills/gemini-image-generation/scripts/generate-image.mjs --prompt "Create a wide cinematic food photo of a nano banana dish in a fancy restaurant with a Gemini theme" --output "outputs/gemini-wide.png" --aspectRatio "16:9" --imageSize "2K"
```

```powershell
node ./.claude/skills/gemini-image-generation/scripts/edit-image.mjs --prompt "Turn this cat into a watercolor illustration eating a nano-banana in a fancy restaurant under the Gemini constellation" --input "inputs/cat.png" --output "outputs/cat-watercolor.png" --aspectRatio "5:4" --imageSize "2K"
```

```powershell
node ./.claude/skills/gemini-image-generation/scripts/edit-image.mjs --prompt "Create an office group photo of these people making funny faces" --input "inputs/person-1.jpg" --input "inputs/person-2.jpg" --input "inputs/person-3.jpg" --output "outputs/group-photo.png"
```

## Notes

- The script prints `TEXT:` lines for model text and `IMAGE:` lines for each saved file.
- The final JSON summary only includes generated image paths and optional image config so prompts, model IDs, and source image paths are not echoed back into logs.
- Saved file extensions follow the returned image mime type. If the requested output path uses a different suffix, the scripts keep the base name and write the file with the returned type instead.
- If the model returns multiple images, the scripts save them as `name-1.png`, `name-2.png`, and so on.
- `edit-image.mjs` supports repeated `--input` flags. You can also pass a comma-separated list to a single `--input` value.
- `edit-image.mjs` infers the source mime type from `.png`, `.jpg`, `.jpeg`, or `.webp`. Use one `--mime-type` for all inputs, or repeat `--mime-type` so it lines up with each `--input`.
- Both scripts accept `--aspectRatio` and `--imageSize`. They also accept the kebab-case forms `--aspect-ratio` and `--image-size`.
- The scripts only send `config.imageConfig` when at least one of those parameters is provided.