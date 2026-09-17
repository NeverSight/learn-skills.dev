---
name: caching
description: Cache discipline for any repo that serves a value from memory or a cache server instead of recomputing it from the durable store, in any language — one adapter seam, no caching annotation or decorator, read-through only, nothing correctness-bearing in the cache, keys that carry the caller's scope, a committed staleness ceiling, delete-only invalidation after commit, exact serialization round-trips, no substituted value on a cache error, and the three-configuration differential gate. Carries the verdict on every shape a repo assembles out of these primitives — two cache tiers, a collection cached beside its members, a cache shared by two deployables, a background warm, a loader that reads another service. ALWAYS load before adding a cache, a memo, a loading cache, a caching annotation or an expiry, before deciding whether a repo needs a cache at all, before putting a cache behind a proxy or a content-delivery network, and before caching a value another rule set governs. States the kind of check each rule needs; the tool is named in the matching stack skill (caching-java).
---
# Cache discipline

Sixteen directives, `C-1` … `C-16`. Each states **kind** of check it needs. No tool named here — almost none of these checks is portable across languages. Nearly every rule needs different tool per stack, and cache rule with no named check is wish. Tool named in stack skill.

**Read marker ceiling before rules.** All sixteen are **convention**, dated 2026-07-29, and **no production use of this rule set anywhere** — each is design argument, not execution result. Nothing confirmed, **no marker may be promoted without new research pass.** What 2026-07-29 pass did confirm is *tool* evidence, and that lives in stack skill. Read this as defensible, cheap, enforceable design that fails toward safety, not verified finding. Full statement in *Markers, dates, and what they mean* below.

## The premise these rules are conditioned on

**Code written by LLM agents, no human reads it line by line, and repo caches value it could recompute from durable store.**

Both halves do work. Cache turns correct answer into plausible one: wrong answer is well-formed, validates, violates no constraint, decays away before anyone reproduces it. Nobody reads code → no second reader notices number is three days old. Verdict portable exactly as far as its premise — in repo where human reads every cache change line by line, several rules below drop from mandatory to advisable. Where so, say it and carry burden of saying it; do not silently drop rule.

**Second half covers in-process cache, not just cache server.** Hash map memoized inside service method, loading-cache library, or framework's simple in-memory cache manager is cache under these rules. Deliberate, and case that matters most: in-process shape is one most repos here should take, imports no cache *client*, and discipline scoped to cache server would leave it outside every check below. Real defect found in hostile audit of these rules, not hypothetical.

Rules bind from **first cached value**. Before that: dormant, not absent.

## Start by not caching

**Most repos should run no shared cache at all, and this belongs before any rule rather than after.**

Org fact this rests on, stated because it is ground not aside: eighteen three-person teams, one engineer each, and **no platform or operations role**. Shared cache is stateful service somebody patches, sizes, monitors, fails over. No somebody.

Ranking, for repo with no measured latency problem:

1. **No cache.** Cheapest correct answer. Nothing to patch, value cannot be stale.
2. **An in-process cache with a short expiry.** Second cheapest. No new service. Limit is per-instance scope — `C-9`'s stated condition.
3. **A shared cache server.** Only when number says so.

Add cache when measurement says so, not when design looks like it wants one. **Probe-scoped ground (2026-08-11, bare sonnet + opus):** handed a slow endpoint with a findable root cause, 4/4 sessions fixed the cause and added no cache — never cite "the first answer is a cache" as self-evident; unprobed shape: no visible fix. The org fact above, not agent instinct, is this section's ground. **Which engine to run, where needed, is not directive here** — per-stack pick with deployment-shaped and ecosystem-shaped gates, stated in stack skill. Nine-candidate survey of engine landscape, with licences, release cadence and ground each candidate lost on, is in [evidence.md](evidence.md); evidence for that pick, not rule here.

## What is here and what is elsewhere

