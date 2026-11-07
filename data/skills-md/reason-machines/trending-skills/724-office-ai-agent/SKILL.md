---
name: 724-office-ai-agent
description: Self-evolving AI agent system with 26 tools, three-layer memory, MCP plugins, and 24/7 self-repair in pure Python.
triggers:
  - set up a self-evolving AI agent
  - add tools to my AI agent at runtime
  - configure three-layer memory for an agent
  - connect MCP servers to my agent
  - schedule recurring tasks with an AI agent
  - build a 24/7 production AI agent system
  - integrate WeChat Work with an AI agent
  - create custom agent tools with a decorator
---

# 7/24 Office AI Agent System

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A 24/7 production AI agent in ~3,500 lines of pure Python with no framework dependencies. Features 26 built-in tools, three-layer memory (session + compressed + vector), MCP/plugin support, runtime tool creation, self-repair diagnostics, and cron scheduling.

## Installation

```bash
git clone https://github.com/wangziqi06/724-office.git
cd 724-office

# Only 3 runtime dependencies
pip install croniter lancedb websocket-client

# Optional: WeChat silk audio decoding
pip install pilk

# Set up directories
mkdir -p workspace/memory workspace/files

# Configure
cp config.example.json config.json
```

## Configuration (`config.json`)

```json
{
  "models": {
    "default": {
      "api_base": "https://api.openai.com/v1",
      "api_key": "${OPENAI_API_KEY}",
      "model": "gpt-4o",
      "max_tokens": 4096
    },
    "embedding": {
      "api_base": "https://api.openai.com/v1",
      "api_key": "${OPENAI_API_KEY}",
      "model": "text-embedding-3-small"
    }
  },
  "messaging": {
    "platform": "wxwork",
    "corp_id": "${WXWORK_CORP_ID}",
    "corp_secret": "${WXWORK_CORP_SECRET}",
    "agent_id": "${WXWORK_AGENT_ID}",
    "token": "${WXWORK_TOKEN}",
    "encoding_aes_key": "${WXWORK_AES_KEY}"
  },
  "memory": {
    "session_max_messages": 40,
    "compression_overlap": 5,
    "dedup_threshold": 0.92,
    "retrieval_top_k": 5,
    "lancedb_path": "workspace/memory"
  },
  "asr": {
    "api_base": "https://api.openai.com/v1",
    "api_key": "${OPENAI_API_KEY}",
    "model": "whisper-1"
  },
  "scheduler": {
    "jobs_file": "workspace/jobs.json",
    "timezone": "Asia/Shanghai"
  },
  "server": {
    "host": "0.0.0.0",
    "port": 8080
  },
  "workspace": "workspace",
  "mcp_servers": {}
}
```

Set environment variables rather than hardcoding secrets:

```bash
export OPENAI_API_KEY="sk-..."
export WXWORK_CORP_ID="..."
export WXWORK_CORP_SECRET="..."
```

## Running the Agent

```bash
# Start the HTTP server (listens on :8080 by default)
python3 xiaowang.py

# Point your messaging platform webhook to:
# http://YOUR_SERVER_IP:8080/
```

## File Structure

```
724-office/
├── xiaowang.py      # Entry point: HTTP server, debounce, ASR, media download
├── llm.py           # Tool-use loop, session management, memory injection
├── tools.py         # 26 built-in tools + @tool decorator + plugin loader
├── memory.py        # Three-layer memory pipeline
├── scheduler.py     # Cron + one-shot scheduling, jobs.json persistence
├── mcp_client.py    # JSON-RPC MCP client (stdio + HTTP)
├── router.py        # Multi-tenant Docker routing
├── config.py        # Config loading and env interpolation
└── workspace/
    ├── memory/      # LanceDB vector store
    ├── files/       # Agent file storage
    ├── SOUL.md      # Agent personality
    ├── AGENT.md     # Operational procedures
    └── USER.md      # User preferences/context
```

## Adding a Built-in Tool

Tools are registered with the `@tool` decorator in `tools.py`:

