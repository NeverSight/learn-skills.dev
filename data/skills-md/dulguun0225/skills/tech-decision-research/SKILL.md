---
name: tech-decision-research
description: The procedure a technology decision clears before it becomes a rule a future agent follows — frame the situation weights, the premises and the decision owner in writing before naming any candidate; run an adversarial panel rather than one agent's survey, with a steelman for the loser and a planted canary in every hostile audit; verify each load-bearing claim by three independent refutation votes and mark the survivors confirmed, primary-source verified, convention or uncertain; date every version fact and name the re-open trigger; and re-verify on adoption rather than on a calendar. ALWAYS load before picking a library, a framework, a datastore, an architecture or a tool, before grading the evidence behind a decision someone else made, and before re-dating a decision that has gone stale. This skill defines the four confidence markers the rest of this skill set marks its claims in.
---
# Researching a decision an agent will follow without re-deriving it

Procedure verdict must clear before become rule. Skip step → the one failure whole shape exist to stop: **plausible-but-unverified verdict that downstream agent follow faithfully.** Wrong decision that look researched worse than open question — open question get asked again, recorded verdict not.

Output = decision someone act on months later with no re-run of research. So output not just pick. Pick + premises it conditioned on + what lose and why + marker how strong held + date + condition that reopen it. Pick with none of those = opinion with timestamp.

**Write decision down as rule = separate job, own bar**, published as `enforceable-rules` in this skill set: shape of rule, filter rule clear to earn space in agent context, enforcement markers, five checks rule set pass while still incomplete — predicate, composite-shape, layer, enumeration, token-placement checks. This skill stop at verdict. That one start there.

**No rule ids here. Deliberate.** Every directive named by subject — *the frame*, *the canary rule*, *the three votes*, *the provenance line*. Each is `###` heading; heading = anchor id would be. Cite from elsewhere as this skill name + subject. That resolve whether or not reader install skill; number resolve for one install, dangle for other.

## Read the markers first — nothing here is above convention

**Every directive here = *convention*. Source material carry no confidence marker, no date on any claim.** Nothing here survive refutation vote. Nothing rest on primary source. Method recorded by person who run it. By own rule in *A claim with no execution and no primary source is convention* below → convention. **Method self-applied = whole of its evidentiary standing.**

Two consequences:

- **Lapse rule cannot run here. Absence not oversight.** Every other skill in set carry `review-by` date; past it, *confirmed* marker read as *convention* with no maintainer action. No such date in material behind this skill; none invented. Rule vacuous anyway: it demote *confirmed* → *convention*, and no *confirmed* claim here to demote. **Cost real** — nothing make this skill age visible, so reader must.
- **No per-claim date here. No date invented.** Material undated. Dated thing = conversion: **text below written 2026-07-30** = when *converted*, not when anything *verified*. Do not read as verification date. No verification happen.

Status tier: **decided, not yet validated** — researched and decided, **no production use yet**. Method make every rule set behind this skill set = usage, not validation. Nobody measure whether decision run this way survive longer than run without. That measurement = single most valuable thing that could happen to skill. *Named gaps* say so.

## The premise, and the two problems

**Code written by LLM agents. No human read line by line.** Every skill in set conditioned on that. Here it bite specific place: one human gate read plan and spec, **not code**. So plan = last cheap moment wrong technology decision get caught. After implementation, review = model checking model output — share implementer blind spots. Backstop, never gate.

That premise + two problems = why procedure exist instead of "just research it":

- **LLM implementer alone pick technology by training-data default.** Not careless — *confident*, with working code. Corpus-dominant pick = statistically likely one whether right or not. Often library that was right five years ago.
- **Proper research slow, get redone per project.** Decision researched once and recorded properly get consulted. Decision researched informally get re-derived, and re-derivation land on corpus default again.

Verdict portable exactly as far as its premises. Not caveat — reason *the frame* below record premises before any candidate named. That is what let different repo read verdict and know it not apply.

## 1. Frame the decision before naming candidates

State all four in writing **before any candidate compared**. Frame written after candidates on table = rationalisation of pick already made, and it read same as real one.

### State the situation weights

**Name what dominate this decision, in writing, before compare anything.** Four that recur:

- **Exactness** — wrong value have victim.
- **Operability** — who run this in production, what happen at 3am.
- **Verification** — what build can be made to refuse to ship.
- **Corpus depth** — agents implement this, so how well model actually know candidate.

Internal tool that can be wrong for day vs ledger weigh these different. Every later step read different depending which dominate. **Corpus depth most often left out**, and under this skill premise it is the one that change answer: technically superior candidate model know badly produce worse code than adequate one model know well.