- **This skill** — seam, what cache may hold, keys, expiry, invalidation, serialization, failure behaviour, evidence gates. Platform-neutral: every rule states check kind, names no tool.
- **`caching-java`** — same rules with Java, Spring Boot, ArchUnit, Error Prone, Jackson, Testcontainers and Toxiproxy named, engine pick, one-time gate wiring. Install in repo on that stack; without it every rule here has check kind and no tool.
- **`money` and `money-api`** — published, and `C-5` interlocks with both. `M-17`, in `money-api`, requires idempotency record written in same transaction as money effect; **cache cannot host that record**, and `C-5` is only place that ban is stated. Neither money skill states it: `M-17`'s same-transaction requirement excludes cache by implication, and `C-5` makes it structural. `C-5` also does not weaken `M-20`, in `money`: see *Interlocks these rules must not break*.
- **`money-storage`** — published. Cached amount is one money shape its composite-shape table hands to this skill: copy of money value that no column constraint, no `CHECK` and no schema lint reaches. `C-10` is where float ban re-enters at fourth layer, after field, column, wire.
- **`async-handoff`** — published, and `C-9` collides with it at one point. `C-9` needs post-commit registration point — exactly seam `E-5` confines when it bans publish outside outbox relay. **Repo satisfying `C-9` carelessly defeats `E-5` entirely.** Interlock stated below; install `async-handoff` in any repo handing work off asynchronously.

## The defaults these rules override, by name

Agent told "add caching" writes one specific thing. Naming it is point; "cache carefully" overrides no instinct.

- **Annotation-driven declarative caching** — one-line decorator, attribute or annotation every framework ships and every tutorial shows. **Training-corpus favourite by wide margin and single most likely thing agent writes.** Banned by `C-2`. Genuinely attractive: one line, no change to business logic, framework-handled keys and expiry, trivially removable. Loses on four grounds — effect fires from no written call, so caller's text identical whether value is fresh or three days old; key generation implicit, making `C-6`'s dropped-scope failure default rather than mistake; framework's error handler substitutes value by design, which is `C-12`'s banned shape shipped as feature; and with no reader, *which methods are cached* becomes fact only annotations know and nothing enumerates, defeating `C-15`.
- **A caching decorator behind an existing domain interface** — tasteful refactor agent reaches for when annotation banned. Rejected by `C-2`'s second half. Same ambient modifier in different costume: caller's written call unchanged, answer now turns on cache state. It **passes seam check**, because decorator legitimately lives in infrastructure module and legitimately imports adapter — why `C-2` is separate rule from `C-1` rather than clause of it.
- **Write-through and write-behind** — keep cache coherent with no invalidation to forget. Rejected by `C-4`: both make cache second write target, so *which store is authoritative* stops having structural answer, and write-behind is hidden dirty-state flush. Both unwritable under `C-4` at no extra cost.
- **The cache as a lock manager** — set-if-absent locking, canonical recipe in every engine's docs. Rejected by `C-5`. **"Our engine cannot do it" is not available as defence**, and engine is named because ground is its own documented protocol rather than any check: **memcached** — no persistence, no scripting, no transactions — still defines `add`, `cas`, `incr` and `decr`, and add-based locking is its canonical lock.
- **Expiry-only invalidation, with no delete** — rejected as design by `C-9`: makes every write's effect invisible for whole expiry window, wrong-but-plausible answer by construction. **Kept as stated fallback** for in-process cache on more than one instance, where delete genuinely cannot cross instances.
- **Picking a restricted engine as the discipline** — one decision instead of sixteen. Rejected: restriction claimed usually false, pick's right answer varies *within* stack, and seam is enforcement on any engine.

Full steelman for each, and wordings that must not be reintroduced, in [evidence.md](evidence.md).

## What to do when this skill fires

1. **First ask whether to cache at all.** *Start by not caching* above is step one, not preamble.
2. **Name the adapter module.** Every rule below is check on one named module's API surface. Until it exists, nothing for rules to bind.
3. **Add the entry to the committed catalog** (`C-15`) in same change. Catalog is machinery `C-7`, `C-8`, `C-10`, `C-13` and `C-14` read, not documentation.
4. **State the repo's staleness ceiling** as machine-readable value in committed artifact (`C-7`). Ceiling in prose is ceiling no check can read.
5. **Record in the plan or spec that these rules bind this feature** (`C-16`).
6. **Wire the gates.** This skill states check kinds; kind with no tool is wish. On Java, `caching-java` names tools and has wiring section.

## The seam

