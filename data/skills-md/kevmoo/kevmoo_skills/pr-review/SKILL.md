---
name: pr-review
description: >-
  Reviews GitHub Pull Requests or local Git branch diffs for defects, removed behavior, and specification drift using a 13-angle rubric and adversarial noise filtering. Use when reviewing a GitHub PR (#N or URL), auditing a local feature branch before opening a PR, or invoked via /pr-review. Don't use for triaging existing PR review comments or CI failures (use pr-triage), multi-repo branch cleanup sweeps (use pr-cleanup), or Google3 Piper changelists (use cl-finalize or review).
key_features:
  - Explicit 3D Paranoia Tiering (Ring, Confidence, One-Way/Two-Way Door) with --deep escalation
  - Two-Axis Evaluation (Linked Issue Spec Traceability + CODING_STANDARDS.md)
  - 13 analytical review angles + Inquisitor Presumption of Theater doctrine
  - 2-Tier ownership action gate (own repo auto-fix vs. external read-only)
---

# GitHub PR Reviewer (`/pr-review`)

A disciplined, senior-grade code reviewer for GitHub Pull Requests and local Git
branches. Powered by the 13-angle evaluation rubric and the adversarial
**Inquisitor Doctrine ("Presumption of Theater")** in [`RUBRIC.md`](RUBRIC.md)
to purge hallucinatory AI fluff, pedantic theater, and unverified assumptions.

---

## 🎯 Primary Capabilities

1. **Explicit 3D Paranoia Tiering (`OQ3`)**: Computes Audience Ring
   (`Ring 0..4B`), Author Domain Confidence (`High|Low`), and Reversibility
   (`🚪 One-Way` vs. `🔄 Two-Way` Door) to select `Standard` (single-pass) or
   `Deep` (multi-subagent parallel) review mode.
2. **Two-Axis Evaluation (`Spec` vs. `Standards`)**: Verifies issue requirement
   traceability (`gh issue view <N>`) alongside `~/.agents/CODING_STANDARDS.md`
   and the 13-angle defect rubric in [`RUBRIC.md`](RUBRIC.md).
3. **Adversarial Inquisitor Gating & Clickable Permalinks**: Filters every
   candidate finding through the Five Inquisitorial Filters in
   [`RUBRIC.md`](RUBRIC.md) and links directly to GitHub source lines
   (`https://github.com/<owner>/<repo>/blob/<sha>/<file>#L<start>-L<end>`).
4. **2-Tier Ownership Action Gate (`OQ1`)**: Adapts `ask_question` defaults
   between owned `kevmoo/*` branches (auto-fix + `kscripts pr-check`) and
   external/peer PRs (strictly read-only local checkout).

---

## 🛠️ Execution Protocol

### Step 1: Pre-Flight Scope, Ownership & 3D Paranoia Classification

1. **Target & Ownership Detection (`OQ1`)**:
   - **Explicit PR (`#N` or URL)**:
     ```bash
     gh pr view <PR> --json author,headRepositoryOwner,headRepository,headRefName,baseRefName,headRefOid,number,title,body,url
     gh pr diff <PR>
     ```
   - **Local Branch / Worktree (no arguments)**:
     ```bash
     TARGET_BASE=$(git merge-base origin/main HEAD 2>/dev/null || git merge-base origin/master HEAD 2>/dev/null || git merge-base main HEAD)
     git diff ${TARGET_BASE}..HEAD
     gh pr view --json author,headRepositoryOwner,headRefName,number,title,url,headRefOid 2>/dev/null
     ```
   - Classify ownership into two tiers:
     - **Tier 1 (Own Repo `kevmoo/*` + Author `kevmoo` /
       `$(gh api user --jq .login)` with `headRefName` checked out locally, or
       local feature branch)**: Local remediation and test execution
       (`kscripts pr-check`) enabled.
     - **Tier 2 (External/Peer PR, non-`kevmoo` author, or PR branch not checked
       out locally)**: Strictly read-only local checkout.

2. **Linked Issue, Spec & Prior Review Thread Extraction (`FU1`)**:
   - When a PR links an issue (`Fixes #N`, `Closes #N`, or prompt issue URL),
     fetch the specification contract:
     ```bash
     gh issue view <N> --json title,body
     ```
   - On explicit PRs with prior review rounds, fetch existing review threads
     (resolved and unresolved) to respect settled design decisions and skip
     previously addressed feedback:
     ```bash
     gh api graphql -F owner='{owner}' -F name='{repo}' -F pr={pr_number} -f query='query($owner:String!, $name:String!, $pr:Int!) { repository(owner:$owner, name:$name) { pullRequest(number:$pr) { reviewThreads(first:100) { nodes { isResolved path line comments(first:10) { nodes { author { login } body } } } } } } }'
     ```

3. **3D Paranoia Header & Review Mode Selection (`OQ3`)**:
   - Always compute and render at the top of `pr_review_<PR>.md` and in visible
     chat:
     `🛡️ Paranoia Tier: Ring <0..4B> (<Label>) · Confidence: <High|Low> · Door: <🚪 One-Way | 🔄 Two-Way> -> Review Mode: <Standard | Deep>`
   - **Ring Defaults**:
     - **`Ring 0-2` (`kevmoo/*` personal dotfiles, skills, scripts)**: Default
       to `Review Mode: Standard` (single-pass review across the 13 angles)
       unless `--deep` / `--paranoid` is passed or `Door: 🚪 One-Way`.
     - **`Ring 3-4` (`kevmoo/*` published `pub.dev` packages, `dart-lang/*`,
       `flutter/*`, `google/*`, or low-confidence C++/VM/Wasm/Skwasm/WIMP
       domains) or `Door: 🚪 One-Way` (public API/wire/schema changes)**:
       Default to `Review Mode: Deep` (multi-subagent parallel angle audit +
       adversarial verification).
   - Support `--deep` (`--paranoid`) as an upfront flag to force
     `Review Mode: Deep` on any ring.

---

### Step 2: Two-Axis Grounding (`Spec` + `CODING_STANDARDS.md`)

Inspect complete modified files (`view_file`) along with callers and SDK/package
dependencies rather than diff hunks in isolation.

1. **Axis A — Spec & Issue Contract Traceability (`FU1`)**:
   - Cross-check every requirement in the linked issue (`gh issue view <N>`)
     against the implementation and test suite (`Met ✅`, `Partial ⚠️`,
     `Unmet ❌`, `Out-of-Scope ➖`). Flag unwired CLI flags or missing
     acceptance criteria.
2. **Axis B — Dart & Package Standards (`~/.agents/CODING_STANDARDS.md`)**:
   - Audit Dart diffs against `~/.agents/CODING_STANDARDS.md`:
     - **Deep Externally, Pure Internally**: Keep `lib/<pkg>.dart` and `api.txt`
       minimal, and use pure private functions (`_computeX(input) -> output`)
       for internal decomposition.
     - **Load-Bearing Library Boundary Rule**: Extract a standalone `lib/src/`
       library (`Tier 1`) only when zero `_private` visibility widening is
       needed; use `part` / `part of` (`Tier 2`) when crossing `sealed`,
       `final`, `interface`, `base`, `._()`, or `_private` class members so
       `_private` members stay library-scoped.
     - **Public API Surface Verification**: When refactors extract helpers
       across files, verify public API stability with
       `dart run api_summary@^1.1.0` (`--check` if `api.txt` exists, or
       before/after diff).

---

### Step 3: Adversarial Evaluation (`RUBRIC.md`)

1. **Sweep the 13 Angles in [`RUBRIC.md`](RUBRIC.md)**:
   - _1. Line Scan_ · _2. Removed Behavior_ · _3. Cross-File Tracer_ · _4.
     Language Pitfalls_ · _5. Invariants & Wrappers_ · _6. Error Handling_ · _7.
     Testing (Anti-Tautology & Public-Entrypoint Seams)_ · _8. Reuse_ · _9.
     Simplification_ · _10. Efficiency_ · _11. Altitude_ · _12. Readability &
     Conventions_ · _13. Cyclomatic Complexity_.
   - In `Review Mode: Deep`, run deterministic CLI verification (`dart format`,
     `dart analyze --fatal-infos`, `cognitive_complexity`, `dart test`) in the
     parent agent, and dispatch read-only subagents (`Model: "flash"`) across
     bounded file slices (`<= 10` files per subagent) and angle clusters before
     running the Inquisitor pass. Have each subagent return its markdown
     findings directly in its response message so the parent agent can
     synthesize and write `pr_review_<PR>.md` inside the parent session's
     artifact sandbox.
2. **Execute Inquisitor Filters ("Presumption of Theater")**: Discard any
   finding matching `[DISMISSED: INVENTED_ARCHITECTURE]`,
   `[DISMISSED: PARANOIA]`, `[DISMISSED: PEDANTIC_ESCALATION]`,
   `[DISMISSED: HARMLESS]`, or `[DISMISSED: HALLUCINATED_API]`.
3. **Assign Severity**: 🚨 `[BLOCKING]`, 💡 `[SUGGESTION]`, or 🧹
   `[HYGIENE_NIT]` (suppress nits if zero blocking/suggestions exist).

---

### Step 4: Two-Layer Report Formatting (`Internal Proof` vs. `Outbound Comment`)

Save the report to `<appDataDir>/brain/<conversation_id>/pr_review_<PR>.md`
using the active conversation's own `<conversation_id>` (if running inside a
delegated subagent, return the markdown directly in your response for the parent
agent to write `pr_review_<PR>.md`, and echo the Paranoia Header in visible
chat).

