---
name: novelty-assessment
description: Assess research idea novelty through systematic literature search. Multi-round search-evaluate loops with harsh critic persona. Binary novel/not-novel decision with justification. Use before committing to a research direction.
argument-hint: [idea]
---

# Novelty Assessment

Rigorously assess whether a research idea is novel through systematic literature search.

## Input

- `$0` — Research idea description, title, or JSON file

## Scripts

### Automated novelty check
```bash
python ~/.claude/skills/idea-generation/scripts/novelty_check.py \
  --idea "Your research idea description" \
  --max-rounds 10 --output novelty_report.json
```

### Literature search
```bash
python ~/.claude/skills/deep-research/scripts/search_semantic_scholar.py \
  --query "relevant search query" --max-results 10
```

## References

- Assessment prompts and criteria: `~/.claude/skills/novelty-assessment/references/assessment-prompts.md`

## Workflow

### Step 1: Understand the Idea
- Identify the core contribution
- List the key technical components
- Determine the research area and subfield

### Step 2: Multi-Round Literature Search (up to 10 rounds)
For each round:
1. Generate a targeted search query
2. Search Semantic Scholar / arXiv / OpenAlex
3. Review top-10 results with abstracts
4. Assess overlap with the idea
5. Decide: need more searching, or ready to decide

### Step 3: Make Decision
- **Novel**: After sufficient searching, no paper significantly overlaps
- **Not Novel**: Found a paper that significantly overlaps

### Step 4: Position the Idea
If novel, identify:
- Most similar existing papers (for Related Work)
- How the idea differs from each
- The specific gap this idea fills

## Harsh Critic Persona

```
Be a harsh critic for novelty. Ensure there is a sufficient contribution
for a new conference or workshop paper. A trivial extension of existing
work is NOT novel. The idea must offer a meaningfully different approach,
formulation, or insight.
```

## Output Format

```json
{
  "decision": "novel" | "not_novel",
  "confidence": "high" | "medium" | "low",
  "justification": "After searching X rounds...",
  "most_similar_papers": [
    {"title": "...", "year": 2024, "overlap": "..."}
  ],
  "differentiation": "Our idea differs because..."
}
```

## Rules

- Minimum 3 search rounds before declaring novel
- Try to recall exact paper names for targeted queries
- A paper idea is NOT novel if it's a trivial extension
- Consider both methodology novelty AND application novelty
- Check for concurrent/recent arXiv submissions

## Related Skills
- Upstream: [literature-search](../literature-search/), [deep-research](../deep-research/)
- Downstream: [idea-generation](../idea-generation/), [research-planning](../research-planning/)
- See also: [related-work-writing](../related-work-writing/)
