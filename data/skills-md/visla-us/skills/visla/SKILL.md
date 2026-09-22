---
name: visla
description: Creates AI-generated videos from text scripts, URLs, PPT/PDF documents, or AI-generated visuals (AIGC) using Visla. Use when the user asks to generate a video, turn a webpage into a video, convert a PPT/PDF into a video, create a video with AI-generated visuals/storyboards/motion video, or check Visla account credits/balance.
argument-hint: <script|url|doc|idea|visual|speech|aigc|aigc-styles|aigc-status|aigc-image|aigc-motion|account|avatar|voice> [args]
metadata:
  clawdbot:
    emoji: ""
    requires:
      env: [ "VISLA_API_KEY", "VISLA_API_SECRET" ]
    primaryEnv: "VISLA_API_KEY"
    files: [ "scripts/*" ]
---

# Visla Video Generation

**Version: 260811-1640**

Create AI-generated videos from text scripts, web URLs, documents (PPT/PDF), or AI-generated visuals (AIGC) using Visla's
OpenAPI. AIGC generates original storyboard images and motion videos for each scene with AI instead of matching stock
footage.

## Before You Start

**Credentials** (NEVER output API keys/secrets in responses):

**IMPORTANT**: Never output API keys/secrets in responses.

1. Check if `~/.config/visla/.credentials` exists (do NOT read it yet).
2. If the file exists, use a **choice-based confirmation** to ask the user:
   "Found saved credentials. Allow reading `~/.config/visla/.credentials`?"
   Options: **Allow** / **No**
3. If the user selects **Allow**: proceed with the command.
4. If the user selects **No**, or the file does not exist:
   Ask the user to provide credentials via one of:
   - Environment variables (`VISLA_API_KEY`, `VISLA_API_SECRET`)
   - CLI arguments (`--key`, `--secret`)
   - Direct input of API key and secret
5. If provided credentials fail with `VISLA_CLI_ERROR_CODE=missing_credentials` or
   `VISLA_CLI_ERROR_CODE=auth_failed`, ask the user to re-enter valid credentials.

Only process local files (scripts/docs) explicitly provided by the user, and remind users to avoid uploading sensitive
data.

