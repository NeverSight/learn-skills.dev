---
name: paper-writing-section
description: Write a specific section of an academic paper (Abstract, Introduction, Background, Related Work, Methods, Experiments, Results, Discussion/Conclusion) with section-specific guidance and two-pass refinement. Use when the user wants to write, draft, or improve a paper section.
argument-hint: [section-name]
---

# Paper Section Writer

Write a publication-quality section for an academic paper.

## Input

- `$0` — Section name: `abstract`, `introduction`, `background`, `related-work`, `methods`, `experimental-setup`, `results`, `discussion`, `conclusion`
- `$1` — (Optional) Path to context file (research plan, results, prior sections)

## Workflow

### Step 1: Gather Context
Read the paper's existing `.tex` files, experiment logs, result files, and any provided context. Understand: title, contributions, methodology, key results, figures, tables.

### Step 2: Write the Section
Load section-specific tips from `references/section-tips.md`. Before every paragraph, include a brief plan as a LaTeX comment (`% Plan: ...`).

### Step 3: Two-Pass Refinement
Apply both refinement passes from `references/refinement-prompts.md`:
- **Pass 1**: Fix errors (unenclosed math, broken refs, hallucinated numbers, duplicate labels)
- **Pass 2**: Remove redundancies, compress, ensure smooth transitions

## References

- Section writing tips: `~/.claude/skills/paper-writing-section/references/section-tips.md`
- Refinement prompts and error checklist: `~/.claude/skills/paper-writing-section/references/refinement-prompts.md`

## Output

LaTeX fragment (no `\documentclass`, no preamble). All math enclosed in `$...$` or `\begin{equation}`, all figures referenced with `\ref{}`, all cited works use `\cite{}`, no placeholder text.

## Quality Checklist
- All math enclosed properly
- All `\ref{}` and `\cite{}` valid
- No TODO/TBD/FIXME markers
- Numbers match experimental logs exactly
- Writing style is objective — no hype words
- Section length appropriate for venue

## Related Skills
- Upstream: [data-analysis](../data-analysis/), [figure-generation](../figure-generation/), [table-generation](../table-generation/), [related-work-writing](../related-work-writing/)
- Downstream: [latex-formatting](../latex-formatting/), [citation-management](../citation-management/)
- See also: [paper-assembly](../paper-assembly/)
