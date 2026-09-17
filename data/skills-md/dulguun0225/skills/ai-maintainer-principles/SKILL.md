---
name: ai-maintainer-principles
description: The architecture and process rules a repo commits to because its maintainer is an LLM agent rather than a person — startup-loud magic allowed and runtime-silent magic banned, whole-program reasoning designed out, operational state in the repo, a module sized to one session, topology by the number of independent wills rather than services, one idiom imposed mechanically, a steering human who is not a reviewer, a fresh-context adversarial pass as the review substitute, a predecessor system as inventory and never oracle, zero retries and a quarantine that cannot rot, dependencies priced by failure shape, and a safety argument beside every hand-built subtle piece. Carries one repo's worked case — the corpus favourites it rejected, each named with the ground it lost on — and the verdict on every shape a repo assembles out of two of these primitives — a module two wills push on, a dependency that brings its own idiom, a quarantine that lives in a console, a predecessor still serving traffic. ALWAYS load before drawing or moving a module boundary, choosing a runtime topology, deciding what a build gate may be relaxed for, adopting a framework, database, managed service or vendor API, writing a retry or an error handler, writing a piece of code subtle enough to need a safety argument, introducing a second way to do something the repo already does, migrating from an existing system, or writing a repo constitution.
---
# Rules for a codebase whose maintainer is an agent

**This skill about decisions that change answer *because* maintainer is an LLM
agent, not a person.** Not how to write a rule — that `enforceable-rules`. Not
which stack — `backend-stack`. Not which gates — `guardrails-toolchain`. This one
about **shape of system those rules bind**: what maintainer can see, how system
cut, what stand in for review, what maintainer able to do alone.

**Two halves.** Directives portable — hold on Go, .NET, TypeScript same way.
Worked case = one repo's decisions, dated **2026-06-11..14**, plus two
re-derivations that repo ran under changed premises. Worked case there as
*evidence directives discriminate*, not template to copy.

## The marker ceiling, before anything else

**Everything here is *convention*.** Source = one org's architecture decision
records, written 2026-06-11..14 by pass that ran adversarial agent panels and
recorded verdicts. **Records carry no per-claim confidence marker and cite no
primary source for any claim in them.** So *convention* is floor, and what
generalise below is reasoning, never measurement.

- **Central claim is *uncertain*, not convention**: that these decisions come out
  different under agent maintainer than under human team. **Nobody built same
  system both ways.** Records argue premise-sensitivity and two of them re-derive
  under a changed axiom — argument, and good one, with no outcome behind it. Marked *uncertain* where it appear.
- **Lapse rule vacuous here, stated not hidden.** Past `review-by` every
  *confirmed* marker read as *convention* with no maintainer action; nothing here
  above convention, so rule demote nothing. Stated cuz every sibling carry
  `review-by` and silence read as omission. **Cost: nothing make this skill's age
  visible.** Conversion date **2026-08-01** — conversion date, not verification
  date.
- **No date invented.** Directive carry date of record that ground it. Where
  directive state something no record wrote in that form, date is conversion date
  and say so.

Status tier: **decided, not yet validated** — researched and decided, **no
production use yet**. One repo build against these; none run long enough to report
whether any of them predicted anything.

## The premise, and the two failure modes under it

**Code written by LLM agents. No human read it line by line.**

Every sibling skill state this premise. Directives here hang on **second half**,
which the records state and no skill had carried as a premise before this one —
`backend-stack`'s evidence file now narrate it as prior art, and that the only other
place it appear:

- **Runtime behaviour absent from program text is invisible to maintainer in
  absolute sense.** Agent simulate framework behaviour from training corpus rather
  than observe it, and **simulation error pass unit test and fail silently in
  production**. Human maintainer read same file and no better off in principle —
  difference is human attach debugger, watch process, ask colleague. Agent's whole
  sensory channel is committed text plus what build print.
- **Context locality is characteristic failure mode.** Maintainer see one file at
  a time. **Any correctness requirement demanding whole-program reasoning degrade
  across sessions** — not once, continuously, cuz every session start over.

