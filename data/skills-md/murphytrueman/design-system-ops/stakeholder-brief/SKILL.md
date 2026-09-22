---
name: stakeholder-brief
description: "Write a one-page stakeholder brief translating design system health or status into business language. Trigger when someone says: stakeholder update, exec brief, leadership summary, status report for leadership, system status for non-designers, write a brief for the business, or anything about communicating design system status to an audience that does not have a design systems background."
references:
  - ../../knowledge-notes/output-discipline.md
---


# Stakeholder brief

A skill for writing a one-page stakeholder brief that translates design system health, status, or a specific recommendation into business language. Output requires no design systems knowledge to read, leads with business impact, and ends with a clear ask.

## Context

Design systems teams are often better at building systems than at communicating their value to the people who fund and prioritise them. The result is that design systems work gets under-resourced, and the case for investment gets made reactively — when something breaks — rather than proactively, when there is time to think clearly.

A stakeholder brief is not a technical report with a summary at the top. It is a business communication that happens to be about design systems work. The reader should be able to understand the situation, the recommendation, and the ask without any prior knowledge of what a design system is or how it works. If a term requires explanation, the explanation belongs in the brief, not in a separate glossary.

## Workflow overview

The stakeholder brief workflow follows five distinct steps:

1. **Establish the brief's purpose** — Confirm the context and the single ask
2. **Structure and write the brief** — Build the five-part template with business framing
3. **Calibrate tone by audience** — Adjust language and emphasis for the specific stakeholder group
4. **Apply framing patterns** — Lead with the insight that resonates most
5. **Review for clarity and quality** — Ensure no jargon, verify the one-page constraint

---

## Step 1: Establish the brief's purpose

Ask for or confirm:
- What is this brief for? (Status update / investment ask / specific recommendation / incident summary / launch announcement)
- Who is the primary audience? (VP, C-suite, product director, budget owner — this determines the level of business abstraction)
- What is the one thing the reader should do or believe after reading it?
- What is the underlying situation? (Health report findings, a specific blocker, a proposed investment, a recent achievement)
- Is there a deadline or decision this brief is feeding into?

The brief should have a single primary purpose. A brief that tries to deliver a status update and make an investment ask and announce a new feature is three briefs, and it will not do any of them well.

**Small-system note (fewer than 5 components):** For systems with fewer than 5 components, the brief needs to frame the system as a deliberate, focused investment rather than something that is small because it is under-resourced. Use "specialised system" or "targeted component library" framing. The ROI argument shifts from scale efficiency ("20 teams reuse the same components") to quality consistency ("every customer-facing surface uses the same interaction patterns") and speed ("new features compose from proven components instead of starting from scratch"). Avoid metrics that make a small system look weak by enterprise standards — "3 components" sounds unimpressive without context. Instead, lead with what those components cover: "Our component library handles 80% of our interface patterns, ensuring consistent experience across all product surfaces."

---

## Step 2: Write the brief using the five-part template

---

### [Brief title — describes the situation and the ask in plain language]

**Date:** [date]
**Prepared by:** [name]
**For:** [audience]
**Regarding:** [one-sentence description of the subject]

---

#### The situation

Two to four sentences. What is the current state of affairs that makes this brief necessary? Write in terms of business impact, not design system mechanics.

Not: "The design system has 42 components and a 60% engineering adoption rate across product teams."
But: "Three product teams are currently maintaining separate, inconsistent versions of core interface components. This creates inconsistent customer experiences and duplicates development effort across the organisation."

If the situation requires a brief explanation of what a design system is: include one sentence. Do not assume the reader knows. Do not patronise them with a long explanation. "A design system is the shared library of interface components and visual standards that product teams use to build consistently without building from scratch each time" is usually sufficient.

---

#### Why this matters

Two to three sentences. What is the business consequence of the situation? Translate into the currency that matters to this audience: time, money, customer experience, risk, competitive position.

