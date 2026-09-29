---
name: design-it-twice
description: "Before implementing a new module, package, class, API, or CLI, sketch two or three radically different interface designs, compare them, and pick or synthesize the best (Ousterhout's \"design it twice\"). Use when the user is about to write a new module or package from scratch and wants help designing its interface first, asks what an API should look like, wants alternatives before coding, or says \"design it twice\". Not for reviewing or refactoring existing code or choosing a library."
---

# Design It Twice

Your first idea is rarely the best one. Settle the interface before you write any implementation.

## Process

1. **State the need.** Write down what callers must do in the common case, as 2–4 concrete call sites.
2. **Sketch 2–3 radically different interfaces.** Signatures plus a one-line comment each. No bodies. If only one design seems reasonable, still sketch a deliberately different one: its weaknesses teach you something. For large designs, run one sub-agent per alternative in parallel.
3. **Write the common-case call sites for each alternative.** The design that makes callers write extra glue loses.
4. **Compare**, most important criterion first:
   - Ease of use for the common case (higher-level code stays simple)
   - Interface simplicity (fewer methods and concepts, same power)
   - Depth (how much it hides)
   - Generality: *somewhat* general-purpose, meaning the functionality serves today's needs but the interface isn't tied to them
   - Whether it allows an efficient implementation
5. **Synthesize.** The winner is often a hybrid. If every option is awkward, turn the shared awkwardness into a requirement and design again. (Line-based and char-based text APIs both force callers to do text manipulation, which leads to a range-based API.)
6. Repeat for the implementation when it's non-trivial. For implementations, weigh simplicity and performance.

## Useful questions

- What is the simplest interface that covers all current needs?
- In how many situations will each method be used? A method used in one place only is a red flag.
- Is it easy to use for today's needs without piles of caller code?

## Output

```
Alternatives:
  A — <name>: signatures, common-case call site, pros/cons
  B — ...
  C — ...
Decision: <chosen or hybrid> — why, in 2–3 lines
Interface: final signatures + interface comments (see comments-first)
```

Then stop, or implement if the user asked. Units of development are abstractions, not features: design the whole core interface now instead of growing it one test at a time. TDD is still fine inside the chosen abstraction, and write a failing test first when fixing a bug.
