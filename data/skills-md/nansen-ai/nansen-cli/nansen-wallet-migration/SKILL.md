---
name: nansen-wallet-migration
description: Migrate an existing nansen-cli wallet from insecure password storage (env files, .credentials) to the new secure keychain-backed flow.
metadata:
  openclaw:
    requires:
      env:
        - NANSEN_API_KEY
      bins:
        - nansen
    primaryEnv: NANSEN_API_KEY
    install:
      - kind: node
        package: nansen-cli
        bins: [nansen]
allowed-tools: Bash(nansen:*)
---

# Wallet Migration — Old Flow to Secure Keychain

Use this skill when a user already has a nansen-cli wallet set up with the
**old** password storage method and wants to migrate to the new secure flow.

## When to use

- User mentions they stored their password in `~/.nansen/.env`, a `.env` file, or `memory.md`
- User gets the stderr warning: `⚠ Password loaded from insecure .credentials file`
- User asks to "secure my wallet" or "migrate to keychain"
- User created a wallet before the keychain update was released

## Detect current state

`wallet show` only displays addresses and does NOT load or check the password.
To detect the actual password situation, check for stored password sources:

```bash
# 1. Check if a wallet exists at all
nansen wallet list 2>&1

# 2. Check for insecure password stores
ls -la ~/.nansen/.env 2>/dev/null && echo "FOUND: ~/.nansen/.env (insecure)"
ls -la ~/.nansen/wallets/.credentials 2>/dev/null && echo "FOUND: .credentials file (insecure)"

# 3. Try an operation that requires the password (without setting env var)
nansen wallet export default 2>&1
```

Interpret the `export` output:
- `⚠ Password loaded from ~/.nansen/wallets/.credentials` on stderr → needs migration (Path B)
- Export succeeds silently → password is in keychain, no migration needed
- `PASSWORD_REQUIRED` JSON error → password not persisted anywhere (Path C or D)

## Migration paths

### Path A: Password in `~/.nansen/.env` (old skill pattern)

The previous wallet skill told agents to write the password to `~/.nansen/.env`.

**Step 1 — Ask the human for their password:**

> "Your wallet password is currently stored in ~/.nansen/.env, which is insecure.
> I can migrate it to your OS keychain. Please confirm the password you used when
> creating the wallet, or I can read it from ~/.nansen/.env if you authorize it."

**Step 2 — Migrate:**

The `source` and `nansen wallet secure` MUST run in the same shell so the env
var is available to the node process:

```bash
source ~/.nansen/.env 2>/dev/null && nansen wallet secure
```

**Step 3 — Verify the password actually decrypts the wallet:**

```bash
# Unset env var to prove keychain works, then export to verify decryption
unset NANSEN_WALLET_PASSWORD
nansen wallet export default 2>&1
```

If export succeeds (shows private keys), the migration worked. If it shows
`Incorrect password`, the wrong password was migrated — run `nansen wallet
forget-password` and retry with the correct password.

**Step 4 — Clean up the insecure file:**

```bash
rm -f ~/.nansen/.env
```

### Path B: Password in `.credentials` file (auto-saved fallback)

This happens when `wallet create` couldn't access the OS keychain (containers, CI).

```bash
nansen wallet secure
```

If the keychain is still unavailable (e.g. containerized Linux without D-Bus),
`nansen wallet secure` will explain the situation and suggest alternatives.

After migrating, verify decryption works:

```bash
nansen wallet export default 2>&1
```

### Path C: Password only in `NANSEN_WALLET_PASSWORD` env var

```bash
# Persist the env var password to keychain
nansen wallet secure
```

Then verify without the env var:

```bash
unset NANSEN_WALLET_PASSWORD
nansen wallet export default 2>&1
```

### Path D: Password lost entirely

The password cannot be recovered. The wallet's private keys are encrypted with
AES-256-GCM and the password is not stored anywhere recoverable.

**Tell the human:**

> "Your wallet password cannot be recovered. If you have funds in this wallet,
> they may be inaccessible. You can create a new wallet and transfer any remaining
> accessible funds."

```bash
# Create a fresh wallet (human must provide a new password)
NANSEN_WALLET_PASSWORD="<new_password_from_user>" nansen wallet create --name new-wallet
```

## Post-migration verification

After any migration, confirm the password was migrated correctly by proving
the keychain password can actually decrypt the wallet:

```bash
# Unset env var to prove keychain works
unset NANSEN_WALLET_PASSWORD

# This MUST succeed — it proves the keychain password decrypts the wallet
nansen wallet export default 2>&1
```

If export shows `Incorrect password`, the wrong password was saved to the
keychain. Fix with:

```bash
nansen wallet forget-password
NANSEN_WALLET_PASSWORD="<correct_password>" nansen wallet secure
```

If `stderr` still shows the `.credentials` warning, the keychain migration did
not succeed — check if the OS keychain service is running (`secret-tool` on Linux,
`security` on macOS).

## Forget password (all stores)

If the user wants to remove their persisted password entirely:

```bash
nansen wallet forget-password
```

This clears the password from both OS keychain and `.credentials` file. Future
wallet operations will require `NANSEN_WALLET_PASSWORD` env var or re-running
`nansen wallet secure`.

## Critical rules for agents

- **NEVER generate a password** — always ask the human
- **NEVER store the password** in files, memory, logs, or conversation history
- **NEVER use `--human` flag** — interactive prompts break agents
- If the human authorizes reading `~/.nansen/.env`, read it in the same command
  (`source ~/.nansen/.env && nansen wallet secure`) — do not echo or log the value
- **ALWAYS verify after migration** with `nansen wallet export default` — `wallet show` does NOT prove the password works (it never loads the password)
