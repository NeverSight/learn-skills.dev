---
name: wise-mcp
description: Best practices for building MCP servers with FastMCP, informed by battle-tested agentic tool design patterns. Use when building, wrapping, or refactoring MCP servers, tools, resources, or prompts.
---

# MCP Server Development

This skill guides you through building high-quality MCP servers using FastMCP (Python). It combines two knowledge sources:

- **FastMCP** — the framework for building MCP servers. Docs: https://gofastmcp.com | LLM-optimized: https://gofastmcp.com/llms-full.txt
- **Arcade patterns** — 52 battle-tested design patterns for building tools that AI agents can use effectively. Reference: https://www.arcade.dev/patterns | LLM-optimized: https://www.arcade.dev/patterns/llm.txt

> **Always check the latest docs before implementing.** Both FastMCP and the arcade patterns evolve. Fetch the LLM-optimized URLs above to get current guidance before writing any MCP server code.

## When to use

- Building a new MCP server with FastMCP
- Wrapping an existing API or service as MCP tools
- Designing tool interfaces, resources, or prompts for LLM consumption
- Reviewing or refactoring an existing MCP server for quality
- Deciding how to structure tool inputs, outputs, errors, or auth
- Choosing between tools, resources, and prompts for a given use case
- Setting up authentication, authorization, or server composition

## Instructions

### 1. Before you start

Fetch the latest documentation before writing any code:
- Read https://gofastmcp.com/llms-full.txt for current FastMCP API, decorators, and patterns
- Read https://www.arcade.dev/patterns/llm.txt for the full pattern catalog with explanations

These are LLM-optimized text files designed for agent consumption. Use them as your primary reference throughout implementation. API signatures, decorator options, and best practices may have changed since this skill was written.

### 2. Guiding principles

These cross-cutting concerns apply to every decision you make when building MCP servers:

- **Machine Experience** — design for LLM comprehension, not human reading. Tool descriptions, parameter names, and error messages should be clear, unambiguous, and structured for machines. A human developer might understand a terse description, but an LLM needs explicit context about purpose, prerequisites, and valid inputs. *(see: TOOL_DESCRIPTION, MACHINE_EXPERIENCE)*

- **Tool DAGs** — hint at what comes next. Tools should suggest related operations and prerequisites so agents can build workflows without trial and error. Every tool description should answer: "What should the agent call before this?" and "What might it call after?" *(see: DEPENDENCY_HINT, NEXT_ACTION_HINT)*

- **Error-Guided Recovery** — errors should teach, not just fail. When something goes wrong, tell the agent what happened, why, and exactly how to fix it. Include the specific tool to call, parameters to adjust, or conditions to meet. An agent that receives "Permission denied" learns nothing; one that receives "Permission denied: requires 'admin' scope. Call request_elevated_access() first" can self-correct. *(see: RECOVERY_GUIDE, ERROR_CLASSIFICATION)*

- **Security Boundaries** — prompts express intent, code enforces rules. Never trust the agent to enforce security. Authorization, validation, and audit happen in the tool layer, not in system prompts or tool descriptions. *(see: SECRET_INJECTION, PERMISSION_GATE)*

### 3. Tool design

Tools are the primary way agents interact with your server. Get these right and orchestration stays simple. Get them wrong and no amount of prompt engineering will compensate.

#### Classify your tools

Know whether each tool is a query, command, or discovery tool. This classification drives every other design decision:

- **Query tools** are read-only, safe to retry, and their results can be cached. Mark them clearly so agents know they're side-effect-free. *(see: QUERY_TOOL)*
- **Command tools** perform actions with side effects. Document what changes, whether the operation is reversible, and whether confirmation is needed for destructive actions. *(see: COMMAND_TOOL)*
- **Discovery tools** reveal available operations, schemas, or capabilities. Examples: `list_tables()`, `describe_schema()`, `get_capabilities()`. These are essential for agents working with dynamic or unfamiliar data. *(see: DISCOVERY_TOOL)*

#### Write LLM-optimized descriptions

The docstring is your tool's interface to the agent. Invest in it:

- State what the tool does in the first sentence
- Explain when to use it (and when not to)
- List prerequisites: "Call `get_project_id()` first if you don't have a project ID"
- Describe follow-up actions: "After creating a user, call `assign_role()` to set permissions"
- Include examples of valid inputs for non-obvious parameters
- Mention performance characteristics: "This tool queries all records — use `search_users()` for filtered results"

