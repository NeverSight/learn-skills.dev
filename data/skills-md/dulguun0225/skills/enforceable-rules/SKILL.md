---
name: enforceable-rules
description: How to write a rule that actually binds an LLM agent — the premise-specificity test that decides whether a rule earns space in an agent's context, eight principles every rule is judged against (machine-enforced or it is not a rule, unwritable beats banned, no ambient modifier, no ambient trigger, fail loud, distrust what the agent picks and reads, deterministic output from committed inputs, gates need an outside oracle), the enforcement markers and status tiers that keep a rule set honest, and five checks a rule set passes while still being silently incomplete — the predicate, composite-shape, layer, enumeration and token-placement checks. ALWAYS load before writing or revising a coding rule, a constitution, a lint policy, an architecture test, a CLAUDE.md rule, or any text meant to override an agent's default behaviour. This skill defines the enforcement markers and status tiers the rest of this skill set uses.
---
# Writing a rule that binds an agent

Rule agent follow ≠ rule person follow. Person read rule, disagree, ask. Agent read rule, obey letter, ship working code that break intent — or not read at all, because rule was one of four hundred lines fighting for context. **This is the bar a rule clears before it is worth writing down**, plus checks that catch rule set reading thorough while incomplete.

Two things this not. Not research that make verdict — that ship as `tech-decision-research` in this skill set, step before this. Not style guide: nothing here about wording, all about enforceable, earns space, and whether its set have holes.

**There are no rule ids here.** Source material behind eight principles give each stable number for reason ids exist — citation survive list reorder. Two things override that here. Nothing consumer installs carry copy of that material, so number point into text reader not have; and other skills in set already cite these principles in prose, so shipping numbers make worse case set already rejected — **an id that resolves for a reader who installed this skill and dangles for one who did not.**

So each principle carry **stable name**, name is its `###` heading, and transferable half of never-renumber rule ship intact: **cite a rule by a stable anchor, never by its position in a list.** Citation saying "principle 3" break silent first reorder, and silent break is failure whole apparatus exist to stop. Rename anchor = break every citation to it; treat these names as ids that happen to be readable.

## Read the markers first

**Every directive here is *convention*, and the material it was drawn from carries no confidence marker and no date on any claim.** Nothing here survive refutation vote or rest on primary source. Authoring bar recorded by person who set it.

- **No `review-by` date, and the lapse rule is vacuous here.** Every other skill in set carry date past which *confirmed* marker degrade to *convention* alone. No such date in source material, none invented — and rule do nothing anyway, no *confirmed* claim to demote. **The cost is that nothing makes this skill's age visible**, so reader must.
- **No directive carries a per-claim date.** Material undated. **The conversion happened on 2026-07-30**, stated once, here; not verification date, never repeat as one.
- **The five incompleteness checks below are the exception that matters**, each rest on observed failure not argument. Failures real, and predicate, composite-shape and layer checks **verifiable by anyone who installed the other skills in this set** — worked case named beside each. *Check* still convention: nobody voted whether it is right response to failure.

Status tier: **decided, not yet validated** — researched and decided, **no production use yet**. What exist is every other skill in set, written against this bar = usage, not validation: no repo run any long enough to report whether bar predicted anything.

## The premise, and the review model that forces this kind of rule

**Code is written by LLM agents and no human reads it line by line.** Two consequences, and they make this bar not preference:

- **Machine evidence substitutes for code review, so a rule set's evidence rules are gates rather than advice.** No second reader. Build not object → nothing object. Weakening gate is stated deviation for repo where human truly read code — **that repo is the exception and carries the burden of saying so**, not default everyone quietly assume.
- **The plan is the last cheap place a wrong decision is caught.** After implementation, review is model checking model output; share implementer blind spots, so backstop never gate. Hence rule only a reviewer could enforce is barely rule.

Verdict portable exactly as far as its premises. Record them with rule set, so repo reading it can tell whether it applies.

## The premise-specificity test

**The filter every rule clears before it ships. A rule earns its place only when the absent reader changes its *stakes*: the failure it prevents turns invisible-forever or unbounded once no human reads the code.**

