---
name: aios-writing-linkedin
description: >
  Write LinkedIn posts and articles. Use when asked to write, create, draft,
  or produce a LinkedIn post, LinkedIn article, LinkedIn update, or LinkedIn
  thought leadership content. Also use when user mentions LinkedIn in a social
  media writing context. Outputs publish-ready LinkedIn content with hooks,
  hashtags, and CTAs.
metadata:
  author: claim-supply
  version: 1.0.0
---

# Writing LinkedIn

## Purpose
Produce publish-ready LinkedIn posts that match brand voice, target the correct audience, and follow LinkedIn best practices.

## When to Use
- User asks to write a LinkedIn post, update, or article
- User mentions LinkedIn in a writing context
- Orchestrator (aios-writing-social) delegates a LinkedIn post

### Do NOT Use For
- Other platforms (use aios-writing-twitter, aios-writing-instagram, etc.)
- LinkedIn ads or sponsored content (use writing-ads)

## Context Loading
Read all context files listed in aios-writing-social.

## Process

### Step 1: Parse the Request
Extract topic, content pillar, audience, type.

Defaults if unspecified:
- Content Pillar: Pillar 1 — Lead Economics and ROI (30%)
- Audience: Managing Partners / Firm Owners
- Type: Educational (40% of content mix)

If 2+ variables missing, confirm defaults before generating.

### Step 2: Write the Post

LinkedIn Format Rules:
- Hook in first 2 lines (before see more fold) — critical
- 800-1,500 characters recommended (3,000 max)
- Line breaks between ideas for readability
- Professional but not stiff — operational, direct tone
- 3-5 hashtags at end
- CTA as final line before hashtags

Tone:
- Professional but conversational
- Infrastructure/supply-chain framing over sales language
- Challenge the industry, not the reader
- Founder voice — experienced, direct, no fluff

### Step 3: Self-Review
Apply all quality gates from aios-writing-social.

Additional LinkedIn checks:
- Hook compelling in first 2 lines
- Post 800-1,500 characters
- 3-5 relevant hashtags
- CTA is soft invitation not hard sell
- Line breaks for readability

## Output Format

```
PLATFORM: LinkedIn
CONTENT PILLAR: [pillar]
AUDIENCE: [segment]
TYPE: [type]

---

[POST TEXT]

---

HASHTAGS: [3-5 hashtags]
CTA: [if not embedded]
IMAGE PROMPT: [optional]
NOTES: [reviewer notes]
```

## References
- references/hook-patterns.md
- references/post-templates.md
- shared/platform-specs.md
- shared/compliance-rules.md
