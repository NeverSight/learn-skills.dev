---
name: context7
description: "Use this skill when you need to work with context7 through its generated async Python app, call its MCP-backed functions from code, or inspect available functions with the mcp-skill CLI."
metadata:
  short-description: "Use context7 from async Python"
---

# context7

Use this skill when you need to work with context7 through its generated async Python app, call its MCP-backed functions from code, or inspect available functions with the mcp-skill CLI.

## Authentication

No authentication required.

```python
app = Context7App()
```

Passing an `auth` argument is accepted but has no effect and will emit a warning.

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
from context7.app import Context7App


async def main():
    app = Context7App()
    result = await app.resolve_library_id(query="example", libraryName="example")
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
uvx mcp-skill list-functions context7
uvx mcp-skill inspect context7 resolve_library_id
```

**Important:** Add `.agents/skills` to your Python path so imports resolve correctly:

```python
import sys
sys.path.insert(0, ".agents/skills")
from context7.app import Context7App
```

Or set the `PYTHONPATH` environment variable:

```bash
export PYTHONPATH=".agents/skills:$PYTHONPATH"
```

**Preferred: use `uv run`** (handles dependencies automatically):

```bash
PYTHONPATH=.agents/skills uv run --with mcp-skill python -c "
import asyncio
from context7.app import Context7App

async def main():
    app = Context7App()
    result = await app.resolve_library_id(query="example", libraryName="example")
    print(result)

asyncio.run(main())
"
```

**Alternative: use `python` directly** (install dependencies first):

```bash
pip install mcp-skill
PYTHONPATH=.agents/skills python -c "
import asyncio
from context7.app import Context7App

async def main():
    app = Context7App()
    result = await app.resolve_library_id(query="example", libraryName="example")
    print(result)

asyncio.run(main())
"
```
