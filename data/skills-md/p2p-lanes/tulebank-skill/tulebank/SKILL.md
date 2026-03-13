---
name: tulebank
description: TuleBank — check wallet balance, process invoice inbox messages, send ARS to any CVU/ALIAS, swap USDC/wARS, manage beneficiaries, and move funds with ARS off-ramp/on-ramp flows.
user-invocable: true
metadata: {"clawdbot":{"requires":{"bins":["tulebank"]}}}
---

You can send Argentine pesos (ARS) to any bank account via CVU or ALIAS and fund your wallet from ARS bank transfers using the `tulebank` CLI, which talks to a proxy that handles Ripio Ramps API credentials.

## CVU vs ALIAS

- **ALIAS**: a text string (e.g., `franv98`, `pilarcastilloz`, `tulezao`). If the user provides a word or short text, it's an alias.
- **CVU**: a 22-digit numeric string (e.g., `0000003100099123456789`). If the user provides a long number, it's a CVU.
- Both are valid destinations for `--to` in `beneficiaries add` and `send`.

## Important rules

- **ALWAYS confirm** the destination and action with the user before executing `tulebank send`. Use question format (e.g., "Should I send 3,000 ARS to Pilar Castillo (pilarcastilloz)?").
- **CLI only**: run TuleBank through CLI commands. Do not import files under `lib/` or run ad-hoc JavaScript to bypass the CLI.
- Use the installed `tulebank` binary for all commands in this skill.
- If `tulebank` is not available, ask the user to install it or fix PATH before continuing.
- When the user refers to someone by name or description (e.g., "la verdulería", "mi hermano"), search beneficiaries first.
- If multiple matches are found, ask the user to clarify.
- If no match is found and the user provides an alias or CVU, run `beneficiaries add --to <alias_or_cvu>` to register it. Ripio will return the holder's name, CUIT, and bank — show this to the user and ask for confirmation before sending. The `send` command requires an existing beneficiary; it will NOT auto-create one.
- Output from the CLI is JSON. Parse it and present it in a human-friendly way.
- The user must sign up before adding beneficiaries or sending. If not configured, run `tulebank signup` first.
- **OTP flow**: For existing Ripio users, `check-kyc` sends an OTP to their phone. You must ask the human for the 6-digit code and use `otp --code <code>` to validate.
- The `send` command creates an off-ramp session and returns deposit addresses. The user deposits USDC or wARS to that address, and Ripio converts to ARS and sends to the bank.
- If the user has a wallet configured (`tulebank wallet setup`), `send` can auto-send tokens with `--amount`. Omit `--token` for smart send (auto-picks wARS or swaps USDC→wARS).
- `--to` accepts beneficiary names (e.g., `--to Pili` matches "Pilar Castillo"). Word-prefix matching is supported.
- Auto-send shows a confirmation prompt with beneficiary, amount, and destination. The human must confirm before funds are sent. Use `--yes` to skip the prompt only after the human has already confirmed to you directly.
- **Fiat account activation**: Ripio only allows one enabled fiat account per customer. The `send` command automatically activates the target beneficiary's fiat account before sending. This may take a few extra seconds if the account was suspended.
- After auto-sending, show the transaction hash and run `tulebank history` to confirm the record.
- **Swaps**: Use `tulebank swap` to convert between USDC and wARS on Base. wARS converts 1:1 to ARS via off-ramp, so swapping USDC to wARS before sending can lock in the rate.
- **On-ramp (bank transfer)**: Use `tulebank onramp quote/create/status` for ARS -> wARS (default, session flow) or ARS -> USDC (order flow). Workstream 5 v1 supports `bank_transfer` only.
- **Inbox (invoice intake)**: Use `tulebank inbox` commands to inspect inbound emails, process extraction, and manage trusted senders/rules before triggering any payment.
- **ARS amounts → just use `--amount`, no `--token`**: When the user specifies an amount in ARS/pesos, ALWAYS use `--amount <n>` WITHOUT `--token`. The `--amount` value is in ARS. The CLI handles everything (picks wARS if available, or auto-swaps USDC→wARS). Never manually calculate USDC equivalents — it introduces rounding errors and the result won't be exact. Only use `--token USDC` when the user explicitly says they want to send USDC (not ARS).
- **History**: After every send, swap, or on-ramp create, call `tulebank history` to confirm the transaction was recorded.

## Available commands

Run these via the exec tool using the `tulebank` CLI binary.

### Wallet setup
```
tulebank wallet setup
```
Creates a CDP smart wallet on Base via the proxy (no local credentials needed).

