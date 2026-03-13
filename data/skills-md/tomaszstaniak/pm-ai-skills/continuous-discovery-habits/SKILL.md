---
name: continuous-discovery-habits
description: 'Product discovery framework based on Teresa Torres'' "Continuous Discovery Habits". Use when you need to: (1) build an opportunity solution tree from desired outcomes, (2) identify and prioritize customer opportunities, (3) design assumption tests for product ideas, (4) structure customer interview snapshots, (5) map assumptions to experiments, (6) move from output-driven to outcome-driven product development, (7) map current-state customer experiences, (8) build a weekly discovery habit.'
license: CC-BY-SA-4.0
metadata:
  author: Tomasz Staniak
  version: "1.1.0"
---

# Continuous Discovery Habits

A structured, repeatable approach to product discovery that helps teams make better product decisions through weekly customer touchpoints, opportunity mapping, and rapid assumption testing. Based on Teresa Torres' "Continuous Discovery Habits."

## Core Principle

**Good product teams don't debate opinions — they test assumptions.** The goal of discovery is not to validate ideas, but to discover opportunities and find the best path to a desired outcome. Discovery is not a phase; it is a continuous, weekly habit embedded into how teams work.

The foundation: most product teams skip discovery entirely, jumping from a business outcome directly to a solution. The Opportunity Solution Tree (OST) provides the missing structure — it forces teams to explore the problem space before committing to solutions, and to compare multiple solutions against clear criteria before building anything.

## Scoring

**Goal: 10/10.** When reviewing product discovery work, rate it 0-10:

| Score | Description |
|-------|-------------|
| 0-2 | No discovery. Team builds what stakeholders request or what feels right. No customer contact. |
| 3-4 | Sporadic discovery. Occasional user research, but not connected to decisions. Ideas come from inside the building. |
| 5-6 | Some structure. Team talks to customers but lacks a systematic way to prioritize opportunities or test assumptions. |
| 7-8 | Strong discovery. OST exists, weekly customer touchpoints, assumption testing before building. |
| 9-10 | Exceptional. Full OST discipline, compare-and-contrast experiments, story-based interviews, and the whole team participates in discovery weekly. |

## The Opportunity Solution Tree (OST)

The core visual framework connecting business outcomes to solutions through opportunities:

```
        Desired Outcome
        (metric to move)
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
Opportunity Opportunity Opportunity
 (unmet need) (pain point) (desire)
    │         │
  ┌─┴─┐    ┌─┴─┐
  ▼   ▼    ▼   ▼
Sol. Sol.  Sol. Sol.
  │         │
  ▼         ▼
Assumption Assumption
  Tests      Tests
```

**Rules for a good OST:**
- **One desired outcome** at the top — the metric the team is trying to move
- **Opportunities** are customer needs, pain points, or desires — never solutions
- **Solutions** address specific opportunities — each solution maps to at least one opportunity
- **Assumption tests** validate the riskiest assumptions before building
- The tree is a living document, updated weekly

### Premortem Check

Before committing to a solution branch on the OST, run a premortem: imagine the solution has shipped and failed completely. Ask "What went wrong?" and have every member of the product trio independently write down failure causes. Cluster the answers — recurring themes reveal the assumptions that are most likely to be fatal.

**How to run it:**

| Step | Action |
|------|--------|
| 1. Set the scene | "It's six months from now. We shipped this solution and it failed. Walk me through what happened." |
| 2. Write independently | Each person writes 3-5 failure reasons before discussing — avoids anchoring bias |
| 3. Cluster themes | Group similar failures; the clusters with the most entries are your highest-risk assumptions |
| 4. Map to assumption types | Assign each cluster to desirability, viability, feasibility, or usability |
| 5. Prioritize the tree | Branches whose premortem reveals high-risk untested assumptions should be tested before branches with lower risk profiles |

