---
name: content-autopsy
description: Use when analyzing why content performed well or poorly, doing post-mortem analysis, or comparing content performance.
---

# Content Autopsy

This is an investigation, not a report card. The goal is understanding what happened and why — framed as "here's what likely drove this" rather than "this was good/bad."

## Signal vs. Noise

A single post's performance is noisy. External factors can dominate: time of day, platform outages, competing events, algorithmic lottery. One viral post doesn't mean you cracked the code. One flop doesn't mean the content was bad.

Look for patterns across multiple posts before drawing conclusions. If someone asks about a single post, analyze it but flag that single-post analysis is inherently uncertain.

## Metric Interpretation

Different metrics tell different stories. Read them in layers:

**Reach / impressions** — how far did the algorithm push this? High reach means the platform thought it was worth distributing. Low reach on otherwise good content usually means the hook didn't convert or the initial audience didn't engage fast enough.

**Engagement rate** — of people who saw it, how many interacted? Break this down by type:
- Likes are low-effort (cheap signal)
- Comments are medium-effort (stronger signal, especially longer ones)
- Saves and shares are high-intent (strongest signal — "I want this later" or "someone else needs to see this")

**Retention / watch time** — for video, where did people drop off? The drop-off point often reveals the problem. Mass drop-off at 3 seconds = hook failed. Drop-off in the middle = pacing issue. Drop-off before the end = too long or lost the thread.

**Follow-through** — did engagement translate to follows, profile visits, link clicks? High engagement but no follows = entertaining but not compelling enough to commit to. Save-heavy but low likes = useful reference content (often undervalued).

## Performance Patterns

**Spike-and-die** — went semi-viral then flatlined. Usually means the content appealed broadly but didn't connect with a retainable audience. Common with trending audio or meme formats where the trend did the work, not the creator's unique angle.

**Slow burn** — modest initially, grows over days or weeks. Common with search-discoverable content (YouTube especially) or content that gets shared in group chats over time. Often the most valuable content a creator makes.

**Second wave** — initial modest performance, then the algorithm resurfaces it. Can be triggered by a share from a larger account, sudden trend alignment, or the algorithm's own re-testing cycle.

**Save-heavy** — low visible engagement but high saves. The content is reference-worthy. This often looks like underperformance but is actually high-quality signal — people are bookmarking it to come back to.

## Causal Analysis

When investigating why something performed the way it did, check these in order:

1. **Hook** — did people stay past the first few seconds? If not, nothing else matters.
2. **Topic** — was there demand for this? Was the timing right relative to trends or conversations?
3. **Format** — was it native to the platform? Right length, right aspect ratio, right pacing?
4. **Audience match** — did it reach the right people? Broad distribution to the wrong audience tanks engagement rate.
5. **Timing** — posting time, day of week, competing with a major event?

It's usually one or two of these, not all five. Start with the most likely culprit based on the metrics.

For platform-specific metric interpretation, load `references/platforms/{platform}.md` from this skill's own directory.
