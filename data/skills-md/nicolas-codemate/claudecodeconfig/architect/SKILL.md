---
name: architect
description: Software architecture skill for designing high-quality implementation plans. Provides universal patterns, quality checklists, and architectural guidelines. Use during planning phase to ensure plans are well-structured, atomic, and follow best practices.
---

# Architect Skill - Implementation Plan Design

This skill provides architectural guidance for creating high-quality implementation plans.
It focuses on universal principles applicable to any technology stack.

## When to Use

- During the PLAN phase of AEP workflow
- When reviewing an existing implementation plan
- When designing a new feature architecture
- When refactoring or restructuring code

## Core Principles

### 1. Atomic Phases

Each phase MUST be:
- **Self-contained**: Can be understood without reading other phases
- **Independently deployable**: Could theoretically be deployed alone
- **Reversible**: Can be rolled back without affecting other phases
- **Testable**: Has clear validation criteria

**Rule of thumb**: If a phase touches more than 3 files, it's probably too big.

### 2. Dependency Management

```
GOOD: Linear dependency chain
Phase 1 → Phase 2 → Phase 3

GOOD: Independent phases (can run in parallel)
Phase 1 ──┐
Phase 2 ──┼→ Phase 4
Phase 3 ──┘

BAD: Circular dependencies
Phase 1 ←→ Phase 2
```

**Always ask**: "Can this phase be completed if the next phase fails?"

### 3. Risk Ordering

Order phases by risk level (lowest risk first):
1. **Infrastructure** - New files, directories, configs (low risk)
2. **Data structures** - Types, interfaces, schemas (low-medium risk)
3. **Core logic** - Business rules, algorithms (medium risk)
4. **Integration** - Connecting components (medium-high risk)
5. **Migration** - Data changes, breaking changes (high risk)

### 4. Validation at Every Step

Each phase MUST specify:
- What to validate (tests, linter, manual check)
- Expected outcome
- How to verify success

## Phase Design Checklist

Before finalizing each phase, verify:

```
[ ] SCOPE
    [ ] Does this phase have a single, clear goal?
    [ ] Are all changes directly related to that goal?
    [ ] Would splitting this phase improve clarity?

[ ] FILES
    [ ] Are there 3 or fewer files modified?
    [ ] If more, is there a strong reason?
    [ ] Are all file paths explicit and correct?

[ ] DEPENDENCIES
    [ ] Are all dependencies on previous phases explicit?
    [ ] Can this phase run if the next phase fails?
    [ ] Are external dependencies documented?

[ ] VALIDATION
    [ ] Is there a concrete way to validate this phase?
    [ ] Are tests specified (new or existing)?
    [ ] Is the expected outcome clear?

[ ] ROLLBACK
    [ ] Can changes be reverted without side effects?
    [ ] Are database migrations reversible?
    [ ] Is there a rollback procedure documented?

[ ] COMMIT MESSAGE
    [ ] Does it follow conventional commits?
    [ ] Does it accurately describe the change?
    [ ] Is it in English and imperative mood?
```

## Plan-Level Checklist

Before finalizing the complete plan:

```
[ ] COMPLETENESS
    [ ] Does the plan fully address the original request?
    [ ] Are edge cases considered?
    [ ] Is error handling included?

[ ] ORDERING
    [ ] Are phases in optimal order (lowest risk first)?
    [ ] Are dependencies respected?
    [ ] Could any phases be parallelized?

[ ] TESTING STRATEGY
    [ ] Are unit tests included where appropriate?
    [ ] Are integration tests planned?
    [ ] Is manual verification documented?

[ ] DOCUMENTATION
    [ ] Will code changes require doc updates?
    [ ] Are API changes documented?
    [ ] Are breaking changes clearly marked?

[ ] RISKS
    [ ] Are potential risks identified?
    [ ] Are mitigations proposed?
    [ ] Is there a fallback if something goes wrong?
```

## Universal Patterns

### Pattern: Feature Flag Approach

For risky features, consider:
```
Phase 1: Add feature behind flag (disabled)
Phase 2: Implement feature logic
Phase 3: Add tests
Phase 4: Enable flag (or remove)
```

**Benefit**: Can ship incrementally, easy rollback.

### Pattern: Strangler Fig

