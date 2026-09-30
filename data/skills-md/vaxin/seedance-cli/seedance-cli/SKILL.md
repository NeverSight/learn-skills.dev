---
name: seedance-cli
description: 'Use the seedance CLI to generate, track, download, and manage Seedance 2.0/2.5 AI videos from the terminal. Covers all subcommands (generate, extend, edit, status, download, list, config), flag reference, model differences (2.0 vs 2.5), workflow patterns, CI/CD integration, and error handling. Use when generating a video, extending or editing a video, checking task status, downloading results, configuring defaults, or building automated pipelines with Seedance.'
license: MIT
user-invocable: true
user-invokable: true
tags: ["cli", "terminal", "automation", "pipeline", "seedance-20", "seedance-25"]
metadata: {"version": "1.3.0", "updated": "2026-08-20", "parent": "seedance-20"}
---

# seedance-cli

Command-line interface for **Seedance 2.0/2.5** video generation on Volcengine Ark.

Binary name: `seedance`. Written in Rust. Config stored at `~/.config/seedance/config.toml`. Task history in local SQLite at `~/.config/seedance/tasks.db`.

> The same repo also ships a `seedream` binary for image generation — see the `seedream-cli` skill.

---

## Quick Start

```bash
# 1. Configure API key (interactive)
seedance config init

# 2. Generate a video (text-to-video)
seedance generate "A cat sits on a windowsill watching rain fall outside"

# 3. Generate and wait for result
seedance generate "Sunset over mountain lake, slow drone pullback" --wait

# 4. Generate with full control
seedance generate "Product bottle on marble surface, slow orbit" \
  --model standard --duration 8 --ratio 16:9 --resolution 1080p --wait
```

---

## Installation

```bash
# From source
cargo install --path .

# Verify
seedance --version
```

---

## Environment


| Variable      | Purpose                                |
| ------------- | -------------------------------------- |
| `ARK_API_KEY` | API key (overrides config file if set) |


Priority: `ARK_API_KEY` env var > `config.toml` api_key.

---

## Commands

### `seedance generate` — Create a Video

The core command. Supports T2V, I2V, V2V, and R2V workflows.

```
seedance generate <PROMPT> [OPTIONS]
```

**PROMPT** can be a literal string or `@file.txt` to read from a file.

#### Generation Options


| Flag                  | Short | Default    | Description                                                  |
| --------------------- | ----- | ---------- | ------------------------------------------------------------ |
| `--model`             | `-m`  | `standard` | Model: `standard`/`fast` (2.0), `2.5` — or a raw Ark model ID |
| `--duration`          | `-d`  | `5`        | Duration in seconds. 2.0: 4–15. 2.5: 4–30, or `-1` (model picks) |
| `--ratio`             | `-r`  | `16:9`     | Aspect ratio (`16:9` `9:16` `4:3` `3:4` `21:9` `1:1` `adaptive`) |
| `--resolution`        |       | `1080p`    | Resolution (`480p` `720p` `1080p`). **2.5 supports 480p/720p only** |
| `--output-format`     |       |            | Output container: `mp4` (default) or `mov` — 2.5 only        |
| `--seed`              |       |            | Random seed for reproducibility                              |
| `--watermark`         |       | `false`    | Add watermark                                                |
| `--audio-gen`         |       | `false`    | Enable native audio generation                               |
| `--return-last-frame` |       | `false`    | Return the last frame as an image                            |
| `--callback`          |       |            | Webhook callback URL                                         |
| `--web-search`        |       | `false`    | Enable web search tool (text-only input)                     |
| `--service-tier`      |       |            | Service tier: `flex` for offline inference                   |


#### Material Inputs (I2V / V2V / R2V)


| Flag            | Short | Repeatable | Max | Description                         |
| --------------- | ----- | ---------- | --- | ----------------------------------- |
| `--image`       | `-i`  | Yes        | 9   | Image reference (URL or local path) |
| `--video`       | `-v`  | Yes        | 3   | Video reference (URL or local path) |
| `--audio`       | `-a`  | Yes        | 3   | Audio reference (URL or local path) |
| `--first-frame` |       | No         | 1   | First frame image (role: `first_frame`) |
| `--last-frame`  |       | No         | 1   | Last frame image (role: `last_frame`)   |


