---
name: business-case-strategy
description: "Strategy analysis for BAs: current state, future state and SMART objectives, gap analysis, risk, change strategy, business case and financial analysis (cost-benefit, ROI, NPV, IRR), SWOT, root cause, KPIs; use when justifying or choosing a direction for change before going into detailed requirements."
---

# Business Case and Strategy

Based on BABOK v3 chapter 6 (Strategy Analysis: 6.1–6.4), 10.7 (Business Cases), 10.20 (Financial Analysis), 10.38 (Risk Analysis and Management), 10.46 (SWOT), 10.40 (Root Cause Analysis), 10.28 (Metrics and KPIs) and chapter 8 (measuring value after deployment). Respond in the user's language. This is the level of **why and which direction**; detailed requirements belong to the other skills.

## Hard rules
1. **Never invent numbers.** Every amount of money, rate, duration, discount rate and market size must come from the user or from a readable source; label it [Stated] / [Source: …] / [Assumption, needs confirmation]. Where something is missing: ask a question, do not fill it in to make the table "complete". BABOK requires assumptions and estimation methods to be stated so that others can review and challenge them (10.20).
2. **Compute with code, not in your head.** Use `scripts/fin.py` for ROI, NPV, IRR and payback; re-check one number by hand. Never present results that were not run.
3. **This is analysis, not investment advice.** Present facts, assumptions, sensitivity and risk so the decision-maker can weigh them; say plainly that you are not a financial/legal adviser. The discount rate and the hurdle threshold are set by the organization's finance function (BABOK notes that organizations often have a standard rate set by the chief financial officer); do not choose them yourself.
4. **State the need from the organization's viewpoint, independent of the solution.** Needs are often stated together with a predetermined solution; ask again about the assumptions and constraints so that you solve the right problem and keep a wide range of options (6.1). The desired outcome of the business case must likewise be independent of the proposed solution (10.7).
5. **Always include a "do nothing" option** and count it in the comparison (10.7). Compare options over the same period (10.20).
6. **Objectives must be measurable** (SMART; 6.2). Convert qualitative goals into specific objectives tied to an indicator, or state plainly "not yet measurable" and how it would be measured.
7. **Say what cannot be quantified.** Non-financial benefits (reputation, compliance, flexibility) are still recorded, tied to strategic objectives, and are not forced into money without a basis (10.7, 10.20).
8. **Distinguish facts, opinions and assumptions** in SWOT, root cause analysis and attitude assessments. Causes found by fishbone/5-why are only potential causes until checked against data (10.40).
9. **State the limit of the sections read** at the end of this file; do not cite sections that were not read.

## Overall process
1. **Clarify the need** (`references/current-future-state.md`): the problem/opportunity, who is affected, the cost of doing nothing.
2. **Current state**, just enough to confirm the need and the strategy (6.1): organization and culture, capabilities and processes, technology, policy, assets, external influences.
3. **Future state** (6.2): SMART objectives, scope of the solution space, constraints, assumptions, potential value.
4. **Gap** between current ↔ future (6.4.4.2) and the organization's **readiness** (6.4.4.3).
5. **Risk** (6.3, 10.38) and risk appetite.
6. **Options and change strategy** (6.4): several options, selection criteria, transition stages.
7. **Business case** (10.7) and **financial analysis** (10.20): `references/business-case-financial.md`.
8. **Metrics** (10.28) to track value after deployment (chapter 8).
9. **Return**: a document per `templates/business-case-template.md` + open questions + assumptions + next steps (link to `requirements-stakeholders`, `requirements-elicitation`, `requirements-document`).

## Modes
- **Full business case** from a problem description and the data available.
- **Quick partial analysis**: only current state/gap, or SWOT, or root cause, or metrics.
- **Review an existing business case**: look for a need stated together with a solution, a missing "do nothing", unstated assumptions, numbers without sources, unmeasurable objectives, risks without an owner, inconsistent comparison periods.
- **Financial calculation** from a cost-benefit table the user provides.

## Reference files
- `references/current-future-state.md`: need, current state, future state, SMART objectives, external influences.
- `references/gap-risk-strategy.md`: gap, readiness, risk, options, strategy and transition stages.
- `references/business-case-financial.md`: business case structure, TCO, cost-benefit, ROI, NPV, IRR, payback, limits.
- `references/analysis-techniques.md`: SWOT, root cause, KPIs, post-deployment measurement.
- `templates/business-case-template.md`: template and worksheet.
- `scripts/fin.py`: financial calculation (use `python3 scripts/fin.py input.json`).

## BABOK sections not read (say so plainly if relevant)
Not read: Business Capability Analysis (10.6), Business Model Canvas (10.8), Balanced Scorecard (10.3), Benchmarking and Market Analysis (10.4; the frameworks 5 Forces, PEST, STEEP, CATWOE are known by name only, through section 6.1), Vendor Assessment (10.49), chapters 8.3 and 8.4 (solution limitations, enterprise limitations). Decision Analysis (10.16) was read only in part. The source documents contain no investment appraisal standard or accounting standard; the discount rate and thresholds are set by the organization.
