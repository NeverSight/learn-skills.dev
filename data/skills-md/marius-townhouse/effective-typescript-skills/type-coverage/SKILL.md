---
name: type-coverage
description: Use when measuring type safety. Use when any types creep in. Use when migrating from JavaScript.
---

# Track Your Type Coverage to Prevent Regressions in Type Safety

## Overview

**Monitor how much of your code is typed vs any.**

Type coverage measures the percentage of symbols with real types vs `any`. Track it over time to prevent type safety regressions.

## When to Use This Skill

- Migrating JavaScript to TypeScript
- Maintaining type quality over time
- Code reviews for type safety
- Measuring progress on any elimination

## The Iron Rule

```
What gets measured gets managed.
Track type coverage; set coverage goals.
```

**Remember:**
- `any` spreads silently through code
- Coverage can regress without notice
- Explicit tracking prevents decay
- Set team goals for coverage improvement

## Understanding Type Coverage

```typescript
let x: number = 1;        // x is covered (has real type)
let y: any = 2;           // y is NOT covered (has any)
let z = JSON.parse('{}'); // z is NOT covered (implicit any from JSON.parse)
```

Type coverage = (covered symbols) / (total symbols)

## Tools for Measuring Coverage

### type-coverage package

```bash
npm install -g type-coverage
type-coverage --detail
```

Output:

```
23384/24058 97.20%
```

With `--detail`, it shows which symbols have `any`:

```
src/api.ts:15:7 - data
src/utils.ts:42:3 - result
```

### Project-Specific Configuration

```json
// package.json
{
  "scripts": {
    "type-coverage": "type-coverage --at-least 95"
  }
}
```

Fail CI if coverage drops below threshold.

## Sources of any

### 1. Explicit any

```typescript
function process(data: any) { ... }  // Developer wrote any
```

### 2. Implicit any (when noImplicitAny is off)

```typescript
function process(data) { ... }  // data is implicitly any
```

### 3. any from Libraries

```typescript
const data = JSON.parse(str);   // Returns any
const result = $.ajax(url);     // jQuery returns any
```

### 4. Contagious any

```typescript
function getUser(): any { ... }
const user = getUser();
//    ^? any - spreads from function

const name = user.name;
//    ^? any - continues spreading
```

## Strategies for Improvement

### Replace JSON.parse

```typescript
// Before: returns any
const data = JSON.parse(str);

// After: validate with zod
const schema = z.object({ name: z.string() });
const data = schema.parse(JSON.parse(str));
//    ^? { name: string }
```

### Fix Library Types

```typescript
// Augment JSON.parse to return unknown
declare global {
  interface JSON {
    parse(text: string): unknown;
  }
}
```

### Use unknown Instead

```typescript
// Before
function parse(): any { ... }

// After
function parse(): unknown { ... }
```

### Add Type Annotations

```typescript
// Before: inferred as any from library
const result = externalLib.process(data);

// After: explicitly typed
const result: ProcessedData = externalLib.process(data);
```

## Tracking Over Time

```bash
# Record in CI
echo "$(date): $(type-coverage)" >> coverage-history.txt

# Fail if coverage decreased
type-coverage --at-least $(cat .type-coverage-baseline)
```

## Setting Team Goals

| Milestone | Coverage Target |
|-----------|-----------------|
| Migration start | 50% |
| Phase 1 | 75% |
| Phase 2 | 90% |
| Stable | 95%+ |

Increase targets as codebase matures.

## Preventing Regressions

### Pre-commit Hook

```bash
# .husky/pre-commit
type-coverage --at-least 95
```

### CI Check

```yaml
# .github/workflows/ci.yml
- name: Type Coverage
  run: npx type-coverage --at-least 95
```

### Code Review Checklist

- [ ] No new `any` types without justification
- [ ] Type coverage didn't decrease
- [ ] External data is validated

## Dealing with Necessary any

Sometimes `any` is unavoidable:

```typescript
// Document why any is needed
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const legacy: any = oldSystem.getData();  // TODO: Type when migrating legacy system
```

Track these with comments and tickets.

## Real-World Example

```typescript
// Before migration: 60% coverage
// Sources of any:
// - JSON.parse: 15%
// - Legacy API: 12%
// - Untyped dependencies: 8%
// - Explicit any: 5%

// Action plan:
// 1. Add zod validation: +10%
// 2. Type legacy API responses: +10%
// 3. Add @types packages: +8%
// 4. Remove explicit any: +5%

// After: 93% coverage
```

## Pressure Resistance Protocol

### 1. "We Can't Achieve 100%"

**Pressure:** "Some code can't be typed"

**Response:** Aim for improvement, not perfection. Track what you can.

**Action:** Set realistic goals; document necessary exceptions.

### 2. "It's Too Much Work"

**Pressure:** "Fixing all any types takes too long"

**Response:** Incremental improvement. Block new any types first.

**Action:** Ratchet: prevent new any, fix old over time.

## Red Flags - STOP and Reconsider

- Coverage decreasing over time
- New `any` types without justification
- `any` spreading from function returns
- Untested code with heavy `any` usage

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's just one any" | any spreads; one becomes many |
| "We'll fix it later" | Later never comes without tracking |
| "Coverage is high enough" | Set higher goals as you improve |

## Quick Reference

```bash
# Measure coverage
npx type-coverage

# With details
npx type-coverage --detail

# Fail if below threshold
npx type-coverage --at-least 95

# In package.json
"scripts": {
  "type-coverage": "type-coverage --at-least 95"
}
```

## The Bottom Line

**Track type coverage to prevent regression.**

any types spread silently. Without measurement, type safety erodes over time. Use tools to track coverage, set goals, and fail builds when coverage drops.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 49: Track Your Type Coverage to Prevent Regressions in Type Safety.
