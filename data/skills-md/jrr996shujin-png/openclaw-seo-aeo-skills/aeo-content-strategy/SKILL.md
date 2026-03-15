---
name: aeo-content-strategy
description: "AEO/GEO content strategy skill that combines Reddit and Quora monitoring, long-tail question mining, and content topic recommendations into one actionable report. Use this skill whenever the user wants to: discover what people are asking about their product category on Reddit or Quora, find unanswered or low-competition long-tail questions for AEO optimization, generate blog topic ideas based on real community discussions and search intent, build a content calendar targeting AI citation opportunities, understand what questions AI tools like ChatGPT/Perplexity/Gemini might pull answers for, do competitive content gap analysis for AI search visibility, or plan content that targets specific user decision-making questions. Also trigger when user mentions 'AEO', 'answer engine optimization', 'AI search visibility', 'what should I write about', 'content gaps', 'Reddit monitoring', 'community listening', 'long-tail keywords for AI', or 'content strategy for LLM citations'. This skill produces a comprehensive report — not just raw data — with prioritized, actionable recommendations."
metadata: {"openclaw":{"emoji":"📡","homepage":"https://github.com/jrr996shujin-png/openclaw-seo-aeo-skills"}}
---

# AEO Content Strategy: Community Monitoring + Long-Tail Mining + Content Planning

## What This Skill Does

This skill generates a complete AEO content strategy by combining three interconnected analyses:

1. **Reddit/Quora Community Monitoring** — Discovers what real users are asking, complaining about, and recommending in communities relevant to the user's product
2. **Long-Tail Question Mining** — Transforms community signals and product knowledge into specific, conversational questions that AI platforms are likely to surface
3. **Content Topic Recommendations** — Prioritizes which content to create first based on competition level, purchase intent, and AI citation potential

The output is a single actionable report the user can hand to their content team and start executing immediately.

## Why This Combination Matters

These three activities form a natural pipeline. Community discussions reveal what real users care about (not what keyword tools think they care about). Those discussions contain raw long-tail questions that no one has properly answered yet. And those unanswered questions become high-value content opportunities — because when AI searches for answers and finds only your content addressing a specific question, it has no choice but to cite you.

Doing these separately wastes time and loses the connections between them. A Reddit thread about "frustrating email tools" directly feeds into a long-tail question like "what AI tool can automatically sort and reply to customer emails in my brand voice" which directly becomes a blog topic recommendation.

## Required Inputs

Before starting, collect these from the user:

| Input | Why It's Needed | Example |
|-------|----------------|---------|
| **Product/brand name** | To search for direct mentions | "Genspark" |
| **Product category** | To search for category discussions | "AI agent", "AI productivity tool" |
| **Target audience** | To calibrate question language and intent | "Solo entrepreneurs and small teams" |
| **2-3 competitor names** | To monitor competitor mentions and find gaps | "Manus, ChatGPT, Perplexity" |
| **Key use cases** (3-5) | To focus long-tail mining on real scenarios | "Email automation, meeting notes, research" |
| **Target language/market** | To determine which communities to scan | "English, US market" |

If the user doesn't provide all of these, ask for the missing ones before proceeding. The quality of the output depends heavily on having clear inputs.

## Execution Steps

### Phase 1: Reddit/Quora Community Scan

Search Reddit and Quora for recent discussions (prioritize last 6 months) using these query patterns:

**Direct brand searches:**
- `"{brand name}" site:reddit.com`
- `"{competitor 1}" OR "{competitor 2}" site:reddit.com`

**Category searches:**
- `"best {product category}" site:reddit.com`
- `"{product category} recommendation" site:reddit.com`
- `"{product category} vs" site:reddit.com`
- `"looking for {product category}" site:reddit.com`
- `"{product category}" site:quora.com`

**Problem/pain-point searches:**
- `"{use case 1} frustrated" OR "help" OR "alternative" site:reddit.com`
- `"how to {use case 2}" site:reddit.com`

**Subreddit-specific searches (identify 3-5 relevant subreddits first):**
- Search within subreddits like r/productivity, r/artificial, r/SaaS, r/smallbusiness, r/Entrepreneur, etc. depending on the product category

For each relevant thread found, extract:
- The original question or complaint (exact user language)
- Number of upvotes and comments (signals engagement/demand)
- Whether any brand was recommended in top responses
- Whether the question was adequately answered or left unanswered
- The subreddit it appeared in

Aim to collect 30-50 relevant threads across all searches.

### Phase 2: Signal Analysis

Categorize the collected threads into:

**Category A — Unanswered or Poorly Answered Questions**
These are gold. No one has properly answered them, meaning content you create could become the only source AI can cite.

**Category B — Questions Where Competitors Are Recommended But You're Not**
These reveal gaps in your brand visibility. Someone asked for a tool like yours and your competitors got mentioned but you didn't.

**Category C — Questions Where Your Brand Is Mentioned**
Track sentiment — are mentions positive, negative, or neutral? What specific features or limitations do users highlight?

**Category D — General Category Discussions**
Broader discussions about the product category that reveal user priorities, decision criteria, and common misconceptions.

### Phase 3: Long-Tail Question Generation

Transform the community signals into specific, conversational long-tail questions (25+ words each). These are the exact questions users would ask an AI assistant.

**Sources for question generation:**

1. **From Category A threads** — Rephrase unanswered Reddit questions into natural AI conversation format
2. **From Category B threads** — Create questions where your product could be the answer
3. **From user's key use cases** — Generate specific scenario-based questions for each use case
4. **From competitor comparison angles** — Create "X vs Y for [specific scenario]" questions
5. **From customer journey stages** — Questions at awareness, consideration, and decision stages

