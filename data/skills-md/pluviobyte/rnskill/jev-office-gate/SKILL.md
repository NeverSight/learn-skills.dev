---
name: jev-office-gate
description: Add a Jev-powered decision and release gate after an office assistant generates a report, proposal, spreadsheet, document, or slide deck. Use for claim-to-evidence checks, narrow requirement decisions, risk triage, and human-review routing; do not use it to generate the deliverable or claim that Jev browsed or verified a URL.
---

# Jev Office Gate

Use Jev as a narrow judgment layer after an office assistant has produced a deliverable. Keep the producing assistant and Jev separate unless an actual product integration is verified.

## Workflow

1. Identify the deliverable and its release criteria. Preserve the user's requested format and office tool.
2. Extract bounded review items. For citation review, each item needs a claim and an excerpt copied from the source. A URL alone is not evidence.
3. Run deterministic checks outside Jev when relevant: file opens, links resolve, quoted text exists, dates and numbers match, formulas calculate, required sections exist, and document layout renders in the target application.
4. Use Jev only for narrow questions with predefined choices. Prefer claim support, evidence disposition, contradiction/overclaim risk, requirement coverage, or routing priority.
5. Apply explicit thresholds and route uncertain or consequential items to a human. Never treat model probability as calibrated truth without task-specific evaluation.
6. Return a release table with the original item, deterministic findings, Jev probabilities, decision, reasons, and required human action. Keep the original generated file unchanged unless the user asked for edits.

## Citation gate

Use [scripts/jev_office_gate.py](scripts/jev_office_gate.py) for repeatable claim-to-evidence review. Read [references/input-schema.md](references/input-schema.md) when preparing its JSON input.

Default review questions:

- Does the supplied excerpt support the full claim?
- Is the supplied source suitable as a formal citation, supporting context, unusable, or in need of manual review?
- Does the supplied claim/excerpt pair show an obvious semantic conflict or overclaim risk?

The default thresholds are starting points: support below `0.70`, risk above `0.60`, disposition confidence below `0.50`, or any disposition other than `formal_source` routes the item to review. A selected contradiction or `cannot_use` result becomes an automatic rejection only when its option probability is at least `0.80`. Calibrate these values on representative examples before automating release.

## Other office decisions

For requirement coverage, row classification, or routing, read [references/decision-patterns.md](references/decision-patterns.md). Keep the state small and the answer space fixed. Split compound decisions into separate questions.

## Boundaries

- Jev does not fetch pages, test URL reachability, authenticate a source, or know whether an excerpt was copied correctly.
- Do not call it a fact checker. Report that it judged the supplied state and choices.
- Use code for exact arithmetic, dates, identifiers, string matching, link checks, file integrity, and spreadsheet formulas.
- Avoid asking one question to combine relevance, freshness, authority, and factual support. Split these dimensions or handle deterministic parts in code.
- Treat company statements as self-disclosure, not independent verification.
- For legal, medical, financial, compliance, or externally binding decisions, Jev may prioritize review but must not be the final approver.
- If Jev is unavailable or credentials are absent, preserve the same review table and mark the judgment columns for human review. Do not pretend the API ran.

## Credentials

The helper reads `TYPESAFE_API_KEY` by default and also accepts `JEV_API_KEY`. Never place an API key in a document, prompt, source file, or saved review artifact.
