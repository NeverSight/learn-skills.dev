---
name: research-paper-review
description: Review and analyze academic research papers. Use this skill when the user asks to review a paper, analyze a publication, summarize research, critique methodology, extract key findings, compare papers, check for numerical inconsistencies, or assess novelty and contributions of academic work. Also triggers when the user mentions reading a PDF of a paper, wants a literature review, asks about related work, or wants to improve a paper before submission.
---

# Research Paper Review

Assist researchers in reviewing, analyzing, and criticizing academic papers systematically and thoroughly.

## When to Use

- User asks to review, summarize, or critique a research paper
- User shares a PDF or link to an academic paper
- User wants to assess methodology, contributions, or novelty
- User needs help writing a peer review
- User wants to compare multiple papers or do a literature survey
- User wants to improve a paper before submission (pre-submission review)
- User wants to check for numerical/statistical inconsistencies
- User wants venue-specific feedback (conference, journal, or preprint)

## Inputs

- Paper content: PDF, LaTeX source, or plaint text
- Target Venue (optional but recommended): conference, journal, or preprint target
               - Example: "Models 2026", "TOSEM", "Sosym", "arXiv preprint"
- Type of paper (**important — ask the user if not provided**): the review criteria change substantially by type. Common types: "full research" paper, "short" paper, "new ideas"/vision paper, "tool demo" paper, "poster", "extended abstract"/"short abstract", "journal"/"extended" paper. If the user does not state the type, ask before reviewing (or state the assumed type explicitly in the review).
- Explicit reviewing guidelines (optional): if available provide a description or URL with the reviewing criteria.

## Review Workflow

###Step 0: Pre-Processing / Venue Context

- If target venue and/or the type of paper are provided, include them as context for all subsequent steps:

> “Review this paper as if it is intended for [TARGET VENUE] as a [TYPE PAPER] submission. Consider typical standards, expectations, page limits, scope, and audience for this venue and type of paper”

- **Calibrate expectations to the paper type.** Do not apply full-paper standards to every submission. In particular, do not fault a paper for missing something its type does not require (e.g., do **not** criticize a tool demo paper for lacking a real-world validation study, or a vision paper for lacking large-scale experiments). Use the table below as the baseline, then adjust with the venue's own guidelines:

| Paper type | Primary evaluation focus | Validation expected | Common pitfalls to flag / *not* flag |
|-----------|--------------------------|---------------------|--------------------------------------|
| **Full research / journal (extended)** | Novelty, soundness, significance, completeness | Strong, thorough empirical or theoretical validation; complete related work; reproducibility | Flag weak/absent validation, thin related work, non-reproducible results |
| **Short paper** | A single focused, sound contribution | Preliminary but credible validation; scope intentionally narrow | Flag if the core claim is unsupported; do *not* flag limited scope or lack of exhaustive experiments |
| **New ideas / vision paper** | Novelty, potential impact, clarity of the idea | Conceptual argument or early evidence; full validation not required | Flag vague or unmotivated ideas; do *not* flag absence of experiments |
| **Tool demo paper** | Usefulness, maturity, architecture, availability, a clear demo scenario | Demonstration of the tool working; strong empirical/user validation is **not** required | Flag unclear tool value, no availability/reproducibility of the tool, missing demo walkthrough; do *not* flag lack of a real-world evaluation study |
| **Poster / extended abstract / short abstract** | Clarity of the idea and early-stage promise | Minimal; preliminary results at most | Flag unclear framing; do *not* flag limited depth, short related work, or minimal evaluation |

- If the paper type is unknown, ask the user (or state the assumption you are reviewing under) before applying validation criteria.

- Optional: Use the provided reviewing guidelines or try to find them on the venue website (if available) with standards for methodology, novelty, empirical rigor, validation and formatting. Venue-specific guidelines override the defaults above. 

### Step 1: Read the Paper

Identify the format and read accordingly:

- **PDF**: Use the Read tool with the `pages` parameter for large documents (max 20 pages per request).
- **LaTeX source**: Read the main `.tex` file first. Look for `\input{}` or `\include{}` commands to find additional sections, figures, and bibliography files. Use Grep to search for key commands like `\begin{abstract}`, `\section`, `\cite` across all `.tex` files.
- **Multiple files**: Use Glob with `**/*.tex` to find all source files, then read them in logical order (main file → sections → appendix).

In all cases, skim the abstract, introduction, and conclusion first to get the big picture before diving into details.

### Step 2: Structured Summary

Show that you understand the paper by producing a summary covering:

1. **Problem Statement** — What problem does the paper address? Why does it matter?
2. **Contributions** — What are the claimed contributions? (list them)
3. **Approach/Methodology** — How do the authors solve the problem?
4. **Key Results** — What are the main findings/metrics?
5. **Limitations** — What are the acknowledged (and unacknowledged) limitations?


### Step 3: Numerical & Consistency Checks   - most info from linkedin

This is where LLM-assisted review adds the most value, catching things humans easily miss during manual review. Run these checks systematically:

- **Numbers across text, tables, and figures**: Do values reported in the text match what's in the tables? Do figures reflect the data described?
- **Statistical consistency**: Do p-values, confidence intervals, and effect sizes align? Are sample sizes consistent throughout?
- **Calculations**: Verify percentages, averages, sums. Check that reported improvements (e.g., "30% improvement") match the actual numbers.
- **Internal references**: Do all \ref, \cite, figure/table references resolve? Are there dangling references or wrong numbering?
- **Acronyms**: Are all acronyms defined on first use?
- **Terminology consistency**: Is the same concept always referred to with the same term?
- **Citations**: Do all citations exist? Is citation style uniform (i.e. all conference papers are cited using the same fields, same for other venues) 

Even minor errors (typos, broken references, wrong numbering) matter. reviewers often use these as signals that the paper was not carefully prepared.

### Step 4: Critical Analysis

Evaluate the paper on these dimensions, **weighting them according to the paper type** (see the calibration table in Step 0). For example, weight *Reproducibility* and *Soundness* heavily for a full/journal paper, but weight *Significance* (tool usefulness, availability, demo clarity) more than exhaustive *Soundness* for a tool demo, and *Novelty*/*Clarity* over *Soundness* for a vision paper. When a dimension is not applicable to the paper type, say so explicitly rather than penalizing the paper for it.

| Dimension | Questions to Answer |
|-----------|-------------------|
| **Novelty** | Is this genuinely new? How does it differ from prior work? |
| **Soundness** | Is the methodology rigorous? Are experiments well-designed? |
| **Significance** | Does this advance the field meaningfully? |
| **Clarity** | Is the paper well-written and well-structured? |
| **Reproducibility** | Could someone replicate this work from the paper alone? |
| **Related Work** | Is the positioning against prior work fair and complete? |
| **Venue Alignment** | Does the paper meet expectations of the target venue (scope, depth, format, length, contribution type)? |


### Step 5: Provide Actionable Feedback

Structure feedback as:

- **Strengths** — What the paper does well (be specific, cite sections)
- **Weaknesses** — What could be improved (be constructive, suggest fixes)
- **Questions for Authors** — Things that need clarification
- **Minor Issues** — Typos, formatting, citation issues, broken references
- **Venue-Specific Recommendations** — Highlight alignment issues, potential improvements to meet venue expectations

### Step 6: Start here

Write down a list of the top 10 most immediate actions that the author should address. 

These should be the ones that will bring the best "bang for the buck", i.e. actions that generate the most benefit relative to the cost of implementing them.


## Output Format

Use this template for the review:

```markdown
# Paper Review: [Title]

## Summary
[2-3 paragraph summary]

## Strengths
- S1: ...
- S2: ...

## Weaknesses
- W1: ...
- W2: ...

## Questions for Authors
- Q1: ...

## Minor Issues
- ...

## Venue-Specific Recommendations
- V1: ...
- V2: ...

## Overall Assessment
[1 paragraph verdict: accept/revise/reject with justification]

## Top actions . Start here
- T1: ...
- T2: ...


## Confidence
[Your confidence level in this review: low/medium/high, and why]
```
