---
name: primary-keys
description: How a row is identified, and what that identity may never be used for — rank key candidates by the surfaces the id lands on rather than by index size, treat a key an outsider can enumerate as a volume disclosure and a forced retrofit, count the manual steps each key mechanism costs a data move because sequences do not replicate and counter rows do, apply one mechanical rule with a computed table classification instead of per-table judgment, check the anti-UUID cost folklore against your own engine because the classic numbers are UUIDv4 numbers and the fat-key-multiplies-every-index claim is InnoDB lore, ban ORDER BY on any id column because a time-ordered key is monotonic per generator and not across a pool, keep the opaque key and the human-facing business number as two identifiers with disjoint namespaces, put the generator default in the schema and the banned generator beside it, give pure-child tables their parent's key plus a sequence, and remember the key is what survives erasure. Carries the verdict on every shape a repo assembles out of the key — the key as a partition key, inside a cache key, inside an object-storage path, as a correlation id, derived from another identifier — and one repo's UUIDv7-everywhere verdict as its worked case, with bigint identity, the bigint-plus-external-id hybrid and TSID recorded as losers with the ground each lost on. ALWAYS load before creating a table, choosing or changing a primary key, generating an id in application code, designing a human-facing number format, writing an object-storage key template or a log field set, putting an id in a URL, a log line, a payload or an export, writing an ORDER BY over an id column in any language, or moving tenant data between databases.
---
# Primary keys — what identifies a row, and what that identity may never mean

**Two halves.** Directives portable — hold on any relational store, any language.
Worked case = one repo's verdict, dated **2026-06-12**, with the candidates it
rejected and the ground each lost on. Worked case there as *evidence the criterion
discriminate*, not recommendation to copy the verdict.

**Central claim, and it what the rest hang on: key type is decided by the surfaces
the id land on, not by what it cost to store.** URL, log line, wire payload,
export file, replication stream, escape-hatch store. Index size is real and it is
the last input, not the first.

## The marker ceiling, before anything else

**Everything here is *convention*.** Source = one org's architecture decision
records, 2026-06-12. **Records carry no per-claim confidence marker and cite no
primary source for any claim in them** — including the ones most worth citing:
engine behaviour, a benchmark, an RFC mandate.

- **Central claim is *uncertain*, not convention.** One repo decided this way;
  none decided the other way for comparison, and no key strategy in this set has
  been observed at volume. Argument, with no outcome behind it.
- **This record do name an adversarial structure, and that worth stating precisely
  because sibling skills here could not.** Its own status line record a three-way
  evaluation — a UUIDv7-everywhere steelman, a bigint-identity steelman, and a
  hostile audit of the hybrid and TSID options — and grounds per loser are written
  down. **It still cite no primary source**, and `tech-decision-research` grade
  *confirmed* on refutation votes cast **against primary sources**. So: better
  provenance than an undocumented preference, and still convention.
- **Lapse rule vacuous here, stated not hidden.** Past `review-by` every
  *confirmed* marker read as *convention* with no maintainer action; nothing here
  above convention, so the rule demote nothing. Stated cuz every sibling carry
  `review-by` and silence read as omission. **Cost: nothing make this skill's age
  visible** — and the engine facts below are the fastest-decaying claims in it.
- **No date invented.** Directive carry date of the record that ground it. Where a
  directive state something no record wrote in that form, date is the conversion
  date **2026-08-01** and the directive say so.

Status tier: **decided, not yet validated** — researched and decided, **no
production use yet** at the volume that would test it.

## The premise, and the one thing it make irreversible

**Code written by LLM agents. No human read it line by line.** Every sibling skill
state this. Two consequences specific to keys:

- **The maintainer debug from text.** Its whole sensory channel is committed text
  plus what the build print. An id that is ambiguous in a log line — `42` exist in
  every table and every tenant — cost this maintainer more than it cost a human
  with a debugger attached.
- **Per-table judgment is session-drift.** A key rule that say "surrogate here,
  natural there, depending" is re-decided every session, differently.
  `ai-maintainer-principles` own that ground as *One idiom, imposed mechanically*;
  it is why the directives below insist the classification be **computed**, not
  reasoned about.

**And the thing that make this decision unlike the others in this set: it is
effectively irreversible once real data exist.** The key leak into every table,
every generated database class, every URL an integrator signed against, every log
line, every export. There is no migration that change it quietly. **Decide it
before the first table, and record the decision where the next session read it** —
which is why this skill's description is written to fire at `CREATE TABLE`, not
after.

## Choosing the key

### Rank key candidates by the surfaces the id lands on

**Enumerate the surfaces the identifier reach before comparing candidates, and
score each candidate per surface.** The list is not generic — it is this repo's:
URL of any API an outsider integrate against, log line the maintainer grep, JSON
or wire payload, analytics or export file, replication stream between databases,
and any escape-hatch store the design have already named as a possible future
home.

**This is the criterion, and the reason it beat the obvious one.** Storage cost is
a number anyone can produce, so it dominate the discussion by default. It is also
the input least likely to decide anything: it is bounded, measurable and
recoverable. The surface inputs are unbounded and irrecoverable — an id published
in a sold API cannot be withdrawn, and a key mechanism that cannot cross a
replication stream become a manual checklist that must be right every time.

Candidate that win on every surface but one, where that one is a surface with an
outside party on it, **have not won**.

*Check: written selection record enumerating the surfaces this repo have and each
candidate's behaviour on each. Convention as enforcement — written artifact, absence
visible, cannot catch a surface nobody listed. **Convention**, 2026-06-12.*

