---
name: geo-conversion-optimizer
description: >
  GEO conversion optimization engine that balances AI citation readiness with real user conversion. Use this skill whenever the user wants content that both ranks well in AI answers and actually drives sign-ups, leads, purchases, or other business outcomes, not just “SEO/GEO for its own sake”.
---

## Overview

`geo-conversion-optimizer` is a GEO (Generative Engine Optimization) conversion-focused skill.
Its purpose is to help you systematically **optimize content for both**:

- **AI / GEO performance**: structure, clarity, citability, schema, FAQ sections, etc.
- **Real-world conversion**: sign-ups, purchases, demo requests, bookings, downloads, or other business KPIs.

This skill exists to avoid the trap of **“content that AIs love but humans never convert on”**.
Whenever you are asked to optimize or create content for GEO, **explicitly consider and protect conversion quality** using this skill.

`geo-conversion-optimizer` can be used alone or together with other `geo-*` skills
such as `geo-schema-gen`, `geo-bulk-processor`, and content-focused GEO optimizers.

## When to use this skill

Always consider `geo-conversion-optimizer` when:

- The user mentions **conversion**, **sign-ups**, **leads**, **sales**, **bookings**, **trial activations**, or **ROI**.
- The goal is to **change or create content** for:
  - Landing pages and product pages.
  - Pricing pages and comparison pages.
  - Long-form articles with embedded calls to action.
  - Local / location pages that ultimately need calls, bookings, or visits.
- The user is worried about trade-offs like:
  - “Will this hurt my conversion rate?”
  - “This feels written for bots, not people.”
  - “We optimized for AI but leads went down.”

If the task is **purely informational** (for example, an internal knowledge base article
with no conversion goal), you may not need this skill. But whenever **business outcomes**
are in scope, prefer to invoke `geo-conversion-optimizer`.

## High-level workflow

When this skill is invoked, follow this structured workflow:

1. **Clarify business and conversion goals**
2. **Map user and AI intents**
3. **Audit current content (if it exists)**
4. **Design a dual-track GEO + conversion strategy**
5. **Redesign structure, messaging, and CTAs**
6. **Plan measurement, experiments, and safeguards**
7. **Produce concrete deliverables and implementation notes**

Each step is described below.

### 1. Clarify business and conversion goals

Always start with the business outcome, not just “improve GEO”.

- Identify:
  - **Primary conversion goal** (e.g., demo request, free trial, add to cart, book appointment).
  - **Secondary goals** (newsletter sign-up, add to wishlist, download content, account creation).
  - **Constraints**:
    - Brand tone and visual identity.
    - Legal / compliance requirements.
    - Traffic sources and existing funnels.
- Ask (or infer) the **time horizon**:
  - Short-term campaign vs. always-on evergreen content.
  - Need for quick uplift vs. long-term learning and optimization.

Document these clearly in the plan so all later choices can be traced back.

### 2. Map user and AI intents

GEO content must serve **two overlapping but distinct “consumers”**:

- The **human user** with:
  - A specific problem, job to be done, or context.
  - A stage in the funnel (awareness, consideration, decision, post-purchase).
- The **AI model** that:
  - Needs clear structure, unambiguous facts, and stable patterns.
  - Prefers well-defined entities, relationships, and FAQs.

Actions:
- Define the **top 3–7 user intents** this page/content should satisfy.
- For each intent, note:
  - Funnel stage.
  - Desired **next action** (what good looks like).
  - Potential **AI queries** or prompts that should surface this content.
- Identify where **human and AI needs overlap**, and where they diverge.

### 3. Audit current content (if applicable)

If the content already exists (e.g., a landing page or product page):

- Evaluate **GEO readiness**:
  - Clear headings and structure?
  - Concise, factual sections suitable for AI summarization?
  - FAQs and schema present where appropriate?
- Evaluate **conversion readiness**:
  - Clear primary CTA above the fold?
  - Compelling value propositions and social proof?
  - Friction points (confusing copy, missing information, trust gaps)?
- Identify **points of conflict**:
  - Overloaded with keywords and robotic language.
  - Walls of text that harm scannability and decision-making.

Summarize issues as **tensions** (e.g., “explains features well for AI, but hides pricing and CTAs”).

### 4. Design a dual-track GEO + conversion strategy

For this skill, every recommendation should explicitly show how it serves **both tracks**:

- **GEO / AI track**:
  - Improve structure, clarity, and citability.
  - Ensure important entities, relationships, and FAQs are explicit.
  - Align with relevant schemas (Article, Product, LocalBusiness, FAQPage, etc.).

- **Conversion track**:
  - Prioritize information architecture that mirrors the decision journey.
  - Make CTAs, proof, and risk reducers visible and compelling.
  - Support multiple entry points (e.g., from AI answers deep-linking into sections).