For replacing existing code:
```
Phase 1: Create new implementation alongside old
Phase 2: Route new requests to new implementation
Phase 3: Migrate existing usages
Phase 4: Remove old implementation
```

**Benefit**: Never breaks existing functionality.

### Pattern: Database Migration Safety

For schema changes:
```
Phase 1: Add new column (nullable)
Phase 2: Dual-write to old and new
Phase 3: Backfill existing data
Phase 4: Make new column required
Phase 5: Remove old column
```

**Benefit**: Zero-downtime migrations.

### Pattern: API Evolution

For API changes:
```
Phase 1: Add new endpoint/field (don't remove old)
Phase 2: Update consumers to use new
Phase 3: Deprecate old endpoint/field
Phase 4: Remove old (after deprecation period)
```

**Benefit**: Backwards compatibility maintained.

### Pattern: Test-First Integration

For complex integrations:
```
Phase 1: Write integration tests (failing)
Phase 2: Implement minimal passing version
Phase 3: Refine and optimize
Phase 4: Add edge case handling
```

**Benefit**: Clear success criteria from start.

## Anti-Patterns to Avoid

### Anti-Pattern: Big Bang Phase

**Bad**:
```markdown
## Phase 1: Implement the feature
- Modify 15 files
- Add database tables
- Create API endpoints
- Add frontend components
```

**Fix**: Split into focused phases by layer/concern.

### Anti-Pattern: Hidden Dependencies

**Bad**:
```markdown
## Phase 2: Add validation
(secretly depends on Phase 4's utility functions)
```

**Fix**: Make dependencies explicit or reorder phases.

### Anti-Pattern: Optimistic Validation

**Bad**:
```markdown
**Validation**: Should work
```

**Fix**: Specify concrete command: `make test`, `npm run lint`, etc.

### Anti-Pattern: Implicit Rollback

**Bad**:
```markdown
## Phase 3: Migrate user data
(no mention of what happens if it fails)
```

**Fix**: Add rollback procedure or mark as high-risk.

### Anti-Pattern: Kitchen Sink Commit

**Bad**:
```markdown
**Commit message**: `feat: add feature and fix bugs and refactor`
```

**Fix**: One concern per phase = one clear commit message.

## Plan File Format

Plans MUST follow this format for compatibility with `solo-implement.sh`:

```markdown
---
feature: {ticket-id-slug}
ticket_id: {ticket-id}
created: {ISO timestamp}
status: pending
total_phases: {N}
---

# {ticket-id}: Implementation Plan - {title}

## Overview

{Brief description of what will be implemented}

---

## Phase 1: {Phase Title}

**Goal**: {What this phase accomplishes}

### Files to modify/create

- `path/to/file.ext` - Description of changes

### Validation

{Concrete command: make test, phpunit tests/Specific/, npm run lint, etc.}

### Commit message

```
{conventional commit: feat|fix|refactor(scope): description}
```

---

## Phase 2: {Phase Title}

...

---

## Summary

| Phase | Description | Files | Complexity |
|-------|-------------|-------|------------|
| 1 | ... | N | Low/Medium/High |
| 2 | ... | N | Low/Medium/High |
```

**Important**:
- Frontmatter is REQUIRED for `solo-implement.sh` automation
- Phase headers MUST follow format: `## Phase N: Title`
- Commit messages MUST be in code blocks
- Validation MUST be concrete commands, not "should work"

## Output Format

When using this skill during planning, structure architectural decisions as:

```markdown
## Architectural Decisions

### Decision 1: [Title]
- **Context**: Why this decision is needed
- **Options considered**: What alternatives exist
- **Decision**: What was chosen
- **Rationale**: Why this option
- **Consequences**: What this implies for implementation

### Phase Structure Rationale
- Why phases are ordered this way
- Which phases could potentially be parallelized
- Where the highest risk lies
```

## Integration with AEP

This skill is designed to be invoked during AEP's PLAN phase:

1. AEP completes ANALYSE and EXPLORE
2. Before creating the plan, invoke Architect skill
3. Apply checklists to each phase
4. Validate plan structure against anti-patterns
5. Document architectural decisions
6. Output final plan with confidence

## Language

**ALL OUTPUT MUST BE IN FRENCH** when communicating with the user.
Technical terms and commit messages remain in English.

