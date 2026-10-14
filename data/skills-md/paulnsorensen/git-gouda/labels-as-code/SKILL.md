---
license: MIT
name: labels-as-code
description: >
  Manage a GitHub repository's labels as a version-controlled file and
  auto-label pull requests by changed path. Export current labels, diff
  them against a proposed `.github/labels.yml`, sync the difference
  (one-shot or via a scheduled workflow using one verified, SHA-pinned
  action), and wire path-based PR labeling with `actions/labeler` and
  `.github/labeler.yml`. Use when the user says "standardize labels",
  "sync labels", "auto-label PRs by path", "labels as code", or invokes
  /labels-as-code. Do NOT use for org-wide label policy across many
  repos — route that to /safe-settings, which reconciles labels
  (rename, exclude) from a central admin repo. Do NOT use for issue
  forms or templates — that is /oss-hygiene. Label deletions are never
  automatic; the skill asks for explicit authorization first.
---

# labels-as-code

Brings a single GitHub repository's labels under version control and keeps pull-request labeling in sync with the files that changed.

## Where this skill fits

| Concern | Skill |
|---|---|
| One repo's label set, tracked in a file, synced on demand or on schedule | **`/labels-as-code`** (this skill) |
| Path-based PR auto-labeling for one repo | **`/labels-as-code`** (this skill) |
| Label policy across many repos, reconciled from one admin repo | `/safe-settings` |
| Issue forms, PR templates, community health files | `/oss-hygiene` |

`/safe-settings` can also manage labels org-wide through its `labels` block (rename via `oldname`, exclusion patterns), reconciled every `full-sync` run. Reach for `/safe-settings` when label policy must stay in sync across many repos from a central admin repo. Reach for this skill when the scope is one repository and the file lives in that repository.

## What gets configured

| File | Purpose |
|---|---|
| `.github/labels.yml` | The label set: `name`, `color`, `description` per label |
| `.github/labeler.yml` | Path-to-label rules consumed by `actions/labeler` |
| `.github/workflows/labels-sync.yml` (optional) | Scheduled/on-push sync of `.github/labels.yml` to the repo |
| `.github/workflows/labeler.yml` (optional) | Runs `actions/labeler` on every pull request |

## Protocol

### 1. Export current labels and diff

```bash
gh label list --json name,color,description
```

Compare the export against the proposed `.github/labels.yml` (create it from `assets/labels.yml` if the file does not exist yet). Print the diff — labels to create, labels to recolor or redescribe, and labels present on GitHub but absent from the file — before proposing any change.

### 2. Propose a default label set

`assets/labels.yml` ships a starting set grouped by prefix:

- `type/*` — one label per Conventional Commits type (`feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`), aligned with the types `/pr-title-lint` checks in the PR title.
- `priority/*` — `critical`, `high`, `medium`, `low`.
- `status/*` — `blocked`, `in-progress`, `needs-review`.
- `good first issue`, `help wanted` — GitHub's own community-standards labels.
- `dependencies` — Dependabot and manual dependency-bump PRs.
- `breaking` — a breaking change, called out at release time.

Read `references/label-scheme.md` for the full table and for how `type/*` and `breaking` map onto `/gh-bootstrap`'s `.github/release.yml` categories (that file's `Breaking changes` bucket keys on `breaking-change`/`breaking`; its `Features`/`Fixes`/`Documentation`/`Internal` buckets key on bare Conventional-Commits-style names, not the `type/` prefix). If the repo already runs `/gh-bootstrap`'s release notes, either keep both label spellings on the affected PRs or extend `release.yml`'s category lists with the `type/*` names — `/gh-bootstrap` owns that file; this skill only documents the mapping.

Ask the user whether to adopt the default set as-is, trim it, or start from the exported labels instead. Do not assume — a repo with an established label set may prefer to keep its own names.

### 3. Sync options

Two ways to apply `.github/labels.yml` to the repo. Ask the user which one before doing either.

The workflow templates in this step and in step 4 pin Node 24 actions. Before you copy either workflow, confirm that any self-hosted runner is Actions Runner v2.327.1 or later. GitHub-hosted runners already meet this requirement.

#### One-shot sync

