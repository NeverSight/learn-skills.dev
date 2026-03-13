---
name: fastmcp-builder
description: Build production-ready MCP servers using FastMCP framework with proven patterns for tools, resources, prompts, OAuth authentication, and comprehensive testing. Use this when creating FastMCP-based MCP servers with features like Google OAuth, multiple resource types, testing with FastMCP Client, or complex tool implementations.
---

# FastMCP Builder - Production MCP Server Development

## Overview

This skill provides comprehensive, production-ready patterns for building MCP (Model Context Protocol) servers using **FastMCP**, the official high-level Python framework. It includes complete reference implementations, working examples, and best practices proven in production.

**FastMCP** is the recommended approach for building MCP servers in Python - it's simpler, faster to develop, and more maintainable than the low-level MCP SDK.

## What's Included

This skill contains:

1. **Reference Documentation** (`reference/`) - 6 comprehensive guides covering all aspects of FastMCP development
2. **Code Examples** (`examples/`) - Runnable examples from minimal to complete servers
3. **Complete Reference Project** (`reference-project/`) - Full production implementation with:
   - 6 production-ready tools
   - 7 resource instances (4 types)
   - 1 universal prompt
   - 145 passing tests
   - OAuth integration
   - Complete documentation

**💡 Tip:** When in doubt, look at the reference-project for real-world implementation examples.

## When to Use This Skill

Use this skill when you need to:

✅ **Build MCP servers with FastMCP** - Python-based MCP server development
✅ **Add OAuth authentication** - Especially Google OAuth for remote access
✅ **Implement production patterns** - Tools, resources, prompts with best practices
✅ **Set up comprehensive testing** - Using FastMCP Client for fast, in-memory tests
✅ **Structure larger projects** - Proper organization and separation of concerns
✅ **Deploy to production** - With authentication, error handling, monitoring

**Don't use this skill for:**

- ❌ TypeScript/Node.js MCP servers (use mcp-builder skill instead)
- ❌ Low-level MCP protocol work (use MCP SDK directly)
- ❌ Non-FastMCP Python servers (this is FastMCP-specific)

## Consulting Official Documentation

**IMPORTANT:** When encountering questions or issues not covered in this skill's reference materials, you should:

### Primary Method: Use WebSearch (Recommended)

The most reliable way to find FastMCP documentation is using WebSearch with site-specific queries:

```
WebSearch(
    query="site:gofastmcp.com [your specific topic]"
)
```

This will search the official FastMCP documentation site and return relevant pages.

### Alternative: Direct Page Access

If you know the general documentation structure, you can fetch specific pages directly:

```
WebFetch(
    url="https://gofastmcp.com/[section]/[topic]",
    prompt="Your specific question about this topic"
)
```

**Common documentation sections:**

- `/getting-started/` - Installation, quickstart, welcome
- `/servers/` - Tools, resources, prompts, context, logging
- `/deployment/` - Running servers, HTTP deployment, configuration
- `/integrations/` - Auth0, AWS Cognito, Azure, GitHub, Google, WorkOS, OpenAI, etc.
- `/testing/` - Testing guides and best practices

**Tip:** Any page can be accessed as markdown by appending `.md` to the URL.

### When to Consult Official Docs

Consult official documentation when:

- You encounter a feature or API not covered in this skill's references
- You need the latest updates or breaking changes
- User asks about FastMCP capabilities you're unsure about
- You're implementing advanced patterns not in the reference materials
- There are version-specific behaviors or deprecations
- You need clarification on authentication providers beyond Google OAuth
- You want to verify current best practices

### Example Workflows

1. **User asks about OpenAI integration:**

   ```
   WebSearch(query="site:gofastmcp.com openai integration")
   → Find https://gofastmcp.com/integrations/openai
   → Fetch that page for details
   ```

2. **User asks about AWS Cognito authentication:**

   ```
   WebSearch(query="site:gofastmcp.com aws cognito oauth")
   → Find relevant auth documentation
   → Implement based on official guidance
   ```

