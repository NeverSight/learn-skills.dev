---
name: doctor
description: Check and configure motiscope — verify ffmpeg/ffprobe are installed and scaffold the API-key config used for optional (stubbed) asset generation. Use for first-time setup, "motiscope isn't working", dependency errors, or /motiscope:doctor.
argument-hint: ""
allowed-tools: Bash, AskUserQuestion
user-invocable: true
---

# motiscope: doctor

Verify dependencies and scaffold config. motiscope's pipeline is pure Python
standard library, so the only hard dependencies are **ffmpeg** and **ffprobe**.

<!-- motiscope:preamble:start -->
## Resolve the scripts directory

```bash
SCRIPTS="${CLAUDE_PLUGIN_ROOT:-}/scripts"
[ -f "$SCRIPTS/mvsetup.py" ] || SCRIPTS="<absolute dir of this SKILL.md>/../../scripts"
```

(Windows: use `python`.)
<!-- motiscope:preamble:end -->

## Run status

```bash
python3 "$SCRIPTS/mvsetup.py" --json
```

The JSON reports `status`, `missing_binaries`, `install_hint`, `platform`, `config_file`, `env_file`, and per-provider key presence.

## If ffmpeg/ffprobe are missing

Do **not** install silently. Ask the user for permission (`AskUserQuestion`), then run the platform command:

- **macOS (Homebrew):** `brew install ffmpeg`
- **Linux:** `sudo apt-get install -y ffmpeg` (or `sudo dnf install ffmpeg`)
- **Windows:** `winget install Gyan.FFmpeg` (or `choco install ffmpeg`)

Re-run `mvsetup.py --check` afterward to confirm (exit 0 = ready).

## Scaffold config

```bash
python3 "$SCRIPTS/mvsetup.py"
```

This creates, if absent:
- `~/.config/motiscope/config.json` — non-secret preferences (`default_target`, `frame_budget`, `resolution`, `frame_format`, `image_provider`, `video_provider`).
- `~/.config/motiscope/.env` (mode `0600`) — **optional** API keys for asset generation, commented out by default.

## API keys (optional)

Asset generation (creating an image an animation needs) is **optional** — no key is required for analysis or code recreation. Image generation is real for **Gemini/Imagen**; the other providers write a labeled placeholder until wired. To configure one, ask the user (`AskUserQuestion`) which provider, and write the key into `~/.config/motiscope/.env`:

| Purpose | Providers (env var) |
|---|---|
| Image | **Gemini/Imagen (`GEMINI_API_KEY`) — implemented**; OpenAI (`OPENAI_API_KEY`), Stability (`STABILITY_API_KEY`), Replicate (`REPLICATE_API_TOKEN`), fal (`FAL_KEY`) |
| Video | Runway (`RUNWAY_API_KEY`), Replicate (`REPLICATE_API_TOKEN`), fal (`FAL_KEY`) |

Image generation works today with **`gemini`** (Imagen). Other providers write a
labeled placeholder until wired.

Reassure the user: keys stay in a local `0600` file, are never printed, never written into generated code, and never committed (the repo `.gitignore` excludes `.env`).

## Report back

Summarize: dependency status, what was scaffolded, and whether any provider keys are configured. If everything is ready, say so in one line and point them at `/motiscope:analyze`.
