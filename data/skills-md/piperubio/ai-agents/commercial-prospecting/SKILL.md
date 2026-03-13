---
name: commercial-prospecting
description: >
  Research and profile prospective B2B clients for technology consulting
  services (Software, Data, AI). Assess Ideal Client Profile (ICP) fit,
  evaluate technology maturity, and score lead quality. Use when the
  commercial pipeline needs new qualified prospects, when researching a
  specific company, or when building a target account list for outreach
  campaigns.
---

# Commercial Prospecting

## Purpose

- Research companies and individuals to build qualified prospect profiles for technology consulting services.
- Assess fit against ICP criteria, evaluate tech maturity across Software/Data/AI axes, and produce actionable intelligence for outreach.

## Scope

- This skill WILL:
  - Research and compile company intelligence from available sources
  - Assess technology maturity across Software, Data, and AI axes
  - Score ICP fit with dimension-level breakdown
  - Identify key contacts and likely pain points
  - Recommend approach angles (service line, lead pain)
  - Surface competitive landscape signals
  - Update the commercial pipeline state

- This skill WILL NOT:
  - Draft outreach messages or sequences
  - Conduct discovery calls or meeting preparation
  - Negotiate or make pricing decisions
  - Fabricate or assume company data

## Inputs

- **commercial-state.md** — current pipeline state.
- **user_input** — company name, industry, or target criteria.
- Optional: company website URL, LinkedIn profile, existing intel.

## Workflow

### 1. Company Research

- Gather publicly available information: industry, employee count, revenue range, geography, founding year.
- Identify digital presence signals: website technology, tech job postings, public repositories, engineering blog, conference participation.
- Note recent events: funding rounds, M&A activity, leadership changes, digital transformation announcements.

### 2. Tech Maturity Assessment

Score the company on three axes using a 1-5 scale:

| Score | Level | Description |
|-------|-------|-------------|
| 1 | Ad-hoc/None | No formal practices |
| 2 | Emerging | Some awareness, initial efforts |
| 3 | Defined | Structured processes, some tooling |
| 4 | Managed | Metrics-driven, good practices |
| 5 | Optimized | Industry-leading, continuous improvement |

Axes:
- **Software**: Development practices, architecture, DevOps, deployment maturity.
- **Data**: Data infrastructure, governance, analytics capability, self-service BI.
- **AI**: ML in production, data science team, AI strategy, experimentation infrastructure.

The sweet spot for consulting is companies scoring 2-3. Companies at 1 lack readiness; companies at 5 rarely need external help.

Each score MUST include evidence or justification.

### 3. ICP Scoring

Score against six dimensions (total 0-100). See [references/icp-framework.md](references/icp-framework.md) for the full scoring rubric.

| Dimension | Max Points |
|-----------|------------|
| Company size & budget capacity | 20 |
| Technology maturity gap | 25 |
| Industry alignment | 15 |
| Decision-making accessibility | 15 |
| Growth trajectory | 15 |
| Cultural fit for consulting | 10 |
| **Total** | **100** |

Show dimension breakdown, not just total.

### 4. Contact Identification

- Identify key decision makers and influencers (name, role).
- Map likely pain points per contact based on role and company context.

### 5. Approach Recommendation

- Determine which service line to lead with (Software Engineering, Data Engineering, AI/ML).
- Identify which pain point to open with.
- Note competitive landscape: who else might be pitching this company.
- Do NOT recommend approach without sufficient intel — flag gaps instead.

## Outputs

### 1. New File: `prospect-profile.md`

```markdown
# Prospect Profile: {Company Name}

## Company Overview
- **Industry**:
- **Size**: employees / revenue range
- **Geography**:
- **Website**:

## Tech Maturity Assessment
| Axis | Score (1-5) | Justification |
|------|-------------|---------------|
| Software | | |
| Data | | |
| AI | | |

## ICP Fit Score
| Dimension | Max | Score | Justification |
|-----------|-----|-------|---------------|
| Company size & budget capacity | 20 | | |
| Technology maturity gap | 25 | | |
| Industry alignment | 15 | | |
| Decision-making accessibility | 15 | | |
| Growth trajectory | 15 | | |
| Cultural fit for consulting | 10 | | |
| **Total** | **100** | **XX** | |

**Tier**: 1 / 2 / 3 / 4

## Key Contacts
| Name | Role | Likely Pain Points |
|------|------|--------------------|
| | | |

## Recommended Approach
- **Lead service line**:
- **Lead pain point**:
- **Competitive landscape**:

## Data Freshness
- Research date: YYYY-MM-DD
- Sources: [list]
- Gaps: [list unknowns]
```

### 2. Updated: `commercial-state.md`

Add or update entry in the Account Intelligence section with prospect tier, ICP score, and recommended next action.

## Guardrails

1. Never fabricate company data — mark unknowns explicitly as `[Unknown]` or `[Estimated]`.
2. Tech maturity assessment must include evidence/justification for each score.
3. ICP score must show dimension breakdown, not just a total.
4. Do not recommend outreach approach without sufficient intel — flag gaps instead.
5. Flag when prospect data is stale (>90 days from research date).

## Example

**Input**: "Research LogiTrack Solutions for our pipeline. Mid-market logistics company, ~400 employees, based in Bogotá."

**Output** (excerpt):

```markdown
# Prospect Profile: LogiTrack Solutions

## Company Overview
- **Industry**: Logistics & Supply Chain
- **Size**: ~400 employees / estimated USD $30-50M revenue
- **Geography**: Bogotá, Colombia
- **Website**: [Unknown]

## Tech Maturity Assessment
| Axis | Score (1-5) | Justification |
|------|-------------|---------------|
| Software | 2 | Job postings show legacy Java/.NET stack, no CI/CD mentions |
| Data | 2 | Uses Excel-based reporting, no dedicated data team |
| AI | 1 | No AI/ML roles or initiatives identified |

## ICP Fit Score
| Dimension | Max | Score | Justification |
|-----------|-----|-------|---------------|
| Company size & budget capacity | 20 | 16 | 400 employees, mid-market — strong fit |
| Technology maturity gap | 25 | 22 | Scores 2/2/1 — high need, sufficient baseline |
| Industry alignment | 15 | 12 | Logistics has strong consulting demand |
| Decision-making accessibility | 15 | 10 | Mid-market, likely reachable CTO |
| Growth trajectory | 15 | 9 | [Estimated] stable growth in LatAm logistics |
| Cultural fit for consulting | 10 | 7 | Mid-market LatAm companies generally open to consulting |
| **Total** | **100** | **76** | |

**Tier**: 2 (Standard)

## Key Contacts
| Name | Role | Likely Pain Points |
|------|------|--------------------|
| [Unknown] | CTO / VP Engineering | Legacy modernization, scaling challenges |
| [Unknown] | COO | Operational visibility, route optimization |

## Recommended Approach
- **Lead service line**: Data Engineering
- **Lead pain point**: Lack of operational visibility — Excel-based reporting limits decision speed
- **Competitive landscape**: [Unknown] — research needed

## Data Freshness
- Research date: 2026-02-20
- Sources: Job postings, industry reports
- Gaps: Website, revenue confirmation, org chart, competitive landscape
```
