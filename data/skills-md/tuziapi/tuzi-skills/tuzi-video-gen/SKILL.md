---
name: tuzi-video-gen
description: 通过兔子API进行AI视频生成。支持 Veo、Sora、Kling、Seedance 等模型，单视频和长视频（多段合成）模式。当用户要求生成视频、创建视频或需要视频生成后端时使用。
---

# Video Generation (AI SDK)

Tuzi API video generation backend. Default model: veo3.1.

## Script Directory

**Agent Execution**:
1. `SKILL_DIR` = this SKILL.md file's directory
2. Script path = `${SKILL_DIR}/scripts/main.ts`

## Step 0: Load Preferences ⛔ BLOCKING

**CRITICAL**: This step MUST complete BEFORE any video generation. Do NOT skip or defer.

### 0.1 Check API Key

```bash
echo "${TUZI_API_KEY:-not_set}"
grep -s TUZI_API_KEY .tuzi-skills/.env "$HOME/.tuzi-skills/.env"
```

| Result | Action |
|--------|--------|
| Key found | Continue to Step 0.2 |
| Key NOT found | ⛔ Run API key setup (see [references/config/first-time-setup.md](references/config/first-time-setup.md)) → Store key → Then continue |

### 0.2 Check EXTEND.md

```bash
test -f .tuzi-skills/tuzi-video-gen/EXTEND.md && echo "project"
test -f "$HOME/.tuzi-skills/tuzi-video-gen/EXTEND.md" && echo "user"
```

| Result | Action |
|--------|--------|
| Found | Load, parse, apply settings |
| Not found | ⛔ Run first-time setup ([references/config/first-time-setup.md](references/config/first-time-setup.md)) → Save EXTEND.md → Then continue |

| Path | Location |
|------|----------|
| `.tuzi-skills/tuzi-video-gen/EXTEND.md` | Project directory |
| `$HOME/.tuzi-skills/tuzi-video-gen/EXTEND.md` | User home |

**EXTEND.md Supports**: Default model | Default seconds | Default size

Schema: `references/config/preferences-schema.md`

## Usage

```bash
# Single video
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A cat walking in a garden" --video cat.mp4

# With model and duration
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "城市夜景延时" --video city.mp4 --model veo3 --seconds 8

# With reference image
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "Animate this scene" --video out.mp4 --ref source.png

# From prompt file
npx -y bun ${SKILL_DIR}/scripts/main.ts --promptfiles prompt.md --video out.mp4

# Long video (multi-segment with ffmpeg concat)
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A journey through seasons" --video long.mp4 --segments 3

# Long video with per-segment prompts
npx -y bun ${SKILL_DIR}/scripts/main.ts --video long.mp4 --segments 3 --segment-prompts seg1.md seg2.md seg3.md
```

## Options

| Option | Description |
|--------|-------------|
| `--prompt <text>`, `-p` | Prompt text |
| `--promptfiles <files...>` | Read prompt from files (concatenated) |
| `--video <path>` | Output video path (required) |
| `--model <id>`, `-m` | Model ID (default: veo3.1) |
| `--seconds <n>`, `-s` | Duration in seconds |
| `--size <WxH>` | Video size (e.g., `1280x720`, `16x9`) |
| `--ref <files...>` | Reference images |
| `--ref-mode reference\|frames\|components` | Reference image mode |
| `--segments <n>` | Long video segment count (min 2) |
| `--segment-prompts <files...>` | Per-segment prompt files |
| `--json` | JSON output |

## Models

| Model | Provider | Duration | Sizes | Image Mode |
|-------|----------|----------|-------|------------|
| `veo3` | Veo | 8s | 16:9, 9:16 | reference |
| `veo3.1` (default) | Veo | 8s | 16:9, 9:16 | frames |
| `veo3.1-4k` | Veo | 8s | 4K | frames |
| `sora-2` | Sora | 10/15s | 16:9, 9:16 | reference |
| `sora-2-pro` | Sora | 10/15/25s | 16:9, 9:16, HD | reference |
| `kling-v1-6` | Kling | 5/10s | 16:9, 9:16, 1:1 | reference |
| `seedance-1.5-pro` | Seedance | 5/10s | 1080p, 720p | frames |

## Long Video Mode

When `--segments N` is specified (N >= 2):

1. Generates N video segments sequentially
2. After each segment, extracts last frame via ffmpeg
3. Last frame becomes next segment's reference image (continuity)
4. All segments concatenated via `ffmpeg -f concat`
5. Temporary files cleaned up

**Requirements**: ffmpeg must be installed.

**Per-segment prompts**: Use `--segment-prompts` to provide individual prompt files for each segment. If fewer files than segments, remaining segments use the main `--prompt`.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `TUZI_API_KEY` | Tuzi API key (https://api.tu-zi.com) |
| `TUZI_VIDEO_MODEL` | Default video model (default: veo3.1) |
| `TUZI_BASE_URL` | Custom Tuzi endpoint (default: https://api.tu-zi.com) |

**Load Priority**: CLI args > EXTEND.md > env vars > `<cwd>/.tuzi-skills/.env` > `~/.tuzi-skills/.env`

## Model Resolution

Priority (highest → lowest):

1. CLI: `--model <id>`
2. EXTEND.md: `default_model`
3. Env var: `TUZI_VIDEO_MODEL`
4. Built-in default: `veo3.1`

**Agent MUST display model info** before each generation:
- Show: `Using [model]`
- Show switch hint: `Switch model: --model <id> | EXTEND.md default_model | env TUZI_VIDEO_MODEL`

## Error Handling

- Missing API key → ⛔ MUST run API key setup from Step 0.1
- Generation failure → auto-retry once
- Business failure (content rejected) → no retry, report error
- Network error → exponential backoff (1.5x, max 60s)
- Timeout → error after 90 minutes
- Missing ffmpeg (long video mode) → clear error with install instructions

## Extension Support

Custom configurations via EXTEND.md. See **Step 0** for paths and supported options.
