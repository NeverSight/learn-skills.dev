---
name: product-discovery
description: Methodology for discovering and specifying new software products. Use when starting greenfield projects, exploring new ideas, or defining MVP scope.
---

# Product Discovery Skill

Transform vague ideas into actionable specifications through structured questioning.

## Core Methodology

### Questioning Frameworks

**Five Whys** - Reach root problems:
1. "Why is this a problem?" → Surface answer
2. "Why does that matter?" → Deeper impact
3. Continue until you reach the core motivation

**MECE** (Mutually Exclusive, Collectively Exhaustive):
- Cover all aspects without overlap
- Users, features, constraints, success criteria

**Socratic Probing**:
- Never accept surface-level answers
- "Can you give me a specific example?"
- "What would happen if...?"

## Discovery Phases

### Phase 1: Vision
**Key Questions:**
- "What moment made you think 'someone should build this'?"
- "If this existed perfectly, walk me through using it tomorrow"
- "Fast forward one year - what changed in the world?"

### Phase 2: Core Problem
**Key Questions:**
- "If you could only solve ONE aspect, which unlocks the most value?"
- "What's the smallest thing that would make one person genuinely grateful?"
- "What part do you understand best? What's still fuzzy?"

**Scope Control:**
- "If you had budget for only 3 features, which would they be?"
- "Now pick just ONE to prove the concept"

### Phase 3: Users
**Key Questions:**
- "Think of one specific person who needs this. What's their name? Their story?"
- "What do they do immediately before/after using your software?"
- "Which user type would be easiest to satisfy? Hardest?"

### Phase 4: Technical
**Key Questions:**
- "What could you hardcode for MVP that becomes dynamic later?"
- "Which technical decisions can wait until concept is validated?"
- "What existing tools could you leverage instead of building?"

### Phase 5: Validation
**Key Questions:**
- "How would you know, objectively, that MVP is working?"
- "What number would make you confident to continue? What would make you pivot?"
- "What feedback would change your direction most dramatically?"

### Phase 6: Scoping
**Effort-Based Framing (NOT time-based):**

| Scope Level | Definition |
|-------------|------------|
| **Core MVP** | Solves ONE problem for ONE user type |
| **Expanded MVP** | Multiple features, still single user focus |
| **Full Vision** | Complete feature set, all user types |

## Facilitation Techniques

### When They're Stuck
- Offer contrasts: "Would you rather have X or Y? Why?"
- Provide examples: "Some approach this as a marketplace, others as a tool..."
- Break it down: "Let's start with just the first step"

### When They're Overcomplicating
- "That's a powerful feature. For MVP, what's the simplest version?"
- "Let's put that in the 'full vision' bucket for now"
- "On a scale of 1-10, how much value vs how much effort?"

### When They're Too Vague
- "Walk me through the exact steps someone would take"
- "What would the screen look like at this moment?"
- "When you say 'fast', what specific measurement?"

## Document Templates

### SPEC.md (What to Build)
```markdown
# [Project Name] Specification

## Problem Statement
[Core problem, why it matters, who has it]

## Target Users
- **Primary:** [Specific user type and needs]
- **Secondary:** [If applicable]

## MVP Scope (Core)
### Must Have
1. [Essential capability 1]
2. [Essential capability 2]

### Explicitly Excluded
- [Deferral 1 with reasoning]

## Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [User can accomplish X]

## Full Vision
[Complete feature list for later phases]

## Scenarios
### Scenario 1: [Name]
- Given: [Context]
- When: [Action]
- Then: [Outcome]
```

### DESIGN.md (How to Build It)
```markdown
# [Project Name] Technical Design

## Architecture Overview
[High-level system structure]

## Technology Choices
| Layer | Choice | Reasoning |
|-------|--------|-----------|
| Frontend | [Tech] | [Why] |
| Backend | [Tech] | [Why] |
| Database | [Tech] | [Why] |

## Data Models
### [Entity]
- field: type (constraints)

## Key Decisions
### [Decision]
- **Choice:** [What was decided]
- **Reasoning:** [Why]
- **Trade-offs:** [What we accept]

## Technical Risks
| Risk | Mitigation |
|------|------------|
| [Risk] | [How we handle it] |
```

### PLAN.md (Implementation Roadmap)
```markdown
# [Project Name] Implementation Plan

## MVP Scope
[Reference to SPEC.md MVP section]

## Implementation Order
### Phase 1: Foundation
- [ ] [Task 1]
- [ ] [Task 2]

### Phase 2: Core Features
- [ ] [Task 3]
- [ ] [Task 4]

### Phase 3: Polish & Launch
- [ ] [Task 5]
- [ ] Launch preparation

## Go/No-Go Criteria
### Continue if:
- [ ] [Success metric achieved]

### Pivot if:
- [ ] [Failure condition]

## Post-MVP Phases
### Phase 2 (After validation)
- [Feature additions]
```

## Specification Principles

- **Behaviors over implementation** - What the system does, not how
- **Examples over abstractions** - Concrete scenarios that illustrate
- **Constraints as features** - Limitations that shape the solution
- **Edge cases as teachers** - Unusual situations that clarify boundaries

These specs become context for AI implementation - clarity here multiplies effectiveness later.

---

## Version
- v1.0.0 (2025-12-05): Initial documented version
