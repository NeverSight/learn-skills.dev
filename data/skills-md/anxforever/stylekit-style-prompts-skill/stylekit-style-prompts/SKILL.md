---
name: stylekit-style-prompts
description: Use when users ask to generate beautiful frontend prompts from StyleKit styles, select the best matching style, blend multiple styles, or audit/fix prompt quality for ChatGPT, Cursor, Claude, and other coding assistants.
---

# StyleKit Style Prompts

## Purpose

Generate better-looking frontend output by combining StyleKit style identity, actionable constraints, and quality checks.

## When to Use

Activate this skill when the user:
- Asks to generate a frontend design prompt or style prompt
- Wants to select, compare, or blend StyleKit visual styles
- Needs a design brief for a new page, dashboard, or landing page
- Asks to audit or fix an existing frontend prompt's quality
- Mentions StyleKit, style prompts, or design system prompt generation
- Wants to convert a screenshot or Figma frame into a style-constrained prompt

Do NOT use this skill for general CSS questions, backend logic, or non-visual tasks.

## Quick One-shot Command

Run handbook mode in one command (default):

`python scripts/run_pipeline.py --query "<requirement>" --stack nextjs --format json`

Run site-type routed composition (style + layout + motion + interaction):

`python scripts/run_pipeline.py --query "<requirement>" --stack nextjs --site-type dashboard --recommendation-mode hybrid --content-depth skeleton --decision-speed fast --format json`

Run prompt-generation mode with QA gate:

`python scripts/run_pipeline.py --workflow codegen --query "<requirement>" --stack nextjs --format json`

Force multi-style blend:

`python scripts/run_pipeline.py --workflow codegen --query "<requirement>" --stack nextjs --blend-mode on --format json`

Run targeted refinement (polish/debug/contrast/layout/component-fill):

`python scripts/run_pipeline.py --workflow codegen --query "<requirement>" --stack nextjs --refine-mode debug --format json`

Run with screenshot/Figma reference constraints:

`python scripts/run_pipeline.py --workflow codegen --query "<requirement>" --stack nextjs --reference-type screenshot --reference-notes "<what to preserve/fix>" --format json`

Run with structured reference payload:

`python scripts/run_pipeline.py --workflow codegen --query "<requirement>" --stack nextjs --reference-type screenshot --reference-file refs/screen-analysis.json --format json`

Run strict schema mode for reference payload:

`python scripts/run_pipeline.py --workflow codegen --query "<requirement>" --stack nextjs --reference-type screenshot --reference-file refs/screen-analysis.json --strict-reference-schema --format json`

Benchmark current quality:

`python scripts/benchmark_pipeline.py --format json`

Benchmark with snapshot output:

`python scripts/benchmark_pipeline.py --format json --snapshot-out tmp/benchmark-latest.json`

Run regression gate against baseline snapshot:

`python scripts/benchmark_pipeline.py --format json --baseline-snapshot tmp/benchmark-baseline.json --fail-on-regression`

Auto-update baseline on successful gate:

`python scripts/benchmark_pipeline.py --format json --baseline-snapshot references/benchmark-baseline.json --baseline-update-mode on-pass --baseline-update-target references/benchmark-baseline.json`

CI one-command gate:

`bash scripts/ci_regression_gate.sh --baseline references/benchmark-baseline.json --snapshot-out tmp/benchmark-ci-latest.json`

Run taxonomy guard with strict style-tag registry usage:

`python scripts/validate_taxonomy.py --format json --max-unused-style-tags 0 --fail-on-warning`

Run output-contract sync guard (docs example JSON vs tests schema):

`python scripts/validate_output_contract_sync.py --format text --fail-on-warning`

Dry-run taxonomy expansion (including optional `new_style_tags` in input JSON):

`python scripts/merge_taxonomy_expansion.py --type animation --input tmp/gemini-output.json --dry-run`

## Workflow 1: Requirement -> Style Candidates -> Design Brief -> Prompt

1. Refresh dataset when needed:
   `bash scripts/refresh-style-prompts.sh /mnt/d/stylekit`
2. Retrieve top style candidates:
   `python scripts/search_stylekit.py --query "<requirement>" --top 5 --site-type <auto|blog|saas|dashboard|docs|ecommerce|landing-page|portfolio|general>`
