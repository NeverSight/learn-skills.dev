---
name: review-lenses
description: The perspectives every review in this workflow looks through, one question each (impact, removal, logic, behaviour, business sense, proof, coherence), the checklist each lens walks, the table of which gate runs which lens at what depth, and the brief for handing a review to an outside model. Shared reference loaded by brainstorm, write-plan and 3p-review. It is a reference, not a step of its own.
user-invocable: false
allowed-tools: Read, Grep, Glob, Bash
---

# Review Lenses

This file holds the perspectives the workflow reviews through: what each lens asks, what it catches,
and the checklist it walks. `/brainstorm` looks through them at an approach, `/write-plan` at a
plan, and `/3p-review` at built code. The gate table at the end says which gate runs which lens and
how deep. A gate names its column there and keeps a short binding copy of each checklist inline; it
does not restate the checklist, because two copies drift and the weaker one wins.

**Why lenses, and why one at a time.** Asked by hand, each of these questions has turned up a real,
usually critical defect in work that had already been reviewed: a plan, a decision, a finished build.
A review that carries several questions at once answers whichever is easiest and reports clean on
the rest, and nothing on the page shows which ones it skipped. So each lens is run on its own, with
its own question in front of you. What it finds is settled before the next lens looks: fixed, or put to the owner where it is theirs to decide.

## Rules for every lens

*Cited as **RL-N**, here and from other skills. The tag is the rule's name, not its position: a rule that is retired keeps its number and is marked retired.*

- **RL-1 · One question per lens, run separately.** Do not merge two lenses into one read, and do not skip one because an earlier lens "already looked at it". They start from different places and see different things.
- **RL-2 · Change the angle, not the effort.** Repeating a lens with the same method returns what it returned before, and that empty delta reads exactly like a clean result. When a lens is run again, it searches on something new: a different spelling, the rendered form instead of the identifier, the code inward instead of the document outward, what the change *creates* instead of what it changes.
- **RL-3 · Report a lens exactly as far as it went.** If a tool it needed was unavailable, if it covered part of the artifact, or if it checked the original code instead of the changed copy, say so, along with what you did instead. A lens reported as done when it was half done is worse than one reported as skipped, because nobody goes back to it.
- **RL-4 · A "nothing found" needs a control.** Before you trust an empty search, a clean type check or "no callers", run the same method against something you know is there and watch it find it. A check that cannot see what it is looking for returns the same empty result as one that looked and found nothing.
- **RL-5 · Reject a finding only on evidence that would have shown it.** That means a run, a probe, or a query against real data. An empty grep is not disproof, because the finding may describe a path your search did not spell. Neither is local development data: a dev fixture that lacks a condition only shows that the fixture lacks it. Without disproof, the finding stands. This is AW-16 and BS-11 (an outside review is evidence, never a verdict) applied in the other direction: evidence is also what it takes to dismiss one.
- **RL-6 · A review ends on a round that changed nothing.** Settling a lens's findings changes the artifact, and the lenses that already ran never saw that change. So when a round of lenses ends having changed what the artifact contains or how it works (a file, caller, phase, step, rule or mechanism added, removed or reshaped), run another round: every lens again, in order, each starting from what the last round changed and what that reaches, and each on a new angle (RL-2). Reworded text, corrected counts and fixed names do not start a round. A round that changed nothing ends the review. If a third round is still changing contents, stop and tell the owner in those words: the work is larger than the artifact describes, and that is theirs to decide. That stop is for a review of a document (a decision document, a plan). `/3p-review` on code keeps its own loop, every section re-run each round until zero findings, which already meets this rule and does not stop early.

## The lenses

### Impact: *what does this break that nobody mentioned?*

The method is `/existing-mechanisms`' **impact trace**, all three axes (structural, functional,
consolidation); it lives there and is not restated here. Three additions every gate uses:

- **Count with types, not names.** A graph index links symbols by name, so it misses calls made
  through an instance and merges symbols that share a name. In typed code, take every structural
  count from the language server's *find references* or the type checker, and use the graph only to
  find where to look (`/knowledge-graph`, *Counting in typed code*).
