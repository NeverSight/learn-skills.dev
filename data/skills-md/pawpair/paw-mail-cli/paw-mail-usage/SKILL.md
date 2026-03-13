---
name: paw-mail-usage
description: >
  How to use the Paw Mail CLI (paw-mail). Use this skill when:
  (1) you need to run a CLI command (auth, accounts, emails, sync, threads, config),
  (2) someone asks how to use or invoke the mail CLI,
  (3) you need to check CLI flags or subcommands.
license: MIT
compatibility: Linux x86_64/aarch64, macOS x86_64/aarch64
metadata:
  author: pawpair
  version: "3.0.0"
allowed-tools: Bash(paw-mail:*) Bash(paw-mail-tui:*) Read Glob Grep
---

# Paw Mail CLI

The CLI is distributed as pre-built binaries via the [paw-mail-cli](https://github.com/pawpair/paw-mail-cli) repository. It must be installed before use.

## Installation

```bash
# Nix (recommended)
nix profile install 'github:pawpair/paw-mail-cli?dir=nix#paw-mail'

# Homebrew (macOS / Linux)
brew tap pawpair/paw-mail-cli && brew install paw-mail

# Arch Linux (AUR)
yay -S paw-mail-bin

# Debian / Ubuntu — download .deb from latest release
# https://github.com/pawpair/paw-mail-cli/releases/latest
sudo dpkg -i paw-mail_*_amd64.deb
```

## Binaries

| Binary        | Description                     |
|---------------|---------------------------------|
| `paw-mail`    | Unified CLI + TUI (recommended) |
| `paw-mail-tui`| Terminal user interface only     |

All examples below use `paw-mail`. The TUI can be launched with `paw-mail-tui` or `paw-mail tui`.

## Global Flags

These flags go **before** the subcommand:

| Flag | Env Var | Description |
|------|---------|-------------|
| `--server <url>` | `MAIL_SERVER` | gRPC backend address |
| `--format <table\|json>` | — | Output format (default: table) |
| `--auth-backend <auto\|keyring\|file>` | `MAIL_AUTH_BACKEND` | Token storage backend |
| `-v, --verbose` | — | Enable debug logging |

## Subcommands

### Config
```bash
paw-mail config refresh  # Fetch remote config and cache locally
paw-mail config show     # Show current config values
```

Config is cached locally at `~/.local/pawpair/config.json` (or `~/.pawpair/config.json`). First run bootstraps automatically from the remote config service.

### Auth
```bash
paw-mail auth login      # OAuth device flow login
paw-mail auth status     # Show auth state + backend
paw-mail auth logout     # Clear stored tokens
```

### Accounts
```bash
paw-mail accounts list
paw-mail accounts get --provider <google|microsoft>
paw-mail accounts add --email <e> --provider <google|microsoft>  # Opens browser for OAuth
paw-mail accounts delete --provider <google|microsoft>
paw-mail accounts activate --id <uuid>
paw-mail accounts deactivate --id <uuid>
paw-mail accounts oauth-clients            # List user OAuth clients
paw-mail accounts oauth-clients --system   # List system OAuth clients
```

### Emails
```bash
paw-mail emails folders --provider <p> --email <e>
paw-mail emails list --provider <p> --email <e> --folder INBOX [--limit 50]
paw-mail emails fetch --provider <p> --email <e> --folder INBOX --uid <n>
paw-mail emails body --provider <p> --email <e> --folder INBOX --uid <n>
paw-mail emails search --provider <p> --email <e> --folder INBOX --query <q>
paw-mail emails read --provider <p> --email <e> --folder INBOX --uid <n>
paw-mail emails unread --provider <p> --email <e> --folder INBOX --uid <n>
paw-mail emails flag --provider <p> --email <e> --folder INBOX --uid <n> [--unflag]
paw-mail emails move --provider <p> --email <e> --folder INBOX --uid <n> --destination Trash
paw-mail emails delete --provider <p> --email <e> --folder INBOX --uid <n>
```

### Sync
```bash
paw-mail sync status --account-id <id>
paw-mail sync trigger --account-id <id>
paw-mail sync history --account-id <id>
```

### Threads
```bash
paw-mail threads list --account-id <id>
paw-mail threads get --thread-id <id> --account-id <id>
```

## Auth Backends

```bash
# Auto-detect (default) — tries keyring, falls back to file
paw-mail auth status

# Force file-based storage
paw-mail --auth-backend file auth status

# Force keyring (errors if unavailable)
paw-mail --auth-backend keyring auth status

# Verbose to see backend selection
paw-mail -v auth status
```

## Common Issues

- **`command not found: paw-mail`** — The CLI is not installed. See Installation above.
- **`Keyring write failed: locked collection`** — GNOME Keyring is locked. Use `--auth-backend file` or unlock your keyring.
- **`Could not open browser`** — Headless/SSH session. Copy the printed URL manually.
