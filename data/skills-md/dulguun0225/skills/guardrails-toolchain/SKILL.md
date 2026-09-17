---
name: guardrails-toolchain
description: How to choose and compose the machine guardrails that stand in for human code review in a repo whose code is written by LLM agents and read line by line by nobody — adopt only tools whose verdict fails a build by itself, reject the ones that need a standing server to operate or a paid vendor plan to report, keep a non-deterministic reviewer out of any defect class a deterministic gate can own, record the caveat that bites beside every tool so an empty caveat reads as unexamined rather than clean, assign each defect class to the earliest layer that can own it, and gate a measurement only where that measurement is honest. Carries the four whole concerns a tool-by-tool comparison never surfaces — an unguarded performance threshold, end-to-end output stability, byte-reproducible generation of committed artifacts, and semantic diff on every surface a consumer binds to — plus the standing full-system adversarial sweep that catches erosion no diff-scoped review can see, the verdict on every shape a repo assembles out of two gates — a suppression, a generated baseline, a ratchet, a gate scoped by another gate's output, a shared configuration — and one repo's whole tool map as the worked case. ALWAYS load before adopting a static analyser, scanner, coverage or mutation tool, contract or migration lint, before wiring or removing a CI gate, before adding a suppression or a baseline file, before changing branch protection or a shared workflow, and before claiming a defect class is covered.
---
# The guardrail toolchain for code nobody reviews

**This skill about gates themselves — which tool earn a place, and how gates
compose.** Sibling skills state rules and name check per rule. This one state
what make a check adoptable at all, and what whole concerns a rule-by-rule stack
leave unguarded.

**Two halves.** Criterion portable — it decide Python, Go or TypeScript
toolchain same way. Worked case = one repo's map, dated **2026-06-13**, a
tool per concern with what each cost and what each miss. Map there as *evidence criterion
discriminate*, not shopping list.

## The marker ceiling, before anything else

**Everything here is *convention*.** Source = one adversarially fit-checked
research sweep run 2026-06-13 by an org of the shape below, folded into that
project's decision records same day. **It carry no per-claim confidence marker
and cite no primary source for any tool claim.** So *convention* is floor, and
tool facts here are what someone checked in June 2026, not what is true today.

- **Central claim is *uncertain*, not convention**: that running a completeness
  critic over a whole gate stack surface concerns no tool-by-tool comparison
  reach. Sweep did produce four such concerns and they published below, which is
  one run and no control — nobody ran a tool-by-tool comparison beside it and
  compared what each found. Marked *uncertain* where it appear.
- **Tool version pins deliberately not carried.** Sweep pinned exact versions and
  said itself they not load-bearing for selection and must be re-checked at
  adoption. Copying them here manufacture freshness. Where version *is* the rule
  — one dependency ceiling — `llm-default-traps` own it and state value.
- **Lapse rule vacuous here, stated not hidden.** Past `review-by` every
  *confirmed* marker read as *convention* with no maintainer action, and nothing
  here above convention, so rule demote nothing. Stated because every sibling
  carry `review-by` and silence read as omission. Cost real: **nothing make this
  skill's age visible**, and tooling claims decay fastest of any kind in this
  set. Conversion date **2026-08-01** — conversion date, not verification date.

Status tier: **decided, not yet validated** — researched and decided, **no
production use yet** behind criterion as criterion.

## The premise, and the org fact under it

**Code written by LLM agents. No human read it line by line.**

Consequence that make this skill exist: **guardrail is not quality bar, it is the
review.** In a repo with reviewers, failing gate is second opinion. Here it only
opinion, so gate absent = defect class nobody hold.

**Org fact the selection rest on, stated because it change answers:** teams of
about three, no platform or operations role, nobody on rota to run a service.
Team with staffed ops can operate a server, and *Reject a guardrail that needs a
standing server* soften to a cost question for them. Every other directive hold
regardless.

## Choosing a guardrail

### A guardrail is a tool whose verdict fails a build by itself

**Adopt tool that emit machine-readable verdict — exit code, SARIF, JSON — and
wire it to fail build on that verdict; tool whose output need reading is a
report, and under premise nobody read reports.** *(Core desk pro-default,
2026-08-11 audit; the clauses below be the contra half.)*

**Advisory tool may still be adopted, into named advisory lane, never as the
answer for defect class.** Distinction load-bearing cuz advisory tool is the one
that get described as coverage later. Where tool adopted advisory, record say
which class stay **uncovered** — not which tool "watch" it.

`enforceable-rules` own the principle that rule need machine check or it not
rule. **This the tool-side half**: same standard applied to thing hosting check,
so unwired or advisory host no let rule keep calling itself enforced.

