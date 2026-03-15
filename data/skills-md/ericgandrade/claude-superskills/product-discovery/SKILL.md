---
name: product-discovery
description: This skill should be used when the user needs to run continuous discovery to find problems worth solving. Use when setting up weekly discovery rhythm, building Opportunity Solution Trees, creating interview snapshots, exploring solutions, or testing assumptions before committing engineering resources.
license: MIT
---

# Product Discovery System

> "Discovery without delivery = analysis paralysis. Delivery without discovery = feature factory."

This skill covers the **Discovery System** — continuously discovering which problems matter and which solutions might work. It maintains a living map of customer opportunities and tests solution ideas before committing engineering resources.


**Related skills**: `product-strategy`, `product-architecture`, `product-delivery`, `ai-native-product`, `product-leadership`

---

## When to Use This Skill

Use this skill when:
- Setting up a weekly discovery rhythm
- Building or updating an Opportunity Solution Tree (OST)
- Creating interview snapshots after customer conversations
- Exploring multiple solution approaches
- Designing and running assumption tests
- Synthesizing insights across multiple interviews
- Running an Opportunity Council meeting

**Cadence**: Weekly rhythm | **Owner**: Product Trio (PM + Designer + Tech Lead)

---

## The Problem This Solves

Most teams either:
1. Do discovery once, then execute for months on stale assumptions
2. Skip discovery entirely and build what stakeholders request
3. Do discovery but don't connect it to what actually gets built

The Discovery System creates a weekly rhythm that keeps you close to customers and ensures **evidence—not opinions—drives decisions**.

---

## Philosophy

### Core Beliefs

1. **Weekly rhythm over big research projects** — 2-3 interviews per week beats quarterly research sprints
2. **The crossfunctional discovery** — Handoffs kill learning
3. **Opportunities are problems, not solutions** — "Users need faster onboarding" not "Add a wizard"
4. **Multiple solutions per opportunity** — Always explore 3+ options before committing
5. **Test in hours and days, not weeks** — If your test takes a month, you're testing too much

### What This Framework Rejects

