---
name: rm-brief
license: MIT
description: Rebuild a developer's or operator's project context from current evidence after a gap or handoff. Use for status re-entry and pending decisions; do not turn ordinary progress updates into a full project history or start implementation.
---

# Project briefing

Give the reader enough current context to make the next decision. Report outcomes and their evidence, not a transcript of the agent's activity.

## Inputs

- Required: project or run scope and accessible current evidence.
- Optional: last known commit, run identifier, timestamp, last user decision, audience, and requested length.
- Default: a concise read-only briefing. If no reliable baseline exists, report a current snapshot rather than inventing a change history.

## Procedure

1. Read relevant current sources: repository instructions, status and diffs, recent commits, run state, validation results, and maintained project notes. Conversation memory can locate evidence but cannot establish current completion alone.
2. Verify the baseline when supplied. A file modification time is not proof of a completed change, and a commit timestamp does not establish when the user last understood the project.
3. Separate verified outcomes, pending work, blocked checks, and unresolved decisions. Distinguish local verification from deployment, authenticated checks, and external state. A passing run at a revision establishes that run's result, not coverage of every change in that revision. A recorded blocker does not establish that it is the only blocker. Reconcile contradictory sources or identify the conflict.
4. Lead with decisions or inputs the reader actually needs to provide. Then explain relevant changes since the baseline, or current state if the baseline is unknown. Include the next useful action supported by the evidence.
5. Explain unfamiliar project terms where needed, and adapt to the stated audience.

## Rules

- **Anchor first, then exclude what is already known.** Establish the reader's last touch — a revision, a dated observation, or a prior report. Everything after it is the delta; anything at or before it counts as already understood and is left out, the anchor's own contents included. When no anchor is supplied and none can be established from evidence, say so, report a current snapshot, and name what would establish one.
- **The ask comes first and carries its own qualification.** Open with what this reader must decide; a briefing that buries it is a log. State material uncertainty inside that opening claim, because naming one blocker while its supporting evidence is unmeasured is a stronger claim than the evidence supports, and a caveat further down does not repair it.
- **Outcomes, not the journey.** "The scoring rule was replaced" is a briefing; "three analysis passes ran" is a self-report about the agent.
- **Gloss on first use, and only where it is needed.** A project-specific term gets a short plain-language aside where it first appears, even when a terminology section follows. Skip the gloss for a term the reader used to make a decision or draw a distinction; supply it when they only repeated it back.
- **Report completion only where you verified it.** Relocated is not reconciled, passing is not covered, and local is not deployed — name the one you actually have. A settled decision or a healthy check gets one line or none.
- **A screen by default, expansion on offer.** Close with per-section drill-down offers rather than delivering everything expanded, and report an inaccessible source instead of widening the briefing to compensate.
- **Every claim opens to something.** Attach the file, commit, run, or artifact the reader can inspect, with the observation date wherever current status could be mistaken for a durable fact.

## Output and stopping

Use the caller's schema or requested format. Without one, order the briefing by what the reader must do:

- **Needs you** — whatever this reader alone can decide, judge, or supply, each carrying enough detail that no second file has to be opened.
- **Changed since the anchor** — outcomes and their evidence. With no established anchor, report current state under this heading instead.
- **New words** — terminology this project coined or repurposed since the anchor, with a line apiece naming where each one is defined. Omit the section when there is none.

Then the next useful action and the material verification limits.

Stop when the requested scope is understandable or inaccessible evidence prevents a reliable account. Report missing sources rather than expanding indefinitely. Do not fix files, choose unresolved product policy, send messages, or create monitoring jobs as part of the briefing.

## Examples

- Normal: after a paused refactor run, summarize the verified changes, the failed check requiring attention, and the next command or decision, each grounded in run state and repository evidence.
- Edge: no last-known baseline exists and files have recent mtimes. Provide the present status with its sources; do not claim those files changed while the user was away or that a deployment succeeded.

## Completion check

The reader can act without remembering the previous session, completion claims have evidence, the baseline is honest, and no requested decision was silently made for them.
