---
name: gh-grep
description: Search real-world code examples across millions of GitHub repositories using grep.app. This skill should be used when looking for implementation patterns, API usage examples, library integration patterns, or production code references. Supports literal code search, regex patterns, and filtering by language/repo/path.
---

# GitHub Grep

Base directory for this skill: C:\Users\lyf1143312445\.agents\skills\gh-grep

Search for real-world code examples across over a million public GitHub repositories via grep.app.

## When to Use

- Finding implementation patterns for unfamiliar APIs or libraries
- Looking for correct syntax, parameters, or configuration examples
- Discovering production-ready code examples and best practices
- Understanding how different libraries/frameworks work together

## Quick Start

Run the CLI script with bun from this skill directory:

```bash
bun ./scripts/grep.ts searchGitHub --query "<code-pattern>" [options]
```

## Core Options

| Option | Description |
|--------|-------------|
| `--query` | Literal code pattern (required) |
| `--match-case` | Case-sensitive search |
| `--match-whole-words` | Match whole words only |
| `--use-regexp` | Interpret query as regex |
| `--repo` | Filter by repository (e.g., `facebook/react`) |
| `--path` | Filter by file path (e.g., `src/components/`) |
| `--language` | Filter by language (comma-separated, e.g., `TypeScript,TSX`) |

## Global Options

- `-t, --timeout <ms>`: Call timeout (default: 30000)
- `-o, --output <format>`: Output format: `text` | `markdown` | `json` | `raw`

## Search Patterns

**Important**: This tool searches for literal code patterns, not keywords.

Good searches:
- `useState(` - Find React useState usage
- `import React from` - Find React import statements
- `async function` - Find async function declarations

Bad searches:
- `react tutorial` - Keywords, not code
- `best practices` - Concepts, not patterns
- `how to use` - Questions, not code

For detailed pattern examples and regex usage, see `references/api_reference.md`.

## Common Examples

```bash
# Find Authentication Patterns
bun ./scripts/grep.ts searchGitHub \
  --query "getServerSession" --language "TypeScript,TSX"

# Find Error Boundary Implementations
bun ./scripts/grep.ts searchGitHub \
  --query "ErrorBoundary" --language "TSX"

# Find useEffect Cleanup with Regex
bun ./scripts/grep.ts searchGitHub \
  --query "(?s)useEffect\(\(\) => {.*removeEventListener" --use-regexp true

# Find CORS Handling in Flask
bun ./scripts/grep.ts searchGitHub \
  --query "CORS(" --match-case true --language "Python"

# Search Within Specific Repository
bun ./scripts/grep.ts searchGitHub \
  --query "createContext" --repo "facebook/react"
```

## Requirements

- [Bun](https://bun.sh) runtime
- `mcporter` package (embedded in script)

## Resources

- `scripts/grep.ts` - Main CLI tool wrapping grep.app MCP server
- `references/api_reference.md` - Detailed parameter documentation and regex patterns
