---
name: jms-terminal
description: >-
  jms-cli terminal backends (SSH / WebSocket): BackendType and connect(),
  SSH exec semantics (overall deadline, recv_exit_status, stderr never mixed
  into stdout), WS exec marker protocol (double __JMSDONE marker + __JMSRC
  exit code, binary frames, drain after each execute), keepalive (SSH
  transport 30s / WS application-level PING text frames every 30s, never WS
  opcode 0x9), interactive PTY (Ctrl+] to exit, SIGWINCH resize sync), and
  adding new backends (register_backend / AbstractTerminal /
  _AUTO_SEQUENCE). Use whenever exec times out or hangs, WS output parsing
  misbehaves, sessions drop on heartbeat, login interactive sessions, adding
  a protocol backend, or writing execute() code. CLI first (jms exec / jms
  login); use the connect() library API for embedded terminals.
compatibility: Python >= 3.10; uv environment (paramiko, websocket-client are project dependencies)
metadata:
  author: codex
  version: "1.0"
  project: jms-cli
---

# jms-terminal — Terminal backends

## When to use

Trigger on mentions of exec, remote commands, terminal, WebSocket, WS backend,
SSH backend, marker, heartbeat, keepalive, Ctrl+], PTY, interactive,
`BackendType`, or adding a backend/protocol — even without naming the
transport module. Use cases: `jms exec` timeouts or empty output, polluted WS
output, dropped interactive sessions, or reserving a future RDP/VNC backend.

## Prerequisites

- Terminal authentication material (connection token, `jms_sessionid` cookie)
  comes from the `jms-auth` skill: confirm the session is usable before
  debugging the terminal layer.
- File transfer reuses this layer's `execute()` for hashing/merging; that
  semantics belongs to the `jms-transfer` skill.

## Core facts (read first)

1. **Backend selection**: `BackendType.AUTO` tries `_AUTO_SEQUENCE = ("ssh",
   "ws")` in order, falling back from SSH to WS on failure; `-b ssh|ws`
   forces a backend. The registry (`register_backend / open_backend /
   list_backends / auto_sequence`) is the extension point.
2. **SSH**: token auth to KoKo 2222 (`open_koko_transport`, one retry with a
   fresh token); `execute()` uses `exec_command` with clean start/end
   semantics — **no** WS marker tricks needed; the timeout is an overall
   deadline; with `check=True` a non-zero exit raises `TerminalError(
   exit_code, output)`; stderr goes to logs only.
3. **WS**: must use `/koko/ws/terminal/` (`/koko/ws/token/` 404s on some
   versions), carrying the `jms_sessionid` cookie; output arrives as **binary
   frames** (opcode 2), command input is a text frame
   `{"type":"TERMINAL_DATA","data":"cmd\r"}`; the exit code is captured via
   `__JMSRC:N__`; residual data is drained after every execute. Details in
   `references/ws-protocol.md`.
4. **Keepalive**: SSH uses `transport.set_keepalive(30)`; WS uses
   **application-level PING text frames** every 30s (the Nginx WS reverse
   proxy is a transparent TCP tunnel, so WS opcode 0x9 pings never reach
   KoKo).

## Workflow

### A. CLI first (user operations)

```bash
uv run jms exec web@prod 'df -h'          # default auto (SSH first)
uv run jms exec -b ws web whoami          # force the WS backend
uv run jms exec -t 60 web 'sleep 30'      # 60s timeout (default 30s), propagates exit code
uv run jms login web@prod                 # interactive PTY, Ctrl+] to exit
uv run jms login -b ssh web               # force SSH (native PTY)
```

Troubleshoot with `uv run jms -l DEBUG exec ...` to see backend selection and
connection logs.

### B. Library API (programmatic terminal)

```python
from jms import JMSSession, BackendType, connect, resolve_asset
from jms.config import load_config

sess = JMSSession(load_config().get_server("prod"), otp_prompt=lambda: input("OTP: "))
sess.login()
asset = resolve_asset(sess, "web")
with connect(sess, asset, backend=BackendType.AUTO) as term:
    out = term.execute("uname -a", timeout=30, check=True)
    print(term.backend_name, out)
```

`connect()` wraps only connection setup, never the yield body — a
`TerminalError` raised inside the with-body is not mistaken for a connect
failure that would trigger fallback.

### C. SSH vs WS quick reference

| Dimension | SSH | WS |
|---|---|---|
| Port/path | KoKo 2222 | `/koko/ws/terminal/` |
| Auth | `JMS-{id}` / token password | URL `token={id}` + cookie |
| exec start/end | clean exec-channel semantics | double marker + `__JMSRC` |
| Timeout | overall deadline | overall deadline + 3s recv |
| Keepalive | `set_keepalive(30)` | app-level PING every 30s |
| Known traps | none | trailing `#`/`\` or unbalanced quotes swallow the marker chain and hang until timeout |

### D. Interactive sessions

- A TTY is required (otherwise `TerminalError: Interactive mode requires a
  TTY`).
- Raw-mode bidirectional relay; Ctrl+] exits; SIGWINCH syncs the size (SSH
  `resize_pty` / WS `TERMINAL_RESIZE`).
- WS interactive mode runs a heartbeat thread; SSH relies on transport
  keepalive.

### E. Adding a backend (e.g. future RDP/VNC)

1. Create `src/jms/transport/<proto>.py` implementing `AbstractTerminal`'s
   `execute/interactive/close/backend_name`, with a `capabilities` class
   attribute.
2. Provide `open_<proto>_terminal(session, asset)` and self-register at the
   bottom: `register_backend("<proto>", open_..., frozenset({...}))`.
3. `connect()`/`BackendType` need no change; `_AUTO_SEQUENCE` does not
   automatically include the new backend — only explicit
   `open_backend("<proto>", ...)` works until the tuple in `registry.py` is
   edited.

Template: `references/backend-extension.md`.

### F. Verification

After touching terminal code, run the relevant regressions (deterministic
tooling, never eyeballing):

```bash
uv run pytest tests/test_backend_connect.py tests/test_backend_ssh.py \
  tests/test_backend_ws.py tests/test_backend_token.py tests/test_verify.py -q
```

Real-server exec e2e cases are gated by `JMS_TEST_*` env vars.

## Scope & Boundaries

> - Capabilities, commands, subcommands, flags, parameters, environment
>   variables, endpoints, and file paths **not mentioned in this skill are not
>   part of this skill**. Do not guess or extrapolate them from related tools,
>   documentation memory, or pattern-matching across similar CLIs.
> - If the user asks for functionality outside this skill, stop and ask — do
>   not invent it.
> - The consuming agent is not responsible for completing or improving the
>   skill. Discovering missing functionality is a signal to **ask the user**,
>   not to fill the gap silently.
> - If the skill's instructions appear wrong, contradictory, outdated, or
>   produce errors when executed, stop and consult the user before proceeding.
>   Do not "fix" the skill on the fly, substitute an alternative command, or
>   retry with guessed parameters.
> - Modifying or extending the skill itself requires explicit user permission
>   and should be routed back through `skill-creator`.

This skill covers terminal protocols and backend registration only;
authentication belongs to `jms-auth`, transfer orchestration to
`jms-transfer`. Do not extend beyond that here.
