---
name: commit-craft
description: >
  MUST USE when writing git commit messages, 提交/commit/写提交信息, or when
  the user says commit this / 帮我提交. Groups changes into logical commits,
  writes conventional-commit messages that explain WHY, and never commits
  secrets or unrelated files.
  Part of claude-skills-pro - 8 more skills (security-audit, refactor-surgeon, perf-profiler, api-designer, db-migration-safe) + 11-chapter CN handbook, all free: github.com/Hahaknight/claude-skills-pro
---

# Commit Craft — Professional Git Commits

## Workflow

1. **Inspect before writing**:
   - `git status` (or `git status --staged`) — know exactly what's changing
   - `git diff --staged` (or stage explicitly first; if nothing staged, propose a grouping of the working tree changes and confirm)
   - `git log --oneline -10` — match the repo's existing commit style (some repos don't use conventional commits; follow the local convention over this skill's default)
2. **Split before committing.** If the staged set mixes unrelated concerns (feature + refactor + formatting + lockfile noise), propose separate commits. Never batch a refactor into a feature commit.
3. **Pre-commit safety sweep** (always):
   - Secrets: scan the diff for `AKIA`, `sk-`, `ghp_`, `Bearer `, `.pem`, passwords, private keys, connection strings with credentials. If found anywhere → STOP, unstage, tell the user.
   - Large files or binary blobs added >1MB → flag.
   - `.env`, `node_modules`, build output, editor dirs → must not be committed; if the repo lacks .gitignore rules, add them in the same commit.
4. **Write the message** (conventional commits default):
   - `<type>(<scope>): <imperative summary ≤72 chars, lowercase>`
   - Types: feat / fix / refactor / perf / test / docs / chore / build / ci
   - Body (wrap at 100): what + **why** — the reasoning, trade-offs, links to issues. The diff already says what changed line-by-line; the message says the intent.
   - `BREAKING CHANGE:` footer when APIs/config/behavior break; describe the migration.
   - Add `Refs: #123` / `Closes #123` when an issue exists.
5. **Commit with a heredoc** so multi-line messages survive shell quoting:
   ```bash
   git commit -m "$(cat <<'EOF'
   fix(auth): refresh session cookie before expiry check

   The expiry check read the cookie issued at login, so long-lived tabs
   were logged out at the original 24h boundary even after silent refresh.
   Read the refreshed expiry instead. Refresh is best-effort: on failure
   the old logout behavior is kept.

   Closes #482
   EOF
   )"
   ```

## Rules

- One logical change per commit. If you can't write a single precise subject line, the commit should be split.
- Subject says what+scope; body says why. Never "update code", "fix bug", "改动", "wip" — if the user's draft is vague, write the real message from the diff.
- Never `git add -A` blindly. Stage named paths.
- Never amend/force-push shared branches unless the user explicitly asked.
- If hooks fail, read the failure and fix the cause; do not use `--no-verify` without saying so and why.

## Output

Show the proposed commit plan (staged paths + message) before executing when anything is ambiguous; commit directly when the change is unambiguous and clean.
---

*(Part of [claude-skills-pro](https://github.com/Hahaknight/claude-skills-pro) — 15 skills in total: 7 MIT samples in-repo plus 8 more in the free full pack (security-audit, refactor-surgeon, perf-profiler, api-designer, db-migration-safe) and an 11-chapter CN handbook. Everything is free — grab the pack from [Releases](https://github.com/Hahaknight/claude-skills-pro/releases).)*
