---
name: startup-validator
description: Rigorously validate startup ideas using Peter Thiel's 7 questions, Y Combinator PMF indicators, The Mom Test, and related frameworks. Produce scoring, weakness analysis, and prioritized improvement roadmap.
---

# Startup Validator Skill

> Evaluate startup ideas with proven validation frameworks, not optimism.

---

<when_to_use>

| Situation | Example |
|------|------|
| **Idea validation** | Evaluate a new startup concept |
| **Before fundraising** | Identify weaknesses before pitching |
| **Pivot decisions** | Continue current direction vs pivot |
| **Competitive review** | Compare your position vs competitors |
| **PMF check** | Assess Product-Market Fit readiness |

```bash
/startup-validator AI-based education service
/startup-validator subscription healthcare app
/startup-validator crawling-based purchasing automation
```

**Output**: total score (100) + 7-question analysis + weakness diagnosis + improvement roadmap.

</when_to_use>

---

<argument_validation>

```
If $ARGUMENTS is missing, ask immediately:

"Which startup idea should we validate?

Examples:
- 'AI-based education service'
- 'Subscription healthcare app'
- 'B2B SaaS marketing automation'"
```

</argument_validation>

---

<validation_frameworks>

## Core Validation Frameworks

### 1. Peter Thiel's 7 Questions (Zero to One)

| # | Question | Evaluation criteria | Points |
|---|------|----------|------|
| **1. Engineering** | Can you build a **10x better technology**, not incremental improvement? | Disruptive vs incremental | 15 |
| **2. Timing** | Is **now** the right time for this business? | Market maturity, regulation, tech readiness | 10 |
| **3. Monopoly** | Do you start with **high share in a small market**? | Niche focus vs broad diffusion | 15 |
| **4. People** | Do you have the **right team**? | Founder-market fit | 10 |
| **5. Distribution** | Do you have a way to **deliver and sell** the product? | Channels, GTM strategy | 15 |
| **6. Durability** | Is it **defensible in 10-20 years**? | Moat durability | 15 |
| **7. Secret** | Did you discover a **non-obvious opportunity**? | Unique insight | 20 |

