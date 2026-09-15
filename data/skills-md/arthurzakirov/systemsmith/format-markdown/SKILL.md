---
name: format-markdown
description: Generate properly formatted Markdown from unstructured notes, scratch text, transcripts, or rough drafts. Use when the user wants content rewritten into cleaner Markdown without inventing new information.
argument-hint: "[[--RAW] Raw message here..] [[--PART] Which part to apply guidelines to (default all)] [[--PRINCIPLE] Which specific guideline to apply (default all)] [[--SKIP] Which guidelines to skip (default none)]"
---

# Markdown Formatter

User request: `$ARGUMENTS`

Also apply the [`living-artifacts`](../living-artifacts/SKILL.md) skill when the output contains current-state values, snapshots, file trees, versions, paths, or any other data likely to drift.

## Core Task

Take unstructured content and rewrite it into clear Markdown while preserving meaning.

Likely problems in the source:

- Spelling or grammar errors
- Broken markdown syntax
- Bad structure
- Repetition
- Transcript noise or malformed sentences

## Preservation Rules

- Preserve all key information already present.
- Preserve nuance and examples.
- Fix obvious errors.
- Do not invent missing content.
- If extra guidance is valuable, add it only as an HTML comment.
- Reorder content when it improves readability.

## DRY Rule

Merge repeated sentences when they say the same thing without adding nuance, but do not collapse examples or erase meaningful distinctions.

## Formatting Techniques

- Use headings, lists, tables, callouts, emphasis, and code spans where helpful.
- Convert repeated items with shared properties into tables.
- Keep simple linear flows as lists.

## Code References

When repositories, folders, files, functions, or variables are mentioned:

1. Identify the exact target when possible.
2. Format names with inline code.
3. Link real file paths when the output is a maintained markdown artifact.

## Information Architecture

- Add higher-level grouping when the source has several substantial sections.
- Use a table of contents only when the document is large enough to justify it.
- Avoid over-structuring short content.
- Keep heading depth proportional to the material.

## Markdown-Specific Rules

- Preserve literal `$` syntax when it is semantically part of the source.
- Use valid heading levels.
- Keep frontmatter valid when the target artifact expects it.

## Self-Check

Review the result for:

- Preserved meaning
- Improved clarity
- No invented facts
- Consistent formatting
- Appropriate structure for the actual content size