3. Generate design brief and prompts:
   `python scripts/generate_brief.py --query "<requirement>" --stack nextjs --site-type dashboard --recommendation-mode hybrid --content-depth skeleton --decision-speed fast --mode brief+prompt`
4. If needed, force multi-style blend ownership:
   `python scripts/generate_brief.py --query "<requirement>" --stack nextjs --mode brief+prompt --blend-mode on`
5. For iterative work, set refine mode:
   `python scripts/generate_brief.py --query "<requirement>" --stack nextjs --mode brief+prompt --refine-mode polish`
6. For screenshot/Figma-driven generation, add reference context:
   `python scripts/generate_brief.py --query "<requirement>" --stack nextjs --mode brief+prompt --reference-type figma --reference-notes "<frame scope>"`
7. If reference analysis is available, pass structured payload:
   `python scripts/generate_brief.py --query "<requirement>" --stack nextjs --mode brief+prompt --reference-type screenshot --reference-json '{"layout":{"issues":["sidebar overlaps content"]}}'`
8. For high-confidence pipelines, enable strict schema mode:
   `python scripts/generate_brief.py --query "<requirement>" --stack nextjs --mode brief+prompt --reference-file refs/screen-analysis.json --strict-reference-schema`
9. If quality gate fails, run audit + fix workflow.

## Workflow 1.5: Novice Decision Assist (Recommended)

1. User only provides a high-level goal (example: "I want to build a blog").
2. Run handbook mode:
   `python scripts/run_pipeline.py --query "<requirement>" --stack nextjs --format json`
3. Read `manual_assistant.decision_assistant.recommended_style_options` and explain 3-4 options with trade-offs.
4. Ask `manual_assistant.decision_assistant.decision_questions` to help user pick direction.
5. After user selects one option, run codegen mode with forced style:
   `python scripts/run_pipeline.py --workflow codegen --query "<requirement>" --stack nextjs --style <slug> --site-type <type> --content-depth skeleton --blend-mode off --format json`
6. Follow `references/cc-decision-conversation-template.md` for a turn-by-turn assistant script.

## Workflow 2: Existing Prompt -> Quality Audit -> Fix Suggestions

1. Audit prompt text:
   `python scripts/qa_prompt.py --input prompt.md --style <slug>`
2. If this is an iterative update, enforce mode alignment:
   `python scripts/qa_prompt.py --input prompt.md --style <slug> --require-refine-mode layout-fix`
3. If screenshot/Figma context is required, enforce reference guard:
   `python scripts/qa_prompt.py --input prompt.md --style <slug> --require-reference-type screenshot`
4. If structured reference payload exists, require extracted-signal block:
   `python scripts/qa_prompt.py --input prompt.md --style <slug> --require-reference-type screenshot --require-reference-signals`
5. Read `violations` and `autofix_suggestions`.
6. Rewrite prompt and re-run audit until status is `pass`.

## Workflow 3: Multi-style Blend with Conflict Resolution

1. Identify base style from search rank #1.
2. Select up to 2 supporting styles from top candidates.
3. Resolve ownership explicitly:
   - color owner
   - typography owner
   - spacing owner
   - motion/interaction owner
4. Output one merged prompt with priority order.

## Output Contract

Always follow `references/output-contract.md`.

Primary output object fields:

- `design_brief`
- `hard_prompt`
- `soft_prompt`
- `ai_rules`
- `style_choice`
- `site_profile`
- `tag_bundle`
- `composition_plan`
- `decision_flow`
- `content_plan`
- `upgrade_candidates`
- `quality_gate` (for audits)
- `design_brief.refine_mode`
- `design_brief.input_context.reference_type`

## Working Rules

- Never invent style slugs.
- Use only `references/style-prompts.json` as style source of truth.
- Keep aiRules concrete and testable.
- Remove contradictory rules before output (single source-of-truth per constraint).
- Prefer imperative constraints over decorative language.
- Start with explicit design intent (purpose, audience, tone, memorable hook).
- Enforce anti-generic constraints to avoid interchangeable AI-looking output.
- Include pre-delivery validation tests (swap/squint/signature/token).
- Include an anti-pattern blacklist (absolute layout misuse, nested scroll, missing focus states, etc.).
- Preserve user language (Chinese in -> Chinese out; English in -> English out).
- If intent is ambiguous, return top 5 candidates with reasons before final prompt.

