---
name: unity-code-architecture
description: "Architecture and code-quality standard for Unity / C# game code: game programming patterns (State, Observer, Command, Object Pool, Component, Event Queue, Service Locator, Update Method, Type Object, Flyweight, Dirty Flag and the rest of the Nystrom catalog), the classic GoF patterns, code smells and refactoring techniques, clean-code rules for functions/names/error handling/tests, component and boundary architecture (assembly definitions, dependency rule, Humble Object), C#/CLR semantics that drive allocations and leaks, OOP principles, SOLID and KISS — applied when writing, reviewing and refactoring code. ALWAYS use this skill for ANY work on game code: new classes, systems and features, refactoring existing code, code review, architecture design, choosing a pattern for a problem, bug fixes that change code. Triggers: 'write', 'rewrite', 'refactor', 'clean up', 'design', 'add a class/system/manager', 'how should I organize', 'which pattern should I use', 'review/rate this code', 'is this code smelly', and any message containing C# code that needs changes or evaluation — even if the user never mentions patterns, smells or SOLID. Do NOT use for non-code questions: game design, balance, art, marketing."
---

# Unity / C# Code Architecture

A stack-agnostic standard. It assumes Unity and C#, and nothing else — no specific DI container, reactive library, async library or inspector plugin.

## 0. First: read the room

Before applying anything below, spend one minute on the repository. **Existing conventions of the codebase outrank the defaults in this skill.** A consistent codebase with conventions you dislike is worth more than a codebase with two competing styles.

Detect and then follow:

| Question | How to check | Why it matters |
|---|---|---|
| Where does *our* code live vs. third-party? | a single root folder such as `Assets/_Project/Scripts`, `Assets/!Content/Scripts`, `Assets/Game/` | never restyle or refactor vendor code |
| Is there a DI container? | `using Zenject` / `VContainer` / `Reflex` / installers / `LifetimeScope` | changes how dependencies are wired (§5.2) |
| Reactive or plain events? | `UniRx` / `R3` / `IObservable` / `event Action` | changes how Observer is implemented |
| Async style? | `UniTask` / `Task` / coroutines | changes how deferred work is written |
| Inspector plugin? | `Sirenix.OdinInspector` / `NaughtyAttributes` | changes how fields are validated/grouped |
| Assembly definitions? | `*.asmdef` files | tells you whether layer boundaries are enforced |
| Tests? | test assemblies, `[Test]` / `[UnityTest]` | tells you how much you can safely refactor |
| C# language level? | `csc.rsp`, `<LangVersion>`, editor version; `#nullable` in existing files | decides file-scoped namespaces, records, pattern matching, nullable annotations |
| Naming conventions? | private field prefix, enum prefix, class suffixes | match them exactly (§ `references/conventions.md`) |

If the repo has no convention for something, use this skill's default and say which default you picked.

## 1. Scope

**Applies to** any task touching game code:
- writing a new class, system, component, manager or feature;
- refactoring existing code;
- code review — "check this", "rate this", "what's wrong here";
- architecture design, choosing a pattern;
- bug fixes that change code;
- any message containing C# that must be changed or evaluated.

**Does not apply to**: game design, balance, narrative, art, audio, marketing, editor/scene setup with no code change.

## 2. Working protocol

### 2.1 Before writing any code

1. **Look for what already exists.** Extending an existing class beats adding a new one. Duplicating an existing utility is a defect.
2. **State the responsibility** of the new unit in one sentence with no "and". If you need "and", that is two units.
3. **Place it in a layer** and namespace (§5.1).
4. **Pick a pattern from the table in §4** — or decide explicitly that no pattern is needed (KISS).
5. If two designs are genuinely comparable, **present both briefly with a recommendation** instead of silently choosing.

### 2.2 While writing

- Contract first (public API / interface), implementation second.
- Smallest possible public surface: `private`, `internal`, `readonly`, `sealed` by default.
- No speculative infrastructure. Interfaces, events and abstract bases are introduced for a **second real** implementation, not a hypothetical one.
- Every `+=`, subscription, `Instantiate`, pool rent, `CancellationTokenSource` gets its matching release written at the same time.

### 2.3 Refactoring

