---
name: wallet-integration
description: "Integrate wallets with IC dApps using ICRC signer standards (ICRC-21/25/27/29/49). Covers the popup-based signer model, consent messages, permission lifecycle, and transaction approval flows. Implementation uses @dfinity/oisy-wallet-signer. Do NOT use for Internet Identity login, delegation-based auth (ICRC-34/46), or threshold signing (chain-key). Use when the developer mentions wallet integration, OISY, oisy-wallet-signer, wallet signer, relying party, consent messages, wallet popup, or transaction approval."
license: Apache-2.0
compatibility: "Node.js >= 22"
metadata:
  title: Wallet Integration
  category: Wallet
---

# Wallet Integration

## What This Is

Wallet integration on the Internet Computer uses the ICRC signer standards — a popup-based model where every action requires explicit user approval via JSON-RPC 2.0 over `window.postMessage`.

This skill covers integration using `@dfinity/oisy-wallet-signer`. Other integration paths (IdentityKit, signer-js) exist but are not covered here.

**The signer model = explicit per-action approval.** `connect()` establishes a channel. Nothing more.

**It is not:**

- A session system
- A delegated identity (no ICRC-34)
- A background executor

**ICRC standards implemented:**

- ICRC-21 — Canister call consent messages
- ICRC-25 — Signer interaction standard (permissions)
- ICRC-27 — Accounts
- ICRC-29 — Window PostMessage transport
- ICRC-49 — Call canister

**Not implemented:**

- ICRC-46 — Session-based delegation (not supported; use a delegation-capable model if you need sessions)

## When to Use

- Clear, intentional, high-value actions: token transfers (ICP / ICRC-1 / ICRC-2), NFT mint/claim, single approvals
- Funding / deposit flows: "Top up", "Deposit into protocol"
- Any action where a confirmation dialogue per operation feels natural

## When NOT to Use

- **Delegation or sessions**: sign once / act many times, background execution, autonomous behaviour
- **High-frequency interactions**: games, social actions, rapid write operations
- **Invisible writes**: autosave, cron jobs, auto-compounding

> **Decision test:** If your app still feels good when every meaningful update shows a confirmation dialogue, this library is appropriate. If not, use a delegation-capable model instead.

## Prerequisites

- `@dfinity/oisy-wallet-signer` installed
- Peer dependencies installed: `@dfinity/utils`, `@dfinity/zod-schemas`, `@icp-sdk/canisters`, `@icp-sdk/core`, `zod`
- A non-anonymous identity on the signer side (e.g. `Ed25519KeyIdentity`)
- For local development: a running local network (`icp network start -d`)

```bash
npm i @dfinity/oisy-wallet-signer @dfinity/utils @dfinity/zod-schemas @icp-sdk/canisters @icp-sdk/core zod
```

## How It Works

### End-to-End Lifecycle

```text
1. dApp: IcrcWallet.connect({url})              → opens popup, polls icrc29_status
2. dApp: wallet.requestPermissionsNotGranted()   → prompts user if needed
3. dApp: wallet.accounts()                       → signer prompts, returns accounts
4. dApp: wallet.transfer({...})                  → signer fetches ICRC-21 consent message
                                                    → signer prompts user with consent
                                                    → signer executes canister call
                                                    → returns block index
5. dApp: wallet.disconnect()                     → closes popup, cleans up
```

## Pitfalls

1. **Importing classes from the wrong entry point.** `Signer`, `RelyingParty`, `IcpWallet`, and `IcrcWallet` are **not** exported from the main entry point. Import them from their dedicated subpaths or you get `undefined`.

   ```typescript
   // WRONG — will fail
   import {Signer} from '@dfinity/oisy-wallet-signer';

   // CORRECT
   import {Signer} from '@dfinity/oisy-wallet-signer/signer';
   import {IcpWallet} from '@dfinity/oisy-wallet-signer/icp-wallet';
   import {IcrcWallet} from '@dfinity/oisy-wallet-signer/icrc-wallet';
   ```

2. **Using `IcrcWallet` without `ledgerCanisterId`.** Unlike `IcpWallet` (which defaults to the ICP ledger `ryjl3-tyaaa-aaaaa-aaaba-cai`), `IcrcWallet.transfer()`, `.approve()`, and `.transferFrom()` all **require** `ledgerCanisterId`. Omitting it causes a runtime error.

