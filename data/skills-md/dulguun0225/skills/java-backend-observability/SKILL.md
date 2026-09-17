---
name: java-backend-observability
description: The logging, metrics and alerting rules for a Java backend on Spring Boot, for a deployed system nobody watches between incidents — one typed logging facade with domain types unloggable by type, compile-checked event and metric catalogs, correlation fields established by visible wrappers and captured explicitly at every virtual-thread fork, bounded metric label cardinality, and committed alert rules that each carry a fire-test. The -javaagent bytecode-weaving path, raw logger APIs with free-form messages, regex PII scrubbing in the pipeline, per-user or per-request metric labels, dashboards as the primary surface, and untested alert rules are banned by name, each with the check that fails the build. ALWAYS load before adding a log line, a metric, a tag, an alert rule, or a fan-out that logs, and before wiring telemetry or picking a logging backend.
---
# Java backend — the observability rules

**These rules bind when deployed system have no human watch it always** — no
staffed ops rota, operator come only after alert fire. **They other half of fail
loud: code that throw into channel nobody collect have fail silent.**

Skill one of three for this stack. Repo install all three:

- **`java-backend-rules`** — platform constitution. **Install with this skill**:
  fan-out context rule below is second duty on helper that skill specify, and
  its ban list is where logger bans live as entries.
- **`java-backend-api`** — HTTP contract rules. Its generic internal problem
  response carry only correlation id, and **rule that make id retrievable live
  here, not there.**

**No rule ids here. On purpose.** Each directive is `###` heading, and that
heading is how you cite it — *the weaving-agent ban*, *domain types are
unloggable*, *the fan-out context capture*. Nothing in this skill set number
these rules, so number invent here resolve only for repo that install this
skill; skill name plus subject resolve either way.

## The marker ceiling, before the rules

**One pass write this area, 2026-07-27, and it fall short of panel. Exactly one
claim in it go through adversarial panel and three refutation votes — the one
about whether logging context reach forked subtask.** Everything mark *confirmed*
below is that claim or fact panel establish while examine it. That why **two**
directives carry marker: *the fan-out context capture* and *the logging backend
is pinned*. Panel produce both — "pin backend, and do not depend on inheritance
even where it work" is one conclusion, not two findings.

Every other claim here is **primary-source verified** at best: one researcher
against vendor docs, no panel.

Pass also harvest from prior architecture decision record. **That prior art, not
independent confirmation.**

Read that as ceiling on whole area, not per-rule accident. Two consequences worth
act on:

- **These directives are convention, no external evidence sought or found:**
  autoconfiguration probe test, event and metric catalogs,
  mandatory-correlation-field contract test, error-id-resolves-to-a-log test,
  export-facts-from-database poller, and disposability of telemetry. Each state
  because it enforceable and cheap, and each mirror rule shape this stack already
  carry. **Enforcement is not confirmation.** One more claim is convention without
  its directive being so: call-site-over-pipeline half of *domain types are
  unloggable by type*, whose tool split is primary-source verified but reason for
  prevent at call site is not. Read marker beside each half, not directive whole.
- **Two *enforcement* markers get correct upward during pass** — cardinality gate
  and alert fire-test draft as **bespoke**, in fact **off-the-shelf**. Nothing
  about their *confidence* change. Record so reader who find older copy know which
  way correction go, and so correction not mistake for promotion of evidence.

Whole set is `review-by` **2027-01-21**. **Past that date every *confirmed*
marker here read as *convention*** until new pass re-date it. No maintainer
action need.

Status tier: **decided, not yet validated** — research and decide, with **no
production use yet** behind enforcement shapes.

## Two premises, and only one of them is the stack's

**This area carry premise rest of stack's rules do not**, and distinction not
pedantic — it decide who can drop these rules.

- **Stack's premise, apply here too**: code write by LLM agents, no human read it
  line by line.
