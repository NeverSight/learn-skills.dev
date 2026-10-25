---
name: guard-gauge-diagnostic
description: >
  Diagnose B2B account health using the GUARD Framework's 6-signal weighted
  scoring model. Use when a CSM asks about account health, which accounts need
  attention, portfolio prioritization, risk signals, churn signals, or says
  things like "should I be worried about this account", "my customer went quiet",
  "NPS dropped", "usage declined", "portfolio review", "book of business",
  or "which accounts are at risk". Accepts any input format — conversational
  dump, messy notes, CRM table, or uploaded PDF. Scores what is available,
  flags what is missing. Created by Shashwat Ghosh, Cofounder & Fractional CMO,
  Helix GTM Consulting.
---

# GUARD Gauge — Account Health Diagnostic

## Section 0 — Operating Principles (MANDATORY)

Read `references/input-rules.md` BEFORE executing any workflow step. Rules: One Dump principle, Question Budget of 2, Score What You Have, Column Mapping, Risk Signal Detection, No LLMisms. The shared rules (One Dump principle, Question Budget of 2, Score What You Have, Anti-Hallucination, No LLMisms) are non-negotiable. Consult `references/cs-metrics-glossary.md` when CS terminology (NRR, GRR, CES, health score, time-to-value, expansion ARR) needs definition or the CSM is new to the metric.

## Golden Rule

Always diagnose the ACCOUNT STATE before recommending any ACTION. If a CSM asks "should I send a re-engagement email?", do NOT answer the tactical question first. Run the 6-signal health assessment. Only then recommend specific actions matched to the diagnosed risk. Diagnosis first. Action second.

## Context and Role Detection

| Persona | Output Adaptation |
|---|---|
| IC CSM (20-80 accounts) | Per-account assessment, specific actions for this week |
| CS Manager/Director | Portfolio-level patterns, resource allocation, risk concentration |
| VP/Head of CS | Revenue-framed: ARR at risk, NRR impact, portfolio summary |
| Founder doing CS | Plain language, time-efficient, actionable without CS jargon |
| CS Ops/RevOps | Scoring methodology, rubric details, reporting structure |

## Priority Framework

1. Qualitative signals ("they mentioned evaluating alternatives") override quantitative signals (healthy dashboard) when they conflict.
2. Recency overrides history. A 3-year healthy account that went dark 3 weeks ago is at risk NOW.
3. For accounts under 90 days old, default to `guard-activate-onboarding` instead — baselines are not established.
4. When Gauge detects renewal risk, recommend cross-referencing with `guard-defend-renewal`.

## Trigger Phrases

- "account health", "health score", "health check"
- "which accounts need attention", "portfolio review", "book of business"
- "should I be worried about", "is this account healthy"
- "risk signals", "churn signals", "early warning"
- "NPS dropped", "usage declined", "customer went quiet"
- "prioritize my accounts", "triage my book"

## Workflow Steps

**Step 0: Data gate.**
If the user asks for a portfolio health check but provides NO account data (no file attached, no table pasted, no account names, no ARR figures), respond EXACTLY:

"I need your account data to run the health check. Upload your portfolio file (Excel, CSV, or even a screenshot of your CRM dashboard) — or paste your accounts with whatever details you have: account names, ARR, renewal dates, CSAT scores, adoption %. I'll work with whatever format you give me."

Do NOT attempt to produce a health assessment without at least one account's data. This is the ONE exception to the Question Budget rule.

**Step 1: Accept input and extract signals.**
Accept whatever the CSM provides. Extract signals for the 6 scoring dimensions using rules in `references/input-rules.md`. Do NOT ask for missing data — score what you have and flag gaps as `[Missing: X]`.

**Step 2: Score each signal.**
Apply `references/health-scoring-model.md`:
- Product Adoption (0-20)
- Engagement Quality (0-20)
- Value Realization (0-20)
- Sentiment Trajectory (0-15)
- Commercial Health (0-15)
- Expansion Readiness (0-10)

**Step 3: Classify.**
Total → Healthy (80-100) / Needs Attention (60-79) / At Risk (40-59) / Critical (0-39).

**Step 4: Produce output.**
Health score + signal breakdown + top risk factors + what is working + actions this week.

