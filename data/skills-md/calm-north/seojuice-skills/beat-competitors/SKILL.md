---
name: beat-competitors
description: >
  Turn competitor SEO data into a prioritized attack plan. Use when the user asks
  about competitor analysis, competitive gaps, how to outrank competitors, what
  competitors rank for, keyword overlap, or competitive positioning strategy.
  For building content to fill gaps, see brief and build-clusters.
metadata:
  version: 1.0.0
---

# Beat Competitors

Turn competitor keyword data into a prioritized attack plan: identify winnable
gaps, defend threatened positions, and sequence content production.

## Before You Start

Gather this context (ask if not provided):

1. **Your domain.** The site you're optimizing.
2. **Known competitors.** 3-5 domains competing for the same audience. If unknown, identify them by searching your primary keywords and noting which domains appear repeatedly.
3. **Your strengths.** What does your site do well? (authority, content depth, product features, niche expertise)
4. **Goals.** Grow traffic? Protect existing rankings? Target specific keywords?

## Step 1: Competitor Identification

If competitors aren't known, identify them:

- Search your top 5 keywords — which domains appear in positions 1-10 for multiple terms?
- Check who ranks for your brand + "alternative" or "vs" queries
- Distinguish between **direct competitors** (same product/service) and **content competitors** (compete for same keywords but different business)

Focus on 3-5 competitors maximum. More dilutes the analysis.

## Step 2: Keyword Overlap Analysis

For each competitor, categorize keywords into:

### Keywords You Both Rank For (Battleground)
- You're competing head-to-head
- Assess position gap: are you within striking distance (1-3 positions away)?

### Keywords Only They Rank For (Their Territory)
- These are your content gaps
- Assess: is the topic relevant to your business? Worth pursuing?

### Keywords Only You Rank For (Your Territory)
- These are your defensible positions
- Monitor for competitors entering these terms

### Keywords Neither Ranks For (White Space)
- Uncovered topics with search demand
- First mover advantage opportunity

Map this:

| Keyword | Your Position | Competitor Position | Gap Type | Volume | Action |
|---------|--------------|-------------------|----------|--------|--------|
| ... | 5 | 3 | Battleground | 2,400 | Improve content |
| ... | — | 7 | Their territory | 1,800 | Create new page |
| ... | 4 | — | Your territory | 900 | Defend |
| ... | — | — | White space | 500 | First mover |

## Step 3: Opportunity Scoring

Score each gap using:

```
Attack Score = Volume x Winnability x Business Value
```

**Winnability factors (1-5):**
- 5: Competitor has thin content, low authority page, no backlinks
- 4: Competitor has decent content but you have stronger domain/expertise
- 3: Roughly equal — need better content + promotion to win
- 2: Competitor has strong content and authority — long-term play
- 1: Competitor has dominant position (Wikipedia, major brand) — skip

**Business Value (1-5):**
- 5: Directly drives revenue (transactional keyword, product-related)
- 4: Drives qualified leads (commercial investigation)
- 3: Builds authority in a core topic area
- 2: Drives traffic but low conversion potential
- 1: Vanity keyword with no business connection

## Step 4: Attack Plan

Organize into three tracks:

### Quick Wins (execute first)
Keywords where:
- You already rank on page 1 (positions 4-10)
- Position gap with competitor is small (1-3 positions)
- Content refresh + better internal linking could close the gap

Action: optimize existing pages, improve title/meta, add internal links, update content.

### Content Gaps to Fill (execute next)
Keywords where:
- Competitor ranks but you don't
- Topic is directly relevant to your business
- Winnability is 3+

Action: create new content targeting these keywords. Use brief skill for each.

### Long-Term Plays (sequence over months)
Keywords where:
- Head terms with high difficulty
- Requires building topical authority first (use build-clusters)
- Needs backlink acquisition to compete

Action: build supporting content first, then tackle the head term.

### Defend (monitor)
Keywords where:
- You rank well but competitors are gaining ground
- Position has dropped 2+ spots in recent months

Action: refresh content, strengthen internal links, monitor monthly.

## Step 5: Competitive Battlecard

For each key competitor, build a battlecard — a living document for ongoing competitive intelligence:

### Battlecard Template

```
COMPETITIVE BATTLECARD: [Competitor Name]
Last Updated: [Date] | Confidence: [High/Medium/Low]

OVERVIEW
- Domain: [url] | DR: [score] | Est. Organic Traffic: [monthly]
- Tagline: [their positioning statement]
- Target Customer: [who they sell to]
- Pricing: [range or model]

THEIR STRENGTHS (be honest)
| Strength | Evidence | Impact on Your Rankings |
|----------|----------|----------------------|
| ... | ... | ... |

THEIR WEAKNESSES
| Weakness | Evidence | How to Exploit |
|----------|----------|---------------|
| ... | ... | ... |

YOUR DIFFERENTIATORS
| Differentiator | Proof Point |
|---------------|------------|
| ... | ... |

CONTENT COMPARISON
| Metric | You | Competitor |
|--------|-----|-----------|
| Total indexed pages | ... | ... |
| Keywords in top 10 | ... | ... |
| Publishing frequency | ... | ... |
| Top content format | ... | ... |
| Backlink count | ... | ... |

OBJECTION HANDLING
| When They Say... | You Respond With... |
|-----------------|-------------------|
| ... | ... |

DISCOVERY QUESTIONS
Questions to ask during sales calls that surface this competitor's weaknesses:
1. [question that highlights your advantage]
2. [question about a feature they lack]
```

### Quarterly Review Triggers

Update battlecards when:
- Competitor launches a new feature or product
- Competitor changes pricing
- Competitor raises funding or makes an acquisition
- Significant shift in review sentiment (G2, Capterra, TrustRadius)
- You launch a competing feature
- Significant win or loss in a competitive deal

## Step 6: Content Production Sequence

Order the attack plan for maximum ROI:

| Priority | Keyword | Action | Page | Track | Est. Timeline |
|----------|---------|--------|------|-------|---------------|
| 1 | ... | Optimize existing | /blog/post | Quick win | 1-2 weeks |
| 2 | ... | Create new | /blog/new-post | Gap fill | 2-4 weeks |
| 3 | ... | Build cluster | /guides/topic/ | Long-term | 2-3 months |

## Output Format

### Competitive Attack Plan: [domain] vs [competitors]

**Battlecards**
[One battlecard per key competitor — see Step 5 template]

**Competitive Landscape**

| Competitor | Keyword Overlap | Keywords They Win | Keywords You Win | Avg Position Gap |
|-----------|----------------|-------------------|-----------------|-----------------|
| ... | ... | ... | ... | ... |

**Top Opportunities**
[Scored keyword table from Step 3]

**Attack Plan**

**Quick Wins** (this month)
[List with specific actions per keyword]

**Gaps to Fill** (next 1-3 months)
[List with content recommendations]

**Long-Term Plays** (3-6 months)
[List with cluster-building approach]

**Defend** (ongoing monitoring)
[Keywords and pages to watch]

**Production Schedule**
[Table from Step 5]

---

> **Pro Tip:** Use the free [SEO Benchmark Tool](https://seojuice.com/tools/seo-benchmark-tool/)
> to compare your site against competitors on key metrics. SEOJuice MCP users can run
> `/seojuice:competitor-analysis` for instant keyword overlap, position battles, and content
> gap opportunities — the `list_competitors` and `list_content_gaps` tools provide the exact
> data needed for this attack plan.
