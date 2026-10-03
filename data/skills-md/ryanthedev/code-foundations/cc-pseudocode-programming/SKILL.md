---
name: cc-pseudocode-programming
description: "Structures routine design through pseudocode-first iteration: clarifies naming and purpose before any code, catches design flaws cheaply, and prevents compile-debug loops on poorly understood routines. For designing a routine before writing it; not for assessing routines that already exist (use cc-routine-and-class-design)."
user-invocable: false
---

# cc-pseudocode-programming

Design a routine in pseudocode before writing it. Iterating on intent is cheaper than iterating on code, and four questions catch the expensive mistakes early:

| Question | Why |
|---|---|
| Can you name it clearly? | Naming difficulty signals an unclear design — clarify purpose first |
| Is there pseudocode before the code? | Refining pseudocode is cheaper than refining code |
| Do you understand why it works? | Working code you can't explain probably doesn't really work |
| Did you consider an alternative? | The first design is rarely the best |

If the user asks to skip pseudocode, comply or surface the tradeoff once (the routine will likely cost more in debugging) — don't refuse.

Shared CC vocabulary and thresholds (cohesion, parameters, routine length): `Read(${CLAUDE_PLUGIN_ROOT}/references/cc-foundations.md)`.

## When the routine is exempt

Skip the process only when one of these holds:

- **Simple accessor** — `getValue()`/`setName()` with no validation, transformation, or side effects.
- **Pure pass-through** — delegation with no parameter transformation or error wrapping.
- **Trivial one-liner** — all of: single statement, zero decision points, zero loops, implementation obvious from the signature alone.
- **Already designed** — a design document specifies the exact algorithm, error handling, and edge cases.

A routine you're debating as "trivial enough" is not trivial — design it.

## Modes

### APPLIER

Guide routine design with the Pseudocode Programming Process. Produces pseudocode design, header comments, and an implementation plan.

1. Confirm the routine's place in the overall design is clear.
2. Define the problem: inputs, outputs, preconditions, postconditions, what it hides.
3. Name the routine — if naming is hard, the design is unclear; iterate.
4. Plan how you'll test it before writing code.
5. Check libraries for existing functionality before building.
6. Plan error handling — think through failure modes.
7. Research relevant algorithms if needed.
8. Write pseudocode as a header comment in natural language (language-independent, intent not syntax).
9. Iterate until generating code from each line is nearly automatic — you can write each line without pausing to decide *how*. If you stop to think "how do I implement this part?", the pseudocode needs more detail.
10. Try alternatives; keep the best.
11. Code from the pseudocode, which becomes the comments.
12. Compile clean at the strictest warning level.

**"Convinced it's correct"** means you can mentally trace every path — happy, error, edge — and explain why each produces the right output. "It looks right" is not convinced.

#### Good vs bad pseudocode

Pseudocode at the level of intent, no target-language syntax:

```
If another resource is available
    Allocate a dialog box structure
    If a dialog box structure could be allocated
        Note that one more resource is in use
        Initialize the resource
        Store the resource number at the location provided by the caller
        Return success
    Endif
Endif
Return failure
```

This reads as English, becomes excellent comments, and is precise enough to generate code from. The anti-pattern instead writes `*hRsrcPtr`, `malloc()`, `return 1` — target-language detail that focuses on HOW, exposes implementation, and makes poor comments.

### CHECKER

Verify the produced pseudocode and resulting routine. Checklist: `Read(${CLAUDE_SKILL_DIR}/checklists.md)`. Assess the artifacts:

- Is the pseudocode at the level of intent (English, not target-language syntax)?
- Is it detailed enough that code generation from it is nearly automatic?
- Does at least one alternative approach appear to have been weighed?
- Can the routine's correctness be explained by tracing all paths?
- Are all compiler warnings eliminated?

## Evidence

- Programmers preferred pseudocode for construction ease and detecting insufficient detail [Ramsey, Atwood, Van Doren 1983]. Modern IDEs catch syntax faster, which makes design errors — what this process prevents — the dominant problem.
- ~95% of errors are programmer errors, not hardware/compiler/OS [Ostrand and Weyuker 1984].
- Catch errors at the least-value stage; iterating on pseudocode is cheaper than iterating on code [McConnell pp.220, 225].

## Chain

| After | Next |
|---|---|
| Pseudocode complete | `Skill(code-foundations:cc-routine-and-class-design)` |
| Implementation done | `Skill(code-foundations:cc-defensive-programming)` |