```python
from tools import tool

@tool(
    name="fetch_weather",
    description="Get current weather for a city.",
    parameters={
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "City name, e.g. 'Beijing'"
            },
            "units": {
                "type": "string",
                "enum": ["metric", "imperial"],
                "default": "metric"
            }
        },
        "required": ["city"]
    }
)
def fetch_weather(city: str, units: str = "metric") -> str:
    import urllib.request, json
    api_key = os.environ["OPENWEATHER_API_KEY"]
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={api_key}"
    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read())
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    return f"{city}: {temp}°, {desc}"
```

The tool is automatically available to the LLM in the next tool-use loop iteration.

## Runtime Tool Creation (Agent Creates Its Own Tools)

The agent can call `create_tool` during a conversation to write and load a new Python tool without restarting:

```
User: "Create a tool that converts Markdown to HTML."

Agent calls: create_tool({
  "name": "md_to_html",
  "description": "Convert a Markdown string to HTML.",
  "parameters": { ... },
  "code": "import markdown\ndef md_to_html(text): return markdown.markdown(text)"
})
```

The tool is saved to `workspace/custom_tools/md_to_html.py` and hot-loaded immediately.

## Connecting an MCP Server

Edit `config.json` to add MCP servers (stdio or HTTP):

```json
{
  "mcp_servers": {
    "filesystem": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/data"]
    },
    "myapi": {
      "transport": "http",
      "url": "http://localhost:3000/mcp"
    }
  }
}
```

MCP tools are namespaced as `servername__toolname` (double underscore). Reload without restart:

```
User: "reload MCP servers"
# Agent calls: reload_mcp()
```

## Scheduling Tasks

The agent uses `schedule` tool internally, but you can also call the scheduler API directly:

```python
from scheduler import Scheduler
import json

sched = Scheduler(jobs_file="workspace/jobs.json", timezone="Asia/Shanghai")

# One-shot task (ISO 8601)
sched.add_job(
    job_id="morning_brief",
    trigger="2026-04-01T09:00:00",
    action={"type": "message", "content": "Good morning! Here's your daily brief."},
    user_id="user_001"
)

# Recurring cron task
sched.add_job(
    job_id="weekly_report",
    trigger="0 9 * * MON",          # Every Monday 09:00
    action={"type": "llm_task", "prompt": "Generate weekly summary"},
    user_id="user_001"
)

sched.start()
```

Jobs persist in `workspace/jobs.json` across restarts.

## Three-Layer Memory System

```python
from memory import MemoryManager

mem = MemoryManager(config["memory"])

# Layer 1 — session history (auto-managed, last 40 msgs)
mem.append_session(user_id="u1", session_id="s1", role="user", content="Hello!")

# Layer 2 — long-term compressed (triggered on session overflow)
# LLM extracts structured facts; deduped at cosine similarity 0.92
mem.compress_and_store(user_id="u1", messages=evicted_messages)

# Layer 3 — vector retrieval (injected into system prompt automatically)
results = mem.retrieve(user_id="u1", query="user's dietary preferences", top_k=5)
for r in results:
    print(r["content"], r["score"])
```

The LLM pipeline in `llm.py` injects retrieved memories automatically before each call:

```python
# Simplified from llm.py
relevant = memory.retrieve(user_id, query=user_message, top_k=5)
memory_block = "\n".join(f"- {m['content']}" for m in relevant)
system_prompt = base_prompt + f"\n\n## Relevant Memory\n{memory_block}"
```

## Personality Files

Create these in `workspace/` to shape agent behavior:

**`workspace/SOUL.md`** — Personality and values:
```markdown
# Agent Soul
You are Xiao Wang, a diligent 24/7 office assistant.
- Always respond in the user's language
- Be concise but thorough
- Proactively suggest next steps
```

**`workspace/AGENT.md`** — Operational procedures:
```markdown
# Operational Guide
## On Error
1. Check logs in workspace/logs/
2. Run self_check() tool
3. Notify owner if critical

## Daily Routine
- 09:00 Morning brief
- 17:00 EOD summary
```

**`workspace/USER.md`** — User context:
```markdown
# User Profile
- Name: Alice
- Timezone: UTC+8
- Prefers bullet-point summaries
- Primary language: English
```