*(see: TOOL_DESCRIPTION, PERFORMANCE_HINT)*

#### Constrain inputs

Every free-form string parameter is an opportunity for the agent to make a mistake. Reduce the error surface:

- Use Python `enum.Enum` or `typing.Literal` for parameters with known valid values
- Use `pydantic.Field` with `ge`, `le`, `min_length`, `max_length`, `pattern` for bounded values
- Validate early and return clear errors explaining what values are accepted
- Prefer structured types over strings: use `datetime` instead of asking for "a date string"

*(see: CONSTRAINED_INPUT)*

#### Additional tool design patterns

- **Smart defaults** — reduce required parameters. Default to the most common case, use context-aware defaults (current user, current time), and document defaults explicitly in the description. *(see: SMART_DEFAULTS)*
- **Natural identifiers** — let agents pass human-friendly names (email, username, display name) and resolve to system IDs internally. When ambiguous, return candidates with enough context for the agent to choose. *(see: NATURAL_IDENTIFIER, PARAMETER_COERCION)*
- **Mutual exclusivity** — if parameters conflict ("exactly one of X or Y"), enforce it in validation and document valid combinations clearly. Don't rely on the agent to read the rules. *(see: MUTUAL_EXCLUSIVITY)*
- **Batch operations** — when agents need to process multiple items, provide a batch variant that accepts arrays and returns per-item results. This saves round trips and reduces token overhead from repeated tool calls. *(see: BATCH_OPERATION)*

Refer to FastMCP docs on the `@mcp.tool` decorator, type hints, and parameter schemas for current API details.

### 4. Resources and resource templates

Resources are the MCP protocol's mechanism for read-only data access. They serve a fundamentally different purpose than tools.

#### When to use resources vs tools

- **Use resources** when the data is stable, identified by a URI, and has no side effects to read. Resources are like GET endpoints — the agent reads them when it needs context.
- **Use tools** when the operation requires parameters beyond a URI path, has side effects, involves computation, or returns different results based on context.
- **Use resource templates** when the resource is parameterized (e.g., user profiles, project configs) and follows a consistent URI pattern.

#### URI design

- Use clear, hierarchical URIs: `config://app/settings`, `data://users/{user_id}/profile`
- Be consistent with your scheme naming across the server
- Use resource templates (`{param}` syntax) for parameterized data rather than creating individual resources for each entity

#### Making resources discoverable

Resources are only useful if agents know they exist. List them in relevant tool descriptions: "For full project configuration, read the resource at `config://project/{project_id}`." This connects the Tool DAGs principle to resources. *(see: RESOURCE_REFERENCE)*

Refer to FastMCP docs on `@mcp.resource`, resource templates, and URI conventions for implementation.

### 5. Prompts

Prompts are reusable message templates for LLM conversations. They're the least commonly used MCP primitive but valuable in specific scenarios.

#### When to use prompts

- **Standardized workflows** — when agents should follow a specific conversation pattern (e.g., a code review checklist, a troubleshooting flowchart)
- **Report formats** — when output should follow a consistent structure (e.g., incident reports, analysis summaries)
- **Complex instructions** — when a multi-step task needs structured guidance that's too long for a tool description
- **User-facing templates** — when end users should be able to trigger specific agent behaviors by name

#### Design guidelines

- Keep each prompt focused on a single purpose
- Use clear parameter names with descriptions — prompts are discovered and invoked by agents just like tools
- Prompts return message arrays, not plain text. Structure the messages (system, user, assistant) to guide the LLM effectively
- Don't overuse prompts — if the guidance is short enough to fit in a tool description, put it there instead

Refer to FastMCP docs on `@mcp.prompt` for the decorator API and message formatting.

### 6. Context and state

The FastMCP Context object provides session-scoped capabilities within your tools. It's the primary mechanism for tools to interact with the broader MCP session.

#### Core capabilities

- **Dependency injection** — use `CurrentContext()` as a default parameter to access the context object. This works in tools, resources, and prompts.
- **Logging** — use `ctx.info()`, `ctx.warning()`, `ctx.error()` to send structured log messages back to the client. Use these for operational visibility, not for returning data to the agent.
- **Progress reporting** — use `ctx.report_progress()` for operations that take more than a few seconds. Without progress signals, agents may assume the tool has hung and retry or abort.