3. **User asks about testing patterns:**

   ```
   WebSearch(query="site:gofastmcp.com testing")
   → Find testing documentation
   → Apply patterns from official docs
   ```

4. **Exploring what's available:**
   ```
   WebSearch(query="site:gofastmcp.com deployment options")
   WebSearch(query="site:gofastmcp.com authentication providers")
   → Browse results to see available topics
   ```

**Note:** Always try the reference materials in this skill first, then consult official docs if needed.

---

## Workflow - Building a FastMCP Server

### Phase 1: Planning & Setup

**Step 1.1: Review FastMCP Overview**

- Load [fastmcp_overview.md](./reference/fastmcp_overview.md)
- Understand FastMCP vs MCP SDK
- Confirm FastMCP is right choice (it usually is)

**Step 1.2: Understand Requirements**

- What tools does the server need?
- Do you need OAuth authentication?
- Will you have resources? Prompts?
- What's the deployment target?

**Step 1.3: Review Project Structure**

- Load [project_structure.md](./reference/project_structure.md)
- Understand the recommended directory layout
- Learn about the common.py pattern (DRY principle)
- Understand dual-mode pattern (with/without OAuth)

**Step 1.4: Set Up Project**

Create project structure:

```bash
mkdir my-mcp-server
cd my-mcp-server

# Create directories
mkdir -p app/tools app/resources app/prompts tests

# Create initial files
touch app/__init__.py
touch app/main.py
touch app/main_noauth.py
touch app/common.py
touch app/config.py
touch tests/__init__.py
touch pyproject.toml
touch .env.example
touch README.md
```

Initialize with uv:

```bash
# Install FastMCP
uv add fastmcp==2.13.0.1
uv add python-dotenv==1.2.1

# Add test dependencies
uv add --optional test pytest==8.4.2 pytest-asyncio==1.2.0 pytest-mock==3.15.1 httpx==0.28.1
```

---

### Phase 2: Core Implementation

**Step 2.1: Implement Configuration**

Create `app/config.py` based on patterns in [project_structure.md](./reference/project_structure.md):

- Environment variable loading
- Configuration class with validation
- OAuth settings (if needed)
- Server metadata

**Step 2.2: Implement Tools**

Load [tool_patterns.md](./reference/tool_patterns.md) for comprehensive patterns:

1. **Identify tool patterns needed:**
   - Basic sync tools (health checks, simple queries)
   - Data processing tools (analysis, transformation)
   - Tools with Context (logging, progress)
   - Stateful tools (if state management needed)
   - API integration tools (external services)

2. **Create tools in `app/tools/`:**
   - One file per tool or logical group
   - Follow patterns from tool_patterns.md
   - Use proper error handling
   - Add comprehensive docstrings

3. **Example tool structure:**

```python
# app/tools/my_tool.py

async def my_tool(param: str, ctx: Context | None = None) -> dict:
    """
    Tool description

    Args:
        param: Parameter description
        ctx: FastMCP context (auto-injected)

    Returns:
        dict: Result structure
    """
    try:
        if ctx:
            await ctx.info("Processing...")

        # Tool logic here
        result = process(param)

        if ctx:
            await ctx.info("Completed!")

        return {"status": "success", "data": result}

    except Exception as e:
        if ctx:
            await ctx.error(f"Failed: {e}")
        return {"status": "error", "error": str(e)}
```

**Step 2.3: Implement Resources** (if needed)

Load [resource_patterns.md](./reference/resource_patterns.md) for all resource types:

1. **Choose resource types:**
   - Static resources (status, features, documentation)
   - Dynamic resources (generated content)
   - Template resources (with path parameters)
   - Wildcard resources (multi-segment paths)

2. **Create resources in `app/resources/`:**
   - static.py for static resources
   - Separate files for dynamic/template/wildcard

3. **Example resource:**

```python
# app/resources/welcome.py

def get_welcome_message() -> str:
    """Welcome message resource"""
    return "Welcome to my MCP server!"
```

