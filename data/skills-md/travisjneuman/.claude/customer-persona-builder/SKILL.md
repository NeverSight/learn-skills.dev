---
name: customer-persona-builder
description: Data-driven customer persona development combining market research, user behavior analysis, and segmentation frameworks. Use when creating buyer personas, ideal customer profiles (ICPs), or user archetypes.
---

# Customer Persona Builder

Structured frameworks for creating data-driven customer personas, ideal customer profiles, and user archetypes.

## Persona vs ICP Distinction

### When to Use Which

```
IDEAL CUSTOMER PROFILE (ICP):
- Company-level / account-level description
- Used by: Sales, marketing (targeting), product (roadmap)
- Answers: "What companies should we sell to?"
- Firmographic: industry, size, revenue, tech stack

BUYER PERSONA:
- Individual-level description
- Used by: Sales (conversations), marketing (messaging), content
- Answers: "Who are the people making buying decisions?"
- Behavioral: goals, pain points, decision process

USER PERSONA:
- End-user description (may differ from buyer)
- Used by: Product, design, engineering
- Answers: "Who uses the product daily?"
- Task-based: workflows, jobs-to-be-done, frustrations

RELATIONSHIP:
ICP (company) contains multiple Buyer Personas (people)
who may differ from User Personas (daily users).
```

## Ideal Customer Profile Template

### ICP Framework

```
IDEAL CUSTOMER PROFILE:

FIRMOGRAPHICS:
- Industry:        [specific verticals]
- Company Size:    [employee range]
- Annual Revenue:  [revenue range]
- Geography:       [regions/countries]
- Growth Stage:    [startup/growth/enterprise]

TECHNOGRAPHICS:
- Current Stack:   [tools they use today]
- Infrastructure:  [cloud, on-prem, hybrid]
- Maturity:        [early adopter, mainstream, laggard]

BUSINESS CHARACTERISTICS:
- Pain Intensity:  [how acute is the problem we solve]
- Budget Authority:[does this level have budget]
- Buying Process:  [simple, committee, procurement]
- Contract Value:  [expected ACV range]

QUALIFYING SIGNALS:
- Positive: [hiring for X role, using Y tool, in Z market]
- Negative: [too small, wrong industry, already solved]

DISQUALIFYING CRITERIA:
- [specific reasons to exclude]
```

### ICP Scoring Matrix

| Attribute | Ideal (5) | Good (3) | Poor (1) | Weight |
| --- | --- | --- | --- | --- |
| Industry | [exact verticals] | [adjacent verticals] | [unrelated] | 20% |
| Company Size | [sweet spot range] | [workable range] | [too small/large] | 15% |
| Pain Intensity | Active seeking solution | Aware of problem | Unaware | 25% |
| Budget | Dedicated budget exists | Can find budget | No budget | 20% |
| Tech Fit | Perfect stack match | Partial overlap | Incompatible | 10% |
| Champion | Identified internal advocate | Potential champion | No access | 10% |

```
SCORING THRESHOLDS:
  4.0-5.0: Tier 1 — pursue aggressively
  3.0-3.9: Tier 2 — pursue selectively
  2.0-2.9: Tier 3 — qualify carefully
  < 2.0:   Disqualify
```

## Buyer Persona Template

### Full Persona Document