*Check: selection record state per tool its verdict mechanism and whether build
fail on it, and no tool appear as host for defect class while marked advisory.
Convention as enforcement — check is written artifact, absence visible.
**Convention**, 2026-06-13.*

***"Fails the build" be a property of four files and the record be a fifth.* Layer
check, 2026-08-02, conversion-dated.** Record state whether a tool fail build.
Whether it actually do is decided in **CI configuration** (is the step allowed to
continue on error), in the **build file** (is the plugin's failure severity set to
error or warning), in the **tool's own configuration** (severity per rule, and
whether a baseline file exempt existing findings) — and, past all three, in the
**hosting forge's branch-protection or ruleset settings, which are not a committed
file at all** (on **GitHub**, the one this skill name elsewhere, that is the
required-status-checks list on a branch protection rule or ruleset).
**A gate can exit non-zero, be listed, be recorded, and still not block a merge**,
cuz which checks are required lives in a settings page nobody diff. That is this
directive's own failure — an unwired host that keep calling itself enforced — one
layer above where it look. **Decidable half: assert the required-check list against
the committed CI job names, from the forge's API, in the build.** Not carried here.

### Reject a guardrail that needs a standing server

**Prefer self-contained CLI or CI-native binary. Reject tool whose analysis
require operated service — dashboard server, standing quality server, hosted
inventory service — no matter how good analysis is.** Server is thing nobody
present maintain, and gate that stop cuz its server drift is worse than gate that
never existed: it report green while stopped.

Not aesthetic. **Server-backed tool move gate's state out of repo**, so answer to
"what does this build enforce" stop being greppable from committed files.

*Check: no gate in build depend on service not started by build itself. Bespoke —
grep CI config for host names and service URLs get most of it, completeness not.
**Convention**, 2026-06-13.*

### Gate on exit codes and committed artifacts, never on a vendor plan

**Where tool have free CLI and paid hosted reporting surface, gate on CLI exit
code and commit its JSON or SARIF output. Never make gate depend on vendor plan,
seat tier or hosted ingestion.** Two failure modes, both real: plan lapse turn
gate off silently, and vendor's free tier change what CLI report.

**This bite in specific place worth naming: security scan upload.** Uploading
findings to **GitHub's** hosted code-scanning surface need **GitHub Advanced
Security** on a private repository, while same scanner's exit code is free. Gate
on exit code, commit the SARIF, treat upload as reporting. **Second reason the
record give, and it independent of price: the scanner's own upload path had an
open defect**, so a lane depending on upload would have been down for a reason
nobody controls.

*Record name one platform; that this generalise to other hosted surfaces is this
skill's inference and no pass checked it.*

*Check: every gate's pass/fail derive from exit code or committed artifact in
repo, and CI config name no upload step as the gate. Off-the-shelf — CI config is
committed and greppable. **Convention**, 2026-06-13.*

### A non-deterministic reviewer is never sole arbiter of a mechanical class

**Adversarial agent review is backstop for semantics only. Where defect class is
mechanical — a taint path, banned construct, incompatible signature change,
unrounded division — deterministic gate own it, and reviewer's finding in that
class is trigger to build gate, not a disposition.**

Ground is asymmetry: reviewer that miss defect leave no trace, deterministic gate
that miss it leave one — the rule it never had. **Treating reviewer as the gate
convert absent rule into invisible one.** And reviewer here share training
distribution with the author, so its misses correlate with author's.

**Practical form:** when review find something in mechanical class, finding
close by adopting or extending gate. Finding disposed inside review — argued,
accepted, closed — leave class exactly as uncovered as before, with a record that
look like coverage.

*Check: review process state which finding classes it may dispose and which it
must escalate to gate adoption, and every escalation name gate that would catch
it. Convention as enforcement — written artifact. **Convention**, 2026-06-13.*

### Record the caveat that bites, per tool

**Every adopted tool carry, beside its row, the specific thing it does not
reach.** Not general disclaimer — the named gap: intra-file-only taint analysis
against a cross-file risk path, bytecode analyser that cannot see string
literals, lint that read committed migration text and nothing about data already
in column, differ that see structure and not meaning.

**Empty caveat field read as unexamined, never as clean.** That is the whole
value of the field: it distinguish tool whose limits somebody found from tool
nobody pushed on.

**Caveat is what force second tool.** Worked case in the map below: bytecode
analyser and source-level analyser both needed, cuz bytecode one cannot see
string literal or raw arithmetic on erased types. Repo that record only "we have
architecture tests" adopt one and believe it cover both.

