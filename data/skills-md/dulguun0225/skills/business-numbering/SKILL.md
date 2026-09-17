---
name: business-numbering
description: How a system issues the human-facing identifiers people read out loud — an account number, a loan number, a voucher number, a document number — for any repo in any language. Enumerate the number classes in a compile-checked catalog with a scope, an issue moment and a gapless decision each; issue from a counter row incremented inside the caller's transaction rather than from an engine sequence, because gapless is a transactional property and not a cleanup job, and because counter rows replicate where sequences do not; take the caller's transaction handle as a written argument so same-transaction issuance is structural; draw periods from the business calendar and never the wall clock; build formats from ordered typed parts rather than a pattern string, validated at load or the application refuses to boot; carry a Damm check digit on human-keyed classes with the algorithm in stored config, validated at every ingress and resolved by lookup rather than by parsing shape; hard-fail on exhaustion rather than widening silently; and name the contention threshold and its relief ladder before either is needed. Carries one repo's seven-class catalog as its worked case, with the rejected alternatives and the ground each lost on. ALWAYS load before adding a number a person will read out, quote or type; before writing an issuer, a counter, a format or a check digit; before adding any entry point that accepts a number, including a file import; before writing a report that filters, groups or sorts on one; before importing legacy numbers; and before making any number gapless.
---
# Business numbering — the identifier a person reads out

**Two identifiers, and this skill owns the second one.** The row key is opaque,
machine-scoped, and the target of every foreign key; **`primary-keys` owns it** and
states the split. **The business number is short, checkable, issued under a stated
format, and never a primary key and never a URL identifier.** It is a filter, a
display value and document text.

**Everything here is portable** — it holds on any relational store, any language.
The worked case is one repo's catalog, dated **2026-06-12**, carried as evidence the
criteria discriminate rather than as a template.

**Central claim, and it is what the rest hangs on: a business number is issued by a
counter row inside the caller's transaction, and every other property people want
from these numbers — gaplessness, atomicity with the business write, survivability
across a data move — falls out of that one decision.**

## The marker ceiling, before anything else

**Everything here is *convention*.** Source is one organisation's architecture
decision record, 2026-06-12, plus the use case written from it. **The record carries
no per-claim confidence marker and cites no primary source for any claim in it** —
including the two most worth citing: the check-digit algorithm's detection
guarantees, and a statutory search that returned nothing.

- **Central claim is *uncertain*, not convention.** One repo decided this way; none
  decided the other way for comparison, and no numbering scheme in this set has been
  observed at volume. Argument, with no outcome behind it.
- **The record names an adversarial structure**, and that is worth stating precisely
  because it is the same shape `primary-keys` carries: its status line records a
  three-agent evaluation — evidence mining over a predecessor system, a design
  steelman, and a hostile audit — with grounds recorded per rejected alternative.
  `tech-decision-research` grades *confirmed* on refutation votes cast **against
  primary sources**, and there were none. So: better provenance than a preference,
  and still convention.
- **One claim in the source is a negative result and it is carried as one.** The pass
  searched for a statute requiring gapless or per-period voucher numbering and
  **found none**. That is a search, not a proof, and it was run in one jurisdiction.
  **Do not read it as "no such law exists anywhere."**
- **No date invented.** Directives carry the date of the record that grounds them.
  Where a directive states something no record wrote in that form, the date is the
  conversion date **2026-08-02** and the directive says so.

Status tier: **decided, not yet validated** — researched and decided, **no production
use yet**. The catalog below was specified for a first milestone slice, not run.

## The premise, and what it changes here

**Code is written by LLM agents and no human reads it line by line.** Every sibling
skill states this. Two consequences specific to numbering:

- **A number that is silently wrong stays wrong.** A duplicated account number, a
  gap in a register somebody will audit, a number whose width overflowed — none of
  these throw. They surface when a person outside the system complains, which is the
  same shape the money rules are built on.
- **A number is the one identifier a human dictates.** That is what earns it a check
  digit and what makes *parse the prefix* an attractive shortcut. Under this premise
  nobody reviews the parse, and the value it reads was a fact about the world on the
  day the number was issued.

## The catalog

### Enumerate the number classes, with a decision per class

**Every business number belongs to a named class in a compile-checked catalog, and
each class states its counter scope, whether it is gapless, the moment it is issued,
its check-digit algorithm, and its format version.** A repo that issues numbers
without this list has the decisions anyway — made per call site, differently.

