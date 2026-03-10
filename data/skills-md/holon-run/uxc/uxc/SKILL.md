---
name: uxc
description: Discover and call remote schema-exposed interfaces with UXC. Use when an agent or skill needs to list operations, inspect operation schemas, and execute OpenAPI, GraphQL, gRPC, MCP, or JSON-RPC calls via one CLI contract.
metadata:
  short-description: Discover and call remote schema APIs via UXC
---

# UXC Skill

Use this skill when a task requires calling a remote interface and the endpoint can expose machine-readable schema metadata.

## When To Use

- You need to call APIs/tools from another skill and want one consistent CLI workflow.
- The interface may be OpenAPI, GraphQL, gRPC reflection, MCP, or JSON-RPC/OpenRPC.
- You need deterministic, machine-readable output (`ok`, `kind`, `data`, `error`).

Do not use this skill for pure local file operations with no remote interface.

## Prerequisites

- `uxc` is installed and available in `PATH`.
- For gRPC runtime calls, `grpcurl` is installed and available in `PATH`.

### Install uxc

Choose one of the following methods:

**Homebrew (macOS/Linux):**
```bash
brew tap holon-run/homebrew-tap
brew install uxc
```

**Install Script (macOS/Linux, review before running):**
```bash
curl -fsSL https://raw.githubusercontent.com/holon-run/uxc/main/scripts/install.sh -o install-uxc.sh
# Review the script before running it
less install-uxc.sh
bash install-uxc.sh
```

**Cargo:**
```bash
cargo install uxc
```

For more options, see the [Installation](https://github.com/holon-run/uxc#installation) section in the UXC README.

## Core Workflow

1. Discover operations:
   - `uxc <host> -h`
2. Inspect a specific operation:
   - `uxc <host> <operation> -h`
3. Execute with structured input:
   - `uxc <host> <operation> key=value`
   - `uxc <host> <operation> '<payload-json>'`
4. Parse result as JSON envelope:
   - Success: `.ok == true`, consume `.data`
   - Failure: `.ok == false`, inspect `.error.code` and `.error.message`
5. For disambiguation, use operation-level help first:
   - `uxc <host> <operation> -h`
6. For auth-protected endpoints, use the right auth track:
   - simple bearer / single-secret API key: see `references/auth-configuration.md`
   - multi-field auth or request signing: see `references/auth-configuration.md`
   - OAuth flows: see `references/oauth-and-binding.md`

## Link-First Workflow For Wrapper Skills

Wrapper skills should default to a fixed local link command instead of calling `uxc <host> ...` directly on every step.

1. Pick a fixed command name during skill development:
   - naming convention: `<provider>-mcp-cli`
   - examples: `notion-mcp-cli`, `context7-mcp-cli`, `deepwiki-mcp-cli`
2. Check whether the command already exists:
   - `command -v <link_name>`
3. If command is missing, create it:
   - `uxc link <link_name> <host>`
   - For OpenAPI services whose schema is hosted at a separate fixed URL, create the link with `uxc link <link_name> <host> --schema-url <schema_url>`
   - For stdio hosts that need credential-driven child env auth, create the link with `uxc link <link_name> <host> --credential <credential_id> --inject-env NAME={{secret}}`
4. Validate link command:
   - `<link_name> -h`
5. Use only the link command for the rest of the skill flow.

### Naming Governance

- Link naming is a skill author decision, not a runtime agent decision.
- Resolve ecosystem conflicts during skill development/review.
- Do not implement dynamic rename logic inside runtime skill flow.
- If runtime detects a command conflict that cannot be safely reused, stop and ask for skill maintainer intervention.

### Equivalence Rule

- `<link_name> <operation> ...` is equivalent to `uxc <host> <operation> ...`.
- If the link was created with `--schema-url <schema_url>`, it is equivalent to `uxc <host> --schema-url <schema_url> <operation> ...`.
- If the link was created with `--credential <credential_id> --inject-env NAME={{secret}}`, it is equivalent to `uxc --auth <credential_id> --inject-env NAME={{secret}} <host> <operation> ...`.
- Callers can still override that persisted schema by passing `--schema-url <other_url>` explicitly at runtime.
- Use `uxc <host> ...` only as a temporary fallback when link setup is unavailable.

## Input Modes

- Preferred (simple payload): key/value
  - `uxc <host> <operation> field=value`
- Bare JSON positional:
  - `uxc <host> <operation> '{"field":"value"}'`
Do not pass raw JSON through `--args`; use positional JSON.

## Output Contract For Reuse

Other skills should treat this skill as the interface execution layer and consume only the stable envelope:

- Success fields: `ok`, `kind`, `protocol`, `endpoint`, `operation`, `data`, `meta`
- Failure fields: `ok`, `error.code`, `error.message`, `meta`

Default output is JSON. Do not use `--text` in agent automation paths.

## Reuse Rule For Other Skills

- If a skill needs remote API/tool execution, reuse this skill instead of embedding protocol-specific calling logic.
- Wrapper skills should adopt a fixed link command (`<provider>-mcp-cli`) as the default invocation path.
- Upstream skill inputs should be limited to:
  - target host
  - operation id/name
  - JSON payload
  - required fields to extract from `.data`

## Reference Files (Load On Demand)

- Workflow details and progressive invocation patterns:
  - `references/usage-patterns.md`
- Protocol operation naming quick reference:
  - `references/protocol-cheatsheet.md`
- Public endpoint examples and availability notes:
  - `references/public-endpoints.md`
- Authentication configuration (simple `secret`, named `fields`, headers/query params, and request signers):
  - `references/auth-configuration.md`
- OAuth and credential/binding lifecycle:
  - `references/oauth-and-binding.md`
- Failure handling and retry strategy:
  - `references/error-handling.md`
