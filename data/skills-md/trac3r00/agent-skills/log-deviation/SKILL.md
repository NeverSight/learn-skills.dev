---
name: log-deviation
description: Record a place where the code forced a deviation from the agreed plan. Use mid-implementation whenever reality contradicts the plan, or when the user says "log this deviation". The log feeds future planning and the merge quiz.
version: 1.0.0
author: Hien Dinh
license: MIT
---

# Deviation Log

The plan said one thing; the code demanded another. Record it while it's fresh —
these entries are the highest-value input to the next plan.

## Where the log lives

- In a git repo: `docs/deviations/YYYY-MM-DD-<task-slug>.md` at the repo root
  (create `docs/deviations/` if needed). `<task-slug>` = short kebab-case name
  of the current task. Slugs are minted freely, so two sessions will name the
  same task differently: before creating a new file, list what already exists
  in `docs/deviations/` and reuse the slug of any file that is plausibly this
  task — appending to it even if it's from an earlier day/session — rather than
  minting a near-duplicate.
- Outside a git repo: write to the session scratchpad instead and tell the user
  the path.

## Entry format (append, newest last)

```markdown
## <YYYY-MM-DD HH:MM> — <one-line summary>
- **Plan said:** <what the plan/spec assumed>
- **Code forced:** <what was actually done instead>
- **Why:** <the real-world constraint that made the plan wrong>
- **Ripple:** <other plan steps this invalidates, or "none">
```

The heading carries the full date: the file spans days by design, and `HH:MM`
alone goes ambiguous on the second session.

## Discovered drift

Not every deviation is caught live. When work reveals that plans or docs
already disagree with the shipped code (a stale roadmap item, a doc promising
a design the code abandoned), log it with the same fields plus one more:

```markdown
- **Found while:** <the current activity that surfaced it>
```

Date the heading with the *discovery* time; if the deviation's original date
is known, name it in **Code forced**.

## Rules

- One entry per deviation, logged at the moment it happens — not batched at the end.
- "Why" names the constraint (API limitation, hidden coupling, wrong assumption),
  never just "it didn't work".
- If invoked with no deviation to log, ask what deviated rather than inventing one.
- Do not commit the log automatically; leave staging to the user's normal flow.