1. Write down current behaviour first: "what it does today".
2. **Name the smell using its canonical name** (Long Method, Feature Envy, Shotgun Surgery, Primitive Obsession — full catalog in `references/refactoring.md`), then name the **refactoring technique** that treats it. Diagnosis before treatment; never start from "I'll rewrite this with a state machine".
3. Propose **behaviour-preserving** steps; each step must compile on its own.
4. Never mix a refactor with a behaviour change — separate commits.
5. Do not restyle unrelated code. Collect unrelated findings under "noticed, did not touch".
6. Check the Unity-specific hazards before structural moves: renaming types/files/`.meta`, moving types between assemblies, renaming serialized fields, splitting a `MonoBehaviour` that prefabs and scenes reference (`references/refactoring.md` §3).
7. Run the checklist (§7) and state explicitly what you verified and what you did not.

### 2.4 Code review

Use the format in §8.2. A review reports findings first; it does not silently rewrite the code.

### 2.5 Bug fixing

Root cause before patch. If the bug is a symptom of an architectural problem, fix it narrowly and raise the architectural problem separately as a proposal — do not smuggle a redesign into a bug fix.

## 3. Principle hierarchy

Conflicts resolve top-down; the higher rule wins:

1. **Works and is readable.** Clarity beats theoretical purity.
2. **KISS / YAGNI.** The simplest thing that solves today's problem.
3. **The three foundations** — encapsulate what varies; program to an interface, not an implementation; favor composition over inheritance.
4. **SOLID** — as a cure for a concrete pain, not as decoration.
5. **A pattern** — as a proven solution to a concrete problem.
6. **Micro-optimization** — only after profiling, except the free wins listed in `references/unity-pitfalls.md`.

**Architecture is about change.** Code has two values: what it does today, and how cheaply it can be made to do something else tomorrow. The second is worth more and is always the one traded away first, because behaviour is urgent and structure is merely important. Decoupling buys structure at the cost of indirection, more moving parts, and sometimes speed — so buy it where change is actually expected, not everywhere.

**Four rules of simple design**, in priority order, as a tie-breaker between two reasonable designs: (1) it is verifiable — the tests run and pass; (2) no duplication; (3) it expresses intent; (4) fewest classes and methods. Rule 4 is last and weakest — never use it to justify a god class.

**Rule of three.** An abstraction (interface, base class, generic, factory) earns its place when there are **two real** usages and a third is plausible. One usage → a concrete class.

**Cost statement.** Before introducing a pattern, state in one line what pain it removes and what it costs (extra layer, indirection, init order, harder debugging). If the cost exceeds the pain, skip it.

**Prototypes.** Throwaway code is legitimate — as long as everyone agrees it gets thrown away. Prototype code that quietly becomes production is how codebases rot.

## 4. Problem → pattern

| Problem | Pattern | Note |
|---|---|---|
| Behaviour differs by mode; boolean flags are multiplying | **State** (FSM); nested → hierarchical; needs return-to-previous → pushdown | 3+ behavioural booleans = time for a state machine |
| Two independent properties multiply states (armed × grounded) | **Concurrent state machines** | n + m states instead of n × m |
| Something must notify N unknown listeners | **Observer** | Use the repo's reactive lib if it has one, otherwise `event Action` |
| A request must be deferred, queued, undone, replayed, remapped or sent over the wire | **Command** | A method call turned into an object |
| Sender and receiver must be decoupled **in time** | **Event Queue** | Audio, analytics, breaking feedback loops |
| Frequent runtime create/destroy | **Object Pool** | Bullets, VFX, damage numbers, enemies |
| Behaviour is assembled from independent parts | **Component** | Unity's native model — compose, don't inherit |
| A collection of objects each advance one frame at a time | **Update Method** | Hundreds of objects → one central ticker instead of N `Update()` |
| The world must advance independent of frame rate | **Game Loop** | Engine-provided; what matters is fixed vs. variable step |
| A global service is needed in many places | **Service Locator** (registered from a composition root) | Priority: injection > locator > singleton |
| Many objects share identical immutable data | **Flyweight** → shared config asset | Intrinsic vs. extrinsic state |
| One class, many variants differing by data | **Type Object** → data assets/definitions | Beats a subclass per enemy breed |
| Objects created from a template | **Prototype** → prefab + factory | Prefer factories/generics over `Clone()` hierarchies |
| A family of behaviours built from the same toolkit | **Subclass Sandbox** | Abilities, effects, powers |
| Expensive derived value recomputed too often | **Dirty Flag** | Recompute on read, not per frame |
| State must not tear mid-update; order must not matter | **Double Buffer** | Simulations, simultaneous resolution |
| "Find things near X" is O(n²) | **Spatial Partition** | Only after profiling |
| Cache misses dominate a hot loop | **Data Locality** | Last resort; profile first |
| Designers need to author behaviour, not just numbers | **Bytecode / scripting** | Very high cost — exhaust simpler options first |

