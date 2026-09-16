---
name: shell-history
description: Search shell history using atuin. Use when the user mentions searching shell history, finding a past command, or recalling a URL or tool invocation from the terminal.
---

## Shell History Search

When the user wants to find something from their shell history, use atuin with timestamps and grep for filtering.

### Standard invocation

```
atuin search --after "<N> days ago" --format "{time} {command}"
```

Default `<N>` is 1.

If the user specifies a day count, use that number instead. Examples that set the day count:

- "search last 2 days of shell history"
- "check 3 days of history"
- "last two days"

This returns all shell commands from the past N days, each prefixed with a timestamp.

### Filtering by keyword

Then grep for the relevant term (URL, tool name, flag, etc.).

Run each command as a separate Bash call — never chain with pipes in a single call.

Step 1: capture history to a temp file in the job directory if one is available, otherwise write to a uniquely named file under /tmp.

Step 2: grep that file for the keyword.

### Expanding the search window

If nothing useful is found with the default 1-day window, expand incrementally: try 2 days, then 3, and so on — up to 7 days before giving up or asking the user for more context.

Report what window you searched each time so the user knows how far back you looked.

### When to use this skill

- User says "check my shell history", "look in my history", "find that command I ran"
- User wants a URL they visited via curl/wget or a tool they ran recently
- User asks what flags or arguments they used for a past command
