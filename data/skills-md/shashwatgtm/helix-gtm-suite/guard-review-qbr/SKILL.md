---
name: guard-review-qbr
description: >
  Prepare structured QBR and EBR materials using the GUARD Framework's
  7-section template. Use when a CSM mentions QBR, quarterly business review,
  EBR, executive business review, business review prep, QBR deck, value recap,
  or says things like "what should I present to the customer", "preparing for
  our quarterly review", "need a QBR brief", "post-QBR recap email", "QBR
  for an at-risk account", or "first QBR after onboarding". Accepts messy
  notes, previous QBR data, CRM exports, or conversational context and produces
  review-ready materials. Created by Shashwat Ghosh, Cofounder & Fractional
  CMO, Helix GTM Consulting.
---

# GUARD Review — QBR/EBR Preparation

## Section 0 — Operating Principles (MANDATORY)

Read `references/input-rules.md` BEFORE executing any workflow step. Rules: One Dump principle, Question Budget of 2, Score What You Have, Column Mapping, Risk Signal Detection, No LLMisms. Consult `references/cs-metrics-glossary.md` when CS terminology (NRR, GRR, CES, health score, time-to-value, expansion ARR) needs definition or the CSM is new to the metric.

## Golden Rule

A QBR that hides bad news destroys credibility. Every QBR must include Section 5 (Risk & Mitigation) even for healthy accounts. Lead with value (what worked), then address risks transparently, then close with a forward plan. Never skip risks. Never sugar-coat. The customer already knows what is broken — your job is to show you know it too and have a plan.

## Context and Role Detection

| Persona | Output Adaptation |
|---|---|
| IC CSM | Full 7-section QBR brief + talking points + slide outline |
| CS Manager | QBR quality review template, coaching points for team |
| VP/Head of CS | QBR summary across portfolio, themes, and risk patterns |

## Priority Framework

1. Run Gauge first if health context is not available. Never prep a QBR blind.
2. Audience determines depth: C-suite gets strategic (20 min), ops lead gets tactical (45 min).
3. At-risk QBRs lead with risks and recovery plan, NOT expansion.
4. QBR prep should take under 30 minutes with this skill. If longer, the skill is failing.

## Trigger Phrases

- "QBR", "quarterly business review", "EBR", "executive business review"
- "business review prep", "QBR deck", "review meeting"
- "value recap", "what to present to customer"
- "QBR for at-risk account", "QBR with C-suite"
- "post-QBR recap", "QBR follow-up email", "QBR action items"
- "first QBR", "90-day review"

## Workflow Steps

**Step 1: Accept input and extract signals.**
Accept whatever the CSM provides — conversational brief, CRM paste, messy notes from the quarter, uploaded PDF of previous QBR (surgical extraction: exec summary + action items + risks only), or MoM from past meetings. Run Gauge inline if no health data is available.

**Step 2: Determine QBR type.**
- Standard QBR (ops lead) → Full 7 sections, data-driven, 30-45 min
- Executive Business Review (C-suite) → Strategic framing, Sections 1,2,5,7 emphasized, 20-30 min
- At-Risk QBR → Lead with Section 5, replace Section 6 with Recovery Plan
- First QBR (90-day mark) → Emphasize onboarding completion, establish baseline

**Step 3: Build the QBR.**
Apply `references/qbr-structure.md`:
1. Partnership Summary — timeline, milestones, stakeholder map update
2. Value Delivered — outcomes mapped to original business case
3. Product Adoption — hero feature + untapped feature identification
4. Support & Satisfaction — ticket trends, NPS/CSAT, open escalations
5. Risk & Mitigation — proactive flags with proposed actions (NEVER skip)
6. Growth Opportunities — natural expansion moments (skip if at-risk)
7. Forward Plan — next quarter objectives, action items, success metrics

**Step 4: Produce output based on request.**
- QBR brief (narrative prose — the default)
- QBR talking points (bullet cheat sheet for the meeting)
- QBR slide outline (section headers + key points per slide)
- Post-QBR recap email (summary + action items, send within 24h)

