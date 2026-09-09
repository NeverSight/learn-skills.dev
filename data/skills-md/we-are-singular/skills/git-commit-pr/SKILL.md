---
name: git-commit-pr
description: Use when preparing local changes for commit, push, and pull request creation, especially in repositories that use conventional commits, package/workspace scopes. This skill optimizes for clean history, package-scoped commits, repository-specific rules, and a PR body that explains intent.
---

# Git Commit PR

Use this skill to take a working tree from local changes to an intentional pushed draft PR. Optimize for clean history, package-scoped commits, repository-specific rules, and a PR body that explains intent.

Command examples in this skill describe the intended effect. If the environment provides reliable Git or GitHub tooling through an IDE, app, connector, or other integration, use that tooling to perform the same checks, staging, commits, pushes, and PR operations instead of forcing the `git` or `gh` CLI.

## First Read The Repo

Before staging or committing, inspect local conventions:

```bash
git status --short
git branch --show-current
git remote -v
git log --format='%h %s' -n 30
```

Look for:

- Commit rules: `commitlint.config.*`, package manager workspace config (e.g., `pnpm-workspace.yaml`, `package.json` workspaces, `.code-workspace`), `.github/instructions/*`, `AGENTS.md`, `CLAUDE.md`.
- Hooks: `.husky/pre-commit`, `.husky/commit-msg`, `.husky/pre-push`, `lint-staged`, `pretty-quick`.
- PR rules: `.github/pull_request_template.md`, `.github/prompts/*pr*`, existing merged PR bodies when available.
- Default base branch: prefer `main`, but verify from local branch/upstream context.

Local repo rules win. Use this skill's defaults only when the repo is ambiguous.

## Safety Gate

Do not run broad staging commands until every changed path is understood.

Flag and ask before committing:

- Secrets, credentials, `.env` files, tokens, keys, certs, or copied production data.
- Logs, dumps, screenshots, archives, local scratch files, generated reports, or one-off test artifacts.
- LLM planning docs, handoff notes, temporary markdown, or example files created only to prove an approach.
- Unrelated files, editor metadata, lockfile churn without dependency changes, or generated files with unclear source.
- User-curated staged changes that would need to be reorganized.

Use exact paths and hunks. Prefer `git add -p` or explicit `git add path/to/file` over `git add .`.

## Branches And Linear History

Keep history linear. Rebase everywhere; do not merge `main` into a feature branch.

Preferred branch names:

```text
codex/ticket-123-feature-title
username/ticket-123-feature-title
claude/feature-title
feature/feature-title
fix/bug-title
```

The prefix can be the person or agent doing the work (`codex`, `claude`, `opencode`, a username). Ticket branches are best when a ticket exists.

Before final push:

```bash
git fetch origin
git rebase origin/main
```

If the branch was already pushed and rebase rewrote commits, use:

```bash
git push --force-with-lease
```

Never use plain `--force` for this workflow without consulting the user first. request explicit confirmation.

## Commit Shape

Prefer several focused commits over one large feature commit. Group by package/workspace and feature boundary, not by every tiny file change.

Bad:

```text
feat(frontend): feature a
```

Better:

```text
feat(db): add webhook delivery tables
feat(api): add webhook delivery routes
feat(frontend): add webhook management screens
test(frontend): cover webhook filters
```

If one feature touches five packages, usually make five package-scoped commits. Keep tightly coupled files together when separating them would make the history misleading or unbuildable.

## Commit Message Rules

Use the repo's configured type and scope rules. Common Singular-style default:

```text
type(scope): subject
```

Common types:

```text
build ci tools docs feat feature fix perf refactor design style test release
```

Prefer conventional `feat` for new features. Accept `feature` as a fallback/alias when the repository allows it. Use `tools` or `build`, not `chore`, unless the repo explicitly allows `chore`.

If changelog or semantic-version tooling reads commit types, verify that an allowed `feature` alias maps to the same release behavior as `feat`. Keep generated examples on `feat` unless that mapping is proven.

Scope should identify the package, workspace, app, or root area changed. Derive valid scopes from the repo's workspace package names (e.g., `package.json` workspaces, `pnpm-workspace.yaml`, `.code-workspace`), `commitlint.config.*`, or `git log`. When unsure, the commit hook will reject invalid scopes and report which are allowed.

Some types do not require a scope: `build`, `ci`, `docs`, `tools`, `style`. These are often cross-cutting and a scope is optional. For all other types, scope is required. Use `root` when changes are truly cross-cutting and no single package applies.

