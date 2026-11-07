---
name: explain-outcome
description: "Use when reporting a failed command, test, build, or deploy, an investigation into an error or incident, or the result of a multi-step task. Structures the report as three parts: what happened, what it means, what's next."
user-invocable: true
argument-hint: <thing to explain>
---

# Explain Outcome

Report the result in three parts, in this order. The goal is only this: a human reads it once and understands.

Write in ASD-STE100 Simplified Technical English. Short sentences are easier to read than long ones. The active voice is easier than the passive. One word for one meaning is easier than a synonym each time. Plain words are easier than jargon.

## Format

```
**What happened**
<the facts: what ran, what it returned, what changed>

**What it means**
<the cause, the effect, and what is not known yet>

**What's next**
<the action the agent will do, or the decision the user must make>
```

Facts go under "What happened". Guesses go under "What it means", marked "likely" or "not confirmed". "What's next" is an action: "I will..." or "You must decide...". If no action is necessary, write "Nothing. Done." For a small result with no decision, reply in one sentence instead.

## Worked example

User: *"Run the tests."*

Good:

```
**What happened**
`make test` failed. 1 of 42 tests failed:

    FAIL: TestOrderTotal_Discount (order_test.go:88)
    expected 90.00, got 100.00

**What it means**
The discount is not in the order total. The likely cause is an early return in `applyDiscount` (order.go:41). This is not confirmed. No other test failed.

**What's next**
- I will read `applyDiscount` to confirm the cause, then fix it.
- You must decide: does a 0% discount call `applyDiscount`, or skip it?
```

Bad — facts and guesses in one sentence, asks instead of states:

> Tests failed because the discount logic is broken in order.go, probably the early return. I can fix it if you want.
