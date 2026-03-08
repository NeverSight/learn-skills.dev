---
name: tuzi-short-video
description: 为小红书、抖音、X/Twitter、视频号等平台生成短视频内容。分析用户输入，自动适配平台规格，生成视频脚本并调用视频生成后端。当用户要求"生成短视频"、"做一个视频"、"短视频"或为社交平台创建视频内容时使用。
---

# Short Video Creator

Creates short videos for social media platforms. Analyzes content, adapts to platform specs, generates prompts, and calls tuzi-video-gen backend.

## Script Directory

This is a workflow-only skill (no scripts). It delegates video generation to `tuzi-video-gen`.

**VIDEO_GEN_DIR**: Resolve from `skills/tuzi-video-gen/SKILL.md` relative to project root.

## Step 0: Load Preferences ⛔ BLOCKING

**CRITICAL**: This step MUST complete BEFORE any video generation.

### 0.1 Check API Key

```bash
echo "${TUZI_API_KEY:-not_set}"
grep -s TUZI_API_KEY .tuzi-skills/.env "$HOME/.tuzi-skills/.env"
```

| Result | Action |
|--------|--------|
| Key found | Continue to Step 0.2 |
| Key NOT found | ⛔ Run API key setup (see [references/config/first-time-setup.md](references/config/first-time-setup.md)) |

### 0.2 Check EXTEND.md

```bash
test -f .tuzi-skills/tuzi-short-video/EXTEND.md && echo "project"
test -f "$HOME/.tuzi-skills/tuzi-short-video/EXTEND.md" && echo "user"
```

| Result | Action |
|--------|--------|
| Found | Load, parse, apply settings |
| Not found | ⛔ Run first-time setup ([references/config/first-time-setup.md](references/config/first-time-setup.md)) |

| Path | Location |
|------|----------|
| `.tuzi-skills/tuzi-short-video/EXTEND.md` | Project directory |
| `$HOME/.tuzi-skills/tuzi-short-video/EXTEND.md` | User home |

**EXTEND.md Supports**: Default platform | Default model

Schema: `references/config/preferences-schema.md`

## Step 1: Analyze User Input

Analyze the user's content (text, article, script, topic description):

- Identify main topic and key points
- Determine content type (tutorial, story, showcase, explainer)
- Estimate ideal video length and segment count

## Step 2: Confirm Platform and Parameters

Use AskUserQuestion to let user choose target platform (unless specified or saved in EXTEND.md):

```yaml
header: "Target Platform"
question: "目标发布平台？"
options:
  - label: "小红书"
    description: "9:16 竖屏, 720x1280"
  - label: "抖音"
    description: "9:16 竖屏, 1080x1920"
  - label: "X/Twitter"
    description: "16:9 横屏, 1280x720"
  - label: "视频号"
    description: "9:16/16:9, 1080x1920"
```

### Platform Presets

| Platform | Aspect | Size | Duration | Notes |
|----------|--------|------|----------|-------|
| 小红书 | 9:16 | 720x1280 | 15-60s | 竖屏短视频 |
| 抖音 | 9:16 | 1080x1920 | 15-60s | 竖屏，高分辨率 |
| X/Twitter | 16:9 | 1280x720 | 5-140s | 横屏为主 |
| 视频号 | 9:16 | 1080x1920 | 15-60s | 竖屏优先 |

Platform details: See [references/platforms/](references/platforms/)

## Step 3: Generate Video Script

Based on content analysis and platform:

### Single Video (content fits one clip)

1. Write a detailed video generation prompt in English
2. Include: visual scenes, camera movements, style, mood, lighting
3. Save prompt to `prompts/01-video-prompt.md`

### Long Video (content needs multiple segments)

1. Split content into logical segments (opening + body + ending)
2. Write per-segment prompts with continuity notes
3. Save to `prompts/01-segment-opening.md`, `02-segment-main.md`, etc.

Workflow details: See [references/workflows/](references/workflows/)

## Step 4: Generate Video

### Single Video

```bash
npx -y bun ${VIDEO_GEN_DIR}/scripts/main.ts \
  --promptfiles <output-dir>/prompts/01-video-prompt.md \
  --video <output-dir>/01-video-<slug>.mp4 \
  --size <platform-size> \
  --seconds <duration>
```

### Long Video

```bash
npx -y bun ${VIDEO_GEN_DIR}/scripts/main.ts \
  --video <output-dir>/01-video-<slug>.mp4 \
  --segments <N> \
  --segment-prompts <output-dir>/prompts/01-segment-opening.md <output-dir>/prompts/02-segment-main.md ... \
  --size <platform-size> \
  --seconds <per-segment-seconds>
```

## Step 5: Completion Report

Display:
- Output video path
- Platform and specs used
- Model used
- Duration

## Output Directory

```
short-video/{topic-slug}/
├── source-{slug}.md
├── prompts/
│   ├── 01-video-prompt.md          (single video)
│   ├── 01-segment-opening.md       (long video)
│   ├── 02-segment-main.md
│   └── 03-segment-ending.md
├── segments/                        (long video temp, cleaned up)
└── 01-video-{slug}.mp4             (final output)
```

## Extension Support

Custom configurations via EXTEND.md. See **Step 0** for paths and supported options.
