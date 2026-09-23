---
name: daily-brief
description: Build a short daily brief from Obsidian vault(s) - recent note changes, weather, new emails, major plans, minor plans, coding tasks. Writes a dated note to "AI System/daily-brief/" and never edits user files. Use whenever user asks for a daily brief, morning brief, "brief me", "what's on my plate", "what's planned today/tomorrow", "what happened in my vault", or when a daily loop or schedule runs it, even if the word "brief" is missing.
---

# daily-brief

Scan recent vault activity. Write one short brief note. Read-only on user files.

## Style

Drop: filler (just/really/basically/actually/simply), pleasantries (sure/certainly/of course/happy to), hedging. Fragments OK. Short synonyms (big not extensive, fix not "implement a solution for"). No tool-call narration, no decorative tables/emoji, no dumping long raw error logs unless asked quote shortest decisive line. Standard well-known tech acronyms OK (DB/API/HTTP); never invent new abbreviations (cfg/impl/req/res/fn) tokenizer split them same as full word: zero token saved, reader still decode. Full word cheaper AND clearer. No causal arrows (→) either own token, save nothing. Technical terms exact. Code blocks unchanged. Errors quoted exact.

## Hard rules

- Never edit, move, rename, delete existing vault files.
- Write only inside `<vault>/AI System/`. Create folder if missing. Files there are AI-owned, overwrite OK.
- Skip `AI System/`, `.obsidian/`, `.trash/` when scanning.
- Loop run (no user to answer): never block. Note missing setup in output, continue.

## Inputs

Resolve in order: user message, `<first vault>/AI System/daily-brief.config.md`, ask user.

- vaults: absolute paths. Default: current dir if it has `.obsidian/`.
- scan: folders holding personal projects, tasks, daily notes. Default: whole vault.
- days: lookback. Default 3.
- city: for weather.
- email: source (Gmail, Outlook, GitHub, other).

Value missing and user present: ask once, batch all questions in one message, save answers to config as `key: value` lines. Next runs reuse config, no re-ask.

## Steps

1. Today's date: run `date +%F`. Never guess.
2. Find recent notes per vault:
   `find "$V" -type f -name '*.md' -mtime -3 -not -path '*/.obsidian/*' -not -path '*/.trash/*' -not -path '*/AI System/*'`
   Sort newest first. Cap 25. Fewer notes fine.
3. Extract, do not read whole notes. Per note grep:
   `grep -nE '^\s*- \[ \]|[0-9]{4}-[0-9]{2}-[0-9]{2}|due::|scheduled::|#(todo|plan|meeting|code|dev)'`
   Read up to 80 lines only when grep hits are unclear. Also note first heading.
4. Weather: use weather tool or web search for city. One line: range, conditions, rain if any. City unknown and no user: `City not set.`
5. Email: check available tools for email (Gmail, Outlook, IMAP, GitHub notifications).
   - Connected: fetch new since yesterday, max 10. Sender, subject, one-line gist. Skip newsletters/promo.
   - Not connected, user present: ask which email. Google mail: suggest Gmail integration. Repo-based work: suggest GitHub. Save answer to config.
   - Not connected, no user: write `Email not connected.`
6. Classify items:
   - Major: dated within 7 days (today/tomorrow first) AND travel, visa, meeting with named person, deadline, event, money, launch. Also anything marked high priority (`#important`, `priority:: high`, Tasks-plugin high marks).
   - Minor: personal errands, small edits, low stakes, no fixed date.
   - Coding: implement/fix/refactor/bug/PR/repo/deploy/test, tags `#code` `#dev`, notes in code project folders.
   Item fits several: highest class wins. Done tasks (`- [x]`) skip, except fold into `Recent:` line.
7. Write brief. Path `<first vault>/AI System/daily-brief/YYYY-MM-DD.md`.

## Format

Use exactly these headers, always, in this order. Empty section keeps header, one line inside.

```markdown
---
generated-by: daily-brief
date: YYYY-MM-DD
---
# Daily brief YYYY-MM-DD
Recent: N notes changed in D days. Main: [[Note A]], [[Note B]]. Done: short list.

## Date and weather
Weekday, YYYY-MM-DD. 14-22 C, clear.

## New emails
- Sender: subject. Gist.

## Major plans
- Tomorrow: Turkey visit. [[Trip note]]

## Minor plans
- Edit contract draft. [[Contracts/Draft]]

## Coding tasks
- Implement export endpoint. [[Projects/API]]
```

Empty text: emails `No new emails.` Others `Nothing planned.`

Rules:
- One line per item. Most urgent first. Max 7 per section, then `+N more`.
- Cite source note as `[[wikilink]]`. Multi-vault: add `(vault-name)`.
- Only facts found in notes/email/weather. No invented plans.

## Reply

User asked interactively: show brief content. Loop run: path only.
