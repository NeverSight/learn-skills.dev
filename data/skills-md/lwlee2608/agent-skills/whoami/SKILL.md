---
name: whoami
description: Use when the user asks for the current session's ID (e.g., "/whoami", "what's your session id", "who are you") so another agent session can find or message this one. Works in Claude Code, pi, and OpenCode.
user-invocable: true
---

# Who Am I

Report how another session can reach this one: harness, session ID, working directory, transcript, resume command, PID, and git branch.

## Rules

1. **Read the ID from the environment, never guess it.** Each harness sets it in the shell tool's env:

   | Harness     | Detect by              | Session ID                | Transcript                          | Resume                 | PID             |
   |-------------|------------------------|---------------------------|-------------------------------------|------------------------|-----------------|
   | Claude Code | `CLAUDECODE=1`         | `$CLAUDE_CODE_SESSION_ID` | `~/.claude/projects/*/<id>.jsonl`   | `claude -r <id>`       | `$CLAUDE_PID`   |
   | pi          | `PI_CODING_AGENT=true` | `$PI_SESSION_ID`          | `$PI_SESSION_FILE`                  | `pi --session <id>`    | none            |
   | OpenCode    | `OPENCODE=1`           | none — see rule 2         | none (stored in SQLite)             | `opencode -s <id>`     | `$OPENCODE_PID` |

   Resolve the Claude Code transcript with the glob rather than rebuilding the encoded directory name. Omit any field marked none, and omit the pi transcript when `PI_SESSION_FILE` is unset (ephemeral session).

2. **For OpenCode, take the newest session for the current directory.** OpenCode sets no session-ID env var. Run `opencode session list --format json -n 10` and pick the most recently `updated` entry whose `directory` equals `$PWD`. The live session updates on every turn, so it is usually the newest. If two sessions in this directory updated within the last few minutes, say the ID is ambiguous and list both.

3. **Print only the env vars you need.** Never dump the whole environment; it holds API keys.

4. **Include the working directory and git branch.** Claude Code and pi group sessions by project directory, so another session must resume from it. Omit the branch outside a git repo, and end the branch lookup with `|| true` — git exits 128 there, and harnesses render the whole call as a failure.

5. **Warn against resuming a live session.** Two processes writing one session interleave or fork its history. A live peer should read the transcript; resume only after this session exits.

6. **Reply in this format and nothing else:**

   ```
   harness:    <Claude Code | pi | OpenCode>
   session:    <id>
   cwd:        <absolute path>
   branch:     <git branch>
   pid:        <pid>
   transcript: <absolute path>
   resume:     cd <cwd> && <resume command>  (only after this session exits)
   ```

7. **If no harness matches, say so.** Don't fall back to a made-up ID.
