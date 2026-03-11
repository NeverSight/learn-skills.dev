---
name: engagement-analyzer
description: Analyze employee engagement survey data to identify trends, prioritize actions, and design targeted interventions
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Engagement Analyzer

> Transform engagement survey data into actionable insights with trend analysis, priority identification, and targeted intervention design.

## When to Use This Skill

- Analyzing survey results
- Identifying engagement drivers
- Prioritizing action areas
- Designing interventions
- Tracking improvement

## Methodology Foundation

Based on **Gallup Q12 framework** and **Qualtrics engagement research**, combining:
- Driver analysis
- Benchmarking
- Action prioritization
- Intervention design

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Analyzes survey data | Survey questions |
| Identifies patterns | Data collection |
| Prioritizes actions | Resource allocation |
| Suggests interventions | Implementation |
| Creates action plans | Executive priorities |

## Instructions

### Step 1: Understand Engagement Model

**Key Engagement Dimensions:**

| Dimension | What It Measures | Example Questions |
|-----------|------------------|-------------------|
| **Purpose** | Connection to mission | "My work has meaning" |
| **Development** | Growth opportunity | "I learn and grow here" |
| **Manager** | Leadership quality | "My manager supports me" |
| **Team** | Collaboration | "My team works well together" |
| **Wellbeing** | Work-life balance | "I can manage my workload" |
| **Recognition** | Appreciation | "I feel valued for my contributions" |

### Step 2: Analyze Results

**Analysis Framework:**

| Metric | Calculation | Interpretation |
|--------|-------------|----------------|
| Overall Score | Average of all items | Health indicator |
| Favorability | % Agree + Strongly Agree | Positive sentiment |
| eNPS | Promoters - Detractors | Loyalty indicator |
| Participation | Responses / Invited | Data reliability |

**Comparison Points:**
- Previous survey (trend)
- Company benchmark
- Industry benchmark
- Team vs. company

### Step 3: Identify Priorities

**Priority Matrix:**

| Score | Impact | Priority |
|-------|--------|----------|
| Low | High | P1 - Critical |
| Low | Medium | P2 - Important |
| Low | Low | P3 - Monitor |
| High | Any | Maintain |

### Step 4: Design Interventions

**Intervention Types:**

| Level | Examples | Timeline |
|-------|----------|----------|
| Quick Wins | Recognition, communication | 0-30 days |
| Process Changes | Meeting structure, feedback | 30-90 days |
| Structural Changes | Role design, team structure | 90+ days |
| Culture Shifts | Values, behaviors | 6+ months |

### Step 5: Create Action Plan

**Plan Components:**
1. Priority area
2. Root cause hypothesis
3. Proposed intervention
4. Success metrics
5. Owner and timeline

## Examples

### Example 1: Full Engagement Analysis

**Input:**
```
Analyze these engagement survey results:

Company Overall: 72 (was 68)
Participation: 85%

By Dimension (favorability %):
- Purpose: 82%
- Development: 58%
- Manager: 71%
- Team: 76%
- Wellbeing: 54%
- Recognition: 65%

Engineering Dept: 64 overall
- Development: 45%
- Wellbeing: 42%

Sales Dept: 78 overall
- Recognition: 52%
```

**Output:**
```
## Employee Engagement Analysis

### Executive Summary

**Overall Health:** Improving (+4 points to 72)
**Key Wins:** Purpose (82%), Team (76%)
**Critical Areas:** Wellbeing (54%), Development (58%)
**Hot Spots:** Engineering (64 overall), Sales Recognition (52%)

---

### Overall Results

| Metric | Score | vs. Last | vs. Benchmark |
|--------|-------|----------|---------------|
| Overall Score | 72 | +4 | +2 |
| Participation | 85% | +3% | +10% |
| eNPS | +18 | +6 | +8 |

**Interpretation:** Solid improvement across the board. High participation
indicates employees feel their voice matters.

---

### Dimension Analysis

| Dimension | Score | Trend | Priority |
|-----------|-------|-------|----------|
| Purpose | 82% | → | Maintain |
| Team | 76% | ↑ | Maintain |
| Manager | 71% | ↑ | Improve |
| Recognition | 65% | → | Improve |
| Development | 58% | ↓ | Critical |
| Wellbeing | 54% | ↓ | Critical |

---

### Priority Matrix

```
                    HIGH IMPACT
                         │
    ┌────────────────────┼────────────────────┐
    │   P1: CRITICAL     │   MAINTAIN         │
    │   • Wellbeing      │   • Purpose        │
    │   • Development    │   • Team           │
