---
name: aios-writing-twitter
description: >
  Write Twitter/X posts and threads. Use when asked to write, create, draft,
  or produce a tweet, Twitter post, X post, Twitter thread, or tweetstorm.
  Also use when user mentions Twitter or X in a social media writing context.
  Outputs publish-ready tweets and threads with proper formatting.
metadata:
  author: claim-supply
  version: 1.0.0
---

# Writing Twitter/X

## Purpose
Produce publish-ready tweets and threads that match brand voice with a punchier, more opinionated tone suited to the platform.

## When to Use
- User asks to write a tweet, Twitter post, X post, or thread
- User mentions Twitter or X in a writing context
- Orchestrator (aios-writing-social) delegates a Twitter post

### Do NOT Use For
- Other platforms (use aios-writing-linkedin, aios-writing-instagram, etc.)
- Twitter/X ads (use writing-ads)

## Context Loading
Read all context files listed in aios-writing-social.

## Process

### Step 1: Parse the Request
Extract topic, content pillar, audience, type.

Defaults if unspecified:
- Content Pillar: Pillar 2 — Industry Contrarian Takes (25%)
- Audience: General PI audience
- Type: Thought Leadership

### Step 2: Write the Post

Single Tweet Rules:
- 280 characters max
- Punchy, direct, more personality than LinkedIn
- 1-2 hashtags or none
- Contrarian takes work best on this platform

Thread Rules:
- 5-10 tweets for longer content
- Tweet 1 is a contrarian hook that stands alone
- Number tweets as 1/, 2/, etc.
- Each tweet under 280 characters
- Last tweet is CTA
- Thread readable if someone only sees tweet 1

Tone:
- Punchier and more opinionated than LinkedIn
- Short sentences, strong verbs
- Casual but credible

### Step 3: Self-Review
Apply all quality gates from aios-writing-social.

Additional Twitter checks:
- Each tweet under 280 characters
- Tweet 1 hooks standalone
- Thread flows logically
- 1-2 hashtags max or none

## Output Format

Single tweet:

    PLATFORM: Twitter/X
    CONTENT PILLAR: [pillar]
    AUDIENCE: [segment]
    ---
    [TWEET TEXT]
    ---
    HASHTAGS: [0-2]

Thread:

    PLATFORM: Twitter/X (Thread)
    CONTENT PILLAR: [pillar]
    TWEET 1/[N]: [text]
    TWEET 2/[N]: [text]

## References
- references/hook-patterns.md
- references/post-templates.md
- shared/platform-specs.md
- shared/compliance-rules.md
