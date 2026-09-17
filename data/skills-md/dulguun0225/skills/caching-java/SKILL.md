---
name: caching-java
description: The Java checks that make the cache rules fail the build — which tool enforces each directive on Java, Spring Boot, ArchUnit, Error Prone, Jackson, Maven, JUnit, Testcontainers and Toxiproxy — plus the cache engine pick (Valkey, with Redis 7.4 through 7.8 banned by name), the one-time gate wiring, and the named gaps where this toolchain can host no check. ALWAYS load in a Java repo alongside the caching skill, before adding a cache, a memo, a loading cache, a caching annotation, an expiry, or a cache engine. Every check here except the engine pick is keyed to a directive id that lives in the caching skill.
---
# Cache discipline: the Java checks

**Install this skill with `caching`.** Every check keyed to directive id — `C-1` … `C-16` — and **all those ids live in `caching`, not here**. This skill name tool, add only Java-shaped part. No restate directive, its reason, or default it override. Read alongside, not instead.

**One directive here got no id — deliberate: engine pick.** Which cache engine repo run not rule in `caching` — its gates deployment-shaped, not language-shaped, and right answer vary *within* stack. So stated here as this skill own directive. Platform-neutral nine-candidate survey behind it live in `caching` skill own `evidence.md`.

**Stack.** Java as pinned in build, Spring Boot, ArchUnit, Error Prone, Jackson, Maven with failsafe, JUnit, jqwik, Testcontainers with Toxiproxy, Caffeine where want in-process cache.

**Start by not caching.** That instruction in `caching`, not decoration: no measured latency problem → right answer no cache. Next best: in-process cache, short expiry. Nothing below argue repo should have one.

## The engine pick

- **Shared cache engine, where needed, is Valkey, pinned by image digest.** Valkey BSD-3-Clause under Linux Foundation governance, guarantee compatibility with **Redis OSS 7.2 and every earlier open-source Redis version**, so existing Redis clients connect unchanged. **Guarantee no run forward:** RDB files from Redis CE 7.4+ not compatible — the one stated incompatibility, check before moving repo off newer Redis.
- **Redis 7.4 through 7.8 banned by name.** Those releases offer only the Redis Source Available License v2 (RSALv2) or the Server Side Public License v1 (SSPLv1), neither OSI-approved, so that line got **no licence-cost-free exit at all**.
- **Redis 8.0.1+ permitted only with plan decision recording which licence branch taken and who accepted.** From 8.0 licence tri-licence at recipient choice — RSALv2, SSPLv1, **or** the GNU Affero General Public License v3 (AGPLv3). **Ground is the choice, not the AGPL.** Running unmodified server as backing service no trigger AGPLv3 §13, and this design treat AGPLv3 as licence-cost-free elsewhere. What disqualify by default: two of three branches not OSI-approved, and somebody must make and record election — organisation with no legal function got nobody to run that analysis. Valkey got no such analysis to run.
- **On managed platform, engine = whichever managed cache that platform provide**, and licence question never reach repo.
- Licence and version facts checked 2026-07-29, in *Evidence and dates* below. **Re-check at adoption**, not on calendar.

*(Banned-dependency rule on client packages plus image-digest pin — off-the-shelf hosts; licence scan over dependency graph authored per repo.)*

## The seam

- **`C-1` — ArchUnit over cache adapter package.** Ban list must name clients for **the engine this repo actually run**, plus in-process libraries and Spring own cache abstraction. Redis-family-only list on Valkey repo = gate with hole, because Valkey clients separately named packages. (ArchUnit — off-the-shelf host; package allowlist and long-lived-bean field-type rule for hand-rolled-memo case authored per repo, **and that field-type rule need reviewed per-entry opt-out list** — see named gap below.)
- **`C-2` — ArchUnit, annotations banned by name.** `@Cacheable`, `@CachePut`, `@CacheEvict`, `@Caching`, and AOP aspects on domain code sit on repo runtime-silent-behaviour ban list, alongside any caching decorator wired behind domain interface. That ban list itself **executable ArchUnit test class, not prose**, with meta-test asserting every entry either enforced by named test or explicitly marked deferred with reason. (ArchUnit — off-the-shelf host; domain-interface predicate authored per repo.)
- **`C-3` — javac plus ArchUnit.** Loader port declared with two abstract members, so **lambda = compile error** and every loader named class the architecture test can place; loader implementations and database client confined to persistence package. **This wording forced by tool limit, not taste:** ArchUnit read bytecode, cannot follow lambda or method reference into body, so rule like "loader must query the database" unsound by construction — must not be written. (Javac plus ArchUnit — off-the-shelf hosts; port type this repo own.)

