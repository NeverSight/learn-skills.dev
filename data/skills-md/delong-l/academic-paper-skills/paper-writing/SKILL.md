---
name: paper-writing
description: Policy-aware academic paper prose writing and rewriting with public academic defaults and an optional strict house-style policy set. Use for drafting or revising abstracts, introductions, RQ framing, related work, background, method prose, system-model prose, results narrative, discussion, limitations, conclusions, contribution lists, claim calibration, citation-integrated prose, venue-aware section structure, and academic prose cleanup. Do not use for final figure/table rendering, data plotting, self-review, reviewer response, or rebuttal drafting.
---

# Paper Writing

Use this as the single entrypoint for academic paper prose. It combines claim calibration, public academic defaults, optional house-style rules, introduction/RQ framing, citation discipline, and academic prose cleanup.

## Priority Model

Always load `references/priority-model.md` first. For any prose-writing task, also load `references/style-profile.md`.

Authority order:

1. Core integrity constraints from the sibling `paper-policy` skill.
2. User-provided facts, approved evidence, author intent, and task constraints.
3. Verified venue or template requirements.
4. Hard rules from all activated policy sets, including optional house rules only after explicit opt-in.
5. `references/style-profile.md` and enabled soft guidance.
6. Task-specific references and then generic advice.

When sources conflict, prefer the higher item. Do not treat disabled house rules as public academic requirements.

## Policy Consumption

Load `references/policy-integration.md` for full-paper, multi-section, outline,
polish, venue-aware, submission-stage, citation-aware, or conditionally governed
section work. Resolve the sibling `paper-policy` rules before drafting.

Consume policy read-only. Apply active hard rules before adapting active soft
rules. Resolver warnings are unresolved context, not compliance. Do not infer
permission to apply semantic fixes, mutate unrelated manuscript files, or edit
`.bib` files.

A short isolated rewrite may use transient context and must not create a
persistent policy file solely to satisfy workflow machinery.

## Task Routing

Load only the references needed for the current writing task:

| Task | Load |
|---|---|
| Full paper, multi-section, venue-aware, polish, or submission-stage work | `policy-integration.md`, then applicable section references |
| Outline or top-level section structure | `policy-integration.md`, `section-architecture.md`, optionally `venue-adaptation.md` |
| Abstract or general section draft | `section-drafting.md`, `academic-prose.md`; add `policy-integration.md` when context is persistent or conditional |
| Introduction, gap, or RQs | `policy-integration.md`, `introduction-framing.md`, contribution guidance in `section-drafting.md` |
| Related Work or Background and Related Work | `policy-integration.md`, `related-work.md`, `citation-integration.md` |
| Method, System Model, Approach, or technical prose | `policy-integration.md`, `section-drafting.md`, `citation-integration.md` if claims cite prior work |
| Results narrative without making plots/tables | `policy-integration.md`, `section-drafting.md`, `artifact-handoffs.md` |
| Discussion, limitations, conclusion | `policy-integration.md`, `section-drafting.md`, `academic-prose.md` |
| Contribution list or claim calibration | `policy-integration.md`, `section-drafting.md`, `style-profile.md` |
| Prose polish, AI-pattern cleanup, or "make this sound less AI" | `academic-prose.md`, `style-profile.md` |
| Citation-aware writing | `citation-integration.md` |
| Need a figure or table artifact | `artifact-handoffs.md`; hand off artifact production to Figures & Tables |

If a task spans multiple sections, load `section-architecture.md` first, then the section-specific reference files.

## Integrity And Hard Boundaries

- When `STRUCT.TRADITIONAL_HEADINGS` is active, keep top-level section names traditional and concise. Otherwise treat that pattern as optional structure guidance.
- When `RELATED.COMPARISON_REQUIRED` is active, include a Related Work comparison-table plan unless an authorized waiver or venue requirement applies. Otherwise propose a table only when it improves the argument.
- Do not produce final figure/table layout in this skill. Writing may produce an artifact plan, caption draft, or table spec, then hand off to Figures & Tables.
- Use only citation and evidence sources declared by the user or project; local `.bib` files and user notes are the default. Do not invent citations, BibTeX entries, venues, years, or paper claims. If support is missing, request a manual update or an explicitly authorized citation audit. Use `citation-integration.md`.
- During Anti-AI cleanup, preserve claim strength, causal status, evidence scope, limitations, technical terms, citations, values, and the author's evidence-bound position.
- Do not use detector, perplexity, authenticity, or human-likeness scores to judge compliance, readiness, or authorship, and do not rewrite prose to evade such detectors.
- Do not write meta-text such as "this draft", "this manuscript aims to", or "in xxx-style" in the paper body unless the source paper itself uses that phrase for a substantive reason.
- Keep internal provenance out of the paper body unless the paper is explicitly about audit methods. Internal paths, script names, renderer names, DPI checks, placeholder-citation status, and artifact-bundle notes belong in README, artifact specs, review files, appendices, or comments.

