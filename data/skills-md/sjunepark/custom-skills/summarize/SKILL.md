---
name: summarize
description: Use the steipete/summarize CLI to summarize URLs, local files, stdin, YouTube links, podcasts, and media with LLM models. Trigger when users ask to install or run summarize, configure model/provider API keys, tune output flags (length/language/json/extract/slides), set defaults in ~/.summarize/config.json, or troubleshoot summarize CLI errors.
---

# Summarize CLI

Use this skill to run `summarize` effectively in terminal workflows.
Focus on practical usage and command execution, not broad project background.

## Workflow

1. Confirm input type and desired output format.
2. Run a minimal real command first (`summarize "<input>"`).
3. Select a model/provider and ensure matching API credentials.
4. Add flags incrementally only after a baseline run succeeds.
5. If it fails, re-run with `--verbose` or `--json` before changing multiple variables.

## Quick Patterns

- Summarize a URL: `summarize "https://example.com"`
- Summarize a local file: `summarize "/path/to/file.pdf"`
- Summarize piped input: `cat notes.md | summarize -`
- Summarize YouTube/media URL: `summarize "https://youtube.com/watch?v=..."`
- Force model/provider: `summarize "https://example.com" --model openai/gpt-5-mini`
- Control length: `summarize "https://example.com" --length long`
- Return diagnostics JSON: `summarize "https://example.com" --json`
- Extract content without summarizing: `summarize "https://example.com" --extract --format md`

## Configuration Rules

- Prefer explicit `--model` on task-critical runs.
- Use `~/.summarize/config.json` for stable defaults.
- Remember precedence for model selection:
  1. `--model`
  2. `SUMMARIZE_MODEL`
  3. `~/.summarize/config.json`
  4. built-in default (`auto`)

## Troubleshooting Flow

1. Re-run with `--verbose`.
2. Confirm API key matches the chosen provider/model.
3. Switch to a known-good model (for example `openai/gpt-5-mini` or `google/gemini-3-flash-preview`).
4. For media or YouTube failures, verify external dependencies (`yt-dlp`, `ffmpeg`, optionally `tesseract`).
5. Use `--json` to inspect extraction and metric fields.

## Scope

- Prioritize how to run commands and fix concrete failures.
- Do not include full repository-level documentation unless explicitly requested.
- Use [references/cli.md](references/cli.md) only for deeper flag/provider details.

## References

Read [references/cli.md](references/cli.md) for install commands, provider keys, advanced flags, and error-specific guidance.
