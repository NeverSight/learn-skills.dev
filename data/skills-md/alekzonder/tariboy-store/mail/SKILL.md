---
name: mail
description: Use when a letter arrives under Messages in the iteration prompt, or when sending, replying to, inspecting or recovering Tariboy mail with tmail.
---

# Tariboy Mail

**REQUIRED:** Use `cli-text` before passing text to this CLI. Keep the storage
rules below; quote transport separately. Resolve skill-local launchers relative
to this skill directory, not the current working directory.

This skill's `scripts/mail.sh` launcher lives inside this skill directory and
hands all its arguments to `tmail`, which the daemon puts on the agent PATH.
`tmail` acts as you through `TARIBOY_TOOLS_SOCKET`: you are the sender of
every letter you write, and you read only your own mailbox. Execute the
command when command execution is available. If it is unavailable, return the
exact command instead; never claim a letter was sent or answered unless the
command succeeded. `tmail --help` and `tmail COMMAND --help` are authoritative
for flags.

## Letters you receive

Letters arrive inline in the iteration prompt under "Messages", each with its
own id, sender (`from`), kind and subject: requests first, notices after them.

| Letter | What closes it |
| --- | --- |
| A request | Your one `tmail reply ID TEXT`. Unanswered, it is shown again next iteration and dead-lettered after 5 attempts |
| A notice | Nothing: it closes by itself when this iteration finishes. Send no reply and run no command for it |
| A `task.question` request | Your answer on the task with `ttasks comment KEY TEXT` (the letter's `answer:` line names it), never by mail. The letter then closes itself |
| A request from a `system:*` sender (`system:goal`, `system:scripts`, `system:schedule`) | Your `tmail reply ID TEXT`. It is your agent report: nobody reads it, so it states what you did and the result, never a bare `ok` or `done` |

A reply goes only to the sender of the letter and is a notice. Add `--ask`
when the reply asks something back: `tmail reply ID TEXT --ask` makes it a
request that the sender must answer.

A letter from a task's customer that answers your open question on that task
or approves your plan is handled by the `tasks` skill's "Answers from a
letter": record it on the task before acting on it.

Finish the work first, then send once. Before any notification, request or
reply, complete the reading, commands and checks its text depends on; only then send one message that closes the request completely. A
fact you cannot establish belongs in that same text as a named unknown
together with what would settle it. Never send a provisional or placeholder
text and never promise a corrective follow-up. A blocked sender, a deadline,
brevity, and a request to answer now and correct afterwards do not authorize
one; that request is answered by one finished message that names whatever is
still running. Send again only for new external state, or to correct an error
already sent.

## Commands

- Reply and close: `tmail reply ID TEXT [--ask]`; a TEXT of `-` reads it from
  stdin.
- Send: `tmail send --to PRINCIPAL[,PRINCIPAL] --subject S --text T
  [--deadline 5m] [--notice]`. A principal is `agent:NAME`, `user:LOGIN`,
  `group:NAME` or `plugin:NAME`; one comma-separated `--to` writes one letter
  to each. The letter is a request unless `--notice`; `--deadline` sets when
  you expect the answer. `--text -` reads the body from stdin.
- Inspect: `tmail inbox [--all]` (open letters, oldest first), `tmail sent`,
  `tmail archive` (closed letters, dead ones tagged `dead:REASON`),
  `tmail show ID` (one letter and its reply).
- Recover: `tmail requeue ID` puts a dead letter back into your inbox.

`close`, `read`, `unread` and `clear` are operator-only: an agent answers a
letter instead of archiving it.
