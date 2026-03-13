---
name: content-parser
description: |
  Extract and parse content from URLs. Triggers on: user provides a URL to extract
  content from, another skill needs to parse source material, "parse this URL",
  "extract content", "解析链接", "提取内容".
metadata:
  openclaw:
    emoji: "🔗"
    requires:
      env: ["LISTENHUB_API_KEY"]
    primaryEnv: "LISTENHUB_API_KEY"
---

## When to Use

- User provides a URL and wants to extract/read its content
- Another skill needs to parse source material from a URL before generation
- User says "parse this URL", "extract content from this link"
- User says "解析链接", "提取内容"

## When NOT to Use

- User already has text content and doesn't need URL parsing
- User wants to generate audio/video content (not content extraction)
- User wants to read a local file (use standard file reading tools)

## Purpose

Extract and normalize content from URLs across supported platforms. Returns structured data including content body, metadata, and references. Useful as a preprocessing step for content generation skills or standalone content extraction.

## Hard Constraints

- No shell scripts. Construct curl commands from the API reference files listed in Resources
- Always read `shared/authentication.md` for API key and headers
- Follow `shared/common-patterns.md` for polling, errors, and interaction patterns
- URL must be a valid HTTP(S) URL
- Always read config following `shared/config-pattern.md` before any interaction
- Never save files to `~/Downloads/` or `.listenhub/` — save to the current working directory

<HARD-GATE>
Use the AskUserQuestion tool for every multiple-choice step — do NOT print options as plain text. Ask one question at a time. Wait for the user's answer before proceeding to the next step. After collecting URL and options, confirm with the user before calling the extraction API.
</HARD-GATE>

## Step -1: API Key Check

Follow `shared/config-pattern.md` § API Key Check. If the key is missing, stop immediately.

## Step 0: Config Setup

Follow `shared/config-pattern.md` Step 0.

**If file doesn't exist** — ask location, then create immediately:
```bash
mkdir -p ".listenhub/content-parser"
echo '{"autoDownload":true}' > ".listenhub/content-parser/config.json"
CONFIG_PATH=".listenhub/content-parser/config.json"
# (or $HOME/.listenhub/content-parser/config.json for global)
```
Then run **Setup Flow** below.

**If file exists** — read config, display summary, and confirm:
```
当前配置 (content-parser)：
  自动下载：{是 / 否}
```
Ask: "使用已保存的配置？" → **确认，直接继续** / **重新配置**

### Setup Flow (first run or reconfigure)

1. **autoDownload**: "自动保存提取的内容到当前目录？"
   - "是（推荐）" → `autoDownload: true`
   - "否" → `autoDownload: false`

Save immediately:
```bash
NEW_CONFIG=$(echo "$CONFIG" | jq --argjson dl {true/false} '. + {"autoDownload": $dl}')
echo "$NEW_CONFIG" > "$CONFIG_PATH"
CONFIG=$(cat "$CONFIG_PATH")
```

## Interaction Flow

### Step 1: URL Input

Free text input. Ask the user:

> What URL would you like to extract content from?

### Step 2: Options (optional)

Ask if the user wants to configure extraction options:

```
Question: "Do you want to configure extraction options?"
Options:
  - "No, use defaults" — Extract with default settings
  - "Yes, configure options" — Set summarize, maxLength, or Twitter tweet count
```

If "Yes", ask follow-up questions:
- **Summarize**: "Generate a summary of the content?" (Yes/No)
- **Max Length**: "Set maximum content length?" (Free text, e.g., "5000")
- **Twitter count** (only if URL is Twitter/X profile): "How many tweets to fetch?" (1-100, default 20)

### Step 3: Confirm & Extract

Summarize:

```
Ready to extract content:

  URL: {url}
  Options: {summarize: true, maxLength: 5000, twitter.count: 50} / default

  Proceed?
```

Wait for explicit confirmation before calling the API.

## Workflow

