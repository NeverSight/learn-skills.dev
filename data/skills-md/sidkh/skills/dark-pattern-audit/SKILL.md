---
name: dark-pattern-audit
description: Audit codebases and product copy for deceptive dark patterns that are inferable from local source code and text. Produce a structured narrative report with confidence, source locations, concise reasoning, and the official pattern link for each detected pattern.
disable-model-invocation: true
---

# Dark Pattern Audit

Audit a repository for dark patterns using only what is inferable from local source code and copy text. Do not rely on runtime inspection, screenshots, live browsing, telemetry, or external allegations.
Audit the entire repository by default unless the user narrows scope.

## Workflow

1. Confirm scope.
Default to the full repository. If the user names files, directories, or flows, constrain the audit to that scope.

2. Load the pattern catalog.
Read [pattern-index.md](./references/pattern-index.md) first. Open only the detailed pattern files that match candidate evidence.

3. Search for evidence in code and copy.
Look for product surfaces where dark patterns commonly appear:
- pricing, checkout, billing, fees, cart, upsells
- subscriptions, trials, renewal, cancellation
- consent, privacy, notification prompts, permissions
- modals, interstitials, nags, countdowns, stock counters
- preselected controls, bundled choices, forced steps
- misleading CTA text, disclaimers, low-contrast disclosures

Use fast repository search and then inspect surrounding implementation details. Prefer direct evidence in copy, component props, business logic, and tests over broad speculation.

4. Decide confidence conservatively.
Use:
- `likely` when the code or copy directly supports the pattern
- `possible` when the cues are meaningful but static analysis cannot prove the full behavior
- `insufficient evidence` for internal triage only; do not include these as findings in the final report

5. Write a structured narrative report.
Include only detected patterns with `likely` or `possible` confidence. If nothing persuasive is found, say:

`No dark patterns detected from the local codebase. That is a good sign.`

Then add a short caveat that static analysis cannot rule out runtime or operational behavior outside the repository.

## Output Template

# Dark Pattern Audit Report

## Summary
- Scope reviewed
- Method: local codebase and copy text only
- Result: number of detected dark patterns

## Detected Dark Patterns

### {Pattern Name}
- Confidence: `likely` or `possible`
- Source locations:
  - absolute file path with line references where possible
- Evidence:
  - concise narrative describing the relevant code, copy, or logic
- Reasoning:
  - brief explanation of why the evidence maps to this pattern
- Pattern link:
  - official deceptive.design URL

Repeat one section per detected pattern.

## Reporting Rules

- Use the exact pattern names from the catalog.
- Point to source locations for every finding.
- Do not include remediation advice unless the user asks for it later.
- Do not claim intent, legality, or proven harm unless the repository itself establishes it.
- Prefer exact strings, component names, flags, and control flow over vague claims.
- If evidence is weak, downgrade confidence or omit the finding.

## Reference Files

- Use [pattern-index.md](./references/pattern-index.md) as the navigation file.
- Open pattern files under `references/patterns/` only for relevant candidates.
- When new patterns are added later, add a new markdown file under `references/patterns/` and append it to the index.
