---
name: mcp-builder
description: "Comprehensive guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Covers both Python (FastMCP) and Node/TypeScript (MCP SDK) implementations."
applyTo: "**/*.py, **/*.ts, **/*.js, **/pyproject.toml, **/requirements.txt, **/package.json"
license: Complete terms in LICENSE.txt
---

# MCP Server Development Guide

## Overview

Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks.

---

# Process

## 🚀 High-Level Workflow

Creating a high-quality MCP server involves four main phases:

### Phase 1: Deep Research and Planning

#### 1.1 Understand Modern MCP Design

**API Coverage vs. Workflow Tools:**
Balance comprehensive API endpoint coverage with specialized workflow tools. Workflow tools can be more convenient for specific tasks, while comprehensive coverage gives agents flexibility to compose operations. Performance varies by client—some clients benefit from code execution that combines basic tools, while others work better with higher-level workflows. When uncertain, prioritize comprehensive API coverage.

**Tool Naming and Discoverability:**
Clear, descriptive tool names help agents find the right tools quickly. Use consistent prefixes (e.g., `github_create_issue`, `github_list_repos`) and action-oriented naming.

**Context Management:**
Agents benefit from concise tool descriptions and the ability to filter/paginate results. Design tools that return focused, relevant data. Some clients support code execution which can help agents filter and process data efficiently.

**Actionable Error Messages:**
Error messages should guide agents toward solutions with specific suggestions and next steps.

#### 1.2 Study MCP Protocol Documentation

**Navigate the MCP specification:**

Start with the sitemap to find relevant pages: `https://modelcontextprotocol.io/sitemap.xml`

Then fetch specific pages with `.md` suffix for markdown format (e.g., `https://modelcontextprotocol.io/specification/draft.md`).

Key pages to review:
- Specification overview and architecture
- Transport mechanisms (streamable HTTP, stdio)
- Tool, resource, and prompt definitions

#### 1.3 Study Framework Documentation

**Recommended stack:**
- **Language**: TypeScript (high-quality SDK support and good compatibility in many execution environments e.g. MCPB. Plus AI models are good at generating TypeScript code, benefiting from its broad usage, static typing and good linting tools)
- **Transport**: Streamable HTTP for remote servers, using stateless JSON (simpler to scale and maintain, as opposed to stateful sessions and streaming responses). stdio for local servers.

**Load framework documentation:**

- **MCP Best Practices**: [📋 View Best Practices](./reference/mcp_best_practices.md) - Core guidelines

**For TypeScript (recommended):**
- **TypeScript SDK**: Use WebFetch to load `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- [⚡ TypeScript Guide](./reference/node_mcp_server.md) - TypeScript patterns and examples

**For Python:**
- **Python SDK**: Use WebFetch to load `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [🐍 Python Guide](./reference/python_mcp_server.md) - Python patterns and examples

#### 1.4 Plan Your Implementation

**Understand the API:**
Review the service's API documentation to identify key endpoints, authentication requirements, and data models. Use web search and WebFetch as needed.

**Tool Selection:**
Prioritize comprehensive API coverage. List endpoints to implement, starting with the most common operations.

---

### Phase 2: Implementation

#### 2.1 Set Up Project Structure

**Python Setup:**
- Use **uv** for project management: `uv init mcp-server-demo` and `uv add "mcp[cli]"`
- Create module structure with clear separation of concerns
- Set up configuration management with environment variables

**TypeScript Setup:**
See [⚡ TypeScript Guide](./reference/node_mcp_server.md) for project structure, package.json, tsconfig.json

#### 2.2 Implement Core Infrastructure

Create shared utilities:
- API client with authentication
- Error handling helpers
- Response formatting (JSON/Markdown)
- Pagination support

#### 2.3 Python Implementation with FastMCP

