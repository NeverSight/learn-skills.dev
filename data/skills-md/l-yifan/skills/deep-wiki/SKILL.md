---
name: deep-wiki
description: Access AI-generated documentation and insights for GitHub repositories via DeepWiki. This skill should be used when exploring unfamiliar codebases, understanding repository architecture, finding implementation patterns, or asking questions about how a GitHub project works. Supports any public GitHub repository.
---

# DeepWiki

Base directory for this skill: C:\Users\lyf1143312445\.agents\skills\deep-wiki

DeepWiki provides AI-generated documentation and Q&A for GitHub repositories. Use it to quickly understand codebases, explore architecture, and get answers about how projects work.

## When to Use

- Exploring an unfamiliar GitHub repository
- Understanding project architecture and structure
- Finding how specific features are implemented
- Getting quick answers about a codebase without reading all source code
- Learning about dependencies, patterns, and design decisions

## Quick Start

Run the CLI script with bun (use absolute path):

```bash
bun C:/Users/lyf1143312445/.agents/skills/deep-wiki/scripts/deepwiki.ts <command> [options]
```

DeepWiki now uses the Streamable HTTP MCP endpoint at `https://mcp.deepwiki.com/mcp`.
If a repository has not been indexed yet, DeepWiki may return a "Repository not found" error and ask you to visit the repository page on DeepWiki first.

## Available Commands

### read-wiki-structure

Get a list of documentation topics available for a repository.

```bash
bun C:/Users/lyf1143312445/.agents/skills/deep-wiki/scripts/deepwiki.ts read-wiki-structure --repo-name "facebook/react"
```

### read-wiki-contents

View the full AI-generated documentation for a repository.

```bash
bun C:/Users/lyf1143312445/.agents/skills/deep-wiki/scripts/deepwiki.ts read-wiki-contents --repo-name "vercel/next.js"
```

### ask-question

Ask any question about a repository and get an AI-generated answer.

```bash
bun C:/Users/lyf1143312445/.agents/skills/deep-wiki/scripts/deepwiki.ts ask-question \
  --repo-name "prisma/prisma" --question "How does the query engine work?"
```

## Global Options

- `-t, --timeout <ms>`: Call timeout (default: 30000)
- `-o, --output <format>`: Output format: `text` | `markdown` | `json` | `raw`

## Requirements

- [Bun](https://bun.sh) runtime
- `mcporter` package (embedded in script)

## References

See `references/api_reference.md` for detailed API documentation.
