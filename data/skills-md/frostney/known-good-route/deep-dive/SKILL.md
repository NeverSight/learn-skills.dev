---
name: deep-dive
description: >-
  Establishes the actual cause of something observed by checking what really
  ran or loaded, trying to break each candidate explanation, and having the
  result reviewed in a fresh context before reporting it. Use before claiming a
  cause or proposing a fix for an observed failure, hang, leak, or unexpected
  agent behavior, when asked why something happened or what is causing it, or
  when the user runs /deep-dive. Inside an authorized development, delivery or
  fix loop, a failing check whose own output or trace already shows an uncontested
  in-scope cause is fixed in that loop instead, unless the user ran /deep-dive.
license: Unlicense OR MIT
metadata:
  agents-role: ambient
  agents-text: Before claiming the cause of something observed, check what actually ran, try to break each explanation, and cite a fresh review's verdict; skip that only when the failing output or trace already shows the mechanism, or the observation is itself the defect, such as a required control a view never renders, and treat a symptom whose cause sits in another step or file as a cause to establish.
---

# Deep dive

The person should not have to ask you to check what actually happened. Before
you name a cause or propose a fix for something observed, establish the cause
from the record of what ran, try to break it, and have it reviewed in a fresh
context.

An explicit `/deep-dive` always runs the full procedure below. Otherwise, a
check that fails inside an authorized development, delivery or fix loop needs no
deep dive only when the failing run's own output or trace already shows the
in-scope mechanism that produced the failure, not only the failed assertion or
the defect it names, and nothing contradicts it. State that cause and its
evidence, fix it in the loop, and rerun; the rerun confirms the fix, not the
cause. If you had to read source, files or history beyond the failing output
to find the cause, or set aside a conflicting claim, such as a note blaming
another component, you did a deep dive: get its fresh review before the fix.
When the observation is itself the defect, such as a required control a view
never renders, there is no cause to claim: fix it and verify it against the
requirement. A symptom whose cause sits in another step or file, such as a
total that is wrong because an earlier step rounded it, is a cause to
establish. A failure the evidence does not explain, or a fix the rerun does not
confirm, also returns to this procedure.

## Look at what actually ran

Start from the record, not the story about it. Depending on the problem, that
is the session transcript and the instructions and skills it actually loaded,
logs, CI runs and the revisions they ran on, process and lock state, and the
deployed version. A process name, a status message, a teammate's note, a PR
description, or a file that should have been loaded is a lead until the record
confirms it. So is what the person told you: confirm it in the record and cite
the record. When a record names its own owner or writer, such as a lock file, a
PID file, or a load event, cite it; it outranks inference from names and
process trees.

Do not stop at the first explanation that fits. Raise every candidate the
evidence suggests. A cause says why it happened, not only what happened: for
each confirmed link, ask what produced or allowed it, such as an instruction,
an input, or a check that never ran, and follow that back while the evidence
reaches. When the outcome broke a constraint, find where that constraint should
have been stated or checked and was not, such as a brief that never said it,
and name each fact it left out.
There is no fixed number of candidates.

Use read-only probes. Diagnosis does not authorize killing processes, releasing
locks, editing, rewriting history, or publishing.

## Try to break every candidate

Run two probes on each candidate explanation and keep both results:

- **Falsification:** look for the observation that would be impossible if the
  candidate were true, such as an ordering, a timestamp, a load event, an
  identical hash, or a probe that tells two candidates apart, and check it.
- **Truthiness:** reread each source you cite and confirm it says what you
  claim, about the object and time you claim. A source that only repeats
  someone's belief is a lead, not evidence.

Put the times from every source on one timeline: when each candidate started,
when the record last changed, when the symptom began. An order a candidate
cannot fit rules it out; report the times that decided it.

A candidate that fails falsification is ruled out by the observation that broke
it. A failed truthiness probe breaks the citation, not the candidate: correct or
drop the citation, and keep the candidate open until other evidence fits or
breaks it.

## Get a fresh review

Before returning, have the result reviewed in a fresh agent context: a subagent
when the host has one, otherwise a separate CLI run such as `claude -p` or
`codex exec`. Use the reviewer the caller names. Read
[references/fresh-review.md](references/fresh-review.md) before starting it.

The reviewer gets the symptom, the surviving explanation or the gap, where each
piece of evidence lives, and each ruled-out candidate with what ruled it out.
It reads the sources itself, tries to break the explanation, and returns agree
or disagree with its evidence. A disagreement that holds reopens the
investigation.

A review counts only when the reviewer ran and wrote its verdict to a file
that you cite by its exact path. Read that file and report the verdict it
holds. Before starting it, look through your tools
for one that runs a worker, subagent, or command and returns its output, and
use that. Recording a request, or waiting when no reviewer was started, is not
a review. A read-only boundary on the investigation does not forbid a read-only
reviewer; starting one changes nothing. When a route returns no verdict file,
try the next one. Without a verdict file to cite, the result is unreviewed,
whatever else happened.

When you are the reviewer, do not start another review. Read the named sources
yourself, write your verdict and its evidence once, through the verdict tool
your host gives you or to a file when it has none, and return that path. A
tool that only records a request to write did not write the file; the write
counts when it returns the path. Do not also record or copy it anywhere else. That one write is part of the review,
not a change to what is under investigation.

## Stop

Stop only when one of these holds:

- One explanation survives both probes and the fresh review, and every other
  candidate you raised is ruled out with evidence.
- The evidence runs out. Report what is missing, where you looked, and which
  candidates remain open, without choosing between them.

## Report

Keep it short. When the deep dive ran inside a larger task, such as a delivery,
its report still goes in the final message, including the verdict file's exact
path:

- the surviving explanation as a cause, back to its earliest supported link,
  or the gap;
- the evidence, each item with its source and the value that decides between
  candidates, such as a timestamp, exit code, hash, load event, or setting;
- each fact the person stated that the explanation relies on, with the record
  that confirmed or contradicted it;
- each ruled-out candidate, including the first explanation that seemed to fit
  and any the person or a document offered, with the observation that ruled it
  out;
- the falsification and truthiness results for each candidate, with the
  observation each rests on;
- which reviewer ran, by route and model, its verdict, and the exact path of
  its verdict file, or that the result is unreviewed.

Propose a fix only after this, and only for the surviving cause.