Total files across all types: max 12 (Rule of 12).

Local files are automatically converted to base64 data URIs. Supported formats: JPG, PNG, WEBP (images), MP4, MOV (video), MP3 (audio).

**Asset URLs:** Virtual avatars and authorized real-person assets can be passed via `asset://<asset-id>` to any `--image`, `--video`, or `--audio` flag.

#### Wait & Output Options


| Flag              | Short | Default | Description                                     |
| ----------------- | ----- | ------- | ----------------------------------------------- |
| `--wait`          | `-w`  | `false` | Wait for completion and auto-download           |
| `--output`        | `-o`  |         | Output file path (default: `seedance_<id>.mp4`) |
| `--timeout`       |       | `300`   | Max wait seconds (with `--wait`)                |
| `--poll-interval` |       | `10`    | Poll interval seconds                           |
| `--strict`        |       | `false` | Exit code 2 on timeout (for CI)                 |


#### Output Format Options


| Flag      | Short | Description                                       |
| --------- | ----- | ------------------------------------------------- |
| `--quiet` | `-q`  | Quiet mode: only print task_id or final file path |
| `--json`  |       | JSON output                                       |


---

### `seedance extend` — Extend or Bridge Videos

Extend a video forward/backward, or bridge 2–3 clips into one continuous video. Pass local video files directly. Videos longer than `min(5s, --duration)` are automatically trimmed from the end before upload（需要安装 ffmpeg）.

> With `--model 2.5` this submits a **native `extend` task** instead: no 5s trimming (up to 30s total across clips), ratio forced to `adaptive`, duration 4–30 or `-1`.

```
seedance extend --source-video <VIDEO>... <PROMPT> [OPTIONS]
```

Pass 1 video for forward/backward extension, or 2–3 videos for multi-clip bridging.

| Flag                  | Short | Default    | Description                                                   |
| --------------------- | ----- | ---------- | ------------------------------------------------------------- |
| `--source-video`      | `-s`  | *(required)* | Source video file (1–3, repeatable). Auto-trimmed if too long |
| `--model`             | `-m`  | `standard` | Model variant                                                 |
| `--duration`          | `-d`  | `5`        | Duration (4–15s)                                              |
| `--ratio`             | `-r`  | `16:9`     | Aspect ratio                                                  |
| `--resolution`        |       | `1080p`    | Resolution                                                    |
| `--audio-gen`         |       | `false`    | Enable audio generation                                       |
| `--watermark`         |       | `false`    | Add watermark                                                 |
| `--return-last-frame` |       | `false`    | Return last frame (for chaining further extends)              |
| `--seed`              |       |            | Random seed                                                   |
| `--image`             | `-i`  |            | Additional image reference (repeatable)                       |
| `--wait`              | `-w`  | `false`    | Wait and auto-download                                        |
| `--output`            | `-o`  |            | Output file path                                              |
| `--timeout`           |       | `300`      | Max wait seconds                                              |
| `--strict`            |       | `false`    | Exit 2 on timeout                                             |
| `--quiet` / `--json`  |       |            | Output format                                                 |

**Examples:**

```bash
# Forward extension (auto-trims if video > 5s)
seedance extend -s input.mp4 "角色走出房间，镜头跟随" --duration 8 --wait

# Backward extension
seedance extend -s source.mp4 "向前延长视频1，镜头从远处推近" --wait

# Bridge 3 clips (each auto-trimmed to min(5s, duration))
seedance extend -s clip1.mp4 -s clip2.mp4 -s clip3.mp4 \
  "视频1打开门，进入室内，接视频2，镜头推进，接视频3" \
  --duration 10 --audio-gen --wait

# Chain generation with return-last-frame
seedance generate "开场：日出" --wait -o opening.mp4
seedance extend -s opening.mp4 "中段：城市苏醒" --duration 8 --wait -o middle.mp4
seedance extend -s middle.mp4 "结尾：人潮涌动" --duration 8 --wait -o ending.mp4
```

---

### `seedance edit` — Edit an Existing Video

Edit a completed video: replace subjects, add/remove objects, repaint regions. Automatically resolves the source video URL from task ID.