*Check: frame document exist and name weights before candidate list. Convention — no build gate can host this. Failure mode = frame written last, dated first.*

### State the premises the verdict is conditioned on

**Write conditions verdict hold under, as list. Treat list as part of verdict.** Agents implement; no human read code; no operations team; money domain; whatever else decision lean on.

Highest-value line in frame, because it is what *reader* need and researcher never need. **Verdict with no recorded premises get applied where it not hold, or ignored where it do hold** — and reader cannot tell which mistake they make.

*Check: premise list ship with verdict, not in researcher head. Convention.*

### Name the decision owner, verbatim

**Record who decide — user, panel, or *delegated* — and record which, verbatim, in provenance line.** Not paraphrase: *delegated* is value in own right, and pass that write it also write what it delegated on (standing case: no in-house expertise to defer to). Decision with unrecorded owner get re-opened by whoever disagree next, because no one it can be referred back to.

*Check: provenance line name owner. Convention.*

### Strike what an existing rule set already decided

**Read rule sets that already bind repo first. Remove their directives from frame.** Panel spent re-deriving decided verdict make **second copy, not second opinion** — second copy worse than no work, because now two texts state rule and one will drift.

Standing case in this skill set = money: money skills own those directives outright, so decision about stack cover only **this stack check for each of them**, plus whatever platform need that no existing rule set carry. Same for caching, same for asynchronous handoffs.

**Frame = where scope narrow, and only place that is cheap.** Discover mid-panel that directive already decided elsewhere → panel output now must be reconciled against text nobody read.

*Check: frame name rule sets read and what struck. Convention. When nothing struck, say so — empty strike list and unread one look same.*

## 2. Run an adversarial panel, not a survey

**One agent researching one answer converge on training-corpus default.** It make well-written comparison, cite real sources, recommend what corpus recommend. This step exist to break that, and it is step most often skipped under time pressure — survey feel like research and cost quarter as much.

### Pick a panel shape with an adversary in it

**Three shapes, each with hostile lens that is somebody whole job:**

- **Four agents** — two opposed steelmen, each argue one candidate on its best current form, + domain architect, + hostile audit of the lot.
- **Three agents** — evidence miner (legacy-system forensics, law, production incidents; facts not opinions), + design steelman, + hostile audit.
- **Steelman duel plus hybrid audit** — candidate A steelman vs candidate B steelman, + hostile audit aimed at hybrids and middle roads, which is where unaudited duel land.

What make these work = not count. **No agent in them asked to "research the best option"** — each get position or lens and told to push it. Disagreement structural, not dependent on one agent happening to be sceptical.

*Check: provenance line name shape. Convention.*

### Steelman the loser, and name it

**Rejected alternative argued on best current form. Rejection grounds numbered.** Then: **record training-corpus favourite by name and why it lose.**

That sentence = most important line research make. Agent told "use X" still drift to corpus default. Agent told "default is Y, rejected because Z" not drift. **Do not compress away when verdict become rule** — named loser is load-bearing half, and it work because it address the instinct instead of talk past it.

Steelman on *best current form* = part that get dropped. Five-year-old objection to candidate that since fix it not rejection ground — stale citation, and agent training data full of those.

*Check: rejected-alternatives section name corpus favourite and number grounds. Convention. Its absence visible = whole gate.*

### Every hostile audit carries a canary

**Plant defect of audit own class in what it review. Require audit to find it. "Found nothing" count only from lens that catch its canary.**

This is the one rule here that make negative result mean anything. Audit agent reporting clean bill of health either do work or make most likely text for agent asked to audit something — two outputs indistinguishable. Caught canary = the difference.

**Uncanaried "found nothing" not evidence of correctness. Must not be recorded as one.** Record as audit that ran, no calibration.

*Check: canary and its detection recorded per lens. Convention, and cheapest high-value step in whole procedure.*

### Evidence is execution or a primary source, not prose

**Claim is evidence when it come from something run or something authoritative and dated — not from well-argued paragraph.** Model summary of library behaviour not evidence of that behaviour. Library own documentation is. Library actually doing it under test better.

Claim backed by neither not discarded. It **downgrade**, by rule in step 3 below, and stay as convention if worth keeping.

*Check: each load-bearing claim evidence name the execution or the source. Convention.*

## 3. Verify claims by refutation

### Three independent refutation votes per load-bearing claim

**Each load-bearing claim go to three fresh-context agents told to refute it. Claim survive on majority.** Fresh context = operative word: agent that read panel reasoning defend it, not attack it.

