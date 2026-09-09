---
name: tiktok-shop-growth-research
description: Conduct an evidence-backed TikTok Shop business study with current KOLSprite product, creator, video, shop, and caption data. Use for opportunity evaluation, cold-start planning, winning-content research, creator selection, competitor comparison, growth diagnosis, and questions such as whether and how a direction is worth testing. Do not use for a single direct lookup or caption-only request.
---

# TikTok Shop Growth Research

Turn a seller's decision into a bounded recommendation by combining data-search and caption tools exposed through the unified KOLSprite MCP. Use MCP automatically; do not ask whether to use it.

## Required shared references

Read [principles.md](references/principles.md) first. It defines evidence labels, query transparency, links, preference memory, product hand-offs, and stopping rules.

Read [judgment-guide.md](references/judgment-guide.md) when interpreting product stages, opportunity, creator fit, content patterns, shop concentration, or time windows. These definitions are calibrated to fields currently returned by the public KOLSprite MCP and must not be replaced with unavailable FastMoss-style trend or attribution fields.

For a substantial study, reusable workflow run, or partner-facing example, read [evidence-display.md](references/evidence-display.md) before delivery. Read [known-issues.md](references/known-issues.md) only after a matching current error, suspiciously repeated result set, or schema mismatch; historical observations are not active tool rules until reproduced.

## Select one primary workflow

- New product launch, go/no-go, first content tests, and initial creators: read [cold-start.md](references/cold-start.md).
- Reference videos, hooks, selling points, scripts, CTA patterns, and creator-ready shooting briefs: read [winning-content.md](references/winning-content.md).
- Category opportunity, proven demand, product candidates, and entry hypotheses: read [opportunity-scan.md](references/opportunity-scan.md).
- Creator shortlist, seeding, collaboration fit, or outreach cohort: read [creator-partnership.md](references/creator-partnership.md).
- Competitor shop/product comparison or growth-bottleneck diagnosis: read [competitor-growth.md](references/competitor-growth.md).

Choose one primary workflow even when several references contribute. A cold-start study may use opportunity, content, and creator methods, but it should still deliver one cold-start decision rather than three disconnected reports.

## Public MCP capability boundary

- Use `product_search`, `shop_search`, `video_search`, and `creator_search` for current structured evidence.
- Use `caption_extract_url` only for a small, decision-relevant video sample when spoken content matters.
- Reuse returned `product_id` and `shop_id` in supported downstream filters.
- Do not assume public detail, historical time-series, advertising, SKU, review-list, livestream, audience-demographic, channel-attribution, or exact product-to-creator relationship tools.

If the unified MCP service is missing or unauthenticated, identify the missing dependency. Continue only with a clearly bounded partial answer when the remaining evidence can still support it.

## Research control

1. State the decision, target market, product/category, constraints, and evidence needed.
2. Ask only for missing inputs that materially change scope or conclusion. A broad category request may proceed as a labelled preliminary scan.
3. Query only the tools needed for the decision. Reuse IDs, remove obvious contamination, and broaden an empty query once when appropriate.
4. Stop when the evidence supports the requested decision or when a missing capability prevents a reliable conclusion.
5. Deliver a recommendation, supporting evidence, interpretation, smallest next test, and material unknowns.

Point usage follows the actual tools executed, and different operations may consume different amounts. Use the smallest decision-sufficient call plan, reuse IDs and collected evidence, and stop when additional calls are unlikely to change the decision. Read the point controls in [principles.md](references/principles.md); do not hardcode prices or describe Skill selection itself as a deduction.

Prefer a defensible shortlist and explicit validation criteria over a long raw export.
