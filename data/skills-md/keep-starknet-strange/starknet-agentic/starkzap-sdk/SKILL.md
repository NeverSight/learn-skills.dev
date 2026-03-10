---
name: starkzap-sdk
description: "Use when integrating or maintaining applications built with keep-starknet-strange/starkzap. Covers StarkSDK setup, onboarding (Signer/Privy/Cartridge), wallet lifecycle, sponsored transactions, ERC20 transfers, staking flows, tx builder batching, examples, tests, and generated presets."
license: Apache-2.0
metadata:
  author: keep-starknet-strange
  version: "1.0.0"
  org: keep-starknet-strange
compatibility: "Node.js 20+, TypeScript 5+, starkzap repository workflows"
keywords:
  - starknet
  - starkzap
  - sdk
  - typescript
  - onboarding
  - wallet
  - privy
  - cartridge
  - paymaster
  - erc20
  - staking
  - tx-builder
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - Task
user-invocable: true
---

# Starkzap SDK

Project-focused guide for `https://github.com/keep-starknet-strange/starkzap`.

Use this skill when requests involve Starkzap SDK code, examples, or docs.

## When To Use

Trigger for tasks like:
- "Add a new onboarding flow in Starkzap"
- "Fix sponsored transaction behavior in wallet.execute"
- "Update staking pool logic or validator presets"
- "Patch Privy signer/server integration"
- "Review Starkzap tests/docs/examples"

## Repository Map

Primary implementation:
- `src/sdk.ts` - top-level orchestration (`StarkSDK`)
- `src/wallet/*` - wallet implementations and lifecycle
- `src/signer/*` - `StarkSigner`, `PrivySigner`, signer adapter
- `src/tx/*` - `Tx` and `TxBuilder`
- `src/erc20/*` - token helpers, balance/transfer logic
- `src/staking/*` - staking operations and pool discovery
- `src/types/*` - shared domain types (`Address`, `Amount`, config)

Operational and docs:
- `tests/*` and `tests/integration/*`
- `examples/web`, `examples/server`, `examples/mobile`, `examples/flappy-bird`
- `scripts/*` for generated artifacts in the Starkzap repo
- `docs/*` and `mintlify-docs/*`

Skill resources:
- `skills/starkzap-sdk/references/signer-integration.md` - signer trust boundaries and auth assumptions
- `skills/starkzap-sdk/references/sponsored-transactions.md` - paymaster flow and fee mode behavior
- `skills/starkzap-sdk/references/erc20-helpers.md` - `Amount` semantics and transfer patterns
- `skills/starkzap-sdk/references/staking-reliability.md` - pool discovery and timeout/abort safety
- `skills/starkzap-sdk/scripts/wallet-execute-example.ts` - wallet readiness and execute flow
- `skills/starkzap-sdk/scripts/staking-pool-discovery.ts` - staking pool discovery and diagnostics

## Quick Reference

Common starknet.js patterns (provider/account/call/execute/listen):

```typescript
import { Account, Contract, RpcProvider } from "starknet";

const provider = await RpcProvider.create({
  nodeUrl: process.env.RPC_URL!,
});

const account = new Account({
  provider,
  address: process.env.ACCOUNT_ADDRESS!,
  signer: process.env.PRIVATE_KEY!,
  cairoVersion: "1",
});

const contract = new Contract({
  abi,
  address: process.env.CONTRACT_ADDRESS!,
  providerOrAccount: account,
});
await contract.call("balance_of", [account.address]); // read

const tx = await account.execute([
  {
    contractAddress: process.env.CONTRACT_ADDRESS!,
    entrypoint: "do_work",
    calldata: [],
  },
]);
await provider.waitForTransaction(tx.transaction_hash);
```

```typescript
// With Starkzap Tx wrapper
const submitted = await wallet.execute(calls, { feeMode: "user_pays" });
const stop = submitted.watch(
  ({ finality, execution }) => console.log(finality, execution),
  { pollIntervalMs: 5000, timeoutMs: 120000 }
);
// stop(); // call to unsubscribe early
```

Common error classes and immediate recovery:

| Error Class | Typical Signal | Immediate Recovery |
| --- | --- | --- |
| `VALIDATION_ERROR` | `Invalid token decimals`, `Amount.parse(...)` failure | Re-check token decimals/symbol, parse from known token preset, avoid mixing token types. |
| `UNDEPLOYED_ACCOUNT` | `Account is not deployed` on `wallet.execute(...)` | Run `wallet.ensureReady({ deploy: "if_needed" })` before `user_pays` writes. |
| `RPC_OR_NETWORK` | timeout, 429, provider mismatch | Retry with backoff, confirm `rpcUrl` and `chainId`, switch to stable RPC for production. |
| `TX_REVERTED` | `preflight.ok === false` or reverted receipt | Run `wallet.preflight({ calls })`, inspect reason, reduce batch size, verify call ordering. |
| `AUTH_OR_PERMISSION` | Privy 401/403, invalid signature response | Verify signer server auth, headers/body resolver, and trusted `serverUrl`. |

