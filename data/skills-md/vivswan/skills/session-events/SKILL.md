---
name: session-events
description: Use when a session needs events from any polled system delivered as messages instead of polls, or when writing the source that polls it, so one daemon the session owns carries each poll's alerts in the peer envelope, keeps its notes in the log, and quotes nothing from the polled system.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: Vivswan
---

# Session Events

One daemon per Claude Code session, started by the session as a background task, polls a system for the targets that session watches, delivers each poll's alerts as one message, and logs every event as a line any agent can read. What it polls is a source: a script of a few lines that says what a target is, how it is read, and what its events say.

Three sources ship in this catalog: the `/watch-github` skill polls GitHub for PRs and branch tips, the `/orchestrator-mode` skill's `fleet-events` polls a fleet's agent transcripts and worktrees, and `scripts/examples/log-source.mts` watches a file's size. A session writes its own source for anything else that must be polled.

Operating envelope: one Claude Code session, one user, the daemon started once by that session, the polled system reachable.

## The Specimen

An agent is waiting on a build that writes `/var/log/build.log`. It starts the daemon on the file source, once per session, as a background task, and one line subscribes the file:

```bash
bun "<skill-dir>/scripts/examples/log-source.mts" daemon --interval 5   # once per session, as a BACKGROUND task
bun "<skill-dir>/scripts/examples/log-source.mts" watch /var/log/build.log
```

The session goes back to work. The build appends a line, and the next poll delivers this frame to the session's inbox, which renders it as a message from `log-events`:

```text
<cross-session-message from="uds:/run/user/1000/session-events/4242.log-events.sock" from-name="log-events" from-mode="bypass">
/var/log/build.log: 0 to 1097 bytes
file:///var/log/build.log
automated notice from log-events; no reply needed
</cross-session-message>
```

No turn was spent on "nothing changed yet". The source wrote the kind, the text, and the URL. The daemon wrote the rest: the envelope naming the sender, the closing line, the log line, and the saved state the next poll resumes from. The whole source is [`scripts/examples/log-source.mts`](./scripts/examples/log-source.mts):