## Error Handling

- If `quality_gate.status` is `"fail"`, read `violations` and `autofix_suggestions`, apply fixes, then re-run the QA audit. Repeat up to 3 rounds.
- If the pipeline exits with a non-zero code, check stderr for `ModuleNotFoundError` (missing Python dependency or wrong cwd) or `FileNotFoundError` (missing reference data — run `refresh-style-prompts.sh` first).
- If `search_candidates` returns 0 results, broaden the query or remove `--site-type` constraint.

## Parameter Interactions

- `--blend-mode on` + `--style <slug>`: forces blend OFF (explicit style selection overrides blend).
- `--refine-mode` requires `--workflow codegen`; ignored in handbook mode.
- `--reference-type` + `--strict-reference-schema`: strict mode validates the reference JSON payload against the expected schema and fails fast on mismatch.
- `--recommendation-mode hybrid` uses both BM25 search and taxonomy routing; `rules` skips BM25 and relies solely on site-type routing rules.
- `--content-depth skeleton` produces minimal structure; `storyboard` adds section copy; `near-prod` generates production-ready content blocks.
- `validate_taxonomy.py --max-unused-style-tags 0 --fail-on-warning` enforces zero unused tags in `style-tag-registry` and treats warnings as failures.

## Stack Adapters

Supported stack hints in generation:

- `html-tailwind`
- `react`
- `nextjs`
- `vue`
- `svelte`
- `tailwind-v4`

If stack is unknown, fallback to framework-agnostic Tailwind semantics.

## Resource Files

- `references/style-prompts.json`: full style prompt catalog.
- `references/style-search-index.json`: lightweight search document index.
- `references/output-contract.md`: output schema and examples.
- `references/frontend-design-principles.md`: distinctiveness and anti-generic design heuristics.
- `references/design-system-patterns.md`: token hierarchy and component architecture.
- `references/accessibility-gate.md`: WCAG + mobile touch baseline for prompt quality.
- `references/cc-decision-conversation-template.md`: assistant dialogue template for novice user decision flow.
- `scripts/refresh-style-prompts.sh`: rebuild style dataset from local repo.
- `scripts/search_stylekit.py`: query -> ranked style candidates.
- `scripts/generate_brief.py`: query -> design brief + prompts.
- `scripts/qa_prompt.py`: prompt quality gate and autofix hints.
- `scripts/run_pipeline.py`: one-shot search + brief generation + QA gate.
- `scripts/benchmark_pipeline.py`: benchmark pass-rate, hard-check pass rate, bucket pass-rate (`strict-domain`/`balanced`/`expressive`), snapshot export, and baseline regression gate.
- `scripts/ci_regression_gate.sh`: CI wrapper for benchmark regression gate (supports baseline bootstrap).
- `scripts/smoke_test.py`: validate end-to-end script integrity.
- `scripts/validate_taxonomy.py`: taxonomy consistency + style-tag-registry coverage guard (`--fail-on-warning` promotes warnings to failures).
- `scripts/validate_output_contract_sync.py`: output-contract markdown JSON examples vs tests schema sync guard (uses the first JSON block in each required section as canonical; `--fail-on-warning` promotes warnings to failures).
- `scripts/merge_taxonomy_expansion.py`: merge Gemini taxonomy expansion payloads (animation/interaction + optional `new_style_tags`).
- `scripts/propose_upgrade.py`: generate manual-review upgrade candidates from pipeline output.
- `scripts/review_upgrade_candidate.py`: validate upgrade candidate schema and gate requirements.
- `references/benchmark-baseline.json`: default baseline snapshot for CI gate.
- `references/github-actions-regression-gate.yml`: GitHub Actions template for regression automation.
- `references/taxonomy/style-tag-registry.json`: controlled style tag dictionary used by routing validation.
- `references/taxonomy/*`: site-type routing, controlled tags, alias mapping, and style-tag overrides.
