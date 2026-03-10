---
name: writing-rubrics
description: >
  Creates or updates rubric Markdown files (and their review-template/prompt integration) with consistent
  grade bands, P1/P2/P3 definitions, and evidence-backed verification rules. Use when: the user asks to
  add a new rubric, align/consolidate rubrics, or sync rubric expectations with reviewer templates/prompts.
---

# Writing Rubrics

## Objective

Create or update rubric documents in this repo and keep their integration points in sync:
- Rubric files (typically under `*/references/*rubric*.md`)
- Reviewer report templates (typically `*/references/review-template.md`)
- Reviewer prompts (`*/agents/openai.yaml`)

## When to use / When not to use

Use when:
- The user asks to create, edit, align, or consolidate rubric files (especially `*/references/*rubric*.md`).
- The user asks to sync rubric expectations with reviewer templates (`**/references/review-template.md`) or reviewer prompts (`**/agents/openai.yaml`).

Do not use when:
- The user wants a rubric-only review/grade without editing (use the review prompt at [references/review-prompt.md](references/review-prompt.md) directly).
- The user wants to write a non-rubric skill or policy doc unrelated to rubric meta-patterns.

## Safety / Constraints (non-negotiable)

- Never read, request, or paste secrets.
- Do not browse the web or call external systems unless the user explicitly requests it.
- Keep diffs small: change only the rubric meta-pattern or the user-requested rubric content.
- Before making bulk edits across multiple rubrics/templates, summarize the planned changes and get approval.

## Quality Bar (default)

Target outcome:
- **No spec violations**, and
- **Weighted score ≥ 4.5/5.0** (A- or better), and
- **No P1 findings** in a critic review

The review prompt (contains scoring dimensions and review workflow): [references/review-prompt.md](references/review-prompt.md) (single source of truth for grading rubric documents).
The review report template: [references/review-template.md](references/review-template.md).

## Canonical Rubric Meta-Pattern (repo default)

Apply these conventions across rubrics unless a rubric explicitly documents a justified exception:

- **Grade bands**
  - **A:** 4.5–5.0
  - **B:** 3.5–4.49
  - **C:** 2.5–3.49
  - **D:** 1.5–2.49
  - **F:** < 1.5
- **Findings priorities**
  - **P1 (Critical):** likely to cause broken workflows, unsafe actions, or repeated failure loops.
  - **P2 (Important):** likely to waste tokens/time, reduce output quality, or cause repeated clarification.
  - **P3 (Nice):** polish and future-proofing.
- **Evidence-backed verification**
  - Prefer **PASS/FAIL/SKIP** reporting for checks.
  - Use **SKIP** when verification would require executing code or accessing secrets.
  - Do not claim **FAIL** without evidence (file path + what was checked).

## Workflow (decision-complete)

1. Discover rubric files
   - Find rubric markdown files under the repo (default: `*/references/*rubric*.md`).
   - If the user provided paths, restrict to those.
2. Decide scope
   - **Single-file edit:** only the requested rubric changes.
   - **Alignment pass:** apply the Canonical Rubric Meta-Pattern across all discovered rubrics.
3. Ensure the linter is available
   - If `packages/skillcheck/dist/` exists (inside this repo), use: `node packages/skillcheck/bin/skillcheck.js`
   - Otherwise, build it first: `cd packages/skillcheck && npm ci && npm run build`
   - Outside this repo: `npx skillcheck` (not yet published; skip validation and note it was skipped if unavailable)
4. Optional preflight (recommended)
   - Run the linter with `--rubrics-only` on the repo skills directory to locate drift in grade bands, P-definitions, and evidence-backed verification sections.
   - Run `npx agnix <skill-dir>` on any skill directories that will be modified.
   - Only run the linter with `--fix` after summarizing the expected file changes and getting explicit user approval (it writes files).
5. Apply changes (write)
   - Update rubric(s) to match the canonical meta-pattern.
   - If a rubric requires a domain-specific verification section, keep it domain-specific but enforce the evidence rule.
6. Sync integration points (write)
   - Ensure reviewer templates include a “Verification Results” section if the rubric expects evidence-backed checks.
   - Ensure reviewer prompts mention the correct rubric path(s).
7. Validate
   - If preflight reports drift, propose the smallest set of edits to resolve it (by file), then re-run the preflight.
   - For any changed skill directories, run both linters on each:
     - `node packages/skillcheck/bin/skillcheck.js <skill-dir>`
     - `npx agnix <skill-dir>`

### Quality Gate

Two-phase review after validation. Target: Quality Bar (score >= 4.5, no P1 findings).

#### Phase 1: Self-critic review

Review the changed rubric(s) and integration points for:
- **Internal consistency** — grade bands, P-definitions match the canonical meta-pattern.
- **Completeness** — all dimensions have 1/3/5 criteria.
- **Cross-reference accuracy** — reviewer templates/prompts reference correct rubric paths.

Fix inline or flag. If score < 4.5 or P1 findings remain, fix before proceeding to Phase 2.

#### Phase 2: Fresh-context subagent review

Run a **fresh-context critic** pass using [references/review-prompt.md](references/review-prompt.md):
- If your environment supports subagents, **spawn a fresh-context subagent** with the review prompt. Otherwise, perform the review directly following the prompt instructions.
- Apply **P1 + P2** fixes (P3 last).
- Re-run validation.
- Repeat up to **3 loops**, stop early when the Quality Bar is met.

## Edge Cases

- **Linters not available (no Node.js / npx):** warn the user; skip validation but note it was skipped in the deliverable.
- **No rubric files found:** stop and ask the user for the correct path(s) before proceeding.

## Examples

- "Use $writing-rubrics to create a new rubric for reviewing deployment configs."
- "Use $writing-rubrics to align all rubrics in this repo to the canonical meta-pattern."
- "Use $writing-rubrics to sync the reviewer template with the updated skills-rubric.md."

## Output Rules

- Keep rubric prose dense and scannable (tables/bullets preferred).
- Avoid time-sensitive claims unless the rubric explicitly requires web browsing and says so.
