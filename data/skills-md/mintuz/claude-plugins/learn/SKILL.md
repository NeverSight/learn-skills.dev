---
name: learn
description: WHEN capturing learnings/gotchas/decisions into CLAUDE.md; NOT trivial changes; guides what to record, where it lives, and format.
---

# CLAUDE.md Learning Integration

Use this skill to identify learning opportunities and document insights into CLAUDE.md. The goal is to ensure hard-won knowledge is preserved for future developers.

## When to Use

- User discovers a gotcha or unexpected behavior
- User completes a complex feature and wants to document learnings
- User makes an architectural decision worth preserving
- User fixes a tricky bug with insights to share
- User says "I wish I'd known this earlier"

## Philosophy

**Core Principle:** Knowledge that isn't documented is knowledge that will be lost. Every hard-won insight must be preserved for future developers.

## Identifying Learning Opportunities

Watch for these signals during development:

- Gotchas or unexpected behavior discovered
- "Aha!" moments or breakthroughs
- Architectural decisions being made
- Patterns that worked particularly well
- Anti-patterns encountered
- Tooling or setup knowledge gained

## Discovery Questions

### About the Problem

- What was unclear or surprising at the start?
- What took longer to figure out than expected?
- What assumptions were wrong?
- What would have saved time if known upfront?

### About the Solution

- What patterns or approaches worked particularly well?
- What patterns should be avoided?
- What gotchas or edge cases were discovered?
- What dependencies or relationships were not obvious?

### About the Context

- What domain knowledge is now clearer?
- What architectural decisions became apparent?
- What testing strategies were effective?
- What tooling or setup was required?

## Learning Significance Assessment

**Document if ANY of these are true:**

- Would save future developers significant time (>30 minutes)
- Prevents a class of bugs or errors
- Reveals non-obvious behavior or constraints
- Captures architectural rationale or trade-offs
- Documents domain-specific knowledge
- Identifies effective patterns or anti-patterns
- Clarifies tool setup or configuration gotchas

**Skip if ALL of these are true:**

- Already well-documented in CLAUDE.md
- Obvious or standard practice
- Trivial change (typos, formatting)
- Implementation detail unlikely to recur

## CLAUDE.md Section Classification

Determine which section the learning belongs to:

### Existing Sections

- **Core Philosophy** - Fundamental principles (TDD, FP, immutability)
- **Testing Principles** - Test strategy and patterns
- **TypeScript Guidelines** - Type system usage
- **Code Style** - Functional patterns, naming, structure
- **Development Workflow** - TDD process, refactoring, commits
- **Working with Claude** - Expectations and communication
- **Example Patterns** - Concrete code examples
- **Common Patterns to Avoid** - Anti-patterns

### New Sections (if learning doesn't fit existing)

- Project-specific setup instructions
- Domain-specific knowledge
- Architectural decisions
- Tool-specific configurations
- Performance considerations
- Security patterns

## Formatting Guidelines

### For Principles/Guidelines

````markdown
### New Principle Name

Brief explanation of why this matters.

**Key points:**

- Specific guideline with clear rationale
- Another guideline with example
- Edge case or gotcha to watch for

```typescript
// ✅ GOOD - Example following the principle
const example = "demonstrating correct approach";

// ❌ BAD - Example showing what not to do
const bad = "demonstrating wrong approach";
```
````

### For Gotchas/Edge Cases

````markdown
#### Gotcha: Descriptive Title

**Context**: When does this occur
**Issue**: What goes wrong
**Solution**: How to handle it

```typescript
// ✅ CORRECT - Solution example
const correct = handleEdgeCase();

// ❌ WRONG - What causes the problem
const wrong = naiveApproach();
```
````

### For Project-Specific Knowledge

```markdown
## Project Setup / Architecture / Domain Knowledge

### Specific Area

Clear explanation with:

- Why this is important
- How it affects development
- Examples where relevant
```

## Documentation Proposal Format

````markdown
## CLAUDE.md Learning Integration

### Summary

Brief description of what was learned and why it matters.

### Proposed Location

**Section**: [Section Name]
**Position**: [Before/After existing content, or new section]

### Proposed Addition

```markdown
[Exact markdown content to add to CLAUDE.md]
```

### Rationale

- Why this learning is valuable
- How it fits with existing guidelines
- What problems it helps prevent
- Time saved by documenting this

### Verification Checklist

- [ ] Learning is not already documented
- [ ] Fits naturally into CLAUDE.md structure
- [ ] Maintains consistent voice and style
- [ ] Includes concrete examples if applicable
- [ ] Prevents future confusion or wasted time
````

## Voice and Style

- **Imperative tone**: "Use X", "Avoid Y", "Always Z"
- **Clear rationale**: Explain WHY, not just WHAT
- **Concrete examples**: Show good and bad patterns
- **Emphasis markers**: Use **bold** for critical points, ❌ ✅ for anti-patterns
- **Structured format**: Use headings, bullet points, code blocks consistently

## Quality Standards

- **Actionable**: Reader should know exactly what to do
- **Specific**: Avoid vague guidelines
- **Justified**: Explain the reasoning and consequences
- **Discoverable**: Use clear headings and keywords
- **Consistent**: Match existing CLAUDE.md conventions

## Quality Gates

Before proposing documentation, verify:

- Learning is significant and valuable
- Not already documented in CLAUDE.md
- Includes concrete examples (good and bad)
- Explains WHY, not just WHAT
- Matches CLAUDE.md voice and style
- Properly categorized in appropriate section
- Actionable (reader knows exactly what to do)

## Example Learning Integration

````markdown
## CLAUDE.md Learning Integration

### Summary

Discovered that Zod schemas must be exported from a shared location for test files to import them, preventing schema duplication in tests.

### Proposed Location

**Section**: Schema-First Development with Zod
**Position**: Add new subsection "Schema Exports and Imports"

### Proposed Addition

```markdown
#### Schema Organization for Tests

**CRITICAL**: All schemas must be exported from a shared module that both production and test code can import.

```typescript
// ✅ CORRECT - Shared schema module
// src/schemas/payment.schema.ts
export const PaymentSchema = z.object({
  amount: z.number().positive(),
  currency: z.string().length(3),
});
export type Payment = z.infer<typeof PaymentSchema>;

// src/services/payment.service.ts
import { PaymentSchema, type Payment } from "../schemas/payment.schema";

// src/services/payment.service.test.ts
import { PaymentSchema, type Payment } from "../schemas/payment.schema";
```

**Why this matters:**

- Tests must use the exact same schemas as production code
- Prevents schema drift between tests and production
- Ensures test data factories validate against real schemas
- Changes to schemas automatically propagate to tests

**Common mistake:**

```typescript
// ❌ WRONG - Redefining schema in test file
// payment.service.test.ts
const PaymentSchema = z.object({
  /* duplicate definition */
});
```
```

### Rationale

- Encountered this when tests were failing due to schema mismatch
- Would have saved 30 minutes if schema export pattern was documented
- Prevents future schema duplication violations
- Directly relates to existing "Schema Usage in Tests" section

### Verification Checklist

- [x] Learning is not already documented
- [x] Fits naturally into Schema-First Development section
- [x] Maintains consistent voice with CLAUDE.md
- [x] Includes concrete examples showing right and wrong approaches
- [x] Prevents the specific confusion encountered during this task
````