- **Let the compiler do the structural axis for removals and signature changes.** In an isolated copy of the tree (a worktree or scratch checkout, never the working tree), apply every deletion, rename and signature change, then run the project's type checkers over it. Prove it sees the change first by feeding it a deliberate break (RL-4). Empty a deleted module rather than removing it, so every use fails at its own line instead of one unresolved import per file. Point it at everything, not just the source package: scripts, tests, frontend, tooling. Then search for the names as strings, because mocks, patch targets, dispatch tables and config keys are invisible to a type checker.
- **Follow coupling through storage to both ends.** One piece of code writes a value to a table, file, queue or cache, and another acts on it. No call graph and no type checker connects them. For every value this change writes, find every reader; for every value it reads, find every writer. Check that both ends agree on what the value means. A reader with no writer is a feature that never shows anything. A writer whose value nothing reads is work thrown away. A flag that is set but never cleared makes something run forever.

### Removal: *is every removal justified, and is its job still done?*

A scalpel, not a butcher's knife. Removing working code is the one change whose damage never shows
as a failing test: what it did stops happening, and nothing asserts that it ever did. For each
removal:

- **What it was there for**, in terms of the job it did, read from the code and its history. Code that looks dead often has one caller, or guards a case that is simply rare.
- **Wire before deleting.** Code nothing calls is not always dead. Sometimes it is the right thing with its call missing. Before removing an uncalled method, ask where it *should* be called from, and whether the defect you are fixing is that missing call.
- **What does that job afterwards**, and the test on the new path that proves it. A replacement with no test proving it is an assumption.
- **What reaches it today**, from the impact lens, scripts and strings included. A removal with a live caller is a break, not a cleanup.
- **One removal, one step.** "Delete the old module" covering four jobs, one of them still live, is how a whole behaviour disappears in a single line of diff.
- **No replacement goes to the owner.** If the job simply stops being done, it is a lost capability, and only the owner can agree to it. Put it to them in those words.

### Logic: *does it work when it actually runs?*

Stop reading and run it. Pick concrete inputs and step the mechanism through one write at a time,
noting the state after each. Reading checks whether it sounds right; stepping it through shows what
it does. Walk every one of these:

- **The main case, end to end, with real values.** Most of the cases below come from one detail of this walk being different.
- **Zero, one, many, and the edge.** Empty collection, absent target, first run, last item removed, exactly at a limit, over a budget, a page boundary. Watch for an empty value that falls through to a *different meaning* rather than to nothing.
- **Rules that overlap.** Look for an input that satisfies two conditions. If order decides, the order is stated and pinned. Anything evaluated in declaration order says that the order is load-bearing.
- **Time.** What is written before what, and what a reader sees in between. A value copied at write time freezes; one worked out at read time moves. Caches, polls and stale windows show the old answer for their whole length. Timers stop when a screen is hidden.
- **Crash and retry.** Kill the process between every pair of writes. Does the retry repeat the work, skip it, or do it twice? A progress marker written before the work it records makes a crash skip that work for good.
- **Two at once.** Parallel jobs, two tabs, a worker and a route. A load-edit-save of a whole object puts back a field another copy just changed. Anything shared rather than copied is visible to both at once.
- **Work reported but never cleared.** For every scheduler, sweeper, retry or queue, find what makes it stop. If the work it does never clears the report that started it, it runs forever. Once you find one path into the loop, look for a second.
- **Values against each other.** Put every threshold, weight, limit, timeout and budget next to the ones it interacts with. A name weight of 0.85 against a grouping threshold of 0.85 means a name match alone groups two different people. No single value is wrong; together they are.
- **Can the mechanism express the rule?** Read the rule as decided, then the reducer, scorer, key or query meant to implement it. Averaging can never let a second reason raise a score. A unique key on name alone can never express "same name, different type".
- **Where each promise is enforced.** Name the layer that makes each rule impossible to break. A rule enforced only by the UI, a prompt or a comment is not enforced. When something is deleted, ask what it was the *only* enforcement of.
- **Reuse across a contract.** A helper built for unpaged, ordered, single-threaded or trusted input, reused where those do not hold, spreads its defect to the new caller.
- **Hostile input.** None, empty, unicode, a budget of 0 or -1, a duplicate. Does it terminate, is it idempotent, does it leave the caller's data alone?

**Probe it rather than reasoning about it.** When a conclusion rests on how existing code behaves at
runtime, and a read-only local probe costs minutes, run the probe. A table worked out by reading can
be wrong four times in a row where one call with real inputs is right the first time.

### Behaviour: *does a human user get what they expect, on every surface?*

The logic lens asks whether the mechanism is correct. This one asks whether the product is. Sit in
the user's seat: the person who opens the screen, reads the report, clicks the button.

