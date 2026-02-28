---
name: injective-cli
description: Use the Injective `injectived` CLI against a chain with consistent wallet, endpoint, and gas handling. Use the CLI map and reference docs to find commands and build transactions safely.
license: Apache-2.0
metadata:
  author: InjectiveLabs
  version: "1.18.0"
---

# Injective CLI Skill

## Overview

Use the `injectived` binary to query and transact against an Injective chain with consistent wallet handling, endpoint selection, and gas configuration. Use the bundled CLI command map and reference docs to find the right subcommands and flags quickly.
By invoking any script in this skill, you agree to the Terms of Use in `TERMS_OF_USE`.

## Workflow

### 1) Locate or install the binary

Use a local `injectived` binary if possible. If it is not on PATH,

```bash
npm i -g injective-core@latest
```

One-time commands can be run via `npx injective-core`, example: `npx injective-core --version`.
The rest of documentation will use `injectived` as a reference.

### 2) Use the CLI against the chain

Spot check critical paths (for example `query`, `tx`, `keys`) by running `injectived <path> --help`.

### 3) Refresh the CLI command map (as needed)

The command map should track the installed `injectived` binary. If you suspect a discrepancy between docs and the local binary, regenerate the map using the script in `scripts/` and diff it against the current map.

Example:

```bash
python3 scripts/map_injectived_cli.py --output /tmp/injectived-cli-map.new.md
diff -u references/injectived-cli-map.md /tmp/injectived-cli-map.new.md
```

## Account and Endpoint Conventions

- Use `~/.injectived` as the home dir for config and key material, unless overriden by user.
- Read endpoint and chain-id from `~/.injectived/config/client.toml` (fields: `node`, `chain-id`).
- Use these defaults when configuring the client:
  - mainnet endpoint: `https://sentry.tm.injective.network:443`
  - mainnet chain-id: `injective-1`
  - testnet endpoint: `https://testnet.sentry.tm.injective.network:443`
  - testnet chain-id: `injective-888`
- Keyring handling:
  - Default behavior uses a passphrase-protected file keyring.
  - If the keystore prompts for a passphrase, pipe it in:
    - `yes "passphrase" | timeout 10s injectived tx ...` (one-off/manual passphrase entry pattern)
    - `cat ~/.injectived/keystore_password.txt | timeout 10s injectived tx ...` (opt-in stored passphrase)
  - Agent behavior for persisted passphrase files:
    - Use `~/.injectived/keystore_password.txt` only when the user explicitly opts in to storing the passphrase on disk.
    - Treat this as sensitive local secret material (file mode `600`), and do not print passphrase contents in command output or logs.
    - Keep `timeout 10s` on keyring-touching commands to prevent hangs while waiting for unlock input.
  - `--keyring-backend test` is available and skips passphrase prompts, but it is not safe and leaves private keys exposed. Use only for local, disposable workflows.
  - Raw Ethereum private key import/export uses unsafe commands:
    - `injectived keys unsafe-export-eth-key <key_name>`
    - `injectived keys unsafe-import-eth-key <key_name> <hex_private_key>`
  - These commands are marked unsafe, but they are the required path for raw HEX private key workflows.
  - Never share raw HEX private keys in open channels or public communication.
- Ledger signing:
  - Use `--ledger --sign-mode amino-ledger` on Ledger-backed transactions.
  - Example:
    - `injectived tx bank send <from> <to> <amount> --ledger --sign-mode amino-ledger --chain-id injective-1 --gas auto --gas-prices 160000000inj --yes`
- Use `--yes` on transactions to skip interactive confirmation.
- Use `--gas auto --gas-adjustment 1.5 --gas-prices 160000000inj` for fee estimation.
- After broadcasting, verify with `injectived q tx <tx_hash>`.
- When creating a new keystore, store the passphrase in `~/.injectived/new_keystore_password.txt`, remind the user to remember it, and delete the file after use.

## Resources

### scripts/

- `map_injectived_cli.py`: Recursively runs `injectived <cmd> --help` to refresh the CLI mapping of commands.

### references/

- `injectived-cli-map.md`: Command map for the `injectived` binary.