1. **Validate URL**: Must be HTTP(S). Normalize if needed (see `references/supported-platforms.md`)
2. **Build request body**:
   ```json
   {
     "source": {
       "type": "url",
       "uri": "{url}"
     },
     "options": {
       "summarize": true/false,
       "maxLength": 5000,
       "twitter": {
         "count": 50
       }
     }
   }
   ```
   Omit `options` if user chose defaults.
3. **Submit (foreground)**: `POST /v1/content/extract` → extract `taskId`
4. Tell the user extraction is in progress
5. **Poll (background)**: Run the following **exact** bash command with `run_in_background: true` and `timeout: 300000`. Note: status field is `.data.status` (not `processStatus`), interval is 5s, values are `processing`/`completed`/`failed`:

   ```bash
   TASK_ID="<id-from-step-3>"
   for i in $(seq 1 60); do
     RESULT=$(curl -sS "https://api.marswave.ai/openapi/v1/content/extract/$TASK_ID" \
       -H "Authorization: Bearer $LISTENHUB_API_KEY" 2>/dev/null)
     STATUS=$(echo "$RESULT" | tr -d '\000-\037\177' | jq -r '.data.status // "processing"')
     case "$STATUS" in
       completed) echo "$RESULT"; exit 0 ;;
       failed) echo "FAILED: $RESULT" >&2; exit 1 ;;
       *) sleep 5 ;;
     esac
   done
   echo "TIMEOUT" >&2; exit 2
   ```
6. When notified, **download and present result**:

   If `autoDownload` is `true`:
   - Write `{taskId}-extracted.md` to the **current directory** — full extracted content in markdown
   - Write `{taskId}-extracted.json` to the **current directory** — full raw API response data

   ```bash
   echo "$CONTENT_MD" > "${TASK_ID}-extracted.md"
   echo "$RESULT" > "${TASK_ID}-extracted.json"
   ```

   Present:
   ```
   内容提取完成！

   来源：{url}
   标题：{metadata.title}
   长度：~{character count} 字符
   消耗积分：{credits}

   已保存到当前目录：
     {taskId}-extracted.md
     {taskId}-extracted.json
   ```

7. Show a preview of the extracted content (first ~500 chars)
8. Offer to use content in another skill (e.g. `/podcast`, `/tts`)

**Estimated time**: 10-30 seconds depending on content size and platform.

## API Reference

- Content extract: `shared/api-content-extract.md`
- Supported platforms: `references/supported-platforms.md`
- Polling: `shared/common-patterns.md` § Async Polling
- Error handling: `shared/common-patterns.md` § Error Handling
- Config pattern: `shared/config-pattern.md`

## Example

**User**: "Parse this article: https://en.wikipedia.org/wiki/Topology"

**Agent workflow**:
1. URL: `https://en.wikipedia.org/wiki/Topology`
2. Options: defaults (omit options)
3. Submit extraction

```bash
curl -sS -X POST "https://api.marswave.ai/openapi/v1/content/extract" \
  -H "Authorization: Bearer $LISTENHUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "source": {
      "type": "url",
      "uri": "https://en.wikipedia.org/wiki/Topology"
    }
  }'
```

4. Poll until complete:

```bash
curl -sS "https://api.marswave.ai/openapi/v1/content/extract/69a7dac700cf95938f86d9bb" \
  -H "Authorization: Bearer $LISTENHUB_API_KEY"
```

5. Present extracted content preview and offer next actions.

---

**User**: "Extract recent tweets from @elonmusk, get 50 tweets"

**Agent workflow**:
1. URL: `https://x.com/elonmusk`
2. Options: `{"twitter": {"count": 50}}`
3. Submit extraction

```bash
curl -sS -X POST "https://api.marswave.ai/openapi/v1/content/extract" \
  -H "Authorization: Bearer $LISTENHUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "source": {
      "type": "url",
      "uri": "https://x.com/elonmusk"
    },
    "options": {
      "twitter": {
        "count": 50
      }
    }
  }'
```

4. Poll until complete, present results.