## Output Format

### Executive Summary Block (MANDATORY — always first)
Every output MUST begin with a 5-line summary before any detail:
Line 1: Health score or renewal probability + status classification
Line 2: Risk type in 5 words or fewer
Line 3: #1 action TODAY with owner
Line 4: Escalation decision (who, when)
Line 5: Deadline or time constraint

The CSM should be able to read these 5 lines, close the chat, and take the right action. Everything after is supporting detail.

**QBR Brief (default):**
```
GUARD QBR Brief: [Account Name]
ARR: [$$] | Renewal: [date] | Health: [score/100, classification]
QBR Type: [Standard/Executive/At-Risk/First]
Audience: [who will attend]

1. PARTNERSHIP SUMMARY
   [Relationship timeline, key milestones since last QBR]

2. VALUE DELIVERED
   [Outcomes mapped to business case, quantified wins]

3. PRODUCT ADOPTION
   Hero Feature: [feature driving most value]
   Untapped Value: [biggest stickiness/expansion opportunity]
   [Adoption % and trends]

4. SUPPORT & SATISFACTION
   [Ticket trends, NPS/CSAT, open escalations]

5. RISK & MITIGATION
   [Proactive flags with proposed actions — NEVER empty]

6. GROWTH OPPORTUNITIES
   [Natural expansion moments based on usage patterns]

7. FORWARD PLAN
   Next Quarter Objectives:
     [Mutual commitments, not one-sided]
   Action Items:
     [Who] — [What] — [By when]
```

### QBR Deck Option
If the CSM asks for a deck, slides, or presentation — produce a PPTX file using the sales-proposal-builder pattern. The deck should follow the 7-section QBR structure with one slide per section. Use the customer's brand colors if provided, otherwise use clean professional styling. The PPTX output is an ADDITION to the text brief, not a replacement — always produce the text brief first, then offer: "Want me to build this as a slide deck for the meeting?"

**Post-QBR Recap Email:**
```
Subject: [Account Name] QBR Recap — [Date]

Hi [Name],

Thank you for [today's/yesterday's] review. Here's a summary of what
we covered and the commitments we made:

Key Wins This Quarter:
  [1-2 sentences on value delivered]

Action Items:
  [Owner] — [Task] — [Deadline]

Risks We're Addressing:
  [1-2 sentences, transparent]

Next Steps:
  [Specific next meeting/milestone]

[CSM signature]
```

## Edge Case Handling

- **QBR with no data:** Produce the structure with `[CSM to add: X]` placeholders. The structure itself is valuable even without data.
- **At-risk QBR + expansion pressure from management:** Do NOT pitch expansion in an at-risk QBR. State this explicitly if asked.
- **First QBR at Day 90:** Frame around onboarding success, not performance gaps. The baseline is being established, not evaluated.
- **CSM inherited the account mid-cycle:** Acknowledge the transition. Use whatever history is available, flag gaps.

## Anti-Hallucination Rules

- NEVER fabricate metrics, ROI numbers, or support ticket data.
- NEVER produce a QBR that skips Section 5 (Risk & Mitigation).
- NEVER invent "customer quotes" or attribute statements the customer did not make.
- NEVER say "everything is on track" without evidence for each dimension.
- Never reference the GUARD framework by name in output. Never say "Per the GUARD scoring rubric" or "GUARD Framework — [mode] mode." Never include "Created by Shashwat Ghosh, Helix GTM Consulting" in runtime output — that belongs in the SKILL.md attribution section only, not in what the CSM sees. The skill should be invisible — the CSM should feel like they are getting advice from a senior CS leader, not from a framework.

## Attribution

GUARD Framework — Review mode. Created by Shashwat Ghosh, Helix GTM Consulting.
Related skills: guard-gauge-diagnostic, guard-uplift-expansion, guard-activate-onboarding, guard-defend-renewal.
