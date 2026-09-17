---
name: async-handoff-java
description: The Java checks that make the asynchronous-handoff rules fail the build — which tool enforces each directive on Java, Spring Boot, Spring for Apache Kafka, ArchUnit, Error Prone, Jackson, jOOQ, Flyway, Maven, JUnit, jqwik, Testcontainers and Toxiproxy — plus the broker pick (Apache Kafka in KRaft mode, with Redpanda and AutoMQ banned by name), the outbox-library pick, the one-time gate wiring, and the named gaps where this toolchain can host no check. ALWAYS load in a Java repo alongside the async-handoff skill, before publishing a message, adding a queue or broker client, an in-process event bus, an executor submit, an @Async or @Scheduled task, a polled table, or an outbound webhook. Every check here except the broker and outbox picks is keyed to a directive id that lives in async-handoff; the composite-shape checks are in shapes.md.
---
# Asynchronous-handoff discipline: the Java checks

**Install this skill with `async-handoff`.** Every check below keyed to directive
id — `E-1` … `E-28`, `E-32`, `E-33` — and **every one of those ids live in
`async-handoff`, not here**. This skill name tool, add only Java-shaped part. No
restate directive, its reasoning, or default it override. Read alongside, not
instead.

**Composite-shape checks in [shapes.md](shapes.md)** — `E-29` … `E-31`,
`E-34` … `E-36`, directives live in `async-handoff-shapes`. Read that file when
flow commit in more than one transaction, when webhook cross org boundary, or
when payload cannot meet size limit.

**Two directives here got no id. Deliberate: broker pick and outbox-library
pick.** Which transport repo run, and whether relay hand-written — not rules in
`async-handoff`. Their gates deployment-shaped, not language-shaped, and right
answers vary *within* stack. So stated here, as this skill own directives.
**Contrast money skills, where every `money-java` entry keyed to `M-n`:** reader
who assume that invariant hold everywhere go hunt missing directive.
Platform-neutral nine-candidate transport survey behind broker pick live in
`async-handoff` skill own `evidence.md`.

**Stack.** Java as pinned in build, Spring Boot, Spring for Apache Kafka,
ArchUnit, Error Prone, Jackson, jOOQ, Flyway, Maven with failsafe, JUnit, jqwik,
Testcontainers with Toxiproxy, PostgreSQL for outbox and dedup record.

**Version pairing these checks assume, read from Spring Boot dependency manifest
2026-07-29:** Boot 4.1.0 manage spring-kafka 4.1.0, kafka-clients 4.2.1,
jOOQ 3.21.5, Testcontainers 2.0.5. ArchUnit 1.4.2 (2026-04-18). **Pin gates to
these, re-check at adoption.**

**First ask: must work leave caller control flow?** Note one consequence of
broker pick below, easy to miss: **until named cluster owner exist, this service
got no compliant async path. Correct response: keep work synchronous, no
improvise transport.**

## The broker pick

- **Self-hosted broker = Apache Kafka in KRaft mode, pinned by image digest, and
  named person own cluster, its upgrade calendar, its metadata version. Owner is
  prerequisite, not condition.** Kafka Apache-2.0 under foundation governance,
  only candidate that both replayable log *and* work queue with per-message ack
  while hold no feature back — every security mechanism ship free, where two
  rivals put role-based access control behind licence key. Documented minimum:
  three or more controllers. Only route to three total nodes is combined mode,
  which its own docs call not recommended for critical deployments; **metadata
  downgrade out of 4.3 unsupported, so finalising upgrade is one-way door.** On
  Kubernetes, Strimzi carry that load.
- **Off Kubernetes, substitute = NATS JetStream at three replicas** —
  Apache-2.0, one static binary, no external dependency, smallest operational
  surface of any candidate. That why it substitute where named owner got least
  time to give. **It no remove ownership requirement.** Configure against two
  documented traps: file-sync interval default **two minutes**, and its own docs
  say OS failure in non-replicated setup may lose data; storage directory
  default to path under `/tmp`. Single-replica stream got no recovery path but
  backup.
- **Redpanda banned by name:** source-available under business source licence,
  not OSI open source; its additional-use grant exclude offering queuing
  service; role-based access control and identity-provider auth licence-gated.
- **AutoMQ banned by name:** Apache-2.0, but make object store you also operate
  mandatory, and its low-latency write-ahead log plus **its metrics export are
  enterprise features** — broker whose metrics export paid cannot join `E-9` or
  `E-16` alerts.
- **RabbitMQ permitted only where strict message priority is stated
  requirement** — only licence-cost-free candidate that got it — and then plan
  record that community support run roughly four months per minor series, that
  upgrades strictly one series at a time, and that Erlang pinned to single major
  version. **Erlang pin = second runtime to track in JVM shop that already track
  one.**
