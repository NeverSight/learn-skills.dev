---
name: explainer
description: |
  Create explainer videos with narration and AI-generated visuals. Triggers on:
  "解说视频", "explainer video", "explain this as a video", "tutorial video",
  "introduce X (video)", "解释一下XX（视频形式）".
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      env: ["LISTENHUB_API_KEY"]
    primaryEnv: "LISTENHUB_API_KEY"
---

## When to Use

- User wants to create an explainer or tutorial video
- User asks to "explain" something in video form
- User wants narrated content with AI-generated visuals
- User says "explainer video", "解说视频", "tutorial video"

## When NOT to Use

- User wants audio-only content without visuals (use `/speech` or `/podcast`)
- User wants a podcast-style discussion (use `/podcast`)
- User wants to generate a standalone image (use `/image-gen`)
- User wants to read text aloud without video (use `/speech`)

## Purpose

Generate explainer videos that combine a single narrator's voiceover with AI-generated visuals. Ideal for product introductions, concept explanations, and tutorials. Supports text-only script generation or full text + video output.

## Hard Constraints

- No shell scripts. Construct curl commands from the API reference files listed in Resources
- Always read `shared/authentication.md` for API key and headers
- Follow `shared/common-patterns.md` for polling, errors, and interaction patterns
- Always read config following `shared/config-pattern.md` before any interaction
- Never hardcode speaker IDs — always fetch from the speakers API
- Never save files to `~/Downloads/` — use `.listenhub/explainer/` from config
- Explainer uses exactly 1 speaker
- Mode must be `info` (for Info style) or `story` (for Story style) — never `slides` (use `/slides` skill instead)

<HARD-GATE>
Use the AskUserQuestion tool for every multiple-choice step — do NOT print options as plain text. Ask one question at a time. Wait for the user's answer before proceeding to the next step. After all parameters are collected, summarize the choices and ask the user to confirm. Do NOT call any generation API until the user has explicitly confirmed.

</HARD-GATE>

## Step -1: API Key Check

Follow `shared/config-pattern.md` § API Key Check. If the key is missing, stop immediately.

## Step 0: Config Setup

Follow `shared/config-pattern.md` Step 0.

**If file doesn't exist** — ask location, then create immediately:
```bash
mkdir -p ".listenhub/explainer"
echo '{"outputDir":".listenhub","outputMode":"inline","language":null,"defaultStyle":null,"defaultSpeakers":{}}' > ".listenhub/explainer/config.json"
CONFIG_PATH=".listenhub/explainer/config.json"
# (or $HOME/.listenhub/explainer/config.json for global)
```
Then run **Setup Flow** below.

**If file exists** — read config, display summary, and confirm:
```
当前配置 (explainer)：
  输出方式：{inline / download / both}
  语言偏好：{zh / en / 未设置}
  默认风格：{info / story / 未设置}
  默认主播：{speakerName / 未设置}
```
Ask: "使用已保存的配置？" → **确认，直接继续** / **重新配置**

### Setup Flow (first run or reconfigure)

Ask these questions in order, then save all answers to config at once:

1. **outputMode**: Follow `shared/output-mode.md` § Setup Flow Question.

2. **Language** (optional): "默认语言？"
   - "中文 (zh)"
   - "English (en)"
   - "每次手动选择" → keep `null`

3. **Style** (optional): "默认风格？"
   - "Info — 信息展示型"
   - "Story — 故事叙述型"
   - "每次手动选择" → keep `null`

After collecting answers, save immediately:
```bash
# Follow shared/output-mode.md § Save to Config
NEW_CONFIG=$(echo "$CONFIG" | jq --arg m "$OUTPUT_MODE" '. + {"outputMode": $m}')
echo "$NEW_CONFIG" > "$CONFIG_PATH"
CONFIG=$(cat "$CONFIG_PATH")
```

Note: `defaultSpeakers` are saved after generation (see After Successful Generation section).

## Interaction Flow

### Step 1: Topic / Content

Free text input. Ask the user:

> What would you like to explain or introduce?

Accept: topic description, text content, or concept to explain.

### Step 2: Language

If `config.language` is set, pre-fill and show in summary — skip this question.
Otherwise ask:

```
Question: "What language?"
Options:
  - "Chinese (zh)" — Content in Mandarin Chinese
  - "English (en)" — Content in English
```

### Step 3: Style

If `config.defaultStyle` is set, pre-fill and show in summary — skip this question.
Otherwise ask:

```
Question: "What style of explainer?"
Options:
  - "Info" — Informational, factual presentation style
  - "Story" — Narrative, storytelling approach
```

### Step 4: Speaker Selection

Follow `shared/speaker-selection.md` for the full selection flow, including:
- Default from `config.defaultSpeakers.{language}` (skip step if set)
- Text table + free-text input
- Input matching and re-prompt on no match

Only 1 speaker is supported for explainer videos.

### Step 5: Output Type

```
Question: "What output do you want?"
Options:
  - "Text script only" — Generate narration script, no video
  - "Text + Video" — Generate full explainer video with AI visuals
```

### Step 6: Confirm & Generate

Summarize all choices:

```
Ready to generate explainer:

  Topic: {topic}
  Language: {language}
  Style: {info/story}
  Speaker: {speaker name}
  Output: {text only / text + video}

  Proceed?
```

