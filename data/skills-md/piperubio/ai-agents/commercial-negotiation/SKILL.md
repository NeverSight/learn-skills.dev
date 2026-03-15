---
name: commercial-negotiation
description: >
  Prepare negotiation strategies and playbooks for B2B technology consulting
  deals. Covers BATNA/ZOPA analysis, concession planning, objection handling,
  closing techniques, and procurement navigation. Includes consulting-specific
  objection responses (pricing vs. Big4, internal team, offshore). Use when
  preparing for price negotiations, handling client objections to consulting
  proposals, navigating procurement/RFP processes, or developing closing
  strategies for complex deals.
---

# Commercial Negotiation

## Purpose

Prepare the commercial team for successful negotiations by creating structured playbooks per opportunity. The goal is to reach a fair agreement that satisfies both parties and sets the stage for a healthy long-term relationship. This is NOT about "winning" at the client's expense.

### Key Consulting Negotiation Differences

- We negotiate ongoing relationships, not one-time transactions.
- The people we negotiate with today are the people we work with tomorrow.
- Our "product" is our people — discounting too much signals low quality.
- Scope flexibility is our biggest lever (not price).

## Inputs

- `commercial-proposal.md` — from `commercial-proposal-writer` (implementation proposal, Branch A)
- `discovery-proposal.md` — from `commercial-discovery-proposal` (Discovery service proposal, Branch B)
- `qualification-scorecard.md` — from commercial-qualification
- `discovery-notes.md` — from commercial-discovery
- `commercial-state.md` — pipeline context
- `user_input` — specific objections received, procurement requirements, competitive intel

**Branch context**: Check the opportunity `branch` and `type` fields in `commercial-state.md`:
- **Branch A / type: implementation**: Standard implementation negotiation. Apply full playbook.
- **Branch B / type: discovery_service**: Negotiating the Discovery engagement. The negotiation dynamic is different — you are selling risk reduction, not implementation. Scope flexibility is limited (Discovery deliverables are fixed). Price defense focuses on the cost of proceeding without structured discovery. See `commercial-discovery-proposal/references/negotiation-playbook.md` for Discovery-specific scripts, objection handlers, and closing techniques.

## Outputs (contract)

### 1. `negotiation-playbook.md` — per opportunity

Contains the following sections:

#### Deal Summary
Key terms on the table, our position, their likely position.

#### BATNA Analysis
- **Our BATNA**: What happens if we don't close this deal.
- **Their BATNA**: What alternatives do they have.
- **Walk-away point**: Minimum acceptable terms.

#### ZOPA (Zone of Possible Agreement)
- Our ideal outcome.
- Their likely ideal outcome.
- Overlapping zone where agreement is possible.

#### Concession Strategy
- Planned concessions ordered by willingness to give.
- For each concession: what we give, what we get in return, when to deploy.
- Rule: never give a free concession; concessions must decrease in size.
- Include non-monetary concessions (faster start, knowledge transfer scope, reporting frequency).

#### Objection Handling (consulting-specific)
- "Too expensive" → value reframe, scope adjustment, phasing.
- "Why not Big4?" → agility, senior-heavy teams, cost-effectiveness, lower overhead.
- "Why not build internally?" → time to market, expertise ramp-up, opportunity cost.
- "Why not offshore?" → communication, quality, time zones, cultural fit, true cost.
- "Can you reduce the rate?" → scope/seniority trade-offs, volume commitment.
- "We need a fixed price" → scope definition requirements, risk premium, phase approach.
- "Your timeline is too long" → trade-offs (speed vs. scope vs. cost triangle).

See `references/objection-playbook.md` for the complete objection library with scripted responses.

#### Closing Techniques (consulting-appropriate)
- **Assumptive close**: Schedule kickoff planning.
- **Summary close**: Recap agreed terms.
- **Urgency close**: Market timing, team availability window.
- **Trial close**: Start with Phase 0.
- **Split-the-difference**: On specific terms, not overall price.

#### Procurement Navigation
- RFP response strategy (if applicable).
- Procurement stakeholder identification.
- Compliance requirements checklist.
- Competitive bid positioning.

#### Red Lines
Terms we will NOT accept: below-cost rates, unlimited liability, unreasonable IP terms, penalty clauses without caps.

#### Risk Matrix
What could go wrong in negotiation + mitigation plan.

See `references/negotiation-playbooks.md` for BATNA templates, ZOPA methodology, concession matrix, closing technique details, procurement/RFP navigation guide, anchoring strategies, competitive displacement tactics, contract terms guide, post-mortem template, and communication templates.

### 2. Updated `commercial-state.md`
Negotiation progress logged, opportunity moved to `negotiation` stage, probability and next actions updated.

## Guardrails

1. Never recommend deceptive tactics — long-term relationship trumps short-term win.
2. Never suggest conceding below minimum margin without escalation to leadership.
3. Always have a walk-away point defined BEFORE entering negotiation.
4. Every concession must have a corresponding ask (trade, don't donate).
5. If the negotiation becomes adversarial, recommend a pause and relationship reset.
6. Warn against competing solely on price — it's a race to the bottom.
7. Flag negotiations taking >3 rounds as potential red flags.
8. Procurement navigation must remain ethical — no kickbacks, no side-deals.

## Example

### Mid-Market Data Platform Deal — Client Comparing Against Offshore Provider

**BATNA Analysis**:

| Dimension | Our Position | Their Position |
|-----------|-------------|----------------|
| **BATNA** | Strong pipeline; two other qualified deals in same quarter. Losing this deal doesn't create revenue pressure. | Evaluated two offshore providers at 40% lower rate. Internal team has partial capability but no data platform experience. |
| **Walk-away** | Below $180/hr blended or >20% scope discount. | They need to start before Q3 regulatory deadline — delay is costly. |
| **Leverage** | Domain expertise in financial data platforms; three similar references in their industry. | Procurement has budget authority but technical team prefers us. |

**ZOPA**: Our floor is $850K (at minimum margin). Their ceiling is estimated at $1.1M based on budget signals. Target: $950K with Phase 0 + Phase 1 commitment. ZOPA exists — overlap of $250K to negotiate within.

**Objection Handling — "Why not go offshore at half the price?"**:

- **Acknowledge**: "That's a fair comparison to make. Cost matters."
- **Clarify**: "When you compare, are you looking at rate alone, or total cost including your internal coordination effort?"
- **Response**: "On a similar data platform project, a client initially engaged an offshore team at $85/hr. After 6 months of rework, timezone-driven delays, and two senior internal engineers spending 40% of their time on coordination, the true cost exceeded $210/hr. We start at $185/hr with senior architects who have done this 12 times — no ramp-up, no rework cycle. The regulatory deadline in Q3 means the cost of delay far exceeds the rate difference."
- **Pivot**: "We could do a 3-week Phase 0 at $45K. If our approach doesn't demonstrate clear superiority in speed and quality, you've lost very little. But if it does, you'll have confidence and a running start toward Q3."
