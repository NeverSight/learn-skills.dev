---
name: marketing-automation
description: Generate marketing deliverables across CRO, copywriting, SEO, analytics, and growth using 23 specialized sub-skills with clear objectives, constraints, and validation.
metadata:
  tags: marketing, cro, copywriting, seo, analytics, growth, automation
  platforms: Claude, ChatGPT, Gemini, Codex
---


# Marketing Skills Collection

A collection of 23 sub-skills for marketing deliverables. Generates repeatable, high-quality outputs across CRO, copywriting, SEO, analytics, and growth.

## When to use this skill

- **Marketing Deliverables Needed**: CRO, copy, SEO, analytics, growth outputs
- **Repeatable High-Quality Outputs**: Generate assets tuned to a single KPI
- **Business Goal → Skill Mapping**: Convert goals to specific marketing sub-skills

---

## 23 Sub-Skills Overview

### CRO (Conversion Rate Optimization)
| Sub-Skill | Description |
|-----------|-------------|
| `page-cro` | Landing page conversion rate optimization |
| `signup-flow` | Signup flow optimization |
| `onboarding` | Onboarding experience improvement |
| `form-optimization` | Form optimization (fields, UX) |
| `paywall` | Paywall/pricing page optimization |

### Copywriting
| Sub-Skill | Description |
|-----------|-------------|
| `copywriting` | Ad/marketing copy writing |
| `copy-editing` | Improve existing copy |
| `email-sequence` | Email sequence design |
| `social-content` | Social media content |

### SEO
| Sub-Skill | Description |
|-----------|-------------|
| `seo-audit` | SEO audit and improvements |
| `programmatic-seo` | Programmatic SEO pages |
| `comparison-page` | Comparison page writing |
| `schema-markup` | Structured data markup |

### Ads & Analytics
| Sub-Skill | Description |
|-----------|-------------|
| `analytics-tracking` | Analytics tracking setup |
| `paid-ads` | Paid ads strategy/copy |
| `ab-test` | A/B test design |

### Strategy & Growth
| Sub-Skill | Description |
|-----------|-------------|
| `launch-strategy` | Product launch strategy |
| `pricing-strategy` | Pricing strategy |
| `retention` | Retention improvement strategy |
| `churn-analysis` | Churn analysis |
| `growth-experiments` | Growth experiment design |
| `referral-program` | Referral program design |
| `content-strategy` | Content strategy |

---

## Instructions

### Step 1: Define Objective and Constraints

```yaml
marketing_brief:
  objective: [single KPI - conversion rate, CTR, activation]
  target_audience:
    segment: [customer segment]
    pain_points: [key pain points]
    terminology: [terms they use]
  channel: [LP, email, social, SEO, ads]
  format: [format]
  offer:
    value_prop: [value proposition]
    positioning: [positioning]
    proof_points: [proof points]
```

### Step 2: Select the Sub-Skill

Select the appropriate sub-skill for the situation:

```bash
# When CRO is needed
→ page-cro, signup-flow, onboarding, form-optimization, paywall

# When copy is needed
→ copywriting, copy-editing, email-sequence, social-content

# When SEO is needed
→ seo-audit, programmatic-seo, comparison-page, schema-markup

# When ads/analytics are needed
→ analytics-tracking, paid-ads, ab-test

# When strategy/growth is needed
→ launch-strategy, pricing-strategy, retention, churn-analysis, growth-experiments
```

### Step 3: Build the Prompt

Build structured prompt:

```markdown
## Marketing Asset Request

### Product Context
- **Product**: [product name]
- **Category**: [category]
- **Stage**: [stage - early, growth, mature]

### Audience
- **Segment**: [target segment]
- **Pain Points**: [1-3 pain points]
- **Current State**: [solution they currently use]

### Offer
- **Value Prop**: [core value proposition]
- **Differentiator**: [differentiation point]
- **Proof**: [trust elements - numbers, clients, awards]

### Constraints
- **Tone**: [tone - professional, casual, bold]
- **Brand Voice**: [brand voice guide]
- **Do NOT**: [things to avoid]

### Output Format
- [desired format - table, checklist, bullets]
```

### Step 4: Generate and Validate

```bash
# Generate
claude task "generate marketing asset with sub-skill name"

# Validation checklist
- [ ] KPI alignment
- [ ] Target audience fit
- [ ] Brand voice consistency
- [ ] Actionability
```

### Step 5: Handoff + Measurement

```markdown
## Implementation Checklist
- [ ] Asset publishing
- [ ] Tracking event setup
- [ ] Success threshold definition

## Tracking Events
| Event | Description | Success Threshold |
|-------|-------------|-------------------|
| page_view | Page view | baseline |
| cta_click | CTA click | +20% vs control |
| signup_complete | Signup complete | +15% vs control |

## A/B Test Proposals
1. [Hypothesis 1]: [variant] vs [control]
2. [Hypothesis 2]: [variant] vs [control]
```