- **On managed platform, transport = that platform own queue or
  publish-subscribe service, never managed Kafka, unless retained log is stated
  requirement.** Deciding number is billing floor, not message rate:
  queue-shaped and pub-sub services carry no minimum fee plus standing monthly
  free allowance, while every cluster-shaped managed service priced per
  cluster-hour, so idle cluster cost hundreds of dollars a month and floor
  dominate low-volume bill. **One shared cluster across teams is not escape** —
  it create component no role in this org own.
- Three grounds Java-shaped, belong here not in neutral survey: **Kafka JVM
  heap, GC and page-cache tuning is skill no role in this org hold**; its 4.0
  upgrade mechanism removed `inter.broker.protocol.version` in favour of
  `metadata.version` via `kafka-features.sh`, so **agent writing operational
  tooling from corpus memory produce config key broker reject**; and two bans
  above are Java-ecosystem form of licence findings.
- Versions, licences, support windows checked 2026-07-29. **Re-check at
  adoption**, not on calendar. Prices move too, and expect at least one vendor
  pricing page render client-side and yield no figure at all.

*(Banned-dependency rules on client packages plus image-digest pin —
off-the-shelf hosts; licence scan over dependency graph authored per repo.
Managed-platform pick is plan decision — convention, spec and review.)*

## The outbox and relay pick

- **Outbox and its relay not hand-rolled unless plan say why.** Three Apache-2.0
  libraries on this stack write outbox row in caller transaction and need
  nothing beyond PostgreSQL: **gruelbox transaction-outbox 7.0.707**, got
  first-class jOOQ module, README state polling loop "is up to you" — so relay
  lifecycle is bespoke residue; **namastack-outbox 1.8.0**, automatic schema
  creation; and **Spring Modulith event publication registry 2.1.0**, which
  write log entry "as part of the original business transaction" with
  republication on restart opt-in — **its broker-externalization module not
  verified.** `raedbh/spring-outbox` got no releases, not recommended.
- **Change-data-capture route is different trade, rejected by default.**
  Debezium 3.6.0.Final Apache-2.0, but its outbox router is Kafka Connect
  single-message transformation, so it need Connect cluster or standalone
  server, logical replication, replication slot, and **connector config that
  live outside this build where no Maven gate can read it.** For team with no
  operations role, that second always-on system on top of broker.
- **Match that router expected outbox columns in first migration anyway** —
  aggregate id, aggregate type, payload, timestamp, event type. Cost nothing
  now, and make swapping hand-written relay for connector, or back, config
  change not rewrite. **Use standard event envelope for every payload, same
  reason:** transport most likely thing to change, payload shape should not have
  to.
- **PostgreSQL queue extension not a Java option, and usual objection to it
  wrong.** Its control file set `superuser = false`, so superuser claim false.
  Real barriers: host filesystem access to place extension files — its own docs
  mark managed-cloud support limited — and provider allowlisting, and it
  **absent from AWS RDS supported-extensions list** for every version checked.
  Raw-SQL install work on managed service but unversioned, no upgrade path. No
  first-party Java client: of three third-party JVM clients, one not on Maven
  Central, others last touched 2024.
- Versions checked 2026-07-29.

*(Convention — plan decision. Banned-dependency rule for change-data-capture
path off-the-shelf; envelope is bespoke schema lint over committed schema
files.)*

## The seam

- **`E-1` — ArchUnit over committed async-capable type list, plus
  dependency-manifest check.** List name broker and queue clients, in-process
  event buses, `ExecutorService` submits, `CompletableFuture.supplyAsync`,
  `Thread.startVirtualThread`, `@Async`, `@Scheduled`, reactive subscribe
  operators; no class outside adapter package may reference one. **List is
  allow-list, so construct nobody thought of is missing entry not silent pass**,
  and list file reviewed like code. New dependency matching committed transport
  pattern fail build until catalog entry exist. (ArchUnit plus
  dependency-manifest check — off-the-shelf hosts; list, predicates, and
  long-lived-bean field-type rule for hand-rolled cases authored per repo.)
- **`E-2` — ArchUnit on methods *and* classes, plus generated subscription
  list.** Spring document both binding paths — reference state messages can be
  received "by configuring a `MessageListenerContainer` and providing a message
  listener or by using the `@KafkaListener` annotation", with container,
  container-properties, factory and endpoint-registry types all present — **so
  annotation ban got supported replacement, not demand to hand-roll poll loop.**
  That fact is what directive depend on.

  **Divergence, and this the one to get right: rule must cover meta-annotated
  and class-level forms.** `@KafkaListener` `@Target` include annotation types
  and classes as well as methods, so repo can wrap it in own annotation and
  **methods-only, direct-annotation rule report green while banned thing pass.**
  Use both annotated and meta-annotated predicates. (ArchUnit — off-the-shelf
  host, predicates per repo; annotation processor or test generating
  subscription list with regenerate-and-diff — bespoke.)