Details, boundaries, "when NOT to use" and code live in `references/patterns.md`. **Read that file before implementing a pattern** rather than reconstructing it from memory.

## 5. Project rules

### 5.1 Layers and dependency direction

Whatever the folder names are, keep these roles separate and keep dependencies flowing one way:

```
Bootstrap / Composition root  →  entry points, wiring
UI / Presentation             →  views, presenters, screens
Gameplay / Domain             →  rules, entities, systems
Core / Infrastructure         →  services, pooling, save, event bus, utilities
Data / Configs                →  config assets, DTOs, constants (no logic)
Integrations                  →  third-party SDK wrappers (ads, IAP, analytics)
Editor                        →  editor-only tooling
```

`Bootstrap → UI → Gameplay → Core/Data`. Reverse dependencies are forbidden: `Core` must not know about `Gameplay`, `Gameplay` must not know about `UI`. UI subscribes to gameplay, never the other way around.

**The Dependency Rule:** source-code dependencies point inward, toward higher-level policy. When control has to flow outward — the domain needs to play a sound, save a file, show a popup — you invert the dependency: the inner layer declares the interface, the outer layer implements it. That is the only legal way to cross a boundary outward.

Where assembly definitions exist (or can be added), give each layer its own — that turns a layer violation into a compile error instead of a matter of discipline. Three rules govern how the assemblies are cut (details and metrics in `references/architecture.md` §3–4):

- **Group by reason to change**, not by technical kind — classes that change together belong in the same assembly.
- **No cycles.** Break one by inverting a dependency or extracting a shared component, never by adding a backwards reference.
- **Depend toward stability, and make the stable things abstract.** `Core`/`Data` are small, mostly interfaces and plain data, and everything depends on them; `UI`, `Integrations`, `Editor` are concrete and nothing depends on them. A big concrete `Utils`/`Shared` assembly that everyone references is the classic failure.

**Third-party SDKs never leak.** Ads, IAP, analytics, attribution, notifications and similar are used through your own interface (`IAdsService`, `IAnalyticsService`) implemented in the integration layer. Gameplay code must never `using` a vendor namespace. This is what makes SDK swaps and stubbed dev builds cheap.

### 5.2 Composition and access to services

Preference order:

1. **Constructor injection** — for plain C# classes.
2. **`[SerializeField]` reference or an explicit `Construct(...)`/`Initialize(...)` method** — for `MonoBehaviour`.
3. **DI container** — if the project has one, follow its idiom (installers, scopes) rather than inventing a parallel mechanism.
4. **Service Locator** — only for genuinely global, single-instance services, and only registered from the composition root.
5. **Singleton `MonoBehaviour`** — default answer is no. If it looks unavoidable, work down the ladder in `references/patterns.md` § Singleton first, and say why the alternatives failed.

There should be one composition root per application/scene that creates services, wires them and hands out dependencies. Never resolve dependencies with `FindObjectOfType`/`FindAnyObjectByType`. The composition root is the only place allowed to know every concrete type — which is what makes a `DevBootstrap` with stubbed SDKs a plugin rather than `#if` branches scattered through gameplay.

**Keep the `MonoBehaviour` humble.** Split every behaviour into the part that needs the engine and the part that does not: the `MonoBehaviour` holds serialized references, forwards lifecycle calls and moves already-computed values into the scene; the rules live in a plain C# class next to it. A view assigns strings and flags that a presenter has already decided — it does not format, branch on game state, or compute. This one habit is what makes gameplay logic testable without opening a scene (`references/architecture.md` §6).

### 5.3 Unity hard rules

- `GetComponent`/`Find*` only during initialization; cache the result. Never per frame.
- Cache `Camera.main`.
- Fields are `[SerializeField] private`. Public fields are not allowed.
- Physics in `FixedUpdate`, input in `Update`, camera/follow in `LateUpdate`.
- Every subscription has a matching unsubscription. A leaked subscription is a bug, not a style issue.
- No per-frame allocations: no LINQ, string concatenation, or new collections in `Update`.
- No string-based dispatch (`SendMessage`, `Invoke("Name")`, `BroadcastMessage`).
- Config values live in config assets or serialized fields, never as magic numbers in code.
- Anything that survives a scene load or lives in static state must have an explicit reset path.

Full list with examples: `references/unity-pitfalls.md`.

### 5.4 Naming and style

