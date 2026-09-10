---
name: scrooge-stats
description: >
  Show measured Scrooge session token usage and estimated savings when
  available. Use when the user invokes /scrooge-stats, $scrooge-stats, asks for
  Scrooge token stats, or asks how many output tokens Scrooge saved.
allowed-tools: Bash
---

Run the stats script and show its output verbatim:

```bash
node "${CLAUDE_PLUGIN_ROOT:-.}/hooks/scrooge-stats.js"
```

Append `--share` for a one-line summary. Report only what the script prints
(measured output tokens, plus a benchmark-based "(est)" savings figure when
available) — do not recompute or estimate tokens yourself. If the script is not
found (a host without the plugin files), say so rather than fabricating numbers.

On Codex installs the `UserPromptSubmit` hook (`hooks/scrooge-activate.js`)
intercepts the stats trigger and returns the figures directly, so this body
never runs there. It is the path for hosts (e.g. Claude in the editor) where the
hook's block payload is not surfaced to the user.
