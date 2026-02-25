---
name: openclaw-grok-search
description: Cross-platform real-time web research and search via an OpenAI-compatible Grok endpoint, returning JSON with content and sources. Use for version checks, API and docs verification, troubleshooting, and any time-sensitive facts on Windows, macOS, or Linux.
---

# Openclaw Grok Search

Run cross-platform web research and return structured JSON output with `content` and `sources`.
This skill is project-local and should run directly from the downloaded project directory.

## When to Use

Use this skill before answering when any of these apply:

1. The user asks for latest/current/today/recent information.
2. The answer depends on versions, releases, changelogs, or compatibility.
3. The task needs official docs, API references, or source URLs.
4. The user reports an error and root-cause analysis needs web evidence.
5. You are uncertain and need external confirmation before final output.

## Quick Start

1. Write config interactively (first run only).

```bash
python scripts/configure.py
```

2. Run a query.

```bash
python scripts/grok_search.py --query "What changed in Python recently?"
```

## Config Priority

1. CLI args such as `--base-url` and `--api-key`
2. Environment vars `GROK_*`
3. Config files

Default config lookup order:

1. `config.json`
2. `config.local.json`

## Cross-Platform Rules

1. Prefer `python ...` commands, do not require PowerShell-only syntax.
2. Keep config in the project folder, do not install or copy into `~/.codex`.
3. Support `GROK_CONFIG_PATH` only when you explicitly want a custom path.

## Output Shape

Always print JSON with:

1. `ok`
2. `content`
3. `sources`
4. `raw`

## Anti-Patterns

| Prohibited | Correct |
|------------|---------|
| No source citation | Include `Source [<sup>1</sup>](URL)` |
| Give up after one failure | Retry at least once |
| Use built-in WebSearch/WebFetch | Use GrokSearch tools/CLI |