***A caveat that get encoded stop being a caveat and become an exemption.* Layer
check, 2026-08-02, conversion-dated.** Record hold the caveat in prose. **What the
build read is the suppression** — an inline comment that switch a rule off for one
line, an annotation, a committed baseline file that exempt every finding present on
the day it was generated, a per-rule severity override. Each is a second language
where a recorded caveat become a silent green, and **the baseline is the worst
shape**: it is generated once, it exempt an unbounded set, and its own regeneration
is invisible in any gate this skill require. Nothing here read any of them.
**Decidable half: commit the suppression inventory and diff it, so a new
suppression is a git-visible line at the gate a human read** — same shape `E-26`
and `C-15` use for their catalogs, and not carried here.

*Check: selection record have caveat per adopted tool, empty ones listed as
unexamined. Convention as enforcement — written artifact, catch omission, cannot
catch a caveat written vaguely. **Convention**, 2026-06-13.*

### Licences gate deny-by-default over a committed dependency inventory

**Build generate machine-readable dependency inventory and fail on any licence
not on committed allowlist — including undeclared and unknown.** Deny-by-default
fail by construction on licence nobody anticipated; **adopted tool's own licence
is selection input too** — record it beside the tool with the condition it hold
under (build-only, internal code, never request path). *(Trimmed 2026-08-12 — desk
pro-default, 2026-08-11 audit; the layer clause below be the contra half.)*

*Check: build have licence gate over generated inventory, allowlist committed,
undeclared licence rejected; selection record carry licence column. Off-the-shelf
— licence-gate tools consume standard inventory formats. **Convention**,
2026-06-13.*

***The inventory be generated from the package manifest and code arrive four other
ways.* Layer check, 2026-08-02, conversion-dated.** Gate read a dependency
inventory, which a package manager produce from declared dependencies. **Licensed
code also enter as the container base image's operating-system packages, as
vendored or copied source, as a binary the build download, and as a git
submodule** — none of which the package manager know about, and the base image is
usually the largest set of the four. **Deny-by-default hold only over the set the
inventory enumerate**, so a green licence gate say nothing about the image the
service actually ship. Decidable half is a second inventory over the built image
and a rule that the build download no unpinned binary; **the image scan is
off-the-shelf and the vendored-source half is not.** Neither carried here.

## Composing the gates

### Assign each defect class to the earliest layer that can own it

**Earliest gate win. Defect belong to earliest layer that can reject it, and
later layers exist for what earlier ones structurally cannot see.**

Ordering, from earliest: compile wall; architecture and boundary tests; unit and
property tests; golden and characterization tests; integration against real
dependencies; contract gates; supply-chain and security gates; end-to-end
behaviour; mutation; performance; **coverage**; reproducibility; standing
invariants; agent review last, semantics only.

**Coverage sit below mutation deliberately, and that is the ladder's one
inversion of "earliest".** Coverage is floor, mutation is ceiling: floor prove a
line ran, ceiling prove a test would notice if the line changed. Ordering by
earliest would put coverage first and read as though it caught something mutation
does not. `java-backend-rules` own the floor rule and state the same limit from
its side.

**Two things this ordering is for.** It stop same class being gated twice in two
places that drift, and it make honest answer possible to "where is this caught" —
class caught nowhere is visible as blank row, not hidden by three tools that each
half-cover it.

**Ordering is not ranking of importance.** Late layer catch what no earlier one
can: mutation testing probe whether tests assert anything, which no test can
assert about itself.

*Check: defect-class-to-layer map exist as committed artifact and each class name
one owning layer. Bespoke and unbuilt here — nothing generate this map.
**Convention**, 2026-06-13.*

### A gate only gates where its measurement is honest

**Measurement gate only in environment that support claim it make. Where
environment cannot, signal move to environment that can — production, nightly,
dedicated runner — rather than being asserted where it lie.** **Flaky gate is
worse than no gate** — it train the maintaining agent that a gate is ignorable —
and the worked split live under *Every named numeric threshold* below: relative
ratchet in CI, absolute budget as production alert rule. **Same number, two
homes, split by what each home can prove.** *(Trimmed 2026-08-12 — desk pro-default,
2026-08-11 audit.)*

*Check: every gate state environment its claim hold in, and no gate assert
absolute value in environment that cannot reproduce production topology. Bespoke
and unbuilt. **Convention**, 2026-06-13.*

## The four concerns a tool comparison never surfaces

### Run a completeness critic against the whole gate stack