- **`E-3` — javac plus ArchUnit.** Handler port declared with two abstract
  members, so **lambda is compile error** and every handler is named class
  architecture test can place; implementations confined to package permitted to
  depend on domain services. **This wording forced by tool limit, not chosen for
  taste:** ArchUnit read bytecode, cannot follow lambda into its body. Second
  member also matter for `E-2`: lambda handler unnameable in generated list, so
  diff produce rows nobody can act on. (Javac plus ArchUnit — off-the-shelf
  hosts; port type is this repo own.)
- **`E-4` — banned-dependency rule plus `E-1` allow-list plus outbox-read
  confinement rule.** In-process event bus — including Spring own application
  event publisher used as handoff — banned by dependency; reads of outbox table
  confined by ArchUnit to relay package, **which is what make "table is not a
  transport" checkable not merely stated.** (ArchUnit — off-the-shelf host,
  predicates per repo.)

## The write path

- **`E-5` — ArchUnit for confinement, plus config assertion.** Publish call
  reachable only from relay package; producer ack and durability settings
  asserted as committed values, not relied on as defaults. **Nothing off shelf
  detect publish inside transactional method** — see *Static analysis* below —
  so confinement rule is whole gate and its predicate is this repo own.
  (ArchUnit — off-the-shelf host, predicate per repo; config assertion —
  bespoke. **Named gap:** broker-side durability, replica counts, minimum
  in-sync replicas invisible to every check in this build.)

  **One off-the-shelf rule exist, worth wiring:** Error Prone
  `FutureReturnValueIgnored` fire on bare `kafkaTemplate.send(...)`, because
  template return `CompletableFuture<SendResult<K,V>>` and carry **no**
  `@CanIgnoreReturnValue`. It `WARNING` by default and **must be raised to
  `ERROR` to gate build.** Two limits: idiomatic fix — chaining `whenComplete` —
  return another future and fire again, so expect noise; and variable named with
  tool `unused` prefix silence it, **which agent will find.**
- **`E-6` — javac and ArchUnit on port signature, plus two Testcontainers tests.
  Do not try to check this with ArchUnit.** Whether transaction active at call
  site depend on which callers reach it, on whether call arrived through Spring
  proxy at all — self-invocation bypass it, identical bytecode, opposite runtime
  answer — on propagation of every intermediate frame, and on which data source
  in play, since requirement is *the same* transaction and two transaction
  managers both satisfy "a transaction is active". Rule written there report
  green over exactly the case it exist to catch.

  **Divergence: handle cannot be jOOQ own.** `transaction()` hand back
  *derived* `Configuration` and manual warn that using outer scope inside block
  will "silently run outside the transaction" — but **both same static type**,
  so no compiler, processor or bytecode reader distinguish them, and
  `jooq-checker` (3.21.6) ship only dialect checker and plain-SQL checker.
  Spring offer strictly less: transaction thread-bound and ambient. So repo own
  wrapper handle type, compiler discharge obligation at call site, and
  **rollback test is thing that actually decide property.** (Javac plus ArchUnit
  on port signature and its referencing packages — off-the-shelf hosts, type is
  this repo own; two Testcontainers tests — roll business transaction back after
  append and assert no outbox row and no published message, and kill process
  after commit and before relay, restart, assert message published and
  observably once — bespoke. One data source and one transaction manager is
  committed config fact, not type fact: assert it.)
- **`E-7` — javac and ArchUnit for type and package ban, Flyway constraint,
  jqwik property test, golden re-derivation test.** Identity type got private
  constructor and one static factory per strategy; no clock or random source
  reachable from factory package; column `NOT NULL UNIQUE` in committed
  migration; golden test re-derive every identity in committed corpus from its
  payload. **Unique constraint alone is wrong check** — random value assigned at
  row-write time satisfy not-null, unique, and "not generated at publish time" —
  so re-derivation test is half that matter. (Javac and ArchUnit —
  off-the-shelf hosts; migration constraint, property test, golden test —
  bespoke.)
- **`E-8` — ArchUnit for confinement, `FOR UPDATE SKIP LOCKED` in claim query,
  Testcontainers kill test.** Relay claim rows at partition-key granularity
  inside transaction, publish before marking sent, never delete unsent row, and
  its concurrency and retention window are committed values. Claim query and its
  key granularity are this repo own. (ArchUnit — off-the-shelf host; claim query
  plus Testcontainers test that kill relay between publish and mark-sent and
  assert one observable effect — bespoke.)
