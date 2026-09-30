---
name: roadmap-planning
description: Plan and prioritize roadmaps with RICE, ICE, value-effort scoring, sequencing, and capacity tradeoffs.
---

## Roadmap Formats

Choose the format that matches your audience and planning horizon.

### Now / Next / Later

A time-horizon approach that avoids false date precision:

- **Now** (active sprint or current month): Work the team is executing. Scope and delivery confidence are high.
- **Next** (one to three months out): Prioritized and roughly scoped. The "what" is clear; the "when" carries some uncertainty.
- **Later** (three to six months and beyond): Strategic intentions and directional bets. Scope and timing remain deliberately flexible.

Best suited for: external communication, leadership updates, and teams that want to avoid locking into specific dates prematurely.

### Thematic Quarterly Plans

Structure each quarter around two or three investment themes:

- Themes articulate strategic focus areas (examples: "Self-serve onboarding", "Enterprise security posture", "Developer ecosystem growth")
- Individual initiatives roll up under each theme
- Themes should trace to company or team-level objectives and key results
- This format foregrounds the strategic "why" behind every initiative

Best suited for: executive reviews, planning cycles, and demonstrating alignment between execution and strategy.

### OKR-Driven Roadmaps

Wire every roadmap item directly to an Objective and Key Result:

- Begin with the team's OKRs for the planning period
- Beneath each Key Result, enumerate the initiatives expected to move that metric
- Annotate each initiative with its anticipated contribution to the Key Result
- This creates a direct accountability chain between delivery and measurement

Best suited for: organizations that run OKR processes and want a tight feedback loop between building and measuring.

### Gantt / Timeline View

Calendar-oriented layout showing durations, parallelism, and sequencing:

- Displays start dates, end dates, and work duration for each initiative
- Reveals resource conflicts and scheduling bottlenecks
- Exposes inter-item dependencies visually
- Highlights where parallel workstreams converge

Best suited for: engineering coordination and resource allocation discussions. Avoid sharing externally, as calendar precision sets rigid expectations.

## Scoring and Prioritization Models

### RICE Scoring

Quantify priority using four dimensions: Score = (Reach x Impact x Confidence) / Effort

- **Reach**: Number of users or customers affected within a defined period. Use concrete estimates ("800 accounts per quarter").
- **Impact**: Degree of change for each person reached. Scale: 3 = transformative, 2 = significant, 1 = moderate, 0.5 = minor, 0.25 = negligible.
- **Confidence**: Certainty in the reach and impact estimates. 100% = data-backed, 80% = reasonable evidence, 50% = informed guess.
- **Effort**: Total person-months across all functions (engineering, design, research, etc.).

Best suited for: comparing a large backlog with quantitative rigor. Less effective for bold strategic bets where impact is inherently speculative.

### ICE Scoring

A streamlined alternative when detailed data is unavailable. Rate each item 1-10 on three axes:

- **Impact**: Expected movement on the target metric
- **Confidence**: Reliability of the impact estimate
- **Ease**: Implementation simplicity (inverse of effort; higher means simpler)

Score = Impact x Confidence x Ease

Best suited for: rapid backlog triage, early-stage products, or situations where RICE inputs are unavailable.

### MoSCoW Classification

Sort initiatives into four buckets to force prioritization dialogue:

- **Must have**: The plan fails without these. They represent non-negotiable commitments.
- **Should have**: High-value and expected, but the plan remains viable if they slip.
- **Could have**: Welcomed if capacity exists. Dropping them does not affect the timeline.
- **Won't have**: Deliberately excluded for this period. Listing them removes ambiguity.

Best suited for: release scoping and negotiation sessions with stakeholders who need to see what trades are being made.

### Value vs. Effort Quadrant

Visualize initiatives on a two-by-two grid:

