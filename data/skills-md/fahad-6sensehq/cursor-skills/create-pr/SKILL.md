---
name: create-pr
description: >-
  Create pull requests with Conventional Commits titles, Jira traceability, a
  hard 200-line DORA change budget, and full stack work reports on tip PRs.
  Use when the user asks to create a PR, open a PR, draft a PR, write a PR title
  or body, generate a PR description, or run gh pr create.
---

# Create PR

Team/shared, project-agnostic playbook for opening pull requests.

Examples: [examples.md](examples.md)

## Hard rules

1. **Max 200 changed lines** (insertions + deletions) vs the PR base. Hard gate before `gh pr create`.
2. If size **> 200**, stop. Report the shortstat, suggest split slices, and do **not** open the PR unless the user explicitly overrides.
3. **Title** must be Conventional Commits + Jira key: `type(scope): imperative summary (PROJ-1234)`.
4. **Never invent a Jira key.** Extract from branch name, commits, or chat. If missing, ask. Omit the Jira section only when the user confirms there is no ticket.
5. Commit subjects on the branch should already follow Conventional Commits. When committing in the same flow and a Jira key exists, put `Refs PROJ-1234` in the commit body.
6. Return the PR URL when done.
7. Stricter project docs (e.g. EasyGig Elite &lt; 100) win when that project process applies — still run this skill’s checks, then apply the tighter budget.
8. **Stack work report (stacked PRs):** when the tip layer is done, put a **full stack work report** on the **top** PR (every layer, review notes, test plan). Reviewers must not need to open lower PRs to understand earlier changes. If the stack already has a report and another layer is added, **rewrite the entire report on the new tip** — do not leave the old report on a lower PR as the source of truth.

## Title format

```
<type>(<optional-scope>): <imperative summary> (PROJ-1234)
```

- Types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `chore`, `build`, `ci`, `style`, `revert`
- Imperative mood: add / fix / remove — not added / fixes / removing
- Prefer ≤72 characters; no trailing period
- No Jira key → ask first; only then use title without `(PROJ-1234)`

## Body template (single PR)

Use this structure with `gh pr create` via HEREDOC when the PR is **not** part of a stack (or is the only PR):

```markdown
## Summary
- <1-3 bullets, why-focused>

## Jira
- Key: PROJ-1234
- Link: <browse URL if known>

## Test plan
- [ ] <checklist items>

## Size
- Changed lines vs <base>: N (budget 200)
```

Omit the **Jira** section only when the user confirmed no ticket.

## Body template (stacked tip PR)

When this PR is the **top of a stack**, replace/extend the body so the tip is the single source of truth:

```markdown
## Summary
- <why this stack exists — product/outcome focused>

## Jira
- Key: PROJ-1234
- Link: <browse URL if known>

## Stack work report
Full report for the entire stack. Reviewers should not need to open lower PRs.

### Layer 1 — <branch or PR title> (#N or URL)
- What changed
- Why
- Review notes / risks / follow-ups

### Layer 2 — <branch or PR title> (#N or URL)
- What changed
- Why
- Review notes / risks / follow-ups

### Layer N (tip) — <this PR>
- What this layer adds
- Why
- Review notes / risks / follow-ups

## Test plan
- [ ] <covers the whole stack, not only the tip layer>

## Size
- This PR vs its base: N (budget 200)
- Stack vs merge target (optional): M
```

### Stack report rules

1. Detect a stack when the PR base is another feature branch / open PR (not only `main`/`master`/`beta`), or the user says the work is stacked / `gh-stack` / dependent PRs.
2. Put the **full** report only on the **current tip** PR body.
3. When adding a new tip layer: rewrite the **entire** Stack work report on the new tip (all layers 1…N). Then trim or replace the previous tip’s body so it is no longer the report source of truth (short “Superseded: full stack report is on #NEWTIP” is enough).
4. Include every layer: summary of changes, review notes, and a **stack-wide** test plan.
5. Keep per-PR Size against that PR’s own base (still ≤200 unless overridden).

## Workflow

Copy and track:

```
PR Progress:
- [ ] 1. Gather context
- [ ] 2. DORA preflight (≤200)
- [ ] 3. Resolve Jira key
- [ ] 4. Detect stack / tip
- [ ] 5. Draft title + body (single or stack report)
- [ ] 6. Push if needed
- [ ] 7. gh pr create (or update tip body)
- [ ] 8. Return URL
```

### 1. Gather context (parallel)

- `git status`
- `git diff` and `git log` (branch vs base)
- `git diff --stat <base>...HEAD`
- Branch tracking / whether push is needed
- Infer base branch (`main`, `master`, `beta`, feature tip, or repo default) from tracking and user intent
- If stacked: list lower PRs (`gh pr list`, `gh pr view`, stack tool) so the report can cover every layer

### 2. DORA preflight (hard gate)

```bash
git fetch origin <base>
git diff --shortstat <base>...HEAD
```

Parse insertions + deletions. If total **> 200**:

- Report N and the file stats
- Suggest how to split (by layer, file group, or subtask)
- **Stop** unless the user explicitly says to override

Project-specific tighter budgets (e.g. &lt; 100) still apply when documented for that repo.

### 3. Resolve Jira key

From branch patterns such as:

- `EG-1234/feature-name`
- `PROJ-1234-feature-name`
- `feature/PROJ-1234-...`

Else from recent commit messages / chat. If still missing → ask.

When a browse URL is available (user, project config, or Atlassian MCP), put it under **Jira → Link**.

### 4. Detect stack / tip

- Single PR onto a shared trunk → use **Body template (single PR)**
- PR onto another feature PR/branch, or user asks for a stack report → use **Body template (stacked tip PR)** and gather notes for every layer

### 5. Draft title + body

- Title: Conventional Commits + `(PROJ-1234)`
- Body: single template or full stack work report on the tip
- Size line must match the preflight number for **this** PR vs its base
- When generating a PR description only (no create), still follow these templates

### 6–7. Push and create / update

Follow the user’s PR creation rules (`gh`, HEREDOC body, push `-u` if needed). For stack tip updates use `gh pr edit <n> --body ...` after rewriting the full report.

### 8. Return URL

Print the PR URL. Do not merge unless asked.

## Updating an existing PR

When the user asks to update title/body on an open PR, apply the same title, Jira, and body rules. Re-run the 200-line check against the PR base before claiming size is OK.

If the PR is (or becomes) the stack tip, rewrite the **full** Stack work report on that PR. Do not leave an older tip’s report as the source of truth.