See also:
- `skills/starkzap-sdk/references/*` for implementation-specific troubleshooting
- `skills/starkzap-sdk/scripts/*` for runnable diagnostic examples

## Core Workflows

### 1) Configure `StarkSDK` and Connect Wallets

Common API path:
1. Instantiate `StarkSDK` with `network` or `rpcUrl + chainId`.
2. Use `sdk.onboard(...)` or `sdk.connectWallet(...)`.
3. Call `wallet.ensureReady({ deploy: "if_needed" })` before user-pays writes.

Supported onboarding strategies:
- `OnboardStrategy.Signer`
- `OnboardStrategy.Privy`
- `OnboardStrategy.Cartridge`

For Cartridge:
- Treat as web-only runtime.
- Expect popup/session behavior and policy scoping requirements.

```typescript
import {
  ChainId,
  OnboardStrategy,
  StarkSDK,
  StarkSigner,
} from "starkzap";

const sdk = new StarkSDK({ network: "sepolia" });

const customSdk = new StarkSDK({
  rpcUrl: process.env.RPC_URL!,
  chainId: ChainId.SEPOLIA,
});

const signerResult = await sdk.onboard({
  strategy: OnboardStrategy.Signer,
  account: { signer: new StarkSigner(process.env.PRIVATE_KEY!) },
  feeMode: "user_pays",
  deploy: "if_needed",
});

const privyResult = await sdk.onboard({
  strategy: OnboardStrategy.Privy,
  privy: {
    resolve: async () => ({
      walletId: process.env.PRIVY_WALLET_ID!,
      publicKey: process.env.PRIVY_PUBLIC_KEY!,
      serverUrl: process.env.PRIVY_SIGNER_URL!,
    }),
  },
  feeMode: "sponsored",
});

const cartridgeResult = await sdk.onboard({
  strategy: OnboardStrategy.Cartridge,
  cartridge: {
    preset: "controller",
    policies: [{ target: "0xPOOL", method: "stake" }],
  },
});

const wallet = await sdk.connectWallet({
  account: { signer: new StarkSigner(process.env.PRIVATE_KEY!) },
  feeMode: "sponsored",
});

await wallet.ensureReady({ deploy: "if_needed" });
```

### 2) Execute Transactions (`wallet.execute`, `wallet.preflight`, `wallet.tx`)

Use:
- `wallet.execute(calls, options)` for direct execution.
- `wallet.preflight({ calls, feeMode })` for simulation checks.
- `wallet.tx()` (`TxBuilder`) for batched operations with deterministic ordering.

```typescript
const calls = [
  {
    contractAddress: process.env.CONTRACT_ADDRESS!,
    entrypoint: "do_work",
    calldata: [],
  },
];

const preflight = await wallet.preflight({
  calls,
  feeMode: "user_pays",
});
if (!preflight.ok) {
  throw new Error(`Preflight failed: ${preflight.reason}`);
}

const userPaysTx = await wallet.execute(calls, { feeMode: "user_pays" });
await userPaysTx.wait();

const sponsoredTx = await wallet.execute(calls, { feeMode: "sponsored" });
await sponsoredTx.wait();

const batchedTx = await wallet
  .tx()
  .add(...calls)
  .send({ feeMode: "sponsored" });
await batchedTx.wait();
```

```typescript
function getSdkErrorClass(error: unknown): string {
  const message = error instanceof Error ? error.message : String(error);
  if (message.includes("not deployed")) return "UNDEPLOYED_ACCOUNT";
  if (message.includes("timed out") || message.includes("429")) {
    return "RPC_OR_NETWORK";
  }
  if (message.includes("signature") || message.includes("Privy")) {
    return "AUTH_OR_PERMISSION";
  }
  if (message.includes("Invalid") || message.includes("Amount")) {
    return "VALIDATION_ERROR";
  }
  return "UNKNOWN";
}

try {
  await wallet.execute(calls, { feeMode: "user_pays" });
} catch (error) {
  const kind = getSdkErrorClass(error);
  if (kind === "UNDEPLOYED_ACCOUNT") {
    await wallet.ensureReady({ deploy: "if_needed" });
  }
  throw error;
}
```

When changing execution behavior:
- Audit deploy vs execute path for undeployed accounts.
- Verify runtime constraints (`OnboardStrategy.Cartridge` is web-only).
- Cover both `user_pays` and `sponsored` branches in tests.

### 3) ERC20 and Staking Scope