**Import and Initialize:**
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My Server")
```

**Key Principles:**
- Import FastMCP from `mcp.server.fastmcp`: `from mcp.server.fastmcp import FastMCP`
- Use `@mcp.tool()`, `@mcp.resource()`, and `@mcp.prompt()` decorators for registration
- Type hints are mandatory - they're used for schema generation and validation
- Use Pydantic models, TypedDicts, or dataclasses for structured output
- Tools automatically return structured output when return types are compatible
- For stdio transport, use `mcp.run()` or `mcp.run(transport="stdio")`
- For HTTP servers, use `mcp.run(transport="streamable-http")` or mount to Starlette/FastAPI

**Context and Advanced Features:**
- Use `Context` parameter in tools/resources to access MCP capabilities: `ctx: Context`
- Send logs with `await ctx.debug()`, `await ctx.info()`, `await ctx.warning()`, `await ctx.error()`
- Report progress with `await ctx.report_progress(progress, total, message)`
- Request user input with `await ctx.elicit(message, schema)`
- Use LLM sampling with `await ctx.session.create_message(messages, max_tokens)`

**Configuration:**
- Configure icons with `Icon(src="path", mimeType="image/png")` for server, tools, resources, prompts
- Use `Image` class for automatic image handling: `return Image(data=bytes, format="png")`
- Define resource templates with URI patterns: `@mcp.resource("greeting://{name}")`
- Implement completion support by accepting partial values and returning suggestions
- Use lifespan context managers for startup/shutdown with shared resources
- Access lifespan context in tools via `ctx.request_context.lifespan_context`
- For stateless HTTP servers, set `stateless_http=True` in FastMCP initialization
- Enable JSON responses for modern clients: `json_response=True`

**Testing:**
- Test servers with: `uv run mcp dev server.py` (Inspector) or `uv run mcp install server.py` (Claude Desktop)
- Mount multiple servers in Starlette with different paths: `Mount("/path", mcp.streamable_http_app())`
- Configure CORS for browser clients: expose `Mcp-Session-Id` header
- Use low-level Server class for maximum control when FastMCP isn't sufficient

#### 2.4 Implement Tools

For each tool:

**Input Schema:**
- **Python**: Use Pydantic models or type hints (automatic schema generation)
- **TypeScript**: Use Zod schemas
- Include constraints and clear descriptions
- Add examples in field descriptions

**Output Schema:**
- Define `outputSchema` where possible for structured data
- Use `structuredContent` in tool responses (TypeScript SDK feature)
- **Python**: Return Pydantic models or TypedDicts for automatic structured output
- Helps clients understand and process tool outputs

**Tool Description:**
- Concise summary of functionality
- Parameter descriptions
- Return type schema
- **Python**: Docstrings automatically become tool descriptions

**Implementation:**
- Async/await for I/O-bound operations
- Proper error handling with actionable messages
- Support pagination where applicable
- Return both text content and structured data when using modern SDKs

**Annotations:**
- `readOnlyHint`: true/false
- `destructiveHint`: true/false
- `idempotentHint`: true/false
- `openWorldHint`: true/false

---

### Phase 3: Review and Test

#### 3.1 Code Quality

Review for:
- No duplicated code (DRY principle)
- Consistent error handling
- Full type coverage
- Clear tool descriptions

#### 3.2 Build and Test

**Python:**
- Verify syntax: `python -m py_compile your_server.py`
- Test with MCP Inspector: `uv run mcp dev server.py`
- Run type checker if using mypy/pyright

**TypeScript:**
- Run `npm run build` to verify compilation
- Test with MCP Inspector: `npx @modelcontextprotocol/inspector`

See language-specific guides for detailed testing approaches and quality checklists.

---

### Phase 4: Create Evaluations

After implementing your MCP server, create comprehensive evaluations to test its effectiveness.

**Load [✅ Evaluation Guide](./reference/evaluation.md) for complete evaluation guidelines.**

#### 4.1 Understand Evaluation Purpose

Use evaluations to test whether LLMs can effectively use your MCP server to answer realistic, complex questions.

#### 4.2 Create 10 Evaluation Questions

To create effective evaluations, follow the process outlined in the evaluation guide:

1. **Tool Inspection**: List available tools and understand their capabilities
2. **Content Exploration**: Use READ-ONLY operations to explore available data
3. **Question Generation**: Create 10 complex, realistic questions
4. **Answer Verification**: Solve each question yourself to verify answers

#### 4.3 Evaluation Requirements

Ensure each question is:
- **Independent**: Not dependent on other questions
- **Read-only**: Only non-destructive operations required
- **Complex**: Requiring multiple tool calls and deep exploration
- **Realistic**: Based on real use cases humans would care about
- **Verifiable**: Single, clear answer that can be verified by string comparison
- **Stable**: Answer won't change over time

#### 4.4 Output Format

Create an XML file with this structure:

```xml
<evaluation>
  <qa_pair>
    <question>Find discussions about AI model launches with animal codenames. One model needed a specific safety designation that uses the format ASL-X. What number X was being determined for the model named after a spotted wild cat?</question>
    <answer>3</answer>
  </qa_pair>
<!-- More qa_pairs... -->
</evaluation>
```

---

# Best Practices

## General Best Practices

- Always use type hints - they drive schema generation and validation
- Return Pydantic models or TypedDicts for structured tool outputs
- Keep tool functions focused on single responsibilities
- Provide clear docstrings - they become tool descriptions
- Use descriptive parameter names with type hints
- Validate inputs using Pydantic Field descriptions
- Implement proper error handling with try-except blocks
- Use async functions for I/O-bound operations
- Clean up resources in lifespan context managers
- Log to stderr to avoid interfering with stdio transport (when using stdio)
- Use environment variables for configuration
- Test tools independently before LLM integration
- Consider security when exposing file system or network access
- Use structured output for machine-readable data
- Provide both content and structured data for backward compatibility

## Python-Specific Best Practices

- Always use FastMCP unless you need low-level Server control
- Leverage automatic schema generation from type hints
- Use Pydantic models for complex structured outputs
- Return Python objects directly - FastMCP handles serialization
- Use `@mcp.tool()` decorator for all tools
- Implement lifespan context managers for shared resources (database connections, API clients)
- Use Context parameter for logging, progress reporting, and user interaction
- Test with both `mcp dev` (Inspector) and actual client integration

---

# Common Patterns

## Python FastMCP Patterns

### Basic Server Setup (stdio)

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.tool()
def calculate(a: int, b: int, op: str) -> int:
    """Perform calculation"""
    if op == "add":
        return a + b
    return a - b

if __name__ == "__main__":
    mcp.run()  # stdio by default
```