**The issue moment is the field most often left implicit and it is a business
decision, not a technical one.** The worked case issues a loan number at **booking**
and gives an application its own class with its own format, so that a rejected
application never consumed a loan number. Nothing about the mechanism forces that;
the catalog is where it gets stated once.

**Uniqueness is per tenant, always**, in any system that has tenants — and each class
sits behind its own unique index.

*Check: the class list is a compile-checked enumeration, not strings; a schema check
asserts a unique index per class; and every use case or spec that creates a numbered
record names the class and the step at which the number is issued. **Bespoke**;
the enumeration half is off-the-shelf in any typed language. **Convention**,
2026-06-12.*

***The class list exists twice, in two languages, and the compiler reads one.* Layer
check, run 2026-08-02 against this skill, conversion-dated. The enumeration is code;
the **format rows and counter rows that give each class its behaviour are data**, seeded
and per tenant. A class in the enumeration with no seeded format fails at first
issuance, inside a business transaction; a seeded format for a class the enumeration
no longer has is dead configuration nothing reports. **The compile-checked half
buys less than it appears to** — it makes the *name* unmisspellable and says nothing
about whether the class is configured. **Decidable half: a startup check that the
seeded classes and the enumerated classes are the same set, failing the boot on
either direction**, which is the same both-directions reconciliation
`java-backend-rules` requires of its ban list.*

### Numbers are immutable, never reused, never reassigned, and stored exactly as issued

**Store the canonical compact form — one case, no separators — and treat display
grouping as rendering.** A number stored as it is displayed cannot be looked up by
the person who typed it without separators, and a number stored twice in two forms is
two numbers.

**Renumbering is banned, in writing.** Not discouraged: banned, and written down,
because the request arrives with a good reason attached and the cost lands on every
document, export and integration that already carries the old value.

*Check: schema check that number columns are not nullable and have no update path
outside issuance; a lint banning any update statement targeting a number column.
**Bespoke**. **Convention**, 2026-06-12.*

### Parsing meaning out of a number is banned everywhere

**No code, no report, no plugin and no country pack reads a substring of a business
number to learn anything.** A number is a **birth fact**: it records what was true
when it was issued. A closed branch's code lives on in old account numbers forever,
and the current branch is a column.

**This is the directive most likely to be violated by an agent doing something
reasonable.** *Filter by branch* has an obvious cheap implementation and a correct
one, and the cheap one keeps working until the first reorganisation.

*Check: a lint banning substring, prefix, regular-expression and pattern reads of a
number column outside its own rendering module — in application source **and in query
text**, which is where the reporting version of this defect is written.
**Bespoke**. **Convention**, 2026-06-12; the query-text half **2026-08-02**,
conversion-dated, from the layer check `primary-keys` ran against its own equivalent
rule.*

### Where an ordering over numbers is wanted, persist the ordering columns

**Persist the period and the sequence as their own columns beside the rendered
string, and sort on those.** Never on the string — a rendered number sorts wrong the
moment its width changes or its prefix does — and never on the row key, which
`primary-keys` bans for its own reasons.

**One legitimate exception, and it is a property of the mechanism rather than a
convention**: for a gapless class, **the sequence is commit order** within its
counter, because the number is drawn inside the committing transaction. That is a
real ordering the design may depend on, unlike a key's.

*Check: schema check that every orderable class carries its ordering columns; a lint
asserting no `ORDER BY` targets a rendered-number column. **Bespoke**.
**Convention**, 2026-06-12.*

## Issuing

### Issue from a counter row inside the caller's transaction, never from an engine sequence

**One mechanism: a counter row keyed by class, series and period, incremented and
returned in a single statement, inside the transaction that writes the business
row.** No engine sequences anywhere.

Two grounds, and they are independent:

- **Gapless is a transactional property, not a cleanup job.** A sequence increments
  outside the caller's transaction by design, so a rollback leaves a gap and no
  amount of later reconciliation closes it. A counter row incremented in the same
  transaction **rolls back with it** — the gap never exists. The cost is stated
  rather than hidden: a failed business write retries the whole transaction.
- **Counter rows replicate as data; sequences do not.** In a logical-replication
  move, a sequence's current value arrives at zero and must be reset by hand, per
  sequence, per move, before the target takes writes. **A schema with no sequences
  owes zero resets**, and `primary-keys` carries that argument in full as the ground
  for its own decision.

