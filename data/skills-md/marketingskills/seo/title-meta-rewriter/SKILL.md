---
name: title-meta-rewriter
description: Generate title and meta description alternatives from GSC query evidence and SERP intent. Use when Codex needs to improve organic CTR by rewriting page metadata.
---

# Title Meta Rewriter

## Overview

Given a page URL and its GSC query performance, produce title and meta description alternatives that better match search intent and improve organic CTR. Uses actual query data to understand what users are searching for.

## Inputs

- Page URL
- GSC query data for the page (queries driving impressions, CTR per query)
- Optional: current SERP titles from top-ranking competitors

## Workflow

1. Analyze GSC queries that drive impressions to the page.
2. Identify the primary query and secondary queries.
3. Check the current SERP for competitor title patterns.
4. Evaluate the current title and meta description: does it match the dominant query intent?
5. Generate 3-5 title alternatives that:
   - Include the primary query or close variant
   - Match the search intent (informational, commercial, etc.)
   - Differentiate from competitor titles
   - Stay within length limits (60 chars for title, 160 for meta)
6. Generate 2-3 meta description alternatives.
7. For each alternative, note the expected CTR impact.

## Output

Title and meta description alternatives with CTR rationale and recommendation.
