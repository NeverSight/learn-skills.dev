---
name: pica-crewai
description: Integrate PICA into a CrewAI Python application via MCP. Use when adding PICA tools to a CrewAI agent, setting up PICA MCP with CrewAI, or when the user mentions PICA with CrewAI.
---

# PICA MCP Integration with CrewAI

PICA provides a unified API platform that connects AI agents to third-party services (CRMs, email, calendars, databases, etc.) through MCP tool calling.

## PICA MCP Server

PICA exposes its capabilities through an MCP server distributed as `@picahq/mcp`. It uses **stdio transport** — it runs as a local subprocess via `npx`.

### MCP Configuration

```json
{
  "mcpServers": {
    "pica": {
      "command": "npx",
      "args": ["@picahq/mcp"],
      "env": {
        "PICA_SECRET": "your-pica-secret-key"
      }
    }
  }
}
```

- **Package**: `@picahq/mcp` (run via `npx`, no install needed)
- **Auth**: `PICA_SECRET` environment variable (obtain from the PICA dashboard https://app.picaos.com/settings/api-keys)
- **Transport**: stdio (standard input/output)

### Environment Variable

Always store the PICA secret in an environment variable, never hardcode it:

```
PICA_SECRET=sk_test_...
```

Add it to `.env` and load with `python-dotenv`.

## Using PICA with CrewAI

CrewAI provides built-in MCP support via `MCPServerStdio` from `crewai.mcp`. **Always refer to the latest docs before implementing.** See [crewai-mcp-reference.md](crewai-mcp-reference.md).

### Required packages

```bash
pip install "crewai[anthropic]" python-dotenv
```

The `[anthropic]` extra is **required** when using Anthropic models — without it you get `Anthropic native provider not available`.

### Before implementing: look up the latest docs

The CrewAI API evolves across versions. **Always check the latest docs** before writing code. See [crewai-mcp-reference.md](crewai-mcp-reference.md).

### Integration pattern

1. **Attach MCP servers** directly to an `Agent` via the `mcps` parameter using `MCPServerStdio`
2. **Configure the LLM** with `LLM(model="anthropic/claude-haiku-4-5-20251001", stream=True)`
3. **Create a Task and Crew**, then call `crew.kickoff()`
4. Pass environment variables (`PICA_SECRET`, `PATH`, `HOME`) to `MCPServerStdio`'s `env` config

### Minimal example

```python
from crewai import Agent, Task, Crew, Process, LLM
from crewai.mcp import MCPServerStdio

llm = LLM(model="anthropic/claude-haiku-4-5-20251001", stream=True)

agent = Agent(
    role="PICA Assistant",
    goal="Help the user with their request",
    backstory="You are a helpful AI assistant with access to PICA tools.",
    llm=llm,
    mcps=[
        MCPServerStdio(
            command="npx",
            args=["@picahq/mcp"],
            env={
                "PICA_SECRET": os.environ.get("PICA_SECRET", ""),
                "PATH": os.environ.get("PATH", ""),
                "HOME": os.environ.get("HOME", ""),
            },
        ),
    ],
    verbose=True,
)

task = Task(
    description="User's prompt here",
    expected_output="A helpful response addressing the user's request.",
    agent=agent,
)

crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
result = crew.kickoff()
```

### Important: streaming with CrewAI events

CrewAI runs synchronously. To stream responses (e.g., via FastAPI SSE), run the crew in a thread executor and use an event listener to forward chunks:

```python
from crewai.events import BaseEventListener, LLMStreamChunkEvent

class StreamListener(BaseEventListener):
    def setup_listeners(self, crewai_event_bus):
        @crewai_event_bus.on(LLMStreamChunkEvent)
        def on_chunk(source, event):
            # event.chunk contains the text chunk
            pass
```

**Thread safety**: when using `asyncio.Queue` to bridge the sync crew thread and an async event loop, use `loop.call_soon_threadsafe(queue.put_nowait, item)` instead of `queue.put_nowait()` directly — `asyncio.Queue` is not thread-safe.

### Key event types

- `LLMStreamChunkEvent` — streaming text chunks (`event.chunk`)
- `ToolUsageStartedEvent` — tool call started (`event.tool_name`, `event.tool_input`)
- `ToolUsageFinishedEvent` — tool call finished (`event.tool_name`, `event.tool_output`)
- `CrewKickoffCompletedEvent` — crew finished execution

## Checklist

When setting up PICA MCP with CrewAI:

- [ ] `crewai[anthropic]` is installed (the `[anthropic]` extra is required)
- [ ] `PICA_SECRET` is set in `.env`
- [ ] `.env` is loaded via `python-dotenv` (`load_dotenv()` at top of file)
- [ ] `MCPServerStdio` uses `npx @picahq/mcp` with `PICA_SECRET`, `PATH`, `HOME` in `env`
- [ ] LLM model string uses `anthropic/` prefix (e.g., `anthropic/claude-haiku-4-5-20251001`)
- [ ] If streaming, event listener uses `loop.call_soon_threadsafe()` for thread-safe queue puts
- [ ] Entire crew setup is wrapped in `try/except` with a `finally` to signal completion

## Additional resources

- For CrewAI MCP docs and API details, see [crewai-mcp-reference.md](crewai-mcp-reference.md)
