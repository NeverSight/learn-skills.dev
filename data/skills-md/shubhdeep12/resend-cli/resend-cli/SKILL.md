---
name: resend-cli
description: Use when the user wants to run Resend operations from the command line (send email, list emails, manage domains, contacts, templates, webhooks) via the Resend CLI. Prefer this when the task is CLI/terminal-based or when you need scriptable, JSON output.
license: MIT
metadata:
  author: Shubhdeep
  version: "0.4.16"
  homepage: https://github.com/Shubhdeep12/resend-cli
  source: https://github.com/Shubhdeep12/resend-cli
inputs:
  - name: RESEND_API_KEY
    description: Resend API key. Get one at https://resend.com/api-keys
    required: true
---

# Resend CLI

CLI for [Resend](https://resend.com). Use it when the user asks to send emails, list emails, manage domains, contacts, templates, or webhooks **from the terminal** or from scripts.

## When to use

- User says "send an email from the command line", "use resend cli", "run resend in terminal"
- Task is to list/send/get emails, manage domains, contacts, templates, webhooks, or API keys via CLI
- Script or automation needs to call Resend with deterministic, parseable output (use `--json`)

## Run the CLI

**One-off (no install):**
```bash
npx @shubhdeep12/resend-cli --help
```

**With auth:**
```bash
export RESEND_API_KEY="re_xxx"
npx @shubhdeep12/resend-cli <group> <command> [options]
```

**No Node.js:** Download the binary for your OS from [Releases](https://github.com/Shubhdeep12/resend-cli/releases/latest), extract, and run the executable.

**Binaries:** Standalone executables (darwin arm64/x64, linux x64, windows x64) are built per release. No Node or npm required; download the archive for your platform, extract, and run (e.g. `resend-cli-<version>-darwin-arm64` or `resend-cli-<version>-win-x64.exe`). Checksums are on the release page.

## Behavior contract

- **Exit code:** `0` on success, non-zero on failure.
- **Data commands:** Always add `--json` for a single JSON payload (e.g. `resend emails list --json`, `resend domains list --json`).
- **Pagination:** List commands support `--limit`, `--after`, `--before`.

## Quick reference

| Task           | Example |
|----------------|--------|
| Send email     | `resend emails send --from "x@domain.com" --to "y@example.com" --subject "Hi" --html "<p>Hi</p>"` |
| List emails    | `resend emails list --json --limit 10` |
| Auth (optional)| `resend auth login --key re_xxx` or set `RESEND_API_KEY` |

For full commands and flags, run `resend --help` and `resend <group> --help`, or see [Command Reference](./docs/COMMANDS.md).