PascalCase types/methods/properties, `_camelCase` private fields, `I`-prefixed interfaces, one type per file, namespace mirroring the folder path. Full rules — including class-name suffix vocabulary and the words to avoid — in `references/conventions.md`.

### 5.5 Method-level rules

- One thing, one level of abstraction, a name that makes a comment unnecessary.
- 0–2 parameters is normal, 3 needs a reason, 4+ is a Parameter Object.
- **No flag arguments** — `Fire(bool charged)` is two methods.
- **Command–Query Separation** — a method either changes state or answers a question, never both.
- **Never return `null`** where an empty collection, a Null Object or a `TryX(out …)` would do; do not pass `null` into your own APIs.
- Exceptions carry context and are never swallowed; conditions you can test for are tested, not thrown.
- Third-party APIs are consumed through an interface you own — the shape you wish they had, not the shape they have.

Full treatment in `references/clean-code.md`.

### 5.6 C# semantics that bite

- Every allocation is real: Unity's collector is non-generational and there is no cheap gen-0.
- The invisible allocators are **closures** (a capturing lambda allocates per call), `yield return` state machines and uncached `WaitForSeconds`, LINQ, string building, and **boxing** — a struct reaching an `object`, an interface call on a struct, `Enum.HasFlag`, `foreach` over `IEnumerable<T>`.
- A delegate holds a strong reference to its target, so **an object subscribed to an event cannot be collected**. That is why the unsubscribe rule is a correctness rule, not a style one. An inline lambda cannot be unsubscribed — keep a field or a handle.
- `struct` only for small (~16 bytes), immutable, primitive-like values; a struct read out of a collection is a copy.
- `const` is baked into consuming assemblies; anything crossing an assembly or package boundary is `static readonly`.
- Unity's fake null: `?.`, `??` and `is null` bypass the destroyed-object check on `UnityEngine.Object`.

Full treatment in `references/csharp-runtime.md`.

## 6. Red flags — call these out on sight

Use the canonical smell name (in bold) so the finding is diagnosable; the catalog with treatments is in `references/refactoring.md`.

- Method over ~30 lines, or nesting deeper than 3 → **Long Method** → Extract Method, guard clauses.
- Class over ~200 lines or with more than ~7 public members → **Large Class** → Extract Class.
- Floats, ints and strings standing in for concepts (ids, currency, damage types, tags) → **Primitive Obsession** → typed values, config assets.
- More than 3–4 parameters, or the same group of them travelling together → **Long Parameter List** / **Data Clumps** → Introduce Parameter Object.
- The same `switch`/`if-else` over a type or enum in two or more places → **Switch Statements** → polymorphism, Type Object, State.
- 3+ booleans describing an object's mode → State machine.
- One class edited for many unrelated reasons → **Divergent Change**; one change forcing edits in many files → **Shotgun Surgery**.
- A method that uses another object's data more than its own → **Feature Envy** → Move Method.
- `a.B.C.D.Method()` → **Message Chains**; a class that only forwards calls → **Middle Man**.
- An abstraction with exactly one implementation, added "for later" → **Speculative Generality** → delete it.
- Unused fields, methods, parameters, unreachable branches → **Dead Code** → delete it.
- A comment explaining *what* the code does → **Comments** smell → rename or extract instead.
- A subclass that overrides members into no-ops or uses little of what it inherits → **Refused Bequest** → replace inheritance with delegation.
- `Manager`, `Helper`, `Utils`, `Controller`, `Handler` as a complete name → undefined responsibility.
- `GetComponent`, `Find`, `Instantiate`, `Destroy` inside `Update` → cache or pool.
- Mutable `static` state → hidden global dependency.
- Public fields, or setters with no reason, or a mutable collection returned from a getter → leaking encapsulation.
- Subscribe without unsubscribe → leak (the "lapsed listener" problem).
- Magic numbers and magic strings → constants or config assets.
- Empty `catch`, or `catch (Exception)` that swallows → hidden failure.
- Gameplay logic inside a UI class, or vice versa → layer violation.
- A vendor SDK namespace imported into gameplay code → missing integration wrapper.
- Config data mutated at runtime on a shared asset → shared-state corruption.
- A `bool` parameter that selects behaviour → **flag argument** → split the method.
- A method that both changes state and returns an answer → **CQS violation**.
- A method returning `null` for "nothing found" → empty collection, Null Object or `TryX(out …)`.
- `catch` that logs and continues, or rethrows with `throw ex;` (which erases the stack trace).
- A capturing lambda, LINQ query or `new WaitForSeconds` created on the per-frame path → allocation per frame.
- A struct going through `object`, an interface or `HasFlag` in a hot loop → hidden boxing.
- A `MonoBehaviour` view that formats, computes or branches on game state → it is not humble; move the logic out.
- A cycle between assemblies, or a backwards `.asmdef` reference added to make something compile.
- A large concrete `Utils`/`Shared`/`Common` assembly that every other assembly references.
- `using UnityEditor;` reachable from runtime code, or editor-only code outside an `Editor` assembly.
- Save data keyed by object name, scene path or sibling index, or written without a version field.
- Folders named `Managers`, `Controllers`, `Interfaces`, `Abstracts` at the top level → the structure describes the framework, not the game.

