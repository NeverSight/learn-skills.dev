---
name: openclaw-add-feishu-bot
description: Adds a new Feishu bot account to openclaw and wires it up to a new agent. Use this skill whenever the user wants to add a Feishu bot, register a new Feishu App to openclaw, configure a second (or third, etc.) Feishu account, or set up a new Feishu App ID + App Secret pair in openclaw. Trigger on phrases like "add feishu bot", "新增飞书 bot", "add feishu account", "register feishu app", "接入飞书", or whenever the user provides a Feishu appId + appSecret pair and wants to connect it to openclaw.
---

# Add Feishu Bot to Openclaw

Automates the full workflow of registering a new Feishu bot in openclaw: JSON config edits, workspace creation, gateway restart, and optional pairing approval.

## Required inputs

Gather these from the user before starting (ask in one message if any are missing):

| Field | Description | Example |
|-------|-------------|---------|
| `agentId` | Short unique name for this bot/agent | `dabao` |
| `appId` | Feishu App ID from the Feishu Open Platform | `cli_xxxxxxxxxxxx` |
| `appSecret` | Feishu App Secret | `your-app-secret-here` |
| `pairingCode` | (optional) Pairing code if the bot is already added to a group | `LNPQR9W9` |

## Steps

Execute all steps in order. Read the config file first so you can do targeted edits rather than overwriting the whole file.

### Step 1 — Read current config

```
Read ~/.openclaw/openclaw.json
```

### Step 2 — Edit `channels.feishu`

**If feishu uses the old single-account format** (has `appId`/`appSecret` at top level, no `accounts` key):

Migrate to multi-account structure — replace the entire `feishu` block:
```json
"feishu": {
  "enabled": true,
  "domain": "feishu",
  "groupPolicy": "open",
  "defaultAccount": "default",
  "accounts": {
    "default": {
      "appId": "<existing-appId>",
      "appSecret": "<existing-appSecret>"
    },
    "<agentId>": {
      "appId": "<new-appId>",
      "appSecret": "<new-appSecret>"
    }
  }
}
```

**If feishu already has `accounts`** (multi-account format):

Add just the new account entry inside `accounts`:
```json
"<agentId>": {
  "appId": "<appId>",
  "appSecret": "<appSecret>"
}
```

### Step 3 — Add agent to `agents.list`

Append to the `agents.list` array:
```json
{
  "id": "<agentId>",
  "workspace": "~/.openclaw/workspace-<agentId>",
  "subagents": {
    "allowAgents": ["*"]
  }
}
```

### Step 4 — Add binding to `bindings`

Append to the `bindings` array:
```json
{
  "agentId": "<agentId>",
  "match": {
    "channel": "feishu",
    "accountId": "<agentId>"
  }
}
```

### Step 5 — Add to `tools.agentToAgent.allow`

Add `"<agentId>"` to the `allow` array under `tools.agentToAgent`.

### Step 6 — Create workspace directory

```bash
mkdir -p ~/.openclaw/workspace-<agentId>
```

### Step 7 — Restart gateway

```bash
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
```

### Step 8 — Pairing approve (if code provided)

If the user provided a `pairingCode`:
```bash
openclaw pairing approve feishu <pairingCode>
```

If not, remind the user to run this after adding the bot to a group:
```
openclaw pairing approve feishu <code>
```

## After completion

Confirm:
- Which account was added (`default` → `<agentId>`)
- Binding: feishu / `<agentId>` → agent `<agentId>`
- Workspace: `~/.openclaw/workspace-<agentId>`
- Gateway restarted ✓
- Pairing: approved or pending

If pairing is still pending, tell the user to add the bot to the target group first, then run the approve command.