### A key an outsider can enumerate is a disclosure you cannot take back

**Where row ids appear in an API sold to or integrated against by outsiders, a
densely sequential key publish volume and growth rate to every holder of two ids.**
Two invoices a week apart bracket a count. That is the signal a random or
high-entropy key do not carry, and it is commercially sensitive in most businesses
and regulated in some.

**The trap is that the fix is not a fix — it is a second identifier.** Repo that
pick a sequential key and later need opacity on the exposed tables end up adding an
external id to precisely those tables: two identifiers, two indexes, two grep
namespaces, translation at every edge, forever. **That is the hybrid, arrived at by
accident rather than chosen**, and it is a rejected candidate in the worked case
below for reasons that do not improve when it is reached late.

*Check: contract lint over the committed API document — no path template bind an id
parameter whose backing column is a densely sequential type. Bespoke; where no
committed document exist this have no gate at all and is review-only.
**Convention**, 2026-06-12.*

### Count the manual steps each key mechanism costs a data move

**Before adopting a key mechanism, ask what a copy of this data into another
database require of a human, and count the steps.** The asymmetry that decide it
in a PostgreSQL logical-replication move: **counter rows replicate as data;
sequences do not.** Logical replication carry table rows, so a sequence's current
value arrive at zero and must be reset by hand, per sequence, per move, before the
target take writes.

Consequence stated as arithmetic rather than as taste: a schema whose numbering
run on sequences owe one `setval` per sequence on every move, and a schema with
none owe zero. **Zero is a different kind of number than a small one** — a
single-digit checklist still have to be executed correctly at cutover by an agent
that have never done it before, and a checklist with no items cannot be executed
wrongly.

This generalise past PostgreSQL: **any key mechanism whose state live outside the
rows** — a sequence, a broker-assigned block, a node id baked into a generator —
is state that must be moved by a second procedure. Prefer the mechanism whose
entire state is the data.

*Check: grep the committed migrations for sequence-creating DDL (`CREATE SEQUENCE`,
`serial`, `bigserial`, `GENERATED ... AS IDENTITY`), and a written move procedure
whose reset step is enumerated rather than assumed. **Off-the-shelf** for the grep;
convention for the procedure. **Convention**, 2026-06-12.*

***A sequence is declarable in three languages and the grep reads one.*** *Added by
the layer check, **2026-08-02**, conversion-dated. DDL text is where the grep looks;
the same sequence is also created by an **object-relational mapping annotation**
(`@GeneratedValue(strategy = SEQUENCE)` and its equivalents), by a **non-SQL
changelog format** — Liquibase XML, YAML or JSON, where the token is `<createSequence>`
or `autoIncrement`, not `CREATE SEQUENCE` — and by a third-party library's own
migrations, which the* library-table *exception below deliberately leaves alone. A
repo on any of those three gets a green grep and a non-zero reset obligation, which
is the exact number this directive exists to make visible.*

### One mechanical key rule, and the exceptions are computed

**State one key rule for every table, and make each exception to it a
machine-decidable classification rather than a judgment call.** "Surrogate key
generally, natural key where it makes sense" is not a rule — it is a decision
re-made in every session by an agent reading one file.

The shape that work: the default apply to every table, and a table fall into an
exception class **only if a check can prove it does** from committed artifacts. The
worked case's pure-child test is the model — no other table declare a foreign key
to it, and its rows appear in no API URL except as a sub-path of its parent. Both
halves are derivable, from the foreign-key graph in `information_schema` and from
the path templates in the committed API document. Neither half is an opinion.

**Where an exception cannot be computed, it is not an exception — it is the
default with a comment.**

*Check: CI job classifying every table from the foreign-key graph and the committed
API document, and failing on a table whose declared class disagree. Bespoke — the
classifier is per repo, and the API-document half have no host where no document
exist. **Convention**, 2026-06-12.*

### Check the key-cost folklore against your own engine

**The received costs of a wide key are mostly true of a different key and a
different engine, and both errors run in the same direction.** Two specific
corrections, both stated by the source record and both worth re-verifying against
your own engine's documentation before you pay or refuse to pay:

- **The classic anti-UUID performance numbers are UUIDv4 numbers.** A random key
  scatter inserts across the whole index and generate full-page-image write-ahead
  log storms — the record put that at roughly twenty times the log volume. A
  time-ordered key insert at the right edge instead, and the record's own
  controlled benchmark had UUIDv7 and bigint tied on insert throughput, at
  3,420 against 3,480 transactions per second. **Applying the v4 numbers to a v7
  key is the single most common error in this decision.**
- **"A fat primary key multiplies every secondary index" is InnoDB lore.** It
  hold where secondary indexes carry the primary key as their row pointer. In
  PostgreSQL secondary indexes point at heap tuple identifiers, so the claim is
  false there. **Engine-specific, and the wrong engine's rule will be applied by
  default**, because the corpus an agent reason from is not weighted toward yours.

What the record left as the real cost, once the folklore is subtracted: primary-
and foreign-key index entries roughly a quarter to two fifths larger, and about
eight more bytes of heap per key column. **That is a cost, and it is the one to
argue about.**

*Check: the selection record name which cost claims were checked, against which
engine's documentation, on what date. **Convention**, 2026-06-12 — and the
benchmark is the record's own, run by the pass, **not reproduced here**.*

## What the key may never mean

### A time-ordered key is not an ordering