> With `--model 2.5` this submits a **native `edit` task**: duration/ratio follow the source video automatically (`--duration`/`--ratio` ignored).

```
seedance edit <SOURCE_TASK_ID> <PROMPT> [OPTIONS]
```

| Flag                 | Short | Default    | Description                             |
| -------------------- | ----- | ---------- | --------------------------------------- |
| `--model`            | `-m`  | `standard` | Model variant                           |
| `--duration`         | `-d`  | `5`        | Duration (4–15s)                        |
| `--ratio`            | `-r`  | `16:9`     | Aspect ratio                            |
| `--resolution`       |       | `1080p`    | Resolution                              |
| `--audio-gen`        |       | `false`    | Enable audio generation                 |
| `--watermark`        |       | `false`    | Add watermark                           |
| `--seed`             |       |            | Random seed                             |
| `--image`            | `-i`  |            | Image for replacement/addition (repeat) |
| `--audio`            | `-a`  |            | Audio reference (repeatable)            |
| `--wait`             | `-w`  | `false`    | Wait and auto-download                  |
| `--output`           | `-o`  |            | Output file path                        |
| `--timeout`          |       | `300`      | Max wait seconds                        |
| `--strict`           |       | `false`    | Exit 2 on timeout                       |
| `--quiet` / `--json` |       |            | Output format                           |

**Examples:**

```bash
# Replace subject
seedance edit cgt-abc123 "将视频1中的香水替换成图片1中的面霜，运镜不变" \
  --image cream.jpg --duration 5 --audio-gen --wait

# Modify attribute
seedance edit cgt-abc123 "将面霜颜色修改为白色" --ratio 16:9 --wait

# Add element
seedance edit cgt-abc123 "在桌面右侧添加一杯咖啡" --wait
```

---

### `seedance status` — Check Task Status

```
seedance status <TASK_ID> [OPTIONS]
```


| Flag        | Default | Description                      |
| ----------- | ------- | -------------------------------- |
| `--json`    | `false` | JSON output                      |
| `--wait`    | `false` | Poll until task completes        |
| `--timeout` | `300`   | Max wait seconds (with `--wait`) |


---

### `seedance download` — Download Completed Video

```
seedance download <TASK_ID> [OPTIONS]
```


| Flag       | Short | Description                                     |
| ---------- | ----- | ----------------------------------------------- |
| `--output` | `-o`  | Output file path (default: `seedance_<id>.mp4`) |


---

### `seedance list` — View Task History

```
seedance list [OPTIONS]
```


| Flag       | Short | Default | Description      |
| ---------- | ----- | ------- | ---------------- |
| `--limit`  | `-n`  | `20`    | Number of tasks  |
| `--status` |       |         | Filter by status |
| `--json`   |       | `false` | JSON output      |


---

### `seedance cleanup` — Clean Up TOS Temp Files

Delete expired TOS temporary files (those uploaded during `extend` or `generate --video`). Each uploaded file carries a `x-amz-meta-expire-at` metadata header set to 8 hours after upload. This command lists and deletes all objects under the `seedance-cli/` prefix.

```bash
seedance cleanup
```

Requires TOS env vars (`TOS_ACCESS_KEY`, `TOS_SECRET_KEY`, `TOS_BUCKET`). Safe to run anytime — only deletes temporary uploads, never user data.

> **Tip:** Add to crontab for automatic cleanup:
> ```bash
> 0 */4 * * * seedance cleanup
> ```

**Auto-cleanup on `--wait`:** When `extend --wait` completes successfully, source video temp files are deleted immediately — no need to run `cleanup` for those.

---

### `seedance config` — Manage Configuration

```bash
seedance config init          # Interactive setup wizard
seedance config show          # Display all settings
seedance config get <KEY>     # Get a single value
seedance config set <KEY> <VALUE>  # Set a single value
```

Available keys: `api_key`, `base_url`, `model`, `resolution`, `ratio`, `duration`, `output_dir`.

---

## Seedance 2.5

Use `--model 2.5` (upstream `doubao-seedance-2-5-260628`, launched on Ark 2026-08-07). Model ID, `duration: -1`, and `mov` output are verified against the live API.