Part misread both directions:

- **Many rules worth keeping are also generic good engineering.** Not disqualifying. What earn place: no-human-reading **raises them from advisable to mandatory** — same rule, different stake.
- **Cut a rule only when the absent reader changes nothing about its stakes.** Failure equally visible either way = advice. Advice in agent context window not free: displace rules doing work, and rule set long enough to skim enforce nothing.

**A rule that fails the test has exactly two honest fates**: cut it, or keep because cheap and fails safe — then **mark it *convention* and never dress it up as premise-derived.** Dishonest third option, what actually happen: write premise-shaped justification for rule equally sensible in human-reviewed repo. Inflate rule set and worse, teach next author test is formality.

*Check: each rule's text says what turns invisible or unbounded under the premise. Bespoke at best — reviewer or agent read rule and justification together. **Convention** in practice, nothing can decide whether justification is real.*

## The eight principles

**Every rule is written and judged against these, and a rule that serves none of them is advice rather than a rule** — cut it, or mark *convention* and say plain it not premise-derived. Run from how rule enforced, through how code must read, to who wrote it, to how gates stay honest.

### Machine-enforced or it is not a rule

**Ship a rule only with a named check that fails the build. A ban with no check is a wish.**

Then clause left off, the more important half: **never wire a gate whose blind spot lets the banned thing pass while it reports green. False assurance is worse than none.** Rule with no gate = known gap reader can act on. Gate with blind spot = *green build* over thing it was installed to stop, and it kill pressure to build real one.

**Every worked case published in this skill set is a false green rather than a missing gate** — ratio worth noticing. Two, first recurs:

- **The erasure false green.** `llm-default-traps` ban **ArchUnit** as host for "never log this type" rule, because it read erased signature so rule pass while protecting nothing; **Error Prone** is host instead. That gate shipped before caught. `caching` then hit identical trap from different rule — value-round-trip check written against cache adapter type parameter read same erased top type — and refuse that host by name, citing earlier shipment. **One defect, two rules, and it was only stopped the second time because the first was written down.**
- **The false-green gate shipped as a product.** `async-handoff-java` record published contract-comparison tool that detect incompatibilities, write report file, exit green regardless. That skill refuse it and name two usable alternatives, but **identifies the refused product by ecosystem and repository signature rather than by name** — so instance real and product not citable by name anywhere in this skill set. That is anonymised-subject defect `tech-decision-research` state under *Record the negative results*, surviving in the one place reader would go to obey it.

*Check: every rule has a named check and an enforcement marker; every gate's blind spot is stated. Bespoke — marker greppable, blind spot not.*

### Unwritable beats banned

**Prefer a construct that cannot be written — an absent method, a compile error, an uninjectable object — over one that is written and then flagged.** Flag fire after code exist, in build somebody can override. Absent method fire while agent write the call — only moment correction is free.

**Where a capability cannot be designed out, confine it to the fewest named seams**, so static check over those seams is *complete* not best-effort. Capability reachable from anywhere need check reading everything; capability reachable from one factory need check reading one file.

In this skill set caching rules lean hardest, several directives are type design not prohibition: expiry value constructible only at catalog registration never at call site, and cache factory accepting no free-text parameter, so wrong call not compile. Seam version is `async-handoff` post-commit rule: a *general-purpose* post-commit callback **not exist**, because one such method defeat every check over the seam it confines.

*Check: design principle not rule, so its check is the absence itself — method not there, and test assert it cannot be called. Off-the-shelf where architecture test can assert absence; **bespoke** where construct is a type shape.*

### The source is the whole behaviour

**What a written call does is fixed by the call and its arguments at that call site — never by an ambient modifier: a mode, a surrounding scope, configuration, or in-memory object state.**

Govern **where a call's inputs come from**. Rule behind naming rounding at every call site not configuring once, and behind rejecting ambient session that change what identical statement does. Under premise it matter because reading the call is all anybody does: reader — human or agent — who must reconstruct ambient mode to know what a line does will get it wrong, and no second reader catch it.

