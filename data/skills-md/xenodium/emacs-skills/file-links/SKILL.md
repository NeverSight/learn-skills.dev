---
name: file-links
description: 'When referencing files, format them as markdown links with line numbers using GitHub-style #L syntax.'
---

# Format file references as markdown links

When referencing files in your output, always format them as markdown links. Use the GitHub-style `#L` fragment for line numbers.

## Format

With a line number:

```
[filename.el:42](relative/path/to/filename.el#L42)
```

With a line range:

```
[filename.el:42-50](relative/path/to/filename.el#L42-L50)
```

Without a line number:

```
[filename.el](relative/path/to/filename.el)
```

## Important

- The link text uses `:` for line numbers (e.g., `filename.el:42`).
- The URL uses `#L` for line numbers (e.g., `filename.el#L42`).
- For ranges, the link text uses `-` (e.g., `filename.el:42-50`) and the URL uses `-L` (e.g., `filename.el#L42-L50`).
- The range must appear in both the link text and the URL.

Do NOT do this:

```
[filename.el#L42-L50](filename.el#L42)
```

## Rules

- Use paths relative to the project root.
- Include line numbers when they are relevant (e.g., error locations, function definitions, modified lines).
- Use line ranges when referring to a block of code.
- The link text should be the filename (or relative path if needed for clarity) followed by the line number.
