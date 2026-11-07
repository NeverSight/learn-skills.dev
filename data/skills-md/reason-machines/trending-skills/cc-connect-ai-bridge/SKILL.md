---
name: cc-connect-ai-bridge
description: Bridge local AI coding agents (Claude Code, Cursor, Gemini CLI, Codex) to messaging platforms (Feishu, Telegram, Slack, Discord, DingTalk, WeChat Work, LINE) without a public IP.
triggers:
  - connect claude code to telegram
  - bridge AI agent to messaging platform
  - chat with claude from my phone
  - set up cc-connect for feishu
  - control AI coding agent from slack
  - configure cc-connect bot
  - send messages to gemini cli from discord
  - schedule AI agent tasks from chat
---

# CC-Connect AI Bridge

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

CC-Connect bridges locally running AI coding agents (Claude Code, Codex, Cursor Agent, Gemini CLI, Qoder CLI, OpenCode, iFlow CLI) to messaging platforms you already use. You can chat with your local agent from Telegram, Feishu, Slack, Discord, DingTalk, WeChat Work, LINE, or QQ — no public IP required for most platforms.

---

## Installation

### Via npm (recommended)

```bash
# Stable
npm install -g cc-connect

# Beta (includes personal WeChat / Weixin ilink and other beta features)
npm install -g cc-connect@beta
```

### Via binary

```bash
# Linux amd64
curl -L -o cc-connect https://github.com/chenhg5/cc-connect/releases/latest/download/cc-connect-linux-amd64
chmod +x cc-connect
sudo mv cc-connect /usr/local/bin/

# macOS arm64
curl -L -o cc-connect https://github.com/chenhg5/cc-connect/releases/latest/download/cc-connect-darwin-arm64
chmod +x cc-connect
sudo mv cc-connect /usr/local/bin/
```

### Build from source (Go 1.22+)

```bash
git clone https://github.com/chenhg5/cc-connect.git
cd cc-connect
make build
# binary appears at ./bin/cc-connect
```

### Self-update

```bash
cc-connect update          # stable
cc-connect update --pre    # beta / pre-release
```

---

## Quick AI-assisted Setup

Send this prompt to Claude Code or any AI coding agent — it will install and configure cc-connect automatically:

```
Follow https://raw.githubusercontent.com/chenhg5/cc-connect/refs/heads/main/INSTALL.md to install and configure cc-connect.
```

---

## Configuration

```bash
mkdir -p ~/.cc-connect
cp config.example.toml ~/.cc-connect/config.toml
```

### Minimal `config.toml` — Claude Code + Telegram

```toml
[project.my-project]
name        = "my-project"
work_dir    = "/home/user/myproject"
data_dir    = "/home/user/.cc-connect/data"
admin_from  = "123456789"          # Your Telegram user ID

[project.my-project.agent]
type = "claude-code"               # claude-code | codex | cursor | gemini | qoder | opencode | iflow

[project.my-project.platform]
type  = "telegram"
token = "$TELEGRAM_BOT_TOKEN"      # set via env or paste value
```

### Multi-project config

```toml
# Project 1: Claude on Telegram
[project.dev]
name     = "dev"
work_dir = "/home/user/project-a"
data_dir = "/home/user/.cc-connect/data/dev"

[project.dev.agent]
type = "claude-code"

[project.dev.platform]
type  = "telegram"
token = "$TELEGRAM_BOT_TOKEN"

# Project 2: Gemini on Feishu
[project.research]
name     = "research"
work_dir = "/home/user/project-b"
data_dir = "/home/user/.cc-connect/data/research"

[project.research.agent]
type = "gemini"

[project.research.platform]
type           = "feishu"
app_id         = "$FEISHU_APP_ID"
app_secret     = "$FEISHU_APP_SECRET"
verification_token = "$FEISHU_VERIFICATION_TOKEN"
```

### All supported platform types

| `type` value | Platform | Public IP needed? |
|---|---|---|
| `telegram` | Telegram | No (long polling) |
| `feishu` | Feishu / Lark | No (WebSocket) |
| `dingtalk` | DingTalk | No (Stream) |
| `slack` | Slack | No (Socket Mode) |
| `discord` | Discord | No (Gateway) |
| `wecom` | WeChat Work | No (WS) / Yes (Webhook) |
| `line` | LINE | Yes (Webhook) |
| `qq` | QQ via NapCat/OneBot | No |
| `qqbot` | QQ Bot Official | No |
| `weixin` | Personal WeChat (beta) | No (ilink long polling) |

### All supported agent types

| `type` value | Agent |
|---|---|
| `claude-code` | Claude Code (Anthropic) |
| `codex` | Codex (OpenAI) |
| `cursor` | Cursor Agent |
| `gemini` | Gemini CLI (Google) |
| `qoder` | Qoder CLI |
| `opencode` | OpenCode / Crush |
| `iflow` | iFlow CLI |