Human team drift toward same failures slower and recover from them by talking.
Neither recovery exist here. **Verdict travel exactly as far as premise:** repo
where person read every diff should re-derive most of this and will get different
answers on several.

## What the maintainer cannot see

### Startup-loud magic is acceptable; runtime-silent magic is banned

**Discriminator, not blanket ban. Magic that make app fail to boot is caught by
first integration test, always. Magic that silently change runtime semantics have
no reliable gate.** Constructor wiring resolved at startup, route registration,
typed configuration binding: acceptable, cuz failure is total, immediate and
reproducible in every run. Proxy that skip transaction on self-invocation,
persistence context that flush on read, cache that serve stale value, aspect woven
at load time: banned, cuz failure is partial, conditional and silent.

**This is the allowance half, and it what stop the ban becoming useless.** Repo
that ban "magic" as category ban its own dependency injection, then relax ban
informally, and now nothing is banned. Repo that state discriminator can ban
by mechanism, one by one, with check per mechanism.

**Third branch, and it the one repo skip: accepted runtime trust, priced.** Some
machinery is neither boot-failing nor bannable, cuz hand-rolling replacement is
worse code than trusting library — a security filter chain, an at-least-once event
registry that persist inside caller's transaction. **Those get accepted one at a
time, each with named standing test pinning contract** — kill process between commit
and handler, assert redelivery; test authorization outcome per endpoint rather than
belief that config is right. **Accepted-and-tested, never accepted-and-assumed**;
piece with no such test is runtime-silent wearing an exception.

`enforceable-rules` own the ban half as *No silent runtime behaviour*, with reason
naming mechanisms beat naming category; `java-backend-rules` carry the list for
one stack. **Neither state why the boot-time cousin is fine**, and repo that no
state it will either over-ban or under-ban.

*Check: every accepted piece of framework machinery carry written line saying which
of three classes it in, and each runtime-trust piece name its standing test.
Convention as enforcement for classification — written artifact, absence visible,
cannot catch wrong classification; **off-the-shelf** for the standing tests
themselves. **Convention**, 2026-06-12.*

### Design out any requirement that needs whole-program reasoning

**Where correctness depend on facts spread over files — flush ordering, proxy
reach, cache coherence, lock ordering, initialisation order — requirement is not
documentable. It must be made structurally impossible or accepted as permanent
defect source.** Document it and every session re-derive it from one file, wrong.

**Practical form is question asked before adopting a construct:** to know this
line correct, how many files must be read? Answer above one is design input, not
trivia. Construct whose semantics live at call site survive session boundary;
construct whose semantics live in relationship between a session, an object's
dirty state and a flush point no survive it.

Under human review this cost is real too and pay for itself in expertise that
accumulate in people. **Here nothing accumulate** — every session is first
session — so cost is charged every time and never amortised.

*Check: each rejected construct's record name the whole-program fact it require.
Bespoke and mostly unbuilt — architecture test assert absence of specific named
construct, nothing assert reasoning span. **Convention**, 2026-06-12.*

**Worked instance, 2026-08-02, conversion-dated — this directive caught a
draft that violated it.** The composite-shape check on `business-numbering` found a
repo can hold **two contended rows in one transaction**: a numbering counter row,
and the mutable balance row `money-storage` `M-39` permits. Two transactions taking
them in different orders deadlock. **The draft answer written into three skills was
"decide one lock order and write it down"** — which is this directive's own named
example of the thing that cannot be documented, published in the same skill set.
Rewritten to the two answers this directive allows: **remove the second contended
row** — `money-storage` `M-38`'s append shape has none — or **confine every such
transaction to one named operation that takes both in a fixed order**, so no call
site chooses. **The instance is recorded because the directive's abstract form did
not stop the defect and its named example did.**

### Operational state lives in the repo or it does not exist

