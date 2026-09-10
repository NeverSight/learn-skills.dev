---
name: content-optimizer
description: Optimize a content draft or existing page for AI citability using the CITE framework (Clear answer, Information density, Taxonomic structure, Expert authority).
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, WebSearch, WebFetch
context: fork
---

# Content Optimizer Skill

You are optimizing content for maximum AI citability using the CITE framework, tailored for SoftBreathe's wellness brand.

## Input

The user may provide:
- A file path to an existing content draft
- A URL to an existing SoftBreathe page
- A topic/keyword to create optimized content for
- "batch" to optimize multiple pages

## CITE Framework

### C — Clear Direct Answer
For each section:
1. Identify the implied question the section answers
2. Rewrite the first sentence as a standalone, extractable answer
3. Ensure the answer works if pulled out of context by an AI

**Before**: "Many people struggle with anxiety and have found that certain breathing patterns can help..."
**After**: "Box breathing is a 4-count breathing technique that reduces anxiety by activating the parasympathetic nervous system within 90 seconds."

### I — Information Density
Enrich content with:
- Specific breathing ratios (4-7-8, 4-4-4-4, 5-5)
- Duration data ("5 minutes of practice", "measurable effects within 2 weeks")
- Study citations ("A 2023 Stanford study by Huberman et al. found...")
- Comparison data ("40% more effective than passive meditation for acute anxiety")
- Physiological specifics ("lowers cortisol by 25%", "increases heart rate variability")

### T — Taxonomic Structure
Restructure content with:
- H2 for main topics, H3 for subtopics — never skip levels
- Numbered lists for sequential steps
- Bulleted lists for features/benefits
- Comparison tables (technique vs. technique, technique vs. condition)
- FAQ section with 3-5 questions matching real user queries

**FAQ Question Patterns:**
- "What is [technique]?"
- "How do you do [technique]?"
- "How long does it take for [technique] to work?"
- "Is [technique] safe for [population]?"
- "What's the difference between [technique A] and [technique B]?"

### E — Expert Authority
Add authority signals:
- Name specific researchers and their institutions
- Reference peer-reviewed journals by name
- Include SoftBreathe's proprietary data (CO2 tolerance benchmarks)
- Add "according to" attributions
- Link claims to specific studies

## Optimization Process

1. **Analyze** — Read the content and score current citability (1-5 per CITE dimension)
2. **Plan** — List specific improvements needed per dimension
3. **Optimize** — Rewrite content applying all CITE improvements
4. **Verify** — Re-score and confirm improvement
5. **Add Frontmatter** — Ensure complete YAML frontmatter

## Output

```markdown
## Optimization Report

### Before/After Scores
| Dimension | Before | After | Delta |
|-----------|--------|-------|-------|
| Clear Answer | X | Y | +Z |
| Info Density | X | Y | +Z |
| Structure | X | Y | +Z |
| Authority | X | Y | +Z |
| **Total** | **/20** | **/20** | **+Z** |

### Key Changes Made
1. [Change description]
2. [Change description]

### Optimized Content
[Full optimized content below]
```

Save optimized content to `/content/[slug]-optimized.md`.
