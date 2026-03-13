---
name: commercial-discovery-proposal
description: >
  Create proposals for Strategic Discovery as a paid, fixed-price consulting service.
  Use when an opportunity has high scope uncertainty, ambiguous requirements, or estimation
  risk above +/- 30% — and therefore cannot be priced as a direct implementation proposal.
  This skill produces a Discovery Service proposal (Branch B of the commercial pipeline),
  treating the discovery engagement as an independent commercial opportunity with its own
  qualification, proposal, negotiation, and close cycle. The resulting Discovery deliverables
  (architecture, roadmap, refined estimation) feed into a separate, subsequent implementation
  opportunity. Triggers on: discovery proposal, discovery service, paid discovery, strategic
  discovery, fase de descubrimiento, propuesta de discovery, discovery pagado, scope uncertainty,
  ambiguous requirements, cannot estimate, needs investigation before proposal.
---

# Commercial Discovery Proposal

## Purpose

Produce a commercial proposal for Strategic Discovery as a standalone paid engagement.

This skill handles **Branch B** of the commercial pipeline — when scope uncertainty is too high
to generate a credible implementation proposal directly. The Discovery Service is sold as an
independent engagement with its own commercial lifecycle, not as a precursor step bundled into
the implementation price.

**Key principle**: Discovery converts an ambiguous problem into an executable plan with
defensible estimation. It is a service the client buys. Its output may or may not lead to an
implementation opportunity with us.

**Core selling principle**: If the client will not invest in understanding the problem, they
will not invest in solving it. A prospect who resists paying for structured understanding is
signaling that the problem, urgency, or budget may not be real. Conviction in Discovery's
value is non-negotiable — doubt in the seller transmits directly to the buyer.

## When to Use This Skill (Branch B Criteria)

Apply this skill when qualification reveals:

- Scope cannot be defined with estimation accuracy better than +/- 30%.
- Client has vague requirements or multiple undecided directions.
- Technical complexity requires investigation before architecture can be proposed.
- Multiple systems, domains, or stakeholders need assessment before scoping.
- Client has a problem but does not know what solution they need.
- Qualification scorecard shows confidence: Low or scope-changing assumptions > 3.

See Branch A vs. Branch B guidance in the commercial-core-agent lifecycle documentation.

## Inputs

- **`qualification-scorecard.md`** — from `commercial-qualification` (required: verdict must be Pursue).
- **`discovery-notes.md`** — from `commercial-discovery` (primary source of context and pain points).
- **`prospect-profile.md`** — from `commercial-prospecting` (company and stakeholder context).
- **`commercial-state.md`** — current pipeline state.
- **`user_input`** — discovery sizing preference (S/M/L), rate parameters, specific deliverables requested.

## Workflow

1. **Assess uncertainty level**: Review qualification scorecard for scope-changing assumptions and confidence level. Confirm Branch B is the right path.
2. **Size the Discovery**: Determine S/M/L sizing based on domain count, stakeholder groups, and technical complexity (see `references/discovery-service-playbook.md`).
3. **Define deliverables**: Select the Discovery deliverables relevant to this client's situation from the standard checklist.
4. **Price the engagement**: Apply fixed-price based on effort estimate for the Discovery only. Validate with user before including in proposal.
5. **Write the proposal**: Use the template below. Reference the playbook for phase descriptions and exclusions.
6. **Prepare for the close**: Review the Discovery-specific closing scripts, objection handlers, positioning directives, and the Smart Clause in `references/discovery-closing-playbook.md`. Select the relevant objection scripts based on what is known about this prospect.
7. **Prepare negotiation brief**: Key scripts and objection responses for the Discovery sale (see `references/negotiation-playbook.md`).
8. **Plan linked opportunity**: Document the potential implementation opportunity that may follow if Discovery closes won.

## Discovery Sizing Reference

For detailed sizing table, pricing guidelines, and deliverables checklist:
see `references/discovery-service-playbook.md` — Section 8.

Quick guide:
- **Small (2-3 weeks)**: 1-2 domains, clear problem, low integration complexity.
- **Medium (3-5 weeks)**: 3-5 domains, multiple stakeholder groups, medium complexity.
- **Large (5-8 weeks)**: 6+ domains, complex architecture assessment, proof-of-concept required.

## References

| File | Purpose |
|------|---------|
| `references/discovery-service-playbook.md` | Phase model, sizing table, deliverables checklist, commercial rules, pricing guidelines |
| `references/negotiation-playbook.md` | Negotiation stages, economic qualification, budget calibration, post-Discovery number presentation, objection handling (price/scope/discount), closing scripts |
| `references/discovery-closing-playbook.md` | Discovery-specific closing: positioning directive, 4-step presentation structure, objection scripts (why pay to quote, deliverables independence, no budget defined), Smart Clause, close/no-close signals, silence technique, pre-close readiness checklist |

## Outputs (Contract)

### Output 1: `discovery-proposal-{company-slug}.md`

