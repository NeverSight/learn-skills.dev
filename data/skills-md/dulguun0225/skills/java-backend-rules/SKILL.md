---
name: java-backend-rules
description: The platform constitution for a Java backend on Spring Boot Web MVC, jOOQ and PostgreSQL — the rules that bind every line of code in the repo, each with a named build gate. Reactive WebFlux, JPA and Hibernate, Spring Data JDBC and the JdbcTemplate family, jOOQ's attached-record CRUD, plain-SQL strings, an injectable DSLContext, fixed thread pools for request work, StructuredTaskScope, an extra semaphore over the connection pool, wall-clock reads in domain code, `octet_length` and `varchar(n)` length limits in migrations, `create trigger` and `create function` in migrations, and the runtime-silent Spring annotations — field injection, @Transactional, @Scheduled, @Async, @Cacheable — are banned by name, each with the check that fails the build. ALWAYS load before writing a query, a transaction, an in-request fan-out, a Flyway migration, a scheduled task, or a test on this stack, before picking a persistence, concurrency, JSON or nullness library for it, and before creating a build file or pinning the Java or Spring Boot version for a new repo.
---
# Java backend — the platform rules

Rules bind **every line of code** in Java backend on this stack, plus named check enforce each. Six area — platform picks, concurrency, time, nullness, runtime-silent ban list, test toolchain.

Two sibling skill carry area with own condition. Repo on this stack install all three:

- **`java-backend-api`** — HTTP contract rules. Bind when backend expose HTTP API described by OpenAPI doc.
- **`java-backend-observability`** — logging, metrics, alerting. Bind when deployed system have no human watching continuously.

**No rule ids here, deliberate.** Each directive be `###` heading; heading be how you refer to it — *the transaction seam*, *the preview-API ban*, *the fan-out helper*. Nothing else in skill set number these, so invented number point nowhere except repo that install this skill; skill name plus subject read as instruction, resolve either way. Cite these rules same way from anywhere.

## The marker ceiling, before the rules

**Evidence behind six area uneven, and unevenness run by area not by rule.** Read first — rule stating check look equally settled whichever group it in.

- **Every Concurrency claim re-verified 2026-07-24 under three-vote adversarial panel**; survivor carry **confirmed**. One starting claim **refuted** there, rule rewritten around refutation — see *The keep-alive safeguard*. No ranking against other group here intended, none against other skill in set: several had own panelled pass.
- **Persistence claims marked confirmed checked against primary vendor doc, no panel** (2026-07-25) — jOOQ attached-record CRUD and fetch cardinality, plain-SQL injection hazard, lambda-scoped transaction API and autocommit, four migration hazard. **Mandates** built on them be this rule set own synthesis, and say so.
- **So *confirmed* mean two thing in this skill; date be only teller.** Against claim dated **2026-07-21** or **2026-07-24** it mean claim survive three independent refutation vote — both pass run panel. Against **2026-07-25** it mean one researcher check against primary source — **pass wrote "confirmed" while running no panel**. That usage carried here not silently corrected, because re-marking someone else verdict not what converting do. Read 2026-07-25 *confirmed* as documentation check. **2026-07-27** carry one panelled claim, belong to `java-backend-observability` not this skill; correction it made to rule here dated to it. Nothing here dated **2026-06-11..14** and marked confirmed — that pass record no per-claim marker at all.
- **Nullness confirmed** mainstream (2026-07-21) — panelled date, so strong sense.
- **Time, ban list, real-database test rule be convention, no citation at all.** No external evidence survive for any. Kept because enforceable, cheap, fail toward safety — **enforcement never confirmation**, and green ArchUnit run say nothing about ban being good idea.
- **Three Platform directive carry no own evidence note** — WebFlux paradigm ban, Flyway-migrations rule, Jackson pick. Their dating be inference drawn while writing this skill, not date any research pass wrote. [evidence.md](evidence.md) say so where it state them.

Whole set `review-by` **2027-01-21**. **Past that date every *confirmed* marker read as *convention*** until new pass re-date it, no maintainer action needed. Rule only work if date visible beside claim — why every directive carry one.

Status tier: **decided, not yet validated** — researched and decided, **no production use yet** behind enforcement shapes.

## The premise, and the thing it is not

**Code written by LLM agents, no human read it line by line.**

Every rule conditioned on that. Verdict portable exactly as far as premise: in repo where human read every diff, several drop from mandatory to merely advisable, and repo in that position should say so and carry burden of saying it, not silently drop rule.

**This skill not argument for choosing this stack.** It assume platform decision — Java, Spring Boot Web MVC, jOOQ, PostgreSQL — already made, and state rules that follow. **Rule set never reason to adopt stack**, and this one not evidence for own platform: fifteen sibling skill on one stack be accumulated *consequence*, not accumulated justification.

**Argument for choice live in `backend-stack`**, which rank candidate by what their build can refuse to ship, carry this stack as worked case. If platform still open, read that skill and come back. Two thing it settle: **deciding criterion be stack enforcement surface, not operability** — operability be veto winner must clear, different thing, different answer, because "we already know it" not guardrail when nobody read code. And candidate list behind Java verdict — C#/.NET, Kotlin, Go, TypeScript, each with ground it lost on — **published in `backend-stack`**, not here; what still missing there be primary source per ground and re-open trigger per loser, which that skill state about itself rather than leave to be inferred from silence here.

**Three tripwire mean repo left this skill assumptions entirely**, not merely added feature: first LLM call in product, hard real-time deadline, shipped SDK. None covered here; rules below written with none in view.

## The defaults these rules override

Picks unbriefed agent statistically make. **Naming loser be load-bearing half** — "use jOOQ" not override instinct, "corpus default be JPA with dirty checking, rejected because accidentally mutated entity become silent UPDATE" do. Do not compress these when carrying rule into repo own text.