## 7. Pre-delivery checklist

- [ ] One responsibility per class, expressible without "and".
- [ ] No unused abstractions, fields or usings.
- [ ] Every subscription, token and pooled object is released.
- [ ] No `GetComponent`/`Find`/allocations on the per-frame path — including closures, LINQ and boxing.
- [ ] Dependencies point in the allowed direction (§5.1), and the assembly graph has no cycles.
- [ ] Logic that does not need the engine is in a plain C# class, not in the `MonoBehaviour`.
- [ ] No method returns `null` where an empty collection or Null Object works; no flag arguments.
- [ ] Naming matches the repository's existing conventions.
- [ ] Designer-tunable values live in serialized fields or config assets.
- [ ] Edge cases handled: null, empty collection, destroyed object, re-entrant call.
- [ ] The pattern(s) used and the reason are stated — or it is stated that no pattern was needed.
- [ ] What was **not** verified is stated explicitly (compilation in-editor, play-mode run).

## 8. Output formats

### 8.1 New code / feature

```
Problem: <one sentence>
Approach: <pattern(s) and why — or "no pattern, KISS">
Files:   <paths and the role of each>

<code>

Trade-offs: <what was simplified and why>
Open questions: <if any>
```

### 8.2 Code review

Findings ordered by severity. For each:

```
[Critical | Important | Minor] <file:line> — <one-line claim>
Why:  <principle/pattern violated and the failure it leads to>
Fix:  <concrete change>
```

Close with two or three lines on what is good. Do not invent findings to fill space — if the code is fine, say so.

### 8.3 Architecture choice

At most two or three options, each with essence / upside / downside / cost, then **one explicit recommendation**. Never a survey without a recommendation.

## 9. References

Load on demand — do not read them all up front:

| File | Read it when |
|---|---|
| `references/patterns.md` | implementing any game programming pattern — **required** before writing one |
| `references/refactoring.md` | reviewing or refactoring: code smell catalog, refactoring techniques, safe process, Unity refactoring hazards |
| `references/clean-code.md` | writing or reviewing at method/class scale: functions, names, comments, error handling and null, boundaries, tests, review heuristics |
| `references/architecture.md` | cutting assemblies, drawing a boundary, dependency direction, Humble Object / testability, "is this a detail?" |
| `references/csharp-runtime.md` | allocations, boxing, GC, struct-vs-class, events and lifetime, `const` vs `static readonly`, exceptions, nullability |
| `references/gof-patterns.md` | choosing among the classic GoF patterns; the three design principles under SOLID |
| `references/solid.md` | applying SOLID/OOP, or explaining why something violates them |
| `references/unity-pitfalls.md` | lifecycle, per-frame performance, leaks, serialization, null semantics, scenes, save data, editor code |
| `references/conventions.md` | naming, file layout, namespaces, assembly definitions, tests, version control |

## 10. Sources

- Robert Nystrom, *Game Programming Patterns* — https://gameprogrammingpatterns.com/contents.html (free online)
- Alexander Shvets, *Dive Into Design Patterns* — https://refactoring.guru/design-patterns/book
- Alexander Shvets, *Dive Into Refactoring* — https://refactoring.guru/refactoring/course
- Martin Fowler, *Refactoring* — the origin of the smell and refactoring catalogs
- Robert C. Martin, *Clean Code* — functions, names, error handling, tests, review heuristics
- Robert C. Martin, *Clean Architecture* — component principles, boundaries, Humble Object, policy vs. detail
- Jeffrey Richter, *CLR via C#* — value/reference semantics, boxing, GC, events, exceptions
- Paris Buttfield-Addison, Jon Manning, Tim Nugent, *Unity Game Development Cookbook* — engine-level recipes
- Unity Manual — order of execution, performance, serialization

The reference files are distilled working guidance, not substitutes for the books. When a decision is close, go read the source chapter.