Avoid design system metrics as the evidence of impact. "Low token adoption" is not a business problem. "Inconsistent interfaces are generating support tickets and reducing customer trust" is a business problem. Find the business translation.

If you have data, use it. If you do not, be honest about what is estimated and why the estimate is reasonable.

---

#### What we recommend

One sentence stating the recommendation. Then two to four sentences explaining why this recommendation over the alternatives.

Be specific. "Invest in the design system" is not a recommendation. "Dedicate one engineering day per sprint to design system integration across the three product teams, for the next two quarters, to consolidate the parallel component implementations" is a recommendation.

If there are alternatives, acknowledge the most plausible one and explain why the recommendation is preferred. A brief that presents only one option looks like it has not considered the problem fully.

---

#### What we need

The ask. One to three specific items. Each item should be concrete: a decision, a resource allocation, an approval, or a timeline confirmation.

Format:
- [Specific ask 1]
- [Specific ask 2]
- [Specific ask 3, if needed]

No more than three items. A brief with six asks does not get any of them approved.

---

#### Expected outcome

Two to three sentences. If the recommendation is followed and the ask is granted: what changes, when, and what does success look like?

Be honest about timelines and realistic about what the investment will and will not solve. Overpromising in a stakeholder brief erodes trust faster than almost anything else.

---

## Step 3: Calibrate tone and framing by audience

Different stakeholders care about different things. Adjust the brief's emphasis and language based on who is reading:

### Engineering leadership

**What matters:** Technical debt, team velocity, engineering productivity, maintenance burden, system reliability.

**How to frame it:**
- Lead with efficiency: "The current approach costs [n] engineering weeks per quarter in duplicated work."
- Emphasise technical sustainability: "Consolidating parallel implementations reduces our maintenance surface and makes the system a stable platform for growth."
- Reference system health/maturity: "We are at Level 2 (Managed). Moving to Level 3 (Systematic) requires [specific actions] and will enable [technical benefit]."
- Use infrastructure language: "The design system is platform infrastructure for the engineering organisation."