**Separate Internal Proof from Outbound Comments**: Keep mechanical call-site
traces and rubric checks in **`Internal Proof (Do Not Post)`** for the local
reviewer gate, and write a self-contained **`Outbound Inline Comment`** capped
at **`<= 50 words` (2-3 sentences)** that states only **(1) what breaks or
regresses** and **(2) the concrete fix**.

```markdown
# Code Review: <Repo> PR #<Number> - <PR Title>

🛡️ Paranoia Tier: Ring <0..4B> (<Label>) · Confidence: <High|Low> · Door: <🚪 One-Way | 🔄 Two-Way> -> Review Mode: <Standard | Deep>

**PR**: [<owner>/<repo>#<number>](https://github.com/<owner>/<repo>/pull/<number>) | **Author**: `<author>` | **Head**: `<headRef>` (`<headSHA>`)
**Verdict**: `✅ Approved` | `⚠️ Approved with suggestions` | `❌ Changes requested`

## Executive Summary
- <1-2 bullet summary of change intent, review outcome, and Inquisitor filter count>

### Spec & Issue Contract Traceability
| Requirement | Status [Met ✅ / Partial ⚠️ / Unmet ❌ / Out-of-Scope ➖] | Evidence (file:line & test) |
| :--- | :--- | :--- |
| <Requirement from issue #N> | Met ✅ | `lib/foo.dart:42`, `test/foo_test.dart:18` |

## Findings

### 🚨 Blocking Issues
- [ ] [**path/to/file.dart#L42-L48**](https://github.com/<owner>/<repo>/blob/<sha>/path/to/file.dart#L42-L48)
  - **Internal Proof (Do Not Post)**: <Call-site trace, invariant check, and why alternatives fail Inquisitor filters.>
  - **Outbound Inline Comment (`<= 50 words`)**:
    > <1 sentence stating what breaks/throws + 1 sentence or `suggestion` block with the fix. Zero call-stack narration.>

### 💡 Suggestions
- [ ] [**path/to/file.dart#L105**](https://github.com/<owner>/<repo>/blob/<sha>/path/to/file.dart#L105)
  - **Internal Proof (Do Not Post)**: <Verification of caller fan-in, complexity delta, or test seam.>
  - **Outbound Inline Comment (`<= 50 words`)**:
    > <1-2 sentences stating the simplification or edge case + concrete fix.>

### 🧹 Hygiene Nits
- [ ] [**path/to/file.dart#L12**](https://github.com/<owner>/<repo>/blob/<sha>/path/to/file.dart#L12)
  - **Outbound Inline Comment (`<= 25 words`)**:
    > <Direct 1-line nit.>
```

