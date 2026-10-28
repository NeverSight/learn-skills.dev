---
name: Life-Science-Evidence-Review
description: Generate evidence-based literature reviews, structured evidence synthesis, and knowledge-gap analyses for life science research.
---

# Life-Science-Evidence-Review

## Purpose

This Skill generates evidence-based literature reviews for life science research.

Rather than simply summarizing publications, it performs:

- systematic literature search
- biological context expansion
- evidence extraction
- critical evidence appraisal
- evidence synthesis
- thematic synthesis
- knowledge gap analysis
- future research planning

The final review should be generated from the structured Evidence Database, with every major conclusion traceable to one or more primary publications.

---

## When to Use

Use this Skill whenever the user requests:

- a literature review
- an evidence synthesis
- a research overview
- a knowledge gap analysis
- a gene review
- a pathway review
- a review of a biological process
- a review of a signaling pathway
- a review of a gene family
- a research roadmap for a biological topic

Typical examples include:

- "Review the genetics of human height."
- "Summarize current knowledge of rice grain quality."
- "Review flowering-time regulation in Arabidopsis."
- "Review CRISPR applications in crop breeding."
- "Review the evolution and functional diversification of the FatB gene family in rice."

---

## Required Input

The user should ideally provide:

### Required

- Species
- Trait or biological topic

### Optional

- Representative gene(s)
- Biological pathway
- Research question
- Time range
- Preferred journals
- Target output language

If representative gene(s) are not provided, infer biologically relevant candidate genes from the literature whenever appropriate.

---

## Execution

Follow the instructions in the following files in order:

1. prompt.md
2. workflow.md
3. output.md

Treat:

- **prompt.md** as the global behavioral specification.
- **workflow.md** as the reasoning and evidence synthesis protocol.
- **output.md** as the output specification.

Never skip workflow steps.

Always generate every deliverable defined in the Output Specification unless the user explicitly requests otherwise.

---

## Scientific Standards

Always:

- Prefer primary literature.
- Preserve the original meaning of published findings.
- Distinguish evidence from speculation.
- Evaluate evidence critically.
- Compare studies rather than summarize them individually.
- Clearly identify consensus and conflicting evidence.
- Clearly distinguish established knowledge, evidence-supported conclusions, emerging evidence, and hypotheses.

Never:

- Fabricate references.
- Fabricate DOI numbers.
- Fabricate publication links.
- Invent experimental results.
- Present hypotheses as established facts.

If sufficient evidence cannot be verified, explicitly acknowledge the limitation rather than generating unsupported conclusions.