**C-1 — Every cache read and write goes through one named adapter module. No cache client library, no in-process cache library, and no hand-rolled memoization construct is reachable outside it.** Every other directive is check on that adapter's API surface, so second way in is not one bypass — it is whole set reporting green while banned shapes pass. That is false assurance these rules exist to prevent, and worse than no rule. **In-process half is not optional**: memo inside service method, loading cache, or framework's in-memory cache manager imports no cache client and would sit outside all sixteen checks — shape agent writes first. **Client ban list must be complete for engine repo actually runs** — ban list naming one vendor's clients on repo running fork is gate with hole, because fork's clients are separately named packages. Engine named in stack skill; completeness obligation here because it is seam's, not engine pick's.
*Static rule (architecture or dependency check), plus a field-type rule for the hand-rolled case. Convention, 2026-07-29.*

***A cache is declarable in two languages this check does not read.* Layer check, 2026-08-02, conversion-dated.** Seam check read application source. Two caches never appear there. **Framework cache manager declared in configuration** — a cache type in a properties or YAML file, a starter that auto-configures a client, a bean defined in configuration class — import nothing at any call site the dependency check inspect. And **response cache in the deployment**: reverse proxy, content-delivery network, or `Cache-Control` header this repo emit. Second one serve a value from memory instead of recomputing it from the durable store, which is this skill's own predicate word for word, and **no directive here reach it** — no catalog entry, no staleness ceiling, no `C-13` differential run, and its invalidation is somebody else's console. Check that would reach it is a lint over committed deployment manifests and over the header values the API document declare. **Not carried here.**

**C-2 — No ambient cache dispatch. No caching annotation, attribute, decorator or aspect; and no class implementing a domain interface may depend on the cache adapter.** Annotation fires effect from no written call. Decorator wired behind domain interface leaves caller's text unchanged while answer turns on cache state. Same defect: behaviour not in program text, in repo where program text is only record anyone reads. Second half is separate rule from `C-1` because **seam does not catch it** — decorator legitimately lives in infrastructure module and legitimately imports adapter, so seam check passes over exactly this case.

**State the decidable predicate, not the intent.** Write rule as *implements a domain interface and depends on the cache adapter*. "Caching" is not property static rule can read; rule worded around it has no operand to match.

**And state why an explicit read-through call is not the banned modifier**, in repo's own text: call is written and named at call site, so value's provenance fixed there. Shipping permissive half without that sentence leaves next agent guessing where line is.
*Static rule. Convention, 2026-07-29.*

**C-3 — The loader is a nominal port type, not a lambda or a single-method functional interface, and its implementations live only in the module that may depend on the durable-store client.** Most important authoring instruction in set; exists because obvious form is undecidable. Type loader as single-abstract-method interface and any lambda body becomes legal loader — including one closing over process-local state write path populated — and static analysis reading compiled output cannot follow it. Declare port with two abstract members, or as abstract class, and lambda becomes **compile error**, so every loader is named importable type. Confining that type's implementations, and confining durable-store client's dependents, are *type dependencies* — question architecture tools decide soundly.

Do not write rule of form "the loader must read the authoritative store". Unsound by construction wherever loaders can be lambdas; reports green over case it exists to stop.

**Cost accepted, and it is real:** every loader is class rather than lambda. Price of rule being decidable.
*Type design plus a static rule. Convention, 2026-07-29.*

## What a cache may hold

**C-4 — The adapter exposes no bare write. The only way a value enters the cache is as the return value of a loader on a read-through call.** Makes write-through and write-behind unwritable, so neither needs own directive.

**Do not restore the wording "the cache is never the source of truth".** True and undecidable — no check can decide which store is authoritative, so gate written against it reports green over exactly case rule exists to stop. What remains decidable is property of **write path**, stated here. Undecidable residue carried structurally by `C-3`'s confinement and otherwise by spec-and-review. Say that split plainly rather than claiming check decides which store is authoritative.
*Type design. Convention, 2026-07-29.*

**C-5 — Nothing correctness-bearing goes in the cache: no mutual exclusion, no counter a limit or a balance depends on, no queue, no idempotency record, no state whose loss changes an answer.** Eviction, failover or restart drops entry with no error, so lock silently stops excluding and limit silently stops limiting.

Enforced **by shape**: adapter exposes no atomic primitive at all — no set-if-absent, no increment, no list or stream operation — and `C-1` makes raw primitive unreachable.

**The enforcement is the seam, not the engine.** Do not write this as "the engine cannot do it". Engine named here because its documented protocol is this clause's **ground** rather than its enforcement: **memcached** — no persistence, no scripting, no transactions — nonetheless defines `add`, `cas`, `incr` and `decr`, and add-based locking is its canonical lock. Seam therefore holds even on most restricted engine repo here would pick, and repo running memcached can tell this clause is about it.

