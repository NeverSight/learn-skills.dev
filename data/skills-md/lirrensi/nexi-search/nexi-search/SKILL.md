---
name: nexi-search
description: Web search CLI that uses LLMs to search, read pages, and synthesize answers with citations. Use when you need current information from the web - news, documentation, recent events, or any topic requiring up-to-date sources. Invoke with `nexi --plain "query"` for programmatic use.
---

# NEXI for Agents

NEXI is a web search tool. It searches, reads multiple pages, and returns synthesized answers with source citations.

## Invocation

Always use `--plain` for non-interactive use:

```bash
nexi --plain "your search query"
```

The output is plain text with citations in `[1]`, `[2]` format and a sources section at the end.

## Effort Levels

Control search depth with `-e`:

| Level | Iterations | Use When |
|-------|------------|----------|
| `-e s` | 8 | Quick facts, simple lookups |
| `-e m` | 16 | Default, most queries |
| `-e l` | 32 | Deep research, complex topics |

Example:
```bash
nexi --plain -e l "compare React vs Svelte performance 2024"
```

## Output Format

```
[Answer text with inline citations like [1] and [2]...]

Sources:
[1] https://example.com/page1 - "Page Title"
[2] https://example.com/page2 - "Another Title"
```

Parse the sources section to extract URLs for further processing if needed.

## Additional Flags

| Flag | Purpose |
|------|---------|
| `--max-len N` | Limit output tokens (default 8192) |
| `--max-iter N` | Override max iterations |
| `--time-target N` | Force answer after N seconds |
| `-v` | Verbose: show tool calls (debugging) |

## Prerequisites

NEXI requires configuration before use. See [references/installation.md](references/installation.md) for:
- Install commands
- Required API keys (OpenAI-compatible + Jina)
- Config file location and format

If NEXI fails with config errors, read the installation reference to help set it up.
