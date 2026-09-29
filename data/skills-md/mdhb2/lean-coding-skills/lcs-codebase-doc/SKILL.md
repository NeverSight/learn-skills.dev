---
name: lcs-codebase-doc
description: 'use this skill when the user explicitly asks to map, document, inspect, analyze, understand, or onboard into an existing codebase or repository. trigger for prompts like "map this codebase", "document this architecture", "onboard me to this repo", "create codebase docs", "analyze this repository", or "help me understand this codebase". do not trigger for routine feature implementation, bug fixes, narrow code edits, single-file refactors, or isolated programming questions unless the user asks for repository-level discovery.'
---

# LCS Codebase Doc

Map existing repositories into evidence-based docs for onboarding, architecture discovery, technical review, and long-term maintainability.

## Mode selection (required before execution)
Before any scan or documentation step, ask user to choose exactly one mode by number only:

1. `Quick Update`
   - Focus on latest changes and update only impacted sections in existing docs.
2. `Standard Refresh`
   - Run full scoped scan and refresh all existing docs in place.
3. `Rebuild Docs`
   - Recreate content for all seven docs from scratch in `.lcs/codebase/`.

Rules:

- Do not start Phase 1 before user selects `1`, `2`, or `3`.
- Accept numeric input only.
- If input is invalid, ask one more time with the same three options.
- After valid input, print `Selected mode: <name>` and continue.
- If docs already exist in `.lcs/codebase/`, never overwrite full files in mode `1` or mode `2`; update sections in place.
- Full-file regeneration is allowed only in mode `3`.

## OKF Frontmatter & Writing Safety

- When creating codebase documentation files (`.lcs/codebase/*.md`), include YAML frontmatter following the schema in `../lcs-shared/contract.md` with `artifact_type: codebase_doc`.
- Follow the Artifact Writing Safety rules in contract.md — generate content first, write one file, verify, stop on failure.

## Output contract
Before finishing, ensure exactly these files exist under `.lcs/codebase/`:

- `.lcs/codebase/STACK.md`
- `.lcs/codebase/STRUCTURE.md`
- `.lcs/codebase/ARCHITECTURE.md`
- `.lcs/codebase/CONVENTIONS.md`
- `.lcs/codebase/INTEGRATIONS.md`
- `.lcs/codebase/TESTING.md`
- `.lcs/codebase/CONCERNS.md`
- `.lcs/codebase/CHAIN-OF-TRUTH.md` *(Chain of Truth Report — written in Phase 4)*

Rules for every doc:

- Base claims only on verifiable evidence from source files, manifests, configs, docs, git history, or terminal output.
- Add an `Evidence` section with concrete file paths.
- Use `[TODO]` when evidence is missing.
- Use `[ASK USER]` for product/team intent, ownership, or decisions requiring human clarification.
- Separate stated intent from actual implementation.
- Never guess or invent architecture.

## Workflow checklist
- [ ] Mode selection: Ask and confirm `1|2|3`, then print selected mode
- [ ] Phase 1: Create `.lcs/codebase/`, run scan, read intent documents from `.lcs/docs/`
- [ ] Phase 2: Investigate each documentation area
- [ ] Phase 3: Populate all seven docs in `.lcs/codebase/`
- [ ] Phase 4: Validate docs, repair unsupported claims, write `.lcs/codebase/CHAIN-OF-TRUTH.md`, present findings

## Phase 1: Scan and read intent
1. Create output directory using host shell.
   - Unix-like example: `mkdir -p .lcs/codebase`
   - PowerShell example: `New-Item -ItemType Directory -Force -Path ".lcs/codebase"`
2. Run bundled scan script from target project root.
   - Unix-like example: `python3 "$SKILL_ROOT/scripts/scan.py" --output .lcs/codebase/.codebase-scan.txt`
   - PowerShell example: `python "$SKILL_ROOT/scripts/scan.py" --output .lcs/codebase/.codebase-scan.txt`
   - If `python` is unavailable on Windows, use: `py -3 "$SKILL_ROOT/scripts/scan.py" --output .lcs/codebase/.codebase-scan.txt`
   - `$SKILL_ROOT` is absolute path to `skills/lcs-codebase-doc`.
3. Read intent docs in `.lcs/docs/` before deep source inspection.
4. Prioritize files and content signals: README, PRD, TRD, ROADMAP, SPEC, DESIGN, ARCHITECTURE, CONTRIBUTING, ADR, planning notes, product requirements, technical requirements, implementation plans, decision records.
5. If `.lcs/docs/` missing or no relevant docs, mark `[TODO]` or `[ASK USER]` where needed.
6. Summarize stated intent separately from observed implementation.

## Phase 2: Investigate
Use `.lcs/codebase/.codebase-scan.txt` and direct inspection.

Scope rules for investigation:

- Inspect project source, configs, and manifests only.
- Ignore hidden directories (`.*`) except `.lcs`.
- Within `.lcs`, read only `.lcs/docs/` as intent source.
- Root dot-files are allowed (for example `.env.example`, `.gitlab-ci.yml`).
- Do not inspect `.github/`.
- Do not inspect `skills/`, `vendor/`, or generated/dependency/build/cache folders.

- Primary questions and validations: `references/inquiry-checkpoints.md`
- Ambiguous stack detection: `references/stack-detection.md`

Cover at least:

- Language/runtime detection
- Package manager detection
- Dependency classification (production vs development)
- Entry points and directory structure
- Architecture/module boundaries and conventions
- Integrations and environment configuration
- Testing setup and CI/CD
- Containerization and orchestration
- Security/compliance tooling
- Performance/benchmark markers
- TODO/FIXME/HACK markers
- High-churn files from git history (if available)

## Phase 3: Populate templates
Copy templates from `assets/templates/` to `.lcs/codebase/` and complete in order:

1. `STACK.md`
2. `STRUCTURE.md`
3. `ARCHITECTURE.md`
4. `CONVENTIONS.md`
5. `INTEGRATIONS.md`
6. `TESTING.md`
7. `CONCERNS.md`

## Phase 4: Validate and report
Before final response:

1. Validate each doc using `references/inquiry-checkpoints.md`.
2. Ensure every non-trivial claim has evidence.
3. Replace unsupported claims with `[TODO]` or remove them.
4. Collect `[ASK USER]` items as numbered questions.
5. Highlight intent-vs-implementation divergence.
6. Summarize outputs created under `.lcs/codebase/`.
7. Clearly report limitations, missing evidence, missing `.lcs/docs/`, or scan failures.
8. Write `.lcs/codebase/CHAIN-OF-TRUTH.md` with the Chain of Truth Report (Level: Strict) covering sources checked, assumptions, actions taken, verification results, and confidence rating.

## Focus-area mode
If user asks for a subset (for example: architecture only, testing and concerns, stack and integrations, security concerns only):

1. Always run Phase 1 fully.
2. Complete requested focus docs first.
3. Still create all seven docs under `.lcs/codebase/`.
4. For non-focus docs, keep sections and mark unresolved parts as `[TODO]`.
5. Run full Phase 4 validation across all seven docs.

## Gotchas and anti-patterns
- For monorepos, inspect workspaces/packages/apps/services and package-level manifests.
- Do not assume root manifest represents full repo.
- Treat `.lcs/docs/` as primary intent source, but verify all implementation claims from real files.
- Do not trust docs claims without source/config/manifest confirmation.
- Do not infer databases from env variable names alone.
- Do not document generated output folders as source conventions.
- Map TypeScript path aliases from `tsconfig.json` to actual directories.
- Distinguish production dependencies from dev dependencies.
- Treat TODOs in tests as testing gaps, not production debt.
- Use git history for churn signals when available.
- Never expose secrets; document variable names only from `.env.example`, `.env.sample`, `.env.template`, or equivalents.
- If repo too large, prioritize manifests, entry points, core source dirs, test setup, CI/CD, and integration boundaries.
- If CI/security evidence lives only under skipped hidden directories (for example `.github/`), mark related items as `[TODO]`.

## Chain of Truth Report

### Level
Strict

### Sources Checked
- Project source files, configs, and manifests
- Intent documents from `.lcs/docs/`
- `.codebase-scan.txt` scan output
- Git history (if available)
- `references/inquiry-checkpoints.md` and `references/stack-detection.md`

### Assumptions
- User selected a valid mode (1, 2, or 3) before execution
- `.lcs/codebase/` is the canonical output directory
- Hidden directories (except `.lcs`) do not contain project source

### Plan
1. Phase 1: Create `.lcs/codebase/`, run scan, read intent docs
2. Phase 2: Investigate each documentation area
3. Phase 3: Populate all seven docs in `.lcs/codebase/`
4. Phase 4: Validate docs, repair unsupported claims, write CHAIN-OF-TRUTH.md

### Actions Taken
- Ran mode selection with user
- Executed scan via bundled `scripts/scan.py`
- Read intent documents from `.lcs/docs/`
- Investigated codebase areas (stack, structure, architecture, conventions, integrations, testing, concerns)
- Populated templates from `assets/templates/`
- Validated claims against evidence from source files
- Wrote `.lcs/codebase/CHAIN-OF-TRUTH.md`

### Verification
- Each doc validated against `references/inquiry-checkpoints.md`
- Every non-trivial claim has evidence or `[TODO]` marker
- `[ASK USER]` items collected as numbered questions
- All seven output files exist under `.lcs/codebase/`

### Report
**Confidence**: Medium (varies per doc area based on evidence availability)
**Limitations**: Claims without source confirmation marked as `[TODO]`; intent-vs-implementation divergence noted where found

## Handoff

Next recommended skill: lcs-doc-finalizer

Next file to read: .lcs/codebase/CHAIN-OF-TRUTH.md

Current phase: codebase_documentation

Current confidence: medium

Blocking questions: None

Risks to carry forward: Unvalidated claims marked as `[TODO]`; missing intent docs may reduce accuracy

Source of Truth Bundle: .lcs/state.md, .lcs/codebase/STACK.md, .lcs/codebase/STRUCTURE.md, .lcs/codebase/ARCHITECTURE.md, .lcs/codebase/CONVENTIONS.md, .lcs/codebase/INTEGRATIONS.md, .lcs/codebase/TESTING.md, .lcs/codebase/CONCERNS.md, .lcs/codebase/CHAIN-OF-TRUTH.md

Must Preserve IDs: None

Unresolved IDs: None

Suggested next command: Finalize codebase documentation

## Chain of Truth Level

Level: Strict

This skill follows the LCS Chain of Truth protocol at the declared level.
