---
name: agent-harness-evolve
description: >
  Harness evolution skill. Collects and generalizes feedback on a
  running harness's results, reflects it back into agents/skills/the
  orchestrator, and updates the change log by capturing the delta
  against the harness's original configuration. Always use this skill
  for improvement requests grounded in an existing harness's track
  record — "retrospect on the harness", "evolve the harness",
  "incorporate this feedback into the harness", "improve the harness",
  "the results were disappointing, fix the harness", "apply this
  feedback to the harness", "summarize harness lessons learned".
  Building a new harness, redesigning its structure, or adding agents is
  the `agent-harness` skill's job, not this one.
---

# Agent Harness Evolve — the harness evolution mechanism

A harness isn't a fixed artifact; it's a system that evolves. This skill
captures the delta between "what worked and what didn't" and feeds it
back into the harness, so the next run is measurably better.

```
initial harness ──▶ used on a real project ──▶ current harness
                                        │
                                        ▼ (evolve captures the delta)
                                  generalize feedback → reflect into agents/skills/orchestrator
                                        │
                                        ▼
                                  update change log → next run starts from a better draft
```

## Workflow

### Phase 1: collect the delta

1. Read this project's agent directory, skill directory, and top-level
   agent-instructions file (whichever ones this harness actually uses —
   see `agent-harness`'s Core principles 1 and 4 for how those were
   determined; don't assume `AGENTS.md`/`CLAUDE.md` if the change log
   says otherwise), with its change-log table.
2. If this is a git repository, look at the change history of the
   harness's files (e.g. `git log --oneline -- <agent-dir> <skill-dir>
   <top-level-instructions-file>`) to see what changed, when, and why
   relative to the original setup.
3. If `_workspace/` exists, skim recent runs' intermediate output for
   actual evidence of execution:
   - Does output actually exist at the path the orchestrator defined?
     (if not, the checklist/workflow was bypassed, or that path is dead
     code)
   - Does the output's quality follow the format/criteria the skill
     specifies?
4. Ask the user for feedback (skip if they already gave it):
   - "Is there anything about the result you'd like improved?"
   - "Is there anything about the agent composition or the workflow
     you'd like changed?"
   - Don't press if there's no feedback — but do proactively suggest
     improvements when the observation-based signals below are present.

**Observation-based evolution signals (suggest improvements even
without explicit feedback):**
- Evidence that the same kind of fix request has come up 2+ times
- A pattern of an agent repeatedly failing/retrying
- Evidence the user bypassed the orchestrator and did the work manually
  (suspect the orchestrator's trigger condition failed to fire — a
  candidate for expanding `description`)
- Leftover references in the orchestrator to one proprietary tool's
  multi-agent API that don't belong in a portable harness — point to
  "Porting an existing tool-specific harness" in `agent-harness`'s
  `references/execution-modes.md`

### Phase 2: classify feedback type and map it to what needs fixing

| Feedback type | What to fix | Example |
| --- | --- | --- |
| Output quality | The relevant agent's skill | "the analysis was too shallow" → add a depth standard to the skill |
| Agent role | The agent definition file | "we also need a security review" → point to `agent-harness` to add an agent |
| Workflow order | The orchestrator skill | "verification should come first" → reorder stages |
| Team composition | Orchestrator + agents | "these two could be merged" → merge agents |
| Missing trigger | The skill's `description` | "it didn't fire when I phrased it this way" → expand `description` |
| Wrong execution primitive | The orchestrator | "it's the same slow fan-out every time" → switch execution primitive |
| Scale/cost | The orchestrator | "it's burning too many tokens" → shrink default scale, add budget awareness |

**Scope check:** if the fix needs a brand-new agent, removing one, or an
architectural redesign, don't do it in this skill — point to
`agent-harness` (its step 0 extending-an-existing-harness procedure)
instead. This skill focuses on **adjusting what already exists.**

### Phase 3: generalize and apply

1. **Generalize the feedback** — a narrow fix that only matches one
   instance is overfitting. For "the intro in this report was too
   long," don't write "keep intros under 10% of the total" — find *why*
   it ran long (the skill had no guidance on how to allocate length) and
   fix it at that level of principle.
2. **Record the why alongside the change** — every revised instruction
   should note its reason. Knowing the reason lets the agent judge
   correctly in edge cases too.
3. Apply changes one at a time, and run Phase 4 immediately after each one.
4. **Guard against regressions:** if a change would reverse an earlier
   change in the log, surface the conflict to the user and get
   confirmation (if a past change shortened something for being "too
   long" and this one says "too short," the right fix is a standard that
   satisfies both).
5. **Keep each file's existing language** — write whatever you add to
   an agent, skill, orchestrator, or top-level instructions file in the
   language already used in that file. Don't mix in a different
   language just because this skill document happens to be written in
   one.

### Phase 4: update the change log and verify

1. Record it in the top-level agent-instructions file's **change-log** table:

```markdown
**Change log:**
| Date | Change | Target | Reason |
| --- | --- | --- | --- |
| 2026-07-19 | Added a tone guide | skills/content-creator | Feedback: "too stiff" |
```

2. Verify the structure of whatever file you changed (frontmatter,
   reference consistency).
3. If you changed a `description`, verify triggers (3+ should-trigger
   and 3+ near-miss cases).
4. Do a final check that the top-level file matches the actual files.

### Phase 5: report the evolution

Report to the user:
- A summary of the captured delta (original setup → current state)
- What was changed this round, and the generalized reasoning behind it
- Any feedback deliberately not applied, and why
- What improvement to expect in the next run

## Principles

- **The delta is an asset** — the more the change log accumulates, the
  closer to "launch-ready" the next harness in the same domain starts
  out. Don't delete history.
- **No change without generalization** — adding one rule per instance
  turns a skill into a pile of rules. Compress feedback into a
  principle.
- **One change at a time** — batching several changes together makes it
  impossible to tell which change actually had the effect.

## Attribution

This skill is a derivative work of the `evolve` skill in
[revfactory/harness](https://github.com/revfactory/harness), licensed
under the Apache License, Version 2.0. See `LICENSE` and `NOTICE` in
this directory for the full license text and a summary of what was
changed.