**One mechanism beats two, and the worked case makes the point against itself**: its
own predecessor decision had left a carve-out permitting sequences for gap-tolerant
classes, and this decision **left the carve-out on the books and deliberately
unexercised** rather than taking it.

*Check: grep the committed migrations for sequence-creating DDL and fail on any hit —
**and point it at the mapping annotations and non-SQL changelog formats this repo
actually uses**, not at one spelling. **Off-the-shelf** as a migration grep, patterns
per repo. **Convention**, 2026-06-12; the second-language clause **2026-08-02**,
conversion-dated.*

### The issuer takes the caller's transaction handle as a written argument

**The issue operation's signature takes the transaction handle the caller already
holds, and the issuer can obtain one no other way — no ambient lookup, no
no-argument overload, no self-opened transaction.** Then same-transaction issuance is
**structural**: the wrong call does not compile, rather than being reviewed against.

**This is the same construction `async-handoff` `E-6` uses for the outbox append, and
for the same reason.** Whether a transaction is "active" at a call site depends on
which callers reach it, on proxy boundaries, on propagation settings and on resource
identity — so no static analysis decides it soundly, and the requirement is
discharged at the call site by the compiler instead.

**One caller discipline survives and cannot be made structural: issue late in the
transaction.** The counter row is a serialization point, and holding it from early in
a long transaction multiplies the contention below by the transaction's length.
**Name it, pin it with the stress suite, and do not pretend a check covers it.**

*Check: the port's signature and an architecture rule that no module constructs a
transaction inside the issuer; plus a rollback integration test — force the business
transaction to roll back after issuance and assert the counter is unchanged and no
number was consumed. **Off-the-shelf** hosts, predicates per repo. **Convention**,
2026-06-12.*

### Gapless only where it earns its keep, and say what it is insurance against

**Make a class gapless only where something outside the system expects an unbroken
register, and write down what that expectation is.** Gapless issuance serializes
every write in its scope; applied everywhere it buys nothing and costs the whole
throughput of the system.

**The worked case is worth copying for its honesty rather than its verdict.** It
made journals gapless per tenant and fiscal year, and recorded that **the statutory
search it ran found no such requirement** — so it states the ground as *cheap
insurance against a standing audit expectation*, plus two real bonuses: the number is
commit order, and the invariant is trivially checkable. **An unexamined "the auditors
require it" is the version of this decision to distrust.**

**Where a class is not gapless, gaps need an explanation that exists before anyone
asks.** A gap report per class and period, with a one-page narrative, is a shipped
reporting artifact — not a query somebody writes during an audit.

*Check: the gapless decision is a field in the catalog, not a comment; a production
invariant per gapless class asserting the sequence range equals the row count and the
counter equals the maximum, paged on failure **or on staleness**; and the gap report
exists as a committed artifact. **Bespoke**. **Convention**, 2026-06-12.*

### Periods come from the business calendar, never the wall clock

**A period-scoped counter draws its period from the system's own business date, not
from the clock.** A backdated or replayed run that reads the wall clock issues
numbers into the wrong period, and every one of them is well-formed.

**Pre-create the next period's counter rows as part of the period-open step**, and
where a row must be created on demand, create it with an insert that collapses on the
unique constraint over class, series and period — so the rollover race yields exactly
one row rather than a duplicate sequence.

**State what happens outside an open period rather than letting it be discovered**:
issuing into an unopened period and issuing after a hard close are two distinct typed
errors.

*Check: a ban on wall-clock reads in the issuing module — `now()` and its
equivalents **in query text and in column defaults as well as in application code**;
the unique constraint over class, series and period; and a rollover race test.
**Off-the-shelf** for the constraint, **bespoke** for the clock ban's query-text half.
**Convention**, 2026-06-12; the query-language clause **2026-08-02**,
conversion-dated.*

### Name the contention threshold and the relief ladder before either is needed

**A gapless counter is one hot row, and the serialized window is the increment
through to commit — including any synchronous replication acknowledgement.** Compute
the ceiling that implies, compare it to the projected workload, and **write the
threshold and the response down before the first incident.**

