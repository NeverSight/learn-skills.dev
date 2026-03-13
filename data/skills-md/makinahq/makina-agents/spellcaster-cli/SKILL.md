---
name: spellcaster-cli
description: Operate the `spellcaster` binary for Makina machine and caliber workflows in non-interactive mode, including balances, positions, swaps, bridge actions, and maintenance commands. Use this skill whenever the user asks to run or debug `spellcaster` terminal commands (as an installed binary), compose command flags, configure `~/.config/spellcaster/config.toml`, or fix CLI errors related to `--machine`, `--caliber`, signer mode, `--dev`, Safe, and RPC settings.
---

# Spellcaster CLI

## Overview

Use this skill to produce correct, executable `spellcaster` commands for operators using the installed CLI binary. Keep responses operational: verify prerequisites, provide exact commands, and map common errors to concrete fixes.

## Workflow

1. Confirm binary and config availability.
- Run `spellcaster --version` to verify the binary is installed.
- Assume config path precedence:
  - `--config <path>` if provided.
  - `$XDG_CONFIG_HOME/spellcaster/config.toml` when `XDG_CONFIG_HOME` is set.
  - Otherwise `~/.config/spellcaster/config.toml`.
- If config is missing and the workspace includes `example.config.toml`, provide a copy command and call out the minimum sections needed (`[machines]`, `[rpc_urls]`, `[signer]`).

2. Prefer non-interactive mode.
- In non-interactive mode, require:
  - `--machine <NAME>` for all commands.
  - `--caliber <CHAIN>` for all commands except `full-aum-update-cycle`.

3. Build commands in the canonical order.
- Put global flags before the subcommand:
  - `spellcaster [--config ...] [--dev] [--unsigned] [--safe ...] --machine ... --caliber ... <command> [command flags]`
- Prefer exact token values supplied by the user (addresses, amounts, chain names).
- If required values are missing, ask only for missing fields and keep placeholders minimal.

4. Handle signing and environment safely.
- Respect signer configuration in `config.toml`.
- Use `--unsigned` when the user explicitly wants unsigned/dev execution.
- Use `--dev` only when targeting Tenderly virtual testnets and ensure `dev_rpc_urls` are configured.
- Never echo secret values (private keys, API keys, tokens) in output.

5. Troubleshoot with direct fixes.
- If error says `must specify machine...`, add `--machine <NAME>`.
- If error says `must specify caliber...`, add `--caliber <CHAIN>` unless command is `full-aum-update-cycle`.
- If error says `please set [dev_rpc_urls]...`, add `[dev_rpc_urls]` entries in config or remove `--dev`.
- If machine resolution fails, check `[machines]` mapping and `github_token` access for private repos.

## Response Template

Use this concise structure unless the user requests something else:

1. `Preflight`: installed binary + config path assumptions.
2. `Command`: one or more ready-to-run commands in fenced `bash`.
3. `Why`: one sentence explaining key flags.
4. `If It Fails`: 1-3 targeted troubleshooting checks.

## Command Discovery

When users ask what is available, use help output first:
- `spellcaster --help`
- `spellcaster <subcommand> --help`

Do not guess unsupported flags when help output can resolve uncertainty.

## References

Load [references/command-snippets.md](references/command-snippets.md) for concrete examples and error-to-fix mappings.
