---
name: send-telegram
description: Send a message to Dhruv's Telegram. Use when user says "send to telegram", "telegram me", "notify me", or wants to receive any text/note/reminder on Telegram.
---

# Send Telegram Message

## Goal
Send any message to Dhruv's Telegram (chat ID: 637313836) via n8n workflow.

## How to Use

### Method 1: Via n8n MCP (preferred)
Use the `mcp__claude_ai_n8n__execute_workflow` tool:
```
workflowId: fkErsg4iulUvpcsa
inputs: { "type": "chat", "chatInput": "<your message here>" }
```

### Method 2: Direct API (fallback if MCP fails)
```bash
python3 -c "
import urllib.request, json, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
url = 'https://n8n.aiwithdhruv.cloud/webhook/claude-telegram'
data = json.dumps({'message': '<your message here>'}).encode('utf-8')
req = urllib.request.Request(url, data=data, method='POST')
req.add_header('Content-Type', 'application/json')
resp = urllib.request.urlopen(req, context=ctx)
print(resp.read().decode())
"
```

## Setup Required (one-time)
1. Go to n8n UI: https://n8n.aiwithdhruv.cloud
2. Open workflow: **Claude Telegram Sender** (ID: fkErsg4iulUvpcsa)
3. Click Settings (gear icon) → Toggle **"Available in MCP"** ON
4. Save

## Details
- Workflow ID: `fkErsg4iulUvpcsa`
- Chat ID: `637313836`
- Telegram credential: `W6XV6RQORTB3eBDg`
- Supports HTML formatting in messages
- Created: Feb 15, 2026

## Example Uses
- "Send my interview prep notes to Telegram"
- "Telegram me a reminder about the Monday 10:30 call"
- "Send this summary to my Telegram"

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `message` | string | Yes | Message to send (supports HTML formatting) |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `sent` | boolean | Whether message was delivered |

### Credentials
| Name | Source |
|------|--------|
| `n8n_workflow` | n8n MCP (workflow ID: fkErsg4iulUvpcsa) |

### Cost
Free (Telegram Bot API)
