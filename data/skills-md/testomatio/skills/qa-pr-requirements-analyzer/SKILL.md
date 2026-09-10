---
name: qa-pr-requirements-analyzer
description: Analyze a pull request's context - title, description, comments, linked issues, attached schemas/images — to understand the original intent, verify scope against the linked ticket, surface ambiguities and edge cases, and produce a structured requirements summary with testable acceptance criteria. Use this skill when the user wants to understand WHAT a PR is supposed to do (not just what code changed), check whether the PR matches its linked ticket/task or generate acceptance criteria from PR/ticket context rather than from code.
license: MIT
metadata:
  author: Testomat.io
  version: 1.1.0
---

# QA PR Requirements Analyzer

Reviews a pull request's human-written context — title, description, comments, linked tickets, attached images — to extract the original requirements, verify scope, and produce a requirements summary that downstream skills (`qa-write-test-cases`) can consume.

Complement of `pull-request-diff-analyzer`:

| Skill | Input | Output | Focus |
|-------|-------|--------|-------|
| `pull-request-diff-analyzer` | git diff, changed files | AC from code changes | "what the code does" |
| `qa-pr-requirements-analyzer` | PR title, description, comments, linked issue | summary of requirements with scope verification, AC | "what the PR is supposed to do" |

- Use them together for a full picture.
- If the user only wants to know what code changed, use `pull-request-diff-analyzer` instead.

## Step 1: Detect PR Context

Accept, in priority order:
1. A PR number or URL from the user prompt (e.g. `https://github.com/org/repo/pull/1234`).
2. The open PR for the current branch: `gh pr view --json number,title,baseRefName,headRefName,url`.
3. A ticket key only (Jira `PRJ-123`, Linear, etc) — analyze the ticket, then check for any open PR referencing it.

- If none are detectable, ask the user for a PR number/URL, branch name, or ticket key.
- If the branch exists only locally, ask the user to push it or provide the PR details directly.

## Step 2: Read PR Context

Collect what the developer and team wrote — not the code. Detect available MCP/CLI tools and pull:
- PR metadata (title, description, comments, labels, milestone, assignees) — via Jira/Linear/GitHub MCP if enabled, else `gh` CLI.
- Embedded images/diagrams in the body — read them (vision-capable agent or `fetch` + describe); they often capture UI changes, error states, or flows that text misses.
- Linked tickets — parse the PR body and branch name for ticket references.

**Do not fabricate ticket content or add incorrect information.**

## Step 3: Resolve Linked Tickets

The PR description is often a thin summary; the ticket has the real requirements. Use the first available tool:

1. Jira/Linear MCP if enabled — fetch issue summary, description, AC, comments, linked issues, attachments.
2. GitHub MCP if enabled — fetch the linked issue.
3. `gh` CLI fallback — `gh issue view {N} --json title,body,comments,labels`. For Jira/Linear without an MCP, ask the user to paste the issue content.
4. No access — note the gap explicitly in the output and continue with what you have.

## Step 4: Verify Scope and Detect Ambiguities

Compare what the PR does against what the ticket asked for. These are questions to raise, not assertions that the code is wrong.

Scope verification — build three lists:
- In scope — ticket requirements addressed by the PR (description or code, see Step 5).
- Out of scope — ticket requirements with no corresponding PR change. These are the most valuable output of this skill.
- Extra (not in ticket) — PR changes not mentioned in the ticket. Flag for review (intentional or accidental?).

Ambiguities, edge cases, open questions — surface only issues supported by the available context. **Do not invent new requirements** or assume the product should handle a scenario unless the ticket, PR description, comments, or surrounding context suggest it is relevant. Look for:
- Underspecified behavior — the ticket describes a capability but omits important details (e.g. export is required, but format, naming, permissions, or empty-state behavior are not defined).
- Unanswered comments — questions in PR or ticket comments with no visible resolution.
- Conflicting requirements — different parts of the ticket, comments, or PR description disagree.
- Potentially relevant edge cases — scenarios related to the stated requirements whose expected behavior is not specified. Present these as questions, not requirements.
  - **Never report an edge case solely because it is a common software concern.**
  - Only raise an edge case when the ticket, PR description, affected domain, or discussion suggests it may be relevant.