**Question format guidelines:**
- Write them as a real person would ask ChatGPT or Perplexity, not as SEO keywords
- Include context and constraints (team size, budget, specific needs)
- Make each question specific enough that only 1-3 tools could properly answer it
- Vary the format: "What's the best...", "How do I...", "Can [tool] do...", "I need something that..."

**Example transformations:**

Reddit thread: "Anyone know a good tool for automating email responses? I run a small Etsy shop and spend 2 hours/day on customer emails"

Generated long-tail questions:
- "I run a small e-commerce shop on Etsy and spend too much time replying to customer emails. Is there an AI tool that can learn my reply style and auto-draft responses to common questions like shipping times and return policies?"
- "What's the best AI email assistant for solo e-commerce sellers who get 50-100 customer emails per day and need responses that don't sound robotic?"
- "Can an AI tool automatically sort customer emails into categories like shipping questions, complaints, and product inquiries and draft different response templates for each?"

Generate at least 30 long-tail questions, aiming for 40-50.

### Phase 4: Content Topic Prioritization

Score each long-tail question cluster on three dimensions:

**1. Competition Level (Low / Medium / High)**
- Low: No existing content directly answers this specific question (confirmed by web search)
- Medium: 1-3 articles exist but are generic or outdated
- High: Multiple high-quality articles already cover this exact topic

**2. Purchase Intent (Low / Medium / High)**
- Low: Informational curiosity ("what is AI email automation")
- Medium: Active research ("best AI email tools for small business")
- High: Decision-ready ("Genspark vs Manus for email automation pricing")

**3. AI Citation Potential (Low / Medium / High)**
- Low: Topic is well-covered by authoritative sources; AI already has good answers
- Medium: Some coverage exists but lacks specific angles or updated data
- High: Little to no direct coverage; your content would fill a clear gap

Priority formula: **High priority = Low competition + High intent + High AI citation potential**

### Phase 5: Report Assembly

Compile everything into a structured report with these sections:

---

## Output Report Structure

ALWAYS use this exact template for the final report:

```
# AEO Content Strategy Report: [Brand Name]
Generated: [Date]

## Executive Summary
[3-4 sentences: key findings, biggest opportunities, recommended immediate actions]

## Part 1: Community Landscape

### Brand Mentions Overview
| Platform | Your Brand Mentions | Competitor A Mentions | Competitor B Mentions |
|----------|-------------------|---------------------|---------------------|
| Reddit   | [count]           | [count]             | [count]             |
| Quora    | [count]           | [count]             | [count]             |

### Sentiment Summary
[Brief analysis of how your brand vs competitors are being discussed]

### Top Unanswered Questions (Category A)
[List the 10 most promising unanswered questions from Reddit/Quora with source links]

### Competitor Visibility Gaps (Category B)
[List 5-10 threads where competitors were recommended but you weren't]

## Part 2: Long-Tail Question Bank

### High-Priority Questions (Top 15)
[Each question with: the question itself, source context, competition level, intent level, AI citation potential]

### Medium-Priority Questions (Next 15)
[Same format]

### Additional Questions (Remaining)
[Shorter format, just the questions grouped by theme]

## Part 3: Content Recommendations

### Immediate Actions (This Month) — Top 5 Topics
For each topic:
- **Recommended title**: [SEO and AEO optimized title]
- **Target questions answered**: [Which long-tail questions this article addresses]
- **Content format**: [Guide / Comparison / Tutorial / Case study]
- **Key sections to include**: [H2 outline]
- **Unique angle**: [What makes this different from existing content]
- **Estimated word count**: [Based on topic depth needed]

### Next Quarter — Topics 6-15
[Shorter format: title, target questions, format, unique angle]

### Content Calendar Suggestion
| Week | Topic | Format | Target Questions | Priority |
|------|-------|--------|-----------------|----------|
| 1    |       |        |                 |          |
| 2    |       |        |                 |          |
| ...  |       |        |                 |          |

## Part 4: Ongoing Monitoring Recommendations

### Subreddits to Watch
[List 5-10 subreddits with explanation of why each matters]

### Search Queries to Track Weekly
[List of 10-15 Reddit/Quora search queries to run regularly]

### Competitor Content to Monitor
[List competitor blogs and specific content types to watch]

## Appendix: Raw Data
### All Reddit/Quora Threads Collected
[Table: Thread title | URL | Subreddit/Topic | Upvotes | Comments | Category (A/B/C/D) | Key insight]
```

---

## Quality Checks Before Delivery

Before finalizing the report, verify:

- [ ] Every recommended topic has a clear "unique angle" — if your content would say the same thing as existing articles, it won't get cited by AI
- [ ] Long-tail questions are truly conversational (25+ words) and not just keyword phrases
- [ ] Priority scoring is consistent — double-check that "high priority" items genuinely have low competition
- [ ] Content calendar is realistic for a small team (not recommending 10 articles per week)
- [ ] Recommendations include specific structural advice (use tables for comparisons, FAQ sections for question-based content, H2 headers that match how users phrase questions)
- [ ] Each recommended article includes which AI platform citation it's primarily targeting (ChatGPT favors third-party consensus, Perplexity favors Reddit and niche directories, Gemini favors structured owned content)

## Important Reminders

- Reddit and Quora data is publicly accessible but rate-limited. If searches fail, retry with slight query variations.
- The value of this skill is in the CONNECTIONS between community data and content recommendations, not in the raw data alone. Always explain WHY a topic is recommended, not just WHAT to write.
- Content recommendations should follow the "information gain" principle from AEO best practices: only recommend topics where the user can provide genuinely new information (original data, unique expertise, first-hand testing) that doesn't already exist online.
- When competition is high for a topic, recommend a specific sub-angle rather than the broad topic. "Best AI tools" is saturated; "Best AI tools for Etsy sellers who handle 50+ daily customer emails" probably isn't.