---

## Examples

### Example 1: Landing Page CRO

**Prompt**:
```
Optimize the landing page for higher signup conversion.
Audience: indie founders building side projects.
Offer: AI co-pilot for product launches.
Output: prioritized CRO changes + A/B tests.
```

**Expected output**:
- CRO checklist prioritized by impact/effort
- 3 A/B test hypotheses with expected lift
- Hero + CTA copy suggestions (3 variants each)

### Example 2: Email Sequence

**Prompt**:
```
Create a 5-email welcome sequence for a B2B SaaS.
Audience: ops managers at 50-500 employee companies.
Goal: drive first workflow setup within 7 days.
```

**Expected output**:
```markdown
## Welcome Sequence

### Email 1: Welcome (Day 0)
- **Subject**: Welcome to [Product] - Let's get started
- **Goal**: Account confirmation + quick win
- **CTA**: Complete profile

### Email 2: Value Demo (Day 1)
- **Subject**: See what [Product] can do in 2 minutes
- **Goal**: Feature awareness
- **CTA**: Watch demo video

### Email 3: First Workflow (Day 3)
- **Subject**: Create your first workflow (step-by-step)
- **Goal**: Activation milestone
- **CTA**: Create workflow

### Email 4: Use Case (Day 5)
- **Subject**: How [Customer] saved 10 hours/week
- **Goal**: Social proof + inspiration
- **CTA**: Try this template

### Email 5: Check-in (Day 7)
- **Subject**: Need help getting started?
- **Goal**: Rescue non-activated users
- **CTA**: Book a call / Reply for help

## Metrics
| Email | Open Rate Target | CTR Target |
|-------|------------------|------------|
| Email 1 | 60%+ | 30%+ |
| Email 2 | 45%+ | 15%+ |
| Email 3 | 40%+ | 20%+ |
| Email 4 | 35%+ | 12%+ |
| Email 5 | 40%+ | 15%+ |
```

### Example 3: Programmatic SEO

**Prompt**:
```
Create a programmatic SEO template for comparison pages.
Target: "[Tool A] vs [Tool B]" searches.
Include: H1, meta description, comparison table, CTA.
```

**Expected output**:
- Page template with placeholders
- Schema markup (JSON-LD)
- Internal linking strategy
- Content guidelines per section

---

## Best practices

1. **One KPI per deliverable**: Avoid mixed objectives
2. **Audience specificity**: Use segment-specific needs and terminology
3. **Instrument measurement**: Set up tracking before launch
4. **Iterate with data**: Treat outputs as hypotheses

---

## Common pitfalls

- **Mixed Objectives**: Multiple goals in one asset
- **Missing Audience Context**: Unclear who it's for
- **No Tracking/Validation Plan**: Unable to measure impact

---

## Troubleshooting

### Issue: Output is generic
**Cause**: Vague product/audience information
**Solution**: Provide positioning, competitors, proof points

### Issue: Output conflicts with brand voice
**Cause**: No tone/voice constraints
**Solution**: Provide brand do/don't list and sample copy

### Issue: Can't measure impact
**Cause**: Tracking events not defined
**Solution**: Define events and success thresholds in advance

---

## Output format

```markdown
## Marketing Asset Report

### Brief Summary
- **Sub-Skill Used**: [sub-skill]
- **Objective**: [KPI]
- **Audience**: [segment]

### Deliverable
[generated asset]

### Implementation Checklist
- [ ] Asset ready
- [ ] Tracking configured
- [ ] Success criteria defined

### A/B Test Plan
| Test | Hypothesis | Metric | Expected Lift |
|------|------------|--------|---------------|
| Test A | [hypothesis] | [metric] | [%] |
```

---

## Multi-Agent Workflow

### Validation & Retrospectives

- **Round 1 (Orchestrator)**: Coverage of 23 sub-skills across 5 categories
- **Round 2 (Analyst)**: KPI alignment, prompt structure review
- **Round 3 (Executor)**: Output format, actionability check

### Agent Roles

| Agent | Role |
|-------|------|
| Claude | Brief composition, asset generation |
| Gemini | Competitor research, trend analysis |
| Codex | Tracking code generation, automation |

---

## Metadata

### Version
- **Current Version**: 1.0.0
- **Last Updated**: 2026-01-21
- **Compatible Platforms**: Claude, ChatGPT, Gemini, Codex

### Related Skills
- [presentation-builder](../../documentation/presentation-builder/SKILL.md)
- [frontend-design](../../frontend/design-system/SKILL.md)
- [image-generation](../../creative-media/image-generation/SKILL.md)

### Tags
`#marketing` `#cro` `#copywriting` `#seo` `#analytics` `#growth` `#automation`