The worked case's shape, carried as the shape rather than as numbers to copy: a
stated ceiling in commits per second per tenant, a projected workload well below it,
a **pre-decided trigger** on counter lock-wait latency and sustained commit rate, and
a **relief ladder in order** — first reduce the batch size that concentrates
issuance, then reduce granularity by configuration, never improvise. **For
gap-tolerant classes there is a further step gapless classes cannot take**:
allocating a block in memory, which trades gaps on restart for no contention at all.

**Batch work takes one block per batch, not one increment per row** — still gapless,
and it keeps the lock held once rather than N times.

*Check: the counter wait time is a metric with a committed alert rule and a
fire-test; the threshold and the ladder are written in a committed artifact; the
block-allocation call is the one the batch path uses. **Bespoke**. **Convention**,
2026-06-12.*

## The format

### A format is an ordered list of typed parts, never a pattern string

**Model a format as a sequence of sealed typed parts** — a literal, a code of a
declared width, a period token, a sequence of a minimum width, a check digit naming
its algorithm — **stored as immutable versioned rows and deserialized into those
types.**

**The named loser is a pattern-string interpolation engine, and it lost on a real
defect rather than on taste.** Where a format is a string template and the counter
key is composed dynamically from parts of it, two unrelated domains can compose the
same key and **share a counter** — which is how the predecessor system in the worked
case contaminated counters across domains. A typed part list has no expressive room
for that, because the counter key is not something the format can build.

**Validate structurally at load, and refuse to boot on failure**: exactly one
sequence part, the check digit terminal, a period token present exactly when the
class is period-scoped, digits-only where a downstream rail requires it. **A
malformed format that fails at issue time fails during a business transaction; one
that fails at boot fails in the deployment.**

*Check: the parts are a sealed type hierarchy so an unknown part does not
deserialize; a structural validation run at startup that fails the boot; and a golden
test per seeded format pinning the rendered output. **Off-the-shelf** for the golden
tests, **bespoke** for the validator. **Convention**, 2026-06-12.*

### A format change is a new version, effective at the next period rollover

**Formats are versioned and immutable once anything has been issued under them.** A
tenant may customise before first issuance; afterwards a change is a new version that
applies to new numbers only.

**This is not ceremony — it is forced by the storage rule.** Numbers are stored
exactly as issued, so **re-rendering old numbers under a new format is impossible by
construction**, which means a mid-period width or shape change produces a register
that sorts and aligns two ways.

*Check: a status field on the format row plus a rejection when a format with issued
numbers is edited; the edit path is a create-version operation and there is no update
operation to call. **Bespoke**. **Convention**, 2026-06-12.*

### Exhaustion hard-fails; widening is never automatic

**When a class exhausts its width, issuance fails with a typed error and pages.** Do
not widen automatically, and do not let a padding helper silently drop the overflow —
that is the predecessor defect this rule exists for, and its symptom is numbers that
are wrong rather than absent.

**Size widths against a projection with an order of magnitude of headroom, and gauge
the fill.** A capacity metric per class and width, with a ticket threshold well below
a paging one, turns exhaustion into scheduled work.

**Widening is a new format version effective at a period rollover**, because a
mid-period width change breaks fixed-width interchange files and every sort that
assumed the old width.

*Check: the renderer's width handling has a test asserting it throws rather than
truncates; a capacity gauge per class and width with committed alert rules and
fire-tests. **Bespoke**. **Convention**, 2026-06-12.*

## The check digit

### Carry a check digit on every human-keyed class, with the algorithm in stored config

**A number a person dictates carries a check digit; a number only machines exchange
does not.** The worked case's split is exactly that: customer, account and loan
numbers carry one; journal, transaction-reference, operation and document numbers do
not.

**The default is Damm, and the losers are named because the corpus favours them.**
Damm catches all single-digit errors and all adjacent transpositions at **one** digit
of cost, from one table. **Luhn is the corpus default by a wide margin and misses the
09↔90 transposition.** **mod-97** costs two digits and its home is IBAN
construction, where it belongs. **Verhoeff** needs three tables to Damm's one and
buys nothing Damm does not already give here. **All four named**, because a
directive that says *a three-table scheme* leaves the reader unable to tell which
one it declined.

**The algorithm is a typed value in the stored format, not a hardcoded call**, so a
later session reaching for the corpus favourite cannot silently swap it.

