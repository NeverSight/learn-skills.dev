---
name: faceless-shorts
description: >-
  Use this skill to create 100% free premium vertical faceless shorts/videos for YouTube Shorts, Instagram Reels, and TikTok. Generates viral scripts (presets + curated knowledge packs + optional local LLM), realistic voiceovers (Edge-TTS), dynamic AI visuals (Pollinations Flux / local ComfyUI / offline procedural), 45 three-stage art styles (pixel art, chalkboard, glow sketch, PS2, comic, flat vector, minimal line, CGI, LEGO, explainer 3D...), premium Post-FX grading (bloom, halation, teal-orange, film grain), 17 scene transitions, Hormozi-style animated karaoke subtitles with neon glow, audio ducking, 5 quality profiles up to 1440x2560@60fps, and renders MP4 videos with zero API cost.
---

# Faceless Shorts Generator Skill

This skill guides you (Claude, Gemini, Antigravity, OpenCode, or any AI assistant) in orchestrating the complete end-to-end production of publication-ready, vertical 9:16 faceless videos **completely for free**.

---

## 1. Capabilities Overview

* **Zero-Cost Stack**: Microsoft Edge-TTS (multilingual neural voices + word boundaries) + Pollinations AI (Flux.1 9:16 visuals) or local ComfyUI + FFmpeg + Pillow. No API keys, no subscriptions.
* **Target Platforms**: YouTube Shorts, Instagram Reels, TikTok (9:16 vertical, 1080x1920 → 1440x2560).

### 1.1 Three-Stage Art Style Engine (`--art-style` / `-a`) — 45 styles in 6 categories
Every style = AI prompt suffix → offline PIL transform → FFmpeg grade.
* **🎬 Cinematic**: `hyperreal`, `cinematic_noir`, `old_style`, `cyberpunk_glitch`, `teal_orange`, `anamorphic_epic`, `documentary`, `noir_bw`, `neon_noir`
* **🎨 Illustration**: `sketch`, `chalkboard`, `glow_sketch`, `comic_art`, `flat_vector`, `minimal_line`, `watercolor`, `oil_painting`, `pop_art`, `blueprint`, `anime`, `storybook`, `ink_wash`
* **🕹️ Retro & Games**: `pixel_art`, `ps2_style`, `crt_retro`, `vaporwave`, `low_poly`, `game_boy`, `lego`
* **🧊 3D & Motion**: `cgi_motion`, `explainer_3d`, `isometric_3d`, `claymation`, `product_render`
* **📰 Texture & Craft**: `paper_craft`, `riso`, `halftone_news`, `steampunk`, `ukiyo_e`
* **⚡ Neon & Future**: `neon_glow`, `synthwave`, `hologram`, `matrix_code`

### 1.2 Premium Post-FX Grade (`--effects` / `-fx`) — 15 effects + 6 packs
Single effects: `bloom`, `halation`, `chroma`, `grain`, `vignette`, `sharpen`, `punch`, `teal_orange`, `dreamy`, `motion_blur`, `vhs`, `vivid`, `anamorphic`, `noir`, `night`.
Packs: `cinematic` (bloom+halation+teal_orange+grain+vignette), `premium`, `dreamy`, `retro`, `clean`, `nofx`. Comma-separable: `-fx bloom,grain`.

### 1.3 Open-Source VFX & Animation Suite (`--vfx` / `-x`)
* **`hollywood`** (Natron `github.com/natrongithub/natron`): multi-pass bloom, chromatic aberration, 35mm grain.
* **`particles`** (Effekseer `github.com/effekseer/effekseer`): cosmic stardust, sparks, electric arcs.
* **`smoke_fire`** (OpenVDB `github.com/academysoftwarefoundation/openvdb`): volumetric embers & smoke dynamics.
* **`svg_hud`** (SVG.js `github.com/svgdotjs/svg.js` & Friction): sci-fi reticles, telemetry gauges, HUD brackets.
* **`mocap`** (FreeMoCap `github.com/freemocap/freemocap`): kinematic tracking points & coordinate radars.
* **`toon`** (OpenToonz `github.com/opentoonz` & Pencil2D): cel-shading with Sobel contour inking.
* **`theatre`** (Theatre.js `github.com/theatre-js/theatre`): bezier spring easing for camera motion.

### 1.4 Scene Transitions (`--transition` / `-tr`) — 17 total
`flash` (white flash cut, default) · `zoom` (impact punch) · `dissolve` · `pixelize` · `blur` (whip) · `radial` · `circle` · `slide` · `wipe` · `smooth` · `diag` · `black` · `gray` · `wind` · `squeeze` · `crossfade` · `cut`.

### 1.5 Camera Motion — 10 Ken Burns moves
`punch_zoom_in`, `dramatic_zoom_out`, `pan_left`, `pan_right`, `vertigo_shake`, `whip_zoom`, `rise_up`, `orbit_sway`, `pulse_heartbeat`, `shockwave_out`.

### 1.6 Quality Profiles (`--quality` / `-q`) — 5 tiers
| profile | resolution | fps | crf | encoder |
|---|---|---|---|---|
| `draft` | 1080x1920 | 24 | 26 | ultrafast |
| `social` (default) | 1080x1920 | 30 | 21 | faster |
| `hd` | 1080x1920 | 30 | 18 | medium |
| `cinematic` | 1080x1920 | 60 | 17 | medium |
| `ultra` | 1440x2560 | 60 | 15 | slow |

