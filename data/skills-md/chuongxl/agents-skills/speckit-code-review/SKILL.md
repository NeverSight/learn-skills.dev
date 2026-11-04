---
name: speckit-code-review
description: |
  Deep line-by-line code review against the feature spec at specs/<feature-folder>/spec.md,
  produced by either speckit.specify (GitHub Spec Kit) or superpowers:brainstorming.
  Produces strict JSON pass/fail with business coverage, missing requirements, code issues, security issues, architecture issues, and unit test coverage.
  Triggers: "speckit code review", "review with spec", "compare code to spec.md", "spec coverage audit",
  "invoke speckit-code-review", "run speckit-code-review".
compatibility: Runs on GitHub Copilot, Claude Code, OpenCode, and Hermes Agent. Discovered from ~/.agents/skills/, ~/.claude/skills/, ~/.config/opencode/skills/, or ~/.hermes/skills/. Requires git, bash, and a spec at specs/<feature-folder>/spec.md.
license: MIT
allowed-tools: bash glob grep view create edit
metadata:
  specification: agentskills.io/specification
  output_contract: strict-json
  author: Alex Nguyen
  version: "0.0.4"
---

# Speckit Code Review

Compare implementation code to `specs/<feature-folder>/spec.md` and return a strict JSON verdict.
The spec may come from `speckit.specify` (usually already has `FR-*`/`NFR-*` IDs) or from
`superpowers:brainstorming` (narrative design doc, usually no IDs) — both are reviewed identically.

**Always run inline.** Never dispatch as a background task or sub-agent; the caller needs the JSON in-band.

Portability note: `allowed-tools` uses GitHub Copilot-style names (`bash glob grep view create edit`).
Claude Code and OpenCode expose the same capabilities under their own names (`Bash`, `Read`, `Edit`,
`Write`, `Glob`, `Grep`). Hermes Agent exposes them as `terminal`, `read_file`, `patch`,
`write_file`, `search_files`. The review procedure below is identical on all four hosts.

## Inputs

- `spec.md` for the target feature. If no path is given, resolve from `specs/*/spec.md` using the
  current branch name or changed files; ask the user only if still ambiguous.
- Review scope = current git change set (staged + unstaged, incl. renames/deletes), evaluated in
  the current working directory. Optional `base_ref` input (a commit/ref, e.g. the merge-base with
  the base branch): when provided, scope = the **union** of `git diff <base_ref>...HEAD` and the
  working-tree change set, so committed feature work is reviewed even when the tree is clean.
  `speckit-auto` always passes this. When invoked from `speckit-auto`, the caller must run this
  skill inline from inside the Stage 01 linked worktree, never from the base checkout.