**Ask, once, what whole concerns the stack omit — not which tool is best per
concern already listed.** Tool comparison answer questions already on list.
Missing concern have no row to lose, so it never come up.

Four found this way in the worked case, and they are the four `###` headings
after this one — unguarded numeric threshold, end-to-end output stability,
byte-reproducible generation, semantic diff on every consumer-bound surface. Each
is class a human-reviewed shop cover with people — someone notice dashboard turn red,
someone remember last release's output — and each need encoding as gate where
those people gone.

*Check: gate-stack record carry a "concerns with no gate" section, written by
asking what a reviewer used to catch, and it non-empty or its emptiness argued.
Convention as enforcement — written artifact. Central claim **uncertain**,
2026-06-13 — one run, no control.*

### Every named numeric threshold has a guardian

**Every performance number a design lean on — latency budget, throughput floor,
wall-clock window — either have gate that measure it, or is prose nobody
measure.** Under premise this cut deep: **agent cannot feel 5× slowdown by
reading diff.** Refactor that double per-transaction work compile, pass every
test, keep every invariant green, and read clean.

**Correctness gates never measure cost.** That is the gap, stated exactly: whole
stack above prove program compute right answer, nothing prove it still compute it
fast enough.

Three layers, split by what each honestly prove:

- **Relative ratchet on CPU-bound hot paths.** Benchmark suite with committed
  baselines, gate on relative delta with band wide enough that runner variance
  never trip it, improvement re-ratchet baseline down in same change. Run on same
  quiesced machine every time or band must be so wide it prove nothing.
- **Contention harness against real dependency, blocking.** For paths whose risk
  is behaviour under N concurrent writers, assert correctness *and* throughput
  floor together. This layer usually already exist as correctness test; adding
  floor assertion is the change.
- **Absolute budgets as production alert rules, not CI gates.** Measured where
  topology real. These are re-architecture triggers, so they page nobody — they
  feed the periodic review that a threshold nobody set out to cross was crossed.
  **Rule that alert rule is committed code with a fire-test live in
  `java-backend-observability`**; this directive only say which numbers belong
  there rather than in a build.

Load profile against production-shaped environment sit between, as opt-in
nightly, never per-change gate — per-change latency assertion against non-prod
environment reintroduce exactly the flake trap.

*Check: every numeric threshold in design docs appear in one of three layers, and
mapping is committed. Bespoke — thresholds greppable where written as numbers,
mapping is not. **Convention**, 2026-06-13.*

### Pin end-to-end output stability, not just invariants and goldens

**Invariants prove internal consistency at one moment; goldens pin cases author
thought of; neither pin that realistic end-to-end output stay same across code
versions.** Gate shape: committed corpus of realistic end-to-end cases run whole
path, rendered output compared against approved copy, **fail on any unapproved
diff** — every output change become explicit committed re-approval.
**Condition this fire under: any recompute-must-match-previous-output assumption
anywhere in system.** Repo that never re-render past output need not carry it.
*(Trimmed 2026-08-12 — desk pro-default, 2026-08-11 audit.)*

*Check: committed approved-output corpus exercised end-to-end each build, diff
fail build. Off-the-shelf — approval-test libraries exist in most ecosystems;
corpus itself bespoke. **Convention**, 2026-06-13.*

### Every committed generated artifact is byte-reproducible

**Repo that commit generated artifacts and gate on their diff must also assert
generation is byte-reproducible and its generators version-pinned.** Otherwise
the drift gate flap on iteration order, locale-dependent sorting or embedded
timestamp — and flapping gate get relaxed, at which point it mask the drift it
exist to catch.

Gate shape: regenerate twice on canonical build image under varied timezone and
locale, assert byte-identical to itself *and* to committed tree; pin generator
plugin versions by checksum.

**Applies to every committed generated artifact, not one.** Client types,
database access classes, permission or endpoint snapshots, module descriptors.

**One instance published in this skill set, and reading the other side prove the
point.** `java-backend-api` carry exactly this gate for the contract document —
regenerate twice under varied timezone and locale in one pinned container, all
three copies byte-identical. `java-backend-rules` carry regenerate-and-diff for
generated database classes and **not** the double-regeneration half, so that
artifact's drift gate rest on generation being reproducible with nothing
asserting it. **That gap is live, it is in this skill set, and it is what this
directive is about** — repo enumerate its own generated artifacts and find the
gate cover a subset.

*Check: enumerate committed generated artifacts, and each appear in a
regenerate-twice job. Bespoke — enumeration is the hard half and nothing
generate it. **Convention**, 2026-06-13.*

### Enumerate every surface a consumer binds to, and give each a deterministic diff

