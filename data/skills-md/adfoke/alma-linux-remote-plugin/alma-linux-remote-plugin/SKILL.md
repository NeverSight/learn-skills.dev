---
name: alma-linux-remote-plugin
description: Remote Linux management for Alma via SSH/SFTP with persistent stateful SSH sessions, thread-session binding, NL-to-command bridge, xterm.js websocket terminal bridge, dangerous-command approval flow, strict command policy option, host-key verification modes, RBAC allowlist, and SIEM-friendly redacted audit fields.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Alma Linux Remote Plugin

Use this project to manage remote Linux hosts from Alma with safety controls.

## Capabilities

- SSH connection test
- Single/batch command execution
  - Primary tools: `run_command`, `run_batch`
  - Compatibility aliases: `execute_command`, `execute_batch`
- Upload/download files via SFTP
- Service status and journal logs
- Dangerous command protection:
  - Manual approval workflow (`approval_id`)
  - Operator RBAC allowlist (`approval.allowed_operators`)
  - Optional one-time confirmation token mode
- Command policy hardening:
  - `policy.strict_policy=false` (compatible mode)
  - `policy.strict_policy=true` (normalized/token-level matching)
- Host key verification policy (`ssh.host_key_policy`):
  - `known_hosts` (RejectPolicy + optional `known_hosts_required`)
  - `reject` (strict reject unknown hosts)
  - `auto_add` (compatibility mode)
- Server profile docs:
  - First remote access auto-creates `server_profiles/<IP>.md`
  - Subsequent remote calls read this profile before connect
- Audit logging (`JSONL`) with SIEM-friendly fields and safety:
  - `request_id` / `trace_id` / `operator_ip`
  - Sensitive fields redacted (`password/token/secret/key/passphrase`)
  - `stdout/stderr` truncated for log safety
- Persistent SSH sessions (stateful shell):
  - `open_session`, `list_sessions`, `close_session`
  - `run_command_in_session`, `write_session`, `read_session`, `resize_session`
  - Session metadata persistence (`session.storage_file`)
- Real terminal bridge (xterm.js + WebSocket):
  - `start_terminal_ws` returns `ws://.../terminal/<session_id>`
  - `stop_terminal_ws` unregisters a session or stops the WS server
- Session key injection:
  - `send_keys_to_session` supports `ESC/UP/DOWN/LEFT/RIGHT/TAB/ENTER`
- Thread-session binding layer:
  - `bind_thread_session`, `get_thread_session`, `unbind_thread_session`
  - `ensure_thread_session` (auto-open and bind when missing)
- NL -> command bridge:
  - `plan_command_from_text` (plan only)
  - `execute_text_in_session` (plan + run in persistent session)

## Install

```bash
git clone https://github.com/adfoke/alma-linux-remote-plugin.git
cd alma-linux-remote-plugin
uv sync --all-extras
```

## Quick Start

```bash
uv run python demo_cli.py --config ./examples/hosts.example.yaml handle health
uv run python demo_cli.py --config ./examples/hosts.example.yaml tools
uv run python demo_cli.py --config ./examples/hosts.example.yaml handle execute_command '{"host_name":"prod-web-1","command":"uptime"}'
uv run python demo_cli.py --config ./examples/hosts.example.yaml handle open_session '{"host_name":"prod-web-1"}'
uv run python demo_cli.py --config ./examples/hosts.example.yaml handle list_sessions '{"status":"all"}'
uv run python demo_cli.py --config ./examples/hosts.example.yaml plan-text thread-a prod-web-1 "帮我看下磁盘和内存"
uv run python demo_cli.py --config ./examples/hosts.example.yaml exec-text thread-a prod-web-1 "查看 nginx 状态和最近日志"
uv run python demo_cli.py --config ./examples/hosts.example.yaml handle send_keys_to_session '{"session_id":"<SESSION_ID>","keys":["ESC",":wq","ENTER"]}'
```

English doc: `README.en.md`

## Safety Workflow (dangerous command)

1. Run dangerous command → receive `approval_required` and `approval_id`
2. Approver calls `approve_request` with allowed `operator`
3. Re-run command with `approval_id`

## Code Audit Notes

- `plugin.py` now uses `_with_connected_client(...)` to consolidate repeated connect/close patterns.
- Added focused tests for `ssh_client.py` and `terminal_ws.py` to keep critical path coverage high.

## Quality Gate

```bash
uv run ruff check src tests demo_cli.py
uv run pytest --cov=src/alma_linux_remote_plugin --cov-report=term-missing --cov-fail-under=65
```

## Main Entrypoint

- Runtime adapter: `src/alma_linux_remote_plugin/runtime_adapter.py`
- Plugin metadata: `plugin.yaml`