**Ban `ORDER BY` on any id column.** A time-ordered key is monotonic **per
generator**, not globally. PostgreSQL 18's native `uuidv7()` is monotonic per
backend; across a connection pool it is not. Any generator with a sub-millisecond
counter have the same shape — the counter is per producer.

**The failure mode is why this is a ban and not a caution.** `ORDER BY id` is
correct in a single-connection test, correct in local development, correct in the
integration suite, and wrong under a pool in production, silently, on the rows that
happen to interleave. Nothing in the result set is malformed. It just is not in the
order somebody assumed.

**Business ordering come from explicit columns** — a business date, a line number,
a posting sequence. Where the domain have an ordering the design care about, say so
in writing as a **named non-property of the key**: *id order is not posting order*,
recorded so no future session discover the correlation and quietly depend on it.

**One carve-out, and it grant determinism rather than meaning.** A keyset
pagination helper may append the row's key as the **final** tiebreak of its sort,
so cursors are gapless. Four constraints, each enforced:

1. At least one declared business sort column precede it — **the tiebreak is never
   the leading key.**
2. The id never appear in any API sort vocabulary, and cursors are opaque and
   sealed, so no client can observe or request id order.
3. The exemption is scoped to **that one pager class**; an `ORDER BY` touching an
   id column anywhere else remain a build failure.
4. The documented response order is the business ordering; **the relative order of
   ties is an explicit non-promise** in the contract.

*Check: architecture test banning id columns in `ORDER BY` targets, with the
exemption scoped to the single pager class by name; contract lint asserting no id
in any declared sort enum. **Off-the-shelf** host (ArchUnit), predicate authored per
repo. **Convention**, 2026-06-12.*

***The architecture test reads one language, and the ban is written in three.***
*Added by the layer check, run **2026-08-02**, conversion-dated. An architecture
test on the JVM reads bytecode: it can see a query-builder `orderBy` call and the
id field it is handed, and it cannot see the four letters `ORDER BY` inside a
string. The same sort crosses into **query text, view and materialized-view
definitions, stored functions, migrations, reporting and analytics queries, and
support scripts** — every one of them a place `ORDER BY id` is written and none
of them reachable by that host. So the ban needs the same two-part shape
`money-storage` gives arithmetic in the query language: the architecture
predicate over builder calls, **plus a lint over committed query text**. Blind
spot on both, stated because a green pair reads as coverage: query text assembled
at runtime from fragments is reached by neither.*

### A key is never a capability and never a secret

**Holding an id must never be what authorizes access to the row.** RFC 9562 state
this for UUIDs outright, and the rule is wider than the format. **A time-ordered
key also disclose its row's creation instant to anyone who hold it** — decide that
deliberately; a resource class that must hide it take a second, non-time-bearing
identifier, a business-identifier question, never a key-strategy change. *Trimmed 2026-08-12:
probed pro-default at N=2 (bare sonnet, effort high, 2026-08-11 — both sessions
designed a separate revocable grant unprompted). The check stays.*

*Check: per-endpoint authorization probe asserting a valid id from another tenant or
another principal return the same response as an id that never existed —
byte-identical, no existence oracle. **Off-the-shelf** as a test; the probe matrix
is authored per repo. **Convention**, 2026-06-12.*

***An endpoint is one of the ways an id gets dereferenced.*** *Layer check,
**2026-08-02**, conversion-dated. A probe matrix built per endpoint covers the HTTP
surface and nothing else, and the same id is handed to **a message consumer, a
batch or import job, a pre-signed object-storage URL, a report parameter and a
support script** — each a place where "holding the id" can quietly become the
authorization, and none of them an endpoint. The rule is stated wider than the
format; the check is narrower than the rule.*

### The opaque key and the human-facing number are two identifiers

**A row's key and the number a person read out over the phone are different
identifiers with different jobs, and neither may do the other's.** The key is
opaque, machine-scoped, and the target of every foreign key; the business number
is short, checkable, issued under a stated format, **never a primary key and never
a URL identifier** — a filter, a display value and document text, behind its own
unique index. *Split core trimmed
2026-08-12: probed pro-default at N=2 (bare sonnet, effort high, 2026-08-11).
**The renumbering ban below binds** — one probed session proposed a rotatable
account number.*

Three rules that follow, and each of them is a defect somebody shipped:

- **The grep namespaces stay disjoint.** Logs carry keys; the business number is the
  human and API handle. One identifier appearing in both roles make every search
  ambiguous.
- **Parsing meaning out of a business number is banned** — in code, in reports, in
  any pluggable extension. A number is a birth fact: a closed branch's code live on
  in old account numbers forever, and the current branch is a column. Every
  "just parse the prefix" is a bug with a delay fuse.
- **Renumbering is banned, in writing.** Numbers are immutable, never reused, never
  reassigned, and **stored exactly as issued** — canonical form, no separators;
  display grouping is rendering.

**Those two bans are `business-numbering`'s, and it is the owner of record since
2026-08-02.** They are stated here rather than pointed at, and **the duplication is
deliberate rather than accidental**: a repo can install this skill and not that one,
and both bans bear directly on the split this directive exists to make. **What lives
only there**: the class catalog, the counter mechanism, gaplessness, periods,
formats, check digits, exhaustion and legacy import — a skill's worth of material,
none of it restated here. **The index is this paragraph**; a change to either ban's
wording is a change in two files, and the owner is the other one.

**Where an ordering over business numbers is wanted, persist the ordering columns
beside the rendered string** and sort on those, never on the string and never on
the key.

