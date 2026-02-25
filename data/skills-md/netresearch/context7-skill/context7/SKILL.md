---
name: context7
description: "Use when needing API docs, framework patterns, or code examples for any library. Fetches up-to-date documentation via Context7 REST API."
---

# Context7 Documentation Lookup Skill

Fetch current library documentation, API references, and code examples without MCP context overhead.

## When to Use This Skill

When the user asks about library APIs or framework patterns, use this skill to fetch current documentation.

When encountering import statements (`import`, `require`, `from`), use this skill to provide accurate API information.

When the user asks about specific library versions or "How do I use X library?", use this skill to get official patterns.

## Core Workflow

To answer questions about library documentation, follow these steps:

1. Search for the library ID using `scripts/context7.sh search`
2. Fetch documentation using `scripts/context7.sh docs`
3. Apply returned documentation to provide accurate, version-specific answers

## Running Scripts

### Searching for Libraries

To find a library ID for documentation lookup:

```bash
scripts/context7.sh search "library-name"
```

This returns library IDs in the format `/vendor/library` (e.g., `/facebook/react`).

### Fetching Documentation

To fetch documentation for a specific library:

```bash
scripts/context7.sh docs "<library-id>" "[topic]" "[mode]"
```

Parameters:
- `library-id` (required): From search result (e.g., `/facebook/react`)
- `topic` (optional): Focus area (e.g., `hooks`, `routing`, `authentication`)
- `mode` (optional): `code` for API references (default) or `info` for conceptual guides

### Examples

To get React hooks documentation:

```bash
scripts/context7.sh search "react"
scripts/context7.sh docs "/facebook/react" "hooks" "code"
```

To get Next.js routing guide:

```bash
scripts/context7.sh search "nextjs"
scripts/context7.sh docs "/vercel/next.js" "routing" "info"
```

## Documentation Modes

When fetching API references, examples, or code patterns, use `code` mode (default).

When fetching conceptual guides, tutorials, or explanations, use `info` mode.

## Environment Configuration

To use authenticated requests (optional), set the `CONTEXT7_API_KEY` environment variable:

```bash
export CONTEXT7_API_KEY="your-api-key"
```

---

> **Contributing:** https://github.com/netresearch/context7-skill
