---
name: resume-handoff
description: Pick up unfinished work from docs/<feature>/HANDOFF.md in a fresh session — you are the agent the handoff was written for, and you verify it before you trust it. Use when the user invokes /resume-handoff <feature>, points at a HANDOFF.md, or asks to continue, resume, or pick up where the last session stopped on a plan or roadmap built by execute-plan, execute-roadmap or build-feature, e.g. "pick up the handoff and keep going while I sleep". Reads the project's agent orientation and the handoff, reconciles its claims with git and the code, surveys the pending merge and proposes the scope — then stops and asks the user to confirm the merge and plan of work, or give new instructions, before anything changes the tree. On confirmation it deletes the consumed handoff, merges through the merge-branch gate, continues under execute-plan or execute-roadmap, and writes a fresh handoff at the end if work is still owed. For writing a handoff, use write-handoff; for retiring finished work, use close-plan or close-roadmap.
---

# Resume from a handoff

A previous session stopped with work still owed and left
`docs/<feature>/HANDOFF.md` (in the project's planning folder, unless it uses
another) behind for you. You have none of its conversation. You have the
tree, the handoff, and the documents it points at — and the handoff was
written on the assumption that you would read it in full before touching
anything.

You are judged on two things that pull against each other. **Your first hour
must be productive rather than archaeological** — the handoff exists so that
you do not re-derive what it already says. And **you must trust the handoff
exactly as much as it deserves** — it was true as of a date, written by an
agent under time pressure, and the tree has been the only thing that moved
since. A resumed session that believes a stale handoff builds on a branch
state that no longer exists; one that ignores the handoff pays again for
every trap it names.

The [write-handoff](../write-handoff/SKILL.md) skill says what the writer was
told to put in it. Read that skill once: knowing what the page *should*
contain tells you what to look for when it is missing.

Below, `<main>` is the main integration branch (e.g. `main` or `dev`), and
"the questions log" is wherever the project keeps open questions (if it has
no convention, a questions section or file beside the plan).

## Which skill this is

- **This skill** — the intake. Read, verify, propose, and **ask**; then, on
  the user's confirmation, merge and keep going under the executing skill
  that matches the doc. It ends by handing over, not by finishing the
  feature.
- **[execute-plan](../execute-plan/SKILL.md)** — where you go once the intake
  is done and the feature has a `PLAN.final.md`. You code it.
- **[execute-roadmap](../execute-roadmap/SKILL.md)** — where you go when the
  feature has a `ROADMAP.final.md`, or the handoff describes plans running in
  parallel. You brief and review.
- **[write-handoff](../write-handoff/SKILL.md)** — the writer's side. You will
  use it at the end of this session, because you will almost certainly stop
  with something still owed too.
- **[close-plan](../close-plan/SKILL.md)** /
  **[close-roadmap](../close-roadmap/SKILL.md)** — if the reconciliation shows
  the scope is actually complete, the handoff is stale and there is nothing
  to resume. Say so and switch; do not invent a next phase.

## Inputs

The argument names the feature, optionally a scope, and optionally a model or
effort directive, e.g.:

- `/resume-handoff cloud-sync`
- `/resume-handoff spell-check p4-p5`
- `/resume-handoff finish the roadmap, high effort for the workers`

The scope and the directive pass through unchanged to the executing skill;
resolve them the way it does, and honor any model/effort directive if your
agent tool supports it. **If the argument is only a path to a HANDOFF.md, the
feature is the folder it sits in.**

## Read before touching anything

In this order, and all of it before the first command that changes the tree:

1. **The project's agent orientation** (an `AGENTS.md`, `CONTRIBUTING.md` or
   similar). Every handoff assumes you have read it — the testing rules, the
   docs map, any rules about where you may work — and usually says so in its
   first lines.
2. **`docs/<feature>/HANDOFF.md`, in full.** Not the first screen. The traps
   are at the bottom, and the trap you skipped is the one you will hit.
3. **The documents the handoff names as authoritative, in the order it gives
   them** — usually the final doc, then the decision records or contracts,
   then `EXECUTION.md`, then the questions log. Where it says "the summary is
   not the specification", believe it: the handoff's prose recap of what was
   built is the one part of the page most likely to be wrong, because it was
   a copy the moment it was written.
4. **The project's stated principles** (a `PRINCIPLES.md` or similar), if it
   has them, and the area docs for the code this work touches.

**Do not read the revs.** `PLAN.revN.md` and `ROADMAP.revN.md` are the
history of how the final doc was reached; the executing skills work from the
final doc only. If the handoff sends you to a rev for one specific piece of
reasoning, read that piece.

## Reconcile the handoff with the tree

The handoff is a set of claims. Each one is cheap to check and expensive to
be wrong about, so check every one before acting on any. This is the same
rule [close-plan](../close-plan/SKILL.md) applies to `EXECUTION.md`: claims,
not facts. **Everything in this section and the two after it is read-only.**
Nothing changes the tree until the user has confirmed the proposal.

