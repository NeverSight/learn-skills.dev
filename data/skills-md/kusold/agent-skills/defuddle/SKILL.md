---
name: defuddle
description: Extract clean article content and metadata from a web page as Markdown with the defuddle CLI; use for "extract this article", "convert this page to markdown", "get the main content of this URL", "clean up this HTML", "save a readable snapshot", or when asked to fetch a page's readable text instead of raw HTML.
metadata:
  credits:
    skill: defuddle
    author: Steph Ango
    organisation: Obsidian
    url: "https://github.com/kepano/obsidian-skills/blob/main/skills/defuddle/SKILL.md"
---

# Defuddle

Extract the main content and metadata from a web page with the defuddle CLI. Defuddle strips navigation, ads, and boilerplate, returning readable article content rather than a raw HTML dump. Sources can be a URL, a local HTML file, or stdin.

This skill depends on the `defuddle` CLI (npm package `defuddle`). When it is not installed, or when the result feeds something durable (archival snapshots, extractions compared over time), run it through npx with a pinned version so results stay reproducible:

```bash
npx --yes defuddle@0.19.5 parse <source>
```

A locally installed `defuddle` is fine for one-off extractions; record its version when the output is kept.

## Choose where to save

For an article extraction or snapshot request (including a bare invocation with a URL), save a Markdown file with frontmatter by default. Requests only to read, summarize, or inspect metadata do not require a saved file.

1. Honor an explicit output path or a destination supplied by the calling workflow.
2. Otherwise, read applicable repository instructions and look for `_inbox/` in the current directory or at the current repository root. If it exists, save the result there, including when invoked from a repository subdirectory.
3. If neither has an `_inbox/`, save in the current directory. Do not create an inbox or use a temporary directory as the final destination unless requested.

Use a descriptive kebab-case filename based on the article title or URL, such as `_inbox/pi-durable.md`. Check for an existing file before writing; add a date or unique suffix on collision rather than overwriting it. Temporary files are fine for discovery and validation, but deliver the verified snapshot at the selected destination and report its final path.

For example, from a repository root containing `_inbox/`, after confirming the filename is available:

```bash
npx --yes defuddle@0.19.5 parse https://flaviocopes.com/pi-durable/ --frontmatter --markdown --output _inbox/pi-durable.md
```

Saving in `_inbox/` queues the source; it does not authorize wiki ingestion, wiki page edits, or a commit.

## Choose the output format

| Need | Command |
| --- | --- |
| Readable Markdown | `defuddle parse <source> --markdown` |
| Content plus all metadata | `defuddle parse <source> --json` |
| One metadata field | `defuddle parse <source> --property <name>` |
| Complete page snapshot | `defuddle parse <source> --frontmatter --markdown --output <file>` |

- `--markdown` (`-m`) prints extracted content as Markdown. Tables become Markdown tables and code fences survive conversion.
- `--json` (`-j`) is the discovery mode: one JSON object with content and every metadata field. Inspect it before pulling individual properties.
- `--property` (`-p`) names are the JSON keys: `title`, `description`, `author`, `published`, `site`, `domain`, `language`, `image`, `favicon`, `wordCount`, `content`, `contentMarkdown`. They are case-sensitive camelCase — `--property word_count` fails with "Property not found"; use `wordCount`.
- `--frontmatter` (`-f`) prepends YAML frontmatter (`title`, `site`, `source`, `domain`, `language`, `word_count`) to the content. Combined with `--markdown` and `--output` (`-o`), this produces a complete page snapshot in one step.

Other options: `--user-agent <string>` (`-u`) for servers that reject the default agent, and `--lang <code>` (`-l`) as a BCP 47 language hint for multilingual sites.

Read from stdin when the page needs to be fetched another way (cookies, custom headers, `curl`):

```bash
curl -sL <url> | defuddle parse - --markdown
```

## Verify the extraction before using it

Treat the output as a claim to check, not a completed fetch.

- Fetch failures print `Error: ...` but **exit 0** — the exit code is not a success signal. Check the output itself.
- Confirm real content arrived: a non-empty body, a plausible `wordCount`, and the expected topic. A result that is empty, a single line, or a login/cookie-consent/paywall notice means extraction failed — report that instead of summarizing the stub as the source.
- JavaScript-rendered pages (SPAs) often return little or no content. Try once; if the result is clearly incomplete, report the limitation and fall back to another route (the page's native Markdown or API, a reader-mode proxy, or asking the user) rather than presenting a partial extraction as complete.
- On 403/FORBIDDEN, retry once with `--user-agent` set to a browser string. If it still refuses, report the failure with the URL.

## Boundaries

- HTML only. For PDFs, JSON APIs, or pages behind authentication, use an appropriate tool instead of forcing defuddle.
- When serving as the extraction step for a wiki-ingest URL snapshot, the wiki-ingest workflow stays in charge: provenance, retrieval date, and commit discipline belong to it. Record the defuddle version as the extraction method alongside any omissions.