- **This area's own extra premise**: **nobody watch running system between
  incidents.** Operator invoke in sessions, not staff on rota, and arrive after
  alert fire.

**Repo with staffed ops rota do not throw away this skill.** It keep every
**emission** rule — facade, unloggable domain types, catalogs, correlation
fields, cardinality bound, poller. Those **code rules** and they hold under
stack's premise alone. What it re-decide is **alerting** side — fire-tested
rules, and reasoning that reject dashboards for have no audience — against how
its rota really work.

Say which of two you drop, and carry burden of say it. Verdict portable exactly
as far as its premise.

## The defaults these rules override

Picks unbriefed agent make by statistics. **Name loser is load-bearing half.**

- **The OpenTelemetry Java agent (`-javaagent`)** — corpus favourite for
  telemetry, and **vendor's own default recommendation for most Spring Boot
  applications**, in those words. Reject as runtime-silent: JVM call agent's
  `premain` before app start, and agent register transformer that **rewrite
  classes as they load**, so effect fire from launcher flag, not from any written
  call — same grounds that ban `@Transactional`. **Cost is honest and real:**
  SDK-plus-instrumentation-libraries path cover fewer libraries and each addition
  is written dependency. That trade this rule set take, and repo should take it
  knowing.
- **Raw SLF4J with free-form message strings** — corpus-default logging call.
  Reject on two counts: alert rule or grep target free-form string **break silent
  next time agent reword message**, and raw logger's `Object...` signature accept
  domain object carrying personal data from any call site. Typed facade plus event
  catalog make both unwritable.
- **Regex scrubbing of personal data in the log pipeline** — corpus-default
  privacy control. Reject: **it run after value already leave process**, it fail
  open on any format pattern not expect, and **it report no error when it miss.**
  Type facade cannot accept never produce log line.
- **Per-user or per-request metric labels** — what agent add when ask to "make
  this observable per customer". Reject: **every unique label combination is new
  time series**, and Prometheus's own naming guidance say do not use labels for
  high-cardinality dimensions like user ids or email addresses. **Failure invisible
  for weeks, then unbounded** — exactly class absent reader make worse.
- **Dashboards as the primary surface** — corpus image of observability. Reject
  here for same reason this area condition on unwatched system: **dashboard need
  someone looking at it.** These rules target what fire without audience — alert
  rules with fire-tests, and text responder can query.
- **Alert rules committed without tests** — near-universal practice. Reject:
  **alert rule that cannot fire is gate report green over unwatched failure.**
  Fire-test is off-the-shelf, so **reason not to write one is habit.**

## Instrumentation

### The weaving-agent ban

**Instrumentation is visible program text; `-javaagent` bytecode-weaving path is
banned** — no agent JAR in image, container file, compose file, or build. Weaving
agent rewrite classes as they load, so what call do is decide by **launcher flag
instead of by call.**

*Bespoke — CI grep over launcher arguments, container and compose files, and
dependency set, in shape of `--enable-preview` grep in `java-backend-rules`.
**Not ArchUnit**, which read bytecode and cannot see launcher flags or image
layers. **Primary-source verified 2026-07-27** on both halves: agent mechanism is
vendor's own description, and default-pick status is vendor's own words.*

**Precision, and correction to tempting shortcut.** OpenTelemetry file its own
**Spring Boot starter** under "zero-code" too, **but that starter use Spring
autoconfiguration, not weaving.** So `-javaagent` grep **do not ban starter**,
and this rule must not be describe as banning "zero-code instrumentation" —
**banned thing is bytecode weaving.** That gap is exactly why next rule exist.

### Autoconfigured telemetry needs a probe test

**Telemetry register by autoconfiguration allow only where probe test assert at
startup that each meter, appender and context wrapper it suppose to register is
there.** Autoconfigured telemetry that silently fail to register leave **green
build and blind production.**

*Bespoke — one context probe test per registered component. **Convention**,
2026-07-27 — no external evidence sought or found; keep because enforceable and
cheap, and it close gap weaving ban's grep leave open.*