**Where you are.** `git rev-parse --show-toplevel` must be the checkout the
handoff names, or a moved copy of it — drive letters and roots differ between
machines, and a path that is not this root is not yours to edit. If the
checkout (or worktree) does not exist but the branch does, note that creating
it is the first thing you will propose. If the branch does not exist locally
either and the handoff says nothing was pushed, **stop**: the work is on
another machine and nothing here recovers it. Tell the user which branch and
which machine.

**The state of the branch**, against what the handoff says:

- `git status` — is the tree clean? An unclean tree at resume means the last
  session stopped mid-write, or someone has worked here since. Read the diff
  before deciding which.
- `git fetch`, then `git log --oneline <branch>..<main>` and
  `<main>..<branch>` — the ahead/behind counts the handoff quotes were true on
  its date. If they have grown, the handoff's merge advice was written
  against a smaller `<main>`.
- `git log origin/<branch>` — does "not pushed" still hold? The answer changes
  what a mistake costs.
- **Every commit hash the handoff cites** exists (`git cat-file -t <hash>`),
  and the newest one is at or near the tip. **Anything committed after the
  handoff's date is work the handoff does not know about.** Read those commits
  before trusting "where to resume".

**What was built**, against the code. For each phase or plan the handoff and
`EXECUTION.md` call landed, open the code and check it does what the final
doc's verification step says. A phase is landed when the code does it, not
when three documents agree that it does. You need not re-run every suite to
resume — but a claim you could not confirm is a claim you carry forward
marked as such, not as a fact.

**What changed while nobody was looking:**

- **The questions log** — the user may have answered questions since the
  handoff was written, and an answer can unblock a phase the handoff calls
  blocked or reverse a decision it calls settled. Read every entry; the
  handoff was written before the answers. Some handoffs exist *for* this
  moment ("for the session that runs after the user answers Q5 and Q6").
- **The blockers.** A handoff that says "waits on another branch landing in
  `<main>`" was true on its date; check whether it landed. A blocker that has
  cleared moves work into scope; one that has not stays a blocker, however
  much the handoff's ordering would like it otherwise.
- **The pre-existing failures.** A handoff that names tests as red on the
  parent branch names them so you do not chase them. Confirm the list is still
  the list — run those tests on the parent, or check its most recent CI —
  before either chasing a red or dismissing one.
- **Private memory.** A handoff that cites a memory or note outside the repo
  is citing something this session may not have. The tree is the record. If
  the fact matters, it belongs in the handoff or a doc; inline it when you
  write the next handoff at the end.

Keep the result as a short table — claim, what the tree says, what you
propose to do about it. It is the first part of the proposal below.

**When there is no HANDOFF.md**, you are not resuming a handoff; you are
doing archaeology. Say so. Reconstruct the same table from `EXECUTION.md`,
the questions log, `git log` and the final doc — the executing skills already
know how to cross off committed work — and expect the traps to be
unrecorded. Write the handoff you wish you had received at the end of this
session.

## Survey the merge

The handoff's first action is usually **merge `<main>` before anything else
touches the tree**. Survey it now, without performing it — the
[merge-branch](../merge-branch/SKILL.md) gate's "before merging" half:

- `git log --oneline <branch>..<main>` and `git diff --stat <branch>...<main>`,
  then the hunks that touch the files this feature builds on. Say what
  `<main>` gained, which of it lands near this work, and where you expect
  conflicts.
- **Name the conflict rules the handoff recorded** and say you will apply
  them: "the published decision-record number wins, the newcomer moves";
  "expect append conflicts in the string tables and the docs index". These
  were paid for last time; a conflict resolved a different way this time is a
  second decision nobody made.
- Recommend the direction — `<main>` → branch, verified there, is the usual
  case for a long-lived branch — with your reasoning.

If the handoff's first action is something else — confirm a fact with a
provider before designing around it, delete a stray checkout, answer a
question — survey that instead, and do not skip to the phase list because the
phase list looks more like progress.

## Propose the scope

The handoff's "what to do next" section is its ordering; the user's argument
narrows or overrides it; the reconciliation adjusts both. Resolve as the
executing skill does — ids against the final doc's headings, forgivingly,
crossing off what is committed — with three rules the handoff adds:

- **Blocked stays blocked** until the reconciliation showed the blocker
  cleared. Do not start "just the part that does not need the answer" of a
  phase the handoff deferred for a reason; that is how a phase gets built
  twice.
- **Deliberately-not-done stays not done.** The handoff names intentional
  gaps so you extend the work instead of fixing them. A gap you fill anyway
  is a product decision taken in the user's absence.
- **Deprioritised means ask.** "Milestone P — do not start without asking" is
  not in scope however idle you become.

Write the scope as a list, in the order you would build it, and say what the
first increment would be and how it would be verified.