LOW ├────────────────────┼────────────────────┤ HIGH
SCORE│   P2: IMPORTANT   │   LEVERAGE         │
    │   • Recognition    │                    │
    │   • Manager        │                    │
    └────────────────────┴────────────────────┘
                    LOW IMPACT
```

---

### Department Deep Dive

#### Engineering (64 Overall) - NEEDS ATTENTION

| Dimension | Engineering | Company | Gap |
|-----------|-------------|---------|-----|
| Development | 45% | 58% | -13 |
| Wellbeing | 42% | 54% | -12 |

**Root Cause Hypotheses:**
1. Technical debt creating burnout
2. Limited career progression paths
3. On-call burden distributed unevenly

**Recommended Actions:**
| Action | Owner | Timeline |
|--------|-------|----------|
| Engineering career ladder review | VP Eng + HR | 90 days |
| On-call rotation audit | Eng Managers | 30 days |
| 20% learning time policy | VP Eng | 60 days |

---

### Company-Wide Action Plan

#### P1: Wellbeing Initiative (54%)

**Target:** Increase to 65% by next survey

**Actions:**
| Action | Owner | Timeline |
|--------|-------|----------|
| "No Meeting Fridays" pilot | Leadership | 30 days |
| Workload survey by department | HRBP | 30 days |
| Manager training: sustainable teams | L&D | 90 days |

---

#### P1: Development Initiative (58%)

**Target:** Increase to 70% by next survey

**Actions:**
| Action | Owner | Timeline |
|--------|-------|----------|
| Learning stipend communication | HR | 30 days |
| Career pathing by function | HR + Leaders | 90 days |
| Mentorship program launch | L&D | 90 days |

---

### Success Metrics

| Area | Current | 6-Month Target | Owner |
|------|---------|----------------|-------|
| Overall Score | 72 | 76 | CHRO |
| Wellbeing | 54% | 65% | HR |
| Development | 58% | 70% | L&D |
| Engineering Overall | 64 | 72 | VP Eng |
```

### Example 2: Quick Pulse Analysis

**Input:**
```
Analyze this pulse survey (3 questions):
1. "I would recommend this company" - 62% favorable (down 8%)
2. "I have what I need to do my job" - 71% favorable (up 3%)
3. "I feel valued" - 48% favorable (down 12%)
```

**Output:**
```
## Pulse Survey Quick Analysis

### Summary

| Metric | Current | Change | Status |
|--------|---------|--------|--------|
| eNPS Indicator | 62% | ↓ 8% | WARNING |
| Enablement | 71% | ↑ 3% | GOOD |
| Recognition | 48% | ↓ 12% | CRITICAL |

---

### Key Finding

**Recognition is in crisis** - 12-point drop is a red flag.
This is likely driving the eNPS decline.

---

### Immediate Actions

| Priority | Action | Owner | Timeline |
|----------|--------|-------|----------|
| 1 | Leadership acknowledgment | CEO | This week |
| 2 | Manager recognition training | HR | 2 weeks |
| 3 | Focus groups on "valued" | HRBP | 2 weeks |
```

## Skill Boundaries

### What This Skill Does Well
- Analyzing survey patterns
- Prioritizing action areas
- Designing interventions
- Creating action plans

### What This Skill Cannot Do
- Access actual survey data
- Know company-specific context
- Replace qualitative research
- Guarantee improvement

## Iteration Guide

**Follow-up Prompts:**
- "Create focus group questions for [area]"
- "Design intervention for [specific issue]"
- "How do we communicate results to [audience]?"
- "What metrics should we track for [initiative]?"

## References

- Gallup Q12 Engagement Framework
- Qualtrics Employee Experience
- Culture Amp Engagement Drivers
- Glint People Science

## Related Skills

- `employee-support` - Ongoing support
- `onboarding-guide` - Initial engagement
- `churn-prediction` - Turnover risk

## Skill Metadata

- **Domain**: HR Operations
- **Complexity**: Intermediate-Advanced
- **Mode**: centaur
- **Time to Value**: 2-4 hours per analysis
- **Prerequisites**: Survey data, company context
