---
name: commercial-qualification
description: >
  Score and qualify B2B consulting opportunities using the BANTTD framework
  (Budget, Authority, Need, Timeline, Tech-fit, Decision Date). Run the
  P.U.D.T.F pre-filter to rapidly screen opportunities before full scoring.
  Produce opportunity scorecards with a Pursue/Nurture/Disqualify verdict and
  recommended next actions. Execute the Professional Cut protocol when
  disqualifying. Use when evaluating whether to invest resources in an
  opportunity, after a qualification meeting or discovery meeting, or during
  pipeline reviews to re-qualify stale opportunities.
---

# Commercial Qualification

## Purpose

- Systematically qualify consulting opportunities to ensure the pipeline contains real deals worth pursuing.
- Prevent the team from wasting time on unwinnable or unprofitable deals.
- Produce a defensible, data-backed qualification verdict using the BANTTD framework.
- Execute graceful disqualifications (Professional Cut) to preserve relationships and pipeline hygiene.

## Scope

- This skill WILL:
  - Run the P.U.D.T.F pre-filter to screen opportunities before full BANTTD scoring
  - Score opportunities across six dimensions (Budget, Authority, Need, Timeline, Tech-fit, Decision Date)
  - Produce a qualification scorecard with verdict and confidence level
  - Identify key risks, information gaps, and recommended next actions
  - Update pipeline state with qualification results
  - Flag deals below minimum engagement thresholds
  - Trigger re-qualification for stale opportunities (30+ days)
  - Execute the Professional Cut protocol for disqualified opportunities

- This skill WILL NOT:
  - Design solutions or estimate effort (that is `solution-design`)
  - Conduct discovery meetings (that is `commercial-discovery`)
  - Make final go/no-go business decisions — it provides the data for humans to decide

## Inputs

- **qualification-meeting-notes.md** — notes from the qualification meeting (primary evidence source for P.U.D.T.F and BANTTD scoring).
- **discovery-notes.md** — from `commercial-discovery` (supplementary evidence when available).
- **prospect-profile.md** — from `commercial-prospecting` (company and stakeholder context).
- **commercial-state.md** — current pipeline context (stage, history, capacity).
- **user_input** — additional intel, override context, or competitive intelligence.

Notes:
- Meeting notes may be incomplete. Score conservatively and flag gaps.
- Tolerate ambiguity — never invent evidence to fill scoring gaps.

## Reference

- **[qualification-meeting-guide.md](references/qualification-meeting-guide.md)** — Full meeting script (30-40 min), P.U.D.T.F operational guide, budget calibration techniques, decision date extraction scripts, Professional Cut protocol, red/green flags, and Branch B transition script.

---

## Step 1 — P.U.D.T.F Pre-Filter

Before running the full BANTTD scoring, apply the P.U.D.T.F pre-filter. This is a rapid in-meeting or post-meeting screen (5 dimensions, 1-5 each, total /30). It maps directionally to BANTTD dimensions and provides an early signal.

| P.U.D.T.F | Maps to BANTTD | Key Question |
|-----------|---------------|-------------|
| **P — Problema** | Need | Is there a specific, real, acknowledged problem? |
| **U — Urgencia** | Timeline | Is there urgency or a compelling event driving action? |
| **D — Decisor** | Authority | Are we talking to someone with decision-making power or a clear path to it? |
| **T — Ticket** | Budget | Is there budget allocated or a realistic path to it? |
| **F — Fecha** | Decision Date | Is there a defined decision date or timeline to act? |

**Pre-filter verdict**:

| P.U.D.T.F Total | Signal | Action |
|-----------------|--------|--------|
| 22-30 | Pass — proceed to full BANTTD scoring | Schedule Discovery meeting |
| 16-21 | Borderline — gaps exist | Identify which dimension(s) are weak. Determine if gaps can be closed before full scoring. Consider requesting a follow-up call to address specific gaps. |
| < 16 | Fail — execute Professional Cut | Do not invest further resources. Follow the Professional Cut protocol in the meeting guide. |

> **Single-dimension hard block**: A score of 1 on any P.U.D.T.F dimension (no problem, no decision maker access, no budget signal, no urgency, no timeline) is a hard red flag regardless of total score. Escalate to human judgment before proceeding.

For detailed scoring guides per dimension (1-5 scales with examples), see [qualification-meeting-guide.md](references/qualification-meeting-guide.md).

---

## Step 2 — BANTTD Framework

Score each dimension 0-20. Total score range: **0-120**.

### B — Budget (0-20)

Is there money? Is it allocated? Is the range known and consistent with our engagement model?

### A — Authority (0-20)

Do we have access to the economic buyer? Is the champion identified and actively engaged?

### N — Need (0-20)

Is the pain real and urgent? Is the prospect actively looking for solutions? Is the impact quantified?

### T — Timeline (0-20)

Is there a defined timeline? Is there an external deadline or event driving urgency?

### T — Tech-fit (0-20)

Does our expertise match their needs? Can we deliver meaningful value without excessive subcontracting?

### D — Decision Date (0-20)

Is there a specific date by which the prospect expects to make a decision? Is it tied to a business event? Is it near-term enough to drive action?

