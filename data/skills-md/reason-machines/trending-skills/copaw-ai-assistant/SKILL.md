---
name: copaw-ai-assistant
description: Personal AI assistant framework supporting multiple chat channels (DingTalk, Feishu, QQ, Discord, etc.) with extensible skills, local/cloud deployment, and cron scheduling.
triggers:
  - set up CoPaw personal AI assistant
  - configure CoPaw with DingTalk or Feishu
  - add custom skills to CoPaw
  - deploy CoPaw on my machine
  - integrate CoPaw with Discord or Telegram
  - schedule tasks with CoPaw cron
  - connect CoPaw to local LLM models
  - troubleshoot CoPaw channel configuration
---

# CoPaw AI Assistant Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

CoPaw is a personal AI assistant framework you deploy on your own machine or in the cloud. It connects to multiple chat platforms (DingTalk, Feishu, QQ, Discord, iMessage, Telegram, Mattermost, Matrix, MQTT) through a single agent, supports custom Python skills, scheduled cron jobs, local and cloud LLMs, and provides a web Console at `http://127.0.0.1:8088/`.

---

## Installation

### pip (recommended if Python 3.10–3.13 is available)

```bash
pip install copaw
copaw init --defaults    # non-interactive setup with sensible defaults
copaw app                # starts the web Console + backend
```

### Script install (no Python setup required)

**macOS / Linux:**
```bash
curl -fsSL https://copaw.agentscope.io/install.sh | bash
# With Ollama support:
curl -fsSL https://copaw.agentscope.io/install.sh | bash -s -- --extras ollama
# Multiple extras:
curl -fsSL https://copaw.agentscope.io/install.sh | bash -s -- --extras ollama,llamacpp
```

**Windows CMD:**
```cmd
curl -fsSL https://copaw.agentscope.io/install.bat -o install.bat && install.bat
```

**Windows PowerShell:**
```powershell
irm https://copaw.agentscope.io/install.ps1 | iex
```

After script install, open a new terminal:
```bash
copaw init --defaults
copaw app
```

### Install from source

```bash
git clone https://github.com/agentscope-ai/CoPaw.git
cd CoPaw
pip install -e ".[dev]"
copaw init --defaults
copaw app
```

---

## CLI Reference

```bash
copaw init                  # interactive workspace setup
copaw init --defaults       # non-interactive setup
copaw app                   # start the Console (http://127.0.0.1:8088/)
copaw app --port 8090       # use a custom port
copaw --help                # list all commands
```

---

## Workspace Structure

After `copaw init`, a workspace is created (default: `~/.copaw/workspace/`):

```
~/.copaw/workspace/
├── config.yaml          # agent, provider, channel configuration
├── skills/              # custom skill files (auto-loaded)
│   └── my_skill.py
├── memory/              # conversation memory storage
└── logs/                # runtime logs
```

---

## Configuration (`config.yaml`)

`copaw init` generates this file. Edit it directly or use the Console UI.

### LLM Provider (OpenAI-compatible)

```yaml
providers:
  - id: openai-main
    type: openai
    api_key: ${OPENAI_API_KEY}        # use env var reference
    model: gpt-4o
    base_url: https://api.openai.com/v1

  - id: local-ollama
    type: ollama
    model: llama3.2
    base_url: http://localhost:11434
```

### Agent Settings

```yaml
agent:
  name: CoPaw
  language: en                        # en, zh, ja, etc.
  provider_id: openai-main
  context_limit: 8000
```

### Channel: DingTalk

```yaml
channels:
  - type: dingtalk
    app_key: ${DINGTALK_APP_KEY}
    app_secret: ${DINGTALK_APP_SECRET}
    agent_id: ${DINGTALK_AGENT_ID}
    mention_only: true                # only respond when @mentioned in groups
```

### Channel: Feishu (Lark)

```yaml
channels:
  - type: feishu
    app_id: ${FEISHU_APP_ID}
    app_secret: ${FEISHU_APP_SECRET}
    mention_only: false
```

### Channel: Discord

```yaml
channels:
  - type: discord
    token: ${DISCORD_BOT_TOKEN}
    mention_only: true
```

### Channel: Telegram

```yaml
channels:
  - type: telegram
    token: ${TELEGRAM_BOT_TOKEN}
```

### Channel: QQ

```yaml
channels:
  - type: qq
    uin: ${QQ_UIN}
    password: ${QQ_PASSWORD}
```

### Channel: Mattermost

```yaml
channels:
  - type: mattermost
    url: ${MATTERMOST_URL}
    token: ${MATTERMOST_TOKEN}
    team: my-team
```

### Channel: Matrix

```yaml
channels:
  - type: matrix
    homeserver: ${MATRIX_HOMESERVER}
    user_id: ${MATRIX_USER_ID}
    access_token: ${MATRIX_ACCESS_TOKEN}
```

---

## Custom Skills

Skills are Python files placed in `~/.copaw/workspace/skills/`. They are **auto-loaded** when CoPaw starts — no registration step needed.

### Minimal skill structure

