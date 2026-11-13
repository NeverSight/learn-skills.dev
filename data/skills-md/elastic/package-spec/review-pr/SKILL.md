---
name: review-pr
description: Review a package-spec pull request or branch for completeness and correctness. Use when the user asks to review a PR, check their branch is ready to merge, verify they have not missed required changes, or wants a pre-submission checklist. Accepts a PR number, a branch name, or no argument (current branch vs main).
license: Elastic License (see LICENSE.txt in repository root)
compatibility: Requires git. For PR number resolution, also requires the gh CLI authenticated against elastic/package-spec. For local validation (make check, go test), requires a Go toolchain and make. Compatible with Claude Code (/review-pr), Cursor, GitHub Copilot, Gemini CLI, and other Agent Skills-compatible agents.
metadata:
  spec: https://agentskills.io/specification.md
---

# package-spec PR Review (Agent Skill)

This skill conforms to the **[Agent Skills](https://agentskills.io/specification.md)** open format ([agentskills.io](https://agentskills.io/)).

**This skill does not modify the codebase.** It does not edit source files, run any git
command that modifies state (no commit, push, checkout, reset, stash, merge, or rebase), or
change anything on the branch under review. If an issue is found, describe it and stop — do
not attempt to fix it. The only file it writes is the review report at `.cursor/review-pr-output.md`.

Reviews a branch or pull request against the contribution rules for this repository.
See [references/checklist.md](references/checklist.md) for full rules and examples.

For narrative onboarding (Makefile targets, scaffolding test packages, testing against the integrations repo), see **[CONTRIBUTING.md](../../../CONTRIBUTING.md)** at the repository root. This skill and the checklist focus on **PR completeness** against those practices.

## How to Use This Skill

| Situation | What to do |
| --- | --- |
| **Claude Code** | `/review-pr`, `/review-pr <branch>`, or `/review-pr <PR-number>` |
| **Cursor / Copilot** | Attach this file to your chat and say "review my changes" or paste your diff |
| **Any LLM** | Paste this file as a system message, then provide the output of `git diff main...HEAD` |

---

## Step 1 — Resolve the Target

Determine what to diff based on the input provided:

**If a PR number was given** (e.g., `1140`):

```bash
gh pr view 1140 --repo elastic/package-spec --json headRefName,baseRefName,title,url
git fetch origin <headRefName>
# diff: FETCH_HEAD vs <baseRefName>
git diff <baseRefName>...FETCH_HEAD --stat
git diff <baseRefName>...FETCH_HEAD
```

**If a branch name was given** (e.g., `my-feature`):

```bash
git diff main...<branch> --stat
git diff main...<branch>
```

**If no argument was given** (review current branch):

```bash
git branch --show-current          # confirm we are not on main
git diff main...HEAD --stat
git diff main...HEAD
```

If the current branch is `main` and no argument was given, report that there is nothing to review.

---

## Step 2 — Categorize Changed Files

Using the file list from `--stat`, bucket each changed file into one or more categories:

| Category | File pattern |
| --- | --- |
| **Spec files** | `spec/**/*.spec.yml` |
| **Changelog** | `spec/changelog.yml` |
| **Semantic validators** | `code/go/internal/validator/semantic/*.go` (excluding `*_test.go`) |
| **Validator registry** | `code/go/internal/validator/spec.go` |
| **Validator unit tests** | `code/go/internal/validator/semantic/*_test.go` |
| **Validator integration tests** | `code/go/pkg/validator/validator_test.go` |
| **Test packages** | `test/packages/**` |
| **Compliance packages** | `compliance/testdata/packages/**` |
| **Compliance features** | `compliance/features/*.feature` |

Use the categories internally to pick checklist sections; do not paste the full categorized file list into the report unless it clarifies an extra-review item.

---

## Step 3 — Run the Checklist

Work through each applicable section from [references/checklist.md](references/checklist.md).

Below is a compact version of the checks. The reference file has full rules, edge cases, and
exact examples.

### Contribution process (when relevant)

Consult section **0** in the reference file and [CONTRIBUTING.md](../../../CONTRIBUTING.md#change-proposals).

- Cross-stack or cross-product spec changes should follow the **Change Proposals** process before merge.
- New **package categories** require the **Category Proposals** process.
- If the change is large and the PR does not reference a proposal or tracking issue, add an extra-review note asking the author to confirm process was followed.

### Always: Changelog

- Is `spec/changelog.yml` modified?
  - If not: **flag as missing** (required for all non-trivial changes; dependency-bump PRs
    from Dependabot are the only exception).
- If modified, verify:
  - Entry is under the correct in-development version (the one with `-next` suffix).
  - New entry is at the **bottom** of that version's `changes` list.
  - `description` is a complete sentence ending with a period.
  - `type` is one of: `enhancement`, `bugfix`, or `breaking-change`.
  - `link` points to a valid PR URL or is `TBD` (not empty, not an issue URL unless the
    change originated from an issue with no PR).
  - If the feature is blocked on Kibana/elastic-package: a `# Pending on <url>` comment
    appears directly above the entry.

### If spec files changed

Consult the "Version patches" and "Schema reuse" sections of the reference file.

- For new `properties` or `definitions` that older `format_version` values must **not** include, add
  `versions[].patch` remove operations (see the reference file). **Not** every addition needs a
  patch: if the change is **only** meaningful at the introducing spec version (e.g. a new
  **required** field or other **breaking** change with a clear minimum `format_version`), rely on
  **version scoping** instead of remove patches when appropriate.
- The remove order matters: property `$ref` entries must be removed before the definition
  they reference.
- Shared fields used in multiple spec files must be defined once in
  `spec/integration/manifest.spec.yml` and referenced via `$ref` elsewhere — not duplicated
  inline.

### If semantic validators changed

Consult the "Semantic validators" section of the reference file.

- New validator function: check it is registered in `code/go/internal/validator/spec.go`
  in the `rulesDef` slice, with appropriate `fn`, `since`, and `types` fields.
- Tests: at least one of the following must be present:
  - A `*_test.go` file alongside the validator using `t.TempDir()` (simple/single-file rules).
  - New test cases in `code/go/pkg/validator/validator_test.go` referencing packages in
    `test/packages/` (complex multi-file scenarios).

### If test packages changed

Consult the "Test packages" section of the reference file.

- Prefer scaffolding with **`elastic-package create package`** or, for new data streams in an
  existing package, **`elastic-package create data-stream`** (from that package’s directory), over
  manual copies.
- Each package under `test/packages/` or `compliance/testdata/packages/` must contain:
  `manifest.yml`, `changelog.yml`, `docs/README.md`.
- Any data stream must include a valid ingest pipeline: processors need a `tag` field, and
  there must be an `on_failure` block that sets `event.kind: pipeline_error` and
  `error.message` to a string containing the three Handlebars placeholders.

### If compliance feature files changed

Consult the "Compliance features" section of the reference file.

- Every `Scenario:` must have a `@X.Y.Z` version tag immediately above it.
- A `@skip` tag must always be paired with a `# Pending on <url>` comment on the next line.
- When `@skip` is added, the corresponding `spec/changelog.yml` entry must also have a
  matching `# Pending on <url>` comment.

### If new Go files added

- Every new `.go` file must start with the Elastic license header:

  ```go
  // Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
  // or more contributor license agreements. Licensed under the Elastic License;
  // you may not use this file except in compliance with the Elastic License.
  ```
- Variable and function names must be unabbreviated (e.g., `packageName` not `pkgName`,
  `dataStreamManifests` not `dsManifests`).
- Indentation must use tabs, not spaces.

---

## Step 4 — Run Local Validation

If a Go toolchain and `make` are available in the environment, run at minimum (same order as [CONTRIBUTING.md](../../../CONTRIBUTING.md#testing-your-changes)):

```bash
# Validate spec YAML syntax (fast, always do this after spec changes)
go test ./code/go/internal

# Lint and license headers
make check
```

**Optional (broader validation):** When the diff warrants it, also run `make test` for the full suite ([CONTRIBUTING.md](../../../CONTRIBUTING.md#testing-your-changes)). For changes that should be exercised across many real packages, see **Testing with integrations repository** in [CONTRIBUTING.md](../../../CONTRIBUTING.md#testing-with-integrations-repository) (e.g. `test integrations` PR comment and closing the spawned integrations PR when done).

Record validation outcomes only as described in **Step 5** (short summary per command; on failure, include a small excerpt only). If the toolchain is not available, note `skipped` for those commands.

---

## Step 5 — Write the Report

Write a **short** report to `.cursor/review-pr-output.md`, overwriting any previous run. Use **plain text only** (no emoji or decorative symbols). Aim for roughly one screen of content.

Include **only** what follows. Omit empty sections entirely.

```markdown
# PR review: <branch or PR title>
<!-- reviewed: <ISO date> -->

## Scope

At most 2–4 bullets: what the diff changes, only if that context helps a reviewer. Omit this section if the PR title and `git diff --stat` are enough and nothing needs extra review.

## Extra review

Bullets **only** for items that need human attention: checklist gaps, blockers, open questions, or parts of the change that are easy to get wrong (for example new `versions` patches, new semantic validators, `spec/changelog.yml` entries, compliance `@skip`, or cross-file `$ref`). For each bullet use `path:approximate-line` (or `path` and a short region description) plus **one sentence**. Prefix with `blocker`, `suggestion`, or `question` when useful.

If there is nothing to flag here and validation passed, use a single line instead of a list:

No items flagged for extra review.

## Validation

One line per command you ran, for example: `go test ./code/go/internal: pass`. Use `fail` or `skipped` as appropriate. If a command failed, add a **short** excerpt (failing test name or error lines only), not the full log. If no commands ran, one line: `Validation: skipped (toolchain not available).`
```

**Do not** add per-topic sections (changelog, version patches, tests, etc.) when there is nothing to say. Do not paste full `go test` or `make check` output on success. Do not list files that look fine.

After writing the file, print this message to the user:

```
Review written to .cursor/review-pr-output.md
```

## Validating this skill

After substantive edits to this skill, run (if installed):

```bash
skills-ref validate ./.cursor/skills/review-pr
```
