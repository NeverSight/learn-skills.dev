---
name: cc-routine-and-class-design
description: "Applies Code Complete's routine and class design rules at the routine level: cohesion classification, parameter-count thresholds, LSP inheritance verification, and containment-vs-inheritance decision. For routine and class scope, not system architecture (use ca-architecture-boundaries)."
user-invocable: false
---

# cc-routine-and-class-design

Three checks catch design problems that can't be patched post-hoc (they require architectural change, not a fix):

| Check | What |
|---|---|
| LSP test | Is "A is a B" literally true? If not, the inheritance is wrong |
| Containment default | If LSP feels like purity theater, use containment — it's fixable; inheritance isn't |
| Parameter count | Over 7 parameters predicts interface errors — the interface is wrong |

A passing test suite does not clear these: code can pass all tests on day 1 and still carry VIOLATION-level design debt that surfaces during later modification.

Shared thresholds (parameters 7±2, inheritance depth, routine length, cohesion spectrum): `Read(${CLAUDE_PLUGIN_ROOT}/references/cc-foundations.md)`.

## When NOT to apply

- One-off scripts and automation.
- Prototyping (time-boxed before committing to a design).
- Pure DTOs without behavior (but DTOs with validation/equals/toString are NOT exempt).
- Framework-mandated inheritance (e.g. Android `Activity`) — but "framework examples use inheritance" is not a mandate.
- Profiled performance-critical inner loops (show the data).
- Test doubles — empty overrides and minimal abstractions are appropriate in test code.

## Modes

### CHECKER

Execute the design checklists against routines and classes: `Read(${CLAUDE_SKILL_DIR}/checklists.md)`. Output one row per item: `| Item | Status | Evidence | Location |`.

| Severity | Criteria |
|---|---|
| VIOLATION | Fails a checklist item (e.g. 10+ params); breaks LSP/encapsulation (empty override, protected base data) |
| WARNING | Near a limit needing justification (8–9 params, 3-level inheritance); a subjective abstraction concern |
| PASS | Meets or exceeds the requirement |

### APPLIER

Produce class interface designs, inheritance/containment decisions, routine signatures, and cohesion classifications.

- Default to containment; inherit only if "is-a" is literally true (LSP) [p.133].
- Inheritance depth: target <3, WARNING at 3, VIOLATION at 4+, SEVERE at 6+ [p.143].
- Parameters: 7 maximum, graduated per the table below [p.178].
- Target functional cohesion [p.168].
- Ask "What should this class hide?" to drive the design [p.139].

### Parameter thresholds

| Count | Status | Action |
|---|---|---|
| 1–5 | PASS | None |
| 6–7 | PASS | Minor concern; document if unusual |
| 8–9 | WARNING | Justify in review or redesign |
| 10+ | VIOLATION | Redesign — parameter object or split responsibilities |

Count all parameters including defaulted ones; variadic (`*args`/`...`) counts as 1. Ordering convention (order implies data flow): input-only first, input-output second, output-only third.

## LSP

If A inherits from B, every place that uses B can substitute A without breaking. Inheritance requires both:

1. **Semantic**: "A is a B" makes sense to a domain expert (Dog is an Animal — yes; UserSession is a Logger — no).
2. **LSP**: every method of B works when A is substituted — no empty overrides, no new exceptions the base doesn't throw, no strengthened preconditions.

If either fails, use containment.

## Inheritance vs containment decision

- Shares only data → contain a common object.
- Shares only behavior (method signatures) → use an interface/protocol, not inheritance.
- Shares both data and behavior → inherit only if "A is a B" is literally true (LSP); otherwise contain.

**FINAL CHECK** (after deciding INHERIT, before committing): depth < 3 (definitely < 6)? No empty overrides needed? All base data private (not protected)? If any answer is NO → contain instead.

## Functional cohesion

A routine performs one and only one operation. If you need "and" or "then" to name it, it has multiple operations.

- PASS: `ValidateUserInput()`, `CalculateTotalPrice()`, `SendWelcomeEmail()`.
- FAIL: `ValidateAndSaveUser()`, `ReadFileThenParseJSON()`.

"One operation" is at the routine's declared abstraction level: `CreateUser()` is one operation even though it validates, hashes, and inserts — those are at a lower level.

### Cohesion classification (best to worst — stop at the first match)

| Type | Definition | Verdict |
|---|---|---|
| Functional | One and only one operation | ACCEPT |
| Sequential | Operations share data step-to-step in required order | ACCEPT w/caution |
| Communicational | Operations use the same data but are otherwise unrelated | ACCEPT w/caution |
| Temporal | Combined because done at the same time (startup/shutdown) | ACCEPT if it orchestrates calls; FIX if it does the work directly |
| Procedural | Ordered by external requirement (UI flow), not logic | REJECT |
| Logical | A control flag selects one of several unrelated operations | REJECT |
| Coincidental | No discernible relationship | REDESIGN |

"ACCEPT w/caution" = document why this type is acceptable here, review whether functional cohesion is reachable, and add a TODO if it should improve. Caution is permission with accountability, not permission to ignore.

**Detecting orchestration (temporal OK):** verbs like orchestrates/coordinates/delegates/dispatches/routes suggest orchestration (calls other routines). Verbs like handles/processes/performs/calculates suggest direct work — check the cohesion type and extract the direct work into named routines.

### Improving cohesion

| Type | Steps |
|---|---|
| Sequential | Split per operation; have the dependent routine call what it depends on |
| Communicational | Split into individual routines; reinitialize data near creation; call both from a higher level |
| Temporal | Make the routine an organizer that calls doers; name at the right abstraction level |
| Logical | One routine per distinct operation; move shared code lower; package into a class |

## Pattern-specific guidance

- **Builder** — evaluate cohesion at the class level; methods returning `this` are fine; class cohesion = "constructs one type of object".
- **Mixin/trait** — single focused responsibility, fewer than 3 per class; prefer containment, which makes the relationship explicit.
- **Singleton** — extra scrutiny: does the state truly need to be global? Would DI be cleaner?
- **Event handlers/callbacks** — one event type with one response; for async, evaluate the complete operation, not just what runs before `await`.

## Evidence

- High cohesion → fewer faults: 50% fault-free vs 18% [Card et al. 1986, N=450].
- Deep inheritance correlates with more faults [Basili 1996].
- Information hiding reduces faults ~4x [Korson/Vaishnavi 1986].
- High coupling → ~7x errors, ~20x fix cost [Selby 1991].

This is maintenance data, not shipping data: the gap appears during modification, not first commit.

## Chain

| After | Next |
|---|---|
| Design verified | `Skill(code-foundations:cc-defensive-programming)` |
