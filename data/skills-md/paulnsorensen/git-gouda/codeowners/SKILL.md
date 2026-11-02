---
license: MIT
name: codeowners
description: >
  Author, validate, and enforce a CODEOWNERS file: detect an existing file,
  gather ownership evidence from directory structure and git history, write
  or update rules with correct CODEOWNERS syntax, validate the file against
  the GitHub API, and wire the ruleset rule that requires code owner review
  on pull requests. Use when the user says "add CODEOWNERS", "who owns this
  path", "require owner review", "validate CODEOWNERS", or invokes
  /codeowners. Idempotent — safe to re-run; diffs before overwriting and
  never auto-assigns an owner without confirmation. Do NOT use for branch
  rulesets in general (use /gh-bootstrap) or community health files such as
  README, LICENSE, CODE_OF_CONDUCT, and SECURITY (use /oss-hygiene) — this
  skill only covers the CODEOWNERS file and the review rule it feeds.
---

# codeowners

Author and maintain a `CODEOWNERS` file, then wire the ruleset rule that
turns it into an enforced review requirement.

This skill covers one file and the rule it feeds. It does not configure
branch rulesets in general (`/gh-bootstrap`) or community health files
(`/oss-hygiene`).

## When to use

- The user asks to add or update a `CODEOWNERS` file.
- The user asks who owns a path, or wants ownership suggestions from git
  history.
- The user asks to require owner review on pull requests.
- The user asks to validate an existing `CODEOWNERS` file.

## Protocol

### 1. Detect the existing file and the default branch

GitHub reads `CODEOWNERS` from one of three locations, checked in this
order: `.github/`, the repository root, then `docs/`. Only the first file
found takes effect.

```bash
for path in .github/CODEOWNERS CODEOWNERS docs/CODEOWNERS; do
  test -f "$path" && echo "Found: $path"
done
REPO="$(gh repo view --json nameWithOwner --jq '.nameWithOwner')"
DEFAULT_BRANCH="$(gh repo view "$REPO" --json defaultBranchRef --jq '.defaultBranchRef.name')"
```

If more than one location has a file, tell the user only the first match
(`.github/`, then root, then `docs/`) is active and ask which one to keep.
If none exists, ask which location to create — `.github/CODEOWNERS` is the
conventional choice because it keeps repository policy files together.

### 2. Gather ownership evidence

Offer two approaches. Present results as suggestions and confirm them with
the user before writing any rule — never auto-assign an owner.

**Static, by directory structure.** List top-level and second-level
directories as candidate ownership boundaries:

```bash
git ls-files | awk -F/ 'NF>1 {print $1"/"$2"/"} NF==1 {print $1}' | sort -u
```

**History-derived, by committer.** For a given path, rank contributors by
commit count and list unique authors:

```bash
git shortlog -sn -- <path>
git log --format=%an -- <path> | sort -u
```

A top committer is a candidate, not a decision. Match each candidate name
or email to a GitHub handle or team before it goes in the file — a
CODEOWNERS entry that does not resolve to a valid GitHub user, or a team
with write access, is silently ignored by GitHub, not an error.

### 3. Author the rules

Write rules in the order the user confirmed, respecting CODEOWNERS syntax:

- **Last matching pattern wins.** Order general rules first, specific
  overrides last. A file matches its last matching line, not its first.
- **`@org/team` needs write access.** A team reference only takes effect if
  the team has been explicitly granted write access to the repository, not
  merely membership in the org. Before you write the line, confirm that the
  team exists and then confirm its write access (see Guardrails).
- **A trailing `*` fallback rule** (`* @org/default-owners`) catches paths
  no other rule matches. Put it first so more specific rules below it can
  override it.
- **Path patterns** follow `.gitignore` syntax: `/dir/` anchors to the repo
  root, `dir/` without a leading slash matches anywhere, and `*.ext` matches
  by extension. Directories match recursively unless narrowed.
- **Comments** start with `#` and section headers such as `# Frontend`
  group related rules for readability; GitHub also renders sections as
  named groups in file review UI when written as `#SECTION_NAME` blocks.

See `references/syntax.md` for the full syntax and precedence reference,
and `assets/CODEOWNERS.example` for a starting template.

Before writing, diff any existing file against the proposed content and
show the user the diff. Do not overwrite silently.

### 4. Validate

After the file is pushed to the default branch, GitHub can check it for
syntax and ownership errors:

```bash
gh api "repos/$REPO/codeowners/errors"
```

A `404` here means no `CODEOWNERS` file was found at any of the three
valid locations on the default branch — push first, then re-check. A `200`
with an empty `errors` array means the file is valid. Non-empty entries
name the line and the problem (unknown user, team without write access,
bad pattern).

As a local sanity check before push, confirm the paths a rule targets
actually exist in the tree:

```bash
git ls-files -- '<path pattern from the rule>'
```

An empty result means the rule's pattern does not match anything tracked,
which is often a typo.

### 5. Enforce with the ruleset rule

`CODEOWNERS` by itself only requests reviews; it does not block a merge.
To require an approving review from a code owner, the default-branch
ruleset's `pull_request` rule needs `require_code_owner_review: true`:

```bash
gh api "repos/$REPO/rulesets" --jq '.[] | select(.target=="branch") | {id, name}'
gh api "repos/$REPO/rulesets/<id>" --jq '.rules[] | select(.type=="pull_request")'
```

Show the user the current `pull_request` rule parameters and the proposed
change (`require_code_owner_review: true`), and get explicit authorization
before any write:

```bash
gh api -X PUT "repos/$REPO/rulesets/<id>" --input "$TMPDIR/ruleset.json"
```

See `references/enforcement.md` for the full parameter set and for the
complementary required-reviewer ruleset rule (GA 2026-02-17), which
requires approvals from specific teams scoped to path patterns,
independent of `CODEOWNERS`. GitHub documents this rule as augmenting
CODEOWNERS, not replacing it: `CODEOWNERS` still drives auto-requested
reviewers, while the required-reviewer rule enforces the policy at the
ruleset level. Mention it as an option; do not enable it without the user
asking for it.

### 6. Verify and report

- `CODEOWNERS` file location and content match what the user confirmed.
- `gh api repos/$REPO/codeowners/errors` returns an empty `errors` array
  (or explain the 404 if the file has not been pushed yet).
- Every `@org/team` reference was confirmed to have write access.
- The ruleset's `pull_request.require_code_owner_review` value matches what
  was authorized (report skip if the user declined enforcement).

## Guardrails

- Diff any existing `CODEOWNERS` file before overwriting it; ask before
  replacing content the user did not confirm.
- Never invent a GitHub handle or team slug. Before adding `@org/team` to a
  rule, run `gh api -H 'Accept: application/vnd.github.v3.repository+json'
  orgs/{org}/teams/{slug}/repos/$REPO`. Require `.permissions.push` to be
  `true`. A 404 means the team does not exist, has no access, or is not
  visible to your token. Confirm the slug with
  `gh api orgs/{org}/teams/{slug}` before you ask for an access grant.
- Never mutate the ruleset (`require_code_owner_review` or the
  required-reviewer rule) without explicit user authorization for that
  specific write.
- Re-running this skill on an already-configured repo must be a no-op
  except where the user asks for a change — re-read the current file and
  ruleset state before proposing edits.

## What this skill is NOT for

- Branch rulesets in general (merge queue, required status checks, PR
  review counts) — use `/gh-bootstrap`.
- Community health files (README, LICENSE, CODE_OF_CONDUCT, CONTRIBUTING,
  SECURITY, issue and PR templates) — use `/oss-hygiene`.
- Local git operations unrelated to ownership evidence gathering.