**When to use it:** After generating solution candidates (step 4 below) but before selecting which to test first. A 20-minute premortem is the cheapest way to surface the assumption most likely to kill the solution — before any engineering time is spent.

## The Seven Habits

### 1. Setting the Desired Outcome

**Core concept:** A product trio (PM, designer, engineer) needs a single, clear outcome to optimize for. This outcome should be a measurable business or product metric that the team can directly influence.

**Why it works:** Without a clear outcome, teams optimize for output (ship features) instead of impact. A well-chosen outcome gives the team autonomy to find the best path while staying aligned with business goals.

**Key insights:**
- Outcomes should be lagging indicators of customer value (retention, activation, task success rate), not business vanity metrics (revenue alone)
- Teams need the authority to choose their own path to the outcome
- "Increase revenue" is too broad; "Increase 30-day retention for new users from 40% to 55%" is actionable
- Product outcomes (what customers do) lead to business outcomes (what the company gets)

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Quarterly planning | Assign outcomes, not features, to teams | "Improve onboarding completion rate" instead of "Build new onboarding flow" |
| OKR setting | Use product outcomes as key results | KR: "Increase 7-day activation from 30% to 45%" |
| Roadmap review | Check if planned work connects to outcomes | If a feature doesn't map to an outcome, question why it's being built |

**Ethical boundary:** Never manipulate outcomes to justify pre-decided solutions. The outcome must come before the solution, not be reverse-engineered to support it.

See: [references/desired-outcomes.md](references/desired-outcomes.md)

### 2. Discovering Opportunities

**Core concept:** Opportunities are unmet customer needs, pain points, and desires discovered through continuous customer interviews. They live in the middle layer of the OST, between the outcome and solutions.

**Why it works:** Most teams jump from outcome to solution. The opportunity layer forces teams to understand the problem space first. Multiple opportunities exist for any outcome; choosing the right one to address is a strategic decision.

**Key insights:**
- Opportunities come from customer stories, not from asking "what do you want?"
- Use story-based interviews: "Tell me about the last time you [did the thing]"
- Extract opportunities from stories — pain points, workarounds, unmet needs
- Organize opportunities in a hierarchy (parent opportunities break into sub-opportunities)
- Prioritize by frequency, intensity, and alignment with the desired outcome

**The Interview Snapshot:**

| Field | Content |
|-------|---------|
| Quick facts | Date, participant, context |
| Key moments | 3-5 notable quotes or behaviors from the interview |
| Opportunities | Unmet needs or pain points identified |
| Insights | Patterns or surprises worth noting |

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Weekly interviews | Extract opportunities from each interview | "Users struggle to find where they left off after a break" |
| Opportunity prioritization | Score by frequency + severity + outcome alignment | High frequency + high severity + directly tied to retention = top priority |
| Stakeholder alignment | Share the opportunity tree, not just ideas | "We found 3 major opportunities. Here's why we're addressing this one first." |

**Copy patterns:**
- Frame features around the opportunity they solve: "Never lose your place — pick up exactly where you left off"
- Use customer language from interviews, not internal jargon

**Ethical boundary:** Never cherry-pick interview quotes to support a preferred solution. Report all opportunities honestly, even if they challenge existing plans.

See: [references/opportunity-discovery.md](references/opportunity-discovery.md)

### 3. Experience Mapping

**Core concept:** Current-state experience maps capture how customers accomplish a goal today, step by step, revealing pain points and unmet needs that become opportunities on the OST.

**Why it works:** Teams often assume they understand the customer's current experience, but mapping it collaboratively from interview data reveals gaps, workarounds, and emotions that are invisible from the inside. The map generates opportunities you would never brainstorm from a conference room.

