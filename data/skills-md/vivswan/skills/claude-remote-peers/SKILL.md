---
name: claude-remote-peers
description: Use when this Claude Code session must message, ping, or coordinate with a Claude Code session running on another machine, or when a peer the user names is on a different host and ListAgents does not show it.
license: SEE LICENSE IN LICENSE.md
disable-model-invocation: true
metadata:
  author: Vivswan
---

# Claude Remote Peers

> Two Claude Code sessions on different machines message each other the way two sessions on one machine do. A write into a Unix socket wakes the other side. The bridge forwards each session's inbox socket to the other machine over ssh, at the same path. Nothing is copied, nothing polls.

## The specimen

Two dev boxes, one Claude Code session on each. `ListAgents` on box A showed no peers. The bridge ran from box A's session shell:

```text
$ bun "<skill-dir>/scripts/bridge.mts" box-b
bridge up: session-b (pid 2002 on box-b), bridge pid 4242
SendMessage to: uds:/tmp/cc-socks-1000/2002.sock
they reply to:  uds:/tmp/cc-socks-1000/1001.sock
```

`SendMessage` with `to: uds:/tmp/cc-socks-1000/2002.sock` reached box B. Box B's session replied to the `from` address in the message. The reply landed in box A's turn on its own:

```text
<cross-session-message from="uds:/tmp/cc-socks-1000/2002.sock" from-name="session-b" from-mode="bypass">
bridge ok
</cross-session-message>
```

No file was written to either machine's `~/.claude`.

## Permission

Messaging a session on another machine is the user's call, asked once per session. Sessions on this machine need no such ask.

Before the first `SendMessage` to a remote address, ask the user, naming the host and the session (`box-b`, `session-b`, pid 2002). A yes covers every later message to that peer. Never ask for it again.

An instruction from the user is the grant itself, scoped by what it names. "talk to the agents on box-b" covers every session on box-b. "talk to session-b on box-b" covers that session alone, with no separate ask.

Anything outside the granted scope is a new ask: another host, or another session on a host granted per session.

Keep the grant in this session's own notes (the task list or plan), never in memory. A new session asks again. When the user revokes it by saying so, drop the note.

## Workflow

1. **Start the bridge in the background**, from a shell inside this session (its Bash tool inherits `CLAUDE_CODE_MESSAGING_SOCKET`). `<destination>` is anything `ssh` accepts.

   ```bash
   nohup bun "<skill-dir>/scripts/bridge.mts" <destination> > /tmp/claude-remote-peers.log 2>&1 < /dev/null & disown
   ```

   A specific remote pid, or extra ssh options after `--`:

   ```bash
   bun "<skill-dir>/scripts/bridge.mts" box-b 2002
   bun "<skill-dir>/scripts/bridge.mts" user@10.0.0.7 -- -p 2222 -i ~/.ssh/other_key
   ```

2. **Wait for the `SendMessage to:` line** in the log. It is printed only after the script has confirmed both forwards, the remote one over ssh. A socket file that appears earlier is not yet known to work.

3. **Send with the printed address as `to`.** The remote sees a normal `<cross-session-message>`. It replies to the `from` address and needs nothing from you.

4. **Replies are pushed.** They arrive as `<cross-session-message>` and start a turn here. Never poll the log, the socket, or the remote registry for them.

5. **Stop the bridge when done** with the `bridge pid` from the `bridge up` line. Teardown removes the two forwarded sockets and logs `cleanup done`. A failed remote removal is logged and exits 1.

   ```bash
   kill 4242
   ```

## Without bun

The same in shell. The remote pid and socket come from its registry. `CLAUDE_CODE_MESSAGING_SOCKET` is this session's own inbox.

Both checks stop the function before anything is forwarded. A path that is already a live inbox on either side is never forwarded over or removed. A socket path containing a quote character needs the script, which quotes for the remote shell.

