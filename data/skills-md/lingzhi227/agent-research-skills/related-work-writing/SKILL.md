---
name: related-work-writing
description: Write Related Work sections that compare and contrast prior work with your approach. Organize by theme, cite broadly, and explain how your work differs. Use when writing or improving the Related Work section of a paper.
argument-hint: [paper-draft]
---

# Related Work Writing

Generate publication-quality Related Work sections with proper citations and thematic organization.

## Input

- `$0` — Current paper draft or method description
- `$1` — Collected literature (BibTeX entries, paper summaries, or literature review notes)

## References

- Related work writing prompts and strategies: `~/.claude/skills/related-work-writing/references/related-work-prompts.md`

## Workflow

### Step 1: Analyze the Paper's Contributions
- Read the current paper draft (especially Methods and Introduction)
- Identify the key contributions and novelty claims
- List the technical components that need literature context

### Step 2: Organize Literature by Theme
Group related papers into thematic clusters:
- Each cluster should represent a research direction or technique
- Common themes: problem formulation, methodology family, application domain, evaluation approach
- Order themes from most to least relevant to your work

### Step 3: Write Each Theme Paragraph
For each thematic group:
1. **Topic sentence** — Introduce the research direction
2. **Describe key works** — Summarize 2-5 representative papers
3. **Compare and contrast** — How does each approach differ from yours?
4. **Transition** — Connect to the next theme or to your contribution

### Step 4: Refine
- Ensure every cited paper has a clear reason for inclusion
- Check that your work's novelty is clear from the comparisons
- Verify all `\cite{}` keys exist in the `.bib` file
- Aim for 1-2 pages (single column) or 0.5-1 page (double column)

## Rules

- **Compare and contrast, don't just describe** — "Unlike [X] which assumes..., our method..."
- **Organize by theme, not chronologically** — Group by research direction
- **Cite broadly** — Not just the most popular papers; include recent and diverse work
- **Be fair** — Acknowledge strengths of prior work before stating limitations
- **Explain inapplicability** — If a method could apply to your setting, explain why you don't compare experimentally, or add it to experiments
- **Use present tense for established facts** — "Smith et al. propose..." or "This approach uses..."
- **End with positioning** — The final paragraph should clearly position your work relative to all discussed prior work

## Related Skills
- Upstream: [literature-search](../literature-search/), [literature-review](../literature-review/), [citation-management](../citation-management/)
- Downstream: [paper-writing-section](../paper-writing-section/)
- See also: [survey-generation](../survey-generation/)