Refutation not confirmation, same reason panel adversarial: agent asked "is this true?" reach for supporting evidence and find it. Agent asked "show this is false" reach for counter-case, and either bring one back or not.

**Only load-bearing claims get votes.** Three votes expensive; spend them on claim nothing rest on = why load-bearing ones get skipped.

*Check: vote outcome recorded per claim, not per decision. Convention.*

### A claim with no execution and no primary source is convention

**Claim backed by neither execution nor primary source auto-downgrade to convention. No vote spent on it** — nothing for refuter to attack. Not penalty. It keep marker vocabulary meaning something, and rest of skill set lean on it hardest.

**Whole rule set can land here honestly.** In this skill set caching rules = worked case: every directive marked *convention* because each is design argument not execution result, and rule set say so at top not in footnote. Not weak rule set. Honestly marked one, more useful than same text with markers it not earn.

*Check: nothing marked above convention lack named execution or source. Convention — and the one directive here reviewer can actually verify, by reading marker table against evidence.*

### Mark the outcome per claim, in four values

**Per claim, not per decision** — decision usually rest on claims of several strengths, and one marker on whole thing take the strongest.

- **confirmed** — survive the three votes, against independent primary sources.
- **primary-source verified** — one researcher check it against primary source, no panel. **Whatever its evidentiary strength, this is not *confirmed*; running votes is what promote it.** Pass that run out of budget land claims here honestly instead of promoting them, and say which passes stop short.
- **convention** — kept without surviving external evidence. **Say why kept**: cheap, enforceable, fail toward safety. Convention marker with no reason beside it read as admission, not decision.
- **uncertain** — known gap, stated so it visible.

**These four = vocabulary rest of skill set mark claims in**, so defined here not in each skill. All four in live use across published skills. `llm-default-traps` add fifth value, **recorded**, for dated observation carried as history not current fact — local extension, defined where used, not part of this vocabulary. **Do not reach for *production-confirmed* here**: that is status tier for whole rule set, owned by `enforceable-rules`, not confidence marker on claim — and no skill in set reach it.

**Failure this vocabulary exist to stop is one-word one.** Drop *convention* marker → design argument promoted to verified fact, silently, and nothing downstream can tell. Treat marker as part of claim text.

*Check: every claim in evidence trail carry one of these. Convention.*

### Record the negative results

**Source that not survive verification recorded as "do not cite", by name, so next pass not re-import it.** Same for claim that turn out to be about different version, different product, or neighbouring issue.

Cheapest step here, longest payoff: next pass usually run by agent whose training data hold same discredited source, and it will reach for it again. **Do-not-cite entry with anonymised subject cannot be obeyed** — it announce trap exist and withhold which thing is trap, worse than no entry. So name source, version, issue.

*Check: evidence trail have do-not-cite list, every entry name its subject. Convention.*

## 4. Date everything, name the exits

### Every version fact and tool verdict carries its verification date

**And release dates too, where decay matter.** Version fact with no date unusable within months: reader cannot tell whether to trust it or re-check it, and re-check everything = same as trust nothing.

Dates make staleness **visible**, not impossible. That is whole ambition — nobody claim dated fact stay true.

*Check: no version number or tool verdict without date beside it. Convention, and mechanically checkable in way most of procedure is not: version-shaped token with no nearby date is a grep.*

### Every decision names its re-open triggers

**Name condition that reopen decision — and where stakes justify, escape hatch: named fallback + tripwire that activate it.**

Then payoff clause, point of whole step: **absent the trigger, decision not re-litigated. Record once, point at it forever.** Decision with no trigger get re-argued whenever someone feel uneasy, and re-argument land on corpus default, because that is what unframed re-derivation land on.

Trigger = *condition*, not date. "Revisit in six months" not trigger; "a maintained implementation appears on this stack" is.

*Check: every verdict have at least one trigger. Convention.*

### The provenance line

**One line on verdict: who decided, by what method — the panel shape — and on what date.** It make every marker above auditable, and later reader use it to decide how much research to redo.

*Check: verdict have provenance line. Convention. Its absence cheapest thing to spot in review and most commonly missing.*

## 5. The re-verification pass, on adoption or on lapse

**Smaller than original pass, deliberately, and scoped not re-run.** Full re-run = what make re-verification never happen.

- **Re-check dated version facts and every claim marked *uncertain*.**
- **Re-run refutation votes only on claims whose ground shifted** — new major version, maintainer change, withdrawn standard, named trigger firing. Not everything.
- **Re-date `verified`, move `review-by`.**
- **Note superseded verdicts with dated notes pointing at successor — never silent edits.** Silently edited verdict destroy only record of what was believed and when, which is what every marker above was for.

