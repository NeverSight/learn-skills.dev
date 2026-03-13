---
name: ssh-tunnel
description: >
  Manage SSH tunnels declaratively. Use when the user wants to create, start,
  stop, enable, disable, or check the status of SSH port-forwarding tunnels.
  Also use when the user mentions SSH tunnels, port forwarding, bastion hosts,
  or connecting to remote databases/services through SSH.
---

# SSH Tunnel Manager

You are managing SSH tunnels using the `ssh-tunnels` CLI tool backed by a
declarative JSON config at `~/.ssh-tunnels/config.json`.

## Step 1: Ensure the tool is installed

Before doing anything, check if the CLI is available:

```bash
which ssh-tunnels 2>/dev/null && echo "installed"
```

If NOT installed, run:

```bash
npm install -g @statechange/ssh-tunnel-manager
```

This single command installs the CLI, creates `~/.ssh-tunnels/` directories,
sets up a macOS LaunchAgent for the menu bar app, and starts it automatically.

After installation, verify:
```bash
ssh-tunnels status
```

## Step 2: Manage tunnels

### Check current tunnels
```bash
ssh-tunnels status
```

### Add a new tunnel
```bash
ssh-tunnels add \
  --name "Descriptive Name" \
  --host <ssh-host> \
  --user <ssh-user> \
  --localPort <local-port> \
  --remoteHost <remote-host> \
  --remotePort <remote-port> \
  --enabled
```

### Enable / disable / remove
```bash
ssh-tunnels enable <tunnel-id>
ssh-tunnels disable <tunnel-id>
ssh-tunnels remove <tunnel-id>
```

### Sync all tunnels to match config
```bash
ssh-tunnels sync
```

### Use --json for programmatic output
```bash
ssh-tunnels status --json
ssh-tunnels enable <id> --json
```

## Critical knowledge

### The --user flag is the #1 source of errors
The SSH username defaults to the local OS user. Most servers require `root`
or a specific service account. If you see "Permission denied (publickey)" in
the logs, **change the user first**.

### The --remoteHost is relative to the SSH server
When the service runs directly on the SSH host, use `--remoteHost localhost`.
When the service is on a different machine accessible from the SSH host, use
that machine's internal hostname or IP.

### Common ports
| Port  | Service                |
|-------|------------------------|
| 5432  | PostgreSQL             |
| 3306  | MySQL                  |
| 6379  | Redis                  |
| 27017 | MongoDB                |
| 80    | HTTP                   |
| 443   | HTTPS                  |
| 8080  | Dev server / admin UI  |
| 8089  | Splunk / custom        |
| 18789 | OpenClaw admin         |
| 3000  | Node.js dev server     |
| 9200  | Elasticsearch          |

### Tunnel IDs
The ID is auto-generated from the name by slugifying it (lowercase, hyphens).
For example, "Production Postgres" becomes `production-postgres`. Always use
the ID (not the name) for enable/disable/remove/logs commands.

### After adding an enabled tunnel, verify it started
Always check status or logs after enabling a tunnel. The `enable` and `add --enabled`
commands will automatically verify and report issues, but with `--json` output
you should check the `healthy` field:

```bash
ssh-tunnels enable my-tunnel --json
# Look for: "healthy": true
```

If unhealthy, check logs:
```bash
ssh-tunnels logs my-tunnel
```

## Menu bar app

The Electron menu bar app provides a GUI for the same functionality:
- Tray icon: green (all OK), yellow (partially running), red (failures)
- Click to see tunnel list with toggle switches
- "Add Tunnel..." opens a form
- "Sync Now" forces immediate reconciliation
- Auto-syncs every 30 seconds for crash recovery

The app reads/writes the same `~/.ssh-tunnels/config.json` as the CLI.
Changes from either the CLI or the app are reflected in both.

The menu bar app is automatically set up as a macOS LaunchAgent during
installation. To manually start it:
```bash
cd $(npm root -g)/@statechange/ssh-tunnel-manager && npx electron dist/app.mjs
```
