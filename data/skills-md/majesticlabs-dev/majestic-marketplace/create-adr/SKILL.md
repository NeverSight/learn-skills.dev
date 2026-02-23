---
name: create-adr
description: Create Architecture Decision Records (ADRs) to document significant technical decisions, their context, alternatives considered, and consequences. Use when making architectural choices, selecting libraries/frameworks, or designing system components.
disable-model-invocation: true
---

# Create ADR Skill

**Purpose:** Document architectural decisions to provide context for future developers and maintain institutional knowledge about why technical choices were made.

## When to Use This Skill

Trigger this skill when:
- Making significant architectural decisions
- Choosing between competing technologies or approaches
- Designing new system components or APIs
- Refactoring that changes system structure
- After implementing a feature that involved design trade-offs

## Skip ADR Creation If

- Only minor bug fixes or refactoring
- Documentation or test-only changes
- Configuration tweaks without architectural impact
- Trivial changes with obvious implementation

## Workflow

### 1. Gather Context

Review the implementation to understand:
- What technical decisions were made
- Why this approach was chosen
- What alternatives existed
- What trade-offs were accepted

**If reviewing existing code:**
```bash
git diff main...HEAD
git log --oneline main..HEAD
```

### 2. Investigate Further

If the diff doesn't provide enough context:
- Read referenced files/functions
- Check configuration files
- Review related tests
- Look at dependencies added

### 3. Create the ADR

**Location:** `docs/adr/NNNN-descriptive-title.md`

**Naming convention:**
- Sequential number (0001, 0002, etc.)
- Lowercase with hyphens
- Descriptive but concise

**Examples:**
- `0001-use-jwt-for-authentication.md`
- `0002-adopt-event-sourcing-for-orders.md`
- `0003-postgres-over-mysql.md`

### 4. Use the Template

Use the template from `assets/adr-template.md` to structure the document.

**Key sections to complete:**
- **Status**: Proposed, Accepted, Deprecated, or Superseded
- **Context**: The problem or opportunity driving the decision
- **Decision**: What was decided and the technical approach
- **Consequences**: Positive, negative, and risks
- **Alternatives**: What else was considered and why it wasn't chosen

## Quality Guidelines

**Good ADRs have:**
- Specific technical details (not vague descriptions)
- Concrete examples and code snippets where helpful
- Honest assessment of trade-offs
- Links to relevant resources or prior art

**Avoid:**
- Vague justifications ("it's better")
- Missing alternatives section
- No discussion of consequences
- Too much implementation detail (that belongs in code comments)

## Example

**User:** "Document the decision to use Redis for caching"

**Skill activates:**

1. Review caching implementation
2. Identify alternatives considered (Memcached, in-memory, etc.)
3. Document trade-offs (complexity vs performance)
4. Create `docs/adr/0005-redis-for-application-cache.md`

## Integration

**Works well with:**
- Major feature implementations
- System refactoring efforts
- Technology migrations
- API design decisions
