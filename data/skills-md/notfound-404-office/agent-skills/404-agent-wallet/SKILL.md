---
name: 404-agent-wallet
description: Operate 404 private wallets and authorization packets on BSC with the bundled local CLI, including encrypted seed custody, wallet history recovery, ZK transaction preparation and cancellation, human-readable batch purchase quotes, packet inspection, and Binance Agentic Wallet preview and confirmed execution. Use when a user asks to create or restore a 404 wallet, inspect balances, orders, or history, quote a purchase, prepare or void a 404 action, or submit one through BAW.
---

# 404 Agent Wallet

This release is `0.2.0` and is Agent-only. It contains the wallet runtime, prover resources, chain readers and CLI; it does not contain the website UI.

**Capability gate:** If this Agent cannot use local tools or execute code, state that it cannot perform AI Mint and stop. Never claim a proof was generated, a mint ran, or a transaction reached the chain.

Use the bundled CLI for 404 wallet and transaction work. Read [references/usage.md](references/usage.md) before setup or any wallet, protocol, or Binance Agentic Wallet operation.

Resolve scripts from this skill's actual loaded `SKILL.md` directory, regardless of Agent or installation location. Run `node scripts/setup.mjs` there once: it uses the bundled SDK, complete circuits and proof assets, installs the locked agent-runtime and relayer dependencies, and restores proof resources. Then use `node --experimental-strip-types scripts/404.mjs ...` without requiring the user to set an SDK path. `--root` remains an optional override for a local checkout. Never assume a host-specific hidden directory.

## Boundaries

- Support BSC mainnet chain ID `56` only. Require a local verified deployment config for chain operations. Never invent a deployment address or reuse a Sepolia or Launchpad example as the 404 BSC deployment.
- The bundled public deployment config is `config/bsc-mainnet-404.json`; pass it explicitly with `--config` after reviewing it. It contains no private keys.
- Keep the 404 private wallet separate from the Binance Agentic Wallet. The local encrypted 404 seed owns private notes; BAW submits the prepared call, supplies gas, and may carry the exact value encoded by that call. Do not introduce MetaMask.
- Preserve the existing ZK prover and circuits. Preparing an authorization may create a real proof locally; do not replace, bypass, or describe it as a mock.
- Treat authorization packets and BAW preview state as bearer credentials. Store them only in private `0600` files under private `0700` directories.
- Keep each packet with its hash-bound `.intent.json` file. Review its amount/recipient/action as well as the encoded call; the proof alone does not reveal all private intent. Do not delete attempt records to bypass duplicate-submission protection.
- In this skill, mint runs only through the tool-enabled Agent path. If the controlled runtime or safe credential is unavailable, stop; do not substitute a manual web-mint claim. Users may independently choose the website or the Agent for later send, withdraw, and market operations.
- Do not invent Swap or liquidity operations. This release supports single-order fills and MarketV2 batch sweeping, but not Swap, add-liquidity, or remove-liquidity commands.
- `404Bundle` is an optional atomic action wrapper: it verifies a native-fee proof through the Pool and then executes one bound nested call. It is deployed for protocol compatibility, but the wallet skill does not invoke it directly.
- Wallet history is wallet-scoped, not the pool's public transaction feed. Never expose a seed, proof, or nullifier, and never infer private intent that neither the chain nor the local journal records.
- Wallet addresses support `--address-index N` for deterministic `pm/address/N` derivation with `N=0..255`; default `N=0` preserves existing behavior. This is local address derivation and does not create an on-chain account.
- Market order reads use the persistent local market snapshot and bounded Multicall3 batches when the RPC exposes Multicall3; the sequential read path remains as a compatibility fallback.
- History stores the verified head, wallet indexes and completed result in the private wallet directory. Repeating history at the same verified head is served locally; a changed head scans only the blocks after the verified history cursor and merges the new events.

## Secret handling

- Create the 404 seed in the local process and save only the project's encrypted vault format. A valid 24-word backup restores the same seed.
- Never request, receive, print, paste, or read a password, mnemonic, seed, witness, or full proof in chat. Never use `cat` or similar output on secret files.
- Use the tool-enabled App conversation plus its controlled background runtime as the primary mode. The user provisions the password through the platform's Secret manager or a local secret channel that exposes it only as a `0600` `--password-file` inside that runtime.
- TTY input is an optional initialization or maintenance path: let the local terminal request the password with hidden input, and ask twice for creation/import. Never pass a password value directly on the command line.
- If neither a protected password file nor a local TTY exists, stop the private operation. Do not ask for the credential in chat or claim execution succeeded.
- Do not create or print a mnemonic backup by default. Use `wallet create --mnemonic-file FILE` only after the user explicitly requests it, then remind them to move the `0600` file to offline storage.
- A chat-only bot gains no filesystem, process, wallet, or transaction authority merely by installing this skill. Do not claim that the unimplemented web intent/deep-link flow exists.

