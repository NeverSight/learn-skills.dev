---
name: survey-generation
description: Generate complete academic survey papers using multi-LLM parallel outline generation, RAG-based subsection writing, citation validation, and local coherence enhancement. Based on AutoSurvey pipeline. Use for writing comprehensive literature surveys.
argument-hint: [topic]
---

# Survey Generation

Generate complete academic survey papers with structured outline, RAG-based writing, and citation validation.

## Input

- `$0` — Survey topic or research area

## Scripts

### Literature search
```bash
python ~/.claude/skills/deep-research/scripts/search_semantic_scholar.py \
  --query "relevant search query" --max-results 50
```

## References

- Survey prompts (outline, writing, citation, coherence): `~/.claude/skills/survey-generation/references/survey-prompts.md`

## Workflow (from AutoSurvey)

### Step 1: Collect Papers
1. Search Semantic Scholar / arXiv for papers on the topic
2. Collect 50-200 relevant papers with titles and abstracts
3. Filter by relevance and citation count

### Step 2: Generate Outline (Multi-LLM Parallel)
1. Generate N rough outlines independently (parallel)
2. Merge outlines into a single comprehensive outline
3. Expand each section into subsections
4. Edit final outline to remove redundancies

### Step 3: Write Subsections (RAG-Based)
For each subsection:
1. Retrieve relevant papers for the subsection topic
2. Generate content with inline citations `[paper_title]`
3. Enforce minimum word count per subsection
4. Only cite papers from the provided list

### Step 4: Validate Citations
For each subsection:
1. Check that cited paper titles are correct
2. Verify citations support the claims made
3. Remove or correct unsupported citations
4. Use NLI (Natural Language Inference) for claim-source faithfulness

### Step 5: Enhance Local Coherence
For each subsection:
1. Read previous and following subsections
2. Refine transitions and flow
3. Preserve core content and citations
4. Ensure smooth reading experience

### Step 6: Convert Citations to BibTeX
1. Replace `[paper_title]` with `\cite{key}`
2. Generate BibTeX entries for all cited papers
3. Validate all citation keys exist in .bib file

## Output Structure

```
survey/
├── main.tex          # Complete survey paper
├── references.bib    # All citations
├── outline.json      # Survey outline
└── sections/         # Individual section files
```

## Rules

- Only cite papers from the collected paper list — never hallucinate citations
- Each subsection must meet minimum word count
- No duplicate subsections across sections
- Citation validation is mandatory before final output
- Local coherence enhancement must preserve all citations
- The survey should be comprehensive and logically organized

## Related Skills
- Upstream: [deep-research](../deep-research/), [literature-search](../literature-search/), [literature-review](../literature-review/)
- See also: [related-work-writing](../related-work-writing/)