- Tell the user: this is a one-time setup (once configured, they won't need to do this again)
- Tell the user: get API Key and Secret from https://www.visla.us/visla-api
- Do not repeat the secrets back in the response.

Credential validity check (practical):

- If credentials exist but running `account` fails with `VISLA_CLI_ERROR_CODE=missing_credentials` or
  `VISLA_CLI_ERROR_CODE=auth_failed`, treat credentials as invalid and ask the user to provide real ones.

File format (bash/zsh):

```bash
export VISLA_API_KEY="your_key"
export VISLA_API_SECRET="your_secret"
```

For PowerShell (temporary session):

```powershell
$env:VISLA_API_KEY = "your_key"
$env:VISLA_API_SECRET = "your_secret"
```

**Script**: `scripts/visla_cli.py` — pure Python standard library (**no third-party dependencies**, no
`pip install`). Runs out-of-the-box on macOS, Linux, and Windows with Python 3.7+.

## Platform Execution

The CLI is a single cross-platform Python script.

**Python command differs by platform** — the interpreter is launched differently:

| Platform | Command |
|----------|---------|
| macOS / Linux | `python3` |
| Windows | `python` (or `py -3` if `python` is not on PATH) |

On Windows, `python3` usually does not exist — always use `python` (or `py -3`). All examples below use
`python3`; substitute `python` on Windows. When unsure, detect first: `python3 --version 2>/dev/null || python --version`.

**macOS / Linux**:

```bash
# With user consent, you may source ~/.config/visla/.credentials
export VISLA_API_KEY="your_key"
export VISLA_API_SECRET="your_secret"
python3 scripts/visla_cli.py <command>
# Or, credentials are auto-detected from ~/.config/visla/.credentials (with user consent):
python3 scripts/visla_cli.py <command>
```

**Windows** (PowerShell/CMD):

```powershell
$env:VISLA_API_KEY = "your_key"
$env:VISLA_API_SECRET = "your_secret"
python scripts/visla_cli.py <command>
```

Windows notes:

- For multi-line or complex scripts, use stdin with `-` (recommended, no temp files):
  ```powershell
  @"
  Scene 1: ...
  Scene 2: ...
  "@ | python scripts/visla_cli.py script -
  ```
- Credentials:
    - The CLI auto-detects `~/.config/visla/.credentials` when present.
    - On Windows the default path is typically: `%USERPROFILE%\.config\visla\.credentials`.


## Commands

| Command                           | Description                                       |
|-----------------------------------|---------------------------------------------------|
| `/visla script <script-or-@file>` | Create video from a script (text or a local file) |
| `/visla url <URL>`                | Create video from web page URL                    |
| `/visla doc <file>`               | Create video from document (PPT/PDF)              |
| `/visla idea <text-or-@file>`     | Create video from an idea                         |
| `/visla visual <file> [file ...]` | Create video from visual resources (images/videos), supports multiple files |
| `/visla speech <file> [file ...]` | Create video from speech (audio/video file), supports multiple files |
| `/visla aigc-styles`              | List available AIGC visual styles                 |
| `/visla aigc <script-or-@file>`   | Create AIGC video with AI-generated visuals (storyboard images + motion videos) |
| `/visla aigc-status <projectUuid>`| Show per-scene AIGC status (storyboard + motion video progress) |
| `/visla aigc-image <projectUuid>` | Generate/regenerate storyboard images for scenes  |
| `/visla aigc-motion <projectUuid>`| Generate/regenerate motion videos for scenes      |
| `/visla account`                  | Show account info and credit balance              |
| `/visla avatar`                   | List available AI avatars                         |
| `/visla voice`                    | List available AI voices                          |

**Important**: For `avatar` and `voice` commands:
- **Run the full CLI command** (`python3 scripts/visla_cli.py avatar` or `python3 scripts/visla_cli.py voice`).
- **You may filter** the output before presenting to the user:
  - For `avatar`: remove `Thumbnail:` lines
  - For `voice`: remove `URL:` lines
- **Categorize and format avatar results as follows:**
  - Group avatars by **gender category** (Female, Male, Neutral, Dynamic)
  - List each avatar name with **(n)** where n = number of looks
  - For each look, show: **Look Name (lookUuid)**
  - Format: `- AvatarName (n): Look1 (uuid), Look2 (uuid), ...`
  - Example:
    ```
    **Female (16):**
    - Emma (5): Blue Dress (1000145), Patterned Dress (1000146), Black Blazer (1000147), Light Gray Blazer (1000148), Emerald Green Pantsuit (1000149)
    ```
- **Categorize voice results by language/region** (e.g., System, US English, Chinese, Japanese, French, etc.)
- **You must NOT omit any items** from the list. The user must see all available avatars/voices, even if the list is long.
- Agents must use the exact ID from the listing when configuring videos.

### Optional Parameters

| Parameter             | Description                                                     |
|-----------------------|-----------------------------------------------------------------|
| `-c, --config <file>` | Path to JSON config file with video options                     |
| `--avatar <id>`       | Avatar ID to use for the video (get list from `avatar` command) |
| `--voice <id>`        | Voice ID to use for the video (get list from `voice` command)  |

#### visual command specific
| Parameter             | Description                                                     |
|-----------------------|-----------------------------------------------------------------|
| `--script, -s <text>`| Script or description text (or @filename)                       |
| `--style <style>`     | Video style: `montage`, `storytelling` (default), `explainer`  |

#### speech command specific
| Parameter             | Description                                                     |
|-----------------------|-----------------------------------------------------------------|
| `--function <func>`   | Speech to video function: `SPEECH_TO_VIDEO_SUMMARY` or `SPEECH_TO_VIDEO_FULL_LENGTH` |

#### aigc command specific
| Parameter             | Description                                                     |
|-----------------------|-----------------------------------------------------------------|
| `--style <style>`     | AIGC visual style (run `aigc-styles` to list; e.g. `cinematic`, `photorealistic`, `anime`, `flat_vector`). Omit to let AI pick. |
| `--auto-motion`       | Automatically generate motion videos after storyboards (default) |
| `--no-auto-motion`    | Stop after storyboard images; review, then run `aigc-motion`   |
| `--to-clip`           | Create and auto-export to a clip in a single step              |
| `--webpage <url>`     | Add a webpage URL as reference material (repeatable)           |
| `--doc <file>`        | Add a PDF/PPT as reference material (repeatable)               |
| `--media <file>`      | Add an image/video/audio as reference material (repeatable)    |

#### aigc-image / aigc-motion command specific
| Parameter             | Description                                                     |
|-----------------------|-----------------------------------------------------------------|
| `--scene <id>`        | Scene ID (repeatable, required; get IDs from `aigc-status`)    |
| `--prompt <text>`     | Override the prompt for the selected scene(s)                  |
| `--aspect-ratio <r>`  | `landscape` / `portrait` / `square`                            |
| `--ref <url\|id>`     | Reference image: a URL or an asset entity ID (repeatable, up to 3) |
| `--force`             | Force regeneration (aigc-image: override scenes that already have a motion video; aigc-motion: overwrite existing motion videos) |
| `--mode <m>`          | (aigc-motion) `prompt_to_video` / `first_frame_to_video` / `first_and_last_frame_to_video` / `ingredients_to_video`. Must match the number of `--ref` images. |
| `--audio` / `--no-audio` | (aigc-motion) Enable/disable generated audio                  |
| `--model <model>`     | (aigc-motion) Generation model (default: `veo_3.1`)            |

All other options (aspect_ratio, pace, burn_subtitles, footage_options, bgm_options, etc.) can be set in the config
file.

**Cleanup**: After video creation completes, delete the config file unless it's intended for reuse.

### Config File Format (JSON)

All video options can be stored in a JSON config file (nested structure matches API request body):

```json
{
  "video_title": "My Video",
  "video_description": "Video description",
  "project_function": "SPEECH_TO_VIDEO_SUMMARY",
  "script_text_mode": "ai_rewrite",
  "doc_usage": "page_by_page_walkthrough",
  "speaker_notes_verbatim": false,
  "target_video": {
    "aspect_ratio": "16:9",
    "video_pace": "fast",
    "burn_subtitles": false,
    "video_duration_in_seconds": 60
  },
  "avatar_options": {
    "use_avatar": false,
    "look_id": 12345,
    "avatar_layout": "smart_composition",
    "enable_auto_wallpaper": true,
    "enable_in_preview": true
  },
  "voice_options": {
    "use_voice": false,
    "voice_id": 1
  },
  "footage_options": {
    "enable_footage": true,
    "use_free_stocks": true,
    "use_premium_stocks": true,
    "use_premium_stocks_getty": true,
    "use_private_stocks": true,
    "private_stock_ids": 123456
  },
  "bgm_options": {
    "enable_bgm": true,
    "use_free_stocks": true,
    "use_premium_stocks": true
  }
}
```

**Note**: `avatar_options.avatar_layout` accepts only: `host_only`, `host_pip`, `smart_composition`.

CLI arguments (avatar, voice) override config file values.

Source of truth for the exact CLI surface: run `python3 scripts/visla_cli.py --help`.

## Script Format

```
**Scene 1** (0-10 sec):
**Visual:** A futuristic calendar flipping to 2025 with digital patterns.
**Narrator:** "AI is evolving rapidly! Here are 3 game-changing AI trends."

**Scene 2** (10-25 sec):
**Visual:** Text: "Trend #1: Generative AI Everywhere." Show tools like ChatGPT.
**Narrator:** "Generative AI is dominating industries—creating content and images."
```

## Workflow

The `script`, `url`, `doc`, `idea`, `visual`, and `speech` commands execute the complete flow automatically:

1. Create project
2. Poll until generation completes (may take a few minutes)
3. Auto-export and return download link

## AIGC Video (AI-Generated Visuals)

The `aigc` command uses the AIGC pipeline: instead of matching your script to stock footage, Visla **generates
original visuals for each scene** — a storyboard image first, then an animated motion video clip. Browse visual styles
first with `aigc-styles`. (AIGC generation is credit- and time-heavier than stock-footage creation.)

Two control modes, set by `--auto-motion` / `--no-auto-motion`:

- **Automatic (default)** — storyboard images **and** motion videos are generated end-to-end, then the video is
  auto-exported. One-shot, like the other commands:
  `/visla aigc "Scene 1: ..." --style cinematic`
- **Manual (`--no-auto-motion`)** — generates storyboard images only, then reports each scene's image and the project
  UUID. Review the frames, optionally regenerate any you dislike, then generate motion videos yourself:
  `/visla aigc "Scene 1: ..." --style anime --no-auto-motion` → `/visla aigc-status <uuid>` →
  `/visla aigc-motion <uuid> --scene <id>`

Add `--to-clip` to create and auto-export to a clip in a single step (the clip is populated when the pipeline finishes).

### Scene-level operations

Use these after an AIGC project exists (the project UUID is printed by `aigc`):

- `aigc-status <projectUuid>` — per-scene status: storyboard + motion video progress, image/video links, and scene IDs.
- `aigc-image <projectUuid> --scene <id> [--scene ...]` — generate/regenerate storyboard images. Pass `--force` to
  regenerate scenes that already have a motion video.
- `aigc-motion <projectUuid> --scene <id> [--scene ...]` — generate/regenerate motion videos. Choose `--mode` to match
  the number of reference images (`prompt_to_video`=0, `first_frame_to_video`=1, `first_and_last_frame_to_video`=2).
  Use `--force` to overwrite existing motion videos.

> Scene IDs come from the `aigc-status` output. Both endpoints pre-check credits and reject early if the workspace
> balance is insufficient.

**Execution Instructions**:

- Inform user that video generation takes some time
- Report progress status periodically during polling

### Timeout Guidance

- This workflow typically takes **3-10 minutes**, but can take **up to ~30 minutes** in the worst case. AIGC videos
  (storyboard images **plus** motion videos) are heavier — allow **up to ~30-45 minutes** in the worst case. Set the
  task/command `timeout` to **>= 30 minutes** for stock-footage videos and **>= 45 minutes** for AIGC (Windows defaults
  are often ~10 minutes and need to be increased). If you cannot change the timeout, warn the user up front and, on
  timeout, ask whether to continue or switch to a step-by-step run.
- If timeout occurs, the CLI returns `project_uuid` in the output. Inform the user they can manually check project
  status and continue later using the Visla web interface or API (e.g. `aigc-status <projectUuid>`).

## Examples

```
/visla script @myscript.txt
/visla script "Scene 1: ..."
/visla url https://blog.example.com/article
/visla doc presentation.pptx
/visla idea "Create a video about machine learning"
/visla idea @my_idea.txt
/visla visual image.jpg
/visla visual photo1.jpg photo2.jpg photo3.jpg
/visla visual image.jpg --script "Description of the images..."
/visla visual image.jpg --style montage
/visla speech interview.m4a
/visla speech podcast.mp3 audio1.mp3 audio2.mp3
/visla speech podcast.mp3 --function SPEECH_TO_VIDEO_SUMMARY

# AIGC: AI-generated visuals (browse styles first)
/visla aigc-styles
/visla aigc "Scene 1: A robot waving hello." --style flat_vector
/visla aigc @script.txt --style cinematic --to-clip

# AIGC manual mode: storyboards first, review, then motion videos
/visla aigc "Scene 1: ..." --style anime --no-auto-motion
/visla aigc-status 1536918152879824988
/visla aigc-image 1536918152879824988 --scene 1536919353067339776 --prompt "Brighter lighting"
/visla aigc-motion 1536918152879824988 --scene 1536919353067339776 --scene 1536919353067339777

/visla account
/visla avatar
/visla voice

# With config file
/visla script "Scene 1: Hello" -c config.json

# With avatar/voice (CLI overrides config)
/visla script "Scene 1: Hello" --avatar avatar_123 --voice voice_456
```

## Supported Document Formats

- **PowerPoint**: `.pptx`, `.ppt`
- **PDF**: `.pdf`

## Supported Media Formats

### Visual Resources (visual command)
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- **Videos**: `.mp4`, `.mov`, `.avi`, `.mkv`

### Audio/Speech (speech command)
- **Audio**: `.mp3`, `.wav`, `.m4a`, `.aac`, `.flac`
- **Videos**: `.mp4`, `.mov`, `.avi`, `.mkv`

## Output Format

- **Start**: Display "Visla Skill v260811-1640" when skill begins
- **End**: Display "Visla Skill v260811-1640 completed" when skill finishes

## Security

The CLI scripts enforce the following safety measures to prevent unauthorized file access:

- **Path traversal**: Paths containing `..` are rejected.
- **System directories**: Access to `/etc/`, `/proc/`, `/sys/`, `/dev/`, `/run/`, `/var/log/` (and Windows equivalents) is denied.
- **Text file extension restriction**: The `@file` syntax in `script`, `idea`, and `visual --script` commands only accepts `.txt`, `.md`, `.srt`, `.vtt`, `.csv` files.
- **Document/media file validation**: The `doc`, `visual`, and `speech` commands validate file extensions against supported formats before upload.
- **Credentials**: The Python CLI auto-detects `~/.config/visla/.credentials` only. No arbitrary credential file paths are accepted.
- **User consent**: The agent must ask for user consent before accessing local files, as specified in the "Before You Start" section.
