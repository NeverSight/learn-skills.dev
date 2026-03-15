---
name: refactoring-code
description: Improves code structure while preserving behavior through test verification. Use when cleaning up code, reducing duplication, simplifying complexity, or reorganizing modules.
argument-hint: "<file-path-or-pattern>"
---

# Refactoring Code

**Core principle:** Refactoring changes structure, not functionality. If behavior changes, you're rewriting.

**Target:** If `$ARGUMENTS` is provided, use it as the refactoring target. Otherwise, check for unstaged changes. If none, diff against main: `git diff --name-only $([ "$(git rev-parse --abbrev-ref HEAD)" = "main" ] && echo "HEAD^" || echo "main...HEAD")`

## The Five Phases

```
Refactoring Progress:
- [ ] Phase 1: Understand current behavior
- [ ] Phase 2: Verify behavior-driven tests exist
- [ ] Phase 3: Identify issues
- [ ] Phase 4: Plan incremental steps
- [ ] Phase 5: Execute with continuous verification
```

### Phase 1: Understand Current Behavior

- Read code to understand purpose, not just implementation
- Use Grep to find all call sites and consumers
- Document inputs, outputs, side effects, edge cases

### Phase 2: Verify Test Coverage (CRITICAL)

**Tests must verify BEHAVIOR, not implementation:**

```typescript
// ✅ Behavior-driven - survives refactoring
test('displays error when API returns 404', async () => {
  server.use(http.get('/api/users', () => new HttpResponse(null, { status: 404 })));
  render(<UserList />);
  expect(await screen.findByText(/not found/i)).toBeInTheDocument();
});

// ❌ Implementation-detail - breaks during refactoring
test('sets error state', () => {
  wrapper.instance().handleError(new Error('404'));
  expect(wrapper.state('error')).toBe('404');
});
```

**If tests are missing:** Add behavior-driven tests first using `Skill(ce:writing-tests)`.

### Phase 3: Identify Issues

| Issue | Indicators | Fix |
|-------|------------|-----|
| Complexity | Deep nesting, >50 line functions | Extract smaller functions |
| Duplication | Copy-pasted code | Extract shared utility |
| Poor naming | `x`, `data`, `temp` | Rename to intent |
| Type gaps | `any` types, assertions | Add proper types |

### Phase 4: Plan Refactoring

- Break into small, independently testable steps
- High impact + low risk first (e.g., renames)
- Defer high-risk changes (algorithm rewrites)

### Phase 5: Execute & Verify

1. Make one change at a time
2. Run tests after each change
3. Check TypeScript compilation
4. Verify behavior unchanged

**If something breaks:** STOP. Use `Skill(ce:systematic-debugging)`. Don't proceed until understood.

## Red Flags - STOP and Reassess

- Changing behavior while refactoring (separate concerns)
- Skipping tests ("just this once")
- Adding complexity to remove complexity
- "This is clever!" (clarity > cleverness)
- Abstracting before seeing pattern 3 times

## Quick Reference

| Smell | Refactoring |
|-------|-------------|
| Long function | Extract smaller functions |
| Duplicate code | Extract to shared utility |
| Deep nesting | Early returns, guard clauses |
| Magic numbers | Named constants |
| Large component | Split into smaller components |
| Long parameter list | Parameter object |

## When to Stop

Stop when code is clear, duplication eliminated, types explicit, tests pass.

**Don't continue if:**
- Making code "elegant" but harder to understand
- Abstracting before 3 occurrences
- Optimizing without measuring

For React/TypeScript patterns, see [references/react-typescript.md](references/react-typescript.md).
