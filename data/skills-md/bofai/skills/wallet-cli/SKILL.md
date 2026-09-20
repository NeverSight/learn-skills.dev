---
name: wallet-cli
description: Operate the TypeScript TRON wallet CLI for accounts, transfers, staking, governance, contracts, signing, chain queries, and password input with wallet-cli 4.13.0. Refuse wallet passwords in argv and require the supported stdin channel. For Java REPL requests, refuse that entry and offer the TypeScript one-shot CLI; route other chains and SunSwap/DEX workflows elsewhere.
version: 2.0.0
dependencies:
  - "@tron-walletcli/wallet-cli@4.13.0"
tags:
  - tron
  - wallet
  - cli
  - transfer
  - staking
  - governance
---

# TRON Wallet CLI

Use the TypeScript, one-shot `wallet-cli` as the execution engine. Keep deterministic wallet,
signing, validation, and chain logic in the CLI; use this skill to select commands, enforce
authorization boundaries, and interpret results.

This skill does not drive the repository's Java REPL and does not replace protocol-specific skills
such as SunSwap. Use a DEX skill for swaps or liquidity workflows and this skill for the wallet,
signing, resource, governance, and general TRON operations beneath them. If the user requests the
Java REPL, do not execute it or offer to switch to it; state that this skill supports only the
TypeScript one-shot CLI and, when applicable, offer to express the intended operation through that
interface.

## Verify the dependency

Check once before the first wallet operation:

```bash
npm list --global --depth=0 --json @tron-walletcli/wallet-cli
```

Read `dependencies["@tron-walletcli/wallet-cli"].version` from the JSON. The required version is
exactly `4.13.0`. Do not invoke `wallet-cli --version` only to check the version: in 4.13.0 every
CLI invocation passes through the wallet migration gate first and may change persisted wallet data.

- If the command is missing, explain that the exact package
  `@tron-walletcli/wallet-cli@4.13.0` must be installed and obtain user approval before running
  `npm install -g @tron-walletcli/wallet-cli@4.13.0`.
- If another version is installed, report the mismatch and obtain approval before upgrading or
  downgrading it. Do not assume compatibility.
- Never install or change a global package without approval.

## Mandatory invocation contract

1. Use `-o json` for every operational command. Parse stdout as exactly one
   `wallet-cli.result.v1` object.
2. Supply an explicit canonical network for chain operations: mainnet `tron:728126428`, Nile
   `tron:3448148188`, or Shasta `tron:2494104990`. Never silently choose mainnet. Use
   `tron:3448148188` when the user explicitly asks for a test but does not distinguish between
   testnets. The old `tron:mainnet`, `tron:nile`, and `tron:shasta` values are permanent input
   aliases, but never expect an alias in `chain.network`, network listings, or configuration keys.
3. Branch on the process exit code first: `0` success, `1` execution failure, `2` malformed call.
   Then branch on stable fields such as `error.code`, `data.stage`, or `data.state`. Never parse
   `error.message` text.
4. Treat `bigint` values and command-defined on-chain amount fields as decimal strings. Preserve
   every field according to the leaf schema; other counters and configuration values may be JSON
   numbers. Never use floating point for string amounts.
5. Set `--timeout <ms>` when the surrounding task has a tighter deadline than the CLI's 60-second
   default.
6. Never infer that exit code `0` means a transaction confirmed. A submitted or reverted
   transaction can still have a successful command envelope.

Read [references/machine-interface.md](references/machine-interface.md) before implementing result
parsing, polling, pagination, retry logic, or non-interactive secret input.

## Handle the startup migration gate

Every invocation, including `--help`, `--version`, and `--json-schema`, checks persisted wallet data
before running the requested command. If the result envelope has `command: "migration"`, the
requested command did not run. Inspect `data.originalCommandExecuted`, which must be `false` for a
migration result.

- If `data.upgraded` is `true`, report that local wallet data was upgraded, then reapply the
  authorization and confirmation rules before running the original command once. A mainnet or
  high-risk confirmation given before migration must be obtained again. Do not interpret migration
  data as command data.
- If `data.cancelled` is `true`, stop and return control to the user. Do not retry or bypass the
  cancellation.