**Every operational surface — schema, topic, ACL, alert rule, cron, feature flag,
connector config — is committed text the build read, or it is state maintainer
cannot reason about.** Console change is unreviewable by construction and leave no
trace in repo; infrastructure needing its own out-of-repo control plane cost more
here than its feature list suggest, and that cost belong in the choice, not in the
incident afterward. Trimmed 2026-08-12 — desk pro-default, 2026-08-11 audit (GitOps
mainstream); kept for its check and the composite shapes that lean on it.

*Check: every operational surface have committed artifact and gate that diff it;
surface with no artifact listed as gap. Off-the-shelf per surface — migration
lint, alert-rule test, committed ACL diff. **Convention**, 2026-06-12.*

## How the system is cut

### A module is what one session can hold, and no larger

**Module must be fully understandable — schema, API, invariants, tests — inside
one session's context. Too big to load is as mis-drawn as too small to mean
anything.** Both directions are boundary defects and only one of them get noticed.

This is boundary criterion that human-team literature no have, and it **added
beside the usual ones, never instead of them** — information hiding, bounded
context, one capability, common closure, transactional consistency, exclusive data
ownership, coupling balance. Criterion here rank *loadability*, and it can be
violated by module that pass every other test.

**Relief valve matter more than criterion**, cuz obvious cure is wrong one:
oversized module split into two top-level modules trade loadability problem for
coupling problem, and coupling problem is worse — it permanent. **Cure is named
nested sub-module inside same module**: own table prefix, own API package,
boundary test pinned to it. Sub-module already own its tables and its API, so later
promotion to top level is cheap if named trigger ever fire.

**Names must bind mechanically.** Package name, artifact name, module name one-to-
one, so boundary test key off name with no translation table. Translation table is
one more whole-program fact.

*Check: boundary test assert declared module set and its nesting; module over
budget commit its sub-module map before its build milestone. Off-the-shelf for
boundary test, **convention** for budget itself — nothing measure "fits one
session". **Convention**, 2026-06-12.*

### Count the independent wills, not the services

**Topology question is how many independent wills push on codebase. One will:
in-process boundary unbeatable — coordination cost near zero, consistency free,
cross-module break caught at compile. N wills: network boundary start buying
something real, cuz contracts let teams stop talking.**

**Parallel agents are not N wills.** They share one codebase perfectly, have no
release politics, and benefit maximally from whole-system compile-time checking.
Argument that "AI works like many people, so build like many teams" invert the
conclusion: microservices were invented for human organisation problem — independent
teams that cannot share codebase or deploy cadence, accepting runtime failure as
price of autonomy. **Adopt them for agents and you pay coordination tax of human
teams without having human teams.**

Decisive half is where failure surface. One compiled codebase: cross-module break
fail build before merge, detection instant and free. Separately deployed services:
same break become runtime contract failure between versions, surfacing in an
environment. **Under premise build is the review**, so moving failure off compile
path weaken exact mechanism substituting for reviewer.

What enable parallel work is **enforced ownership boundary, not network boundary**
— typed module API, no cross-module data access, violation fail build. Agents work
those boundaries concurrently in one repo today.

**Direction asymmetric, and that why this decided early:** start as one deployable
and extract on named trigger is routine; start as N and merge back never happen.
So record split trigger and extraction procedure at start, and let trigger fire.

*Check: record state will count and name split triggers with extraction procedure;
boundary tests exist from first commit, cuz they what keep later extraction cheap.
Convention as enforcement — written artifact. **Convention**, 2026-06-12..13.*

### One idiom, imposed mechanically

**Second dialect for same job is standing session-drift generator. One idiom
everywhere is self-stabilizing; boundary between two is not, cuz boundary itself
is whole-program fact each session re-derive.** Two persistence dialects, two error
shapes, two test styles, two formatting conventions — each cost is not the second
idiom, it is the *judgment call about which applies here*, made fresh, differently,
every session.

Human team converge by habit and by reading each other's code. **Neither mechanism
exist here**, so convergence must be mechanical: deterministic zero-configuration
formatter that fail build on unformatted file, and canonical-form rewriting where
ecosystem offer it, so equivalent constructs collapse to one shape before they
accrete.

