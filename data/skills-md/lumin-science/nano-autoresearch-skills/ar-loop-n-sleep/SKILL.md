---
name: ar-loop-n-sleep
description: Continue iterative research in tmux while avoiding model-token use during long external runs. Read the original task and recent event log, advance until the run is healthy, then schedule a tmux-only wakeup at the next useful checkpoint.
---

# AR Loop & Sleep

Use this skill only inside tmux. Its job is to follow the user's research task,
sleep while external training runs, and wake the same Codex pane when useful work
should resume.

Accept an optional working directory (for example, `workdir=.worktrees/my-run`);
default to `./` when none is supplied. Resolve it to an absolute path before
reading or creating control files, and use it for the research work and every
callback. If the task creates an isolated worktree, use that worktree as the
working directory. Concurrent loops need separate working directories and tmux
panes.

Keep exactly two persistent control files in the selected working directory:

- `.ar/PROMPT.md`: the task supplied with the first invocation,
  recorded verbatim rather than summarized.
- `.ar/events.tsv`: one concise event per row with columns
  `time_utc`, `state`, `handoff`, and `next_check_utc`.

## On every invocation

If the current user message begins with `@@AR-CONTINUE@@`, select the working
directory included in that message first. Treat it as a scheduled continuation,
not a new kickoff task, and do not overwrite `PROMPT.md`. A `[wake:...]` token
identifies the delivery; it does not change the task and needs no acknowledgment.

Enter the selected working directory, read `.ar/PROMPT.md` and the last five
rows of `.ar/events.tsv`, then inspect the real project and run state.

- **First invocation:** create the two files, record the original task, and
  follow it until training is underway and healthy.
- **Previous run succeeded:** follow the original task through whatever should
  happen after that run, then continue until the next training run is underway
  and healthy.
- **Previous run failed:** inspect the failure and, following the original task,
  fix and retry or move on. Continue until training is underway and healthy.
- **Run still running:** if the estimated remaining time is under five minutes,
  wait and continue. Otherwise, use the exit procedure.

“Next” is defined only by the original task. Do not impose a particular
evaluation, analysis, or experiment-selection workflow.

## Exit procedure

Before a normal exit:

1. Confirm that training is running healthily.
2. Append one event whose handoff is one or two sentences describing the
   current step.
3. Estimate the next useful check time and convert it to a delay in seconds.
4. Use the bundled [wake helper](scripts/wake.py) to start one background sleeper
   for this exact tmux pane. It uses Python 3's standard library and tmux, with
   no external packages or `tmux-bridge` dependency. Resolve the helper from the
   directory containing this `SKILL.md`; use its absolute path below.

```bash
python3 /absolute/path/to/ar-loop-n-sleep/scripts/wake.py \
  --workdir "${workdir:-./}" \
  --pane "${TMUX_PANE:?invoke ar-loop-n-sleep from inside tmux}" \
  --delay-seconds "$delay_seconds"
```

The helper preserves the tmux socket, pane identity, foreground command and
absolute research directory. After the delay it leaves copy mode, checks for an
empty composer, and types one callback with a unique wake ID. Existing input is
left intact and reported as a delivery failure.

Delivery is observed from the pane, without a `.ar` flag or transcript-file
dependency:

- Ignore braille animation characters and display whitespace when recognizing
  the callback. Allow redraws time to settle.
- Send `Enter` when that callback is visible in the composer. Retry only `Enter`,
  at five-second intervals, at most four times and within thirty seconds. Never
  type the callback again during a retry.
- A newer composer below the callback shows that it was submitted. Stop sending
  keys immediately, even while the model is still preparing its response.
- Fresh assistant or tool content below this callback confirms activity. Raw
  vertical distance, wrapping, animation and status widgets are not activity.
- If submitted but no activity is visible within two minutes, preserve diagnostics
  and report that outcome; do not submit a duplicate continuation. Changed panes,
  interruptions and unconfirmed delivery also stop the helper.

The scheduling command prints a temporary diagnostics directory. Failed wakes
keep `delivery.jsonl`, the before/latest captures and a copy of the helper there;
successful wakes remove their temporary directory. A per-pane lock prevents
concurrent sleepers from typing duplicate callbacks. These are delivery artifacts
outside the research directory; `.ar/PROMPT.md` and `.ar/events.tsv` retain their
existing roles as the task and research history.

Use the bundled helper rather than recreating the delivery code in each research
turn. Do not use `codex queue` in this skill. Do not spend model turns polling a
healthy run. Do not claim success, fabricate healthy training, or schedule an
unsafe continuation when work is genuinely blocked.