```python
# ~/.copaw/workspace/skills/weather.py

SKILL_NAME = "get_weather"
SKILL_DESCRIPTION = "Get current weather for a city"

# Tool schema (OpenAI function-calling format)
SKILL_SCHEMA = {
    "type": "function",
    "function": {
        "name": SKILL_NAME,
        "description": SKILL_DESCRIPTION,
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name, e.g. 'Tokyo'"
                }
            },
            "required": ["city"]
        }
    }
}


def get_weather(city: str) -> str:
    """Fetch weather data for the given city."""
    import os
    import requests

    api_key = os.environ["OPENWEATHER_API_KEY"]
    url = f"https://api.openweathermap.org/data/2.5/weather"
    resp = requests.get(url, params={"q": city, "appid": api_key, "units": "metric"})
    resp.raise_for_status()
    data = resp.json()
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    return f"{city}: {temp}°C, {desc}"
```

### Skill with async support

```python
# ~/.copaw/workspace/skills/summarize_url.py

SKILL_NAME = "summarize_url"
SKILL_DESCRIPTION = "Fetch and summarize the content of a URL"

SKILL_SCHEMA = {
    "type": "function",
    "function": {
        "name": SKILL_NAME,
        "description": SKILL_DESCRIPTION,
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL to summarize"}
            },
            "required": ["url"]
        }
    }
}


async def summarize_url(url: str) -> str:
    import httpx

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url)
        text = resp.text[:4000]   # truncate for context limit
    return f"Content preview from {url}:\n{text}"
```

### Skill returning structured data

```python
# ~/.copaw/workspace/skills/list_files.py

import os
import json

SKILL_NAME = "list_files"
SKILL_DESCRIPTION = "List files in a directory"

SKILL_SCHEMA = {
    "type": "function",
    "function": {
        "name": SKILL_NAME,
        "description": SKILL_DESCRIPTION,
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Absolute or relative directory path"
                },
                "extension": {
                    "type": "string",
                    "description": "Filter by extension, e.g. '.py'. Optional."
                }
            },
            "required": ["path"]
        }
    }
}


def list_files(path: str, extension: str = "") -> str:
    entries = os.listdir(os.path.expanduser(path))
    if extension:
        entries = [e for e in entries if e.endswith(extension)]
    return json.dumps(sorted(entries))
```

---

## Cron / Scheduled Tasks

Define cron jobs in `config.yaml` to run skills on a schedule and push results to a channel:

```yaml
cron:
  - id: daily-digest
    schedule: "0 8 * * *"            # every day at 08:00
    skill: get_weather
    skill_args:
      city: "Tokyo"
    channel_id: dingtalk-main         # matches a channel id below
    message_template: "Good morning! Today's weather: {result}"

  - id: hourly-news
    schedule: "0 * * * *"
    skill: fetch_tech_news
    channel_id: discord-main
```

---

## Local Model Setup

### Ollama

```bash
# Install Ollama: https://ollama.ai
ollama pull llama3.2
ollama serve   # starts on http://localhost:11434
```

```yaml
# config.yaml
providers:
  - id: ollama-local
    type: ollama
    model: llama3.2
    base_url: http://localhost:11434
```

### LM Studio

```yaml
providers:
  - id: lmstudio-local
    type: lmstudio
    model: lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF
    base_url: http://localhost:1234/v1
```

### llama.cpp (extra required)

```bash
pip install "copaw[llamacpp]"
```

```yaml
providers:
  - id: llamacpp-local
    type: llamacpp
    model_path: /path/to/model.gguf
```

---

## Tool Guard (Security)

Tool Guard blocks risky tool calls and requires user approval before execution. Configure in `config.yaml`:

```yaml
agent:
  tool_guard:
    enabled: true
    risk_patterns:
      - "rm -rf"
      - "DROP TABLE"
      - "os.system"
    auto_approve_low_risk: true
```

When a call is blocked, the Console shows an approval prompt. The user can approve or deny before the tool runs.

---

## Token Usage Tracking

Token usage is tracked automatically and visible in the Console dashboard. Access programmatically:

```python
# In a skill or debug script
from copaw.telemetry import get_usage_summary

summary = get_usage_summary()
print(summary)
# {'total_tokens': 142300, 'prompt_tokens': 98200, 'completion_tokens': 44100, 'by_provider': {...}}
```

---

## Environment Variables

Set these before running `copaw app`, or reference them in `config.yaml` as `${VAR_NAME}`:

```bash
# LLM providers
export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...

# Channels
export DINGTALK_APP_KEY=...
export DINGTALK_APP_SECRET=...
export DINGTALK_AGENT_ID=...

export FEISHU_APP_ID=...
export FEISHU_APP_SECRET=...

export DISCORD_BOT_TOKEN=...
export TELEGRAM_BOT_TOKEN=...

export QQ_UIN=...
export QQ_PASSWORD=...

export MATTERMOST_URL=...
export MATTERMOST_TOKEN=...

export MATRIX_HOMESERVER=...
export MATRIX_USER_ID=...
export MATRIX_ACCESS_TOKEN=...

# Custom skill secrets
export OPENWEATHER_API_KEY=...
```