**This is why a "flexible" convention cost more than a rigid one here** — cost of
rigidity is occasional worse line, and it paid once; cost of flexibility is a
decision re-made every session, and it compound.

*Check: formatter run in build with fail-on-diff, zero per-file configuration;
where two dialects genuinely required, boundary is enforced by test, never by
convention. Off-the-shelf — formatter and canonical-form rewriter both fail a
build; **`guardrails-toolchain` carry the canonical-form rewriter's row and no
formatter row, and no skill in this set carry one — re-runnable as a grep for
`Spotless` and `palantir-java-format` across `skills/`, clean 2026-08-02**, stated
that way by the enumeration check because a cross-document superlative a reader
cannot re-check is a count in disguise. **Convention**, 2026-06-12..13.*

## The review model

### A human who steers the agent is not a code reviewer

**Person who direct agent, read its summaries, accept its demos do *requirements*
review. That never a substitute for a gate, and their presence never a reason to
relax one.**

Trap is specific and it arrive as reasonable sentence: *the owner looked at it, so
relax the gate*. Owner looked at behaviour, spec, demo. **They will not catch a
rounding-mode drift, a swallowed exception, a cache serving stale money any better
than nobody**, cuz they never read the line. Humans add better specs and faster
acceptance. They no add second reader.

**Rule bind hardest exactly when org grow**, cuz that when people appear beside
agent and premise look weaker than it is. Premise is about *line-by-line reading*,
and it hold until somebody actually do it, on every diff, as their job.

`enforceable-rules` state converse from rule-authoring side: repo where human truly
read code may weaken gates, and that repo carry burden of saying so. **This is same
line seen from org side, and pressure comes from here.**

*Check: repo state who read code line by line, by role, and gate relaxation cite
that statement. Convention as enforcement — written artifact, catch omission, cannot
catch wishful claim. **Convention**, 2026-06-13.*

### The review substitute is a fresh-context pass with a committed verdict

**Where no human read code, review substitute is adversarial pass run in fresh
context, given diff, spec and rules and *none of authoring history*, returning
structured verdict committed to repo.** Three properties load-bearing, and dropping
any one make it theatre:

- **Fresh context** — reviewer sharing authoring session share its assumptions and
  ratify its own reasoning.
- **Inputs only** — diff, spec, rule set, defect-class checklist. Authoring
  rationale is exactly what must be re-derived, not read.
- **Committed verdict** — skipped or softened review is invisible unless its output
  is artifact in repo. Verdict in repo make omission a diff.

**Honest limit stated with it, always: reviewer share author's model**, so its
misses correlate with author's misses. Backstops carrying real weight are gates
that **no share that model** — mutation testing that probe whether tests assert
anything, goldens from worked examples a person computed and validated, invariant
suites over real data. **Change on a value-bearing path is done when those pass
*and* verdict is approve** — that conjunction is what the record scope to its money
paths, and widening it past them is this skill's choice, not the record's.

`guardrails-toolchain` own the harder half of same seam — **non-deterministic
reviewer never sole arbiter of mechanical defect class**, and its finding in such
class is trigger to build a gate rather than a disposition. Install it; this
directive only say what positive shape of review substitute is.

*Check: verdict schema committed, verdict file required per change, inputs list
pinned in process document. Bespoke — file presence greppable, reviewer's blindness
not. **Convention**, 2026-06-14.*

### A predecessor system is an inventory, not an oracle

**Old system document what capabilities exist. It never ground truth for what
correct behaviour is, and no test may assert parity with its output.** Oracle is
worked example somebody computed by hand and a person validated.

Passes `enforceable-rules`' *gates need an outside oracle* by letter — predecessor
output *is* outside authoring model — and fail it in substance, cuz **oracle's
authority come from being right, not from being external**. Legacy output encode
every bug nobody found. Under premise, agent that find predecessor will treat it as
specification, cuz it the most specification-shaped artifact available, and
resulting parity fixture lock in behaviour nobody ever chose.

Keep predecessor as capability checklist: what business does, what must be ported,
replaced, or consciously dropped. **Record dropped ones**, else next session
re-import them as gaps.

