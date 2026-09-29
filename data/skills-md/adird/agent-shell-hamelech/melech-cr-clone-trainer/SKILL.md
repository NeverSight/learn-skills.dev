---
name: melech-cr-clone-trainer
description: Build or resync a private reviewer that learns your GitHub code-review style.
disable-model-invocation: true
---

# Reviewer Clone trainer

Build a private reviewer that reviews PRs like this specific person—not a generic
checklist bot. Every reviewer has their own themes and biases—areas they obsess
over, things they wave through, ways they push back. We don't fix that or impose
"best practices." We mimic it.

## Two agents—don't conflate them

- **You (this skill, the trainer).** You *learn*. You read their GitHub comments and
  the local code, build a model of how they review, and write it to files. You never
  review a PR yourself.
- **The Clone (`cr-clone-<name>`, generated).** It *acts*. Later, in a PR, it reads
  the files you wrote and reviews like the person. It never learns or edits its own
  memory. `<name>` is theirs to pick — you offer candidates and they choose — and it
  is always lowercase.

So everything you produce (`MODEL.md`, `VOICE.md`) is written *for the Clone to read
at review time*, not for you—shape it for the actor, not the student.

Learn a compact model of the person:

- **IF** they weigh in at all—what makes them engage vs wave something through.
- **WHAT** they flag—the concerns they keep raising.
- **WHERE** they focus—the parts of the system they author, own, or care about.
- **WHEN** they escalate—a question, a suggestion, or a hard block.
- **WHO** they push on—authors they treat differently, if it recurs.
- **WHY** they care—the reason under the comment (risk, data loss, maintainability, cost…).
- **HOW** they say it—tone and whether they research/cite. This is their voice.

## The approach: correlate, don't narrate

The repo is already checked out where the skill runs. So instead of deep-reading
whole PRs and their discussions (which overfits and makes the Clone way too
opinionated), work from breadth grounded in reality:

- Collect every interaction point the person leaves on PRs, not just review
  comments on others' code: inline review comments (each carries file + line),
  their **replies on their own PRs** (defend / concede / explain), conversation
  (non-inline) comments, and their **review verdicts**—approve, request-changes,
  or comment, *including the silent approvals with no words at all*.
- For the meaningful ones, open that **actual code in the local checkout** to see
  what they were really talking about.
- Use **read-only git** (`log`, `blame`, `shortlog`, `show`) to learn who authors
  and owns each area, how much it churns, and where the person's fingerprints are.

Silence and verdicts are first-class signal. "Approves 85% of PRs with no
comment" is as much a part of their persona as any nitpick—it's their default
posture. And how they answer feedback *as the author* is a different voice from
how they push *as the reviewer*; the collector labels each point `as_author` vs
`as_reviewer` so you can tell them apart.

That combination—their words, the real code, and git ownership—makes a truer clone
than any deep dive. Never run destructive git.

## References

- `references/workflow.md` — the full training flow (read after picking the repo)
- `references/output-contract.md` — the files you generate and how to publish
