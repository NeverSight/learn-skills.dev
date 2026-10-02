---
name: proposal-builder
description: Convert a prospects public site and optionally connected GSC/GA4 into an agency SEO proposal. Use when Codex needs to generate a client-ready SEO proposal from live or public data.
---

# Proposal Builder

## Overview

Analyze a prospect's website from public data (crawl, SERP analysis, sitemap) and optionally connected GSC/GA4 to produce a structured SEO proposal with diagnosis, opportunity sizing, recommended services, and pricing.

## Inputs

- Prospect domain URL
- Optional: GSC property data (via live data bridge)
- Optional: GA4 property data
- Optional: crawl output or sitemap

## Workflow

1. Discover the prospect's site (sitemap, crawl, public pages).
2. Run initial diagnosis:
   - Technical SEO issues (via technical-seo-triage)
   - Content gaps and decay signals
   - Keyword opportunities
   - Authority assessment (via serp-authority-mark for key queries)
3. If GSC/GA4 connected, analyze actual performance data.
4. Size the opportunity: estimated traffic gain, conversion uplift.
5. Structure the proposal:
   - Executive summary
   - Current situation and findings
   - Recommended services (technical, content, strategy)
   - Estimated impact
   - Pricing and timeline options
6. Generate a client-ready proposal document.

## Output

Structured SEO proposal document ready for client delivery.
