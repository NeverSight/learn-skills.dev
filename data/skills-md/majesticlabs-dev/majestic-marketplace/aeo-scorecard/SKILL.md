---
name: aeo-scorecard
description: Measurement framework for Answer Engine Optimization (AEO). Provides AI visibility metrics, share of voice tracking, citation monitoring, and referral demand measurement. Use when discussing AEO/GEO metrics or AI visibility performance.
triggers:
  - AEO metrics
  - AI visibility measurement
  - answer engine performance
  - GEO scorecard
  - AI share of voice
  - citation tracking
disable-model-invocation: true
---

# AEO Scorecard: Measuring AI Visibility

## The Four AEO Metrics

Track these metrics to measure Answer Engine Optimization success:

### 1. AI Visibility

**Definition:** Are you recommended for your priority queries?

**How to Measure:**
- Test priority queries in ChatGPT, Perplexity, Gemini, Claude
- Document which queries return your brand
- Track visibility over time (weekly/monthly)

**Tools:**
- HubSpot AEO Grader (free audit)
- XFunnel (comprehensive tracking)
- Manual testing with query lists

**Target:** Appear in recommendations for 60%+ of priority queries.

### 2. AI Share of Voice

**Definition:** Of all recommendations for a query, how often is YOUR brand named vs. competitors?

**Calculation:**
```
Share of Voice = (Your mentions / Total brand mentions) × 100
```

**Why It Matters:**
- Distinguishes platform changes (everyone drops) from brand failures (you drop, competitors stay)
- Tracks competitive position in AI recommendations

**Example:**
- Query: "Best CRM for small business"
- Total recommendations across 10 AI sessions: 50 brand mentions
- Your brand mentioned: 8 times
- Share of Voice: 16%

**Target:** Match or exceed your traditional search market share.

### 3. AI Citations

**Definition:** How often is YOUR WEBSITE the source of the answer?

**Why It Matters:**
- Being cited = more positive recommendation
- Citation = authority signal for future queries
- Direct traffic potential from "learn more" links

**How to Track:**
- Monitor AI bot traffic in analytics (GPTBot, Anthropic-AI, etc.)
- Use XFunnel to track citation sources
- Test queries and note source attribution

**Target:** Be cited (not just mentioned) in 30%+ of relevant queries.

### 4. Referral Demand

**Definition:** Traffic and conversions that originated in AI but didn't click through immediately.

**The Problem:** AI users often:
1. Get answer from AI
2. Remember brand name
3. Search directly or visit later
4. No referral attribution

**How to Measure:**
Implement post-purchase survey:
- "How did you first hear about us?"
- Options: "AI assistant (ChatGPT, Perplexity, etc.)"

**Survey Placement:**
- Post-purchase confirmation
- Onboarding flow
- Trial signup

**Target:** Track trend over time; aim for growth in AI-attributed discovery.

## AEO Scorecard Template

```
┌─────────────────────────────────────────────────────────┐
│                    AEO SCORECARD                        │
│                    Month: [DATE]                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  AI VISIBILITY                          [X]% → Target: 60%
│  ──────────────────────────────────────                 │
│  Priority queries with brand presence: X/Y              │
│                                                         │
│  AI SHARE OF VOICE                      [X]% → Target: Match SEO
│  ──────────────────────────────────────                 │
│  Your mentions / Total brand mentions                   │
│  Competitor A: X%  |  Competitor B: X%  |  You: X%      │
│                                                         │
│  AI CITATIONS                           [X]% → Target: 30%
│  ──────────────────────────────────────                 │
│  Queries where YOUR site is cited: X/Y                  │
│                                                         │
│  REFERRAL DEMAND                        [X]% → Trend: ↑↓
│  ──────────────────────────────────────                 │
│  Post-purchase survey: "Found via AI"                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Measurement Tools

| Tool | What It Measures | Cost |
|------|------------------|------|
| **HubSpot AEO Grader** | AI visibility audit | Free |
| **XFunnel** | Full AEO tracking suite | Paid |
| **Manual Testing** | Query-by-query visibility | Free (time) |
| **Google Analytics** | AI bot traffic | Free |
| **Post-Purchase Survey** | Referral demand | Free |

## Setting Up AI Bot Tracking

In Google Analytics 4, create a segment for AI crawler traffic:

**User Agents to Track:**
- `GPTBot` (OpenAI)
- `Anthropic-AI` (Claude)
- `Google-Extended` (Gemini)
- `PerplexityBot`
- `CCBot` (Common Crawl, used by many)

## Interpreting Results

**Scenario Analysis:**

| Visibility | Share of Voice | Diagnosis |
|------------|----------------|-----------|
| ↓ Down | ↓ Down | Platform algorithm change (industry-wide) |
| ↓ Down | → Stable | Your content quality declined |
| → Stable | ↓ Down | Competitors improved |
| ↑ Up | ↑ Up | Your AEO strategy is working |

## Action Triggers

| Metric | Threshold | Action |
|--------|-----------|--------|
| Visibility < 40% | Critical | Run `llm-optimizer` on all priority content |
| Share of Voice < competitor | Competitive gap | Run `entity-builder` for authority building |
| Citations < 20% | Authority gap | Add original data, improve fact-density |
| Referral Demand flat | Attribution gap | Improve survey placement and options |

## Monthly Review Cadence

1. **Week 1:** Run visibility audit on priority queries
2. **Week 2:** Calculate share of voice vs. top 3 competitors
3. **Week 3:** Analyze citation sources and bot traffic
4. **Week 4:** Review referral demand survey data
5. **Monthly:** Update scorecard, prioritize improvements