## Logging

### Structured JSON on stdout

**Logs are structured JSON on stdout,** from Spring Boot's own structured
logging — `logging.structured.format.console`, set in committed config.

*Config-default assertion — off-the-shelf, same shape as virtual-threads property
in `java-backend-rules`. **Check read checked-in default, not effective runtime
value**, which env vars or external config can override. **Primary-source
verified 2026-07-27** — structured logging with Elastic Common Schema and
Logstash formats ship natively in Spring Boot since 3.4 and carry forward on 4.0
line, so this is configuration, not bespoke work.*

### One typed logging facade

**One typed logging facade. Raw logger APIs, `System.out` / `System.err`, and
`printStackTrace` are banned.**

*ArchUnit — off-the-shelf for console-output and wrong-framework halves, per-repo
for third: ArchUnit ship
`GeneralCodingRules.NO_CLASSES_SHOULD_ACCESS_STANDARD_STREAMS` and
`NO_CLASSES_SHOULD_USE_JAVA_UTIL_LOGGING` as public API, and they work because
**each is type dependency**, which is what ArchUnit read soundly from bytecode.
Per-repo predicate ban direct dependency on raw logger type. **Primary-source
verified 2026-07-27.***

### Domain types are unloggable by type

**Facade take catalog keys plus whitelisted scalars and identifiers, so type
carrying personal data cannot pass to it. Log entity ids, never names or account
numbers.** Regex scrubbing in collection pipeline is **not substitute** — it run
after value already leave process.

***Error Prone read this repo source, and two other things emit log lines.* Layer
check, 2026-08-02, conversion-dated.** Check see call sites in code this build
compile. **A dependency that log a domain type do not appear there** — a client
library logging a request object at debug, a framework logging a bound parameter,
an error handler logging what it caught — and the facade cannot make a type
unloggable to code that never import the facade. **And the appender's own
configuration decide what a log line actually contain**: a pattern that render the
whole context map, a structured layout that serialise an object's fields, an
exception renderer that walk a cause chain into a domain object. Both are
configuration and a dependency, neither is source this check read. **Decidable half
be a serializer-level rule at the logging backend — a converter that refuse the
banned types wherever they arrive — which hold regardless of who call.** Not
carried here, and it be the only form that reach a dependency at all.

**Second rule set reach same split independently, and that worth stating because
nothing else here have corroboration.** `primary-keys`, published 2026-08-01 from
external records of a different pass, carry *The opaque key and the human-facing
number are two identifiers* — logs carry keys, the account number is the human and
API handle, grep namespaces stay disjoint — and *The key is what survives erasure*,
which require log lines and object-storage paths carry the key and **never a name**.
**Same verdict, different source, neither pass reading the other.** What that skill
add on top: which identifier a repo may sort on, and that a key derived from personal
data is not pseudonymous after erasure — it is the erased data, encoded. Install it
in any repo choosing a key. **It corroborate the split only**, not this directive's
tool choice.

*Error Prone on source — check itself bespoke. **Not ArchUnit**: it see logger's
erased `Object...` signature, not argument's static type, so ArchUnit rule here
**report green while protect nothing.** Tool split is **primary-source verified
2026-07-27**; call-site-over-pipeline choice is **convention** — no primary source
survive for it, and keep because type-check at compile time and fail toward
safety, where pattern that miss report nothing.*

**This rule whose enforcement `llm-default-traps` ban wrong host for.** That skill
carry ban on ArchUnit and erasure ground behind it, as cross-cutting trap that
bind any JVM repo; **this directive is rule itself.** Both need: repo with this
rule and not that skill will eventually host it in wrong tool and get green build
over unprotected type. `caching-java` record same erasure trap for its own
serialization rule, where bytecode-reading tool see erased type parameter and
decide nothing.

### Event and metric names come from a compile-checked catalog