For detailed scoring rubrics with criteria at each 5-point increment, see [references/scoring-models.md](references/scoring-models.md).

---

## Step 3 — Verdict Logic

| Total Score | Verdict | Action |
|-------------|---------|--------|
| 84-120 | **Pursue** | Advance to next step (see Pipeline Branch below). Invest full resources. |
| 48-83 | **Nurture** | Define nurture plan with timeline. Re-qualify in 30-90 days. |
| 0-47 | **Disqualify** | Execute Professional Cut. Archive with documented reasons. |

**Confidence Level**: High / Medium / Low — based on information completeness across all dimensions.

**Critical override**: A single dimension at 0-5 should trigger concern regardless of total score (e.g., no budget = hard to pursue even if need is 20/20).

---

## Disqualify / Nurture Flow

### Disqualify — Professional Cut Protocol

When verdict is **Disqualify**, execute a Professional Cut within 24 hours. Do not ghost.

1. **Identify the primary disqualification reason** (weak Budget, no Authority path, no real Need, no Timeline, poor Tech-fit, no Decision Date).
2. **Select the appropriate Professional Cut script** from [qualification-meeting-guide.md](references/qualification-meeting-guide.md):
   - Script 1: No Budget / Not the Right Time
   - Script 2: No Decision Maker Access
   - Script 3: Problem is Not Real or Not Urgent Enough
   - Script 4: Catch-All (multiple weak signals)
3. **Execute the cut in the final minutes of the meeting or via follow-up call** (same day or next day at latest).
4. **Send the follow-up email** within 24 hours using the template in the meeting guide.
5. **Archive the opportunity** in `commercial-state.md` with stage `closed_lost`, documented disqualification reason, and a re-engage trigger date if applicable.

**Principle**: A respectful, honest disqualification preserves the relationship. The prospect may return when timing changes, or refer others. A ghosted prospect never does either.

### Nurture — Holding Pattern

When verdict is **Nurture**:
1. Define which dimensions need to improve and what would trigger re-qualification.
2. Set a re-qualification date (30-60 days typical; 90 days maximum before escalating to Disqualify).
3. Define a lightweight nurture action (1-2 touchpoints before re-qualification: article share, event invitation, check-in call).
4. Update `commercial-state.md` with nurture plan, weak dimensions, and re-qualification trigger.

---

## Pipeline Branch Recommendation

When verdict is **Pursue**, immediately determine which commercial branch to follow. This decision drives the next skill to invoke.

### Branch A — Direct Implementation Proposal

Use when ALL of the following are true:
- Scope can be defined with estimation accuracy +/- 20% or better.
- Requirements are clear and bounded.
- Client knows what they want to build (or discovery already clarified it).
- Scope-changing assumptions are 2 or fewer.
- Qualification confidence: **High** or **Medium** with low ambiguity.

**Next step**: invoke `commercial-solution-design` → `commercial-proposal-writer`.

### Branch B — Discovery Service Proposal

Use when ANY of the following is true:
- Scope cannot be reliably estimated (uncertainty > +/- 30%).
- Client has vague requirements or multiple undecided directions.
- Technical complexity requires investigation before architecture can be proposed.
- Multiple systems, domains, or stakeholder groups need assessment before scoping.
- Client has a problem but does not know what solution they need.
- Qualification confidence: **Low**, or scope-changing assumptions > 3.

**Next step**: invoke `commercial-discovery-proposal` to create a paid Discovery engagement.

> **Note**: The Discovery engagement is an independent commercial opportunity — it has its own proposal, negotiation, and close cycle. Implementation is a separate, subsequent opportunity that may or may not stay with us after Discovery closes.

For the Branch B transition script (how to explain Discovery to the prospect), see [qualification-meeting-guide.md](references/qualification-meeting-guide.md).

### Branch Decision Table

| Signal | Branch A | Branch B |
|--------|----------|----------|
| Requirements clarity | Clear and bounded | Vague or multiple directions |
| Estimation confidence | +/- 20% achievable | +/- 30% or worse |
| Scope-changing assumptions | <= 2 | > 3 |
| Qualification confidence | High / Medium | Low |
| Systems/domains to assess | 1-2, known | 3+, unknown |
| Client knows what to build | Yes | No |

---

## Framework Comparison

- **BANT**: Classic but misses tech-fit and decision date — both critical for consulting.
- **BANTT**: Our prior framework — extended BANT with Tech-fit. Now superseded by BANTTD.
- **MEDDIC/MEDDPICC**: Comprehensive but complex — BANTTD captures the essentials for consulting.
- **P.U.D.T.F**: Operational in-meeting filter (1-5 scale, /30). Used as a pre-filter before BANTTD, not a replacement.
- **CHAMP**: Good but less structured scoring.
- **ANUM**: Budget-first approach may miss good nurture opportunities.

BANTTD extends BANTT with Decision Date to address a critical gap: a well-qualified deal with no clear decision date cannot be forecast reliably and tends to stall.

---

## Outputs (contract)

### 1. New File: `qualification-scorecard.md`

Per opportunity, containing:

```markdown
# Qualification Scorecard: {Company Name}

## Opportunity Summary
- **Opportunity ID**:
- **Company**:
- **Opportunity description**:
- **Qualification Date**: YYYY-MM-DD

## P.U.D.T.F Pre-Filter

| Dimension | Score (1-5) | Evidence |
|-----------|------------|----------|
| P — Problema   |            |          |
| U — Urgencia   |            |          |
| D — Decisor    |            |          |
| T — Ticket     |            |          |
| F — Fecha      |            |          |
| **Total**      | **/30**    |          |

**Pre-filter verdict**: Pass (>=22) | Borderline (16-21) | Fail (<16)

## Urgency Score (1-10)
- **Score**: X/10
- **Prospect's exact words**:
- **Compelling event (if any)**:

## BANTTD Scores

| Dimension | Score (0-20) | Evidence |
|-----------|-------------|----------|
| Budget        |             |          |
| Authority     |             |          |
| Need          |             |          |
| Timeline      |             |          |
| Tech-fit      |             |          |
| Decision Date |             |          |
| **Total**     | **X/120**   |          |

## Verdict: {PURSUE / NURTURE / DISQUALIFY}

**Confidence Level**: {High / Medium / Low}

### Justification
[2-3 sentences explaining the verdict based on scores and evidence]

### Key Risks
- [Risk 1]
- [Risk 2]

### Missing Information
- [What we still need to learn]

### Recommended Next Actions
- [ ] Action 1
- [ ] Action 2

## Deal Estimate
- **Size estimate**: $X - $Y
- **Probability**: X%

## Pipeline Branch
- **Recommended branch**: A (Direct Proposal) | B (Discovery Service)
- **Branch rationale**: [1-2 sentences explaining why this branch was selected]
- **Next skill to invoke**: `commercial-solution-design` | `commercial-discovery-proposal`
```

### 2. Updated: `commercial-state.md`

Update opportunity stage, probability, and notes based on qualification verdict.

---

## Guardrails

1. Always run the P.U.D.T.F pre-filter before the full BANTTD scoring.
2. Every dimension score must include specific evidence or cite information gaps.
3. Never default to "Pursue" without strong justification — bias toward honesty.
4. If confidence is Low, recommend information-gathering actions before final verdict.
5. A single dimension at 0-5 should trigger concern regardless of total score.
6. Re-qualification should happen if opportunity has been stale for 30+ days.
7. Compare qualification against team capacity — a qualified deal we cannot staff is still a problem.
8. Flag deals that are qualified but below minimum engagement size.
9. A Disqualify verdict must trigger a Professional Cut within 24 hours — never ghost.
10. Record the prospect's exact words for urgency (1-10 scale) and decision date — these are the most reliable forecasting inputs.

---

## Example

**Scenario**: Mid-market fintech (200 employees) wants to build a data platform to unify customer analytics across three product lines. Qualification meeting completed with VP Engineering.

**P.U.D.T.F Pre-Filter**:

| Dimension | Score | Evidence |
|-----------|-------|----------|
| P — Problema | 4 | Three siloed analytics systems causing duplicate reporting and 2-week lag on cross-product metrics. |
| U — Urgencia | 3 | Urgency score 7/10. "Board is asking for unified view before Q1 planning." No hard external deadline. |
| D — Decisor | 3 | VP Engineering is champion. CTO is economic buyer, aware and supportive but not yet engaged directly. |
| T — Ticket | 4 | "Low six figures approved for H2." Previous consulting spend at ~$150K confirmed. |
| F — Fecha | 3 | "Want something in place before Q1 planning" — soft deadline, approximately 4 months out. |
| **Total** | **17/30** | Pre-filter: **Borderline** — proceed with BANTTD scoring but flag Authority and Decision Date gaps. |

**BANTTD Scores**:

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Budget | 14/20 | VP mentioned "low six figures" budget approved for H2. No specific allocation yet. Previous consulting spend with a competitor at ~$150K. |
| Authority | 16/20 | VP Engineering is champion and budget holder. CTO (economic buyer) aware and supportive but not yet directly engaged. |
| Need | 18/20 | Three siloed analytics systems causing duplicate reporting, 2-week lag on cross-product metrics. Board asking for unified view. Actively evaluating solutions. |
| Timeline | 12/20 | "Want something in place before Q1 planning" — soft deadline, no regulatory or contractual driver. |
| Tech-fit | 15/20 | Data platform and analytics are core capabilities. Minor gap in their specific CDP tooling — would need 1-2 sprints of ramp-up. |
| Decision Date | 10/20 | "Before Q1 planning" implies ~4 months. No specific date given. No hard commitment. |
| **Total** | **85/120** | |

**Verdict**: **Pursue** (85/120, Confidence: Medium)

- Key risk: CTO not yet directly engaged — authority could stall at final approval.
- Key risk: Decision date is soft — "before Q1 planning" could slip.
- Missing: Specific budget figure, CTO meeting, specific decision date (day/week).
- Next actions: Schedule CTO introduction meeting. Request specific decision date. Prepare capability deck on data platform work. Confirm budget range before solution-design.