- **The goal, as the owner will see it.** Name what the owner will see, on which screen or in which output, once this ships. A design can honour every decision and still produce something the owner looks at and says was not the point, such as "retain what extraction returns" built as a log table nothing reads.
- **Every surface that shows the changed data.** Screens, reports, exports, dossiers, notifications, and the prompts that feed a model. Walk the changed data onto each one. A field that is blank on three of them, or a link that opens nothing, is invisible to the mechanism's tests.
- **Similar actions behave the same.** Re-read and delete, archive and remove, retry and resume, bulk and single. If one cleans up after itself and the other does not, the user sees an inconsistency no single code path shows.
- **The second caller, and the late one.** What does the second tab, second worker or resumed job get when the first already did the work? Do "already done" and "nothing there" look the same? Is a cache keyed on what the user typed rather than on what they meant?
- **The expectation, in the user's words.** For the two or three main actions, write one sentence as the user would say it ("I delete the document and its entities go with it"). Check the design does exactly that, or says plainly where and why it does not.

### Business sense: *would this make sense to the business, and to a typical user who never heard the reasoning?*

This lens questions the *decisions*, including the owner's own. The behaviour lens checks that the
design delivers what was intended. This lens checks whether what was intended is sensible for the
business and unsurprising to its users. It catches the design that is internally consistent,
correctly built, and odd: a rule no user would guess, a step that exists only because of how the
code is shaped, a term that means something different in the user's domain, an outcome that is
technically right and commercially wrong.

- **Read it cold.** The defects this lens exists for look reasonable to anyone who knows why they were decided, and you usually do. So work from the outcomes alone: what the user does, sees and gets, not the rationale. If you can hand this lens to a reader with fresh context (a subagent started without this conversation, or another model; see the outside-review brief below), do. The value comes from not knowing the reasons.
- **Walk it as a typical user of this domain**, not as its builder. Name the user (an analyst on a case, a shopper at checkout, an operator at 3 a.m.), then take them through the main journeys. At each step, ask: would they expect this? Would they need to be told? Would they be annoyed, confused, or wrong about what just happened?
- **Ask the business questions directly.** Does it serve the requirement it was built for, or a proxy that is easier to build? Does it cost the user time, money or trust in a way the business would not sign off on? Would a competitor's user find this normal? Does anything contradict what the product tells users elsewhere?
- **Challenge the owner's steer as well.** Where a decision came from the owner, and a typical user would find the result odd, say so. Put it as a question with the user's-eye view attached, not as a correction. The owner may have a reason; the point is that they choose with it in view.
- **Each finding says who is surprised, by what, and what they would have expected.** "Odd" alone is not actionable.
- **A defect or a question: decide which before you report it.** It is a **defect** when the user's expectation is plain and no decision chose the odd outcome: the artifact simply does something nobody asked for, such as a run over one aspect of a pending item marking the whole item done. Fix it as you would any other finding, and tell the owner in one line what changed. It is a **question** only when a recorded decision or the owner's steer produced the odd outcome, or when typical users could reasonably expect two different things. **If you cannot tell which it is, it is a question.** Asking the owner whether to fix a plain defect hands them a decision nobody needed to make.
- **Once the owner has ruled on a point, it stays ruled.** Their answer is recorded under the decision document's *Would find odd*. A later gate does not raise it again unless something new changes it: a surface nobody had considered, or a build that behaves differently from what they ruled on. Then say what is new.

### Proof: *would the tests fail if this were built wrong?*

A test is worth only the defect it rejects.

- **Name the defect each test exists to catch, then break it that way and check that it fails.** Watch for these shapes: a fixture too small to reach the path; an assertion on a symptom that holds while the defect is live; a substring check that passes on reworded or re-wrapped leftovers; an assertion true in every mode; "exits 0" with nothing asserted.
- **Every guard has a mutation check**: the exact revert, and the failure it must produce.
- **Existing tests, in three kinds.** Tests that will break are updated to assert the new truth, never loosened to accept it. Tests that keep passing and stop meaning anything are rewritten or retired. Tests that reach the code indirectly (patched factories, captured arguments, module mocks) are named, because they break in ways that look nothing like the cause.
- **Tests run the path production runs.** A test that builds through a shortcut, calls an internal step production never takes, or stubs the layer the defect lives in proves the shortcut.
- **Anything held constant and relied on gets a pin**: a byte-identity fixture or a golden output, because prose does not stop a reword.

### Coherence: *does the document still agree with itself?*

Every lens edits the artifact in one place against its own question. Read the result once, top to
bottom, as the next reader will.

- **Contradictions** between sections, steps, criteria, scope and risks.
- **Orphans**: anything whose reason a later decision removed.
- **Stale summaries**: counts, lists, mappings and headlines that no longer match the body.
- **One name per thing**, and no new name that collides with an existing one.
- **Sequence**: if it is built in order, does each step stand on what came before?
- **One story**: would someone who did only the steps end up where the summary says?