3. **Forgetting to register prompts on the signer side.** The signer returns error 501 (`PERMISSIONS_PROMPT_NOT_REGISTERED`) if a request arrives and no prompt handler is registered for it. Register all four prompts (`ICRC25_REQUEST_PERMISSIONS`, `ICRC27_ACCOUNTS`, `ICRC21_CALL_CONSENT_MESSAGE`, `ICRC49_CALL_CANISTER`) before the signer can handle any relying party traffic.

4. **Sending concurrent requests to the signer.** The signer processes one request at a time. A second request while one is in-flight returns error 503 (`BUSY`). Serialize your calls — wait for each response before sending the next. Read-only methods (`icrc29_status`, `icrc25_supported_standards`) are exempt.

5. **Assuming `connect()` = authenticated session.** `connect()` only opens a `postMessage` channel. The user has not pre-authorized anything. Permissions default to `ask_on_use` — the signer will prompt the user on first use of each method. Call `requestPermissionsNotGranted()` after connecting to request all permissions upfront in a single prompt instead of per-method prompts.

6. **Not handling the consent message state machine.** The `ICRC21_CALL_CONSENT_MESSAGE` prompt fires multiple times with different statuses: `loading` → `result` | `error`. If you only handle `result`, the UI breaks on loading and error states. Always branch on `payload.status`.

7. **`sender` not matching `owner`.** The signer validates that `sender` in every `icrc49_call_canister` request matches the signer's `owner` identity. A mismatch returns error 502 (`SENDER_NOT_ALLOWED`). Always use the `owner` from `accounts()`.

8. **Not calling `disconnect()`.** Both `Signer.disconnect()` and `wallet.disconnect()` must be called on clean-up. Forgetting this leaks event listeners and leaves popup windows open.

9. **Ignoring permission expiration.** Permissions default to a 7-day validity period. After expiry, they silently revert to `ask_on_use`. Don't cache permission state client-side beyond a session.

10. **Auto-triggering signing on connect.** Never fire a canister call immediately after `connect()`. Let the user initiate the action. The signer is designed for intentional, user-driven operations.

## Implementation

### Import Map

```typescript
// Constants, errors, and types — from main entry point
import {
  ICRC25_REQUEST_PERMISSIONS,
  ICRC25_PERMISSION_GRANTED,
  ICRC25_PERMISSION_DENIED,
  ICRC25_PERMISSION_ASK_ON_USE,
  ICRC27_ACCOUNTS,
  ICRC21_CALL_CONSENT_MESSAGE,
  ICRC49_CALL_CANISTER,
  DEFAULT_SIGNER_WINDOW_CENTER,
  DEFAULT_SIGNER_WINDOW_TOP_RIGHT,
  RelyingPartyResponseError,
  RelyingPartyDisconnectedError
} from '@dfinity/oisy-wallet-signer';

import type {
  PermissionsPromptPayload,
  AccountsPromptPayload,
  ConsentMessagePromptPayload,
  CallCanisterPromptPayload,
  IcrcAccounts,
  SignerOptions,
  RelyingPartyOptions
} from '@dfinity/oisy-wallet-signer';

// Classes — from dedicated subpaths
import {Signer} from '@dfinity/oisy-wallet-signer/signer';
import {RelyingParty} from '@dfinity/oisy-wallet-signer/relying-party';
import {IcpWallet} from '@dfinity/oisy-wallet-signer/icp-wallet';
import {IcrcWallet} from '@dfinity/oisy-wallet-signer/icrc-wallet';
```

### dApp Side (Relying Party)

#### Choosing the Right Class

| Class          | Use for                                                                      |
| -------------- | ---------------------------------------------------------------------------- |
| `IcpWallet`    | ICP ledger operations — `ledgerCanisterId` optional (defaults to ICP ledger) |
| `IcrcWallet`   | Any ICRC ledger — `ledgerCanisterId` **required**                            |
| `RelyingParty` | Low-level custom canister calls via protected `call()`                       |

#### Connect, Permissions, Accounts

