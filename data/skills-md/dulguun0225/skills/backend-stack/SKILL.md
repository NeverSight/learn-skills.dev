---
name: backend-stack
description: How to choose a backend stack for a repo whose code is written by LLM agents and read line by line by nobody — rank candidates by what their build can refuse to ship rather than by what they let you express, count the independent enforcement hosts a stack offers rather than its type-system features, prefer a stack where the wrong call cannot be written over one where it is written and then flagged, price corpus gravity as a cost the winner carries rather than a reason it won, and treat operability as a veto rather than as the deciding criterion. Carries this skill set's own worked case, Java with Spring Boot Web MVC, jOOQ and PostgreSQL, with the language-layer losers — C#/.NET, Kotlin, Go and TypeScript, each with the ground it lost on — plus the verdict on every shape an organisation assembles out of stack choices — a second stack beside the first, a second language inside one repository, and a rejected candidate that arrives as a dependency anyway. ALWAYS load before picking a language, runtime, web framework, persistence library or database for a new backend, before arguing that an existing stack should change, before adding a second language to a repository or an organisation, and before writing a rule set for a stack nobody has justified in writing.
---
# Choosing a backend stack for code nobody reviews

**This skill argue the choice.** Every other stack-shaped skill here —
`java-backend-rules`, `java-backend-api`, `java-backend-observability`,
`money-java`, `caching-java`, `async-handoff-java` — assume choice already made,
state rules that follow. This one say *why* one stack beat another, on criterion
that only apply when no human read code.

**Two halves on purpose.** Criterion portable, and criterion is payload: it
decide Go, .NET or TypeScript question same as it decide this one. Worked case =
Java on Spring Boot Web MVC, jOOQ, PostgreSQL — there as *evidence criterion
discriminate*, not thing to copy. Reader on other stack apply criterion, get own
answer.

## The marker ceiling, before anything else

**Everything here is *convention*.** Read literal — argument below strong, and
strong argument read like verified one.

- **Criterion is this skill set's synthesis of criteria the pass did write
  down.** Platform pass listed five things stack must maximise — compile-time
  error surface, test-ecosystem quality, exact decimal money math, minimal
  operational surface, idiom stability across sessions — and this skill
  generalise first, second and fifth into one criterion. **Generalisation is
  the part nobody checked**: no panel argue other side, no outcome measured, no
  backend built on stack picked by rival criterion and compared. Central claim:
  ranking stacks by build-refusable defects beat ranking by expressiveness,
  velocity or hiring pool for machine-written code. **That claim uncertain, not
  convention** — marked *uncertain* where it appear.
- **Java verdict inherit one date, no markers.** Platform pass ran
  **2026-06-11..14** and its record is dated **2026-06-12**; it recorded
  rejections + grounds at both layers **with no per-claim confidence marker**.
  So *convention* is floor here, not verdict anyone wrote down. Primary sources
  behind those grounds not published here — owed, and the four gaps are named in
  [evidence.md](evidence.md).
- **Only non-opinion thing here is host census**, and it not research: it grep
  over published skills, dated, stated in [evidence.md](evidence.md) with its
  command so anyone re-run it and watch it move.
- **Lapse rule vacuous here — stated, not hidden.** Past `review-by`, every
  *confirmed* marker read as *convention* with no maintainer action, and
  **nothing here above convention**, so rule demote nothing. Stated because
  every sibling skill carry `review-by` and silence look like omission. Cost
  real: **nothing make this skill's age visible.** Conversion date
  **2026-08-01** — conversion date, not verification date.

Status tier: **decided, not yet validated** — researched and decided, **no
production use yet** behind criterion as criterion.

## The premise

**Code written by LLM agents. No human read it line by line.**

Every directive below hang on it. This the one skill where dropping premise
don't weaken rules — it **delete them**. If human read every diff, reviewer is
enforcement host, count below is noise, and stack should be picked on velocity,
hiring, operability like normal. Verdict travel exactly as far as its premise;
this one travel no further than first sentence.

