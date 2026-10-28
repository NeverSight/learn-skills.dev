---
name: stash-ai-memory
description: Persistent memory layer for AI agents using Postgres/pgvector with MCP server support
triggers:
  - add persistent memory to my AI agent
  - set up stash memory server
  - give my LLM memory across sessions
  - install stash MCP server
  - configure AI agent memory with postgres
  - stash episodes facts working context
  - self-hosted AI memory layer
  - connect Claude to persistent memory
---

# Stash AI Memory

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Stash is a self-hosted persistent memory layer for AI agents. It stores episodes, facts, and working context in Postgres with pgvector, runs an 8-stage consolidation pipeline to turn raw observations into structured knowledge, and exposes everything via an MCP server that works with any MCP-compatible agent (Claude Desktop, Cursor, Windsurf, Cline, Continue, OpenAI Agents, Ollama, OpenRouter).

## Architecture

```
Agent ──► MCP Server ──► Postgres + pgvector
                │
                └──► Background Consolidation Pipeline
                     (Episodes → Facts → Relationships →
                      Causal Links → Goals → Failures →
                      Hypotheses → Confidence Decay)
```

## Quick Start (Docker — Recommended)

```bash
git clone https://github.com/alash3al/stash.git
cd stash
cp .env.example .env
# Edit .env with your LLM API key and model
docker compose up
```

This starts Postgres with pgvector, runs migrations, and launches the MCP server with background consolidation.

## Environment Configuration

```bash
# .env
# LLM provider (OpenAI-compatible endpoint)
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=$OPENAI_API_KEY
LLM_MODEL=gpt-4o-mini

# Or use Ollama (local)
# LLM_BASE_URL=http://localhost:11434/v1
# LLM_API_KEY=ollama
# LLM_MODEL=llama3.2

# Or OpenRouter
# LLM_BASE_URL=https://openrouter.ai/api/v1
# LLM_API_KEY=$OPENROUTER_API_KEY
# LLM_MODEL=anthropic/claude-3-haiku

# Postgres connection
DATABASE_URL=postgres://stash:stash@localhost:5432/stash?sslmode=disable

# MCP server
MCP_SERVER_ADDR=:8080

# Consolidation pipeline interval
CONSOLIDATION_INTERVAL=5m
```

## Binary / Manual Install

```bash
git clone https://github.com/alash3al/stash.git
cd stash

# Build the binary
go build -o stash ./cmd/stash

# Run migrations and start server
./stash serve
```

## Connecting MCP Clients

### Claude Desktop (`~/Library/Application Support/Claude/claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "stash": {
      "url": "http://localhost:8080/mcp",
      "transport": "http"
    }
  }
}
```

### Cursor / Windsurf / Cline (`.cursor/mcp.json` or equivalent)

```json
{
  "mcpServers": {
    "stash": {
      "url": "http://localhost:8080/mcp",
      "transport": "http"
    }
  }
}
```

### Continue (`~/.continue/config.json`)

```json
{
  "experimental": {
    "modelContextProtocolServers": [
      {
        "transport": {
          "type": "http",
          "url": "http://localhost:8080/mcp"
        }
      }
    ]
  }
}
```

## MCP Tools Exposed to Agents

Stash exposes these tools via MCP that agents call automatically:

| Tool | Purpose |
|------|---------|
| `stash_remember` | Store an episode or observation |
| `stash_recall` | Semantic search across memory |
| `stash_facts` | Query consolidated facts |
| `stash_context` | Get/set working context |
| `stash_forget` | Remove specific memories |

## Using Stash Programmatically (Go)

```go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/alash3al/stash/pkg/client"
)

func main() {
    c, err := client.New(client.Config{
        BaseURL: "http://localhost:8080",
    })
    if err != nil {
        log.Fatal(err)
    }

    ctx := context.Background()

    // Store an episode
    err = c.Remember(ctx, client.Episode{
        AgentID: "my-agent",
        Content: "User prefers dark mode and uses vim keybindings",
        Tags:    []string{"preferences", "ui"},
    })
    if err != nil {
        log.Fatal(err)
    }

    // Recall relevant memories
    results, err := c.Recall(ctx, client.RecallQuery{
        AgentID: "my-agent",
        Query:   "what are the user's editor preferences?",
        Limit:   5,
    })
    if err != nil {
        log.Fatal(err)
    }

    for _, r := range results {
        fmt.Printf("[%.2f] %s\n", r.Score, r.Content)
    }
}
```

## Docker Compose (Full Reference)

```yaml
# docker-compose.yml (from repo)
services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_USER: stash
      POSTGRES_PASSWORD: stash
      POSTGRES_DB: stash
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U stash"]
      interval: 5s
      timeout: 5s
      retries: 5

  stash:
    build: .
    env_file: .env
    environment:
      DATABASE_URL: postgres://stash:stash@postgres:5432/stash?sslmode=disable
    ports:
      - "8080:8080"
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  pgdata:
```

## Consolidation Pipeline

The 8-stage pipeline runs on a configurable interval (default 5 minutes) and processes only new data since the last run:

1. **Episodes** — raw observations stored by agents
2. **Facts** — discrete true/false statements extracted from episodes
3. **Relationships** — links between facts and entities
4. **Causal Links** — cause-and-effect patterns
5. **Goal Tracking** — inferred agent/user goals
6. **Failure Patterns** — what went wrong and why
7. **Hypothesis Verification** — testing inferred beliefs against new data
8. **Confidence Decay** — reducing confidence in stale/unconfirmed facts

To trigger consolidation manually (if supported):

```bash
curl -X POST http://localhost:8080/consolidate
```

## Working Context API

Working context is a scratchpad for in-flight session state:

```bash
# Set context
curl -X PUT http://localhost:8080/api/context/my-agent \
  -H "Content-Type: application/json" \
  -d '{"key": "current_task", "value": "debugging auth middleware"}'