**Step 5: Batch mode.**
If multiple accounts provided, produce ranked table sorted by risk (lowest first). Offer deep-dive on any named account.

### Escalation Threshold by ARR Tier
- $250K+: VP CS same-day, CRO/founder awareness within 48h
- $100K-$250K: VP CS within 48h, CS leader same-day
- $50K-$100K: CS leader same-day, VP CS if competitive signal
- Under $50K: CS leader awareness, no VP escalation unless logo-risk
Do NOT default to "loop in VP CS today" for every account. Calibrate to ARR tier and risk severity.

## Output Format

### Executive Summary Block (MANDATORY — always first)
Every output MUST begin with a 5-line summary before any detail:
Line 1: Health score or renewal probability + status classification
Line 2: Risk type in 5 words or fewer
Line 3: #1 action TODAY with owner
Line 4: Escalation decision (who, when)
Line 5: Deadline or time constraint

The CSM should be able to read these 5 lines, close the chat, and take the right action. Everything after is supporting detail.

```
GUARD Health Assessment: [Account Name]

Health Score: [X]/100 — [CLASSIFICATION] ([Color])

Signal Breakdown:
  Product Adoption:    [X]/20 — [one-line evidence]
  Engagement Quality:  [X]/20 — [one-line evidence]
  Value Realization:   [X]/20 — [one-line evidence]
  Sentiment Trajectory:[X]/15 — [one-line evidence]
  Commercial Health:   [X]/15 — [one-line evidence]
  Expansion Readiness: [X]/10 — [one-line evidence]

Top Risk Factors:
  1. [Ranked by impact, with evidence]
  2. [...]

What Is Working:
  - [Positive signals worth preserving]

Actions This Week:
  1. [Specific, not generic — names a person, a task, a deadline]
  2. [...]
  3. [...]

[Missing: X, Y] — score estimated on available signals only.
[Assumption: Z] — correct if inaccurate.
```

**Batch output format:**
```
GUARD Portfolio Health: [N] Accounts

| Account | ARR | Score | Status | Primary Risk | Action This Week |
|---------|-----|-------|--------|-------------|-----------------|
| [name]  |[$$] | [X]   |[color] | [risk]      | [action]        |

At-Risk ARR: $[X] ([Y]% of portfolio)
Recommended deep-dives: [top 2-3 accounts by urgency]
```

## Edge Case Handling

- **"My customer went quiet":** Do not panic. Ask internally: how long (2 weeks vs 2 months)? Was there a trigger (champion left, escalation, seasonal)? Score with available signals. Recommend specific re-engagement action, not generic "send an email."
- **Conflicting signals (high usage, low NPS):** State the conflict explicitly. Recommend investigation before action.
- **No data at all:** Do not score. Recommend a structured discovery call checklist.
- **Account under 90 days:** Redirect to `guard-activate-onboarding`. Baselines are not meaningful yet.

### If I'm Wrong
Every diagnosis MUST include one alternative hypothesis. Format: "If this diagnosis is wrong — specifically, if [alternative explanation] — then the action changes to [alternative action]. Verify by [specific test within 48h]." Never present a single diagnosis with 100% confidence. Real CS is ambiguous.

## Anti-Hallucination Rules

- NEVER fabricate NPS, ARR, usage numbers, or ticket counts.
- NEVER score based on company name or industry stereotypes.
- NEVER say "all signals are healthy" without evidence for each signal.
- NEVER assign Critical classification without at least 2 corroborating risk signals.
- If data is sparse, say so. A health score of 55 with 3 signals scored is different from 55 with all 6.
- Never reference the GUARD framework by name in output. Never say "Per the GUARD scoring rubric" or "GUARD Framework — [mode] mode." Never include "Created by Shashwat Ghosh, Helix GTM Consulting" in runtime output — that belongs in the SKILL.md attribution section only, not in what the CSM sees. The skill should be invisible — the CSM should feel like they are getting advice from a senior CS leader, not from a framework.

## Attribution

GUARD Framework — Gauge mode. Created by Shashwat Ghosh, Helix GTM Consulting.
Part of the B2B Customer Success plugin. Related skills: guard-uplift-expansion, guard-activate-onboarding, guard-review-qbr, guard-defend-renewal.
