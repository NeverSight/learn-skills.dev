---
name: write-acceptance
description: Write docs/<feature>/ACCEPTANCE.md — the ordered checklist a person works through by hand to deploy, test and accept finished work, because a machine could not do it. Use at the end of every implementing skill (execute-plan, execute-roadmap, build-feature), or when the user invokes /write-acceptance <feature> or asks for a test plan, an acceptance checklist, or "tell me how to verify this". Covers only what could not be automated — consoles and accounts, physical devices, GUI surfaces, two-machine and multi-user cases — with copy-pasteable commands, the exact observable that counts as evidence, and what you expect back. The reader may be the user or a tester who has never seen the feature. For handing unfinished work to the next agent, use write-handoff instead.
---

# Hand the work to a person to accept

You have finished building something and a person has to see it work before
it is real. They come to this with none of the session in their head: not
what you decided, not what you already checked, not which of the five buttons
on that screen is the new one.

`docs/<feature>/ACCEPTANCE.md` (in the project's planning folder, unless it
uses another) is the page that closes that gap. It is **an ordered checklist
of what is expected of them**, and nothing else. You are judged on whether
they can work top to bottom without asking you a single question, and on
whether every step ends in an observable they can actually check.

**Know who is reading.** Usually the user, who knows the product but not this
week's work. Sometimes a tester who has never seen the feature and cannot be
assumed to know where anything lives. Write for the second: name the screen,
the menu and the button, not "the usual place". A step the user could guess
is a step the tester reports back as blocked.

**This is not [write-handoff](../write-handoff/SKILL.md).** That one hands
*unfinished* work to the next agent — branch state, what to merge, where to
pick up. This one hands *finished* work to a human to accept. A run can need
both, and they share nothing: different reader, different question.

## What goes in it — and what never does

**Only what a machine could not do.** That is the whole filter, and it is the
difference between a checklist someone runs and one they skim and abandon:

- Consoles and accounts you have no credentials for — a hosting dashboard,
  DNS, an app store, a repository secret.
- **Physical or multi-device cases** — two machines on different networks, a
  phone on a hotspot, a second user, a reboot.
- **What only a human eye settles** — does the new UI look right beside its
  neighbours, does the animation feel laggy, is the wording right.
- **Anything you could not run here** — a platform you cannot build for, a
  suite that needs hardware, an asset that is not installed. Say so plainly
  and say what it would prove.
- **The one demonstration that proves the feature exists at all**, even if
  you verified it in a test — they want to see the thing work once.

**Never ask for what you already did.** The test suite, the formatter,
anything green in `EXECUTION.md` — those are your job and they are done.
Repeating them here buries the three steps that actually need a person. If
something failed, that is not an acceptance step either; it is a defect you
fix or a deferral you record in the questions log (wherever the project keeps
open questions; if it has no convention, a questions section or file beside
the plan).

## How to write it

Open by saying what is already built and verified, with a pointer to
`EXECUTION.md`, then what remains and **why it needs a person** (a console, a
second device, their eyes). Then the checklist.

- **Group into ordered sections they can stop between**, each with a rough
  time cost — `## A. Provision (console work, ~30 min plus DNS propagation)`.
  Someone with twenty minutes should be able to see what fits.
- **Every command is copy-pasteable, and says where it runs** — which
  machine, which console, which shell. Fenced blocks, real values not
  placeholders, except the ones only they can supply (say what those are and
  where to get them).
- **State the observable that counts as evidence**, not the vibe. "Sync
  completing is not the evidence; the relay path is." "`systemctl is-enabled
  docker` must print: `enabled`." A step whose success criterion is "it
  should work" cannot be reported back.
- **Name what will look broken but is not.** A gate that fails closed, a
  deliberate absence of a recovery email, a first run that takes ten minutes
  — say "that is designed, not broken" where they will hit it, not in a
  footnote.
- **Point at the runbook for the detailed how** rather than restating it.
  This page is the ordered list of what is expected; the operations doc or
  the user guide is the how. Two copies of a procedure drift.
- **Say what you want back**: which steps to report on, which files to
  commit, which open questions you are waiting on. Be explicit that the open
  questions do not block the checklist, when they do not.
- **Write for someone who just woke up.** Plain sentences, product language,
  no phase ids or shorthand from the run. Where a step exists because of a
  decision you took while they were away, say so in one clause.

Keep it as short as honesty allows. If the work genuinely needed nothing
beyond a look, the file says that in three lines and points at the one thing
to open — an invented ceremony is worse than a short page.

## The acceptance section

End with the numbered checks — **the user's own use cases from the plan**,
restated as things to do rather than things to assert. Each one names: what
to set up, what to do, and the exact observable that closes it. These are
what let the work be called done, so they are the last thing on the page and
they are numbered, so the reader can answer "D.2 passed, D.3 showed X".

If a later round of work adds acceptance on top of an earlier one, append a
new section rather than rewriting the old — they may have already worked
through it.

## Where it sits

- Write it to `docs/<feature>/ACCEPTANCE.md` and commit it with the last
  phase.
- **Link it from `EXECUTION.md`** ("remaining acceptance is the checklist in
  ACCEPTANCE.md") and from your closing report, which stays a summary — the
  checklist lives here, not in a chat message that scrolls away.
- Update it in place when a later run adds or closes steps.
  [close-roadmap](../close-roadmap/SKILL.md) and
  [close-plan](../close-plan/SKILL.md) review it check by check before
  anything is called landed, then retire it — carrying anything still worth
  re-running into the feature's live test plan. **A check nobody reported
  back on blocks the closure**, so keep the list short enough to be worked
  through.