**Key insights:**
- Map the current state, not a future ideal — you need to understand reality first
- Include actions, thoughts, and feelings at each step
- Build maps collaboratively with the full product trio
- Use interview data as the source, not assumptions
- Journey maps (your product's touchpoints) differ from experience maps (the customer's full experience regardless of your product)
- Pain points and moments of high emotion on the map become opportunities on the OST

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| New problem space | Map the end-to-end experience before designing anything | Map how a small business owner handles invoicing today, from creating to chasing payment |
| Churn analysis | Map the experience of users who churned to find failure points | Discover that users abandon onboarding at step 4 because they need data they don't have handy |
| Cross-functional alignment | Build the map together so engineering, design, and product share one view | Three-hour collaborative session produces a shared reference artifact |

**Ethical boundary:** Experience maps must reflect real customer experiences from interviews, not the team's projection of what they imagine customers feel.

See: [references/experience-mapping.md](references/experience-mapping.md)

### 4. Generating and Evaluating Solutions

**Core concept:** For each target opportunity, generate multiple solutions (at least 3) and compare them. Never go with the first idea. Use compare-and-contrast thinking to find creative combinations.

**Why it works:** The first idea is rarely the best. By forcing multiple options, teams escape anchoring bias and find solutions that are simpler, cheaper, or more effective than the obvious choice.

**Key insights:**
- Generate at least 3 solutions per opportunity
- Mix solution types: product changes, process changes, service changes, content changes
- Use "How Might We" (HMW) framing to generate ideas: "How might we help users pick up where they left off?"
- Evaluate solutions against effort, impact, and assumption risk
- Combine elements from different solutions — the best solution is often a hybrid

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Ideation | Generate 3+ solutions for top opportunity | For "users lose their place": (1) auto-save with resume, (2) activity timeline, (3) daily digest email |
| Evaluation | Compare on effort/impact/risk | Auto-save: low effort, high impact, low risk → start here |
| Design review | Check that solutions map to opportunities | "Which opportunity does this feature address? Is it the top-priority one?" |

**Copy patterns:**
- "We explored [N] approaches before choosing the one that best addresses [opportunity]"
- "Instead of building the obvious solution, we tested [alternatives] and found [insight]"
- "This solution combines the best of [approach A] and [approach B]"

**Ethical boundary:** Never pre-select a solution and reverse-engineer the comparison to justify it. Compare-and-contrast must be genuine — if the process always picks the first idea, it's theater.

See: [references/solution-generation.md](references/solution-generation.md)

### 5. Prioritizing Opportunities

**Core concept:** Use structured methods to compare opportunities against each other rather than evaluating them in isolation. Assess opportunity size, market factors, company factors, and customer factors to find the highest-leverage bets.

**Why it works:** Teams default to prioritizing by loudest stakeholder voice, recency bias (whatever the last customer said), or gut feel. Structured comparison forces explicit tradeoff discussions and surfaces disagreements that would otherwise go unspoken until implementation is underway.

**Key insights:**
- Compare opportunities head-to-head rather than scoring them independently — relative comparison produces better decisions
- Consider opportunity sizing: how many customers are affected, how often, how severely
- Assess alignment with company strategy and team capabilities
- Factor in what you already know — opportunities with more supporting evidence are less risky to pursue
- Avoid analysis paralysis: the goal is to make a good-enough decision quickly, then learn fast
- Revisit prioritization as you learn — new evidence may shift the ranking

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Quarterly planning | Rank the top 5-7 opportunities from the OST to decide team focus | Compare "users struggle to find content" vs. "users can't collaborate in real time" using structured criteria |
| Sprint planning | Choose which opportunity to tackle this iteration based on current evidence | Pick the opportunity where you have the most interview evidence and a testable solution |
| Portfolio decisions | Distribute team effort across opportunities by risk and potential impact | 60% on high-confidence opportunity, 30% on medium, 10% on exploratory |

**Ethical boundary:** Prioritization frameworks should surface real customer needs, not be gamed to justify features that serve business metrics at the expense of user value.

See: [references/prioritization-methods.md](references/prioritization-methods.md)

### 6. Assumption Mapping and Testing

