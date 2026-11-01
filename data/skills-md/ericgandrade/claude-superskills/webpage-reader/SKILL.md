---
name: webpage-reader
description: This skill should be used when the user wants to read, fetch, extract, or analyze the content of a web page from a URL. Use when the user provides a URL to access documentation, articles, blog posts, research papers, release notes, or any online content and needs clean, readable Markdown output without navigation clutter, advertisements, or boilerplate HTML.
license: MIT
---

## Purpose

This skill extracts clean, readable Markdown from any web page URL by stripping navigation menus, advertisements, sidebars, footers, cookie banners, and all other non-content elements. It produces token-efficient output that focuses exclusively on the meaningful content of the page.

When agents fetch web pages using standard tools, the raw output often includes hundreds of navigation links, promotional widgets, and boilerplate text that consume tokens without adding value. This skill eliminates that noise using Defuddle, a purpose-built content extraction tool, to isolate the article body, documentation text, or main content and return only what matters.

The skill gracefully degrades when Defuddle is not installed: it offers to install it automatically or falls back to standard web fetching with a clear note about the trade-off in output quality and token usage.

This is a **universal skill** — it works in any project, any terminal context, and does not require Obsidian or any specific project structure.

## When to Use

Invoke this skill when:

- The user provides a URL and asks to "read", "fetch", "extract", or "get the content" of a page
- The user wants to analyze online documentation, API references, or technical guides
- The user shares a blog post, article, or research paper URL and needs the body content
- The user wants to save web content to a local Markdown file for offline reference or notes
- The agent needs to reference external content during a research or writing workflow
- The user asks to clean up or strip the noise from a page before reading it
- Multiple URLs are provided for batch processing in a research session

Do NOT use this skill when:

- The URL ends in `.md` — those files are already Markdown, use WebFetch directly instead
- The URL points to a PDF, DOCX, PPTX, or binary file — use `docling-converter` instead
- The user needs a multi-source research synthesis with citations — use `deep-research` instead
- The user needs to interact with the page (forms, logins, JavaScript-heavy apps)
- The URL requires authentication that the agent cannot provide
- The user asks to summarize a YouTube video — use `youtube-summarizer` instead

## Workflow

### Step 1: Validate the Input

Before fetching, inspect the URL provided by the user:

1. Verify the input is a valid HTTP or HTTPS URL. If it is not a URL, ask: "Please provide a valid URL starting with http:// or https://."
2. Check the file extension. Apply these routing rules:
   - `.md` files → use WebFetch directly (already Markdown, no extraction needed)
   - `.pdf`, `.docx`, `.pptx`, `.xlsx` files → redirect to `docling-converter`
   - `.mp3`, `.mp4`, `.wav` files → redirect to `audio-transcriber`
   - `.png`, `.jpg`, `.gif`, `.svg` files → inform the user that image extraction is not supported
   - All other URLs → proceed with extraction
3. If multiple URLs are provided, confirm the count and process each one sequentially.

### Step 2: Check Defuddle Availability

Run a quick availability check before attempting extraction:

```bash
defuddle --version
```

If Defuddle is available, proceed to Step 3a.

If Defuddle is not installed, present this offer to the user:

> "Defuddle is not installed. It extracts clean Markdown from web pages with significantly better quality than standard fetching. Install it now with `npm install -g defuddle`? It takes about 10 seconds. (yes/no)"

- If the user confirms: run `npm install -g defuddle`, then proceed to Step 3a.
- If the user declines: proceed to Step 3b with a note about reduced output quality.

### Step 3a: Extract Content with Defuddle (Preferred Path)

Use Defuddle to extract the page content:

```bash
# Extract and display as Markdown
defuddle parse <url> --md

# Extract and save to a file
defuddle parse <url> --md -o output-filename.md

# Extract specific metadata only
defuddle parse <url> -p title
defuddle parse <url> -p description
defuddle parse <url> -p author
defuddle parse <url> -p domain
```

Output format flags:

| Flag | Output | When to use |
|------|--------|-------------|
| `--md` | Markdown | Default choice for all content |
| `--json` | JSON with HTML and Markdown | When structured metadata is needed |
| (none) | HTML | Avoid — use `--md` instead |
| `-p <name>` | Single metadata property | When only title, author, or description is needed |

Always prefer `--md` unless the user explicitly requests another format.

### Step 3b: WebFetch Fallback (When Defuddle Is Unavailable)

If Defuddle is not available and the user declined installation, use the standard WebFetch capability with this note prepended to the output:

> Note: Fetching without Defuddle — output may contain navigation elements and non-content text that increases token usage. Install Defuddle with `npm install -g defuddle` for cleaner results.

Apply best-effort cleanup to the WebFetch output:
- Remove lines that appear to be navigation (very short lines containing only link text)
- Remove excessive blank lines (collapse to a maximum of two consecutive blank lines)
- Return the best available content with the caveat clearly noted

### Step 4: Handle Extraction Errors

If the page returns an error or blocks the request, respond with clear guidance:

| Situation | Response |
|-----------|----------|
| 403 Forbidden | "This site blocks automated access. Try opening it manually in a browser." |
| 404 Not Found | "Page not found. Please verify the URL is correct." |
| Timeout | Retry once automatically; if it fails again, report the timeout |
| Login required | "This page requires authentication. Log in first and share the content manually." |
| Paywall detected | "This content is behind a paywall and cannot be extracted automatically." |
| Empty extraction | Fall back to WebFetch and note the reduced quality |
| Invalid SSL | Report the SSL error and ask if the user wants to proceed anyway |

