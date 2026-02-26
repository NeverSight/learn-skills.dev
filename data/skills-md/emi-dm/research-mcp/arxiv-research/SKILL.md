---
name: arxiv-research
description: Expert research assistant for querying and analyzing academic papers from arXiv. Use when the user needs to search for papers, analyze specific papers, extract methodology/findings, compare papers, or conduct literature reviews focused on Software Engineering and Computer Science research.
license: MIT
---

# arXiv Research Assistant

Expert workflow for conducting structured research on arXiv papers with optimized information extraction and analysis.

## Prerequisites

This skill requires the arXiv MCP server to be running. Ensure the server is started before use.

## Core Workflows

### 1. Finding Relevant Papers

**When to use:** User wants papers on a specific topic, methodology, or author.

**Process:**
1. Use `arxiv_search_papers` with clear keywords
2. Default searches Software Engineering (cs.SE) category
3. Review results and identify most relevant papers
4. For broad topics: start with recent papers (sort_by: "submitted_date")
5. For established topics: use relevance sorting

**Key parameters:**
- `query`: Be specific ("test generation neural networks" vs "testing")
- `max_results`: Start with 5-10, expand if needed
- `categories`: Empty `[]` to search beyond SE

### 2. Deep Paper Analysis

**When to use:** User needs detailed understanding of a specific paper.

**Structured extraction approach:**

```markdown
## Paper Analysis: [TITLE]

### 1. Core Contribution
- Main problem addressed
- Novel approach/solution
- Key insight or innovation

### 2. Methodology
- Research method (empirical, theoretical, survey, etc.)
- Datasets or subjects used
- Experimental design
- Evaluation metrics

### 3. Key Findings
- Primary results (with numbers/statistics)
- Performance comparisons
- Limitations acknowledged by authors

### 4. Implications
- Impact on the field
- Practical applications
- Future research directions

### 5. Related Work Context
- How it builds on prior work
- Key papers cited
- Position in research landscape
```

**Tools sequence:**
1. `arxiv_get_paper` - Get metadata first (authors, abstract, year)
2. `arxiv_query_paper` - Ask specific questions about content
3. `arxiv_convert_to_markdown` - Only if full text reading needed

### 3. Comparative Analysis

**When to use:** User wants to compare multiple papers or approaches.

**Process:**
1. Search and identify papers (2-5 papers max for deep comparison)
2. Extract comparable dimensions for each:
   - Problem scope
   - Methodology
   - Datasets/evaluation
   - Results
   - Year and citations context
3. Create structured comparison table
4. Synthesize insights: commonalities, differences, evolution

**Output format:**

```markdown
## Comparison: [TOPIC]

| Dimension | Paper 1 | Paper 2 | Paper 3 |
|-----------|---------|---------|---------|
| Approach | ... | ... | ... |
| Dataset | ... | ... | ... |
| Key Metric | ... | ... | ... |
| Results | ... | ... | ... |
| Year | ... | ... | ... |

### Key Insights
- **Trend:** ...
- **Best for X:** ...
- **Evolution:** ...
```

### 4. Literature Review

**When to use:** User needs comprehensive overview of a research area.

**Systematic approach:**
1. **Scope definition** - Clarify time range, subtopics, inclusion criteria
2. **Initial search** - Broad query, recent papers (last 2-3 years)
3. **Seed paper selection** - Identify 3-5 highly relevant papers
4. **Iterative expansion** - Search related terms, check citations
5. **Synthesis** - Group by themes, identify trends, gaps

**Output structure:**

```markdown
## Literature Review: [TOPIC]

### Research Landscape
- Number of papers found: X
- Time range: YYYY-YYYY
- Key categories: ...

### Major Themes
1. **Theme 1**: Description
   - Representative papers: [ID1, ID2]
   - Key findings: ...

2. **Theme 2**: Description
   - Representative papers: [ID3, ID4]
   - Key findings: ...

### Methodological Trends
- Dominant approaches: ...
- Evolution over time: ...

### Research Gaps
- Understudied areas: ...
- Contradictory findings: ...
- Future directions: ...

### Recommended Starting Papers
1. [Title] (ID) - Why: ...
2. [Title] (ID) - Why: ...
```