- **`E-9` — Prometheus rules with `promtool` fire-tests, plus Testcontainers
  outage test.** Two alerts: outbox depth above committed threshold, and **age
  of oldest unpublished row**, most important signal in this design and one
  every consumer-side alert blind to. Test hold transport down past threshold
  and assert alert fired and no business transaction blocked. (`promtool` —
  off-the-shelf host, fixtures per repo; outage test — bespoke.)

## The consume path

- **`E-10` — config assertion on **two** settings, javac for void port, and
  ArchUnit to keep acknowledgement type out of handler packages. Two settings
  must be pinned, not one, and this the finding most likely missed.** Spring
  listener ack mode default to **`BATCH`, not `RECORD`** — it commit offsets of
  all records from previous poll once all processed, so crash after record three
  of fifty redeliver all fifty, and reasoning about "at-least-once per record"
  is wrong about the **unit**. And **share-consumer ack mode added in 4.1 got
  implicit value under which broker acknowledge every record regardless of
  processing outcome, no listener involvement**, so rule inspecting only
  listener mode green over it. Pin both, in shape of config-default assertion.
  (Config assertions — bespoke; javac for void port and ArchUnit for type ban —
  off-the-shelf hosts.)

  **Named gap: catch that swallow by returning default stay invisible to this
  toolchain** — ArchUnit expose catch block caught type but not its body, and
  Error Prone `EmptyCatch` no fire on block that return value. Same gap, same
  reason money rules (`M-5`) and cache rules (`C-12`) record. Spec and review.
- **`E-11` — sealed exception hierarchy plus rule on catch.** Terminal and
  retryable are sealed types, so no third option compile; `catch` in handler
  package must rethrow one of them, which is Error Prone or ArchUnit rule
  authored per repo. **Do not implement terminal classification as marker
  interface on broad exception type** — if any exception can be re-tagged
  terminal at catch site outside handler, `E-16` attempt budget stop being
  bound. (Sealed hierarchy — off-the-shelf via javac; catch rule — bespoke.)
- **`E-12` — JUnit test over committed catalog and configuration, plus ArchUnit
  on handler packages.** Test assert budget at or below lease, and batch size
  times per-item budget at or below budget; ArchUnit ban sleep, unbounded wait,
  un-timed outbound calls in handler packages. **Arithmetic not hypothetical:**
  `max.poll.records` default **500** against `max.poll.interval.ms` of
  **300000**, so per-record work above roughly **600 ms** guarantee redelivery
  loop. (Both hosts off-the-shelf, predicates per repo. **Named gap:** handler
  that ignore interruption still overrun.)
- **`E-13` — ArchUnit on transitive dependencies of effect-free port package,
  plus Testcontainers duplicate test and jqwik property test.** Effect-free port
  package may not depend, transitively, on any repository, outbox, publish port,
  outbound client or file-write API — **so it got no way to have effect.**
  Deduplicated port effect operation take message identity and write dedup row
  in same transaction, in this service PostgreSQL — **never in cache, never in
  map field, never in broker.** Idempotency record `M-17` require in money
  effect own transaction is this same record, and `C-5` in published `caching`
  skill already ban it from cache. (ArchUnit — off-the-shelf host, predicate per
  repo; Testcontainers test delivering one message twice and asserting one
  effect, plus jqwik property test that dedup key is function of identity alone
  — bespoke. **Named gap:** whether two *distinct* messages denote one effect is
  semantic.)
- **`E-14` — JUnit test over committed catalog.** It compare committed dedup
  retention against committed lease, attempt limit and redrive window on one
  side, committed upper bound on other. (Bespoke. **Named gap:** operands are
  this repo declarations of broker-side retention, which can be lie.)

## Ordering

- **`E-15` — javac and ArchUnit on factory and port signatures, cross-field
  JUnit test over catalog, and Testcontainers out-of-sequence test per ordered
  subscription.** Key type got private constructor and one factory per family;
  no factory and no port method accept `String`. **Ground no-free-text clause on
  unwritability, not on bytecode** — factory that cannot take `String` make
  wrong call uncompilable, which hold regardless of how compiler emit string
  concatenation, and bytecode argument cache rules once used for their key rule
  is challenged and unverified (see *Evidence and dates*).

  **`@RetryableTopic` permitted only on `unordered` subscriptions**, because its
  own docs state "By using this strategy you lose Kafka's ordering guarantees
  for that topic". Also documented as unsupported with batch listeners and
  unable to combine with container transactions. (Javac and ArchUnit —
  off-the-shelf hosts, predicates per repo; cross-field catalog test and
  out-of-sequence Testcontainers test — bespoke. **Named gap:** that handler
  assume order *across* keys not decidable.)