**Published API is one surface. Enumerate rest — event payload schemas, error
code catalogs, permission catalogs, cross-module published types, anything a
consumer bind to — and give each deterministic diff that fail on incompatible
change.** Change that compile, pass tests and break a consumer is exactly the
class only a diff catch.

**What make this a gap rather than a rule already kept:** diff usually adopted
for one surface, the one with a published document, and rest inherit the belief
that contract is covered. Non-deterministic reviewer then own them by default,
against *A non-deterministic reviewer is never sole arbiter of a mechanical
class*.

**Instances live in sibling skills, and the apparent disagreement is narrower
than it look.** `java-backend-api` own contract diff and error-catalog snapshot;
`java-backend-observability` own event-and-metric catalog snapshot. That skill
scope breaking-change diff to surface crossing build boundary, on ground that
atomically-rebuilt consumer's compile is the check. **Record behind this skill
run full-document diff too — but under calibrated allow policy whose allowed set
is exactly "additive change the same-change client regeneration and compile
already absorb".** So both hold the same ground; they differ on whether that
ground **removes the gate or configures it**, and record's answer is that the
stricter published-surface contract sit *on top of* the wider diff rather than
replacing it.

**One genuine difference remain: japicmp.** Record propose source-and-binary
compatibility check on each module's published package; `java-backend-api`
evaluated japicmp and **dropped it** on the atomic-build ground, keeping it only
as re-open trigger. Named here rather than described, cuz that skill name it too
and a reader comparing the two positions need the same word in both.

*Check: committed enumeration of consumer-bound surfaces, each row naming its
diff gate or marked as having none. Bespoke. **Convention**, 2026-06-13.*

## The standing sweep

### A diff-scoped review cannot see erosion across changes

**Per-change review see one diff against current tree. Erosion that accrete
across many individually-fine changes is invisible to it** — boundary drifting,
invariant weakened by degrees, security posture decaying by increments, running
code diverging from approved behaviour. Add recurring full-system adversarial
sweep beside it, and treat two as different instruments.

Six properties make it gate rather than good intention:

- **Named firing mechanism, not "when someone remember".** Scheduled job whose
  absence or rename is itself a config-drift failure. On-demand audit degrade to
  audit-when-a-session-happen-to-remember, which under this premise mean never.
- **Cost bounded, cuz cost grow with codebase not with diff.** Full sweep at
  release milestones; periodic sweep scoped to what changed since last one, with
  per-run budget and a stated action when budget exceed — shard, or reduce
  cadence, decided in advance.
- **Evidence contract split by finding class.** Reproducible classes need
  executable evidence — failing test, counter-example, demonstrated breach —
  and unevidenced finding auto-downgrade. Structural classes cannot produce it
  without neutering the lens, so they need *structured* evidence instead: the
  rule the drift would violate if encoded, a diff trail across changes, or the
  named approved behaviour contradicted. **Demanding executable evidence
  uniformly delete exactly the findings this instrument exist for.**
- **Committed artifact the building agent cannot self-clear.** Sweep produce
  record — panel, lenses, findings, dispositions — and release gate fail without
  it. Contested finding get one re-run then escalate to a human decision, so
  nothing wedge indefinitely on unfalsifiable structural finding adjudicated by
  the same mind that wrote code.
- **Canary per lens, or "found nothing" mean nothing.** Each lens run against a
  known synthetic defect of its own class, seeded into scratch tree. **Clean
  report count only from lens that just caught its canary**; lens that miss its
  canary is itself a hard finding, blocking until re-aimed. This is mutation
  testing's argument applied one layer up — self-authored lens reporting
  "covered, nothing found" is coverage theatre in prose. Lens silent across many
  sweeps *while* passing its canary is also a finding: either mis-aimed, or that
  area genuinely clean, and which one is a disposition somebody make.
- **Different-vendor panel, scheduled not encouraged.** Panel is agents and share
  blind spots, so at least the binding sweep run models from a **different
  vendor**. Encouragement that fire on a trigger this layer cannot observe is not
  a mechanism. **This is the one structural fix for refuter independence** —
  `tech-decision-research` name that as the failure mode it is least protected
  against, and same-vendor fresh contexts reproduce a shared training consensus
  as many times as you run them.

`tech-decision-research` own the panel shape and its canary rule for *research*
passes. **This the same instrument pointed at a running system on a cadence**;
install that skill for how panel is run.

*Check: scheduled sweep exist in CI config inventory; milestone gate require its
committed artifact; evidence contract stated per finding class; **artifact record
canary result per lens and which vendor's models the panel ran**, so a clean
report carry its own evidence of being able to fail. Bespoke. **Convention**,
2026-06-13.*

