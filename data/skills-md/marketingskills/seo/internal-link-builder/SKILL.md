---
name: internal-link-builder
description: Suggest source pages, anchor text, target URLs, and rationale for internal link improvements. Use when Codex needs to strengthen topical clusters and distribute page authority through internal links.
---

# Internal Link Builder

## Overview

Analyze a set of pages to recommend internal link additions that strengthen topical clusters, distribute authority to thin content, and improve crawl efficiency.

## Inputs

- Target page URLs (pages needing more internal links)
- Optional: site crawl or sitemap to discover link sources
- Optional: GSC data to identify high-traffic source candidates

## Workflow

1. Identify target pages (content needing authority support, new pages, deep pages).
2. Find candidate source pages: high-traffic pages, pillar pages, topic hub pages.
3. For each source-to-target pair, recommend:
   - Anchor text (relevant, varied, descriptive)
   - Placement context (where in the content the link fits)
   - Rationale (topical relevance, authority flow, user journey)
4. Avoid over-optimization patterns: excessive exact-match anchors, links from unrelated pages.
5. Prioritize by: source page authority, topical relevance, and expected click-through.

## Output

Internal link plan with source page, target URL, anchor text, placement context, and priority.