### Wallet info
```
tulebank wallet info
```
Shows the wallet address.

### Wallet balance
```
tulebank wallet balance
```
Shows USDC, wARS, and ETH balances on Base.

### Sign up (prerequisite)
```
tulebank signup --email <email> --phone <phone>
```
Creates a TuleBank account, generates a per-user API key, and saves it to config. Only needed once. Use `tulebank setup --api-key <key>` to log in on another device.

### KYC flow (existing Ripio users)
```
tulebank check-kyc
tulebank otp --code <123456>
```
`check-kyc` triggers an OTP to the user's phone. Ask the human for the code, then validate with `otp`.

### Check KYC status
```
tulebank kyc-status
```

### Search beneficiaries
```
tulebank beneficiaries search "<query>"
```
Searches name, description, and CVU/ALIAS. Use this when the user refers to someone by name or description.

### List all beneficiaries
```
tulebank beneficiaries list
```

### Add a beneficiary
```
tulebank beneficiaries add --to <CVU_OR_ALIAS> [--name "<name>"] [--description "<desc>"]
```
Creates a fiat account via the proxy (creates + confirms + polls until enabled), then saves locally. If `--name` is omitted, the holder's name is auto-detected from Ripio (metadata includes name, CUIT, and bank). The response includes a `holder` field with the detected info — use this to confirm with the user.

### Send (off-ramp)
```
tulebank send --to <name/CVU_OR_ALIAS>
```
Sends to an existing beneficiary. The `--to` value is resolved via exact alias/CVU match or fuzzy name search. If the beneficiary is not found, the command errors and asks you to add them first with `tulebank beneficiaries add`.

### Send (off-ramp) — auto-send from wallet
```
tulebank send --to <CVU_OR_ALIAS> --amount <n> --token <USDC|wARS>
```
Creates off-ramp session and automatically sends tokens from the configured wallet to the Ripio deposit address on Base. Shows a confirmation prompt before sending. Add `--yes` to skip the prompt (only after human has confirmed to you). Use `--manual` to skip auto-send entirely.

### Swap tokens on Base
```
tulebank swap --from USDC --to wARS --amount 10
```
Swaps tokens via DEX on Base. Default slippage is 100 bps (1%). Use `--slippage <bps>` to change. Add `--yes` to skip confirmation (only after human has confirmed to you).

### Check off-ramp session status
```
tulebank send-status --session <session-id>
```
Shows deposit addresses and transactions for an off-ramp session.

### Get a quote
```
tulebank quote --from USDC --to ARS --amount 10 [--chain BASE]
```

### On-ramp quote (ARS -> wARS or USDC)
```
tulebank onramp quote --amount 50000 [--asset wARS|USDC] [--chain BASE]
```

### Create on-ramp flow (bank transfer)
```
tulebank onramp create --amount 50000 [--asset wARS|USDC] [--to-address 0x...] [--chain BASE]
```
Creates an on-ramp flow using a fresh quote. `wARS` (default) creates a session; `USDC` creates an order. Uses configured wallet address when available; pass `--to-address` to override.

### Check on-ramp status
```
tulebank onramp status --transaction <transaction-id> [--asset wARS|USDC]
```

### Inbox receiving address
```
tulebank inbox address
```

### List inbox messages
```
tulebank inbox list [--state <state>] [--classification <classification>]
```

### Show one inbox message
```
tulebank inbox show --id <message-id>
```

### Process one inbox message (extract payment details)
```
tulebank inbox process --id <message-id>
```

### Trusted sender management
```
tulebank inbox senders list
tulebank inbox senders add --email <email> [--primary]
tulebank inbox senders remove --email <email>
```

### Sender-specific extraction rules
```
tulebank inbox rules list
tulebank inbox rules upsert --sender <email> --prompt "<text>"
tulebank inbox rules remove --sender <email>
```

### Check transaction limits
```
tulebank limits
```

### Check fiat account status
```
tulebank fiat-account --id <fiat-account-id>
```

### Transaction history
```
tulebank history
tulebank history --beneficiary "<name>"
tulebank history --type send
tulebank history --type onramp
tulebank history --from 2026-01-01 --to-date 2026-01-31
```
Shows local transaction history. Supports filtering by beneficiary (fuzzy), type (`send`/`swap`/`onramp`), and date range. Default: last 30 days.

## Smart send rules