*Check: the algorithm is an enumerated value in the committed format; the
implementation is pinned by golden vectors **and by a property test asserting the
detection guarantees themselves** — every single-digit error and every adjacent
transposition on generated inputs. **Off-the-shelf** hosts, vectors per repo.
**Convention**, 2026-06-12 for the choice; **the detection guarantees are stated by
the record and cited to nothing** — see the do-not-cite list in `evidence.md`.*

### Validate at every ingress, resolve the format by lookup, never by parsing shape

**Every entry point that accepts a number validates it before any lookup** — the user
interface, a partner interface, a file import. Validation that lives in one of three
entry points is a control the other two do not have.

**Resolve which format a number belongs to by looking the number up, never by
matching its shape.** Shape matching breaks on the first legacy number, and legacy
numbers are guaranteed: an imported number has no check digit and no current format.
**A number that fails the current check still gets an exact-match lookup before it is
rejected**, or the system tells a customer their own account number is invalid.

**The check digit never participates in uniqueness, sorting or ranges.** The number
is an opaque unique whole; treating the payload and the check digit as separable
invites arithmetic on the payload.

*Check: an architecture rule that every ingress adapter calls the validator before
any repository call; a test per ingress; and a lint asserting no index, sort or range
predicate is built on a substring of a number column. **Bespoke**. **Convention**,
2026-06-12.*

## The edges

### Legacy numbers land in the same columns, under a version that says so

**Imported numbers go into the same columns as issued ones, under a format version
reserved for exactly that: one opaque literal part, no check digit.** They are real
numbers with real history; a parallel column for "old" numbers doubles every lookup
in the system forever.

**Collisions go to a reconciliation report and are never auto-suffixed.** An
automatically de-duplicated legacy number is a number nobody outside the system
recognises.

**Counters seed to the maximum imported value plus headroom, per scope, and a
cutover gate verifies it** — a gate that fails, not a dashboard somebody reads.
**A gapless class starts at one in the cutover period**, because the legacy register
belongs to closed periods of the old system.

*Check: the cutover gate asserts, per class and scope, that the counter exceeds every
imported value; the reconciliation report is a committed artifact.
**Bespoke**. **Convention**, 2026-06-12.*

### An idempotent retry returns the stored number and never issues a second one

**Where a command is replayable, the number is allocated inside the command's
transaction and a replay returns the stored response — including the original
number.** A replay that issues a fresh number produces two numbers for one business
fact, and both look correct.

*Check: an integration test that replays a command with the same idempotency key and
asserts the same number, and that the counter advanced once. **Bespoke**.
**Convention**, 2026-06-12.*

### The rail's constraints belong to the rail's adapter, not to the core

**Where a number must fit an external scheme — a bank-account format, a regulator's
register, an interchange file layout — the core guarantees uniqueness, charset and a
declared maximum width, and the adapter for that scheme owns everything else.**
Registries of external codes are configuration data, never a map compiled into the
core; the worked case names a hardcoded bank registry as a predecessor defect.

**The core does honour the strictest declared target, and that is the one leak
allowed**: a class whose numbers must fit a twelve-digit slot has a digits-only
default of that width, and the reason is recorded beside the class rather than
discovered later.

*Check: the width and charset per class are in the committed catalog; an architecture
rule that the core module does not depend on any rail adapter; external registries
load from configuration. **Bespoke**. **Convention**, 2026-06-12.*

## The worked case — one repo, 2026-06-12

**One organisation's catalog, kept as evidence the criteria above discriminate. Not a
template.** A multi-tenant financial backend on PostgreSQL, agent as sole maintainer,
tenants in per-tenant schemas that move between database cells by logical
replication, with a jurisdiction whose interbank scheme mandates a twelve-digit
account slot. **Its seven classes, their widths and scopes, and the counter-table
mechanism behind them are in [evidence.md](evidence.md).**

**The alternatives it rejected, and the ground each lost on:**

- **Engine sequences for the gap-tolerant classes** — the obvious mechanism, lost
  because **sequences do not replicate**, so every tenant move owes a manual reset
  per sequence, and one mechanism beats two. At the recorded volumes the row lock is
  noise.
- **Gapless everywhere** — one rule with no per-class argument, lost because it
  serializes every issuance in the system **for no evidence of need**: no statute
  found, and the predecessor system had no gapless numbering anywhere with no audit
  complaint against it.