**Specific language to use:**
- "Engineering velocity" (not "design consistency")
- "Technical debt" (don't hide the cost)
- "System reliability" or "system stability"
- "Maintenance burden"
- "Platform dependency" (frame the system as critical infrastructure)

**What to avoid:**
- Design-specific terminology without translation
- Aesthetic arguments without engineering benefit
- Vague efficiency claims without numbers

### Product leadership

**What matters:** User experience, feature velocity, customer satisfaction, time-to-market, competitive positioning.

**How to frame it:**
- Lead with customer experience: "Customers encounter [n] distinct interface patterns for the same interaction across our products, creating confusion."
- Emphasise speed: "Teams building from shared components ship features [n] weeks faster than teams building custom."
- Reference competitive positioning: "Consistency and polish in the interface are competitive differentiators in our market."
- Quantify the benefit: "Faster feature shipping + consistent customer experience = improved market position."

**Specific language to use:**
- "Customer experience" (not "visual consistency")
- "Feature velocity"
- "Time-to-market"
- "Competitive positioning"
- "Customer confidence" or "customer trust"

**What to avoid:**
- Technical implementation details
- Component counts or metrics that mean nothing outside the design world
- Process-focused arguments without customer impact

### Design leadership

**What matters:** Design quality, design team autonomy, consistency, scalability of design work.

**How to frame it:**
- Lead with design quality: "Inconsistent interface patterns create a fragmented user experience that undermines our design intent."
- Emphasise design leverage: "A well-maintained system allows designers to focus on novel problems instead of recreating standard patterns."
- Reference design standards: "The system enforces [n] core design standards, which we currently enforce per-team instead of at the platform level."
- Language around design maturity: "We are currently at Level 2 (Managed design) — components exist but are not consistently governed. Level 3 (Systematic) requires documented design standards and contribution processes."

**Specific language to use:**
- "Design consistency"
- "Design quality"
- "Design scalability"
- "Design leverage"
- "Design standards"

**What to avoid:**
- Engineering-only arguments without design framing
- Numbers without context (component counts)
- Technical implementation choices as the main point

### Executive/C-level

**What matters:** Strategic alignment, risk mitigation, financial impact, competitive positioning, organisational efficiency.

**How to frame it:**
- Lead with strategic impact: "Design system investment is foundational to [strategic goal — e.g., 'scaling to [n] products' or 'competing on user experience']."
- Emphasise risk: "The current approach creates [specific risk — inconsistent user experience, compliance gaps, developer onboarding friction] that undermines [strategic priority]."
- Quantify financial impact: "Eliminating duplicated work is worth [estimated cost savings or engineer-weeks recovered per year]."
- Frame as infrastructure: "This is infrastructure investment, not a design initiative — it is the shared platform that all products depend on."

**Specific language to use:**
- "Strategic alignment"
- "Risk mitigation" or "risk exposure"
- "Operational efficiency"
- "Competitive positioning"
- "Return on investment"
- "Platform infrastructure"
- "Scalability"

**What to avoid:**
- Design and engineering jargon equally
- Discussions of specific components or design patterns
- Implementation details
- Assume any prior knowledge of what a design system is

---

## Step 4: Framing patterns — choose how to lead

The same situation can be framed three ways. Choose the frame that will resonate most with the audience and the context:

### Lead with growth

Use this framing when the situation is about enabling scale or speed.

**Pattern:** "We are currently [current state]. To [strategic goal], we need [investment]. This investment will [specific speed/scale benefit]."

**Example:** "We are currently building features through per-product design cycles. To scale to [n] products without proportionally scaling the design team, we need to formalize the design system. This investment will let us ship [n] new products using [n]% of the design effort currently required."

**Works best for:**
- Product leadership (competitive positioning, speed)
- Growth-stage organisations
- Situations where the system enables new products or markets

### Lead with risk

Use this framing when the situation involves technical or user-facing risk.

**Pattern:** "We are currently [current state], which creates [specific risk]. The cost of this risk is [impact]. We can eliminate this risk by [investment]."

**Example:** "We are currently using [n] accessibility implementations across [n] teams, each implemented differently. This creates legal compliance risk and excludes users with disabilities. We can eliminate this risk by centralizing accessibility implementation in the design system."

**Works best for:**
- Executive/C-level (risk mitigation, compliance)
- Situations with measurable compliance or security gaps
- Preventing incidents from happening again

### Lead with cost

Use this framing when the situation involves efficiency or waste.

**Pattern:** "We are currently [current state], which costs us [specific financial or effort metric]. We can recover this cost by [investment]."

**Example:** "We are currently estimating [n] engineering weeks per quarter spent on duplicated component work across [n] teams. We can recover this cost by consolidating implementations, freeing up [effort or FTE] for product work."

**Works best for:**
- Engineering leadership (velocity, technical debt)
- Finance-conscious organisations
- Situations where the cost is quantifiable

**Choose the frame that matches the audience's priorities:**
- Growth frame → Product, executive
- Risk frame → Executive, compliance-conscious organisations
- Cost frame → Engineering, finance-conscious organisations

---

## Step 5: Business metrics translation guide

Design system health metrics do not land with stakeholders unless they are translated into business consequences. Use this reference when writing the "Why this matters" section:

| Design system metric | Business translation |
|---|---|
| Low token adoption | "Visual inconsistency across products is creating a fragmented brand experience" |
| High component drift | "Teams are maintaining separate versions of the same interface elements, duplicating engineering effort" |
| Poor documentation coverage | "New team members take longer to become productive because system knowledge is tribal, not documented" |
| Low accessibility scores | "We have measurable compliance gaps that create legal exposure and exclude users with disabilities" |
| Declining adoption | "Teams are choosing to build independently rather than use shared infrastructure — the system is not serving their needs" |
| No AI-readiness | "Our component library cannot be consumed by AI development tools, which means we are not benefiting from AI-assisted coding workflows" |
| Version lag across teams | "Multiple teams are running outdated versions, which means bug fixes and improvements are not reaching users" |
| Missing governance process | "There is no defined process for how the system evolves, which creates unpredictability for teams that depend on it" |

When writing the brief, choose the 1–2 translations most relevant to the audience's priorities. Do not list all of them — a brief with eight business consequences reads as a list of complaints, not a focused argument.

---

## Step 6: Maturity-level framing (staff-level)

At the staff level, stakeholder briefs should frame the design system as infrastructure, not as a design convenience. This changes how the situation, recommendation, and outcome are written.

If a system-health assessment has been completed, reference the maturity level in the brief. Frame the recommendation as moving from the current level to the next:

**Infrastructure language:**
- Instead of "the design system needs investment" → "our component infrastructure has reliability gaps that are creating downstream production cost"
- Instead of "teams are building outside the system" → "teams are creating parallel infrastructure because the shared platform doesn't cover their needs — each parallel implementation costs [X] and creates a maintenance liability"
- Instead of "we need a dedicated team" → "the infrastructure needs a defined SLA: expected response time for bug reports, predictable release cadence, and documented API contracts"

**Maturity level context:**
- "We are currently at Level 2 (Managed) — the system exists and is used, but governance is informal and documentation is inconsistent. The recommendation moves us to Level 3 (Systematic), which requires [specific actions]."
- Stakeholders respond to clear progression frameworks. Maturity levels make the investment concrete and the progress measurable.

**Mapping maturity to investment:**
- L1 → L2: "Establish governance. Formalise contribution and deprecation processes."
- L2 → L3: "Standardise token architecture. Enforce documentation standards. Create predictable release cadence."
- L3 → L4: "Implement adoption tracking. Establish system health metrics. Conduct recurring reviews."
- L4 → L5: "Make system machine-readable. Implement consumer contract testing. Optimise for AI consumption."

---

## Step 7: Common anti-patterns in stakeholder communication

Avoid these mistakes — they erode credibility faster than almost anything else:

### Anti-pattern 1: Reporting only good news

**The mistake:** "The design system shipped 5 new components this quarter. Teams love the new Button variant. Component adoption is up 2%."

**Why it fails:** Readers detect cherry-picking. If you only mention wins, they wonder what you are hiding.

**The fix:** Lead with the honest situation — what is working and what is not. "The design system shipped 5 new components this quarter, bringing core coverage to 85%. However, adoption of the new components is only 40% in the first month, well below our target of 80%. This suggests the components are not meeting team needs or there is friction in the adoption process."

### Anti-pattern 2: Design system jargon without translation

**The mistake:** "The component library has low token adoption and declining API consistency. We need to improve the design-to-code contract and implement automated drift detection."

**Why it fails:** Non-design audience stops reading and dismisses it as design-specific. You lose them in the first sentence.

**The fix:** Translate everything. "Teams are not using the shared design tokens consistently, which means interfaces look different across products even when they should look the same. We need to clarify how components should be built and automated tools to detect when they drift from the standard."

### Anti-pattern 3: Asking for resources without business justification

**The mistake:** "We need a dedicated design systems team. Please allocate 1 FTE."

**Why it fails:** Readers have no context for whether 1 FTE is reasonable. You are asking them to trust your judgment, but you have not given them the information to make the decision.

**The fix:** Show the math. "Teams are spending an estimated [n] weeks per quarter on duplicated work. Dedicating 1 FTE ([cost]) to system maintenance will recover [n] weeks of duplicated effort, paying for itself in [timeline]. Without this investment, the duplicated work continues to compound."

### Anti-pattern 4: Presenting data without interpretation

**The mistake:** "The design system has 92 components. 34% of teams are using it. Average component adoption time is 3.2 weeks."

**Why it fails:** Raw metrics mean nothing without context. Is 34% adoption good or bad? Is 3.2 weeks fast or slow? The reader has to guess your conclusion.

**The fix:** Interpret the data. "The design system has 92 components covering the core patterns most teams need. However, only 34% of teams are actively using the system — the rest are either unaware it exists or finding it difficult to adopt. The average adoption time of 3.2 weeks is longer than target, suggesting we need better documentation or training."

### Anti-pattern 5: Mixing the ask with the situation

**The mistake:** Throughout the brief, references to multiple things being asked for — "We need governance," "We need a dedicated team," "We need better documentation," "We need tool investment."

**Why it fails:** A brief with six asks dilutes each one. The reader remembers none of them.

**The fix:** State three asks or fewer, and state them explicitly in the "What we need" section. Everything else in the brief should build the case for those three asks specifically.

### Anti-pattern 6: Overpromising outcomes

**The mistake:** "This investment will eliminate all design inconsistencies, reduce feature shipping time by 50%, and solve all accessibility compliance gaps."

**Why it fails:** Unrealistic promises create expectation debt. When you ship and the promised outcomes do not fully materialise, you lose trust permanently.

**The fix:** Be honest and specific. "This investment will establish consistent interface standards that new teams can use as their baseline, reducing the time to design consistency for new products from [current] weeks to [new] weeks. It will not eliminate legacy inconsistencies — addressing those is a separate effort. It will prevent new inconsistencies from accumulating."

---

## Step 8: Quality checks

Before delivering the brief, verify all of these:

- No design system jargon that is unexplained
- The situation section describes a business problem, not a design system metric
- A specific recommendation is present, not a general direction
- The ask is three items or fewer, each specific and actionable
- The brief fits on one page (approximately 400-500 words)
- A reader with no design systems background can understand the situation and the ask
- The expected outcome is honest about timeline and scope
- If maturity level is referenced, it is explained in plain terms with evidence
- If AI-readiness is referenced, the business value is framed in terms the audience understands (efficiency, speed, competitive positioning), not in technical terms
- Tone is calibrated to the audience (engineering vs. product vs. design vs. executive)
- The framing pattern (growth/risk/cost) matches the audience's priorities
- No anti-patterns from Step 7 are present

---

## Configuration for .ds-ops-config.yml

If this skill runs as part of a recurring workflow, configure it as follows:

```yaml
skills:
  stakeholder-brief:
    trigger: "quarterly-governance-review"  # or "on-demand"
    audience: "engineering-leadership"      # or "product-leadership", "design-leadership", "executive"
    framing: "cost"                         # or "growth", "risk"
    maturity_level: true                    # if a maturity assessment is available, reference it
    include_anti_patterns_check: true       # always include
```

For quarterly stakeholder briefs:
1. Schedule this skill to run after `system-health` completes
2. Pass the health assessment findings as input
3. Output is a brief ready for leadership distribution
4. Archive the brief in the project's decision record

---

## Platform and maturity framing (staff-level)

At the staff level, stakeholder briefs should frame the design system as infrastructure, not as a design convenience. This changes how the situation, recommendation, and outcome are written.

**AI-readiness as a competitive/efficiency argument:**
If relevant to the organisation, include the AI-readiness angle: "Design systems that are machine-readable enable AI-assisted development — code generation, automated testing, and design-to-code workflows. Our current system is not structured for AI consumption. The proposed investment includes making the system machine-readable, which positions the organisation to benefit from AI tooling without a separate initiative."

---

## Summary: From brief to decision

A stakeholder brief is only valuable if it leads to a decision. The brief should:

1. Be sent to the decision-maker (not their staff) directly
2. State when a decision is needed
3. Offer a follow-up conversation if there are questions
4. Arrive 5–7 days before the decision deadline (enough time to ask questions, not so early that it gets forgotten)

If the brief does not result in a decision after 2 weeks, follow up: "I wanted to check whether you have questions about the brief, or whether we need to adjust the proposal."

If the decision is no: ask why. Often the objection is not what was addressed in the brief — the brief revealed a different constraint.

If the decision is yes: confirm what changed, document it as a decision record, and set up the follow-up communication for consuming teams.
