---
name: notion
description: "Use this skill when you need to work with notion through its generated async Python app, call its MCP-backed functions from code, or inspect available functions with the mcp-skill CLI."
metadata:
  short-description: "Use notion from async Python"
---

# notion

Use this skill when you need to work with notion through its generated async Python app, call its MCP-backed functions from code, or inspect available functions with the mcp-skill CLI.

## Authentication

This app can use the MCP client's built-in OAuth flow when the server requires it.
In most cases, the default constructor is enough. Tokens are persisted to
`~/.mcp-skill/auth/` so subsequent runs reuse the same credentials automatically.

```python
app = NotionApp()
```

If you need a custom OAuth provider, pass it via the `auth` argument:

```python
app = NotionApp(auth=my_oauth_provider)
```

## Dependencies

This skill requires the following Python packages:

- `mcp-skill`

Install with uv:

```bash
uv pip install mcp-skill
```

Or with pip:

```bash
pip install mcp-skill
```

## Python Usage

Use the generated app directly in async Python code:

```python
import asyncio
from notion.app import NotionApp


async def main():
    app = NotionApp()
    result = await app.notion_search(query="example", query_type="example", content_search_mode="example")
    print(result)


asyncio.run(main())
```

## Async Usage Notes

- Every generated tool method is `async`, so call it with `await`.
- Use these apps inside an async function, then run that function with `asyncio.run(...)` if you are in a script.
- If you forget `await`, you will get a coroutine object instead of the actual tool result.
- Be careful when mixing this with other event-loop environments such as notebooks, web servers, or async frameworks.

## Discover Functions with the CLI

Use the CLI to find available apps, list functions on an app, and inspect a function before calling it:

```bash
uvx mcp-skill list-apps
uvx mcp-skill list-functions notion
uvx mcp-skill inspect notion notion_search
```

**Important:** Add `.agents/skills` to your Python path so imports resolve correctly:

```python
import sys
sys.path.insert(0, ".agents/skills")
from notion.app import NotionApp
```

Or set the `PYTHONPATH` environment variable:

```bash
export PYTHONPATH=".agents/skills:$PYTHONPATH"
```

**Preferred: use `uv run`** (handles dependencies automatically):

```bash
PYTHONPATH=.agents/skills uv run --with mcp-skill python -c "
import asyncio
from notion.app import NotionApp

async def main():
    app = NotionApp()
    result = await app.notion_search(query="example", query_type="example", content_search_mode="example")
    print(result)

asyncio.run(main())
"
```

**Alternative: use `python` directly** (install dependencies first):

```bash
pip install mcp-skill
PYTHONPATH=.agents/skills python -c "
import asyncio
from notion.app import NotionApp

async def main():
    app = NotionApp()
    result = await app.notion_search(query="example", query_type="example", content_search_mode="example")
    print(result)

asyncio.run(main())
"
```
