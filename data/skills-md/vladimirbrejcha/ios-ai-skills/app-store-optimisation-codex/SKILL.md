---
name: app-store-optimisation-codex
description: App Store Optimization (ASO) workflows for Apple App Store and Google Play Store. Use when Codex is asked to research keywords, optimize app metadata (titles, subtitles, descriptions, keywords), analyze competitors, plan A/B tests, compute ASO scores, analyze reviews, plan localization, or build launch/update checklists for mobile apps.
---

# App Store Optimisation (Codex)

## Overview

Provide end-to-end ASO support for App Store and Play Store listings, from research to execution. Use bundled Python modules for structured analysis and planning, and use browsing or user-provided inputs for live data.

## Quick Start

1. Identify the task: keyword research, metadata optimization, competitor analysis, review analysis, ASO scoring, A/B testing, localization, or launch planning.
2. Request required inputs (platforms, markets, current metadata, target keywords, metrics).
3. Use the matching script from `scripts/` to generate analysis or plans.
4. Validate character limits and platform rules, then deliver actionable recommendations.

## Core Tasks

### Keyword research

Use `scripts/keyword_analyzer.py`.

Request:
- Candidate keywords
- Estimated search volume and competition (user-provided or inferred)
- Relevance score per keyword

Deliver:
- Ranked keywords (primary, secondary, long-tail)
- Difficulty and potential scores

### Metadata optimisation

Use `scripts/metadata_optimizer.py`.

Request:
- Current metadata (title, subtitle, descriptions)
- Target keywords and value proposition
- Platform(s) and markets

Deliver:
- Optimized titles and descriptions with character counts
- Keyword density guidance

Default character limits (verify current limits before final output):
- Apple App Store: title 30, subtitle 30, promo text 170, description 4000, keywords 100
- Google Play: title 50, short description 80, full description 4000

### Competitor analysis

Use `scripts/competitor_analyzer.py`.

Request:
- Competitor names or IDs
- Platform and market

Optional data collection:
- Use `scripts/itunes_api.py` for Apple metadata
- Use browsing with prompt templates from `scripts/scraper.py`

Deliver:
- Keyword overlap, metadata patterns, visual asset notes, and gaps

### Review analysis

Use `scripts/review_analyzer.py`.

Request:
- Review text, ratings, and date range

Deliver:
- Sentiment split, top issues, feature requests, response templates

### ASO scoring

Use `scripts/aso_scorer.py`.

Request:
- Metadata quality inputs, ratings data, keyword ranking counts, conversion metrics

Deliver:
- Overall score with category breakdown and prioritized recommendations

### A/B testing

Use `scripts/ab_test_planner.py`.

Request:
- Baseline conversion rate and traffic
- Variants and test goal

Deliver:
- Sample size, duration guidance, and success metrics

### Localization planning

Use `scripts/localization_helper.py`.

Request:
- Current markets and target locales
- Budget and priority markets

Deliver:
- Localization priority order and draft localized metadata

### Launch and update checklists

Use `scripts/launch_checklist.py`.

Request:
- Platform(s), launch date, category, and key features

Deliver:
- Pre-launch checklist and post-launch monitoring plan

## Data Sources

See `references/data_sources.md` for API and browsing guidance.

## Resources

### scripts/

- `keyword_analyzer.py`
- `metadata_optimizer.py`
- `competitor_analyzer.py`
- `review_analyzer.py`
- `aso_scorer.py`
- `ab_test_planner.py`
- `localization_helper.py`
- `launch_checklist.py`
- `itunes_api.py`
- `scraper.py`

### references/

- `data_sources.md`
- `sample_input.json`
- `expected_output.json`
