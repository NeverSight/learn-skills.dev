---
name: cannibalization-check
description: Find query and page overlap from GSC data and recommend consolidation, differentiation, or internal-link fixes. Use when Codex needs to identify and resolve keyword cannibalization issues.
---

# Cannibalization Check

## Overview

Analyze GSC query and page data to find situations where multiple pages compete for the same or closely related queries, diluting ranking potential. Recommend consolidation, 301 redirects, or differentiation strategies.

## Inputs

- GSC query + page export or live data
- Optional: site content inventory or sitemap

## Workflow

1. Load GSC data and group queries by semantic similarity.
2. For each query group, identify pages that appear for the same query.
3. Score cannibalization severity:
   - Multiple pages in top 20 for the same query
   - Pages splitting clicks/impressions across similar queries
   - High-authority page being cannibalized by a lower-authority page
4. For each cannibalization instance, recommend:
   - Consolidation: 301 to the best page
   - Differentiation: adjust targets so pages cover distinct subtopics
   - Internal link fix: adjust anchor text and link structure
5. Estimate the traffic recovery from resolving each instance.

## Output

Cannibalization report with competing page pairs, query overlap, severity score, and fix recommendation.
