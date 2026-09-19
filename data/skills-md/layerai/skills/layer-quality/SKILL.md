---
name: layer-quality
description: "Use when judging Layer output before it ships: scoring generated files against a workspace's output scoring rules, reading back verdicts on a file, reviewing a batch against the brief, or choosing which candidate to deliver. Also when a studio has automated quality standards, or a set must be checked for consistency before handoff. Keywords: quality gate, scoring, review, batch, verdict, approve, QA, consistency check."
license: MIT
---

# Layer Quality Review

## Overview

Generation is not delivery. A batch comes back, and something has to decide which of it is usable,
against the brief and against whatever standards the studio has already set. Layer records those
standards as output scoring rules, and exposes three tools:

| Tool                        | Purpose                                                  |
| --------------------------- | -------------------------------------------------------- |
| `list_output_scoring_rules` | The rules in force for a workspace, optionally a project |
| `score_files`               | Queue a scoring run. Asynchronous and billed             |
| `get_file_scores`           | Read the verdicts recorded on one file                   |

Generation mechanics are in the `layer` skill. If a sibling skill named here is missing from your
available skills, ask the user to install it (`npx skills add layerai/skills --skill <name>`);
unattended, proceed from tool schemas and flag the gap.

## Check for rules before inventing standards

Call `list_output_scoring_rules` before judging anything by eye. Each rule is a standard the studio
has written down, and a delivery that contradicts one is wrong however good it looks. Rules can be
scoped to a project as well as a workspace, so pass the project when the work belongs to one.

When rules exist, `score_files` queues the batch and `get_file_scores` reads the verdicts back.

Three things about that contract are easy to get wrong and expensive to get wrong:

- **`score_files` is asynchronous.** It returns as soon as the run is queued, not with results. Poll
  `get_file_scores` afterwards; a large request takes a few minutes.
- **An empty `scores` list means not judged yet, not a zero.** Treating the queue acknowledgement as
  a verdict, or an empty list as a failing score, is the defect this contract invites.
- **It is billed, and there is no estimate tool for it.** Every file and rule pair is a vision-model
  call that spends Creative Units, and none of the `estimate_*` tools price it. Scoring the same file
  again is allowed and appends a fresh verdict rather than replacing the old one, so a re-score
  because the first call "returned nothing" is a real double spend. Read `get_file_scores` first.

When no rules exist, say so rather than implying the output passed a gate it never met, then review
against the brief.

## Review against the brief, not against taste

The question is never "is this good". It is "does this do what was asked". Work back through the
brief item by item:

- The **stated constraints**: aspect ratio, pixel size, transparent background, palette, poly budget,
  clip length. These are pass or fail, and they are the ones most often silently missed because the
  image looks fine.
- The **intended use**: an icon judged at its target size, a texture judged tiled at 3x3, a loop
  judged across its seam, a background judged with a character on it. Judging an asset out of its
  context is how defects reach delivery.
- The **set**, not the item. For anything that belongs to a group, lay the candidates out together.
  Drift between siblings is invisible one at a time and obvious side by side.

## Choosing from a batch

`batch_size` returns variations, and the temptation is to pick the most striking one. Pick the one
closest to the brief instead, because the striking one is usually striking for a reason that will not
repeat across the rest of the set.

When no candidate is close, the fix is the prompt, not another batch. Two identical rerolls in a row
mean the prompt is underspecified: go back to what the prompt failed to name (framing, lighting,
background treatment) rather than spending again on the same string.

## Report honestly

Say what is wrong with what you deliver. A run that produced three usable assets and one with a
mangled hand is reported as exactly that, not as four assets. Where a reference set was degraded,
name it (`layer-reference-sets`). Where a constraint was missed, name the constraint.

Creative Units were spent either way, so a quiet pass costs the user a second discovery later, on
work already built on the flawed asset.

## Worked example

"Are these eight icons ready to ship?"

1. `list_output_scoring_rules` for the workspace and the project. Two rules exist: transparent
   background, and a minimum legibility standard.
2. `get_file_scores` on the eight `file_id` values first, in case an earlier session already judged
   them. For the ones with no scores, `score_files` to queue a run, telling the user it spends
   Creative Units since no estimate tool prices scoring.
3. Poll `get_file_scores` until scores appear. An empty list means not yet judged, so keep polling
   rather than re-scoring.
4. Two fail the transparency rule. Those are not judgement calls, so they go back through
   `background_removal` (`layer-image-editing`).
5. View the remaining six together at their target size, not at full resolution, and check stroke
   weight and palette against the two icons approved earlier.
6. One has drifted heavier than the set. Reroll that one against the approved icons as references.
7. Deliver with the state named: six passing, one rerolled, two fixed for transparency.

## Common mistakes

- Judging by eye without checking whether scoring rules exist.
- Reporting output as passing a gate when no rules were ever in force.
- Reading `score_files` as if it returned verdicts, when it only acknowledges the queued run.
- Reading an empty `scores` list as a zero rather than as not yet judged.
- Re-scoring because the first call "returned nothing", which spends again and appends a second
  verdict.
- Re-scoring files whose verdicts `get_file_scores` already holds.
- Judging an icon, texture, or loop outside the context it ships in.
- Reviewing set members one at a time, so drift goes unnoticed.
- Picking the most striking candidate rather than the one matching the brief.
- Rerolling an underspecified prompt a third time instead of fixing it.
- Delivering silently around a known defect.