- **Submodule expansion (mandatory when `.gitmodules` exists):** a top-level `git diff`/`git
  status` only ever shows a changed submodule as a single gitlink entry (mode `160000`), never the
  files changed inside it — reviewing that entry alone is reviewing nothing. Resolve every area's
  "git change set" as follows before any area review runs:
  1. Compute the top-level change set as above. For every changed path that appears in
     `.gitmodules`, that path is a submodule, not a regular file.
  2. For each changed submodule path: `old_sha = git rev-parse <base_ref>:<path>` (skip if the
     path didn't exist at `base_ref` — treat every tracked file in the submodule as new),
     `new_sha = git rev-parse HEAD:<path>`.
  3. Get its real file-level diff: `git -C <path> diff <old_sha> <new_sha>` (committed range)
     **union** `git -C <path> diff` and `git -C <path> status --porcelain` (uncommitted work
     inside the submodule). Prefix every resulting file path with `<path>/` so it composes with
     the rest of the scope.
  4. Replace the gitlink entry in the change set with these expanded file paths. The change set
     every area below operates on is this expanded set, never the raw gitlink line.
  5. Log one line per expanded submodule: `[Code Review] Expanded submodule <path>:
     <old_sha>..<new_sha>, <n> file(s)`.
  Nested submodules (a submodule with its own `.gitmodules`) are out of scope — flag any found as
  a `CODE-*` finding recommending manual review instead of expanding recursively.

## Spec ID

`<spec-id>` drives all output paths. Derive it from the feature folder name — never invent one, so
reruns resolve to the same paths:

| Folder | `<spec-id>` | Rule |
|---|---|---|
| `010-user-login` | `010` | leading numeric prefix |
| `ddm-6157-user-login` | `ddm-6157` | leading issue key (`<letters>-<digits>`) |
| `some-feature` | `some-feature` | whole folder name |

Lowercase; strip any character outside `[a-z0-9-]`.

## Requirement Checklist

Step 1 must always yield a numbered checklist.

- **IDs present** → use verbatim; set `requirements_source: "declared"`.
- **No IDs** → synthesize; set `requirements_source: "synthesized"`:
  1. Extract one testable statement per requirement, in priority order: acceptance criteria,
     requirements/behaviour sections, user stories, explicit constraints, any must/should sentence.
  2. Classify `FR-` (functional) vs `NFR-` (performance, reliability, security posture, scalability,
     maintainability, compliance, UX).
  3. Number in document order so IDs stay stable across reruns.
  4. Record each as `{id, statement, spec_anchor}` under `synthesized_requirements` in the
     `business-gap` detail file, so findings trace back to the spec.

If zero requirements are extractable, return `failed` with one `FR-000` fix telling the user to add
testable requirements to the spec. Never return `pass` against an empty checklist.

## Procedure

1. Build the requirement checklist (see above).
2. Resolve the git change set as review scope (union with `git diff <base_ref>...HEAD` when a
   `base_ref` was passed), applying the Submodule Expansion rules above when `.gitmodules` exists.
   This expanded set is what every area below means by "the git change set" — no area re-derives
   it independently.
3. **Project guidelines (conditional)** — if `docs/guidelines/architecture.md` exists, load
   [references/project-guidelines-review.md](references/project-guidelines-review.md) and follow its
   Steps 1–4 to load only the guideline files matching the changed-file categories. Skip silently
   if that file is absent.
4. Run each standard area — load its reference file, run the review, then **discard it from context**
   before loading the next:

   | Area | Reference | Issue IDs |
   |---|---|---|
   | Business Gap | [business-gap.md](references/business-gap.md) | `FR-*`, `NFR-*` |
   | Code Quality (incl. conditional SonarQube MCP scan) | [code-quality.md](references/code-quality.md) | `CODE-*` |
   | Security | [security.md](references/security.md) | `SEC-*` |
   | Architecture | [architecture.md](references/architecture.md) | `ARCH-*` |
   | Unit Test Coverage (last) | [unit-test-coverage.md](references/unit-test-coverage.md) | `TEST-*` |

5. If guideline files were loaded in step 3, run the advanced pass (Step 5 of
   project-guidelines-review.md) and merge its findings into the standard results, tagging each with
   `guideline_source`.
6. `Business cover = round(covered / total * 100)`.
7. Write `state_file`, plus one detail file **per category that has issues**. Skip empty categories;
   on `pass` write only `state_file`.
8. Build `fixes` from all **blocking** findings ordered high → medium → low severity, then keep
   only the **top 3** inline. Every finding is blocking except a `TEST-*` advisory gap (see
   unit-test-coverage.md Step 4): those are recorded in `unit-tests.json` for visibility only and
   never enter `fixes` or count toward step 9. The rest of the blocking findings live in
   `state_file` and the category detail files.
9. `status` = `pass` only if the blocking-finding count is zero **and** coverage ≥ 80% (or `N/A`)
   **and** the checklist is non-empty; otherwise `failed`. `fixes` reflects the same blocking set,
   so `fixes` empty and blocking-finding count zero always agree.

## Output Contract

Return **exactly one compact JSON object**, ≤ 400 tokens, no markdown, no prose outside the JSON.
Field names are literal (keep spaces and capitalization). Never mirror verbose findings inline —
they already live in the files.

| Field | Value |
|---|---|
| `status` | `"pass"` or `"failed"` |
| `Business cover` | percent string, `"0%"`–`"100%"` |
| `unit-test-coverage` | percent string, or `"N/A (no test runner detected)"` — `N/A` counts as passing |
| `state_file` | `.speckit/review-<spec-id>-<ts>/state.json` — ordered issue inventory + next fix queue, so speckit-auto can resume without reloading findings |
| `detail_files` | map of category → path; `{}` on pass. Keys: `business-gap`, `architecture`, `security`, `code-quality`, `unit-tests`, each at `.speckit/review-<spec-id>-<ts>/<key>.json` |
| `fixes` | `[]` on pass; else ≤ 3 objects with exactly `id`, `file`, `method`, `lines`, `action` |

`fixes` entry fields:

- `id` — prefix selects the detail file: `FR-*`/`NFR-*` → business-gap, `ARCH-*` → architecture,
  `SEC-*` → security, `CODE-*` → code-quality, `TEST-*` → unit-tests
- `file` — relative path · `method` — `Class::method` or function name
- `lines` — range like `"88-140"`, or `"new"` when the file/method must be created
- `action` — one imperative sentence, no sub-bullets, specific enough to act on **without** opening
  the detail file

```json
{
  "status": "failed",
  "Business cover": "70%",
  "unit-test-coverage": "61.2%",
  "state_file": ".speckit/review-010-1722348000/state.json",
  "detail_files": {
    "business-gap": ".speckit/review-010-1722348000/business-gap.json",
    "security": ".speckit/review-010-1722348000/security.json",
    "unit-tests": ".speckit/review-010-1722348000/unit-tests.json"
  },
  "fixes": [
    {"id": "FR-004", "file": "src/account/service.ts", "method": "AccountService::createAccount", "lines": "88-140", "action": "Add password minimum-length validation (>=8 chars) before calling hashPassword"},
    {"id": "SEC-001", "file": "src/auth/password.ts", "method": "validatePassword", "lines": "5-20", "action": "Enforce min 12 chars, 1 uppercase, 1 digit, 1 symbol in password policy"},
    {"id": "TEST-001", "file": "src/account/service.spec.ts", "method": "AccountService::createAccount", "lines": "new", "action": "Add test: password shorter than 8 chars throws ValidationException"}
  ]
}
```

A passing result is the same shape with `"status": "pass"`, `detail_files: {}`, `fixes: []`.

## Quality Bar

- Never report `pass` while a blocking finding exists (`fixes` non-empty), coverage < 80%, or the
  checklist is empty. A `TEST-*` advisory gap (unit-test-coverage.md Step 4, coverage already
  ≥ 80%) is not a blocking finding and never fails a pass on its own.
- Keep verbose analysis in the category files; the inline object stays under 400 tokens.
- Severity scale for every area: `high` = exploitable or breaks a requirement/invariant;
  `medium` = degrades correctness, security posture, or maintainability; `low` = cosmetic or
  non-exploitable.
