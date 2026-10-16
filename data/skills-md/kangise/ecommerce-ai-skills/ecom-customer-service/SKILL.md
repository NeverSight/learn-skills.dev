---
name: ecom-customer-service
description: Respond to buyer messages and negative reviews, draft refund and return replies, review-request emails, Plan of Action appeals, FAQ, and CS KPI tracking. Use for complaint handling, account appeal, or after-sales support.
---

# Customer Service Skill

## When to Use

Respond to buyer messages and negative reviews, draft refund and return replies, review-request emails, Plan of Action appeals, FAQ, and CS KPI tracking. Use for complaint handling, account appeal, or after-sales support.

## Method

### Step 1: Read Platform Constraints

Read `references/constraints.md` for platform-specific rules (response deadlines, commitment boundaries, AI-content licensing).

### Step 2: Review Boundaries

Read `references/boundaries.md` to know when this skill should NOT be used.

### Step 3: Pick the Prompt

Pick the appropriate prompt from `references/playbook.md` for your scenario (review analysis, public reply, appeal letter, multilingual templates, review-request email, FAQ, return analysis, KPI design, sentiment monitoring).

### Step 4: Execute and Verify

Execute the prompt with your data. Use the `<自检>/<self_check>/<セルフチェック>` self-check block in each prompt to verify output quality before delivering results. Never send customer-facing content without a human check on commitments (refunds, compensation, timelines).

## References

- [Constraints](references/constraints.md) — Platform rules and limits
- [Playbook](references/playbook.md) — Prompt collection
- [Boundaries](references/boundaries.md) — When not to use

## Templates

Copy-ready prompt templates (in `assets/templates/`):

- [Negative Review Public Response](assets/templates/template-1-negative-review-response.md)
- [Review Request Email](assets/templates/template-2-review-request-email.md)
- [Plan of Action Appeal](assets/templates/template-3-plan-of-action-appeal.md)