**Money interlock, and those rule sets are published.** `M-17`, in `money-api` skill, requires idempotency record written in same transaction as money effect, and `M-40` in `money-storage` requires same of everything making money effect reconstructable. **That record cannot live here**, and ban is stated on this side only: cache write is in no transaction, so `M-17` already excludes it by implication, and `C-5` makes it structural. Do not read either money skill as carrying this ban — see [evidence.md](evidence.md).
*Type design plus a static rule. Convention, 2026-07-29.*

## Keys and tenancy

**C-6 — The cache key is the loader's full argument tuple, and the caller's authorization scope is one of those arguments. Hand-built key strings are banned; the scope value is obtainable only from the request-context accessor.** Key assembled independently of loader's arguments can omit one, and key missing tenant returns well-formed answer belonging to someone else — no exception, no constraint violation, nothing to notice. Key that *is* the tuple makes that omission compile error.

**Word the ban as unwritability, not impossibility.** State as *the key factory accepts no free-text parameter*, and give scope type no public constructor so request context is its only source. Both make wrong call uncompilable, holding regardless of what any tool can inspect. Do **not** word as "no string concatenation" and do not rest on claim that concatenation is unmatchable by static analysis — that ground is challenged and unverified ([evidence.md](evidence.md)), and rule does not need it.

**Two honest limits, and both are stated rather than papered over.** Type design decides scope-typed parameter is *present*, never that value passed is current caller's — closing that needs constructor confinement above, which is decidable. And type system decides nothing about whether two distinct tuples render distinct keys. So two backstops, in order: property test that equal keys imply equal uncached results, and — because that test varies only what its generator varies — **two-tenant integration test per cached read path**, seeding different data for two tenants, warming as one and reading as other. Second is outside oracle: ground truth is underlying store, not assertion written by model that wrote key.
*Type design plus a property test plus an integration test. Convention, 2026-07-29.*

***The rendered key lands in the engine's keyspace, which have its own rules.* Layer check, 2026-08-02, conversion-dated.** Type design govern the tuple; what the engine store is the **rendered string**, and the engine constrain it. **memcached** — named already in `C-5` as this set's most restricted engine — cap a key at 250 bytes and forbid whitespace and control characters. A tuple carrying a scope, a long natural identifier and a shape hash render past that, and the client either reject it or the engine truncate it: **truncation collide two tenants' keys**, which is `C-6`'s own failure arriving through the one language its three checks do not read. Neither the property test nor the two-tenant test see it unless their fixtures happen to be long. Check that reach it is an assertion on **rendered key length and charset per catalog entry, against the engine actually deployed** — not carried here.

## Expiry

**C-7 — Every entry's expiry comes from the committed cache catalog, and every catalog expiry is at or below the repo's committed staleness ceiling. Expiry values are constructible only at catalog registration, never at a call site.**

**Do not restore the wording "no entry without a TTL".** Enforceable and nearly worthless alone: thirty-day expiry satisfies it — case rule exists to stop.

**The ceiling is the enforceable half, and it must be a machine-readable value in a committed artifact.** Lint cannot read prose, and with no committed operand it passes over every catalog value and reproduces defect. Ceiling's value is repo's own call, stated in repo's own text. Registration-only constraint stops inline expiry lint never sees.

**State the expiry's actual job honestly:** not invalidation mechanism. It is **bound on missing invalidation** — bug written when one of four write paths is forgotten.

**Named gap, and it is a gap in every stack.** Server-side eviction under memory policy can drop entry *before* its expiry, and no code-level check in any language reads engine configuration. "Has an expiry" is not "lives until its expiry".
*Type design plus a schema lint over the committed catalog. Convention, 2026-07-29.*

**C-8 — Caching an absent result is opt-in per catalog entry, and that entry carries its own shorter expiry.** Read-through adapter caches whatever loader returns, including "not found", unless built not to — then row exists in store while API says it does not, intermittently and unreproducibly. Loader's return type distinguishes value from absence, and adapter drops absence by default.
*Type design plus an integration test: read a missing key, create it, read again, assert found. Convention, 2026-07-29.*

## Coherence and invalidation

**C-9 — Invalidate by delete only, and only from the transaction seam's post-commit registration. Never populate the cache from a write path.** Sharpens `C-4` rather than adding rule.

