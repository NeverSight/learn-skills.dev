---
name: literature-review
description: Conduct comprehensive literature reviews using multi-perspective dialogue simulation. Generate diverse expert personas, conduct grounded Q&A conversations, and synthesize findings into structured knowledge. Use when starting a new research project or writing a survey section.
argument-hint: [topic]
---

# Literature Review

Conduct deep literature reviews through multi-perspective dialogue and systematic search.

## Input

- `$0` — Research topic or question
- `$1` — Optional: specific focus or angle

## References

- Multi-perspective dialogue prompts (STORM): `~/.claude/skills/literature-review/references/dialogue-prompts.md`
- Literature review workflow (AgentLaboratory): `~/.claude/skills/literature-review/references/review-workflow.md`

## Scripts (from literature-search skill)

```bash
# Search Semantic Scholar
python ~/.claude/skills/deep-research/scripts/search_semantic_scholar.py --query "topic" --max-results 20

# Search OpenAlex
python ~/.claude/skills/literature-search/scripts/search_openalex.py --query "topic" --max-results 20

# Search arXiv
python ~/.claude/skills/deep-research/scripts/search_arxiv.py --query "topic" --max-results 10
```

## Workflow

### Step 1: Generate Expert Personas (from STORM)
Given the topic, create 3-5 diverse expert personas:
- Each represents a different perspective, role, or research angle
- Example: "ML systems researcher focused on efficiency", "Theoretical statistician concerned with guarantees"
- Use the persona generation prompts from references

### Step 2: Multi-Perspective Dialogue
For each persona, simulate a multi-turn Q&A conversation:
1. **Persona asks a question** from their unique angle
2. **Generate search queries** from the question
3. **Search literature** using the search scripts
4. **Synthesize an answer** grounded in retrieved papers with inline citations
5. **Record the dialogue turn** with search results
6. Repeat for 3-5 turns per persona
7. End when persona says "Thank you so much for your help!"

### Step 3: Synthesize Knowledge
- Combine all persona conversations into a unified knowledge base
- Remove redundancy across personas
- Organize by theme/subtopic
- Generate an outline based on the collected information

### Step 4: Generate Literature Review
- Write a structured review organized by the generated outline
- Every claim must be supported by a citation
- Include a summary table of key papers (method, contribution, limitations)

## Output

A structured literature review with:
1. **Outline** — Hierarchical topic structure
2. **Per-section summaries** — Each grounded in retrieved papers
3. **Paper database** — Structured entries for all reviewed papers
4. **Knowledge gaps** — Identified areas needing further investigation

## Rules

- Every sentence in the review must be supported by gathered information
- If information is not found, explicitly state the gap
- Cite broadly — cover diverse approaches, not just the most popular
- Include recent papers (last 2-3 years) alongside foundational work
- Use inline citations: "Smith et al. [1] propose..."

## Related Skills
- Upstream: [literature-search](../literature-search/), [deep-research](../deep-research/)
- Downstream: [related-work-writing](../related-work-writing/), [research-planning](../research-planning/)
- See also: [survey-generation](../survey-generation/)