ERC20 notes (starkzap-sdk internal token operations, no avnu required):
- Validate `Amount` with the token preset used for the call.
- Keep multicall ordering explicit for batched transfers.

```typescript
import { Amount } from "starkzap";

const usdcAmount = Amount.parse("25", USDC);

try {
  const tx = await wallet
    .tx()
    .transfer(USDC, [
      { to: recipientA, amount: usdcAmount },
      { to: recipientB, amount: Amount.parse("5", USDC) },
    ])
    .send({ feeMode: "user_pays" });
  await tx.wait();
} catch (error) {
  // Re-parse Amount from the expected token preset before retrying.
  throw error;
}
```

Staking notes (starkzap-specific staking flows):
- Membership-sensitive operations: `enter`, `add`, `exit intent`, `exit`.
- Validate staking config and chain presets before execution.
- Verify timeout/abort behavior where pool resolution is involved.

For general DeFi operations (swaps, DCA, lending) and STRK staking via the avnu aggregator, use the `starknet-defi` skill.

### 4) Examples + Integration Surfaces

Check for drift between:
- `examples/web/main.ts`
- `examples/server/server.ts`
- `README` and docs links

Specifically verify endpoint and auth consistency for Privy + paymaster proxy flows.

## Guardrails

Do not hand-edit generated files:
- `src/erc20/token/presets.ts`
- `src/erc20/token/presets.sepolia.ts`
- `src/staking/validator/presets.ts`
- `src/staking/validator/presets.sepolia.ts`
- `docs/api/**`
- `docs/export/**`

Regenerate with scripts:

```bash
npm run generate:tokens
npm run generate:tokens:sepolia
npm run generate:validators
npm run generate:validators:sepolia
npm run docs:api
npm run docs:export
```

Keep API export changes explicit:
- If new public API is added/removed, update `src/index.ts`.

## Validation Checklist

Run minimal set first:

```bash
npm run typecheck
npm test
```

Run broader checks when behavior is cross-cutting:

```bash
npm run build
npm run test:all
```

Integration tests may require local devnet/fork setup:

```bash
npm run test:integration
```

If not run, clearly report why.

## Error Codes & Recovery

Map observed errors to actionable recovery:

| Error Class | Typical Trigger | Recovery Steps |
| --- | --- | --- |
| `VALIDATION_ERROR` | `Amount.parse(...)`/token mismatch, malformed address, invalid config | Confirm token decimals/symbol, re-create `Amount` from known token presets, validate config against `src/types/*` and `src/sdk.ts`. |
| `RPC_OR_NETWORK` | RPC timeout, `429`, transient JSON-RPC failures, chain mismatch | Retry with exponential backoff, check `rpcUrl`/`chainId`, verify provider health, reduce batch size for retries. |
| `TX_REVERTED` | `wallet.preflight(...)` fails or receipt is reverted | Run `wallet.preflight({ calls, feeMode })` first, inspect revert reason, reorder calls in `wallet.tx()`, split large multicalls. |
| `RATE_LIMIT_OR_TIMEOUT` | `tx.watch` timeout, stalled polling, pool resolution timeout | Increase timeout where appropriate, add abort handling, retry on fresh provider session, avoid parallel heavy queries. |
| `AUTH_OR_PERMISSION` | Privy signing errors, 401/403, invalid signature payloads | Verify signer server auth headers/body, validate trusted `serverUrl`, check `examples/server/server.ts` auth middleware alignment. |
| `UNDEPLOYED_ACCOUNT` | `wallet.execute(..., { feeMode: "user_pays" })` on undeployed account | Run `wallet.ensureReady({ deploy: "if_needed" })`, then retry execution; use sponsored mode only when paymaster path is configured. |
| `GENERATED_ASSET_DRIFT` | Preset/docs changes diverge from source of truth | Regenerate via `npm run generate:tokens`, `npm run generate:tokens:sepolia`, `npm run generate:validators`, `npm run generate:validators:sepolia`, `npm run docs:api`, `npm run docs:export`. |

If a fix is uncertain:
- Reproduce with the closest example in `examples/*`.
- Capture command, environment, and failing test IDs.
- Report exact file/path + remediation attempted.

## Useful Task Patterns

- **Bug fix in wallet lifecycle**:
  - inspect `src/wallet/index.ts`, `src/wallet/utils.ts`
  - patch
  - update `tests/wallet*.test.ts`

- **Privy auth/signature issue**:
  - inspect `src/signer/privy.ts`
  - align with `examples/server/server.ts`
  - update `tests/privy-signer.test.ts`

- **Staking regression**:
  - inspect `src/staking/staking.ts`, `src/staking/presets.ts`
  - add/adjust integration assertions in `tests/integration/staking.test.ts`

## Example Prompt

"Use this skill to fix Starkzap sponsored execution for undeployed accounts, add tests, and list behavior changes."
