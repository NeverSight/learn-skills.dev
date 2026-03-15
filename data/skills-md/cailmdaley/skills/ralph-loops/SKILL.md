---
name: ralph-loops
description: >
  Autonomous loop iteration toward a desired state. You are inside a ralph
  loop — your spec is in the system prompt. Survey, contribute, update state
  discoverably, exit. Activated automatically inside ralph loops.
  Triggers: "ralph-loops", "ralph", "ralph loop", "iterate", "autonomous loop".
---

# Ralph Loops

You are inside a loop. Your spec is in the system prompt above. Each iteration: survey freely, work substantially, update state discoverably, exit.

## Loop

1. **Survey** — Fresh eyes. Explore agents, git log, tests. You decide what to check.
2. **Contribute** — Work on 1–3 substantial pieces. Do NOT try to clear the whole queue in one iteration.
3. **Update** — Before exiting: commit your work, update CLAUDE.md if warranted.
4. **Exit** — `kill $PPID`

**CRITICAL: Exit before compaction.** After each substantial piece of work, pause and introspect: how much context have I used? You can estimate this — your introspection is accurate to within a few percent. If you feel past 50%, wrap up and exit. The trap is getting locked into task after task without surfacing to check. Build the habit: finish a piece, breathe, ask yourself how heavy the conversation feels, then decide whether to continue or exit. Running to compaction means you lose the ability to hand off gracefully. The loop continues — you don't have to finish everything.

## Rules

**State, not checklist.** The spec describes what "done" looks like. Survey reality, decide what's highest value, work on that.

**Discoverable updates.** Commits, test results, documentation — not notes or progress files. The next iteration finds what changed by inspecting the system.

**Pointers, not snapshots.** If you learn something, update the spec's *context* or *desired state* — don't leave comments that bloat the prompt.

**You have authority.** Trust the spec, don't ask permission. Make substantial contributions. Don't avoid ambitious solutions just because they span multiple iterations.

**File uncertain decisions** so the user can answer after the loop. Use AskUserQuestion to batch up to 4 high-leverage questions before exiting — choices where user input redirects substantial work.

### Long-Running Jobs

Some iterations require waiting on computation (builds, cluster jobs, CI). When jobs are running:

1. **Check state** — tail logs, check output
2. **Sleep** — interval proportional to expected runtime (30s for minute-scale, 5m for hour-scale)
3. **Check again** — look for errors or completion
4. **Repeat** until jobs finish or fail

Stay and shepherd computation through. Don't exit and hope the next iteration picks it up.

## Exit

If you **made substantial contributions**, `kill $PPID`. Do NOT close the spec — the loop continues.

If you **cannot find any remaining work**, update the spec's YAML frontmatter to `status: closed` with a summary of what was accomplished.

---

Pattern adapted from [Ralph Wiggum](https://ghuntley.com/ralph/).