**Two things premise not say.** Not say code unowned — someone answer for it in
production. Not say agent careless. It say the *line-by-line reading* that used
to catch defects below is gone, and nothing replace it but build.

## The criterion

### Rank a stack by what its build can refuse to ship

**Deciding question not what stack let you express. Question is what its build
can refuse to ship.** Two stacks that both express correct implementation are
not equal when no human read diff: the one that mechanically reject the wrong
implementation has property the other lack, and under premise it the only
property left standing.

Expressiveness, terseness, velocity, library breadth all describe how easy
*correct* program get written. Under this premise binding constraint is not
that — agent write plausible code at any terseness — it how reliably wrong one
get stopped with no reader. **Stack's ceiling = set of defect classes its build
can name and reject.**

*Check: decision record rank each candidate by defect classes its build reject,
and ranking written before any candidate named winner. Convention as enforcement
— no build host this, check is written artifact, absence visible; record written
after winner picked still pass. Confidence **convention**, 2026-06-11..14.
Criterion itself **uncertain** — no outcome measured against stack picked
another way.*

### Count the independent enforcement hosts, not the type-system features

**Type system is one host. Ask how many independent hosts stack offer, and what
fraction of intended rules each carry.** Stack with strong types but no
architecture-test library, no compiler-plugin surface, no container-test story
is weaker under this premise than raw type comparison suggest, because most
rules a repo need are not expressible as types.

Hosts worth counting are ones that **fail a build**, and they not
interchangeable — each reach different defect class:

- **Compiler**, for what can be type error.
- **Compiler plugin / annotation processor**, for what compiler won't do native
  — nullness, non-loggability, banned API on compile path.
- **Architecture test**, for reachability and layering no type express — which
  package call which, which construct appear where.
- **Bytecode, AST or source-level rule**, for constructs architecture test can't
  see into.
- **Schema, contract or migration lint**, for artifacts that not code.
- **Contract diff**, for changes that compile and still break.
- **Property or fuzz generator**, for input space written test miss.
- **Real-dependency container test**, for behaviour only real engine have.

**Count these, per candidate, before ranking.** Stack missing one entirely has a
rule class it can only carry as convention — and convention is what this premise
strip the reader from.

*Check: decision record list hosts per candidate with named tool for each, and
mark host-less ones as gaps instead of dropping them. Bespoke — record greppable
for tool names, completeness not. **Convention**, 2026-06-11..14.*

### Prefer a stack where the wrong call cannot be written

**Between two stacks that both reject a defect, prefer one that reject it
earlier — at writing, not at building.** Absent method, uninstantiable type,
factory that take no free-text parameter, unreachable constructor: these correct
agent while it write the call. Build failure correct it after, in a run somebody
can be tempted to override.

This is `enforceable-rules`' *unwritable beats banned* principle one altitude up
— platform choice, not rule design. Stated, not restated: **that skill own the
principle and its grounds; this one only say principle discriminate between
stacks, not just between rule designs.** Install `enforceable-rules` for
argument.

Stack property that matter is narrower than "good type system": can a library
author make a call *unrepresentable* — sealed hierarchies, package-private
constructors, absent methods on interface outsider can't implement — and does
ecosystem use that power or route around it with reflection and runtime config.

*Check: for each rule stack must carry, record state whether it land as
type-design constraint or as flag, and count of first category is stated input
to ranking. **Convention**, 2026-08-01 — conversion-dated statement of principle
platform pass did not write in this form.*

### Price corpus gravity as a cost the winner carries

**Idiom LLM generate for a stack by default = that stack's corpus gravity. It
cost, not feature.** Where corpus-dominant idiom is runtime-silent — config that
change behaviour invisibly, annotations whose effect not at call site,
conventions resolved by reflection at startup — every future agent session pull
toward it, and repo pay permanent ban list plus enforcement to make bans stick.

**Asymmetry is what make this decision input, not complaint.** Big-corpus stack
generate more plausible code faster *and* drift harder toward that corpus's
defaults. These don't cancel: first is one-time gain per feature, second is
standing cost at every later session, and second compound while nobody read
diffs.

