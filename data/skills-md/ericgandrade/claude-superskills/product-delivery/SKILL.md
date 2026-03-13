---
name: product-delivery
description: This skill should be used when the user needs to ship, measure, and learn effectively. Use when planning staged rollouts, setting up metrics hierarchies, running bet retrospectives, or executing GTM launches. Part of the Modern Product Operating Model collection.
license: MIT
---

# Product Delivery System

> "The goal isn't shipping. The goal is learning whether your bet was right."

This skill covers the **Delivery System** — how we ship, measure, and learn. It runs discovery and delivery in parallel (dual-track), ships with staged rollouts, measures with a clear hierarchy, reflects through retrospectives, and executes GTM with precision.


**Related skills**: `product-strategy`, `product-discovery`, `product-architecture`, `ai-native-product`, `product-leadership`

---

## When to Use This Skill

Use this skill when:
- Planning how to roll out a new feature or product
- Designing a metrics hierarchy for a bet or product
- Running bet retrospectives after shipping
- Executing GTM launches
- Setting up dual-track development rhythm
- Deciding when to scale, iterate, or kill a bet

**Cadence**: Continuous | **Owner**: Product Trio + GTM Team

---

## The Problem This Solves

Most teams either:
1. Ship features and never measure impact
2. Measure vanity metrics that don't connect to outcomes
3. Do "big bang" launches that create risk
4. Never officially conclude bets—zombies live forever
5. Treat GTM as marketing's problem after PM ships

The Delivery System ensures **shipping is the beginning of learning, not the end**.

---

## Philosophy

### Core Beliefs

1. **Discovery and delivery run in parallel** — Don't pause discovery to deliver
2. **Staged rollouts are the default** — Ship to 10% before 100%
3. **Metrics exist in hierarchy** — Leading → Core → Lagging
4. **Every bet gets a retrospective** — Explicit scale/iterate/kill decision
5. **GTM is a product responsibility** — PM owns adoption, not just availability

### What This Framework Rejects

- Ship and forget (no measurement)
- Big bang launches (maximum risk)
- Vanity metrics (activity without outcome)
- Zombie bets (never concluded, never killed)
- Throwing features over the wall to marketing

---

## Progress Tracking

Display progress during delivery planning:

```
[████░░░░░░░░░░░░░░░░] 25% — Phase 1/4: Rollout Planning & Risk Assessment
[████████░░░░░░░░░░░░] 50% — Phase 2/4: Metrics Hierarchy & GTM Coordination
[████████████░░░░░░░░] 75% — Phase 3/4: Launch Execution & Monitoring
[████████████████████] 100% — Phase 4/4: Bet Retrospective & Learning Loop
```

## Framework Components

### 1. Dual-Track Development

**The Core Idea:**
Discovery and delivery happen simultaneously. While one bet is being built, the next bet is being shaped.

```
Week 1    Week 2    Week 3    Week 4    Week 5    Week 6
─────────────────────────────────────────────────────────
[  Discover Bet B  ][  Shape Bet B  ][  Discover Bet C  ]
         [    Build Bet A    ][   Build Bet B   ]
                    [ Ship A ]        [ Ship B ]
```

**How It Works:**

| Track | Activities | Who |
|-------|------------|-----|
| **Discovery Track** | Interviews, OST updates, solution exploration, assumption tests | Full trio (PM heavy) |
| **Delivery Track** | Building, testing, shipping, measuring | Full trio (Eng heavy) |

**Time Allocation (Example):**

| Role | Discovery | Delivery |
|------|-----------|----------|
| PM | 60% | 40% |
| Designer | 50% | 50% |
| Tech Lead | 30% | 70% |

**Coordination Points:**
- **Weekly sync**: What's in flight on each track
- **Handoff moment**: When a bet moves from "shaped" to "building"
- **Learning moment**: When shipped bet results inform discovery

**0→1 Mode**: Tracks may blur. Everyone does everything. Speed > separation.

**Scaling Mode**: Clear separation. Dedicated discovery time. Research ops support.

---

### 2. Staged Rollout

**The Core Idea:**
Never ship to everyone at once. Start small, learn, expand.

**Default Rollout Stages:**

| Stage | Audience | Duration | Purpose |
|-------|----------|----------|---------|
| **Stage 0: Internal** | Team dogfooding | 1-3 days | Find obvious bugs |
| **Stage 1: Alpha** | 5-10 friendly customers | 1 week | Qualitative feedback |
| **Stage 2: Beta** | 10% of users | 1-2 weeks | Quantitative signal |
| **Stage 3: GA** | 100% of users | Ongoing | Full measurement |

**Progression Criteria:**

| From | To | Criteria |
|------|----|----------|
| Internal → Alpha | Ready for external | No P0 bugs, core flow works |
| Alpha → Beta | Validated experience | Positive qualitative feedback, no major usability issues |
| Beta → GA | Metrics acceptable | Leading metrics trending right, no guardrail breaches |

