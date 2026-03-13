---
name: claude-code-copy-markdown
description: Copy Claude Code's previous response (or a specific part of the conversation output) to the clipboard as clean Markdown. Trigger phrases include "copy this", "copy to clipboard", "markdown copy", "md copy", "I want to copy this", "copy the last output", "paste this somewhere", etc. Do NOT use this skill when the user explicitly asks to write to a file — just write to a file normally in that case. Trigger this skill proactively whenever the user wants to "copy", "paste", "share", or "export" Claude Code output.
---

# Claude Code Copy Markdown

Copy Claude Code's response as clean Markdown to the macOS clipboard (pbcopy).

## Why this skill exists

Claude Code renders output richly in the terminal — box-drawing tables, indented lists, colored text, etc. This looks great in the terminal, but when you copy-paste it elsewhere, line breaks get mangled and tables fall apart. Asking "write that to a markdown file" every time is tedious. This skill reduces that to a single action.

## Workflow

1. User says "copy this", "copy as markdown", etc.
2. Identify the previous response (or the part the user specified)
3. Reformat the content as proper Markdown
4. Pipe it to `pbcopy`
5. Confirm completion

## Formatting rules

Convert the previous response into clean Markdown following these rules.

### Headings

- Section titles that were displayed as bold or prominent text become `##` or `###` headings

### Lists

- Use `- ` for all bullet points
- Nest with 2-space indentation

### Code blocks

- Wrap inline code with `` ` ``
- Wrap multi-line code with ` ``` ` and include the language name when known
- File path references (e.g. `path/to/file.ts:10`) become inline code

### Tables

- Convert box-drawing tables (`┌─┬─┐`, etc.) into Markdown pipe tables
- Include header row and separator row

```markdown
| Field   | Meaning                               |
| ------- | ------------------------------------- |
| foundAt | The date the job was first discovered |
```

### Line breaks and whitespace

- One blank line between paragraphs
- Remove excessive consecutive blank lines
- Join lines that were split by terminal word-wrapping into a single paragraph

### Emphasis

- Use `**bold**` for keywords or field names that were emphasized in the original output

## Partial copy

When the user specifies a range (e.g. "just copy the table part", "copy the code section"), extract and copy only that portion. If no range is specified, copy the entire previous response.

## Execution

Pipe the formatted Markdown to `pbcopy` using a heredoc to safely handle quotes and special characters:

```bash
pbcopy <<'MARKDOWN_EOF'
(formatted Markdown here)
MARKDOWN_EOF
```

## Completion message

After copying, respond briefly:

> Copied to clipboard.

No need for lengthy explanation or repeating the full content — the user already saw the output and just needs confirmation that it's now in the clipboard as Markdown.