```typescript
const wallet = await IcrcWallet.connect({
  url: 'https://your-wallet.example.com/sign', // URL of the wallet implementing the signer
  host: 'https://icp-api.io',
  windowOptions: {width: 576, height: 625, position: 'center'},
  connectionOptions: {timeoutInMilliseconds: 120_000},
  onDisconnect: () => {
    /* wallet popup closed */
  }
});

const {allPermissionsGranted} = await wallet.requestPermissionsNotGranted();

const accounts = await wallet.accounts();
const {owner} = accounts[0];
```

#### IcpWallet — ICP Transfers and Approvals

Uses `{owner, request}` — no `ledgerCanisterId` needed.

```typescript
const wallet = await IcpWallet.connect({url: 'https://your-wallet.example.com/sign'});
const accounts = await wallet.accounts();
const {owner} = accounts[0];

await wallet.icrc1Transfer({
  owner,
  request: {to: {owner: recipientPrincipal, subaccount: []}, amount: 100_000_000n}
});

await wallet.icrc2Approve({
  owner,
  request: {spender: {owner: spenderPrincipal, subaccount: []}, amount: 500_000_000n}
});
```

#### IcrcWallet — Any ICRC Ledger

Uses `{owner, ledgerCanisterId, params}` — `ledgerCanisterId` is **required**.

```typescript
const wallet = await IcrcWallet.connect({url: 'https://your-wallet.example.com/sign'});
const accounts = await wallet.accounts();
const {owner} = accounts[0];

await wallet.transfer({
  owner,
  ledgerCanisterId: 'mxzaz-hqaaa-aaaar-qaada-cai',
  params: {to: {owner: recipientPrincipal, subaccount: []}, amount: 1_000_000n}
});

await wallet.approve({
  owner,
  ledgerCanisterId: 'mxzaz-hqaaa-aaaar-qaada-cai',
  params: {spender: {owner: spenderPrincipal, subaccount: []}, amount: 5_000_000n}
});

await wallet.transferFrom({
  owner,
  ledgerCanisterId: 'mxzaz-hqaaa-aaaar-qaada-cai',
  params: {from: {owner: fromPrincipal, subaccount: []}, to: {owner: toPrincipal, subaccount: []}, amount: 1_000_000n}
});
```

#### Query Methods and Disconnect

```typescript
const standards = await wallet.supportedStandards();
const currentPermissions = await wallet.permissions();

await wallet.disconnect();
```

#### Error Handling (dApp Side)

```typescript
try {
  await wallet.transfer({...});
} catch (err) {
  if (err instanceof RelyingPartyResponseError) {
    switch (err.code) {
      case 3000: /* PERMISSION_NOT_GRANTED */ break;
      case 3001: /* ACTION_ABORTED — user rejected */ break;
      case 4000: /* NETWORK_ERROR */ break;
    }
  }
  if (err instanceof RelyingPartyDisconnectedError) {
    /* popup closed unexpectedly */
  }
}
```

### Wallet Side (Signer)

#### Initialise and Register All Prompts

```typescript
const signer = Signer.init({
  owner: identity,
  host: 'https://icp-api.io',
  sessionOptions: {
    sessionPermissionExpirationInMilliseconds: 7 * 24 * 60 * 60 * 1000
  }
});

signer.register({
  method: ICRC25_REQUEST_PERMISSIONS,
  prompt: ({requestedScopes, confirm, origin}: PermissionsPromptPayload) => {
    confirm(
      requestedScopes.map(({scope}) => ({
        scope,
        state: userApproved ? ICRC25_PERMISSION_GRANTED : ICRC25_PERMISSION_DENIED
      }))
    );
  }
});

signer.register({
  method: ICRC27_ACCOUNTS,
  prompt: ({approve, reject, origin}: AccountsPromptPayload) => {
    approve([{owner: identity.getPrincipal().toText()}]);
  }
});

signer.register({
  method: ICRC21_CALL_CONSENT_MESSAGE,
  prompt: (payload: ConsentMessagePromptPayload) => {
    if (payload.status === 'loading') {
      // show spinner
    } else if (payload.status === 'result') {
      // payload.consentInfo: { Ok: ... } (from canister) or { Warn: ... } (signer-generated fallback)
      // show consent UI, then: payload.approve() or payload.reject()
    } else if (payload.status === 'error') {
      // show error, optionally payload.details
    }
  }
});

signer.register({
  method: ICRC49_CALL_CANISTER,
  prompt: (payload: CallCanisterPromptPayload) => {
    if (payload.status === 'executing') {
      /* show progress */
    } else if (payload.status === 'result') {
      /* call succeeded */
    } else if (payload.status === 'error') {
      /* call failed */
    }
  }
});

```