```ts
import { statSync } from "node:fs";
import { runEvents, UsageError } from "../session-events.mts";

/** The cursor: the size at the last poll, null before the file has been seen or while it is gone. */
type File = { path: string; size: number | null };

runEvents<File>({
  name: "log-events",
  interval: 5,
  usage: ["targets: the absolute path of a file; an event when its size changes or it disappears"],
  parseTarget([path, ...rest]) {
    if (path === undefined || !path.startsWith("/"))
      throw new UsageError("watch needs an absolute path");
    if (rest.length > 0) throw new UsageError(`unknown option: ${rest[0]}`);
    return { path, size: null };
  },
  async poll(targets) {
    const events = [];
    for (const file of Object.values(targets)) {
      const size = statSync(file.path, { throwIfNoEntry: false })?.size ?? null;
      const url = `file://${file.path}`;
      if (size === null && file.size !== null) {
        events.push({ kind: "gone", text: `${file.path}: gone`, url });
      } else if (size !== null && file.size !== null && size !== file.size) {
        events.push({ kind: "changed", text: `${file.path}: ${file.size} to ${size} bytes`, url });
      }
      file.size = size;
    }
    return { events, busy: events.length > 0 };
  },
});
```

## When to Apply

- A session is waiting on something outside it that has to be polled: a build log, a queue, a deployment, a ticket. One daemon polls; the session keeps working and reads the messages.
- PRs, branch tips, and CI: the `/watch-github` skill, a source of this daemon with its own page. Start there, not here.
- Writing a source: the contract below, with the file source as the worked example.

## The Source Contract

A source script imports `runEvents` from `scripts/session-events.mts` and calls it at top level with one object; `runEvents` reads the process's arguments and runs the whole CLI for that source. Four fields and three optional:

| Field | The file source says | The daemon uses it for |
| --- | --- | --- |
| `name` | `"log-events"` (`[a-z0-9-]{1,40}`) | the file stems, the envelope's `from-name`, the `msg_id` prefix, the closing line |
| `interval` | `5` | seconds between polls while busy, and the default of `--interval`; floor 1, cap 86400 |
| `idleInterval` (optional) | not set, so `5` | the longest wait between polls; a quiet poll doubles the wait from `interval` up to it |
| `usage` (optional) | one line: the target is an absolute file path | the lines `--help` ends with: the target's forms and the source's own flags |
| `parseTarget(args)` | the path, refused unless absolute | `watch <target> [flags]`: the arguments after `watch`, the target text first; throws `UsageError` for exit 2 |
| `poll(targets, io)` | stat each file, compare with its saved size | every poll: the events, and whether anything is still moving |
| `summary(target)` (optional) | not set, so the target line stands alone | `status`: the lines printed under each target, what stands right now (a standing alert each) |

The daemon keeps `targets`, a map from the text the user typed to the object `parseTarget` returned, and saves it after every poll. A source writes its cursor onto each target object: the file source keeps the last size there. The daemon adds nothing else to the state but the event counter.

An event is `{ kind, text, url }` plus any field the source adds; the daemon prepends `id` and `at`. The log line is `{"id":17,"at":"2026-10-12T14:03:20Z","kind":"changed","text":"/var/log/build.log: 0 to 1097 bytes","url":"file:///var/log/build.log"}`.

One added field the daemon reads: `level`, either `alert` (the default: delivered as a message) or `note` (numbered, logged, counted, shown by `wait` and `status`, never delivered), so a source says what is wrong as alerts and keeps the rest readable as notes.

Rules a poll keeps:

- **It returns, it does not stream.** The events come back in one array; the daemon numbers and stamps them, appends them to the log, saves the state, then delivers.
- **It writes cursors on the way to returning.** A poll that throws is a failed poll: the daemon logs the reason and saves nothing, so a source that moved a cursor before throwing would skip what the cursor passed.
- **`busy` says which interval comes next.** True while something is pending or an event just happened, and the next poll comes after `interval`; false doubles the wait, up to `idleInterval`.
- **Text is the source's own words.** Identifiers, counts, states, URLs: never a line quoted from the polled system (below).

## Commands

Every source runs the same commands. The file source's `--help` (`<source.mts>` elsewhere on this page is your own source script):

```text usage=skills/session-events/scripts/examples/log-source.mts
usage: log-source.mts <command> [options]
  daemon [--interval <s>] [--mode bypass|prompting] [--id <name> [--pid <pid>]]
  watch <target> [the source's flags] [--id <name>]
  unwatch <target> | --all [--id <name>]
  wait [--since <id>] [--timeout <s>] [--id <name>]
  poll | status | stop [--id <name>]
the daemon serves the Claude Code session named by CLAUDE_CODE_MESSAGING_SOCKET and exits with it;
--id <name> names a file-sink daemon for a non-Claude agent instead, --pid <pid> ends it with that process;
--mode is the session's permission mode, carried in the envelope: bypass (the default) or prompting;
--interval is 5 s by default, 1 to 86400
targets: the absolute path of a file; an event when its size changes or it disappears
files: <dir>/<pid>-<start>.log-events.{state.json,events.jsonl,log} and <dir>/<pid>.log-events.sock for a session; <id>.log-events.* for a file sink;
  <dir> is $SESSION_EVENTS_DIR, else $XDG_RUNTIME_DIR/session-events, else $CLAUDE_CODE_TMPDIR/session-events-<uid>, else <os tmpdir>/session-events-<uid>, else /tmp/session-events-<uid>
prints: one message per poll with alerts, wrapped in <cross-session-message from="uds:<socket>" from-name="log-events" from-mode="<mode>"> and ending "automated notice from log-events; no reply needed";
  wait prints the new events as JSON lines, then cursor: <id>
exits: 0 ok (stop with no daemon running, and a second daemon start, are ok too); 2 usage, a state file that is not JSON, or no runtime directory;
       3 no daemon answers for this session: stderr names the socket and the background command that starts one; 4 wait only: the timeout passed with no newer line
```

| Exit | Meaning |
| --- | --- |
| 0 | ok; `stop` with no daemon running is ok too, and so is a second `daemon` start, which says the first is up |
| 2 | usage (`CLAUDE_CODE_MESSAGING_SOCKET` unset and no `--id`, a bad `--id`, `--pid` without `--id`, `--interval` off the scale, a target the source refuses), a state file that is not JSON, or no runtime directory |
| 3 | no daemon answers for this session: stderr names the socket and the exact background command that starts one |
| 4 | `wait` only: the timeout passed with no newer line |

`watch` saves the target and polls at once, so it returns after that poll. A second `watch` of the same text replaces the target, cursor included. `poll` runs one poll now, for tests and debugging. `--interval` moves the busy interval; the idle one never drops below it. `--mode` is the session's permission mode (below), `bypass` by default.

## The Envelope and the Text

A frame to a session's inbox is user-role text: the same channel the owner types in, with no data channel. Two rules follow.

- **The envelope names the sender and its mode.** The daemon wraps every message in `<cross-session-message from="uds:<socket>" from-name="<source name>" from-mode="<mode>">` ... `</cross-session-message>`, with `from_mode` on the frame too; measured against the other frame shapes, this is the one the client renders as a named sender. The attribute values escape `&`, `"`, `<`, and `>`.
- **The mode is the session's permission mode.** A session that bypasses permission prompts is `bypass` (the default); one that asks is `prompting`. The receiver holds a frame whose mode does not match its own, so start the daemon with the mode of the session it serves.
- **Nothing in the text is quoted from the polled system.** A comment body or a log line in a message would read as something the owner wrote, so a source never puts one there: it says what moved and where (an identifier, a count, a state, a URL). An identifier that spells the closing tag gets a space before its bracket; nothing else in the body is rewritten.

The daemon is the session's own child, so its frames are delivered with no permission hold, and it exits on its own when the session does. Started detached (`nohup`, `setsid`, `disown`, a shell that exits), it is a cross-session sender and every message is held (Gotchas below).

One poll's alerts are one message, at least 1.1 s after the one before, since the receiver drops a second frame from one sender within a second, and its notes stay in the log. The alerts are separated by a blank line, each its text and its URL, and the message ends `automated notice from <name>; no reply needed`.

## Lifecycle

```text
start     the session runs `daemon` as a background task; the owner is the session whose inbox
          CLAUDE_CODE_MESSAGING_SOCKET names
one only  binding `<runtime-dir>/<pid>.<source>.sock` is the rule: a second start finds the first
          answering and exits 0; a socket file nobody answers on was left by a crash and is removed
          once; two sources of one session are two daemons
poll      every `interval` seconds while busy; each quiet poll doubles the wait, up to `idleInterval`;
          at once on `watch`, and on a restart with saved targets; each poll that returns is a log
          line with its event count and the next wait
trouble   a failed poll is a log line; three in a row are one event, `<name>: the last 3 polls
          failed; read the daemon log for the reason`, with the log's path as its URL, and nothing
          more until a poll succeeds and three fail again
stop      the owner's pid gone (checked every second and before each poll): finish the poll in
          flight, save, unlink the socket, exit; `stop`, SIGTERM, SIGINT: the same at once
```

**The two-hour cap.** Claude Code ends a background task after two hours, the most it allows; the log then ends `daemon <pid> stopped: SIGTERM` with the session still running. Start the daemon again with the same command: the saved targets carry on, the restart polls at once, and the events keep their numbering.

**A crash.** The log is appended before the state is saved, so a daemon killed between the two restarts from cursors a poll behind and reads that poll again: at most one poll is delivered twice, and none is lost. A daemon killed before delivering leaves the events in the log, where `status` and `wait` read them.

## Files

The runtime directory, tried in this order. Each must be creatable as a private directory (mode 0700, owned by the user) or the next is tried; none at all exits 2 asking for `SESSION_EVENTS_DIR`.

| Tried | When |
| --- | --- |
| `$SESSION_EVENTS_DIR` | set, as an absolute path |
| `$XDG_RUNTIME_DIR/session-events` | `XDG_RUNTIME_DIR` set |
| `$CLAUDE_CODE_TMPDIR/session-events-<uid>` | `CLAUDE_CODE_TMPDIR` set |
| `<os tmpdir>/session-events-<uid>` | the OS temp dir, honouring `TMPDIR` |
| `/tmp/session-events-<uid>` | the last resort |

| File | Holds |
| --- | --- |
| `<pid>.<source>.sock` | the control socket, also the daemon's `from` address |
| `<pid>-<start>.<source>.events.jsonl` | the events log, one line per event, appended before the state is saved |
| `<pid>-<start>.<source>.state.json` | the targets with their cursors and the event counter, written tmp-then-rename |
| `<pid>-<start>.<source>.log` | the daemon's log; the first place to read when something is off |

`<start>` is the session's start token (its process start time from `/proc`, or its inbox socket's inode where there is no `/proc`). A later session that happens to get the same pid opens other files and starts from an empty state; nothing compares owners. A file-sink daemon (below) names its files `<id>.<source>.` instead.

