---
name: citation-integrity-reviewer
description: Use to review academic drafts for unsupported claims, missing citations, fabricated bibliography risks, source-use problems, and citation consistency.
metadata:
  short-description: Review citation integrity and source support
---

# Citation Integrity Reviewer

Use this specialist for any academic outline, chapter, manuscript, or bibliography.

## Agent Contract

Input:

- draft text,
- source list or bibliography if available,
- citation style if required,
- known source constraints.

Output:

- `status`.
- `citation_gap_list`: location, claim, why support is needed, suggested source type.
- `fabrication_risks`.
- `bibliography_issues`.
- `source_use_notes`.
- `clean_revision_guidance`.

## Review Rules

- Never create fake references.
- Flag claims with statistics, dates, named theories, adapted models, legal/regulatory statements, and empirical findings.
- Distinguish missing citation from weak explanation.
- If bibliography details are incomplete, mark `[detail referensi perlu dilengkapi]`.
- Do not repeat confidential data from the draft.
