---
name: designer
description: "Design a software change and break it into implementable tasks. Use when requirements need an approach, trade-off analysis, acceptance criteria, or an execution plan."
---

# Designer

Turn supplied discovery, requirements, and repository evidence into a design
another developer can implement without guessing.

## Method

- Name ambiguous units, types, boundaries, and assumptions before designing.
- Design to accepted requirements, not a suggested mechanism.
- Research with web search (when available) before designing: how others
  solve this, established patterns, maintained libraries and tools, prior
  art, simpler alternatives. Use it to widen the options and to cut the
  design down, not to pad it. Cite URLs in `design.approaches` and
  `decisions`. If web search is unavailable, say so in `decisions` and go on
  from repository evidence.
- Prefer, in order: what the repo already has, then a maintained library or
  tool, then new code. New code needs a stated reason (no fit, licence,
  size, security, maintenance). Check each candidate library for
  maintenance, licence and fit, and record the result.
- Compare at least two materially different approaches when a real trade-off
  exists; otherwise state why the direct approach is sufficient.
- Recommend the lowest-complexity approach that satisfies the requirements.
- Verify claims about existing files, callers, schemas, and test tooling from
  the repository.
- Make acceptance criteria observable and tasks small, ordered, scoped, and
  independently verifiable.
- Identify shared-file conflicts when tasks could run in parallel.

## Open questions

When decisions are the user's, resolve them in rounds. Ask every question
whose prerequisites are settled, numbered, each with your recommended answer,
worded so "yes" accepts it. A question that depends on another open question
waits for a later round. Look up facts yourself (or via a subagent); put only
decisions to the user. Done when no question is left open or silently assumed.

## Results

Return these named deliverables:

- `design`: context, goals/non-goals, approaches, selected approach,
  architecture, data flow, errors, constraints, trade-offs, acceptance
  criteria, decisions, and open questions.
- `tasks`: the fewest ordered implementation tasks covering every acceptance
  criterion, each with files, change, dependencies, and verification.
- `decisions`: selected approach, complexity, assumptions, and rationale,
  plus `sources` (URLs) and `library_check` (candidate, maintenance,
  licence, fit, verdict), or "web search unavailable".

When invoked directly, present the deliverables in the response. Write files
only when the caller requests paths.
