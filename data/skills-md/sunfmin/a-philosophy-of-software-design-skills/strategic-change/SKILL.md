---
name: strategic-change
description: "Modify existing code strategically instead of tactically. After the change, the system should look as if it had been designed with that change in mind from the start (Ousterhout's \"A Philosophy of Software Design\", ch. 3 and 16). Use when adding a feature to or fixing a bug in existing code and the user wants to keep the design clean, says \"don't just patch it\", \"quick fix or proper fix?\", \"what's the right way to add this\", or asks before committing whether a change made the design worse. Not for new modules from scratch (design-it-twice) or reviewing someone else's PR (complexity-review)."
---

# Strategic Change

Working code isn't enough. Each minimal patch adds a special case, a flag, or a dependency, and complexity grows one small change at a time. **If you're not making the design better, you are probably making it worse.**

## Before editing

1. Read the design around the change: the module's interface, its callers, and the conventions in use.
2. Ask: *if this module had been designed from scratch with this change in mind, what would it look like?* Sketch that shape.
3. List where the current structure fights the change. Typical signs: you would need a new flag or boolean parameter, a parameter threaded through layers that don't use it, knowledge duplicated in a second module, or an `if` for one caller.

## Choose the path

- **Ideal:** refactor toward the sketch, then make the change. Default to this when the refactor stays close to the code you're touching. Aim to spend about 10–20% extra effort on it.
- **Nearly as clean:** if the ideal is too costly, look for a variant that gets most of its benefit for a fraction of the work.
- **Tactical, with debt recorded:** only under a real constraint, such as a deadline or a cross-team incompatibility. Name the debt explicitly (a TODO with the reason, or an issue), never silently.

## While editing

- Absorb the change into the normal path instead of adding special cases.
- Pull new complexity down behind the interface rather than exposing it to callers.
- Fix one nearby design imperfection when it's cheap.
- When in Rome, do as the Romans do: follow existing conventions. Change a convention only when both are true: you have significant new information, and it's worth updating every old use. Then leave no trace of the old one.

## After editing — check the diff

- Did the change add a special case, flag, config knob, or pass-through parameter?
- Is any design decision now known in two places?
- Are comments near the change stale? Update them in place.
- Is the "why" (a subtle bug, a workaround) only in the commit message? Put it in the code.
- Is any debugging code or stray TODO left behind?

## Too far

Don't turn a small fix into an unrelated rewrite. Refactor only what the change touches or what directly blocks it, and propose larger cleanups separately.

## Output

Make the change, then report a short design delta:

```
Design: better | same | worse — one line why
Refactored: <what, if anything>
Debt: <recorded shortcuts, or "none">
```
