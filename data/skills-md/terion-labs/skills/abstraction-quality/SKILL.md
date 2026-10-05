---
name: abstraction-quality
description: Use when deciding whether to extract a function, introduce an interface, create a new class, add a helper, split a module, add a plugin hook, or generalize a piece of code; when reviewing a pull request that proposes a new abstraction; when a shared helper is growing flag parameters; when you have duplication and are unsure whether to extract it; or when an existing abstraction feels wrong but you cannot name why. Also trigger when the user asks "should I extract this?", "is this the right abstraction?", "is this over-engineered?", "is this DRY enough?", "should I generalize this?", "should I add an interface here?", or "is this premature abstraction?". This skill provides a decision procedure; it is referenced by writing-good-code and refactoring-and-reviewing-code, and can also be used on its own.
---

# Abstraction quality

Decide whether a proposed or existing abstraction — function, class, interface, module, generic, plugin hook — is worth having. Bad abstractions calcify. The cost of a wrong abstraction exceeds the cost of the duplication it replaces. This skill is a decision procedure, not philosophy.

## First principles

An abstraction is worth having only if it **hides substantially more complexity than its interface exposes**. Ousterhout calls this *depth*. A shallow abstraction — where interface surface and implementation size are close — pays interface cost without delivering benefit.

Abstractions fail in two classic ways. Guard against both:

- **Leaky** (Joel Spolsky): the abstraction claims to hide a lower layer, but the layer breaks through at the margins — performance, error modes, semantics. All non-trivial abstractions leak to some degree; the sin is pretending they do not. Document the leaks.
- **Wrong** (Sandi Metz): the abstraction was extracted from apparent duplication that was actually coincidence. Over time, flags and conditionals accumulate as callers diverge. The fix is to **go back**: inline, delete per-caller dead branches, re-derive.

## Decision procedure — "Should I extract this abstraction?"

Run in order. A single **no** means do not extract yet.

1. **Is the concept nameable in the domain?** Can you name it with a precise noun or verb from the problem domain, *without* `Manager`, `Helper`, `Handler`, `Processor`, `Util`, `Wrapper`, `Base`, `Abstract*`, `*Impl`, `Info`, `Data`? If not, the concept is not real yet.
2. **Are there at least three call sites** that would all need the same change if the underlying concept changed (Rule of Three)? Two sites are usually coincidence. One is certainly too early.
3. **Do the call sites truly share behavior?** If extracting requires new parameters or flags at each site to match each caller's needs, the sites are not the same concept. Stop.
4. **Is the interface smaller than the implementation?** Count public parameters + method signatures; count non-trivial implementation lines. If the ratio is close to 1, you are about to create a shallow module. Redesign or keep duplication.
5. **Would inlining this abstraction produce clearly worse code?** If inline looks equal or better, prefer inline.
6. **Is the underlying domain stable?** If you are still learning the problem, duplicate. The right abstraction becomes visible only after you have seen the variations.

If all six pass, extract. If any fail, **duplicate instead** and tag with a one-line comment noting where the duplication lives, so you can revisit.

## Decision procedure — "Is this existing abstraction good?"

Score each. Two or more failures → refactor candidate.

- **Depth.** Interface substantially smaller than implementation.
- **Cohesion.** One-sentence description without "and". If you need "it does X *and* Y", the module is two things wearing a trench coat.
- **Honest leaks.** Where it leaks (timing, error semantics, resource ownership), the leak is documented and predictable.
- **Loud failure.** When it breaks, callers get a typed error or a crash, not a plausible wrong answer.
- **Stable signature.** Changes to implementation rarely force signature changes. If every new requirement adds a parameter, the abstraction is misaligned with the real axis of variation.
- **No flag parameters.** Boolean flags that switch behavior are evidence of two concepts fused into one. `do(x, shouldValidate=true, exceptIfDraft=false)` is the Wrong Abstraction in progress.
- **Stable conditional count.** Count `if`s keyed on parameters inside the abstraction. Growing over time ⇒ Metz decay.
- **Reversible.** You could inline it back without structural loss. An abstraction that cannot be inlined is either genuinely deep or badly entangled — inspect further.

## The cost of a wrong abstraction, and how to escape it

The failure mode (Metz):

1. A sees duplication, extracts a shared helper, replaces callers.
2. A new requirement is *almost* like the helper. B, feeling honor-bound, adds a parameter and a conditional.
3. Time passes. C, D, E each add flags. The helper now does several unrelated things, interleaved.

**Escape:**

- Inline the helper back into each call site.
- In each call site, set flag parameters to that caller's actual values and **delete the unreachable branches**.
- You now have concrete, possibly repetitive code at each site. Read them side by side. The true axes of variation are often different from what you originally extracted — or there are none.
- Re-extract only what passes the six-point procedure above.

The fastest way forward is back.

## Against speculative generality

Do not build hooks for imagined future needs.

- **No "we might need another provider someday."** Until the second provider exists, a factory hides nothing and adds surface area. When the real second provider arrives, you will know its shape; guessing now is almost certainly wrong.
- **No `IFoo` per `Foo`.** Create an interface only when ≥2 real implementations exist, or when you have a concrete seam the tests need that a simpler mechanism cannot provide.
- **No configuration for things that never vary.** Hard-code until variation becomes real.
- **No generics you cannot fill with three concrete type instantiations.** Generics express real polymorphism, not expected flexibility.

Fowler's cost ledger for unneeded generality: cost to build (wasted if unused), cost of delay (displaced a real feature), cost of carry (every reader must understand it), cost of repair (rip out when the guess turns out wrong). Four costs against a benefit that may never arrive.

## Against naming-as-concealment

`Util`, `Helper`, `Manager`, `Handler`, `Processor`, `Wrapper`, `Common`, `Base`, `Abstract*`, `*Impl` are not concepts. They are confessions that the author could not find a name. Sometimes these names are appropriate because they are genuinely domain-accepted (e.g., `HttpHandler` in a web framework, `EventHandler` in a UI toolkit). Test: does the word appear in the user's domain vocabulary, or only in your code? If only in your code, it is an unhooked bag.

## Locality vs DRY

Locality of Behavior (Carson Gross) and DRY (Hunt & Thomas) are in tension. DRY says "knowledge should have one representation." Locality says "code you need to understand a unit should be near that unit." When they conflict:

- **DRY wins for true knowledge duplication** — a business rule, a schema, an invariant. Change it in one place, safely.
- **Locality wins for coincidental duplication** — two functions that happen to have similar shapes but model different things — and for glue code (event bindings, markup, styles) where following a cross-file pointer hurts comprehension more than the duplication does.
- If unsure whether duplication is "true" or "coincidental," treat it as coincidental until evidence says otherwise. That defaults you to the Rule of Three plus the name test.

Note: DRY in Hunt & Thomas's original formulation is about *knowledge*, not text. Two functions with identical bodies that represent different business rules are not a DRY violation — they are a naming opportunity. Remember: different things should look different.

## See also

- `references/decision-trees.md` — flowcharts for extract / keep / inline decisions, with each branch labeled.
- `references/good-vs-bad-abstractions.md` — paired TypeScript examples with commentary.