## Tool-Use Loop (Core LLM Flow)

```python
# Simplified representation of llm.py's main loop
async def run(user_id, session_id, user_message, media=None):
    messages = memory.get_session(user_id, session_id)
    messages.append({"role": "user", "content": user_message})

    for iteration in range(20):          # max 20 tool iterations
        response = await llm_call(
            model=config["models"]["default"],
            messages=inject_memory(messages, user_id, user_message),
            tools=tools.get_schema(),    # all 26 + plugins + MCP
        )

        if response.finish_reason == "stop":
            # Final text reply — send to user
            return response.content

        if response.finish_reason == "tool_calls":
            for call in response.tool_calls:
                result = await tools.execute(call.name, call.arguments)
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": str(result)
                })
            # Loop continues with tool results appended
```

## Self-Repair and Diagnostics

```python
# The agent runs self_check() daily via scheduler
# Or you can trigger it manually:

# Via chat: "run self-check"
# Agent calls: self_check()

# Via chat: "diagnose the last session"
# Agent calls: diagnose(session_id="s_20260322_001")
```

`self_check` scans:
- Error logs for exception patterns
- Session health (response times, tool failures)
- Memory store integrity
- Scheduled job status

Sends notification via the configured messaging platform if issues are found.

## Multi-Tenant Docker Routing

`router.py` provisions one container per user automatically:

```python
# router.py handles:
# POST / with user_id header -> route to user's container
# If container missing -> docker run 724-office:latest with user env
# Health-check every 30s -> restart unhealthy containers

# Deploy the router separately:
python3 router.py  # listens on :80, routes to per-user :8080+N
```

Docker labels used for discovery:
```
724office.user_id=<user_id>
724office.port=<assigned_port>
```

## Common Patterns

### Send a proactive message from a scheduled job

```python
# In a scheduled job action, "type": "message" sends directly to user
{
  "type": "message",
  "content": "Your weekly report is ready!",
  "attachments": ["workspace/files/report.pdf"]
}
```

### Search memory semantically

```python
# Via agent tool call:
results = tools.execute("search_memory", {
    "query": "what did the user say about the Q1 budget?",
    "top_k": 3
})
```

### Execute arbitrary Python in the agent's process

```python
# exec tool (use carefully — runs in-process)
tools.execute("exec", {
    "code": "import psutil; return psutil.virtual_memory().percent"
})
```

### List and manage schedules

```
User: "list all scheduled tasks"
Agent calls: list_schedules()

User: "cancel the weekly_report job"
Agent calls: remove_schedule({"job_id": "weekly_report"})
```

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `ImportError: lancedb` | Missing dependency | `pip install lancedb` |
| Memory retrieval empty | LanceDB not initialized | Ensure `workspace/memory/` exists; send a few messages first |
| MCP tool not found | Server not connected | Check `config.json` mcp_servers; call `reload_mcp` |
| Scheduler not firing | Timezone mismatch | Set `scheduler.timezone` in config to your local TZ |
| Tool loop hits 20 iterations | Runaway tool chain | Add guardrails in `AGENT.md`; check for circular tool calls |
| WeChat webhook 403 | Token mismatch | Verify `WXWORK_TOKEN` and `WXWORK_AES_KEY` env vars |
| High RAM on Jetson | LanceDB index size | Reduce `retrieval_top_k`; use local embedding model |
| `create_tool` not persisting | Wrong workspace path | Confirm `workspace/custom_tools/` directory exists and is writable |

## Edge Deployment (Jetson Orin Nano)

```bash
# ARM64-compatible — no GPU required for core agent
# Use a local embedding model to avoid cloud latency:
pip install sentence-transformers

# In config.json, point embedding to local model:
{
  "models": {
    "embedding": {
      "type": "local",
      "model": "BAAI/bge-small-en-v1.5"
    }
  }
}

# Keep RAM under 2GB budget:
# - session_max_messages: 20 (reduce from 40)
# - retrieval_top_k: 3 (reduce from 5)
# - Avoid loading large MCP servers
```
