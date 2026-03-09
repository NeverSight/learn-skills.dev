---
name: aios-writing-threads
description: >
  Write Threads posts. Use when asked to write, create, draft, or produce
  a Threads post or Threads content. Also use when user mentions Threads
  in a social media writing context. Outputs short casual quick-take posts.
metadata:
  author: claim-supply
  version: 1.0.0
---

# Writing Threads

## Purpose
Produce publish-ready Threads posts with the most casual quick-take tone.

## When to Use
- User asks to write a Threads post
- User mentions Threads in a writing context
- Orchestrator delegates a Threads post

### Do NOT Use For
- Other platforms

## Context Loading
Read all context files listed in aios-writing-social.

## Process

### Step 1: Parse the Request
Defaults: Pillar 2 (25%), General audience, Thought Leadership.

### Step 2: Write the Post
Format: Under 500 characters. Casual, conversational. Quick takes. No hashtags.
Tone: Most casual of all platforms. Short and punchy.

### Step 3: Self-Review
Apply quality gates from aios-writing-social. Under 500 chars, no hashtags, casual tone.

## Output Format
    PLATFORM: Threads
    CONTENT PILLAR: [pillar]
    AUDIENCE: [segment]
    ---
    [POST TEXT]

## References
- references/hook-patterns.md
- shared/platform-specs.md
- shared/compliance-rules.md