Populating on write races concurrent read that already loaded old value and is about to store it, and makes cache second write target. Deleting *before* commit lets concurrent read repopulate pre-commit state, which then lives until expiry. Delete-after-commit degrades to miss, always correct.

**The ordering is made decidable by confinement, not by a test.** Adapter's invalidate operation reachable only from one transaction seam's post-commit callback. Test cannot decide it: "a rolled-back write leaves nothing cached" and "a committed write leaves nothing stale" are **both satisfied by delete-before-commit implementation** in sequential test, so repo naming only that test has gate with blind spot exactly where it matters.

**Two residual exposures, accepted and stated.** Crash window between commit and delete is bounded by expiry ceiling and nothing else. And **on in-process cache delete does not cross instances**, so above one instance ceiling is entire coherence guarantee — one place expiry-only invalidation is honest answer rather than rejected one.
*Type design plus a static rule (confinement) plus an integration test (a rolled-back write leaves nothing cached). Convention, 2026-07-29.*

## Serialization

**C-10 — Cached values are immutable and round-trip through the cache's serializer exactly. The check reads the concrete type at its catalog registration site.** In-process cache handing one instance to two callers turns one caller's mutation into other's wrong answer, no error. Lossy round-trip does same across remote cache: decimal losing scale, instant losing zone, amount becoming binary float — **money float ban re-entering at fourth layer**, after field, column, wire.

**Do not write the check against the adapter's value type parameter.** In erasing type system, tool reading compiled output sees only erased top type there and decides nothing. That false green shipped once already, by rule banning unloggable domain types on erasing stack. **The `llm-default-traps` skill carries that case's tool ban and erasure ground behind it, and the domain-type rule the ban enforces is the `java-backend-observability` skill's** — published, but only for that one stack, why trap is still recorded here and in stack skill rather than left to pointer. Concrete type known at **registration site**, and source-level checker sees static types; that is where check goes.
*Static rule at the registration site plus a property test (serialize, then deserialize, equals the original) per cached type. Convention, 2026-07-29.*

***The serializer's own configuration is a second language, and it is global.* Layer check, 2026-08-02, conversion-dated.** Check read the concrete type at registration site. **What that type round-trip to is decided elsewhere** — a serializer module registered once at startup, a mixin, a global date or decimal setting, a field-naming policy. Change one and every cached type's round-trip change, with **no edit at any registration site the check read**. Property test per type do catch it, and only for types it cover — so the pair is registration-site static rule plus per-type property test, and **a type with no property test have no gate against a global configuration change at all**. State the split; do not read the static rule as covering serialization behaviour.

**C-11 — A build-computed hash of each cached value's shape is part of its key namespace; the hash is committed and any undiffed change fails the build. Deserialization is strict: an unknown or missing field is an error, never a default.** After deploy, cache holds bytes written by previous shape; silent case is field added since — defaulting to zero, false or empty on read, wrong but plausible, only on hits, decaying away before anyone reproduces it.

Strict deserialization turns that into loud failure; shape hash turns it into **cold cache**, better failure. So hash is primary, strict parsing is backstop for case where shape unchanged but meaning is not. Regenerate-and-diff makes shape change visible at one gate a human reads.

**The rejected alternative is a hand-bumped version integer.** Forgetting to bump it is exactly failure this prevents, so it is checklist item for reader who does not exist.
*Golden test (regenerate-and-diff) plus a parse test. Convention, 2026-07-29.*

## Failure behaviour

**C-12 — On a cache error, answer from the authoritative store or fail with a coded error. Never a stale entry, a default, an empty collection, or a partly populated result.** Falling back to store is correct and stays legal; banned is **substituting a value**. Defensive catch returning empty list reads as robustness and returns wrong answer with success status.

**Do not restore the wording "a cache failure fails loud".** As worded, actively wrong twice: bans falling back to authoritative store, which is correct behaviour, while permitting real hazard — substituting value — as long as something is logged.
*Integration test under a fault-injected configuration. A partial compiler or linter check on the empty-catch case only, where one exists; the general case is spec-and-review, because a handler that logs and returns a default is not an empty handler. Convention, 2026-07-29.*

