---
name: video-qa
description: "Review AI-generated clips like a QC department: per-shot checklists, frame evidence, continuity across joins, and honest verdicts. Use when deciding whether a clip ships, gets fixed, or gets cut."
---

# Video QA

Every AI clip gets reviewed before it ships. Not watched, but reviewed: against
its brief, frame by frame where it matters, with a written verdict. The
review is short, but it's written down, because "looked fine" is how bad
shots survive into the final cut.

## The workflow

1. **Check against the brief.** The shot-brief is the spec
   (`references/qa-checklist.md`). The clip either does its story job or it
   doesn't. Everything else is secondary. Name failures from the taxonomy
   (`references/failure-taxonomy.md`) so each defect maps to its fix.
2. **Pull frame evidence.** Contact sheets at clip boundaries and key beats
   (`references/frame-evidence.md`, `scripts/contact_sheet.py`). For volume,
   run the embedding triage first (`references/automated-identity-qa.md`,
   `scripts/identity_score.py`). Humans review the failures plus a sample
   of passes. Eyes miss drift that stills catch.
3. **Check the joins.** Continuity across every cut
   (`references/continuity.md`): geography, light, wardrobe, screen
   direction.
4. **Write the verdict.** Ship, fix (with the one variable to change), or
   cut. No fourth option, no "maybe it'll work in the edit."

## Rules that don't bend

- **The brief is the spec.** "It's a nice clip" is not a pass. Does it do
  what the shot list row says? That's the only question.
- **Check the tails.** AI clips degrade toward their ends. The last two
  seconds get the hardest look, not the first two.
- **One variable per fix.** A failed clip goes back with exactly one slot
  changed. Two failures with two different changes teach you nothing.
- **Two strikes, then replan.** If a clip fails twice, the problem is the
  shot, not the prompt: simplify it, shorten it, switch to image-to-video,
  or cut it.
- **Write it down.** Clip ID, verdict, what was wrong, what changed. This log
  becomes your project's failure-mode list. The most valuable document you
  own by the end.