---

## Platform-specific configuration

### Telegram

```toml
[project.mybot.platform]
type  = "telegram"
token = "$TELEGRAM_BOT_TOKEN"
# Get token from @BotFather on Telegram
# No public IP required — uses long polling
```

### Feishu / Lark

```toml
[project.mybot.platform]
type               = "feishu"
app_id             = "$FEISHU_APP_ID"
app_secret         = "$FEISHU_APP_SECRET"
verification_token = "$FEISHU_VERIFICATION_TOKEN"
# Uses WebSocket — no public IP needed
# Set up at https://open.feishu.cn/
```

### Slack

```toml
[project.mybot.platform]
type              = "slack"
bot_token         = "$SLACK_BOT_TOKEN"
app_token         = "$SLACK_APP_TOKEN"
# app_token must start with xapp- (Socket Mode)
# Enable Socket Mode in your Slack app settings
```

### Discord

```toml
[project.mybot.platform]
type  = "discord"
token = "$DISCORD_BOT_TOKEN"
# Uses Discord Gateway — no public IP needed
```

### DingTalk

```toml
[project.mybot.platform]
type       = "dingtalk"
client_id  = "$DINGTALK_CLIENT_ID"
client_secret = "$DINGTALK_CLIENT_SECRET"
# Uses DingTalk Stream — no public IP needed
```

### WeChat Work (WeCom)

```toml
[project.mybot.platform]
type           = "wecom"
corp_id        = "$WECOM_CORP_ID"
agent_id       = "$WECOM_AGENT_ID"
secret         = "$WECOM_SECRET"
connection_type = "websocket"   # websocket (no public IP) or webhook
```

### Personal WeChat (beta only)

```bash
# Install beta build first
npm install -g cc-connect@beta

# Scan QR code to log in
cc-connect weixin setup
```

```toml
[project.mybot.platform]
type = "weixin"
# Auth state is stored after QR scan — no public IP needed
```

---

## Running cc-connect

```bash
# Default config location: ~/.cc-connect/config.toml
cc-connect

# Custom config path
cc-connect --config /path/to/config.toml

# Run specific project only
cc-connect --project my-project
```

---

## Chat Commands (sent in the messaging platform)

| Command | Description |
|---|---|
| `/help` | Show all available commands |
| `/model <name>` | Switch AI model (e.g. `/model claude-opus-4-5`) |
| `/mode <mode>` | Change permission mode (e.g. `/mode auto`) |
| `/reasoning <level>` | Tune reasoning intensity |
| `/dir <path>` | Switch working directory for next session |
| `/dir <number>` | Jump to a directory from history |
| `/dir -` | Toggle to previous directory |
| `/dir reset` | Restore configured `work_dir` |
| `/cd <path>` | Alias for `/dir` |
| `/memory` | Read or write the agent's memory/instruction file |
| `/shell <cmd>` | Run a shell command (admin only) |
| `/session` | Manage sessions (list, continue, new) |
| `/continue` | Continue from last session (forks to avoid inheriting broken state) |
| `/cron <spec> <task>` | Schedule a recurring task |
| `/stop` | Stop the currently running agent |

### Slash command examples (in chat)

```
# Ask the agent to review a PR
Review the changes in branch feature/auth and summarize the risks.

# Switch to a different model
/model gemini-2.0-flash

# Change working directory
/dir /home/user/other-project

# Schedule a daily summary
/cron 0 6 * * * Summarize GitHub trending Go repos and post here

# Read agent memory
/memory

# Update agent memory
/memory Always prefer table-driven tests in Go. Use context.Context for cancellation.
```

---

## Multi-Agent Relay (group chat orchestration)

Bind multiple bots in one group chat so they communicate with each other:

```toml
# Bot 1: Claude
[project.claude-bot]
name     = "claude-bot"
work_dir = "/home/user/project"
data_dir = "/home/user/.cc-connect/data/claude"

[project.claude-bot.agent]
type = "claude-code"

[project.claude-bot.platform]
type  = "telegram"
token = "$TELEGRAM_CLAUDE_BOT_TOKEN"

# Bot 2: Gemini (same group)
[project.gemini-bot]
name     = "gemini-bot"
work_dir = "/home/user/project"
data_dir = "/home/user/.cc-connect/data/gemini"

[project.gemini-bot.agent]
type = "gemini"

[project.gemini-bot.platform]
type  = "telegram"
token = "$TELEGRAM_GEMINI_BOT_TOKEN"
```

Add both bots to the same Telegram group. Mention them by name and they will pick up and respond to each other's output.

---

## Voice and Multimodal

