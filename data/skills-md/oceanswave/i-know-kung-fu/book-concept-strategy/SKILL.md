---
name: book-concept-strategy
description: Develop market-ready nonfiction book positioning from idea to reader-facing packaging. Use when users ask for book concept generation, audience targeting, title and subtitle options, market size estimation, trend alignment, introductions, back-cover copy, or author bios.
---

# Book Concept Strategy

## Overview

Use this skill to shape a commercially viable book concept before full drafting. Focus on reader demand, clear differentiation, and packaging that increases click-through and purchase intent.

## Workflow

1. Capture core inputs: niche, audience, genre, author background, and publishing goal.
2. If inputs are missing, make explicit assumptions and proceed.
3. Generate options, not one-offs, then score and rank.
4. Tie every recommendation to buyer motivation and discoverability.
5. For demand claims, include source and year whenever data is available.

## Capability 1: Generate 5 Book Concepts

Use when user asks for concept ideation in a specific niche.

Output for each concept:
- Title and subtitle.
- Target audience demographics.
- Unique angle versus existing books.
- Estimated market size (range + confidence).
- Why readers would pay $20-30.
- Trending topics aligned with current demand.

Recommended output shape:
```markdown
## Concept 1: <title>
- Subtitle:
- Audience:
- Unique angle:
- Market size estimate:
- Price justification:
- Trend alignment:
```

## Capability 2: Generate 15 Title + Subtitle Combinations

Use when user asks for title testing or Amazon-facing packaging options.

Hard requirements:
- 15 unique combinations.
- Under 60 characters total where feasible.
- Clear core benefit.
- Power words used naturally.
- Different enough to avoid looking templated.

Rate each option:
1. Clarity (1-10)
2. Intrigue (1-10)
3. SEO potential (1-10)

Use a table with columns: `Title + Subtitle`, `Length`, `Clarity`, `Intrigue`, `SEO`, `Notes`.

## Capability 3: Write Book Introduction

Use when user asks for an introduction draft.

Default structure:
1. Hook reader in first two sentences (fact, contradiction, or bold claim).
2. Define the problem the book solves.
3. Establish author credibility.
4. State what reader gains by finishing.
5. Preview structure.
6. Close with transformation promise.

Defaults:
- Length: 800-1200 words.
- Tone: mirror user request, else conversational-authoritative.

## Capability 4: Write Back Cover Copy (3 Versions)

Use formula in each version:
Problem -> Agitation -> Solution -> Benefits -> Credibility -> Call to action

Requirements per version:
- 100-150 words.
- Problem opening.
- Body with solution without full reveal.
- 3-5 bullet learning outcomes.
- Credibility markers.
- Final CTA.

## Capability 5: Write Author Bio (2 Lengths)

Output both:
- 100-150 words (back cover).
- 50 words (Amazon author page).

Include:
- Relevant credentials and experience.
- Why qualified for topic.
- 2-3 notable achievements.
- Personal connection.
- One humanizing detail.
- Third person voice.

## Quality Bar

- Avoid generic fluff or unsupported market claims.
- Keep language specific and audience-aware.
- Prefer concrete buyer outcomes over abstract promises.
- If trend or market data is uncertain, label confidence clearly.

## Hand-off Format

When delivering multiple assets in one response, use this section order:
1. `Concepts` (if requested)
2. `Title Options` (if requested)
3. `Introduction`
4. `Back Cover Versions`
5. `Author Bio`
6. `Assumptions and Data Notes`