*Check: schema check that no business-number column is a primary key or a foreign-key
target and that each carry a unique index; lint banning substring or pattern reads of
a number column outside its own rendering module. Bespoke. **Convention**, 2026-06-12.*

***The directive bans parsing in reports and the lint reads only code.*** *Layer
check, **2026-08-02**, conversion-dated. `substring(account_no, 1, 2)`,
`LIKE '01%'` and their equivalents are written in **query text, view definitions
and the report or business-intelligence tool's own expression language** — the
last of which is usually not committed to this repo at all. The lint over
application source reaches none of them, and the ban was stated for exactly those
places.*

## Generating it

### The schema default is the backstop, and the banned generator is named beside it

**Declare the key column with the generator as its column default, so a row written
by ad-hoc operator SQL cannot carry a wrong-version or null id.** The application
is not the only writer — a migration, a repair script and a session at a database
prompt all write rows, and none of them go through application code.

**And name the wrong generator, banned, in the same place.** In PostgreSQL that is
`gen_random_uuid()`: a version-4 random key, the exact scatter the time-ordered
choice exist to avoid, and **the function an agent reach for by default** because
it is the one the corpus is full of. `enforceable-rules` state the general form as
*Distrust what the agent picks* — name the favourite and ban it, never a bare "use
the good one".

**Check your engine version before assuming the default exist.** Native `uuidv7()`
is a PostgreSQL 18 function. A repo pinned to an older major have no native
generator at all, and its key column's default is a gap that must be named rather
than assumed away.

*Check: grep over committed migrations for primary-key column shape and for the
banned generator by name; gate on exit code. **Off-the-shelf** as a migration grep,
patterns authored per repo. **Convention**, 2026-06-12.*

***The banned generator has a twin in application source and the migration grep
never sees it.*** *Added by the layer check, **2026-08-02**, conversion-dated. The
schema default is the backstop precisely because the application is the usual
writer — so the version-4 random generator has to be banned by name in the
application's language too, and it is the same function everywhere the corpus
reaches for it: `UUID.randomUUID()` on the JVM, `uuid.uuid4()` in Python,
`crypto.randomUUID()` in Node. Each produces the scatter the time-ordered choice
exists to avoid; each is what an agent writes when the column default is present
and it decides to be explicit anyway. The migration grep is over migration text and
reads none of them; the ban belongs in the same host as* Exactly one
application-side producer *below.*

### Exactly one application-side producer, adopted rather than hand-rolled

**Where the application assign ids itself, exactly one utility produce them, it
wrap a maintained library rather than a hand-written bit layout, and a golden test
pin the layout it emit.**

Application-side assignment is worth having, and the cases are specific: batch
inserts that would otherwise pay a round trip per row to read the key back;
idempotent-create endpoints where the client supply the id and the key's own unique
index do the deduplication; and any escape-hatch store the design have named whose
API mandate client-generated identifiers.

**Hand-rolling the layout is the trap.** A key format is a bit layout with a
timestamp field, a counter field and a version nibble, and it is exactly the kind of
subtle code an unreviewed agent write confidently and wrongly.
`ai-maintainer-principles` own that ground as *A hand-built subtle piece ships with
a safety argument and a stress test* — and the honest reading here is that the
build-versus-buy answer is **buy**, so the obligation is discharged by adopting a
maintained implementation instead of taking it on. **A candidate key format with no
maintained generator on your stack is asking you to hand-build a subtle piece**,
and that is a cost against the candidate, not a detail.

*Check: architecture test that exactly one type construct key values and nothing else
call a generator — **and the banned version-4 generator named in that predicate by
name**, per the directive above. Golden test asserting the emitted bit layout —
version field, timestamp field, monotonic counter. **Off-the-shelf** hosts, both
predicates authored per repo. **Convention**, 2026-06-12; the named-ban clause
**2026-08-02**, conversion-dated.*

***The client is a language nothing here reads.*** *Added by the layer check, same
date, **and corrected the same day by the enumeration check, which found the count
below wrong**. Of the three cases above, the one that hands id generation to code
this repo does not compile is **the idempotent-create endpoint where the client
supplies the id** — the draft said two, counting the escape-hatch store, where this
application is itself the client that generates. Batch inserts generate here too.
The architecture test governs one codebase; the id arriving over the wire was made
by another. **The check that reaches it is an ingress assertion on the contract** —
the version field and the format rejected at parse rather than trusted — and this
skill does not carry one.*

## Where a surrogate key is the wrong shape

### A pure child takes its parent's key plus a sequence

**A detail table that nothing else reference and that no URL address independently
take a composite natural key — parent key plus an ordinal — and no surrogate at
all.** Both halves of the test are computed, per *One mechanical key rule* above:
no foreign key declared to it anywhere in `information_schema`, and no path template
in the committed API document addressing its rows except as a sub-path of the
parent's.

**The payoff is largest exactly where the cost of a wide key is largest.** The
highest-volume table in a system is usually a pure child — journal lines, order
lines, ledger legs — and under this rule it carry no key column of its own, no
generator, and a primary-key index that **is** its dominant access path rather than
a second structure beside it. The precedent is old: document number plus line
number is how the enterprise accounting systems have keyed line items for decades.

**Its URL follow the same shape** — the child address by its natural key under the
parent's path, never by an id of its own.

*Check: the classification job above, plus a schema check that a table classed pure
child declare a composite primary key and no surrogate column. Bespoke.
**Convention**, 2026-06-12.*

### An externally governed code is already a key

