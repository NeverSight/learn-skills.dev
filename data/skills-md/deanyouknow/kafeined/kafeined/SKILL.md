---
name: kafeined
description: Keep-awake guard for AI agent sessions. When the user mentions /kafeined or @kafeined, hold the machine awake (no auto-sleep, idle logout, or shutdown) for the whole task, then release when done. Works on macOS (caffeinate), Windows (PowerShell), and Linux (systemd-inhibit) with no third-party installs.
---

# kafeined — keep-awake guard for agent sessions

The user has asked you (usually by including `/kafeined` or `@kafeined` in their
message) to keep their machine awake while you work, so that idle sleep, idle
logout, or shutdown never interrupts your task. Do this **before starting the
main task**, and always release the hold **when the task ends**.

## Quick reference

Scripts live next to this file in `scripts/`:

- macOS / Linux / Windows-GitBash: `scripts/kafeined.sh` — run with `bash`
- Windows PowerShell: `scripts/kafeined.ps1` (or `scripts/kafeined.cmd` from cmd)

Paths below use `$SKILL_DIR` = the directory containing this SKILL.md.

## 1. Parse the user's request

From the user's message, extract:

- **Duration** — if the user wrote something like `2h`, `30min`, "for an hour",
  use it (rounded up to whole hours; minimum 1). Pass it as `--hours N`.
  If nothing is specified, use the default (no flag) — 6 hours.
- **Screen** — if the user asks to keep the *screen/display* on too, add
  `--display`. Otherwise never pass it.

## 2. START the hold (before doing any real work)

macOS / Linux (and Windows agents running inside Git Bash):

```bash
bash "<SKILL_DIR>/scripts/kafeined.sh" start [--hours N] [--display]
```

Windows (PowerShell):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<SKILL_DIR>\scripts\kafeined.ps1" start [-Hours N] [-Display]
```

- Expect `kafeined: holding machine awake (pid ..., cap Nh, ...)`. The hold is
  idempotent — running `start` twice is harmless.
- For a task that is a **single command** (e.g. one long build), prefer
  `while` mode — it releases automatically:

  ```bash
  bash "<SKILL_DIR>/scripts/kafeined.sh" while --hours 4 -- <command...>
  ```

## 3. During long work

If your session runs long and the user's task is still unfinished, re-run the
same `start` command roughly every 30–60 minutes (or run `renew`). It is
idempotent; if the hold expired it simply starts a fresh one. You may briefly
mention this in your narration, e.g. "renewed kafeined hold".

## 4. STOP the hold (as the FINAL step — always, even on failure)

When the task ends — completed, failed, or abandoned mid-way, including when
the user interrupts you — run exactly one of:

macOS / Linux / Windows-GitBash:

```bash
bash "<SKILL_DIR>/scripts/kafeined.sh" stop
```

Windows (PowerShell):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<SKILL_DIR>\scripts\kafeined.ps1" stop
```

- Run `stop` in the same final tool block as your closing message so it is not
  forgotten. `stop` is safe to run when nothing is held.

**Closing ritual — mandatory.** Your final message must state the hold status
in this format so the user can see it worked:

- `☕ hold released` after a successful `stop`
- `☕ hold active (cap Nh)` only if the user explicitly asked to keep the
  machine awake after the task

## 5. Status / troubleshooting

- `status` prints `ACTIVE (pid ...)` and exits 0 when holding, or `inactive`
  and exits 1 when not. Use it if `start` behaves unexpectedly.
- State lives in `${TMPDIR:-/tmp}/kafeined/` (`pid`, `meta`, `log` files).
  If `start` fails, read the `log` file there and tell the user what it says.
- If the machine still sleeps: lid-close, low battery, or user-initiated
  suspend are outside any program's control — say so plainly.

## Rules of thumb

1. Never run real task work while the hold is inactive — start it first.
2. Never leave the session without running `stop`.
3. Only pass `--display` when the user explicitly wants the screen kept on.
4. Never modify the scripts to extend the cap beyond what the user asked for.
