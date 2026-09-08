---
name: paper-review
description: Academic paper review, self-review, red-team review, reviewer-response, rebuttal planning, rebuttal drafting, and revision verification. Use when Codex needs to audit a manuscript before submission, simulate reviewers, prepare a prioritized fix list, analyze external reviewer comments, draft or check author responses, verify promised revisions, check submission readiness, or review paper quality without entering any external literature-management workflow.
---

# Paper Review

## Overview

Use this skill to evaluate a paper as a reviewer would: identify evidence-bound weaknesses, rank fixes by risk and cost, prepare grounded rebuttals, and verify that promised revisions are actually traceable. Keep this skill separate from `paper-writing`, `paper-figures-tables`, and any external literature-management workflow.

## Boundaries

- Do not invoke external literature-management tools or separate review/rebuttal builders by default. Use them only when the user explicitly asks for that separate workflow.
- Do not perform automatic citation retrieval or reference verification. Use the citation and evidence sources declared by the user or project; local `.bib`, manuscript text, and supplied notes are the default.
- Do not invent experiments, numbers, p-values, baselines, reviewer comments, citations, links, or revision status.
- Do not rewrite prose as the primary deliverable. Route substantial prose drafting to `paper-writing`.
- Do not redraw or typeset figures/tables as the primary deliverable. Route artifact creation or revision to `paper-figures-tables`.
- Do not submit reviews, rebuttals, or OpenReview/CMT/HotCRP responses for the user. Produce drafts and checks for user sign-off.
- Do not treat local house policy as a rejection criterion when formally reviewing someone else's paper. Apply the policy readiness gate to the user's own manuscript workflows only.

## Source Priority

When reviewing or drafting responses, use evidence in this order:

1. Core integrity constraints from the sibling `paper-policy` skill.
2. User-confirmed facts, experimental results, revision decisions, and author intent.
3. Verified venue or template requirements with source and freshness date.
4. The current manuscript, local LaTeX/PDF/source files, local tables/figures, and local `.bib`.
5. Reviewer comments and local rebuttal drafts.
6. Rules from explicitly activated policy sets and the skill references listed below.

If a likely needed citation is missing locally, use the manual handoff format in `references/citation-and-evidence-policy.md`. Do not search, fetch, or validate references unless the user explicitly asks for that separate task.

## Mode Routing

Read `references/review-modes.md` for mode details, then load only the references needed for the request.

- **Pre-submission audit**: read `policy-compliance.md`, `pre-submission-audit.md`, `quality-gates.md`, and `citation-and-evidence-policy.md`.
- **Red-team my draft / simulate reviewers**: read `policy-compliance.md`, `reviewer-panel.md`, `issue-board.md`, and `quality-gates.md`; use policy as a diagnostic surface, not as proof of reviewer reaction.
- **Formal review of someone else's paper**: read `reviewer-panel.md`, `pre-submission-audit.md`, and `quality-gates.md`; keep tone fair and evidence-bound.
- **Analyze external reviews**: read `issue-board.md`, `rebuttal-strategy.md`, and `citation-and-evidence-policy.md`.
- **Draft or polish rebuttal**: read `rebuttal-strategy.md`, `rebuttal-drafting.md`, `revision-plan.md`, and `quality-gates.md`.
- **Verify revised manuscript after rebuttal**: read `policy-compliance.md`, `revision-plan.md`, `quality-gates.md`, and the relevant writing or figure/table handoff rules.

## Default Workflow

1. Identify the mode, manuscript stage, venue if known, deadline pressure, and available inputs.
2. For the user's own audit or revision-verification workflow, resolve policy and run the read-only compliance assessment in `policy-compliance.md`.
3. Establish an evidence map: manuscript locations, local results, local `.bib`, reviewer comments, user-confirmed constraints.
4. Atomize failures and unresolved evidence into issue cards instead of free-form critique.
5. Classify each issue by severity, policy status, evidence anchor, affected claim, and required action.
6. Apply quality gates: provenance, coverage, commitment, tone, fairness, citation policy, readiness, and handoff routing.
7. Return the most actionable artifact for the mode: compliance audit, reviewer-panel report, issue board, rebuttal strategy, rebuttal draft, or revision checklist.

