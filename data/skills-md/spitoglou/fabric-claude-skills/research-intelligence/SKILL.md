---
name: research-intelligence
description: Extract insights, analyze claims, and synthesize knowledge from research content. Use when processing academic papers, articles, podcasts, videos, meeting transcripts, or any content where the goal is to extract wisdom, analyze arguments, summarize findings, or compile references. Triggers include "analyze this paper", "extract key insights", "summarize the research", "what are the main claims", "extract wisdom from", "compile references", "critique this argument".
---

# Research Intelligence

Transform research content into actionable knowledge using structured extraction patterns.

## Pattern Selection

Determine the appropriate pattern based on user intent:

| Intent | Pattern | When to Use |
|--------|---------|-------------|
| Deep paper analysis | `analyze_paper` | Scientific papers requiring methodology/findings assessment |
| Quick paper overview | `summarize_paper` | Need key points without deep critique |
| Extract insights | `extract_wisdom` | Podcasts, videos, articles, general content |
| Evaluate arguments | `analyze_claims` | Content with truth claims requiring evidence analysis |
| Compile citations | `extract_references` | Building bibliographies, literature reviews |
| Identify key ideas | `extract_ideas` | Brainstorming, concept extraction |
| Find controversies | `extract_controversial_ideas` | Identifying contested viewpoints |

**Decision flow:**
1. **Is it a scientific paper?** → `analyze_paper` (deep) or `summarize_paper` (quick)
2. **Does it contain claims to verify?** → `analyze_claims`
3. **Need citations/references?** → `extract_references`
4. **General content for insights?** → `extract_wisdom`

## Pattern Execution

Each pattern follows the Fabric structure. Load the appropriate reference file, then apply its IDENTITY, STEPS, and OUTPUT format to the user's content.

### Core Patterns

See `references/` for full pattern definitions:
- [analyze_paper.md](references/analyze_paper.md) - Scientific paper deep analysis
- [summarize_paper.md](references/summarize_paper.md) - Quick paper summary
- [extract_wisdom.md](references/extract_wisdom.md) - General insight extraction
- [analyze_claims.md](references/analyze_claims.md) - Truth claim evaluation
- [extract_references.md](references/extract_references.md) - Citation compilation

## Output Guidelines

- Use bulleted lists for extracted items (not numbered)
- Never repeat ideas, insights, or quotes
- Don't start consecutive items with the same words
- Match output verbosity to user's apparent needs
- For papers: always note limitations and methodology quality

## Chaining Patterns

Offer logical follow-ups after completing a pattern:
- After `analyze_paper` → offer `extract_references` for bibliography
- After `extract_wisdom` → offer to create flashcards or summary
- After `analyze_claims` → offer to find supporting/contradicting evidence