---

### Step 5: 2-Tier Interactive Action Gate (`ask_question`) & Posting Hygiene

Present the `ask_question` gate tailored to the Ownership Tier (`OQ1`) and
`Review Mode` (`OQ3`):

- **Tier 1 (Own Repo `kevmoo/*` + Author `kevmoo` or local feature branch)**:
  1. `"(Recommended) Auto-fix valid findings locally, run tests (kscripts pr-check), and stage/push"`
  2. `"Keep findings in local report artifact"`
  3. `"Select findings to post inline to GitHub"`
  4. _(Include whenever `Review Mode: Standard` was used)_
     `"Escalate to Deep / Paranoid Review (--deep multi-agent pass)"`
- **Tier 2 (External/Peer PR or non-`kevmoo` author — Strictly Read-Only Local
  Checkout)**:
  1. `"(Recommended) Keep findings in local report artifact"`
  2. `"Select findings to post inline to GitHub"`
  3. _(Include whenever `Review Mode: Standard` was used)_
     `"Escalate to Deep / Paranoid Review (--deep multi-agent pass)"`

**Outbound Posting Guardrails (When Option
`"Select findings to post inline to GitHub"` Is Chosen)**:

- **Verify Diff-Hunk Bounds Before Inline Anchoring**: Because Step 2 inspects
  complete modified files (`view_file`), a finding may fall on a pre-existing
  line outside the modified `@@ -a,b +c,d @@` diff hunk, and GitHub's Pull
  Request Review API resolves inline `comments[].line` anchors only within
  modified diff hunks (returning `HTTP 422: Line could not be resolved` outside
  the hunk). Check each surviving finding's line number against
  `git diff --unified=0` (or `gh pr diff <PR>`) before offering inline anchors:
  - **In-hunk lines**: Anchor inline via `comments[].line` (`side: "RIGHT"`).
  - **Out-of-hunk / pre-existing lines**: Label as
    `(Pre-existing, outside diff hunk)` in the report and place in the top-level
    review `body` with a blob permalink
    (`https://github.com/<owner>/<repo>/blob/<sha>/<path>#L<line>`).
- **Post Only the Outbound Comment Text**: In GitHub review comments, include
  only the `Outbound Inline Comment` prose (`<= 50 words`) and any `suggestion`
  block, keeping `Internal Proof` traces and severity badges (`🚨`, `💡`) in the
  local report artifact.
- **Keep Top-Level Review Body Minimal**: Set the top-level GitHub review `body`
  to `""` when all posted comments are in-hunk inline comments, populating
  `body` only when routing an out-of-hunk note or a user-requested summary lead.
