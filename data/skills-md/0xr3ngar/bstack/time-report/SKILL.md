---
name: time-report
description: "Estimate active work time from local Claude Code, Cursor, Codex, and Pi conversations and attribute it to tickets and PRs. Optionally log the hours to Jira. Use for 'how much time did I spend yesterday', 'find my conversations and how long they took', 'log my hours', morning time reports."
license: MIT
compatibility: "Requires Bun 1.4 or newer and local Claude Code, Cursor, Codex, or Pi transcripts. GitHub CLI and Jira access are optional."
---

# Time report

Estimate active work time per ticket from conversation history. These estimates describe gaps between recorded messages, not continuous observation of the user. The default range is yesterday.

## 1. Scan the conversations

First locate the user's transcript files. Check the agent's configuration, environment, and any paths the user supplied. Verify that the directories contain session JSONL files; do not assume the defaults exist or contain the history the user wants. If locations remain unknown, report which paths you checked and ask only for the missing location. Complete the report for sources you can read.

Run [the scanner](scripts/scan-sessions.ts) with Bun 1.4 or newer:

```bash
bun <skill-dir>/scripts/scan-sessions.ts --since YYYY-MM-DD --until YYYY-MM-DD
```

Both dates are local midnights and `--until` is exclusive. With no flags it scans yesterday. Use the requested range, or yesterday even on weekends. State the dates in the report. Ask about the working calendar only when the requested range depends on it.

Likely locations, also used as the scanner defaults:

- Claude Code: `~/.claude/projects/*/*.jsonl`
- Cursor: `~/.cursor/projects/*/agent-transcripts/**/*.jsonl`
- Codex: `~/.codex/sessions/**/*.jsonl` and `~/.codex/archived_sessions/**/*.jsonl`
- Pi: `~/.pi/agent/sessions/**/*.jsonl`

For files stored elsewhere, pass the verified directory with `--transcripts SOURCE=DIR`. This replaces the defaults for that source and searches the directory recursively. Repeat the option to include multiple directories, including any separate archive:

```bash
bun <skill-dir>/scripts/scan-sessions.ts --since YYYY-MM-DD --until YYYY-MM-DD \
  --transcripts "codex=/path/to/sessions" --transcripts "pi=/another/path/sessions"
```

An empty result does not prove there was no activity. Confirm the locations and requested dates before drawing that conclusion.

Codex and Pi use the working directory in the session header as the project. It prints UTC timestamps in one JSON line per conversation with `source`, `project`, `file`, `start`, `end`, `active_seconds`, `first_prompt`, `tickets` with each key and its first mention time, and `pull_requests`.

Conversations with less than one minute of estimated activity are omitted. Use `--home PATH` to scan these paths under another home directory and `--gap-minutes N` to change the idle threshold. Bun downloads the pinned Zod dependency on first run. Later runs use its local cache.

Active time is the sum of the gaps between messages that are shorter than 15 minutes. Longer gaps count as time away. Cursor timestamps user messages to the minute. The scanner uses the last write time as the final edge when it follows those messages. It does not use filesystem creation times.

## 2. Attribute time to tickets

- A conversation lists every ticket key it mentions, including keys it only read about. Open the transcript near each key's first mention and keep only the tickets the user actually worked on in that conversation (planned, implemented, opened or fixed a PR).
- When one conversation covers several tickets, split its active time by the stretch spent on each ticket if the transcript makes that clear. If the split is unclear, keep the time unattributed and explain why. Do not turn a guess into billable hours.
- Check for overlapping parent and subagent conversations. Count overlapping intervals once; a separate file or worktree does not establish separate human work time.
- If a ticket has no conversation, say so. Don't invent time.

## 3. Look up PR state and waiting time

For each ticket with a PR, get the open and merge times:

```bash
gh pr view <number> --repo <owner/repo> --json createdAt,mergedAt,state
```

If GitHub access is unavailable, report the conversation estimates and say that PR state was not checked.

PR waiting time runs from open to merge. It is elapsed time, not work performed. Show it separately when useful. Do not add it to active work time or log it to Jira. Keep conversation activity after PR creation, since review fixes are work too.

## 4. Show the report

Show a table with the ticket, PR state, estimated active work time, and optional PR waiting time. Round displayed work estimates to minutes. Do not imply second-level accuracy from Cursor's minute-level timestamps.

Include unmatched conversations with their first prompts and estimated activity. Deliver the useful report without waiting for the user to classify every row. State any assumptions about overlapping sessions or ticket attribution.

Stop here unless the user asked to log the hours.

## 5. Log to Jira when asked

Use allocations and hours the user already approved. If the report introduced unapproved estimates or uncertain allocations, show the proposed entries and ask for those details before writing. Do not request the same approval twice. Jira access is required; if it is unavailable, return the report and identify what remains unlogged.

- Log only the approved active work estimate, rounded to the nearest whole minute. Set `started` to the first activity.
- Include a concise source and rounding note in the worklog description. Keep local transcript contents private. Do not add a separate ticket comment unless asked.
- Move a ticket to Done only if its PR is merged and the user asked for that transition.
- Check existing worklogs before writing. Skip entries that already match; update only entries covered by the request. After a failed write, read the remote state before retrying to avoid duplicates.
- Verify the saved entries and report what was logged, skipped, or blocked. A successful tool call alone is not proof of the saved hours.