## Poison messages and retries

- **`E-16` — JUnit test over committed catalog, `promtool` fire-tests for both
  alerts, Testcontainers exhaustion test.** Five fields are committed catalog
  row; test assert none declare unlimited attempts or drop, and that every
  backoff got non-zero minimum interval. **That last clause exist because of
  specific default:** Spring `DefaultErrorHandler` bounded and tight-looping —
  ten total attempts with `FixedBackOff(0, 9)`, **zero-millisecond** interval —
  so "retries are bounded" and "a backoff is configured" **both pass on
  zero-delay ten-times hammer.**

  **And silent drop is platform default on queue-shaped broker, with log-shaped
  one asserted rather than sourced.** RabbitMQ drop message past its delivery
  limit unless dead-letter exchange configured — that half primary-source
  verified, in `async-handoff` skill own `evidence.md`. Claim that Kafka share
  groups move record to archived state past delivery-attempt limit, where it not
  eligible for further delivery and routed nowhere, is **this pass own assertion
  with no primary-source citation recorded** (see table below). Directive no
  turn on it — `E-16` ban `drop` declaration and unlimited attempts on every
  shape — so **do not cite it as documented behaviour; read share-group docs
  before relying on it.** (Catalog test and `promtool` — off-the-shelf hosts,
  fixtures per repo; exhaustion test — bespoke.)
- **`E-17` — ArchUnit plus catalog test, plus Testcontainers assertions on
  destination and its partition.** ArchUnit ban sleep and park primitives in
  handler packages; catalog test compare terminal destination retention against
  its source and assert shape-conditional policy.

  **Assert dead-letter topic partition count as well as its name.**
  `DeadLetterPublishingRecoverer` **no create its destination and no fail loudly
  when it missing**: default destination is source topic suffixed `-dlt` on same
  partition number, its partition check log unknown topic at **DEBUG** and
  missing partition at **WARN** before letting producer choose one. So test
  asserting "the failed record reached the dead-letter topic, partition N"
  **must assert partition and must not rely on recoverer to fail.** (ArchUnit
  and catalog test — off-the-shelf hosts; Testcontainers assertions — bespoke.
  **Weakest clause:** that redrive was run from console rather than committed
  operation not visible to this build — spec and review.)

## The payload as a published contract

- **`E-18` — generator bound to build with `check` goal, plus ArchUnit on port
  parameter type.** Payload classes generated from committed schemas, generated
  code committed, `check` goal diff it. (Generator — bespoke; ArchUnit —
  off-the-shelf host.)
- **`E-19` — build-failing compatibility check over committed history directory,
  and one apparent host must be refused by name.**

  **Divergence: AsyncAPI route got no build-failing Java host.** Only Java Maven
  AsyncAPI comparator **detect incompatibilities then pass build** — its plugin
  declare three parameters, never throw build-failing exception, write report
  file, exit green regardless; its repository got one published version, two
  stars, no commit since 2024. **That false-green gate shipped as product, and
  signature above is what repo match it against — this pass recorded shape not
  artifact coordinates, so no name printed here and none should be inferred.**
  Usable routes: AsyncAPI **CLI** `diff` command, which do fail on breaking
  changes against committed file with no network unless opt-out flag passed but
  is Node binary invoked through exec plugin; or **`buf
  breaking`** for Protobuf, which compare against committed baseline including
  git ref, need no network, Apache-2.0.

  **And no tool on JVM validate actual published message against committed
  AsyncAPI document** — official parsers are JavaScript and Go, and payload
  validators are Node, Python and TypeScript and cover payloads only, never
  headers or channel names.

  **Corpus-favourite schema registry not usable in self-hosted variant:** its
  own licence file put project under Confluent Community License "except some
  modules such as the client-* and avro-* libs, which are licensed under the
  Apache 2.0 license", so not OSI open source. **Apicurio Registry 3.3.1 and
  Karapace 6.2.1 are Apache-2.0**; whether either drop-in for given client
  **not verified**. Facts checked 2026-07-29. (Build-failing compatibility check
  over committed history — bespoke host, off-the-shelf checker. **Named gap:**
  checker decide shape and never meaning, so redefining amount from gross to net
  pass every level — spec and review at plan gate.)
