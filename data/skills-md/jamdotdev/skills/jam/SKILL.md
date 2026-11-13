---
name: jam
description: Route a Jam (a jam.dev screen recording or screenshot with the console, network and user actions attached) to the right Jam skill. Use when the user shares a jam.dev link with no clear ask ("look at this jam", a bare link), or types /jam. For a clear ask (fix, test, ticket, record, annotate), use that skill directly.
---

# jam

Read the request, pick one skill below, and load it with your skill tool
(the Skill tool in Claude Code, `$name` in Codex), not by opening its file,
so its references and scripts resolve. Do not do the work from this file;
the target skill holds the steps. Say which skill you picked in one line
before you start.

## Route by what was asked

| The user wants | Load |
| --- | --- |
| the cause of a bug, a fix, triage, "what went wrong" | `jam-fix` |
| an e2e test, a regression test, a repro | `jam-to-e2e` |
| the changes they narrated done ("do what I said", "make it look like this") | `jam-to-tasks` |
| a ticket in Linear, GitHub Issues or Jira, or whether one exists | `jam-to-ticket` |
| a recorded Jam of their change working, a shareable demo video | `jam-proof` |
| a screenshot marked up and shared as a Jam | `jam-annotate` |
| one table of claims and the Jam that shows each | `jam-proof-table` |
| a video file they already have turned into Jams | `video-to-jam` |
| Jam set up for this agent: the CLI, sign-in, Jam MCP, the skills | `jam-setup` |
| a polished, narrated demo video of a feature | `record-demo` |
| a spoken voiceover on a video | `add-voiceover` |
| a terminal run recorded as a GIF for the pull request | `record-terminal-proof` |

Several asks in one request ("fix it and file a ticket"): run the skills in
the order asked, and pass what the first one found to the next.

## A Jam link with no clear ask

Read the Jam's details first: the `getDetails` MCP tool, or
`jam get jam <id> --json`. For a video with the mic on (`micEnabled`), read
the transcript too (`getVideoTranscript`, or `jam get transcript <id> --json`):
the spoken asks are there, and a title like "Feedback" says nothing about
them. If captions are not ready, wait a minute and retry once, then route on
the details and say so. Then route by what it holds:

- Several changes asked for, in the narration or in the title, description
  or comments of a silent Jam: `jam-to-tasks`.
- One bug, an error, or a failed request: `jam-fix`. It diagnoses without
  changing code, so it is the safe default.
- Neither is clear: ask one question that names the options in plain words
  ("fix it, write a test for it, or file a ticket?").

## Nothing matches

For anything else about Jams (list, search, comment, move to a folder),
use the Jam MCP tools or the `jam` CLI directly. `jam agent-context` prints
every command.

## Send feedback to Jam

When this skill, a Jam MCP tool, a `jam` command or a Jam doc was wrong,
stale or confusing, or worked unusually well, tell Jam. Send it yourself:
Jam's agents read it, so it needs no approval.

Call the `submitFeedback` MCP tool with `body`, `category` and `subject`.

When MCP is unavailable, use the CLI:

```bash
jam feedback "<what you were doing, what you expected, what happened, the mistake>" --category <skills|mcp|cli|docs> --subject <skill name, tool name or command>
```

- Jam surfaces only, not the user's code or other tools.
- At most once per session, and never for a slip you corrected yourself.
- No secrets, customer data, source code, stack traces or recording content.
