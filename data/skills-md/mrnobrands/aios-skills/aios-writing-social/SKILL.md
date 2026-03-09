---
name: aios-writing-social
description: >
  Orchestrate social media content creation across platforms. Use when asked
  to write, create, or draft social media content without specifying a platform,
  or when requesting multi-platform batches, content calendars, or social media
  planning. Delegates to platform-specific skills for LinkedIn, Twitter/X,
  Instagram, Facebook, and Threads. Do NOT use for blog posts, emails, ads,
  or landing pages.
metadata:
  author: claim-supply
  version: 2.0.0
---

# Writing Social — Orchestrator

## Purpose
Route social media requests to the correct platform skill. Handles multi-platform batches, content calendars, and requests where the platform is unspecified. Owns the shared quality gates, context loading, and compliance checks that all platform skills reference.

## When to Use
- User asks to write social content without specifying a platform
- User asks for a content calendar or batch of social posts across platforms
- User asks for multi-platform content repurposing
- User says "write me a social post" or "create some content"

### Do NOT Use For
- Platform-specific requests (use aios-writing-linkedin, aios-writing-twitter, etc.)
- Blog posts or long-form (use writing-blog)
- Email sequences (use writing-email)
- Ad copy for paid campaigns (use writing-ads)

## Context Loading

### Always Read (Before Every Post)
1. `companies/claim-supply/brand.md` — positioning, differentiators, personality
2. `companies/claim-supply/audiences.md` — who we write for
3. `companies/claim-supply/voice-and-tone.md` — how we sound, words to use/avoid
4. `companies/claim-supply/content-strategy.md` — pillars, platform rules, content mix

### Read If Relevant
5. `companies/claim-supply/goals.md` — align with current objectives
6. `companies/claim-supply/calendar.md` — timely topics or blackout periods
7. `companies/claim-supply/products.md` — if referencing a specific product/service
8. `companies/claim-supply/founder.md` — if writing as/about the founder
9. `companies/claim-supply/competitors.md` — if writing competitive content

### Always Reference
10. `shared/platform-specs.md` — character limits, image sizes, posting rules
11. `shared/compliance-rules.md` — legal disclaimers, TCPA, ABA rules
12. `shared/writing-rules.md` — universal writing standards

### Deduplication Check
13. Query Supabase `content_log` — last 14 days
14. Query Supabase `publishing_queue` — what is already planned

## Process

### Step 1: Determine Platform
If user specifies a platform, delegate immediately to the platform skill:
- LinkedIn → use aios-writing-linkedin
- Twitter/X → use aios-writing-twitter
- Instagram → use aios-writing-instagram
- Facebook → use aios-writing-facebook
- Threads → use aios-writing-threads

If no platform specified, ask: "Which platform? LinkedIn, Twitter/X, Instagram, Facebook, or Threads? Or want me to create for multiple?"

If user says "all" or "multiple" or "batch":
- Generate one post per platform using platform-specific skills
- Cycle through content pillars: Pillar 1 (30%), Pillar 2 (25%), Pillar 3 (25%), Pillar 4 (20%)
- Alternate audiences across posts

### Step 2: Batch / Calendar Mode
For content calendar requests:
- Ask for timeframe (1 week, 2 weeks, 1 month)
- Distribute across platforms per content-strategy.md allocation
- Balance content pillars and audiences
- Output as a table with date, platform, pillar, audience, topic

### Step 3: Apply Shared Quality Gates
Every post from every platform skill must pass these checks before output:

#### Voice Check
- Does this sound like the brand? Compare against voice-and-tone.md examples
- Are any words to avoid present? Remove them
- Does the post challenge the industry/system, not the reader?
- Is the CTA an invitation, not a command?

#### Audience Check
- Written for the target audience, not a general audience?
- Addresses their pain points from audiences.md?
- Would this audience find it valuable or shareable?

#### Strategy Check
- Aligns with a content pillar from content-strategy.md?
- Content mix balance maintained?
- Clear CTA or takeaway?

#### Data Integrity Check
- Every statistic sourced or qualified
- No unsourced percentage or multiplier claims stated as fact
- Proprietary data labeled as such

#### Compliance Check
- No false or misleading claims
- No guaranteed outcomes or settlement amounts
- Appropriate disclaimers for legal services
- No real lead/client data exposed
- Compliant with ABA Model Rules

#### Writing Quality Check
- Strong opening hook?
- Every sentence earns its place?
- Active voice? Specific over vague? No filler?

## Output Format
Delegates to platform-specific skill output formats. For multi-platform batches, output each post with its platform header.

## References
- `references/hook-patterns.md` — proven opening hooks
- `references/post-templates.md` — platform-specific structure templates
- `shared/platform-specs.md` — character limits, image sizes
- `shared/compliance-rules.md` — legal and regulatory rules
- `shared/writing-rules.md` — universal writing standards