- **Gapless nowhere** — the honest reading of a statutory search that found nothing,
  rejected **narrowly, for journals only**: one hot row per tenant and fiscal year is
  bounded, and a gap-free register is cheap insurance against a standing expectation.
- **A pattern-string format language** — flexible, familiar, and what the predecessor
  had; lost because dynamically composed counter keys **contaminated counters across
  domains** in that system.
- **A two-digit checksum as the default** — stronger detection and a named standard,
  lost on two digits of a scarce width; available to a country pack as a typed
  option, not the domestic default.
- **Random or opaque business identifiers** — lost because the row key already
  provides opacity, and **the business number exists precisely to be short, keyable
  and human-orderable**.

**No re-open trigger per rejected alternative**, and that is one habit failing three
times rather than three omissions — **`primary-keys` and `backend-stack` owe it
identically.** The record sets a threshold on the winner and nothing states what
would make sequences or gapless-everywhere worth re-examining. Not invented here:
writing a trigger nobody set authors the verdict rather than records it.

*Check: none — this a record of a decision, not a directive. Grounds **convention**,
2026-06-12.*


## Wiring the gates

Run once, in a repo adopting this skill. Record what got wired and what got skipped
with a reason — a skipped item with no reason reads as done by the next session.

1. **Migration grep** — no sequence-creating DDL, in every language this repo
   declares schema in.
2. **Catalog checks** — the class enumeration compiles; a unique index per class; the
   width and charset per class committed.
3. **Issuer signature and confinement** — the transaction handle is a parameter, the
   issuer opens no transaction, and an architecture rule holds both.
4. **Rollback test** — a business transaction that rolls back after issuance leaves
   the counter unchanged.
5. **Rollover race test** — concurrent first issuance in a new period yields one
   counter row and no duplicate first sequence.
6. **Stress suite** — concurrent writers, mixed single and block issuance, injected
   aborts: no duplicates, the sequence range equals the count for gapless classes,
   the counter equals the maximum. Plus a kill-mid-issue variant.
7. **Check-digit vectors and properties** — golden vectors, plus a property test
   asserting the detection guarantees rather than assuming them.
8. **Format validation at boot** — a malformed committed format fails startup, with a
   test that asserts it.
9. **Ingress validation tests** — one per entry point, and a cross-tenant probe
   asserting another tenant's number returns the same bytes as one that never
   existed.
10. **Production invariants** — per gapless class and period, the range-equals-count
    and counter-equals-maximum assertions, paged on failure **or staleness**.
11. **Capacity gauges and the contention metric**, each with a committed alert rule
    and a fire-test.
12. **The gap report and the cutover gate**, as committed artifacts.

**Which of these fail a build off the shelf, named rather than counted:** the
migration grep, the catalog's compile-checked enumeration, the unique-index schema
check, the architecture rules on the issuer, the golden vectors, and the boot-failure
test. **Bespoke:** the stress suite, the invariant suite, the property test's
predicates, the capacity gauges, the gap report and the cutover gate.

## Composite shapes a repo assembles out of these primitives

**`enforceable-rules`' composite-shape check, run 2026-08-02,
conversion-dated.** The directives govern a class,
a counter row, a period, a format version, a check digit, a block, a gapless flag and
a legacy import. **A repo builds things out of two of them.** Every entry marked;
**silence about a shape is a defect in this section.** No marker promoted, **no ban
added** — each entry resolves to a condition, and the one that looks like a ban is a
verdict two published directives already imply.