**Where an outside authority own the code space and guarantee its stability —
ISO 4217 currency codes, ISO 3166 country codes, and reference data of that
shape — the code is the primary key.** Adding a surrogate beside it buy nothing:
the code is already short, already stable, already the value every join and every
payload carry, and the surrogate become a second identifier for the same thing.

The condition is **externally governed**, not merely unique-looking. An internal
code somebody promise not to change is not this case.

*Check: reference tables enumerated in the schema record with the governing standard
named per table. Convention — written artifact, absence visible. **Convention**,
2026-06-12.*

### A library's own tables keep the library's key

**Tables a third-party library create and own — a migration tool's history table, a
scheduler's task table, an event-registry or session store — keep whatever key
shape that library ship, and are out of scope of this repo's rule. No domain table
declare a foreign key into one** — without that the exception spread and the repo
depend on a schema its own migrations do not own. *Trimmed 2026-08-12: probed
pro-default at N=2 (bare sonnet, effort high, 2026-08-11 — both refused the
conforming migration and the foreign key).*

*Check: foreign-key graph assertion that no table outside the library-owned set
reference one. **Off-the-shelf** as a schema query, the owned set listed per repo.
**Convention**, 2026-06-12.*

## The edges every key type pays

### Ids cross the wire as strings whatever the key type is

**Serialize ids as strings on every wire, and do not book that as a cost of the
wide key.** It is a cost of JSON: a 64-bit integer id corrupt silently in a
JavaScript consumer past 2^53. *Trimmed 2026-08-12: probed pro-default at
N=2 (bare sonnet, effort high, 2026-08-11 — both declared the bigint id
`type: string`, citing 2^53).*

**Export formats are the second edge, and this one is honest uncertainty.**
Columnar formats have a UUID logical type whose support across writers and readers
is uneven. Until it is verified end to end in the actual export toolchain, a key
render as its 36-character text form in exports — **which is a real size cost, and
it belong in the cost column rather than in a footnote.**

*Check: contract lint asserting every id field declare a string type, and a
round-trip test through the actual export toolchain before any logical-type claim
is made. **Off-the-shelf** for the lint where a committed contract exist.
**Convention**, 2026-06-12.*

***The document declares the type and the serializer emits it.*** *Layer check,
**2026-08-02**, conversion-dated. The lint reads the committed contract; what a
consumer actually receives is decided by the **serializer configuration** — a
mapper module, a custom serializer, a field annotation — and by the **generated
client** on the far side. A document saying `type: string` over a serializer
emitting a number passes this lint and truncates in the consumer anyway, which is
the defect the directive names. The check that closes it is a serialization
round-trip assertion over a real payload, not a read of the document.*

### The key is what survives erasure

**Under a right-to-erasure regime the key is usually what remain.** Where a record
link to something retained — a ledger, a contract, a statutory window — the lawful
answer is anonymization rather than deletion, with **the key retained as the
pseudonym** that keep the retained rows joinable. Two consequences: **the key
contain no personal data and derive from none** (a key computed from an email or a
name is the erased data, encoded), and object keys and log lines carry the key,
**never a name** — the key is what appear in places the erasure sweep cannot
reach. *Core trimmed 2026-08-12: probed
pro-default at N=2 (bare sonnet, effort high, 2026-08-11). The 2026-08-01 clause
below is unprobed and stays.*

**One interaction the source records do not state, added here and marked as this
conversion's own.** A time-ordered key retain the row's creation instant *after*
anonymization, so a repo whose erasure story lean on the key as pseudonym have
retained one more fact than it may have intended. In most designs that is
acceptable and already published — but it is a decision, and no record read for
this skill made it.

*Check: schema record naming the erasure class per table and the retained-identifier
set; grep asserting object-storage key templates and log field sets carry the key and
no name field. Bespoke. **Convention**, 2026-06-12 — except the time-ordered-key
clause, **2026-08-01, conversion-dated**.*

***A path concatenated at runtime is a template the grep never sees.*** *Layer
check, **2026-08-02**, conversion-dated. The grep reads committed templates. An
object key built by string concatenation at the call site, a log field set assembled
from a map, and a filename a third-party library chooses are the same three shapes
`money-storage` names for runtime-assembled query text, and they carry the same
blind spot — with one difference that makes it worse here: **the value lands in a
control-plane log the repo does not own and cannot sweep**, so a name that reaches
it is not retractable.*

## Composite shapes a repo assembles out of the key

**`enforceable-rules`' composite-shape check, run 2026-08-02, conversion-dated.**
The directives above govern primitives — a row key, a composite child key, an
externally governed code, a library's own key, a human-facing number, an id on the
wire. **A repo assembles things out of two of them, and naming an undecidable
property inside each directive does nothing to surface a shape nobody wrote a rule
about.** That is the failure this check exists for, and this skill had it: every
shape below was decided by nothing here until this table was written. **Silence
about a shape is a defect in this section, not the reader's problem.**

**This table promotes no marker and adds one ban.** Most entries are a verdict that
already followed from a published directive and was never stated as a shape; those
name the directive that decides them. The one ban carries its ground, the
organisation fact it rests on, the absence of a panel, and the condition that
reopens it.