*Check: no test compare against predecessor output; capability map exist and mark
each item ported, replaced or dropped. Off-the-shelf — absent fixture layer is
greppable. **Convention**, 2026-06-12.*

### Zero retries, and a quarantine that cannot rot

**Test never retried to green. Flaky test quarantined explicitly, in committed file
with owner and expiry, and named set never quarantinable at all** — isolation
probes, money invariants, crash-recovery.

Retry is cheap everywhere and expensive here. **Build is only signal, so retry
convert the signal into noise**, and noise train reader — human or agent — to
disregard the one mechanism substituting for review. Retried flake also hide real
concurrency defect exactly where they cost most.

**Quarantine file must be structurally un-rottable**: entry carry expiry, and build
fail when entry outlive it. Quarantine list with no expiry become permanent
disable list within a quarter, and its green build is a false green
`enforceable-rules` warn is worse than no gate.

*Check: runner configured with zero retries; quarantine file schema-checked, expiry
enforced in build, non-quarantinable set listed by name. Off-the-shelf for retry
setting, bespoke for expiry gate. **Convention**, 2026-06-14.*

## What the maintainer must be able to do alone

### Price the bus factor by failure shape, with an exit ladder

**For every load-bearing dependency, price abandonment once, deliberately, by
*shape* of failure rather than by likelihood — and record exit ladder cheapest step
first, with the trigger that step down it.**

Shape is what maintainer control; likelihood is what nobody know — a compile-time
dependency with committed generated output freeze benignly where a runtime
framework in the request path do not, and popularity metrics mislead across
ecosystems. That half trimmed 2026-08-12 — desk pro-default, 2026-08-11 audit;
the concession below already say why.

Ladder is where premise bite: **steps must be ones an agent can execute**. Freeze
and pin, then fork and apply targeted compatibility patch, then migrate
incrementally behind a seam already in the code. Step requiring a team, a rewrite,
or standing operational judgment is not an exit — it is an outage with a plan
attached.

**Weakest directive here on premise-specificity, and it say so rather than dress
up.** Pricing dependency risk is ordinary engineering, sensible in any repo. Only
ladder-executability clause turn on the premise — and **that clause is this skill's
addition, not something a research pass wrote or tested**, which its check line
date record. Kept anyway cuz it cheap and fail safe; **read it as *convention* in
the strict sense `enforceable-rules` mean, no as premise-derived rule.**

*Check: each load-bearing dependency's record state failure shape, ladder, and
trigger to step down. Convention as enforcement — written artifact. **Convention**,
2026-06-12, and ladder-executability half **2026-08-01**, conversion-dated
statement of what record's steps were chosen by.*

### A hand-built subtle piece ships with a safety argument and a stress test

**Where repo hand-build something subtle — concurrency control, crash recovery,
gapless counter, retention sweep, compensation logic — piece ship with written
safety argument in its record *and* dedicated stress test. Without both it not
done.**

Build-versus-buy corollary, and it exist cuz **hand-built subtle code is precisely
what an unreviewed agent write most confidently and most wrongly**. Library got
adversarial users; this got one author simulating concurrency in its head.

Safety argument is not a comment. It the enumeration of interleavings, crash points
and failure modes considered, written where next session read it — else next
session re-derive it, differently, from one file.

**Test must be stress-shaped, not example-shaped**: injected crash between commit
and acknowledge, contention at real parallelism, volume above the sweep's cap.
Example test over hand-built concurrency is false green.

*Check: rule list constructs classed subtle; each carry record section and named
test class; meta-test assert every listed construct have both. Bespoke.
**Convention**, 2026-06-12.*

## The worked case — one repo, 2026-06-11..14

**One org's decisions, kept as evidence the directives above discriminate. Not
template.** That repo is a single multi-tenant financial backend, agent as sole
maintainer, no operations role, no human code reader. **The decision-by-decision
table, and the two counterfactuals that re-derived it under changed premises, are
in [evidence.md](evidence.md).**