***A schedule in a committed file be not a schedule that run.* Layer check,
2026-08-02, conversion-dated.** Whether the declared sweep fire is decided by the
hosting forge, named — **GitHub**: **GitHub Actions disable a scheduled workflow
after a period of repository inactivity** — **verify the behaviour and its window
against the forge's current documentation at adoption**, it is vendor policy with
no primary source here — a fork inherit the workflow file and never its schedule,
a runner label can stop matching, and a dead credential make every run fail
identically to none. **Decidable half: the milestone gate already require the
sweep's committed artifact, so require it to carry its own run timestamp and fail
when the newest is older than the declared cadence** — hold on any forge, why the
remedy is stated in artifact terms. *(Trimmed 2026-08-12 — desk pro-default,
2026-08-11 audit; the dated forge facts stay.)*

## The worked case — one repo's map, 2026-06-13

**One org, one sweep, one map — Java backend plus a browser frontend.** That record
**not published in this skill set**, so what this skill carry is restated, not a
pointer. Grounds are the sweep's; markers are not — it wrote none. **The map itself
— every concern, the tool adopted for it, its licence and the caveat that bites —
is a dated selection record and sit one hop away in [evidence.md](evidence.md).**

**Rows this skill set already own, named not restated.** Architecture and boundary
tests, compile-time nullness, migration lint, contract lint, contract diff,
conformance fuzzing, property tests, real-dependency container tests, coverage
floor, mutation on money paths, dependency ceiling: every one is a directive with a
check in `java-backend-rules`, `java-backend-api`, `java-backend-observability`,
`money-java`, `caching-java`, `async-handoff-java` or `llm-default-traps`. **Map's
frontend column is restated in `backend-stack` as host categories** rather than row
for row, cuz those cells are that skill's evidence about host counting.

**Two frontend rows fall between the two skills and are published in neither** — the
component test runner and committed visual-regression baselines. They map to no host
category `backend-stack` count, and they are frontend-shaped so this skill's worked
case no carry them. **Named as a gap, cuz a reader sent to `backend-stack` for them
find nothing and cannot tell whether they were dropped or never existed.**

**What the map show about the criterion above, and the reason it is worth opening.**
Rejections ran on **four** grounds, and naming them all matters cuz a repo screening
on the first two alone will adopt something the sweep rejected. **Standing server**:
SonarQube's server, Dependency-Track's server, pa11y-dashboard, Chromatic.
**Advisory-only verdict**: Fallow, which was **adopted into an advisory MCP lane
rather than rejected**, cuz its verdict class is one an agent might act on by
deleting live code. **Licence or second dialect**: jQAssistant, on GPL plus a rule
dialect outside the compile wall; conftest/OPA and CodeQL on the same second-language
and licence axes. **Maturity, scope or abandonment**: Konsist on language scope,
Deptective abandoned, Structurizr modelling rather than enforcing, Spectral stale,
Atlas's lint paywalled, migra dead, Checkov generic.

**And the caveat column is where the value concentrate** — intra-file taint limit,
unverified Find-Sec-Bugs compatibility, inventory-format lag, the OpenRewrite licence
condition, Renovate's own AGPL against the licence gate beside it, Jazzer's discovery
mode blocked on a JDK 25 segfault. **Each is a thing a tool list without the column
would have shipped as covered**, which is *Record the caveat that bites* holding over
the record that produced it. They sit with their tools in [evidence.md](evidence.md).

*Check: none — this a record of a selection, not a directive. Grounds **convention**,
2026-06-13.*

## Wiring the gates

Run once per repo. Record what wired and what skipped, with reason — skipped item
with no record become skipped item nobody remember choosing.

1. **Write the defect-class-to-layer map** (*Assign each defect class to the
   earliest layer*). Blank rows are the output that matter.
2. **Write the selection record**: per tool, verdict mechanism, whether build fail
   on it, licence, and caveat. Empty caveat marked **unexamined**.
3. **Wire licence gate** over generated dependency inventory, allowlist committed,
   undeclared rejected.
4. **Wire supply-chain gates on exit codes** — vulnerability scan, secrets scan,
   image scan — with every action and scanner pinned by digest per
   `llm-default-traps`, and committed output artifacts rather than hosted upload.
5. **Enumerate committed generated artifacts**, wire regenerate-twice byte-identity
   job over all of them.
6. **Enumerate consumer-bound surfaces**, name diff gate per row or mark row as
   having none.
7. **Map every numeric threshold** to ratchet, contention harness or production
   alert. Threshold with no row is the finding.