- **`E-20` — Jackson configuration assertion plus parse test over committed
  corpus.** Configure it in adapter only, as committed values: **fail on missing
  creator properties, do not fail on unknown properties, bind through
  constructors** so missing field cannot be defaulted after construction. Parse
  test cover malformed, truncated, missing-field, extra-field payloads.
  Unknown-field meter and its alert rule are Micrometer plus Prometheus rule.
  **Note that "counted and alerted" with no threshold and no owner is
  structurally the catch-log-continue `E-10` ban.** (Jackson assertion and meter
  — off-the-shelf; parse test — bespoke.)
- **`E-21` — bespoke schema lint plus parse test plus ArchUnit for dereference
  ban.** Lint read committed schema files for every content ban; parse test
  cover unrecognised enumeration value; ArchUnit enforce that handler package
  may not depend on outbound client for service it consume from. **Float ban
  unqualified**, with any exception listed explicitly rather than scoped to
  "money fields", for reason `M-2` give — and **this the float ban fifth
  layer**, after field (`M-2`), wire (`M-12`), column (`M-10`) and cached value
  (`C-10`). **And do not log message payload to make consumer debuggable:** it
  copy personal data into log store with its own longer retention and its own
  access control, and that copy is what survive after destination retention
  expire. (Schema lint and parse test — bespoke; ArchUnit — off-the-shelf host.
  **Named gap:** personal data not decidable without type-level classification
  regime — same gap cache rules record.)

## Tenancy and replay

- **`E-22` — javac and ArchUnit, plus two-tenant Testcontainers test per
  subscription.** Nominal data-scope type with no public constructor;
  authorized-actor type whose constructor unreachable from handler packages, so
  **privileged call no compile there**; ArchUnit ban request-context accessor
  and any ambient scope holder in handler packages. Two-tenant test seed two
  tenants and assert each effect land in its own scope. **That test is outside
  oracle: its ground truth is database, not assertion written by model that
  wrote handler.** (Javac and ArchUnit — off-the-shelf hosts, predicates per
  repo; two-tenant test — bespoke.)
- **`E-23` — ArchUnit on handler packages plus double-pass replay test.**
  ArchUnit ban clock and random sources in `replay-safe` packages; replay test
  process committed message corpus twice and assert second pass produce no
  additional observable effect. **State exemption or this contradict three other
  checks:** what banned is reading clock as value that reach effect or payload —
  expiry windows and telemetry timestamps computed inside dedup and telemetry
  adapters, which handler call without reading time itself. (ArchUnit —
  off-the-shelf host, predicate per repo; replay test — bespoke. **Named gap:**
  "the handler is a total function of the message" not decidable; these
  proxies.)

## Evidence gates

- **`E-24` — four maven-failsafe executions against Testcontainers broker**,
  with test-scoped duplicating and reordering harness and Toxiproxy for fault
  arm. Arms split by ordering declaration, per directive.

  **`EmbeddedKafkaBroker` not deprecated and docs record no divergence from real
  broker** — `testing.adoc` contain zero occurrences of "testcontainer", and
  since 4.0 only KRaft implementation exist. **So "prefer Testcontainers because
  the embedded broker diverges" is bet, not citation, and must not be written as
  one.** Documented caveats operational: no shutdown mechanism when tests
  finish, do not mix global embedded broker with per-class ones, use distinct
  topic per test. Containers still default here because fault and
  multi-instance arms need real network surface — state that as reason.
  (Bespoke.)
- **`E-25` — counters on adapter asserted per configuration, `promtool`
  fire-tests, and one violating fixture per ArchUnit rule.** Hit, duplicate,
  reorder and fault counters carry positive controls; normal arm fail if any
  subscription **in committed catalog** processed zero messages.

  **Three tool facts make each clause necessary not defensive, and their markers
  differ — read them as marked, not as one block.** Two of three **confirmed**
  by cache rules pass, which ran three refutation votes this pass did not:
  Toxiproxy limit and no-op cache manager, both carried with that marker in
  `caching-java`. `failOnEmptyShould` finding is this pass own and
  **primary-source verified, not confirmed** — see table below. Toxiproxy module
  confirm nothing about itself — its client expose only name, stream, toxicity
  and remove, no counter, no bytes-affected, no fired flag — **and toxicity is
  probability**, so registered toxic can legitimately not affect call under
  test; chaos test asserting only "the toxic was added and the call succeeded"
  cannot distinguish tolerance from fault that never arrived. **ArchUnit reject
  empty should-clause by default** (since 0.23.0) **but guard one line from
  being disabled** — property or per-rule override, neither visible in passing
  build log — and it no cover importer pointed at wrong path; **this finding not
  broker-specific and apply to every ArchUnit gate in this repo.** And no-op
  cache manager byte-identical to its binding never having been applied, same
  shape cache rules record. (Bespoke.)

## The catalog, the topology, and the plan