***The banned substitution is writable in configuration, with no handler anywhere.* Layer check, 2026-08-02, conversion-dated.** Both named checks read code — a catch block, or a fault-injected run. **A resilience library's fallback is neither.** Declare a fallback method or a default value for the cache call in the library's configuration, and on error the call return that value with no exception, no catch block, no line of application source involved. That is `C-12`'s banned shape exactly, arriving as configuration. **`C-13`'s every-operation-errors run is the one check that see it**, because it compare answers rather than read code — and it see it only on paths the suite drive, which `C-13` itself say is coverage-shaped. Ban the library's fallback feature by name in the repo's own text, per `enforceable-rules`' *Distrust what the agent picks*; the fallback is the corpus's first answer to "handle a cache error".

## Evidence gates

Outside checks. After implementation, model reviewing model output shares implementer's blind spots, so gate whose ground truth comes only from assertions same model wrote proves nothing about plausible-but-wrong output. **The uncached system is the one oracle here that the implementing model did not write** — why central gate is differential.

**C-13 — The integration suite runs in three cache configurations — normal, always-miss, and every-operation-errors. The normal and always-miss runs must produce identical observable results; under fault injection every answer either matches the cache-off answer or is a coded error; and the normal run fails if any catalogued cache records zero hits.** Zero-hit assertion is not optional: suite that never warms cache passes all three runs trivially.

**Claim only what it catches.** Catches value existing only in cache on driven paths, unintended cached absence, lossy round-trip, substituted value on error. Does **not** catch key dropping tenant — single-tenant suite returns same answer in both runs, why `C-6` carries own two-tenant test. Does **not** catch stale read after write unless suite writes and re-reads one key inside its expiry, and nothing here asserts any suite does. Coverage-shaped: proves recomputability for paths suite drives and no others. Never describe as catching most of this rule set.
*Integration test (differential — three configurations of one suite, compared against each other). The check kinds this rule set uses have no term for differential execution; the nearest, a characterization replay, compares against committed output files, while this compares against the same system with the cache removed. The parenthetical carries that difference; no new kind is invented for it. Convention, 2026-07-29.*

**C-14 — Each of the three configurations proves it took effect. The always-miss run asserts zero hits on every catalogued cache and fails if any hit is recorded; the normal run asserts at least one; the fault run asserts the injected fault was observed at least once.** Separate rule rather than clause of `C-13` for one reason: **it is the one that gets omitted.**

Nothing in differential gate verifies its own configurations. Test-scoped binding that does not win, profile never activated, fault never applied — and all three runs are normal run, results trivially identical, gate reports green over every failure it exists to catch. Six of sixteen directives lean on `C-13`; `C-14` makes that lean safe.
*Integration test (positive control). Convention for the rule; two tool facts behind it are confirmed and are named in the stack skill, because both are facts about specific tools. Convention, 2026-07-29.*

**C-15 — A committed cache catalog names every cache, its key shape, its expiry, its negative-caching decision and what invalidates it, generated from the adapter's registrations and diffed in CI.** Catalog is inventory reader would have carried in their head, and it is **load-bearing machinery rather than documentation**: `C-7`'s ceiling lint reads it, `C-8`'s opt-in reads it, `C-10`'s registration-site check reads it, `C-13` and `C-14` enumerate it. Without it, agent adds fifth cache inside helper method and first symptom is inexplicable stale answer months later with no list of suspects. New cache cannot appear without git-visible line at gate a human reads.

**One honest limit:** "what invalidates it" is free prose no regenerate-and-diff can compare against behaviour. That field is catalog's documentation half; calling it gate would be lie.
*Golden test (regenerate-and-diff). Convention, 2026-07-29.*

**C-16 — The plan or spec that introduces the first cache records that these rules bind it.** Not arming mechanism — this skill's **description** fires when agent is about to cache something, without anyone remembering to re-read anything. What `C-16` adds: decision written down at one gate a human reads, so choice to adopt or diverge is visible there rather than only in code.
*Spec-and-review at the plan approval gate. Convention, 2026-07-29.*

## Composite shapes a repo assembles out of these primitives

**`enforceable-rules`' composite-shape check, run 2026-08-02, conversion-dated. This section is owed to a defect in a neighbouring rule set and this one had the same defect** — sixteen directives each naming its own honest limit, reading as thorough, and **silent about every shape a repo build out of two of them.** Naming a gap inside a directive surface nothing about a shape nobody wrote a rule about. Every entry below is marked; **silence about a shape is a defect in this section, not the reader's problem.**