```markdown
# Strategic Discovery Proposal: {Company Name}

**Prepared by**: {Consulting Firm}
**Date**: YYYY-MM-DD
**Valid until**: YYYY-MM-DD (30 days default)
**Version**: 1.0

---

## 1. Executive Summary

[2-3 paragraphs. State: the problem and its business impact, why a structured
Discovery is needed before committing to implementation, what the Discovery will
produce, and the investment required. This section must stand alone.]

---

## 2. The Challenge

### Current Situation
[From discovery notes: current state, pain points, business impact. Use client's
own words where possible — they carry the most weight.]

### Why a Direct Proposal Is Not the Right Answer Yet
[Explain honestly why the scope cannot be reliably estimated without structured
investigation. Frame this as responsible consulting, not a limitation.]

### Cost of Proceeding Without Discovery
[What happens if they skip this step: scope creep, cost overruns, wrong solution
built, rework costs. Quantify if possible.]

---

## 3. The Discovery Engagement

### Objective
Convert an ambiguous problem into an executable plan with a defensible estimation
and clear implementation strategy.

### Approach
[2-3 sentences describing the methodology: stakeholder interviews, technical
assessment, architecture workshops, etc.]

### Deliverables

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | Executive Summary of Findings | ... |
| 2 | Current State Assessment | ... |
| 3 | Problem Prioritization Matrix | ... |
| 4 | High-Level Solution Architecture | ... |
| 5 | Technology Recommendations | ... |
| 6 | Phased Implementation Roadmap | ... |
| 7 | Effort Estimation (+/- 20%) | ... |
| 8 | Risk Register | ... |
| 9 | Team Composition Recommendation | ... |
| 10 | Implementation Strategy | ... |

[Include only the deliverables relevant to this engagement. Add or remove rows.]

### What Is NOT Included
- Productive development or implementation.
- Final technical designs or implementation specs.
- Any code, infrastructure, or integrations.
- Ongoing support or advisory after delivery.

### Duration and Team

| Item | Detail |
|------|--------|
| Duration | X weeks |
| Consulting hours | X - Y person-hours |
| Team size | X consultants |
| Client time required | X hours/week (stakeholder interviews, reviews) |

### Exit Criteria
At the end of Discovery, you will have:
- [ ] Scope defined and validated.
- [ ] Critical risks identified.
- [ ] Estimation with margin <= +/- 20%.
- [ ] Clear recommendation for implementation approach.

---

## 4. Investment

### Pricing Model: Fixed Price

| Item | Amount |
|------|--------|
| Discovery Engagement | $X,XXX |
| **Total** | **$X,XXX** |

### Payment Schedule

| Milestone | Trigger | Amount |
|-----------|---------|--------|
| Kickoff | SOW signed | 50% |
| Delivery | Final deliverables accepted | 50% |

### What Happens After Discovery
The Discovery deliverables include a full implementation roadmap and refined
estimation. At that point, you will have everything needed to:
- Proceed with implementation with confidence.
- Evaluate implementation vendors (including us) with a complete brief.
- Make an informed build/buy/partner decision.

There is no obligation to proceed with implementation through us.

---

## 5. Why Invest in Discovery

### The Risk of Skipping It
[1-2 specific examples or analogies: what happens when organizations build without
proper discovery — scope creep, wrong solutions, sunk costs.]

### What You Get
- Confidence before committing to a larger investment.
- A plan you can take to any implementation vendor.
- Internal alignment across stakeholders before execution starts.

---

## 6. About Us

### Relevant Experience
[1-2 brief examples of similar discoveries or assessments completed.]

### Our Approach
[How we work: collaborative, transparent, client-capability-building.]

---

## 7. Next Steps

1. Review this proposal and provide feedback by YYYY-MM-DD.
2. Schedule a 30-minute alignment call to resolve any questions.
3. Sign the SOW and define kickoff date.
4. Target Discovery start: YYYY-MM-DD.

---

**Contact**: {Name}, {Title}, {Email}

---

*This proposal is valid for 30 days from the date above.*
```

### Output 2: Negotiation Brief (inline, not a separate file)

After the proposal, provide a brief negotiation guide for this specific opportunity:

```markdown
## Negotiation Brief — {Company Name} Discovery

**Key objection risks** (based on discovery notes):
- [Most likely objection based on what you know about the client]

**Budget calibration script**:
> "Projects like this typically involve a Discovery investment of $X to $Y.
> Is that in the range you have considered?"

**If they say "we need to think about it"**:
> "What criteria will you use to make the decision?"
> Then: "When would it make sense to reconnect — would [specific date] work?"

**Pre-close question** (use in the meeting before the close):
> "If the investment is aligned, is there anything else you need to move forward?"

**Closing question**:
> "Is there anything preventing you from moving forward today?"
```

For the full negotiation playbook including all scripts, objection handlers, and closing
techniques: see `references/negotiation-playbook.md`.

### Output 3: Updated `commercial-state.md`

Update the opportunity with:
- `type: discovery_service` — marks this as a Discovery Service opportunity (Branch B).
- `stage: proposal` — proposal has been generated.
- `branch: B` — pipeline branch indicator.
- `linked_impl_opp: TBD` — placeholder for the potential implementation opportunity.
- `next_action`: schedule proposal walkthrough meeting.

## Guardrails

1. **Discovery is sold as an independent engagement by default.** Never bundle Discovery price with implementation price in the base proposal. Exception: the Smart Clause (see `references/discovery-closing-playbook.md`) may be deployed as an optional negotiation lever when the prospect is qualified, the decision-maker is present, and the hesitation is specifically financial rather than a signal of low commitment. Never lead with the Smart Clause — only deploy it when the prospect has shown genuine intent and a budget range for the full project has been validated.
2. **Never promise that Discovery leads to implementation with us** — it is the client's choice.
3. **Always include a "What is NOT Included" section** — prevent scope disputes on day one.
4. **Fixed price only** — Discovery must not be T&M; it is a bounded, defined service.
5. **Never skip the exit criteria** — client must know exactly what done looks like.
6. **Validate pricing with the user** before including in the proposal — never invent rates.
7. **Frame Discovery as risk reduction, not a prerequisite** — it is something they buy because it protects them, not a hoop they jump through. Never use the phrase "gather requirements" — use "structure the solution responsibly" or equivalent. See positioning directive in `references/discovery-closing-playbook.md`.
8. **If qualification confidence is High and scope is clear** — flag that Branch A (direct implementation proposal) may be more appropriate.
