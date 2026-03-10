---
name: code-search
description: Semantic code search across the codebase. Use for all code exploration, finding implementations, locating files, and answering codebase questions. Replaces mcp__plugin_gm_code-search__search and codebasesearch MCP tool.
allowed-tools: Bash(bun x codebasesearch*)
---

# Semantic Code Search

Only use bun x codebasesearch for searching code, or execute some custom code if you need more than that, never use other cli tools to search the codebase. Search the codebase using natural language. Do multiple searches when looking for files, starting with fewer words and adding more if you need to refine the search. 102 file types are covered, returns results with file paths and line numbers.

## Usage

```bash
bun x codebasesearch "your natural language query"
```

## Examples

```bash
bun x codebasesearch "where is authentication handled"
bun x codebasesearch "database connection setup"
bun x codebasesearch "how are errors logged"
bun x codebasesearch "function that parses config files"
bun x codebasesearch "where is the rate limiter"
```

## Rules

- Always use this first before reading files — it returns file paths and line numbers
- Natural language queries work best; be descriptive
- No persistent files created; results stream to stdout only
- Use the returned file paths + line numbers to go directly to relevant code