| Shape | Verdict |
| ----- | ------- |
| **A transaction that touches the counter row and a second contended row** — a balance projection, an aggregate, any hot row | **permitted with conditions, and the conditions were stated in no skill.** *Issue late in the transaction* asks for the counter to be the last lock taken, because it is held until commit. **A repo can have more than one such row**: `money-storage` `M-39` permits a mutable balance row beside the effect rows, and it is contended for the same reason. **Two hot rows taken in different orders by two transactions deadlock**, and that is a failure neither skill's checks reach. **Do not answer this by writing the lock order down.** `ai-maintainer-principles` names lock ordering by name as a requirement that **cannot be documented** — a fact spread over files, re-derived wrongly by every session that reads one of them. Two honest answers, and this skill takes no position on which: **eliminate the second contended row** — `money-storage` `M-38`'s append shape has none, which is that skill's recommendation for its own reasons — or **confine every transaction touching more than one contended row to a single named operation that takes them in a fixed order**, so no call site chooses. A repo doing neither has accepted a permanent defect source and should record that it did |
| **Issuing a number in the same transaction that appends an outbox row** | **permitted, and it does not compete** — stated because it reads as though it should. `async-handoff` `E-5` and `E-6` require the outbox append inside the same transaction, and an append is an insert of a new row: **it takes no contended lock, so it does not belong in the ordering question above.** A reader who has installed both skills sees two *do this inside the transaction* instructions and needs to know that only one of them is about contention |
| **Demoting counter granularity under contention** — the relief ladder's *per-branch series* step | **permitted with conditions.** Splitting a class's counter into per-branch series **changes what gaplessness means mid-life**: numbers before the change are gapless per tenant, numbers after are gapless per branch, and the production invariant that asserts range-equals-count silently starts asserting something weaker. Condition: **a granularity change is a new series key and therefore a new format version at a period rollover**, exactly like a width change — never a configuration flip inside a live period, which is how the relief ladder reads if nobody states this |
| **Two senses of "a block"** | **both permitted, and they must not be confused.** A **transactional block** — increment by N inside the committing transaction — is gapless-safe and is what batch work takes. An **in-memory block** pre-allocated across transactions trades gaps on restart for no contention, and is available **only to gap-tolerant classes**. Marked because this skill uses the same word for both and a reader applying the second to a gapless class breaks its invariant |
| **A check-digited number nested inside a rail-constructed identifier** | **permitted, and it is why the two algorithms are separate.** A domestic account number carries its own Damm digit; the interbank identifier built around it carries its own mod-97 digits. **Two check digits over overlapping payloads is correct, not redundant** — they protect different transcription paths, and neither validates the other |
| **A business number in a message payload or an outbox row** | **permitted, and out of scope here** — `async-handoff` `E-21` governs payload content. **The one clause worth carrying across: a consumer that parses meaning out of the number is this skill's ban arriving in another deployable**, where no lint of this repo's reaches it |
| **A business number as a cache key or part of one** | **out of scope here, owned by `caching` `C-6`** — the cache key is the loader's full argument tuple. Marked because a business number is exactly the shape someone hand-builds a key string from, which `C-6` bans |
| **A tenant customising a format after a legacy import but before any issuance** | **permitted with conditions, and nothing here stated them.** *Legacy numbers land under a reserved version* and *customisation is allowed before first issuance* are both true, and an import is not an issuance — so the window is open with imported numbers already in the column. Condition: **the reserved legacy version is unaffected by any later version**, since old numbers are stored and never re-rendered; what must be re-checked is the counter seed, because a width change after import can seed below an imported value |
| **A period that is reopened after a hard close** | **out of scope, and stated so rather than left silent.** This skill's periods come from the business calendar and it takes no position on reopening one — that is the accounting design's decision. **What it does require is that issuing into a closed period is a typed error rather than a silent draw from the wrong counter**, which holds however reopening is handled |

## Named gaps — where no check reaches

- **The predicate check, run 2026-08-02, left one thing it could not close.** The
  trigger named writing an issuer, a counter, a format or a
  check digit — **and two directives govern acts none of those describe**: *Validate
  at every ingress* is about **adding an entry point that accepts a number**, which is
  the act whose failure mode the directive itself names — validation living in one of
  three entry points; and *Parsing meaning out of a number is banned everywhere*
  extends to reports, so **writing a report that filters or groups on a number** is
  governed by it and fired no trigger. Both are named in the description. **What it
  could not close**: the birth-fact argument bites hardest when a branch closes or an
  organisation restructures, and *reorganising* is not an act anyone loads a
  numbering skill before.
- **"Issue late in the transaction" is a caller discipline no check enforces.** It is
  the one property of this design that is a convention, and the stress suite only
  observes its consequences under the load it happens to generate.
- **Nothing verifies that a gapless class is gapless for a reason.** The catalog
  records the decision; whether the expectation behind it is real is a question about
  the world, and the worked case's own answer was *we searched and found nothing.*
- **The statutory finding is a negative result from one jurisdiction, one search, one
  date.** It cannot be read as a general fact, and a repo elsewhere must run its own.
- **The contention ceiling is an estimate.** Nothing in this set has measured a
  counter row at the rate where its trigger fires — which is the only condition under
  which the cost side of this decision is tested rather than argued.
