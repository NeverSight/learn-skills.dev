---
name: status-updates
description: Draft status updates, launch notes, project reports, agendas, retrospectives, and stakeholder comms.
---

## Audience-Specific Update Formats

### Leadership / Executive Updates

Leaders need: strategic context, progress mapped to goals, risks that require their intervention, and decisions awaiting their input.

**Template**:
```
Status: [Green / Yellow / Red]

Summary: [Single sentence — the one thing they must know]

Progress:
- [Outcome delivered, linked to OKR or strategic goal]
- [Milestone completed, with business impact noted]
- [Key metric shift]

Risks:
- [Risk statement]: [Mitigation underway]. [Specific ask if applicable].

Decisions required:
- [Decision topic]: [Options with a recommendation]. Needed by [date].

Upcoming milestones:
- [Milestone] — [Target date]
```

**Guidance**:
- Open with the conclusion, not the process. Leaders want "we launched X and it moved metric Y" rather than a list of meetings and tickets.
- Stay under 200 words. They will ask for more if they want it.
- The status color should reflect your honest assessment. Yellow signals healthy risk awareness, not failure.
- Only surface risks where you need help. Omit risks you are already resolving unless leadership needs visibility.
- Requests must be precise: "Approve vendor choice by Thursday" rather than "need alignment."

### Engineering Team Updates

Engineers need: priority clarity, technical context, blocker resolution, and awareness of decisions affecting their work.

**Template**:
```
Shipped:
- [Feature or fix] — [Link to PR/ticket]. [Impact note if relevant].

In flight:
- [Work item] — [Owner]. [Expected delivery]. [Blockers if any].

Decisions:
- [Decided]: [Rationale]. [Link to ADR if available].
- [Pending]: [Background]. [Options]. [Recommended path].

Priority shifts:
- [What moved and the reason behind it]

On deck:
- [Upcoming items] — [Why these are sequenced next]
```

**Guidance**:
- Provide links to tickets, pull requests, and documents. Engineers want to drill into specifics.
- When priorities shift, explain the reasoning. Engineers invest more when they understand the why.
- Call out what is blocking them and describe your plan to clear it.
- Omit information that has no bearing on their work.

### Cross-Functional Partner Updates

Partners across design, marketing, sales, and support need: advance notice of changes affecting their teams, preparation requirements, and channels for input.

**Template**:
```
Upcoming:
- [Feature or launch] — [Date]. [Implications for your team].

Action items for your team:
- [Specific request] — [Context]. Needed by [date].

Decisions finalized:
- [Decision] — [How it impacts your workflow].

Open for feedback:
- [Topic where input is welcome] — [How to submit it].
```

### External / Customer-Facing Updates

Customers need: what is new, what is coming, how it benefits them, and how to take advantage of it.

**Template**:
```
What's new:
- [Capability] — [Benefit stated in customer language]. [Link or instructions].

On the roadmap:
- [Capability] — [Approximate timing]. [Why it matters to you].

Known issues:
- [Issue] — [Current status]. [Workaround if one exists].

Share your feedback:
- [Channel or method for submitting feature requests and feedback]
```

**Guidance**:
- Eliminate internal terminology. No ticket IDs. No architecture references.
- Frame everything around what the customer can now accomplish, not what your team built.
- Be candid about timelines without over-committing. "Later this quarter" is preferable to a date you might miss.
- Only include known issues if they are customer-visible and accompanied by a resolution path.

## Traffic Light Status Framework

### Definitions

**Green** (On Track):
- Work is proceeding according to plan
- No material risks or obstacles
- Commitments and deadlines will be met
- Reserve Green for when things are genuinely progressing well, not as a default

**Yellow** (At Risk):
- Progress has slowed or a risk has materialized
- Mitigation is in progress but the outcome remains uncertain
- Commitments may be missed without intervention or scope adjustment
- Flag Yellow early — the sooner risk is visible, the more options remain

**Red** (Off Track):
- Significantly behind schedule
- A major obstacle exists without a clear resolution
- Commitments will not be met without substantial intervention (scope reduction, additional resources, or timeline extension)
- Escalate to Red when your own options are exhausted and you need external help

### Transition Rules
- Shift to Yellow at the first indication of risk, not once you are certain things have gone wrong
- Shift to Red when you have used every lever available to you and require escalation
- Return to Green only after the underlying risk is genuinely resolved, not merely paused
- Always document the reason when changing status: "Moved to Yellow because [explanation]"

## Communicating Risk Effectively

### ROAM Classification
- **Resolved**: the risk no longer applies. Record how it was eliminated.
- **Owned**: the risk is recognized and someone is actively managing it. Name the owner and the mitigation approach.
- **Accepted**: the risk is acknowledged but the team proceeds without active mitigation. Capture the rationale.
- **Mitigated**: actions have reduced the risk to a tolerable level. Document what was done.

