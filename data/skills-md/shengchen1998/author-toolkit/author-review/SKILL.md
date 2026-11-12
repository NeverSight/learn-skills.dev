---
name: author-review
description: Use when running independent final or current-scope manuscript reviews for intent and consistency, writing standards, and a fresh target reader, or preparing separate review handoffs when subagents are unavailable.
---

# Author Review

Organize three independent reviews and produce findings only. Accept `all`, one perspective (`intent`, `standards`, or `fresh`), or `collect`, plus a project root, review job, or review handoff. Accept `review_mode=final|current-scope|request`; the default is `final`.

This skill does not revise prose, update Story Bible creative content, or apply fixes. When called by `write-fiction`, `revise-fiction`, `revise-draft`, `revise-increment`, or `revise-request`, the caller owns manifest and tracker writes. Standalone use leaves shared project state unchanged unless the author explicitly incorporates the resulting reports later.

## Prepare

1. Resolve the project root from the supplied project root, review job, or review handoff. Resolve the installed `setup-author-toolkit` skill's root as `<setup-skill-root>`. Read `../author-project/SKILL.md` and `../author-project/references/read-operations.md`, then run its `read` and `status` procedures separately. If it reports an incomplete toolkit installation, stop and report the missing installed files; do not deploy contracts into the project. These are the only skill procedures this skill may run. Do not run other skills from a reviewer or subagent.
2. Read the controlled workflow terminology in `<setup-skill-root>/assets/references/terminology.md`, [`references/checklists.md`](references/checklists.md) including its review-mode applicability rules, and [`references/chunked-review.md`](references/chunked-review.md) before planning, resuming, or collecting a review. Read the report envelope and finding identity sections of `../revise-fiction/references/state-and-findings.md`; its state-write instructions remain the caller's responsibility.
3. Select the review mode and its output identity:

| Review mode | Report directory under `paths.reports` | Report v2 `stage` | Handoff subdirectory under `paths.handoffs` |
|---|---|---|---|
| `final` | `final-review/` | `final-review` | `final-review/` |
| `current-scope` | `current-scope-review/` | `current-scope-review` | `current-scope-review/` |
| `request` | `current-scope-review/` | `current-scope-review` | `current-scope-review/` |

   With default paths, these report destinations are `reports/final-review/` and `reports/current-scope-review/`. Use unique UTC-stamped filenames. Creation callers retain their own operation identity and never add a creation operation to report v2 `stage`. A request report's `operation_coverage` describes the requested perspectives and checks, while its `Review coverage` identifies the actual selected units; neither claims full-target reading.
4. Establish one confirmed `scope_id` and one manuscript scope for all three perspectives. A final review covers the whole book. A current-scope review covers only the confirmed current scope and never claims whole-book final approval. A request review retains the target scope ID but reads only the declared changed and dependency-affected passages with necessary local context; it never claims full-target coverage or current-draft revision convergence. Apply the checklist's skipped-item rules for whole-book and unreviewed-passage questions that do not apply.
5. Create or resume one review job per requested perspective and its chunk -> volume/phase -> book plan from actual manuscript paths, hashes, chapter or scene boundaries, and the available context budget. Use the installed review-job and reader-state artifact contracts; the handoff carries their paths rather than copying their content.
6. Use the uppercase finding ID prefixes `INTENT`, `STANDARD`, and `READER`. Before dispatch, request the required consecutive ID block from `author-project` with `next-finding-id` and place the exact block in each handoff or reviewer prompt. Assign disjoint subranges of that block to independently written chunks. Reuse IDs only after the caller reconciles prior observations; an isolated reviewer does not read prior reports or allocate its own IDs. Every reviewer uses judgment confidence and includes a recommendation. The caller enters returned findings as `open` through `author-project record-findings`; status is not a finding v2 property.
7. Preserve input independence as follows:

| Perspective | Permitted inputs |
|---|---|
| Intent and consistency | Manuscript, Story Bible, approved draft-baseline when supplied, approved revision plan, and intent checklist |
| Writing standards | Manuscript and writing standards checklist only, plus [`references/chinese-writing-standards.md`](references/chinese-writing-standards.md) for Chinese work; exclude previous self-assessments, Story Bible, draft-baseline and other baselines, plans, and prior review reports |
| Fresh reader | Actual manuscript units in sequence, target reader description, fresh-reader questions, and only its own reader-state after the first unit; exclude all other review and baseline inputs |

For `language=zh*` or an actually Chinese manuscript, the standards reviewer must load [`references/chinese-writing-standards.md`](references/chinese-writing-standards.md). If the language label and manuscript disagree, follow the actual manuscript and disclose the mismatch. Include this reference in that reviewer's permitted inputs and handoff; do not give it to the intent or fresh-reader perspectives.

## Run layered reviews

Follow [`references/chunked-review.md`](references/chunked-review.md) for unit coverage, synthesis dependencies, reader-state, findings, and completion. Dispatch independent perspectives with fresh contexts. `intent` and `standards` chunk work may run in parallel; the `fresh` chain remains strictly sequential with one logical reviewer. Do not share one perspective's output with another.

Write immutable chunk reports and each applicable volume/phase and book synthesis report with human-readable scope, a `Language coverage` section, a `Review coverage` section, and exactly one report v2 JSON envelope. Mark inapplicable whole-book checklist items `skipped` with reasons in current-scope mode; in request mode, mark checks requiring unread passages `skipped` with `outside request review` and record every other gap truthfully.

For Chinese standards, `Language coverage` must itemize the Chinese subchecks in the loaded reference as actually performed, with `full`, `partial`, or `skipped` status and reasons for gaps. Claim `full` only when every applicable Chinese subcheck covers the requested actual manuscript scope; a sampled, translated, unread, or unexecuted check cannot be folded into `full`. Keep `Review coverage` tied to actual manuscript units and syntheses.

Use `engine.name: "conversational"` and record the actual execution path, version or `unknown`, and degradation. Every report's `engine.notes` contains:

- `scope_id=<actual-scope-id>`;
- `review_mode=final|current-scope|request`;
- actual `operation_coverage=full|partial|skipped`;
- `subchecks=intent`, `subchecks=standards`, or `subchecks=fresh` for one perspective.

For a consolidated report containing all perspectives, use `subchecks=intent,standards,fresh` and the same scope ID. Preserve every finding ID and disagreement. `collect` validates the review job and coverage, including all units and syntheses and the fresh reader-state chain, before reporting consolidated or remaining coverage.

## Run without subagents

Resolve `paths.handoffs` and create resumable handoffs from [`assets/review-handoff-template.md`](assets/review-handoff-template.md) beneath the mode-specific `<paths.handoffs>/<review-mode-directory>/<review-id>/`. Use the registered custom directory when present. Give each handoff only its permitted inputs, review-job path, next unfinished unit, report destination, and resume command. Only the fresh handoff names its own reader-state path.

Stop while work is pending. Resume the named perspective in a separate session, write the completed chunk or synthesis report, update the review job and handoff to the next unfinished unit, and stop again when no further work fits. Fresh sessions continue the same logical reviewer only through that reviewer's own reader-state. Once all required evidence exists, the author can start `author-review` with `collect` and the same review mode or return to the calling strategy's review operation.

## Findings and completion

Use `author-review-intent`, `author-review-standards`, and `author-review-fresh-reader` as audit names. Report concrete observations at verified locations. Linked cross-file findings retain real locations; no broad issue receives an invented single-file location. Produce no manuscript replacements or automatic resolutions.

A perspective is complete only when every required unit and applicable synthesis validates and covers the agreed scope, with all gaps disclosed. `all` is complete only when all three perspectives meet that condition for the same current `scope_id` and review mode. Return report paths, actual coverage, and finding counts; do not start another operation or describe current-scope or milestone evidence as whole-book final review.
