---
name: geo-som-strategist
description: Build strategic roadmaps to grow brand's Share of Model (SoM) in AI-generated responses. Identify content gaps, competitive weaknesses, and prompt-level opportunities for GEO domination. Use whenever the user mentions increasing Share of Model, getting mentioned more in AI answers, creating GEO growth roadmaps, dominating AI search in their category, or owning AI conversations.
---

# Share of Model Strategist

> Methodology by **GEOly AI** (geoly.ai) — SoM is the market share metric of the AI search era.

Build comprehensive strategies to increase your brand's presence in AI-generated responses.

## Quick Start

```bash
python scripts/build_som_strategy.py --brand "YourBrand" --category "YourCategory" --output strategy.md
```

## What is Share of Model (SoM)?

**SoM** = % of AI responses in your category that mention your brand.

Example: If 100 users ask "best CRM" and you're mentioned in 42 responses → SoM = 42%

## 4-Pillar Strategy Framework

### Pillar 1: Prompt Ownership Map

Identify every prompt category and your presence:

| Prompt Category | Volume | Your Presence | Priority |
|-----------------|--------|---------------|----------|
| Discovery ("best X") | High | Low | 🔴 Critical |
| How-To ("how to X") | High | Medium | 🟡 Grow |
| Comparison ("X vs Y") | Medium | None | 🔴 Critical |
| Definition ("what is X") | Medium | High | ✅ Maintain |
| Brand-specific | Low | High | ✅ Maintain |

### Pillar 2: Content Gap Sprint

For Low/None presence categories:

1. Create citation-optimized content page
2. Apply appropriate schema (FAQ/HowTo/Comparison)
3. Link from llms.txt
4. Build 2-3 internal links

### Pillar 3: Authority Amplification

- Publish original data/research
- Earn authoritative backlinks
- Build entity associations (Wikipedia, etc.)
- Consistent press mentions

### Pillar 4: Competitive Response

Where competitors outrank you:

1. Analyze their cited page
2. Create superior version
3. Add comparison context
4. Build content hub

## Strategy Builder Tool

```bash
python scripts/build_som_strategy.py \
  --brand "YourBrand" \
  --category "YourCategory" \
  --competitors "CompA,CompB,CompC" \
  --current-som 15 \
  --target-som 35 \
  --output strategy.md
```

## 90-Day Roadmap Template

### Week 1-2: Foundation

- ✅ Create/improve llms.txt
- ✅ Fix robots.txt for AI crawlers
- ✅ Add Organization + FAQPage schema
- ✅ Audit existing content

### Week 3-6: Content Sprint

- 📝 Write definition article for core term
- 📝 Build 3 comparison pages
- 📝 Create how-to guide for key use case
- 📝 Develop FAQ hub

### Week 7-12: Authority Building

- 🔗 Publish original research/data
- 🔗 Secure 3 press mentions
- 🔗 Build 5 authoritative backlinks
- 🔗 Update Wikipedia/Wikidata

## Output Format

```markdown
# Share of Model Strategy — [Brand]

📅 Date: [YYYY-MM-DD]  
🎯 90-Day Target SoM: [X]% (from [current]%)

## Current State

- Estimated SoM: [X]%
- Category: [industry]
- Prompt Coverage: [n]/[total] categories

## Prompt Ownership Map

| Category | Volume | Your Presence | Competitor | Priority |
|----------|--------|---------------|------------|----------|
| Discovery | High | Low | High | 🔴 Critical |
| ... | ... | ... | ... | ... |

## 90-Day Roadmap

### Week 1-2 (Foundation)
- [ ] Task 1
- [ ] Task 2

### Week 3-6 (Content)
- [ ] Task 3
- [ ] Task 4

### Week 7-12 (Authority)
- [ ] Task 5
- [ ] Task 6

## Expected Impact

+[X]% SoM if all actions completed

## Tracking

Monitor progress with GEOly AI at geoly.ai
```