- **`E-26` — one Java `record` with every component required, plus annotation
  processor or test generating catalog with regenerate-and-diff.** Record with
  no defaults and no builder is what make ~twenty fields per subscription exist
  at registration site at all; **without it catalog generated in part and
  hand-maintained in part, and diff cannot tell which half drifted.** (Record —
  off-the-shelf via javac; generator — bespoke. **Named gap:** owning-team field
  is prose no diff can check against behaviour, **and catalog is repo-local** —
  cross-repository union check got no host on this stack.)
- **`E-27` — bespoke schema lint over committed topology file**, with
  partition-count change behind review gate. (Lint — bespoke; review gate — spec
  and review.)
- **`E-28` — Decision Trace line.** Plan or spec introducing first async handoff
  record that these rules bind it, and name destination, its catalog row,
  ordering declaration, and every team expected to consume it, at plan approval
  gate. (Convention — spec and review.)

## The two bans

- **`E-32` — ArchUnit banned dependencies by group id, plus query-package
  rule.** Event-store and event-sourcing framework clients banned from committed
  group-id list, and no query or read-model package may depend on messaging
  adapter or on outbox tables.

  **Both banned architectures got first-class Java presence, which exactly why
  ban has to be dependency rule.** Axon is JVM-native event-sourcing framework
  whose **Framework is Apache-2.0 while its Server is not** — agent reading
  "Axon is open source" reading something true about wrong artifact — and
  EventStoreDB moved to Event Store License v2 with its 24.10 release, where
  enterprise features need licence key. Licences checked 2026-07-29; re-check at
  adoption. (ArchUnit — off-the-shelf hosts. **Named gap:** whether projection
  being treated as authority is semantic and unreachable; decidable half is
  dependency direction.)
- **`E-33` — ArchUnit banned dependencies plus ArchUnit field rules plus
  two-instance Testcontainers arm.** Kafka Streams, framework Kafka Streams
  binder, and other stream-processing libraries banned by dependency — **Kafka
  Streams ship in same ecosystem as client repo legitimately need, so it one
  dependency line away at all times.** Field rules — no non-final field and no
  static collection in handler or flow packages — catch hand-rolled version,
  which is what get written once dependency banned. Two-instance arm run second
  consumer container and assert same aggregate query answer identically however
  messages split. Documentation checked 2026-07-29. (ArchUnit — off-the-shelf;
  two-instance arm — bespoke. **Named gap:** wrong window committed as parameter
  pass every check; committed parameter is what put it in diff.)

## Static analysis — one usable rule, and a documented absence

Sweep of Error Prone, SpotBugs, all 714 sonar-java rules, PMD, fb-contrib,
find-sec-bugs and error-prone-support, 2026-07-29:

- **One off-the-shelf rule exist, worth wiring:** Error Prone
  `FutureReturnValueIgnored`, on bare `kafkaTemplate.send(...)`. `WARNING` by
  default, so **promote to `ERROR`**. Two limits, both recorded above under
  `E-5`.
- **Nothing exist for three rules that matter most.** No rule in any of those
  indexes detect publish inside transactional method, consumer acknowledging
  before handling, or unbounded retry; **`acknowledg*` return zero hits across
  every index.** Nearest transaction rules concern self-invocation, non-public
  proxied methods, rollback-for declarations, and **none reason about what
  transactional method call out to.** So `E-5`, `E-6`, `E-10` and `E-16` are
  **bespoke on this stack** — fact about toolchain, not weakness of rules, and
  why their evidence is test not lint.
- **Not searched, absence not claimed for them:** Semgrep, CodeQL, commercial
  analysers. "Publish inside `@Transactional`" pattern plausible in either and
  **would be cheapest upgrade available** — recorded as trigger in
  `async-handoff` skill own `evidence.md`.

## Wiring the gates

Run once per repo, in PR that land first async handoff — not per messaging
change. Instructing agent do nothing for gate: **gate is what catch next agent**,
and unwired gate is rule described as enforced that is not. **Ordering, and the
record to commit after: [gates.md](gates.md).**

## Named gaps — where this stack can host no check

Silence read as coverage, so each stated.

1. **Swallowing catch invisible** (`E-10`), unchanged from money and cache
   rules. Void handler port reduce it — no default to return — but general case
   is spec and review.
2. **Broker-side and infrastructure configuration invisible to every check in
   this build** (`E-5`, `E-14`, `E-27`). Catalog declarations are lints
   operands.
3. **Same-transaction property decided by test, not type** (`E-6`), per jOOQ
   divergence above.
4. **Hand-rolled request-reply pair** built from two subscriptions and
   correlation id not decidable (`E-1`).
