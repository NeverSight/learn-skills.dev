---
name: slack-cli-read
description: Access Slack through the global `slack` CLI for read-only workflows. Use when asked to list chats or DMs, read message history, inspect threads, fetch exact messages, or summarize recent Slack activity.
---

# slack-cli-read

Use this skill to read Slack content via the global `slack` command.

## Scope

- Read-only commands are supported.
- Writing/sending/replying is not implemented yet. If asked to write, state that it is not available yet and offer to draft message text only.

## Environment

- Assume `slack` is available as a global command.
- Slack credentials are expected at `~/.config/slack/slack.env`.
- Required variables:
  - `SLACK_WORKSPACE`
  - `TOKEN`
  - `D_COOKIE`
- If auth fails or env vars are missing, help the user populate that file.

## Command Map

- Login bootstrap (interactive): `slack auth login <workspace>`
- Auth diagnostics: `slack auth status`
- Verify auth/workspace: `slack me`
- List all conversations: `slack chat list`
- List unread conversations: `slack chat list --unread`
- List DM inbox: `slack dm list`
- List unread DMs: `slack dm list --unread`
- Read chat history: `slack chat history "<chat>" --limit 30`
- Read DM history: `slack dm history <user_or_dm_id> --limit 30`
- Read full thread: `slack thread show <chat_or_dm> <thread_ts>`
- Read one full message: `slack chat message <chat_or_dm> <ts>`
- Search users: `slack users list --query <text>`
- Raw API call (expert mode): `slack api call <endpoint> -p key=value`
- Raw API curl wrapper (expert mode): `slack api curl <endpoint> -- [curl args]`

## Working Style

1. Start broad with `chat list` or `dm list` when intent is vague.
2. Narrow into history with a bounded `--limit`.
3. Expand parent threads via `thread show` when inline replies are truncated.
4. Fetch exact messages with `chat message` when full text is needed.

## Command Hygiene

- Quote names starting with `#` in shell commands, for example: `slack chat history "#general"`.
- Prefer IDs when names are ambiguous.
- Keep commands bounded with `--limit` unless the user asks for more.
- Use pretty output for human reading.
- Use `--format json` or `--format jsonl` for structured parsing.
- Use `slack api call`/`slack api curl` only when typed commands do not cover the needed endpoint behavior.
- If auth fails, run `slack auth status` before retrying read commands.

## Response Guidance

- Summarize key findings instead of dumping raw command output.
- Keep timestamps and IDs in results when they help the user drill down.
- Treat attachment lines (`📎 ...`) as message context.