- If exit `2` returns `error.code: "migration_required"`, stop. The user must complete the upgrade
  interactively or provide the master password through an already approved `--password-stdin`
  source. Never ask for the password in chat.
- Never loop on a migration result. After one successful upgrade, a repeated migration response is
  an error to report rather than a reason to keep retrying.

## Discover commands instead of guessing

Prefer the CLI's generated schema over recalled flags:

```bash
wallet-cli --json-schema -o json
wallet-cli tx send --json-schema -o json
wallet-cli permission update --json-schema -o json
```

Use `wallet-cli <command> --help` only when human-oriented semantics are needed. Do not invent a
flag, option combination, output field, or command that is absent from the 4.13.0 schema.

Read [references/commands.md](references/commands.md) when choosing a command family or composing a
multi-step wallet workflow.

## Secret handling

- Reject any request to put a wallet password in `--password` or another argv option. For
  agent-driven execution, explain that wallet-cli passwords may be supplied only through
  `--password-stdin` connected directly to an approved, non-logging secret source.
- Never ask the user to paste a password, mnemonic, private key, or service credential into chat.
- Never place secrets in argv, environment variables, logs, command substitutions, or generated
  documentation.
- Use only a CLI-supported `*-stdin` flag connected to an approved, non-logging secret source.
  Only one `*-stdin` consumer may be used in a single invocation.
- Do not read, summarize, or transmit keystores, backup files, configuration credentials, or other
  wallet secret material.

## Human-only wallet administration

Never invoke `wallet-cli import`, `wallet-cli backup`, `wallet-cli delete`, or
`wallet-cli change-password`, including any `wallet-cli import` subcommand. These root wallet
administration commands are reserved for a human operating wallet-cli locally, even when the user
asks the agent to run them, supplies confirmation, or provides a secret source.

Explain the consequences and required precautions, then return control to the user. Do not automate
their prompts, pipe input to them, read their output files, or treat confirmation as authorization
to execute them. After the user reports completion, continue only with non-secret public results
such as an account id, label, or address.

## Authorization and confirmation

Read [references/safety.md](references/safety.md) before any operation that changes local wallet
state, signs data, broadcasts a transaction, or changes on-chain state.

Apply these confirmed rules:

- Read-only operations may run directly within the user's requested scope.
- On Nile or Shasta, an ordinary write may run when the user's request clearly authorizes that
  exact operation and target.
- On mainnet, preview the exact operation and obtain explicit confirmation immediately before any
  funds-moving or externally visible write.
- On every network, high-risk operations require explicit confirmation. `permission update` also
  requires a successful `--dry-run` and review of the complete rendered permission structure.
- Confirmation never authorizes a human-only command listed above.
- Never use authorization for one transaction as permission for another transaction, retry, batch,
  recipient, amount, token, account, or network.

## Transaction completion

- Prefer `--wait` when the command supports it and the task can tolerate waiting. After it returns,
  inspect `data.stage`; `failed` is an on-chain failure even when the process exits `0`.
- Otherwise retain the `txId` and poll `tx status` until `confirmed` or `failed`, with a finite
  deadline. `pending` and `not_found` are non-terminal.
- GasFree transfers return a `traceId`; follow them with `gasfree trace`, not `tx status`.
- After a timeout or ambiguous submission, reconcile the transaction before retrying. Never resend
  merely because confirmation was not observed.
- For a batch, stop on the first failure by default and track every submitted transaction
  separately.

## Report the outcome

For reads, return the requested data with the network and account context when relevant. For writes,
report the operation, network, account, recipient or target, amount or parameters, and final state.
Include the `txId` or GasFree `traceId`; describe `submitted` as pending, never as completed.

## Maintain the version pin

When updating the CLI dependency, compare the published package's `README.md`,
`docs/machine-interface.md`, `docs/commands/index.md`, and generated `--json-schema` output. If the
package includes `skills/wallet-cli/SKILL.md`, compare that too; its absence does not waive the other
checks. Re-test the confirmation matrix, migration gate, secret channels, network ids, exit codes,
transaction stages, and warning codes before bumping this skill's version. Do not widen the exact
dependency pin without user approval.