| Capability | 2.0 | 2.5 |
| --- | --- | --- |
| Duration | 4–15s | **4–30s**, or `-1` (model picks the best length) |
| Resolution | 480p / 720p / 1080p | **480p / 720p only** (no 1080p — validated with an error) |
| Reference assets | 9 images / 3 videos / 3 audios (Rule of 12) | **50 total**: 30 images + 10 videos + 10 audios; audio may be the *only* reference |
| Task types | generate | generate / **edit** / **extend** (native) |
| Output format | mp4 | mp4 / **mov** (H.264 + yuv444p + PCM — better for grading/keying) |
| Audio | opt-in | `--audio-gen` sent explicitly (server default is true on 2.5) |

```bash
# 30s max length, model picks duration, mov delivery
seedance generate "One-take cinematic hallway dolly shot" \
  --model 2.5 --duration -1 --resolution 720p --output-format mov --wait
```

### Native extend (2.5)

`seedance extend --model 2.5` submits a native `extend` task: source clips are **not** trimmed to 5s (up to 30s total across 1–3 clips), ratio is forced to `adaptive` (matches the source), and duration accepts `-1`.

### Native edit (2.5)

`seedance edit --model 2.5` submits a native `edit` task: duration and ratio follow the source video automatically (`--duration`/`--ratio` are ignored with a note). Supports replace / add / remove objects and audio-track editing via prompt.

> ⚠️ On 2.5, edit/extend are billed by **source + output** total duration. At 720p, 2.5 costs ~37% more per second than 2.0.

---

## Prompt Engineering Guide