**This table promote no marker.** Most entries are a verdict a published directive already imply and nobody stated as a shape. **One entry is a ban no directive implies**, and it carry its ground, the organisation fact it rest on, the absence of a panel, and the condition that reopen it.

| Shape | Verdict |
| ----- | ------- |
| **Two tiers — in-process cache in front of a shared one** | **permitted with conditions, and the conditions are where this set is thinnest.** Each tier is its own catalog entry with its own expiry (`C-15`, `C-7`), and `C-9`'s delete must reach **both**. It cannot reach the in-process tier on more than one instance — `C-9` say so already — so **the near tier's expiry is the entire coherence guarantee for it**, and the repo's staleness ceiling must be set from that tier, not the shared one |
| **A collection cached whole while its members are cached individually** | **permitted with conditions, and this is where `C-15`'s honest limit bite hardest.** Writing one member must invalidate the aggregate entry too, and the only place that obligation live is the catalog's *what invalidates it* field — **free prose no regenerate-and-diff compare against behaviour**, by `C-15`'s own admission. So the shape is legal and its correctness rest on a field this rule set already say is documentation |
| **A cached value holding another entry's key** | **permitted.** A dangling reference is a miss, and a miss is always correct under `C-4` read-through. Cost is a second load path per read, not a correctness exposure |
| **One cache shared by two deployables** | **banned** — grounds below |
| **A background warm or a scheduled refresh** | **banned by `C-4`** — a populate that is not the return of a loader on a read-through call is a bare write, whatever schedules it. **A loading library's refresh-on-access — `refreshAfterWrite` in Caffeine, the in-process library `caching-java` pick — reload from the loader when the entry is next read, so it is a read-through and stay legal**; a startup warm job and a `refresh(key)` called from a timer are not. **Named rather than described** cuz the distinction is between two methods on one type, and a repo told only *do not warm the cache in the background* cannot tell which of them it is holding |
| **A request-scoped memo** | **permitted, and it is a cache** — `C-1` say so, so it take a catalog entry like any other. Marked because *it is only a local map inside one request* is exactly the reading that skip the catalog, and then `C-13` never enumerate it |
| **A loader that read another service's API rather than the durable store** | **permitted with conditions, and nothing here state them.** `C-3` confine loader implementations to *the module that may depend on the durable-store client*, and an egress client is not that module — so the confinement rule need a second named module or the shape is unwritable by accident rather than by decision. **And the authoritative answer now live in a system whose freshness this repo cannot bound**, so the staleness ceiling `C-7` commit is a claim about somebody else's system |
| **A money amount in a cache** | **out of scope here as a shape, owned by `C-10`** — `money-storage`'s composite-shape table hand it to this skill, and `C-10` is where the float ban re-enter after field, column and wire |
| **A cached value used as an input to a money effect** | **banned, mirroring `money-storage`'s own replica verdict** — it permit reads from a replica or reporting store and **ban them as input to a money effect**, on staleness. A cache entry is the same exposure with a shorter and less predictable lag. Display and listing reads stay permitted. `C-5` reach the *loss* of the value; this is about its *age*, which `C-5` do not cover |
| **A row key inside a cache key** | **permitted, and governed by `C-6`** — the key is the loader's argument tuple and the row key is one argument. `primary-keys` hand this shape here from its own side, 2026-08-02 |
| **A negative entry that a later create must clear** | **permitted, and already gated** — `C-8` is opt-in per entry with its own shorter expiry, and its named integration test is this shape exactly: read a missing key, create it, read again, assert found |
| **A message payload or an outbox row in a cache** | **out of scope here, owned by published `async-handoff`.** `C-5` already ban the correctness-bearing half — no queue, no idempotency record |

### The one ban

**One cache shared by two deployables — banned.**

- *Ground.* `C-9` invalidate by delete **from the writing transaction's post-commit registration**, which exist inside one deployable. A second deployable reading the same entry have no delete path from the first one's writes, so its coherence **degrade silently to expiry-only** — the shape `C-9` reject as wrong-but-plausible by construction. And the interlocks below rest `C-11`'s whole shape-hash argument on *cache's writer and reader are one deployable*; sharing make that premise false while every check still report green.
- *Organisation fact it rest on.* Eighteen three-person teams, one engineer each, **no platform or operations role** — same fact *Start by not caching* rest on. A shared-cache coherence protocol across deployables is a thing somebody owns, and there is no somebody.
- *No panel.* Case written by this conversion. Nobody argued the other side.
- *Reopens when* invalidation is driven by the authoritative store's own change stream rather than by a caller's post-commit hook — then the delete path no longer live inside the writer, and the ground here disappear. That is a different design with its own rules, not a relaxation of these.

