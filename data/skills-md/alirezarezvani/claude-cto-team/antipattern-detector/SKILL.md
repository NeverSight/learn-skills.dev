---
name: antipattern-detector
description: Detect common technical and organizational anti-patterns in proposals, architectures, and plans. Use when strategic-cto-mentor needs to identify red flags before they become problems.
---

# Anti-Pattern Detector

Identifies recurring failure patterns in technical decisions, organizational structures, and project plans.

## When to Use

- Reviewing architecture proposals
- Evaluating project plans and roadmaps
- Assessing team structures and processes
- Validating technology choices
- Checking migration strategies

## Why Anti-Patterns Matter

Anti-patterns are **proven failure modes**. They look reasonable on the surface but lead to predictable problems:

- **Technical debt accumulation**
- **Team burnout and turnover**
- **Missed deadlines and budgets**
- **System instability**
- **Organizational dysfunction**

Detecting them early saves months of pain.

---

## Anti-Pattern Categories

### 1. Architecture Anti-Patterns

Structural problems in system design.

| Pattern | Description | Symptoms |
|---------|-------------|----------|
| **Big Ball of Mud** | No clear architecture, everything coupled | Can't change X without breaking Y |
| **Golden Hammer** | Using one tech for everything | "We'll use Kubernetes for that too" |
| **Premature Microservices** | Splitting before understanding boundaries | 3 devs managing 20 services |
| **Distributed Monolith** | Microservices with tight coupling | Deploy all services together |
| **Resume-Driven Development** | Tech choices for career, not product | "Let's use Rust for the admin panel" |

### 2. Timeline Anti-Patterns

Planning failures that guarantee missed deadlines.

| Pattern | Description | Symptoms |
|---------|-------------|----------|
| **Timeline Fantasy** | Optimistic estimates ignoring reality | "6 weeks if everything goes well" |
| **Scope Creep Blindness** | Not accounting for inevitable additions | Same deadline, 2x features |
| **Parallel Path Delusion** | Assuming unlimited parallelization | "Add more devs to go faster" |
| **MVP Maximalism** | MVP that's actually V3 | 47 features in "minimum" product |
| **Demo-Driven Development** | Building for demos, not production | "It works on my machine" |

### 3. Team Anti-Patterns

Organizational structures that create dysfunction.

| Pattern | Description | Symptoms |
|---------|-------------|----------|
| **Hero Culture** | Reliance on key individuals | "Only Sarah can fix that" |
| **Knowledge Silos** | Critical info in one person's head | Bus factor of 1 |
| **Conway's Law Violation** | Architecture doesn't match team structure | Team boundaries ≠ service boundaries |
| **Understaffed Ambition** | Big plans with tiny teams | 2 devs building "the platform" |
| **Absent Ownership** | No clear owner for components | Bugs fall through cracks |

### 4. Process Anti-Patterns

Workflow failures that slow delivery.

| Pattern | Description | Symptoms |
|---------|-------------|----------|
| **Cargo Cult Agile** | Agile ceremonies without principles | Standups but no shipping |
| **Analysis Paralysis** | Over-planning, under-executing | Month 3 of "finalizing requirements" |
| **Infinite Refactoring** | Never shipping, always "improving" | "One more cleanup before release" |
| **Documentation Theater** | Docs that no one reads or maintains | 200-page spec, outdated day 1 |
| **Meeting Madness** | More meetings than coding time | "Let's schedule a meeting to discuss" |

### 5. Technology Anti-Patterns

Poor technology decisions.

| Pattern | Description | Symptoms |
|---------|-------------|----------|
| **Shiny Object Syndrome** | Chasing latest tech without reason | "We should rewrite in [new thing]" |
| **Not Invented Here** | Building what should be bought | Custom auth, custom logging, custom everything |
| **Vendor Lock-in Denial** | Ignoring exit costs | "We can always migrate later" |
| **Premature Optimization** | Optimizing before measuring | Caching layer with 10 users |
| **Framework Overload** | Too many frameworks/libraries | 47 npm dependencies for a button |

---

## Detection Process

### Step 1: Scan for Signals

Look for these phrases that often indicate anti-patterns:

**Timeline signals**:
- "If everything goes well..."
- "We can do it faster if we're focused..."
- "Just need to hire..."
- "Should only take..."

**Architecture signals**:
- "We'll figure out the boundaries later..."
- "Everything talks to everything..."
- "It's only for now..."
- "We can always refactor..."

**Team signals**:
- "Only [person] knows..."
- "We'll hire for that..."
- "[Person] will handle all of..."
- "The team can absorb..."

**Process signals**:
- "We don't need docs for this..."
- "We'll add tests later..."
- "Let's discuss in the meeting..."
- "Requirements are still evolving..."

### Step 2: Verify Pattern Match

For each suspected anti-pattern:

1. **Identify the pattern**: Which specific anti-pattern?
2. **Gather evidence**: What in the proposal matches?
3. **Assess severity**: How bad is it? (Critical/High/Medium/Low)
4. **Check context**: Could this be a reasonable exception?

### Step 3: Document Findings

```markdown
### Anti-Pattern: [Name]

**Category**: Architecture / Timeline / Team / Process / Technology
**Severity**: Critical / High / Medium / Low

**Evidence**:
- [Quote or observation 1]
- [Quote or observation 2]

**Why This Is a Problem**:
[Explain the typical failure mode]

**Historical Examples**:
[Reference similar failures if known]

**Recommendation**:
[Specific action to address]
```

---

## Severity Framework

### Critical
Will cause project failure if not addressed.
- **Examples**: No clear ownership, timeline fantasy for commitments, hero dependency
- **Action**: Stop and address before proceeding

### High
Will cause significant problems.
- **Examples**: Premature microservices, understaffed plans, shiny object syndrome
- **Action**: Address in planning phase

### Medium
Will cause friction and delays.
- **Examples**: Documentation gaps, process inefficiencies, minor scope creep
- **Action**: Include in risk mitigation

### Low
Worth noting but manageable.
- **Examples**: Style inconsistencies, minor tech debt, preference-based choices
- **Action**: Track and address opportunistically

---

## Output Format

```markdown
# Anti-Pattern Analysis: [Plan/Proposal Name]

## Summary
- **Patterns Detected**: [Count]
- **Critical Issues**: [Count]
- **Overall Risk Level**: Critical / High / Medium / Low

## Critical Issues (Must Address)

### 1. [Pattern Name]
**Category**: [Category]
**Evidence**: [What triggered this detection]
**Risk**: [What will go wrong]
**Fix**: [How to address]

---

## High-Priority Issues (Should Address)

### 2. [Pattern Name]
[Same format]

---

## Medium-Priority Issues (Consider Addressing)

### 3. [Pattern Name]
[Same format]

---

## Patterns NOT Detected
[List patterns that were checked but not found - provides confidence]

## Recommendations

### Before Proceeding
1. [Critical action 1]
2. [Critical action 2]

### During Execution
1. [Mitigation 1]
2. [Mitigation 2]

### Monitoring
- [Warning sign to watch for]
- [Metric to track]
```

---

## Common Pattern Combinations

Certain anti-patterns tend to appear together:

### The Startup Death Spiral
- Timeline Fantasy + Understaffed Ambition + Hero Culture
- Result: Burnout, missed deadlines, key person leaves

### The Enterprise Trap
- Analysis Paralysis + Documentation Theater + Meeting Madness
- Result: Nothing ships, team frustrated, competition wins

### The Tech Debt Avalanche
- "We'll refactor later" + No clear ownership + Premature optimization
- Result: System becomes unmaintainable, rewrite required

### The Microservices Mistake
- Premature Microservices + Distributed Monolith + Not enough DevOps
- Result: Complexity explosion, slower delivery than monolith

---

## Integration with Validation

The antipattern-detector feeds into the broader validation workflow:

```
Proposal/Plan
     │
     ▼
[assumption-challenger] → Assumptions identified
     │
     ▼
[antipattern-detector] → Patterns identified
     │
     ▼
[validation-report-generator] → Combined 8-section report
```

---

## References

- [Anti-Pattern Catalog](antipattern-catalog.md) - Complete catalog with examples
- [Challenge Questions](../assumption-challenger/challenge-questions.md) - Questions to probe for patterns