Source: [Zero to One](https://grahammann.net/book-notes/zero-to-one-peter-thiel)

---

### 2. Y Combinator PMF Indicators (Michael Seibel)

| Indicator | Description | Check |
|------|------|------|
| **Demand pressure** | Demand/usage outpaces ability to supply | ☐ |
| **Organic growth** | 40-60% from word of mouth | ☐ |
| **Support overload** | Customer requests become hard to handle | ☐ |
| **User pain on downtime** | Users react strongly when unavailable | ☐ |
| **Repeat usage** | Core metric shows frequent repeat behavior | ☐ |

**Pre-PMF checklist**:
- [ ] Is this a "hair-on-fire" problem?
- [ ] Would users adopt even a rough v1 from a tiny team?
- [ ] Are customers paying (or clearly willing to pay)?

Source: [Y Combinator Library](https://www.ycombinator.com/library/5z-the-real-product-market-fit)

---

### 3. The Mom Test (Rob Fitzpatrick)

**Three core rules**:

| Rule | Better question | Bad question |
|------|------------|------------|
| **Focus on customer life** | "How did you solve this last time?" | "Would you use our product?" |
| **Ask about past behavior** | "When was the last time you did X?" | "How often do you usually do X?" |
| **Listen more than talk** | silence and probing | long product pitch |

**Bad data to reject**:
- Empty praise ("Great idea")
- Hypothetical language ("I might use it")
- Feature wishlists without commitment

Source: [The Mom Test Summary](https://www.ricklindquist.com/notes/the-mom-test-by-rob-fitzpatrick)

---

### 4. Customer Development (Steve Blank)

| Stage | Key question | Evidence |
|------|------|------|
| **Customer Discovery** | Is the problem real? | 10+ interviews |
| **Customer Validation** | Is acquisition repeatable/scalable? | 5+ paying customers |
| **Customer Creation** | Can demand be generated systematically? | Organic growth signal |
| **Company Building** | Can the company operationalize growth? | Defined process |

Source: [Steve Blank](https://steveblank.com/tag/customer-development/)

---

### 5. JTBD Validation (Clayton Christensen)

**Forces of Progress**:

```
For change:
- PUSH: pain in current situation
- PULL: attraction of new solution

Against change:
- HABIT: inertia of current behavior
- ANXIETY: fear of switching
```

Decision signal: `Push + Pull > Habit + Anxiety`

Source: [Christensen Institute](https://www.christenseninstitute.org/theory/jobs-to-be-done/)

---

### 6. Lean Canvas Critical Checks

| Block | Validation question | Risk level |
|------|----------|----------|
| **Problem** | Are the top 3 problems real? | High |
| **Customer Segments** | Are early adopters clearly defined? | High |
| **UVP** | Can differentiation be explained in one sentence? | High |
| **Solution** | Can it be validated with MVP scope? | Medium |
| **Channels** | Is there a practical acquisition path? | Medium |
| **Revenue Streams** | Will users pay? | High |
| **Cost Structure** | Do unit economics work? | Medium |
| **Key Metrics** | Is one critical metric defined? | Medium |
| **Unfair Advantage** | Is there something hard to copy? | High |

Source: [Lean Canvas](https://leanstack.com/about)

</validation_frameworks>

---

<scoring_system>

## Scoring System

### Total score (100)

| Area | Weight | Rule |
|------|------|----------|
| **Thiel 7 questions** | 100 | Based on table above |
| **PMF readiness bonus** | +10 | If 3 or more PMF checks pass |
| **Critical-risk penalty** | -10 each | For each unresolved critical weakness |

### Grade bands

| Grade | Score | Verdict | Next step |
|------|------|------|----------|
| **S** | 90+ | Execute now | Full commitment, fundraising ready |
| **A** | 80-89 | Strong | Patch weaknesses and proceed |
| **B** | 70-79 | Promising | More validation required |
| **C** | 60-69 | Needs rethink | Consider pivot |
| **D** | 50-59 | Risky | Fundamental redesign |
| **F** | <50 | Stop recommended | Explore alternatives |

### Weakness severity

| Level | Meaning | Action |
|------|------|------|
| **Critical** | Failure likely if unresolved | Fix immediately |
| **Major** | Likely growth bottleneck | Fix within 6 months |
| **Minor** | Improvement opportunity | Lower priority |

</scoring_system>

---

<workflow>

| Phase | Task | Tool | Required check |
|-------|------|------|----------|
| **0** | Input check | - | Validate ARGUMENT |
| **1** | Understand idea | Sequential Thinking (3) | Extract 3 core hypotheses |
| **2** | Analyze 7 questions | Parallel Task x3 | Score + evidence for each question |
| **3** | Validate PMF/JTBD | Sequential Thinking (5) | Forces analysis + PMF checklist |
| **4** | Final assessment | Sequential Thinking (3) | Total score + grade + weakness map |
| **5** | Improvement roadmap | Sequential Thinking (3) | Prioritized actions |
| **6** | Save output | Write | `.hypercore/validation-results/` |

### Phase 1: Extract core hypotheses

```
Sequential Thinking:
  thought 1: define idea in one sentence
  thought 2: value hypothesis - do customers want this?
  thought 3: growth hypothesis - can this scale?
```

### Phase 2: Parallel 7-question analysis

```typescript
Task({ subagent_type: 'analyst', model: 'sonnet',
       prompt: 'Analyze Thiel Q1-2-3 (Engineering, Timing, Monopoly) with scores and evidence' })
Task({ subagent_type: 'analyst', model: 'sonnet',
       prompt: 'Analyze Thiel Q4-5 (People, Distribution) with scores and evidence' })
Task({ subagent_type: 'analyst', model: 'sonnet',
       prompt: 'Analyze Thiel Q6-7 (Durability, Secret) with scores and evidence' })
```

### Phase 3: Forces of Progress

```
Sequential Thinking:
  thought 1: PUSH - pain in status quo
  thought 2: PULL - attractiveness of new solution
  thought 3: HABIT - inertia of current behavior
  thought 4: ANXIETY - switching risks
  thought 5: estimate switching probability from force balance
```

### Phase 4: Final scoring

```
Sequential Thinking:
  thought 1: compute total 7-question score
  thought 2: evaluate PMF bonus
  thought 3: identify critical weaknesses and penalties
  thought 4: decide final grade
```

</workflow>

---

<result_structure>

| Section | Content |
|------|------|
| **Header** | date, idea name, total score/grade |
| **1. Executive summary** | one-line verdict + top strengths/weaknesses |
| **2. Thiel 7-question analysis** | per-question score + detailed rationale |
| **3. PMF readiness** | checklist + Forces analysis |
| **4. Weakness diagnosis** | severity classification + evidence |
| **5. Improvement roadmap** | immediate / 30-day / 90-day actions |
| **6. Go/No-Go** | final recommendation |

### Question analysis format

```markdown
### Q1. Engineering (10x technology) - [X]/15

**Current state**: ...
**10x benchmark**: ...
**Scoring rationale**: ...
**Improvement direction**: ...
```

### Weakness diagnosis format

```markdown
### [Critical] Weakness 1: [Title]

**Current state**: ...
**Risk if unresolved**: ...
**Fix**: ...
**Required resources**: ...
```

### Roadmap format

```markdown
## Immediate (This Week)
1. [Action] - [Goal] - [Owner]

## Within 30 Days
1. [Action] - [Goal] - [Owner]

## Within 90 Days
1. [Action] - [Goal] - [Owner]
```

</result_structure>

---

<examples>

```bash
/startup-validator crawling-based purchasing automation

Phase 1:
  - Core idea: AI crawls commerce products and automates buying workflows
  - Value hypothesis: purchasing agents suffer from manual workload
  - Growth hypothesis: 10x throughput leads to scalable revenue

Phase 2 (parallel):
  Q1 Engineering: 8/15
  Q2 Timing: 9/10
  Q3 Monopoly: 12/15
  Q4 People: 7/10
  Q5 Distribution: 10/15
  Q6 Durability: 8/15
  Q7 Secret: 12/20

Phase 3:
  PUSH: high manual pain
  PULL: high automation benefit
  HABIT: medium inertia
  ANXIETY: low to medium transition concern

Phase 4:
  total: 66/100 -> Grade C
  critical weakness: platform policy dependency
  major weakness: weak 10x technical moat

Saved: .hypercore/validation-results/00.purchasing-automation.md
```

</examples>

---

<validation>

| Item | Required |
|------|------|
| ARGUMENT | Ask immediately if missing |
| Phase 1 | Three hypotheses (one-line core/value/growth) |
| Phase 2 | **All 7 questions** scored with evidence |
| Phase 3 | **All four forces** + PMF checklist |
| Phase 4 | Total score + grade + severity map |
| Phase 5 | Immediate/30-day/90-day roadmap |
| Save | `.hypercore/validation-results/` |

| Forbidden |
|------|
| Start without ARGUMENT |
| Analyze only part of the 7 questions |
| Provide only qualitative judgment without scoring |
| Provide only positive review without weaknesses |
| Criticize without actionable improvements |
| End without saving output |

</validation>

---

<synergy_with_genius_thinking>

## Workflow with `genius-thinking`

| Step | Skill | Goal |
|------|------|------|
| 1 | `/genius-thinking` | Generate 10+ ideas |
| 2 | `/startup-validator` | Strictly validate top candidates |
| 3 | Final selection | Choose highest-scoring direction |

```bash
/genius-thinking AI healthcare startup ideas

/startup-validator [idea 1]
/startup-validator [idea 2]
/startup-validator [idea 3]
```

</synergy_with_genius_thinking>

---

<references>

**Core frameworks**:
- Zero to One: [Peter Thiel notes](https://grahammann.net/book-notes/zero-to-one-peter-thiel)
- Thiel 7 questions: [reference](https://fjbookclub.substack.com/p/zero-to-one-7-questions-every-business)
- PMF: [Y Combinator](https://www.ycombinator.com/library/5z-the-real-product-market-fit)
- Michael Seibel PMF notes: [YC blog](https://blog.ycombinator.com/the-real-product-market-fit/)

**Validation methods**:
- The Mom Test: [summary](https://www.ricklindquist.com/notes/the-mom-test-by-rob-fitzpatrick)
- Customer Development: [Steve Blank](https://steveblank.com/tag/customer-development/)
- Lean Canvas: [Ash Maurya](https://leanstack.com/about)
- JTBD: [Christensen Institute](https://www.christenseninstitute.org/theory/jobs-to-be-done/)

**Additional reading**:
- [How to Get Startup Ideas](https://paulgraham.com/startupideas.html)
- [The Lean Startup Principles](https://theleanstartup.com/principles)
- [Pretotyping](https://www.pretotyping.org/)

</references>
