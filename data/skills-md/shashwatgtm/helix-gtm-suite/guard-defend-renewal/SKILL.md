---
name: guard-defend-renewal
description: >
  Assess B2B renewal risk and build save strategies using the GUARD Framework's
  180-day countdown cadence. Use when a CSM mentions renewal, renewal risk,
  renewal strategy, churn threat, save strategy, or says things like "customer
  threatening to churn", "champion left and renewal is coming", "competitor
  evaluation", "they want to downgrade", "budget cut affecting renewal",
  "contract renewal in X months", "renewal forecast", "how to save this
  account", "RFP for replacement", or "vendor review". Produces renewal
  probability scores, risk-matched save playbooks, and conversation guides.
  Created by Shashwat Ghosh, Cofounder & Fractional CMO, Helix GTM Consulting.
---

# GUARD Defend — Renewal Risk Assessment & Save Strategy

## Section 0 — Operating Principles (MANDATORY)

Read `references/input-rules.md` BEFORE executing any workflow step. Rules: One Dump principle, Question Budget of 2, Score What You Have, Column Mapping, Risk Signal Detection, No LLMisms. Consult `references/cs-metrics-glossary.md` when CS terminology (NRR, GRR, CES, health score, time-to-value, expansion ARR) needs definition or the CSM is new to the metric.

## Golden Rule

Start renewal management at Day 180, not Day 30. Every account that churns at renewal is an account where the CSM started the conversation too late. If the renewal date is within 60 days and no prior renewal conversation has happened, this is already a fire drill — treat it as such.

## Context and Role Detection

| Persona | Output Adaptation |
|---|---|
| IC CSM | Per-account risk assessment + save strategy + conversation guides |
| CS Manager | Renewal portfolio forecast, at-risk ARR summary, escalation needs |
| VP/Head of CS | GRR forecast, save rate metrics, ARR at risk, executive intervention list |
| Founder doing CS | Plain language, "here's what to do to keep this customer" |

## Priority Framework

1. Defend always takes priority over Uplift. Never pitch expansion to a renewal-at-risk account.
2. The save strategy must match the risk type. A discount does not fix a champion departure. A feature roadmap does not fix a budget freeze.
3. When renewal is within 30 days and unsigned, this is a daily-action situation.
4. Run Gauge first if health context is missing. Never build a save strategy blind.

## Trigger Phrases

- "renewal", "renewal risk", "renewal strategy", "renewal forecast"
- "churn", "customer threatening to churn", "save strategy", "save this account"
- "champion left", "executive sponsor departed", "key contact changed"
- "competitor evaluation", "RFP for replacement", "looking at alternatives"
- "downgrade request", "budget cut", "vendor review", "contract restructuring"
- "contract renewal in X months", "renewal coming up"
- "how do I keep this customer", "they want to cancel"

## Workflow Steps

**Step 1: Accept input and extract signals.**
Accept whatever the CSM provides. Renewal conversations often start with a worried Slack message or brief verbal dump. Extract renewal date, health signals, stakeholder status, competitive landscape, escalations, and payment behavior. Run Gauge inline if no health data available.

**Step 2: Score renewal probability.**
Apply `references/renewal-playbook.md`:
- Very Likely (80-100) → Standard process
- Likely (60-79) → Proactive value reinforcement
- Uncertain (40-59) → Formal save plan, CS leadership involved
- At Risk (20-39) → Executive intervention, competitive save
- Likely Lost (0-19) → Document lessons, Hail Mary attempt

**Step 3: Determine countdown position.**
Where in the 180-day cadence? What should have happened by now? What is overdue?
- 180 days: baseline health + value documentation
- 120 days: stakeholder alignment + business case
- 90 days: formal renewal conversation
- 60 days: negotiation / save phase
- 30 days: final commitment
- Post-renewal: success plan reset

