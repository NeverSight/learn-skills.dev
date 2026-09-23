---
name: repo-align
description: >-
  Audits and standardizes personal GitHub repositories under ~/github/kevmoo
  for CI workflow parity, Markdown formatting configs, analyzer lints, and
  GitHub remote branch protection rulesets. Use when checking or fixing CI
  workflows (lower_bound.yml, complexity.yml, autosubmit.yml, dependabot.yml,
  markdown.yml), .prettierrc.json, analysis_options.yaml lints, or remote
  auto-merge and status-check rulesets across one or all personal repositories.
  Don't use for non-kevmoo repositories (dart-lang/*, flutter/*, google/*),
  Dart source code refactoring (use dart-cleanup), or PR and worktree branch
  pruning (use pr-cleanup).
compatibility: "Requires kscripts (kevmoo_scripts via dart install) and local checkouts in ~/github/kevmoo"
metadata:
  author: kevmoo
  target_environment: personal
---

# Personal Repository Alignment & Hygiene (`repo-align`)

> [!NOTE] This skill targets personal repositories under `~/github/kevmoo/*` and
> invokes the unified `kscripts` AOT CLI.

## Quick Start & Prerequisites

Ensure `kscripts` is installed and up to date on `PATH`. If `kscripts` is
missing, install it from the canonical Git remote:

```bash
dart install 'kevmoo_scripts@{git: https://github.com/kevmoo/scripts.dart}'
```

Thereafter `upkeep update dart_install` keeps it current -- it re-reads the
source descriptor from the installed bundle's own `pubspec.lock` and reinstalls
from the same remote.

> [!WARNING] Do **not** run `dart install ~/github/kevmoo/scripts.dart`.
> Installing from a local path builds whatever branch that checkout is on, and
> it _replaces_ the `app-bundles/kevmoo_scripts/git/<sha>/` bundle with a
> `local/` one -- which permanently repoints `upkeep update dart_install` at
> that checkout instead of the remote. Only use a path install to test
> uncommitted work, and reinstall from Git afterwards.

## 1. Read-Only Alignment Audit (`check`)

Always begin with a non-destructive check to identify drift across local files
and remote GitHub settings:

1. **Single Repository Audit**:
   ```bash
   kscripts repo-align check -r <repo_name>
   ```
2. **Fleet-Wide Audit (`~/github/kevmoo/*`)**:
   ```bash
   kscripts repo-align check
   ```
   _(Pass `--json` when programmatically filtering or grouping drift across many
   repositories)._

### What `kscripts repo-align check` Verifies

- **Analyzer Lints (`--lints`)**: Strict mode (`strict-casts`,
  `strict-inference`, `strict-raw-types`) and canonical lint package includes in
  `analysis_options.yaml`.
- **CI Workflows & Markdown Config (`--ci`)**:
  - Standard workflow templates (`lower_bound.yml`, `complexity.yml`,
    `autosubmit.yml`, `dependabot.yml`, `publish.yaml`, `health.yaml`,
    `post_summaries.yml`, `markdown.yml`).
  - Canonical `.prettierrc.json` and absence of stray `.prettierignore` files
    (applies across all `RepoKind`s, including `agentSkills`).
  - Flags deprecated root `uses: kevmoo/analytica.dart@...` workflow references
    and narrow `.github/workflows/**` path triggers.
- **GitHub Remote Settings (`--github`)**:
  - `allow_auto_merge` enabled on the repository.
  - Presence of the `autosubmit` repository label.
  - Branch protection rulesets and required status checks matching the workflow
    matrix jobs (detects critical ungated auto-merge configurations).

## 2. Step 1 of Remediation: Local Repository File Fixes (`--ci --lints` via Worktree PR)

Always land local workflow and lint file fixes on `main` via a Pull Request
**before** applying remote GitHub branch rulesets (`--github`). Requiring a
status check (such as `markdown`) in a GitHub branch ruleset before its workflow
file exists on `main` deadlocks open PRs
(`Expected — waiting for status to be reported`) and causes `repo-align`'s
ruleset sync to skip the missing workflow check.

Never modify files directly on `main`. For each target repository:

1. **Create or Enter a Sibling Worktree** (via `/new-worktree`, e.g.
   `~/github/kevmoo/_<repo>-repo-align`).
2. **Apply Alignment & Lint Fixes Inside the Worktree (`--dir`)**: Pass
   `--dir <worktree_path>` so `repo-align` writes `.github/workflows/*`,
   `.prettierrc.json`, and `analysis_options.yaml` inside the sibling worktree
   rather than mutating the primary `~/github/kevmoo/<repo_name>` checkout:
   ```bash
   kscripts repo-align fix -r <repo_name> --dir <worktree_path> --ci --lints
   kscripts lint-cleanup --package-dir <worktree_path> --rewrite
   ```
3. **Optional Dependency Tightening** _(only when requested or preparing a
   release)_:
   ```bash
   cd <worktree_path> && kscripts tighten
   ```
4. **Pre-PR Verification Gate**:
   ```bash
   cd <worktree_path>
   npx --yes prettier@3.9.6 --write "**/*.md"
   dart format --output=none --set-exit-if-changed .
   dart analyze --fatal-infos
   dart test -c source
   ```
5. **Commit, Push, & Open PR**:
   - Check `pubspec.yaml` for published packages: if at a released version
     (missing `-wip`), bump to the next `-wip` patch version and add a matching
     empty `## <version>-wip` section header in `CHANGELOG.md`.
   - Push the feature branch and open a PR via `gh pr create --body-file -`.

## 3. Step 2 of Remediation: Remote GitHub Settings (`--github`)

Once the workflow files exist on `main` (or if only remote settings are
drifted), confirm with the user via `ask_question` and apply remote ruleset,
auto-merge, and `autosubmit` label fixes:

```bash
kscripts repo-align fix -r <repo_name> --github
```

Finally, re-run `kscripts repo-align check -r <repo_name>` to verify
`🟢 Aligned` status across both local files and GitHub branch rulesets.