- **JPA, Hibernate, Spring Data JPA** — corpus-dominant Java persistence. Rejected as runtime-silent: dirty checking turn accidentally mutated entity into silent `UPDATE`, and silence most expensive where money move. **Corpus advantage self-cancel** — every future agent session generate against corpus gravity toward banned patterns, which be cost this ban pay for.
- **Spring Data JDBC, and `JdbcTemplate` / `JdbcClient` for hand-written SQL** — pick agent reach for *after* being told JPA banned, and it survive that ban because ground JPA lost on not carry: **Spring Data JDBC do no dirty checking.** Own ground be three. **Query derived from repository method name** — statement that exist in no committed text, so method rename rewrite SQL and nothing type-check either half against schema. **Row mapping by reflection over column name** — dropped or renamed column be runtime failure where generated jOOQ class make it compile error. And **second persistence idiom beside jOOQ in one repo**, which `ai-maintainer-principles` reject on its own ground — one idiom imposed mechanically. `CrudRepository.save()` also pick INSERT-versus-UPDATE from in-memory id state, same shape as *jOOQ's own runtime-silent CRUD* below, though that claim **uncertain**, nothing here rest on it — verify against pinned Spring Data line before citing or carrying it. `JdbcTemplate` and `JdbcClient` carry reflective mapping plus plain-SQL hazard *Plain-SQL `String` constructs are banned* already state.
- **Annotation-driven transactions, caching, scheduling** — corpus default Spring style, banned as runtime-silent. See *The runtime-silent ban list*.
- **Fixed-size platform-thread request pool** — classic Tomcat and executor tuning, and do-nothing default. Under blocking Web MVC plus jOOQ it reintroduce thread-pool exhaustion, because slow database call starve request thread under load. Virtual threads remove exactly that failure mode, keep identical blocking top-to-bottom code shape.
- **Manually pooling virtual threads** — fixed or cached pool of them. Defeat point: pooling reintroduce scarce-resource bottleneck they designed to remove, and pooled virtual thread caching per-thread state just reallocate per task.
- **Raw `newVirtualThreadPerTaskExecutor` plus `Future.get` loop for in-request fan-out** — compile, pass happy-path test, silently wrong. See *The fan-out helper*.
- **Adopting `StructuredTaskScope` now** — ergonomically attractive fan-out API, preview on JDK 25. Dominant corpus shape for it (JDK 21–24 `ShutdownOnFailure` and `ShutdownOnSuccess` constructors) **not even compile on JDK 25** — the corpus-poisoning these rules exist to prevent.
- **Extra `Semaphore` on top of connection pool to limit database load** — redundant. Pool already block caller past its size.
- **Regenerating jOOQ classes against live or shared database** — path of least resistance, make generated tree function of whatever that database happen to hold.

**More corpus default rejected by rules living elsewhere in this skill set**, because their rules do; named here only so reader not conclude stack have no verdict. Binary floating-point for amounts, reaching for money library — `money`, `money-api`, `money-storage`, `money-java` skills. Spring `@Cacheable` and cache abstraction, reaching for Caffeine or Guava outside cache adapter — `caching` and `caching-java` skills. `@KafkaListener` on handler, broker publish beside repository save — `async-handoff` family. Cross-cutting dependency traps binding any agent-built repo on any stack — `llm-default-traps`, also this stack owner of record for jqwik version pin.

## Platform

### Java and Spring Boot Web MVC, with WebFlux banned as a paradigm

**Java at version pinned in build — pin created by directive below — Spring Boot with servlet Web MVC stack. Reactive WebFlux banned as paradigm** — one concurrency model be blocking thread-per-request on virtual threads, and second model in same repo mean every later piece of code must answer which one it in.

*ArchUnit — off-the-shelf. **Convention**, 2026-06-11..14 — platform pass decision; no note in evidence trail address WebFlux ban directly. **Nothing about this ban confirmed**: virtual-thread claims the alternative measured against be, but one-concurrency-model argument itself be reasoning no pass put to source. Probed pro-default at N=2 (bare sonnet, effort high, 2026-08-11 — both picked Web MVC over WebFlux unprompted). See [evidence.md](evidence.md).*

### The pin is created at the newest supported LTS, and after that it is the pin

**Repo with no pin — greenfield, or first build file — pin newest Java LTS and newest Spring Boot GA line, verified against vendor own release page at that moment, with version, source and date recorded in repo. Repo that have pin defer to it**, above every version fact written anywhere in this skill set. **No floating version: no range, no `LATEST`, no `RELEASE`, no version resolved at build time.**

Two failure this close. **Training corpus be years behind at every point of its life**, so unbriefed pick be superseded LTS and superseded framework major, and nothing else in this skill contradict it — version fact appear here only as ambient worked-case detail (`backend-stack` record Java 25 LTS as one dated pass verdict; JDK 25 claims here dated 2026-07-24), which be **record of what was newest then, never floor**. Second, **newest that break a gate be no win**: JaCoCo trail each Java release, Error Prone and NullAway sit on compile path, pitest fix per-release defects. **Where named enforcement host not yet support newest LTS, pin one LTS back and record which host forced it** — enforcement surface be whole reason this stack chosen, so build that cannot gate be worse than build one release behind.

*Enforcer `requireJavaVersion` and `banDynamicVersions`, plus `maven.compiler.release` — off-the-shelf, and they **pin what was chosen, they not know what be newest**. Verification that pick was newest at adoption be **convention**: agent state it done against vendor release page, dated, same shape and same weakness as registry verification in `llm-default-traps`. **No gate here read currency and none can without reading network at build time.** Re-verify at adoption rather than on calendar be `tech-decision-research` rule, cited not restated. **Convention**, 2026-09-01 — no research pass; written from observed failure, agent scaffolding greenfield backend on superseded LTS and superseded Boot major.*

### jOOQ against PostgreSQL, with JPA and Spring Data banned