```
BUYER PERSONA:

──────────────────────────────────────────────
NAME:   [Representative name, e.g., "Marketing Maria"]
ROLE:   [Title / function]
REPORTS TO: [Their boss's role]
──────────────────────────────────────────────

DEMOGRAPHICS:
- Age Range:      [25-35, 35-45, etc.]
- Education:      [Degree, field]
- Career Stage:   [IC, manager, director, VP, C-level]
- Income Range:   [if relevant to pricing]

PROFESSIONAL CONTEXT:
- Team Size:      [who they manage]
- Budget Authority: [Y/N, amount range]
- KPIs They Own:   [what they're measured on]
- Tools They Use:  [current stack]
- Reports They Read: [information sources]

GOALS (what they're trying to achieve):
1. [Primary business goal]
2. [Secondary business goal]
3. [Personal career goal]

PAIN POINTS (what frustrates them):
1. [Primary pain point]
   Impact: [time, money, reputation]
2. [Secondary pain point]
   Impact: [time, money, reputation]
3. [Tertiary pain point]
   Impact: [time, money, reputation]

BUYING BEHAVIOR:
- Trigger Event:     [what initiates their search]
- Research Process:  [where they look for solutions]
- Decision Criteria: [ranked priorities]
  1. [e.g., ease of use]
  2. [e.g., integration with existing tools]
  3. [e.g., price/value]
  4. [e.g., vendor reputation]
  5. [e.g., implementation speed]
- Decision Timeline: [typical buying cycle length]
- Influencers:       [who else is involved]

OBJECTIONS:
1. [Common objection]
   Root Cause: [underlying concern]
2. [Common objection]
   Root Cause: [underlying concern]

MESSAGING THAT RESONATES:
- Value Prop:   "[specific statement that speaks to their goals]"
- Proof Point:  "[customer story or metric that builds credibility]"
- CTA:          "[appropriate next step for this persona]"

QUOTE:
"[A representative statement capturing their perspective,
  drawn from interviews or synthesized from research]"
```

## Data Sources for Persona Building

### Primary Research Methods

| Method | Best For | Sample Size | Time Investment |
| --- | --- | --- | --- |
| **Customer interviews** | Deep qualitative insights | 10-20 per persona | 2-4 weeks |
| **Sales team interviews** | Patterns from prospect conversations | 5-10 reps | 1 week |
| **Customer success interviews** | Post-purchase behavior, retention drivers | 5-10 CSMs | 1 week |
| **Win/loss analysis** | Decision criteria and competitive dynamics | 15-30 deals | 2-3 weeks |
| **Surveys** | Quantitative validation of qualitative findings | 100-500+ | 2-3 weeks |
| **On-site observation** | Real workflow and context understanding | 5-10 visits | 4-6 weeks |

### Secondary Research Methods

| Source | Data Type | Actionability |
| --- | --- | --- |
| **CRM data** | Firmographics, deal history, conversion rates | High |
| **Product analytics** | Feature usage, engagement patterns, drop-off | High |
| **Support tickets** | Pain points, confusion areas, feature requests | High |
| **G2/Capterra reviews** | Buying criteria, competitor sentiment | Medium |
| **Social media** | Interests, content consumption, influence | Medium |
| **Census / industry data** | Market sizing, demographic baselines | Low-Medium |
| **Job postings** | Role responsibilities, tools, priorities | Medium |

### Interview Question Bank

```
DISCOVERY QUESTIONS (for persona interviews):

ROLE & CONTEXT:
- "Walk me through a typical day in your role."
- "What are the top 3 things you're measured on?"
- "Who do you report to, and what do they care about most?"
- "What tools do you use every day?"

GOALS:
- "What are you trying to accomplish this quarter/year?"
- "What does success look like in your role?"
- "If you could wave a magic wand, what would change?"

PAIN POINTS:
- "What's the most frustrating part of [process we address]?"
- "How do you currently solve [problem we address]?"
- "What have you tried that didn't work?"
- "How much time/money does this problem cost you?"

BUYING BEHAVIOR:
- "When you last evaluated a new tool, how did you start?"
- "Who else was involved in that decision?"
- "What was the single most important factor in your decision?"
- "What almost stopped you from buying?"

INFORMATION SOURCES:
- "Where do you go to learn about new tools or approaches?"
- "Which blogs, podcasts, or communities do you follow?"
- "Whose opinion do you trust most when making decisions?"
```

## Jobs-to-Be-Done Integration

### JTBD Framework for Personas

```
JOB STATEMENT FORMAT:
When [situation/trigger],
I want to [motivation/goal],
so I can [expected outcome].

EXAMPLE:
When I'm preparing the monthly board report,
I want to pull real-time metrics from all our tools,
so I can present accurate data without 4 hours of manual work.

JOB MAP:
1. DEFINE    — What triggers the need?
2. LOCATE    — Where do they search for solutions?
3. PREPARE   — What setup is required?
4. CONFIRM   — How do they validate it works?
5. EXECUTE   — What does actual usage look like?
6. MONITOR   — How do they track ongoing results?
7. MODIFY    — What adjustments happen over time?
8. CONCLUDE  — What does completion look like?
```

