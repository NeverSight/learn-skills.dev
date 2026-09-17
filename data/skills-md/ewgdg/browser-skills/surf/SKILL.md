---
name: surf
description: Real browser control for web research, documentation lookup, testing, screenshots, forms, page inspection, and debugging. Use when lightweight API tools are unavailable or rendered pages, authenticated sessions, or browser interaction are required.
---

# Surf

Follow the workflow below; open linked `docs/` only when the stated task or problem applies.

Run ordinary Python through `scripts/run.py`. Each call starts a fresh interpreter: import and initialize handles each time. Named browser threads persist between calls; Python variables and emission baselines do not. Save intermediate data to files when needed across calls.

## Prepare

Set `SURF_SKILL` to the absolute directory containing this installed `SKILL.md`, not the working directory. Requires Python 3, `uv`, and Google Chrome; the launcher manages Python dependencies.

The launcher installs the runtime pinned by this skill. If it reports a missing or invalid pin, the skill is incorrectly installed; report that instead of working around it. For dependency failures, read [launcher setup](docs/launcher.md).

Run setup once, or after installation changes:

```bash
python3 "$SURF_SKILL/scripts/run.py" - <<'PY'
from surf_agent import Browser

browser = Browser()
browser.setup()
print(browser.backend())
print(browser.profile())
PY
```

For backend selection, profile configuration, or startup problems, read [backends](docs/backends.md) and its backend-specific guide.

## Browse, observe, decide

Use a unique thread name per task. Surf owns a dedicated Chrome window/profile, separate from the user's main browser. Reuse the name to continue the task without navigating again.

```bash
python3 "$SURF_SKILL/scripts/run.py" - <<'PY'
from surf_agent import Thread

thread = Thread("research-42")
thread.open("https://example.com")  # creates its window when missing
thread.emit(thread.snapshot())
PY
```

Inspect the snapshot before choosing targets. Batch deterministic actions until a new observation or human decision is needed:

```python
from surf_agent import Thread

thread = Thread("research-42")
thread.fill("@query", "browser skills")  # use a target from the observed snapshot
thread.press("Enter")
thread.emit(thread.snapshot())
```

Actions and observations are silent; print only useful results. `snapshot().text` is complete. `emit(snapshot)` outputs a numbered observation with explicit BEGIN/END boundaries: full text first, then useful diffs; `full=True` forces full output. Multiple emissions appear in order in the same script output, not separate agent turns. End the script when the next action requires a decision. Read [snapshot semantics](docs/python-api.md#snapshot-output) for the format, baselines or custom sinks.

Pass a Python file or `-` for stdin; subsequent arguments reach `sys.argv`. For large text or JavaScript, read files in Python rather than nesting shell quoting:

```bash
python3 "$SURF_SKILL/scripts/run.py" /tmp/surf-step.py /tmp/body.txt /tmp/inspect.js
```

For action signatures and administrative operations, read [Python API](docs/python-api.md).

## Login and human unblock

For existing Chrome login state, read [cookie import](docs/cookie-import.md) before configuring access. For extension-based login, read [1Password setup](docs/1password-setup.md) once and [autofill](docs/1password-autofill.md) when logging in.

When blocked, ask the user to complete the blocker in the Surf Agent window and confirm when done. Preserve the page and wait for that confirmation, then inspect it using the same thread. Reopening the URL may destroy completed human work.

For manual login, close Surf automation windows and call `Browser().open_profile(url)`. Close manual Chrome before resuming automation. Bring a window forward with `Thread(name).focus()` only when requested.

## Recovery

After timeout or connection loss, inspect the same named thread before deciding whether to repeat an action: submissions, purchases, or messages may already have taken effect.

`is_open()` checks without creating a page, but false can also mean the bridge is unavailable. Reopen only when absence is established and navigation is safe. For a persistently unavailable bridge, use `Browser().stop_bridge()`; the next browser action restarts it. Restarting does not make replay safe.

## Cleanup

Close every thread you opened when its work is complete, including after errors; retain a thread only for an explicit pending human handoff.

```python
from surf_agent import Browser, Thread

Thread("research-42").close()
Browser().close_matching("run-42-*")
```

Use only task-owned cleanup patterns. `close_matching("*")` requires ownership of all remembered threads. For inventory or intentional detachment, consult the [API reference](docs/python-api.md).