*Check: bans on the specific ambient mechanism, per stack. **Off-the-shelf** where architecture test can forbid injection point.*

### No silent runtime behaviour

**An effect fires only from a written, named call — never from an ambient trigger.** Then operative instruction: **ban ambient dispatch by name.** Annotation-driven aspects, field or setter injection, aspect-oriented weaving, reflective dispatch, classpath scanning, hidden dirty-state flush.

Govern **what fires the call**, previous principle govern where inputs come from. Naming mechanisms not decoration — general ban on "magic" unenforceable and agent will not recognise own code as instance. `java-backend-rules` is worked case: ban field injection, transaction annotations, scheduling annotations, async annotations and caching annotations **individually, each with the check that fails the build**, not banning category.

*Check: a banned-annotation or banned-construct rule per mechanism. **Off-the-shelf** — principle with best tool support of the eight.*

### Fail loud, never silently wrong

**On a value-bearing path, throw or reject rather than take the silent default** — null, arbitrary row, swallowed catch, silent round, defaulted-missing field.

Premise argument exact, carry verbatim: **a wrong-but-plausible value on an unread path is invisible forever; a crash is caught by any test.** That asymmetry is whole principle. Also explain why this one make rules looking hostile to operability — service that throw worse than one that limp, right up until limp is wrong number nobody see.

Money rules built on it end to end: fail-loud money paths, over-scale write rejected by store not quietly rounded, JSON number on money field rejected at parse not coerced.

*Check: per instance — a lint on the swallowing catch, a store constraint, a parse-time rejection. Mixed **off-the-shelf** and **bespoke**; swallowing catch is the one with named gap in every rule set here that touch it.*

### Distrust what the agent picks and what it reads

Two halves, both about agent as untrusted input channel.

**Where the corpus-dominant pick is wrong, name that favourite and ban it.** "The default is Y, rejected because Z" override instinct that bare "use X" does not. That sentence is most important line a rule set contain — **do not compress it away**, and do not swap named loser for category.

**And treat every input the agent selects or reads as untrusted until pinned, verified to exist, and shielded from the channels the agent reads** — dependencies, tool versions, generated code. Second half is one authors forget: agent read test output, CI logs and release notes, so anything that can write into those channels can write instructions to maintainer. `llm-default-traps` is this principle as whole skill.

*Check: a banned-dependency rule, a lockfile gate, a pin check, a version ceiling. **Off-the-shelf** for pinning half; "verified to exist" half is **convention** in every ecosystem, and that skill says so.*

### Deterministic output from committed inputs

**Make every generated artifact and computed output a pure function of committed inputs — an injected clock, stable ordering, no wall-clock read, no live database — so that a regenerate-and-diff or a replay gate is trustworthy.**

Reason one sentence: **here the diff is the review.** Regenerate-and-diff gate is closest thing to second reader, and any nondeterminism anywhere in pipeline destroy it — not by wrong answer, by noise that train everyone to ignore gate.

`java-backend-rules` carry clock half (wall-clock reads banned in domain code, injected clock instead) and `money-storage` committed-input half (schema lint asserted over committed migrations not against live database).

*Check: a clock ban, an ordering rule, and the regenerate-and-diff gate itself. **Off-the-shelf** for gate; **bespoke** for clock ban on most stacks.*

### Gates need an outside oracle

**Draw a semantic gate's ground truth from outside the implementer model** — spec-derived fuzzer, human-approved golden corpus, invariant asserted on real data, mutation testing that probe the tests — **never only from tests the same model wrote to describe its own output.**

This principle decide whether green build mean anything. Model write implementation then write tests describing what it wrote; both pass; nothing verified except internal consistency. **A coverage floor does not fix this**, coverage cannot see whether test asserted anything.

Two worked cases: `java-backend-api`, whose committed interface document is single conformance oracle a fuzzer generate against, and `money-java` `M-23`, which pin mutation testing scoped to money packages — **the scope is a named gap, stated on `M-23`'s own side: everything outside it sit green over vacuous tests.**