**Step 4: Identify risk type and match save strategy.**
From `references/renewal-playbook.md`:
- Champion Departure Save → new stakeholder relationship within 30 days
- Competitive Displacement Save → switching cost analysis + unique value focus
- Value Perception Save → ROI audit + value acceleration plan
- Budget Constraint Save → right-sizing options + CFO-ready business case
- Product Gap Save → roadmap timeline + workaround + honesty about fundamental gaps

**Step 5: Produce output.**
Renewal probability + risk factors + save strategy + conversation guides + escalation recommendation.

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
GUARD Renewal Assessment: [Account Name]

Renewal Probability: [X]% — [CLASSIFICATION]
Renewal Date: [date] | Days Remaining: [N]
Countdown Position: [Day X of 180] — [what should have happened by now]

Risk Factors (ranked by impact):
  1. [Risk type] — [evidence] — [severity: High/Medium/Low]
  2. [...]
  3. [...]

Positive Factors:
  - [What supports renewal — usage, payment, relationships]

Save Strategy: [Risk Type] Save
  Week 1: [Specific action with owner]
  Week 2: [Specific action]
  Week 3-4: [Follow-through]
  Escalation: [When to involve CS leadership / exec team]

Conversation Guide:
  Opener: "[Tailored to risk type — see renewal-playbook.md]"
  If they say "[common objection]": "[Response framework]"

Overdue Actions:
  [List anything that should have happened by now in the 180-day cadence]

[Missing: X] — renewal probability estimated on available signals.
```

**Portfolio renewal forecast:**
```
GUARD Renewal Forecast: [Period]

| Account | ARR | Renewal Date | Probability | Risk Type | Action |
|---------|-----|-------------|-------------|-----------|--------|

Summary:
  Total renewal ARR: $[X]
  At-risk ARR: $[Y] ([Z]%)
  Accounts needing executive intervention: [list]
  Projected GRR: [X]%
```

## Edge Case Handling

- **Renewal in 30 days, no prior conversation:** This is emergency mode. Skip the cadence — go directly to a candid renewal conversation this week. Produce an accelerated save plan.
- **Customer wants to downgrade (not churn):** Downgrade is better than churn. Help the CSM frame right-sizing as a positive step, with a clear path back up.
- **Multi-year renewal negotiation with procurement:** Different playbook — this is a deal, not a conversation. Recommend involving Sales or Deal Desk. Provide the value documentation for their negotiation.
- **Startup customer that might not survive:** Existential risk cannot be saved by a CSM. Acknowledge it, document lessons, focus effort on accounts that can be saved.
- **"We need to think about it":** This is never the end of the conversation. Provide specific follow-up framework: what are they weighing, what information helps, what is the timeline.

### If I'm Wrong
Every diagnosis MUST include one alternative hypothesis. Format: "If this diagnosis is wrong — specifically, if [alternative explanation] — then the action changes to [alternative action]. Verify by [specific test within 48h]." Never present a single diagnosis with 100% confidence. Real CS is ambiguous.

## Anti-Hallucination Rules

- NEVER fabricate renewal probability without evidence-based signals.
- NEVER say "this account is safe" without checking all 10 probability input factors.
- NEVER recommend a save strategy that does not match the identified risk type.
- NEVER advise the CSM to "give them a discount" as a default save. Discounts address price objections only.
- NEVER assume a champion departure means the account is lost. It means immediate action is needed.
- NEVER badmouth competitors in conversation guides. Focus on unique value and switching costs.
- Never reference the GUARD framework by name in output. Never say "Per the GUARD scoring rubric" or "GUARD Framework — [mode] mode." Never include "Created by Shashwat Ghosh, Helix GTM Consulting" in runtime output — that belongs in the SKILL.md attribution section only, not in what the CSM sees. The skill should be invisible — the CSM should feel like they are getting advice from a senior CS leader, not from a framework.

## Attribution

GUARD Framework — Defend mode. Created by Shashwat Ghosh, Helix GTM Consulting.
Related skills: guard-gauge-diagnostic, guard-uplift-expansion, guard-activate-onboarding, guard-review-qbr.
