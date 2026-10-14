---
license: MIT
name: pr-title-lint
description: >
  Add or verify CI enforcement of Conventional Commits pull request titles.
  Detects whether the repo squash-merges with the PR title as the commit
  subject, checks for an existing title check, scaffolds
  `.github/workflows/pr-title.yml` using amannn/action-semantic-pull-request
  at a pinned SHA, and verifies it fails a bad title and passes a good one.
  Use when the user says enforce conventional commit PR titles, lint PR
  titles, semantic pull request check, add a PR title check, or invokes
  /pr-title-lint. Do NOT use for switching a repo to squash-merge with
  PR-title commit messages (use gh-bootstrap for merge defaults and
  rulesets), cutting a release (use release), or local commit-message
  hooks (use prek).
---

# pr-title-lint

Scaffold a CI check that rejects a pull request title that does not follow
[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

This matters most when squash merge uses the PR title as the commit subject:
an unchecked title becomes permanent history the moment the PR merges.

## Where this fits

| Concern | Skill |
|---|---|
| Switch a repo to squash-only with PR-title commit messages | `gh-bootstrap` |
| Enforce the PR title format itself, in CI | **`pr-title-lint`** (this skill) |
| Add the check name to required status checks on a ruleset | `gh-bootstrap` |
| Cut a versioned release | `release` |
| Local commit-message hooks (commitlint via prek) | `prek` |

## Protocol

### 1. Detect squash-merge with PR-title commit messages

```bash
REPO="$(gh repo view --json nameWithOwner --jq '.nameWithOwner')"
gh api "repos/$REPO" --jq '.squash_merge_commit_title'
```

A value of `PR_TITLE` means the squash commit subject is the PR title
verbatim, so `git log --oneline` on the default branch becomes a list of PR
titles. An unchecked title turns a typo, a missing type, or a vague summary
into permanent history the moment the PR merges. This is the strongest
reason to add the check; still offer to scaffold it if the value is
`COMMIT_OR_PR_TITLE` or unset, since the title can still land as history.

### 2. Detect an existing check

```bash
grep -rl 'action-semantic-pull-request' .github/workflows/ 2>/dev/null
grep -rl 'commitlint' .github/workflows/ .commitlintrc* commitlint.config.* 2>/dev/null
```

If a workflow already runs `action-semantic-pull-request` against PR titles,
or a commitlint job already lints PR titles (not just commit messages), stop
and report it instead of adding a duplicate check.

### 3. Scaffold the workflow

Copy [`assets/pr-title.yml`](assets/pr-title.yml) to
`.github/workflows/pr-title.yml`. It pins
`amannn/action-semantic-pull-request` by commit SHA (not a floating tag), and
ships with:

- `permissions: pull-requests: read` — least privilege; the action only
  needs to read the PR title
- `on.pull_request.types: [opened, edited, synchronize, reopened]` — reruns
  the check whenever the title or the PR itself changes
- `merge_group` trigger with a job-level
  `if: github.event_name == 'pull_request'` — the job validates the title
  only on the PR, because a merge group event has no PR title; on
  `merge_group` the job is skipped, and a skipped job reports success
- Commented-out `types` and `scopes` lists, and a `subjectPattern` example,
  for the user to uncomment and tailor
- `requireScope: false` — most repos do not need a mandatory scope

Ask before overwriting an existing `.github/workflows/pr-title.yml`; show
the diff first.

See [`references/conventional-commits.md`](references/conventional-commits.md)
for the full Conventional Commits summary, the squash-merge citations, and
the action's configuration options.

### 4. Optional: commit-message linting via prek

If the user also wants to lint local commit messages (not just PR titles),
that is a `commit-msg` hook, not a GitHub Actions job. Point them at `prek`
and offer [`assets/commitlint.config.example`](assets/commitlint.config.example)
as a starting config for prek to wire in.

### 5. Make it required (optional, needs authorization)

Adding `pr-title-lint`'s check name to a ruleset's required status checks is
`gh-bootstrap`'s job, not this skill's. Hand off to `gh-bootstrap` for that
step, and require explicit user authorization before any ruleset write —
never add a required check to a live ruleset without asking first.

Before the check becomes required, tell the user about merge queues. If the
branch uses a merge queue, GitHub waits for each required check on the
`merge_group` event. A workflow without a `merge_group` trigger never
reports that check. The queue waits for the check, then drops the PR,
and the merge fails. Keep the `merge_group` trigger
and the job-level `if` from the template. If the user removed the trigger,
add it back before the check becomes required. Sources:
[Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue#triggering-merge-group-checks-with-github-actions)
and
[Handling skipped but required checks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/troubleshooting-required-status-checks#handling-skipped-but-required-checks).

### 6. Verify

Open (or ask the user to open) a pull request with a title that does not
match Conventional Commits, such as `updated stuff`, and confirm the
`pr-title` check fails with a clear error. Then retitle the PR to something
like `fix: correct typo` and confirm the check turns green.

## What this skill is NOT for

- Configuring squash-only merging or `squash_merge_commit_title` — `gh-bootstrap`
- Adding the check name to a ruleset's required status checks — `gh-bootstrap`
- Cutting or publishing a release — `release`
- Local pre-commit or commit-message hooks — `prek`
