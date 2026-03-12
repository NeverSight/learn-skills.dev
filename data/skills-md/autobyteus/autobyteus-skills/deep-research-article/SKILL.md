---
name: deep-research-article
description: "Do deep research and synthesize it into one logically structured article with clear thesis, argument flow, evidence, objections, and takeaways. By default, this skill requires internet source collection and deep reading before drafting. Use when the user wants a strong reasoning artifact first: sermon notes, Bible passage study, policy/tech explainers, product narratives, or any topic where downstream artifacts should start from an approved article."
---

# Deep Research Article

## Overview (primary artifact)

Produce:
1) `article.md`: one coherent article with strong reasoning and transitions

This skill is intentionally topic-agnostic.
If the user later wants an image-only deck, pass the approved article directly to `infographic-powerpoint-deck`, which can ingest raw articles or structured slide tables.

In internet-backed mode, also produce a research package:
- `source_dossier.md`
- `evidence_extract.md`
- `research_notes.md`
- `claim_evidence_ledger.md`

## Workflow

### Step 0 — Confirm constraints and research mode

Ask only what’s necessary:
- Audience + use case (sermon, lesson, blog, internal memo)
- Desired length (minutes or word count)
- Language (CN/EN/bilingual) and tone (academic / pastoral / simple)
- Success criteria (what a “good final article” must achieve for this user)
- Explicit non-goals/out-of-scope topics to prevent drift
- For Bible: translation/version and whether to include cross-references
- Must-use sources or explicit constraints (paywalled-only, region scope, date range)
- Whether web research is prohibited by user/policy

Default mode is **internet-backed deep research**. Only skip internet if user explicitly asks for no-web research.
If the user does not specify a length, do **not** default to a short article. Read `references/longform_depth_standard.md` and use the long-form depth defaults there.

### Step 1 — Internet source sweep (required by default)

Follow `references/web_research_protocol.md` and create `source_dossier.md` using `references/source_dossier_template.md`.

Minimum source counts:
- **Normal**: at least 8 sources
- **Deep**: at least 12 sources

Coverage requirements:
- At least 2 source types (e.g., primary + secondary)
- At least 2 sources that present meaningful tension/alternative interpretation
- For time-sensitive topics: include recent sources and clearly note dates

Drafting is blocked until this step is complete.

### Step 1a — No-web fallback (only when explicitly requested)

If the user explicitly forbids web research:
- Use only provided/local materials.
- Build `source_dossier.md` from local sources.
- Mark mode as `no-web constrained` in the dossier.
- Keep the same extraction/ledger/QA flow, but clearly flag evidence limits in the article.

### Step 1b — Evidence extraction (deep reading)

Create `evidence_extract.md` from the dossier using `references/evidence_extraction_template.md`.

For each major source, record:
- exact claim/data point extracted
- what it supports or challenges
- uncertainty/caveat

For Bible passages:
- Note structure (pericope boundaries), repeated words, contrasts, commands, warnings, comfort.
- Identify “center of gravity” (main burden) and what the text is **not** saying.

### Step 1c — Research notes (synthesis scratchpad)

Create `research_notes.md` using `references/research_notes_template.md`:
- key definitions
- observations from sources/text
- competing interpretations
- load-bearing facts with source IDs
- open questions

### Step 1d — Claim→evidence ledger (required)

Before drafting, build `claim_evidence_ledger.md`:
- Use `references/claim_evidence_ledger_template.md`.
- Every major claim must have at least one evidence anchor and source ID.
- Mark confidence and disconfirmation condition.

### Step 2 — Argument outline (the real engine)

Write an outline that is easy to defend:
- Thesis (one sentence)
- Mainline statement (one sentence): what the article must prove for this user, and what is explicitly out of scope
- 3–6 supporting moves (each is a claim → evidence → implication)
- Guardrails: what to omit, what not to overclaim
- Transition logic: why move A leads to move B

Before drafting, run a quick outline challenge:
- For each move, state “if removed, what breaks?”
- Remove or merge moves that don’t break anything important.

### Step 3 — Draft `article.md`

Use the skeleton in `references/article_skeleton.md`.
Also read `references/longform_depth_standard.md`.

Rules:
- Prefer short paragraphs with explicit signposting (“因此/所以/因为/然而”).
- Separate observation vs application.
- Include explicit citations (source IDs and links) for load-bearing claims.
- Default to a substantial long-form article unless the user explicitly asked for a brief.
- Integrate evidence into the body itself. Do not outsource the reasoning to a references section or tell the reader to “see the sources” instead of explaining the point.
- A 3–6 move outline does **not** mean a short article. Each move may need multiple subsections or several paragraphs of evidence synthesis, tension, and implications.
- If evidence is mixed, present both sides and state your judgment criteria.

### Step 4 — QA gates (logic + evidence)

Run both:
- `references/logic_qa_checklist.md`
- `references/evidence_gates.md`
- `references/objectivity_checks.md`
- `references/mainline_coherence_gate.md`
- `references/final_article_quality_gate.md`

If any hard gate fails, return to Step 1 (source sweep) or Step 1b (evidence extraction).
In no-web constrained mode, return to Step 1a and narrow claims as needed.

### Step 4b — Iterate until it “locks” (human-like drafting)

Deep research writing is normally iterative. Use `references/iteration_protocol.md`:
- revise thesis/outline if QA reveals gaps
- rewrite sections for clarity and scope
- add/remove evidence so every claim is supported
- trim or rewrite off-mainline sections (anything that does not advance the thesis)
- repeat QA + quality scoring until stop criteria are met

### Step 4c — Revision log (recommended for real iteration)

Humans keep track of what changed; do the same to avoid thrash:
- Add a short “Revision notes” section to `article.md`, or keep a separate `revision_log.md`.
- Use `references/revision_log_template.md`.

### Step 5 — Stop at the approved article

The normal end state of this skill is an approved `article.md` plus the supporting research package.
Do **not** create a separate slide-extraction handoff artifact as part of the default deep-research workflow.
If the user wants slides after the article is approved, hand the article directly to `infographic-powerpoint-deck`.

## Output files (recommended)

- `article.md`
- `source_dossier.md` (required in internet-backed mode)
- `evidence_extract.md` (required in internet-backed mode)
- `research_notes.md` (required)
- `claim_evidence_ledger.md` (required)
- `revision_log.md` (optional, but helpful)

## References
- Read `references/article_skeleton.md` when drafting `article.md`.
- Read `references/web_research_protocol.md` for the required search/deep-reading workflow.
- Read `references/source_dossier_template.md` to structure source collection.
- Read `references/evidence_extraction_template.md` for claim-level extraction.
- Read `references/source_strategy.md` to pick sources and record uncertainty.
- Read `references/research_notes_template.md` to structure `research_notes.md`.
- Read `references/claim_evidence_ledger_template.md` to prevent unsupported claims.
- Read `references/logic_qa_checklist.md` for the reasoning QA pass.
- Read `references/evidence_gates.md` for objective evidence sufficiency gates.
- Read `references/objectivity_checks.md` for neutrality and confidence calibration checks.
- Read `references/mainline_coherence_gate.md` to catch and remove sections that drift away from the core thesis/user intent.
- Read `references/final_article_quality_gate.md` for final draft quality scoring before handoff.
- Read `references/longform_depth_standard.md` so the final article defaults to paper-grade depth rather than a short summary.
- Read `references/iteration_protocol.md` for iterative improvement and stop criteria.
- Read `references/revision_log_template.md` to track iterations cleanly.
