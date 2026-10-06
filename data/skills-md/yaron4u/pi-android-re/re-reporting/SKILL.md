---
name: re-reporting
description: Build high-quality reverse-engineering reports from raw findings. Focus on argument structure, evidence quality, and graph planning. Delegate graph implementation scripts to python-scripting skill.
---

# re-reporting skill

## Purpose
Turn technical findings into publishable reports with:
- clear claim chains,
- right evidence per claim,
- correct graph selection,
- strong narrative flow.

## Inputs expected
- raw notes / PoCs / logs / decomp snippets
- source reports for style calibration
- target audience (exec / IR / exploit dev / product security)

## Output contract
Always produce:
1. report outline,
2. evidence-to-claim map,
3. graph plan (question -> visual -> data needed -> acceptance checks),
4. drafting pass using templates,
5. self-score with rubric.

For non-technical or mixed audiences, drafting pass must be two-layer:
- Layer 1: plain-English one-page summary (what happened, business risk, what to do now).
- Layer 2: technical appendix (claim/evidence depth, artifacts, PoC details).

## Hard rules
- No claim without evidence.
- No graph without a single explicit question.
- One figure = one job.
- Put limitations/assumptions in every impact section.
- Keep exploit details safe and audience-appropriate.
- Every finding section must include a one-line "So what" impact statement in plain language.
- Put jargon behind a short glossary if audience is not exploit-dev.
- Do not lead with audit-only visuals (evidence matrices/confidence scoring) for executive readers.

## Graph workflow
1. Read `references/graph-selection-matrix.md`.
2. Pick graph by question, not by aesthetics.
3. Validate against `references/graph-anti-patterns.md`.
4. Run reader-relevance check before finalizing each figure:
   - If removed, would decision quality drop?
   - Can a manager explain the figure in 20 seconds?
   - Does caption state exactly what to notice?
5. Write a graph spec block for python-scripting:
   - objective question
   - dataset schema
   - encoding map
   - style constraints
   - pass/fail checks

### Tool guidance
- **matplotlib**: static publication charts, fine control.
- **seaborn**: statistical distributions / confidence visuals.
- **plotly**: interactive exploratory or polished stakeholder drill-down.
- **altair**: concise declarative charts.
- **graphviz**: architecture and flow graphs.
- **mermaid**: quick in-report flow/sequence diagrams.

## Handoff format to python-scripting
Use this exact block:

```md
### GRAPH_SPEC
- graph_id:
- question:
- audience:
- data_inputs:
- chart_type:
- library_priority: [matplotlib|seaborn|plotly|altair|graphviz|mermaid]
- encodings:
- annotations_required:
- anti_patterns_to_avoid:
- output_files:
- acceptance_tests:
```

## Local references
- `references/report-structure-playbook.md`
- `references/evidence-to-claim-mapping.md`
- `references/graph-selection-matrix.md`
- `references/graph-anti-patterns.md`
- `references/graph-tool-notes-context7.md`
- `references/re-report-rubric.md`
- `assets/report-templates/*`
- `assets/style-profiles/*`
- `examples/liked-reports/*`
- `examples/extracted-style-notes.md`
