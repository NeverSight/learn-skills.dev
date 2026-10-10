---
name: aps-mcp-server-gen
description: >
  Scaffold a custom MCP (Model Context Protocol) server that integrates with
  Autodesk Platform Services (APS). Use this skill when the user wants to
  build, create, generate, or set up an MCP server for APS, Autodesk, Forma,
  or any Autodesk cloud API. Supports Node.js/TypeScript, .NET/C#, and Python.
  Handles STDIO (local) and Streamable HTTP (cloud) transport, and various APS
  auth patterns: 2-legged OAuth, Secure Service Accounts, and 3-legged OAuth.
metadata:
  author: Developer Advocates @ Autodesk
  version: "0.1"
compatibility: Requires Node.js 20+, or .NET 9+, or Python 3.11+, plus internet access for package installation.
---

# APS MCP Server Generator

This skill creates a fully working MCP server project that connects to
Autodesk Platform Services (APS). Follow the steps below exactly.

## Step 1 — Gather Requirements

Ask the user **all three questions at once** if they have not already answered:

1. **Language** — Node.js/TypeScript, .NET/C#, or Python?
2. **Transport** — Local (STDIO, for Claude Desktop or similar) or Cloud (Streamable HTTP, for web deployment)?
3. **Authentication** — Which APS auth pattern?
   - **2-legged OAuth** — app accesses its own resources; no user sign-in (note: legacy, but still supported)
   - **Secure Service Accounts (SSA)** — automated server-to-server; acts on behalf of a real user without interactive login
   - **3-legged OAuth** — user signs in via browser; server acts on their behalf

If the user's request already makes one of the choices clear (e.g., "Python FastMCP server"), skip that question.

## Step 2 — Load Reference Docs

Before writing any files, load the appropriate references:

- **Node.js** → read [`references/nodejs.md`](references/nodejs.md)
- **.NET** → read [`references/dotnet.md`](references/dotnet.md)
- **Python** → read [`references/python.md`](references/python.md)
- **2-legged OAuth** → read [`references/auth-2lo.md`](references/auth-2lo.md)
- **Secure Service Accounts** → read [`references/auth-ssa.md`](references/auth-ssa.md)
- **3-legged OAuth** → read [`references/auth-3lo.md`](references/auth-3lo.md)
- **STDIO** → read [`references/transport-stdio.md`](references/transport-stdio.md)
- **Streamable HTTP** → read [`references/transport-http.md`](references/transport-http.md)
- **Always** → read [`references/testing.md`](references/testing.md)

## Step 3 — Confirm Output Directory

Ask or confirm where to create the project (default: `./aps-mcp-server` in the current directory).

## Step 4 — Scaffold the Project

Create every file needed for a working project. Do **not** leave placeholder TODOs — generate complete, runnable code. Use the patterns from the reference files exactly.

### Files to create (all languages)

| File | Purpose |
|------|---------|
| `.env.example` | All required env vars with placeholder values and comments |
| `README.md` | Setup, run, MCP client config, and test instructions |
| Main server file | Language-specific entry point |
| Tool file(s) | At least one example APS tool (e.g., list OSS buckets) |
| Auth helper | Token acquisition logic for the chosen auth type |
| Test file(s) | Unit tests with mocked APS calls (see `testing.md`) |

### Language-specific additional files

- **Node.js**: `package.json`, `tsconfig.json` (if TypeScript), `vitest` dev dependency
- **.NET**: `.csproj`, `appsettings.json`, `*.Tests` project with xUnit + NSubstitute
- **Python**: `pyproject.toml` (uv-managed), `pytest` + `pytest-asyncio` dev dependencies

## Step 5 — Post-Scaffold Instructions

After creating files, tell the user:

1. How to install dependencies (including test dependencies)
2. How to fill in `.env` (which APS portal pages to visit for each credential)
3. How to run the unit tests (no credentials required)
4. How to run the server
5. How to connect to it from an MCP client (Claude Desktop config or Inspector URL)
6. How to run an interactive smoke test with MCP Inspector

## Key Rules

- **Never implement token passthrough.** The MCP server must authenticate with APS itself — it must never accept APS tokens from the MCP client and forward them.
- **Always cache tokens.** Check expiry before every APS call; refresh proactively (≥60 s before expiry).
- **STDIO ↔ Stateless HTTP distinction.** STDIO servers are inherently single-session. Streamable HTTP servers should default to stateless (no session ID) unless 3-legged OAuth is chosen, which requires stateful sessions to track per-user tokens.
- **Tool descriptions matter.** Write clear docstrings/descriptions for every tool — the LLM uses them to decide when to call each tool.
- **Return both `content` and `structuredContent`** in Node.js tools when the data could be consumed programmatically (e.g., by a UI component). Python FastMCP infers structured output automatically from return types.