- **The check-digit property test proves the algorithm's guarantees on generated
  inputs, not the transcription errors humans actually make.** The two are related by
  an assumption nobody here has checked.
- **No outcome measured anywhere.** One repo specified this; none specified the other
  way. Central claim marked *uncertain* for exactly that.

## Where the rest of this lives

- **`primary-keys`** — the row key, and the split this skill's first paragraph
  restates. It carries the part its own decision rests on: the two identifiers are
  separate, the sequential one is not implemented with sequences, grep namespaces
  stay disjoint, and ordering columns are persisted beside the rendered string.
  **Two directives here are also stated in full there** — *Numbers are immutable,
  never reused, never reassigned* and *Parsing meaning out of a number is banned* —
  and **this skill is the owner of record for both**. The
  duplication is deliberate: a repo can install one skill and not the other, and both
  bans bear on that skill's split as directly as on this one's subject. **A change to
  either ban's wording is a change in two files**, and the index for that is the
  paragraph beside those two bullets there.
  **The replication asymmetry is argued in full there**, as the ground for its own
  verdict.
- **`async-handoff`** — `E-6`'s outbox append is the same construction as this
  skill's issuer signature, for the same reason: a transaction handle taken as a
  written argument, because no static analysis decides "the same transaction"
  soundly. **Do not carry `E-7`'s deterministic message identity over to a business
  number** — a message identity is re-derived on replay, and a business number is
  drawn once from a counter.
- **`money`, `money-api`, `money-storage`** — what the amounts on a numbered document
  must be. This skill constrains the document's identifier; those constrain its
  contents. **And `money-storage` `M-39` is where the second contended row comes
  from**: a mutable balance row beside the effect rows is optional there and hot for
  the same reason the counter is, so a repo taking both owes one lock order over
  both. **Both skills state that from their own side.**
- **`ai-maintainer-principles`** — *A hand-built subtle piece ships with a safety
  argument and a stress test*, which is the ground under this skill's stress suite and
  under stating the safety argument explicitly: **a number exists if and only if its
  transaction committed.**
- **`enforceable-rules`** — *Distrust what the agent picks*, which is why the losing
  check-digit algorithm and the pattern-string format language are named rather than
  described, and **the enforcement markers and status tier** every check line here
  carries.
- **`tech-decision-research`** — **defines the four confidence markers** every claim
  here is graded in, and the downgrade rule that lands all of them at convention.
- **`guardrails-toolchain`** — which tool may occupy a gate at all, and the rule that
  a gate only gates where its measurement is honest, which the production invariants
  above depend on.

## Markers, dates, and what they mean

**Every directive is *convention*.** The source ran a three-agent evaluation and
recorded grounds per rejected alternative, which is more structure than most prior art
in this set carries — and it still **cites no primary source for any claim in it**,
so nothing here reaches *primary-source verified*, let alone *confirmed*.

**Central claim — that a counter row inside the caller's transaction is what every
other property falls out of — is *uncertain*.** Argued, never measured.

| Directive | Date |
| --------- | ---- |
| Every directive under *The catalog*, *Issuing*, *The format*, *The check digit* and *The edges* | 2026-06-12 |
| The query-text half of *Parsing meaning out of a number is banned*, the second-language clause of the sequence grep, and the query-language clause of the wall-clock ban | 2026-08-02 — conversion-dated, each stated in its own check line |
| *Composite shapes a repo assembles out of these primitives*, the enumeration-versus-seed-data layer clause, the widened load trigger, and the naming of Verhoeff and mod-97 beside Damm and Luhn | 2026-08-02 — conversion-dated. **All five of `enforceable-rules`' incompleteness checks were run against this skill on its publication date**, which is the first time any skill here has had them at authoring rather than after. **They promote nothing**: each names a shape two published directives already decide between them, a second language an existing check does not read, or a subject the source named and the draft described |

**Enforcement markers sit beside each check.** The ones carrying an off-the-shelf
host are named rather than counted: the migration grep, the compile-checked class
enumeration, the unique-index schema check, the architecture rules on the issuer and
on ingress ordering, the golden vectors and the boot-failure test. The stress and
invariant suites, the capacity gauges, the gap report, the cutover gate and the
format validator are **bespoke**, and each check line says which.

Evidence, sources, the reading window and the do-not-cite list are in
[evidence.md](evidence.md).
