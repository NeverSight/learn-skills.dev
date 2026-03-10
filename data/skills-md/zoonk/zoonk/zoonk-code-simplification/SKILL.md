---
name: zoonk-code-simplification
description: Review code for simplification opportunities and detect overengineering. Use when reviewing new code, refactoring, or verifying that an implementation follows the "less is more" principle.
license: MIT
metadata:
  author: zoonk
  version: "1.0.0"
---

# Code Simplification

A ruthless approach to eliminating unnecessary complexity. The core principle: **the best code is the code you don't write**.

## Before Suggesting Changes

**CRITICAL: Research before suggesting.**

1. **Read project guidelines** - Check for AGENTS.md, CLAUDE.md, or similar documentation
2. **Search for existing patterns** - Find how similar code is written elsewhere in the codebase
3. **Understand the "why"** - A pattern that looks verbose might exist for good reasons (framework requirements, established conventions, etc.)

**Never suggest a simplification that:**

- Contradicts patterns documented in project guidelines
- Differs from how the same thing is done elsewhere in the codebase
- Breaks framework requirements
- Removes code that exists for a documented reason

## Patterns to Flag

### Over-abstraction

Creating interfaces/types/wrappers for things used only once.

### Premature Generalization

Building for flexibility that isn't needed yet. YAGNI (You Aren't Gonna Need It).

### Unnecessary State

Using `useState`/`useEffect` when derived values or server-rendered data suffice.

### Verbose Patterns

Long-form code when concise alternatives exist:

- Optional chaining (`?.`) instead of nested conditionals
- Nullish coalescing (`??`) instead of `|| defaultValue` with falsy edge cases
- Object shorthand, destructuring, spread operators

### Copy-Paste with Variations

Code that should be a simple parameterized function.

### Configuration Over Convention

Custom setup when defaults would work fine.

### Pass-Through Wrappers

Components or functions that just forward to another without adding meaningful behavior.

## Review Process

### Step 1: Gather Context

1. Read project documentation (AGENTS.md, README, etc.)
2. Search codebase for similar patterns
3. Identify framework/library conventions

### Step 2: Analyze Against Conventions

1. Does the code follow established patterns?
2. Is there similar code elsewhere that follows the same pattern?
3. Are there framework requirements that justify the structure?
4. Would the suggested simplification break any conventions?

### Step 3: Evaluate Simplification Opportunities

1. Is this the cleanest approach within the project's conventions?
2. Is there a simpler way that still follows established patterns?
3. What can be deleted without breaking conventions?
4. Is every abstraction earning its keep?

## Output Format

### Context Gathered

Briefly list what you researched before making suggestions:

- Project conventions reviewed
- Similar patterns found in codebase
- Framework requirements identified

### Simplification Opportunities

For each issue:

1. **What**: Brief description of the complexity
2. **Why it's overengineered**: Explain the unnecessary complexity
3. **Verified against conventions**: Confirm this doesn't break project patterns
4. **Simpler alternative**: Show the cleaner approach with code
5. **Impact**: Lines saved, cognitive load reduced, or maintenance simplified

### Verdict

- **Clean** - This code is already minimal. Ship it.
- **Minor tweaks** - A few small simplifications possible.
- **Needs simplification** - Significant complexity that should be addressed.
- **Overengineered** - This needs a fundamental rethink.

## Principles

- **Research first, suggest second** - Never propose changes without understanding project context
- Be direct and specific. Don't soften feedback with excessive qualifiers.
- Always provide concrete alternatives, not just criticism.
- Recognize that sometimes complexity is warranted—explain when the current approach is justified.
- Consider maintainability: simpler code is easier to debug, test, and modify.
- Remember: every line of code is a liability. Fewer lines = fewer bugs = less maintenance.
- **When in doubt, search the codebase** - If you're unsure about a pattern, find how it's done elsewhere

The goal is code so clean and obvious that it barely needs comments because the intent is crystal clear. But never sacrifice correctness or convention-compliance for brevity.