```bash
# Create or update one label (never deletes):
gh label create "<name>" --color "<hex>" --description "<text>" --force

# Clone another repo's full label set (adds only; existing labels keep
# their color/description unless the label doesn't exist yet):
gh label clone <owner>/<repo>
```

`--force` overwrites color/description on an existing label; it does not delete labels that are absent from the source. **Never delete a label without explicit, per-label user authorization** — list the labels that would be removed and wait for a yes before running `gh label delete`.

#### Scheduled sync workflow

For drift correction without a human running `gh label create` by hand, copy `assets/labels-sync.yml` to `.github/workflows/labels-sync.yml`. It runs `crazy-max/ghaction-github-labeler`, the maintained action verified for this skill (see `references/label-scheme.md` for the verification command and the current pinned SHA). The template ships with `skip-delete: true` — labels absent from `.github/labels.yml` are left alone, not deleted. Flip `skip-delete` to `false` only after the user explicitly authorizes deletions; the diff in step 1 shows exactly which labels that would remove. The template runs weekly on a `schedule` trigger, on each push to `main` that changes `.github/labels.yml` or the workflow file itself, and on manual `workflow_dispatch`.

`EndBug/label-sync` is a viable alternative with the same shape (sync from a YAML file, delete-by-default gated by an option). Verify either action's latest release and SHA with `gh api repos/{owner}/{repo}` and the tag-to-commit lookup in `references/label-scheme.md` before pinning — do not reuse a SHA from this skill without re-verifying it against the current release.

### 4. Path-based PR labeling

Copy `assets/labeler.yml` to `.github/labeler.yml` and adapt the path globs to the repo's directory layout — the shipped file is an example, not a fit-all config. Copy `assets/pr-labeler.yml` to `.github/workflows/labeler.yml`; it runs `actions/labeler` with `permissions: contents: read, pull-requests: write` (the minimum the action needs to read changed files and write labels).

Verify the pinned SHA before relying on it:

```bash
LATEST=$(gh api repos/actions/labeler/releases/latest --jq '.tag_name')
gh api repos/actions/labeler/git/ref/tags/"$LATEST" --jq '.object.sha'
```

If the returned SHA does not match the comment in `assets/pr-labeler.yml`, update both the `uses:` line and its trailing version comment together — a stale comment next to a fresh SHA is worse than no comment.

### 5. Verify

```bash
gh label list --json name,color,description
```

Confirm the output matches `.github/labels.yml` exactly (same names, colors, descriptions — modulo any labels the user chose to keep unmanaged). Then open a pull request that touches a path matched in `.github/labeler.yml` and confirm the expected label lands on it, either by watching the `labeler.yml` run or with:

```bash
gh pr view <number> --json labels --jq '.labels[].name'
```

Report what was created, updated, and left alone, and which labels (if any) are still pending user authorization to delete.

## What this skill is NOT for

- Org-wide label policy reconciled across many repos — use `/safe-settings`
- Issue forms, PR templates, or other community-health files — use `/oss-hygiene`
- Deleting labels without the user's explicit, per-label go-ahead
- Branch protection, merge settings, or release-notes plumbing — use `/gh-bootstrap`

## Gotchas

- `gh label create --force` is idempotent for color/description but never deletes. Deletion is a separate, explicit `gh label delete` call — never bundle it into a routine sync without asking first.
- `crazy-max/ghaction-github-labeler` deletes labels that are absent from the YAML file *unless* `skip-delete: true` is set. Confirm that flag before wiring the workflow into a repo with labels the file doesn't enumerate.
- `actions/labeler`'s `sync-labels` input removes a path-based label when the PR no longer touches that path. Leave it at its default (`false`) unless the user wants that behavior — it is a form of automatic deletion.
- Label colors in `gh label create --color` take a bare hex string without `#`; `.github/labels.yml` conventionally also stores the hex without `#` for `actions/labeler`'s upstream ecosystem, but `crazy-max/ghaction-github-labeler` accepts either. Keep one convention within a repo's file.
- Renaming a label with `gh label create --force` does not rename — it creates a new label. Use `gh label edit <old-name> --name <new-name>` for renames, or `from_name:` in the sync tool's config format if it supports it.
