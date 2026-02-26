---
name: write-user-story
description: Use when creating, writing, or refining a user story or ticket. Produces structured stories with purpose/overview, functional requirements, Given-When-Then acceptance criteria, and manual testing guidance. Also use when asked to define acceptance criteria, scope a feature, or prepare a story for development.
license: Apache-2.0
metadata:
  author: folio-org
  version: "1.0.0"
---

# Write User Story

## User Story Structure

Every story must have these sections (in order):

1. **Purpose/Overview** — What it achieves and why. Include business context, user persona, and links. Optionally add a _Technical Details/Approach_ sub-section for architectural decisions without over-specifying implementation.
2. **Requirements/Scope** — Functional requirements (specific, measurable). Non-functional requirements only when they have measurable impact. Out of Scope only when genuine ambiguity exists.
3. **Acceptance Criteria** — Testable conditions in Given-When-Then format.
4. **Testing Guidance** — Manual testing scenarios only. No unit/integration test specs.

## Template

```markdown
## Purpose/Overview

[High-level description of what this story achieves and why it's important.
Include business context, user persona, and links to related work.]

### Technical Details/Technical Approach (Optional)

[Architectural decisions or implementation strategy — don't over-specify.]

---

## Requirements/Scope

### Functional Requirements
1. [Specific functionality to implement]
2. [Input/output expectations]
3. [Business rules and constraints]

### Non-Functional Requirements (only if significant)
1. [Data integrity requirements]
2. [Performance — only if measurable impact]
3. [Security — only if specific requirements exist]

### Out of Scope (only if needed for clarity)
- [Include ONLY if there's genuine ambiguity about scope]

---

## Acceptance Criteria

**AC1: [Scenario name]**
- Given [initial context]
  When [action occurs]
  Then [expected outcome]

**AC2: [Error handling scenario]**
- Given [error condition]
  When [action occurs]
  Then [expected error behavior]

---

## Testing Guidance

### Manual Testing

**Scenario 1: [Primary user workflow]**
1. [Step-by-step instructions]
2. [Expected outcomes]

**Scenario 2: [Edge case]**
1. [Steps]
2. [Expected outcomes]

**Note:** Unit test specs, integration test code, and test data details belong in the implementation plan, not here.

---

## Additional Notes (optional)

[Risks, dependencies, or other considerations]

## Related Links (optional)
- [Design documents, API specs, related stories]
```

## Writing Guidelines

### Standard User Story Format
```
As a [user persona/role]
I want [goal/desire]
So that [benefit/value]
```

### INVEST Principles
- **I**ndependent — deliverable separately
- **N**egotiable — details can be refined
- **V**aluable — delivers clear value
- **E**stimable — team can estimate effort
- **S**mall — completable within one sprint
- **T**estable — clear verification criteria

## Best Practices

### Do's ✓
1. Write from the user perspective — focus on value, not implementation
2. Make acceptance criteria specific and testable
3. Include error scenarios and edge cases
4. Use consistent domain terminology
5. Link dependencies and related stories
6. Collaborate with developers, testers, and stakeholders

### Don'ts ✗
1. Don't write technical tasks as stories ("Refactor UserService" is a task, not a story)
2. Don't be vague — "improve performance" needs metrics
3. Don't skip acceptance criteria
4. Don't add non-functional requirements unless they have measurable impact
5. Don't add "Out of Scope" unless there's genuine ambiguity
6. Don't include unit/integration test specs in Testing Guidance
7. Don't over-specify implementation — leave the "how" to developers

## Quick Reference Checklist

- [ ] Purpose clearly explains the value and context
- [ ] Requirements are specific and measurable
- [ ] Acceptance criteria are testable and unambiguous
- [ ] Error scenarios and edge cases are covered
- [ ] Testing guidance contains manual scenarios only
- [ ] Dependencies are identified and linked
- [ ] Story is sized for one sprint
- [ ] Technical approach is outlined if needed, but not over-specified
- [ ] Non-functional requirements included only if significant
- [ ] "Out of Scope" omitted unless genuinely needed

For deep-dive guidance on each section, see [references/section-details.md](references/section-details.md).
For common pitfalls with before/after examples, see [references/pitfalls.md](references/pitfalls.md).
For a complete example story, see [references/example.md](references/example.md).
For JIRA markup conversion, see [references/jira.md](references/jira.md).