| Shape | Verdict |
| ----- | ------- |
| The key as a **partition or shard key**, range-partitioned | **permitted with conditions, and the conditions are unmeasured.** A time-ordered key sends every insert to the newest partition. That is the same fact *Check the key-cost folklore* books as the benefit — right-edge insert locality — restated at a level where it becomes a hot partition, and nothing in this set has measured either. Hash-partition, or partition on a business column, or accept the hot partition deliberately |
| A **composite child key three levels deep** — parent key, ordinal, ordinal | **not reachable under *A pure child*, and this is derived from the published test rather than newly banned.** A grandchild declaring a foreign key to the middle table makes that table referenced, so it fails the pure-child test and takes a surrogate. **The chain caps at one level**, and no directive said so |
| The key inside an **object-storage path** | **permitted, and it is the shape *The key is what survives erasure* requires** — the key, never a name. Residue that directive's own 2026-08-01 clause does not extend to: with a time-ordered key the path publishes the row's creation instant into a control-plane log **this repo does not own and cannot sweep** |
| The key inside a **cache key** | **out of scope here, owned by published `caching` `C-6`** — the cache key is the loader's full argument tuple with the caller's authorization scope as one of its arguments, and hand-built key strings are banned. Install `caching` in any repo that caches a row |
| The key as a **client-supplied id on an idempotent create** | **permitted, and named by *Exactly one application-side producer*** — the key's own unique index does the deduplication. **It is not an idempotency key**: `money-api` `M-17` defines that as a client-supplied value with a hash of the request body, written in the money effect's transaction. Two mechanisms, two identifiers; do not let one stand in for the other |
| The key as a **correlation id** | **permitted as a logged field, never as the correlation id.** `java-backend-observability` owns request identity — correlation fields established by visible wrappers, and an error response carrying only the correlation id. A row key is not a request identity, and merging them collapses two grep namespaces exactly as *The opaque key and the human-facing number* forbids for the third |
| The key **derived from another identifier** — a hash, a UUIDv5, any deterministic function of committed inputs | **banned** — grounds below |
| The key and the **business number in one payload** | **permitted, and it is the designed shape.** *The opaque key and the human-facing number* decides which does which job |
| The **business number as a URL identifier or a foreign-key target** | **banned by *The opaque key and the human-facing number***, restated here because a shape table that omits it reads as permitting it |
| The key **rendered into a human-facing document** — an invoice, a letter, a code a person reads out | **that is the business number's job**, same directive. The key is not a display value |
| An **externally governed code inside a composite key** of a keyed table | **permitted** — the code is its own table's key and the value every foreign key carries. Condition: *externally governed* means the authority publishes retirements and successors, so the reference table carries the code's **lifecycle**, not only the code |
| The key in a **message payload or an outbox row** | **permitted, and it is the ground the hybrid candidate lost on** — cross-module events legitimately carry it. The message's *own* identity is a different identifier, `async-handoff` `E-7`, and the two rules do not transfer |
| The key in a **read replica or a reporting store** | **permitted, and under-covered.** The `ORDER BY` ban's query-text lint reads this repo's committed SQL; a reporting or business-intelligence tool's own query layer is outside it, and that is where a sort on an id is most likely to be written (layer check, 2026-08-02) |
| **Two ids in one pagination cursor** | **permitted with conditions** — the four constraints of *A time-ordered key is not an ordering*, cursor opaque and sealed |

### The one ban

**A key derived from another identifier — a hash of a natural key, a UUIDv5, any
deterministic function of committed inputs — is banned.**

- *Ground.* A derived key is placed by its hash, not by its clock, so it scatters
  inserts across the whole index — **the exact behaviour the time-ordered choice
  exists to avoid**, reintroduced by a route no directive above watched. And where
  the derivation reads a natural key, the key becomes derivable from personal data,
  which *The key is what survives erasure* bans outright.
- *Organisation fact it rests on.* This repo's verdict rests on insert locality and
  on the key remaining a pseudonym after erasure. Both are properties of this
  decision, not of key design in general.
- *No panel.* Same position as everything else here: the case was written by the
  conversion, and nobody argued the other side.
- *Reopens when* the store's write position stops being key-ordered — a
  hash-partitioned or log-structured engine where insert locality is not a property
  of the key — **or** when a repo needs a re-derivable row identity badly enough to
  pay the scatter, in which case it is choosing a different key strategy and should
  record it as one. **`async-handoff` `E-7` is not that case**: a message identity is
  a different identifier and stays deterministic.

## The worked case — one repo, 2026-06-12

**One org's verdict, kept as evidence the directives above discriminate. Not a
template.** That repo is a single multi-tenant financial backend on PostgreSQL, agent
as sole maintainer, whose REST API is a sold product banks integrate against and
whose tenants move between database cells by logical replication.

**The verdict: every table's surrogate key is `id uuid NOT NULL DEFAULT uuidv7()`.**
Pure children take a composite natural key instead. Standards-defined codes stay
natural. Library tables keep their own. Sequences banned everywhere — `serial`,
`bigserial`, `GENERATED ... AS IDENTITY`, `CREATE SEQUENCE` — with sequential business
numbers implemented as transactional counter rows in the tenant schema, so a tenant
move carry **zero** sequence-reset obligations. **It cost roughly a quarter more
index and heap footprint on keyed tables, and 36-character ids in every URL and log
line** — booked, not discovered.

**The candidates it beat, and the ground each lost on:**

- **bigint `GENERATED ALWAYS AS IDENTITY` everywhere** — smallest indexes and the
  best token ergonomics, lost on **the sold API**: raw sequential ids in URLs are
  enumerable and leak volume and growth, forcing an external-id retrofit later
  anyway. Plus a two-to-four-hundred-sequence reset obligation per tenant move.
