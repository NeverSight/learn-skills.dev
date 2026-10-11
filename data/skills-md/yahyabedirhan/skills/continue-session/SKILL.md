---
name: continue-session
description: Continue another session's work by reading its transcript, without sending it input. Use when the user asks to continue, pick up or take over from another session, named by its session id or by where it sits in the session host.
argument-hint: "<session id> or its place, such as \"top pane\", \"right tab\" or \"another workspace\""
---

# Continue session

Continue another session's work as a **silent reader**: read its transcript, then do the work in this session. Send the other session no text, keys, prompts or messages, and leave it unresumed: any input wakes it and re-sends its long, uncached history.

## Parameters

- `<session-host>`: where agent sessions run, e.g. `herdr`, Claude Code Desktop, Codex Desktop.

## 1. Find the session

- **When the user gives a session id:** use it.
- **When the user gives a place,** such as "top pane" or "left tab": start from this session's own place, find the target with the session host's read-only commands, and read the session id of the agent there.
  - **When the place is a scope,** such as "another workspace": list the agent sessions in it, leave out this session and the shell panes, and pick by title, working directory and status. Ask the user only when more than one still fits.
  - **When the host reports no session id:** take the newest transcript of that pane's harness whose working directory matches the pane's.

The read-only commands per session host:

- **`herdr`:**
  1. Find this pane: `herdr pane current --current`.
  2. Find the target pane: `herdr pane neighbor --pane <this pane> --direction <up|down|left|right>` for a neighbour, or `herdr pane list` and `herdr tab list` for one farther away.
  3. Read the target's session id: the `agent_session` field of `herdr pane get <target pane>`.

## 2. Read the transcript

Find the transcript on disk, where the session's harness stores it:

- **Claude Code:** `~/.claude/projects/<project>/<session-id>.jsonl`, where `<project>` is the working directory with `/` and `.` turned into `-`.
- **Codex:** under `~/.codex/sessions/`.

Start with the last couple of messages, since they usually say where the session left off. Then search the rest rather than reading it whole: the user's requests, the latest tool results and any open decision. Then check the working directory's branch, uncommitted changes and pull requests.

Read on until you can state the goal, what is done, what was in progress when it stopped, and the next step.

## 3. Continue

Give the user that recap in a few lines, then continue the work here, in the session's working directory.

- **When the other session is still working:** tell the user and wait for their word, since two sessions editing one worktree overwrite each other.
