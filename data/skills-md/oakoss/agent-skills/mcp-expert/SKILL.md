---
name: mcp-expert
description: 'Architects and orchestrates Model Context Protocol (MCP) ecosystems including server development, tool design, and transport configuration. Use when building MCP servers, designing agentic tool interfaces, configuring MCP transports, implementing OAuth security, or troubleshooting MCP connectivity. Use for outcome-oriented tools, Zod validation, progressive disclosure resources, elicitation, and async tasks.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: https://modelcontextprotocol.io
---

# MCP Expert

## Overview

Definitive resource for building and managing Model Context Protocol ecosystems. Covers the full lifecycle from server development and transport configuration to security, elicitation, and async task execution. Designs agent-first tool interfaces that minimize token usage and maximize LLM accuracy.

**When to use:** Building MCP servers, designing tool interfaces, configuring transports (Stdio/Streamable HTTP), implementing OAuth 2.1, troubleshooting connectivity, using elicitation for server-initiated user interaction.

**When NOT to use:** Application-level business logic, non-MCP API design, frontend UI components, general HTTP API development unrelated to MCP.

## Quick Reference

| Pattern                | API/Approach                             | Key Points                                        |
| ---------------------- | ---------------------------------------- | ------------------------------------------------- |
| Outcome-oriented tools | Single-call operations                   | Avoid chatty multi-step APIs                      |
| Argument flattening    | Flat Zod schemas with descriptions       | Reduce model hallucination                        |
| Progressive disclosure | Return `mcp://` URIs for large data      | Agent reads partially via `resources/read`        |
| Retryable tools        | Return `retry_with` suggestions          | Help LLM self-correct on bad inputs               |
| Helpful errors         | Descriptive strings with fix guidance    | Never return raw exceptions or stack traces       |
| Pagination             | `has_more` + `next_cursor` metadata      | 20-50 records per call maximum                    |
| Structured outputs     | JSON Schema in `outputSchema`            | Typed tool results for programmatic consumption   |
| Stdio transport        | Local tools, stderr-only logging         | Never write to stdout except JSON-RPC             |
| Streamable HTTP        | Remote/cloud tools, single endpoint      | Replaces deprecated SSE transport                 |
| OAuth 2.1 with PKCE    | Enterprise data access                   | MCP server is resource server, not auth server    |
| Elicitation            | Server-initiated user input              | Flat schema maps to forms, three response states  |
| Async tasks            | `tasks/get`, `tasks/cancel`              | Long-running operations return task handles       |
| Capability scopes      | `read:docs`, `write:code`, `admin:users` | Granular permission boundaries                    |
| HITL gate              | `confirmation_required` flag             | Manual approval for destructive actions           |
| URL elicitation        | Secure credential collection             | Redirects user to browser for sensitive input     |
| Extensions             | Namespaced capability negotiation        | Optional features without forking the spec        |
| Sampling with tools    | Server-initiated LLM requests            | Enables server-side agent loops                   |
| MCP Inspector          | `npx @modelcontextprotocol/inspector`    | Test tools interactively without an LLM           |
| Unit testing           | InMemoryTransport + Vitest               | Test tool handlers with mock client               |
| Evaluation framework   | Schema, error, pagination assertions     | Validate tool quality for LLM consumption         |
| Tool contract testing  | Schema field descriptions, edge cases    | Every field described, optional params handled    |
| CI smoke tests         | GitHub Actions + Inspector CLI           | Automated build, test, and transport health check |

## Spec Versions

The current MCP specification is **2025-11-25**. Key milestones:

- **2025-03-26**: Streamable HTTP transport (deprecated standalone SSE), tool annotations
- **2025-06-18**: Structured tool outputs, elicitation, OAuth auth server separation
- **2025-11-25**: Async tasks, extensions framework, sampling with tools, CIMD auth, server discovery

## Onboarding Protocol

When an agent needs a new capability:

1. **Validation**: Check if the required MCP server is already active
2. **Guide**: If missing, provide the user with a direct installation path
3. **Config**: Use `uvx` or `npx` for zero-install execution where possible

## Common Mistakes

| Mistake                                              | Correct Pattern                                                             |
| ---------------------------------------------------- | --------------------------------------------------------------------------- |
| Designing chatty APIs requiring many round-trips     | Build outcome-oriented tools that accomplish tasks in a single call         |
| Logging to stdout breaking the Stdio transport       | Log only to stderr to keep the transport channel clean                      |
| Returning raw exceptions and stack traces to the LLM | Return helpful error strings with suggested corrections                     |
| Building monolithic servers with dozens of tools     | Keep servers focused with 5-15 tools for discoverability and maintenance    |
| Using deprecated HTTP+SSE transport for new servers  | Use Streamable HTTP for remote servers (single endpoint, optional SSE)      |
| Hardcoding secrets in MCP server configuration       | Use environment variable mapping for all sensitive values                   |
| Returning large datasets in a single tool call       | Use pagination (20-50 records) or resource URIs for large data              |
| Implementing auth server inside MCP server           | MCP server acts as OAuth 2.1 resource server only, delegate auth externally |
| Vague tool descriptions causing LLM hallucination    | Add example usage and strict constraints to the tool description field      |
| Synchronous blocking on long operations              | Return async task handles for operations exceeding timeout thresholds       |
| Passing received tokens to upstream APIs             | Validate tokens locally; never forward to avoid confused deputy attacks     |
| Requesting secrets through elicitation               | Use URL mode elicitation or dedicated OAuth flows for credential collection |

## MCP Primitives

MCP servers expose three core primitive types to clients:

- **Tools**: Model-controlled actions the LLM invokes to accomplish tasks (function calling)
- **Resources**: Application-controlled data exposed via `mcp://` URIs that clients read on demand
- **Prompts**: User-controlled templates that provide structured context for specific workflows

Servers declare which primitives they support during capability negotiation in the `initialize` handshake. The November 2025 spec adds **Tasks** as an experimental primitive for async execution.

## Transport Selection

| Scenario             | Transport       | Notes                                                   |
| -------------------- | --------------- | ------------------------------------------------------- |
| Local CLI tools      | Stdio           | Fastest startup, no network overhead                    |
| Remote/cloud servers | Streamable HTTP | Single endpoint, optional SSE streaming                 |
| Legacy remote        | HTTP+SSE        | Deprecated since 2025-03-26, migrate to Streamable HTTP |

Clients should support Stdio whenever possible. Streamable HTTP supports both stateless and stateful server implementations via optional `Mcp-Session-Id` headers.

## Delegation

- **Discover and audit existing MCP server configurations**: Use `Explore` agent to check active servers, verify connectivity, and identify missing capabilities
- **Build and deploy a new MCP server with validation and auth**: Use `Task` agent to scaffold the server, implement Zod validation, and configure OAuth
- **Design MCP ecosystem architecture for multi-agent workflows**: Use `Plan` agent to map tool boundaries, transport selection, and security scoping

## References

- [Server development, tool design, argument flattening, pagination, and error handling](references/server-development.md)
- [Transport configuration: Stdio, Streamable HTTP, and migration from SSE](references/transports.md)
- [Security, OAuth 2.1 integration, elicitation, capability scopes, and HITL gates](references/security-auth.md)
- [Testing and evaluation: MCP Inspector, unit tests, contract tests, CI integration](references/testing-and-evaluation.md)
- [Troubleshooting guide, MCP Inspector, common errors, and transport debugging](references/troubleshooting.md)