**What it rejected, by name, and the ground each lost on** — the half that override
an instinct rather than record a choice:

- **Hibernate ORM and Spring Data JPA**, rejected for jOOQ **even in a stateless
  profile** with no persistence context, no dirty checking, no lazy loading and no
  cascades. Load-bearing pair of grounds: corpus gravity toward the banned idioms,
  and the silent `UPDATE` that any lapse back into the stateful API reintroduces.
- **`@Transactional`**, banned — and `DSLContext` made reachable only as the lambda
  parameter of a transaction wrapper, so a query outside a transaction is
  **unwritable** rather than merely banned.
- **Retries**, zero, against an un-rottable quarantine file and a named
  non-quarantinable set.
- **Kept instead of banned, and priced for it:** Spring Security and the Modulith
  event registry, each held as runtime trust pinned by a standing test —
  per-endpoint authorization probes, and a kill-between-commit-and-handler
  redelivery test.

**One directive the worked case half-fails, stated because silence would read as
coverage.** jOOQ's single-maintainer vendor was priced once — health signals,
failure shape, three-step exit ladder, trigger to step down. **The repo's other
load-bearing dependency, Spring, was never priced this way**, which is exactly what
*Price the bus factor by failure shape*'s own runtime-framework clause predicts.

*Check: none — this a record of decisions, not a directive. Grounds **convention**,
2026-06-11..14.*

## Wiring the gates

Run once, in a repo adopting this skill. Record what got wired and what got skipped
with reason — skipped item with no reason read as done by next session.

1. **Boundary tests from first commit** — declared module set, nesting, allowed call
   direction, no cross-module data access. Cheap now, unaffordable later, and they
   what make extraction cheap if a split trigger ever fire.
2. **Formatter with fail-on-diff, zero per-file configuration**, plus canonical-form
   rewriting where the ecosystem host it.
3. **Zero retries in the test runner**, quarantine file with schema and expiry gate,
   non-quarantinable set listed by name.
4. **Verdict artifact required per change** — schema committed, path fixed, absence
   fail the change.
5. **One committed artifact per operational surface**, each with its diff or lint.
   Surface with no artifact goes on the gap list, named.
6. **Meta-test over the subtle-piece list** — every construct declared subtle have a
   record section and a named stress test, both directions reconciled.
7. **Record, in repo, who read code line by line, by role.** Empty is the honest
   answer in most repos here, and it what every gate relaxation must cite.

**Which of these fail a build off the shelf, stated per step rather than by range:**
boundary tests, the formatter and canonical-form rewriter, the retry setting, the
operational-surface lints, and the absent-fixture grep. **Bespoke:** the quarantine
expiry gate, the verdict-artifact requirement, the subtle-piece meta-test. **Step 7
gates nothing by itself** — it is a written artifact every gate relaxation must
cite.

## Composite shapes a repo assembles out of these primitives

**`enforceable-rules`' composite-shape check, run 2026-08-02, conversion-dated.**
Directives above govern a module, a sub-module, a will, a topology, an idiom, a
gate, a review pass, a dependency, a quarantine, a subtle piece and an operational
surface. **A repo build things out of two of them, and this skill decided none of
those.** Every entry marked; **silence about a shape is a defect in this section.**
The table promote no marker and add **no ban** — every entry resolve to a condition
or to an honest blank, cuz a ban here would remove a system shape from every future
repo on grounds this skill's own central claim mark *uncertain*.

