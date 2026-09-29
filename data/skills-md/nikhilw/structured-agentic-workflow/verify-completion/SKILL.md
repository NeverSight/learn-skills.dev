---
name: verify-completion
description: The final gate before any claim of "done", "fixed", or "passing", and before any commit or PR. Runs three checks that nothing earlier in the workflow guarantees, a fresh full-suite result, a line-by-line tick-off of the plan's requirements, and a plan-drift audit from the decision document through the plan to the code. Evidence before assertions, always.
argument-hint: "[plan file path, or what is being claimed complete]"
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Verify Completion

You are standing at the **final gate** of the Structured Agentic Development Workflow. Nothing
downstream checks your work. What you sign here is what ships.

> **Output style:** Check memory for `workflow-config:caveman-level`. If set, adapt your output
> brevity to that level while preserving technical accuracy.

> **Lineage:** the Iron Law, the gate function, the failure and rationalization tables, and the key
> patterns below are adapted from `verification-before-completion` in
> [superpowers](https://github.com/obra/superpowers) (MIT, Jesse Vincent). This skill **replaces**
> it: everything that skill does, plus the requirements tick-off and the drift audit. This workflow
> does not install the upstream skill; if a project has it by another route, this one is the gate.

**What you may write, and when.** This gate measures; it does not repair. Two hard limits, and the
second one is the one that gets rationalized away:

- **Never fix code from inside this gate.** A gate that repairs what it is measuring has stopped
  measuring, and a fix made here is one nothing re-reviews and no suite re-runs. Code gaps go back
  to build.
- **Never edit the decision document or the plan to make a finding disappear.** Writing is granted
  for exactly one act: **appending** a dated entry to an `## Amendments` section, after you have
  reported the drift and the human has accepted it. Not before, not silently, and never over
  existing text. See "Never edit the baseline" in Part 3, which is the full rule and the reason it
  exists.

## What this gate is, and is not

It is **not a second review**. `/3p-review` proved the *code* is sound; re-reading the code here
buys nothing and costs a rework loop's worth of time. This gate proves three different
propositions, none of which review establishes:

1. **The suite is green right now.** Review may have passed several edits ago.
2. **Every requirement was actually built.** Review judges completeness qualitatively; this is the
   line-by-line tick-off.
3. **What shipped is still what was decided.** Plans drift. Every halt, every constraint found
   mid-build, every reverted phase moves the plan a little, and the accumulated distance from the
   decision document is invisible from inside any single step. This is the only place the whole
   chain is read end to end.

Check 3 exists because of a specific, expensive failure: you set out to build one thing, the plan
absorbed a dozen small corrections, and what shipped is a different thing. Nobody notices for days,
because every individual amendment was reasonable.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you have not run the verification yourself, in this session, you cannot claim it passes.

The only exception is a citation meeting all four conditions in Part 1, and it is an exception in
name only: a citation is a *stricter* claim than a fresh run, because it proves both that the suite
passed and that nothing has changed since. Anything less than that, a run someone reported to you,
a run from before an edit, a narrower run described in wider words, is not evidence.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY  What proves this claim? (command, checklist, document comparison)
2. RUN       Execute it fully, fresh, now
3. READ      Full output, exit code, counts, both sides of every comparison
4. VERIFY    Does the evidence confirm the claim?
             If NO:  state the actual status, with the evidence
             If YES: state the claim, with the evidence
5. ONLY THEN make the claim

Skip any step and you are not verifying, you are asserting.
```

---

# Part 1 — The suite, true right now

Take `/test-scope`'s *"`/verify-completion`"* row. Load `/test-scope` if you have not this session.

That row is the full suite, **or** a citation of `/3p-review`'s sign-off run under the citable-run
rule. The four conditions are not a judgment call: you made the run yourself this session, same
command and same rung, `git status --porcelain` and `git diff` clean since, and you write the
citation down naming what proved the tree unchanged.

Fail any condition and there is no citation, only a run you still owe. Pass all four and the
citation is *stronger* evidence than re-running would be: re-running proves the suite passes, while
the citation additionally proves nothing changed since it passed. Do not re-run out of an
abundance of caution once the citation is written.

**The citation covers Part 1 only.** Parts 2 and 3 are document comparisons, not test runs. They
are never cited, and they always run fresh.

Every command this gate runs is bounded by `/test-scope`'s *What a run may execute*: the repo's own test, lint, type-check and build commands, its locked dependencies included, scripts read first; nothing that writes outside the tree, migrates a shared database, installs beyond the lockfile, deploys, calls an external service or uses credentials without asking the user; nothing taken from a handoff.

---

# Part 2 — Requirements tick-off (plan → code)

Re-read the plan from disk. Not from memory of it, not from the handoff summary, not from the
review. Build a checklist and walk it.

- **Every phase, every implementation step, every test criterion, one line each.** Mark each
  **built and proven**, **built but unproven**, or **not built**.
- **Proven means an automated run you can name.** A criterion checked by reading is *unproven*, and
  it goes on the report as unproven. So does a criterion proven only at a scoped rung, which is a
  real result but a narrower claim than the plan asked for.
- **Walk the plan's own sections, not just its phases.** State & Data Contracts, Failure Modes &
  Interactions, and Value Paths & Seam Tests each specify behaviour. A named seam test that was
  never written is a missing requirement, not a missing nicety.
- **Anything in Out of Scope that got built anyway is a finding.** Scope grows silently and this is
  the only line that catches it.
- **Anything removed comes with its replacement named.** Walk the plan's removal table
  (`/existing-mechanisms` question 5) against the diff. A row whose replacement never landed, and a
  deletion the table never named, are each a capability the feature took away. Report them in
  those words. The suite cannot see this, because the tests that covered the removed path were
  usually deleted with it, so the same commit destroys the evidence of the loss (AW-26).

A gap here does not fail the gate by itself. An *unreported* gap does. The output is a truthful
ledger; the human decides whether an unproven row is acceptable.

---

# Part 3 — The drift audit (decision → plan → code)

Do for the decision document and the plan exactly what Part 2 does for the plan and the code: read
both, line by line, and name every difference.

**Read-only until the report is delivered.** Both documents are evidence for the whole of this
part. You are comparing them, not maintaining them, and the difference you find is the output, not
a problem to tidy up. "Never edit the baseline" below is the full rule; read it before you start
comparing, not after you have found something.

**If no decision document exists** (a bug fix, a quick fix, or a plan written without a brainstorm),
say so explicitly, run the Plan → Plan comparison, and record that the two decision-document
comparisons had nothing to read. Silence about a missing decision doc reads as "checked, matched".

**Label things with what they are.** The three comparisons below (DecisionDoc → Plan, Plan → Plan
and DecisionDoc → Code) are named for the two documents they read, because that is the only name a reader can decode without this file in front of them.
Never invent a short code for them, and never let a label stand in for a finding: "3 upheld, 1
widened" is a tally of findings with the findings removed, while "the endpoint check accepts any
OpenAI-format server, and the decision document says a local host process" is the finding. Part 4
is the shape the output takes.

### Baseline: is the decision document still the one that was agreed?

The audit is only worth what its baseline is worth, so fix the baseline first and say where it came
from.

- **Read the decision document from version control where it is tracked** (`git log --follow -p --
  <doc path>`, or `git show HEAD:<doc path>`), not only from the working tree. The committed
  history is the one copy that cannot be quietly reshaped to match the code.
- **Compare it against the working copy.** If they differ, something edited the baseline during or
  after the build. That is not a detail to absorb: find out what changed, who changed it, and
  whether it was recorded, and put it in the report. An edit to the Decision or Consequences
  sections with no Amendments entry is itself a finding, and a serious one.
- **If the document is untracked**, say so in the report. You are auditing against a baseline that
  anyone could have edited at any time, which weakens every conclusion below, and the human should
  know that before reading the verdict.

### DecisionDoc → Plan: what was decided, against the plan as it now stands

Read the decision document and the current plan side by side. For every decision in the document,
and every consequence it recorded:

| Disposition | Meaning | Acceptable? |
|---|---|---|
| **Upheld** | the plan implements the decision as written | yes |
| **Narrowed** | the plan implements part of it, deliberately, and says so | yes, if the plan says so |
| **Superseded** | the plan does something the decision ruled out | only with an Amendment Log entry naming the decision it supersedes |
| **Dropped** | the decision is simply absent from the plan | **no**, this is the finding |

**Record both sides as you go, and quote them.** The disposition word is your judgment about a
difference; it is not the difference. Write down the decided text in the words it was decided in,
and what the plan or the code does instead, with the file and line where it does it. Do it while
both documents are open, because reconstructing the quote later is what turns a finding into
"narrowed" and loses the only part the human needed.

Also check the two lines of the decision document that age fastest:

- **"What would reverse this decision."** The document named the condition under which the
  runner-up wins. Did it come true during the build? A build that discovers exactly that condition,
  patches around it, and ships the original approach anyway is the most expensive form of drift
  there is, and no single amendment entry will show it.
- **Open Questions.** Each is answered, or still open and carried forward in writing. An open
  question that quietly stopped being asked was answered by whoever wrote the code.

### Plan → Plan: the approved plan, against the plan as it now stands

Every difference must have an entry in the plan's **Amendment Log**. Establish the approved
baseline in this order, and say which one you used:

1. **Git history of the plan file** (`git log --follow -p -- <plan path>`), if it is tracked. This
   is the only baseline that cannot be edited after the fact.
2. **The Amendment Log itself**, read as a claim rather than as proof.
3. **The copy the build model was handed**, if the user still has it.

If the plan was never tracked and the log is empty while the code plainly implements something the
plan does not describe, that absence *is* the finding. Write it that way.

### The scenario table, if the decision document has one

A decision that moved a rule carries a table of cases with the outcome decided for each (BS-13),
and it is the only part of the decision document that ticks off mechanically rather than being read
for intent. Take each **differing** row, find what the code now does in that case, and compare. A
row labelled *collateral* is the one to check hardest: it was a behaviour change nobody asked for,
the user accepted it explicitly, and it is the likeliest thing in the whole document to have been
built as though it had never been decided. A row whose built behaviour does not match its decided
outcome is a drift finding like any other, and it is reported with both cells quoted.

### What the User Sees, if the decision document has it

The same check for the section that records what the user was promised (BS-14): each expectation
sentence, in the user's words, against what the built thing does on the surface where the user
would check it. Run it where you can drive it, and say where you only read the code. A sentence the
build does not honour is a drift finding, reported with the sentence quoted beside what the user
actually gets. So is an item under *Would find odd* that the owner ruled on and the build ignored.

### DecisionDoc → Code: what was decided, against what actually shipped

The round trip, and the one that catches what the two comparisons above cannot on their own. Read
the decision document's **Problem** statement, then read the code. Answer in your own words:

- Does what shipped solve the problem that was decided, or a neighbouring one?
- Would the approach comparison in that document still choose this approach, knowing what the build
  found out?
- Did the accumulated amendments move this to a different approach than the one chosen, without any
  single amendment saying so?

The third question is the point of this gate. Six reasonable amendments can add up to Approach C
while every entry in the log reads like a detail.

**A "yes" to any of those three goes to the human, even when every amendment is logged.** Perfect
bookkeeping and a feature that ended up somewhere nobody chose are entirely compatible states, and
this is the last moment anyone is looking at both documents at once.

**Scale the audit to what actually moved.** A plan with an empty Amendment Log and a decision
document it never departed from is audited in minutes: the plan-against-plan comparison is trivially
clean, and the two decision-document reads are one careful pass over documents you already have
open. The work grows with the drift, which is the
correct shape; if this gate feels expensive, that is the feature telling you something.

### Never edit the baseline to make the drift go away

**This is the one way this gate can do more harm than not running at all.** You will find a
difference, and the cheapest-looking move will be to change the decision document so it matches
what was built, then report no drift. Do not do it. Rewriting the baseline does not remove drift;
it destroys the only evidence that drift happened, and it produces a false clean verdict that every
later reader believes. The whole feature was measured against that document. The moment you edit
it, you are no longer measuring anything.

Concretely, during this gate you may not:

- change, reword, soften, "clarify", "correct", or delete **one word** of the decision document's
  Problem, Contracts, Approaches, Decision, What the User Sees, or Consequences sections, or of any existing Amendments
  entry;
- change, reword or delete any part of the plan, including existing Amendment Log entries;
- do any of the above and then report a better verdict.

**Where this gate writes, and that is all of it:** an `## Amendments` entry appended to the end of
the decision document and the matching entry appended to the plan's Amendment Log — both only
after the human has ruled — and the `mv` that moves the plan to `done/`. The completion report
itself is said, not saved (AW-29).

**The verdict is a fact about what the build did, not about what the documents say right now.** If
the work departed from a decision and nobody recorded it, that is UNDOCUMENTED DRIFT, and it stays
UNDOCUMENTED DRIFT in this report no matter what gets written down afterwards. It cannot be turned
into DOCUMENTED DRIFT by you, in this session, with a keystroke. Writing the record later does not
change what was found; it only means the next person inherits an honest document.

### The verdict, and what to do with it

| Verdict | Meaning | Action |
|---|---|---|
| **NO DRIFT** | plan implements the decisions; code implements the plan | record it and move on |
| **DOCUMENTED DRIFT** | differences exist and every one was written down **before you got here** | report each one; the human confirms it is still the feature they wanted |
| **UNDOCUMENTED DRIFT** | a difference nobody wrote down | **blocking, and it stays on the report.** Status is NOT COMPLETE until the human rules on it |

**Report first. Writing is a separate act, and it is the human's call.** Present the drift report,
say plainly what departed from what, and stop. Then:

- **The human accepts the departure.** Only now may you append to the record, and only by adding to
  an `## Amendments` section at the **end** of the decision document, leaving everything above it
  untouched. Every entry is dated and says it was found here, so nobody later mistakes it for
  something that was decided before the work.
- **The human rejects it.** The gap is in the work, not the record. It goes back to build, and the
  status stays NOT COMPLETE.
- **The human says nothing yet.** Nothing is written. An unanswered question is not consent.

```markdown
## Amendments
### YYYY-MM-DD — [what changed]  *(found at verification, accepted by the human)*
- **Supersedes:** [the decision or consequence in this document, quoted so the original is legible]
- **Now:** [what was actually built]
- **Because:** [what the build or the plan found that the decision did not know]
- **Recorded in:** [plan Amendment Log entry ID, or "no plan entry existed; this gap was found here"]
```

Then add the matching plan Amendment Log entry if one is missing, appended the same way.

The point of the written record is that a later reader can see **both** what was decided and what
happened instead. An amendment that replaces the original leaves them one story and no way to tell
it was ever a different one.

---

# Part 4 — The completion report

You are writing to the person who asked for the feature, and the only question they have is *did I
get what we agreed, or not*. Answer that first, in their words. The report is said, not saved
(AW-29), and it is **the one report this gate emits**: Parts 1 to 3 are worked, not narrated, and a
check that came back clean is evidence for the bottom of this report rather than an update of its
own (AW-28). Three rules:

- **Bad news first.** What is wrong opens the report. Everything that checked out is evidence, and
  evidence goes at the bottom. Nobody should have to read a clean checklist to discover that the
  thing they asked for is not there.
- **Show both sides of every difference.** Quote what was decided, in the words it was decided in,
  then say what was built instead and where it lives. "Narrowed", "half-implemented" and "widened"
  are your labels for a difference, not the difference; a reader cannot rule on a label. One row,
  two columns, both filled.
- **Say it in the words of the work, not the words of this skill.** Section names, check names and
  internal shorthand mean nothing outside this file. The verdict keyword and the rung on the suite
  line are the only terms that travel, and each gets a plain sentence next to it.

If there is no decision document, the first section says exactly that, because "nothing departed
from what we decided" and "nothing recorded what we decided" look identical on a page and are not
the same finding.

```markdown
## Completion Verification

**Claim:** [what is being claimed complete]
**Plan:** [path]   **Decision doc:** [path, or "none, so there is no record of what was decided"]

### Status: COMPLETE / NOT COMPLETE
[One line, in the owner's terms: what is wrong, or that nothing is. If the drift verdict is not NO
DRIFT, name it here in a clause: "...and nobody wrote that down before this gate (UNDOCUMENTED
DRIFT)."]

### What we decided and did not build
[Every departure from the decision document, one row each. Or: "Nothing. Every decision in [doc] is
in the code as written."]

| We decided | We built instead | Where | Was it written down before this gate? |
|---|---|---|---|
| "[quoted from the decision doc]" ([which section]) | [what the code actually does, plainly] | [file:line] | no, found here / yes, [amendment entry] |

### What we built and nobody decided
[Capability that widened past what was decided, scope the plan never carried, a plan step with no
amendment behind it. Same two columns, same quoting. Or "Nothing."]

### What the plan asked for and is not there
[Requirements not built; requirements built but unproven; capabilities removed whose named
replacement never landed, and deletions no removal table named. Or "Nothing."]

| The plan asked for | What is actually there | Proven by |
|---|---|---|
| [requirement / contract line / seam test / removal-table row] | not built / built, nothing proves it / replacement never landed | [run name, or why nothing proves it] |

### Your call
[Numbered, one line each, cheapest first. What needs a ruling, and what each choice costs. Or
"Nothing needs a ruling."]

### Evidence
**Suite:** [run name] (rung T4, the full suite) → exit [code], [N passed, M failed, K skipped].
[Fresh, or: cited from /3p-review's sign-off run; tree proven unchanged by git status and git diff.]

**Every requirement, including the ones that passed:**

| Requirement | Status | Evidence |
|---|---|---|
| [phase / criterion / contract line / seam test] | built and proven / built but unproven / not built | [run name, or why not] |

**What the drift audit compared:**
- **Baseline:** decision document read from [git at <ref> / the working tree only, because it is
  untracked]; working copy [identical to the committed version / differs: what, and whether an
  Amendments entry covers it]. Plan baseline: [git history / the Amendment Log read as a claim /
  the handed-off copy].
- **DecisionDoc → Plan:** [N] decisions read, [N] upheld, [N] narrowed, [N] superseded, [N] dropped.
  Each departure is a row above.
- **Plan → Plan:** [each difference from the approved plan and the Amendment Log entry behind it,
  or "none"].
- **Scenario table:** [N] differing rows checked against the built behaviour, [N] matched; each
  mismatch is a row above. [Or: the decision document carries no table, or it records "not a rule
  change".]
- **What the User Sees:** [N] expectation sentences checked against the built behaviour, [N] held;
  each broken one is a row above. [Or: the decision document has no such section.]
- **DecisionDoc → Code:** [does the code solve the problem that was decided; did the document's
  "what would reverse this decision" condition come true during the build; did the amendments add
  up to an approach nobody chose].
- **Verdict:** NO DRIFT / DOCUMENTED DRIFT / UNDOCUMENTED DRIFT
- **Documents I changed during this gate:** [none, or: the appended Amendments entry, after the
  human accepted it, quoting what they said. Nothing else, ever. "None" is the normal answer.]
- **Record still to close:** [what the human has not yet ruled on, or "nothing"]
```

If the verdict is UNDOCUMENTED DRIFT, or any requirement is "not built", the status is **NOT
COMPLETE** until the record is closed or the human accepts the gap in writing.

---

## Common failures

| Claim | Requires | Not sufficient |
|---|---|---|
| Tests pass | Test command output, 0 failures | A previous run, "should pass" |
| Linter clean | Linter output, 0 errors | A partial check, extrapolation |
| Build succeeds | Build command, exit 0 | Linter passing, logs that look fine |
| Bug fixed | The original symptom re-tested, passing | Code changed, fix assumed |
| Regression test works | Red then green, verified | The test passing once |
| Agent completed | The VCS diff, read | The agent reporting success |
| Requirements met | The line-by-line checklist | Tests passing |
| Built what we decided | The drift audit, all three comparisons | The plan being followed |
| Nothing was lost | The removal table walked against the diff, each replacement found | The suite passing after the deletion |
| No drift | Both documents read as they stand, differences named | The documents agreeing after you edited one |
| A difference is reported | The decided text and the built behaviour quoted side by side | A disposition word, a check name, or a count of them |

## Red flags, stop

- "Should", "probably", "seems to"
- Satisfaction expressed before evidence ("Great!", "Perfect!", "Done!")
- About to commit, push, or open a PR without running this gate
- Trusting an agent's or another model's success report
- Relying on a partial run, or on a scoped rung described in full-suite words
- Writing "narrowed", "partial", "widened" or "half-implemented" without the decided text and the
  built behaviour beside it
- A report that opens with what passed
- **Reaching for the decision document or the plan with an edit in mind while the audit is running**
- Noticing that a document "just needs updating" to match the code
- "Just this once"
- Tired and wanting the work over
- Any wording that implies success without the evidence behind it

## Rationalization prevention

| Excuse | Reality |
|---|---|
| "Should work now" | Run it |
| "I'm confident" | Confidence is not evidence |
| "Just this once" | No exceptions |
| "The linter passed" | The linter is not the compiler |
| "The agent said success" | Verify it first-party |
| "I'm tired" | Exhaustion is not an excuse |
| "A partial check is enough" | Partial proves nothing |
| "Different words, so the rule does not apply" | Spirit over letter |
| "Review already ran the tests" | Grounds for a citation if all four conditions hold; never grounds to skip the gate |
| "The plan changed, so the decision doc is out of date" | That is drift. Report it. The document is the baseline, not a draft to refresh |
| "Every amendment was reasonable" | Reasonable amendments still add up to a different feature |
| "I'll update the decision doc so it matches what we built" | That is the failure this gate exists to catch, committed by the gate itself. Report the difference; append only after the human accepts |
| "The decision was clearly superseded, so the old text is just wrong now" | Superseded text is the evidence. It stays, and the amendment goes below it |
| "It's only a wording fix to the old decision" | There are no wording fixes to a baseline during an audit |
| "Nothing went red when we removed it" | The tests for it were removed too. Name the capability, not the suite |
| "The report is accurate" | Accurate and unreadable is a failed report. If the owner cannot see what they decided next to what they got, you have not told them |

## Key patterns

Each row of the Common failures table has a procedure behind it. These are the ones people get
wrong most often, in the form that is quickest to check yourself against.

**Tests**
```
GOOD  run the suite → read "34 passed, 0 failed" → "all tests pass (T4 full, exit 0)"
BAD   "should pass now" / "looks correct" / "tests pass" with no rung and no counts
```

**Regression tests, red then green**
```
GOOD  write the test → run it (passes) → revert the fix → run it (MUST FAIL) → restore → run (passes)
BAD   "I've written a regression test" with no red phase ever observed
```
A regression test that was never seen failing is not known to test the regression. This is the
single most common way a fix ships with a test that would not have caught it, and the revert takes
seconds.

**Build**
```
GOOD  run the build → exit 0 → "the build passes"
BAD   "the linter passed" (a linter does not compile, and a type checker does not link)
```

**Bug fixed**
```
GOOD  reproduce the original symptom → apply the fix → the original reproduction now passes
BAD   the code changed in the right area, so the bug is assumed fixed
```

**Requirements**
```
GOOD  re-read the plan from disk → checklist → verify each line → report gaps or completion
BAD   "tests pass, so the phase is complete"
```

**Delegated or handed-off work**
```
GOOD  the agent (or build model) reports success → read the VCS diff → verify the changes → report the actual state
BAD   the report is taken as the result
```
This is the same rule `/3p-review` runs on a handoff summary, applied here to anything you did not
do with your own hands: a subagent, another session, another model, another person. A report is a
claim about the tree. The tree is the evidence.

## When to apply

**Always, before:** any claim of completion, correctness, or success, in any wording; any
expression of satisfaction with the work; committing, pushing, or opening a PR; moving to the next
task; archiving the plan.

This gate is never optional and is never skipped, regardless of model, time pressure, or
confidence. It also covers the bug and quick-fix path, which skips full review entirely: there the
suite comes from `/test-scope`'s no-plan row, Part 2 runs against the reported symptom instead of a
plan, and Part 3 says explicitly that there was no decision document.

## The bottom line

No shortcuts for verification. Run it, read the output, then claim the result. Read both documents,
then claim it is what was decided. This is non-negotiable, and claiming completion without it is
dishonesty rather than efficiency.

## What happens next

When the report says COMPLETE: move the plan from `docs/plans/` to `docs/plans/done/` with plain
`mv` (not `git mv`; the plan file may not be tracked). The feature is done.