# Get context
curl http://localhost:8080/api/context/my-agent
```

## Common Patterns

### Pattern 1: Agent with Memory in Python (via MCP HTTP)

```python
import requests

STASH_URL = "http://localhost:8080"

def remember(agent_id: str, content: str, tags: list[str] = None):
    requests.post(f"{STASH_URL}/api/episodes", json={
        "agent_id": agent_id,
        "content": content,
        "tags": tags or [],
    })

def recall(agent_id: str, query: str, limit: int = 5) -> list[dict]:
    r = requests.post(f"{STASH_URL}/api/recall", json={
        "agent_id": agent_id,
        "query": query,
        "limit": limit,
    })
    return r.json().get("results", [])

# Usage
remember("assistant-1", "User is building a Go microservice with gRPC")
memories = recall("assistant-1", "what is the user working on?")
for m in memories:
    print(f"[{m['score']:.2f}] {m['content']}")
```

### Pattern 2: Injecting Memory into System Prompt

```python
def build_system_prompt(agent_id: str, base_prompt: str, user_message: str) -> str:
    memories = recall(agent_id, user_message, limit=10)
    if not memories:
        return base_prompt

    memory_block = "\n".join(f"- {m['content']}" for m in memories)
    return f"""{base_prompt}

## Relevant Memory
{memory_block}
"""
```

### Pattern 3: OpenAI Agents SDK Integration

```python
from agents import Agent, Runner
from agents.mcp import MCPServerHTTP

stash_mcp = MCPServerHTTP(url="http://localhost:8080/mcp")

agent = Agent(
    name="my-agent",
    instructions="You have persistent memory. Use stash tools to remember and recall.",
    mcp_servers=[stash_mcp],
)

result = Runner.run_sync(agent, "What do you remember about my coding preferences?")
print(result.final_output)
```

## Troubleshooting

### Postgres connection refused
```bash
# Check pgvector extension is available
docker exec -it stash-postgres-1 psql -U stash -c "SELECT * FROM pg_extension WHERE extname='vector';"

# If missing, install it
docker exec -it stash-postgres-1 psql -U stash -c "CREATE EXTENSION vector;"
```

### MCP server not reachable from Claude Desktop
- Ensure `http://localhost:8080/mcp` is accessible (not `https`)
- Check Claude Desktop supports HTTP MCP transport (requires Claude Desktop ≥ 0.10)
- Try `curl http://localhost:8080/mcp` to verify the server is up

### Consolidation not running
```bash
# Check logs for consolidation pipeline errors
docker compose logs stash | grep -i consolidat

# Verify LLM credentials are correct — consolidation uses the LLM to extract facts
curl $LLM_BASE_URL/models -H "Authorization: Bearer $LLM_API_KEY"
```

### Embedding/recall returning no results
- Consolidation may not have run yet (wait one interval or trigger manually)
- Verify the LLM model supports embeddings or that a separate embedding model is configured
- Check that episodes were actually stored: `curl http://localhost:8080/api/episodes?agent_id=my-agent`

### Resetting all memory
```bash
# Nuclear option: wipe and restart
docker compose down -v
docker compose up
```

## Key Endpoints Reference

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/episodes` | Store a new episode |
| `POST` | `/api/recall` | Semantic recall query |
| `GET` | `/api/facts` | List consolidated facts |
| `GET/PUT` | `/api/context/:agent_id` | Working context |
| `DELETE` | `/api/episodes/:id` | Forget an episode |
| `POST` | `/consolidate` | Trigger consolidation manually |
| `GET` | `/health` | Health check |
| `*` | `/mcp` | MCP protocol endpoint |

## Self-Hosting Checklist

- [ ] Postgres 16+ with pgvector extension
- [ ] LLM API key with access to a chat-completion model
- [ ] Port 8080 accessible to your MCP clients
- [ ] Volume mounted for Postgres data persistence
- [ ] `CONSOLIDATION_INTERVAL` tuned to your usage (default `5m`)
- [ ] Agent IDs are consistent across sessions for memory continuity
