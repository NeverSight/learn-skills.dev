---
name: herdr-reload
description: Move running Claude Code sessions in herdr-app (hc) or herdr terminals, on this machine and on the machines hc is connected to, onto the newest installed claude binary. A running process cannot swap its executable, so each stale idle session is exited and resumed with `claude --resume <session>` in the same terminal, keeping the conversation. Dry run first, restart only on the user's go. Use when the user types /herdr-reload, or asks to get their herdr panes / running Claude sessions onto the latest Claude Code version after an update.
---

# herdr-reload — get running Claude sessions onto the new binary

A new Claude Code install only affects sessions started afterwards. Sessions that were already
running keep the binary they started with until they are restarted. This skill does that
restart for every session that needs it: `/exit`, then `claude --resume <same session>` in
the same terminal.

Two terminal servers can hold the sessions. The script picks `hc` (herdr-core, the server behind
herdr-app) when it holds Claude sessions, else the older `herdr`. `hc` sessions on machines it is
connected to (`hc machine ls`) are covered too; they show as `machine/t7`. `--server hc|herdr`
forces one, and `--local` leaves the connected machines alone.

The mechanics are in `scripts/herdr-reload.py` (next to this file). Run it; don't redo it by hand.

## Steps

1. **Dry run.** `python3 <skill-dir>/scripts/herdr-reload.py`
   It lists every Claude session with its running version and an action. The id is the
   terminal's address (`t2`, or `machine/t5` on a connected machine), or a pane id (`w1:p2`)
   on herdr. Each session is compared with the claude binary a fresh `claude` would start on
   its own machine.
   - `reload`: idle, on an older binary (or one that was deleted), and its session id is
     known. The `->` line is the exact command it will be restarted with (the original
     flags, minus any old `--resume`/`--continue`).
   - `ok`: already on the current binary.
   - `busy`: on an older binary and not `idle` (`working`, `blocked`, or `done`, which both
     servers show for a finished turn that may still have background work, and which clears
     once someone looks at the pane). Never restarted. With `--force`, its agent gets a
     restart note instead (see below).
   - `skip`: with the reason. The session running the script, which is your own, is always
     skipped.
2. **Show the user the list and ask before restarting.** Restarting interrupts their
   sessions. If they want only some of them, pass those pane ids. **Skip this step only
   when the user said `force`** (`/herdr-reload force`, "force reload", "just do it"). Then
   go straight to step 3 with `--force`.
3. **Apply.** `python3 <skill-dir>/scripts/herdr-reload.py --apply [id ...]`
   It goes one session at a time. On `hc` it sends `/exit` (only while the session is idle),
   waits until the terminal's shell is back in the foreground, types
   `claude --resume <session> ...` into that shell, and waits for claude to be the foreground
   program again. On `herdr` it uses `herdr agent prompt` and `herdr agent start` instead.
   Each line then reports the version the session is running now, or `FAILED` with the reason
   and the command to run by hand.

   **`--force`** does the same as `--apply` and also handles the `busy` panes: it queues a
   short `[herdr-reload]` note to each one's agent with `herdr agent prompt`. Claude Code
   queues typed input while it works. The note tells that agent to finish its current task
   and then ask the user to restart it (`/exit`, then `claude --resume <session>`). Nothing
   busy is interrupted or restarted. A `blocked` pane (sitting at a permission or question
   dialog) can't take the note, because herdr won't type into a dialog. Those come back as
   `NOT NOTIFIED`, so pass them on to the user yourself.
4. **Report** what was restarted, what was skipped and why, and any failure as it was
   printed. For your own session, tell the user to `/exit` and run `claude --resume` themselves
   (or `claude -c` in the same folder).

## Things that can go wrong

- **Text sitting unsent in a session's input box.** `/exit` lands after that text, so Claude
  doesn't exit, and the script reports `FAILED: did not exit`. (`hc` also waits up to a minute
  for an unfinished draft before it types.) Leave that session for the user to deal with.
  Never send `ctrl+c` or clear their input to force it.
- **A session that went busy between the dry run and `--apply`.** The plan is rebuilt on
  apply, and `hc` only types `/exit` into an idle session, so it is left alone.
- **`hc send` from inside an hc terminal tags its text** as `<hc from="t6">...</hc>`, and
  Claude then sees `/exit` as plain text. The script sends without `HC_TERMINAL_ID`, so the
  text arrives as typed. Do the same if you restart a session by hand.
- **The session id.** `hc` has no field for it. The script takes it from the terminal's
  `session` label, from `--resume <id>` in the process's flags, from the
  `/tmp/claude-<uid>/<folder>/<id>/tasks` folder the process holds open, and last, for a session
  that has run a turn, from the one transcript written since the process started. A session
  with none of these (no turn yet) shows `skip`. A session with transcripts switched off
  (`CLAUDE_CODE_CHILD_SESSION` inherited from a parent Claude) cannot be resumed.
- **Machines.** A connected machine is read and restarted through `hc exec --on` and
  `hc send machine/tN`, so the machine needs Linux (`/proc`) and `claude` reachable from a
  login shell there. A machine that is not connected, or whose `claude` cannot be found, shows
  `skip` with the reason and the others carry on.
- **A terminal that runs claude as its own program** (`hc run claude`, no shell under it)
  shows `skip`: exiting claude would end the terminal.
- **"Current binary"** is the one `mise which claude` resolves to (or `claude` from a login
  shell if there's no mise), checked on each machine separately. If the user just installed a
  new version and the dry run still shows the old one as current, the install isn't the
  active version yet. Fix that first.
