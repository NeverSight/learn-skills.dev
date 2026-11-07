---
name: htmlrec
description: Render an HTML/CSS/JS animation to a video file — MP4, or WebM/MOV with a real transparent (alpha) channel — using the `hrec` CLI. Use when the user has an HTML/CSS animation (e.g. one Claude just generated) and wants it as an actual video/mp4, or talks about exporting / recording / saving an animation as video instead of screen-recording it.
allowed-tools: Bash(hrec:*), Write
---

# htmlrec

Turn an HTML/CSS/JS animation into a real video file with the `hrec` CLI. It drives a headless Chromium through a virtual clock and captures every frame, so the output is deterministic and frame-perfect — independent of machine speed. **Never fall back to screen recording; this is the whole point.**

## 1. Preflight the dependencies

Check both tools before rendering:

- **`hrec`** — run `hrec --version`. If it's missing, tell the user to install it with either:
  ```
  cargo install htmlrec
  brew install dsplce-co/tap/htmlrec
  ```
- **`ffmpeg`** — run `ffmpeg -version`. Required (it encodes the captured frames). If missing:
  - macOS: `brew install ffmpeg`
  - Debian/Ubuntu: `sudo apt install ffmpeg`
  - Windows: `choco install ffmpeg`
- **Chrome/Chromium** — nothing to install. `hrec` uses any Chrome already on the system, and otherwise downloads a headless Chromium itself on first run and caches it. Just mention the first render may take a little longer while that happens.

## 2. Get the animation into a standalone file

`hrec` renders a single HTML file. If the animation lives in the conversation, a code block, or an artifact, write it to a self-contained `.html` with the CSS and JS inlined so it runs on its own in a browser — no external build step, no missing assets. There's a minimal sample at `references/example.html`.

## 3. Render

```
hrec render <file>.html -o <out>.mp4
```

Defaults: 1280×720, 60 fps, 5 s. Map the user's intent to flags:

| Flag | Default | Use for |
|---|---|---|
| `-o`, `--output` | `output.webm` | output path; the extension picks the format (see below) |
| `-d`, `--duration` | `5.0` | length in seconds — match the animation's real run time |
| `-f`, `--fps` | `60` | frame rate |
| `--width` | `1280` | viewport width in px |
| `--height` | `720` | viewport height in px |
| `--zoom` | — | CSS zoom factor (e.g. `2.0`, `0.5`) |
| `--zoom-element` | `:root` | CSS selector the `--zoom` applies to |
| `-t`, `--transparent` | off | keep the alpha channel — **requires `.webm` or `.mov`** |

### Output format is chosen by the file extension

| Extension | Codec | Alpha |
|---|---|---|
| `.mp4` | H.264 / yuv420p | No |
| `.webm` | VP9 / yuva420p | Yes |
| `.mov` | ProRes 4444 | Yes |

For a normal video, use `.mp4`. For **transparency / overlay** (alpha channel — e.g. compositing the animation over other footage), output `.webm` or `.mov` **and pass `--transparent`**:

```
hrec render <file>.html -o <out>.webm --transparent
```

`.mp4` cannot carry alpha — combining `--transparent` with `.mp4` is an error.

## 4. Return the result

Give the user the output file path. Offer to adjust duration, size, fps, or format. If the output is transparent, point out it's a WebM or MOV (and that the alpha only shows in a player that supports it — over a plain background it just looks like a normal video).