**Event names at WARN and above, and every metric name and tag key, come from
compile-checked catalog; inline string-literal event names and meters are
banned.** Alert rules and greps target these names, so **they API, not prose** —
same argument as error-code catalog in `java-backend-api`.

*ArchUnit ban on inline literals at facade call sites — per-repo predicate — plus
committed catalog snapshot diff each build, in shape of that skill's
error-catalog snapshot. **Convention**, 2026-07-27.*

### Every scoped log event carries the correlation fields

**Every log event emit in request-scoped or task-scoped code carry correlation
fields,** establish by same visible wrappers that establish rest of scope —
**never by ambient interceptor.**

*Bespoke — contract test assert mandatory fields on every event emit inside
scoped block. **Convention**, 2026-07-27.*

### The correlation id in an error response resolves to a log event

**Correlation id in error response is id in logs.** HTTP contract's generic
internal problem carry **only** correlation id, and **id that retrieve nothing
turn that rule into dead end.**

*Bespoke — test read id from 500 response body and assert matching log event
retrievable by it. **Convention**, 2026-07-27. Rule on other side of this seam is
*one advice builds every error body* in `java-backend-api`; neither useful
without other.*

### The logging backend is pinned

**Logging backend is pinned in build, and Logback is default pick.** Correlation
rules turn on **whether backend's context map inherit by child thread, and that
answer differ per backend**: Logback not inherit it since 1.1.5 and offer **no
switch**; Log4j 2 inherit **only when system property set**; JUL and reload4j
bindings **inherit by default.** Unpinned backend make guarantee unpinned too.

*Banned-dependency rule — off-the-shelf, in same enforcer configuration as
platform bans. **Confirmed 2026-07-27** for per-backend inheritance facts, as part
of fan-out context panel below.*

### The fan-out context capture

**Owned virtual-thread fan-out helper establish each subtask's logging context at
fork time, and never rely on inheritance to carry it.**

**Three grounds, and rule stand on any one of them.**

1. **Scoped Value never cross.** Bindings inherit only by threads fork in
   `StructuredTaskScope`, which `java-backend-rules` ban as preview.
2. **Logback's context map never inherit by child thread**, and no configuration
   restore it — 2016 change remove inheritance outright, not make it
   configurable, and proposed flag never ship.
3. **And where backend *can* inherit, depend on it still wrong.** What log call
   record would then turn on ambient system property **and** on which thread
   happen to construct child — and platform specify neither for per-task
   executor. That ambient modifier decide behaviour, class these rules exist to
   remove, **so capture stay explicit even on backend that would inherit.**

**Without it, every subtask log line silently lose its correlation fields:**
missing key render as empty string and throw nothing, so no compiler, linter or
runtime error catch it. **Only assertion do.**

*Bespoke — capture live in one owned helper, and test assert subtask's log event
carry forking thread's correlation fields. **Confirmed 2026-07-27 under
three-vote adversarial panel — this the one claim in this area that have one**,
and panel correct claim's wording in process. Off-the-shelf mechanism, if repo
prefer it to hand-written copy: Micrometer `context-propagation` executor
wrapping — but **register SLF4J accessor programmatically, it not discover
automatically**, and note it cover context map only, **never Scoped Value.** See
[evidence.md](evidence.md) for why hand-written capture is more
principle-consistent route and what else do *not* do this for you.*

## Metrics and alerts

### Metric label cardinality is bounded and budgeted

**Label whose value set not O(1) — user id, request id, correlation id, unbounded
path — is banned; label bounded by known small set is allowed and its ceiling
state in repo.**

*Off-the-shelf on **both** sides: Micrometer's `MeterFilter`
maximum-allowable-tags bound with deny action at runtime, and Micrometer's
high-cardinality-tags detector (`withHighCardinalityTagsDetector()`) run as
one-time check in test over registry after app exercised — form its own
documentation support for verify instrumentation. **Primary-source verified
2026-07-27.** **Detector document no default threshold — repo set it**, and no
number supply here.*

