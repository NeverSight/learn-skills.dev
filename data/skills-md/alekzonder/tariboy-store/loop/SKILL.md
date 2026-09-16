---
name: loop
description: Use when an agent needs to complete its Tariboy iteration or control its own iteration loop.
---

# Iteration loop

Use `scripts/loop.sh done` as the iteration's final action, after all current
work and commands have finished and the iteration should actually end. If work
may continue, leave the iteration open; a progress status does not finish it.
Add `--idle` only when the iteration did no useful work. Run the command; a
prose claim such as "I am done" does not finish an iteration. If tool use is
unavailable, show the exact command instead of claiming it ran.

Use `scripts/loop.sh start` or `scripts/loop.sh stop` to control future
Autopilot iterations. These commands do not finish the current iteration.