```text
feat(api): add request audit events
fix(ui): align dropdown keyboard behavior
refactor(db): simplify mailbox repository filters
test(packages/db): cover publication transitions
fix(@base/utils): preserve query string arrays
docs: update local setup notes
build: upgrade turbo to v2
tools: add pre-push hook
```

Some repos use short scopes like `db`, `ui`, `api`, `frontend`. Stricter repos may require full workspace scopes like `packages/db`, `apps/frontend`, or `@base/db`. Use the repo's convention. If the repo is ambiguous, prefer more specific scopes that identify the package or workspace, not just a broad area.

Subjects should be lowercase imperative, concise, and have no trailing period:

```text
feat(frontend): add saved view filters
fix(api): reject missing webhook signatures
```

Ticket prefixes are acceptable when the repo allows them:

```text
feat(frontend): TICKET-123 add saved view filters
fix(packages/db): ISSUE-456 preserve queue ordering
```

## Staging Pipeline

1. Inspect all changes.

```bash
git status --short
git diff --name-status
git diff --stat
```

2. Build a commit plan.

Group paths by package/workspace and behavior:

```text
Commit 1: packages/db schema and repository changes
Commit 2: apps/api routes and service wiring
Commit 3: apps/frontend UI and query hooks
Commit 4: focused tests for the changed packages
```

3. Stage only the first group.

```bash
git add packages/db/src/webhooks.ts packages/db/test/webhooks.test.ts
git diff --cached --stat
git diff --cached
```

4. Commit that group.

```bash
git commit -m "feat(db): add webhook delivery persistence"
```

5. Repeat for each group.

After each commit, return to:

```bash
git status --short
```

If hooks fail, fix the issue, restage only the affected group, and retry the same commit. Do not bypass hooks unless the user explicitly asks and understands the tradeoff.

## Validation

Before committing, run at least lint and tests for the packages/workspaces that changed. Pushing broken lint or tests wastes reviewer and CI time. If this skill is loaded into a session where the relevant checks already ran and passed for the current changes, do not repeat them just to satisfy the workflow.

Use the repo's package manager commands (e.g., `npm run lint`, `npm run test`, `pnpm lint`, `pnpm test`). Do not invoke linters or formatters directly — the repo's scripts know which tools to use (oxlint, eslint, prettier, biome, etc.).

If the repo has absolutely no linting, testing, or build scripts, you can use `npx prettier -w FILENAME`, some default formatter is better than nothing.

We want to avoid pushing commits that fail lint, tests, formatting, build, or commit message rules. These are usually easy to fix locally and can cause friction for reviewers and CI if pushed. Keep an open communication with the user about what checks are being run and why.

Prefer package-scoped checks first, then broader checks when the blast radius justifies it.

Examples:

```bash
npm run test --workspace=@repo/db
npm run lint --workspace=apps/frontend
npm run build
```

If `pre-push` runs expensive checks (e.g., lint + test + build), mention that before pushing so the user is not surprised. If a relevant check cannot be run, say why in the PR draft.

## Troubleshooting

### If a commit hook fails, due to lint, test, formatting, or commit message errors:

1. Read the hook logs to understand the failure.
2. Fix the underlying issue in the code, not just the symptom.
3. The more runs we can do locally before pushing, the less likely we are to waste reviewer and CI time.
4. After fixing, restage only the affected files and retry the same commit command.

Its usually best to fix the real issue and retry the same commit, rather than bypassing the hook or creating a new commit that hides the issue. This keeps history clean and avoids pushing broken commits.

### If lint-staged or formatter hooks changed files:

Some repos run `lint-staged`, `pretty-quick`, Prettier, ESLint/Biome fixes, or similar staged-file formatters in `pre-commit`. These hooks may modify files and then reject the commit until the modified files are staged again.

When that happens:

1. Read the hook output to identify the command that ran.
2. Inspect the resulting changes with `git diff` and `git diff --cached`.
3. Make sure the formatter did not touch unrelated files.
4. Restage only the intended formatted files.
5. Retry the original commit.

```bash
git diff -- path/to/file.ts
git add path/to/file.ts
git commit -m "feat(frontend): add saved view filters"
```

If the repo exposes a staged-file fix command, prefer that over calling tools directly:

```bash
npm run lint-staged
npx lint-staged
npx pretty-quick --staged
```

Use the command named by the repo's scripts or hook output. Do not assume every repo uses the same staged-file tool.

### If push fails because a hook rejected the branch:

1. Read the hook logs. It is usually a lint, typecheck, test, formatting, or commit message error.
2. Fix the real issue instead of bypassing the hook.
3. Run the relevant package checks again.
4. Decide whether to amend or create a follow-up commit.