**Persistence be jOOQ against PostgreSQL; JPA, Hibernate, Spring Data JPA, Spring Data JDBC banned, and `JdbcTemplate`, `NamedParameterJdbcTemplate`, `JdbcClient`, `SimpleJdbcInsert` banned as second SQL path** — no entity lifecycle, no lazy loading, no query derivation, no reflective row mapping. **Ban be on second persistence layer beside jOOQ, not on Spring Data JDBC as technology**: it be named exit if jOOQ stewardship risk fire, and taking that exit **replace** jOOQ repo-wide as platform decision, never run beside it — repo holding both have two idioms, and every later query answer which one it in.

*Banned-dependency plus ArchUnit rules — off-the-shelf. **Convention**, 2026-06-11..14 for JPA half. Dirty-checking hazard class confirmed against jOOQ own doc for equivalent jOOQ construct — see *jOOQ's own runtime-silent CRUD* — but platform pass recorded rejections and grounds without per-claim confidence marker, so convention be floor rather than verdict it wrote down. Spring Data JDBC and template half added 2026-09-01, **convention**, no research pass behind it — written from observed failure: agent told "JPA banned" reached for Spring Data JDBC as compliant alternative. Its grounds be query derivation, reflective mapping, second idiom — **not** dirty checking, which Spring Data JDBC not do; the `save()` insert-versus-update claim **uncertain**, nothing here rest on it — verify against pinned Spring Data line before citing it.*

### jOOQ classes are generated from the committed migrations

**Regenerate committed jOOQ classes from committed Flyway migrations, never from live or shared database.** Migrations applied to throwaway real PostgreSQL in container, so generated tree be pure function of committed migrations.

*Bespoke — CI job regenerate and fail on any git diff. **Convention**, verified 2026-07-25 — mechanism be jOOQ own documented recommendation; that it mandatory here be this rule set synthesis, because jOOQ present it as one recommended approach not only one.*

### jOOQ's own runtime-silent CRUD is banned

**Attached-record writes banned; writes be explicit DSL statements.** `UpdatableRecord.store()`, `insert()`, `update()`, `delete()`, `refresh()`, plus `changed()` / `touched()` / `modified()` dirty flags, pick INSERT-versus-UPDATE **and** which column to write from in-memory record state that never appear in query text. That be dirty checking under another name — exact hazard this stack rejected JPA for, shipped inside library that replaced it. Records detached repo-wide with `Settings.withAttachRecords(false)`, so these methods **throw rather than guess**.

*ArchUnit — off-the-shelf host; owner-typed `UpdatableRecord` predicate authored per repo, plus config-default assertion, wired by repo, that `withAttachRecords` stay false. Generated jOOQ packages excluded. **Confirmed** against primary jOOQ documentation, verified 2026-07-25.*

### Fetch with `fetchSingle` or `fetchOptional`

**`fetchOne()` and `fetchAny()` banned.** They hide result cardinality: `fetchOne()` return null on zero rows, throw only on more than one, so query that must match exactly one **silently tolerate zero**; `fetchAny()` silently return arbitrary row when several match. `fetchSingle()` throw on zero and on more than one; `fetchOptional()` cover legitimately-optional case.

*ArchUnit — off-the-shelf host; ban on `fetchOne` / `fetchAny` call targets, or Error Prone check on source. **Confirmed** against primary jOOQ documentation, verified 2026-07-25.*

### Plain-SQL `String` constructs are banned

**`DSL.sql`, `field(String)`, `condition(String)`, `table(String)`, `query(String)`, `resultQuery(String)`, `fetch(String)` banned.** Each splice raw string into query tree, defeat jOOQ compile-time type checking, reopen SQL-injection surface type-safe DSL close. If repo need one, **confine to as few named seams as possible** — reference shape use one — each test-pinned named constant, and annotate only that scope `@Allow.PlainSQL`.

*ArchUnit ban on plain-SQL API by signature, generated packages excluded — off-the-shelf host, per-repo predicate. **jOOQ own `PlainSQLChecker` be stronger path**: turn any plain-SQL use into compile error unless scope annotated. Verify it wire against pinned JDK and Error Prone at adoption — that wiring unverified here. Hazard **confirmed** (verified 2026-07-25); single-seam discipline **convention**.*

### SQL is reached only through the one transaction seam

**Code touch SQL only inside lambda-scoped transaction block that receive context as parameter** — `tx.read(dsl -> ...)` and `tx.write(dsl -> ...)` in reference shape, method names be repo call — **and read-only intent be method name, not annotation. `DSLContext` not injectable bean.** Injected `DSLContext` used outside block run in autocommit, commit each statement on own, invisibly. Banning injection make unscoped query **unwritable**, not only reviewed against.

*ArchUnit — off-the-shelf host; no-injectable-`DSLContext` predicate authored per repo. That seam also own connection acquisition, so no `Connection` or `DSLContext` reachable outside transaction block, be **convention**. Two facts underneath — jOOQ own transaction API be lambda-scoped, and JDBC connection created in autocommit mode — be **confirmed**, verified 2026-07-25; mandate be this rule set governance choice.*

**This seam be shared resource, and two other published skill add requirement to it this directive not state.** `caching` require cache invalidation reachable only from seam **post-commit registration**; `async-handoff` require general-purpose post-commit callback registration **not** exist, because nothing at call site would then distinguish cache delete from message publish. Repo wiring this seam alongside either read their rules before fixing seam shape — this rule fix transaction boundary, not post-commit surface.

### Schema changes are committed Flyway migrations

**Schema changes be committed Flyway SQL migrations,** applied in integration tests against real PostgreSQL.

*Convention — integration-test setup be check. Dated 2026-06-11..14, only pass whose scope cover it; no evidence note carry this rule, and dating be inference drawn while writing this skill. Probed pro-default at N=2 (bare sonnet, effort high, 2026-08-11 — both set up committed Flyway migrations unprompted).*

