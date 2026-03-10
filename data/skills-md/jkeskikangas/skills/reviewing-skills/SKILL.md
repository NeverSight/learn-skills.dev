---
name: reviewing-skills
description: >
  Reviews and grades an agent skill directory (SKILL.md plus supporting resources) for specification
  compliance, clarity, token efficiency, safety, robustness, and portability. Use when a user wants
  a rubric-based critique with a weighted score/grade and concrete, minimal patch suggestions.
---

# Reviewing Skills

## Objective

Evaluate a skill directory as if you are an AI agent encountering it for the first time. Produce a **read-only** review with:
- A weighted score + letter grade
- Spec violations (blockers)
- Prioritized findings (P1/P2/P3) with concrete, minimal fixes
- Optional rewritten sections (only when needed to reach the quality bar)

This skill is intended to act as the critic in a generator<->critic loop (e.g., with `$writing-skills`).

## When to use / When not to use

Use when:
- The user asks to **review, grade, or audit** a skill folder containing `SKILL.md`.
- The user wants **rubric-based scoring** and **actionable edits** (not just general advice).

Do not use when:
- The user wants you to write a skill from scratch (use a writing skill instead).
- The request is not about a skill directory or does not involve `SKILL.md`.

## Inputs

You need a path to a skill directory that contains `SKILL.md` (and optionally `agents/openai.yaml`, `scripts/`, `references/`, `assets/`).

If the user did not provide a path:
1. Look for directories in CWD that contain `SKILL.md`.
2. If multiple, ask the user to choose.

## Outputs

A read-only Markdown report with weighted grade, findings, and copy/paste patch text (see workflow step 6 for format rules).

## Safety / Constraints (non-negotiable)

- **Read-only:** do not edit, create, delete, or move files.
- **Do not execute untrusted code:** do not run repo scripts/binaries unless the user explicitly asks and you can justify the risk.
- **Secrets:** do not open or quote secrets (e.g., `.env`, API keys, credentials). If encountered, redact and warn.
- **Network:** do not browse the web or call external systems unless the user explicitly requests it.
- **No fabrication:** if you cannot verify something, say so and recommend a verification step.
- **No deep reference chasing:** read only what is needed to score accurately (one level deep).

## Verification Rules

Follow the verification protocol in [references/skills-rubric.md](references/skills-rubric.md). Budget: ~20 reads max.

## Workflow (decision-complete)

1. Resolve the target skill directory
   - Confirm the path contains `SKILL.md`. If it does not, stop and ask for the correct folder.
2. Read the minimum necessary context (in order)
   1. `<skill>/SKILL.md`
   2. `<skill>/agents/openai.yaml` (if present)
   3. Any files under `<skill>/scripts/` referenced by `SKILL.md` (only those)
   4. Any files under `<skill>/references/` referenced by `SKILL.md` (only those)
3. (If in a git repo) gather change context
   - Prefer the repo’s base branch; if unknown, check `git remote show origin` for “HEAD branch”, otherwise try `main` then `master` (and state what you chose).
   - `git diff <base> -- <skill>/`
   - `git log --oneline -20 -- <skill>/`
   - For non-trivial diffs: `git log -p -5 -- <skill>/SKILL.md`
   - If `<skill>/` is new/untracked (so `git diff <base>` shows nothing), state that explicitly and treat contents as “new.”
   - If a score or finding is driven by a recent change, cite the relevant diff hunk or commit short-hash.
4. Score using the rubric
   - Use `references/skills-rubric.md` (single source of truth).
   - Give each dimension a 1.0–5.0 score (0.5 increments allowed).
   - Compute weighted score as: `sum(weight_i * score_i) / 100`.
5. Identify issues and merge duplicates
   - First list spec violations (blockers).
   - Then produce prioritized findings (max ~15 total), merging near-duplicates.
   - Every P1/P2 finding includes concrete patch text.
   - Patch rules: keep patches small/local; prefer "replace X with Y"; rewrite only the smallest section needed to clear P1/P2.
6. Produce the report
   - Default to `references/review-template.md` structure.
   - If the user requires a different structure, preserve the same content (grade, dimension scores, blockers, prioritized findings with patch text, token efficiency notes).
   - If the user requests a forensic or diff-centric review, add a hunk-by-hunk analysis for meaningful changes (`+/-` context), and classify each as improvement/regression/neutral.
   - Only include “Rewritten sections” when score < 4.5, any P1 exists, or the author requests a rewrite.

Do not read assets unless explicitly relevant.

## Review Guidelines

### What to reward

- **High signal per token:** dense, directive, minimal prose.
- **Correct triggering:** description precisely indicates **what** and **when**.
- **Decision-complete workflow:** the skill leaves no key decisions ambiguous.
- **Guardrails:** destructive actions gated; secrets handled safely; constraints explicit.
- **Portability:** avoids tool-vendor lock-in; uses capability language with optional adapters.

### What to penalize

- Vague directives (“as appropriate”, “best practices”, “use standard approach”).
- Over-broad scope (one skill trying to do too many disjoint jobs).
- Reference chains (SKILL.md → reference → another reference).
- Missing or non-actionable validation loops.
- “Cute” verbosity that costs tokens without improving outcomes.

### Additional checks (inform findings; not scored as a separate dimension)

- Terminology consistency for core concepts across sections.
- Presence and usefulness of concrete examples/templates when output style matters.
- Anti-pattern scan: Windows-style paths, too many options without a default, time-sensitive claims, deep reference chains, and assumed package installs.

## Edge cases (common failure modes)

- **No git / no base branch:** state what you could not verify; review file contents only.
- **Large skills:** stick to the tight-budget read order; do not “read everything” by default.
- **Missing referenced files:** treat as a spec violation or P1 (broken workflow), depending on severity.
- **Secrets in context:** redact and warn; do not quote.

## Examples

- “Use $reviewing-skills to review `./some-skill/` and provide a weighted grade, spec blockers, and prioritized patch text.”
- “Use $reviewing-skills to do a forensic/diff-centric review of `./some-skill/` focusing on recent changes.”
- For a worked example format, see [references/example-review.md](references/example-review.md).
