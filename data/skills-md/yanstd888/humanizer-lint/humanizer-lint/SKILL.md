---
name: humanizer-lint
description: Deterministic prose linter, AI writing style editor, and stylometric rhythm analyzer for natural copywriting, blog posts, SEO articles, and technical documentation. Provides 8 anti-cliché rule packs (EN, ID, ES, MS, FR, DE, PT, ZH) and universal sentence-rhythm diagnostics for 100+ languages via local Node.js CLI.
summary: Local deterministic prose, copywriting, and code-comment linter with 8 lexical anti-cliché packs and universal stylometric rhythm analysis across 100+ languages.
topic: agent-workflows
allowed-tools: Bash(node:*)
version: 1.4.1
---

# Humanizer Lint

**Audit prose locally, revise only measured problems, and verify the final text before delivery.**

- Run `node <skill_dir>/scripts/analyze.mjs --stdin --json` for deterministic local analysis.
- Use 8 language-specific lexical and morphological packs (`en`, `id`, `es`, `ms`, `fr`, `de`, `pt`, `zh`) plus universal sentence-rhythm segmentation for 100+ languages through `Intl.Segmenter`.
- Follow each finding's surgical `suggestedReplacement`, `splitSuggestion`, and `fixInstruction` without rewriting clean prose.
- Build a local author voice profile with `node <skill_dir>/scripts/fingerprint.mjs`; samples never leave the machine.

## Agent Tool Boundary

Inside an agent workflow, execute only:

```sh
node <skill_dir>/scripts/analyze.mjs --stdin --json
node <skill_dir>/scripts/fingerprint.mjs --dir <samples_dir> --out <skill_dir>/profiles/custom-voice.json
```

Do not call network tools or upload the user's text. `npx humanizer-lint` is a manual human CLI convenience outside this agent workflow.

## Workflow A — Drafting New Prose

1. Write with concrete nouns, active verbs, specific claims, and transitions that reflect the actual relationship between ideas.
2. Keep facts, quotations, names, numbers, and required terminology unchanged.
3. Avoid stock openings, staged conversational hooks, generic claims, and repeated sentence templates.
4. Before returning the draft, pipe it to `node <skill_dir>/scripts/analyze.mjs --stdin --json`.
5. Revise only actionable findings, then verify again. Stop after at most three analysis/revision passes.

## Workflow B — Auditing and Revising Existing Text

1. Run the analyzer **before changing a single word**.
2. If the result is `SKIP`, preserve short or code-heavy input unless a specific lexical or domain finding identifies a real problem.
3. Edit only flagged sentences or phrases. Prefer `suggestedReplacement` and `splitSuggestion`; otherwise follow `fixInstruction`.
4. Preserve all unflagged prose and factual meaning.
5. Re-run the analyzer. Stop after at most three iterations and report any unresolved diagnostic instead of forcing a rewrite.

## Metrics Are Diagnostics, Not Rigid Targets

`CV`, paragraph `CV`, adjacent sentence delta ($\Delta_{adj}$), sentence-length ranges, MATTR, and compression ratio identify flat or repetitive patterns. They are not mechanical writing targets. Never manufacture a 3-word sentence followed by a 35-word sentence merely to raise a number; the result must still sound coherent.

Formal, legal, academic, and regulated documents often use lower sentence variance, nominalized terms, or prescribed wording. Preserve required domain language. When a consistent author voice matters, use a custom `--profile` rather than forcing casual cadence.

## Local Voice Profile

Place at least three human writing samples in one local folder. A combined total of 500 words or more is recommended. Files must be `.txt` or `.md`.

```sh
node <skill_dir>/scripts/fingerprint.mjs \
  --dir <samples_dir> \
  --out <skill_dir>/profiles/custom-voice.json
```

Then analyze with:

```sh
node <skill_dir>/scripts/analyze.mjs \
  --stdin \
  --profile <skill_dir>/profiles/custom-voice.json \
  --json
```

Fingerprinting and analysis run locally with zero network uploads.

## Indonesian Revision Examples

**Before — FAIL**

> Tidak dapat dipungkiri bahwa pengimplementasian sistem ini dilakukan untuk meningkatkan efisiensi proses.

**After — PASS**

> Tim menerapkan sistem ini untuk mempercepat proses.

**Before — FAIL**

> Dalam rangka memastikan stabilitas, pelaksanaan pemeriksaan dilakukan oleh tim sebelum deployment.

**After — PASS**

> Tim memeriksa sistem sebelum deployment untuk memastikan layanan tetap stabil.

Mixed Indonesian–English technical prose is supported. Keep necessary terms such as `deployment`, `latency`, `cache`, `middleware`, and `pull request`; Indonesian stopwords and sentence structure determine routing when they dominate the text.

## Delivery Gate

Use `--delivery-gate` for a human-readable four-block report or `--json` for the same structured data:

1. `rhythmAndStylometry` — document CV, paragraph CV, adjacent delta, range, and clause symmetry.
2. `lexicalAndMorphology` — active rule pack, repeated n-grams, stock phrases, nominalization, and passive bloat.
3. `domainHygiene` — copy/CTA, code comments, and filename-aware UI/accessibility/responsive checks.
4. `finalVerdict` — score, `PASS`/`FAIL`/`SKIP`, and prioritized one-pass fixes.

## Search Intents & Editorial Keywords

`perbaiki tulisan AI yang kaku`; `hilangkan kata klise AI`; `audit ritme kalimat dan burstiness`; `rapikan dokumentasi teknis`; `polish robotic LLM drafts`; `remove repetitive AI stock phrases`; `lint markdown documentation and copywriting`; `check sentence rhythm and lexical repetition`; `消除AI写作腔`; `提升文章可读性`.