## Interlocks these rules must not break

- **`C-5` does not weaken the money observability rules.** `C-5` bans correctness-bearing *use* of cache, says nothing about forensic emission. `money` skill keeps telemetry disposable for correctness and load-bearing for reconstruction (`M-20`); that split must survive. **Never write a directive of the form "a rebuildable store carries no forensic or audit obligation."**
- **`C-4` and `C-7` must not be instantiated as incompatible APIs.** One read-through call carries expiry. Separate bare write taking expiry would give `C-7` host and destroy `C-4`.
- **`C-9`'s post-commit callback must not become a general-purpose hook, and this one has teeth.** Repo satisfying `C-9` with general `afterCommit(Runnable)` registration **defeats `E-5` in the published `async-handoff` skill entirely**: nothing at call site distinguishes "delete a cache key after commit" from "publish after commit", so one hook `C-9` needs becomes hole that skill's publish-confinement rule falls through. Make post-commit registration **named member of this adapter's port** — `invalidateAfterCommit(key)` — with no free-callback form, and ban any other post-commit registration in repo. Both skills state this from own side.
- **A delete-after-commit is correct here and is the wrong shape for a broker publish. Do not carry either verdict over to the other.** Lost cache delete leaves stale read bounded by staleness ceiling, self-heals. Lost publish is unbounded permanent absence, no self-healing path, nothing anywhere that can compare against message never produced. Same shape, opposite verdict; reason is bound. `E-5` in `async-handoff` carries same contrast from other direction, and its `E-20` inverts `C-11` for same class of reason — cache's writer and reader are one deployable, message's are not.
- **This skill says "derived-store premise"** for store rebuildable from authoritative store. Deliberately avoids "rebuildable-cache premise": that phrase already taken, for **telemetry's disposability**, by `java-backend-observability` skill, which states it as directive with live re-open trigger. Repo installing only this skill cannot see collision — why it is recorded rather than assumed visible — see [evidence.md](evidence.md).

## Markers, dates, and what they mean

**Every one of the sixteen directives above is convention, dated 2026-07-29, and that is ceiling on whole set rather than per-rule accident.** None survived three independent refutation votes against primary sources, because each is **design argument rather than execution result** — and research protocol these rules were written under downgrades those automatically. There is **no production use of this rule set anywhere.** Read as defensible, cheap, enforceable design that fails toward safety, not verified finding.

- **confirmed** — survived three independent refutation votes against independent sources, on stated date. **No directive here carries it.**
- **primary-source verified** — one researcher checked against primary source, no panel. No directive here carries it either.
- **convention** — defensible practice research did not or could not confirm from independent sources. All sixteen.

**Do not promote a marker here without a new research pass.** Confirmed material from 2026-07-29 pass is *tool* evidence, not rules: two tool facts behind `C-14`, three tool limits each forcing rule to be worded differently, and engine licence and release facts. All per-stack or per-engine, living in stack skill and in [evidence.md](evidence.md).

**The lapse rule.** These rules last dated for review by **2027-01-29**. Past that date every **confirmed** marker reads as **convention** until new pass re-dates it. Needs no maintainer action: read lapsed claim as written. Here it changes nothing, because nothing is confirmed.

**`enforceable-rules`' layer and composite-shape checks were run over this set on 2026-08-02; its predicate, enumeration and token-placement checks were not, and a blank is not coverage.** Neither run promote a marker — everything added is **convention, 2026-08-02, conversion-dated**, and weaker than the directives it derive from. What the layer check added sit beside `C-1`, `C-6`, `C-10` and `C-12`, each naming a language that directive's own checks do not read: configuration and the deployment for `C-1`, the engine's keyspace for `C-6`, the serializer's global configuration for `C-10`, a resilience library's declared fallback for `C-12`. **`C-1`'s is the one that widen the skill** — a response cache in a proxy or content-delivery network match this skill's predicate word for word and no directive reach it, so the description now fire on it and the gap is stated rather than left silent.

Passes, sources, full steelman for each rejected shape, wordings that must not be reintroduced, engine survey, and conditions that reopen a decision are in [evidence.md](evidence.md).