### Every migration is linted for lock and rewrite hazards

**Lint every committed migration for lock and rewrite hazard, not only that it apply.** Migration running clean against empty test database can still take `ACCESS EXCLUSIVE` lock or rewrite table at production volume — exactly gap test-time rule above leave open. Four operation flagged, unwritable without reviewed per-migration opt-out: non-`CONCURRENT` index build, table-rewriting column-type change, `ADD ... NOT NULL` without default, constraint added without `NOT VALID` followed by later `VALIDATE`.

*squawk — off-the-shelf. Plain CLI gate on exit code over migrations in diff, **not pull-request comment bot**; enabled rule set and per-migration opt-outs configured per repo. Four hazards **confirmed** against PostgreSQL own documentation (verified 2026-07-25); choice of squawk over alternatives be **convention** — rule be hazard class, not vendor.*

**`DROP COLUMN` deliberately not on that list.** It be expand-and-contract compatibility concern, not documented lock-or-rewrite hazard; adding it would put rule with different ground behind gate that not evidence for it.

***The lint read SQL and a migration need not be SQL.* Layer check, 2026-08-02, conversion-dated.** squawk parse SQL migration files. **A Java-based migration or a migration callback do the same DDL through JDBC and present the lint no text to parse**, and DDL applied outside the migration tool at all — a manual change, an extension installed by hand, a change made by a library's own bootstrap — be invisible to both this lint and the *schema changes are committed migrations* rule above it. **The second one matter more than it look**: the whole regenerate-jOOQ-from-migrations chain assume committed migrations are the complete schema history, and a schema the migrations do not describe make that generation wrong rather than merely incomplete. **Decidable half be a ban on non-SQL migrations plus a drift check comparing the live schema against the one the committed migrations produce** — the drift check be the one nobody here has written.

### Text lengths are characters, never bytes

**A length limit on a text column be `text` plus `check (char_length(col) between 1 and N)`** — `check (col is null or char_length(col) between 1 and N)` where optional. **`octet_length` banned in every migration**, and `varchar(n)` not used for length limit at all (squawk `prefer-text-field` already ban `varchar`; cited here, not restated). **In the service the count be `String.codePointCount(0, s.length())`** — never `String.length()`, which count UTF-16 unit, never a byte count. Cyrillic and other non-Latin text be two or more byte per character and astral text be two UTF-16 unit per character, so byte count or UTF-16 count admit fewer character than spec state, or reject valid name. **State the unit in the text of the limit**; a limit written as "100" with no unit be read three different ways by three layers.

*`MigrationConventionsTest` rule `octet-length`, fixture `bad_octet-length.sql` — **bespoke**, and the migration lint be the only host: bytecode see no migration text, so ArchUnit cannot reach this. Wired in `dulguun0225/java-backend-template`. **The service-side `codePointCount` half be convention** — no static check exist for it, and it be held by an integration test sending N character of a multi-byte script (`ProductFamilyCollationIT` in `product-catalog` send 100 Cyrillic character = 200 byte and expect acceptance, 101 rejected). 2026-09-16.*

### No trigger, no function, in a migration

**`create trigger` and `create function`, with or without `or replace`, banned in every Flyway migration.** A trigger be behaviour absent from the program text: it run on a write nobody wrote, it read the database clock (`now()`) where the injected `Clock` be the only clock, and it be invisible to every ArchUnit rule, cuz ArchUnit read bytecode. This be the layer clause of the injected-`Clock` directive made explicit. **Audit column — `created_at`, `modified_at`, `modified_by` — be set by the application inside the same `tx.write`.**

*`MigrationConventionsTest` rules `trigger` and `function`, fixtures `bad_trigger.sql`, `bad_function.sql` — **bespoke**, same host and same reason as the rule above. Wired in `dulguun0225/java-backend-template`. 2026-09-16.*

### JSON is Jackson

**JSON be Jackson.**

*Convention. Dated 2026-06-11..14 by same inference as Flyway rule; no evidence note carry it. Probed pro-default at N=2 (bare sonnet, effort high, 2026-08-11).*

## Concurrency

One concurrency model be virtual threads — synchronous, top-to-bottom, un-colored code. **Win be bounded, not free throughput.** PostgreSQL be ceiling, so this remove thread-pool exhaustion and keep blocking shape at scale; not throughput multiplier, and adopting it as one produce disappointed team and rule set nobody trust.

### Virtual threads are enabled by one property

**`spring.threads.virtual.enabled=true` in committed config.**

*Config-default assertion — off-the-shelf. **Confirmed** 2026-07-24. **Check read checked-in default, not effective runtime value**, which env vars or external config can override — see *Named gaps*. Introducing framework version be **convention**, re-verify against pinned Spring Boot line at adoption.*

### The keep-alive safeguard is recommended, not required

**`spring.main.keep-alive=true` be recommended safeguard, not requirement for this stack.** Enabling virtual threads make Spring threads daemon threads, but embedded servlet server keep own non-daemon thread, so actively-serving Web MVC app **not exit without it**. Matter in no-web-server or scheduled-task-only mode.

*Convention, 2026-07-24. **"Required" framing refuted by panel — do not restore it**, and do not cite keep-alive as required for request handling. This be one directive in this skill written around refutation not confirmation.*

### One virtual thread per task, never pooled

**Fork with `Thread.startVirtualThread` or `Executors.newVirtualThreadPerTaskExecutor()`. Fixed-size `ExecutorService` for request or in-request work banned;** one platform-thread executor factory whitelisted for pinning fallback.

*ArchUnit — off-the-shelf host; whitelist predicate authored per repo. **Confirmed** 2026-07-24 — platform own guidance state virtual threads should never be pooled.*

### Bound concurrency at the limited resource, not at the thread count

