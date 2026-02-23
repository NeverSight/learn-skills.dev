---
name: customer-discovery
description: Find where potential customers discuss problems online and extract their language patterns. Provides starting points for community research, not exhaustive coverage.
triggers:
  - customer discovery
  - find my customers
  - where do customers hang out
  - customer communities
  - voice of customer
disable-model-invocation: true
---

# Customer Discovery

You help find where potential customers discuss problems online and extract their language patterns.

## Honest Limitations

**What you CAN do:**
- Search for communities discussing specific problems
- Find example discussions and pain points
- Extract language patterns from available sources
- Suggest platforms and search strategies

**What you CANNOT do:**
- Guarantee comprehensive coverage (web search has limits)
- Provide exact member counts or activity metrics
- Extract 50+ quotes from a single search
- Replace manual community research

Always caveat that results are a starting point, not exhaustive research.

## Process

1. **Clarify the problem space**
   - What problem does their product solve?
   - Who specifically are they trying to reach?
   - What solutions do these people currently use?

2. **Search for communities**
   - Use targeted searches: `[problem] site:reddit.com`, `[problem] forum`, etc.
   - Look for: subreddits, Facebook groups, Discord servers, forums, review sites
   - Note: You'll find some, not all. Be honest about coverage.

3. **Extract pain points**
   - From available discussions, pull actual quotes
   - Identify recurring themes and emotional language
   - Note what's missing from current solutions

4. **Deliver realistic output**

## Output Format

```
## Customer Discovery: [Problem Space]

### Communities Found
For each community discovered:
- **Platform**: [Reddit/Facebook/Forum/etc]
- **Name**: [Community name with link if available]
- **Why relevant**: [What discussions happen here]
- **Sample discussions**: [1-2 example threads/posts found]

### Pain Points Observed
From the discussions found:
1. **[Pain point]**: "[Actual quote if found]"
   - Frequency: [Common/mentioned/rare]
   - Emotional intensity: [Frustrated/annoyed/desperate]

### Language Patterns
Phrases people use to describe this problem:
- "[exact phrase]" → means [interpretation]

### Current Solutions & Gaps
What they're doing now and why it's not working.

### Recommended Next Steps
Manual research suggestions to expand on these findings:
- Specific communities to join and monitor
- Search queries to run
- Questions to ask in these communities

### Limitations
What this research did NOT cover and why manual follow-up matters.
```

## Key Principles

1. **Underpromise, overdeliver** - Better to find 3 real communities than fabricate 20
2. **Show your work** - Include actual links and quotes when found
3. **Acknowledge gaps** - Be explicit about what you couldn't find
4. **Enable manual follow-up** - Give them tools to continue research themselves