## Which gate runs which lens

Each gate is a column. Depth is the gate's, and so is what happens to a finding.

| Lens | `/brainstorm`: on the approaches and the recommendation | `/write-plan`: on the finished plan | `/3p-review`: on the built code |
|---|---|---|---|
| impact | every approach at survey depth; the recommendation in full, in the decision audit | the **impact pass** (structural and functional), then the **consolidation pass** (the trace's third axis and the self-duplication inventory, as a pass of its own under RL-1) | *Consumer authority*, *Coupling through storage, both ends*, and the plan's Impact Analysis block checked against the code |
| removal | what each approach removes and what does that job after; a job with no replacement is a cost in the comparison, and it goes to the owner | the **removal pass** | *Retirement actually happened*, plus the new-path test for each removal |
| logic | every approach through the main case and its edges, enough to rank them; the recommendation in full, especially *values against each other* and *can the mechanism express the rule*, which are cheapest to fix here | the **logic pass** | *Correctness*, walking the built code with concrete values rather than reading it |
| behaviour | what the user sees under each approach; the recommendation's user-facing sentences go into the decision document's **What the User Sees** | the **behaviour pass**, checked against those sentences | the *Behaviour* section: drive the built thing on each surface and compare with the sentences |
| business sense | every approach, and the owner's own steer, read cold | the **business-sense pass** | the *Business Sense* section: the plan does not matter on its own; the built thing has to work the way the business needs. A defect is graded and fixed like any finding; a question goes to the owner and does not hold the gate |
| proof | for each load-bearing claim, what would prove it (BS-9, BS-10) | the **proof pass** | *Tests*, with the mutation checks run |
| coherence | the decision document once written, before `/write-plan`: Decision against Consequences, the scenario table and What the User Sees | the **coherence pass** | not run on code; *Codebase Consistency* covers the equivalent |

## Handing a review to an outside model

An outside reviewer, whether another vendor's model or a fresh-context agent, finds what you cannot:
it does not know why anything was decided, so it sees the result the way a newcomer does. Every
gate that finishes a reviewable artifact (a decision document, a plan, a build) offers the owner
this brief in one line, and writes it out, filled in and ready to paste, when the owner says yes.
The offer is made once per artifact, not repeated.

What goes wrong without a brief: the reviewer starts fixing things, filing tickets, and proposing
edits; it answers "do the plan and the code match?" when the question was "are they both right?";
and it pads the answer with everything that is fine.

```markdown
You are reviewing, not changing. Do not edit files, run anything that writes, or file tickets.
Read-only commands only, one simple command per call. Changes are another model's job; yours is to
find what is wrong.

**What to review:** [the decision document / plan / commits, by path or hash] in [repo path].
**What it is for:** [the business requirement, in one or two sentences, in the owner's words].

**The question is whether it is right, not whether its parts agree with each other.** Is the logic
correct? Does it deliver the business requirement? Does it make business sense? Two documents can
agree and both be wrong, so agreement alone is never the answer.
[For a plan: also check that it implements every decision in the decision document; a decision
with no phase is a finding. For code: do not check that it matches the plan; check that it works.]

Look through each of these separately:
1. Impact: trace callers, call sites and dependants both ways. Count them with the type checker
   or language server this repo uses [e.g. tsc, pyright, go build]; a name-based index misses calls made
   through an instance. Include values one component writes to storage and another reads; no tool
   links those, so check that both ends agree.
2. Removals: a scalpel, not a butcher's knife. Each removal is justified line by line, its job
   still done. If something is uncalled, ask whether it should be wired in rather than deleted.
3. Logic: walk it with concrete inputs, edge cases, crashes between writes, two copies running at
   once, loops that never stop, settings that defeat each other.
4. Behaviour: every screen, report and prompt that shows the changed data. What does the user
   actually see?
5. Business sense: as [the typical user, named], would anything here be odd, surprising or
   pointless, including things that were decided on purpose?

**Report only what is broken, possibly broken, or doubtful, and whether there is a better
approach.** Do not tell me what is fine. For each finding, give the file and line you opened and
confirmed, who or what is affected, and why. Do not repeat points already answered unless new code
changes the answer.
[On a follow-up round: here is what was rejected and why; weigh it and say if the rejection holds.]
```

When its findings come back, they are evidence, not instructions: verify each against the code, fix
what holds, and reject only under RL-5.
