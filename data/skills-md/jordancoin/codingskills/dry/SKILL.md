---
name: dry
description: When writing or reviewing code to eliminate duplicated knowledge and business logic. Use when the user says "this is duplicated," "we have this in two places," "single source of truth," "DRY this up," or "shotgun surgery." For premature abstraction concerns, see yagni.
metadata:
  version: 1.0.0
---

# DRY — Don't Repeat Yourself

## Before Applying

If `.agents/stack-context.md` exists, read it first. Apply this principle using idiomatic patterns for the detected stack. For framework-specific details, use context7 MCP or web search — don't guess.

## Principle

Every piece of knowledge in a system should have a single, authoritative representation. When that knowledge changes, you should only need to change it in one place.

## Why This Matters in Production

Duplicated logic is a ticking time bomb. When a business rule changes and you update it in one place but miss the copy in another, you get inconsistent behavior that's hard to detect and harder to debug. The more copies exist, the more likely one diverges silently.

DRY is not about eliminating similar-looking code. It's about eliminating duplicated knowledge — the same business rule, the same decision, the same source of truth expressed in multiple places.

## Rules

1. **Distinguish knowledge duplication from code duplication.** Two functions that look identical but represent different business concepts should stay separate. Two functions that encode the same business rule should be unified.
2. **Single source of truth for data.** Configuration, constants, schema definitions, and validation rules should each live in exactly one place. Everything else should derive from that source.
3. **Extract when the pattern is stable.** Don't extract on the first occurrence — you don't yet know the right shape of the abstraction. Extract when you've seen the pattern repeat with the same semantics at least twice.
4. **Centralize business rules.** Tax calculations, permission checks, pricing logic — these must live in one module, not scattered across handlers, frontends, and scripts.
5. **Use code generation over manual sync.** If two representations must stay in sync (e.g., API types and client types, schema and documentation), generate one from the other rather than maintaining both by hand.

## Anti-Patterns

- **Shotgun surgery:** Changing one business rule requires edits in 5+ files because the rule is duplicated everywhere
- **Copy-paste-modify:** Cloning a function and tweaking it instead of parameterizing the original
- **Parallel hierarchies:** Maintaining matching structures in multiple layers (e.g., identical type definitions in backend and frontend that aren't generated from a shared schema)
- **Magic strings repeated across files:** The same status code, error message, or config key hardcoded in multiple locations
- **Documentation that restates the code:** Comments or docs that repeat what the code says (and inevitably drift out of sync)

## The Wrong Kind of DRY

```
-- Code looks similar but represents different concepts — DO NOT unify
def calculate_shipping_cost(weight, distance):
    return weight * 0.5 + distance * 0.1

def calculate_insurance_premium(value, risk_factor):
    return value * 0.5 + risk_factor * 0.1

-- These are different business rules that happen to share a formula today.
-- They will diverge. Keep them separate.
```

## The Right Kind of DRY

```
-- Same validation rule duplicated — UNIFY
// in signup handler
if len(password) < 8 or not has_uppercase(password):
    return error("Password too weak")

// in password-reset handler
if len(new_password) < 8 or not has_uppercase(new_password):
    return error("Password too weak")

-- Fix: single source of truth
def validate_password(password):
    if len(password) < 8:
        return error("Password must be at least 8 characters")
    if not has_uppercase(password):
        return error("Password must contain an uppercase letter")
    return ok()
```

## Boundaries

- **DRY is about knowledge, not syntax.** Two blocks of code that look identical may represent different things. Don't unify them just because they look the same.
- **Premature DRY creates wrong abstractions.** A bad abstraction is worse than duplication because it's harder to undo. Wait until you understand the pattern before extracting.
- **Tension with KISS:** An overly aggressive DRY refactor can create layers of indirection that are harder to follow than the original duplication. If the shared function needs 5 parameters and 3 boolean flags to handle all cases, the duplication was simpler.
- **Tension with YAGNI:** Don't build a generic utility "because we might need it elsewhere." Extract when there are concrete, existing duplicates.
- **Cross-boundary DRY has high cost.** Sharing code between services, repos, or teams creates coupling. Sometimes duplication across boundaries is healthier than a shared library that blocks independent deployment.

## Code Review Checklist

- [ ] Does this change introduce duplicated business logic that already exists elsewhere?
- [ ] Are there magic strings or numbers that should be constants?
- [ ] If this business rule changes, how many files need to be updated?
- [ ] Is there a shared abstraction that's been forced to serve too many masters? (Wrong DRY)
- [ ] Are there manually-synced parallel representations that could be generated?

## Related Skills

- **yagni**: When deciding whether to extract (wait for 3 occurrences)
- **kiss**: When DRY abstraction becomes harder to follow than the duplication
- **convention-over-configuration**: For eliminating repeated configuration patterns