*Check: the oracle is named per gate, and a gate with no outside oracle says so. **Off-the-shelf** for fuzzer and mutation tooling; naming the oracle is **convention**.*

## The shape of a rule, and where the evidence goes

**Directive first, in bold. Then the reasoning. Then the enforcing check in parentheses, with its enforcement marker.** That order, because agent reading under context pressure read first clause of each item and shape must put instruction there.

- **Directive text and evidence are separate artifacts.** Directive text is instinct-override payload for scarce context window; **only an instinct-overriding rule justifies space there.** Evidence for whoever decide whether to trust rule — different reader, different moment, one hop away.
- **Group the evidence by the section of the directive text each rule lives in — never by research pass.** Rule set accreting over several passes and filing evidence by pass end ordered by own history not by what reader look for. Put passes and each scope in table at top of evidence file instead, provenance available without becoming index.
- **Every ban names its enforcing check and its enforcement marker.** No exceptions, and where group of rules truly share one check and one marker, state once at group head **and say the sharing is deliberate** — else it read as dropped marker.
- **Every rule clears the premise-specificity test and serves at least one of the eight principles.**
- **Nothing in the directive text may cite an id or link back to material the reader does not have.** Rule set pasted into repo holding no copy of source land with dangling pointer, and cited number read as *that repo's own* numbering, worse than obviously broken link. **Ids belong in the evidence file, or in text the reader demonstrably has.**
- **Set `verified` and `review-by` in the frontmatter**, and let frontmatter be only authority for them — date of last research pass, and date after which rule set stale. Status copied into three files go stale in two.
- **State the condition each conditional group is dormant under, and say *dormant* rather than *inapplicable*.** Rule for capability repo not have yet is rule with **tripwire**: moment first instance of that capability appear, group activate, and cheapest place to say so is the change introducing it. **An adopting repo deletes a rule when the capability is absent by design and keeps it when it is merely absent so far** — and can only tell apart if group state its condition. Deleting dormant group remove tripwire, whole reason group written before anything triggered it.

## Enforcement markers, and the status tier

**This skill owns both vocabularies**, both are properties of a rule's check not of a research claim. Four **confidence** markers — *confirmed*, *primary-source verified*, *convention*, *uncertain* — owned by `tech-decision-research`, where defined and where promoting refutation votes live. **A repo that installs this skill and not that one has these two vocabularies and not the confidence one**, and no skill here supply it then.

**Enforcement, per rule — a ban without a named check is a wish, not a rule:**

