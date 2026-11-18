---
name: paper-review
description: Conduct reviewer-style, evidence-safe reviews of academic manuscripts across disciplines using progressive method, domain, review-round, and optional reviewer overlays. Use when the user asks for a critique, scientific review, priority comments, top-to-bottom review, revision-round assessment, prior-comment regression check, or review memo rather than ordinary drafting. Infer the smallest applicable module set from the conversation and manuscript; ask only when unresolved domain or review-profile ambiguity would materially change the review. Includes optional psychometrics and SEM, computational and LLM, water and CNHS, flood and hydrodynamics, and explicit Ethan-style modules.
---

# Paper Review

## Use the Manuscript-Integrity Base

Use `academic-writing-skills` as the manuscript-integrity base for lifecycle, evidence, prose, change-impact, and release checks. Apply this skill as a reviewer orchestrator that selects only the method, domain, review-round, venue, or reviewer modules needed for the manuscript.

Do not edit the manuscript unless the user authorizes revision. A request to review, critique, comment, or assess a round is non-mutating. Use the appropriate document or PDF skill for extraction, comments, tracked changes, and visual rendering.

## Establish the Review Basis

Identify:

- manuscript and companion artifacts in scope
- review-only versus authorized revision
- manuscript archetype, study design, lifecycle stage, and intended venue
- main questions, outcomes, methods, evidence, and claimed contribution
- prior draft, prior comments, responses, and round label when supplied
- candidate method, domain, venue, reviewer, and project overlays
- unavailable sources or ambiguities that could change the review standard

Prefer an explicit review round. If none is supplied, use `developmental`, `substantive`, `integration`, or `submission`; do not infer R1–R4 from prose quality, filename, or comment count.

Read [overlay-contract.md](references/overlay-contract.md) before applying optional modules. Read [round-calibration.md](references/round-calibration.md) only when review maturity or cross-round progress is in scope.

For a supplied rubric, coded check report, or version-comparison review, use [review-checklist-and-cases.md](references/review-checklist-and-cases.md) to record applicable checks and evidence-backed repairs. It adds traceability and worked cases, not another mandatory full-paper pass.

## Select Modules Progressively

Infer candidate modules from the current conversation, title, Abstract, questions, Methods, tables, figures, equations, and supplement. Select the smallest set that covers the actual study. State the selected modules in the review header.

Ask one targeted question only when the available evidence leaves two materially different review standards plausible—for example, whether a latent-variable model is confirmatory or exploratory, or whether the user wants a neutral review versus a named reviewer style. Do not ask when the manuscript itself resolves the choice.

Load:

- [display-notation-provenance.md](references/display-notation-provenance.md) for equations, formal notation, derived display quantities, normalization or aggregation rules, uncertainty displays, or cross-artifact symbol consistency
- [quantitative-psychometrics-sem.md](references/quantitative-psychometrics-sem.md) for surveys, scales, psychometrics, factor analysis, latent variables, SEM, mediation, or multi-group comparison
- [ai-llm-computational.md](references/ai-llm-computational.md) for simulations, ABM, coupled computational models, ML, GenAI, LLMs, synthetic respondents, or agent evaluation
- [water-cnhs-uncertainty.md](references/water-cnhs-uncertainty.md) for water resources, coupled natural–human systems, water policy, frameworks, reviews, uncertainty, or equifinality
- [flood-hydrodynamics-catastrophe.md](references/flood-hydrodynamics-catastrophe.md) for flood risk, catastrophe models, inundation, drainage, hydrodynamics, hazards, exposure, vulnerability, or loss
- [ethan-style-overlay.md](references/ethan-style-overlay.md) only when the user explicitly requests Ethan-style review or establishes that lab review context
- [project-precedents.md](references/project-precedents.md) only after the exact named project is established and only together with an explicit relevant reviewer or lab context

Load multiple modules for genuinely hybrid studies. A citation, keyword, or study-area mention alone does not establish a module. Treat named methods, thresholds, citations, and reporting practices inside modules as checks to evaluate, not assumptions that the manuscript must follow them.

## Support New Domain Modules

