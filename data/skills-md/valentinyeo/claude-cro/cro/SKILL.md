---
name: cro
description: >
  CRO (Conversion Rate Optimization) skill for auditing websites, analyzing
  conversion funnels, generating A/B test hypotheses, evaluating UX and copy,
  assessing trust signals, and building optimization roadmaps. Use when the user
  mentions CRO, conversion, optimize, A/B test, funnel, landing page, or
  conversion rate. Covers SaaS, e-commerce, lead gen, subscription, local
  service, and agency/B2B sites.
argument-hint: "<subcommand> <url>"
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

# CRO — Conversion Rate Optimization Skill

Analyze any website for conversion optimization opportunities. Detect business
type, evaluate UX, copy, trust signals, forms, tracking, and visual hierarchy,
then produce prioritized recommendations with A/B test hypotheses.

## Quick Reference

| Command | Description |
|---------|-------------|
| `/cro audit <url>` | Full website conversion audit with parallel agents |
| `/cro page <url>` | Single page conversion deep-dive |
| `/cro funnel <url1> <url2>...` | Multi-step funnel mapping and drop-off analysis |
| `/cro test <url>` | A/B test hypothesis generation (ICE framework) |
| `/cro copy <url>` | Conversion copywriting analysis |
| `/cro ux <url>` | UX heuristic evaluation |
| `/cro forms <url>` | Form optimization analysis |
| `/cro ecommerce <url>` | E-commerce CRO (PDP, cart, checkout) |
| `/cro trust <url>` | Trust signals and social proof audit |
| `/cro tracking <url>` | Analytics and tracking setup validation |
| `/cro benchmark <url> <competitor-url>` | Competitor conversion comparison |
| `/cro plan <url>` | CRO strategy and 90-day roadmap |

---

## Orchestration Logic

### Full Audit (`/cro audit $ARGUMENTS`)

1. **Fetch the page** using the fetch script:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/fetch_page.py $ARGUMENTS
   ```
2. **Extract CRO elements** using the parse script:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/parse_cro.py $ARGUMENTS
   ```
3. **Detect business type** using the Industry Detection rules below.
4. **Spawn 6 subagents in parallel** — each receives the page content and
   business type context:
   - `cro-ux` — UX heuristic evaluation
   - `cro-copy` — Conversion copywriting analysis
   - `cro-tracking` — Analytics and tracking validation
   - `cro-visual` — Visual hierarchy and layout analysis
   - `cro-performance` — Page speed and technical performance
   - `cro-trust` — Trust signals and social proof audit
5. **Collect results** from all 6 subagents.
6. **Calculate CRO Health Score** using the weighted formula below.
7. **Generate the final report** with:
   - CRO Health Score (0-100) with rating
   - Business type detected
   - Top 5 critical findings (sorted by impact)
   - Category-by-category breakdown
   - Prioritized recommendation list (Critical > High > Medium > Low)
   - 3 quick-win A/B test hypotheses

### Individual Commands

For individual commands (`/cro page`, `/cro copy`, etc.), load the relevant
sub-skill directly — no subagent spawning needed. Each sub-skill contains its
own evaluation framework and output format.

---

## Industry Detection

Analyze the fetched page for these signals to classify the business type:

| Business Type | Detection Signals |
|---------------|-------------------|
| **SaaS** | `/pricing`, `/features`, "free trial", "sign up", "book a demo", "start free", `/docs`, `/api`, "integrations" |
| **E-commerce** | `/products`, `/collections`, `/cart`, "add to cart", product schema (`Product` JSON-LD), price elements, `/shop`, "buy now" |
| **Lead Gen** | Contact form, "get a quote", "book a call", "request a demo", phone number prominent, `/contact`, form with 3+ fields |
| **Subscription** | `/plans`, "subscribe", recurring pricing, membership tiers, "monthly/annually", "per month", billing toggle |
| **Local Service** | Street address, phone number, service area mentions, Google Maps embed, "serving [city]", "locations", schema `LocalBusiness` |
| **Agency/B2B** | `/case-studies`, `/portfolio`, "our work", client logos section, "we helped", `/about`, team section, industry specializations |

When multiple signals match, choose the primary type but note secondary types
in the report (e.g., "Primary: E-commerce, Secondary: Subscription").

---

## CRO Health Score (0-100)

Weighted composite score across all evaluation categories:

| Category | Weight | Evaluator |
|----------|--------|-----------|
| UX | 25% | cro-ux subagent |
| Copy | 20% | cro-copy subagent |
| Trust | 15% | cro-trust subagent |
| Visual Hierarchy | 15% | cro-visual subagent |
| Forms | 10% | cro-ux subagent (forms section) |
| Performance | 10% | cro-performance subagent |
| Tracking | 5% | cro-tracking subagent |

**Formula:** `Score = (UX × 0.25) + (Copy × 0.20) + (Trust × 0.15) + (Visual × 0.15) + (Forms × 0.10) + (Performance × 0.10) + (Tracking × 0.05)`

Each subagent scores its category 0-100. The orchestrator applies the weights.

### Score Ratings

