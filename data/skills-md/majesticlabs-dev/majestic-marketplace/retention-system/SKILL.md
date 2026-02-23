---
name: retention-system
description: Design customer retention systems with health scoring, churn prediction, and proactive engagement workflows. Use when reducing churn or maximizing LTV.
allowed-tools: Read Write Edit Grep Glob WebSearch WebFetch AskUserQuestion
disable-model-invocation: true
---

# Customer Retention System Designer

## Conversation Starter

Use `AskUserQuestion` to gather initial context. Begin by asking:

"I'll help you design a customer retention system that reduces churn and maximizes lifetime value.

Please provide:
1. **Business Model**: What do you sell? (SaaS, subscription, service, product)
2. **Pricing**: What's your pricing structure? (monthly, annual, tiers)
3. **Current Churn**: What's your monthly/annual churn rate?
4. **Customer Journey**: How long is typical customer relationship?
5. **Team Structure**: Do you have customer success? Support?
6. **Data Available**: What customer behavior data can you track?"

## Research Methodology

Use WebSearch to find:
- Industry-specific churn benchmarks
- Customer health score models
- Onboarding best practices
- Churn prediction methodologies
- NPS and CSAT benchmarks

## Strategy Framework

### 1. Customer Lifecycle Stages

| Stage | Entry Criteria | Success Criteria |
|-------|----------------|------------------|
| Acquisition | Account created | First login |
| Activation | First login | Aha moment achieved |
| Engagement | Activated | Regular usage |
| Expansion | Engaged 90+ days | Upsell/cross-sell |
| Advocacy | Expanded OR high NPS | Referral made |
| At-Risk | Warning signals | Re-engaged |
| Churned | Cancelled/lapsed | Win-back sequence |

### 2. Health Score Model

**Score Components (100 points):**

| Category | Weight | Metrics |
|----------|--------|---------|
| Product Usage | 40% | Login frequency, feature adoption, depth of use |
| Engagement | 25% | Email opens, support tickets, event attendance |
| Relationship | 20% | NPS score, CSM interactions, executive sponsor |
| Business Health | 15% | Payment history, growth rate, expansion potential |

**Health Bands:**

| Score | Status | Action |
|-------|--------|--------|
| 80-100 | Healthy (Green) | Monitor, expansion focus |
| 60-79 | Stable (Yellow) | Proactive engagement |
| 40-59 | At-Risk (Orange) | Intervention required |
| 0-39 | Critical (Red) | Immediate escalation |

See [references/playbooks.md](references/playbooks.md) for detailed scoring criteria.

### 3. Onboarding System

| Day | Goal | Touchpoints |
|-----|------|-------------|
| 1 | First value realization | Welcome email, in-app tutorial, quick win |
| 2-3 | Core setup complete | Setup reminder, CSM intro (high-touch) |
| 7 | Confirm activation | Progress email, feature highlight, check-in call |
| 14 | Habit formation | Use case email, advanced feature intro |
| 30 | First month success | NPS survey, success celebration, QBR (enterprise) |
| 60 | Expansion readiness | ROI report, feature teaser |
| 90 | Renewal prep | Renewal reminder, success summary, renewal call |

### 4. Early Warning Signals

**Usage-Based:**
| Signal | Threshold | Risk |
|--------|-----------|------|
| Login drop | >50% vs prior month | High |
| Feature abandonment | Core feature unused 14+ days | High |
| User count drop | Team members removed | Critical |

**Engagement-Based:**
| Signal | Threshold | Risk |
|--------|-----------|------|
| Email silence | No opens 30 days | Medium |
| Support spike | 3+ tickets in 7 days | Medium |
| NPS decline | Dropped 2+ points | High |

**Business-Based:**
| Signal | Threshold | Risk |
|--------|-----------|------|
| Payment failed | Any failed charge | Critical |
| Downgrade request | Any inquiry | High |
| Competitor mention | In support/conversation | Critical |

### 5. Intervention Playbooks

See [references/playbooks.md](references/playbooks.md) for detailed playbooks:
- Usage Decline (14-day sequence)
- Support Escalation (72-hour response)
- Competitor Threat (48-hour response)
- Payment Failure (30-day dunning)
- Renewal Risk (90-day cycle)

### 6. Retention Metrics

**Primary KPIs:**

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| Gross Revenue Retention | (Start MRR - Churn) / Start | 85-95% |
| Net Revenue Retention | (Start + Expansion - Churn) / Start | 100-120% |
| Logo Churn Rate | Churned / Starting | 3-7%/year |
| Customer LTV | ARPU × (1 / Monthly Churn) | Varies |

**Health Metrics:**

| Metric | Target |
|--------|--------|
| Healthy accounts (>80 score) | >60% |
| At-risk accounts (<60 score) | <15% |
| NPS | >50 |
| CSAT | >85% |
| DAU/MAU | >20% |
| Activation rate | >80% |

## Output Format

```markdown
# RETENTION SYSTEM BLUEPRINT: [Business Name]

## Executive Summary
[2-3 sentences on churn situation and approach]

## Customer Lifecycle Map
[Stages with criteria]

## Health Score Model
[Customized scoring framework]

## Onboarding System
[Day-by-day touchpoints]

## Early Warning System
[Signals and thresholds]

## Intervention Playbooks
[Playbooks for each risk type]

## Success Tier Model
[Tier definitions and engagement]

## Metrics Dashboard
[KPIs and tracking setup]

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [ ] Define health score components
- [ ] Set up tracking infrastructure

### Phase 2: Onboarding (Weeks 3-4)
- [ ] Build onboarding sequence
- [ ] Create activation metrics

### Phase 3: Monitoring (Weeks 5-6)
- [ ] Deploy health scoring
- [ ] Set up early warning alerts

### Phase 4: Optimization (Ongoing)
- [ ] Weekly metrics review
- [ ] Playbook effectiveness analysis
```

## Quality Standards

- **Research-driven**: Use WebSearch for industry benchmarks
- **Customized scoring**: Adjust weights based on business model
- **Actionable playbooks**: Clear triggers and specific actions
- **Measurable outcomes**: Every recommendation tied to metrics
- **Scalable design**: Works at current size and 10x scale
