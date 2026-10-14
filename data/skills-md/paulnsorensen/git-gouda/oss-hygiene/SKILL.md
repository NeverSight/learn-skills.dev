---
license: MIT
name: oss-hygiene
description: >
  Bring an open-source GitHub repository up to community-standards and
  supply-chain hygiene baseline: scaffold the GitHub Community Standards
  files (README check, LICENSE, CODE_OF_CONDUCT, CONTRIBUTING, SECURITY,
  issue + PR templates), wire Dependabot version updates, the Dependency
  Review action, OpenSSF Scorecard, and CodeQL (when applicable), check
  Dependabot alerts and secret scanning, and add the OpenSSF Best
  Practices Badge link. Use when the user says "set up OSS hygiene",
  "make this repo open-source-ready", "add community health files",
  "wire dependabot", "add scorecard", "OSSF badge", "supply chain
  hardening", or invokes /oss-hygiene on a public repo. Idempotent —
  safe to re-run; diffs against templates and asks before overwriting.
  Distinct from /gh-bootstrap (merge-button + branch protection) and
  /safe-settings (org-scale settings as code): focuses on the
  contributor-facing and supply-chain surface, not merge or org policy.
  Run after /gh-bootstrap; before announcing the repo.
---

# oss-hygiene

Brings a public GitHub repo up to the **GitHub Community Standards** baseline and the **OpenSSF Scorecard** supply-chain baseline, and stages it for the **OpenSSF Best Practices Badge**.

This sits next to `/gh-bootstrap` and answers a different question: gh-bootstrap locks the merge surface; oss-hygiene fills the contributor-facing and supply-chain surface.

## Where this skill fits

| Concern | Skill |
|---|---|
| Merge button, branch protection, release-notes config | `/gh-bootstrap` |
| Community files, supply-chain checks, OSSF posture | **`/oss-hygiene`** (this skill) |
| Org-wide settings as code across many repos | `/safe-settings` |

Per-task PR / issue / CI ops are out of scope for this catalog.

Run `/gh-bootstrap` first (so `main` is locked), then `/oss-hygiene` (so contributors can find their way in and supply-chain checks gate PRs).

## What gets configured

The skill operates on three orthogonal surfaces. It diffs every file against `assets/` templates and asks before overwriting anything that already exists.

### Surface 1 — GitHub Community Standards

The "Community Standards" tab under repo Insights surfaces these files. Missing files fail the checklist.

| File | Source asset | Purpose |
|---|---|---|
| `README.md` | (not scaffolded — repo has its own) | Surface check only |
| `LICENSE` | (not scaffolded — choose-a-license decision) | Surface check only |
| `CODE_OF_CONDUCT.md` | `assets/CODE_OF_CONDUCT.md` | Contributor Covenant 2.1 |
| `CONTRIBUTING.md` | `assets/CONTRIBUTING.md` | How to file issues, open PRs, run tests |
| `SECURITY.md` | `assets/SECURITY.md` | Vulnerability reporting (private advisory) |
| `.github/ISSUE_TEMPLATE/bug_report.yml` | `assets/.github/ISSUE_TEMPLATE/bug_report.yml` | Structured bug form |
| `.github/ISSUE_TEMPLATE/feature_request.yml` | `assets/.github/ISSUE_TEMPLATE/feature_request.yml` | Structured feature form |
| `.github/ISSUE_TEMPLATE/config.yml` | `assets/.github/ISSUE_TEMPLATE/config.yml` | Disable blank issues, contact links |
| `.github/PULL_REQUEST_TEMPLATE.md` | `assets/.github/PULL_REQUEST_TEMPLATE.md` | PR checklist |

For LICENSE: if missing, do **not** silently scaffold. License choice is a decision (`MIT`, `Apache-2.0`, `AGPL-3.0`, etc.) — surface the gap and link the user to <https://choosealicense.com/>.

For README: surface a missing-or-thin warning but do not auto-generate. README content is the project's voice.

### Surface 2 — Supply chain (Scorecard checks)

OpenSSF Scorecard runs ~18 automated checks. The skill wires the ones that are scaffold-shaped:

| Scorecard check | Risk | Action |
|---|---|---|
| `Security-Policy` | Medium | `SECURITY.md` (Surface 1) |
| `License` | Low | `LICENSE` (Surface 1, surface only) |
| `Dependency-Update-Tool` | High | `assets/.github/dependabot.yml` |
| `Branch-Protection` | High | covered by `/gh-bootstrap` ruleset |
| `Code-Review` | High | covered by `/gh-bootstrap` PR rule |
| `CI-Tests` | Low | repo's existing CI |
| `Token-Permissions` | High | audit existing workflows for `permissions:` blocks; report only |
| `Dangerous-Workflow` | Critical | audit only — warn on `pull_request_target` + `actions/checkout` of head ref |
| `SAST` | Medium | `assets/.github/workflows/codeql.yml` (when applicable) |
| `Pinned-Dependencies` | Medium | report only — pinning is per-ecosystem and contentious |
| `Maintained` | High | passive — emerges from real activity |
| `Binary-Artifacts` | High | scan for `.so`, `.dll`, `.jar`, `.exe`, `.zip`, `.tgz` in tree; warn |
| `Vulnerabilities` | High | passive — Dependabot alerts handle it |
| `Signed-Releases` | High | report only — sigstore wiring is project-specific |
| `Fuzzing` | Medium | report only — language-specific |
| `Packaging` | Medium | report only — depends on release pipeline |
| `Contributors` | Low | passive |
| `CII-Best-Practices` | Low | Surface 3 |

Plus the GitHub-native Code Security features that **don't go in repo files**:

| Feature | How to enable | Action |
|---|---|---|
| Dependabot alerts | Repo Settings → Advanced Security (auto-on for public) | verify via API |
| Secret scanning alerts (for users) | Repo Settings → Advanced Security (free public, opt-in) | enable via API |
| Push protection (secret scanning) | Repo Settings → Advanced Security | enable via API |
| Dependency graph | Repo Settings → Security (auto-on for public) | verify via API |
| Dependency Review Action | `assets/.github/workflows/dependency-review.yml` | scaffold |
| Scorecard publishing | `assets/.github/workflows/scorecard.yml` | scaffold (uploads SARIF for the badge) |

### Surface 3 — OpenSSF Best Practices Badge

The badge is **self-attested** at <https://www.bestpractices.dev>. The skill doesn't fill it out — the project owner has to. What the skill does:

1. Checks whether the repo already has a badge (looks for the badge URL in README).
2. Prints the registration link with the repo URL pre-filled.
3. Suggests adding the badge markdown to README (`assets/README-badge-snippet.md`).

The badge is a Scorecard `CII-Best-Practices` check enabler — registering even at the in-progress level is the lowest-effort way to bump that score.

## Protocol

### 1. Confirm scope and inspect current state

```bash
gh auth status
gh repo view --json nameWithOwner,visibility,isPrivate,licenseInfo,description
gh api "repos/$REPO/community/profile" --jq '{
  health_percentage,
  files: (.files | to_entries | map(select(.value != null)) | from_entries | keys)
}'
gh api "repos/$REPO/vulnerability-alerts" 2>/dev/null && echo "dependabot alerts: ON" || echo "dependabot alerts: OFF"
gh api "repos/$REPO" --jq '{
  secret_scanning: .security_and_analysis.secret_scanning.status,
  push_protection: .security_and_analysis.secret_scanning_push_protection.status
}'
```

Ask the user — **once, as a single consolidated question** with all decisions inline. Do not prompt sequentially; the user should be able to reply "go with defaults" and have the skill proceed. Cap the list at the items below (≤5):

- Visibility — this skill is sized for **public** repos. Private repos can use a subset (community files yes, secret scanning needs Advanced Security, scorecard publishing needs public visibility for the badge).
- License — if `licenseInfo` is null, surface and stop until the user picks one.
- CodeQL applicability — does the repo contain code in a CodeQL-supported language (`actions`, `c-cpp`, `csharp`, `go`, `java-kotlin`, `javascript-typescript`, `python`, `ruby`, `swift`)? If not, skip the CodeQL workflow. **Surface a recommendation, don't force a question** when the only matches are CI-helper scripts (e.g. `.github/scripts/*.py`) — those are not project code, and the default should be skip with the user opting in.
- FUNDING.yml — does the user accept sponsorship? If yes, ask for platform + handle (GitHub Sponsors, Buy Me a Coffee, Ko-fi, OpenCollective, etc.).
- CODEOWNERS — only suggest when the repo has multiple maintainers. For solo, skip.
- Contact email — ask for the security/conduct reporting address. If the user gives none, do not write `CODE_OF_CONDUCT.md` or `SECURITY.md` with a literal `{{CONTACT_EMAIL}}` placeholder; stop and ask before scaffolding those two files.