| Shape | Verdict |
| ----- | ------- |
| **One module, two independent wills** | **permitted with conditions, and this is the composite of the two central directives.** *A module is what one session can hold* size the module; *Count the independent wills* say N wills buy a network boundary. Neither say whether **the module is the unit of one will.** Condition, stated here for the first time: **a module with two wills pushing on it is a topology decision that has not been taken yet**, not a boundary that happen to be shared — and the loadability criterion cannot see it, cuz a two-will module load exactly as well as a one-will one |
| **A nested sub-module that is itself over budget** | **permitted with conditions.** The relief valve is *a named nested sub-module inside the same module*, and nothing say whether it apply again. Condition: **nesting deeper than one level is the coupling problem the valve exist to avoid, arriving inside the module instead of between two** — at that point the named promotion trigger fire and the sub-module become a top-level module |
| **An adopted dependency that bring its own idiom** | **permitted with conditions, and the condition is the one *One idiom, imposed mechanically* do not state.** That directive govern idioms the repo choose; a client library, a date type, a concurrency model or a test style arrive **with** a dependency and are not chosen separately. Condition: **the idiom a dependency impose is priced in the adoption decision, beside the bus-factor price** — a library that force a second dialect is a standing drift generator with a version number |
| **A quarantine that lives in a broker, a dead-letter queue or a platform console** | **banned by *Operational state lives in the repo*, and neither directive said so.** *Zero retries, and a quarantine that cannot rot* require the quarantine be inspectable and worked; the operational-state directive require every surface be committed text the build read. A quarantine in a console satisfy the first while being exactly the state the second say the maintainer cannot reason about. **Restated as a shape because each directive read as satisfied on its own** |
| **A predecessor system still running during a migration** | **permitted with conditions, and nothing here state them.** *A predecessor system is an inventory, not an oracle* govern it as a **source of requirements**; while a strangler migration run it is also a **load-bearing dependency**, which *Price the bus factor* govern. Condition: it carry both readings at once — inventory for what the new system must do, priced dependency with an exit ladder for as long as it serve traffic — and **the second one is the reading a migration plan forget** |
| **A hand-built subtle piece inside a nested sub-module** | **permitted** — *A hand-built subtle piece* attach its safety argument and stress test to the piece, not to the module, so nesting change nothing. Marked because the module rules are about what one session hold and a subtle piece is exactly what a session hold badly |
| **An operational surface owned by a third party** | **permitted with conditions, already half-stated.** *Operational state lives in the repo* accept openly that infrastructure with its own control plane cost more; what it do not say is what the repo commit instead. Condition: **the repo commit the desired state and a gate that diff it against the vendor's actual**, or the surface is listed as a gap — the same two honest outcomes `guardrails-toolchain` require of a quarantined gate |
| **A gate relaxed by build configuration rather than by a person** | **banned, and the ban is `guardrails-toolchain`'s.** *A human who steers the agent is not a code reviewer* forbid a person relaxing a gate; a continue-on-error step, a warning severity or a required-check list that omit the job do the same thing with nobody to forbid. That skill's layer clause on branch protection own this from its side |
| **The review substitute run by the author's own model** | **banned, and already stated** — *The review substitute is a fresh-context pass* require gates that do not share the author's model. Restated because the fresh-context half is the memorable half and the different-model half is the load-bearing one |

## Named gaps — where no check reaches

- **The applicability predicate was framed on artefacts this skill's own directives do
  not all govern — widened 2026-08-02 by `enforceable-rules`' predicate check.** The
  load trigger named drawing a module boundary, choosing a topology, relaxing a gate,
  adopting a framework whose behaviour is not in the program text, and writing a
  constitution. **Five directives govern acts none of those describe**: writing a
  retry or an error handler (*Zero retries*), writing a subtle piece (*A hand-built
  subtle piece*), adopting a database, vendor API or managed service that is not a
  framework and whose behaviour **is** in the program text (*Price the bus factor*),
  introducing a second way to do something (*One idiom*), and migrating from an
  existing system (*A predecessor system is an inventory*) — **which had no trigger at
  all.** Trigger widened; the directives are unchanged.
- **Three directives quantify over a set given by example, and the examples are the
  definition** — *every operational surface* (schema, topic, ACL, alert rule, cron,
  feature flag, connector config), *every load-bearing dependency*, and *anything
  subtle enough to need a safety argument*. **A repo with a surface outside the list
  gets a green check and an unreasonable-about state**, which is the same failure
  shape as `primary-keys`' surface enumeration. **Naming the check that would close it
  is the honest move and it is not carried here**: an inventory of every out-of-repo
  control plane the deployment touches, generated from the deployment rather than
  listed by hand.
