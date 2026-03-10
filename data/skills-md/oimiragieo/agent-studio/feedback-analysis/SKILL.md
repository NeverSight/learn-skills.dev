---
name: feedback-analysis
description: Customer feedback analysis — sentiment detection, NPS/CSAT frameworks, feature request clustering, support ticket triage, churn signal detection, and feedback-to-roadmap translation
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Bash, WebSearch, WebFetch]
agents:
  - feedback-synthesizer
category: domain-specific
tags: [feedback, sentiment, nps, csat, churn, triage, roadmap, clustering, customer-experience]

verified: false
best_practices:
  - Unify all feedback channels before any analysis (prevents blind spots)
  - Detect mismatch between numerical score and text sentiment
  - Use hierarchical taxonomy for ticket triage (30-50 tags max)
  - Correlate feature requests with churn risk for roadmap prioritization
  - Always produce an actionable output — analysis without action has no value
error_handling: graceful
streaming: supported
---

# Feedback Analysis

## Overview

Customer feedback analysis transforms raw feedback into actionable intelligence across six interconnected capability areas. All capabilities share a common data pipeline: unified multi-channel feedback collection feeds sentiment detection, which powers NPS/CSAT scoring, feature clustering, ticket triage, churn signals, and ultimately roadmap prioritization.

**Six Capability Areas:**

1. **Sentiment Analysis** — Multi-channel emotion detection beyond positive/negative/neutral
2. **NPS/CSAT Frameworks** — Dual-track score + text analysis with mismatch detection
3. **Feature Request Clustering** — Group and prioritize by frequency, emotion, and churn correlation
4. **Support Ticket Triage** — Hierarchical taxonomy-based categorization and routing
5. **Churn Signal Detection** — Behavioral and textual early warning systems
6. **Feedback-to-Roadmap Translation** — Convert clusters to ranked product decisions

## When to Invoke

Invoke `Skill({ skill: 'feedback-analysis' })` when:

- Analyzing customer feedback at scale (>50 items)
- Processing NPS/CSAT survey responses
- Triaging support tickets or classifying issues
- Detecting early churn signals in user behavior or feedback
- Prioritizing the product roadmap from customer requests
- Synthesizing qualitative feedback into actionable themes
- Running feedback campaigns and evaluating results

## The Six-Phase Process

### Phase 1: Multi-Channel Data Unification (MANDATORY FIRST STEP)

**Iron Law**: All analysis degrades without unified data. Single-channel view creates blind spots.

```
Channels to unify:
- In-app surveys (NPS, CSAT, CES)
- Support tickets (Zendesk, Intercom, Freshdesk)
- App store reviews (iOS, Android)
- Social mentions (Twitter/X, Reddit, LinkedIn)
- Chat transcripts (live chat, chatbot logs)
- Product reviews (G2, Capterra, Trustpilot)
- Email responses
```

**Output**: A unified feedback dataset with source, timestamp, channel, user tier, and raw text per item.

### Phase 2: Sentiment Analysis

**Method**: NLP-based multi-dimensional sentiment classification.

**Classifications**:

- **Polarity**: Positive / Negative / Neutral
- **Emotion**: Frustration, Satisfaction, Confusion, Delight, Urgency
- **Intensity**: High / Medium / Low
- **Topic**: Product area, feature, support experience, pricing

**Key Pattern — Mismatch Detection (Critical Insight)**:

> A customer scoring 8 (NPS Passive) with deeply negative text is high churn risk.
> A customer scoring 6 (NPS Detractor) with positive text is recoverable.
> **Mismatch = highest priority segment for intervention.**

```
Mismatch Types:
- High score + negative text → At-risk, intervention needed
- Low score + positive text → Recoverable, reduce friction
- Neutral score + high emotion → Emerging issue, monitor closely
```

**Output**: Sentiment-tagged dataset with polarity, emotion, intensity, and mismatch flags.

### Phase 3: NPS/CSAT Frameworks

**Dual-Track Analysis**: Process numerical scores AND open-text responses in parallel.

**NPS Segments**:

- Promoters (9-10): Surface testimonials, referral triggers
- Passives (7-8): Identify friction points preventing promotion
- Detractors (0-6): Root cause analysis, recovery playbooks

**CSAT Layers**:

- Score distribution by product area, agent, date range, cohort
- Text sentiment correlation with CSAT score
- Trend analysis: rolling averages, anomaly detection on score drops
- Causation analysis: what drove score changes?

**Multi-Dimensional Segmentation**:

```
Dimensions to segment by:
- User tier (free, pro, enterprise)
- Acquisition channel
- Product area (onboarding, core feature, billing, support)
- Agent/team (for support CSAT)
- Cohort (joined date, plan upgrade date)
- Region/language
```

**Output**: NPS/CSAT dashboard data with trend lines, mismatch segments, and causation narratives.

### Phase 4: Feature Request Clustering

**Method**: Group verbatims into themes without manual tagging using pattern detection.

**Clustering Dimensions**:

- **Frequency**: How many users requested this?
- **Emotional Weight**: How strongly do they feel? (high emotion = high priority)
- **Churn Correlation**: Does absence of this feature correlate with churned users?
- **Segment Impact**: Which user tiers/cohorts are most affected?

**Category Taxonomy**:

```
Request Categories:
- Bug Report (broken functionality)
- Feature Gap (missing capability)
- UX Friction (confusing/slow workflow)
- Performance Issue (speed, reliability)
- Integration Request (connect to other tools)
- Pricing Feedback (too expensive, wrong tier)
- Documentation Gap (can't figure out how to use it)
```

**Prioritization Formula**:

```
Priority Score = (Frequency × 0.3) + (Emotion Weight × 0.3) + (Churn Correlation × 0.4)
```

**Output**: Ranked feature request list with evidence count, sentiment weight, and churn correlation per cluster.

### Phase 5: Support Ticket Triage

**Taxonomy Design**: Hierarchical, max 30-50 tags to prevent tag bloat.

**Recommended Taxonomy Structure**:

```
Level 1 (Category):        Level 2 (Subcategory):       Level 3 (Root Cause):
- Technical Issue          - Login/Auth                  - Password reset broken
- Billing                  - Charge dispute              - Double-charged
- Feature Usage            - Onboarding                  - Setup wizard unclear
- Performance              - Slow response               - Database timeout
- Integration              - API error                   - Rate limit exceeded
- Account Management       - Team permissions            - Role not propagating
```

**Triage Modes**:

1. **Rule-based**: Fast pattern matching for obvious categories
2. **AI-powered**: NLP for ambiguous tickets (45% faster routing per Zendesk data)
3. **Human review**: Escalation queue for complex/sensitive cases

**Priority Scoring**:

```
Ticket Priority = Urgency (language cues) + Impact (user tier/revenue) + Sentiment (frustration level)
- P0: Critical + Enterprise user + High frustration
- P1: High urgency + Any paid user + Negative sentiment
- P2: Medium urgency + Any user + Neutral/negative
- P3: Low urgency + Any user + Neutral
```

**Output**: Categorized and prioritized ticket queue with taxonomy assignments and routing rules.

### Phase 6: Churn Signal Detection

**Behavioral Profile Clustering**:

```
User Engagement Profiles:
- Power User: High session frequency, feature breadth, collaborative
- Dabbler: Irregular sessions, single workflow, no integrations
- One-Feature User: Deep single-feature use, no expansion
- Trial Tourist: Onboarding complete, then disengaged
```

**Early Warning Signals (detect BEFORE explicit churn)**:

- Session frequency drop (>50% decrease week-over-week)
- Feature contraction (fewer features used than prior period)
- Support ticket surge (3+ tickets in 2 weeks)
- Negative sentiment spike in recent feedback
- Admin account downgrade events
- Billing inquiry (pricing-related tickets/queries)
- Export activity (data portability requests)

**Churn Risk Scoring**:

```
Churn Risk = (Behavioral signals × 0.4) + (Feedback sentiment × 0.3) + (Support ticket pattern × 0.3)
Risk Tiers:
- High (>0.7): Trigger immediate retention playbook
- Medium (0.4-0.7): Proactive outreach + success check-in
- Low (<0.4): Monitor, standard touchpoints
```

**Reason Code Generation**:
Each high-risk user gets a human-readable reason code:

- "Feature-gap: Missing [X] blocking workflow"
- "Billing: Perceives pricing as misaligned with value"
- "Support: 3 unresolved critical tickets in 14 days"

**Output**: Churn risk cohort with risk scores, reason codes, and triggered playbook recommendations.

### Phase 7: Feedback-to-Roadmap Translation

**Input**: Completed phases 1-6 (sentiment, NPS/CSAT, clusters, triage, churn signals)

**Prioritization Matrix**:

```
Roadmap Score = (Feature Request Frequency × 0.25)
              + (Churn Correlation × 0.35)
              + (NPS Impact × 0.25)
              + (Support Volume × 0.15)
```

**Stakeholder Output Format**:

```markdown
## Roadmap Recommendation: [Feature/Fix Name]

**Evidence Summary**: [N] users requested this across [channels]
**Sentiment**: [Avg. emotional weight and polarity]
**Churn Correlation**: [% of churned users mentioned this]
**NPS Impact**: [Correlation to Detractor-to-Promoter potential]
**Support Impact**: [Ticket volume and priority distribution]

**Recommended Action**: [Implement / Investigate / Defer / Decline]
**Priority Tier**: P0 / P1 / P2 / P3
**Supporting Quotes**: [3-5 verbatim user quotes]
```

**Continuous Loop**: Feed roadmap decisions back into feedback collection ("Did we solve the problem?").

**Output**: Ranked roadmap items with quantitative evidence, stakeholder narrative, and action recommendations.

---

## Iron Laws

1. **ALWAYS unify channels first** — single-channel analysis creates blind spots that lead to wrong prioritization decisions.
2. **ALWAYS run mismatch detection** — numerical scores alone miss high-churn-risk Passives and recoverable Detractors.
3. **ALWAYS produce an actionable output** — analysis that doesn't result in a decision, playbook trigger, or roadmap item has failed its purpose.
4. **NEVER use flat taxonomy with >50 tags** — tag bloat causes inconsistent categorization; use hierarchical taxonomy with 30-50 leaf nodes.
5. **ALWAYS correlate feature requests with churn data** — frequency alone is a poor proxy for priority; churn correlation is the real signal.

## Anti-Patterns

| Anti-Pattern                            | Why It Fails                                                      | Correct Approach                                                       |
| --------------------------------------- | ----------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Analyzing only NPS scores without text  | Misses mismatch segments (fake Promoters, recoverable Detractors) | Always run dual-track score + text analysis                            |
| Flat taxonomy with 200+ ticket tags     | Agents use first matching tag; root cause data is lost            | Hierarchical taxonomy, max 50 leaf nodes                               |
| Clustering by frequency alone           | Missing features that don't come up often but cause 80% of churn  | Weight clusters by churn correlation (0.4 weight)                      |
| Waiting for explicit churn to detect it | Post-churn analysis doesn't save the customer                     | Behavioral early warning signals, 14-day detection horizon             |
| Roadmap items without evidence count    | Stakeholders can't evaluate priority or trade-offs                | Every roadmap item needs: frequency, sentiment weight, churn %, quotes |
| Single-channel feedback collection      | Blind spots by channel; social complaints ≠ support tickets       | Unify all channels before analysis                                     |

## Enforcement Hooks

Input validated against `schemas/input.schema.json` before execution.
Output contract defined in `schemas/output.schema.json`.
Pre-execution hook: `hooks/pre-execute.cjs`
Post-execution hook (observability): `hooks/post-execute.cjs`

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

Check for:

- Previous feedback analysis results
- Known data quality issues in feedback channels
- Prior roadmap decisions from feedback

**After completing:**

- New pattern discovered → `.claude/context/memory/learnings.md`
- Issue found → `.claude/context/memory/issues.md`
- Roadmap decision → `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
