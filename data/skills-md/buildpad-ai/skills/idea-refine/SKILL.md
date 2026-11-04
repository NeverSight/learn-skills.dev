---
name: idea-refine
description: Refines vague ideas into concrete proposals. Use when you have a rough concept that needs exploration, or when requirements are vague and need structured thinking before specification.
---

# Idea Refinement

## Overview

Structured divergent/convergent thinking to turn vague ideas into concrete proposals. Before writing specs or code, ensure the idea is well-formed: the problem is clear, the audience is defined, the scope is bounded, and alternatives have been considered.

## When to Use

- You have a rough concept that needs exploration
- Requirements are vague ("I want a dashboard")
- Multiple approaches exist and you need to choose
- Stakeholders have different visions of the solution

**When NOT to use:** When requirements are already clear and specific — go straight to `spec-driven-development`.

## The Refinement Process

### Phase 1: Diverge (Explore)

Ask expansive questions to understand the full problem space:

```
PROBLEM SPACE:
1. What problem are we solving?
2. Who has this problem? (specific users/roles)
3. How is it solved today? (current workarounds)
4. What happens if we don't solve it?
5. What does "good enough" look like?

SOLUTION SPACE:
6. What are 3 different approaches?
7. What does each approach trade off?
8. What similar solutions exist? (prior art)
9. What constraints exist? (technical, budget, timeline)
10. What would make this fail?
```

### Phase 2: Converge (Focus)

Narrow down to a specific, actionable proposal:

```
PROPOSAL:
- Problem statement: [one sentence]
- Target users: [specific roles]
- Core solution: [chosen approach]
- Key features: [3-5 must-haves]
- Out of scope: [explicit exclusions]
- Success metric: [how to measure]
```

### Phase 3: Validate

Before proceeding to specification:

```
VALIDATION:
- [ ] Problem is real (users actually have this pain)
- [ ] Solution addresses the core problem (not a symptom)
- [ ] Scope is bounded (clear what's included and excluded)
- [ ] Approach is feasible with current stack (Next.js and the project's Buildpad backend: DaaS + Supabase, or the Buildpad Engine)
- [ ] DaaS built-in features are leveraged (not rebuilt)
- [ ] One or more alternatives were considered and rejected with reasons
```

## DaaS Platform Check

Before refining any data-centric idea, check what DaaS provides out of the box:

| If the idea involves... | DaaS already has... |
|------------------------|---------------------|
| Tracking changes | Automatic activity/audit logging |
| Approval processes | Workflow state machines |
| Content drafts | Versioning API |
| File management | Files API |
| Scheduled tasks | Cron jobs |
| Access control | RBAC (roles, policies, permissions) |
| Data partitioning | Scope system (multi-tenancy; on an Engine project the project is one tenant and its scopes sit below it) |
| Data import/export | Utils API |

**If DaaS provides it, the idea refinement should focus on how to configure and present it — not whether to build it.**

## Output Format

```markdown
## Idea: [Name]

### Problem
[Clear statement of the problem and who has it]

### Proposed Solution
[Chosen approach with rationale]

### Key Features
1. [Must-have feature]
2. [Must-have feature]
3. [Must-have feature]

### Out of Scope
- [Explicit exclusion]

### DaaS Features to Leverage
- [Built-in feature and how it applies]

### Alternatives Considered
| Approach | Pros | Cons | Why not |
|----------|------|------|---------|

### Next Steps
- [ ] Write spec (use `spec-driven-development`)
- [ ] Break into tasks (use `planning-and-task-breakdown`)
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I already know what to build" | You know what you think you want. Refinement catches wrong assumptions. |
| "We need to move fast" | Building the wrong thing fast is the slowest path. |
| "Let's just prototype it" | Prototypes without problem clarity become production code. |
| "The user will tell us what's wrong" | Users can identify problems but rarely articulate solutions. |

## Verification

After refinement:

- [ ] Problem statement is clear and specific
- [ ] Target users are identified
- [ ] At least 2 alternatives were considered
- [ ] DaaS built-in features checked for overlap
- [ ] Scope boundaries are explicit
- [ ] Ready to proceed to specification
