---
name: tool-stewardship
description: How the toolkit is consulted, extended, and documented. Use before writing any new code — and after, when a genuinely new instrument has earned its place.
---

# tool-stewardship — consult first, write last, document always

A research program in which agents do much of the work accumulates capability only if someone makes it accumulate. Code gets written constantly; the question is whether the tenth problem starts where the ninth finished or starts from zero. Left to defaults it starts from zero: each session writes a script, solves its problem, and exits, and everything the script learned leaves with the context that held it. A shared toolkit converts that loss into compounding — but only under habits that do not happen on their own: consult before writing, improve in place rather than copy, document the day you build, retire what has been superseded. This file is those habits as procedure.

The economics are lopsided. Consulting an index costs minutes; rebuilding an instrument costs hours, and the rebuild is usually worse, because the existing tool embodies fixes for failures its author already hit and a fresh script embodies none. A tool that has survived many problems carries their corrections; new code carries only its author's foresight. The same asymmetry is why patching beats forking: a fork stops inheriting the moment it is copied, so every later correction to the original must be rediscovered in the fork, usually by getting a wrong answer first. And documentation is same-day work because the author is the only person who knows what the tool assumes, and only briefly. A page written a week later records the memory of an intention; a page written the day of the build records the fact of a behavior.

## Procedure

### Before writing any code

1. **Search the index by capability, not by name.** You are looking for "something that fits a rate to a time-stamped log," not for a title you half-remember. Read past the one-line summaries: a near-miss matters, because a near-miss plus a patch is the usual right answer.
2. **Read the candidate's page in full.** The page says when the tool applies and what test its output must pass. Skimming the page and then "verifying" by eyeballing one output is how the wrong tool gets trusted.
3. **Run it on a trivial case with a known answer** before running it on your problem. This costs a minute and catches both your misreading of the interface and any rot in the tool itself.
4. **Climb the decision ladder in order:** use as-is → patch or extend → wrap → write new. Writing new code obliges you to state, in one written sentence, which existing tools you checked and why each falls short. If you cannot write that sentence, you have not consulted; go back to step 1.

### When patching an existing tool

1. **Patch the upstream copy, in place.** Never a private copy in your working directory — the point is that the next user inherits the fix.
2. **Preserve the interface, or migrate every caller in the same change.** Search for the call sites first. A changed output format with an unmigrated caller produces wrong numbers that still parse (see the catalogue).
3. **Re-run the tool's known-answer tests, plus the case that motivated the patch.** Then add the motivating case to the tests — it is the one input class the tests demonstrably lacked.
4. **Log the change the same day**: date, what changed, why, and what a user of yesterday's version would see differently. The log lives where the next user will look, and the tool's page is updated whenever the meaning of the output moved. An undocumented upgrade is indistinguishable from a regression.

### When new code is justified

1. **Prove it on known answers before the real problem.** New code earns trust the way a new instrument does: by getting right the cases where right is checkable.
2. **Decide, honestly, whether it outlives the problem.** If yes: name it, move it into the toolkit tree rather than leaving it beside the run that spawned it, write the four-question page below, and add the index row — all the day it is built, because tomorrow you will be inside the next problem and the day after you will not remember the preconditions.
3. **If it is genuinely one-shot, say so in a comment at the top of the file**, so a later reader knows it was left unregistered on purpose. Be suspicious of that verdict, though: "one-shot" is usually a failure to imagine the next problem, and the catalogue below is full of one-shot scripts that got rebuilt monthly.

### The four-question page

Every tool's page answers four questions for a reader who has never seen the tool:

1. **What it does** — one plain paragraph.
2. **When to reach for it** — the symptom or task that should route here, and the neighboring tool that covers the adjacent case, so the reader can see the boundary.
3. **What its output means** — units, conventions, and what failure looks like as distinct from success. A tool whose failure output resembles its success output needs that fact stated in bold.
4. **What test its answer must pass before anyone believes it** — the known-answer case, the cross-check against an independent route, whatever the acceptance criterion is.

A tool missing any of the four is not finished, however well it runs. Example of a complete entry:

```
## ratefit — runtime projection from a partial log
Fits a rate to a job's own time-stamped log and projects completion.
When to reach for it: before extending any running job, or when
deciding whether a projected run fits a time budget. Not for jobs
whose per-item cost grows with the item index — no tool covers
those yet; measure directly.
Output: projected finish time plus a fit residual. A residual above
the printed threshold means the rate is unstable and the projection
is VOID, not merely approximate.
Believe it when: the projection from the first half of a finished
job's log matches that job's actual finish.
```

A reader of that block can decide whether to use the tool, use it, and distrust it correctly — without opening the source.

### Retiring duplicates

When two tools overlap, merge into the stronger one and port whatever cases only the weaker handled; the weaker tool's tests are the checklist for the port. Then delete the loser and leave a one-line pointer at its old name and its old index row ("superseded by X, date"), because habits and links keep pointing at dead names for months. Never leave both live "for safety" — every future reader then re-litigates the choice, and some choose wrong.

## Failure-mode catalogue

These are the classes the discipline exists to prevent. Each recurs wherever the procedure is skipped.

- **Parallel half-tools.** Two sessions each need most of the same instrument and each writes its own; each handles the failure cases its own problem hit, and neither inherits the other's. Result: two tools, each incomplete in a different way, with disjoint bugs — and every later user must discover which crash they are going to get.
- **The vanishing script.** A script solves the problem and stays, unnamed, in the run directory. A month later the same problem is solved again from scratch, slightly differently, with a fresh set of bugs, and the second author never learns the first version existed.
- **The drifting fork.** A copy taken "just to change one flag" stops inheriting; upstream later fixes a correctness bug; the fork keeps the bug and returns silently different answers, discovered only when the two are compared by accident.
- **The unregistered capability.** Built, tested, even documented in its own directory — but no index row. Searching agents conclude the capability does not exist and rebuild it. The entire loss traces to one missing line.
- **The author-facing page.** The documentation explains how the tool works inside and says nothing about when to reach for it or what the output means. The next agent reads the page and still cannot decide, so they write their own.
- **The unlogged upgrade.** Behavior changed; nothing was recorded. The next user's results shift with no way to tell fix from regression, so the tool — rather than the change — loses their trust.
- **Silent-caller breakage.** A patch changes the output format; an unmigrated caller parses the old format and receives values that still parse. Nothing crashes. The wrong numbers travel.
- **The shadow fork.** A modified copy quietly becomes the version everyone actually runs while the index still points at the original. Every property documented about the tool is now a property of the wrong file.
- **Documentation from memory.** The page gets written a week after the tool, reconstructing intent. The one precondition that mattered — the input convention, the case the tool must never be fed — is exactly what the author no longer remembers.
- **The undead duplicate.** A tool superseded by a better one is never retired. Someone finds it in the index, uses it, and gets the answer the replacement was built to correct.

## Checklist

Before writing code:

- [ ] Index searched by capability; the nearest tool's page read in full.
- [ ] One sentence written stating why no existing tool, or a patch to one, covers the need — or the ladder stopped before "write new."

Before the session ends, for any tool created or changed:

- [ ] Change logged, dated, with what a user of the old version would see differently.
- [ ] Four-question page written or updated — does the stated meaning of the output still match?
- [ ] Index row added or updated.
- [ ] Known-answer test exists and passed; the motivating case added to the tests.
- [ ] Every caller of a changed interface migrated.
- [ ] Overlapping tools merged; superseded names carry pointers.
- [ ] Nothing capability-bearing left behind in the working directory.