Define:
- **Key sections** and their roles for both GEO and conversion.
- **Message hierarchy** (what must be seen first vs. later).
- **Non-negotiables**:
  - “These CTAs must remain above the fold.”
  - “These trust elements (logos, reviews) must be clearly visible.”

### 5. Redesign structure, messaging, and CTAs

For the page or content in scope:

- Propose a **section-by-section structure**:
  - Top hero: clear value proposition + primary CTA.
  - Problem / pain section.
  - Solution / product overview.
  - Proof (logos, testimonials, case snippets).
  - Detailed comparison, pricing, or feature breakdown.
  - FAQs (designed for both AI and human objections).
  - Supporting resources / long-form content if relevant.
- For each section, specify:
  - **GEO role**: what entities, phrases, or queries it should help with.
  - **Conversion role**: what objection it answers, what action it nudges.
  - **Design notes**: any requirements for clarity, brevity, or visual emphasis.
- Design **CTAs and microcopy**:
  - Primary and secondary CTAs with clear labels.
  - Contextual microcopy that reduces friction and fear (e.g., “no credit card required”, “cancel anytime”).

Avoid sacrificing conversion just to “sound more GEO-friendly”. If a GEO change
risks hurting clarity or trust, flag it and propose safer alternatives.

### 6. Plan measurement, experiments, and safeguards

Always include a **measurement and experimentation plan**:

- **Metrics**:
  - GEO / AI metrics: AI citation presence/coverage if available, impressions or traffic proxies.
  - Conversion metrics: CR%, CTR to CTA, lead quality indicators, downstream revenue where available.
- **Experiments**:
  - A/B or multivariate tests on key elements (hero message, CTAs, FAQ section).
  - Controlled rollouts (e.g., a subset of traffic or a subset of pages).
- **Safeguards**:
  - Baseline snapshots before changes.
  - Guardrail metrics (e.g., “do not accept a GEO uplift that causes >X% drop in CR”).

Make sure the plan is practical for the user’s team and tools (e.g., GA, experimentation platform, internal dashboards).

### 7. Produce concrete deliverables and implementation notes

Outputs should be **ready to act on**, not just high-level advice. Examples:

- **Conversion-aware content blueprint**:
  - Section list, brief description, and GEO vs. conversion role per section.
- **Copy and content recommendations**:
  - Example headlines, CTAs, FAQ questions and answers, proof elements.
- **Integration notes for other `geo-*` skills**:
  - Where to call `geo-schema-gen` for structured data.
  - How to align with `geo-bulk-processor` if many similar pages must be optimized.
- **Rollout and testing checklist**:
  - Steps for implementation, QA, and measurement.

Be explicit about **what is opinionated guidance** vs. what is **strictly required**.

## Input and output expectations

### Inputs

Expect to work with:

- URLs, HTML/Markdown content, or copy drafts.
- Screenshots, wireframes, or descriptions of current pages.
- Conversion data (if shared) such as:
  - Current conversion rates.
  - Click maps, scroll depth summaries, or common user complaints.
- Business constraints (e.g., mandatory legal text, forbidden claims).

If information is missing, **state reasonable assumptions** instead of getting blocked,
and clearly mark them as assumptions.

### Outputs

Unless the user asks for something very specific, default to the following structures:

- **Conversion-aware GEO optimization report**
  - Executive summary.
  - Business goals and constraints.
  - Main recommendations with GEO vs. conversion rationale.
- **Page/content blueprint**
  - Section-by-section outline.
  - Key messages, CTAs, and proof elements.
  - GEO and schema notes.
- **Experiment and measurement plan**
  - Proposed tests.
  - Metrics and guardrails.
  - Rollout and iteration approach.

If the user wants directly usable copy, produce **draft copy** that already
embeds both GEO and conversion principles.

## Use of bundled resources

This skill ships with additional resources:

- `references/conversion_playbook.md`
  - Contains patterns and checklists for balancing GEO and conversion
    across common page types (landing pages, product pages, blogs, local pages).
  - Provides ready-made section archetypes and objection-handling patterns.

- `scripts/conversion_blueprints.py`
  - Contains simple data models and helper functions for representing
    page blueprints, CTAs, and experiments at a structured level.
  - Can be used as inspiration for how teams might represent and track
    conversion-aware GEO changes across many pages.

Use these resources when you need more concrete examples or templates
to structure your recommendations.

## Style and collaboration guidelines

- **Think like a performance marketer plus GEO architect.**
  - Protect user clarity, trust, and intent-to-buy while also serving AI needs.
- **Explain trade-offs.**
  - When a suggestion helps GEO but may harm conversion (or vice versa),
    make the trade-off explicit and offer alternatives.
- **Be concrete and operational.**
  - Favor checklists, sections, and examples that can be implemented directly.
- **Respect domain constraints.**
  - For regulated industries (health, finance, legal), be extra cautious
    about claims and wording. Encourage review by legal/compliance teams.

The mission of `geo-conversion-optimizer` is to make GEO work for the
business, not just for rankings or AI citations in isolation.