#### Session state

Use `ctx.get_state()` / `ctx.set_state()` to persist data across multiple tool calls within the same session. This is essential for two patterns:

- **Identity anchor** — establish who the user is at the start of a session. A `who_am_i()` tool that sets the user context in state means subsequent tools can access user ID, roles, and permissions without requiring them as parameters. *(see: IDENTITY_ANCHOR)*
- **Working context** — maintain the current project, scope, or working directory across calls. Once an agent calls `set_project("my-project")`, all subsequent tools should operate in that context without the agent needing to pass `project_id` every time. *(see: SESSION_CONTEXT)*

#### Advanced context features

- **Resource access** — tools can read resources from within their execution context, enabling tools to compose with resources
- **LLM sampling** — tools can request LLM completions through the context, enabling tools that leverage LLM reasoning as part of their execution
- **User elicitation** — tools can request input from the end user when they need clarification that the agent can't provide

Refer to FastMCP docs on the Context object for the full API and current method signatures.

### 7. Tool output

How you return results matters as much as what you return. Agents consume your output as context for their next decision. Every unnecessary token degrades reasoning quality.

#### Shape responses for agents

- **Flatten nested structures** — agents struggle with deeply nested JSON. Select and flatten to the relevant fields. *(see: RESPONSE_SHAPER)*
- **Rename for clarity** — if the upstream API uses cryptic field names, rename them. `user_email` is better than `usr_eml` for agent comprehension.
- **Never pass raw API responses through** — always transform external API responses into a clean, consistent format. The upstream API's schema is designed for developers, not LLMs.

#### Control response size

- **Return only essential fields** — every field should earn its place. If the agent doesn't need it for its current task, don't include it. *(see: TOKEN_EFFICIENT_RESPONSE)*
- **Truncate long text** — if a field contains lengthy content (descriptions, logs, file contents), truncate with a note about how to get the full version.
- **Count, don't list** — when a collection is large, return the count and a representative sample rather than the full list. "Found 847 matching records. Showing first 10."
- **Paginate large results** — use cursor-based pagination with a `has_more` flag and explicit instructions for getting the next page. Never dump unbounded result sets. *(see: PAGINATED_RESULT)*

#### Guide agent behavior through output

- **Progressive detail** — return summaries by default. Include a `detail` parameter that agents can set to get the full response when needed. *(see: PROGRESSIVE_DETAIL)*
- **Next-action hints** — suggest what the agent should do next. This is one of the highest-impact patterns. Include suggested tool names, required parameters, and alternative paths in your response. Example: include a `next_steps` field like `["Call assign_role(user_id='abc', role='admin') to complete setup"]`. *(see: NEXT_ACTION_HINT, DEPENDENCY_HINT)*
- **Partial success** — for batch operations, report per-item status with summary statistics and retry guidance for failures. Never report a batch as simply "failed" when some items succeeded. *(see: PARTIAL_SUCCESS)*
- **GUI URLs** — when applicable, include links to view or edit results in a web interface. Agents can surface these to users. *(see: GUI_URL)*

### 8. Error handling and resilience

Agents can't debug — they can only retry or try something different. Your error messages are their only guide. Invest heavily in error quality.

#### Recovery-oriented errors

Every error message should answer three questions:

1. **What went wrong?** — a clear description of the failure
2. **Why did it fail?** — the underlying cause
3. **How to fix it?** — specific, actionable steps

Bad: `"Error: not found"`
Good: `"User 'jsmith' not found. The user may have been deleted or the username may be misspelled. Call search_users(query='smith') to find matching users, or list_users() to see all available users."`

*(see: RECOVERY_GUIDE)*

#### Error classification

Distinguish between error types so agents can respond appropriately:

- **Retryable** — transient errors that will likely succeed on retry (rate limits, temporary network issues). Include a `retry_after` hint if possible.
- **Permanent** — errors that won't resolve without changing the request (invalid parameters, missing resources). Tell the agent what to change.
- **Auth required** — the user needs to re-authenticate or the tool needs different permissions. Specify exactly which scope or permission is missing.

*(see: ERROR_CLASSIFICATION)*

#### Handling ambiguity