## What a cache may hold

- **`C-4`, `C-5` — one ArchUnit rule over port declared methods and parameter types.** Port got no bare write, no atomic primitive: no set-if-absent, no increment, no list or stream operation. With `C-1` making raw client unreachable, cache cannot become lock, counter, queue or idempotency record. **Idempotency record the money rules require in same transaction as money effect must not live in cache** — see `M-17` in `money-api` skill and `M-40` in `money-storage`. (ArchUnit — off-the-shelf host; predicate authored per repo.)

## Keys and tenancy

- **`C-6` — ArchUnit on factory and port signatures, plus two tests.** Key type got private constructor and one static factory per key family; no factory and no port method accept free-text parameter. Scope type got no public constructor, so request-context accessor its only source. **Do not write this as ban on string concatenation** — since Java 9 `+` on strings compile to `invokedynamic`, so bytecode rule got no operand to match. That claim challenged and unverified (see *Evidence and dates*), and rule not rest on it: unwritable signature hold either way.

  Two backstops not optional, because signature rule cannot decide the scope passed is *current caller* one: jqwik property test that distinct argument tuples render distinct keys — the injectivity `C-6` stated property follow from — and **two-tenant Testcontainers test per cached read path** seeding two tenants, warming as one, reading as other. Second one is outside oracle; property test only vary what its generator vary. (ArchUnit — off-the-shelf host, predicate per repo; property test and two-tenant test — bespoke.)

## Expiry

- **`C-7` — ArchUnit for construction confinement, JUnit test for ceiling.** Expiry type constructible only in catalog package, so no call site can pass one the lint never see; JUnit test over committed catalog assert every expiry at or below repo committed staleness ceiling. **Ceiling value is this repo call and must be machine-readable value in committed catalog** — test cannot read prose. (ArchUnit — off-the-shelf host; catalog test — bespoke.)
- **`C-8` — type design plus Testcontainers test per path**: read missing key, create it, read again, assert found. Loader return type distinguish value from absence, adapter drop absence by default. (Bespoke.)

## Coherence and invalidation

- **`C-9` — ArchUnit for confinement, Testcontainers rollback test, spec-and-review for residue.** Port invalidate operation reachable only from transaction seam post-commit callback. **Ordering enforced by confinement, not by test** — "rolled-back write leave nothing cached" and "committed write leave nothing stale" both satisfied by delete-before-commit implementation in sequential test, so naming only the test ship gate with blind spot.

  **Two interlocks this stack must get right.** First: post-commit registration is **named member of cache port** — `invalidateAfterCommit(key)` — with no free-callback form, and any other post-commit registration in repo banned; general `afterCommit(Runnable)` become the hole outbox-confinement rule fall through, and nothing at call site distinguish "delete cache key after commit" from "publish after commit". Second: **delete-after-commit correct here and wrong shape for broker publish** — lost delete = stale read bounded by ceiling, self-heal; lost publish = unbounded permanent absence. Do not carry either verdict over to other. **That rule set published**: `E-5` in `async-handoff`, Java confinement rule in `async-handoff-java`. Install in any repo that hand work off asynchronously, and wire named post-commit member before either rule can hold. (ArchUnit — off-the-shelf host, predicate per repo; rollback test — bespoke; residual ordering — spec and review.)

## Serialization

