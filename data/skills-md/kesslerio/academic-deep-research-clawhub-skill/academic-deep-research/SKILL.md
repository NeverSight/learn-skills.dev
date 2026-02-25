---
name: academic-deep-research
description: Transparent, rigorous research with full methodology — not a black-box API wrapper. Conducts exhaustive investigation through mandated 2-cycle research per theme, APA 7th citations, evidence hierarchy, and 3 user checkpoints. Self-contained using native OpenClaw tools (web_search, web_fetch, sessions_spawn). Use for literature reviews, competitive intelligence, or any research requiring academic rigor and reproducibility.
homepage: https://github.com/kesslerio/academic-deep-research-clawhub-skill
metadata:
  openclaw:
    emoji: 🔬
---

# Academic Deep Research 🔬

## When to Use

Trigger this skill when the user wants:
- Deep research, exhaustive analysis, or literature review
- Multi-source verification and evidence hierarchies
- Academic-style reports with citations

## Required Stop Points

1. **Initial engagement**: ask 2–3 clarifying questions and confirm understanding.
2. **Research plan**: present themes, steps, and deliverables; wait for approval.
3. **Final report**: deliver full narrative report with citations.

## Minimum Requirements

- Two full research cycles per theme.
- Analyze between every tool call.
- Multiple sources per claim; contradictions addressed.
- APA 7th in-text citations and reference list.
- Narrative-only final report (no lists or tables).

## References

- `reference/protocol.md` — research phases, tool order, and analysis rules
- `reference/writing-style.md` — narrative constraints and phase formatting
- `reference/citations-apa.md` — citation rules and examples
- `reference/report-template.md` — required report structure
- `reference/error-handling.md` — gaps, contradictions, failures
- `reference/quality-standards.md` — evidence hierarchy and confidence levels
- `reference/parallel-research.md` — sessions_spawn workflow
- `quickref.md` — short checklist
- `example.md` — sample usage