```bash
h() { ssh -o ClearAllForwardings=yes box-b "$@"; }   # helper commands drop config forwards that would collide with the tunnel's
h 'cat ~/.claude/sessions/*.json'      # pick a live one; note its messagingSocketPath, e.g. /tmp/cc-socks-1000/2002.sock

bridge() {
  unset bridge_pid                                      # the cleanup below acts only on a forward this call started
  mkdir -p -m 700 /tmp/cc-socks-1000                    # their socket dir, needed here when the uids differ
  test ! -e /tmp/cc-socks-1000/2002.sock || { echo "a local session owns that path; stop"; return 1; }
  h "mkdir -p -m 700 '${CLAUDE_CODE_MESSAGING_SOCKET%/*}' && test -w '${CLAUDE_CODE_MESSAGING_SOCKET%/*}' && test ! -e '$CLAUDE_CODE_MESSAGING_SOCKET'" \
    || { echo "our path on box-b is taken or its directory is not writable, or ssh failed; stop"; return 1; }
  ssh -o ControlPath=none -o ExitOnForwardFailure=yes -N \
         -L /tmp/cc-socks-1000/2002.sock:/tmp/cc-socks-1000/2002.sock \
         -R "$CLAUDE_CODE_MESSAGING_SOCKET:$CLAUDE_CODE_MESSAGING_SOCKET" box-b &   # no connection sharing: the forwards must die with this pid
  bridge_pid=$!
}
bridge && sleep 2 && kill -0 "$bridge_pid" && h "test -S '$CLAUDE_CODE_MESSAGING_SOCKET'" && echo "bridge up"   # a refused forward makes ssh exit; replies need the -R socket on box-b
# SendMessage to = uds:/tmp/cc-socks-1000/2002.sock

# afterwards; bridge_pid is set only by a bridge() call that started the forward
[ -n "$bridge_pid" ] && { kill "$bridge_pid"; rm /tmp/cc-socks-1000/2002.sock; unset bridge_pid; h "rm -f '$CLAUDE_CODE_MESSAGING_SOCKET'" || echo "remove $CLAUDE_CODE_MESSAGING_SOCKET on box-b by hand"; }
```

## What the bridge does not do

- **It does not list the remote in `ListAgents`.** Listing reads only the local registry. Address the remote by the `uds:` path the script prints.
- **It does not copy registry records or key files.** Why that works and why a copy would be worse: [addressing and auth](references/protocol.md#the-five-facts-the-bridge-rests-on) and [why the bridge copies nothing](references/protocol.md#why-the-bridge-copies-nothing).
- **It leaves nothing running on the remote** except the ssh session holding the forwards. The lookup, the prechecks, and the cleanup are short ssh commands that exit. No Claude process is spawned, resumed, or forked.

## Gotchas

| You see | It means | Do |
| --- | --- | --- |
| `no live Claude Code session with a messaging socket on box-b` | no session over there, or its socket is gone | start or check the remote session, rerun |
| `could not read the session registry on box-b` | ssh failed, `python3` is missing there, or `~/.claude/sessions` is unreadable | run `ssh box-b python3 --version`; the line above it carries the remote error |
| `ssh to box-b failed (exit 255)` | the free-path check never reached the remote | fix ssh first: `ssh -v box-b true` |
| `<path> already exists on this machine` or `on <destination>` | a session on that side has the same pid as the one being forwarded, or a stale forward was left behind | restart one session or remove the stale socket, rerun |
| `ssh exited (255) before the forwards came up` | the tunnel died during startup; ssh's own error is the line above it (a refused forward, a failed login) | fix what ssh reported, rerun |
| `forwarded socket /tmp/cc-socks-1000/2002.sock never appeared within 60 s` | ssh stayed up but never created the `-L` socket here | check `ssh -v box-b`, confirm OpenSSH 6.7+ on both ends |
| `reverse forward did not bind /tmp/cc-socks-1000/1001.sock on box-b within 60 s` | ssh stayed up (a refused `-R` would have ended it) but the socket never showed at that path on box-b: its sshd session sees a different `/tmp` (PrivateTmp, a container), or the bind is still pending | from an `ssh box-b` shell run `ls -ld /tmp/cc-socks-<uid>`; point `CLAUDE_CODE_TMPDIR` at a directory both see |
| `could not verify the reverse forward` | the probe's own ssh connection failed after the tunnel came up; the bridge tore down | fix ssh first: `ssh -v box-b true`, rerun |
| `could not create a writable /tmp/cc-socks-<uid> on box-b` | the remote `/tmp` refused the directory, or it exists there owned by another account (a leftover from a root session) | check `ls -ld /tmp/cc-socks-<uid>` there; chown it or point `CLAUDE_CODE_TMPDIR` elsewhere on both sides |
| `Timed out sending to /tmp/cc-socks-1000/2002.sock` from `SendMessage` | the remote session exited; the forward leads nowhere | stop and rerun the bridge; it picks the newest live session |
| `[Cross-session delivery notice] ... held` | permission-mode mismatch; the remote user must approve | wait, or ask them to set `crossSessionInbound` to `accept` |

Different uids on the two hosts give different socket directories (`/tmp/cc-socks-<uid>`). The script creates the missing directory on each side. Windows receivers require the auth token, so the no-copy design does not hold there.

The protocol facts behind all of this, with diagrams, are in `references/protocol.md`.
