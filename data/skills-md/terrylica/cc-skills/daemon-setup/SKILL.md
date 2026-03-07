---
name: daemon-setup
description: Set up asciinema chunker daemon with interactive wizard. Guides through PAT creation, Keychain storage, Pushover setup, and launchd installation. TRIGGERS - daemon setup, install chunker, configure backup.
allowed-tools: Bash, AskUserQuestion, Write, Read
argument-hint: "[--reinstall] [--skip-pushover]"
disable-model-invocation: true
---

# /asciinema-tools:daemon-setup

Interactive wizard to set up the asciinema chunker daemon. This daemon runs independently of Claude Code CLI, using dedicated credentials stored in macOS Keychain.

## Why a Daemon?

| Problem with old approach     | Daemon solution                  |
| ----------------------------- | -------------------------------- |
| Uses `gh auth token` (shared) | Uses dedicated PAT from Keychain |
| Dies when terminal closes     | launchd keeps it running         |
| Silent push failures          | Logs + Pushover notifications    |
| Tied to Claude Code session   | Completely decoupled             |

## Setup Phases Overview

| Phase | Name                  | Details                                                                            |
| ----- | --------------------- | ---------------------------------------------------------------------------------- |
| 1     | Preflight Check       | Below                                                                              |
| 2     | Check Existing        | Below                                                                              |
| 3     | GitHub PAT Setup      | [PAT Setup Guide](./references/pat-setup-guide.md)                                 |
| 4     | Pushover Setup        | [Pushover Setup Guide](./references/pushover-setup-guide.md)                       |
| 5-6   | Config + Install      | [launchd Installation Guide](./references/launchd-installation.md)                 |
| 7     | Verify + Troubleshoot | [Verification & Troubleshooting](./references/verification-and-troubleshooting.md) |

## Execution

### Phase 1: Preflight Check

**Check required tools:**

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
MISSING=()
for tool in asciinema zstd git curl jq; do
  command -v "$tool" &>/dev/null || MISSING+=("$tool")
done

# macOS-specific: security command for Keychain
if [[ "$(uname)" == "Darwin" ]]; then
  command -v security &>/dev/null || MISSING+=("security (macOS Keychain)")
fi

if [[ ${#MISSING[@]} -gt 0 ]]; then
  echo "MISSING:${MISSING[*]}"
  exit 1
fi

echo "PREFLIGHT:OK"
PREFLIGHT_EOF
```

**If MISSING not empty, use AskUserQuestion:**

```
Question: "Missing required tools: {MISSING}. How would you like to proceed?"
Header: "Dependencies"
Options:
  - label: "Install via Homebrew (Recommended)"
    description: "Run: brew install {MISSING}"
  - label: "I'll install manually"
    description: "Pause setup and show install instructions"
  - label: "Abort setup"
    description: "Exit the setup wizard"
```

**If "Install via Homebrew"**: Run `brew install {MISSING}` and continue.

---

### Phase 2: Check Existing Installation

```bash
/usr/bin/env bash << 'CHECK_EXISTING_EOF'
PLIST_PATH="$HOME/Library/LaunchAgents/com.cc-skills.asciinema-chunker.plist"
DAEMON_RUNNING="false"

if [[ -f "$PLIST_PATH" ]]; then
  echo "PLIST_EXISTS:true"
  if launchctl list 2>/dev/null | grep -q "asciinema-chunker"; then
    DAEMON_RUNNING="true"
  fi
else
  echo "PLIST_EXISTS:false"
fi

echo "DAEMON_RUNNING:$DAEMON_RUNNING"

# Check if PAT already in Keychain
if security find-generic-password -s "asciinema-github-pat" -a "$USER" -w &>/dev/null 2>&1; then
  echo "PAT_EXISTS:true"
else
  echo "PAT_EXISTS:false"
fi
CHECK_EXISTING_EOF
```

**If PLIST_EXISTS=true, use AskUserQuestion:**

```
Question: "Existing daemon installation found. What would you like to do?"
Header: "Existing"
Options:
  - label: "Reinstall (keep credentials)"
    description: "Update daemon script and plist, keep Keychain credentials"
  - label: "Fresh install (reset everything)"
    description: "Remove existing credentials and start fresh"
  - label: "Cancel"
    description: "Exit without changes"
```

---

### Phase 3: GitHub PAT Setup

See [PAT Setup Guide](./references/pat-setup-guide.md) for the full interactive flow: PAT creation walkthrough, Keychain storage, and verification.

---

### Phase 4: Pushover Setup (Optional)

See [Pushover Setup Guide](./references/pushover-setup-guide.md) for the full interactive flow: Pushover explanation, app creation, credential storage, and test notification.

---

### Phase 5-6: Daemon Configuration and launchd Installation

See [launchd Installation Guide](./references/launchd-installation.md) for chunking settings selection, plist generation from template, and service installation.

---

### Phase 7: Verification

See [Verification & Troubleshooting](./references/verification-and-troubleshooting.md) for daemon health checks, post-install verification, the final success message, and the troubleshooting table.

## Quick Reference

### Troubleshooting

| Issue                  | Cause                          | Solution                               |
| ---------------------- | ------------------------------ | -------------------------------------- |
| Keychain access denied | macOS permission not granted   | Grant access in System Settings        |
| PAT test failed        | Token expired or invalid scope | Generate new token with `repo` scope   |
| launchctl load failed  | plist syntax error             | Check `plutil -lint <plist-path>`      |
| Daemon keeps stopping  | Script error or crash          | Check `/asciinema-tools:daemon-logs`   |
| Pushover not working   | Invalid credentials            | Re-run setup with correct app/user key |
| Health file missing    | Daemon not running             | Run `/asciinema-tools:daemon-start`    |

### Related Commands

| Command                          | Description         |
| -------------------------------- | ------------------- |
| `/asciinema-tools:daemon-status` | Check daemon health |
| `/asciinema-tools:daemon-logs`   | View logs           |
| `/asciinema-tools:daemon-stop`   | Stop daemon         |
| `/asciinema-tools:daemon-start`  | Start daemon        |
