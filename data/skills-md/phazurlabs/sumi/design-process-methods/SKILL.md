---
name: design-process-methods
description: "Design process methodology: NNG's six phases, Double Diamond, Google Design Sprint, IDEO, Lean UX, and the bridge from AI-assisted building to evidence-based UX. Use when framing how the work should run, planning a sprint, or grounding a build in Empathize, Define, Ideate, Prototype, Test."
---

# UX Process Workflow — From Process to Product

## Foundation

The gap between "prompting an AI to generate UI" and "designing a product people love" is not capability — it's process. This skill bridges that gap by grounding every build session in established UX methodology, mapped to how developers actually work in the terminal.

### The Core Problem

Modern AI-assisted development (vibe coding) creates a dangerous shortcut:

```
Traditional:  Empathize → Define → Ideate → Prototype → Test → Implement
Vibe coding:  Prompt → Ship → Hope
```

The result: pixel-perfect UIs that solve the wrong problems, look identical to every other AI-generated interface, and erode the developer's own design judgment over time (arXiv:2509.10652).

### The Solution

Ground yourself before you build. This skill provides:
1. **Process frameworks** — NNG, IDEO, Double Diamond, and 6 more methodologies adapted for terminal workflows
2. **The vibe coder's bridge** — Concrete checklists that slot UX thinking into AI-assisted development
3. **Academic foundations** — ISO 9241-210, Norman's 7 principles, cognitive laws that explain *why* process matters
4. **Sumi command mapping** — Every process phase maps to specific Sumi commands

### The Speed Run: Process in 60 Seconds

For builders who won't read further — the entire UX process in one block:

```
BEFORE you prompt: "Who is this for, and what problem does it solve?"
WHILE it generates:  "Does this match the user's reality, or the AI's patterns?"
AFTER it generates:  Run /audit + /a11y. Fix severity 3-4. Ship.
```

That's it. Three questions. Two audits. Everything else in this skill is the *why* behind those three lines.

### Real-World Impact: Process vs. No Process

| Metric | Without Process (Prompt → Ship) | With Process (Ground → Build → Test) |
|--------|-------------------------------|-------------------------------------|
| **Screens shipped** | 10 screens/day | 3 screens/day |
| **Screens users actually use** | 2-3 of 10 | 3 of 3 |
| **Accessibility violations** | 15-25 per screen (average) | 0-3 per screen |
| **Redesign cycles** | 4-7 (because wrong problem) | 1-2 (because right problem) |
| **Time to "done"** | Feels faster, takes longer | Feels slower, ships sooner |
| **User satisfaction** | "It looks nice" | "It solves my problem" |
| **Brand differentiation** | Looks like every other AI-generated app | Looks like *your* product |

The math: 10 screens × 5 redesign cycles = 50 screen-builds to get 2-3 right.
vs. 3 screens × 1 redesign cycle = 6 screen-builds to get 3 right.

Process doesn't slow you down. **Skipping process slows you down.**

---

## NNG Design Thinking — The 6-Phase Framework

Nielsen Norman Group's design thinking model is the most widely-validated UX process. It organizes into three macro stages:

### Macro Stage 1: UNDERSTAND (Empathize + Define)

The stage most vibe coders skip entirely. You cannot design what you do not understand.

#### Phase 1: Empathize

**Goal**: Understand users' needs, pain points, and context through direct observation and engagement.

**Methods**:
- **Contextual inquiry** — Observe users in their natural environment performing real tasks
- **User interviews** — Semi-structured conversations focusing on behaviors, not opinions
- **Diary studies** — Longitudinal capture of experiences over days or weeks
- **Empathy mapping** — Synthesize what users Say, Think, Do, and Feel
- **Stakeholder interviews** — Understand business constraints, technical limitations, and organizational goals

**Key principle**: Empathy is not sympathy. It's not "feeling sorry for users." It's understanding their mental models, frustrations, and workarounds deeply enough to design for their actual reality.

**In terminal workflow**: Before prompting any AI to generate UI, spend 2 minutes answering:
- Who will use this? (Not "users" — a specific person with a specific job)
- What are they trying to accomplish? (Task, not feature)
- What's their current workaround? (They're solving this somehow today)
- What frustrates them about the current solution?
- What environment are they in? (Mobile on a train? Desktop in an office? Accessibility needs?)

**Sumi mapping**: `/brief` (0.2) captures this as a structured problem statement.

#### Phase 2: Define

**Goal**: Synthesize empathy findings into a clear, actionable problem statement.