## Ask, then wait

**Now stop and put the proposal to the user.** This is the checkpoint the
whole intake has been building toward, and it comes before the first command
that changes the tree. In plain sentences, no shorthand from the handoff:

1. **What the handoff claimed and what the tree says** — the reconciliation
   table, with every contradiction and what you propose to do about each.
2. **The merge you would perform** — what is coming in, where you expect
   conflicts, which recorded rules you would apply, and the direction. Ask
   for permission to merge.
3. **The work you would then continue** — the resolved scope as a list, the
   first increment, and which executing skill you would run it under. Ask
   whether that is correct.
4. **Anything you need answered** — an open question that gates the first
   increment, a phase the handoff calls landed that the code does not
   support, a blocker you could not confirm either way.

Then **wait**. The user confirms, corrects the scope, or gives new
instructions — and each of those is a different session from here. Do not
merge on the strength of the handoff's instruction alone, and do not start
building "while they think about it": the handoff was written for a session
that would ask, and an unrequested merge on a branch nobody has pushed is the
most expensive mistake available to you. If the user said "keep going while I
sleep" in the invocation, that authorises the run *after* this answer, not
instead of it — ask anyway, and say you are waiting.

If the reconciliation found nothing owed, say that instead of proposing work,
and point at [close-plan](../close-plan/SKILL.md) or
[close-roadmap](../close-roadmap/SKILL.md).

## Merge, then continue under the executing skill

Once the user has confirmed:

- **Delete `HANDOFF.md`.** It was written for exactly this moment and it has
  been consumed: its claims are reconciled, its traps are in your working
  rules, its ordering has become the confirmed scope. Left in the tree it is
  the page the next reader trusts most, and it stopped being true the moment
  the direction changed. `git rm` it as its own small commit, or with the
  merge. If this session stops with work owed, you write a fresh one at the
  end — from this session's tree, not the last one's.
- **Merge through the [merge-branch](../merge-branch/SKILL.md) gate**, never
  mechanically — `<main>` → branch, resolve using the rules you named, verify
  there. Record in the questions log any resolution that chose between two
  behaviours rather than two texts.
- **Run the suite once on the merged tree** before building anything, so that
  every red you meet later is yours or is on the pre-existing list — not the
  merge's.
- **If the merge changed the scope** — a phase now conflicts with something
  `<main>` landed, a blocker cleared or appeared — say so briefly before
  starting. A small adjustment is reported; a different plan of work is asked
  again.

Now switch. A `PLAN.final.md` continues under
[execute-plan](../execute-plan/SKILL.md); a `ROADMAP.final.md` under
[execute-roadmap](../execute-roadmap/SKILL.md). Where the handoff has a "how
this roadmap expects to be worked" section, that is the executing skill's
contract restated by someone who ran it — follow it. Carry these into the
work:

- **The traps become standing instructions.** Every one the handoff names
  goes into your own working rules and into the brief of every sub-agent you
  spawn — the locked build output, the cleanup sequence that fails on one
  platform, the shell whose working directory persists, the agent that
  reports done without committing. A trap briefed once is a trap the
  sub-agent does not pay for either.
- **Decisions in the questions log are made.** Do not re-decide them because
  the reasoning is not in your head; the log records the alternative that
  lost so you can reopen one deliberately, with the user, rather than by
  accident.
- **The handoff's decisions taken in the user's absence** stay recorded as
  such. If one now looks wrong, that is a new question in the log, not a
  silent reversal.
- **A model or effort directive** from the argument applies as the executing
  skill says it applies.

From here the executing skill owns the run: one verified increment at a time,
one commit per increment, questions recorded rather than blocking, until the
confirmed scope is complete or everything not blocked is done.

## Finishing

The executing skill's finishing steps apply — `EXECUTION.md`,
`ACCEPTANCE.md`, a clean tree, a plain-language report. This skill adds the
handoff itself:

- **Write a fresh `HANDOFF.md`** following
  [write-handoff](../write-handoff/SKILL.md) if anything is still owed. The
  old one was deleted when the direction was agreed, so this one describes
  *this* session's tree: dated, naming this session's scope in the opening
  line, carrying forward only the traps that are still true — a trap for a
  conflict that will not recur is noise for the next reader — and adding the
  traps *you* hit. Inline any fact the old page borrowed from private memory.
- **Write none if the scope is complete.** A handoff for finished work is a
  fourth summary of the run that will be believed after it stops being right;
  `EXECUTION.md` describes finished work, and
  [close-plan](../close-plan/SKILL.md) or
  [close-roadmap](../close-roadmap/SKILL.md) retires the folder.
- **In the report to the user**, say in one paragraph what the handoff
  claimed that the tree contradicted, and what you did about each — that is
  the part of this session they could not have predicted from the previous
  one. Then what was built, in product language; the pointer to
  `ACCEPTANCE.md`; and the questions awaiting their decision.