**Core concept:** Every solution is built on assumptions. Before building, identify the riskiest assumptions and test them with the smallest possible experiment. Map assumptions across four categories: desirability, viability, feasibility, and usability.

**Why it works:** Building is the most expensive way to test an idea. Most solutions fail because of one or two wrong assumptions. Finding those early saves weeks or months of wasted work.

**Assumption categories:**

| Category | Question | Example test |
|----------|----------|-------------|
| Desirability | Will customers want this? | Show a prototype, measure interest |
| Viability | Will this work for the business? | Model unit economics |
| Feasibility | Can we build this? | Technical spike or proof of concept |
| Usability | Can customers use this? | Unmoderated usability test |

**The Assumption Testing Ladder:**

| Level | Method | Speed | Confidence |
|-------|--------|-------|------------|
| 1 | One-question survey | Hours | Low |
| 2 | Fake door / smoke test | Days | Medium |
| 3 | Prototype test (unmoderated) | Days | Medium-High |
| 4 | Concierge / Wizard of Oz | Weeks | High |
| 5 | Live product experiment (A/B) | Weeks | Highest |

**Key insights:**
- Test the riskiest assumption first — the one that, if wrong, kills the whole idea
- Use the smallest experiment that will give you confidence
- "Will customers use it?" is almost always riskier than "Can we build it?"
- Set success criteria before running the test — don't rationalize results after
- Use the premortem output (see OST section) to identify which assumptions to map first

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Before sprint planning | List top 3 assumptions for any committed work | "We assume users will notice the new button" → test with a 5-second test |
| After ideation | Pick the riskiest assumption from the winning solution | Desirability risk: "Do users actually care about resuming?" → survey + prototype |
| Retrospective | Review which assumptions were validated vs. invalidated | Track learning velocity: assumptions tested per week |

**Copy patterns:**
- "Before building, we tested our riskiest assumption: [assumption]. Here's what we found."
- "We set a success threshold of [X] before running the experiment — the result was [Y]"
- "This experiment disproved our assumption that [belief], saving us [time/money] in wasted development"

**Ethical boundary:** Design experiments to learn, not to confirm. If you're only running tests that validate your idea, you're doing it wrong.

See: [references/assumption-testing.md](references/assumption-testing.md)

### 7. Building the Habit

**Core concept:** Continuous discovery only works if it becomes a sustainable weekly habit for the product trio. This requires automating recruitment, creating lightweight rituals, and embedding discovery into the existing workflow rather than treating it as extra work.

**Why it works:** Most teams do a burst of research at the start of a project and then stop. Continuous discovery requires structural support: automated participant recruitment, standing interview slots, shared synthesis artifacts, and team norms that make discovery non-negotiable. The habit compounds — teams that maintain it for months develop deep customer intuition that transforms every decision.

**Key insights:**
- The product trio (PM, designer, engineer) should participate together — not just the PM
- Automate recruitment: in-app intercepts, customer advisory panels, or scheduling tools that fill slots automatically
- Block recurring calendar time — discovery that depends on "finding time" will never happen
- Keep synthesis lightweight: fill in the snapshot immediately after the interview, not days later
- Start small: one interview per week is enough to build the habit; scale from there
- Connect discovery to delivery: insights should flow into the OST and from there into sprint planning

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Team kickoff | Establish the weekly cadence in the first week of a new team or initiative | Set up automated recruitment, block Thursday afternoons, create snapshot template |
| Scaling discovery | Expand from one interview per week to three as the habit solidifies | Add a second slot on Tuesday for churned-user interviews and a Friday slot for prospect interviews |
| Manager support | Leaders protect discovery time and ask for evidence in planning discussions | "What did you learn from interviews this week?" becomes a standing question in 1:1s |