**Do not throttle load by capping threads.** HikariCP pool be database semaphore — small fixed size matched to what PostgreSQL can serve, **never scaled to thread count**; thousands of virtual threads queue on it. Gate any non-database limited resource with explicit `java.util.concurrent.Semaphore`. **Do not add second semaphore on top of pool.**

*Convention — pool sizing be repo call; pool-as-limiter principle be rule. Underlying claim **confirmed** 2026-07-24, platform own words — connection pool already serve as semaphore, need no additional one.*

### Never fan out to database work while holding a connection

**Never fan out to database-touching subtasks while holding connection or open transaction.** Held connection plus subtasks each checking out connection can **deadlock small pool**. Acquire after fan-out join, or size pool by deadlock-avoidance formula.

*Convention — spec and review; **not statically detectable**, and this be one rule here with no possible build gate. Verified 2026-07-24 — deadlock mechanics and sizing formula primary-sourced; mapping onto virtual-thread fan-out be this rule set synthesis.*

### The fan-out helper

**In-request fan-out go through repo one canonical virtual-thread fan-out helper.** It fork one virtual thread per subtask in try-with-resources, cancel siblings on first failure, join all, aggregate exceptions. **Hand-rolled `Future.get` loops and raw executor fan-out in request code banned** — `ExecutorService.close()` neither cancel siblings nor short-circuit, so corpus-generated shape either run every sibling after one already failed, or serialize fan-out through sequential `get()` calls. Trade safe compile error for silent latency-and-correctness defect.

*Bespoke — one owned helper plus ArchUnit ban on raw executor fan-out in request paths. **Convention**, 2026-07-24. `close()` semantics this rest on be stated in rejected-alternatives record, not in dated evidence note with primary source — see [evidence.md](evidence.md).*

**This helper carry second obligation stated in `java-backend-observability` — establishing each subtask logging context at fork time.** That rest on one claim in that skill area put to adversarial panel; panel produced **two** rules there, context capture and logging-backend pin, and that skill mark both **confirmed**. Repo building helper from this directive alone build it without context capture, and every subtask log line then lose correlation fields silently.

### No preview APIs

**Do not use preview APIs; never pass `--enable-preview` to `javac` or to `java` launcher,** in Maven or Gradle. This **categorically** forbid `StructuredTaskScope` — preview on JDK 25 — and every other preview API. Preview-compiled class file stamped so it load only on exact JDK feature release it built on, making artifact version-locked.

*Off-the-shelf plus bespoke — preview code fail to compile without flag, so build fail closed; bespoke CI grep also scan compiler and launcher arguments across Maven and Gradle. **Not ArchUnit**, which read bytecode and cannot see compiler or launcher flags. Preview status and version-locked class file **confirmed** 2026-07-24; per-release API history behind it **uncertain**, nothing here rest on it.*

### Per-request context, and never a cached object in a `ThreadLocal`

**Put per-request context in `ThreadLocal` or, preferably, Scoped Value** (final in JDK 25) — **preferably for bounded lifetime and write-once binding, not for child-thread sharing.** Scoped Value binding inherited only by threads forked inside `StructuredTaskScope`, which preview ban above forbid, so **it never reach subtask here.** `InheritableThreadLocal` do reach one, but do not rely: platform not specify which thread construct child in per-task executor. Context that must reach subtask be established there by fan-out helper. **Never cache reusable object in `ThreadLocal`** — virtual threads never pooled, so per-thread cache just reallocate per task.

*Convention. Child-thread-sharing correction dated 2026-07-27, inheritance facts behind it **confirmed** 2026-07-27 by fan-out context panel; preference for Scoped Value on its other two properties be convention.*

### Keep the pinning event on, and alert on it

**Keep `jdk.VirtualThreadPinned` JFR event on** (default 20 ms threshold) **and alert on it in deployment.** Residual pinning on JDK 25 be native-only — native methods, foreign functions, blocking class initializers. Pinning not make application incorrect, but pinning that exhaust all carriers can stall scheduler, so treat sustained pinning as operability hazard not mere slowdown.

*Convention — monitoring wiring, 2026-07-24. **Tripwire, not guarantee**: many short sub-threshold pins can accumulate cost without ever firing. Residual pinning causes **confirmed** 2026-07-24.*

## Time

### `Clock` is injected

**Wall-clock reads in domain code banned** — `Instant.now()`, `LocalDate.now()`, `new Date()`, `System.currentTimeMillis()`.

*ArchUnit — off-the-shelf. **Convention**, 2026-07-21 — no external evidence survived, rule carry no citation. Kept because enforceable and cheap. Probed pro-default at N=2 per tier (bare sonnet + opus, 2026-08-11 — 4/4 injected `Clock`, fixed-clock tests); held by the cheap gate, the layer clause below be the contra half.*

***The clock be readable in the store's language, and this skill own the stack's clock ban.* Layer check, 2026-08-02, conversion-dated.** ArchUnit read bytecode and match those four calls. **`now()` and `current_timestamp` in query text, a column `DEFAULT` of one, and a trigger that set one are each a wall-clock read** reaching the row the application write, in a language this rule never see — **and the trigger third of that be closed since 2026-09-16 by *no trigger, no function, in a migration* above, whose `MigrationConventionsTest` rule `trigger` fail the build; query text and column `DEFAULT` stay open** — and on this stack they be *more* likely than the banned Java calls precisely because the Java calls fail the build. **`async-handoff` `E-23` replay-safety already depend on this ban reaching further than it do**, and its own layer clause point here; so do the regenerate-and-diff gates that assume committed inputs, which be a class rather than a rule and named as one. **The host exist one family over**: `money-java` `M-35` already pair an ArchUnit predicate with a lint over committed query text, view and function definitions and Flyway migrations, and what it need added is **clock functions in query text and clock defaults on columns** — named, not counted. **Not wired.**

### Business dates are their own concept