**Step 2.4: Implement Prompts** (if needed)

Create reusable prompt templates:

```python
# app/prompts/explain.py

def explain_concept(
    concept: str,
    audience_level: str = "intermediate",
) -> str:
    """Generate explanation prompt"""
    return f"Explain {concept} for {audience_level} audience..."
```

**Step 2.5: Create Common Registration**

In `app/common.py`, register all components:

```python
from fastmcp import FastMCP

# Import tools
from app.tools.my_tool import my_tool

# Import resources
from app.resources.welcome import get_welcome_message

# Import prompts
from app.prompts.explain import explain_concept


def register_all(mcp: FastMCP) -> None:
    """Register all components - DRY principle"""

    # Tools
    mcp.tool()(my_tool)

    # Resources
    mcp.resource("greeting://welcome")(get_welcome_message)

    # Prompts
    mcp.prompt()(explain_concept)
```

**Step 2.6: Create Server Entry Points**

**app/main_noauth.py** (for local development):

```python
from fastmcp import FastMCP
from app.config import Config
from app.common import register_all

mcp = FastMCP(Config.SERVER_NAME)
register_all(mcp)

if __name__ == "__main__":
    mcp.run()
```

**app/main.py** (with OAuth - if needed):
Load [oauth_integration.md](./reference/oauth_integration.md) for complete OAuth setup.

---

### Phase 3: OAuth Integration (if needed)

**Only if you need remote access with authentication.**

**Step 3.1: Set Up Google OAuth**

Follow [oauth_integration.md](./reference/oauth_integration.md):

1. Create OAuth Client in Google Cloud Console
2. Configure environment variables (.env)
3. Implement GoogleProvider in main.py
4. Set up ngrok for testing
5. Configure Claude Desktop Connectors

**Step 3.2: Test OAuth Flow**

1. Start ngrok
2. Start server with base-url
3. Connect Claude Desktop
4. Verify authentication works

---

### Phase 4: Testing

**Step 4.1: Set Up Test Structure**

Load [testing_guide.md](./reference/testing_guide.md) for comprehensive testing patterns.

Create `tests/conftest.py`:

```python
import pytest
from fastmcp import Client
from app.main_noauth import mcp


@pytest.fixture
async def client():
    """Provide FastMCP client for testing"""
    async with Client(mcp) as c:
        yield c
```

**Step 4.2: Write Tool Tests**

```python
# tests/test_tools.py

@pytest.mark.asyncio
async def test_my_tool(client):
    """Should execute my_tool successfully"""
    result = await client.call_tool("my_tool", {"param": "test"})
    assert result.data["status"] == "success"
```

**Step 4.3: Write Resource Tests**

```python
# tests/test_resources.py

@pytest.mark.asyncio
async def test_welcome_resource(client):
    """Should read welcome resource"""
    content = await client.read_resource("greeting://welcome")
    assert "Welcome" in content
```

**Step 4.4: Write Integration Tests**

```python
# tests/test_integration.py

@pytest.mark.asyncio
async def test_complete_workflow(client):
    """Should execute complete workflow"""
    # Test multiple components working together
    pass
```

