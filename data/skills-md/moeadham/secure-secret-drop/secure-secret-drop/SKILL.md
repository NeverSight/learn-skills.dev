---
name: secure-secret-drop
description: "Use when someone needs dead-simple secret sharing with an AI agent. Creates a single-use URL via Cloudflare Quick Tunnels for securely dropping a password, credential, or other secret without putting it in chat."
version: 1.1.0
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [secrets, handoff, cloudflare, one-time-form]
---

# Secure Secret Drop

Use this private local skill when a user needs to provide secrets without chat or vault. It creates a capability-addressed, one-time browser form over an isolated Cloudflare Quick Tunnel and later writes submitted values directly to an explicitly authorized destination.

## Requirements and first-run setup

Required:

- Python 3 with the standard library; no Python packages are needed.
- The `cloudflared` executable.
- Outbound network access to Cloudflare. The local form origin binds only to `127.0.0.1`.

A Cloudflare account, domain, API token, `cloudflared tunnel login`, named tunnel, DNS record, and background service are **not** required. This skill creates an anonymous, temporary Quick Tunnel for each drop.

Before creating the first form, run `doctor`. If it reports `cloudflared=missing`, do not attempt `create` and do not tell the user to solve it manually when terminal tools are available. Read [Cloudflared setup](references/cloudflared-setup.md), identify the host OS and package manager, explain the proposed installation, obtain any approval required for package installation or `sudo`, install from Cloudflare's official distribution channel, and rerun both `cloudflared --version` and `doctor`. Never run `cloudflared tunnel login`, create DNS, install a tunnel service, or alter an existing Cloudflare configuration for this skill.

If `cloudflared` is installed outside `PATH`, set `CLOUDFLARED_BIN` to its absolute executable path for the command invocation or agent service environment. The CLI also checks common macOS/Linux locations automatically.

## Workflow

1. Run `doctor`.
2. Create the form and send the returned URL to the user. Never ask them to paste values in chat.
3. The user submits once and says only that submission is complete.
4. Run `status RECEIPT_ID`; it reveals status and field names, never values, lengths, or hashes.
5. Consume directly into the exact path the user approved, or discard a dummy test receipt.

Resolve the installed skill directory from the skill loader; do not copy an author-specific absolute path. Then use its script:

```bash
PY="$(command -v python3)"
CLI="<installed-skill-directory>/scripts/handoff.py"
$PY "$CLI" doctor
$PY "$CLI" create --field API_KEY --field API_SECRET --ttl 600
$PY "$CLI" status RECEIPT_ID
$PY "$CLI" consume RECEIPT_ID --env-file /exact/approved/path.env
$PY "$CLI" consume RECEIPT_ID --json-file /exact/approved/path.json
$PY "$CLI" consume RECEIPT_ID --env-file /exact/path.env --overwrite
$PY "$CLI" consume RECEIPT_ID --discard
$PY "$CLI" cancel RECEIPT_ID
```

Options: repeat `--field NAME`; use `--label NAME=Visible label`; use `--plain NAME` only for a declared non-secret field. Names initially must match uppercase environment-key style. Default TTL is 10 minutes.

## Operational rules

- Never call `read_file`, `cat`, `show`, or another display command on a receipt. The CLI intentionally has no raw-output command.
- Never put values in arguments, URLs, logs, status output, or chat.
- Existing destination keys require `--overwrite`. A destination path explicitly named by the user already counts as authorization; do not ask again before consuming. Ask only when the destination is missing or ambiguous, or when overwrite approval is required.
- A failed destination validation/write leaves the submitted receipt retriable.
- GET and HEAD are non-consuming; only one valid POST succeeds. Link scanners therefore do not consume the form.
- Forms expire and their local origin/tunnel self-terminate. `cancel` closes early. Submitted forms stop serving immediately and wait for explicit consumption.
- Use absolute script and destination paths so fresh Hermes sessions behave consistently.
- Keep the form visually restrained and professional; do not use purple in its palette.

## Trust and storage model

This is a TLS-only MVP, not browser end-to-end encryption. Cloudflare terminates public TLS at its edge and forwards over the Quick Tunnel to an HTTP origin bound only to `127.0.0.1`. Cloudflare is therefore in the trust boundary. The tunnel is launched with `tunnel --no-autoupdate --config /dev/null --url http://127.0.0.1:<random-port>`; it does not touch named tunnels, existing config, DNS, Workers, or sudo.

Pending form capability/CSRF material and submitted receipts live outside the skill under `$XDG_STATE_HOME/secure-secret-drop/` or `~/.local/state/secure-secret-drop/` by default (directory mode 0700, files mode 0600). Set `SECURE_SECRET_DROP_STATE_DIR` to override it. Receipts are plaintext at rest for this approved MVP and inherit the security of the local user account and disk encryption. Consume or cancel promptly. Receipt/private-form data is deleted after consume, cancel, or expiry; a minimal nonsecret status record remains so `status` can report the terminal state.

See [Security model](references/security-model.md) for limits and invariants.