## Transaction workflow

1. Run `prepare`; it creates a private authorization packet and reserves its input notes, without broadcasting.
2. Run `inspect` and show the exact chain, target, operation, value, and calldata summary.
3. Run `baw preview`; it simulates but does not execute. Show `parsedTx`, `simulationResult`, `risks`, and `authorityChanges`.
4. Obtain explicit confirmation for this exact successful, unexpired preview and its `requestId`. A general instruction such as “follow risk controls” is not transaction confirmation. `requireConfirmation=false` does not remove this conversational confirmation requirement.
5. Only then run `baw execute ... --confirm REQUEST_ID`. Never execute automatically.

Stop on preview failure, expiry, interception, or risk-control rejection. Do not bypass controls or automatically preview/execute again. For `PENDING_CONFIRMATION` or an unknown result, run only the adapter's `baw status`; do not invent a `baw contract-call status` or `result` command.

If the user cancels or changes a prepared payment, use `prepare void --journal-id ORIGINAL_ID --out NEW_FILE`. For an exported request, this prepares a conflicting spend; inspect and submit that cancellation through the same confirmed BAW flow. Only chain confirmation invalidates the old payment and frees its notes. Never delete a journal or attempt record to unlock funds. Repeating preparation of an exported cancellation recovers its saved authorization instead of making another one. A request with no private input cannot be voided this way.

Use `balance.available` for unlocked, unreserved funds and `balance.max` for the largest amount spendable with the circuit's two inputs; it is not the total balance. `total` also includes `reserved` and `locked` amounts. Do not describe `total` as immediately spendable.

Mint remains one lot per transaction and at most ten lots per submitting BAW address; that address must hold the membership NFT. Do not weaken these checks.

For BAW-funded deposits, use `prepare deposit --amount AMOUNT --asset native|token`. The packet targets Pool `shield`; native deposits carry the exact BNB value encoded by the packet, while token deposits carry zero native value and require the BAW wallet to have token allowance. Inspect the target, asset, amount and value, then use the normal BAW preview and confirmation flow.

MarketV2 orders use raw note units. Both sides must be strictly above dust: token amounts must be greater than `1_000_000_000` raw units (10 404), and native amounts must be greater than `10_000` note units (0.0001 BNB). The CLI rejects a smaller or equal amount before proving. Integer rounding can make a near-full partial fill leave a sell-side residual at or below dust; the fill path and contract reject that fill. Use a full-order fill or cancel and relist with adjusted amounts when that happens. For `fill`, `--sell-asset` names the asset being sold by the selected order; the CLI rereads the order and rejects a mismatch before proving.

**Market maker asset warning:** this risk applies only when the maker uses a contract-controlled wallet that cannot later produce the required ECDSA signature. Ordinary EOA makers are not affected. Market order cancellation and maker asset release currently accept ECDSA signatures only; ERC-1271 contract signatures and other contract authorization paths are unsupported, so the maker's assets can otherwise become permanently locked.

For a batch purchase, accept ordinary token amounts and an optional BNB budget from the user. Run `quote sweep --amount DECIMAL [--budget DECIMAL] --out FILE`; the CLI reads on-chain listings, fees and dust constraints and writes the exact fills file. Never ask the user to write raw-unit JSON. Show the actual purchase amount, principal, protocol fee, total and order count, including any difference from the requested quantity. The budget includes principal and buyer protocol fees; BAW Gas is separate. Pass the returned `prepare` fields to `prepare sweep` internally. Do not invent prices or fees. Use one packet for at most 20 fills, then inspect, preview and obtain exact confirmation as above.

For wallet history, sync from the deployment block through one fixed verified head before returning results. Recover only this wallet's notes and order events, including passive fills found by the wallet's maker-key scan. Local journal entries may add private intent labels; without that journal, report unavailable private fields as unknown rather than fabricating them. Note totals include change notes, so received/spent/net do not equal transfer amount.
