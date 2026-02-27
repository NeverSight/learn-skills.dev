---
name: send-feishu
description: Use when user says "发到飞书", "飞书通知", "通知飞书", "feishu", "发给我", "私发飞书", or explicitly invokes /send-feishu to send messages, images, or files to Feishu group chat or individual via webhook or API
allowed-tools: Bash
---

# Send Feishu Message

Send messages, images, and files to Feishu groups or individuals.

## Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `FEISHU_WEBHOOK` | Group Webhook URL | For text/card/image to group |
| `FEISHU_APP_ID` | App credential | For image/file upload & API send |
| `FEISHU_APP_SECRET` | App credential | For image/file upload & API send |
| `FEISHU_CHAT_ID` | Group chat ID (`oc_xxx`) | For API send to group |
| `FEISHU_USER_OPEN_ID` | Personal open_id (`ou_xxx`) | For send to individual |

## Decision Logic

Choose the sending method based on content type and target:

```
Text/Card to group     → Webhook (simple, no auth needed)
Image to group         → Get token → Upload image → Webhook send image_key
File to group          → Get token → Upload file → API send to chat_id
Image/File to person   → Get token → Upload resource → API send to open_id
Text/Card to person    → Get token → API send to open_id
```

## Choosing Format

**Use text** — simple one-liner (status update, quick note).

**Use card** — content has title + body, structured data, summary, or report.

**Use image** — user explicitly asks to send an image file, screenshot, or chart.

**Use file** — user asks to send .html/.md/.pdf/.doc/.xls etc., or content is too long for card display.

**Send to individual** — user says "发给我", "私发", "发到我的飞书", or specifies a person.

## Step A: Get tenant_access_token

Required for image upload, file upload, and API message sending. Skip this step if only sending text/card via Webhook.

```bash
curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d '{"app_id":"'"$FEISHU_APP_ID"'","app_secret":"'"$FEISHU_APP_SECRET"'"}'
```

Response: `{"code":0,"msg":"ok","tenant_access_token":"t-xxx","expire":7200}`

Extract the token and store in a variable for subsequent steps.

## Step B: Upload Image (get image_key)

Required when sending an image. Supports JPEG/PNG/WEBP/GIF/TIFF/BMP/ICO, max 10MB.

```bash
curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/images' \
  -H "Authorization: Bearer $TOKEN" \
  -F 'image_type="message"' \
  -F 'image=@"/path/to/image.png"'
```

Response: `{"code":0,"data":{"image_key":"img_xxx"}}`

## Step C: Upload File (get file_key)

Required when sending a file. Max 30MB.

```bash
curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/files' \
  -H "Authorization: Bearer $TOKEN" \
  -F 'file_type="stream"' \
  -F 'file_name="report.md"' \
  -F 'file=@"/path/to/file"'
```

`file_type` values: `opus` (audio), `mp4` (video), `pdf`, `doc`, `xls`, `ppt`, `stream` (binary, use as default).

Response: `{"code":0,"data":{"file_key":"file_xxx"}}`

## Sending via Webhook

### Send Text

```bash
curl -s -X POST "$FEISHU_WEBHOOK" -H "Content-Type: application/json" \
  -d '{"msg_type":"text","content":{"text":"MESSAGE_HERE"}}'
```

### Send Card

Pick header color by sentiment:
- `green` — success, complete, done
- `orange` — warning, attention
- `red` — error, failure
- `blue` — info, neutral (default)
- `purple` — highlight, special

**Short content (no special characters):**

```bash
curl -s -X POST "$FEISHU_WEBHOOK" -H "Content-Type: application/json" \
  -d '{
    "msg_type":"interactive",
    "card":{
      "header":{"title":{"content":"TITLE","tag":"plain_text"},"template":"COLOR"},
      "elements":[{"tag":"div","text":{"content":"BODY_LARK_MD","tag":"lark_md"}}]
    }
  }'
```

**Long content or content with special characters (`$`, `"`, `\n`, etc.) — always use this pattern:**

```bash
python3 - << 'EOF' | curl -s -X POST "$FEISHU_WEBHOOK" \
  -H "Content-Type: application/json" -d @-
import json
card = {
    "msg_type": "interactive",
    "card": {
        "header": {"title": {"content": "TITLE", "tag": "plain_text"}, "template": "COLOR"},
        "elements": [
            {"tag": "div", "text": {"content": "BODY LINE 1\nBODY LINE 2", "tag": "lark_md"}},
            {"tag": "hr"},
            {"tag": "div", "text": {"content": "SECTION 2 CONTENT", "tag": "lark_md"}}
        ]
    }
}
print(json.dumps(card))
EOF
```

Card body supports lark_md: `**bold**`, `*italic*`, `~~strike~~`, `[link](url)`, `\n` for newlines.

### Send Image via Webhook

After uploading image (Step B) to get `image_key`:

```bash
curl -s -X POST "$FEISHU_WEBHOOK" \
  -H "Content-Type: application/json" \
  -d '{"msg_type":"image","content":{"image_key":"img_xxx"}}'
```

## Sending via API

Use API when sending files, or sending any content to an individual.

### Send to Group (chat_id)

```bash
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{"receive_id":"'"$FEISHU_CHAT_ID"'","msg_type":"MSG_TYPE","content":"CONTENT_JSON_STRING"}'
```

### Send to Individual (open_id)

```bash
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{"receive_id":"'"$FEISHU_USER_OPEN_ID"'","msg_type":"MSG_TYPE","content":"CONTENT_JSON_STRING"}'
```

### API Content Formats

The `content` field must be a **JSON-encoded string** (escaped JSON inside JSON).

**Text:**
```json
{"receive_id":"ID","msg_type":"text","content":"{\"text\":\"Hello\"}"}
```

**Image** (after upload):
```json
{"receive_id":"ID","msg_type":"image","content":"{\"image_key\":\"img_xxx\"}"}
```

**File** (after upload):
```json
{"receive_id":"ID","msg_type":"file","content":"{\"file_key\":\"file_xxx\"}"}
```

## After Sending

Check the response JSON:
- Webhook: `{"code":0,"msg":"success"}` → success
- API: `{"code":0,"msg":"success","data":{...}}` → success
- `code` != 0 → report the error:
  - 19001: webhook URL invalid
  - 19021: signature check failed
  - 19022: IP not whitelisted
  - 19024: keyword check failed
  - 99991663: token invalid or expired (re-run Step A)
  - 230001: bot not in chat or no permission

## Important

- **Always escape** special characters in JSON (quotes, backslashes, newlines)
- Use `printf '%s'` or heredoc to safely pass message content to curl if it contains special characters
- If required env vars are not set, tell user which ones to configure
- Keep messages concise — Feishu cards have display limits
- Token from Step A is valid for 2 hours; no need to refresh within a session
- **App permissions required**: `im:message:send_as_bot` (send messages), `im:resource` (upload images and files)