8. **Schedule the standing sweep**, put its workflow in CI config inventory so
   removal fail a check, and state evidence contract per finding class.
9. **Record what stayed advisory**, and for each, which defect class is therefore
   uncovered. This list is the honest half of steps above.

**A Java repo on the stack `java-backend-rules` binds starts from
`dulguun0225/java-backend-template`** rather than from this list. Steps 3 and 4
are wired there, step 5 for its two generated artifacts (the jOOQ tree and the
OpenAPI document), and the mechanical half of step 2 — tool, gate, host, and the
directive each implements — is its `docs/GATES.md`. Steps 1, 6, 7 and 8 and the
licence-and-caveat half of step 2 stay the repo's to write, and that file says so
by name. (Check: the template's named-gaps table carries a row per unwired step
here; a step absent from both tables is the finding — *convention*, 2026-09-16.)

## Composite shapes a repo assembles out of gates

**`enforceable-rules`' composite-shape check, run 2026-08-02, conversion-dated.
This skill decide which tool may occupy a gate and which layer own which class, and
the directives above decide nothing about what a repo build out of two gates.** Every
entry marked; **silence about a shape is a defect in this section.** The table promote
no marker, and **one entry is a ban no directive implies**, carrying its ground, the
organisation fact, the absence of a panel, and its re-open condition.

| Shape | Verdict |
| ----- | ------- |
| **A gate plus a suppression** — inline comment, annotation, per-rule override | **permitted with conditions, and the conditions were stated nowhere.** The suppression inventory is committed and diffed, so a new exemption is a git-visible line; without that, this composite is how every gate here turn green while covering less each month, and no directive above read it |
| **A gate plus a generated baseline** — a file exempting every finding present the day it was made | **banned** — grounds below |
| **A gate plus a ratchet against a committed baseline** — the performance shape this skill's own worked case use | **permitted, and it is the recommended shape** — with one condition the worked case leave implicit: **the baseline move in one direction only, and its regeneration is a reviewed change**, else the ratchet reset silently and the band read as held |
| **Two gates covering one defect class** | **banned by *Assign each defect class to the earliest layer*** — that directive's stated purpose is stopping exactly this, and it is restated here because a map with one owning layer per class read as an ordering rather than as an exclusion. The two drift, and the class read as doubly covered while each half-cover it |
| **A gate whose scope is another gate's output** — mutation scoped to the packages coverage report as covered, a lint reading a generated artifact | **permitted with conditions, and this is the composite most likely to produce a confident blank.** Everything outside the scoping gate's output is ungated **and reported by neither**. `money-java` `M-23` carry the worked instance — mutation scoped to money packages — and the condition is that the scope be committed and enumerated, never derived at run time |
| **A diff-scoped gate with no sweep partner** | **banned by *A diff-scoped review cannot see erosion***, restated as a shape because that directive read as being about agent review and hold for **every** gate that runs only over changed files |
| **A quarantined gate that stays in the map** | **banned.** *A gate only gates where its measurement is honest* name quarantine as the terminal state of a flaky gate; the shape it did not name is what happen to the map afterwards. A quarantined gate **leaves the map or the class it owned becomes a blank row** — those are the only two honest outcomes, and doing neither is how a class reads as covered by a gate nobody has watched run |
| **An agent reviewer plus a mechanical gate on one class** | **permitted, and it is the designed shape** — *A non-deterministic reviewer is never sole arbiter* decide it: mechanical class keep its mechanical owner, reviewer take semantics |
| **A gate configuration shared across repositories** — a shared workflow, a parent build file, a common ruleset | **permitted with conditions, and the conditions bite hardest in this organisation.** A change to the shared configuration change every consuming repo's gates **with no diff in any of them**, which is this skill's *what does this build enforce* question answered from a file the repo do not hold. Condition: the shared configuration is pinned by revision in each consumer, so an upgrade is a git-visible line there |
| **An advisory lane plus a defect class** | **permitted only where the class is recorded uncovered** — *A guardrail is a tool whose verdict fails a build* already say so, and it is restated because the advisory tool being *in the stack* is what later get described as coverage |

### The one ban

**A gate plus a generated baseline that exempts every existing finding — banned.**

- *Ground.* The baseline exempt an unbounded set, chosen by a date rather than by a
  decision, and **its regeneration is invisible to every check in this skill**. A
  build that fail on new findings and hold thousands of exempted ones report the
  same green as a clean repo, which is the false assurance `enforceable-rules`'
  first principle put above a missing gate. Adopting a tool with a baseline is
  adopting the tool's caveat as its default.
