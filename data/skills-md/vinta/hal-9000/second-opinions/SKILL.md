---
name: second-opinions
description: Use when wanting independent review from external models before merging, committing, or finalizing architecture or plan decisions, or when the user asks for a second opinion, codex review, or gemini review
context: fork
user-invocable: true
model: opus
allowed-tools:
  - AskUserQuestion
  - Read
  - Glob
  - Grep
  - Bash(git diff:*)
  - Bash(git ls-files:*)
  - Bash(git symbolic-ref:*)
  - Bash(timeout:*)
  - Bash(gemini:*)
  - mcp__codex__codex
  - mcp__codex__codex-reply
---

If you are Codex or Gemini CLI, stop and do not use this skill.

# Second Opinions

Run independent reviews using OpenAI Codex (via MCP) and/or Google Gemini (via CLI) for second opinions from different model families.

**Modes:** `both` (default), `codex`, `gemini` -- selected via `AskUserQuestion`.

## When To Use

- Before opening a PR or merging a branch.
- Before committing significant changes.
- Plan or architecture review from multiple perspectives.
- Security, performance, or correctness audit.

## When Not To Use

- Trivial changes you can verify directly.
- When the user asked for your own judgment only.
- Do not send secrets, credentials, or tokens in prompts.

## Workflow

### 1. Gather Context

Use `AskUserQuestion` to collect review parameters in one call. Combine applicable questions (max 4).

**Tool** (always ask):

```
header: "Review tool"
question: "Which tool should run the review?"
options:
  - "Both Codex and Gemini (Recommended)" -> run both in parallel
  - "Codex only"                          -> mcp__codex__codex
  - "Gemini only"                         -> gemini CLI
```

**Scope** (always ask):

```
header: "Review scope"
question: "What should be reviewed?"
options:
  - "Uncommitted changes"  -> git diff HEAD + untracked files
  - "Branch diff vs main"  -> git diff <branch>...HEAD
  - "Specific commit"      -> follow up for SHA
```

**Focus** (always ask):

```
header: "Review focus"
question: "Any specific focus areas?"
options:
  - "General review"
  - "Security & auth"
  - "Performance"
  - "Error handling"
```

### 2. Preview and Validate

Auto-detect default branch for branch diffs:

```bash
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo main
```

Show diff stats for the selected scope. If empty, stop and tell the user. If >2000 lines changed, warn and ask whether to proceed or narrow scope.

### 3. Dispatch Reviews

**Project context:** If a `CLAUDE.md` exists in the repo root, always include it in the review prompt so reviewers check against project conventions.

Run the selected tool(s). When running both, issue `mcp__codex__codex` and `Bash(gemini ...)` calls **in a single message** for parallel execution. Both are read-only operations with no shared state.

See [references/codex.md](references/codex.md) for Codex MCP patterns.
See [references/gemini.md](references/gemini.md) for Gemini CLI patterns.

Do not pre-check tool availability. If a tool fails, report the install instructions from the error handling table and run only the available tool.

### 4. Present Results

When running both, present with clear headers:

```
## Codex Review
<codex findings>

## Gemini Review
<gemini findings>

## Summary
Where the two reviews agree and differ.
Prioritized action items.
```

When running a single tool, present its findings directly with your assessment of which findings are valid vs uncertain.

## Error Handling

| Error                           | Action                                                                   |
| ------------------------------- | ------------------------------------------------------------------------ |
| `mcp__codex__codex` unavailable | Run Gemini only,                                                         |
| `gemini: command not found`     | Run Codex only.                                                          |
| Both unavailable                | Stop and inform the user                                                 |
| Gemini extension missing        | Install: `gemini extensions install <github-url>` (see gemini reference) |
| Empty diff                      | Stop: no changes to review                                               |
| Timeout                         | Suggest narrowing the scope                                              |
| One tool fails                  | Present the other's results, note the failure                            |

## Examples

**Both tools (default):**

```
User: /second-opinions
Agent: [asks 3 questions: tool, scope, focus]
User: picks "Both", "Branch diff", "Security"
Agent: [detects default branch = main, shows diff --stat]
Agent: [auto-includes CLAUDE.md, dispatches mcp__codex__codex + gemini in parallel]
Agent: [presents both reviews, highlights agreements/differences]
```

**Single tool:**

```
User: /second-opinions
Agent: [asks 3 questions: tool, scope, focus]
User: picks "Codex only", "Uncommitted", "General"
Agent: [shows diff --stat]
Agent: [calls mcp__codex__codex with review prompt]
Agent: [presents findings with assessment]
```

**Large diff warning:**

```
User: /second-opinions
Agent: [asks questions] -> user picks "Both", "Uncommitted", "General"
Agent: [shows diff --stat: 45 files, +3200 -890]
Agent: "Large diff (3200+ lines). Proceed, or narrow the scope?"
User: "proceed"
Agent: [runs both reviews]
```
