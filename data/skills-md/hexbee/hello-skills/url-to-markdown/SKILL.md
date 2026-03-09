---
name: url-to-markdown
description: Convert a public webpage URL into Markdown and save it as a reusable `.md` file with the bundled script. Prefer `https://r.jina.ai/<url>` first, and only fallback to `https://markdown.new/` if `r.jina.ai` is unavailable. Use this whenever the user wants to turn a public webpage, article, documentation page, blog post, release note, or reference URL into Markdown for reading, archiving, summarizing, extraction, RAG prep, or downstream agent reuse, even if they do not explicitly mention markdown or saving a file.
---

# URL To Markdown

## Overview

Use this skill to fetch a public URL, convert it to Markdown, and save the result as a timestamped Markdown file for later agent use.

Conversion priority is fixed:

1. `https://r.jina.ai/<url>` (primary)
2. `https://markdown.new/` (fallback only when `r.jina.ai` is unavailable)

This skill is execution-oriented. Prefer running the bundled script instead of manually recreating the workflow.

## When To Use

Use this skill when the user asks for any of the following:

- convert a URL or webpage to Markdown
- save an article, doc page, or blog post as `.md`
- ingest a public webpage for later summarization or extraction
- preserve page content in a machine-friendly text format
- pull a documentation page into a local Markdown file

Do not use this skill for:

- private pages that require browser login
- sites the user is not authorized to access
- tasks that require full site crawling rather than a single page fetch

## Inputs

Decide these inputs before running the script:

- `url`: required (single URL mode); must be a public URL
- `urls`: optional; multiple URLs for batch conversion (mutually exclusive with positional url)
- `concurrency`: optional; number of parallel conversions (default `3`); used in batch mode
- `output_dir`: optional; output directory for batch conversion; creates slug-based filenames
- `method`: optional; one of `auto`, `ai`, `browser`; default `auto`; used by `markdown.new` fallback
- `retain_images`: optional; default `false`; used by `markdown.new` fallback
- `transport`: optional; one of `auto`, `get`, `post`; default `auto`; used by `markdown.new` fallback
- `timeout`: optional; default `30`
- `force_markdown_new`: optional; default `false`; when `true`, skip `r.jina.ai` and call `markdown.new` directly
- `output`: default `./output/` (current directory + `output/`); if the user explicitly provides an output path in the prompt, use that path instead

If the user does not specify these options, keep the defaults.

Output path rule:

- Always pass `--output` when invoking `url_to_md.py`.
- If user prompt explicitly specifies an output path, use that exact path.
- Otherwise use `--output "output/"` (relative to current working directory).

## Run The Script

From the skill directory, run:

```bash
python scripts/url_to_md.py "<url>" --output "output/"
```

Common variants:

```bash
python scripts/url_to_md.py "<url>" --output "output/"
python scripts/url_to_md.py "<url>" --method browser --retain-images --output "output/"
python scripts/url_to_md.py "<url>" --transport post --timeout 45 --output "output/"
python scripts/url_to_md.py "<url>" --force-markdown-new --output "output/"
python scripts/url_to_md.py "<url>" --output "<user_explicit_path>"
```

Batch conversion:

```bash
# Batch convert multiple URLs with parallel processing (default concurrency=3)
python scripts/url_to_md.py --urls "https://example.com" "https://example.org" "https://example.net" --output-dir "output/"

# Batch with custom concurrency
python scripts/url_to_md.py --urls "https://a.com" "https://b.com" "https://c.com" "https://d.com" "https://e.com" --concurrency 5 --output-dir "output/"

# Single URL in batch mode
python scripts/url_to_md.py --urls "https://example.com" --output-dir "output/"
```

Behavior notes:

- The script always attempts `r.jina.ai` first.
- If `--force-markdown-new` is set, the script skips `r.jina.ai` and uses `markdown.new` directly.
- It falls back to `markdown.new` only when `r.jina.ai` is unavailable (for example timeout, network failure, 5xx, or rate limit).
- Skill-level default output directory is `./output/`, and the invocation should always include `--output`.
- If `--output` is a filename, the script appends a timestamp before the extension.
- If `--output` is a directory, the script creates a slug-based filename with a timestamp.

## Required Output Behavior

Prefer producing both:

1. A saved Markdown file.
2. A short conversational summary.

The summary should include:

- source URL
- whether the conversion succeeded
- provider used: `r.jina.ai` or `markdown.new`
- saved file path, if a file was written
- key options used if non-default: `method`, `retain_images`, `transport`, `timeout`

## Summary Template

Use this structure:

```text
Source URL: <url>
Status: success
Provider: <r.jina.ai|markdown.new>
Saved Markdown: <path>
Options: method=<value>, retain_images=<value>, transport=<value>, timeout=<value>
```

If defaults were used, keep `Options` brief.

## Error Handling

If the script fails:

- say that URL-to-Markdown conversion failed
- include the main error briefly
- do not invent page content
- mention likely cause when obvious: network issue, timeout, rate limit, unsupported page access

If both providers fail, report which provider failed first and which provider failed last.
If the service returns rate limiting, report that directly and avoid pretending a retry succeeded.

## Notes

- Prefer saved Markdown over raw stdout because agents can reuse local files more reliably.
- The bundled script uses only the Python standard library.
- The script supports both importable usage and CLI execution, but this skill should normally use the CLI path.
