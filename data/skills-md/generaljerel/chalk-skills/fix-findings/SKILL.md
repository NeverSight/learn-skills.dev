---
name: fix-findings
description: Fix findings from the active review session — reads reviewer findings files, applies fixes by priority, and updates the resolution log. Use after pasting reviewer output into findings files.
owner: chalk
version: "1.0.0"
metadata-version: "1"
allowed-tools: Bash, Read, Edit, Grep, Glob, Write
argument-hint: "[reviewer-name|all] e.g. codex, gemini, gpt4, or omit for all"
---

# Fix Review Session Findings

Read findings from the active review session and apply fixes to the codebase, then update the resolution log.

## Step 1: Resolve the active session

Look for the current session:

1. Check `.chalk/reviews/.current-session`
2. If not found, check for the most recent session directory under `.chalk/reviews/sessions/`
3. If nothing found, stop and tell the user to run `/create-review` first to start a session

Store the session ID as `{session}`.

## Step 2: Determine which findings to load

Based on `$ARGUMENTS`:

- If a reviewer name is provided (e.g. `codex`, `gemini`, `gpt4`, `claude`), sanitize it to kebab-case and load only `.chalk/reviews/sessions/{session}/{reviewer}.findings.md`
- If `all` or no argument → load all `*.findings.md` files in the session directory

Discover available findings dynamically using the Glob tool:

```
.chalk/reviews/sessions/{session}/*.findings.md
```

Do NOT use shell `ls` for discovery — use the Glob tool to avoid command injection and handle special characters safely.

If a findings file doesn't exist or contains only template placeholder text, skip it and note that no findings are available from that reviewer.

If no findings are available from any reviewer, stop and tell the user to paste reviewer output into the findings files first. Show the expected path: `.chalk/reviews/sessions/{session}/{reviewer-name}.findings.md`

## Step 3: Parse findings

From each findings file, extract the findings table. Each row typically has:

- **ID** — finding identifier (e.g. `F-001`, `G-001`, or any prefix)
- **Severity** — `P0`, `P1`, `P2`, `P3`
- **File:Line** — source location (e.g. `src/main/auth.ts:172`)
- **Issue** — description of the problem
- **Failure mode** or **Impact** — what goes wrong
- **Recommended fix** or **Suggested fix** — how to fix it
- **Confidence** — reviewer confidence score (if present)

Sort all findings across all reviewers by severity: P0 > P1 > P2 > P3.

Deduplicate findings that target the same file and line (or overlapping line range) across reviewers. Two findings are duplicates if they reference the same file path AND the same line number (or lines within 5 of each other) AND describe a similar category of issue. When deduplicating, keep all IDs, use the more detailed description, and note both reviewers as sources.

## Step 4: Present findings and get confirmation

Before applying any fixes, present the user with a prioritized summary:

| Priority | ID(s) | Source | File:Line | Issue (1-line) | Action |
|----------|--------|--------|-----------|----------------|--------|
| P0 | G-001 | gemini | src/main/auth.ts:31 | Plaintext token storage | Fix |
| P1 | F-001 | codex | src/main/index.ts:182 | Stale auth target | Fix |
| ... | ... | ... | ... | ... | ... |

Ask the user which findings to fix. Options:
- **All** — fix everything P0-P2 (skip P3 unless trivial)
- **Blocking only** — fix P0 and P1 only
- **Let me choose** — user picks specific finding IDs

## Step 5: Apply fixes

For each finding to fix (in priority order):

1. **Validate the file path** — confirm the path is relative and within the repository root. Reject any absolute paths or paths containing `..` that escape the repo
2. **Read the file** at the specified path and line — read at least 30 lines of surrounding context (15 above, 15 below) to understand the code structure
3. **Design the fix** using the reviewer's suggested fix as guidance, but verify it makes sense in context
4. **Show the proposed fix to the user and ask for explicit confirmation before applying it**
5. **Apply the fix** using Edit tool
6. **Verify** the fix doesn't break surrounding code or introduce new issues

Rules:
- Do NOT blindly copy suggested fixes — they're guidance, not exact patches
- If a fix requires changes across multiple files, make all related changes together
- If a fix is unclear or would require significant refactoring beyond the finding's scope, skip it and mark as `deferred` in the resolution log
- For P3 findings: only fix if the change is a single-line or obvious one-liner (e.g. rename, add a null check, fix a typo). Otherwise skip
- After fixing deduplicated findings, note all IDs as resolved

## Step 6: Update the resolution log

Write or update `.chalk/reviews/sessions/{session}/resolution.md`.

If the file already exists, preserve any metadata comments at the top. Fill in:

```markdown
# Finding Resolution Log

## Summary
- Session: {session}
- Item: {inferred from session name}
- Reviewers: {list of reviewer sources found — e.g. codex, gemini}
- Decision owner:

## Findings

| ID | Severity | Source | File:Line | Decision | Notes |
|---|---|---|---|---|---|
| G-001 | P0 | gemini | src/main/auth.ts:31 | fixed | Wrapped token persistence with safeStorage |
| F-001 | P1 | codex | src/main/index.ts:182 | fixed | Rebind auth target in createWindow |

Decision values:
- fixed
- accepted-risk
- deferred
- not-repro

## Follow-up Tasks
- {deferred work, test gaps, items needing manual verification}

## Final Gate
- Build:
- Tests:
- Ready to merge: yes/no
```

## Step 7: Summary

After all fixes are applied, show:

1. A results table:

| ID(s) | Severity | Source | Status | What was done |
|--------|----------|--------|--------|---------------|
| G-001 | P0 | gemini | Fixed | Wrapped token persistence with safeStorage |
| F-001 | P1 | codex | Fixed | Rebind auth target in createWindow |
| G-004 | P3 | gemini | Skipped | Trivial but not blocking |

2. The resolution log path
3. Suggest next steps:
   - Run build/tests to verify nothing broke
   - Run `/commit` to commit the fixes
   - If all blocking findings are resolved, create or update the PR

## Rules

- ALWAYS validate that file paths from findings are relative and within the repository root — reject absolute paths or paths with `..` escaping the repo
- ALWAYS read the file with surrounding context before applying any fix
- Do NOT modify files that aren't referenced in findings
- Do NOT fix things that aren't in the findings — stay scoped
- If multiple reviewers suggest conflicting fixes for the same issue, present both suggestions to the user and let them choose which approach to take
- Keep fixes minimal — address the finding, don't refactor surrounding code
- If build or typecheck breaks after a fix, attempt to resolve but note it in the resolution log
