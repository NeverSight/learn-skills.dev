---
name: dsearch
description: Search and read offline documentation for various programming languages and libraries. Use this skill when you need to verify syntax, check function signatures, or read documentation without internet access.
license: MPL-2.0
compatibility: Requires dsearch CLI to be installed and available in PATH.
---

# dsearch

`dsearch` is a CLI tool for searching and reading offline documentation (via DevDocs).

## Tools

### dsearch

The primary command for interacting with documentation.

#### Examples

**List installed documentation**

To see what documentation is available:

```bash
dsearch list
```

**Search for a specific term**

To search for a term across all installed documentation:

```bash
dsearch "query string"
```

**Search within a specific documentation set**

To narrow down the search to a specific language or library (e.g., Go):

```bash
dsearch "http.Client" --doc go
```

**Read documentation in Markdown format**

For LLM consumption, always use `--format md` to get clean Markdown output, and include `--full` to ensure the entire page is retrieved without truncation:

```bash
dsearch "http.Client" --doc go --format md --full
```

**Install new documentation**

If the required documentation is missing:

```bash
dsearch install python
```

#### Best Practices

- Always use `--format md` when valid to get machine-readable output.
- Use `--full` to retrieve the complete documentation page, preventing truncation of long articles.
- Use `--doc <name>` to reduce noise when you know the context (e.g., searching for `Map` in `go` vs `javascript`).
- If a search returns too many results, try a more specific query or use the `--limit` flag.