### HTTP Server

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My HTTP Server")

@mcp.tool()
def hello(name: str = "World") -> str:
    """Greet someone"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

### Tool with Structured Output

```python
from pydantic import BaseModel, Field

class WeatherData(BaseModel):
    temperature: float = Field(description="Temperature in Celsius")
    condition: str
    humidity: float

@mcp.tool()
def get_weather(city: str) -> WeatherData:
    """Get weather for a city"""
    return WeatherData(
        temperature=22.5,
        condition="sunny",
        humidity=65.0
    )
```

### Dynamic Resource

```python
@mcp.resource("users://{user_id}")
def get_user(user_id: str) -> str:
    """Get user profile data"""
    return f"User {user_id} profile data"
```

### Tool with Context

```python
from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession

@mcp.tool()
async def process_data(
    data: str,
    ctx: Context[ServerSession, None]
) -> str:
    """Process data with logging"""
    await ctx.info(f"Processing: {data}")
    await ctx.report_progress(0.5, 1.0, "Halfway done")
    return f"Processed: {data}"
```

### Tool with Sampling

```python
from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from mcp.types import SamplingMessage, TextContent

@mcp.tool()
async def summarize(
    text: str,
    ctx: Context[ServerSession, None]
) -> str:
    """Summarize text using LLM"""
    result = await ctx.session.create_message(
        messages=[SamplingMessage(
            role="user",
            content=TextContent(type="text", text=f"Summarize: {text}")
        )],
        max_tokens=100
    )
    return result.content.text if result.content.type == "text" else ""
```

### Lifespan Management

```python
from contextlib import asynccontextmanager
from dataclasses import dataclass
from mcp.server.fastmcp import FastMCP, Context

@dataclass
class AppContext:
    db: Database

@asynccontextmanager
async def app_lifespan(server: FastMCP):
    db = await Database.connect()
    try:
        yield AppContext(db=db)
    finally:
        await db.disconnect()

mcp = FastMCP("My App", lifespan=app_lifespan)

@mcp.tool()
def query(sql: str, ctx: Context) -> str:
    """Query database"""
    db = ctx.request_context.lifespan_context.db
    return db.execute(sql)
```

### Prompt with Messages

```python
from mcp.server.fastmcp.prompts import base

@mcp.prompt(title="Code Review")
def review_code(code: str) -> list[base.Message]:
    """Create code review prompt"""
    return [
        base.UserMessage("Review this code:"),
        base.UserMessage(code),
        base.AssistantMessage("I'll review the code for you.")
    ]
```

### Error Handling

```python
@mcp.tool()
async def risky_operation(input: str) -> str:
    """Operation that might fail"""
    try:
        result = await perform_operation(input)
        return f"Success: {result}"
    except Exception as e:
        return f"Error: {str(e)}"
```

### Tool with Annotations

```python
@mcp.tool(
    readOnlyHint=True,
    idempotentHint=True,
    openWorldHint=True
)
async def search_items(query: str, limit: int = 10) -> list[dict]:
    """Search items with query

    This is a read-only, idempotent search operation that queries
    an open-world dataset.
    """
    # Implementation
    return results
```

---

# Reference Files

## 📚 Documentation Library

Load these resources as needed during development:

### Core MCP Documentation (Load First)
- **MCP Protocol**: Start with sitemap at `https://modelcontextprotocol.io/sitemap.xml`, then fetch specific pages with `.md` suffix
- [📋 MCP Best Practices](./reference/mcp_best_practices.md) - Universal MCP guidelines including:
  - Server and tool naming conventions
  - Response format guidelines (JSON vs Markdown)
  - Pagination best practices
  - Transport selection (streamable HTTP vs stdio)
  - Security and error handling standards

### SDK Documentation (Load During Phase 1/2)
- **Python SDK**: Fetch from `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- **TypeScript SDK**: Fetch from `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`

### Language-Specific Implementation Guides (Load During Phase 2)
- [🐍 Python Implementation Guide](./reference/python_mcp_server.md) - Complete Python/FastMCP guide with:
  - Server initialization patterns
  - Pydantic model examples
  - Tool registration with `@mcp.tool`
  - Complete working examples
  - Quality checklist

- [⚡ TypeScript Implementation Guide](./reference/node_mcp_server.md) - Complete TypeScript guide with:
  - Project structure
  - Zod schema patterns
  - Tool registration with `server.registerTool`
  - Complete working examples
  - Quality checklist

### Evaluation Guide (Load During Phase 4)
- [✅ Evaluation Guide](./reference/evaluation.md) - Complete evaluation creation guide with:
  - Question creation guidelines
  - Answer verification strategies
  - XML format specifications
  - Example questions and answers
  - Running an evaluation with the provided scripts
