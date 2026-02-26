---
name: session-reflection
description: >-
  Structured session analysis and system prompt refinement. Analyzes user
  interventions, categorizes process gaps, generates project-specific system
  prompts, and maintains working state for crash recovery. Activate after
  milestones, repeated corrections, session restarts, or on user request.
license: CC0-1.0
metadata:
  author: jwilger
  version: "1.0"
  requires: []
  optional: [memory-protocol, agent-coordination]
  context: [git-history]
  phase: build
  standalone: true
---

# Session Reflection

**Value:** Feedback -- every user intervention is a signal that the system
prompt is incomplete. Turning corrections into durable instructions creates
compound improvement across sessions.

## Purpose

Teaches agents to analyze session history for recurring corrections, generate
project-specific system prompts that prevent known failure modes, and maintain
working state that survives context compaction and crashes. Transforms reactive
corrections into proactive prevention.

## Practices

### Reflection Triggers

Reflect after: milestones (PR merged, feature complete), 3+ repeated
corrections from the user, session restart or crash recovery, every 5
completed tasks, and on explicit user request. Do not wait for a "good time"
-- reflect when triggered.

### Analyze Session History

Examine conversation history, git log, memory files, WORKING_STATE.md, and
session logs. Categorize each user intervention into one of five types:

- **Correction**: Agent did the wrong thing (system prompt gap)
- **Repetition**: Agent was told the same thing again (emphasis gap)
- **Role Redirect**: Agent stepped outside its role (boundary gap)
- **Frustration Escalation**: User became more forceful (decay problem)
- **Workaround**: User did it themselves (skill gap)

See `references/analysis-framework.md` for detailed categorization and
prioritization.

### Generate or Refine System Prompt

Create a project-specific system prompt file that supplements installed
skills. Structure: Role and Constraints, Startup Procedure, Process
Requirements, Common Mistakes, Reminders.

Refinement rules: add new items for new gaps, promote advisory to structural
when gaps recur, rewrite ambiguous items for clarity. Never remove items
until the gap is confirmed solved across 3+ sessions. See
`references/system-prompt-patterns.md`.

### Generate Launcher Script

For harnesses that support system prompts (Claude Code:
`claude --system-prompt <file> "$@"`), generate a launcher script (e.g.,
`bin/ccf`). For harnesses without system prompt support, fold critical
directives into CLAUDE.md/AGENTS.md. See `references/launcher-templates.md`.

### Self-Reminder Protocol

Every 5-10 messages during long sessions, re-read: system prompt, role
constraints, current task context, WORKING_STATE.md. Mandatory after context
compaction (you lose implicit context). This is the primary defense against
role drift in long sessions.

### Working State Persistence

Maintain WORKING_STATE.md as insurance against context compaction and crashes.
Update after every significant state change. Always read before acting after
any interruption. Location: `.factory/WORKING_STATE.md` (pipeline) or project
root (standalone). See `references/working-state-schema.md` for format.

**Do:**
- Update on task start, phase change, decision made, blocker encountered
- Overwrite with current state (not append)
- Read FIRST after any interruption

**Do not:**
- Guess state from memory after a compaction or restart
- Use as a journal -- keep it concise and current
- Skip updates because "nothing important changed"

### Post-Session Learning Loop

At session end: identify patterns from this session, update memory files,
refine system prompt if triggers were hit, archive working state.

The loop closes when the same category of intervention stops recurring. If
an intervention category persists across 3+ sessions after system prompt
refinement, escalate: the gap may require a new skill or a structural
change to the workflow.

## Enforcement Note

This skill provides advisory guidance. The self-reminder protocol and working
state maintenance require agent self-discipline. On Claude Code, a
pre-tool-use hook could mechanically enforce state file reads, but no such
hook is provided by default. The reflection triggers are event-driven and
cannot be mechanically enforced. If you observe the agent drifting from its
role or repeating corrected mistakes, point out the pattern and suggest a
reflection.

## Verification

After completing work guided by this skill, verify:

- [ ] Reflection performed at every trigger point (milestone, repeated correction, restart)
- [ ] User interventions categorized using the five-type taxonomy
- [ ] System prompt generated or refined with structural (not just advisory) language
- [ ] Self-reminder protocol followed (state re-read every 5-10 messages)
- [ ] WORKING_STATE.md current and accurate
- [ ] State re-read after every context compaction (not guessed)
- [ ] Launcher script generated for harnesses that support system prompts

If any criterion is not met, revisit the relevant practice before proceeding.

## Dependencies

This skill works standalone. For enhanced workflows, it integrates with:

- **memory-protocol:** Persistent storage for session learnings and working state
- **agent-coordination:** Coordination patterns referenced in system prompt generation
- **pipeline:** Pipeline controller benefits from self-reminder and crash recovery
- **ensemble-team:** Team retrospectives feed into session reflection analysis

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill memory-protocol
```