- **Hybrid — bigint internally, uuid `external_id` on API-exposed roots** — the
  strongest-sounding compromise, lost because its enforcement core, an internal-id
  wrapper type with no JSON serializer, **collide with that repo's own outbox**:
  cross-module events legitimately carry internal ids, so the rule become
  serialization-context-dependent and "which context is this DTO in" become a
  standing judgment call.
- **TSID / Snowflake, 64-bit time-sorted** — eight bytes **and** time-sorted, the
  only candidate getting both, lost on node-id coordination whose failure mode is
  **silent key collisions on the money path**, single-maintainer libraries, no native
  generation in the engine, and near-zero entropy meaning a sold API need an external
  id anyway.

**One directive this worked case half-fails, stated because silence would read as
coverage.** Its two re-open triggers are both conditions on the winner; nothing state
what would make the hybrid or TSID worth re-examining, which is what
`backend-stack`'s *Record the losers and their grounds* require — **and that skill's
own worked case half-fails it the same way.** Inventing a trigger nobody set would
author the pass's verdict rather than record it.

**The rest is evidence and sit one hop away in [evidence.md](evidence.md):** what each
candidate won on, the comparable products the pass cited, the full cost booking, the
two winner triggers and what makes one of them executable — it is measured against a
**committed baseline for the losing candidate** — and what the record does not carry.

*Check: none — this a record of a decision, not a directive. Grounds **convention**,
2026-06-12.*


## Wiring the gates

Run once, in a repo adopting this skill. Record what got wired and what got skipped
with reason — skipped item with no reason read as done by the next session.

1. **Migration grep** — primary-key column shape, the sequence ban, the banned
   random generator by name. Exit code, over migrations in the diff. **Point it at
   the changelog format and the mapping annotations this repo actually uses**, not
   at `CREATE SEQUENCE` alone.
2. **Table classification job** — foreign-key graph from `information_schema` crossed
   with the committed API document's path templates; fail on a table whose declared
   class disagree with the computed one.
3. **`ORDER BY` ban on id columns**, in **two hosts**: the architecture-test host over
   query-builder calls, and a lint over committed query text, views, functions and
   migrations — with the pagination helper named as the single scoped exemption in
   both. One host alone leaves the ban written in a language it cannot read.
4. **Contract lint** — every id field declare a string type; no id in any declared
   sort vocabulary; no path template bind a densely sequential id. **Plus a
   serialization round-trip over a real payload**, because the document is not what
   the consumer receives.
5. **Key-producer test** — exactly one type produce key values; the version-4
   generator banned by name in the same predicate; golden test pinning the emitted
   bit layout.
6. **Cross-tenant and cross-principal probe** — a valid foreign id return the same
   bytes as an id that never existed.
7. **Generated database classes** — assert the key column's generated type match the
   declared one, and run the generation twice under varied timezone and locale, per
   `guardrails-toolchain`'s *Every committed generated artifact is byte-reproducible*.
8. **Write the move procedure now, with its reset step count**, even if no move is
   planned. A procedure written after the first move is a procedure written under
   pressure.

**Which of these fail a build off the shelf, named rather than counted:** the
migration grep, the `ORDER BY` architecture test, the contract lints where a
committed document exist, the serialization round-trip, the key-producer and golden
tests, the probe suite, and the generated-class assertions. **Bespoke:** the table
classification job, the `ORDER BY` query-text lint, and the move-procedure artifact,
which gate nothing by itself.

## Named gaps — where no check reaches

- **No check catch a surface nobody listed.** The criterion is an enumeration, and
  `enforceable-rules`' predicate check is the one most likely to bite here: the
  surface list is given by example — URL, log, payload, export, replication stream,
  escape-hatch store — and a repo with a surface outside it get a green selection
  record and a wrong key.
- **`enforceable-rules`' layer, predicate and composite-shape checks were all run
  over this skill on 2026-08-02**, and its enumeration and token-placement checks
  were not. The layer check found a
  second language beside the named check of *Count the manual steps*, *A time-ordered
  key is not an ordering*, *A key is never a capability*, *The opaque key and the
  human-facing number*, *The schema default is the backstop*, *Exactly one
  application-side producer*, *Ids cross the wire as strings* and *The key is what
  survives erasure*, each now carrying that second language beside its check. It
  cleared *One mechanical key rule* and *A pure child*, whose classification job
  reads the foreign-key graph and the API document and so was already written
  across both languages, and *A library's own tables*, whose value never leaves the
  schema. **It left one open rather than closing it**: the enumerable-key contract
  lint reads the committed API document, and a route declared only in framework
  annotations binds an id the document never mentions. The remedy is a route-table
  assertion this skill does not carry — **and a stack whose document is *generated
  from code* has it for free**, which `java-backend-api` is, found by opening that
  skill on 2026-08-02 rather than assuming. So this gap is real for a repo whose
  document is hand-written or generated from a separate specification, and closed
  for one whose document is regenerated and diffed from the routes themselves.
  The check also found one stated gap
  that was **false in the direction that matters**, claiming coverage the named host
  could not deliver. The predicate check widened this skill's own load trigger,
  which had been framed on creating a table while three of its directives govern
  things nobody creates a table to do: an object-storage key template, a
  human-facing number format, and an id generated in application code. **The
  composite-shape check produced *Composite shapes a repo assembles out of the key*
  above** — every entry in it was decided by nothing here before that date, and the
  check's own limit applies unchanged: producing the list is the work, and nothing
  can tell you the list is complete.
- **The classification job need a committed API document for half its input.** Where
  none exist, the pure-child test have only its foreign-key half, and the exception
  class silently widen.