## Step 5: Identify Affected Files

Do not do a deep code review — that is `pull-request-diff-analyzer`. Prefer files mentioned in the PR description or ticket; cross-check with `git diff {base}...HEAD --name-only` only if the description doesn't enumerate them.

**Short-circuit (no source behavior):** if every changed file is non-source (`*.md`, `docs/**`, `tests/**`, configs, CI, deps, lock files):
- Do not invent AC. Do not invoke `pull-request-diff-analyzer`.
- Produce a short summary: PR title, type (`docs`/`chore`/`ci`/`deps`), one-sentence `Changes`, full file list.
- Add the note `> No source code behavior changed. Acceptance criteria generation is not applicable for this PR.`
- Stop here.

**Empty PR description:** if there is no body and the branch name doesn't encode intent:
- Pull `git log {base}..HEAD --pretty=format:"%s%n%b"`.
- Combine with changed files and branch name into a tentative one-sentence `Changes`.
- Mark `> PR description was empty. Summary derived from branch name, commits, and changed files only.`
- If a linked ticket exists, prefer the ticket as source of truth and note the empty body under "Ambiguities".

## Step 6: Generate the Requirements Summary

**Save to a `.md` file only if the original prompt explicitly requests saving.** Write it to the user-specified folder.

Filename: slugify the PR title (lowercase, dashes, no special chars, max 40 chars), append the PR number. Example: `Add user export to CSV` → `add-user-export-to-csv-pr-1234.md`.

Output template (filled example: [summary-example.md](./references/summary-example.md)):

```md
## PR Requirements Summary

**PR:** {title}
**Branch:** {headRefName} → {baseRefName}
**Type:** {feature | bugfix | refactor | deps}
**Linked Tickets:** ... (only if any exist)

**Source of Truth:**
- PR description: {present | empty — derived from commits/branch}
- Jira/GitHub ticket: {resolved | not resolved — no MCP available}
- Most reliable source: {PR description | ticket | commits}

**Changes Overview:** ... (1-2 sentences — intent, not implementation)

**Impacted Areas:**
- Payment processing (6 source files)
- Billing configuration (2 config files)
- ... (bullet list, only meaningful business/technical impact; omit if empty)

**High Level Key files (up to 5):**
- `path/to/file.ts` — source
- ... (categorized: source | config | test | docs | migration | deps)

**Scope Verification:**
- ✅ In scope: {ticket requirement → where in PR it is addressed}
- ⚠️ Out of scope: {ticket requirement not addressed in PR}
- ➕ Extra (not in ticket): {change present in PR but not in ticket}

**Ambiguities, Edge Cases & Open Questions:**
- ... (underspecified behavior / unanswered comment / conflicting requirement / missing edge case)
- ... (empty input / permissions / error path / performance / backward compatibility / ...)
- ...

**Acceptance Criteria:**
- {action to perform} → {expected result}
- ...
```

Summary rules:
- Concise, high-level, requirements-not-implementation — this is a requirements document, not a code review.
- `Changes Overview` is 1-2 sentences.
- `Impacted Areas` — meaningful bullets; omit the section if empty.
- `Source of Truth` is required — tells downstream skills what to trust when sources disagree.
- `Acceptance Criteria` — testable, user-oriented, written as "action → expected result". If no source-code behavior changed, replace this section with the explicit "not applicable" note from Step 5.
- Omit empty sections instead of writing `None`/`N/A` — except the "no source code changed" note, which must be explicit.
- Avoid generic statements like "code cleanup", "minor fixes", "various improvements" — name what changed or omit it.

## References

| Description | File |
|-------------|------|
| Filled example of the output summary | [summary-example.md](./references/summary-example.md) |
| `.testeiya/` directory convention | `../scan-automation-project/SKILL.md` |
| Code-focused PR analysis (companion skill) | `../pull-request-diff-analyzer/SKILL.md` |
| Downstream: generate test cases from requirements | `../qa-write-test-cases/SKILL.md` |
| Downstream: sync generated cases to Testomat.io | `../sync-test-cases-with-tms/SKILL.md` |