## Soft Academic And House Defaults

- Prefer scoped claims, explicit boundaries, evidence-forward paragraphs, and contribution bullets that name artifacts rather than activities.
- Diagnose formulaic AI-associated prose patterns as concrete style issues; do not infer authorship from them or treat every pattern as forbidden.
- Use ordinary roman text by default. Use `\textbf{}` sparingly for named paragraph cues such as RQs or stage names. Avoid frequent `\textit{}` and `\texttt{}` in prose unless the text is a mathematical variable, code literal, file path in an audit appendix, or venue-required notation.
- Adapt paragraph rhythm, list density, RQ-answer presentation, and table/figure references to the manuscript state and venue pressure while preserving all active hard boundaries.

## Output Contracts

For drafting or rewriting prose:

1. Prefer concrete rewritten text over advice.
2. Preserve LaTeX commands, labels, citations, math, and macros unless the user asks to refactor them.
3. State any missing factual input as a bracketed placeholder, not as invented content.
4. Keep claims scoped to the available evidence.
5. For Anti-AI cleanup, distinguish hard integrity boundaries from soft pattern diagnostics and compare the source and revision for semantic drift.

For Related Work:

1. Return prose organized by intellectual axes, not paper-by-paper summaries.
2. Include or specify a comparison table with row groups, 3--4 high-signal dimensions by default, marker semantics only if needed, compact caption draft, placement preference, and the sentence that references it.
3. If the final LaTeX table is outside scope, emit a handoff spec for Figures & Tables.

For Results narrative:

1. Interpret supplied values only within the stated experiment scope.
2. Mention the table or figure that should carry exact values.
3. If an artifact is missing, provide a handoff spec instead of pretending the evidence exists.
4. When `RESULTS.RQ_EXPLICIT_ANSWER` is active, close each load-bearing RQ block with exactly one direct, evidence-traceable, bounded answer.
5. When `RESULTS.RQ_ANSWER_BOX` is enabled, treat the `Answer to RQn` box as an adaptable presentation; otherwise use the manuscript's existing RQ closure style.

For method and evidence architecture:

1. When evidence sources have different roles, declare which claims each source may and may not support before interpreting results.
2. Prefer a compact evidence-role ledger, but keep role boundaries mandatory even when the ledger is adapted to prose or moved partly to an appendix.
3. When a systematic measurement or extraction error is characterized, state its evidence-supported direction and affected claims; say `directionally indeterminate` when the direction cannot be justified.

For threats and limitations:

1. Map each load-bearing threat to the affected claim or RQ, the mitigation or explicit absence of one, and the residual boundary.
2. Choose a taxonomy appropriate to the paper type rather than forcing one universal validity taxonomy.
3. When `STRUCT.CONCLUSION_INTEGRATES_LIMITATIONS` is active, preserve the key limitation inside the Conclusion even when fuller threat analysis appears elsewhere; enforce a single paragraph only when `STRUCT.CONCLUSION_SINGLE_PARAGRAPH` is also active.

## Reference Map

- `references/priority-model.md`: source priority and conflict resolution.
- `references/policy-integration.md`: read-only consumption of context-resolved hard and soft rules.
- `references/style-profile.md`: claim-calibrated public defaults and opt-in house variants.
- `references/section-architecture.md`: adaptive paper structure and optional traditional-heading profile.
- `references/section-drafting.md`: section-level drafting patterns and claim calibration.
- `references/introduction-framing.md`: gap and RQ-driven introduction flow.
- `references/related-work.md`: related work organization and conditional comparison-table planning.
- `references/academic-prose.md`: academic anti-AI cleanup and prose guardrails.
- `references/citation-integration.md`: manual-BibTeX citation integration and local citation hygiene.
- `references/venue-adaptation.md`: venue and checklist adaptation.
- `references/artifact-handoffs.md`: handoff specs for Figures & Tables.