**Feature Flags:**
- Every significant feature ships behind a flag
- Flags enable instant rollback
- Flags enable % rollout control
- Flags are cleaned up after GA (don't accumulate debt)

**Rollback Triggers:**
- Guardrail metric breached
- Error rate > threshold
- Customer-reported critical issue
- Leading metrics trending wrong

**0→1 Mode**: Stages can be compressed. Alpha might be 3 customers for 2 days.

**Scaling Mode**: Formal stage gates. Release management. Beta programs.

---

### 3. Metrics Hierarchy

**The Three-Tier Model:**

```
┌─────────────────────────────────────────────────────┐
│                 LAGGING METRICS                     │
│         (Revenue, Retention, NPS)                   │
│         Move slowly, hard to attribute              │
├─────────────────────────────────────────────────────┤
│                  CORE METRICS                       │
│       (Activation, Engagement, Conversion)          │
│       The outcomes your bets target                 │
├─────────────────────────────────────────────────────┤
│                LEADING METRICS                      │
│         (Feature adoption, Task completion)         │
│         Move fast, early signal                     │
└─────────────────────────────────────────────────────┘
```

**Metric Types:**

| Type | Definition | Example | Use For |
|------|------------|---------|---------|
| **Leading** | Early signal, fast-moving, directly influenced by feature | Feature adoption rate, task completion rate | Weekly decisions, rollout gates |
| **Core** | Primary outcome you're targeting | Activation rate, conversion rate, engagement score | Bet success criteria |
| **Lagging** | Business results, slow-moving, influenced by many factors | Revenue, retention, NPS | Quarterly/annual planning |
| **Guardrail** | Metrics you won't let degrade | Performance, error rate, support tickets | Rollout gates, rollback triggers |

**Hierarchy Example (Activation Bet):**

```
Lagging:    Revenue growth (quarterly)
               ↑
Core:       Activation rate (weekly)
               ↑
Leading:    Onboarding completion (daily)
            First value action (daily)
               ↑
Guardrail:  Support tickets (daily)
            Error rate (real-time)
```

**Metric Selection Criteria:**

| Criterion | Question |
|-----------|----------|
| **Measurable** | Can we actually track this? |
| **Actionable** | Can we influence it with our work? |
| **Attributable** | Can we connect changes to our bet? |
| **Timely** | Will we see signal fast enough to decide? |

**Dashboard Design:**
- Leading metrics: Real-time or daily
- Core metrics: Weekly view with trend
- Lagging metrics: Monthly/quarterly view
- Guardrails: Alerting, not just reporting

---

### 4. Bet Retrospectives

**The Core Idea:**
Every bet concludes with an explicit decision: Scale, Iterate, or Kill.

**Retrospective Format:**

```
BET RETROSPECTIVE: [Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Timebox: [Duration] | Shipped: [Date]

HYPOTHESIS REVIEW
Original: "We believed [X] would result in [Y]"
Result: [ ] Confirmed  [ ] Disproved  [ ] Inconclusive

METRICS REVIEW
| Metric    | Target | Actual | Verdict |
|-----------|--------|--------|---------|
| Primary   | [X]    | [Y]    | ✅ / ❌  |
| Secondary | [X]    | [Y]    | ✅ / ❌  |
| Guardrail | [X]    | [Y]    | ✅ / ❌  |

KEY LEARNINGS
• [Learning 1]
• [Learning 2]
• [Learning 3]

DECISION: [ ] SCALE  [ ] ITERATE  [ ] KILL

NEXT STEPS
• [Action 1]
• [Action 2]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Decision Framework:**

| Outcome | Criteria | Action |
|---------|----------|--------|
| **SCALE** | Primary metric hit, no guardrail issues | Expand rollout, invest more |
| **ITERATE** | Signal positive but not at target | Refine and re-test (one more cycle) |
| **KILL** | Hypothesis disproved or too costly | Stop investment, document learning |

**Iteration Limits:**
- Maximum 2-3 iteration cycles before forcing Scale or Kill
- Each iteration must have a new hypothesis
- Time-bound iterations (don't let them drag)

**Retrospective Cadence:**
- Run at timebox end, regardless of "completion"
- Include full trio + relevant stakeholders
- 30-60 minutes maximum
- Document in central repository

**0→1 Mode**: Informal but still explicit. Even a Slack message: "Bet X result: [Y]. Decision: [Z]."

**Scaling Mode**: Formal retrospective meetings. Learning database. Cross-team sharing.

---

### 5. GTM Execution

**The Core Idea:**
PM owns adoption, not just availability. GTM is part of delivery, not an afterthought.

**GTM Components:**

| Component | Owner | Timing |
|-----------|-------|--------|
| **Positioning & messaging** | PMM / PM | During solution shaping |
| **Sales enablement** | PMM / PM | Before beta |
| **Documentation** | PM / Tech Writer | Before beta |
| **Support training** | PM / Support Lead | Before GA |
| **Launch communications** | PMM / Marketing | At GA |
| **Customer success playbook** | CS / PM | Before GA |

**Launch Tiers:**

| Tier | Definition | GTM Effort |
|------|------------|------------|
| **Tier 1** | Major new capability, strategic priority | Full GTM: press, event, sales training, campaign |
| **Tier 2** | Significant improvement, notable value | Moderate GTM: blog, email, sales brief |
| **Tier 3** | Incremental improvement, quality of life | Light GTM: changelog, in-app, support brief |
| **Tier 4** | Bug fix, minor enhancement | No GTM: release notes only |

**Launch Checklist (Tier 1/2):**

| Phase | Tasks |
|-------|-------|
| **Pre-launch** | Positioning defined, Sales trained, Support trained, Docs ready, Success playbook ready |
| **Launch** | Announcement sent, In-app messaging live, Sales notified, Support notified |
| **Post-launch** | Feedback monitored, Metrics tracked, Issues triaged, Iteration planned |

**Adoption Metrics (PM Responsibility):**

| Metric | Definition |
|--------|------------|
| **Awareness** | % of target users who know feature exists |
| **Trial** | % of aware users who try feature |
| **Adoption** | % of trial users who continue using |
| **Habit** | % of adopters using regularly |

**0→1 Mode**: PM does GTM. Scrappy launches. Focus on learning, not polish.

**Scaling Mode**: PMM partnership. Launch playbooks. Integrated marketing calendar.

---

## Key Outputs

| Output | Description | Update Cadence |
|--------|-------------|----------------|
| **Rollout plan** | Staged rollout with progression criteria | Per bet |
| **Metrics dashboard** | Leading, core, lagging, guardrail metrics | Continuous |
| **Bet retrospective** | Scale/Iterate/Kill decision with learnings | At timebox end |
| **GTM checklist** | Launch activities by tier | Per launch |
| **Learning repository** | Archive of bet results and learnings | After each retrospective |

---

## Templates

This skill includes templates in the `templates/` directory:
- `rollout-plan.md` — Staged rollout checklist
- `metrics-hierarchy.md` — Metrics design template
- `bet-retrospective.md` — Retrospective format and decision framework
- `launch-checklist.md` — GTM execution checklist by tier

---

## Using This Skill with Claude

Ask Claude to:

1. **Design rollout plan**: "Create a staged rollout plan for [feature]"
2. **Build metrics hierarchy**: "Design a metrics hierarchy for [bet/product]"
3. **Set success criteria**: "What metrics should determine success for [bet]?"
4. **Plan retrospective**: "Create a retrospective agenda for [bet] that shipped [X]"
5. **Analyze results**: "Given these metrics, should we scale, iterate, or kill?"
6. **Design launch tier**: "What launch tier should [feature] be? What GTM is needed?"
7. **Create launch checklist**: "Build a GTM checklist for [Tier X] launch"
8. **Identify guardrails**: "What guardrail metrics should we watch for [bet]?"
9. **Plan dual-track**: "Help me design a dual-track rhythm for [team size]"
10. **Write changelog**: "Write release notes for [feature] at [tier]"

---

## Connection to Other Skills

| When you need to... | Use skill |
|---------------------|-----------|
| Define what metrics ladder up to | `product-strategy` |
| Validate before delivery | `product-discovery` |
| Define what you're delivering | `product-architecture` |
| Adapt delivery for AI products | `ai-native-product` |
| Scale delivery across teams | `product-leadership` |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Ship and forget** | No learning, no improvement | Measure and retrospect |
| **Big bang launch** | Maximum risk, no learning | Staged rollout |
| **Vanity metrics** | Activity ≠ outcome | Hierarchical metrics |
| **Zombie bets** | Resources trapped, no clarity | Explicit Scale/Iterate/Kill |
| **GTM afterthought** | Features available but not adopted | GTM as part of delivery |
| **Perfectionism** | Never ships, never learns | Timebox and ship |

---

## Quick Reference: Delivery Quality Checklist

Before GA:

- [ ] **Rollout staged** — Not shipping to 100% first
- [ ] **Feature flagged** — Can roll back instantly
- [ ] **Metrics instrumented** — Can measure leading/core/lagging
- [ ] **Guardrails defined** — Know what triggers rollback
- [ ] **GTM prepared** — Docs, training, comms ready
- [ ] **Retrospective scheduled** — Date on calendar at timebox end
- [ ] **Success criteria agreed** — Team knows what Scale/Iterate/Kill means

---

## Sources & Influences

- **Marty Cagan** — INSPIRED, EMPOWERED
- **Eric Ries** — The Lean Startup
- **Teresa Torres** — Continuous Discovery Habits
- **April Dunford** — Obviously Awesome (for GTM)

---

