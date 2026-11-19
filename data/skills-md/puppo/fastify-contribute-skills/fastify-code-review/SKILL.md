---
name: fastify-code-review
description: Use when reviewing a pull request, branch diff, or patch across any Fastify organization repository (fastify/fastify, @fastify/* plugins and utilities, fastify/workflows, or fastify/website). Standardizes the read-only code review flow, technical & governance checklists, evidence-backed finding classification, GitHub suggestion blocks, and the welcoming, concise Fastify maintainer tone on every PR. Pairs automatically with fastify-core, fastify-plugins, fastify-workflows, or fastify-website.
---

# Fastify Code Review Skill (`fastify-code-review`)

Use this skill whenever reviewing a pull request, commit range, or branch diff in any [Fastify](https://github.com/fastify) repository. It enforces a **consistent review flow**, **consistent technical rigor**, and **consistent Fastify maintainer tone** across every PR.

## Core Principles

1. **Strictly Read-Only During Review:**
   - Preserve the user's working tree and index; do not edit, stage, or commit their files during review.
   - Inspect scripts and their lifecycle hooks before execution; a script named `test` or `lint` is not necessarily non-mutating. Run generators and checks that rewrite tracked files only in an isolated temporary checkout of the reviewed revision.
   - Draft review comments locally. Posting reviews or changing PR metadata requires an explicit user request.
2. **Pair with the Matching Repository Skill:**
   - Always combine this skill with the domain skill for the target repository so technical checks match local conventions:
     - `fastify/fastify` -> load [`fastify-core`](../fastify-core/SKILL.md)
     - Fastify plugins and standalone utilities -> load [`fastify-plugins`](../fastify-plugins/SKILL.md), selecting only checks applicable to the package's exported API
     - `fastify/workflows` -> load [`fastify-workflows`](../fastify-workflows/SKILL.md)
     - `fastify/website` -> load [`fastify-website`](../fastify-website/SKILL.md)
3. **Evidence Over Invention:**
   - Every finding must cite an exact `file:line` in the diff and explain the concrete bug, regression, type mismatch, security risk, or documented rule violation.
   - If a PR is clean, say **`LGTM`** clearly. Never manufacture artificial nitpicks to appear thorough.
4. **No Linter Duplication:**
   - Never leave manual comments on indentation, semicolons, quotes, or import ordering that `neostandard` (`eslint`) or `biome` automatically checks—simply report whether `npm run lint` passes or fails.
5. **Fastify Maintainer Tone:**
   - Be welcoming, direct, collaborative, and concise (*"Thanks for the PR!"*, *"Good catch!"*, *"Can we add a regression test for this edge case?"*).
   - Default to a compact verdict, actionable findings, and brief verification evidence. Omit empty sections and repeated summaries; expand only when requested.
   - Provide GitHub ````suggestion` blocks when a verified, self-contained replacement fits an exact changed line range; otherwise explain the required behavior or regression test.

---

## The Standardized 6-Step PR Review Flow

Follow these 6 steps in order on every PR:

### Step 1: Identify Repository & Load Companion Skill
- Record the target repository, PR base SHA, and head SHA (or the explicitly requested local comparison range). Inspect files at that revision to identify the repository archetype, distinguishing registered plugins from standalone utilities.
- Load the corresponding repository skill ([`fastify-core`](../fastify-core/SKILL.md), [`fastify-plugins`](../fastify-plugins/SKILL.md), [`fastify-workflows`](../fastify-workflows/SKILL.md), or [`fastify-website`](../fastify-website/SKILL.md)).

### Step 2: Check PR Metadata, Title & Governance
Read [references/review-flow-and-checklists.md](references/review-flow-and-checklists.md). Establish policy from the target checkout's contribution rules, package scripts, ignore rules, tracked files, and workflows; compare the base when the PR changes those rules.
- **Title, Branch & Version**: Apply the repository's actual requirements. Distinguish ordinary contributions from documented release PRs, where version bumps can be expected.
- **Artifact & Lockfile Hygiene**: Reject unintended generated output according to repository evidence. Core's `build/` sources and generated validators are maintained files; the website's tracked lockfile is valid.
- **RFC Context**: Read linked or included RFCs and relevant PR discussion. Follow the [RFC currency and adherence procedure](references/review-flow-and-checklists.md#rfc-currency-and-adherence) before assessing compliance.
- **Policy Uncertainty**: Ask a question when a material rule cannot be confirmed; do not turn a convention in this skill into an unsupported blocker.

### Step 3: Audit the Diff Across All Affected Areas
Inspect the full diff (`gh pr diff` or `git diff <base>...HEAD`) against the domain rules in the companion skill:
- **Runtime & Architecture**: Encapsulation (`fastify-plugin`), hook lifecycle, `@fastify/error` (`FST_ERR_*`), V8 monomorphic shapes (`Request`/`Reply` in core), security boundaries (prototype poisoning, header/path injection, XSS sanitization in website), and resource cleanup (`onClose`).
- **TypeScript & `.d.ts` Sync**: Every new/changed public option, decorator, hook, or return type in `.js` must be reflected in `index.d.ts` / `types/index.d.ts` / `fastify.d.ts`.
- **Tests & Type Tests**:
  - Runtime bug fixes need regression coverage; public type changes need type tests using the repository's configured runner. Select validation for the affected behavior; docs-only and workflow-only changes do not require unrelated runtime or type tests.
  - Preserve the coverage metrics and thresholds configured in the checkout. Passing unit tests alone does not prove coverage.
  - For Fastify request behavior, prefer `fastify.inject()`; use real sockets with teardown when necessary. Test standalone utilities through their own API.
- **Docs & Workflows**: Verify relevant documentation matches changed public behavior and external actions follow the repository's pinning policy. Relative local workflow references do not take a commit SHA.

### Step 4: Run Local Verification (Read-Only)
- Follow the revision and isolation procedure in [references/review-flow-and-checklists.md](references/review-flow-and-checklists.md). Verify local `HEAD` matches the reviewed head and no local files contaminate results before running checks.
- Use an isolated temporary checkout when revisions differ, local changes are present, or a check regenerates tracked files. If isolation or prerequisites are unavailable, mark the check `Not run` with the reason.
- Record exact commands, exit status, and tested SHA. Report remote CI separately with its revision; never attribute results from another checkout or commit to this PR.

### Step 5: Classify Findings by Severity
Group findings strictly into three levels (or zero findings if clean):
- **`[Blocking]`**: Demonstrated bugs, regressions, missing tests needed for affected behavior or public types, broken contracts, security issues, unintended breaking changes, or confirmed repository-policy/check failures. Missing local prerequisites are a verification limitation, not proof that the PR fails.
- **`[Suggestion]`**: Concrete improvements to performance, readability, test assertions, or idiomatic Fastify patterns that do not block correctness. Include a ````suggestion` block only when its replacement and line range are verified.
- **`[Question]`**: Clarifying questions about design intent, edge cases, or semver expectations.

### Step 6: Produce the Standardized Review Output
Read [references/tone-and-templates.md](references/tone-and-templates.md). Default to:

1. **Verdict** (`Approve (LGTM)` | `Request Changes` | `Comment`) with a short reason when needed.
2. **Findings**, only when present: ordered by severity, with `file:line`, concrete impact, and the requested change. Write each once as a ready-to-post comment; add verified ````suggestion` blocks where applicable.
3. **Brief verification evidence**: repository/range, reviewed base/head, tested revision, exact commands and exit codes, and material limitations. Distinguish local tests, coverage, and remote CI.

Omit empty sections and duplicated summaries. Provide a detailed report or checklist matrix only when requested.

---

## Reference Navigation

| Reference File | When to Read |
|----------------|--------------|
| [references/review-flow-and-checklists.md](references/review-flow-and-checklists.md) | Always read during Steps 2–4 for git/gh inspection commands, governance checks, and repo-specific technical checklists. |
| [references/tone-and-templates.md](references/tone-and-templates.md) | Always read during Steps 5–6 for the Fastify maintainer tone guide, output template, ````suggestion` formatting, and canonical response examples. |