**Adoption = real re-verification checkpoint, not calendar.** Decision re-verified when someone need it. `review-by` date exist so lapsed decision degrade honestly on own — past it, every *confirmed* marker read as *convention* until pass re-date it, by definition, no maintainer action.

*Check: re-verification pass re-date frontmatter and record what it not re-check. Convention. Pass that re-date everything while re-checking some of it worse than no pass.*

## What checks this — and the principle this skill cannot satisfy

**Nothing in a build check any directive above, and one of them is reason that is worth stating not glossing.**

`enforceable-rules` in this skill set publish principle: rule ship with named check that fail build, or it is not rule — ban with no check is wish. **By that standard nothing here is rule.** Not defect in either skill. Resolution = scope distinction worth being explicit about:

- **That principle govern rules that bind code.** Subject = construct in repository, reachable by linter, compiler, architecture test, fuzzer.
- **This skill subject = the decision, which happen before there is any code to check.** Its directives bind process, and every check named above same kind: **written artifact whose absence is visible.** Frame document, numbered rejection grounds, canary record, marker per claim, do-not-cite list, provenance line, trigger.

Real gate, and weaker than build gate in one specific way that matter: **it catch omission, cannot catch lie.** Frame document written after candidates chosen pass every check here. Provenance line naming panel that never ran pass. **Only defence: artifacts cheap to produce honestly, expensive to fake convincingly**, and reader who doubt one can read panel own output.

So: **no `## Wiring the gates` section in this skill, because nothing to wire**, and absence deliberate not unfinished. Other skills in set have no such section either — `money`, `money-api`, `money-storage`, `caching`, `async-handoff`, `async-handoff-shapes` — but opposite reason: their gates real and wired by stack skill installed beside them. **This skill have no such sibling and never will**, because its directives bind process. What repo adopting this should do instead: name place these artifacts live, so "the frame is missing" is sentence someone can say about specific file.

## Named gaps — where this procedure does not reach

Silence read as coverage, so each stated.

1. **Method have no outcome measurement.** Nobody compare decision made this way against one made without it, on any axis — how long verdict survive, whether panel change pick, whether votes ever overturn claim. **Largest gap here**, and why status tier is *decided, not yet validated* not production-confirmed.
2. **Every check here catch omission, not fabrication** — see section above. Dishonest pass indistinguishable from honest one by inspecting artifacts alone.
3. **Panel shapes = three that were used, not three that were compared.** Nobody run same decision through two shapes to see whether shape change answer. Treat choice between them as cost decision.
4. **Three votes is number, not finding.** Odd, so majority resolve; affordable. Nothing establish three is where returns flatten, and no pass record claim that survive two votes and fail third.
5. **Independence between refuters asserted, not enforced.** Fresh context = what *independent* mean, and three fresh contexts of **same model** share same training corpus. Where corpus itself hold wrong consensus, three votes reproduce it three times. **Failure mode procedure least protected against.** Mitigation = the one in *Evidence is execution or a primary source* — primary source outside model, and vote against one worth more than vote against reasoning.
6. **Cost real and unbudgeted.** Four-agent panel + three votes per load-bearing claim expensive enough that honest failure mode is not skipped step but pass that quietly reclassify its claims as non-load-bearing. **Pass that run out of budget say so and land claims at *primary-source verified*** — that value exist for exactly this, and using it is honest exit.

## Markers, dates, and what they mean

**Confidence, per claim** — four values defined above, in *Mark the outcome per claim, in four values*. This skill own subject, not restatement.

**Enforcement, per rule** — *off-the-shelf*, *bespoke*, *convention*. Those three defined by `enforceable-rules`, which own them, because they are property of rule check not of research claim. Every check named in this skill is the third.

**Status tier, per rule set** — *production-confirmed*, *decided, not yet validated*, *deferred*. Also defined by `enforceable-rules`. **Repo that install this skill and not that one have this skill confidence vocabulary and neither of other two**, and no skill here supply them in that case; they are stated where used, once.

**Marker table for this skill short, and shortness is the point:**

| Claim | Marker |
| ----- | ------ |
| Every directive in this skill | convention — no execution, no primary source, no vote |
| That this procedure improves decision outcomes | **uncertain** — never measured, see gap 1 |
| That three independent refuters of one model are independent enough | **uncertain** — see gap 5 |

No column for dates: material carry none, none invented. **Conversion date is 2026-07-30**, stated once above, and not verification date.

Ground behind these directives, reasoning left out of directive text, and conditions that would reopen any of them = one hop away in **[evidence.md](evidence.md)**.