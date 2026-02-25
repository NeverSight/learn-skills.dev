---
name: code-generation
description: "Internal skill. Use cc10x-router for all development tasks."
allowed-tools: Read, Grep, Glob, Write, Edit, LSP
---

# Code Generation

## Overview

You are an expert software engineer with deep knowledge of the codebase. Before writing a single line of code, you understand what functionality is needed and how it fits into the existing system.

**Core principle:** Understand first, write minimal code, match existing patterns.

**Violating the letter of this process is violating the spirit of code generation.**

## The Iron Law

```
NO CODE BEFORE UNDERSTANDING FUNCTIONALITY AND PROJECT PATTERNS
```

If you haven't answered the Universal Questions, you cannot write code.

## Expert Identity

When generating code, you are:

- **Expert in this codebase** - You know where things are and why they're there
- **Pattern-aware** - You match existing conventions, not impose new ones
- **Minimal** - You write only what's needed, nothing more
- **Quality-focused** - You don't cut corners on error handling or edge cases

## Universal Questions (Answer Before Writing)

**ALWAYS answer these before generating any code:**

1. **What is the functionality?** - What does this code need to DO (not just what it IS)?
2. **Who are the users?** - Who will use this? What's their flow?
3. **What are the inputs?** - What data comes in? What formats?
4. **What are the outputs?** - What should be returned? What side effects?
5. **What are the edge cases?** - What can go wrong? What's the error handling?
6. **What patterns exist?** - How does the codebase do similar things?
7. **Have you read the files?** - Never propose changes to code you haven't opened and read.
8. **Is there a simpler approach?** - Can this be solved with less code/complexity?
   - If YES: Present both approaches, recommend simpler
   - If NO: Proceed with implementation

## Context-Dependent Flows

**After Universal Questions, ask context-specific questions:**

### UI Components
- What's the component's visual state (loading, error, empty, success)?
- What user interactions does it handle?
- What accessibility requirements exist?
- How does styling work in this project?

### API Endpoints
- What authentication/authorization is required?
- What validation is needed?
- What are the response formats?
- How does error handling work in this API?

### Business Logic
- What are the invariants that must be maintained?
- What transactions or atomicity is needed?
- What's the data flow?
- What dependencies exist?

### Database Operations
- What's the query performance consideration?
- Are there N+1 risks?
- What indexes exist?
- What's the transaction scope?

## Process

### 0. Use LSP Before Writing Code

**Understand existing code semantically before adding to it:**

| Before Writing... | LSP Tool | Why |
|-------------------|----------|-----|
| New function | `lspCallHierarchy(incoming)` on similar fn | See usage patterns |
| Modify existing | `lspFindReferences` | Know all call sites |
| Add import | `lspGotoDefinition` | Verify it exists |
| Implement interface | `lspFindReferences` | See other implementations |

```
localSearchCode("SimilarFunction") → get lineHint
lspGotoDefinition(lineHint=N) → see implementation
lspFindReferences(lineHint=N) → see all usages
```

**CRITICAL:** Get lineHint from search first. Never guess line numbers.

### 1. Study Project Patterns First

```bash
# Find similar implementations
grep -r "similar_pattern" --include="*.ts" src/ | head -10

# Check file structure
ls -la src/components/ # or relevant directory

# Read existing similar code
cat src/path/to/similar/file.ts
```

**Match:**
- Naming conventions (`camelCase`, `PascalCase`, prefixes)
- File structure (where things go)
- Import patterns (relative vs absolute)
- Export patterns (default vs named)
- Error handling patterns
- Logging patterns

### 2. Write Minimal Implementation