### Database facts are exported by one poller

**Facts already record in database export by one explicit poller, never
re-instrument in write path.** Counter increment beside row it count **drift from
that row on every rollback and retry.**

*Convention, 2026-07-27.*

### Alert rules are committed code with a fire-test

**Alert rules are committed code, and each carry fire-test:** rule fire at its
threshold plus margin and **stay silent below it.** Rule that cannot fire is
**gate report green over unwatched failure.**

*Off-the-shelf host — `promtool test rules` and its `alert_rule_test` form,
**including empty-expected-alerts case for must-not-fire**; fixtures author per
repo. Rule-file validation step run in CI. **Primary-source verified 2026-07-27**.*

***A rule that fire in a test and a rule that reach somebody are two claims.* Layer
check, 2026-08-02, conversion-dated.** Fire-test read the committed rule file and
prove the expression fire at its threshold. **Whether anything happen then be
decided outside this repo entirely** — and the mechanisms have names, cuz the host
above is `promtool`, so the delivery side is **Alertmanager**: a **silence**, an
**inhibition rule**, a **route** whose matchers drop the label set, a **receiver**
whose credential expired. Each be a configured object, none be in a rule file, and
`promtool test rules` validate none of them. **Under this skill's own premise the alert is the whole channel** —
no staffed rota, operator come only after alert fire — so a silenced rule is the
exact failure this directive exist to prevent, with a green fire-test beside it.
Two published rules already say what to do about state like this and neither cover
it: `ai-maintainer-principles` require **every operational surface, alert rule named
in its own list, be committed text the build read**, and `guardrails-toolchain`
require a gate state the environment its claim hold in. **Decidable half be
committing the routing and silence configuration alongside the rules and diffing
it**, which make a silence a git-visible line rather than a console action. Not
carried here.

### Telemetry is rebuildable, disposable data

**No correctness rule, audit claim, or business record depend on telemetry; audit
trail is transactional tables.**

*Convention, 2026-07-27. Trimmed 2026-08-12 — desk pro-default, 2026-08-11
audit; kept for the phrase ownership below and its live re-open trigger — fire
moment someone propose read business answer out of telemetry.*

**This directive own phrase "rebuildable-cache premise" in this skill set.**
`caching` deliberately say **"derived-store premise"** for store rebuildable from
authoritative store, precisely to avoid redefine this one — different properties:
yesterday's histogram not recomputable from database, derived store is. Redefine
the phrase and this directive's re-open trigger turn incoherent; collision
invisible from either side, why it record here.

## Wiring the gates

**Run this once per repo, in first pull request that emit telemetry.** These
directives are two kinds weld together: instinct-overrides that fire while agent
write log line, and build gates that must exist in repo. **Gate is what catch
next agent**, and unwired gate is rule describe as enforced that is not.

1. **The weaving-agent CI grep** over launcher arguments, container and compose
   files, and dependency set. Not ArchUnit.
2. **A config-default assertion** for structured-logging format. It read
   checked-in default and see no runtime override.
3. **ArchUnit rules** on platform ban list's test class: standard-stream and
   wrong-framework rules off shelf, raw-logger-type dependency ban, and inline
   event-name and meter-name literal bans.
4. **Error Prone** as host for unloggable-domain-type check — **and explicit note
   that ArchUnit is not host**, so next agent not add one there.
5. **The event and metric catalog snapshot**, generate from catalog and diff each
   build.
6. **The banned-dependency rule pinning the logging backend**, in same enforcer
   configuration as platform bans.
7. **The context capture inside the owned fan-out helper**, plus test assert
   subtask's log event carry forking thread's correlation fields. If repo use
   off-the-shelf executor wrapping instead, **register accessor programmatically**
   and record that Scoped Value not covered.
