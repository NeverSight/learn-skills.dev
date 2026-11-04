---
name: spec-review
description: Cold review of a diff against its ticket or contract, each finding quoting the requirement. Use when asked whether a branch, PR or local changes do what the ticket asked, or when another skill dispatches a spec review.
---

# Spec review

Review the diff you were handed against its contract and linked tickets. When you compute the diff yourself, run `git fetch origin <base>` and diff against `origin/<base>`: a local base branch can lag the remote and pull unrelated commits in. With no ticket, contract or spec available, report that in one line and stop.

Fidelity to the requirements is your only axis; bugs, style and complexity belong to the other reviews. Report three kinds of finding:

- **Missing:** a requirement that is absent or only partly implemented.
- **Unrequested:** behavior in the diff that no requirement asks for.
- **Wrong:** a requirement that looks implemented, but in a way that contradicts its wording.

For each finding:

- `file:line`, or the requirement's location when nothing in the diff covers it
- the quoted requirement
- what the diff does instead, in one or two sentences

Mark every finding that depends on reading an ambiguous requirement, and give the reading you used. If the diff meets every requirement, say so in one line.

Completion: every requirement in the contract and tickets checked against the diff, every changed hunk traced to a requirement or reported as unrequested, every finding carrying all three parts, under 400 words.
