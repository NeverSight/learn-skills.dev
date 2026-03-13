---
name: context7-mcp-skill
description: Query up-to-date library documentation and code examples using Context7 MCP. Use when you need current, version-specific documentation for npm packages, Python libraries, or other programming languages.
metadata:
  short-description: Query library docs via Context7 MCP
---

# Context7 Skill

Use this skill to query library documentation and code examples.

## Prerequisites

- `uxc` skill is installed (see [uxc skill](https://github.com/holon-run/uxc/tree/main/skills/uxc) for installation)
- Network access to `https://mcp.context7.com/mcp`

## Core Workflow

1. Use fixed link command by default:
   - `command -v context7-mcp-cli`
   - If missing, create it: `uxc link context7-mcp-cli mcp.context7.com/mcp`
   - `context7-mcp-cli -h`
   - If command conflict is detected and cannot be safely reused, stop and ask skill maintainers to pick a different fixed command name.

2. Resolve a library name to get library ID:
   - `context7-mcp-cli resolve-library-id libraryName=react query='useState hook'`

3. Query documentation:
   - `context7-mcp-cli query-docs libraryId=/reactjs/react.dev query='how to use useState'`

## Available Tools

- **resolve-library-id**: Resolve a package/library name to Context7 library ID
- **query-docs**: Query documentation and code examples for a specific library

## Usage Examples

### Find React documentation

```bash
# First resolve the library
context7-mcp-cli resolve-library-id libraryName=react query='React useState hook'
```

### Query specific documentation

```bash
context7-mcp-cli query-docs '{"libraryId":"/reactjs/react.dev","query":"how to use useEffect"}'
```

### Query Node.js documentation

```bash
context7-mcp-cli resolve-library-id libraryName=node query='file system'
```

## Notes

- Requires library name first, then use the returned libraryId for queries
- Context7 provides version-specific, up-to-date documentation
- Supports npm packages, Python libraries, and more
- `context7-mcp-cli <operation> ...` is equivalent to `uxc mcp.context7.com/mcp <operation> ...`.
- If link setup is temporarily unavailable, use direct `uxc mcp.context7.com/mcp ...` calls as fallback.

## Reference Files

- Workflow details: `references/usage-patterns.md`