**Stack may win while carrying heavy gravity cost** — this one did. Criterion
forbid counting big corpus as advantage without booking drift against it, or
finding ban list later and calling it unforeseen tax.

*Check: record name stack's corpus-dominant idiom, state whether it
runtime-silent, and list bans the choice require — before choice final, so ban
list is priced input not discovery. **Convention**, 2026-06-11..14 — platform
pass recorded rejections and grounds; this generalise what it did.*

### Operability is a veto, not the criterion

**Team must be able to run winner in production. That veto over ranking, not the
thing ranked.** Stack nobody present can operate lose no matter how many defect
classes its build reject, because rules protect a system that must be running to
matter.

Veto not criterion, because they give different answers: as criterion it pick
whatever team already run and guardrail question never get asked; as veto it
kill the unrunnable and let guardrail question decide rest. **Under premise
where nobody read code, "we already know it" is not a guardrail.**

Operability facts that veto are concrete, write them per candidate: who ran it
in production, what deployment target already support, what on-call story is,
whether observability rules this set publish can be hosted at all.

*Check: record state operability veto per candidate as fact about *this team*,
not general property of technology, and state it separate from ranking.
**Convention**, 2026-08-01, conversion-dated — the rejected wider reading,
operability as the dominant criterion, is on the record in
[evidence.md](evidence.md).*

### A rule set is never a reason to adopt a stack

**Good rule set existing for a stack is not evidence stack is good choice, and
this skill set is not evidence for its own platform.** Reasoning circular in way
easy to miss when rule set is artifact in front of you — fifteen skills on one
stack look like accumulated justification. They accumulated *consequence*.

Sentence survive from `java-backend-rules`, which carried it before this skill
existed. It the reason host census is stated as **re-runnable grep with a
date**, not as claim: census of this repo's own tool names is evidence about
**Java's enforcement surface** — fact about ecosystem — and *not* evidence
choosing Java was right.

*Check: no directive anywhere in this skill set cite existence of another skill
here as ground for platform choice. Bespoke and unbuilt — grep find citation
shape, not reasoning. **Convention**, 2026-08-01.*

### Record the losers and their grounds, or it is a preference

**Stack decision with no written losers is preference in decision's clothes.**
Name every candidate, why each lost, and condition that reopen it. Losers are
load-bearing half: "we use Java" override no instinct; "corpus default here is
X, rejected because dominant idiom runtime-silent and no host can reject that"
does.

**Matter more for stack choice than for any rule**, because stack is the one
decision every later rule hang on, and the one nobody re-derive. Agent asked to
add a service two years out will read rule sets, infer stack from them, never
see an argument.

**This skill fail half its own directive**, and say so instead of hiding it.
Losers and their grounds recovered 2026-08-01 and stated below; **re-open
trigger per loser never recorded by the pass and not invented here** — see *What
is recorded and what still is not*.

*Check: decision record name each candidate, its ground for losing, and re-open
trigger. Convention as enforcement — check is written artifact, catch omission,
can't catch rationalisation written after fact. Confidence **convention**,
2026-06-11..14.*

### Enforcement-tool maturity is a separate question from runtime maturity

**Ask how old and how maintained the *enforcement* tools are, separate from
language and runtime.** Mature runtime with young or unmaintained guardrail
tooling score worse under this premise than version numbers suggest — rules
hosted by tools, not by runtime.

Questions per host are ordinary and asked about the tool, not the platform: is
it maintained, what release cadence, does it work on pinned language version,
what happen to every rule it carry if it stop. **Stack where one tool host most
rules has single point of failure version numbers don't show** — live condition
here, where one architecture-test library appear in more files than any other
host.

*Check: record date each named host and state which rules die with it. Bespoke
and unbuilt. **Convention**, 2026-08-01.*

## The worked case — Java, Spring Boot Web MVC, jOOQ, PostgreSQL

**Verdict, dated 2026-06-11..14, marked convention.** Criterion applied once. Not a
recommendation to adopt this stack, and by *A rule set is never a reason to adopt a
stack* it cannot be read as one. **The record it come from is not published in this
skill set**, so everything here is restated, not a pointer a reader can open.

