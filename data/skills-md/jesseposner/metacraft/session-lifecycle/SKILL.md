---
name: session-lifecycle
description: Every session has a beginning, middle, and end. Design for session boundaries instead of being surprised by them.
---

# Session Lifecycle

Every session has a beginning, a middle, and an end. Treat each one deliberately, or entropy will treat them for you.

## What this is

A protocol for the arc of a working session with an AI agent. Not a rigid checklist, but a set of practices that prevent the two most common failures: starting without context (cold start amnesia) and ending without capture (lost work).

The deeper point: context windows are not infinite, memory compaction is not optional, and sessions end whether you plan for it or not. Design around these constraints instead of being surprised by them.

This covers the full arc. For a lighter mid-session pause, see [Gather](../gather/SKILL.md).

## When to use it

- Every session. Scale the ceremony to the session's weight, but the pattern always applies.
- Especially: long sessions, multi-phase work, anything that will span multiple compaction cycles.

## The pattern

### Starting

1. **Load persistent context.** Read memory files, project state, any handoff notes from previous sessions. Don't trust what you remember from last time: trust what's written down.

2. **Check for in-flight work.** Did the last session leave something running? An eval, a build, a long process? Harvest those results before starting new work. Orphaned outputs are wasted compute.

3. **Orient.** Read the roadmap, the task list, the current priorities. Ask: "What matters most right now?" The answer determines the session, not momentum from last time.

4. **Verify the environment.** Is the system in the state you expect? Running processes, git status, server state. Surprises discovered mid-session cost more than surprises discovered at the start.

### During

- **Log as you go.** Record experiments, decisions, and results immediately, even failures. If it's worth trying, it's worth recording. The log is for future-you, who won't remember why you tried that thing.

- **Manage compaction deliberately.** In long sessions, context will compress. Don't let auto-compaction surprise you. When it's approaching, run the handoff cycle yourself:
  1. **Farewell**: the agent wraps up its current thread, surfaces anything unsaid, captures final state
  2. **Log**: produce a structured handoff document: where things stand, what's decided, what's next, any critical context the new session needs
  3. **Compact**: trigger compaction manually, on your terms
  4. **Re-orient**: the agent comes back into a fresh context, re-reads persistent files, re-establishes the frame
  5. **Load the log**: paste the handoff document into the new context so nothing is lost

  This turns compaction from a threat into a tool. Each cycle forces crystallization, and the handoff log becomes an artifact that future sessions can reference.

- **Circuit breaker.** If multiple sessions have been spent on meta-work, process, or infrastructure without producing primary work output, force a reset. Process exists to serve the work, not the other way around.

### Ending

1. **Capture in-flight state.** If anything is still running: record what it is, where its output goes, what to do when it finishes, and any non-standard system state.

2. **Update persistent memory.** Stable findings, new patterns, changed priorities. Future sessions start by reading this. Make it accurate.

3. **Name what's unfinished.** Explicitly. "Continue X" is better than silence. "Blocked on Y, try Z next" is better than "continue X." Unfinished is fine. Unnamed is not.

4. **Clean the ground.** Commit changes. Sync if appropriate. Leave the workspace in a state where the next session, whether it's you or someone else, can start clean.

## Anti-patterns

- **Cold starting.** Jumping straight into work without loading context. You'll rediscover things you already knew, or worse, contradict decisions already made.
- **Hot ending.** Stopping mid-flow without capture. The next session will spend its first 20 minutes reconstructing what you already had.
- **Context hoarding.** Keeping important state only in the context window, not on disk. When compaction hits, it's gone.
- **Infinite sessions.** Trying to keep one session alive forever by fighting compaction. Session boundaries are a forcing function: they make you crystallize what actually matters. Design for them instead of against them.