## Without a Claude Code Inbox

Codex, the Copilot CLI, a shell, or a Claude Code session with no `CLAUDE_CODE_MESSAGING_SOCKET` names a file-sink daemon with `--id` and reads the log instead of receiving messages. Start the daemon as that agent's own background job, then block on `wait`:

```bash
bun "<source.mts>" daemon --id codex-12
bun "<source.mts>" watch <target> --id codex-12
bun "<source.mts>" wait --id codex-12 --since 0 --timeout 540
```

A file-sink daemon runs until `stop`. `--pid <pid>` ends it with that process instead: pass the agent's own pid, never `$$` from a one-shot shell, which becomes the daemon's own pid when the shell execs it (the daemon refuses its own pid).

`wait` blocks in the foreground with a timeout under the tool's own cap, and prints the new lines and `cursor: <id>` on exit 0; pass that cursor as the next `--since`. Exit 4 is the timeout with nothing new: re-arm. Exit 3 is the daemon gone: start it again, then re-arm.

In a fleet, the lead's session runs the daemon as its own background task, with `--mode` matching the session, and watches on behalf of everyone; a builder never runs `watch` there. The lead forwards a line to a builder by one message when it wants that builder to act. The file sink is for non-Claude agents only.

## Gotchas

| What you see | What it means | What to do |
| --- | --- | --- |
| held delivery notices in the session instead of the event text | the daemon runs detached (`nohup`, `setsid`, a shell that exited), so it is a cross-session sender | `stop`, then start it again as a background task of this session |
| `watch` exits 3 naming a socket and a command | no daemon for this session and source | run the printed command as a background task, then `watch` again |
| exit 2: `CLAUDE_CODE_MESSAGING_SOCKET` is unset | not a Claude Code session, or one without an inbox | a file-sink daemon with `--id`, and `wait` (above) |
| a `trouble` event naming the daemon log | three polls in a row failed; the daemon keeps polling | read the log; fix what it names (the polled system, credentials, the network) |
| the log ends `daemon <pid> stopped: SIGTERM` about two hours after the start, with the session still running | the harness's two-hour cap on a background task | start the daemon again with the same command; the saved targets carry on |
| a message arrives twice | the daemon was killed between appending the log and saving the state, and the restart read that poll again | nothing; at most one poll repeats |

A local subagent spawned with the Agent tool shares its session's inbox socket and pid (`CLAUDE_CODE_MESSAGING_SOCKET` and `CLAUDE_PID` are the session's, with `CLAUDE_CODE_CHILD_SESSION=1`), so a `watch` run inside it reaches the session's daemon, and the events land with the session. A teammate from agent teams is a separate process with its own socket and runs its own daemon.
