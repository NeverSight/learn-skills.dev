---
name: use-ctx7
description: Fetch up-to-date library documentation via the ctx7 CLI. Use PROACTIVELY whenever any code change, feature design, or implementation or user request involves a project dependency — always query the matching version's docs first before writing code.
---

Query indexed library documentation via the `ctx7` CLI. Always follow the two-step process below.

## 1.Resolve Library ID

```bash
ctx7 library <name> "<specific question>"
```

The query ranks results by relevance — be descriptive, not single-keyword.

**Pick the best match** by: closest name, highest snippet count, strongest reputation.

| Field            | Description                                              |
| ---------------- | -------------------------------------------------------- |
| Library ID       | Identifier for Step 2 (format: `/org/project`)          |
| Code Snippets    | Number of indexed examples — higher = better coverage    |
| Source Reputation | Authority: High, Medium, Low, Unknown                   |
| Benchmark Score  | Quality score 0–100                                      |
| Versions         | Version-specific IDs (format: `/org/project/version`)   |

For a specific version, use the version ID from results (e.g. `/vercel/next.js/v14.3.0-canary.87`).

## 2.Fetch Documentation

```bash
ctx7 docs <library-id> "<specific question>"
```

Library IDs **always start with `/`**. Using a bare name like `react` will fail.

Write specific queries describing what you want to accomplish — `"How to set up authentication with JWT in Express.js"` >> `"auth"`.

### Output formats

```bash
# Structured JSON
ctx7 docs /facebook/react "How to use hooks for state management" --json

# Pipe-friendly (no spinners/colors outside TTY)
ctx7 docs /vercel/next.js "middleware for route protection" | head -50
```

## Examples

```bash
# Next.js app router
ctx7 library nextjs "How to set up app router with middleware"
ctx7 docs /vercel/next.js "How to set up app router with middleware"

# Scripting: resolve ID then fetch
ctx7 library react "hooks" --json | jq '.[0].id'
```

## Checklist

- [ ] Always run `ctx7 library` first to get the correct ID
- [ ] Use the full `/org/project` ID — never a bare name
- [ ] Write descriptive queries, not single keywords
- [ ] Pick version-specific ID when the user needs docs for a particular version
