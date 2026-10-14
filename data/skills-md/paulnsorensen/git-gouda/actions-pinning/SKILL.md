---
license: MIT
name: actions-pinning
description: >
  Inventory, classify, and pin every `uses:` reference in GitHub Actions
  workflows, composite actions, and reusable workflows to a verified commit
  SHA, then keep those pins fresh with Dependabot. Use when the user says
  "pin actions", "unpinned actions", "SHA pin", "supply chain for
  workflows", or invokes /actions-pinning. Do NOT use for permissions and
  injection hardening of workflow files (route to /oss-hygiene) or for CI
  run-time speed (route to /ci-optimize).
---

# actions-pinning

Pins every `uses:` reference in GitHub Actions workflows, composite
actions, and reusable workflows to a commit SHA, verifies each SHA
belongs to the claimed action repository, and keeps the pins current
with Dependabot.

This skill covers supply-chain pinning only. `/oss-hygiene` covers
`Token-Permissions` and `Dangerous-Workflow` hardening for the same
workflow files; `/ci-optimize` covers wall-clock speed. Run those
separately.

## Protocol

### 1. Inventory

Run the bundled scanner against every workflow and composite/reusable
workflow file:

```bash
python3 scripts/pin_check.py .
```

It walks `.github/workflows/**`, `.github/actions/**`, and every
`action.yml` or `action.yaml` manifest in the tree. It skips VCS and
dependency directories: `.git`, `.hg`, `.svn`, `node_modules`, `.venv`,
`venv`, `__pycache__`, `dist`, `build`, `.tox`, and `target`. It scans
`vendor/`, because a `./vendor/...` reference can run a vendored action.
It prints a table of `(file, line, action, ref, status)` for every
`uses:` line and exits 1 when any reference is unpinned. Use `--json`
for machine-readable output when scripting the remaining steps.

The scanner uses regular expressions, not a YAML parser. It removes one
matching pair of surrounding quotes from each `uses:` value. It has two
known limits; check the workflow by hand when either applies:

- A `uses:` line inside a `run: |` block scalar gives a false row.
- A flow-style mapping such as `- {uses: owner/repo@v1}` gives no row.

### 2. Classify

The scanner assigns one status per reference:

| Status | Meaning | Action needed |
|---|---|---|
| `pinned-sha` | already a full 40-character commit SHA | none |
| `unpinned-tag` | a tag-shaped ref such as `v4` or `v4.1.0` | resolve to a SHA |
| `unpinned-branch` | a common branch name such as `main` | resolve to a SHA |
| `unpinned-ref` | any other ref, such as `release/v1`; type unknown | resolve to a SHA |
| `unpinned-commit` | a commit-like hex ref, such as a short SHA `de0fac2` or an uppercase 40-character SHA | resolve to the full lowercase SHA |
| `missing-ref` | no `@ref` at all | resolve to a SHA |
| `invalid-self-ref` | a `$/path` self-repository reference with an `@ref` suffix | remove the `@ref` suffix |
| `local` | a local `./path` action or a `$/path` self-repository reference | skip — not a supply-chain risk |
| `docker` | a `docker://image` reference | flag separately — SHA pinning applies to the image digest, not this scanner |

### 3. Resolve each ref to a commit SHA

For each `unpinned-tag`, `unpinned-branch`, `unpinned-ref`,
`unpinned-commit`, or `missing-ref` finding:

```bash
# Tag: the ref object is the commit (lightweight) or a tag object (annotated).
gh api repos/{owner}/{repo}/git/ref/tags/{tag} --jq '.object'

# Branch: the ref object is the commit directly.
gh api repos/{owner}/{repo}/git/ref/heads/{branch} --jq '.object.sha'

# Annotated tag: dereference the tag object to get the commit SHA.
gh api repos/{owner}/{repo}/git/tags/{tag_sha} --jq '.object.sha'
```

For an `unpinned-ref`, try the `tags/` path first, then the `heads/`
path.

For an `unpinned-commit`, the tag and branch paths cannot resolve the
ref. Resolve it through the commits endpoint, which returns the full
lowercase SHA:

```bash
gh api repos/{owner}/{repo}/commits/{ref} --jq '.sha'
```

**Impostor-commit check — always run before rewriting a pin.** Confirm
the resolved SHA actually belongs to the action's own repository, not
a fork, a rewritten ref, or a spoofed value:

```bash
gh api repos/{owner}/{repo}/commits/{sha}
```

A 404 here means the SHA does not belong to that repository. Stop and
re-resolve; do not write an unverified SHA.

Once verified, rewrite the line:

```yaml
uses: owner/repo@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
```

Keep the original tag as a trailing comment — it is the human-readable
version marker; the SHA is the enforced pin.

### 4. Keep pins fresh with Dependabot

Add (or merge into an existing `dependabot.yml`) the `github-actions`
ecosystem entry in `assets/dependabot-actions-snippet.yml`. Dependabot
resolves tag bumps to new commit SHAs automatically and opens a PR
with the version comment updated — review and merge those PRs rather
than hand-editing pins later.

Version updates (not security updates) default to a 3-day
registry-availability cooldown as of 2026-07-14; a newly published tag
won't appear in a Dependabot PR until it clears that window. See
`references/policy.md` for the source.

For the full `dependabot.yml` scaffold across every ecosystem in the
repo, use `/oss-hygiene` — this skill only owns the `github-actions`
entry.

### 5. Repository and organization pinning policy

GitHub can enforce SHA pinning at the allowed-actions policy level
(repo, org, or enterprise), including blocking specific actions
outright. Read the current policy at the scope of the request before
proposing any change:

```bash
# Repository scope.
gh api repos/{owner}/{repo}/actions/permissions

# Organization scope. Use this for an organization-wide request.
gh api orgs/{org}/actions/permissions
```

These are reads. Never call the corresponding write endpoints
(`PUT repos/{owner}/{repo}/actions/permissions`,
`PUT orgs/{org}/actions/permissions`, and the `selected-actions` /
`allowed_actions` variants) without the user's explicit authorization
for that specific change — policy changes can block other workflows
from running.

The SHA-pinning policy applies to actions only. Reusable workflows
can still use a tag under that policy, so this skill pins reusable
workflow references itself.

### 6. Flag mutable downloads inside workflow scripts

Regex pinning covers `uses:` only. While reading each workflow, also
flag (findings only, no rewrite) any `run:` step that fetches code
outside the pinned-action mechanism:

- `curl ... | sh` or `curl ... | bash` piping a remote script straight
  into a shell.
- `wget` from a URL with no version or checksum.
- `pip install package` (or `npm install`, `gem install`, ...) with no
  version pin.

These are supply-chain risk in the same family as an unpinned action,
but fixing them is per-ecosystem and often changes build behavior —
report them, do not rewrite them.

### 7. Optional: zizmor

If `zizmor` is installed, run it for a second opinion (it also checks
`bot-conditions` and composite-action internals this scanner does
not):

```bash
zizmor .github/workflows/
```

Skip silently if it is not installed — it is optional tooling, not a
required gate.

### 8. Verify

Re-run the scanner after every rewrite batch:

```bash
python3 scripts/pin_check.py . && echo "all uses: references pinned"
```

Exit 0 with no `unpinned-tag`, `unpinned-branch`, `unpinned-ref`,
`unpinned-commit`, `missing-ref`, or `invalid-self-ref` rows means every
actionable reference is pinned. Report `local` and `docker` rows
separately — they are informational, not failures.

## What this skill is NOT for

- `Token-Permissions` and `Dangerous-Workflow` hardening (least-privilege
  `permissions:` blocks, `pull_request_target` risk, `${{ github.event.* }}`
  interpolation into shell) — use `/oss-hygiene`.
- CI run-time speed — use `/ci-optimize`.
- Choosing or writing the full `dependabot.yml` for non-Actions
  ecosystems — use `/oss-hygiene`.
- Applying an org-wide allowed-actions policy without the repo owner's
  explicit authorization for that specific write.

## References

- `references/policy.md` — cited primary sources for `uses:` syntax,
  SHA pinning, the allowed-actions policy, SHA resolution endpoints,
  the Dependabot cooldown, and zizmor.
- `scripts/pin_check.py` — the inventory/classification scanner used
  in steps 1, 2, and 8 (`--self-test` runs its embedded fixtures;
  `--json` for machine-readable output).
- `assets/dependabot-actions-snippet.yml` — the `github-actions`
  ecosystem entry for `dependabot.yml`.