- **"Fits one session" is unmeasured.** No tool report whether module load. Budget
  is judgment, and criterion's own record give no threshold — no file count, no line
  count, no token count. **Its boundary test is off-the-shelf; its budget is
  judgment**, so the gate assert the shape and not the size — and the size is the
  half most easily applied after the fact to justify a split already wanted.
- **Whole-program-reasoning span is not measurable either.** Check name constructs
  already rejected; nothing detect a new one.
- **Classification of a piece of machinery as startup-loud is unverified.** Nothing
  assert a boot-failing mechanism actually fail boot in every configuration, and
  configuration is exactly where such a claim rot.
- **Review substitute is self-invoked.** Where no infrastructure guarantee it ran or
  that its inputs were not softened, committed verdict make omission visible and
  nothing make softening visible.
- **Will count is not observable.** Nothing detect that a second will appeared —
  a second team, an outsourced module, a vendor — and topology decision built on
  one will silently stop matching.
- **No outcome measured anywhere.** No repo built both ways, so every directive
  here is an argument about a counterfactual. Central claim marked *uncertain* for
  exactly this.

## Where the rest of this lives

- **`enforceable-rules`** — how to write a rule that bind an agent, the eight design
  principles including *no silent runtime behaviour* and *unwritable beats banned*,
  the incompleteness checks, and **the enforcement markers and status tier** every
  check line here carry. **Install it with this skill**: this one state what shape system take, that one state what shape a rule
  take.
- **`backend-stack`** — which stack, ranked by what its build can refuse to ship.
  Corpus gravity and drift asymmetry are its directives, not this skill's.
- **`guardrails-toolchain`** — which gates, how they compose, and the
  non-deterministic-reviewer rule this skill's review directive defer to.
- **`tech-decision-research`** — how to reach a verdict worth recording, including
  the requirement that premises be recorded with it. **Defines the four confidence
  markers** every claim here is graded in.
- **`java-backend-rules`** — one stack's runtime-silent ban list, with a check per
  banned mechanism.

## Markers, dates, and what they mean

**Every directive is *convention*.** Source records ran adversarial agent panels and
recorded verdicts, and carry **no per-claim confidence marker and no primary source
citation**. So nothing here reach *primary-source verified*, let alone *confirmed*,
and a reader who need that must re-verify from primary material.

**Central claim, that these decisions differ under an agent maintainer, is
*uncertain*** — argued, never measured.

**Dates below are the record's, not a verification date:**

| Directive | Date |
| --------- | ---- |
| Startup-loud / runtime-silent; design out whole-program reasoning; operational state in repo; module fits one session; predecessor is inventory; bus factor by failure shape; hand-built subtle piece | 2026-06-12 |
| Count the independent wills | 2026-06-12..13 |
| One idiom imposed mechanically | 2026-06-12..13 |
| A steering human is not a reviewer | 2026-06-13 |
| Review substitute; zero retries and quarantine | 2026-06-14 |
| Exit-ladder executability clause | 2026-08-01 — conversion-dated |
| *Composite shapes a repo assembles out of these primitives*, the widened load trigger, and the two predicate-check entries in *Named gaps* | 2026-08-02 — conversion-dated, from `enforceable-rules`' composite-shape and predicate checks, run by reading. **They add no directive and promote no marker**: each resolve a shape two published directives already decide between them, or name a check that is absent. **The layer check is not applicable here** — nothing this skill governs crosses a layer; its subject is where a boundary falls, not what crosses one. **The enumeration and token-placement checks have not been run** |

**Enforcement markers sit beside each check**, and most are *convention* — these
directives bind decisions taken before code exist, so their check is a written
artifact whose absence is visible. **The ones carrying an off-the-shelf check are
named rather than counted:** boundary tests, the formatter and canonical-form
rewriter, the operational-surface lints, the absent-fixture grep, and the retry
setting. The quarantine expiry gate beside that last one is **bespoke**, and its
own check line say so.

Evidence, sources and the do-not-cite list are in `evidence.md`.
