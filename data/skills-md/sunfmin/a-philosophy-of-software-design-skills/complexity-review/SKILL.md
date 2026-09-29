---
name: complexity-review
description: "Review a diff, PR, module, or design for unnecessary complexity using the red flags from John Ousterhout's \"A Philosophy of Software Design\" (shallow modules, information leakage, pass-through methods, special-general mixture, vague names, and more). Use when the user asks whether a design is too complex, why code is hard to change (every small change touches many files, too much to keep in your head, unclear what to modify), asks for a design review of existing code, or says \"APOSD review\". Not for spec or style-guide compliance (code-review) or local cleanup (simplify)."
---

# Complexity Review

Complexity = anything in the structure that makes the system hard to understand or modify.
Judge every finding by what it costs the **reader**, not the writer.

- **Symptoms** — *change amplification* (one change, many edits), *cognitive load* (too much to know), *unknown unknowns* (can't tell what must change — the worst).
- **Causes** — *dependencies* (code can't be understood or changed in isolation) and *obscurity* (important info isn't obvious).

## Process

1. Scope: the diff (`git diff <base>...HEAD`) plus the interfaces it touches. Read callers, not only the changed lines.
2. Scan for every red flag below. For each hit, write down a concrete location and cost.
3. Check each hit against **Too far** before reporting it. Drop the ones that fail.
4. Report, most expensive first.

## Red flags

| Flag | Signal |
|---|---|
| Shallow module | Interface nearly as complex as the implementation; one-line wrappers; classitis. |
| Information leakage | One design decision (format, protocol, ordering) is known by 2+ modules, even if nothing in their interfaces shows it. |
| Temporal decomposition | Modules split by execution order (read → parse → write) and share knowledge. |
| Overexposure | Common use forces callers to learn rare features; missing defaults. |
| Single-use method | Designed for exactly one caller or situation (`backspace()` on a text class). |
| Caller glue | Using the module for today's need takes lots of extra caller code: the interface lacks the right functionality. |
| Pass-through method | Forwards arguments to a method with a near-identical signature. |
| Pass-through variable | A parameter threaded through layers that never use it. |
| Global state | Globals, or a context object used as a grab-bag, create hidden dependencies (no second instance, hard to test). |
| Same abstraction in adjacent layers | Layers or decorators add boilerplate but no new abstraction. |
| Repetition | The same nontrivial snippet appears in several places. |
| Special-general mixture | General mechanism contains code for one specific use. |
| Special cases | `if` checks for edge cases the normal path could absorb (e.g. an empty selection instead of "no selection"). |
| Conjoined methods | You can't understand one without reading the other. |
| Config punt | Exposed knob the module could compute or default itself. |
| Exposed internals | Getters/setters or returned internal collections leak representation; `private` is not information hiding. |
| Implementation inheritance | Parent and subclasses share state, so changing one requires reading the whole hierarchy. Prefer composition. |
| Exception sprawl | Many throw or `err` sites or handlers. Hand off to `define-errors-out`. |
| Comment repeats code | Comment could be written from the adjacent line alone. |
| Impl contaminates interface | Interface comment describes internals. |
| Vague / hard-to-pick name | `count`, `status`, `result`, `data`; or no short precise name exists. |
| One name, two meanings | Same name for different things (`block` = file block or disk block). Use distinct names or types. |
| Hard to describe | Full interface comment would be long. The design is suspect. |
| Nonobvious code | First guess about behavior is wrong: event handlers with no "when called" comment, `Pair`, declared type ≠ allocated type, surprising side effects (e.g. threads outliving `main`). |

## Too far (don't flag)

- Hiding information callers genuinely need (durability rules, errors they must react to).
- Merging unrelated code just to make it deeper.
- A dispatcher, or several implementations of one interface. Same signatures are fine when each adds real function.
- Splitting a long method that reads fine in blocks. Depth beats length.
- Forcing a convention onto things that are actually different.

## Fix directions

Merge or redistribute leaky modules. Pull complexity down behind the interface. Make interfaces somewhat general-purpose and push specialization up or down. Use a context object for pass-through variables. Define special cases out of existence. Choose precise names.

## Output

One entry per finding, most costly first:

```
[flag] path:line — what's wrong
  cost: <symptom> via <dependency|obscurity> — concrete consequence
  fix: smallest change that removes the flag
```

End with a one-line verdict: is the change making the design better or worse? If it isn't improving the design, it is probably making it worse.
