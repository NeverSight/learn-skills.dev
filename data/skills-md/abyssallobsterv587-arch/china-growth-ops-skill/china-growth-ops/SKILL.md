---
name: china-growth-ops
description: Master compliant China multi-platform growth operations across Douyin, Xiaohongshu, Kuaishou, WeChat, and major ecommerce marketplaces. Use for product selection, offer positioning, content strategy, listing copy, social captions, chat reply flows, lead capture funnels, browser-ready field preparation, publish checklists, and daily growth review. Do not use for spam, fake engagement, mass unsolicited messaging, or platform rule circumvention.
---

# China Multi-Platform Growth

Use this skill for Chinese-market growth operations across short-video, social, chat, and ecommerce workflows.

For repository onboarding and environment checks:
- Use [docs/install.md](docs/install.md) for quick install and execution guidance
- Use [scripts/doctor.sh](scripts/doctor.sh) for a lightweight local readiness check

This skill is for:
- Product selection and demand validation
- Offer positioning and pricing angles
- Drafting scripts, captions, titles, listing copy, and chat replies
- Coordinating semi-automated posting workflows in a browser
- Building lead capture funnels that still require human approval at final publish points

This skill is not for:
- Mass unsolicited outreach
- Fake engagement, bot traffic, or review manipulation
- Account farming, ban evasion, or platform rule circumvention
- Fully autonomous posting without human review on high-risk pages

## Default Execution Model

Treat this as a semi-automatic operating system:

1. Pick one product, offer, or campaign goal.
2. Choose one primary platform and one secondary platform.
3. Produce platform-specific copy from a single source offer.
4. Prepare browser steps and field values.
5. Stop at login, captcha, payment, publish, or other irreversible actions unless the user explicitly wants blind GUI attempts.
6. Record outputs and next actions for reuse.

## Core Workflow

### 1. Define the commercial unit

Before drafting content, lock these inputs:
- Product or service
- Target buyer
- Price band
- Conversion goal
- Primary platform

If the user is vague, default to:
- One SKU
- One audience
- One platform-first test

### 2. Select products and angles

For product selection and offer framing:
- Prefer products with clear pain relief, visible before/after value, repeat demand, or impulse appeal
- Avoid products needing medical, legal, or highly regulated claims
- Generate 3 candidate angles, then select 1 winner

Read [references/platforms.md](references/platforms.md) for platform-specific product and content angles.
For vertical-specific offer angles and output packs, read [references/verticals.md](references/verticals.md).

### 3. Generate copy assets

Always generate from one source brief, then adapt into:
- Short video hook
- Caption
- Product title
- Product highlights
- FAQ / objection handling
- Chat reply templates

Read [references/templates.md](references/templates.md) for reusable copy patterns.
For a full example of one end-to-end run, read [references/example-run.md](references/example-run.md).
For product scoring before execution, read [references/product-scorecard.md](references/product-scorecard.md).

### 4. Browser execution

When using browser or GUI automation:
- Prefer filling drafts, descriptions, tags, and metadata
- Prefer opening the correct page and preparing form values
- Require human confirmation for final publish, payment, private messaging bursts, or irreversible account actions
- If the user insists on blind GUI, report the risk and keep the action scope narrow

### 5. Reporting

After each run, summarize:
- Platform
- Offer
- Copy created
- Page prepared
- Blocking step
- Next manual action

## Platform Coverage

This skill supports:
- Douyin
- Xiaohongshu
- Kuaishou
- WeChat / WeCom style chat workflows
- Taobao / Tmall
- JD
- Pinduoduo
- 1688
- Generic ecommerce landing pages

Use platform-specific language and formatting, not one generic post for everything.

## Safety and Compliance

Never optimize for:
- Spam volume
- Fake scarcity
- Fabricated reviews
- Guaranteed earnings claims
- Misleading health, finance, or compliance claims

When in doubt:
- downgrade to draft-only mode
- ask for human review before publish
- preserve account safety over speed

## Deliverables

A standard run should return:
- Selected product angle
- Platform-specific copy pack
- Suggested browser actions
- Publish blockers
- KPI checklist for the next review

## Recommended Output Format

Return results in this order:

1. Offer decision
2. Platform plan
3. Copy pack
4. Browser-ready fields
5. Risks and blockers
6. KPI checklist

For publish preparation and review, use:
- [references/publish-checklists.md](references/publish-checklists.md)
- [references/daily-review.md](references/daily-review.md)

For service packaging and client delivery, use:
- [references/service-packages.md](references/service-packages.md)
- [references/client-delivery.md](references/client-delivery.md)
