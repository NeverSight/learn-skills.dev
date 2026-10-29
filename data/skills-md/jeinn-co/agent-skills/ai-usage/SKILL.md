---
name: ai-usage
description: Check AI subscription usage limits across Claude, ChatGPT, Grok, Muse and Gemini (Antigravity CLI) in one unified report — percent used, how much is left, when each window resets, the model / effort of each CLI's newest session, and that model's CursorBench score, cost and CP. `setup` chooses which providers to report. It first checks GitHub for a newer version of itself and asks y/n before updating. Use when the user runs /ai-usage or /uu (with or without `setup`), or asks about usage, limits, remaining quota, reset times, rate limits, "am I out of Claude", "how much ChatGPT left", Muse usage, Gemini usage or Antigravity quota, including equivalent requests in any language.
compatibility: Requires Python 3.9+ and permission to launch subprocesses. Each provider shown needs its authenticated CLI and internet access; providers without a CLI are reported as unavailable. The update check reads raw.githubusercontent.com.
metadata:
  author: Jeinn
  version: "1.16.1"
---


# /ai-usage — unified AI usage report

Launcher, from this skill's directory: `./run.sh` on macOS or Linux; `py -3 run.py` on
Windows (`python run.py` if `py` is missing). Never install anything, ask the user to
log in, open a browser yourself, or make HTTP calls of your own. Report only what the
launcher prints; never fill a number from memory or an earlier run.

## Step 0 — update check

Run the launcher with `--check-skill`. It prints one line,
`skill installed=… latest=… status=… update_cmd=…` or `skill check failed (...)`.

- `up to date` or `check failed`: say nothing and continue.
- `update available`: print only

  ```
  ai-usage skill {installed} → {latest} is available.
  Update the skill now?
  [y] Update    [n] Skip
  ```

  and stop. On exact `y`/`Y` run `update_cmd`, report it in one line, re-read this
  `SKILL.md` from disk and continue with the user's request. On `n`/`N` say it was not
  updated and continue. Any other reply: repeat the two choices.

`setup` (`/ai-usage setup`, `/uu setup`): read `references/setup.md` and follow it; do
not run the report.

## Report

Run the launcher (no arguments; `fresh` only means do not reuse an earlier answer).
Each provider has a 20-second budget; never extend it.

- **HTML output** (default): the last line is `### HTML <target>`, an
  `http://127.0.0.1:…/` URL (the local page with a Refresh button) or a file path. Print
  only, with no preamble or recap:
  1. the `### ADVICE` lines as they are (a `> **Warning:**` line when a week window is
     over 80%, then the `> **→ Use … right now:**` line); nothing when the block is empty;
  2. `_Not checked (setup): <names>_` when a `### skipped <ids>` line exists
     (ids: claude Claude, codex ChatGPT, grok Grok, muse Muse, agy Gemini);
  3. `**Report:** [Open the HTML report](<target>)`: the URL as printed, or
     `file:///<path with forward slashes>` for a path. Add a short note for each
     parenthesised note on that line (`Refresh unavailable: …`, `could not open a browser`).
- **Markdown output** (no `### HTML` line, setup saved `md`): read
  `references/markdown-report.md` and render the report it describes.

Do not suggest installing a missing CLI unless asked. `references/providers.md`
explains where each number comes from.

## Language

Use a language the user explicitly asked for, else the OS display language when the
host provides it, else English. Never infer it from the conversation, timezone or
encoding. Translate readable prose only; keep model IDs, numbers, times, commands and
provider diagnostics unchanged.
