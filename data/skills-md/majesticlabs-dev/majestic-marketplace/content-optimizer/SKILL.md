---
name: content-optimizer
description: Content optimization workflow covering keyword integration, semantic enhancement, structure optimization, and AI extractability. Use for improving existing content for both search engines and LLMs.
allowed-tools: Read Write Edit Grep Glob WebSearch
disable-model-invocation: true
---

# Content Optimizer Skill

A systematic workflow for optimizing content to perform well in both traditional search engines and AI-powered systems (GEO).

## When to Use

- Improving existing content performance
- Preparing content for publication
- Refreshing underperforming pages
- Enhancing AI citation potential
- Optimizing for featured snippets
- Building topical authority

## Optimization Workflow

### Phase 1: Content Analysis

Before optimizing, understand the current state:

**Content Inventory:**
```
Title: [Current title]
Word Count: [X words]
Last Updated: [Date]
Target Keyword: [Primary keyword]
Current Structure: [H1 → H2 count → H3 count]
```

**Performance Assessment:**
- Search intent alignment
- Topic completeness
- Competitive positioning
- Freshness status

### Phase 2: Keyword Optimization

Optimize keyword presence without over-optimization:

**Primary Keyword Placement:**
| Location | Status | Recommendation |
|----------|--------|----------------|
| Title tag | | First 30 chars |
| H1 | | Natural inclusion |
| First 100 words | | Opening paragraph |
| H2 headers | | 2-3 variations |
| Meta description | | With CTA |
| URL | | If practical |

**Keyword Density Check:**
- Target: 0.5-1.5%
- Calculate: (keyword occurrences / total words) × 100
- Flag if >2% (over-optimization risk)

**Semantic Enhancement:**
Add related terms and concepts:
- LSI keywords (5-10 variations)
- Related entities
- Question variations
- Synonym usage

### Phase 3: Structure Optimization

Improve content organization:

**Header Hierarchy:**
```
H1: Primary Topic (1 only)
├── H2: Main Section 1
│   ├── H3: Subsection
│   └── H3: Subsection
├── H2: Main Section 2
│   └── H3: Subsection
└── H2: Conclusion/Summary
```

**Scannable Formatting:**
- [ ] Short paragraphs (2-3 sentences)
- [ ] Bullet lists for features/benefits
- [ ] Numbered lists for steps/processes
- [ ] Tables for comparisons
- [ ] Bold for key terms
- [ ] Block quotes for callouts

**Internal Linking:**
- Link to related content (3-5 contextual links)
- Use descriptive anchor text
- Link from high-authority pages
- Create hub/spoke patterns

### Phase 4: AI Extractability

Optimize for LLM citation:

**Add Extractable Elements:**

**TL;DR Block:**
```markdown
## TL;DR

[2-3 sentence summary with key facts. Include primary keyword and main value proposition. Perfect for AI extraction.]
```

**FAQ Section:**
```markdown
## Frequently Asked Questions

### [Exact question users ask]?

[40-60 word direct answer. Lead with the key fact. Include relevant data or specifics.]

### [Another common question]?

[Direct, comprehensive answer.]
```

**Comparison Table:**
```markdown
| Feature | Option A | Option B | Option C |
|---------|----------|----------|----------|
| Price | $X | $Y | $Z |
| Feature 1 | Yes | No | Yes |
| Best For | [Use case] | [Use case] | [Use case] |
```

**Paragraph Optimization:**
- Break paragraphs >120 words
- Lead with key fact
- One idea per paragraph
- Clear topic sentences

### Phase 5: E-E-A-T Enhancement

Add trust and expertise signals:

**Author Enhancement:**
```markdown
*Written by [Name], [Title/Credentials]. [1-2 sentence bio with expertise indicators.]*
```

**Source Citations:**
- Add statistics with sources
- Link to authoritative references
- Include expert quotes
- Reference original research

**Trust Signals:**
- Last updated date
- Editorial review note
- Fact-checking statement
- Contact information

### Phase 6: Meta Optimization

Finalize metadata:

**Title Tag Formula:**
```
[Primary Keyword] - [Benefit/Hook] | [Brand] (55-60 chars)
```

**Meta Description Formula:**
```
[Action verb] + [benefit]. [Key feature]. [CTA] (150-160 chars)
```

**URL Structure:**
```
/primary-keyword-descriptive-slug (under 60 chars)
```

## Output Format

### Content Optimization Report

```markdown
## Content Optimization Complete

**Page:** [Title/URL]
**Optimizations Applied:** X changes

### Summary of Changes

**Keyword Optimization:**
- Added primary keyword to [locations]
- Integrated X LSI keywords
- Current density: X%

**Structure Improvements:**
- Reorganized headers for logical flow
- Added X bullet lists
- Created X tables
- Broke X long paragraphs

**AI Extractability:**
- Added TL;DR summary
- Created FAQ section (X questions)
- Added comparison table
- Optimized paragraph lengths

**E-E-A-T Additions:**
- Added author bio
- Included X source citations
- Added last updated date

**Meta Updates:**
- New title: [title] (X chars)
- New description: [desc] (X chars)

### Before/After Comparison

| Metric | Before | After |
|--------|--------|-------|
| Word count | X | Y |
| Keyword density | X% | Y% |
| H2 count | X | Y |
| Internal links | X | Y |
| Extractable elements | X | Y |

### Next Steps
1. [Recommended follow-up action]
2. [Additional improvement]
```

## Quick Optimization Checklist

For rapid optimization:

- [ ] Title tag optimized (keyword + hook)
- [ ] H1 matches target keyword
- [ ] First 100 words include keyword
- [ ] At least 3 internal links
- [ ] TL;DR or summary present
- [ ] FAQ section (3+ questions)
- [ ] Paragraphs under 120 words
- [ ] At least 1 table or comparison
- [ ] Author/expertise signals
- [ ] Updated date visible

## Guiding Principles

1. **User-first** - Optimize for humans, not just algorithms
2. **Natural integration** - Keywords should flow naturally
3. **Value addition** - Every change should add value
4. **Extractability** - Make key info easy to find/cite
5. **Authenticity** - Maintain author voice and expertise