- **Confirmation requests** — when input could match multiple entities, return the candidates with enough detail for the agent to choose. Include the exact tool call for each option so the agent can proceed without guessing. *(see: CONFIRMATION_REQUEST)*
- **Fuzzy matching** — for high-confidence matches (>90%), auto-accept and proceed. For uncertain matches (50-90%), return options. For low-confidence matches (<50%), ask for different input. *(see: FUZZY_MATCH_THRESHOLD)*
- **Graceful degradation** — return partial results when full operation isn't possible. Note what worked, what failed, and suggest remediation for the failures. *(see: GRACEFUL_DEGRADATION)*
- **Fallback tools** — when a primary data source or service is unavailable, provide an alternative path. Indicate when a fallback was used so the agent knows the results may be incomplete. *(see: FALLBACK_TOOL)*

Refer to FastMCP docs on `ToolError` and error handling for implementation patterns.

### 9. Server composition

FastMCP supports composing multiple servers and sourcing components from various origins. Use composition to keep individual servers focused and maintainable.

#### Mounting and importing

- **Mounting** (`mcp.mount()`) — creates a live, dynamic link. Changes to the mounted server are immediately reflected in the parent. Use namespaces to avoid naming conflicts: `mcp.mount(weather_server, namespace="weather")` prefixes all tool names with `weather_`.
- **Importing** (`import_server()`) — copies components once at import time. Use this when you want a static snapshot and don't need dynamic updates. Lower overhead than mounting.
- **Choose mounting for development**, where sub-servers change frequently, and importing for production, where stability matters more.

#### Provider system

FastMCP v3.0 uses providers to source components from different origins:

- **LocalProvider** — the default. Components registered via decorators on the server instance.
- **FileSystemProvider** — auto-discovers decorated functions from a directory tree. Each file is self-contained. Great for organizing large servers into modular tool files.
- **OpenAPIProvider** — generates MCP tools from an OpenAPI specification. Useful for bootstrapping, but curated tools almost always outperform auto-generated ones. Use selectively: convert the endpoints that matter, exclude the rest with route maps.
- **ProxyProvider** — bridges to remote MCP servers. Useful for transport bridging (exposing an HTTP server via stdio) or aggregating multiple servers behind one interface.

#### Transforms

Transforms modify components after provider aggregation:

- **Namespace** — adds prefixes to avoid naming conflicts between mounted servers
- **Visibility** — controls which components are exposed to clients. Use to hide internal or administrative tools. See *Progressive disclosure* below for a full pattern.
- **VersionFilter** — filters components by version ranges for API evolution
- **ResourcesAsTools / PromptsAsTools** — exposes resources and prompts as tools for clients that primarily interact via tools

#### Progressive disclosure

When a server has many tools (10+), exposing all of them at startup wastes context window and degrades agent tool-selection accuracy. The progressive disclosure pattern starts with a minimal set of *gateway* tools and lets agents opt into additional tools on demand.

**Implementation with FastMCP Visibility:**

```python
from fastmcp.server.transforms import Visibility

# Tag tools by category
@server.tool(tags={"gateway"})
def get_capabilities() -> dict: ...          # always visible

@server.tool(tags={"gateway"})
async def enable_tools(category: str, ctx: Context) -> dict: ...  # always visible

@server.tool(tags={"plans"})
def search_plans(...) -> dict: ...           # hidden until activated

# In server setup — hide all tools, then re-show gateway
mcp.add_transform(Visibility(False, components={"tool"}))
mcp.add_transform(Visibility(True, tags={"gateway"}, components={"tool"}))
```

**Caution:** `match_all=True` short-circuits the `components` filter in FastMCP v3 — always use the two separate transforms shown above instead of a single `Visibility(False, match_all=True, components={"tool"})`.

**`enable_tools()` implementation:**

```python
async def enable_tools(category: str, ctx: Context) -> dict:
    tags = _CATEGORY_TAGS[category]
    await enable_components(ctx, tags=tags, components={"tool"})
    # Return schemas for immediate use (see client-compat note below)
    ...
```

**Client compatibility:** The MCP spec defines `ToolListChangedNotification` so clients re-fetch the tool list after `enable_components()`. However, this notification is optional and many clients (e.g. mcp-go-based editors) do not implement it. If you cannot guarantee client support, also return the activated tool schemas directly in `enable_tools()`'s response — derived from `srv.list_tools()` on the mounted sub-servers (same source of truth as `tools/list`, zero duplication):