- **off-the-shelf** — named tool rule exist (ArchUnit rule, Error Prone check, linter rule — material's own examples, any ecosystem equivalent count); adopting repo copy it and wire it.
- **bespoke** — check must be authored by adopting repo. **The rule set says so and names the tool that can host it** — "bespoke" with no named host is admission dressed as marker.
- **convention** — no gate exist. **The rule states why it is kept anyway.**

**Status tier, per rule set, and per rule where they differ:**

- **production-confirmed** — named repo operate the discipline, rule set cite it.
- **decided, not yet validated** — researched and decided, **no production use yet.** Gloss that way, not "not yet proven at scale" or "not run long enough": those imply production record that not exist.
- **deferred — evidence-driven** — recorded for future decision. Not directive text, not in context window.

**The enforcement marker is the one that decays without anyone touching it.** Rule marked *off-the-shelf* whose gate never wired read as enforced forever, and nothing detect gap between marker and build. Hence rule set wiring step record **what was skipped, with the reason** — record listing only what was wired read as complete coverage.

## Five checks a rule set passes while still being incomplete

**A rule set can satisfy every principle above, pass every machine check over it, read as thorough, and fail all five of these.** None machine-checkable, each about what is **absent** from text, and absence not a property checker can extract. Each exist because shipped rule set failed it.

**Run all five over rule sets that already shipped, not only over the next one.** Layer check was failed by **oldest** rule set in corpus these skills came from, read, lifted and re-reconciled three times without anyone noticing. And keep record of which rule set had which check — **an unaudited entry is a check nobody ran, not a clean rule set.**

First three recorded in material this skill converts. **The last two are additions, drawn from the authoring of this skill set itself** and marked as such below, not presented as inherited.

### The predicate check

**Frame the rule set's applicability predicate on *what the rules must reach* — never on the technology in its name, and never on what the rule set currently recommends.**

Two rule sets in a row scoped seam to obvious client library and left **the cheapest correct option — which imports no client at all — outside every check.** One had its recommendation reversed within hours of shipping, while widened predicate survived untouched. **That is the argument for the rule in one sentence:** predicate written around a recommendation die with the recommendation; predicate written around reach of the rules does not.

Both worked cases published here, readable. `money-storage` predicate written so rules reach hand-written query, view definition, migration and support script — **none of which imports a client library** — and money rules deliberately *not* named for a persistence layer, because in typical shop that name scope them to code that does import one. `async-handoff` named for a broker and bind from **the first asynchronous handoff of any shape**: polled table, in-process bus, bare executor submit, webhook. Its three recommendation thresholds withdrawn on 2026-07-29; predicate needed no change.

*Check: read the predicate and ask what it excludes, then find the cheapest way to do the governed thing that the predicate misses. **Convention** — human or agent judgement, no host.*

### The composite-shape check

**List the shapes a repo will assemble *out of* the primitives the directives govern, and mark each one: permitted, permitted with conditions, banned, or out of scope.**

**Naming the undecidable properties *inside* each directive does not surface a shape nobody wrote a rule about.** One rule set did former diligently — every directive carrying own honest named gap — and passed over **five whole shapes** in silence. Silence about shape worse than usual failure: gap named inside directive at least read as gap, but **silence about a shape reads as nothing at all.**

**Every ban this check produces names the organisation fact it rests on and the trigger that reopens it.** Ban remove option from every future repo, so carry more than a ground.

Worked case published in both halves. `money-storage` carry composite-shape table with verdict on every shape a repo assemble out of stored money, and state it exist *because* of neighbouring rule set's failure. Those five missed shapes now published as `async-handoff-shapes` plus two bans in `async-handoff` — not retiring lesson, because defect was never missing rules. It was that nothing in rule set made absences visible.

*Check: the rule set has a shape table, and every entry is marked. **Convention.** Producing list is the work; nothing can tell you list is complete.*

### The layer check

**For each directive, name the language its check reads — then name every other language the same value passes through.** Query text. Migration text. View and function definitions. A template. A serialized document. A script somebody runs by hand.

**A value that crosses into any of them has left the reach of the rule that governs it, and the rule still reads as complete.** Rule set this was found in had **twenty-nine directives all enforced over application source**, a section correctly answering "which column type?", and **nothing at all about the store's query language.** Finding is sentence to carry: **the gap was not a missing rule; it was a missing layer.**

Published worked case: `money-storage` ban arithmetic on money in store's query language outright, and ship blind spot beside it — lint cannot reach query text assembled at runtime from fragments — **because a green lint otherwise reads as coverage.**

*Check: per directive, enumerate the languages. **Convention**, most mechanical of the five to *perform* while impossible to automate: languages enumerable, but only reader know which ones a value reach.*

### The enumeration check

**Not inherited — an observation from writing this skill set.** State rule set contents **by name, not by count.** Sentence that count or enumerate decay silently when set change, and **has no id to grep for.**

**Every authoring and review pass over this skill set has found new instances, without exception — including the review of this skill, which found them inside the two files publishing this very check.** Most reproducible defect in whole effort, recurring in files an earlier pass already called clean. Running total stood at **ten as of 2026-07-30**; treat as floor and dated observation, not rate. What was learned about where it strike:

- **A split is the highest-risk moment**, each half inherit the whole's number and nothing re-derive it. Two instances created by single split.
- **A cross-document count is worse than a local one**, author cannot see thing being counted. Several were counts of *another* document's contents, wrong at moment written.
- **Publishing a new document obliges a sweep** of every sentence elsewhere that counts, and every sentence saying the new thing not exist. Sweep run after every publish in this set and still left stale sentences — each time caught by later adversarial review, not by sweep.
- **A superlative is a count in disguise** — "the one rule here with a panel behind it", "the strongest group in this set", "the only rule set here that is not predominantly convention", "the weakest-marked skill in the set", "the first skill in this set with no wiring section". Every one false when written, and reader have no way to tell checked superlative from unchecked one.
- **Fixing a count in one file does not fix its copy in the sibling**, and note recording the fix read as coverage for a file the fix never reached.
- **Part of this check automates, and the cheap part is worth wiring.** Where rule set cite rules by id, short script can compare number against ids in every sentence carrying both number word and two or more cited ids. Run over this skill set it found count contradicting two enumerations of same set, one in same file. It see nothing where count stand alone with no ids beside it — more common shape — so it narrow the reading, not replace it.

Practice: **prefer naming to counting.** Where count must appear, put adjacent to the enumeration it counts, so both read together. **Never state a count of another document's contents.** State exception list not remainder — "these two are convention" survive a rule being added, "thirteen of these fourteen" does not.

**One exception, and it has to be stated or the rule is unusable**: where the count *is* the evidence, state it with date taken and say plain it is a check reader can re-run, not a fact to cite. Its decay then the point, not the defect.

*Check: a lint over number words adjacent to list structures is possible and noisy. **Convention** in practice, plus publish-time sweep. **The observed instances are the ground — a dated floor of ten as of 2026-07-30, with more found in every pass since; the response is unvalidated.***

### The token-placement check

**Not inherited — the same origin, and the one check here with a mechanical form.** **Extract every identifier-shaped token from the source material — backticked identifiers, product names, RFC numbers, status codes, configuration keys — and require each to appear in the converted text, per directive rather than per file.**

Failure it catch: rule set **describing a tool where its own source names one** — "the connection pool", "the metrics vendor", "a generator of that class". Invisible to every marker, id and link sweep, and it defeat the rule that a ban ship with a *named* check — described tool is not named one, and reader cannot wire it.

Three things learned running it, each cost a pass:

- **It works.** Run over one rule set's directive text it surfaced twelve described-not-named tools, no other check had seen any.
- **Run it over every source region the text draws from, not only the directive text.** Widening extraction to *evidence* material surfaced twenty-three more, all in evidence files.
- **Per directive, not per file — presence is not placement.** One tool dropped from the two directives its source name it for and inserted into the two where source deliberately leave it generic. All four inversions passed a per-file check, string was present somewhere.

**And the inverse case is a real finding, not a false positive**: where source withhold a tool on purpose, converted text must withhold too. Rule set promising a pick that its own stack material deliberately decline to make is same defect, sign flipped.

*Check: token extraction and per-directive presence — **bespoke**, no published tool does it. Check itself scriptable in an afternoon, which make its absence hard to defend.*

## When the same rule lives in more than one place

**Prefer one owner.** Where rule truly cross-cutting, one document state it and every other point at it by name **without repeating the value** — value stated in *N* documents drift in *N*−1. Worked case: dependency version ceiling three stack skills need and one skill own: `llm-default-traps` state the version, other three name that skill and deliberately omit number, each carry same fallback for repo installing one and not other.

**Where duplication is genuinely deliberate** — same rule instantiated with different check on each platform, cannot centralise without separating rule from gate — then **one index of every instantiation is the only thing between deliberate duplication and drift.** Not convention, not review: index updated in same change as rule. Nothing else catch it.

And accounting rule making inherited rule set safe to build on: **every rule in it is accounted for.** Walk rule by rule. Each is either carried with this platform's named check, or **named as a gap with the reason no check can be hosted**, or recorded as divergence platform's type system or database force. **A rule passed over in silence reads as covered**, hence naming the gap is requirement not courtesy.

## Wiring the gates

Run once per rule set, not per rule. **Two of everything above can be machine checked, and both are worth building before the rule set grows** — most of this skill is convention by construction, so the two exceptions carry weight.

1. **The evidence-order check.** Every subheading in evidence file name real section of directive text, and subheadings run in directive text's order. Fail build on either. Stop accreting rule set from silently reorganising by research date. **Bespoke** — short script over two files, no published tool does it.
2. **The dangling-pointer check.** No directive text cite a rule id, a principle by number, or relative link back to material reader not have. Fail build. **Bespoke**, cheap: pattern match over one file set.

**Then make the check print what it does not decide, on every run.** Step keeping the two above from becoming false assurance the first principle bans. Neither can decide:

- whether a note filed under **right** heading, only that heading exist and is in order;
- whether accounting walk over inherited rule set actually done;
- **any of the five checks above** — all five about absence;
- whether marker table honest, or whether rule marked *off-the-shelf* has gate wired.

**It fails the build; it is not advisory.** Check that warn is check ignored by second week.

**Then record what was wired and what was skipped, with the reason.** Entries *not* gated by anything above, must be listed as such: premise-specificity test, accounting walk, all five incompleteness checks. Every one is human or agent judgement with no host.

## Named gaps — where no check reaches

Silence read as coverage, so each stated.

1. **All five incompleteness checks are unhostable, permanently.** Each ask what is *missing* from a text, no checker can extract an absence. Largest gap here, does not close — mitigation: checks cheap to run by hand, and record of which rule set had which one make skipped check visible.
2. **The two wireable checks ship as description, not as code.** This skill carry no script a reader install, so a reader write or port both, and the earlier implementation the source material record — one script in that project's own build — is unpublished. A reference pair exist in the repository these skills distribute from (`https://github.com/dulguun0225/skills`, under `scripts/`): `npm run gates`, each exiting non-zero and printing what it not decide, run by that repository's CI on every push touching the skills tree or the scripts — a gate for that one skill set, a description for every other. **What building them produced is a finding about the rule, not about the files.** Measured 2026-08-02, re-runnable — **and it moved three times that same day, which is why the command matter more than any figure**: stated as *every subheading in the evidence file name a real section of the directive text*, the evidence-order rule hold over most of that set's evidence files and over none of the rest, which are organised by research pass — how the research happen. **Run `npm run check:evidence-order` there; it print both sides and name every exempt file.** Gate ship with the exempt files declared by name and reason, not with rule bent to fit.
3. **The eight principles have never been tested by exclusion.** Nobody recorded a rule serving none of them and kept anyway, so nothing establish the eight exhaustive — only that no rule so far needed a ninth.
4. **The premise-specificity test has no calibration.** No rule cut by it recorded, so test's discriminating power unmeasured, and honest reading is it may function as justification format not filter.
5. **The enforcement marker decays with nothing watching.** Rule marked *off-the-shelf* whose gate never wired read as enforced forever. **The gap between a rule set's markers and a repo's actual build is checkable in principle and checked nowhere.**
6. **The enumeration and token-placement checks rest on observations from one effort.** Enumeration instances and two token-sweep yields are real ground and narrow: one corpus, one author, one review style. Neither check run against rule set written by anyone else.

## Markers

**Enforcement, per rule** — three values defined above, in *Enforcement markers, and the status tier*, this skill's own subject.

**Confidence, per claim** — *confirmed*, *primary-source verified*, *convention*, *uncertain*, defined by `tech-decision-research`, which owns them.

| Claim | Marker |
| ----- | ------ |
| Every directive in this skill | convention — no execution, no primary source, no vote |
| That a rule set can pass every machine check and fail the predicate, composite-shape and layer checks | convention — but each rest on observed failure of shipped rule set, each has worked case published in this skill set |
| That the enumeration failure recurs — a dated floor of ten instances as of 2026-07-30, one of them created by publishing this skill and more found in its own review the same day | convention as rule; instances are observations from this skill set's own authoring, response unvalidated |
| That token extraction catches described-not-named tools — twelve and twenty-three found, 2026-07-30 | convention as rule; yields are observations from two passes over one corpus |
| That the eight principles are exhaustive | **uncertain** — see gap 3 |
| That the premise-specificity test discriminates | **uncertain** — see gap 4 |

No date column: material carry none, none invented. **The conversion date is 2026-07-30**, not a verification date.

Ground behind each, claims that must not be cited, and conditions reopening one are one hop away in **[evidence.md](evidence.md)**.