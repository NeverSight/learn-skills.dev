---
name: slk-shared
description: "slk CLI: shared reference for authentication, global flags, and security rules."
metadata:
  version: 0.8.1
  openclaw:
    category: "productivity"
    requires:
      bins:
        - slk
---

# slk — Shared Reference

PREREQUISITE for every `slk-<group>` skill. Covers discovery, global flags, and the rules that apply to all commands.

## Discovering Commands

- `slk --help` — all command groups.
- `slk <group> --help` — a group's verbs.
- `slk <group> <verb> --help` — a verb's flags.

## Global Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--as` | — | identity user\|bot: on a command, assert the active token's scope; on 'auth login', which token to mint (default user) |
| `--dry-run` | — | validate without calling the API |
| `--format` | `concise` | output format: concise\|json\|jsonl\|table |
| `--no-resolve` | — | do not resolve IDs to names |
| `--profile` | — | config profile to use |
| `--raw` | — | return raw Slack API response |

## Security Rules

- Never print or log token strings.
- Confirm with the user before any write/destructive command; preview with `--dry-run`.
- Write verbs honor `--raw` (return raw Slack JSON) and `--dry-run` (print the about-to-fire call and return without hitting the API).

## Exit Codes

`0` ok · `3` auth · `4` not found · `5` rate-limited · `1` other.

## Shell Tips

- `--params` takes a flat JSON object; single-quote it so the shell keeps the inner double quotes (`--params '{"k":"v"}'`). Nested values must be pre-serialized JSON strings.
- Shell `"\n"` is literal — for multi-line text use `--text-file` / `--markdown-file` (`-` for stdin).