For platforms that support voice (Telegram, Feishu, DingTalk), enable speech in config:

```toml
[speech]
provider = "openai"           # openai | azure | google
api_key  = "$OPENAI_API_KEY"

[speech.stt]
model = "whisper-1"

[speech.tts]
model = "tts-1"
voice = "alloy"
```

Send a voice message in Telegram → cc-connect transcribes it → forwards text to the agent → optionally speaks the response back.

For images/screenshots: just attach the image in chat. cc-connect forwards it to multimodal-capable agents.

---

## Cron Scheduling

```toml
# In config.toml, per-project cron settings
[project.mybot.cron]
timeout = "30m"          # max runtime per job
fresh_session = true     # start a new session for each run
```

From chat:

```
# Every weekday at 9am, run a standup summary
/cron 0 9 * * 1-5 Summarize open PRs and blockers in this repo

# Every hour, check for new issues labeled "urgent"
/cron 0 * * * * Check for new GitHub issues labeled urgent and notify me
```

---

## Admin configuration

```toml
[project.mybot]
admin_from = "alice,123456789"   # comma-separated usernames or IDs
```

Admins can use `/shell`, `/dir`, and other privileged commands. Non-admins cannot.

---

## Directory structure

```
~/.cc-connect/
├── config.toml                          # main config
└── data/
    └── projects/
        └── my-project.state.json        # persisted dir override, session state
```

---

## Common patterns

### Pattern 1: Mobile-first AI development

Install cc-connect on your dev machine, connect it to Telegram. From your phone:
1. Send a task description as a message
2. Agent runs on your machine
3. Streamed response appears in chat
4. Reply to continue the conversation

### Pattern 2: Team shared AI bot (Slack/Feishu)

One cc-connect instance per project, shared in a team channel. Team members can ask questions, trigger code reviews, or run analyses — all without terminal access.

### Pattern 3: Scheduled reports

```
/cron 0 8 * * 1 Generate a weekly summary of commits and open issues, format as markdown
```

### Pattern 4: Multi-project routing

Run multiple projects in one `cc-connect` process, each bot handles a different repo or concern.

---

## Troubleshooting

### Bot not responding

1. Check that `cc-connect` is running: `ps aux | grep cc-connect`
2. Verify the platform token/credentials in config
3. For Telegram: ensure the bot token is valid (`/start` in BotFather chat)
4. For Feishu: check WebSocket connection in Feishu Open Platform console

### Agent not found

```bash
# Verify agent is installed and in PATH
which claude     # for claude-code
which gemini     # for gemini
which codex      # for codex
```

Set explicit path in config if needed:

```toml
[project.mybot.agent]
type = "claude-code"
bin  = "/usr/local/bin/claude"
```

### Session inherits broken state

Use `/continue` which forks the session, or start fresh:

```
/session new
```

### Personal WeChat not available

You need the beta build:

```bash
npm install -g cc-connect@beta
cc-connect weixin setup   # scan QR in terminal
```

### Context too long / auto-compress

Enable in config:

```toml
[project.mybot.agent]
auto_compress        = true
compress_threshold   = 80000   # tokens before compression kicks in
```

### Config not found

Default path is `~/.cc-connect/config.toml`. Pass explicitly:

```bash
cc-connect --config /custom/path/config.toml
```

### Check version

```bash
cc-connect --version
```

---

## Environment variables reference

| Variable | Used for |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token |
| `FEISHU_APP_ID` | Feishu app ID |
| `FEISHU_APP_SECRET` | Feishu app secret |
| `FEISHU_VERIFICATION_TOKEN` | Feishu verification token |
| `SLACK_BOT_TOKEN` | Slack bot OAuth token (`xoxb-...`) |
| `SLACK_APP_TOKEN` | Slack app-level token (`xapp-...`) |
| `DISCORD_BOT_TOKEN` | Discord bot token |
| `DINGTALK_CLIENT_ID` | DingTalk app client ID |
| `DINGTALK_CLIENT_SECRET` | DingTalk app client secret |
| `WECOM_CORP_ID` | WeChat Work corp ID |
| `WECOM_AGENT_ID` | WeChat Work agent ID |
| `WECOM_SECRET` | WeChat Work app secret |
| `OPENAI_API_KEY` | OpenAI API key (for Codex agent or STT/TTS) |

Values in `config.toml` can reference env vars using `$VAR_NAME` syntax.

---

## Platform setup guides

- Feishu/Lark: `docs/feishu.md`
- DingTalk: `docs/dingtalk.md`
- Telegram: `docs/telegram.md`
- Slack: `docs/slack.md`
- Discord: `docs/discord.md`
- WeChat Work: `docs/wecom.md`
- Personal WeChat (beta): `docs/weixin.md`
- QQ / QQ Bot: `docs/qq.md`
