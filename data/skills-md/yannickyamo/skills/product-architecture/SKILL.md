---
name: product-architecture
description: Structure what you're building and why now. Use when organizing products into capability blocks, creating bet backlogs, building roadmaps, or writing solution briefs. Part of the Modern Product Operating Model collection.
author: YannickMaurice
version: 1.0.0
tags: product-management, roadmap, backlog, solution-brief, product-architecture
---

# Product Architecture System

> "A roadmap is not a feature list. It's a sequence of bets on how to create value."

This skill covers the **Product System** — structuring what you're building and why now. It turns validated opportunities into bets, organizes work into capability blocks, and creates roadmaps that communicate strategy without false precision.

**Part of**: [Modern Product Operating Model](https://github.com/yannickYamo/skills) — a collection of composable product skills.

**Related skills**: `product-strategy`, `product-discovery`, `product-delivery`, `ai-native-product`, `product-leadership`

---

## When to Use This Skill

Use this skill when:
- Organizing your product into capability blocks
- Converting discovery opportunities into prioritized bets
- Building or updating your roadmap
- Writing solution briefs before engineering commits
- Preparing for planning cycles (quarterly, annually)
- Communicating product direction to stakeholders

**Cadence**: Quarterly planning, ongoing refinement | **Owner**: PM with trio input

---

## The Problem This Solves

Most teams have:
1. Feature lists masquerading as roadmaps
2. No clear connection between strategy and what gets built
3. Solution briefs that are either too vague or too prescriptive
4. Backlogs organized by urgency, not impact

The Product Architecture System creates a **clear hierarchy**: Strategy → Bets → Blocks → Features, with traceable connections at each level.

---

## Philosophy

### Core Beliefs

1. **Bets over features** — We're not building features, we're placing bets on outcomes
2. **Roadmaps show direction, not dates** — Commitments are for sprints, not quarters
3. **Problems before solutions** — Every bet must connect to a validated opportunity
4. **Solution briefs over PRDs** — Just enough spec to start, emergent detail through building
5. **Blocks organize complexity** — Group capabilities by customer value, not technical architecture

### What This Framework Rejects

- Feature factories (build what's requested, not what matters)
- Date-driven roadmaps (false precision creates false expectations)
- Disconnected backlogs (no traceability to strategy)
- Waterfall PRDs (200-page specs nobody reads)
- Tech-driven architecture (organizing by system, not customer)

---

## Framework Components

### 1. Product Blocks & Features

**What is a Block?**

A block is a capability area that delivers distinct customer value. Blocks organize your product by what customers can accomplish, not by technical architecture.

**Good Block Examples:**
- "Onboarding" (helps users get started)
- "Reporting" (helps users understand performance)
- "Collaboration" (helps teams work together)
- "Integrations" (connects to existing workflows)

**Bad Block Examples (Tech-Driven):**
- "Backend services"
- "API layer"
- "Database module"

**Block Portfolio View:**

| Block | Owner | Maturity | Strategic Priority | Active Bets |
|-------|-------|----------|-------------------|-------------|
| Onboarding | [PM] | Growth | P1 | 2 |
| Reporting | [PM] | Mature | P2 | 1 |
| Collaboration | [PM] | New | P1 | 3 |
| Integrations | [PM] | Growth | P3 | 0 |

**Block Maturity Stages:**

| Stage | Definition | Focus |
|-------|------------|-------|
| **New** | Unproven, high uncertainty | Find PMF within block |
| **Growth** | Validated, expanding | Scale and optimize |
| **Mature** | Stable, well-understood | Maintain, incremental improvements |
| **Sunset** | Declining value | Deprecate or replace |

**Features Within Blocks:**

Each block contains features. Features are the specific capabilities users interact with.

```
BLOCK: Reporting
├── Feature: Dashboard builder
├── Feature: Scheduled reports
├── Feature: Export to PDF
└── Feature: Custom metrics
```

**0→1 Mode**: One block, maybe two. Don't over-structure before you have PMF.

**Scaling Mode**: Multiple blocks with clear owners. Block health reviews quarterly.

---

### 2. The Bet Backlog

**What is a Bet?**

A bet is a time-boxed investment with a hypothesis, success metrics, and kill criteria. Unlike features, bets explicitly acknowledge uncertainty.

**Bet Format:**

```
BET: [Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hypothesis: We believe that [action] will result in [outcome]
Target metric: [Metric] from [baseline] to [target]
Timebox: [Duration]
Block: [Which block this belongs to]
Opportunity: [Link to validated opportunity in OST]
Kill criteria: [When we stop]
Scale criteria: [When we double down]
Effort: [T-shirt size]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Bet Categories:**

| Category | Description | Example |
|----------|-------------|---------|
| **Value creation** | New capabilities that solve customer problems | New reporting feature |
| **Growth** | Acquisition, activation, expansion | Onboarding improvements |
| **Platform** | Infrastructure, scalability, efficiency | Performance optimization |
| **Trust** | Security, compliance, reliability | SOC 2 certification |
| **Moat** | Building defensibility | Proprietary data features |

**Portfolio Balance:**

| Category | Target Allocation | Rationale |
|----------|-------------------|-----------|
| Core (proven, incremental) | 70% | Keep the lights on, serve existing customers |
| Adjacent (related, moderate risk) | 20% | Expand to new use cases or segments |
| Transformational (new, high risk) | 10% | Explore future opportunities |

**Bet Prioritization:**

Use ICE, RICE, or simple compare-and-contrast:

| Bet | Impact | Confidence | Effort | Score | Priority |
|-----|--------|------------|--------|-------|----------|
| A | High | High | Medium | [X] | P0 |
| B | High | Low | Low | [X] | P1 |
| C | Medium | High | Low | [X] | P1 |

**Backlog Rules:**
- Every bet traces to a validated opportunity
- Maximum 3 P0 bets at any time
- Bets without kill criteria don't make the backlog
- Review and reprioritize quarterly (or when evidence changes)

---

### 3. Roadmap

**Roadmap Philosophy:**

> A roadmap is a communication tool, not a contract. It shows direction and priorities, not delivery dates.

**Roadmap Formats:**

| Format | Audience | Purpose |
|--------|----------|---------|
| **Now / Next / Later** | Team, stakeholders | Current priorities without dates |
| **Quarterly themes** | Executives, board | Strategic direction by time horizon |
| **Outcome roadmap** | Team, stakeholders | What outcomes we're targeting when |

**Now / Next / Later Format:**

```
NOW (Current quarter - high confidence)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• [Bet A] — [Brief description]
• [Bet B] — [Brief description]

NEXT (Next quarter - medium confidence)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• [Bet C] — [Brief description]
• [Bet D] — [Brief description]

LATER (Future - low confidence, subject to change)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• [Bet E] — [Brief description]
• [Bet F] — [Brief description]
```

**Quarterly Themes Format:**

| Quarter | Theme | Key Bets | Target Outcome |
|---------|-------|----------|----------------|
| Q1 | "Foundation" | [Bets] | [Outcome metric] |
| Q2 | "Scale" | [Bets] | [Outcome metric] |
| Q3 | "Expand" | [Bets] | [Outcome metric] |
| Q4 | "Optimize" | [Bets] | [Outcome metric] |

**Outcome Roadmap Format:**

Instead of showing features, show outcomes:

| Timeframe | Outcome | How We'll Know | Key Bets |
|-----------|---------|----------------|----------|
| Q1 | Improve activation rate | 30% → 45% | [Bets focused on this] |
| Q2 | Reduce churn | 5% → 3% | [Bets focused on this] |
| H2 | Enter new segment | 10 customers | [Bets focused on this] |

**Roadmap Anti-Patterns:**

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| Date commitments | Creates false expectations | Time horizons (Now/Next/Later) |
| Feature lists | No strategic context | Outcome-focused themes |
| Too detailed | Can't see forest for trees | High-level, drill down on request |
| Never updated | Becomes fiction | Review quarterly minimum |
| No trade-offs visible | Hides resource constraints | Show what we're NOT doing |

**0→1 Mode**: 4-6 week horizon max. Roadmap changes weekly. Focus on learning milestones.

**Scaling Mode**: Quarterly themes. Public roadmap for customers. Cross-team dependencies tracked.

---

### 4. Solution Briefs

**What is a Solution Brief?**

A solution brief is a lightweight spec that provides enough context to start building without over-prescribing the solution. It replaces heavyweight PRDs.

**Solution Brief Format:**

```
SOLUTION BRIEF: [Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONTEXT
• Bet: [Link to bet]
• Opportunity: [Link to validated opportunity]
• Block: [Which block]

THE PROBLEM
[2-3 sentences on what problem we're solving and for whom]

CUSTOMER QUOTE
"[Actual quote from discovery]"

SUCCESS METRICS
• Primary: [Metric] from [baseline] to [target]
• Secondary: [Metric]
• Guardrail: [What we won't let degrade]

SOLUTION APPROACH
[High-level description of approach — NOT detailed specs]

KEY DECISIONS MADE
• [Decision 1]: [Rationale]
• [Decision 2]: [Rationale]

OPEN QUESTIONS
• [Question 1]
• [Question 2]

CONSTRAINTS
• Must: [Non-negotiable requirements]
• Must not: [Explicit exclusions]
• Timeline: [If relevant]

ASSUMPTIONS TO VALIDATE
• [Assumption 1]
• [Assumption 2]

OUT OF SCOPE
• [What we're explicitly NOT doing]
• [What we're explicitly NOT doing]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Solution Brief Principles:**

| Principle | Why |
|-----------|-----|
| Problem first | Everyone must understand WHY before HOW |
| Customer evidence | Grounds the work in reality |
| Metrics up front | Defines success before building |
| Open questions explicit | Acknowledges uncertainty |
| Out of scope clear | Prevents scope creep |

**What NOT to Include:**
- Detailed UI specs (emerge through design process)
- Technical implementation details (engineering decides)
- Project timelines (delivery system handles)
- Edge cases (discover through building)

**Brief Evolution:**

| Stage | Detail Level | Who Owns |
|-------|--------------|----------|
| **Draft** | Problem + metrics + high-level approach | PM |
| **Shaped** | + Key decisions + constraints | PM + Design |
| **Ready** | + Engineering input on feasibility | Trio |
| **In progress** | Living doc, updated as we learn | Trio |

**0→1 Mode**: Brief can be a Slack message or Notion doc. Speed > formality.

**Scaling Mode**: Template enforced. Linked to bet tracking. Archive for future reference.

---

## Key Outputs

| Output | Description | Update Cadence |
|--------|-------------|----------------|
| **Block portfolio** | Map of capability areas with owners | Quarterly |
| **Bet backlog** | Prioritized list of bets | Weekly refinement, quarterly reprioritization |
| **Roadmap** | Now/Next/Later or quarterly themes | Monthly update, quarterly refresh |
| **Solution briefs** | Lightweight specs for active bets | As bets move to building |

---

## Templates

This skill includes templates in the `templates/` directory:
- `block-portfolio.md` — Block inventory and health tracking
- `bet-backlog.md` — Bet format and prioritization
- `roadmap.md` — Now/Next/Later and quarterly themes
- `solution-brief.md` — Lightweight spec template

---

## Using This Skill with Claude

Ask Claude to:

1. **Design block structure**: "Help me organize [product] into capability blocks"
2. **Convert opportunity to bet**: "Turn this opportunity into a bet with hypothesis and metrics"
3. **Prioritize bets**: "Help me prioritize these bets using [framework]"
4. **Create roadmap**: "Build a Now/Next/Later roadmap from these bets"
5. **Review roadmap**: "Critique this roadmap for common anti-patterns"
6. **Write solution brief**: "Create a solution brief for [bet]"
7. **Scope solution**: "What should be in vs. out of scope for [bet]?"
8. **Define success metrics**: "What metrics should we track for [bet]?"
9. **Plan quarterly themes**: "Help me define themes for the next 4 quarters"
10. **Balance portfolio**: "Is my bet portfolio balanced? What's missing?"

---

## Connection to Other Skills

| When you need to... | Use skill |
|---------------------|-----------|
| Define strategy that informs bets | `product-strategy` |
| Validate opportunities before betting | `product-discovery` |
| Plan delivery and measurement | `product-delivery` |
| Adapt for AI product bets | `ai-native-product` |
| Manage portfolio across products | `product-leadership` |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Feature factory** | No connection to outcomes | Bet-based backlog |
| **Date-driven roadmap** | False precision, broken trust | Time horizons |
| **PRD novels** | Nobody reads, out of date instantly | Solution briefs |
| **Stakeholder-driven backlog** | Politics over impact | Evidence-based prioritization |
| **Tech-organized blocks** | Doesn't reflect customer value | Customer-outcome blocks |
| **No kill criteria** | Zombie projects never die | Every bet has exit conditions |

---

## Quick Reference: Architecture Quality Checklist

Before committing to a quarter:

- [ ] **Every bet traces to opportunity** — No orphan features
- [ ] **Kill criteria defined** — Know when to stop
- [ ] **Portfolio is balanced** — 70/20/10 or similar
- [ ] **Roadmap shows trade-offs** — What we're NOT doing is clear
- [ ] **Solution briefs exist** — For all "Now" bets
- [ ] **Metrics are measurable** — Can actually track success
- [ ] **Team has capacity** — Bets fit within available resources
- [ ] **Dependencies mapped** — Know what blocks what

---

## Sources & Influences

- **Marty Cagan** — INSPIRED, EMPOWERED
- **Ryan Singer** — Shape Up (Basecamp)
- **Teresa Torres** — Continuous Discovery Habits
- **Gibson Biddle** — Product strategy frameworks

---

*Part of the Modern Product Operating Model by Yannick Maurice*