Never fabricate or invent page content when extraction fails. Always report failures honestly.

### Step 5: Format and Deliver the Output

Present the extracted content in a consistent format:

```markdown
# [Page Title]

**Source:** [full URL]
**Domain:** [domain.com]

---

[Extracted Markdown content]
```

If saving to a file, confirm the save:

> "Content saved to `[filepath]` — [word count] words extracted from [domain.com]."

If the user requested metadata only (title, author, description), return just the requested fields without the full body content.

For multiple URLs, separate each result with a clear divider and label each section with its source URL.

## Output Formats Reference

Defuddle supports several output modes. Choose the correct one based on what the user needs:

| Mode | Command flag | Output type | Best for |
|------|-------------|-------------|----------|
| Markdown | `--md` | Clean `.md` text | Reading articles, documentation, blog posts |
| JSON | `--json` | JSON with `html` and `markdown` fields | When structured metadata and body are both needed |
| HTML | (no flag) | Raw cleaned HTML | Avoid — use `--md` for readability |
| Metadata | `-p <name>` | Single string value | When only title, author, description, or domain is needed |

Available metadata properties via `-p`:
- `title` — page title
- `description` — meta description
- `author` — article author
- `domain` — domain name only
- `url` — canonical URL

Always default to `--md` unless the user requests a different format explicitly.

## Integration with Other Skills

This skill works well in combination with others:

- **Before `deep-research`** — use `webpage-reader` to pre-fetch and clean individual pages that will be cited in a research synthesis
- **Before `obsidian-note-builder`** — extract a URL first, then pass the clean Markdown to `obsidian-note-builder` to create a linked vault note
- **Before `youtube-summarizer`** — if the user provides a non-YouTube URL for a video page, route to `youtube-summarizer` instead
- **After `deep-research`** — use `webpage-reader` to fetch individual sources identified during a research session for deeper reading

When chaining skills, always inform the user which skill is handling which step so they understand the workflow.

## Critical Rules

**NEVER:**
- Use Defuddle to fetch URLs ending in `.md` — WebFetch is correct for Markdown files
- Fetch binary files (PDFs, images, Office documents) with this skill — redirect to `docling-converter`
- Fabricate or invent content when extraction fails — always report failures honestly and clearly
- Strip code blocks, technical content, or preformatted text during output cleanup — preserve all code fences exactly as found
- Return raw HTML when the user asked for readable content — always use `--md` flag
- Silently fall back to WebFetch without informing the user about the quality difference
- Attempt to access URLs behind authentication without clearly telling the user it is not possible
- Summarize or truncate extracted content unless the user explicitly requests a summary

**ALWAYS:**
- Check the URL extension before deciding which tool or fallback to use
- Offer to install Defuddle before falling back to lower-quality extraction
- Include the source URL in the output so users know where the content came from
- Preserve the full content without summarizing unless the user explicitly requests a summary
- Report extraction errors clearly with actionable next steps for the user
- Process multiple URLs sequentially and label each result clearly with its source URL
- Confirm file saves with the exact path and an approximate word count
- Respect the user's choice to decline Defuddle installation and proceed with the WebFetch fallback without repeating the install offer

## Example Usage

### Example 1: Read a documentation page

```
User: Read this page for me: https://docs.anthropic.com/en/docs/about-claude/models
```

Action: Check Defuddle availability → run `defuddle parse https://docs.anthropic.com/en/docs/about-claude/models --md` → return clean Markdown of the Claude models page, with source URL noted at the top.

Result: Clean Markdown of the documentation without navigation links, sidebar content, or promotional elements.

---

### Example 2: Save an article to a local file

```
User: Extract this article and save it to notes/microservices.md:
      https://martinfowler.com/articles/microservices.html
```

Action: Run `defuddle parse <url> --md -o notes/microservices.md` → confirm save.

Result: "Content saved to `notes/microservices.md` — 4,200 words extracted from martinfowler.com."

---

### Example 3: Get page metadata only

```
User: What is the title and author of this page?
      https://kentcdodds.com/blog/javascript-to-know-for-react
```

Action: Run `defuddle parse <url> -p title` and `defuddle parse <url> -p author` → return only the two metadata values.

Result: Title and author presented cleanly, without fetching the full body content.

---

### Example 4: Batch extraction for research

```
User: I am researching LLM evaluation frameworks. Read these three pages:
      - https://docs.ragas.io/en/latest/
      - https://www.trulens.org/
      - https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/
```

Action: Process each URL sequentially with Defuddle → return three labeled Markdown sections.

Result: Three clean extractions, each starting with its source URL, ready for comparison or summarization.

---

### Example 5: Defuddle not installed — install offer

```
User: Fetch https://research.google/blog/advances-in-research/ and summarize it
```

Action: Check `defuddle --version` → not found → present install offer.

Response: "Defuddle is not installed. Install it now with `npm install -g defuddle` for clean Markdown output? (yes/no)"

If the user says yes: install and extract. If no: fall back to WebFetch with a quality note, then proceed with extraction and summarization.
