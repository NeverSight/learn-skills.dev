---
name: ai-cli-version
description: Check whether the Claude Code, Codex, Grok Build, Muse Code and Antigravity (Gemini) CLIs are up to date, then optionally update outdated CLIs after a y/Esc choice. `setup` chooses which CLIs to check. It first checks GitHub for a newer version of itself and asks y/n before updating. Use when the user runs /ai-cli-version or /check-uu (with or without `setup`), or asks to check for updates, whether a CLI has a newer version, when a version was released or installed, "is my CLI up to date", or "when was this released", including equivalent requests in any language.
compatibility: Requires Python 3.9+, permission to launch subprocesses, and internet access to registry.npmjs.org, api.github.com, raw.githubusercontent.com, api.meta.ai and the Antigravity CLI auto-updater (run.app). Each tool shown needs its CLI installed; missing tools are reported as not installed. npm and Node.js are not required. Tested on Windows and macOS; Linux is not yet tested.
metadata:
  author: Jeinn
  version: "1.13.1"
---

# /ai-cli-version — CLI version and update check

Launcher, from this skill's directory: `./run.sh` on macOS or Linux (`sh run.sh` if it
is not executable); `py -3 run.py` on Windows (`python run.py` if `py` is missing).
The launcher is check-only. During the check, never run `claude update`, `codex update`
or `grok update` without `--check`, never set `MUSE_SYNC_UPDATE=1`, and never fill a
version or time from memory.

## Step 0 — update check

Run the launcher with `--check-skill`. It prints one line,
`skill installed=… latest=… status=… update_cmd=…` or `skill check failed (...)`.

- `up to date` or `check failed`: say nothing and continue.
- `update available`: print only

  ```
  ai-cli-version skill {installed} → {latest} is available.
  Update the skill now?
  [y] Update    [n] Skip
  ```

  and stop. On exact `y`/`Y` run `update_cmd`, report it in one line, re-read this
  `SKILL.md` from disk and continue with the user's request. On `n`/`N` say it was not
  updated and continue. Any other reply: repeat the two choices.

`setup` (`/ai-cli-version setup`, `/check-uu setup`): read `references/setup.md` and
follow it; do not run the check or any updater.

## Report

Run the launcher with no arguments. Each tool has a 20-second budget; never extend it.

- **HTML output** (default): the last line is `### HTML <target>`, an
  `http://127.0.0.1:…/` URL (the local page with a Refresh button) or a file path. Print
  only, with no preamble or recap:
  1. the `### SUMMARY` lines up to the first blank line, as they are (summary and any
     `Not checked (setup)` line);
  2. `**Report:** [Open the HTML report](<target>)`: the URL as printed, or
     `file:///<path with forward slashes>` for a path. Add a short note for each
     parenthesised note on that line (`Refresh unavailable: …`, `could not open a browser`);
  3. the remaining `### SUMMARY` lines, the y/Esc update prompt, when there are any.
- **Markdown output** (no `### HTML` line, setup saved `md`): read
  `references/markdown-report.md` and render the report it describes.

A `check failed (... CERTIFICATE_VERIFY_FAILED ...)` on macOS means a python.org Python
whose `Install Certificates.command` was never run: say so, do not work around it. On
Linux (untested), report failures as-is and say the platform is untested.
`references/how-it-works.md` explains each source.

## Optional update

The prompt is the `### SUMMARY` lines after its blank line; it appears only when a row has
`status=update available`. Show it (translated if needed, keys exactly `y` and `Esc`) and stop.

- `/ai-cli-version` authorizes the check, not an update. Do not run any updater in the
  same turn as the initial report.
- A subsequent exact `y` or `Y` authorizes every `update_cmd` from the immediately
  preceding report whose status was `update available`. Run those commands separately,
  so one failure does not prevent the remaining updates.
- On Windows, run each `update_cmd` with a PowerShell tool, not Git Bash or another MSYS
  shell. Those shells put Git's GNU `tar` ahead of `System32\tar.exe` on PATH, so the
  Codex installer extracts nothing and fails with `did not contain the expected package
  layout`. If only a Bash shell is available, put `/c/Windows/System32` first on PATH for
  that command.
- `Esc` or `Escape` skips all updates. Confirm that no updates were run.
- Any other reply is not authorization. Repeat the two valid choices without updating.
- After `y`, show success or failure for every selected tool, then run the check-only
  launcher again and show the refreshed report. Do not show another prompt for a tool
  whose updater failed during that same update attempt.
- If all tools are current, or the user explicitly asked for check-only behavior, do not
  show the prompt.
- No preamble, recap, or closing offer outside the report, prompt, and update results.

## Language

Use a language the user explicitly asked for, else the OS display language when the
host provides it, else English. Never infer it from the conversation, timezone or
encoding. Translate readable prose only; keep tool names, versions, dates, commands and
provider diagnostics unchanged. Use the same language for the report, the update prompt
and the update results.