8. **Micrometer's `MeterFilter` maximum-allowable-tags bound with a deny
   action**, and `withHighCardinalityTagsDetector()` as one-time test over
   registry after app exercised. **Repo state threshold** — detector document no
   default.
9. **Probe tests**, one per autoconfigured component, assert registration at
   startup.
10. **The contract test** for mandatory correlation fields inside scoped block,
    and **the test** that read correlation id from 500 response body and resolve
    it to log event.
11. **The alert-rule fire-tests** and rule-file validation step in CI, include at
    least one must-not-fire case express as empty expected-alert list.

**Then record what was wired and what was skipped, with reason.** These entries
**nothing above gates**, and each must list as ungated:

- **The call-site-over-pipeline privacy argument.** Error Prone check gate what
  facade accept; that no other path log domain type depend on facade being only
  logging path, which ArchUnit rules cover only as far as their predicates reach.
- **The database-export poller.** Convention. Nothing detect counter increment in
  write path beside row it count.
- **Telemetry's disposability.** Convention, and unenforceable by construction —
  it constraint on what future rules may depend on, not on any code that exist
  now.
- **Whether the alert thresholds are right.** Fire-test prove rule fire at its
  threshold; **nothing prove threshold is right one**, and fire-tested rule with
  threshold nothing reach is still gate report green.
- **The cardinality ceiling for each allowed label**, which repo state in prose.
  Runtime deny action bound total; it not check any individual label against
  stated ceiling.

**Record that list only what was wired read as complete coverage.** That failure
this step exist to prevent.

## Named gaps — where no check reaches

Silence read as coverage, so each one state.

1. **Config-default assertion is not runtime assertion.** Structured-logging
   format read from committed config; env var or external config source can
   override it in deployed process and **no gate here notice.** Same limitation
   apply to virtual-threads property in `java-backend-rules`.
2. **Weaving-agent grep do not ban OpenTelemetry Spring Boot starter, and should
   not be describe as banning zero-code instrumentation.** That starter use Spring
   autoconfiguration, not weaving, and vendor file it under "zero-code" too.
   Probe-test rule is what cover its failure mode, and it convention.
3. **Nothing here bound what log line cost.** No rule about volume, sampling, or
   retention, and unbounded-cardinality *log field* — as opposed to metric label —
   not cover by cardinality rule at all.
4. **Fire-test prove rule can fire, not that it should.** Threshold correctness
   outside every gate here.
5. **Distributed tracing deliberately absent, not overlook.** This area ship
   correlation-id-only. Reason and adoption trigger in
   [evidence.md](evidence.md), together with status claim about relevant standard
   that **must not be cite as settled.**
6. **Only one claim in this area survive panel**, and two directives it produce
   are only ones carry *confirmed*. Everything else is documentation check or
   design argument, which is ceiling state at top of this file and repeat here
   because it gap in ordinary sense: **for every directive other than those two,
   reader looking for independent verification find none.**
7. **High-cardinality detector need app to have been exercised.** It run over
   registry after test drive application, so it see labels that test produce and
   nothing about code path no test reach.

## Markers, dates, and what they mean

Confidence, per claim: **confirmed** mean claim survive three independent
refutation votes against primary sources on date it state — **one claim here have
that.** **Primary-source verified** mean one researcher check it against primary
source with **no panel**; it not confirmed whatever its evidentiary strength, and
run panel is what promote it. **Convention** mean research did not, or could not,
confirm claim from independent sources; rule keep because enforceable, cheap, and
fail toward safety.

Enforcement, per rule: **off-the-shelf** mean tool do it with configuration;
**bespoke** mean check must be written; **convention** mean human or agent assert
it is all there is.

**Lapse rule:** past `review-by` **2027-01-21**, every *confirmed* marker in this
skill read as *convention* until new pass re-date it. No maintainer action need.


Ground behind each claim — with its sources — claims that must **not** be cite,
and conditions that reopen rule are one hop away in
**[evidence.md](evidence.md)**.