## Question Templates

Use these optimized questions with `arxiv_query_paper`:

**Methodology extraction:**
- "What specific methodology do the authors use? Include datasets, experimental setup, and evaluation metrics."
- "Describe the technical approach in detail. What algorithms or techniques are employed?"

**Results and findings:**
- "What are the quantitative results? Include specific metrics and comparisons to baselines."
- "What are the main findings and their statistical significance?"

**Critical analysis:**
- "What limitations do the authors acknowledge? What threats to validity are discussed?"
- "How does this work compare to previous approaches? What improvements are demonstrated?"

**Practical application:**
- "What are the practical implications of this work? How could it be applied in industry?"
- "What tools, code, or datasets did the authors release?"

**Research context:**
- "What future work do the authors suggest? What open questions remain?"
- "What are the key papers cited in related work? What gap does this paper fill?"

## Best Practices

### Information Extraction
1. **Start broad, then narrow** - Get abstract first, then query specific sections
2. **Be specific in queries** - "What evaluation metrics..." vs "Tell me about the paper"
3. **Cross-reference** - Verify important claims across abstract, methodology, and results
4. **Note limitations** - Always extract acknowledged limitations and threats to validity

### Efficiency Tips
1. **Use metadata first** - Abstract often answers high-level questions
2. **Batch similar papers** - Search once, analyze multiple results
3. **100-page limit** - For long papers, query specific sections instead of full conversion
4. **Cache key info** - Summarize important papers to avoid re-querying

### Critical Reading
1. **Evaluate methodology** - Is the evaluation rigorous? Are datasets appropriate?
2. **Check reproducibility** - Are methods described clearly? Is code/data available?
3. **Assess impact** - How many citations? Recent or dated?
4. **Context matters** - Consider publication venue and year

## Common Patterns

### Pattern: Research Question → Papers

```
User: "What are recent advances in LLM testing?"

1. arxiv_search_papers("LLM testing evaluation", sort_by="submitted_date")
2. Review top 5 papers
3. For 2-3 most relevant:
   - arxiv_query_paper: "What testing techniques are proposed?"
   - arxiv_query_paper: "What are the main results and limitations?"
4. Synthesize: summarize approaches, compare effectiveness, note trends
```

### Pattern: Paper → Understanding

```
User: "Explain paper 2301.12345"

1. arxiv_get_paper(arxiv_id)
2. Read abstract → identify key aspects
3. arxiv_query_paper: "What is the main contribution and methodology?"
4. arxiv_query_paper: "What are the quantitative results?"
5. arxiv_query_paper: "What limitations do authors discuss?"
6. Synthesize into structured analysis
```

### Pattern: Comparative Evaluation

```
User: "Compare mutation testing approaches in Papers X, Y, Z"

1. For each paper:
   - arxiv_get_paper → metadata
   - arxiv_query_paper: "What mutation operators are used?"
   - arxiv_query_paper: "What are the effectiveness metrics?"
2. Create comparison table
3. Synthesize: which approach for which context?
```

## Output Quality Standards

### Always Include
- **Paper IDs** - Full arXiv IDs for reference
- **Specifics** - Numbers, metrics, exact claims (not vague descriptions)
- **Context** - Year, venue, citation count when relevant
- **Limitations** - What the paper doesn't address
- **Actionability** - Practical takeaways or implications

### Avoid
- Vague summaries without specifics
- Uncritical acceptance of claims
- Mixing papers without clear attribution
- Overconfidence about papers not fully analyzed

## Troubleshooting

**"Too many results"** → Add more specific keywords, narrow time range, use categories filter

**"Paper too long to convert"** → Use `arxiv_query_paper` with specific questions instead of full conversion

**"Can't find specific methodology details"** → Query: "Describe the technical implementation and algorithms in detail"

**"Need newer/older papers"** → Use `sort_by: "submitted_date"` or add year to query ("software testing 2023")

**"Rate limit error"** → Wait 3-5 seconds between requests, batch queries when possible