5. **Cross-repository union check got no host** (`E-19`, `E-26`). Catalog and
   schema gate repo-local, so producer renaming subject cannot see other
   seventeen services. **Most consequential gap here and it need infrastructure
   that no exist.**
6. **AsyncAPI path got no build-failing Java host** (`E-19`), and the one that
   look like it is false-green gate — named above so nobody wire it.
7. **Property-test library carry version trap, and its pin not a rule here.**
   `E-7` and `E-13` both name jqwik property tests. That library version pin is
   **cross-cutting dependency rule rather than async-handoff rule** — it bind
   every use of library in repo — so not stated as check here.
   **`llm-default-traps` own it**, with ceiling version, incident behind it, and
   CI version-ceiling check; value **deliberately not repeated here, because pin
   stated in four skills drift in three.** That skill bind every agent-built
   repo regardless of stack, so not optional companion — **install it in any
   repo that install these.** Repo that no install it got no pin from any skill
   here and must decide it at its own dependency review.

8. **The six second languages `async-handoff`'s layer check named 2026-08-02, and
   what this stack can host for each.** Stated here because a check kind with no
   tool is wish, and **one of the six already have a host here that nobody
   wired**.
   - **`E-1`, a handoff declared outside Java.** ArchUnit and the
     dependency-manifest check read bytecode and the build file. A Kubernetes
     `CronJob`, a managed scheduler, a `pg_cron` entry and a broker-side shovel or
     Kafka Connect connector reference no type, so **the allow-list have no
     operand for any of them**. Host would be a lint over committed manifests and
     infrastructure code — no Java tool do it, and this repo run none.
   - **`E-4`, the outbox read from query text.** ArchUnit decide which module
     import the outbox repository and read no SQL. **The stronger half is not a
     Java check at all**: a database grant that make the outbox table unreadable to
     every role but the relay's, asserted by the same schema lint that already read
     committed migrations. Cheap, and not wired.
   - **`E-21`, an untyped schema field.** Schema lint read the Avro or AsyncAPI
     file, so **a `map` or `bytes` field defeat every content ban by declaring
     nothing** — the float ban's fifth layer included. Decidable response is a lint
     clause banning those constructs per subject; same host as the existing schema
     lint, one more rule in it.
   - **`E-22` and `E-23`, scope and clock in query text.** **This one have a host
     already in this stack, in the sibling skill**: `money-java` `M-35` pair an
     ArchUnit predicate with a lint over committed query text, view and function
     definitions and Flyway migrations. Same lint, two more patterns — a missing
     scope predicate cannot be pattern-matched, but `now()`, `current_timestamp`
     and a clock default on a column written by a replay-safe handler can. **Not
     wired, and the lint it would extend already exist in a neighbouring family.**
   - **`E-27`, topology drift.** No host. Reconciliation job reading topology from
     the broker's admin API and diffing against the committed declaration —
     bespoke, and gap 2 above already say the declarations are the lint's operands.
     **This is that gap with a check named for it.**

**Two costs, stated rather than absorbed, and both real numbers for three-person
team.** Cache rules already **triple** integration CI time; this set run suite in
**four** configurations against real broker in container, **which make it most
expensive gate in this skill set. Nobody has run it.** And `E-33` two-instance
arm mean second consumer container four-configuration gate did not previously
need. **If gate cut, `E-10`, `E-13`, `E-15`, `E-22` and `E-23` degrade to
declarations while catalog still report green** — exactly what `E-25`
per-subscription positive controls exist to make visible.

## Markers, dates, and what they mean

**Nothing in `E-1` … `E-33` confirmed** — all convention. **Read every tool claim
behind them as primary-source verified by one researcher, not confirmed:** both
passes behind this skill ran 2026-07-29, pass 1 skipped its three refutation votes
on an exhausted agent budget and stood a canary-carrying hostile audit in their
place, pass 2 closed the composite shapes with no panel and no audit. Between them
the two weakest passes behind any skill in this set. Detail in
[evidence.md](evidence.md).

**Review by 2027-01-29.** Past that date every **confirmed** marker read as
**convention** until new pass re-date it — and nothing here confirmed today, so
lapse rule bite only if future pass promote something. Version pins and licences
age fastest: **re-check Boot, spring-kafka, jOOQ, ArchUnit, Testcontainers, outbox
libraries and every licence at adoption, not on calendar.**

Ground behind each Java claim, with its source and date, the research-method note,
one recorded contradiction between sources, and what must **not** be cited, one hop
away in **[evidence.md](evidence.md)**. Platform-neutral evidence — transport
defaults, hostile audit, steelman per rejected shape, nine-candidate transport
survey, reopen conditions — in `async-handoff` skill own `evidence.md`.