Keep reusable domain knowledge in a direct reference file rather than expanding this routing file. A contributed module should contain:

1. explicit trigger and exclusion cues
2. method and evidence checks
3. claim-scope and alternative-explanation checks
4. figure, table, equation, and reproducibility checks where relevant
5. terminology cautions without project facts
6. at least one routing or boundary eval

Add the module to the routing list and architecture tests. Keep professor, laboratory, journal, and project rules in separate conditional overlays.

## Run the Review

Apply the base skill's four passes, then use the selected modules to deepen—not duplicate—the review:

1. **Framing and contribution:** verify that the literature supports the gap, the task matches the methods, and the contribution does not exceed the evidence.
2. **Design and methods:** verify sampling or source selection, measurement, model logic, estimand, assumptions, uncertainty, comparison design, and reproducibility as applicable.
3. **Results and claim scope:** verify question-to-result coverage, statistical or computational evidence, alternative explanations, mechanisms, and formal versus descriptive comparisons.
4. **Discussion and synthesis:** distinguish direct findings, literature-supported interpretation, plausible alternatives, implications, limitations, and speculation.
5. **Displays and notation:** verify figures, tables, equations, captions, units, symbols, panels, text–display agreement, and the provenance of derived quantities. When the display-and-notation module applies, use its symbol ledger and provenance trace rather than checking each artifact in isolation.
6. **Writing and delivery:** verify terminology, repetition, observable stock phrasing, flow, summaries, citations, companion files, metadata, and named-stage readiness.

For every material issue, inherit the base skill's scope, S0–S4 severity, evidence status, issue status, authority needed, affected artifacts, and blocking stage. If an optional reviewer overlay uses `MUST`, `SHOULD`, `QUERY`, or `PREFERENCE`, keep those labels separate from severity.

## Protect Evidence and Reviewer Boundaries

Do not invent mechanisms, citations, facts, thresholds, analyses, prior comments, or reviewer preferences. A request to explain “why” does not authorize a causal story unsupported by analysis or literature.

Do not infer AI authorship from prose. Report observable features such as vague subjects, stock transitions, empty intensifiers, repetitive cadence, duplicated synthesis, or unsupported mechanisms.

Do not call a cross-round issue resolved without the prior instruction and current evidence. A response letter or resolved comment thread is evidence of an author claim, not evidence that the current artifact contains the requested change. Do not make a preference blocking unless a verified venue, reporting, author, or reviewer requirement makes it so.

## Output Format

Adapt the memo to the available artifact and stage. Do not invent comments for absent sections or target a fixed number.

### Header

```text
REVIEW PROFILE: [general scientific / named conditional overlay]
PAPER: [title]
MODE: [review only / authorized revision]
STAGE OR ROUND: [maturity label or supplied round]
MODULES: [selected references and why]
SOURCE BASIS: [current files, prior material, unavailable sources]
READINESS: [named next-stage readiness and primary bottleneck]
```

### Cross-Round Status

Include only with prior evidence. Classify issues as resolved, partial, open, regressed, waived, new, or not verifiable.

### Priority-Ranked Action Items

For each material issue, give its location, classification, severity and evidence status, specific problem, bounded action or decision, affected artifacts, and whether it blocks the named next stage.

### Section-Linked Comments

Follow the manuscript's actual reader functions and structure. Anchor comments to short fragments. Distinguish validity, reporting, domain convention, venue rule, reviewer preference, and local prose improvement.

### Writing and Presentation Flags

Include representative cases and a revision direction. Do not rewrite unless authorized.

### Next-Step Instruction

State which issues, decisions, sources, and artifacts must be addressed before the next review.

### Functional-Completeness Retrospective

Use the base retrospective. Name the lifecycle stage, modules loaded, selection evidence, unresolved ambiguity, prior-round evidence, artifacts covered, change propagation, checks performed, and readiness limits.

## Safety and Restraint

Be direct, technically precise, and respectful. Do not impersonate a named reviewer, express frustration, or use humiliation. Never suppress a validity, ethics, evidence, or metadata issue because the manuscript is in a late round.