- Discovery theater (interviews that don't change roadmap)
- Solution-first thinking
- PM does interviews alone, hands notes to designers
- Building the first idea that comes to mind
- Waiting for perfect data before deciding

---

## Progress Tracking

Display progress during discovery sessions:

```
[████░░░░░░░░░░░░░░░░] 25% — Phase 1/4: Setting Up Discovery Rhythm
[████████░░░░░░░░░░░░] 50% — Phase 2/4: Customer Interviews & Opportunity Mapping
[████████████░░░░░░░░] 75% — Phase 3/4: Solution Exploration & Assumption Testing
[████████████████████] 100% — Phase 4/4: Synthesizing Insights & Prioritizing
```

## Framework Components

### 1. Continuous Discovery Habits

**The Weekly Rhythm (Minimum Viable Discovery)**

| Activity | Frequency | Purpose |
|----------|-----------|---------|
| Customer interviews | 2-3 per week | Stay connected to real problems |
| Synthesis session | 1 per week | Update opportunity map |
| Assumption test | 1 per week | Validate before building |

**Who Does Discovery: The Product Trio**

| Role | Contribution |
|------|--------------|
| Product Manager | Owns outcome, facilitates, synthesizes |
| Product Designer | Owns experience, visualizes, prototypes |
| Tech Lead | Owns feasibility, estimates, identifies constraints |

> **Principle**: The trio does discovery together. If the PM does interviews alone and hands notes to designers, you've already lost 50% of the insight.

**0→1 Mode:**
- Founder does interviews personally
- 10-15 interviews before patterns emerge
- Daily cadence if possible
- Bias toward speed over rigor

**Scaling Mode:**
- Research ops supports logistics
- Systematic interview quotas by segment
- Centralized insight repository
- Quarterly synthesis reports

---

### 2. Interview Snapshots

After each interview, create a snapshot (not a transcript). Capture the essence, not every word.

**Snapshot Format:**

```
INTERVIEW SNAPSHOT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Date: [Date]
Participant: [Role, Company type, Context]
Interviewer(s): [Names]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEY OPPORTUNITIES (Unmet needs discovered)
• [Opportunity #1]
• [Opportunity #2]
• [Opportunity #3]

KEY QUOTE (In their words)
"[Memorable statement that captures their experience]"

QUICK FACTS
• [Relevant context about their situation]
• [Current workflow or tools]
• [Constraints or requirements]

JOBS TO BE DONE (If surfaced)
• Functional: [Task they're trying to accomplish]
• Emotional: [How they want to feel]
• Social: [How they want to be perceived]

SURPRISES
• [Anything unexpected]
• [Assumptions challenged]

FOLLOW-UPS
• [Questions for next interview]
• [Things to validate]
```

**AI Integration for Snapshots:**
- Use AI to draft snapshot from notes
- **Always review** — AI misses 20-40% of important context
- Never let AI replace the act of listening

---

### 3. Opportunity Solution Tree (OST)

The OST is your living map connecting outcomes to opportunities to solutions to tests.

**Structure:**

```
                    OUTCOME
                    (Metric we're trying to move)
                         │
          ┌──────────────┼──────────────┐
          │              │              │
     OPPORTUNITY    OPPORTUNITY    OPPORTUNITY
     (Unmet need)   (Unmet need)   (Unmet need)
          │              │              │
     ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
     │         │    │         │    │         │
  SOLUTION  SOLUTION SOLUTION SOLUTION SOLUTION SOLUTION
  (Idea)    (Idea)  (Idea)   (Idea)  (Idea)   (Idea)
     │         │
  ┌──┴──┐   ┌──┴──┐
  │     │   │     │
 TEST  TEST TEST  TEST
```

**OST Rules:**

| Rule | Why |
|------|-----|
| One outcome per tree | Don't try to solve everything at once |
| Opportunities are problems, not solutions | "Users struggle to..." not "Add a feature..." |
| Multiple solutions per opportunity | Always explore 3+ before committing |
| Evidence-backed | Each opportunity has interview/data support |
| Living document | Update weekly as you learn |

**Good Opportunity Statements:**
- "Users struggle to understand which metrics matter during their first week"
- "Managers can't quickly see which team members need attention"
- "New users don't know what to do after signup"

**Bad Opportunity Statements (These are solutions):**
- "We need a dashboard"
- "Add an onboarding wizard"
- "Send email reminders"

**Target Opportunity Selection:**

Use compare-and-contrast to select focus:

| Opportunity | Pain Severity | Frequency | Strategic Fit | Evidence Strength |
|-------------|---------------|-----------|---------------|-------------------|
| A | High | Daily | Core | 8 interviews |
| B | Medium | Weekly | Adjacent | 3 interviews |
| C | High | Monthly | Core | 12 interviews |

> **Principle**: Choose ONE target opportunity at a time. Complete focus beats scattered effort.

---

### 4. Solution Exploration

For every target opportunity, generate at least 3 solution approaches before committing.

**The Three Solution Types:**

| Type | Description | Example |
|------|-------------|---------|
| **The obvious solution** | What everyone expects | "Add an onboarding wizard" |
| **The 10x harder solution** | If effort were no constraint | "AI-powered personalized setup" |
| **The non-product solution** | Pricing, process, partnership, or service | "White-glove onboarding call" |

**Solution Categories:**

| Category | When to Consider |
|----------|------------------|
| Product changes | Features, UX improvements |
| Pricing/packaging changes | How value is captured |
| Enablement changes | Documentation, training, support |
| Process changes | How work gets done internally |
| Partnership solutions | Integrate vs. build |

> **Principle**: The best solution to a product problem is often not a product change.

**Thin-Slice MVP:**

Don't build the whole solution. Build the smallest thing that tests your riskiest assumption.

| Full Solution | Thin Slice |
|---------------|------------|
| "Complete onboarding wizard with 10 steps, progress tracking, and personalization" | "Single welcome screen that asks one question and shows one recommendation" |
| "Full analytics dashboard with customizable widgets" | "One pre-built view showing the top 3 metrics" |
| "AI-powered recommendation engine" | "Rule-based suggestions for top 5 use cases" |

---

### 5. Assumption Testing

Every solution has assumptions. Find the ones that would kill it if wrong.

**Assumption Categories:**

| Category | Question |
|----------|----------|
| **Desirability** | Will users want this? |
| **Viability** | Will this work for the business? |
| **Feasibility** | Can we build this? |
| **Usability** | Can users figure it out? |

**Assumption Test Format:**

```
ASSUMPTION TEST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Assumption: [What we believe is true]
Risk level: [High / Medium / Low]
Test method: [How we'll test]
Success criteria: [What would confirm]
Failure criteria: [What would disprove]
Timebox: [Hours/days, not weeks]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Test Methods (Fastest to Slowest):**

| Method | Time | When to Use |
|--------|------|-------------|
| Desk research | 30 min | Does evidence already exist? |
| One-question survey | 1 hour | Quick signal from existing users |
| Fake door test | 1 day | Measure interest before building |
| Concierge test | 1-3 days | Manually deliver the value |
| Wizard of Oz | 1 week | Fake backend, real frontend |
| Prototype test | 1-2 weeks | Clickable prototype with users |
| A/B test | 2-4 weeks | Live code, statistical significance |

> **Principle**: Test in hours and days, not weeks and months. If your test takes a month, you're testing too much at once.

**AI Integration for Testing:**
- Use AI to build prototypes faster (vibe coding)
- Use AI to analyze survey responses
- Use AI to synthesize test results
- **Don't use AI to decide** — Humans interpret, AI assists

---

### 6. Opportunity Council (Scaling Mode)

Weekly cross-functional meeting that turns discovery into decisions. Prevents discovery theater.

**Participants:**
- PM (facilitator)
- Design lead
- Engineering lead
- Sales/CS representative (input, not veto)
- Marketing representative (for GTM alignment)

**Agenda (60 min max):**

| Segment | Time | Focus |
|---------|------|-------|
| New evidence review | 15 min | 2-3 key findings from this week |
| Opportunity prioritization | 20 min | Promote, kill, or park opportunities |
| Solution shaping | 15 min | Review prototype/test results |
| GTM/tech flags | 10 min | Early visibility on constraints |

**Council Rules:**
- Decisions are recorded with rationale
- Single decider (PM) — council advises, PM decides
- No side quests — if it's not on the OST, it waits
- Evidence required — no "I think users want..."

**0→1 Mode:** Skip formal council. Founder + team informal sync.

---

## Primary Outputs

| Output | Description | Update Cadence |
|--------|-------------|----------------|
| **Opportunity Solution Tree** | Living map of outcome → opportunities → solutions | Weekly |
| **Interview snapshots** | Library of customer evidence | After each interview |
| **Test results** | What we learned, what we decided | After each test |
| **Target opportunity** | Current focus area | Weekly review |
| **Solution candidates** | Prototypes ready for prioritization | Ongoing |

---

## Templates

This skill includes templates in the `templates/` directory:
- `interview-snapshot.md` — Post-interview capture format
- `opportunity-solution-tree.md` — OST structure and rules
- `assumption-test.md` — Test design and tracking

---

## Using This Skill with Claude

Ask Claude to:

1. **Set up discovery rhythm**: "Help me design a weekly discovery cadence for [team size/stage]"
2. **Create interview guide**: "Create an interview guide for understanding [JTBD/opportunity]"
3. **Draft snapshot**: "Turn these interview notes into a snapshot"
4. **Build OST**: "Help me build an OST for the outcome: [metric]"
5. **Reframe solutions as opportunities**: "These are solutions — help me reframe as opportunities"
6. **Generate solution options**: "Generate 5 solution approaches for [opportunity]"
7. **Design thin slice**: "What's the thin-slice MVP for [solution]?"
8. **Create assumption test**: "Design an assumption test for [hypothesis]"
9. **Synthesize interviews**: "Find patterns across these [X] interview snapshots"
10. **Prepare Opportunity Council**: "Create an agenda for Opportunity Council with these findings"

---

## Connection to Other Skills

| When you need to... | Use skill |
|---------------------|-----------|
| Define ICP and strategic context | `product-strategy` |
| Convert opportunities to bets | `product-architecture` |
| Plan delivery and measurement | `product-delivery` |
| Discover for AI products | `ai-native-product` |
| Scale discovery across teams | `product-leadership` |

---

## Quick Reference: Discovery Quality Checklist

Before concluding discovery on an opportunity:

- [ ] **Evidence breadth** — 5+ interviews mentioning this opportunity
- [ ] **Evidence depth** — Understand functional, emotional, social jobs
- [ ] **Multiple solutions explored** — 3+ approaches considered
- [ ] **Thin slice identified** — Know the smallest testable version
- [ ] **Riskiest assumption named** — Know what would kill this
- [ ] **Test designed** — Ready to validate before building
- [ ] **Strategic fit confirmed** — Aligns with strategy canvas

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| Discovery theater | Interviews don't change roadmap | Evidence → decisions |
| AI replaces listening | Miss 40% of insight | AI augments, humans decide |
| Solution-first thinking | Build wrong thing | Opportunity-first |
| Homer Simpson car | Feature bloat from asking "what do you want?" | Ask about problems, not solutions |
| PM does discovery alone | Handoffs kill learning | Trio does discovery together |
| One solution per opportunity | Miss better approaches | Always 3+ options |
| Month-long tests | Too slow to learn | Test in hours/days |

---

## Sources & Influences

- **Teresa Torres** — Continuous Discovery Habits, Opportunity Solution Trees
- **Marty Cagan** — INSPIRED, EMPOWERED
- **Rob Fitzpatrick** — The Mom Test
- **Cindy Alvarez** — Lean Customer Development

---

