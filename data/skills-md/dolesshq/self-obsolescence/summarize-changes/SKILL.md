---
name: summarize-changes
description: Summarize code changes by author type and scope. Inputs are author and scope with product plus PR as defaults.
metadata:
  short-description: Inputs author scope. Use PR or branch aliases. Defaults product plus PR
---

# Summarize Changes

## Goal

Produce accurate, audience-specific summaries of code changes from a selected scope.

## When to use

Use this skill when the user asks for change summaries such as:

- "summarize what changed"
- "summarize staged/unstaged changes"
- "summarize all uncommitted work"
- "summarize this branch/PR"
- "write this summary as an engineer/PM"

## Invocation syntax

Preferred invocation:

```text
$summarize-changes <author-type> <scope>
```

No-args invocation is allowed:

```text
$summarize-changes
```

Examples:

```text
$Summarize Changes engineer PR
$summarize-changes engineer branch
$summarize-changes product-manager all-uncommitted
$summarize-changes
```

Normalization rules:

- Treat skill trigger as case-insensitive (`$Summarize Changes` and `$summarize-changes` are both valid).
- Normalize author aliases before execution:
  - `product` -> `product-manager`
  - `pm` -> `product-manager`
- Normalize scope aliases before execution:
  - `PR`, `pr`, `pr-wide` -> `pr-wide`
  - `branch`, `branch-wide` -> `branch-wide`
  - `unstaged` -> `unstaged`
  - `staged` -> `staged`
  - `all-uncommitted`, `uncommitted` -> `all-uncommitted`
  - `last-message`, `last` -> `last-message`
- If scope token is unknown, ask one short clarification question.
- If author and/or scope is missing, ask one short clarification question with choices; if unanswered, default to `product` + `PR`.

## Scope modes

Choose exactly one scope mode unless the user asks for multiple.

1. `last-message`
- Summarize only changes referenced in the latest user/assistant implementation message.
- Validate references against actual git diff before reporting.

2. `unstaged`
- Use: `git diff`
- Include untracked files separately via `git status --porcelain`.

3. `staged`
- Use: `git diff --cached`

4. `all-uncommitted`
- Combine:
  - unstaged diff (`git diff`)
  - staged diff (`git diff --cached`)
  - untracked files (`git status --porcelain`)

5. `branch-wide`
- Use: `git diff <base>...HEAD`
- If base is not provided, infer from upstream (for example `origin/main`) and state assumption.
- Alias support: `branch`, `branch-wide`

6. `pr-wide`
- Prefer GitHub CLI when available:
  - `gh pr view --json baseRefName,headRefName,number,title`
  - `gh pr diff`
- If PR metadata is unavailable, fall back to `branch-wide` and state fallback.
- Alias support: `PR`, `pr`, `pr-wide`

## Author personas

Pick one primary persona. Optional secondary persona is allowed if user asks.

1. `engineer`
- Focus: technical implementation details, files, APIs, data model, migrations, tests, risk.
- Include concrete file-level notes and verification commands/results when available.

2. `product-manager`
- Focus: user-visible features, UX changes, workflow impact, release notes framing.
- Avoid low-value internal details unless they change behavior or risk.

3. `designer`
- Focus: UI/UX behavior, interaction flow, visual hierarchy, accessibility-relevant changes.

4. `qa`
- Focus: test impact, risk areas, regression vectors, what to test manually and automatically.

5. `security`
- Focus: authn/authz changes, data access boundaries, secrets/config, attack surface delta.

6. `executive`
- Focus: concise impact summary, delivery status, risks, and next steps.

## Workflow

1. Resolve scope and persona
- If user did not specify, default to:
  - scope: `PR` (normalized to `pr-wide`)
  - persona: `product` (normalized to `product-manager`)
- Normalize aliases first (`PR` -> `pr-wide`, `branch` -> `branch-wide`, `product` -> `product-manager`).
- Ask at most one question only if required to avoid wrong scope.

2. Collect evidence
- Run scope-appropriate git/PR commands.
- Build file list grouped by area (backend, frontend, db, tests, docs, infra).

3. Classify changes
- Identify:
  - added/changed/removed files
  - behavioral vs refactor-only changes
  - data/model/API/test/documentation deltas

4. Draft persona-specific summary
- Apply persona focus rules.
- Keep statements evidence-based (from diff/logs/PR metadata).

5. Add risks and unknowns
- List material risks, assumptions, and missing validation.

## Required sections

Every summary must include:

- `Scope`: explicit mode and command basis
- `Audience`: selected persona
- `What changed`: concise bullets
- `Files touched`: grouped list or highlights
- `Risks / follow-ups`: only material items

## Output templates

### Template: Engineer

```markdown
Scope: `<scope-mode>`
Audience: `engineer`

What changed:
- <technical change>
- <technical change>

Files touched:
- `<path>`: <what changed and why>
- `<path>`: <what changed and why>

Verification status:
- `<command>` -> `<result>`
- `<command>` -> `<result>`

Risks / follow-ups:
- <risk or gap>
- <next action>
```

### Template: Product Manager

```markdown
Scope: `<scope-mode>`
Audience: `product-manager`

Feature/UX impact:
- <user-visible capability or behavior change>
- <user-visible capability or behavior change>

Experience changes by area:
- `<route/page/feature>`: <what changed for users>
- `<route/page/feature>`: <what changed for users>

Release notes draft:
- <customer-facing summary line>
- <customer-facing summary line>

Risks / rollout notes:
- <known risk, edge case, or migration note>
- <recommended mitigation or follow-up>
```

### Template: QA

```markdown
Scope: `<scope-mode>`
Audience: `qa`

Change inventory:
- <high-risk code path changed>
- <high-risk code path changed>

Regression focus:
- <what can break and where>
- <what can break and where>

Test plan updates:
- Automated: <tests to add/update/run>
- Manual: <critical user flows to verify>

Known gaps / blockers:
- <missing test coverage or environment blocker>
```

## Guardrails

- Do not invent behavior that is not present in diffs/PR evidence.
- Do not mix scopes unless explicitly requested.
- Call out assumptions (for example inferred base branch).
- Prefer concrete file references over vague statements.
- If no changes are found for the selected scope, state that explicitly.

## Useful commands

```bash
# unstaged
git diff

# staged
git diff --cached

# all uncommitted
git diff && git diff --cached && git status --porcelain

# branch-wide
git diff origin/main...HEAD

# PR-wide (if gh is available)
gh pr view --json baseRefName,headRefName,number,title
gh pr diff
```
