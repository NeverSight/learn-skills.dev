---
name: never-twice
description: Use when you just corrected an agent or fixed the same failure class twice, or when a change removes a rule, guard, or check.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: Vivswan
---

# Never Twice

> Categorically eliminate the problem so the failure class cannot recur, through better architecture or a better choice of data structures. That beats fixing its instances one at a time.

Every correction and every repeated failure gets the most durable response reachable:

| Rung | Response | What the class can still do | Preference |
| --- | --- | --- | --- |
| 1 | better architecture or data structures | cannot recur | the goal |
| 2 | a lint rule or test in CI | recurs, but cannot land | acceptable |
| 3 | a skill or written rule | recurs, but the next agent knows | fallback |
| 4 | human vigilance | anything | avoid |

The ladder is not a menu, and preference decays exponentially down it. Rung 1 is the goal, and rung 2 a clearly weaker but acceptable gate. Rungs 3 and 4 are each another large step down, taken only when every higher rung is genuinely unreachable.

A rung-3 or rung-4 landing is a **debt**, not a resolution. When a higher rung becomes reachable, convert the rule or vigilance entry up the ladder.

## Workflow

1. **Name the class** in one sentence: "any new Event member can ship without a roster entry." If you cannot, it is not a class yet: fix the instance and move on.
2. **Find the substrate** that admits new members: two artifacts synced by convention, a string where a closed set belongs, state kept in prose, a hand-typed ritual.
3. **Climb** as close to rung 1 as the task allows: take the most durable rung you can implement within the task's scope and authority.
4. **Ship it.** A lower-rung fallback ships only with the gap to the more durable rung named in your report. Track that gap as its own task where you have the authority to create one. Never park it as a note: a note is state kept in prose, the substrate that admitted the class.

Test whatever ships:

> If a new member of this class appears tomorrow, does the fix hold, or does it silently pass the same way?

Three answers:

- It **silently passes**: the class is alive.
- It **fails loudly but late** (at runtime, after shipping): an instance guard, the class is still alive.
- It **cannot recur**, at the rung that holds it: impossible to build (1), stopped in CI (2), caught by a loaded rule (3).

## Rung 1: the class cannot recur

An event enum keeps outgrowing the roster that dispatches on it:

```ts
// Fix 1 shipped Event.Deleted's missing entry. Fix 2 shipped
// Event.Archived's, plus a guard. Both read as complete:
handlers[Event.Archived] = onArchived;
assert(Object.keys(handlers).length === EVENT_COUNT); // fires at runtime, after the hole ships
```

```ts
// Rung 1: the roster is total, so the hole cannot be built:
const handlers: Record<Event, Handler> = {
  [Event.Created]: onCreated,
  [Event.Updated]: onUpdated,
  [Event.Deleted]: onDeleted,
  [Event.Archived]: onArchived,
};
// A new member fails compilation until the roster covers it.
```

Type-level mechanics (closed unions, branded types, typestate) live in the `/no-invalid-states` skill.

## Rung 2: recurs, but cannot land

The same cleanup keeps getting committed by hand:

```text
$ git log --oneline -- docs/
9e8f7a6 fix: replace curly quotes with ASCII
a1b2c3d fix: replace curly quotes with ASCII (again)
```

```yaml
# Rung 2: a CI check, marked required in branch protection.
# Fail-closed: hits and grep errors both fail; only "no matches" passes.
- name: check-typography
  run: |
    status=0
    grep -rnP '[\x{2018}-\x{201D}\x{2014}]' docs/ || status=$?
    test "$status" -eq 1
```

## Rung 3: recurs, but the next agent knows

The same correction keeps being given across sessions:

```text
"Timestamps in logs are ISO 8601, not epoch."   (Tuesday)
"ISO 8601 in logs, please."                     (Thursday, new session)
```

```text
# Rung 3: the correction becomes a rule in a file every session loads.
$ tail -1 AGENTS.md
Log timestamps are ISO 8601 (2026-08-26T14:03:00Z), never epoch.
```

How to write the rule (where it lives, its trigger, its quality bar) is the `/craft-skills-and-memories` skill's job. This rung decides THAT a loaded rule is the response, then hands off there.

## Deleting a Guard (Chesterton's Fence)

The ladder erects guards, and this rule governs removing them. Never remove a rule, guard, or check without being able to state why it was erected. Every such deletion in a change maps to one of two outcomes, or nothing lands:

- a successor that covers its class: a script that embodies it, a stronger rung, a rewording that keeps the rule
- a named deliberate cut, with the reason recorded in the change

Worked example: a doc rewrite deleted 90 long-standing rule lines. Auditing each line into successor / rewording / named cut found exactly one unmapped real loss, restored before landing.

The audit is the mechanism. This rule makes it the default for every deletion, not a salvage step after someone notices.

The pairing is the point: aggressive rewrites stay allowed BECAUSE deletions are audited. The audit is what makes bold deletion safe, not a brake on it.

## Review Criteria

Skills that run code reviews (such as `/rubber-duck-review`) expand this section into their reviewer prompt when this skill is installed. Ask the reviewer to flag:

- fixes that repeat an earlier fix of the same failure class. Cite the evidence (the prior commit, doc line, or correction), not a hunch
- for each, name the rung the fix sits on, propose a concrete more durable rung, and say why it is reachable within this change's scope (or why it is not)
- apply the test to whatever ships: if a new member of the class appears tomorrow, is it impossible to build, stopped in CI, caught by a loaded rule, or silent?
- deletions of rules, guards, or checks that map to neither a successor covering their class nor a deliberate cut with its reason recorded in the change (Deleting a Guard, above)

Triage the resulting findings with the workflow above.