---

## Common Patterns

### Pattern: Morning briefing to DingTalk

```yaml
# config.yaml excerpt
channels:
  - id: dingtalk-main
    type: dingtalk
    app_key: ${DINGTALK_APP_KEY}
    app_secret: ${DINGTALK_APP_SECRET}
    agent_id: ${DINGTALK_AGENT_ID}

cron:
  - id: morning-brief
    schedule: "30 7 * * 1-5"         # weekdays 07:30
    skill: daily_briefing
    channel_id: dingtalk-main
```

```python
# skills/daily_briefing.py
SKILL_NAME = "daily_briefing"
SKILL_DESCRIPTION = "Compile a morning briefing with weather and news"

SKILL_SCHEMA = {
    "type": "function",
    "function": {
        "name": SKILL_NAME,
        "description": SKILL_DESCRIPTION,
        "parameters": {"type": "object", "properties": {}, "required": []}
    }
}

def daily_briefing() -> str:
    import os, requests, datetime

    today = datetime.date.today().strftime("%A, %B %d")
    # Add your own data sources here
    return f"Good morning! Today is {today}. Have a productive day!"
```

### Pattern: Multi-channel broadcast

```python
# skills/broadcast.py
SKILL_NAME = "broadcast_message"
SKILL_DESCRIPTION = "Send a message to all configured channels"

SKILL_SCHEMA = {
    "type": "function",
    "function": {
        "name": SKILL_NAME,
        "description": SKILL_DESCRIPTION,
        "parameters": {
            "type": "object",
            "properties": {
                "message": {"type": "string", "description": "Message to broadcast"}
            },
            "required": ["message"]
        }
    }
}

def broadcast_message(message: str) -> str:
    # CoPaw handles routing; return the message and let the agent deliver it
    return f"[BROADCAST] {message}"
```

### Pattern: File summarization skill

```python
# skills/summarize_file.py
SKILL_NAME = "summarize_file"
SKILL_DESCRIPTION = "Read and summarize a local file"

SKILL_SCHEMA = {
    "type": "function",
    "function": {
        "name": SKILL_NAME,
        "description": SKILL_DESCRIPTION,
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Absolute path to the file"}
            },
            "required": ["file_path"]
        }
    }
}

def summarize_file(file_path: str) -> str:
    import os

    path = os.path.expanduser(file_path)
    if not os.path.exists(path):
        return f"File not found: {path}"

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read(8000)

    return f"File: {path}\nSize: {os.path.getsize(path)} bytes\nContent preview:\n{content}"
```

---

## Troubleshooting

### Console not accessible at port 8088

```bash
# Use a different port
copaw app --port 8090

# Check if another process is using 8088
lsof -i :8088    # macOS/Linux
netstat -ano | findstr :8088   # Windows
```

### Skills not loading

- Confirm the skill file is in `~/.copaw/workspace/skills/`
- Confirm `SKILL_NAME`, `SKILL_DESCRIPTION`, `SKILL_SCHEMA`, and the handler function are all defined at module level
- Check `~/.copaw/workspace/logs/` for import errors
- Restart `copaw app` after adding new skill files

### Channel not receiving messages

1. Verify credentials are set correctly (env vars or `config.yaml`)
2. Check the Console → Channels page for connection status
3. For DingTalk/Feishu/Discord with `mention_only: true`, the bot must be @mentioned
4. Discord messages over 2000 characters are split automatically — ensure the bot has `Send Messages` permission

### LLM provider connection fails

```bash
# Test provider from CLI (Console → Providers → Test Connection)
# Or check logs:
tail -f ~/.copaw/workspace/logs/copaw.log
```

- For Ollama: confirm `ollama serve` is running and `base_url` matches
- For OpenAI-compatible APIs: verify `base_url` ends with `/v1`
- LLM calls auto-retry with exponential backoff — transient failures resolve automatically

### Windows encoding issues

```cmd
# Set UTF-8 encoding for CMD
chcp 65001
```

Or set in environment:
```bash
export PYTHONIOENCODING=utf-8
```

### Workspace reset

```bash
# Reinitialize workspace (preserves skills/)
copaw init

# Full reset (destructive)
rm -rf ~/.copaw/workspace
copaw init --defaults
```

---

## ModelScope Cloud Deployment

For one-click cloud deployment without local setup:

1. Visit [ModelScope CoPaw Studio](https://modelscope.cn/studios/fork?target=AgentScope/CoPaw)
2. Fork the studio to your account
3. Set environment variables in the studio settings
4. Start the studio — Console is accessible via the studio URL

---

## Key Links

- **Documentation**: https://copaw.agentscope.io/
- **Channel setup guides**: https://copaw.agentscope.io/docs/channels
- **Release notes**: https://agentscope-ai.github.io/CoPaw/release-notes
- **GitHub**: https://github.com/agentscope-ai/CoPaw
- **PyPI**: https://pypi.org/project/copaw/
- **Discord community**: https://discord.gg/eYMpfnkG8h