### 2. Scaffold the community files

For each file under `assets/`, in order:

```text
CODE_OF_CONDUCT.md
CONTRIBUTING.md
SECURITY.md
.github/ISSUE_TEMPLATE/bug_report.yml
.github/ISSUE_TEMPLATE/feature_request.yml
.github/ISSUE_TEMPLATE/config.yml
.github/PULL_REQUEST_TEMPLATE.md
```

Diff against the existing file (if present). If different, ask before overwriting. Substitute `{{REPO}}`, `{{OWNER}}`, `{{CONTACT_EMAIL}}` placeholders.

`CONTRIBUTING.md` includes a generic skeleton — encourage the user to project-specific-ize it after merge.

### 3. Scaffold the supply-chain workflows

| Asset | Target | When to skip |
|---|---|---|
| `assets/.github/dependabot.yml` | `.github/dependabot.yml` | never (always useful) |
| `assets/.github/workflows/dependency-review.yml` | `.github/workflows/dependency-review.yml` | private repo without Code Security |
| `assets/.github/workflows/scorecard.yml` | `.github/workflows/scorecard.yml` | private repo (badge needs public) |
| `assets/.github/workflows/codeql.yml` | `.github/workflows/codeql.yml` | repo has no CodeQL-supported language |

When scaffolding `codeql.yml`, substitute `{{CODEQL_LANGUAGES}}` in the `language` matrix with the CodeQL-supported languages detected in the repo (comma-separated, quoted, e.g. `"python", "go"`).