**Business date be `LocalDate` from explicit business-date source, never derived from wall clock. Timestamps be UTC `Instant`, stored as `timestamptz`.**

*Convention, 2026-07-21 — same standing as injected clock, no citation.*

**Future legal deadline be neither of these**, and `llm-default-traps` carry that rule — stored as local wall time plus governing zone, resolved at evaluation time, because zone rules change between now and deadline. Reading "timestamps are UTC" as covering deadline be specific mistake that rule exist to prevent.

## Null

### JSpecify, checked by NullAway, as compile errors

**JSpecify annotations, checked by NullAway running on Error Prone, as compile errors.** Nullness violation never reach review.

*Off-the-shelf. **Confirmed** mainstream, 2026-07-21 — Spring Boot 4 and Spring Framework 7 ship JSpecify-annotated null-safe APIs across portfolio, deprecate Spring own nullability annotations, check Spring own build with NullAway.*

## The runtime-silent ban list

**Behavior that never appear in program text be behavior implementer guess at.** Each entry below banned with named enforcing check.

*List as whole be **convention**, 2026-07-21 — defect-source claim carry no citation, no external evidence survived. Kept because enforceable, cheap, and every entry have named check. **Enforcement not confirmation**, and ArchUnit class below be enforcement.*

**Marker, date, check stated once here for whole list — one place in this skill they not inline per directive.** Deliberate, not dropped marker: entries below share single ground and single enforcement host, named in *Every ban names the check that enforces it* at end of list. Read each entry as carrying **convention, 2026-07-21** and that host. Two entries probed pro-default at N=2 (bare sonnet, effort high, 2026-08-11): field-and-setter injection and reflection dispatch — both held by the shared host, not by instinct-override.

**What this list not say be why constructor injection, route registration and typed config binding survive it**, since those be framework machinery too. Discriminator be **startup-loud versus runtime-silent** — mechanism whose failure be boot failure caught by first integration test, against one that change semantics silently at runtime — and it published in `ai-maintainer-principles`, not here. Repo carrying this list into own text without it will either ban own dependency injection or relax list informally until nothing banned.

### Field and setter injection

**Banned — constructor injection only.**

### `@Transactional`

**Banned.** Transactions be explicit visible blocks reached only through one transaction seam above; annotation-driven ambient transactions be thing being removed.

### `@Scheduled` and `@Async`

**Banned.** Scheduling and asynchronous work go through one explicit named mechanism. **On this stack that mechanism specified by `async-handoff` family**, which treat bare executor submit as asynchronous handoff with full rule set attached — including outbox requirement. This ban be half saying annotation not the mechanism; it not say what mechanism is.

### `@Cacheable`, `@CachePut`, `@CacheEvict`, `@Caching`, and AOP aspects on domain code

**Banned, together with any caching decorator wired behind domain interface.** This entry put them on list; **`caching` and `caching-java` skills be where ban get its checks, four grounds, and replacement**, not restated here because rule stated in two skills drift in one.

**What this stack add to those grounds be size of pull:** Spring cache abstraction be corpus default for "add caching" on this stack **by wide margin**, why it need ban with check not note. **Repo installing this skill and not `caching` have ban and no replacement** — no adapter seam, no staleness ceiling, no invalidation rule — so agent told only "annotation banned" hand-roll something worse. Install `caching` even if repo cache nothing today; first cached value be tripwire.

### Reflection-based dispatch and stringly-typed behavior lookups

**Banned.**

### Every ban names the check that enforces it

**Ban with no named check not on this list.** ArchUnit host ban on bytecode, Error Prone host one on source, and **which tool host which ban decided per rule by what each can read soundly** — not by preference. Worked case in `java-backend-observability`, where unloggable-domain-type rule must be Error Prone because ArchUnit see logger erased signature not argument static type; `caching-java` have two more of same shape. **Meta-test keep list honest:** each ban either enforced by named test or **explicitly marked deferred with reason**. **Reconcile both directions** — declared-enforced ban name test that actually exist, and test that enforce ban no stay undeclared. One direction alone let deferred ban be described as enforced *or* let wired rule drop off list, and both failure read as complete list. (Prior art, 2026-06-13, from same external record `guardrails-toolchain` convert its own material from; **that record not published in this skill set, and this clause restated in no other skill — this skill own it.** **Convention**, and both-direction clause not from 2026-07-21 pass.)

*ArchUnit on bytecode and Error Prone on source — off-the-shelf hosts; some predicates authored per repo.*

***A ban list match what is written, and the same behaviour be declarable two other ways.* Layer check, 2026-08-02, conversion-dated.**

- **Meta-annotation, and a sibling skill already found this.** Rule matching a banned annotation **directly on a member** report green over a repo-defined annotation that is itself annotated with the banned one — Spring resolve the meta-annotated form and behave identically. `async-handoff` `E-2` state the requirement outright, *check meta-annotated and type-level forms, not just method-level direct annotation*, verified there against one framework's own documentation. **This ban list carry no such clause**, and it be the list every other stack rule here point at. **Every predicate on this list read meta-annotations and type-level placement, or the list be a list of spellings.**
- **Configuration, which no bytecode rule read.** A scheduler, a cache manager or an aspect declared in a properties or YAML file, or a bean defined in a configuration class, produce the banned runtime-silent behaviour with no banned annotation present anywhere. **`caching-java` record the same gap from its own side** for the framework cache abstraction. Decidable half be a lint over committed configuration for the property keys that enable each banned mechanism — **not carried here, and the meta-annotation half is the cheaper and more urgent of the two.**

## Evidence toolchain

**Tests be the code review.** No rule in this skill assume human read generated code line by line.

### Integration tests run against real PostgreSQL

**Integration tests run against real PostgreSQL in throwaway container, applying real migrations. No in-memory substitute database.**

*Convention, 2026-07-21 — no external evidence survived, rule carry no citation. Kept because enforceable and cheap.*

