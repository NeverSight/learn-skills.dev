---
name: markdown-new
description: "Convert public web pages into clean Markdown with markdown.new for AI workflows. Use when tasks require URL-to-Markdown conversion for summarization, RAG ingestion, extraction, archiving, or token reduction, including selecting conversion method (auto/ai/browser), enabling image retention, and handling rate limits or conversion failures."
---

# Markdown.new

Use this skill to convert public URLs into LLM-ready Markdown via [markdown.new](https://markdown.new).

## Path Resolution (Critical)

- Resolve relative paths like `scripts/...` and `references/...` from the skill directory, not workspace root.
- If current directory is unknown, use an absolute script path.

```bash
python3 ~/.codex/skills/markdown-new/scripts/markdown_new_fetch.py 'https://example.com'
```

```bash
cd ~/.codex/skills/markdown-new
python3 scripts/markdown_new_fetch.py 'https://example.com'
```

Avoid this pattern from an arbitrary workspace root:

```bash
python3 scripts/markdown_new_fetch.py 'https://example.com'
```

## Workflow

1. Validate the input URL is public `http` or `https`.
2. Run `scripts/markdown_new_fetch.py` with `--method auto` first.
3. Re-run with `--method browser` if output misses JS-rendered content.
4. Enable `--retain-images` only when image links are required.
5. Capture response metadata (`x-markdown-tokens`, `x-rate-limit-remaining`, and JSON metadata when present) for downstream planning.

## Quick Start

Commands below assume current directory is the skill root (`~/.codex/skills/markdown-new`).

```bash
python3 scripts/markdown_new_fetch.py 'https://example.com' > page.md
```

```bash
python3 scripts/markdown_new_fetch.py 'https://example.com' --method browser --retain-images --output page.md
```

```bash
python3 scripts/markdown_new_fetch.py 'https://example.com' --deliver-md
```

## Method Selection

- `auto`: default. Let markdown.new use its fastest successful pipeline.
- `ai`: force Workers AI HTML-to-Markdown conversion.
- `browser`: force headless browser rendering for JS-heavy pages.

Use `auto` first, then retry with `browser` only when needed.

## Delivery Mode

- Use `--deliver-md` to force file output in `.md` format.
- In delivery mode, content is wrapped as:
  - `<url>`
  - `...markdown...`
  - `</url>`
- If `--output` is omitted, the script auto-generates a filename from the URL.

## API Modes

- Prefix mode:
  - `https://markdown.new/https://example.com?method=browser&retain_images=true`
- POST mode:
  - `POST https://markdown.new/`
  - JSON body: `{"url":"https://example.com","method":"auto","retain_images":false}`

Prefer POST mode for automation and explicit parameters.

## Limits And Safety

- Treat `429` as rate limiting (documented limit: 500 requests/day/IP).
- Convert only publicly accessible pages.
- Respect `robots.txt`, terms of service, and copyright constraints.
- Do not treat markdown.new output as guaranteed complete for every page; verify critical extractions.

## References

- `references/markdown-new-api.md`