- *Organisation fact it rest on.* No human read the code, so nobody encounter the
  exempted findings incidentally; and one engineer per team mean nobody is going to
  work the baseline down. Elsewhere a baseline is a migration plan somebody execute.
- *No panel.* Case written by this conversion; nobody argued the other side, and the
  other side is real — a baseline is how a large existing codebase adopt a strict
  tool at all.
- *Probed pro-default at N=2 per tier* (bare sonnet + opus, 2026-08-11): all four
  sessions refused the plain baseline and derived the never-shrinks ground
  themselves. Demoted 2026-08-12 — the ban match measured instinct; it stay cuz
  the composite table would otherwise read as permitting the shape.
- *Reopens when* the baseline carry a committed expiry per entry and the build fail
  on an entry past it, which turn the unbounded exemption into a dated one. **Then it
  is a ratchet**, and the row above already permit it.

## Named gaps — where no check reaches

- **Nothing here check completeness of any enumeration this skill require.**
  Generated artifacts, consumer-bound surfaces, numeric thresholds, defect
  classes: each check catch a row written wrong, none catch a row never written.
  Same limit `enforceable-rules` state for its own incompleteness checks.
- **Caveat field catch omission, not vagueness.** "Has limits" pass every check
  here.
- **Completeness-critic claim is one run with no control.** Four concerns came
  out of it; nobody ran comparison arm, so whether the critic or ordinary
  attention found them is unmeasured. Central claim marked *uncertain* for this
  reason.
- **Every tool fact here is dated 2026-06-13 and none carry a primary source.**
  Free-tier boundaries, licence terms, compatibility with pinned runtime versions
  and vulnerability-matching quality all move. Re-verify at adoption; treat this
  as record of what one sweep concluded, not as current fact.
- **No cost figure for any gate here.** Standing sweep's budget, benchmark
  runner, characterization corpus, extra fuzz lane — sweep priced none of them
  in a way this skill can carry, and `caching` and `async-handoff` both already
  record unmeasured gate cost as open question. Adopting repo that measure one
  hold the first real number in this set.
- **Performance layer split never ran.** Design is written contract; no repo in
  this set built ratchet, harness or alert rules, so band width, baseline churn
  and whether ratchet actually stay green are all unobserved.

## Where the rest of this lives

- **`enforceable-rules`** — why rule need machine check at all, enforcement
  markers, and the incompleteness checks whose shape the enumerations above
  follow.
- **`tech-decision-research`** — how adversarial panel is run and why hostile
  audit carry canary. Standing sweep here is that instrument on a cadence.
- **`backend-stack`** — how many independent enforcement hosts a stack offer, and
  the frontend census restated from same record as this skill's map.
- **`llm-default-traps`** — pin rule for actions and scanners, and dependency
  ceiling this skill deliberately no restate.
- **`java-backend-rules`, `java-backend-api`, `java-backend-observability`,
  `money-java`, `caching-java`, `async-handoff-java`** — the instances: named
  tool per rule on one stack.

## Markers, dates, and what they mean

- **Confidence.** Everything **convention** except central completeness-critic
  claim, **uncertain**. Definitions in `tech-decision-research`.
- **Enforcement.** *Off-the-shelf* where a tool class exist in most ecosystems,
  *bespoke* where record or enumeration must be authored, *convention* where
  check is written artifact whose absence is visible. Definitions in
  `enforceable-rules`.
- **Dates.** **2026-06-13** = the sweep and the decisions folded from it same
  day. **2026-08-01** = conversion date, stated once, not a verification date.
  No date invented; where sweep gave none, none appear. **2026-08-02** = the date
  of `enforceable-rules`' layer and composite-shape checks, run over this skill by
  reading; also a conversion date, also not a verification date.
- **What those two checks added, and what they did not.** Layer clauses sit beside
  *A guardrail is a tool whose verdict fails a build*, *Record the caveat that
  bites*, *Licences gate deny-by-default* and *A diff-scoped review cannot see
  erosion*, each naming a language that directive's own check do not read — the
  forge's branch-protection settings, the suppression and baseline files, the
  container image and the vendored sources, and the forge's own scheduling
  lifecycle. *Composite shapes a repo assembles out of gates* is the composite-shape
  check's whole output. **All convention, all conversion-dated, none promoting
  anything** — each name a check that is absent, which say nothing about any claim's
  confidence. **The predicate, enumeration and token-placement checks have not been
  run on this skill.**

[evidence.md](evidence.md) carry the grounds, the claims that must not be cited,
and the conditions that reopen each directive.
