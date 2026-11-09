---
name: diagnose-bug
description: Finds the cause of an everyday bug and proves it before anyone fixes it. Questions the ticket first, pins down what fails and how often, ranks the suspects with "not a bug" always among them, checks the cheapest first, reproduces the bug with a control, proves the smallest fix in that repro, and has a fresh helper try to break the answer. Ends with a short diagnosis and a fix plan for the user to approve. Never changes a checkout anyone works in. Use for a bug ticket, a Sentry issue or an error to explain, or for "diagnose this", "why does this happen", "find the root cause" or "is this a bug". Hard bugs and questions about a number go to orb's Research world.
---

# Diagnose a bug

Tickets often blame the wrong thing, and the first cause that fits is often not the real one. You find the cause and prove it with a run, not an argument. This is Research's bug method for one agent in one sitting. You're done when the user could run your repro by hand, see it fail, and see it pass with your fix.

## Input

- **The bug:** a ticket, a Sentry link, an error or the user's words. Open it with whatever tool reads it. One you can't read becomes a question.
- **The repo,** or repos, the bug lives in.

## Notes

Keep everything in `.plans/<bug>/` in the repo, which git ignores: `diagnosis.md`, the repro in `repro/`, and the fix as `fix.patch`. Write `diagnosis.md` as you go, so a fresh session can pick it up. Mark every fact by how you know it: **seen** (you ran or queried it), **read in code** (file:line), **documented**, **told** (by the user or the ticket) or **guessed**.

## 1. Is it a bug?

- **Pin it down:** the exact error or wrong result, how often out of how many, where, and since when.
- **Find what changed around the start:** the git log of the code involved, deploys and config changes.
- **List what the ticket takes for granted,** like "it used to work", "only buyers from X" or "the button is broken". Check the cheapest first. A wrong one can end the job: say so and stop.

## 2. Suspects

- **Write two or more causes, most likely first.** Each is a code path with file:line, traced from where the input comes in to where it goes wrong, plus the check that would rule it out.
- **"Not a bug" is always on the list:** by design, bad data from somewhere else, or a wrong measurement.
- **Look for the same code copied elsewhere.** It has the same bug.

## 3. Check the cheapest first

1. Read the code.
2. Read its git history: log and blame of the lines involved. Was a fix tried and reverted, and why?
3. Pull read-only data: logs, Sentry, staging, or a database you already have access to.
4. Build a repro.

Stop once a check decides between suspects. Rule a suspect out only on evidence, and write down what ruled it out.

## 4. Repro with a control

- **Make the bug happen on purpose:** a failing test where one fits, else a script or a staging request.
- **It counts only with a control.** On the same setup, it fails with the suspect's mechanism and passes without it.
- **Write down how the repro differs from production:** version, data size, config, load. A result that rests on one of these holds only if that difference doesn't matter.
- **Couldn't reproduce it?** Say what would make it reproducible. Don't guess a fix.

## 5. Prove the fix

- **Fix where the bad state starts,** not with a guard where it shows up. Pick the smallest such fix.
- **It counts only if the repro passes with it and fails without it.**
- **Check git history for the same fix,** tried before and reverted.
- **Run the tests around the code you touched.**

## 6. A fresh helper attacks it

Start one helper agent with the notes and the repro. Its job is to break your answer: find another cause that explains the same facts, check that the repro shows the real error, check each count's denominator, and check that the fix removes the cause instead of hiding it. If it breaks your answer, go back to step 2 once. If the second answer breaks too, report what's still open.

## Asking the user

- **Ask once, in one numbered batch,** then keep checking whatever doesn't need the answers. Wait only when nothing else is left.
- **Ask for data, not only answers:** an export, a screenshot with its filters and time window visible, or access to a table. Say exactly what, which suspects it decides between, and where you think it lives. Pulling data by hand is normal.

## Too big for this

Stop and say it needs Research when the cheap checks and one repro attempt don't prove a cause, when the question is about a rate or a number rather than a wrong result, or when it needs a load test or a simulation. Leave `diagnosis.md` complete, so the user can start a Research colony with it as input.

## Never

- Write to production, push, or reply on tickets or in chat.
- Change a checkout anyone works in. Try repros and fixes in a throwaway git worktree, keep the repro and `fix.patch` in the notes, then remove the worktree.
- Open `.env`, or print a token.

## Output

Five bullets:

- **What happened,** in plain words.
- **Why,** with file:line.
- **How often and how bad,** with the denominator.
- **How to see it yourself:** the exact command or steps, which fail today.
- **The fix,** and that the repro passes with it.

Then the other suspects, each with what ruled it out, and anything still open. If it isn't a bug, say what it is and stop there.

Otherwise end with a fix plan for the user to approve, in forge's shape: Problem, Solution, Acceptance criteria (one is that the repro passes), and a table of test cases. Once they approve, approve-plan takes it to a PR. In orb, add a plate item with `orb plate add "Approve the fix for <bug>" --verb approve`. As a colonist, report to your chief instead.