- **`C-10` — Error Prone on source, plus property test per cached type. This the one place this stack diverge from rule natural host, and reason is erasure.** Generics erase, so ArchUnit — reading bytecode — see cache port value type parameter as `Object` and report green while protecting nothing. Same erasure trap as unloggable-domain-type rule on this stack, where ArchUnit see logger erased `Object...` signature instead of argument static type. **`llm-default-traps` carry that case tool ban and erasure ground behind it, and domain-type rule the ban enforce live in `java-backend-observability`** — install it, repo on this stack want both; trap stated here too rather than left to pointer, because this rule must hold whether or not that skill installed. Concrete type known at **catalog registration site** and source-level checker see static types, so check go there. Stack with reified generics no have this divergence; structurally typed one have it worse. (Error Prone — off-the-shelf host, check authored per repo; plus serialize-then-compare property test per cached type — bespoke.)
- **`C-11` — Maven plugin plus Jackson configuration.** Plugin compute each cached value shape hash into committed file with `check` goal that diff it, so undiffed shape change fail build; Jackson configured strict — `FAIL_ON_UNKNOWN_PROPERTIES` and constructor-bound deserialization — as backstop where shape unchanged but meaning not. Hand-bumped version integer rejected: forgetting to bump it is exactly the failure this prevent. (Plugin — bespoke; Jackson configuration — off-the-shelf.)

## Failure behaviour

- **`C-12` — Error Prone `EmptyCatch` promoted to `ERROR`, Toxiproxy test per read-path class, spec-and-review for rest.** Toxiproxy test cut cache connection, assert either database answer or coded error. **Named gap, and it the important one here: swallowing catch invisible to this toolchain.** ArchUnit expose catch block caught type but not its body, and `EmptyCatch` no fire on `catch (e) { return
  Optional.empty(); }` — that block not empty. Wiring ArchUnit rule here report green over the case the rule exist to catch. General half stay spec and review, same shape and same reason as money rule on caught exceptions (`M-5`). (Error Prone — off-the-shelf, empty case only; Toxiproxy test — bespoke; general case — spec and review.)

## Evidence gates

- **`C-13` — three maven-failsafe executions**, test-scoped always-miss cache binding, Toxiproxy for fault arm. Normal and always-miss must produce identical observable results; under fault injection every answer either match cache-off answer or is coded error; normal run fail if any catalogued cache record zero hits. (Bespoke.)
- **`C-14` — hit and miss counters on port, asserted per configuration**, and fault arm assert injected fault was observed. **Two tool facts that make this separate rule rather than clause confirmed for this stack**: Spring `NoOpCacheManager` documented as accepting items and not storing them, so always-miss arm pass condition byte-identical to that arm never applied; and Testcontainers Toxiproxy module apply toxics imperatively with **no toxic-verification API and no assertion helper**. Spring Boot profile validation govern profile-name *pattern*, not whether profile exist or is used, so mis-named test profile raise nothing. Without this rule, bean override that no win make all three runs the normal run and gate report green over everything. (Bespoke.)
- **`C-15` — annotation processor or test generating catalog, with regenerate-and-diff in CI.** Machinery, not documentation: ceiling test read it (`C-7`), negative-caching opt-in read it (`C-8`), serialization check read it (`C-10`), three-configuration gate enumerate it (`C-13`, `C-14`). (Bespoke.)
- **`C-16` — Decision Trace line.** Plan or spec introducing first cache record that these rules bind it, at plan approval gate. (Convention — spec and review.)

## Wiring the gates

Run once per repo, in the PR that land first cache — not per cache change. Instructing agent do nothing for gate: **gate is what catch next agent**, and unwired gate is rule described as enforced that is not. **Ordering, and the record to commit after: [gates.md](gates.md).**

## Named gaps — where this stack can host no check

Silence read as coverage, so each stated.

