---
name: pica-langchain
description: Integrate PICA into a LangChain/LangGraph Python application via MCP. Use when adding PICA tools to a LangChain agent, setting up PICA MCP with LangChain, or when the user mentions PICA with LangChain or LangGraph.
---

# PICA MCP Integration with LangChain

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

## Using PICA with LangChain

LangChain provides MCP client support via the `langchain-mcp-adapters` package. **Always refer to the latest docs before implementing.** See [langchain-mcp-reference.md](langchain-mcp-reference.md).

### Required packages

```bash
pip install langchain-mcp-adapters langgraph langchain-anthropic mcp python-dotenv
```

### Before implementing: look up the latest docs

The `langchain-mcp-adapters` API has changed across versions (e.g., `MultiServerMCPClient` is no longer a context manager as of v0.1.0). **Always check the latest docs** before writing code. See [langchain-mcp-reference.md](langchain-mcp-reference.md).

### Integration pattern

1. **Create an MCP client** using `MultiServerMCPClient` with stdio transport pointed at `npx @picahq/mcp`
2. **Get tools** from the client via `await client.get_tools()`
3. **Create a ReAct agent** using `create_react_agent(model, tools)` from `langgraph.prebuilt`
4. **Stream or invoke** the agent with your messages
5. Pass environment variables (`PICA_SECRET`, `PATH`, `HOME`) to the MCP client's `env` config

### Minimal example

```python
from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

model = ChatAnthropic(model="claude-haiku-4-5-20251001", streaming=True)

client = MultiServerMCPClient({
    "pica": {
        "command": "npx",
        "args": ["@picahq/mcp"],
        "transport": "stdio",
        "env": {
            "PICA_SECRET": os.environ.get("PICA_SECRET", ""),
            "PATH": os.environ.get("PATH", ""),
            "HOME": os.environ.get("HOME", ""),
        },
    },
})
tools = await client.get_tools()
agent = create_react_agent(model, tools)

# Invoke
result = await agent.ainvoke({"messages": [{"role": "user", "content": "..."}]})

# Or stream events
async for event in agent.astream_events({"messages": messages}, version="v2"):
    kind = event["event"]
    if kind == "on_chat_model_stream":
        content = event["data"]["chunk"].content
        # content may be a list of content blocks (Anthropic models) or a string
```

### Important: Anthropic content blocks

When streaming with `astream_events(version="v2")`, Anthropic models return `chunk.content` as a **list of content blocks**, not plain strings. Always handle both:

```python
if isinstance(content, list):
    text = "".join(
        block.get("text", "") if isinstance(block, dict) else str(block)
        for block in content
    )
elif isinstance(content, str):
    text = content
```

## Checklist

When setting up PICA MCP with LangChain:

- [ ] `langchain-mcp-adapters`, `langgraph`, `langchain-anthropic`, `mcp` are installed
- [ ] `PICA_SECRET` is set in `.env`
- [ ] `.env` is loaded via `python-dotenv` (`load_dotenv()` at top of file)
- [ ] MCP client uses stdio transport with `npx @picahq/mcp`
- [ ] `PATH` and `HOME` are passed in the MCP client `env` config
- [ ] `MultiServerMCPClient` is NOT used as a context manager (API changed in v0.1.0)
- [ ] Streaming handles both list and string content from Anthropic models
- [ ] Tool events (`on_tool_start`, `on_tool_end`) are handled for UI rendering

## Additional resources

- For LangChain MCP adapter docs and API details, see [langchain-mcp-reference.md](langchain-mcp-reference.md)
