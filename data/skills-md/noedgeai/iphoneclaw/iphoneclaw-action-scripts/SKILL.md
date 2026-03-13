---
name: iphoneclaw-action-scripts
description: Record, register, and invoke iPhoneClaw action scripts to reduce VLM tokens and make automations repeatable. Use when you want the model/agent to call `run_script(name=..., vars=...)`, when updating `action_scripts/registry.json`, when exporting scripts from `runs/*/events.jsonl`, or when triggering scripts remotely via `python -m iphoneclaw ctl run-script` while the worker is paused.
---

# iPhoneClaw Action Scripts

Use the local script registry (`action_scripts/registry.json`) to give the model a low-token primitive:
`run_script(name=..., ...)` expands into a pre-recorded `.txt` action script and executes the concrete actions.

Key files:
- `action_scripts/registry.json`: short name -> script path
- `action_scripts/common/*.txt`: curated scripts
- `action_scripts/recorded/*.txt`: recordings/exports

## Priority Rules (MUST follow)

**When a registered script covers the task, ALWAYS use `run_script(...)` instead of manually composing individual actions.**

### 1. Launching an App -> ALWAYS use `open_app_spotlight`

Do NOT manually compose `iphone_home()`, `swipe`, `type` sequences to open an app.
Instead, emit a single action:
```text
Action: run_script(name='open_app_spotlight', APP='<app_name>')
```

Examples:
```text
Action: run_script(name='open_app_spotlight', APP='bilibili')
Action: run_script(name='open_app_spotlight', APP='Safari')
Action: run_script(name='open_app_spotlight', APP='Settings')
Action: run_script(name='open_app_spotlight', APP='WeChat')
```

This script does: Home -> swipe left x10 -> swipe up (Spotlight) -> type app name + Enter.

### 2. Return to Home & Swipe -> use `iphone_home_swipe_left_10_then_down`

When you need to go back to home screen and reset scroll position:
```text
Action: run_script(name='iphone_home_swipe_left_10_then_down')
```

This script does: Home -> swipe left x10 + swipe down.

### 3. Killing / Dismissing the Current App -> use `kill_app`

Do NOT manually compose `iphone_app_switcher()` + swipe sequences to kill an app.
Instead, emit a single action:
```text
Action: run_script(name='kill_app')
```

This script does: Cmd+2 (App Switcher) -> swipe up on right side to dismiss the current app.

### General Rule

Before composing a multi-step action sequence, check `action_scripts/registry.json` for an existing script that covers the flow. If one exists, use `run_script(name=...)`. This saves tokens and is more reliable than ad-hoc action chains.

## Available Scripts (Registry)

| Short Name | Script | Description |
|---|---|---|
| `open_app_spotlight` | `common/open_app_spotlight.txt` | Open any app via Spotlight. Var: `APP` |
| `iphone_home_swipe_left_10_then_down` | `common/iphone_home_swipe_left_10_then_down.txt` | Home + swipe left x10 + swipe down |
| `kill_app` | `common/kill_app.txt` | Kill/dismiss current app via App Switcher (Cmd+2 + swipe up) |

## Preferred Model Output (Low Token)

When a stable flow exists, output a single action:
```text
Action: run_script(name='open_app_spotlight', APP='bilibili')
```

Notes:
- Vars can be passed as `vars={...}` or as keyword sugar (`APP='bilibili'`).
- Prefer `name=...` (registry) over `path=...` (arbitrary file) for safety and portability.

## Run Scripts Manually (Local)

Run a script file directly:
```bash
python -m iphoneclaw script run --file action_scripts/common/open_app_spotlight.txt --var APP=bilibili
```

## Run Scripts Remotely (Supervisor API, Worker Paused)

Requirement: the worker must be `paused` and supervisor exec must be enabled (`enable_supervisor_exec`).

Use `ctl`:
```bash
python -m iphoneclaw ctl run-script --name open_app_spotlight --var APP=bilibili
```

This hits supervisor endpoint `POST /v1/agent/script/run`.

## Record And Register A New Script

1. Create or record the script.
```bash
# real user behavior recording (recommended)
python -m iphoneclaw script record-user --app "iPhone Mirroring" --out action_scripts/recorded/my_flow.txt

# quick record from stdin (Ctrl-D to finish)
python -m iphoneclaw script record --out action_scripts/recorded/my_flow.txt
```

Or export from a previous run:
```bash
python -m iphoneclaw script from-run --run-dir runs/<run_id> --out action_scripts/recorded/<run_id>.txt
```

2. Add a registry entry in `action_scripts/registry.json`:
```json
{
  "my_flow": "recorded/my_flow.txt"
}
```

3. Invoke it via model action:
```text
Action: run_script(name='my_flow')
```

You can also compose scripts by nesting inside `.txt`:
```text
include open_app_spotlight APP=bilibili
# or:
run_script(name='open_app_spotlight', APP='bilibili')
```

## Registry Path Resolution

Default registry path is `./action_scripts/registry.json`.

If running from a different working directory, set:
- `IPHONECLAW_SCRIPT_REGISTRY=/absolute/path/to/action_scripts/registry.json`