### Five-Step Risk Communication Pattern
1. **Name it plainly**: "There is a risk that [event] occurs because [cause]"
2. **Size the impact**: "If this materializes, the consequence is [specific impact]"
3. **Estimate probability**: "This is [likely / possible / unlikely] because [evidence]"
4. **Describe the response**: "We are addressing this by [actions taken or planned]"
5. **State the need**: "To further reduce this risk, we need [specific help or decision]"

### Pitfalls to Avoid
- Burying risks inside positive updates. When a risk is significant, lead with it.
- Vagueness: "We might see some delays" — always specify what could be delayed, by how long, and why.
- Presenting risks without accompanying action plans. Every risk should include a mitigation or a request.
- Late disclosure. A risk surfaced early is a planning input. A risk surfaced late becomes a crisis.

## Decision Records

### Lightweight ADR Structure

Record significant decisions for institutional memory:

```
# [Decision Title]

## Status

[Proposed / Accepted / Deprecated / Superseded by ADR-XXX]

## Situation

What circumstances necessitate this decision? What constraints and pressures exist?

## Resolution

What was decided? State the choice clearly and unambiguously.

## Tradeoffs

What follows from this decision?
- Benefits gained
- Downsides or compromises accepted
- Future possibilities opened or closed

## Options Evaluated

What alternatives were considered?
For each: a brief description and the reason it was not chosen.
```

### When to Create a Decision Record
- Strategic product choices (target market, platform support, pricing model)
- Major technical decisions (architecture direction, vendor selection, build vs. buy)
- Contested decisions where the team disagreed (preserve the reasoning for posterity)
- Decisions that narrow future flexibility (technology lock-in, partnership commitments)
- Decisions you anticipate will be questioned later (capture context while it is fresh)

### Practical Tips
- Write the record close to the moment the decision is made, not weeks afterward
- Note who participated and who held final decision authority
- Document the surrounding context generously — future readers will lack today's situational awareness
- Records that prove wrong in hindsight are still valuable; add a "superseded by" reference
- Brevity is an asset. A single page is better than five.

## Meeting Facilitation Patterns

### Daily Sync / Stand-up
**Goal**: uncover blockers, synchronize efforts, sustain momentum.

Each participant shares:
- Work completed since the last sync
- Current focus
- Anything blocking progress

**Running it well**:
- Cap at 15 minutes. Park longer discussions for follow-up.
- Prioritize blockers — they are the highest-leverage item in any standup
- Track blockers explicitly and follow up until resolved
- Skip the meeting if there is nothing to synchronize. Protect people's time.

### Iteration / Sprint Planning
**Goal**: agree on the work for the upcoming cycle and align on scope and priorities.

Agenda:
1. Retrospective glance: what shipped, what carried over, what was descoped
2. Priority declaration: the most important outcomes for the coming sprint
3. Capacity assessment: realistic bandwidth accounting for PTO, on-call duties, and meetings
4. Commitment selection: pull items from the backlog that fit capacity and priority
5. Dependency mapping: flag anything requiring cross-team or external coordination

**Running it well**:
- Arrive with a proposed priority ranking. Do not ask the team to sort from zero.
- Resist overcommitment. Delivering less reliably builds more trust than consistently missing targets.
- Every selected item needs a clear owner and unambiguous acceptance criteria.
- Surface items with hidden complexity or insufficient scoping.

### Retrospective
**Goal**: reflect honestly on what worked, what did not, and what the team will change.

Flow:
1. Frame the conversation: recall the sprint goal and establish psychological safety
2. Collect observations: what went well, what fell short, what caused confusion
3. Identify patterns: find recurring themes and root causes
4. Select improvements: commit to 1-3 concrete changes for the next cycle
5. Close: acknowledge the team's candor

**Running it well**:
- Psychological safety is non-negotiable. People must feel safe to speak honestly.
- Direct attention toward systems and processes, never toward individuals.
- Cap action items at 1-3. More than that and nothing gets implemented.
- Revisit prior retrospective actions. If follow-through never happens, engagement erodes.
- Rotate the retrospective format periodically to maintain freshness.

### Stakeholder Demo / Review
**Goal**: demonstrate progress, solicit feedback, reinforce alignment.

Flow:
1. Set context: remind stakeholders of the objective and what they saw previously
2. Live demo: show the working product, not slide decks
3. Data share: present any early metrics or user feedback
4. Structured feedback: guide questions toward specific topics
5. Forward look: preview what comes next and when the next review will occur

**Running it well**:
- Always demo the real product when possible. Slides are not substitutes.
- Direct feedback requests precisely: "What is your reaction to X?" outperforms "Any thoughts?"
- Capture feedback visibly and commit to addressing each item or explaining why it will not be addressed
- Clarify what type of feedback is actionable at the current stage