Seedance 2.0 internally separates **spatial layer** (what's in frame) from **temporal layer** (how things change over time). Good prompts are **engineering directives**, not literary descriptions.

### Reference Syntax

| Syntax | Usage |
|--------|-------|
| `@图片N` / `@视频N` / `@音频N` | Asset references (numbered by CLI `--image`/`-s`/`--audio` order, starting from 1) |
| `<主体N>@图片N` | Bind a subject to its reference image |
| `将 @图片N 中的[特征]定义为 <主体N>` | Define reusable subject label (best for multi-scene) |

- **Never** use raw asset IDs in action descriptions.
- Always separate `@图片N` from following verbs with a noun: wrong `@图片1跑向…`, right `<主体1>@图片1 跑向…`.

### Task Classification

| Type | Use when | Prompt pattern |
|------|----------|----------------|
| **Reference** | Motion/style/character transfer | `参考 @图片N 中的<主体N>，生成…` |
| **Edit** | Local replacement, removal, modification | `严格编辑 @视频1，将其中的<原特征>修改为<新特征>` |
| **Extend** | Continue storyline, bridge clips | `向后延长 @视频1，生成…` / `@视频1，<过渡>，接@视频2` |
| **Compose** | Reference one asset, edit another | `参考 @图片1 的[维度]，严格编辑 @视频2` |

> ⚠️ **Edit/extend tasks**: use `@视频N` directly, NOT `参考 @视频N` — the latter is treated as a reference task.

### Eight Core Elements

```
1. Subject     — who/what, identity (use <主体N>)
2. Action      — verb + physics consequence, body-part detail + degree quantified
3. Scene       — environment, lighting, time of day
4. Lighting    — color temperature, quality, direction
5. Camera      — ONE move only (push/pull/pan/track/fixed/follow)
6. Style       — ONE primary style anchor (film/realistic/anime/cyberpunk)
7. Quality     — resolution, detail level, texture
8. Constraints — watermark/logo/subtitle suppression, stability, clone prevention
```

### Two Output Paths

**Path A — Simple (one paragraph):** For single-shot, edit, extend, move tasks. One flowing paragraph with inline constraints.

```
[Task pattern], [subject + asset binding], [scene + brief action], [style + constraint pack]
```

**Path B — Complex (three paragraphs):** For ≥2 multi-scene narrative sequences. Must be three complete paragraphs:
1. **Overall setting + subject definitions** — atmosphere, all `<主体N>` bindings, camera references
2. **Scene breakdown** — `镜头1 / 镜头2 / 镜头3 …`, each with camera→action→position→audio. One camera move per shot. NO absolute timestamps (0–3s won't work).
3. **Style + constraint pack** — quality, stability, subtitle/watermark suppression, clone prevention

### Default Constraint Pack (always append)

```
画面稳定无变形，人物面部稳定，五官清晰，动作连贯自然，不僵硬，无穿模无卡顿。
保持无字幕，不要生成水印，不要生成 Logo。
高清电影质感，色彩自然，光影柔和。
```

For multi-character scenes, add: `禁止出现双胞胎/同款分身，同画面仅保留单个对应人物。`

### Critical Don'ts

- ❌ Negative prompts — describe what you WANT, not what you don't want
- ❌ Absolute timestamps (`0–3s`) — Seedance 2.0 doesn't reliably follow them
- ❌ Multiple camera moves in one shot — pick ONE per shot
- ❌ High-impact dynamics (sprinting, big jumps, violent tumbles) — prefer slow, continuous micro-movements
- ❌ Abstract emotion words — externalize as physical details (sad → shoulders trembling, eyes reddening)

---

## Workflow Patterns

### Text-to-Video (T2V)

```bash
seedance generate "A glass perfume bottle on white marble. Smooth 360-degree orbit camera. Soft studio key light." \
  --duration 8 --ratio 16:9 --wait
```

### Image-to-Video (I2V)

```bash
seedance generate "Character walks forward slowly, wind blows hair" \
  --first-frame character_pose.png --duration 5 --wait
```

### Reference-to-Video (R2V) with Multiple Images

```bash
seedance generate "Character A throws a punch at Character B" \
  --image charA.png --image charB.png --duration 8 --wait
```

### Video-to-Video (V2V) with Style Transfer

```bash
seedance generate "Match the camera movement and editing style from reference" \
  --video reference_clip.mp4 --image character.png --duration 10 --wait
```

### Audio-Driven Generation

```bash
seedance generate "Character speaks directly to camera, medium close-up, locked" \
  --audio dialogue.mp3 --image character.png --audio-gen --duration 8 --wait
```

### Music Beat-Sync

```bash
seedance generate "Scene images transition on musical downbeats, energetic pacing" \
  --image scene1.jpg --image scene2.jpg --image scene3.jpg \
  --audio music_track.mp3 --audio-gen --duration 10 --wait
```

### Video Extension (Forward) — Shortcut

```bash
seedance extend -s source.mp4 "角色缓步走出房间，镜头跟随" --duration 8 --wait

# Equivalent base-layer command:
seedance generate "向后延长视频1，角色缓步走出房间，镜头跟随" \
  --video source.mp4 --duration 8 --wait
```

### Video Extension (Multi-clip Bridging) — Shortcut

```bash
seedance extend -s clip1.mp4 -s clip2.mp4 -s clip3.mp4 \
  "视频1中拱形窗户打开，进入室内，接视频2，镜头进入画内，接视频3" \
  --duration 8 --audio-gen --wait
```

### Video Editing — Shortcut

```bash
seedance edit cgt-abc123 "将视频1礼盒中的香水替换成图片1中的面霜，运镜不变" \
  --image cream.jpg --duration 5 --audio-gen --wait

# Equivalent base-layer command:
seedance generate "将视频1礼盒中的香水替换成图片1中的面霜，运镜不变" \
  --video original.mp4 --image cream.jpg --duration 5 --audio-gen --wait
```

### Chain Generation — Using Extend

```bash
seedance generate "开场：日出照亮山脉" --wait -o opening.mp4
seedance extend -s opening.mp4 "中段：城市苏醒，车流涌动" --wait -o middle.mp4
seedance extend -s middle.mp4 "结尾：人潮中一个女孩回头微笑" --wait -o ending.mp4
```

### First + Last Frame (I2V with Anchors)

```bash
seedance generate "角色从站立过渡到奔跑姿势" \
  --first-frame pose_start.png --last-frame pose_end.png \
  --duration 5 --wait
```

### Web Search (Text-only)

```bash
seedance generate "微距镜头对准叶片上翠绿的玻璃蛙，焦点从皮肤转移到透明腹部" \
  --web-search --duration 11 --wait
```

### Virtual Avatar

```bash
seedance generate "图片1中美妆博主面带笑容，向镜头介绍图片2中的面霜" \
  --image "asset://asset-20260401123823-6d4x2" --image product.jpg \
  --audio-gen --ratio adaptive --duration 11 --wait
```

### Offline Inference

```bash
seedance generate "A cinematic landscape shot" \
  --service-tier flex --duration 10 --wait
```

### Prompt from File

```bash
# Write a complex prompt in a text file
echo '古风仙侠场景，白衣剑客凌空而起，剑光如虹划过夜空，远山云海翻涌。升格慢动作，仰拍视角。' > prompt.txt

seedance generate @prompt.txt --duration 10 --ratio 16:9 --wait
```

### Batch Generation with Seed Variation

```bash
for seed in 1000 1001 1002 1003 1004; do
  seedance generate "Sunset over ocean, golden light, slow pan right" \
    --seed $seed --duration 5 -q
done
```

### Fire-and-Forget + Later Download

```bash
# Submit task (returns immediately)
TASK_ID=$(seedance generate "A dramatic scene" -q)

# ... do other work ...

# Check status later
seedance status $TASK_ID

# Download when ready
seedance download $TASK_ID -o final_output.mp4
```

---

## CI / Script Integration

Use `--quiet`, `--json`, and `--strict` for automation:

```bash
# CI pipeline: generate, wait, fail on timeout
TASK_ID=$(seedance generate "Product ad scene" --wait --strict --timeout 600 -q)

# JSON output for parsing
seedance status $TASK_ID --json | jq '.status'

# List recent failures
seedance list --status failed --json | jq '.[].task_id'
```

---

## Task States


| Status      | Terminal | Description                   |
| ----------- | -------- | ----------------------------- |
| `submitted` | No       | Task received by server       |
| `queued`    | No       | Waiting in generation queue   |
| `running`   | No       | Video is being generated      |
| `succeeded` | Yes      | Generation complete           |
| `failed`    | Yes      | Generation failed             |
| `expired`   | Yes      | Task result expired on server |
| `cancelled` | Yes      | Task was cancelled            |


---

## Exit Codes


| Code | Meaning                                |
| ---- | -------------------------------------- |
| `0`  | Success                                |
| `1`  | Error (API failure, invalid args, etc) |
| `2`  | Timeout (only with `--strict`)         |


---

## Agent Gotchas

1. **Always `--wait` for one-shot workflows.** Without it, `generate` returns immediately with just a task_id. The video isn't ready yet.
2. **Use `-q` for scripting.** Quiet mode outputs only the task_id (on generate) or file path (on download), nothing else.
3. **Local files auto-upload.** Pass local paths to `--image`, `--video`, `--audio` — the CLI handles base64 encoding. No manual upload step needed.
4. `**@file.txt` for long prompts.** Chinese prompts with special characters are easier to manage in a file.
5. `**--strict` for CI.** Without it, timeout is a soft warning (exit 0). With it, timeout exits 2 so your pipeline catches it.
6. **Seed for reproducibility.** Same seed + same prompt + same model = same output. Use for A/B testing and iteration.
7. **Config cascade:** `ARK_API_KEY` env var overrides `config.toml`. Useful for CI where you set secrets via env.
8. **Rule of 12:** Total files (images + videos + audios + first_frame + last_frame) cannot exceed 12. CLI validates this before sending.
9. **Duration range is 4–15 seconds.** CLI rejects values outside this range.
10. **Audio must be MP3.** Other formats fail silently on the server side. Convert before passing to `--audio`.
11. **Prefer `extend`/`edit` shortcuts over raw `generate`** for extension and editing tasks. `extend` auto-trims source videos that exceed `min(5s, --duration)` and uploads them as base64. `edit` auto-resolves task IDs to video URLs. Use `generate` with `--video` only for raw video-to-video generation.
12. **Video extension is prompt-driven.** The model understands extend/edit/bridge semantics from the prompt text. Both `extend`/`edit` and raw `generate --video` rely on this — no special API flag exists.
13. **`--web-search` only works with text-only input.** Cannot combine with `--image`, `--video`, or `--audio`.
14. **`asset://` for virtual avatars.** Use `asset://<asset-id>` with `--image`/`--video`/`--audio`. Only works with assets from the same Volcengine account within 30 days.
15. **Prompt references use "素材类型+序号" format.** In Chinese prompts, refer to inputs as 图片1, 视频1, 音频1 (numbered by order within their type in the content array). Do NOT use asset IDs in prompt text.
