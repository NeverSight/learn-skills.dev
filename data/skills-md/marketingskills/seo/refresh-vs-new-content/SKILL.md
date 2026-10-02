---
name: refresh-vs-new-content
description: Decide whether to update, consolidate, prune, or create new content for a given page or topic. Use when Codex needs to recommend the best content action based on performance data and competitive analysis.
---

# Refresh vs New Content

## Overview

Given a page and its performance data, decide the best content action: refresh (update existing), consolidate (merge pages), prune (remove or redirect), or create new. Uses traffic trends, SERP competitiveness, content quality, and business value.

## Inputs

- Page URL and current performance data (GSC/GA4)
- Content quality assessment (depth, freshness, accuracy)
- SERP competitive analysis for the page's primary query
- Business value of the topic

## Workflow

1. Assess the page's current content quality:
   - Outdated information or examples
   - Thin content compared to top SERP results
   - Missing entities or sections
   - Poor user engagement signals (bounce rate, time on page)
2. Assess traffic potential:
   - Total search demand for the primary query
   - Authority feasibility (can this site rank?)
   - Seasonality or trend direction
3. Decision matrix:
   - **Refresh**: page has good bones, query is stable or growing, authority exists
   - **Consolidate**: page is thin, overlaps with another stronger page on the site
   - **Prune**: query demand declining, page has no unique value, better to redirect authority
   - **Create new**: new query opportunity, site has no existing coverage, authority is feasible
4. For refresh: pass to content-refresh-brief for the detailed brief.
5. For create new: pass to seo-content-brief.
6. For consolidate/prune: recommend the target URL or redirect destination.

## Output

Content action recommendation with rationale, expected impact, and handoff to the relevant skill.
