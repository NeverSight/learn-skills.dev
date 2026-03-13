---
name: 30x-seo-content-brief
description: >
  Generate content briefs by analyzing top-ranking SERP results. Extracts common
  topics, identifies content gaps, and creates actionable briefs for content-writer.
  Input: target keyword. Output: content brief with must-cover topics + gap opportunities.
metadata:
  version: 1.0.0
  category: content
  dependencies: [WebFetch]
allowed-tools:
  - WebFetch
  - Read
---

# Content Brief Generator

> SERP Analysis → Content Brief → Outrank Competition

## Goal

**Not rewriting competitors, but analyzing them to write better content.**

| Wrong Approach | Right Approach |
|----------------|----------------|
| Rewrite Top 10 articles | Analyze Top 10 intent |
| Copy content structure | Find gaps (what they missed) |
| Merge competitor content | Outperform (add original data/cases) |

---

## Workflow

### Step 1: SERP Scraping

```
Input: Target keyword
↓
Scrape Top 10 results:
- Title
- URL
- Meta description
- Page content (H1, H2, H3 structure)
- Word count
- Content type (listicle, how-to, guide, comparison, etc.)
```

### Step 2: Intent Analysis

| Dimension | Description |
|-----------|-------------|
| **Search Intent** | Informational / Commercial / Transactional / Navigational |
| **Content Format** | 90% are listicles? You should write a listicle too |
| **Content Depth** | Average word count? Exceed the average |
| **SERP Features** | Featured Snippet? PAA? Video? |

### Step 3: Topic Extraction

Extract common topics covered by Top 10:

```
Example keyword: "how to start a podcast"

Top 10 coverage:
✓ Equipment selection (10/10)
✓ Recording software (9/10)
✓ Hosting platforms (8/10)
✓ Cover design (7/10)
✓ Promotion strategy (6/10)
```

**Rule**: Topics covered by >50% = must include

### Step 4: Gap Analysis

Find content competitors **don't cover** or **cover poorly**:

```
Gap opportunities:
- 2024 AI tool recommendations (only 2/10 mention)
- Monetization strategies (most skim over)
- Real cost breakdown (no specific numbers)
- Common failure reasons (few cover negative angle)
```

**Rule**: Gaps = your differentiation opportunity

### Step 5: Brief Generation

---

## Output Format: Content Brief

```markdown
# Content Brief: [Target Keyword]

## Search Intent
[Informational/Commercial/etc.] - [One sentence describing what users want]

## Content Format
Recommended: [Listicle / How-to Guide / Comparison / etc.]
Reason: X/10 of Top 10 use this format

## Target Word Count
Minimum: [Top 10 average word count]
Recommended: [Average + 20%] to outperform competition

## Must-Have Topics

| Topic | Coverage | Suggested Depth |
|-------|----------|-----------------|
| [Topic 1] | 10/10 | Detailed |
| [Topic 2] | 9/10 | Detailed |
| [Topic 3] | 8/10 | Medium |

## Gap Opportunities (Differentiators)

| Gap | Why It's an Opportunity | Suggested Angle |
|-----|-------------------------|-----------------|
| [Gap 1] | Only 2/10 mention | [Specific suggestion] |
| [Gap 2] | Shallow coverage | [Specific suggestion] |

## Recommended H2 Structure

1. [H2 Title] - Covers [Topic]
2. [H2 Title] - Covers [Topic]
3. [H2 Title] - Gap opportunity: [Gap]
4. ...

## E-E-A-T Recommendations

- **Experience**: Add [specific suggestion, e.g., real case/screenshots]
- **Expertise**: Cite [data sources/expert opinions]
- **Original Value**: [What can you provide that competitors don't]

## SERP Feature Opportunities

- [ ] Featured Snippet: [Opportunity exists? Format suggestion]
- [ ] PAA: [Related questions list]
- [ ] Video: [Video needed?]

## Internal Link Suggestions

- Link to: [Related existing pages]
- Get links from: [Which pages should link to this article]
```

---

## Usage

```bash
# Generate content brief
/seo content-brief "target keyword"

# Then write content using the brief
/seo content-writer --brief [brief-file]
```

---

## Related Skills

| Upstream | This Skill | Downstream |
|----------|------------|------------|
| 30x-seo-keywords | **30x-seo-content-brief** | 30x-seo-content-writer |
| 30x-seo-plan | ↓ Analyze SERP | ↓ Write per brief |

---

## Important Notes

1. **No plagiarism**: Brief is an analysis tool, not a copying tool
2. **Original first**: Gap sections must have original content
3. **E-E-A-T**: Every piece needs real experience/data
4. **Timeliness**: Competitors change, briefs have expiration

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
