---
license: MIT
name: gh-bootstrap
description: >
  One-time GitHub repository configuration via the `gh` CLI: lock the default
  branch with PR and CI rules, optionally enable a supported merge queue, lock
  merging to squash-only with PR-title commit messages, scaffold
  automatically-generated release notes (`.github/release.yml`), and
  optionally add a tag-driven release workflow. Use when the user says
  "set up the repo", "configure the merge queue", "enable squash merging",
  "lock down main", "set up branch protection", "configure release notes",
  "scaffold releases", "set up release tagging", or invokes /gh-bootstrap
  on a fresh or loosely-configured GitHub repository. Idempotent — safe to
  re-run on already-configured repos to bring missing pieces in line.
  This skill covers one-time repo policy, not per-task GitHub
  operations, local git commands, or project task running.
---

# gh-bootstrap

One-shot repository configuration for the **merge-queue + squash-merge + auto-release-notes** pattern.

This is one-time repo policy, distinct from per-task GitHub operations: how should this repo be configured in the first place?

## What gets configured

| Concern | Result | Endpoint |
|---|---|---|
| Repo merge defaults | Squash-only; PR title → commit subject; delete branches on merge | `PATCH /repos/{owner}/{repo}` |
| Default branch protection | Ruleset with PR and required checks, no force-push, no deletion; optional queue | `POST /repos/{owner}/{repo}/rulesets` |
| Release notes | `.github/release.yml` with category buckets driven by PR labels | File commit |
| Release workflow (optional) | Tag push → `gh release create --generate-notes` on the discovered default branch | File commit |

All policy endpoints (repo settings, rulesets, branch protection) run through the `gh` CLI — `gh api` for the JSON endpoints, `gh repo`/`gh release` where there's a first-class subcommand. The skill writes files (`.github/release.yml`, the optional release workflow) directly to the working tree.

## Protocol

### 1. Confirm scope and inspect current state

Before changing anything, read the runway and confirm with the user:

```bash
gh auth status
REPO="$(gh repo view --json nameWithOwner --jq '.nameWithOwner')"
gh repo view "$REPO" --json nameWithOwner,visibility,defaultBranchRef,isPrivate
DEFAULT_BRANCH="$(gh repo view "$REPO" --json defaultBranchRef --jq '.defaultBranchRef.name')"
gh api "repos/$REPO" --jq '{
  squash:   .allow_squash_merge,
  merge:    .allow_merge_commit,
  rebase:   .allow_rebase_merge,
  delete:   .delete_branch_on_merge,
  title:    .squash_merge_commit_title,
  body:     .squash_merge_commit_message,
  auto:     .allow_auto_merge
}'
gh api "repos/$REPO/rulesets" # any rulesets already?

# Legacy branch protection: a 404 with "Branch not protected" means none
# exists. Any other error must stop the protocol before rulesets are applied.
if legacy_protection=$(gh api "repos/$REPO/branches/$DEFAULT_BRANCH/protection" 2>&1); then
  echo "$legacy_protection"
elif [[ "$legacy_protection" == *"HTTP 404"* && "$legacy_protection" == *"Branch not protected"* ]]; then
  echo "No legacy branch protection on $DEFAULT_BRANCH."
else
  echo "::error::Could not check legacy branch protection: $legacy_protection" >&2
  exit 1
fi
```

Ask the user:

- Default branch (assume the repo's `defaultBranchRef`, usually `main`)
- Required status check **names** (e.g. `validate / validate skills`, `ci`, `test`) — these must match what CI emits
- Required approving review count (default `1`; `0` is fine for solo repos)
- Whether to scaffold the optional release workflow, or just `.github/release.yml`

**Merge queue availability.** GitHub supports merge queues on public organization-owned repositories and on private organization-owned repositories with GitHub Enterprise Cloud. A user-owned repository, including a public user-owned repository, is not eligible. Skip the `merge_queue` rule unless the repository and plan meet those requirements.

### 2. Set repo merge defaults

Single `PATCH` lands all the merge-button settings atomically:

```bash
gh api -X PATCH "repos/$REPO" \
  -F allow_squash_merge=true \
  -F allow_merge_commit=false \
  -F allow_rebase_merge=false \
  -F allow_auto_merge=true \
  -F delete_branch_on_merge=true \
  -F squash_merge_commit_title=PR_TITLE \
  -F squash_merge_commit_message=PR_BODY
```

Why each flag:

- `allow_squash_merge=true`, `allow_merge_commit=false`, `allow_rebase_merge=false` — squash is the only button on a merged PR, so `main` history is one commit per merged PR.
- `delete_branch_on_merge=true` — the branch is gone anyway once it's been collapsed into one commit; no point keeping the ref.
- `squash_merge_commit_title=PR_TITLE` — the squash commit's subject line is the PR title verbatim. This makes `git log --oneline` on `main` read as a list of merged PRs.
- `squash_merge_commit_message=PR_BODY` — the PR body becomes the commit body, so the rationale for each change survives in `git log` without needing GitHub.
- `allow_auto_merge=true` — required for the merge queue button to enqueue PRs without human babysitting.

`PATCH` is idempotent: re-running with the same values is a no-op.

### 3. Lock the default branch with a ruleset

Rulesets are GitHub's modern replacement for branch protection — they support merge queues as a first-class rule, layer cleanly with org rulesets, and are queryable via the API. Default to a ruleset; only fall back to classic branch protection if the user explicitly asks (e.g. they are pinned to an older GHE version).

The full payloads, the asset templates, and the create-vs-update logic live in `references/ruleset.md` — read that file before this step. The no-queue variant ships as an asset:

| Variant | Asset | Pick when |
|---|---|---|
| `main: PR + CI` | `assets/rulesets/main-pr-ci.json` | Solo or small repo. Squash-only via `allowed_merge_methods: ["squash"]`, 0 required reviews, single CI check, no merge queue. |
| `main-protection` (queue) | inline JSON in `references/ruleset.md` | Team repo with concurrent PR throughput. Adds the `merge_queue` rule, ≥1 review, matrix of CI checks. |

Both variants share the same shape:

- `target: "branch"`, `conditions.ref_name.include: ["~DEFAULT_BRANCH"]`
- `enforcement: "active"`
- Rules: `deletion`, `non_fast_forward`, `pull_request`, `required_status_checks`

Default to the `main: PR + CI` variant unless the user explicitly asks for the merge queue. It's the simpler shape and the one that matches everyday solo work.

**Idempotency:** list rulesets and look for one targeting the default branch whose name matches either bootstrap variant (`main: PR + CI` or `main-protection`). If found, `GET` it, diff its `rules`, `bypass_actors`, and `conditions` against the rendered payload, show the diff, and ask the user before `PUT`-ing. When the user switches variants, reuse that ruleset's id for the `PUT` instead of creating a second one, and ask before disabling or retiring anything from the prior variant. If absent, `POST` a new one. Never create a duplicate ruleset for the default branch.

### 4. Scaffold the release-notes config

Copy `assets/release.yml` to `.github/release.yml`. This file is consumed by GitHub's auto-generated release notes (the "Generate release notes" button on the New Release page, and `gh release create --generate-notes`). It groups merged PRs into Breaking / Features / Fixes / Docs / Internal / Other buckets driven by PR labels.

If `.github/release.yml` already exists, diff it against the template and ask before overwriting. Don't silently clobber the user's existing categories.

### 5. Scaffold the release workflow (optional)

If the user opted in, copy `assets/release-workflow.yml` to `.github/workflows/release.yml`. The workflow:

- Triggers on `push` to `v*` tags
- Runs a `verify` job (`contents: read`, `persist-credentials: false`) that checks out the repo, discovers the default branch, and refuses to continue if the tag is not its ancestor — so unreviewed branches can't ship a release. Add the caller's setup and quality gate to this job.
- Runs a `publish` job (`contents: write`, `needs: verify`, no checkout) that calls `gh release create "$TAG" --generate-notes --verify-tag`, adding `--prerelease` when the tag contains a `-`

Splitting `verify` from `publish` keeps the job that checks out and gates repository code from ever holding `contents: write`. Action SHAs are pinned (not floating tags) for supply-chain hygiene. `references/release.md` documents which actions are pinned and how to refresh them when a new version comes out.

### 6. Verify and report

Re-read everything and print a small summary table to the user. Don't claim success without reading the post-state back from the API.

```bash
gh api "repos/$REPO" --jq '{
  squash: .allow_squash_merge, merge: .allow_merge_commit, rebase: .allow_rebase_merge,
  delete: .delete_branch_on_merge, title: .squash_merge_commit_title, body: .squash_merge_commit_message
}'
gh api "repos/$REPO/rulesets" --jq '.[] | {id, name, enforcement, target, reviews: ([.rules[] | select(.type=="pull_request") | .parameters.required_approving_review_count][0])}'
test -f .github/release.yml          && echo "release.yml present"
test -f .github/workflows/release.yml && echo "release workflow present"
```

The summary should call out:

- What was changed
- What was already correct (no-op)
- What was skipped (e.g. merge queue on a private free-tier repo) and why

## Idempotency rules

The skill is designed to be re-run safely on a partially-configured repo:

- **Repo settings:** `PATCH` is idempotent — re-applying the same body is a no-op response.
- **Rulesets:** lookup by either bootstrap variant name targeting the default branch. If found, diff and ask before `PUT`; reuse its id when switching variants. `POST` if absent. Never duplicate.
- **`.github/release.yml`:** diff before overwriting; ask if the content differs.
- **Release workflow:** same — diff and ask.
- **Never delete:** if a previous run left an artifact (e.g. a legacy classic branch-protection rule alongside the new ruleset), surface it for the user to decide. Don't quietly remove it.

## What this skill is NOT for

- Per-task GitHub ops (PRs, issues, CI status, releases for a specific tag) — out of scope
- Local git operations — out of scope
- Pre-commit hooks — use `/prek`
- Project task running — out of scope
- Designing a CI pipeline — out of scope; this skill writes one specific release workflow if asked, no more
- Backfilling status check names into a repo whose CI doesn't emit them yet — it tells you what names to use, you wire them in your CI

## Gotchas

- Required status check names must match exactly what your CI emits in the Checks API. After a green run on a PR, run `gh api repos/$REPO/commits/<sha>/check-runs --jq '.check_runs[].name'` to see the real names — silent typos will fail to gate merges.
- Squash merge with `squash_merge_commit_message=PR_BODY` puts the entire PR description into the commit body. Encourage clean PR bodies; sloppy ones become permanent commit history.
- Rulesets require admin permission on the repo (or org-level rulesets if applied at org scope). A token with only push/PR scopes will get a 403 here.
- Auto-generated release notes only categorize **merged PRs**, not direct commits. The default-branch ruleset blocks direct pushes, which is what makes release notes complete in the first place — these features reinforce each other.
- Use a merge queue only when GitHub eligibility is confirmed. A user-owned repository cannot use this rule even when it is public. Keep merge commits disabled at the repo level.
- If the "Merge when ready" button is missing from a PR view after this skill runs, double-check that both `allow_auto_merge=true` (repo-level) and the ruleset's `merge_queue` rule landed.