**Ethical boundary:** Respect participant time. Keep interviews to 30 minutes, compensate fairly, and never use discovery interviews as a disguised sales pitch.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Skipping opportunities, jumping to solutions | You might build the right solution to the wrong problem | Always fill the opportunity layer before ideating solutions |
| Interviewing only when "doing research" | Discovery becomes a phase, not a habit | Schedule 1+ customer interview per week, every week |
| Only the PM talks to customers | Designer and engineer miss context; insights lost in translation | The full product trio interviews together |
| Asking customers what they want | Customers describe solutions, not jobs or needs | Ask about past behavior: "Tell me about the last time..." |
| Testing only desirability | Ignores feasibility, viability, and usability risks | Map assumptions across all four categories |
| One solution per opportunity | First idea bias; no basis for comparison | Generate at least 3 solutions, then compare |
| No success criteria before testing | You'll rationalize any result as positive | Define "we'll proceed if X" before running the test |
| Skipping the premortem | Hidden fatal assumptions go undetected until shipping | Run a 20-minute premortem before committing to any solution branch |
| Scoring opportunities in isolation | No tradeoff discussion; everything looks important | Compare opportunities head-to-head with structured criteria |
| Doing a burst of interviews then stopping | No compounding learning; team reverts to guessing | Automate recruitment and block recurring calendar time |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Do you have a clear desired outcome (metric)? | Team is output-driven | Define a product outcome with the leadership team |
| Did you talk to a customer this week? | Discovery is a phase, not a habit | Schedule a weekly recurring interview slot |
| Does the full trio participate in interviews? | Insights are filtered through one person | Invite designer and engineer to the next interview |
| Do you have an opportunity solution tree? | No structure connecting outcomes to solutions | Build one in 30 minutes with the product trio |
| Did you run a premortem before committing to a solution? | Hidden risks are untested | Run a 20-minute premortem and map the failure themes to assumptions |
| Did you consider 3+ solutions? | First-idea bias | Run a 15-minute HMW brainstorm |
| Are you comparing opportunities, not just listing them? | Prioritization is driven by opinion, not evidence | Run a structured head-to-head comparison on your top 5 opportunities |
| Did you test your riskiest assumption before building? | Building is your test (expensive) | Pick one assumption and design a 1-day experiment |
| Can you trace a shipped feature back to a customer opportunity? | Delivery is disconnected from discovery | Connect backlog items to opportunity nodes on the OST |
| Do you have interview snapshots the whole team can see? | Knowledge is trapped in one person's head | Create a shared snapshot board and fill it after each interview |

## Reference Files

- [Desired Outcomes Guide](references/desired-outcomes.md) — How to set product outcomes vs. business outcomes, outcome anti-patterns, and examples of well-written outcomes across different product stages
- [Opportunity Discovery](references/opportunity-discovery.md) — Story-based interview techniques, opportunity extraction, interview snapshot templates, and opportunity hierarchy construction
- [Experience Mapping](references/experience-mapping.md) — Current-state experience maps, identifying pain points, collaborative mapping exercises
- [Solution Generation](references/solution-generation.md) — How Might We techniques, compare-and-contrast evaluation, solution combination strategies, and avoiding first-idea bias
- [Prioritization Methods](references/prioritization-methods.md) — Opportunity scoring, compare-and-contrast, using data, avoiding analysis paralysis
- [Assumption Testing](references/assumption-testing.md) — Assumption mapping across desirability/viability/feasibility/usability, experiment design templates, the testing ladder in detail, and success criteria frameworks

## Further Reading

- [Continuous Discovery Habits by Teresa Torres](https://www.amazon.com/Continuous-Discovery-Habits-Discover-Products/dp/1736633309?tag=wondelai00-20)
- [Opportunity Solution Tree template (producttalk.org)](https://www.producttalk.org)

## About the Author

Teresa Torres is a product discovery coach who has worked with hundreds of product teams at companies like Netflix, Microsoft, and Spotify. She created the Opportunity Solution Tree framework and advocates for weekly customer touchpoints as a core product team habit.