`dependabot.yml` is configured with the language packages detected in the repo (look for `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `Gemfile`, `composer.json`, `pom.xml`, etc.) plus a `github-actions` ecosystem entry to keep workflow action versions current.

**Manifest detection scope.** Only count manifests in project source roots — *not* under `.github/scripts/`, `.devcontainer/`, `tools/ci/`, or other CI-helper paths. A `pyproject.toml` under a project root is real; a hard-coded `pip install foo==1.2.3` line in a workflow is not, and Dependabot can't track it without a real top-level manifest. When the only language presence is CI-helper code, **skip that ecosystem** and add a one-line comment in the generated `dependabot.yml` explaining why (e.g. "no top-level Python manifest; the only Python is in `.github/scripts/`"). This mirrors the same heuristic used for CodeQL applicability in step 1.

### 4. Toggle the GitHub-native security features

Use `gh api` to enable or verify (idempotent — re-applying is a no-op):

```bash
# Automated security fixes / Dependabot security updates
gh api -X PUT "repos/$REPO/automated-security-fixes"

# Vulnerability alerts (Dependabot alerts)
gh api -X PUT "repos/$REPO/vulnerability-alerts"

# Secret scanning alerts for users + push protection
gh api -X PATCH "repos/$REPO" \
  -F security_and_analysis[secret_scanning][status]=enabled \
  -F security_and_analysis[secret_scanning_push_protection][status]=enabled

# Private vulnerability reporting
gh api -X PUT "repos/$REPO/private-vulnerability-reporting"
```

If private vulnerability reporting cannot be enabled, require a real contact email from the user before writing `SECURITY.md` — do not fall back to a placeholder reporting channel.

For private repos these may 403 unless GitHub Code Security is paid for — surface and skip rather than fail.

### 5. Audit existing workflows for Token-Permissions and Dangerous-Workflow

This is **detection**, not modification. The skill reads each `.github/workflows/*.yml`:

- **Token-Permissions:** flag any workflow without a top-level `permissions:` block (or with `permissions: write-all`). Suggest the safe default `permissions: { contents: read }` and bump only what each job needs.
- **Dangerous-Workflow:** flag the unsafe pattern of `pull_request_target` + `actions/checkout` of the head SHA, and any `${{ ... }}` interpolation of `github.event.*` inputs into shell scripts.

Print findings; don't auto-edit. These are subtle changes the user should review.

### 6. Surface the OpenSSF Best Practices Badge step

Print, don't apply. Substitute `<owner>`, `<repo>`, and the project ID once registered. Read `assets/README-badge-snippet.md` and **strip the block between `<!-- BEGIN-CODEQL -->` and `<!-- END-CODEQL -->` markers when CodeQL was skipped in step 3** — the markers exist precisely so the snippet is conditionally trimmable without ambiguity.

```text
Register at: https://www.bestpractices.dev/en/projects/new
Repo URL:    https://github.com/<owner>/<repo>
Once you have a project ID, paste this into README.md:

[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/<owner>/<repo>/badge)](https://scorecard.dev/viewer/?uri=github.com/<owner>/<repo>)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/<id>/badge)](https://www.bestpractices.dev/projects/<id>)
```

The skill does not register the project for the user — registration is a credential and judgment step (the user attests answers).

### 7. Verify and report

Re-read the community profile and the workflow files. Print a small summary:

```bash
gh api "repos/$REPO/community/profile" --jq '{health_percentage, missing: ([.files | to_entries[] | select(.value == null) | .key])}'
gh api "repos/$REPO/private-vulnerability-reporting"
ls .github/workflows/ | sort
```

The summary should call out:

- What was scaffolded (and the diff vs existing if any)
- What was already correct (no-op)
- What was skipped and why (no LICENSE, private repo, no CodeQL languages, etc.)
- The OSSF badge registration link

## Idempotency

- Files: diff before overwriting; ask if the content differs.
- API toggles: `PUT`/`PATCH` are idempotent.
- Workflow audit: read-only — re-running just re-prints the same findings.
- Never delete: if a previous run left an artifact (an old workflow with a different name), surface it and let the user decide.

## What this skill is NOT for

- License selection — it surfaces the gap, doesn't pick one
- README authoring — content is the project's voice
- Org-wide community files — use `/safe-settings` for that
- Branch protection / merge queue — use `/gh-bootstrap`
- Sigstore release signing — language- and pipeline-specific, out of scope
- Filling out the OSSF Best Practices Badge questionnaire — that's the maintainer's attestation
- Pinning dependencies — per-ecosystem, often contentious
- Setting up fuzzing — language-specific

## Gotchas

- **Default community health files**: if the user/org has a `.github` repo with these files, they apply to *every* repo without its own copy. Scaffolding into a repo overrides the org default; only do it when per-repo overrides are intended.
- **Dependency Review Action**: works on **public** repos for free, and on private repos only with **GitHub Advanced Security**. The workflow will hard-fail on private/free.
- **Scorecard workflow**: needs `id-token: write` for OIDC publishing to scorecard.dev; the asset has the right permissions. If the workflow fails on first run with a 403, the user has org-level OIDC restrictions.
- **CodeQL setup-mode**: `default` setup is configured in the GitHub UI (Settings → Code security → CodeQL → Set up). The asset uses `advanced` setup (workflow file). The two are mutually exclusive — if the user enabled default first, the workflow file will conflict.
- **Token-Permissions audit**: actions like `softprops/action-gh-release` and many publish actions need `contents: write`. Don't tell users to set every workflow to read-only — flag and explain.
- **`pull_request_target` is dangerous by default**: don't use it just to access secrets in fork PRs. The skill flags it; the user should refactor to a separate `workflow_run` or labeled-PR pattern.
- **OSSF badge is self-attested**: a passing badge means the maintainer answered the questions, not that an audit happened. It's a signal, not a guarantee.
- **Scorecard score on tiny / new repos**: the `Maintained` check needs 90 days of activity; new repos will score low until they age in. This is a feature, not a bug.
- **Pinned workflow maintenance**: the scaffolded workflows use reviewed commit SHAs. Dependabot can propose SHA refreshes with version comments; review those PRs before merging and keep the checksum or pin evidence current.

## References

- `references/scorecard-checks.md` — full table of all 18 Scorecard checks, what they measure, and remediation pointers.
- `references/badge-criteria.md` — OpenSSF Best Practices Badge Passing criteria mapped to repo artifacts.
- `references/community-standards.md` — GitHub's own checklist and how each file is detected.
- `references/dependabot.md` — `dependabot.yml` schema reference and per-ecosystem examples.
- `references/workflow-hardening.md` — Token-Permissions and Dangerous-Workflow rules with concrete examples.
