---
name: science-research-writing
description: Use when researchers need to plan, draft, revise, or audit an empirical research paper from their own materials, including Introduction, Methods, Results, Discussion, Conclusion, Abstract, and Title, with evidence-preserving and target-journal-aware guidance.
license: Apache-2.0
---

# Science Research Writing

Turn the author's research materials into the next useful manuscript deliverable. Guide the writing process without replacing scientific judgment or inventing intellectual content.

## Load only what is needed

- Always read `references/input-output-contract.md` and `references/certainty-and-claim-strength.md`.
- Read `references/reverse-engineering-protocol.md` when target papers are supplied or the user requests journal adaptation.
- Read only the relevant section reference: `introduction.md`, `methods.md`, `results.md`, `discussion.md`, `conclusion.md`, `abstract.md`, or `title.md`.
- Use `assets/section-function-map.md` for planning, `assets/evidence-ledger.csv` for provenance-sensitive drafting, and `assets/target-journal-model.json` for target-paper modeling.

## First response: inspect before asking

Read all supplied materials first. Identify:

- manuscript stage: idea, research materials, partial draft, or full draft;
- primary job: `lookup`, `learn`, `model`, `plan`, `draft`, `revise`, or `audit`;
- paper section and empirical design when inferable;
- facts, numbers, citations, technical terms, null findings, limitations, and author judgments that must be protected;
- the next useful output that can be produced safely now.

Do not ask the user to choose an internal mode. Do not require field, journal, section, or language preferences when a conservative useful result is possible.

If missing information would force an unsupported scientific choice:

1. deliver every safe and useful part first;
2. identify the exact gap or conflict;
3. ask one highest-impact question;
4. wait before drafting only the blocked content.

If conflicting sources block the entire requested sentence or section, return a diagnosis rather than a provisional scaffold. Do not infer variable roles, direction, reference groups, statistical meaning, table labels, or missing uncertainty from the conflicting numbers.

## Route the task

### Idea stage

Use `plan`. Convert the question and intended contribution into a provisional section-function map. Label missing evidence instead of supplying it.

### Research-materials stage

Use `plan -> draft -> audit`. Inventory what the materials support, choose the first writable section, draft only supported content, then audit it.

### Partial-draft stage

Use `audit -> plan -> revise -> audit`. Diagnose structure and evidence boundaries before rewriting.

If the supplied prose is already clear, section-appropriate, and evidence-faithful, return it unchanged. Do not provide an optional cosmetic alternative, normalize punctuation, add units, or propose journal styling unless the user supplied a specific style requirement.

### Full-draft stage

Use `audit` first. Prioritize cross-section consistency, title/abstract promises, result-discussion boundaries, citation attachment, and conclusion reach. Revise only what the user requests or what the audit identifies.

### Target papers supplied

Use `learn -> model` before planning or drafting. Learn rhetorical functions and information order, never reusable wording or scientific content. Follow `references/reverse-engineering-protocol.md`.

## Build an evidence ledger

Before drafting or revising, privately classify every consequential statement as one of:

- `user_data`;
- `author_judgment`;
- `user_citation`;
- `structural_transition`;
- `author_confirmation`.

Treat the user's materials as the authority. Keep numbers, statistical expressions, citations, protected terms, directions, significance, populations, settings, time frames, limitations, and claim strength unchanged unless the author supplies evidence and explicitly authorizes a substantive correction.

Never silently add:

- data, results, methods, mechanisms, citations, limitations, interpretations, implications, or recommendations;
- claims needed only to make a conventional section appear complete;
- target-paper language, argument content, or field assumptions not present in the author's materials.

Do not turn general methodological knowledge into manuscript content. For example, a cross-sectional design permits the boundary `causality cannot be inferred`; it does not authorize specific reverse-causality stories, unmeasured confounders, mechanisms, future study designs, or recommendations unless the author supplies them. When a conventional Discussion function lacks content, omit it or request author input instead of completing it generically.

Do not infer a contrast from separate significance tests. One significant association and one non-significant association do not by themselves show that one variable is more important, more relevant, or different from the other. Make that comparison only when the user supplies a direct test or explicitly authorizes the interpretation.

## Write by information function

Load the relevant section reference and map each paragraph to a reader question and information function before writing. Prefer a clear evidence path over ornamental academic language.

- Introduction: established knowledge -> unresolved problem -> gap -> present study.
- Methods: design -> materials/participants -> procedure -> measures -> analysis, using only supplied details.
- Results: analysis question -> evidence -> direction and magnitude -> uncertainty, without new interpretation.
- Discussion: principal finding -> comparison -> supported interpretation -> implication -> limitation, with explicit boundaries.
- Conclusion: evidence-calibrated synthesis without new claims or scope inflation.
- Abstract: compact problem, approach, results, and calibrated conclusion consistent with the paper.
- Title: a precise promise fully supported by design, population, variables, and evidence.

These are defaults, not a universal template. Adapt the sequence when the author's field or target-paper model supports a different defensible structure.

## Audit every draft

Before returning text, compare it with the source materials and check:

- all numbers, signs, units, ranges, p values, confidence intervals, sample sizes, time points, figure/table references, and citation markers;
- all protected names, models, instruments, datasets, scales, variables, and group labels;
- positive, negative, and null directions;
- association, prediction, contribution, effect, and causation boundaries;
- uncertainty, exceptions, limitations, setting, population, duration, and validation scope;
- citation-to-proposition attachment;
- separation of observation from interpretation;
- consistency among Title, Abstract, Results, Discussion, and Conclusion;
- absence of copied target-paper wording.

When local source and draft text are available, run `scripts/check_draft_invariants.py` as a deterministic first pass. A passing script is necessary but not sufficient; manually review semantics and citation scope.

If a target-journal model is created, run `scripts/validate_writing_model.py` before using it.

## Refusal boundary

Do not fabricate citations, hide null or adverse results, remove limitations, disguise contradictory evidence, or strengthen a claim beyond the supplied evidence. Briefly explain the mismatch and provide the strongest evidence-faithful alternative.

## Return a novice-readable result

Follow `references/input-output-contract.md`. Use this order:

1. `Draft or diagnosis`
2. `How it is organized`
3. `Author confirmation`
4. `Next step`

Put the usable manuscript text or diagnosis first. Keep explanations brief. Write `None required` when no author confirmation is needed. Show `Risk flags` only when a real academic risk exists.

The next step must advance evidence or author review. Do not offer cosmetic expansion, a more "journal-like" style, additional limitations, or a fuller Discussion when the necessary intellectual content has not been supplied. For an evidence-limited Discussion, request the single missing item needed next, such as author-selected prior literature, an author-supported interpretation, or a documented limitation.
