---
name: research-spike
description: "Conducts time-boxed technical investigations, competitive research, or feasibility analysis. Asks clarifying questions upfront and produces a structured markdown report with executive summary. Use for technical spikes, architecture decisions, or evaluating new technologies."
---

# Research Spike

Conduct time-boxed technical investigations with structured, citation-backed output.

## When to Use This Skill

- Technical spikes before implementing unfamiliar technology
- Architecture decision records (ADRs) requiring research
- Competitive analysis of tools, libraries, or platforms
- Feasibility studies for proposed features
- Evaluating migration paths or upgrade strategies
- Understanding best practices for a domain

## Research Modes

### Technical Spike
Focused investigation of a specific technology, pattern, or implementation approach. Output emphasizes practical findings, code examples, and implementation recommendations.

### Competitive Research
Comparison of multiple options (libraries, services, approaches). Output emphasizes feature matrices, trade-off analysis, and selection criteria.

### Feasibility Analysis
Assessment of whether a proposed approach is viable. Output emphasizes constraints, risks, effort estimation factors, and go/no-go recommendation.

## Upfront Questions

Before beginning research, use AskUserQuestion to clarify:

1. **Research Type**
   - Technical spike (deep dive on one topic)
   - Competitive research (compare options)
   - Feasibility analysis (assess viability)

2. **Depth Level**
   - Quick exploration (15-20 min equivalent, high-level overview)
   - Standard (45-60 min equivalent, actionable depth)
   - Deep dive (comprehensive, production-ready guidance)

3. **Scope Constraints**
   - Specific technologies to include or exclude
   - Constraints (budget, team expertise, existing stack)
   - Success criteria or decision factors

## Research Methodology

### Phase 1: Scope Definition
- Confirm research question and boundaries
- Identify key terms and concepts
- List known constraints and requirements

### Phase 2: Research Planning
- Identify information sources (web, documentation, codebase)
- Break down into sub-questions if needed
- Prioritize areas based on user's decision factors

### Phase 3: Information Gathering
- Web search for documentation, tutorials, comparisons
- Explore relevant parts of the codebase if applicable
- Gather data points, examples, and evidence
- Track all sources for citation

### Phase 4: Synthesis and Analysis
- Organize findings by theme or question
- Identify patterns, trade-offs, and insights
- Formulate recommendations based on evidence
- Note gaps or areas of uncertainty

### Phase 5: Output Generation
- Write structured report following template
- Ensure all claims cite sources
- Review for completeness and accuracy

## Output Format

Save output to: `research/[topic-slug]/spike-report.md`

### Report Template

```markdown
# [Research Topic]

**Type**: [Technical Spike | Competitive Research | Feasibility Analysis]
**Depth**: [Quick | Standard | Deep]
**Date**: [YYYY-MM-DD]

## Executive Summary

[One-pager synopsis, <250 words. Key findings, recommendation, and confidence level. A busy stakeholder should be able to read only this section and understand the conclusion.]

## Background

### Context
[Why this research was conducted, what triggered it]

### Research Question
[The specific question(s) being answered]

### Scope
[What is and isn't covered, constraints applied]

## Methodology

[Brief description of research approach, sources consulted, tools used]

## Findings

### [Finding Category 1]
[Detailed findings with evidence]

**Sources**: [Citations]

### [Finding Category 2]
[Detailed findings with evidence]

**Sources**: [Citations]

[Continue as needed...]

## Analysis

### Trade-offs
[Key trade-offs identified, with context for when each option is preferable]

### Risks
[Potential risks, unknowns, or concerns]

### Decision Matrix (if competitive research)
| Criteria | Option A | Option B | Option C |
|----------|----------|----------|----------|
| [Factor] | [Score/Note] | [Score/Note] | [Score/Note] |

## Recommendations

### Primary Recommendation
[Clear, actionable recommendation with rationale]

### Alternative Approaches
[Other viable options if primary doesn't fit]

### Confidence Level
[High/Medium/Low with explanation of what would increase confidence]

## Next Steps

1. [Concrete action item]
2. [Concrete action item]
3. [Concrete action item]

## Appendix

### Sources
[Numbered list of all sources cited]

### Glossary (if needed)
[Definitions of technical terms]

### Raw Notes (if applicable)
[Additional detail that didn't fit in main sections]
```

## Quality Gates

Before finalizing output, verify:

- [ ] All factual claims cite a source
- [ ] Executive summary is under 250 words
- [ ] Recommendations are actionable and specific
- [ ] Trade-offs are presented objectively
- [ ] Confidence level is stated with justification
- [ ] Next steps are concrete and prioritized
- [ ] No hallucinated features or capabilities
- [ ] Sources are verifiable (URLs work, docs exist)

## Anti-Hallucination Protocol

- Only state what sources explicitly confirm
- Use hedging language for inferences ("suggests", "likely", "based on X, we can infer")
- Clearly mark opinions vs facts
- If information cannot be verified, note it as "unverified" or "needs confirmation"
- When comparing options, only include features that are documented

## Instructions

1. Use AskUserQuestion to gather research type, depth, and constraints
2. Create the research output directory if it doesn't exist
3. Conduct research according to the methodology phases
4. Write findings progressively to the output file
5. Verify all quality gates before completing
6. Present a summary to the user with the file location