Overrides: `--fps 60 --crf 16 --encoder-preset slow`.

### 1.7 Subtitle Styles (`--style` / `-s`) — 13 with 118% word bounce
`hormozi`, `beast_pop`, `neon_cyberpunk`, `crimson_alert`, `sketch_comic`, `minimalist_gold`, `neon_glow` (blur glow), `chalk_classic`, `retro_pop`, `pixel_arcade`, `luxury_cinema`, `horror_bleed`.

### 1.8 Audio Engineering
* **Clean Studio Voiceover**: default is 100% clean voice, zero background sound, mastered to -14 LUFS.
* Optional presets (`--music`): `sub_bass_808`, `dark_tension`, `cinematic_pulse`, `curiosity_ambient` — all procedurally synthesized (zero copyright risk), with frame-accurate transition whooshes and sidechain ducking.

### 1.9 Multi-Language (`--language` / `-l`) — 11 languages
`en`, `hi`, `es`, `fr`, `de`, `pt`, `ja`, `ar`, `ru`, `it`, `id` — native neural voice + native font auto-selection, continuous prosody.

### 1.10 Free Tool Integrations (`faceless-shorts doctor`)
All optional, auto-detected, graceful degradation (never break the core pipeline):
* **Whisper STT** — FFmpeg's built-in whisper.cpp filter: `faceless-shorts transcribe file.mp4 --language en` → local SRT/JSON, 100% offline.
* **ComfyUI** (`github.com/comfyanonymous/ComfyUI`) — `--engine comfyui` for private local GPU image generation on `127.0.0.1:8188`.
* **yt-dlp** (`github.com/yt-dlp/yt-dlp`) — B-roll / reference media sourcing.
* **Ollama / OpenAI-compatible LLM** — free dynamic scriptwriting when a local LLM is reachable.
* **Pexels / Pixabay** — free-tier stock B-roll via env keys.

### 1.11 Script Intelligence
1. Built-in viral templates (8 niches) + language-suffixed presets (`presets/<niche>_<lang>.json`).
2. **Curated knowledge packs** (factual scene scripts for brain, sleep, ocean, Mars...).
3. Optional free local LLM (Ollama) for any topic.
4. Dynamic viral builder for any topic in any of the 11 languages.

---

## 2. Interactive Agent Workflow

### Step 1: Script & Niche Selection
1. Choose a pre-built niche (`fitness`, `dark_psychology`, `stoicism`, `blackhole`, etc.) or pass ANY custom topic via `--topic "your topic"`.
2. Specify language with `--language` (e.g. `--language hi`).

### Step 2: Configure Aesthetics
* **Art style**: `-a pixel_art` / `chalkboard` / `glow_sketch` / `ps2_style` / `comic_art` / `flat_vector` / `minimal_line` / `cgi_motion` / `lego` / `explainer_3d` / ... (`faceless-shorts art-styles` lists all 45).
* **Post-FX**: `-fx cinematic` (pack) or `-fx bloom,grain`.
* **VFX overlays**: `--vfx hollywood,particles,svg_hud`.
* **Transition**: `--transition flash` (default), `zoom`, `dissolve`, `pixelize`, `blur`, ...
* **Quality**: `-q social` (default) or `-q hd` / `cinematic` / `ultra`.
* **Subtitles**: `--style hormozi`, `neon_glow`, `chalk_classic`, `horror_bleed`, ...
* **Audio**: clean voice by default; `--music sub_bass_808` for a sub-bass bed.

### Step 3: Visual Generation Options
* **Option A (Agent-generated)**: generate 9:16 images per scene into `images/<niche>/scene_01.jpg`... then they're picked up automatically (or pass `--images-dir`).
* **Option B (Pollinations Flux)**: default engine, free & keyless.
* **Option C (Local ComfyUI)**: `--engine comfyui` when ComfyUI runs on :8188.
* **Option D (Offline)**: `--offline` → procedural Pillow canvases (zero network).

### Step 4: Execute the Python CLI

```bash
# Premium Black Hole short (cinematic grade + zoom cuts + neon subs)
python -m faceless_shorts generate --topic "black hole" -q hd -fx cinematic -tr zoom -s neon_glow

# Retro pixel-art style with pixel mosaic transitions
python -m faceless_shorts generate --niche mind_blowing_facts -a pixel_art -tr pixelize -fx retro -s pixel_arcade

# Hindi short, offline, chalkboard aesthetic
python -m faceless_shorts generate --topic "ब्लैक होल" --language hi -a chalkboard -s chalk_classic --offline

# Diagnostics & tools
faceless-shorts doctor          # free tool health check
faceless-shorts art-styles      # all 45 styles by category
faceless-shorts effects         # Post-FX effects & packs
faceless-shorts quality         # quality profiles
faceless-shorts transcribe clip.mp4 --language en   # local Whisper SRT
```

### Step 5: Present Companion Metadata Pack
After rendering, report the video path and the viral metadata (`output/*_metadata.json`): YouTube Title/Description/Timestamps/Hashtags, TikTok Caption, Instagram Reels Caption.