1. **"Loader reads the authoritative store" not decidable.** Confinement make banned *shape* uncompilable and put loaders where database client is only reachable data source. It no decide semantics.
2. **Swallowing catch invisible** (`C-12`). Spec and review.
3. **Engine-side eviction invisible to every check in this build** (`C-7`). Nothing in Java toolchain read cache server memory policy, so "has an expiry" not "lives until its expiry".
4. **Three-configuration gate coverage-shaped** (`C-13`). Prove recomputability only for paths the suite drive. Green run not proof.
5. **Hand-rolled-memo half of seam rule partly undecidable** (`C-1`). Dependency ban catch library case completely; field-type rule over long-lived beans catch plain-map case **over-broadly** and need reviewed opt-out list — hole an agent can widen. **Unmeasured:** nobody wired it and counted how many legitimate entries that list need. If number large, rule not carry its weight, and honest move is name the gap instead of keep the rule.
6. **Property-test library carry version trap, and its pin not a rule here.** `C-6` and `C-10` both name jqwik property tests. That library version pin is **cross-cutting dependency rule rather than cache rule** — bind every use of library in repo — so not stated as cache check. **`llm-default-traps` own it**, with ceiling version, incident behind it and CI version-ceiling check; value **deliberately not repeated here, because pin stated in four skills drift in three.** That skill bind every agent-built repo regardless of stack, so not optional companion — **install it in any repo that install these.** Repo that no install got no pin from any skill here and must decide at its own dependency review.

7. **The four second languages `caching`'s layer check named on 2026-08-02, and what this stack can host for each.** That skill added a clause beside `C-1`, `C-6`, `C-10` and `C-12` naming a language those directives' own checks do not read. Stated here because a check kind with no tool is a wish, and three of these four have no tool on this stack.
   - **`C-1`, a cache declared in configuration or in the deployment.** Framework cache manager configured in `application.yml` rather than written at a call site is **partly covered here already**: banned-dependency rule catch the starter and the client on the classpath, and `C-2`'s ArchUnit list ban Spring own cache abstraction. **Response cache in a reverse proxy or content-delivery network is covered by nothing** — no Java tool read a deployment manifest, and `Cache-Control` this service emit is a header value, not a type dependency. Lint over committed manifests and over the OpenAPI document header declarations would host it; **not wired, and no repo here has one.**
   - **`C-6`, the rendered key against the engine keyspace.** No host. Reachable cheaply as a **JUnit assertion over the committed catalog** — render one key per entry from fixture arguments, assert length and charset against the engine actually deployed. Bespoke, small, and nobody has written it.
   - **`C-10`, the serializer own global configuration.** No host that read it as configuration. What this stack have is the **per-type property test already required**, which catch a global Jackson change for every type that have one — so the gap is exactly the set of cached types with no property test, and that set is enumerable from the committed catalog.
   - **`C-12`, a resilience library declared fallback.** **This one have a host and it is already in this stack**: the ban-list ArchUnit test class `C-2` require. A Resilience4j `@CircuitBreaker(fallbackMethod = …)` or `@Bulkhead` on a cache read path is an annotation, matchable exactly as `@Cacheable` is, and **it is not on the list today.** Add it by name; the fallback is the corpus first answer to "handle a cache error" and it return a substituted value with no catch block anywhere.

**Not measured, and it a real number for three-person team:** running integration suite in three configurations **triple integration CI time**. No repo has run it.

**In-process libraries — one checked, rest not.** Caffeine 3.2.4 (2026-05-03, Apache-2.0, last push 2026-07-28) verified from its own release API. **Guava cache and every other in-process library not** — no licence, version or API-surface check. Rules ban them *outside* the seam, which need no such check; repo that permit one *inside* the seam do that evaluation itself.

## Markers, dates, and what they mean

**Nothing in `C-1` … `C-16` confirmed** — all sixteen convention. What confirmed for this stack is tool, licence and price evidence, and none of it promote a directive.

**Review by 2027-01-29.** Past that date every **confirmed** marker read as **convention** until new pass re-date it. Version pins and prices age fastest — re-check Valkey, Redis, Caffeine and managed pricing at adoption, not on calendar.

Ground behind each Java and engine claim, with its source and date, the managed-cache prices, one recorded contradiction between sources, and what must **not** be cited, one hop away in **[evidence.md](evidence.md)**. Platform-neutral evidence — nine-candidate engine survey, steelman per rejected shape, reopen conditions — in `caching` skill own `evidence.md`.
