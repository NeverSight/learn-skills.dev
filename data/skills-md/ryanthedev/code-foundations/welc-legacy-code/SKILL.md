---
name: welc-legacy-code
description: "Safely modifies untested legacy code by getting it under test first: characterization tests, seam identification, sprout/wrap techniques, and pinch-point testing before any production changes. Not for refactoring code that already has test coverage (use cc-refactoring-guidance)."
user-invocable: false
---

# Working Effectively with Legacy Code

> "Legacy code is simply code without tests." - Michael Feathers

Get code under test before changing it. This is the core principle.

## Quick Reference

| Symptom | Solution |
|---------|----------|
| Can't get class into test harness | Decision Tree: Can't Instantiate |
| Can't run method in test harness | Decision Tree: Can't Call Method |
| Don't know what tests to write | Characterization Tests |
| Under time pressure, need to change now | Sprout/Wrap Techniques |
| Need to change many classes in one area | Pinch Point Testing |
| Class is too big / monster method | Effect Sketching → find clusters |
| Afraid I'll break something | Single-Goal Editing, Preserve Signatures |

---

## The Legacy Code Change Algorithm

**Use this for every change to untested code.**

```
1. IDENTIFY change points
   - Where in the code do you need to make modifications?

2. FIND test points
   - Where can you write tests to cover the change?
   - Look for pinch points where tests cover multiple changes

3. BREAK dependencies
   - Remove obstacles that prevent testing
   - Use dependency-breaking techniques (catalog below)

4. WRITE characterization tests
   - Document what the code DOES, not what it SHOULD do
   - Process: write assertion you know will fail → let failure
     tell you actual behavior → change test to match

5. MAKE changes and refactor
   - Implement the change with test safety net
```

---

## Sprout/Wrap Techniques (Time Pressure)

When you can't test everything but need to change code now:

- **Sprout Method:** Write new code in a new method, call from existing code. New code is separately testable.
- **Sprout Class:** Create new class for new functionality when original is untestable.
- **Wrap Method:** Add behavior before/after existing method. Original code untouched.
- **Wrap Class:** Decorator pattern — wrap existing class with new behavior layer.

These keep new code separate and testable even when old code isn't.

---

## Characterization Tests

When you don't know what tests to write:

1. Write assertion you know will fail
2. Let the failure message tell you what the code actually does
3. Change test to expect actual behavior
4. Repeat for each code path you need to cover

You're documenting what the code **does**, not what it **should** do. This is the test safety net for refactoring.

---

## Effect Sketching and Pinch Points

When you need to change many classes in one area:

1. **Effect Sketch:** From each change point, trace effects outward — what does this affect? Follow return values, modified parameters, modified fields, global/static data.
2. **Find Pinch Points:** Where do effects from multiple change points funnel together? Write tests there first.
3. **Pinch point tests are scaffolding** — delete them when you have proper unit tests. They exist to give you a safety net while breaking things apart.

---

## Dependency-Breaking Catalog

| Technique | When to Use |
|-----------|-------------|
| Adapt Parameter | Parameter class hard to fake |
| Break Out Method Object | Long method with local state |
| Encapsulate Global References | Global variables block testing |
| Expose Static Method | Method uses no instance state |
| Extract and Override Call | Single problematic call |
| Extract and Override Factory Method | Constructor creates dependencies |
| Extract and Override Getter | Instance variable holds problem |
| Extract Implementer | Turn class into interface |
| Extract Interface | Need to fake a class |
| Introduce Instance Delegator | Static method blocks testing |
| Introduce Static Setter | Singleton blocks testing |
| Parameterize Constructor | Constructor creates its dependencies |
| Parameterize Method | Method obtains dependency internally |
| Primitivize Parameter | Parameter hard to create, only data needed |
| Pull Up Feature | Test feature in isolation |
| Push Down Dependency | Separate testable logic from dependencies |
| Replace Global Reference with Getter | Global variable access |
| Subclass and Override Method | Method behavior blocks testing |
| Supersede Instance Variable | Replace after construction |

---

## Decision Trees

### Can't Instantiate Class?

```
Is the problem in the constructor?
├── YES: Does constructor CREATE objects?
│   ├── YES: Parameterize Constructor or Extract and Override Factory Method
│   └── NO: Does constructor USE passed objects?
│       ├── YES: Extract Interface on parameter, pass fake
│       └── NO: Hidden dependency — find the `new` and externalize it
└── NO: Is it a singleton/global?
    ├── YES: Introduce Static Setter
    └── NO: Include/import dependency chain
        └── Extract Interface or Extract Implementer
```

### Can't Call Method?

```
Is the method private?
├── YES: Make protected, create testing subclass
└── NO: Is a parameter hard to create?
    ├── YES: Is parameter sealed/final?
    │   ├── YES: Adapt Parameter
    │   └── NO: Extract Interface from parameter
    └── NO: Does method have invisible side effects?
        └── YES: Extract side effects to separate methods, override in test
```

### Under Time Pressure?

```
Can you test the new code in isolation?
├── YES: Sprout Method or Sprout Class
└── NO: Does new behavior go before/after existing?
    ├── YES: Wrap Method
    └── NO: Can you not modify the class at all?
        └── YES: Wrap Class (Decorator)
```

---

## Key Principles

1. **Tests first, then change.** The Legacy Code Change Algorithm is non-negotiable.
2. **Break dependencies minimally.** Just enough to get tests in place.
3. **Preserve behavior.** Characterization tests document what IS, not what SHOULD BE.
4. **Small steps.** Each refactoring should be verifiable.
5. **Seams enable testing.** A seam is a place where you can alter behavior without editing in that place. Prefer object seams (override via inheritance/interfaces).

---

## Chain

| After | Next |
|-------|------|
| Code under test | `Skill(code-foundations:cc-refactoring-guidance)` (safe refactoring process) |
| Dependencies broken | Continue with Legacy Code Change Algorithm step 4-5 |
