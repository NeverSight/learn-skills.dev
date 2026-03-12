---
name: linear-walkthrough
description: Use when asked to create a code walkthrough, explain how code works linearly, generate a walkthrough for a PR or codebase, or when user says /walkthrough. Triggers on "walkthrough", "explain the code", "how does this work", "walk me through".
---

# Linear Code Walkthrough

Generate a linear, step-by-step markdown walkthrough that explains how code works. Output is GitHub-flavored markdown that can be rendered as a self-contained HTML page.

## Detail Level

If in an interactive session (not piped/scripted), use AskUserQuestion to ask the detail level before writing:

- **Brief** — The user already knows the domain. Keep explanations short, focus on structure and key decisions. Minimal prose, mostly code snippets with short annotations.
- **In-depth** — The user wants thorough understanding. Explain design decisions, trade-offs, how pieces connect, and why things are done a certain way.
- **Beginner-friendly** — The user is new to this topic. Explain concepts as you go, define jargon, add context a newcomer would need. Enough depth to actually teach the topic, not just show the code.

If the user specifies a level in their request (e.g. "give me a quick walkthrough"), skip the question and use that level.

## Modes

### 1. Codebase Walkthrough

When asked to explain a codebase, module, or feature:

1. Read the relevant source files
2. Ask detail level (if interactive)
3. Plan a linear narrative: entry point -> core logic -> supporting pieces
4. Write the walkthrough markdown file
5. Suggest visualization

### 2. Pull Request Walkthrough

When given a PR (URL or number):

1. Fetch the PR diff and source using `gh`
2. Read the changed files and understand the full context
3. Ask detail level (if interactive)
4. Write the walkthrough markdown file
5. Reply with the content (do NOT commit)

## Writing the Walkthrough

**Format:** GitHub-flavored markdown (GFM)

**Structure:** Follow a linear narrative. Start from the entry point and walk through the code in the order it executes or in logical dependency order.

**Rules:**
- Include actual code snippets using fenced code blocks with language tags
- Use `grep`, `sed`, `cat`, or read tools to extract real snippets -- never fabricate code
- Use Mermaid.js diagrams (```` ```mermaid ````) for architecture, data flow, or request lifecycle visualizations
- Name the file something relevant (e.g., `auth-flow-walkthrough.md`, `api-design-walkthrough.md`) unless the user specifies a name
- Do NOT commit the walkthrough file unless explicitly asked

**Code block source links:**

Every code snippet MUST have a source link immediately above or below the fenced block so readers can jump to the original.

- **Remote PR walkthrough:** Link to the file on GitHub at the PR's head commit with line range.
  Format: `[path/to/file.py#L10-L25](https://github.com/OWNER/REPO/blob/HEAD_SHA/path/to/file.py#L10-L25)`
  Get the head SHA via `gh pr view NUMBER --json headRefOid -q .headRefOid`

- **Local codebase walkthrough:** Link using the `vscode://` protocol so clicking opens the file in VS Code at the right line.
  Format: `[path/to/file.py:10-25](vscode://file/absolute/path/to/file.py:10:1)`
  The `vscode://file/PATH:LINE:COLUMN` URI opens the file in VS Code. Use line range in the link text for readability.

**Template structure:**

```markdown
# [Topic]: Walkthrough

[1-2 sentence summary of what this walkthrough covers]

## Entry Point: [filename/function]

[Explanation of where everything starts]

[`src/main.py:10-18`](https://github.com/owner/repo/blob/SHA/src/main.py#L10-L18)
```python
[actual code snippet from the codebase]
`` `

## [Next Logical Step]

[Explanation continuing the narrative]

[`src/handler.py:5-12`](https://github.com/owner/repo/blob/SHA/src/handler.py#L5-L12)
```python
[code snippet]
`` `

## [Continue as needed...]

[Use mermaid diagrams where they help:]

```mermaid
graph LR
    A[Request] --> B[Router]
    B --> C[Handler]
    C --> D[Database]
`` `

## Summary

| Component | File | Purpose |
|-----------|------|---------|
| ... | ... | ... |
```

## For Pull Requests

Use `gh` to fetch PR details:

```bash
gh pr view NUMBER --json title,body,files,additions,deletions
gh pr diff NUMBER
```

Get the merge base commit SHA for GitHub permalinks:

```bash
gh pr view NUMBER --json baseRefOid,headRefOid
```

Then follow the same walkthrough structure, focusing on what the PR changes and why.

**PR-specific additions:**
- Start with a full GitHub PR URL link: `[PR #123: Title](https://github.com/OWNER/REPO/pull/123)` — this format (`https://github.com/OWNER/REPO/pull/NUMBER`) is required so the interactive server can auto-detect and fetch the PR diff for follow-up context.
- Follow with a summary of the PR's purpose
- Walk through changes in logical order (not file order)
- Highlight the key design decisions
- Note any potential concerns or trade-offs

## After Generating

After writing the walkthrough file, tell the user:

> Walkthrough saved to `[filename]`. To visualize it as a styled HTML page:
>
> ```bash
> uvx linear-walkthrough [filename] --serve
> ```
>
> Or generate a static HTML file:
>
> ```bash
> uvx linear-walkthrough [filename] -o walkthrough.html
> ```

**For PR walkthroughs**, suggest `--serve` with `--pr` so the interactive server seeds Claude with the full PR diff and metadata for better follow-up answers:

> ```bash
> uvx linear-walkthrough [filename] --serve --pr owner/repo#123
> ```
>
> The `--pr` flag fetches PR info and diff via `gh` CLI and includes it in the Claude seed context. If omitted, the server auto-detects GitHub PR URLs from the markdown content.

Do NOT run `uvx linear-walkthrough --serve` automatically -- let the user choose.