Wait for explicit confirmation before calling any API.

## Workflow

1. **Submit (foreground)**: `POST /storybook/episodes` with content, speaker, language, mode → extract `episodeId`
2. Tell the user the task is submitted
3. **Poll (background)**: Run the following **exact** bash command with `run_in_background: true` and `timeout: 600000`. Do NOT use python3, awk, or any other JSON parser — use `jq` as shown:

   ```bash
   EPISODE_ID="<id-from-step-1>"
   for i in $(seq 1 30); do
     RESULT=$(curl -sS "https://api.marswave.ai/openapi/v1/storybook/episodes/$EPISODE_ID" \
       -H "Authorization: Bearer $LISTENHUB_API_KEY" 2>/dev/null)
     STATUS=$(echo "$RESULT" | tr -d '\000-\037\177' | jq -r '.data.processStatus // "pending"')
     case "$STATUS" in
       success|completed) echo "$RESULT"; exit 0 ;;
       failed|error) echo "FAILED: $RESULT" >&2; exit 1 ;;
       *) sleep 10 ;;
     esac
   done
   echo "TIMEOUT" >&2; exit 2
   ```

4. When notified, **download and present script**:

   Read `OUTPUT_MODE` from config. Follow `shared/output-mode.md` for behavior.

   **`inline` or `both`**: Present the script inline.

   Present:
   ```
   解说脚本已生成！

   「{title}」

   在线查看：https://listenhub.ai/app/explainer/{episodeId}
   ```

   **`download` or `both`**: Also save the script file.
   - Create `.listenhub/explainer/YYYY-MM-DD-{episodeId}/`
   - Write `{episodeId}.md` from the generated script content
   - Present the download path in addition to the above summary.

5. **If video requested**: `POST /storybook/episodes/{episodeId}/video` (foreground) → **poll again (background)** using the **exact** bash command below with `run_in_background: true` and `timeout: 600000`. Poll for `videoStatus`, not `processStatus`:

   ```bash
   EPISODE_ID="<id-from-step-1>"
   for i in $(seq 1 30); do
     RESULT=$(curl -sS "https://api.marswave.ai/openapi/v1/storybook/episodes/$EPISODE_ID" \
       -H "Authorization: Bearer $LISTENHUB_API_KEY" 2>/dev/null)
     STATUS=$(echo "$RESULT" | tr -d '\000-\037\177' | jq -r '.data.videoStatus // "pending"')
     case "$STATUS" in
       success|completed) echo "$RESULT"; exit 0 ;;
       failed|error) echo "FAILED: $RESULT" >&2; exit 1 ;;
       *) sleep 10 ;;
     esac
   done
   echo "TIMEOUT" >&2; exit 2
   ```
6. When notified, **download and present result**:

**Present result**

Read `OUTPUT_MODE` from config. Follow `shared/output-mode.md` for behavior.

**`inline` or `both`**: Display video URL and audio URL as clickable links.

Present:
```
解说视频已生成！

视频链接：{videoUrl}
音频链接：{audioUrl}
时长：{duration}s
消耗积分：{credits}
```

**`download` or `both`**: Also download the audio file.
```bash
DATE=$(date +%Y-%m-%d)
JOB_DIR=".listenhub/explainer/${DATE}-{jobId}"
mkdir -p "$JOB_DIR"
curl -sS -o "${JOB_DIR}/{jobId}.mp3" "{audioUrl}"
```
Present the download path in addition to the above summary.

### After Successful Generation

Update config with the choices made this session:

```bash
NEW_CONFIG=$(echo "$CONFIG" | jq \
  --arg lang "{language}" \
  --arg style "{info/story}" \
  --arg speakerId "{speakerId}" \
  '. + {"language": $lang, "defaultStyle": $style, "defaultSpeakers": (.defaultSpeakers + {($lang): [$speakerId]})}')
echo "$NEW_CONFIG" > "$CONFIG_PATH"
```

**Estimated times**:
- Text script only: 2-3 minutes
- Text + Video: 3-5 minutes

## API Reference

- Speaker list: `shared/api-speakers.md`
- Speaker selection guide: `shared/speaker-selection.md`
- Episode creation: `shared/api-storybook.md`
- Polling: `shared/common-patterns.md` § Async Polling
- Config pattern: `shared/config-pattern.md`

## Composability

- **Invokes**: speakers API (for speaker selection); may invoke `/speech` for voiceover
- **Invoked by**: content-planner (Phase 3)

## Example

**User**: "Create an explainer video introducing Claude Code"

**Agent workflow**:
1. Topic: "Claude Code introduction"
2. Ask language → "English"
3. Ask style → "Info"
4. Fetch speakers, user picks "cozy-man-english"
5. Ask output → "Text + Video"

```bash
curl -sS -X POST "https://api.marswave.ai/openapi/v1/storybook/episodes" \
  -H "Authorization: Bearer $LISTENHUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sources": [{"type": "text", "content": "Introduce Claude Code: what it is, key features, and how to get started"}],
    "speakers": [{"speakerId": "cozy-man-english"}],
    "language": "en",
    "mode": "info"
  }'
```

Poll until text is ready, then generate video if requested.
