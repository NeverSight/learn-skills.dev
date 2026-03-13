---
name: hackathon-doc-writer
description: >-
  Generate structured technical documentation artifacts including ADRs, PRDs, and feature specs for a hackathon project.
---
# hackathon-doc-writer

## Goal
Generate structured technical documentation artifacts (ADR, PRD, feature specs) for a hackathon project using the appropriate template.

---

## Trigger Conditions

Use this skill when:
- MVP scope is locked and needs to be documented in a PRD
- An architectural decision has been made that should be recorded in an ADR
- A specific feature needs a formal spec before implementation begins
- Invoked during Phase 4 (Project Planning), after `hackathon-scope-cutter` completes
- Can be re-invoked any time a new architectural decision is made during implementation

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `document_type` | enum | Yes | One of: `ADR`, `PRD`, `feature-spec` |
| `project_title` | string | Yes | Name of the project |
| `problem_statement` | string | Yes | Core problem being solved |
| `mvp_features` | string[] | Yes | MVP feature list from `hackathon-scope-cutter` |
| `tech_stack` | string[] | Yes | Technologies being used |
| `architecture_decisions` | object[] | No | For ADR: list of decisions with context and rationale |
| `feature_name` | string | No | For feature-spec: name of the specific feature |
| `constraints` | string[] | No | Technical or product constraints |

---

## Outputs

| Output | Description |
|---|---|
| `document` | Fully populated document in Markdown |
| `document_type` | Type of document generated |
| `missing_fields` | Sections that could not be completed due to missing input |

---

## Rules

1. Use the corresponding template from `templates/` directory as the output structure.
2. Do not omit any section from the template; use `[TBD]` for missing information.
3. Keep language direct and scannable — no filler paragraphs.
4. For ADR: capture exactly one architectural decision per document.
5. For PRD: include success metrics even if they are estimates.
6. For feature-spec: include acceptance criteria as testable conditions.
7. Flag all `[TBD]` sections in `missing_fields` output.

---

## Output Format

```yaml
document_type: "<ADR|PRD|feature-spec>"

missing_fields:
  - "<section name>"

document: |
  <Full Markdown document content>
```

---

## Example

**Input:**
```yaml
document_type: "ADR"
project_title: "AnchorAI"
problem_statement: "How might we provide always-available emotional support for college students?"
mvp_features:
  - "GPT-4 emotional check-in conversation"
  - "Session memory"
tech_stack: ["Python", "FastAPI", "React", "OpenAI API", "Redis"]
architecture_decisions:
  - title: "Session memory storage"
    context: "Need to persist conversation summaries between sessions"
    options: ["Redis (in-memory)", "SQLite (file)", "OpenAI conversation history API"]
    decision: "Redis"
    rationale: "Fastest to set up; sufficient for demo; team familiar with it"
```

**Output:**
```yaml
document_type: "ADR"
missing_fields: []
document: |
  # ADR-001: Session Memory Storage

  **Date:** 2025-06-14
  **Status:** Accepted

  ## Context
  AnchorAI must recall emotional context from past user sessions to deliver its core wow factor.
  Memory must persist across browser refreshes for the demo.

  ## Decision
  Use Redis as an in-process session store keyed by a hardcoded demo user ID.

  ## Consequences
  - Positive: Setup takes <30 minutes; team knows Redis well
  - Negative: Data is lost on server restart; not production-ready
  - Risk: Redis unavailable on demo machine → mitigation: fallback to in-memory dict
```

---

## Context Files

### Knowledge Base

- `knowledge/hackathon-reference-architecture.md`
- `knowledge/hackathon-mvp-strategy.md`

### Templates

- `templates/ADR-template.md`
- `templates/PRD-template.md`
- `templates/feature-spec-template.md`

### Playbooks

- `playbooks/hackathon-workflow.md`