- `--amount` is always in ARS (= wARS, 1:1). Do NOT convert to USDC manually.
- When `--token` is omitted and `--amount` is given, the CLI auto-picks wARS (if balance sufficient) or swaps USDC→wARS first.
- When `--token` is specified, sends that token directly (no auto-swap).
- Example: user says "2300 pesos" → `--amount 2300` (NOT `--amount 1.57 --token USDC`).
- `--to` accepts beneficiary names (e.g., `--to Pili`). If one match is found, it auto-resolves. If multiple, it errors with a list.
- After every send, the transaction is recorded in `~/.tulebank/history.json`.

## Example flows

### User says: "mandale 10k a Pili"
1. Search beneficiaries → finds "Pilar Castillo (pilarcastilloz)"
2. Ask: "Pilar Castillo (pilarcastilloz) — le mando 10,000 ARS?"
3. On confirmation: run `send --to Pili --amount 10000 --yes`
4. Show transaction hash
5. Run `history --beneficiary Pili` to confirm the record

### User says: "mandale plata a la verdulería"
1. Run `beneficiaries search "verdulería"`
2. If found: ask "La Amistad (la verdulería cerca de casa) — le envío plata?"
3. On confirmation: run `send --to <their_alias>`
4. Show deposit address and instructions

### User says: "manda 2000 a franv98"
1. Run `beneficiaries search "franv98"` → not found
2. "franv98" is a text string → it's an alias. Run `beneficiaries add --to franv98` → Ripio returns holder info
3. Ask: "franv98 pertenece a FRANCISCO VARELA (CUIT 20385..., Banco Galicia). Le mando 2,000 ARS?"
4. On confirmation: run `send --to franv98 --amount 2000 --yes`
5. Show transaction hash
6. Run `history` to confirm the record

### User says: "send to 0000003100099123456789"
1. Run `beneficiaries search "0000003100099123456789"` → not found
2. 22-digit number → it's a CVU. Run `beneficiaries add --to 0000003100099123456789` → Ripio returns holder info
3. Ask: "Ese CVU pertenece a MARÍA GARCÍA (CUIT 27..., Banco Nación). Confirmo el envío?"
4. On confirmation: run `send --to 0000003100099123456789`
5. Show deposit address and instructions

### User says: "send to tulezao"
1. Run `beneficiaries search "tulezao"` → not found
2. "tulezao" is a text string → it's an alias. Run `beneficiaries add --to tulezao` → Ripio returns holder info
3. Ask: "El alias tulezao pertenece a JUAN PÉREZ (CUIT 20..., Banco Nación). Lo agrego y le envío?"
4. On confirmation: proceed with send

### Onboarding a new user (existing Ripio account)
1. Ask for their email and phone number
2. Run `signup --email <email> --phone <phone>`
3. Run `check-kyc` (sends OTP)
4. Ask human for the 6-digit code
5. Run `otp --code <code>`
6. Run `kyc-status` to verify COMPLETED

### Autonomous send (wallet configured)
1. Ask: "Le mando 10,000 ARS a Pilar Castillo (pilarcastilloz)?"
2. On confirmation: run `send --to pilarcastilloz --amount 10000 --yes`
   - `--amount` is ARS-denominated (10000 = 10,000 ARS). Do NOT convert to USDC.
   - The CLI handles token selection: uses wARS if available, otherwise auto-swaps USDC→wARS.
3. Show transaction hash from the response
4. Run `history` to confirm the record

### Swap USDC to wARS before sending
1. Run `wallet balance` to check USDC balance
2. Run `swap --from USDC --to wARS --amount 10`
3. Show swap result: "Swapped 10 USDC to ~14,380 wARS"
4. Run `send --to pilarcastilloz --amount 14380 --token wARS`
5. wARS converts 1:1 to ARS via off-ramp

### Checking a rate before sending
1. Run `quote --from USDC --to ARS --amount 10`
2. Tell user: "10 USDC = ~14,300 ARS at current rate"

### Funding wallet from ARS bank transfer
1. Run `onramp quote --amount 50000`
2. Ask user to confirm destination wallet address and amount.
3. Run `onramp create --amount 50000 --yes`
4. Show session/order ID + payment instructions.
5. Run `onramp status --transaction <id>` to track progress.

### Paying from inbox extraction
1. Run `inbox list` to locate candidate messages.
2. Run `inbox process --id <message-id>` and review `classification`, `destination_value`, and `amount`.
3. If `classification` is `payment_detected`, confirm payment details with the user.
4. On explicit user approval, run `send --to <destination_value> --amount <amount> --yes`.
5. Run `history` to confirm record creation.