Amend only when it is safe:

- The fix belongs to the last commit.
- The branch has only one commit.
- The branch has not been pushed, or rewriting it with `--force-with-lease` is expected and safe.

```bash
git add path/to/fixed-file.ts
git commit --amend
```

Create a new focused commit when the fix spans earlier commits, the branch history is already shared, or amending would hide a distinct correction:

```bash
git add path/to/fixed-file.ts
git commit -m "fix(frontend): resolve lint failures in saved views"
```

Avoid vague commits like `fix lint`. Mention the affected scope and behavior.

## PR Draft

Before drafting the PR body, gather the actual branch diff:

```bash
git branch --show-current
git status
git --no-pager log --oneline main..HEAD
git --no-pager diff main..HEAD
```

Start with the ticket relationship when known:

```text
closes TICKET-123
```

or:

```text
related to TICKET-123
```

Use the repo's PR template. A strong default, at the end of the PR body, write an original haiku in blockquotes that summarizes the specific change and intent of this PR.

```markdown
closes TICKET-123

## Description

<!--- Template hint only. Replace comments with final prose before publishing. What changed? Why does it matter? -->

## What changed?

<!--- Template hint only. Replace comments with final prose before publishing. Bullet list or brief summary of the main code changes, UI, API, workflow changes, and blast radius. -->

<!--- Template hint only. Remove this comment before publishing. Optional `## Why`: add before Verification only when the reason is not obvious from the code, using context from this chat, docs, plans, issues, commits, or the diff. -->

## Verification

<!--- Template hint only. Replace comments with final prose before publishing. Brief sentence bullets only. Capture the reviewable verification effort and manual-test path, not intrinsic CI hygiene like npm test/lint/build commands. Include where to see or feel the change locally when useful. -->

> Clean commits tell truth
> Rebase keeps history linear
> Push only what's right
```

Keep the PR body slim:

Before showing or publishing the final PR body, remove every template hint and HTML comment. The final body should contain only reviewer-facing prose, bullets, links, images/logs when useful, and the PR-specific haiku.

- `## Why` is optional. Include it only when the branch carries decision context that a reviewer cannot recover from code alone. Source it from the current chat, repo docs, plans, issues, commit messages, or the diff itself. Do not use it to restate what changed.
- `## Verification` should be a short bullet list of sentences describing the verification effort that makes the change reviewable: exercised flows, scenarios checked, evidence inspected, and how or where a reviewer can manually see the feature.
- Do not list intrinsic hygiene commands such as npm test, npm lint, npm build, turbo checks, or pre-push hooks in the PR body. Those are assumed to have been run and belong in the confirmation/handoff notes when useful, not in `## Verification`.
- Each verification bullet should be concrete and brief, for example:
  - Clicked Buy, then confirmed the order appears in wallet history.
  - Used the browser to assert the new badge and spacing match design.
  - Asserted the order id is present in the API response.
  - Checked the export file size stays under the limit.
  - Visit `/wallet/movements` locally and deposit test funds to see the new movement row.

For UI work, include real screenshots or screen recordings when available. For backend/tooling work, include real command output or logs only if captured from the branch and useful to reviewers. Do not invent preview output. Omit optional sections when there is nothing useful to show.

## Confirm Before Push

When all commits are ready, show the user:

- Branch name.
- Commit list from `main..HEAD`.
- Validation run and result.
- Draft PR title and body.

Ask for confirmation before pushing. If the runtime provides a structured user-question tool, use it here instead of printing a plain-text choice list. Examples include Codex `request_user_input`, Claude Code `AskUserQuestion`, Cursor `cursor/ask_question`, and OpenCode `question`.

Offer these choices, with push first and marked as the recommended/default option so the user can usually approve by pressing Enter:

```text
1. Push it!
2. Request changes to the commit plan or PR body
```

If no structured question tool is available, ask with the same choices in plain text.

Do not push or create the PR until the user clearly confirms.

## Push And Open Draft PR

After confirmation:

```bash
git fetch origin
git rebase origin/main
git push -u origin HEAD
```

Create a draft PR with the GitHub CLI when available:

```bash
gh pr create --draft --base main --head "$(git branch --show-current)" --title "feat(api): add webhook delivery management" --body-file /tmp/pr-body.md
```

If `gh` is unavailable, still push the branch, then print the PR title, PR body, and any PR creation URL emitted by `git push` so the user can create it manually.

If a PR already exists, update it instead of creating a duplicate:

```bash
gh pr view --web
gh pr edit --body-file /tmp/pr-body.md
```