**Winner — JVM, Java 25 LTS**, on verification-platform merit: every ground the pass
gave is a host or a fail-loud default, not an expressiveness claim — pitest as the
mutation ratchet, Error Prone as the one cheap host for *custom* compile-time checks,
sealed interfaces plus exhaustive switch, `BigDecimal.divide` throwing with no
rounding mode, Spring Modulith, and the deepest banking-domain corpus.

**Losers, each with the ground it lost on** — the half of this record that overrides
an instinct, so it stay in directive text:

- **C#/.NET**, close second — silent zero-defaults on deserialization, and **open,
  non-exhaustive enums**, so state machines are not compiler-checked.
- **Kotlin** — mutation testing commercial-or-noisy on its bytecode, and a stdlib
  **silently-rounding `BigDecimal /` operator**.
- **Go** — **no maintained mutation testing**, statement-only coverage, and pervasive
  silent zero-values landing in money code. It lost **despite** the best ops story of
  the four, which is *Operability is a veto, not the criterion* in practice.
- **TypeScript backend** — no enforced decimal type. Disqualified outright for a
  ledger.

**What the choice costs, booked rather than discovered.** Java on Spring Boot is near
worst case for corpus gravity, and the ban lists are the bill: the corpus-dominant
idiom for this stack is runtime-silent almost everywhere it matter —
annotation-driven transactions, caching and scheduling, JPA dirty checking, field
injection, annotation-bound message consumers, `-javaagent` bytecode weaving. **Every
one banned by name in a sibling skill, each with a check**, cuz corpus advantage
self-cancel. Those bans live in `java-backend-rules`, `caching` and `caching-java`,
`async-handoff`, `java-backend-observability` and `llm-default-traps`;
`ai-maintainer-principles` own the line they get drawn on — startup-loud machinery
kept, runtime-silent banned — so a repo reading only a ban list have no way to tell
which framework machinery survive it.

*Check: none — this a record of a decision, not a directive. Grounds **convention**,
2026-06-11..14. Re-open trigger per loser **not recorded by the pass**, and not
invented here.*

**The rest of this record is evidence and sit one hop away in
[evidence.md](evidence.md):** the pass's full candidate list and what each candidate
had, the dated enforcement-host census and the grep that re-runs it, the one
competing census that exist — TypeScript, frontend, same org, role-confounded — and
what the record does not carry: primary sources, a backend-role competing census, a
re-open trigger per loser, and a criterion ever selected against a real alternative.


## Composite shapes an organisation assembles out of stack choices

**`enforceable-rules`' composite-shape check, run 2026-08-02, conversion-dated.**
Directives above govern one decision: a candidate, its enforcement hosts, its corpus
gravity, its operability veto, its losers and their grounds. **An organisation build
things out of two of those and this skill decided none of them** — which matter here
more than the section's usual reason, cuz the organisation this worked case come from
**already run more than one stack**, and the competing census in
[evidence.md](evidence.md) is drawn from its frontend. Every entry marked; **silence about a shape is a defect in this section.**
The table promote no marker and add **no ban**.