**Step 4.5: Run Tests**

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=app --cov-report=html
```

---

### Phase 5: Documentation & Deployment

**Step 5.1: Write README**

Document:

- Project description
- Features
- Quick start guide
- OAuth setup (if applicable)
- Usage examples
- Testing instructions
- Deployment guide

**Step 5.2: Prepare for Deployment**

1. **Environment Variables:**
   - Create .env.example template
   - Document all required variables
   - Never commit .env to git

2. **Testing:**
   - Ensure all tests pass
   - Test OAuth flow (if applicable)
   - Test in production-like environment

3. **Deployment:**
   - Choose platform (Railway, Fly.io, VPS)
   - Set up HTTPS (required for OAuth)
   - Configure environment variables
   - Deploy and test

---

## Reference Documentation

Load these as needed during development:

### Core References

- **[fastmcp_overview.md](./reference/fastmcp_overview.md)** - FastMCP introduction, when to use, key features
- **[project_structure.md](./reference/project_structure.md)** - Recommended structure, file organization, patterns

### Implementation Guides

- **[tool_patterns.md](./reference/tool_patterns.md)** - 6 tool patterns with complete examples
- **[resource_patterns.md](./reference/resource_patterns.md)** - 4 resource types (static, dynamic, template, wildcard)
- **[oauth_integration.md](./reference/oauth_integration.md)** - Complete Google OAuth setup guide
- **[testing_guide.md](./reference/testing_guide.md)** - FastMCP Client testing, patterns, best practices

### Example Code

Run or reference these complete examples:

- **[minimal_server.py](./examples/minimal_server.py)** - Absolute simplest FastMCP server
- **[complete_server_structure.py](./examples/complete_server_structure.py)** - Full-featured single-file example
- **[test_examples.py](./examples/test_examples.py)** - Comprehensive testing examples

---

## Quick Start Examples

### Example 1: Minimal Server

```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def greet(name: str) -> str:
    """Greet someone"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
```

### Example 2: Server with Multiple Components

```python
from fastmcp import FastMCP, Context

mcp = FastMCP("my-server")

# Tool
@mcp.tool()
async def process(text: str, ctx: Context | None = None) -> dict:
    if ctx:
        await ctx.info("Processing...")
    return {"result": text.upper()}

# Resource
@mcp.resource("greeting://hello")
def get_greeting() -> str:
    return "Hello from resource!"

# Prompt
@mcp.prompt()
def explain(topic: str) -> str:
    return f"Explain {topic} in detail"

if __name__ == "__main__":
    mcp.run()
```

### Example 3: With OAuth

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.google import GoogleProvider
import os

auth = GoogleProvider(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    base_url="https://your-server.com",
)

mcp = FastMCP("my-server", auth=auth)

# ... add tools, resources, prompts ...

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
```

---

## Best Practices Summary

1. **✅ Use FastMCP** - Simpler than MCP SDK for most use cases
2. **✅ Follow project structure** - Use common.py pattern (DRY)
3. **✅ Dual-mode servers** - main.py (OAuth) + main_noauth.py (local)
4. **✅ Comprehensive testing** - Use FastMCP Client, aim for >80% coverage
5. **✅ Clear documentation** - Docstrings, README, usage examples
6. **✅ Error handling** - Graceful failures, informative error messages
7. **✅ Context usage** - Logging, progress for better UX
8. **✅ Security** - Environment variables, never commit secrets

---

## Common Workflows

### Creating a New Tool

1. Create `app/tools/my_tool.py`
2. Implement tool function
3. Add to `app/common.py` registration
4. Write tests in `tests/test_tools.py`
5. Run tests: `uv run pytest tests/test_tools.py -v`

### Adding OAuth

1. Review [oauth_integration.md](./reference/oauth_integration.md)
2. Set up Google OAuth credentials
3. Update `app/config.py` with OAuth settings
4. Modify `app/main.py` to use GoogleProvider
5. Test with ngrok
6. Configure Claude Desktop Connectors

### Debugging

1. Use `main_noauth.py` for faster local testing
2. Add logging with Context: `await ctx.debug(...)`
3. Write tests to isolate issues
4. Check tool/resource registration in `common.py`
5. Verify environment variables loaded

---

## Additional Resources

- **FastMCP Documentation:** https://gofastmcp.com/
- **FastMCP GitHub:** https://github.com/jlowin/fastmcp
- **MCP Specification:** https://modelcontextprotocol.io/
- **Google OAuth Guide:** https://developers.google.com/identity/protocols/oauth2

---

## Notes

- This skill focuses on **FastMCP**, not the low-level MCP SDK
- All examples use **Python 3.11+**
- OAuth examples use **Google OAuth** (other providers possible)
- Testing uses **FastMCP Client** (in-memory, fast)
- Deployment examples are production-ready

**Happy building! 🚀**
