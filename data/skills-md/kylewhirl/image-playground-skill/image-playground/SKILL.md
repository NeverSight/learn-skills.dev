---
name: image-playground
description: Use when Codex should generate or edit an image on macOS by preferring the macOS 26+ `Image Playground Skill` shortcut and falling back to the macOS 15 `Image gen` shortcut plus Playwright when the newer path is unavailable or fails.
---

# Image Playground

Prefer the macOS 26+ `Image Playground Skill` path first. If that path is unavailable or fails, fall back to the macOS 15 `Image gen` path in the same skill.

## macOS 26+ primary path

Install the `Image Playground Skill` shortcut if needed:
[https://www.icloud.com/shortcuts/b1370f8002e3410491331b80383af5c6](https://www.icloud.com/shortcuts/b1370f8002e3410491331b80383af5c6)

Requirements:

- Apple Intelligence enabled
- Image Playground available on the Mac
- ChatGPT extension enabled inside Image Playground
- ChatGPT extension logged into a ChatGPT account

Run it with:

```bash
scripts/run_image_playground_shortcut.sh --prompt "a cozy orange cat in a sunlit window" --style "ChatGPT" --output-path output/cat.png --output-type public.png
```

Available styles:

- `ChatGPT`
- `Oil Painting (ChatGPT)`
- `Watercolor (ChatGPT)`
- `Vector (ChatGPT)`
- `Anime (ChatGPT)`
- `Print (ChatGPT)`

Expected input structure:

```json
{
  "prompt": "a cozy orange cat in a sunlit window",
  "style": "ChatGPT",
  "image_path": "/absolute/path/to/source.png"
}
```

Pass `image_path` only when doing image-to-image generation, and use an absolute path.

The wrapper script writes that JSON to a temporary file, then runs `shortcuts run "Image Playground Skill" -i /absolute/path/to/payload.json`.

If you get `There was a problem running the shortcut.`, open the ChatGPT app, confirm you are logged in, and run the shortcut manually once.

## macOS 15 fallback path

If you are on macOS 15, or if the Image Playground path is unavailable or fails, use the legacy `Image gen` shortcut flow bundled in this skill.

Install the `Image gen` shortcut if needed:
[https://www.icloud.com/shortcuts/53b4fdcffbbc4b0d9482710055b471aa](https://www.icloud.com/shortcuts/53b4fdcffbbc4b0d9482710055b471aa)

Requirements:

- ChatGPT macOS app installed
- ChatGPT macOS app open and logged in
- Playwright browser profile already logged into ChatGPT

Run the generation step with:

```bash
scripts/run_image_gen_shortcut.sh --prompt "a cozy orange cat in a sunlit window"
```

Then use the Playwright download guidance in:

- `references/playwright-download.md`