#### Consent Message: `Ok` vs `Warn`

- `{ Ok: consentInfo }` — canister implements ICRC-21; message is canister-verified
- `{ Warn: { consentInfo, canisterId, method, arg } }` — signer generated a fallback (for `icrc1_transfer`, `icrc2_approve`, `icrc2_transfer_from`)

Always distinguish these in the UI — warn the user when the message is signer-generated.

#### Disconnect

```typescript
signer.disconnect();
```

### Error Code Reference

| Code | Name                                | Meaning                     |
| ---- | ----------------------------------- | --------------------------- |
| 500  | `ORIGIN_ERROR`                      | Origin mismatch             |
| 501  | `PERMISSIONS_PROMPT_NOT_REGISTERED` | Missing prompt handler      |
| 502  | `SENDER_NOT_ALLOWED`                | `sender` ≠ `owner`          |
| 503  | `BUSY`                              | Concurrent request rejected |
| 504  | `NOT_INITIALIZED`                   | Owner identity not set      |
| 1000 | `GENERIC_ERROR`                     | Catch-all                   |
| 2000 | `REQUEST_NOT_SUPPORTED`             | Method not supported        |
| 3000 | `PERMISSION_NOT_GRANTED`            | Permission denied           |
| 3001 | `ACTION_ABORTED`                    | User cancelled              |
| 4000 | `NETWORK_ERROR`                     | IC call failure             |

### Permission States

| State      | Constant                       | Behavior                          |
| ---------- | ------------------------------ | --------------------------------- |
| Granted    | `ICRC25_PERMISSION_GRANTED`    | Proceeds without prompting        |
| Denied     | `ICRC25_PERMISSION_DENIED`     | Rejected immediately (error 3000) |
| Ask on use | `ICRC25_PERMISSION_ASK_ON_USE` | Prompts user on access (default)  |

Permissions stored in `localStorage` as `oisy_signer_{origin}_{owner}` with timestamps. Default validity: 7 days.

## Deploy & Test

### Local Development — Your Own Signer

If you are building both the dApp and the wallet/signer, start a local network and pass `host` to both sides:

```bash
icp network start -d
```

```typescript
// dApp side — point to your local wallet's /sign route
const wallet = await IcrcWallet.connect({
  url: 'http://localhost:5174/sign',
  host: 'http://localhost:8000'
});

// Wallet/signer side — same local network host
const signer = Signer.init({
  owner: identity,
  host: 'http://localhost:8000'
});
```

### Local Development — Using the Pseudo Wallet Signer

If you are building a dApp (relying party) and need a signer to test against locally, the library provides a pseudo wallet signer in its demo:

```bash
git clone https://github.com/dfinity/oisy-wallet-signer
cd oisy-wallet-signer
npm ci

cd demo
npm ci
npm run sync:all
npm run dev:wallet    # starts the pseudo wallet on port 5174
```

Then connect from your dApp:

```typescript
const wallet = await IcpWallet.connect({
  url: 'http://localhost:5174/sign',
  host: 'http://localhost:8000' // match your local network port
});
```

### Mainnet

On mainnet, point to the wallet's production signer URL and omit `host` (defaults to `https://icp-api.io`):

```typescript
const wallet = await IcpWallet.connect({
  url: 'https://your-wallet.example.com/sign'
});
```

## Expected Behavior

### Connection

- `connect()` resolves with a wallet instance; throws `RelyingPartyDisconnectedError` on timeout
- `wallet.supportedStandards()` returns an array containing at least ICRC-21, ICRC-25, ICRC-27, ICRC-29, ICRC-49

### Permissions

- `requestPermissionsNotGranted()` triggers the signer's permissions prompt
- After approval, `wallet.permissions()` returns scopes with state `granted`
- A second call returns `{allPermissionsGranted: true}` without prompting again

### Accounts

- `wallet.accounts()` returns at least one `{owner: string}` (principal as text)
- The returned `owner` matches the signer's identity principal

### Transfers and Approvals

- `icrc1Transfer()` / `transfer()`, `icrc2Approve()` / `approve()`, and `transferFrom()` all resolve with a `bigint` block index
- Each triggers the consent message prompt on the signer before execution