### Outcome-Driven Persona Layer

```
FOR EACH PERSONA, MAP:

FUNCTIONAL JOBS:
- [Core task they need to accomplish]
- [Supporting tasks around the core]

EMOTIONAL JOBS:
- [How they want to feel]
- [How they want to be perceived]

SOCIAL JOBS:
- [How they want others to see them]
- [Status or recognition they seek]

RELATED JOBS:
- [Adjacent tasks that affect their success]
- [Upstream/downstream dependencies]
```

## Segmentation Approaches

### Segmentation Decision Matrix

| Approach | Data Needed | Complexity | Actionability |
| --- | --- | --- | --- |
| **Demographic** | CRM / survey data | Low | Medium |
| **Firmographic** | Company data | Low | High (for B2B) |
| **Behavioral** | Product analytics, CRM | Medium | High |
| **Needs-based** | Interviews, surveys | Medium-High | Very High |
| **Value-based** | Revenue, CLV data | Medium | High |
| **Psychographic** | Survey, social data | High | Medium |

### Behavioral Segmentation Template

```
BEHAVIORAL SEGMENTS:

POWER USERS:
- Usage: Daily, multiple features
- Engagement: High (>X sessions/week)
- Value: High CLV, likely to expand
- Strategy: Upsell, advocacy program

REGULAR USERS:
- Usage: Weekly, core features
- Engagement: Moderate
- Value: Stable, predictable revenue
- Strategy: Feature education, expansion

AT-RISK USERS:
- Usage: Declining, sporadic
- Engagement: Low (dropping)
- Value: At risk of churn
- Strategy: Re-engagement, CSM outreach

NEW USERS:
- Usage: Onboarding phase
- Engagement: Variable
- Value: Unknown (measuring)
- Strategy: Guided onboarding, quick wins
```

## Validation and Iteration

### Persona Validation Checklist

| Validation Step | Method | Status |
| --- | --- | --- |
| Based on real data (not assumptions) | Cite sources for each attribute | [ ] |
| Validated with sales team | Sales reps recognize and agree | [ ] |
| Validated with CS team | Matches real customer behavior | [ ] |
| Quantitatively sized | Know how many of each persona exist | [ ] |
| Differentiated | Each persona triggers different actions | [ ] |
| Actionable | Marketing can write copy for each | [ ] |
| Prioritized | Clear tier 1 / tier 2 / tier 3 personas | [ ] |
| Reviewed with product | Product roadmap aligns to persona needs | [ ] |

### Persona Anti-Patterns

```
COMMON PERSONA MISTAKES:

1. OPINION-BASED PERSONAS
   Problem: Built on internal assumptions, not data
   Fix: Ground every attribute in interview/data evidence

2. TOO MANY PERSONAS
   Problem: 8+ personas dilute focus and confuse teams
   Fix: 3-5 primary personas maximum; merge similar ones

3. DEMOGRAPHIC-ONLY PERSONAS
   Problem: "Female, 35-45, suburban" tells you nothing useful
   Fix: Focus on goals, pain points, and buying behavior

4. STATIC PERSONAS
   Problem: Created once and never updated
   Fix: Quarterly review cadence with new data

5. PERSONAS WITHOUT PRIORITY
   Problem: All personas treated equally
   Fix: Rank by revenue potential and market size

6. PERSONA-MESSAGE DISCONNECT
   Problem: Personas exist but messaging ignores them
   Fix: Each persona gets specific value props and content
```

### Iteration Cadence

```
QUARTERLY REVIEW:
- Validate against latest win/loss data
- Check product analytics for behavior shifts
- Interview 3-5 recent customers
- Update pain points and priorities
- Refresh proof points and quotes

ANNUAL REBUILD:
- Full primary research cycle
- Re-validate ICP and persona segments
- Check market shifts and new competitors
- Align with updated company strategy
- Present updated personas to full org
```

## See Also

- [Marketing](../marketing/SKILL.md)
- [Product Management](../product-management/SKILL.md)
- [Sales](../sales/SKILL.md)
- [Data Science](../data-science/SKILL.md)