### The ban list is an executable test class

**Ban list be ArchUnit test class — executable, not prose.**

*Off-the-shelf host; some predicates authored per repo. **Convention**, 2026-07-21 — trail make no confidence claim beyond noting ban-list test class plus meta-test **not independent confirmation** of bans it host.*

### Coverage is gated by JaCoCo

**Coverage gated by JaCoCo — `jacoco-maven-plugin` `check` goal — failing build below per-package `COVEREDRATIO` floor.** Coverage be floor under every package: **it prove line ran, not that test asserted on it**, so green floor necessary and never sufficient. Ratio and per-package split be adopting repo call, stated in repo. Pin JaCoCo to release supporting build Java version — it trail each Java release.

*Off-the-shelf host — ratio thresholds and per-package split authored per repo. Mechanics **confirmed**, verified 2026-07-25; no threshold numbers supplied here, deliberately, because floor tuned to one product risk profile not platform default.*

## Wiring the gates

**Run once per repo, in first pull request touching build.** **On a greenfield repo, create it from `dulguun0225/java-backend-template` instead of wiring the list below by hand — by invoking the sibling skill `new-java-backend`, which carries the one-command script and stops where spec-kit begins, not by retyping the template's README** — items 1 to 9 and 11 are wired there, run green on Java 25 and Spring Boot 4.1.1 on 2026-09-16, and item 10 is deployment. That script is the template's four-command sequence as one command with the template pinned to a recorded commit; it stops before anything that touches the forge and prints those steps, and it lives in `new-java-backend` rather than here so that scaffolding loads the procedure and not this body. Scaffolding is not a decision, so nothing an agent writes during it is wanted: run the script, then start on domain code. The template is the consequence of these directives, not a second statement of them: where it and a directive here disagree, the template is stale and the directive wins. An agent that scaffolds these gates from prose spends its first session on boilerplate and gets a different ban list each time; the template makes that session unnecessary. (Check: the template's `docs/GATES.md` maps every wired gate to its heading here and lists what it does not reach as named gaps — a directive in neither table is the finding; nothing mechanised — *convention*, 2026-09-16.) These directives be two kinds welded together: instinct-overrides firing while agent write code, and build gates that must exist in repo. Instructing agent do nothing for second kind — **gate be what catch next agent**, and unwired gate be rule described as enforced that not.

1. **Ban-list ArchUnit test class**, with meta-test asserting every entry either enforced by named test or marked deferred with reason. Host for runtime-silent bans, WebFlux ban, attached-record and plain-SQL bans, `JdbcTemplate` / `NamedParameterJdbcTemplate` / `JdbcClient` / `SimpleJdbcInsert` type ban, `fetchOne` / `fetchAny` ban, no-injectable-`DSLContext` rule, wall-clock ban, raw-executor fan-out ban. **Generated jOOQ packages excluded** from all.
2. **Banned-dependency rules** for JPA, Hibernate, Spring Data JPA, and Spring Data JDBC — `spring-data-jdbc`, `spring-data-relational`, `spring-boot-starter-data-jdbc`. **`JdbcTemplate`, `NamedParameterJdbcTemplate`, `JdbcClient`, `SimpleJdbcInsert` be not dependency ban** — `spring-jdbc` arrive transitively under jOOQ starter and carry pool plus exception translation this stack use, so artifact ban break build; ban them **by type on ban-list ArchUnit class** in item 1 instead, and verify that transitive shape against pinned Boot line at adoption. Sibling skills add own entries to same config — logging backend pin in `java-backend-observability`, cache and broker client bans in `caching-java` and `async-handoff-java`, JVM dependency bans in `llm-default-traps`.
3. **jOOQ codegen-diff job** — regenerate from committed migrations against throwaway PostgreSQL container, fail on any git diff.
4. **Config-default assertions** for `spring.threads.virtual.enabled=true` and `Settings.withAttachRecords(false)`. Both read checked-in default, neither see runtime override.
5. **Error Prone on compile path**, with NullAway and JSpecify configured to fail compilation. Also host for any non-loggability check and for `fetchOne` / `fetchAny` ban if repo prefer source over bytecode — and **not** ArchUnit for first of those.
6. **squawk** over migrations in diff, gating on CLI exit code, with enabled rule set and per-migration opt-outs committed. **Beside it, `MigrationConventionsTest`** — the repo-authored lint over committed migration text, hosting the rules `octet-length`, `trigger` and `function`, each with a `bad_*.sql` fixture asserting it fire. Both wired in `dulguun0225/java-backend-template`.
7. **Testcontainers integration-test setup** applying real migrations against real PostgreSQL.
8. **`jacoco-maven-plugin` `check` goal** with per-package `COVEREDRATIO` limits this repo state, version pinned to release supporting build JDK.
9. **CI grep for `--enable-preview`** across Maven and Gradle compiler and launcher arguments. Not ArchUnit, which cannot see them.
10. **`jdk.VirtualThreadPinned` JFR event and its alert**, in deployment not in build.
11. **Maven Enforcer** — `requireJavaVersion` at pinned LTS and `banDynamicVersions` over declared dependencies. Neither know what be newest; both stop pin drifting after it set.

**Then record what was wired and what was skipped, with reason.** These be entries **nothing above gate**; each must be listed as ungated:

- **Never fanning out while holding connection** — spec and review. Not statically detectable by anything.
- **Pool sizing**, and ban on second semaphore over pool — pool-as-limiter principle be rule, no check read pool size against what PostgreSQL can serve.
- **Single-seam discipline for plain SQL** — ban gated; that exempted seams be few, named, test-pinned not.
- **That transaction seam own connection acquisition** — ArchUnit ban injecting `DSLContext`, not every path to `Connection`.
- **That the service count character with `codePointCount` rather than `String.length()`** — migration half gated by `MigrationConventionsTest` `octet-length`, service half convention, held only by an integration test a repo must write with multi-byte text in it.
- **Business-date and `ThreadLocal`-caching rules**, and Jackson and Flyway picks — convention, no check.
- **Whether `PlainSQLChecker` wired**, if repo chose it over ArchUnit path. Compatibility with pinned JDK and Error Prone unverified here, must be established by adopting repo.
- **That pinned Java and Spring Boot lines were newest at adoption** — agent assertion plus dated line in repo. Enforcer pin them; nothing read currency.

**Record listing only what was wired read as complete coverage.** That be failure this step exist to prevent.

## Named gaps — where no check reaches

Silence read as coverage, so each stated.

1. **Config-default assertion not runtime assertion.** Both — virtual-threads property and attached-records setting — read checked-in default. Env variable or external config source can override either in deployed process, and **no gate here notice.** Same limitation apply to structured-logging property in `java-backend-observability`.
2. **Fan-out-while-holding-a-connection rule have no possible gate.** One rule here stated as undetectable, not merely ungated.
3. **Generated jOOQ packages excluded from every ArchUnit ban.** Rule written into generated package unreached by design. Correct — generator output not hand-written code — but exclusion boundary be load-bearing, and hand-written class placed in generated package escape whole ban list.
4. **`--enable-preview` grep cover what grep cover.** Compile failure be real gate and fail closed; grep exist for case where flag added deliberately, and be bespoke text-matching over build files, not analysis.
5. **Coverage floor cannot see whether test asserted anything.** Mutation testing, which can, **deliberately scoped to money packages only** by `money-java` skill. So package in general tier can sit green at floor over vacuous machine-written tests, and **nothing in this skill detect that.** Extending mutation testing beyond money be decision with named trigger, not oversight — general-tier defect traced to vacuous tests, or diff-scoped mutation testing becoming affordable.
6. **Three Platform directives rest on no evidence note.** WebFlux ban, Flyway rule, Jackson pick. Dates inferred from pass scope; reader treating them as researched to same standard as jOOQ claims read more than is there.
7. **Plain-SQL checker wireability unverified.** ArchUnit path work and be what ship; stronger compile-error path named as stronger without being tried against this stack pinned versions.
8. **Pinning alert be threshold tripwire.** Accumulated short pins below threshold cost real scheduler time and fire nothing.
9. **Codegen-diff gate assume generation reproducible, and nothing assert it.** Job regenerate once and diff. Non-determinism in generator — iteration order, locale-dependent sorting, embedded timestamp — make gate flap, and flapping gate get relaxed, at which point it mask drift it exist to catch. `java-backend-api` carry stronger form for its document: regenerate **twice** under varied timezone and locale in one pinned container, byte-identical to both. Not carried here — stated 2026-08-01 when `guardrails-toolchain` published general form, cuz asserting it never verified against jOOQ generator on this stack. **Narrowed 2026-09-16:** `java-backend-template` regenerates the jOOQ tree twice, under `Pacific/Kiritimati` and `tr_TR.UTF-8`, and diffs both runs against each other and the committed tree; jOOQ 3.21.7 on a one-table schema came out byte-identical. So the generator has been seen reproducible once, on one version and one schema, and the stronger form is wired in the template — still not a directive here, because one schema is a sighting, not a property.
10. **No rule here say anything about primary keys, and migration lint above no ask.** This skill require schema change be committed Flyway migration and be linted for lock and rewrite hazard; **nothing say what the key column be, how it be generated, or what may be assumed about its order.** Agent writing first migration on this stack therefore reach for its corpus default — `bigserial` or `gen_random_uuid()` — and neither squawk nor any ArchUnit ban here notice. **Key rules live in `primary-keys`**, whose gates are a migration grep, a table-classification job and an `ORDER BY`-on-id ban. **That ban need two hosts — that skill's layer check, run 2026-08-02**: ban-list test class here host the jOOQ-builder half — an `orderBy` call handed a key field is a type dependency ArchUnit read soundly — and it read no SQL text at all, so the other half be a lint over committed view and function definitions and Flyway migrations, **and this skill carry no such lint**; squawk read migrations for lock and rewrite hazard, not for sort columns. **This stack narrow the exposure rather than close it**: plain-SQL `String` constructs banned above, so `ORDER BY id` inside a string be largely unwritable in application code — view text, function bodies and migrations stay reachable by nobody. Gap stated rather than closed here, cuz that skill be stack-neutral and this one carry no key rule of its own to narrow.
11. **Nothing here tell pin that was newest at adoption from pin already stale when written.** Enforcer assert what repo declared, so repo scaffolded on superseded LTS pass every gate in this skill forever, and each later agent read pin as decision. Closing it need oracle outside build — vendor release page read at adoption — and that read be convention, same class as registry verification in `llm-default-traps`. The template records its pin with source and date in a comment beside it; that is the convention performed once, and it decays the same way.

## Markers, dates, and what they mean

Confidence, per claim: **confirmed** mean claim survived three independent refutation votes against primary sources on date it state. **Primary-source verified** mean one researcher checked against primary source with **no panel** — not confirmed whatever its evidentiary strength, and running panel be what promote it. **Convention** mean research did not, or could not, confirm claim from independent sources; rule kept because enforceable, cheap, fail toward safety. **Uncertain** mean claim examined and left unsettled; nothing here allowed to rest on one.

Enforcement, per rule: **off-the-shelf** mean tool do it with configuration; **bespoke** mean check must be written; **convention** mean human or agent asserting it be all there is.

**Lapse rule:** past `review-by` **2027-01-21**, every *confirmed* marker in this skill read as *convention* until new pass re-date it, no maintainer action needed. That be why date sit beside every claim.


Ground behind each claim — with source where pass named one — claims that must **not** be cited, and conditions reopening rule be one hop away in **[evidence.md](evidence.md)**.