- **Nothing verify the ordering non-property, and the ban reaches less SQL than it
  reads as reaching.** Corrected **2026-08-02** by the layer check, which found this
  entry claiming the ban "catch the SQL" while the check line beside it named an
  architecture test as its only host — a host that reads bytecode and never reads
  query text. With the query-text lint added the ban catch the committed SQL and
  the builder calls; it still do not catch SQL assembled at runtime, application
  code that read rows in key order from a set and assume it, nor a report that sort
  in memory. The ban is over two constructs; the assumption is a belief.
- **The benchmark is unreproduced and the engine facts are undated beyond the
  record's own date.** They are the fastest-decaying claims here — a major engine
  release change generator availability, index behaviour and the numbers together.
- **Cost measured on one shape only.** The recorded costs come from one schema at one
  scale. Nothing in this set have measured a key strategy at the volume where its
  re-open trigger would fire, which is the only place the decision is actually tested.
- **No outcome measured anywhere.** One repo decided this way; none decided the other
  way. Central claim marked *uncertain* for exactly that.

## Where the rest of this lives

- **`java-backend-rules`** — the migration and generated-class rules the gates above
  sit on for one stack: committed Flyway migrations, migration lint for lock and
  rewrite hazards, generated database classes regenerated and diffed. **It carry no
  primary-key rule of its own**, which is the gap this skill fill.
- **`java-backend-api`** — keyset pagination and the pager carve-out on that stack.
  Its carve-out directive is written conditionally, on whether the repo ban
  `ORDER BY` on a synthetic id at all. **This skill is where that ban is published**,
  and the condition stay real for a repo that install one and not the other.
- **`async-handoff`** — message identity, and **it is a different identifier from
  this skill's key.** `E-7` require a message identity that is a *deterministic
  function of committed inputs*, so redelivery re-derive the same value. A row key
  is deliberately **not** that — it is assigned once, from a clock and a counter, and
  nothing re-derive it. **Do not carry either rule over to the other**: a
  deterministically derived row key give up the insert locality this skill's verdict
  rest on, and a clock-assigned message identity break deduplication on replay.
- **`money-storage`** — what the money columns of those tables must be, appended
  effect rows, and the guarded update. It constrain the row's contents; this skill
  constrain its identity.
- **`ai-maintainer-principles`** — *One idiom, imposed mechanically*, which is the
  ground under this skill's insistence on a computed classification, and *A
  hand-built subtle piece*, which is the ground under adopting a key generator rather
  than writing one.
- **`java-backend-observability`** — request identity on that stack, which the shape
  table above keeps separate from a row key. **And the closest thing this skill have
  to independent corroboration**: its *Domain types are unloggable by type* directive,
  written 2026-07-27 by a different pass from a different source, say *log entity ids,
  never names or account numbers* — the same split as *The opaque key and the
  human-facing number* and the same log rule as *The key is what survives erasure*,
  reached without reference to either. **It corroborate nothing about the key choice**,
  only the two-identifier split and what a log line may carry.
- **`guardrails-toolchain`** — which tool may occupy a gate at all, and the
  byte-reproducibility rule the generated-class step above defer to.
- **`backend-stack`** — *Record the losers and their grounds*, the bar this skill's
  worked case is measured against and half-fail.
- **`enforceable-rules`** — *Distrust what the agent picks*, the incompleteness
  checks, and **the enforcement markers and status tier** every check line here
  carry.
- **`tech-decision-research`** — **defines the four confidence markers** every claim
  here is graded in, and the downgrade rule that land all of them at convention.

## Markers, dates, and what they mean

**Every directive is *convention*.** The source record ran a three-way adversarial
evaluation and recorded grounds per loser, which is more structure than most
prior art in this set carry — and it still **cite no primary source for any claim
in it**, so nothing here reach *primary-source verified*, let alone *confirmed*. A
reader who need more must re-verify from the engine documentation and the RFC
directly.

**Central claim — that key type is decided by the surfaces the id land on rather
than by storage cost — is *uncertain*.** Argued, never measured.

**Dates below are the record's, not a verification date:**

| Directive | Date |
| --------- | ---- |
| Every directive under *Choosing the key*, *What the key may never mean*, *Generating it*, *Where a surrogate key is the wrong shape*, and *Ids cross the wire as strings* | 2026-06-12 |
| *The key is what survives erasure*, apart from its final clause | 2026-06-12 |
| The time-ordered-key-survives-anonymization clause of that directive | 2026-08-01 — conversion-dated, stated in the directive |
| Every *layer check* clause added beside a check line, and the widened load trigger in this skill's own description | 2026-08-02 — conversion-dated, each stated where it sits. **These add no directive and promote no marker**: each names a second language the existing directive already binds and the existing check never read |
| *Composite shapes a repo assembles out of the key*, and its one ban | 2026-08-02 — conversion-dated. **Convention**, and weaker than the directives it derives from: most entries restate what a published directive already decided, and the ban is the conversion's own with no panel behind it. See its grounds and re-open condition in that section |

**Enforcement markers sit beside each check.** The ones carrying an off-the-shelf
host are named rather than counted: the migration grep, the `ORDER BY` architecture
test, the key-producer and golden-layout tests, the authorization probe, the
library-table foreign-key assertion, the wire-type contract lint and its
serialization round-trip. The table classification job, the `ORDER BY` query-text
lint, the business-number checks, the erasure-scheme greps and the selection and
move records are **bespoke or convention**, and each check line say which.

Evidence, sources, the reading window and the do-not-cite list are in `evidence.md`.
