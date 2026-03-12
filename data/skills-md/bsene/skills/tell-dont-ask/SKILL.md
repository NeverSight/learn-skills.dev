---
name: tell-dont-ask
description: >
  Apply the Tell Don't Ask (TDA) principle when reviewing, writing, or refactoring
  object-oriented code. Use this skill whenever the user asks about OOP design,
  mentions getters/setters, wants to review a class for encapsulation issues, asks
  how to move logic closer to data, or asks why code feels "procedural" despite
  using classes. Also trigger when the user asks to refactor code that queries an
  object's state before making decisions externally. This skill should kick in for
  any code review or design question involving data access patterns, encapsulation,
  or how objects should collaborate.
---

# Tell Don't Ask

## Core Principle

**Tell Don't Ask** (TDA) means: instead of *asking* an object for its data and then acting on it externally, *tell* the object what to do and let it use its own data internally.

This flows directly from OOP's core idea — bundle data with the behavior that operates on it. Tightly coupled data and behavior belong in the same component.

---

## Identifying "Ask" Style (The Problem)

Watch for this pattern: external code **queries** an object's state and then **makes decisions** based on that state.

```ts
if (order.status === "pending" && order.total > 1000) {
    order.approvalQueue.push(order.id);
    order.status = "awaiting_approval";
}
```

Red flags:
- Chains of getters used to make a decision
- `if (obj.getX() > obj.getLimit())` patterns outside the class
- External code setting state after reading state (`get` then `set`)
- Logic that "belongs" to an object scattered across callers

---

## Applying the Refactor

Move the decision-making logic **into the object** that owns the data.

```ts
order.submitForApproval();
```

```ts
class Order {
  submitForApproval(): void {
    if (this.status === "pending" && this.total > 1000) {
      this.approvalQueue.push(this.id);
      this.status = "awaiting_approval";
    }
  }
}
```

The caller **tells** the object what to do; the object **decides** how.

---

## Step-by-Step Refactoring Guide

1. **Find the ask chain** — locate external code that reads object data to make a decision.
2. **Identify which object owns the data** — the class whose fields are being read.
3. **Name the intent** — what is the caller *trying to accomplish*? Name a method for that intent (e.g., `submitForApproval`, `checkAlarm`, `applyDiscount`).
4. **Move the logic in** — cut the conditional/action block and paste it into the new method on the owning class.
5. **Replace the call site** — swap the ask chain with a single tell call.
6. **Remove now-unnecessary getters** if nothing else uses them (be cautious — see nuance below).

---

## Nuance: When Getters Are Fine

Martin Fowler himself notes he doesn't strictly follow TDA. Query methods are legitimate when:

- An object **transforms** data for its caller (e.g., formatting, aggregation)
- The object is a **value object** or DTO whose purpose is to carry data
- You're crossing **architectural layers** (e.g., persistence, serialization)
- Removing a getter would create **convolutions** worse than the query

The goal is **co-locating behavior with data**, not eliminating all accessors. Don't become a "getter eradicator" — use judgment.

---

## Quick Reference Examples

| Ask (avoid) | Tell (prefer) |
|---|---|
| `if (a.value > a.limit) a.alarm.warn(...)` | `a.setValue(newVal)` — alarm logic inside `setValue` |
| `if (cart.items.length === 0) showEmpty()` | `if (cart.isEmpty()) showEmpty()` — at minimum, encapsulate the check |
| `order.status = order.computeNextStatus()` | `order.advance()` |

---

## When Reviewing Code

For each class under review:
1. List all getters — are any used only to make external decisions about the object?
2. Find conditional blocks that read from a single object's fields — can they move in?
3. Look for setter chains (`setA`, `setB`, `setC` in sequence) — could that be one `configure(...)` or `initialize(...)` call?

Flag violations clearly, suggest the encapsulated alternative, but note if the refactor would be overkill (e.g., trivial DTOs, framework-required accessors).