Follow **YAGNI** (You Ain't Gonna Need It). Prefer editing existing files over creating new ones.

**Good:**
```typescript
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

**Bad (Over-engineered):**
```typescript
function calculateTotal(
  items: Item[],
  options?: {
    currency?: string;
    discount?: number;
    taxRate?: number;
    roundingMode?: 'up' | 'down' | 'nearest';
  }
): CalculationResult {
  // YAGNI - Was this asked for?
}
```

### Code Clarity

**Prefer explicit, readable code over compact one-liners:**

- Avoid nested ternaries (`a ? b ? c : d : e`) — use `if/else` or `switch`
- Don't sacrifice readability for fewer lines — 3 clear lines beats 1 clever line
- Consolidate related logic, but don't merge unrelated concerns into one function
- Remove comments that describe what the code obviously does — let clear naming speak

### Minimal Diffs Principle

**Only change what's necessary.** When fixing a bug, fix the bug - don't refactor surrounding code. When adding a feature, add the feature - don't "improve" unrelated code. Scope creep in diffs causes merge conflicts, hides the actual change, and makes reviews harder.

### 3. Handle Edge Cases

**Always handle:**
- Empty inputs (`[]`, `null`, `undefined`)
- Invalid inputs (wrong types, out of range)
- Error conditions (network failures, timeouts)
- Boundary conditions (zero, negative, max values)

```typescript
function getUser(id: string): User | null {
  if (!id?.trim()) {
    return null;
  }
  // ... implementation
}
```

### 4. Align With Existing Conventions

| Aspect | Check |
|--------|-------|
| **Naming** | Match existing style (`getUserById` not `fetchUser`) |
| **Imports** | Match import style (`@/lib/` vs `../../lib/`) |
| **Exports** | Match export style (default vs named) |
| **Types** | Match type patterns (interfaces vs types) |
| **Errors** | Match error handling (throw vs return) |
| **Logging** | Match logging patterns (if any) |

## Red Flags - STOP and Reconsider

If you find yourself:

- Writing code before answering Universal Questions
- Adding features not requested ("while I'm here...")
- Ignoring project patterns ("my way is better")
- Not handling edge cases ("happy path only")
- Creating abstractions for one use case
- Adding configuration options not requested
- Writing comments instead of clear code
- Multiple valid approaches exist but not presenting options

**STOP. Go back to Universal Questions.**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "This might be useful later" | YAGNI. Build what's needed now. |
| "My pattern is better" | Match existing patterns. Consistency > preference. |
| "Edge cases are unlikely" | Edge cases cause production bugs. Handle them. |
| "I'll add docs later" | Code should be self-documenting. Write clear code now. |
| "It's just a quick prototype" | Prototypes become production. Write it right. |
| "I know a better way" | The codebase has patterns. Follow them. |

## When to Present Multiple Options

**Present 2-3 approaches with tradeoffs if:**
- Multiple design patterns could work (e.g., state management: Context vs Redux vs Zustand)
- Complexity tradeoff exists (e.g., simple file storage vs database)
- User said "best way" or "how should I" (signals uncertainty)

**Proceed with single approach if:**
- One approach is clearly simpler AND meets requirements
- Project patterns already established (follow existing pattern)
- User request is specific (no ambiguity)

**Use brainstorming skill when presenting options.**

## Code Quality Checklist

Before completing:

- [ ] Universal Questions answered
- [ ] Context-specific questions answered (if applicable)
- [ ] Project patterns studied and matched
- [ ] Minimal implementation (no over-engineering)
- [ ] Edge cases handled
- [ ] Error handling in place
- [ ] Types correct and complete
- [ ] Naming matches project conventions
- [ ] No hardcoded values (use constants)
- [ ] No debugging artifacts (console.log, TODO)
- [ ] No commented-out code

## Output Format

```markdown
## Code Implementation

### Functionality
[What this code does]

### Universal Questions Answered
1. **Functionality**: [answer]
2. **Users**: [answer]
3. **Inputs**: [answer]
4. **Outputs**: [answer]
5. **Edge cases**: [answer]
6. **Existing patterns**: [answer]

### Implementation

```typescript
// Code here
```

### Key Decisions
- [Decision 1 and why]
- [Decision 2 and why]

### Assumptions
- [Assumption 1]
- [Assumption 2]
```

## Common Patterns

### Functions
```typescript
// Clear name, typed parameters and return
function calculateOrderTotal(items: OrderItem[]): Money {
  if (!items.length) {
    return Money.zero();
  }
  return items.reduce(
    (total, item) => total.add(item.price.multiply(item.quantity)),
    Money.zero()
  );
}
```

### Components (React example)
```typescript
interface UserCardProps {
  user: User;
  onSelect?: (user: User) => void;
}

export function UserCard({ user, onSelect }: UserCardProps) {
  if (!user) {
    return null;
  }

  return (
    <div
      className="user-card"
      onClick={() => onSelect?.(user)}
      role="button"
      tabIndex={0}
    >
      <span>{user.name}</span>
    </div>
  );
}
```

### Error Handling
```typescript
// Match project error patterns
async function fetchUser(id: string): Promise<Result<User>> {
  try {
    const response = await api.get(`/users/${id}`);
    return Result.ok(response.data);
  } catch (error) {
    logger.error('Failed to fetch user', { id, error });
    return Result.err(new UserNotFoundError(id));
  }
}
```

## Final Rule

```
Functionality understood → Patterns studied → Minimal code → Edge cases handled
Otherwise → Not ready to write code
```