```python
tool_schemas = {}
for srv in sub_servers:
    for tool in await srv.list_tools():
        if tool.tags & tags:
            tool_schemas[tool.name] = {
                "description": tool.description,
                "parameters": tool.parameters,  # FunctionTool.parameters in FastMCP v3
            }
return {"activated": category, "tools": tool_schemas}
```

This gives agents immediate usability in the same turn without waiting for a tool list refresh.

#### Design principles for composition

- **Abstraction ladder** — provide tools at multiple granularity levels. Low-level tools for precise control (`create_file`, `write_bytes`), mid-level for common tasks (`create_document`), and high-level for complex workflows (`draft_report`). Let agents choose the right level. *(see: ABSTRACTION_LADDER)*
- **Task bundles** — combine multiple operations into a single tool when they always occur together. Name after the task, not the steps: `onboard_user()` instead of `create_user_and_assign_role_and_send_welcome_email()`. *(see: TASK_BUNDLE)*
- **Gateway pattern** — use a parent server as a unified interface to multiple backends. The agent sees one coherent set of tools; the server routes to the right backend. *(see: TOOL_GATEWAY)*

Refer to FastMCP docs on server composition, providers, and transforms for implementation details.

### 10. Authentication and security

Security is enforced in code, never delegated to the agent via prompts. This is non-negotiable.

#### Credential handling

- **Never accept secrets as tool parameters** — API keys, tokens, and passwords flow through the LLM when passed as parameters. Use the Context to inject credentials at runtime. *(see: SECRET_INJECTION)*
- **Use environment variables or secure vaults** for credential storage. The tool reads credentials from a trusted source, never from the agent's input.

#### Authorization

- **Per-tool auth** — use FastMCP's `require_auth` and `require_scopes` decorators on individual tools to enforce fine-grained access control. *(see: PERMISSION_GATE)*
- **Server-wide policies** — use `AuthMiddleware` to apply blanket authentication requirements. Combine with tag-based restrictions for role-based access.
- **Scope declaration** — declare required OAuth scopes per tool. Check before execution. Return clear errors that name the missing scope and how to obtain it. *(see: SCOPE_DECLARATION)*

#### Audit and boundaries

- **Audit trail** — log all tool invocations with: what (tool name + redacted parameters), who (user ID + session ID), when (timestamp), and result (success/failure + duration). This is critical for debugging and compliance. *(see: AUDIT_TRAIL)*
- **Context boundaries** — define explicit scope limits for tool operations. Restrict file access to specific root paths, data access to specific tenants, and API access to specific endpoints. Never let a tool's blast radius exceed what's necessary. *(see: CONTEXT_BOUNDARY)*

Refer to FastMCP docs on authentication, OAuth proxy, middleware, and `require_auth` / `require_scopes` for implementation.

### 11. Anti-patterns to avoid

These are the most common mistakes when building MCP servers. Each one degrades agent effectiveness:

- **Raw API passthrough** — forwarding upstream API responses without shaping them. Always transform responses into agent-friendly formats with clear field names and flat structures.
- **Free-form string parameters** — accepting open strings when a finite set of valid values exists. Use enums, literals, and constrained types to eliminate invalid inputs at the schema level.
- **Silent failures** — returning empty results without explanation. Always tell the agent what happened and why. An empty list should say "No results found matching criteria X" rather than returning `[]`.
- **Secrets as parameters** — accepting API keys, tokens, or passwords as tool inputs. These flow through the LLM and are logged in conversation history.
- **Unbounded responses** — dumping entire datasets without pagination or truncation. Large responses consume context window and degrade agent reasoning.
- **Human-oriented descriptions** — writing tool descriptions for developers instead of LLMs. Include prerequisites, follow-ups, valid input examples, and performance characteristics.
- **Deep proxy hierarchies** — mounting proxies of proxies of proxies. Each layer adds latency and failure modes. Keep the proxy depth to one level.
- **Auto-converting entire OpenAPI specs** — generating tools for every endpoint without curation. Most API endpoints don't make good agent tools. Select the ones that matter and design proper descriptions for them.
- **Security via prompts** — relying on system prompts or tool descriptions to enforce access control. Prompts can be overridden or ignored. Enforce security in code.
- **Monolithic servers** — putting every tool in one server. Use composition to keep servers focused. An agent connecting to a 50-tool server has worse tool selection accuracy than one connecting to five 10-tool servers via mounting.
- **Missing next-action hints** — returning results without guidance on what to do next. Every response is an opportunity to help the agent make progress.