**Methods**:
- **Problem statement** — "Users who [X] need [Y] because [Z]"
- **How Might We questions** — Reframe problems as opportunities ("HMW make checkout feel instant?")
- **Personas** — Behavioral archetypes (not demographic stereotypes)
- **Jobs to Be Done** — Functional, emotional, and social jobs the product fulfills
- **User stories** — "As a [persona], I want [action] so that [outcome]"
- **Success criteria** — Measurable outcomes that define "done" (functional, usability, accessibility, business)

**Key principle**: A well-defined problem is half-solved. Most design failures trace to building the right solution to the wrong problem.

**In terminal workflow**: Write a single sentence: "Users who [X] need [Y] because [Z]." If you can't fill this in, you haven't empathized enough.

**Sumi mapping**: `/brief` (0.2) generates the problem statement, persona, HMW questions, and success criteria.

### Macro Stage 2: EXPLORE (Ideate + Prototype)

Generate and test multiple solutions before committing.

#### Phase 3: Ideate

**Goal**: Generate a breadth of possible solutions without premature commitment.

**Methods**:
- **Brainstorming** — Quantity over quality, defer judgment, build on others' ideas
- **Crazy 8s** — 8 ideas in 8 minutes, forces divergent thinking
- **How Might We** — Each HMW question generates 3-5 potential solutions
- **Competitive analysis** — Study how others solve the same problem (not to copy — to understand the solution space)
- **Design patterns** — Known solutions to known problems (Sumi's screen-flow-patterns catalog)
- **Sketching** — Low-fidelity exploration before any code or AI generation

**Key principle**: The first idea is almost never the best idea. Diverge before you converge.

**In terminal workflow**: Before prompting AI to generate a component, list 3 different approaches. Even 30 seconds of divergent thinking improves outcomes.

**Sumi mapping**: `/style` (1.2) finds patterns; `/benchmark` (1.3) reveals competitive approaches; `/style` (1.1) establishes style direction.

#### Phase 4: Prototype

**Goal**: Build quick, disposable representations to test ideas — not ship-ready code.

**Methods**:
- **Paper prototypes** — Sketch on paper, test with users pointing at elements
- **Wireframes** — Low-fidelity digital layouts showing structure without style
- **Interactive prototypes** — Clickable mockups (Figma, code) testing specific flows
- **Wizard of Oz** — Human simulates AI/backend behavior to test the interface layer
- **A/B prototypes** — Build 2 versions of a critical interaction to test with users

**Key principle**: Prototypes are questions, not answers. Build them to learn, then throw them away.

**In terminal workflow**: Use AI to rapidly generate 2-3 variations of a component or screen. Treat these as prototypes to evaluate, not production code.

**Sumi mapping**: `/screen` (4.2) and `/component` (4.3) generate prototypes; `/tokens` (4.1) establishes the design foundation.

### Macro Stage 3: MATERIALIZE (Test + Implement)

Validate with real users and ship with confidence.

#### Phase 5: Test

**Goal**: Evaluate prototypes with real users to identify problems before shipping.

**Methods**:
- **Usability testing** — 5 users, think-aloud protocol, task-based scenarios
- **Heuristic evaluation** — Expert review against Nielsen's 10 heuristics
- **Cognitive walkthrough** — Step through tasks from the user's perspective, checking learnability
- **A/B testing** — Statistical comparison of design variants with real traffic
- **Accessibility audit** — WCAG 2.2 compliance, screen reader testing, keyboard navigation
- **Analytics review** — Behavioral data revealing where users struggle

**Key principle**: Testing is not validation — it's learning. The goal is to find problems, not prove your design works.

**In terminal workflow**: After AI generates UI, run Sumi audits before deploying. Each audit simulates expert evaluation.

**Sumi mapping**: `/audit` (2.1) heuristic evaluation; `/audit` (2.2) cognitive audit; `/a11y` (2.3) accessibility; `/audit` (2.4) journey audit; `/audit` (3.1) ethics; `/roast` (5.1) critique; `/grade` (5.3) comprehensive review.

#### Phase 6: Implement

**Goal**: Ship the validated design with production quality, accessibility, and performance.

**Methods**:
- **Design system consumption** — Build with tokens, not magic numbers
- **Component library** — Reusable, tested, accessible components
- **Progressive enhancement** — Core functionality works without JavaScript
- **Performance budgets** — Time-to-interactive targets, bundle size limits
- **Monitoring** — Post-launch metrics tracking against success criteria

**Key principle**: Implementation is not "coding the design." It's translating design intent into technical reality while preserving every UX decision.

**In terminal workflow**: Use Sumi BUILD commands with full context from earlier phases.

**Sumi mapping**: `/tokens` (4.1) tokens; `/screen` (4.2) screens; `/component` (4.3) components; `/onboard` (4.4) onboarding; `/figma` (4.5) Figma pipeline.

---

## The Understand → Explore → Materialize Framework

NNG's three macro stages create a memorable mental model:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   UNDERSTAND    │     │     EXPLORE      │     │   MATERIALIZE   │
│                 │     │                  │     │                 │
│  Empathize      │ ──► │  Ideate          │ ──► │  Test           │
│  Define         │     │  Prototype       │     │  Implement      │
│                 │     │                  │     │                 │
│  "Know the      │     │  "Generate       │     │  "Validate and  │
│   problem"      │     │   solutions"     │     │   ship"         │
└─────────────────┘     └─────────────────┘     └─────────────────┘

Sumi Phase 0: GROUND    Sumi Phases 1-3         Sumi Phases 4-5
+ Phase 1: DISCOVER      DISCOVER, DIAGNOSE,     BUILD, LAUNCH
                          FORTIFY
```

### How Sumi's 6 Phases Map to NNG

| NNG Phase | NNG Stage | Sumi Phase | Sumi Commands |
|-----------|-----------|------------|---------------|
| Empathize | Understand | Phase 0: GROUND | `/sumi` (0.1), `/brief` (0.2) |
| Define | Understand | Phase 0: GROUND | `/brief` (0.2) |
| Ideate | Explore | Phase 1: DISCOVER | `/style` (1.1), `/style` (1.2), `/benchmark` (1.3), `/research` (1.4) |
| Prototype | Explore | Phase 4: BUILD | `/tokens` (4.1), `/screen` (4.2), `/component` (4.3) |
| Test | Materialize | Phase 2: DIAGNOSE + Phase 3: FORTIFY + Phase 5: LAUNCH | `/audit`, `/audit`, `/a11y`, `/audit`, `/audit`, `/ai-audit`, `/roast`, `/grade` |
| Implement | Materialize | Phase 4: BUILD | `/component` (4.3), `/onboard` (4.4), `/figma` (4.5) |

Note: Sumi's phases don't map 1:1 to NNG because Sumi is iterative — you may prototype (BUILD) before you test (DIAGNOSE), then loop back. The NNG framework provides the *thinking*, Sumi provides the *doing*.

---

## Company Methodology Map

Eight leading companies have each adapted design thinking into their own process. Each emphasizes different strengths. Choose based on your context.

| Company | Methodology | Best For | Duration | Key Innovation |
|---------|-------------|----------|----------|----------------|
| **IDEO** | Human-Centered Design | Complex, ambiguous problems | Weeks-months | Radical empathy, multidisciplinary teams |
| **UK Design Council** | Double Diamond | Structured diverge/converge | Days-weeks | Discover-Define-Develop-Deliver framework |
| **Google Ventures** | Design Sprint | Time-critical product decisions | 5 days | Compressed prototype-and-test cycle |
| **IBM** | Enterprise Design Thinking | Large organization alignment | Ongoing | Hills, Playbacks, Sponsor Users at enterprise scale |
| **Lean UX** | Build-Measure-Learn | Startup/hypothesis-driven | Continuous | MVP-first, data-driven iteration |
| **Spotify** | Design Thinking + Squads | Autonomous team design | Continuous | Squad autonomy with design system alignment |
| **Microsoft** | Inclusive Design | Accessibility-first | Ongoing | "Solve for one, extend to many" |
| **Vercel/Figma** | Design Engineer Workflow | Design-to-code speed | Hours-days | Designer-developer convergence, MCP integration |

> **Deep dive**: See `references/company-ux-methodologies.md` for full methodology breakdowns, NNG phase mapping, and AI-adaptation guides for each.

### Quick Selection Guide

```
Are you...

Solo developer / vibe coding?
  → Lean UX + Vercel/Figma workflow
  → Focus: hypothesis, quick prototype, test with Sumi audits

Small team (2-5)?
  → Google Sprint (compressed) or Double Diamond
  → Focus: structured diverge/converge, time-boxed decisions

Large organization?
  → IBM Enterprise Design Thinking
  → Focus: alignment across teams, stakeholder playbacks

Building for accessibility?
  → Microsoft Inclusive Design
  → Focus: "solve for one, extend to many"

Complex/ambiguous problem space?
  → IDEO Human-Centered Design
  → Focus: deep empathy, field research, radical solutions

Continuous product iteration?
  → Spotify model + Lean UX
  → Focus: squad autonomy, continuous experimentation
```

---

## The Vibe Coder's Process Bridge

### The Three Risks of Skipping Process

Research (arXiv:2509.10652) identifies three concrete risks when developers use AI to generate UI without UX process:

1. **Pseudo-productivity** — Shipping more features faster while solving fewer real problems. 10 AI-generated screens vs. 1 well-researched screen: the latter wins.

2. **Homogenization** — AI-generated UIs converge on similar patterns, creating a sameness that erodes brand differentiation and fails edge cases.

3. **Skill erosion** — Developers who always accept AI suggestions lose the ability to evaluate, critique, and improve design independently.

### The Process Bridge: Before / While / After

The bridge doesn't require abandoning AI-assisted development. It adds process *around* the AI interaction.

#### BEFORE Prompting (2 minutes)

The pre-prompt checklist prevents the three risks by forcing human judgment before AI generation:

```markdown
## Pre-Prompt Checklist (2 min)
- [ ] Who is the user? (name a specific persona, not "users")
- [ ] What task are they completing? (verb + noun, e.g., "booking a flight")
- [ ] What's their current workaround? (how they solve this today)
- [ ] What's the success metric? (how you'll know this works)
- [ ] What platform/context? (device, environment, accessibility needs)
```

#### WHILE Generating (ongoing)

Evaluate AI output against UX principles in real-time:

```markdown
## Generation Evaluation
- Does this match the user's mental model, or the AI's training data?
- Is this solving the defined problem, or a different one?
- Would this look identical from a different AI? (homogenization check)
- Does this handle edge cases? (empty, error, loading, offline, first-use)
- Is the information hierarchy correct? (most important → least important)
```

#### AFTER Generating (5 minutes)

Post-generation audit catches the issues AI-generated UI consistently misses:

```markdown
## Post-Generation Audit (5 min)
- [ ] Run `/audit` — catches heuristic violations
- [ ] Run `/a11y` — catches accessibility gaps
- [ ] Check: does this UI work for the persona defined in BEFORE?
- [ ] Check: does this UI handle all 7 states? (empty, loading, populated, error, partial, offline, updating)
- [ ] Check: would you ship this if you couldn't use AI to generate more?
```

> **Deep dive**: See `references/vibe-coder-ux-bridge.md` for the complete bridge framework with anti-patterns, examples, and the 15-minute full UX check.

---

## Academic Foundations

### ISO 9241-210: Human-Centred Design

The international standard for human-centred design (2019 revision) defines six principles:

1. **The design is based upon an explicit understanding of users, tasks, and environments**
2. **Users are involved throughout design and development**
3. **The design is driven and refined by user-centred evaluation**
4. **The process is iterative**
5. **The design addresses the whole user experience**
6. **The design team includes multidisciplinary skills and perspectives**

Every Sumi phase maps to at least one ISO 9241-210 principle. Phase 0 GROUND addresses principles 1 and 2 directly.

### Don Norman's 7 Fundamental Design Principles

From *The Design of Everyday Things* (2013 revised edition):

| Principle | Definition | Process Implication |
|-----------|-----------|-------------------|
| **Discoverability** | Is it possible to figure out what actions are possible? | Test with unfamiliar users |
| **Feedback** | Is there full and continuous information about results? | Define expected system responses in Design phase |
| **Conceptual model** | Does the design project clear understanding of the system? | Empathize to understand user mental models |
| **Affordances** | What actions are possible? | Map affordances to user tasks, not features |
| **Signifiers** | Where should actions take place? | Test that signifiers match affordances |
| **Mapping** | Is there a clear relationship between controls and effects? | Prototype to verify spatial/logical mapping |
| **Constraints** | Are there physical, logical, semantic, or cultural constraints? | Define constraints during problem definition |

### Cognitive Laws That Explain Why Process Matters

| Law | What It Says | Why Process Prevents Violation |
|-----|-------------|-------------------------------|
| **Hick's Law** | Decision time increases with number and complexity of choices | Define phase constrains the solution space |
| **Fitts's Law** | Time to target depends on distance and size | Prototyping reveals sizing/placement issues |
| **Miller's Law** | Working memory holds 7±2 chunks | Empathy reveals users' actual cognitive capacity |
| **Jakob's Law** | Users spend most time on other sites — they expect yours to work the same | Ideation includes competitive analysis |
| **Doherty Threshold** | Productivity soars when response time < 400ms | Testing phase measures actual performance |
| **Peak-End Rule** | Users judge experiences by the peak and end moments | Define phase identifies emotional moments |
| **Von Restorff Effect** | Distinctive items are more likely to be remembered | Ideation explores visual hierarchy options |
| **Aesthetic-Usability Effect** | Attractive things are perceived as more usable | Style direction (Phase 1) matters before building |

---

## Process-to-Sumi Command Mapping

The mapping from NNG's process phases to the commands that serve them:

```
NNG UNDERSTAND ─────────────────────────────────────────────────
  Empathize        → /brief      Problem, persona, HMW questions
                   → /research   Interviews, surveys, usability tests
  Define           → /brief      Success criteria + constraint stack
                   → /map        Information architecture

