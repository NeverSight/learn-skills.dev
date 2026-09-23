---
name: uncomplect
description: Pressure-test a stateful system or replacement design through Rich Hickey's simplicity and complection, Greg Young's deletability, Ousterhout's deep modules, DDD boundaries, typed effects, and explicit lifecycle modeling. Use when the user asks "what would Rich Hickey do", "optimize for deletion", "make this simpler", "define this error out of existence", "review this state machine", "design it twice", or wants to replace a working prototype without preserving its accidental architecture.
basis:
  - https://github.com/matthiasn/talk-transcripts/blob/master/Hickey_Rich/SimpleMadeEasy-mostly-text.md
  - https://www.youtube.com/watch?v=1FPsJ-if2RU
  - https://web.stanford.edu/~ouster/cgi-bin/book.php
  - https://www.domainlanguage.com/ddd/reference/
  - https://effect.website/docs/
  - https://stately.ai/docs/
---

# Uncomplect

Treat the current system as a functional prototype. Preserve proven behavior and evidence. Do not preserve accidental structure.

## Read first

Read the nearest project instructions, decisions, source, tests, runtime receipts, and current incidents before proposing a replacement.

For state-machine code, inspect the machine, persisted state, restoration path, invoked actors, guards, and transition tests.

For effect-system code, inspect the project's pinned version and existing service, error, retry, and transaction boundaries. Do not prescribe APIs from memory.

Completion: every recommendation names its source fact, preserved behavior, and deleted complexity.

## Hickey: separate what was braided

Build a complection table.

| Concern | What is braided together? | Independent values | Separation move |
| --- | --- | --- | --- |

Look for:

- value mixed with time;
- identity mixed with changing state;
- behavior mixed with storage or transport;
- policy mixed with mechanism;
- current truth mixed with historical facts;
- lifecycle state mixed with domain data;
- retry policy mixed with business failure;
- one generic status hiding distinct facts.

Prefer immutable values and pure functions. Keep historical facts true without granting them permanent authority.

## Ousterhout: make the interface deep

Judge complexity by change amplification, cognitive load, and unknown unknowns.

For every proposed type, state, service, interface, or configuration value, ask:

1. What complexity does this element remove?
2. Does it hide a hard problem behind a small interface?
3. Can the API define an accidental error or special case out of existence?
4. Does it pull complexity into one deep module, or spread policy across callers?
5. What can we delete after adding it?

Reject infrastructure that adds names without removing more dependencies or obscurity.

For consequential replacements, design it twice. Sketch two materially different interfaces. Compare caller burden, hidden knowledge, dependencies, failure semantics, and deletion count before choosing.

## Young: optimize for deletion

Greg Young's [The Art of Destroying Software](https://www.youtube.com/watch?v=1FPsJ-if2RU) argues for small programs that can be replaced when their model stops fitting reality.

Ask:

1. Could this module be rewritten from its contracts, tests, and receipts within about one week?
2. If not, which dependency, hidden invariant, or shared state makes it dangerous to replace?
3. Can a new implementation shadow the old one behind the same seam?
4. Does the proposed boundary preserve proven behavior without preserving the current model?
5. What old implementation becomes deletable after cutover?

The one-week horizon is a pressure test, not doctrine. Do not turn it into arbitrary service splitting. Small replaceable programs can live in one process and one repository.

## DDD: put authority in the right boundary

Name the bounded contexts and their trust boundaries. Use domain language, not storage language.

Identify:

- the aggregate that owns each invariant;
- immutable facts versus current decisions;
- commands, events, policies, and projections;
- upstream and downstream contract ownership;
- translation at context boundaries;
- terms that hide several domain meanings.

A projection may report domain truth. It must not become authority over the aggregate that produced it.

Model a workflow as a command plus current facts producing explicit events. The pure workflow returns events. Publishing and persistence are separate effects.

## Typed effects: keep the pure core pure

Use the project's effect system for effects, not for making pure rules look sophisticated.

- Keep domain decisions as pure functions and tagged values.
- Decode untrusted input at boundaries.
- Put database, network, filesystem, clock, configuration, and provider work behind named services.
- Use typed expected errors. Keep defects distinct.
- Retry only typed transient failures with proven idempotency.
- Keep provider calls outside authoritative database transactions.
- Do not introduce an incompatible effect-system version inside one workflow.

If the project does not already use a compatible effect system at this boundary, plain language-native code is better than a framework migration disguised as a simplification.

## Lifecycle: make essential time visible

Use an explicit state machine when modes have different allowed events, cancellation, retries, resumability, or child work. Do not use one for pure migration, parsing, or validation.

- States represent modes with different allowed events.
- Context holds minimal actor data, not duplicate state labels.
- Guards are pure and synchronous.
- Effects live in invoked actors or boundary services.
- Persisted state must be normalized before it receives current authority.
- A transient computation does not need a new durable state.
- Restoration tests must cross version and deployment boundaries.

Prefer a smaller machine fed by validated domain values over a machine that interprets raw database rows.

## Replacement pass

Produce this sequence:

1. **Essential behavior**: what the prototype proves and must preserve.
2. **Complection map**: what is braided today.
3. **Domain map**: contexts, aggregate, invariants, commands, events, projections.
4. **Deep seam**: the smallest public operation that can hide unavoidable complexity.
5. **Effect boundary**: pure core, typed failures, effectful adapters, transaction edge, retry owner.
6. **Lifecycle**: the smallest state machine that still makes time explicit.
7. **Rewrite horizon**: what prevents this module from being replaced within about one week.
8. **Deletion list**: states, flags, exceptions, operator steps, and modules the replacement removes.
9. **Adoption path**: tracer, shadow comparison, cutover, and rollback without dual authority.
10. **Unknowns ledger**: known facts, known unknowns, unknown knowns, suspected unknown unknowns.

Use this sequence as a reasoning checklist, not a demand for ten headings. Combine adjacent items when one table or type definition carries the evidence. Keep the review proportional to the decision risk.

## Output

Lead with one verdict:

```text
More complicated locally, simpler overall
```

or:

```text
More machinery, no net simplification
```

Then include:

- source-grounded complection table;
- proposed domain language;
- one deep interface;
- pure decision types;
- effect and lifecycle ownership split;
- old versus proposed state count;
- rewrite horizon;
- deletion list;
- risks and one material question.

Do not praise the design. Show what becomes impossible, what becomes obvious, and what disappears.

## Compact invocation

```text
Treat the current system as a functional prototype, not an architecture to preserve. Preserve its proven behavior. Find what is complected. Separate values from time, policy from mechanism, and facts from projections. Define accidental errors out of existence. Draw the domain boundaries and aggregate invariants. Keep effects at effectful boundaries and state machines on essential lifecycle. Optimize the seam for deletion instead of predicting future change. Propose the smallest deep replacement, show what it deletes, and name the remaining unknowns.
```

For the source map and the distinct job each lens performs, read [references/source-map.md](references/source-map.md).