## Required Review Discipline

- Every criticism must point to a manuscript location, reviewer quote, local artifact, or `MISSING` marker.
- Keep hard results in PASS, FAIL, UNVERIFIED, NOT_APPLICABLE, or WAIVED. Never convert missing evidence into PASS.
- Record an agent semantic/manual FAIL only when the manuscript provides a precise artifact, locator, and contradictory evidence. Never use an agent record to assign PASS, WAIVED, or NOT_APPLICABLE.
- Keep soft outcomes separate as APPLIED, ADAPTED, or SKIPPED; soft choices do not block submission readiness.
- Separate `substance` problems from `misread-risk` problems. Do not recommend new experiments for wording problems that can be fixed by narrowing or clarifying a claim.
- Diagnose concrete prose defects without using AI-detector, perplexity, authenticity, or human-likeness scores as compliance or readiness evidence; never infer AI authorship from style alone.
- Compare every Anti-AI revision with its source for changes in claim strength, causality, scope, terminology, citations, values, and caveats.
- When a characterized systematic error exists, verify the disclosed bias direction against the error mechanism and affected claims; require explicit indeterminacy when direction is unsupported.
- When evidence sources have different roles, verify that validation, calibration, control, case-study, and exploratory sources never silently support stronger substantive claims.
- Check whether the section and RQ order follows a coherent argumentative spine; treat this as adaptive structure, not a rejection criterion by itself.
- For load-bearing threats, require an affected claim or RQ, a supported mitigation or explicit absence, and a residual boundary after mitigation.
- Treat Related Work as a high-risk area. Enforce a comparison table only when `RELATED.COMPARISON_REQUIRED` is active; otherwise evaluate whether the comparison structure is adequate without imposing house style.
- Enforce traditional concise headings only when `STRUCT.TRADITIONAL_HEADINGS` is active. In formal reviews of other work, criticize headings only when they cause a concrete clarity or venue problem.
- For figures and tables, diagnose the issue and hand off to `paper-figures-tables` when creation, redesign, or LaTeX table work is needed.
- For prose rewrites, diagnose the issue and hand off to `paper-writing` when drafting is the main task.
- For rebuttals, answer every reviewer concern or explicitly mark it as deferred with a reason.

## Scripts

- Use `scripts/count_rebuttal_limit.py` when a rebuttal, author response, or per-reviewer reply has a character or word limit.
- For own-paper compliance audits, use the sibling `paper-policy/scripts/assess_compliance.py`; it reads artifacts and evidence without mutating them.
- For project-local first passes, inspect the sibling runner's section-aware
  `soft-review-worklist.yaml` and locator-rich unused-key report; neither output
  is compliance evidence or mutation authorization.

## Reference Index

- `references/review-modes.md`: mode selection and output shapes.
- `references/policy-compliance.md`: policy resolution, evidence statuses, waivers, and submission readiness.
- `references/pre-submission-audit.md`: manuscript audit dimensions and severity levels.
- `references/reviewer-panel.md`: reviewer personas, fairness firewall, and formal-review mode.
- `references/issue-board.md`: atomic issue schema for audits and external reviews.
- `references/rebuttal-strategy.md`: strategy selection, reviewer intent, and evidence planning.
- `references/rebuttal-drafting.md`: author-response structure, tone, and length discipline.
- `references/revision-plan.md`: mapping rebuttal promises to manuscript edits.
- `references/quality-gates.md`: final gates before returning a review or rebuttal artifact.
- `references/citation-and-evidence-policy.md`: local-only citation and evidence policy.