NNG EXPLORE ────────────────────────────────────────────────────
  Ideate           → /style      Visual direction for the sector
                   → /benchmark  Competitive scorecard and gaps
                   → /measure    Metrics plan, before anything is built
  Prototype        → /wireframe  Low-fidelity structure
                   → /tokens     Token system
                   → /screen     Screen compositions
                   → /component  Component prototypes

NNG MATERIALIZE ────────────────────────────────────────────────
  Test             → /audit      Heuristics, cognitive load, flow, ethics
                   → /a11y       WCAG 2.2 accessibility audit
                   → /ai-audit   AI trust, control, recovery
                   → /responsive Cross-device behaviour
                   → /roast      Fast critique
                   → /grade      Design Quality Score
  Implement        → /component  Production components
                   → /page       Full page compositions
                   → /onboard    Onboarding flows
                   → /figma      Figma design-to-code pipeline
                   → /remix      Evidence-based redesign
                   → /preflight  Pre-launch and post-launch plan
```

Not every phase needs every command. `/start` routes to the right pipeline
without you choosing from this list.

---

## When to Use This Skill

This skill auto-activates when the user mentions:
- UX process, design process, design thinking, design methodology
- Vibe coding, AI-assisted design, prompt-and-ship
- Human-centered design, user-centered design
- Double Diamond, Design Sprint, Lean UX, IDEO
- Empathize, define, ideate, prototype, test (as process phases)
- "Where do I start?", "What's the right process?", "Am I skipping steps?"
- "I'm just vibe coding", "prompt and ship", "AI generated my UI"
- "My app looks generic", "everything looks the same", "no differentiation"
- "How do I make better UIs?", "my designs feel off", "something is wrong but I can't tell what"
- "I shipped without testing", "how do I know if this is good?"
- "What would a senior designer do?", "how do real design teams work?"

---

## The Builder's Cheat Sheet

Quick-reference for builders who want process without theory:

### I have 2 minutes
Run `/brief` on whatever you're about to build. Just the problem statement. That's it.

### I have 10 minutes
`/sumi` → `/brief` → then build with the constraint stack pasted into your prompt.

### I have 30 minutes
`/brief` → `/style` → `/tokens` → then build. You now have a defined problem, visual direction, and token system.

### I have 2 hours
Full Phase 0→5 journey. `/sumi` → `/brief` → `/style` → `/style` → `/tokens` → `/screen` → `/component` → `/audit` → `/a11y` → `/roast`. This is what real design teams do.

### I have a real product to ship
Follow the full 22-step journey via `/sumi`. Run every audit. Loop `/roast` → `/remix` → `/roast` until all scores are 7+. This is how Stripe, Linear, and Notion work.

### The one non-negotiable
Whatever your time budget: **run `/audit` + `/a11y` before shipping**. 5 minutes. Zero excuses.

## Cross-References

This skill connects to and is grounded in:
- `nng-ux-heuristics` — The 10 heuristics used in the Test phase
- `ux-research-methods` — Research methodologies for the Empathize phase
- `cognitive-psychology-ux` — Cognitive laws that justify process rigor
- `agentic-ai-generative-ux` — AI-assisted design patterns and risks
- `ux-ethics-content-strategy` — Ethical frameworks for the Define phase
- `ux-metrics-measurement` — Measurement frameworks for success criteria
- `design-systems-architecture` — System thinking for the Implement phase
- `design-critique-case-studies` — Case studies showing process impact (Stripe, Linear: process-heavy; Sonos 2024, Healthcare.gov: process-light failures)