| Score | Rating | Interpretation |
|-------|--------|----------------|
| 90-100 | Exceptional | Best-in-class conversion optimization. Minor polish only. |
| 70-89 | Strong | Solid foundation with clear optimization opportunities. |
| 50-69 | Moderate | Significant gaps impacting conversion. Prioritized action needed. |
| 30-49 | Weak | Major conversion barriers present. Urgent remediation required. |
| 0-29 | Critical | Fundamental issues blocking conversions. Immediate intervention needed. |

---

## Priority Levels

Every finding must be assigned a priority level:

| Priority | Definition | Action |
|----------|------------|--------|
| **Critical** | Actively blocks conversions. Users cannot complete key actions (broken forms, missing CTAs, trust-destroying issues). | Fix immediately. |
| **High** | Major negative impact on conversion rate. Significant friction or missed persuasion opportunity. | Fix within 1-2 weeks. |
| **Medium** | Optimization opportunity. Current state works but leaves conversions on the table. | Plan and test within 30 days. |
| **Low** | Polish and refinement. Minor improvements that compound over time. | Backlog for future sprints. |

---

## Reference Files

Load on-demand as needed — do NOT load all at startup. Paths are relative to this skill directory.

| File | Path | Use When |
|------|------|----------|
| Conversion Benchmarks | [references/conversion-benchmarks.md](references/conversion-benchmarks.md) | Comparing metrics to industry standards, setting targets |
| Psychology Principles | [references/psychology-principles.md](references/psychology-principles.md) | Evaluating persuasion tactics, recommending psychological triggers |
| Testing Framework | [references/testing-framework.md](references/testing-framework.md) | Generating test hypotheses, calculating sample sizes, ICE scoring |
| UX Heuristics | [references/ux-heuristics.md](references/ux-heuristics.md) | Running UX evaluations, form analysis, mobile assessment |
| Quality Gates | [references/quality-gates.md](references/quality-gates.md) | Checking minimum requirements, pass/fail criteria |
| Proven Tests: Ecommerce | [references/proven-tests-ecommerce.md](references/proven-tests-ecommerce.md) | Referencing data-backed Shopify/ecommerce A/B tests with documented results |
| Proven Tests: B2B/SaaS | [references/proven-tests-b2b.md](references/proven-tests-b2b.md) | Referencing data-backed B2B, SaaS, and consulting landing page tests |
| Proven Tests: General | [references/proven-tests-general.md](references/proven-tests-general.md) | Referencing universal CRO tests with cross-reference tables by principle and page type |

---

## Sub-Skills

Each maps to a `/cro` command and can be invoked independently:

| Sub-Skill | Command | Focus Area |
|-----------|---------|------------|
| `cro-audit` | `/cro audit` | Full-site orchestrated audit |
| `cro-page` | `/cro page` | Single page deep-dive |
| `cro-funnel` | `/cro funnel` | Multi-step funnel analysis |
| `cro-testing` | `/cro test` | A/B test hypothesis generation |
| `cro-copy` | `/cro copy` | Conversion copywriting |
| `cro-ux` | `/cro ux` | UX heuristic evaluation |
| `cro-forms` | `/cro forms` | Form optimization |
| `cro-ecommerce` | `/cro ecommerce` | E-commerce CRO |
| `cro-trust` | `/cro trust` | Trust signals and social proof |
| `cro-tracking` | `/cro tracking` | Analytics and tracking |
| `cro-benchmark` | `/cro benchmark` | Competitor comparison |
| `cro-plan` | `/cro plan` | CRO strategy and roadmap |

---

## Subagents (for `/cro audit`)

These 6 agents run **in parallel** during a full audit. Each receives the page
HTML, detected business type, and its specific evaluation brief.

| Subagent | Responsibility | Loads Reference |
|----------|---------------|-----------------|
| `cro-ux` | UX heuristics, navigation, layout, mobile, accessibility | `ux-heuristics.md` |
| `cro-copy` | Headlines, value prop, CTA text, urgency, clarity, readability | `psychology-principles.md` |
| `cro-tracking` | GA4, GTM, Meta Pixel, conversion events, data layer | `quality-gates.md` |
| `cro-visual` | Visual hierarchy, F/Z patterns, whitespace, contrast, CTA prominence | `quality-gates.md` |
| `cro-performance` | Page speed, LCP, CLS, FID, render-blocking resources | `conversion-benchmarks.md` |
| `cro-trust` | Reviews, testimonials, badges, guarantees, security indicators | `psychology-principles.md` |

Each subagent returns:
- Category score (0-100)
- List of findings with priority level
- Top 3 recommendations
- Relevant A/B test hypothesis (if applicable)

---

## Output Format

All CRO reports follow this structure:

```
## CRO [Audit Type]: [URL]

**Business Type:** [Detected type]
**CRO Health Score:** [Score]/100 — [Rating]
**Date:** [Current date]

### Executive Summary
[2-3 sentence overview of key findings]

### Critical Issues
[Bulleted list of Critical-priority items]

### Category Scores
| Category | Score | Rating |
|----------|-------|--------|
| ... | .../100 | ... |

### Detailed Findings
[Grouped by category, each finding with priority tag]

### Recommendations
[Prioritized action items, numbered]

### Quick-Win A/B Tests
[3 test hypotheses using ICE framework]
```