| Shape | Verdict |
| ----- | ------- |
| **A second stack in the same organisation** — a frontend, a data pipeline, a function in another language | **permitted, and it is the actual condition here, not a hypothetical.** The competing census in [evidence.md](evidence.md) is a *frontend* profile, so the pass that produced this worked case had already made a second choice. What no directive say: **the host census, the gravity price and the rule sets are per stack, and none of them reach the second one.** Condition: each stack carry its own census and its own record, and **the rule sets published for the winner be read as binding nothing outside it** — a repo that assume otherwise have a defect class covered on one side of a language boundary and nowhere on the other |
| **A second stack inside one repository** — a worker, a build tool, a test harness, a script | **permitted with conditions, and the conditions are absent.** *Count the independent enforcement hosts* count them for the language the service is written in. **A repository's build scripts, its code generators and its test fixtures routinely run on a different one**, and every host counted for the winner reach none of it. Condition: the census state which parts of the repository it cover, so the uncounted parts are visible as a blank rather than absent from the question |
| **A rejected candidate that arrive as a dependency** — the losing runtime running the frontend build, the CI actions, the scanners, the code generators | **permitted, and this is the entry most likely to be missed.** A stack can lose the ranking and still be **operationally load-bearing**, and when it arrive that way it arrive with none of this skill's machinery: no operability veto applied to it, no gravity priced, no losers recorded. Condition: **a rejected candidate present in the build is a load-bearing dependency**, and `ai-maintainer-principles`' *Price the bus factor by failure shape, with an exit ladder* govern it from that moment — not this skill |
| **An enforcement host that exist but whose gate is advisory** | **banned as a filled census row, and the competing census in [evidence.md](evidence.md) is where this was caught.** *Count the independent enforcement hosts* already say hosts worth counting are ones that **fail a build**; the recovered competing census found a category where the tool exist and the gate is advisory with an unresolved upstream issue. **Counting that category as filled is the defect** — `guardrails-toolchain` own the general form, that an advisory tool is the one described as coverage later. Restated here because a census is a count, and a count is this repo's most-recorded failure |
| **Two candidates tied on host count** | **permitted, and the tie is where the other directives start doing the work.** The recovered census have two columns filling seven of eight categories, so **host count did not discriminate and was never going to on its own.** What separated them was one absent category and one advisory gate — then *Price corpus gravity*, *Prefer a stack where the wrong call cannot be written* and the operability veto. Condition: a record that stop at the census have not finished the comparison |
| **One host carrying most of a stack's rules** | **permitted with conditions, and the condition is named in a directive that stop short of it.** *Enforcement-tool maturity* record this as a live condition — one architecture-test library appear in more files than any other host here. What it do not say is what the repo owe because of it. Condition: **the rules that die with each host are enumerated per host**, so the blast radius of one tool going unmaintained is a list rather than a discovery |
| **A rule the winning stack can host nowhere** | **permitted, and already decided** — *Count the independent enforcement hosts* say a stack missing a host carry that rule class as convention, and `enforceable-rules`' accounting rule require it be named as a gap rather than passed over. Restated because a stack chosen on a strong census read as covering everything it was ranked for |

## What this skill does not carry

**No `## Wiring the gates` section, and absence deliberate.** Every directive
here bind a decision made before there is code to check, so nothing to wire into
a build — check is written artifact whose absence is visible.
`tech-decision-research` in same position and say same thing; six of the
language-neutral skills here also carry no wiring section, for different reason
— their gates real and a stack sibling wire them.

**Honest limit, stated not glossed:** these checks catch omission, cannot catch
rationalisation. Decision record written after winner picked, listing losers
nobody seriously considered, pass every check here. `tech-decision-research`
publish the procedure that make record trustworthy — framing written before
candidates named, adversarial panel, steelman for loser — and **this skill
downstream of that one**. Install it alongside.

## Where the rest of this lives

- **`tech-decision-research`** — how to run the decision this skill's directives
  say to record. Define the four confidence markers used above.
- **`enforceable-rules`** — *unwritable beats banned* principle, enforcement
  markers, and premise-specificity test that decide whether a rule earn context
  space at all.
- **`java-backend-rules`, `java-backend-api`, `java-backend-observability`** —
  what follow from worked case, once chosen.
- **`guardrails-toolchain`** — once stack picked, which tool may occupy a host
  and what disqualify one, plus four defect classes a host count never reach.
  **Frontend census in [evidence.md](evidence.md) is that skill's map read from
  other side**; same record, published once, here.
- **`llm-default-traps`** — picks an agent make by training-data default on any
  stack, including ones a fresh stack choice hit first.
- **`ai-maintainer-principles`** — decisions above the stack: how system get cut,
  what stand in for code review, what maintainer must be able to do alone. Drawn
  from same 2026-06-11..14 records as this skill, and carry the governing principle
  those records reason the persistence rejections from.

[evidence.md](evidence.md) carry the grounds, the claims that must not be cited,
and the conditions that reopen each directive.