- **High value, Low effort** (Quick wins): Execute immediately. These are the highest-leverage items.
- **High value, High effort** (Strategic investments): Commit resources deliberately. Worth the cost but need careful planning.
- **Low value, Low effort** (Opportunistic fills): Pick these up during slack periods or between larger efforts.
- **Low value, High effort** (Traps): Remove from consideration. They consume resources with minimal return.

Best suited for: collaborative planning sessions where the team needs shared visual alignment on tradeoffs.

## Dependency Management

### Taxonomy of Dependencies

Scan for dependencies across these categories:

- **Technical**: Initiative B relies on infrastructure or platform changes delivered by Initiative A
- **Cross-team**: Work requires deliverables from design, platform, data engineering, or other product teams
- **External**: Blocked on a vendor deliverable, partner integration, or third-party API
- **Informational**: Requires the output of a research spike, user study, or data analysis before work can begin
- **Sequential**: Feature A must ship before Feature B can start due to shared surfaces or user flow constraints

### Handling Dependencies Effectively

- Surface every dependency explicitly in the roadmap artifact
- Designate a single owner responsible for tracking and resolving each dependency
- Establish a "needed by" date: when must the upstream deliverable land for the downstream item to stay on schedule
- Pad timelines around dependencies -- they represent the highest-risk nodes in any plan
- Escalate cross-team dependencies early; coordination overhead grows with delay
- Prepare fallback plans: what is the alternative path if a dependency slips?

### Strategies to Minimize Dependencies

- Explore whether a reduced-scope version sidesteps the dependency entirely
- Use interface contracts or mocks to enable parallel development
- Reorder the sequence so the dependency resolves earlier in the timeline
- Absorb the dependent work into your own team to eliminate coordination overhead

## Team Capacity Planning

### Estimating Available Capacity

- Start with headcount and the planning window
- Deduct known overhead: recurring meetings, on-call rotations, hiring loops, holidays, planned time off
- A practical baseline: engineers typically invest 60-70% of their time on planned roadmap work
- Account for ramp time when new team members join mid-cycle

### Allocation Guidelines

A balanced split for most product teams:

- **70% strategic delivery**: Roadmap initiatives that advance business objectives
- **20% infrastructure health**: Technical debt reduction, reliability hardening, performance tuning, developer tooling
- **10% reserve**: Buffer for urgent requests, incoming escalations, and small-scope opportunities

Adjust the ratios based on context:

- Newer products warrant heavier feature investment and lighter debt work
- Mature products benefit from increased reliability and scalability spending
- Post-incident periods call for elevated infrastructure attention
- Hyper-growth phases demand investment in scalability and operational resilience

### Balancing Ambition and Reality

- When planned commitments exceed available capacity, scope must shrink -- not expectations of individual output
- Adopt a standing rule: adding an initiative to the plan requires removing or deferring another
- Delivering fewer commitments reliably builds more organizational trust than overcommitting and missing dates

## Communicating Roadmap Shifts

### Triggers for Roadmap Revisions

- A new strategic directive from leadership
- User research or customer feedback that reshuffles priorities
- Engineering discovery that materially changes effort estimates
- A dependency from another team slipping its timeline
- Team composition changes: growth, attrition, or key departures
- A competitive development demanding a response

### Communicating Changes Clearly

1. **State the change directly**: What is moving, and in which direction
2. **Explain the catalyst**: What new information prompted this decision
3. **Surface the tradeoff**: What was deprioritized or deferred to accommodate the shift
4. **Present the revised plan**: Updated roadmap reflecting the new state
5. **Address affected parties**: Stakeholders who were counting on deprioritized items deserve direct communication

### Maintaining Stability

- Not every new data point warrants a roadmap revision. Establish a materiality threshold before making changes.
- Consolidate adjustments at natural cadence points (monthly or quarterly) unless genuinely urgent.
- Distinguish strategic reprioritization (roadmap change) from normal execution refinement (scope adjustment within an initiative).
- Track the frequency of roadmap changes. Excessive churn may indicate strategic ambiguity rather than adaptive planning.
