---
name: hyperliquid-setup
description: Prepare the desk computer to work with Hyperliquid - install the SDKs, pick testnet or mainnet, verify connectivity, and (only when the user asks) provision a trade-only API wallet through the secure secret store and verify it is approved. Use during desk setup, when moving between research, testnet and mainnet levels, when a key is rotated, or when any Hyperliquid call fails with an environment problem.
license: MIT
metadata:
  version: "1.2.0"
  author: Galleon Labs
  category: hyperliquid
  network-default: testnet
---

# Hyperliquid setup

Sections 1-3 are read-only and safe to run at any time. Section 4 provisions a key and is done only when the user asks to move to a testnet or mainnet desk. Section 5 is the readiness check the Execution Trader runs before its first send.

## 1. Networks

| | Mainnet | Testnet |
| --- | --- | --- |
| REST | `https://api.hyperliquid.xyz` | `https://api.hyperliquid-testnet.xyz` |
| WebSocket | `wss://api.hyperliquid.xyz/ws` | `wss://api.hyperliquid-testnet.xyz/ws` |
| App | `https://app.hyperliquid.xyz` | `https://app.hyperliquid-testnet.xyz` |
| Faucet | - | `https://app.hyperliquid-testnet.xyz/drip` |

Reads (`/info`) need no key. Writes (`/exchange`) need a signing key and are signed differently per network, so a key and its network go together. The desk records the network in `/workspace/trading-desk/desk.md` and in the environment.

Testnet is the default. Nothing on the desk selects mainnet unless `HYPERLIQUID_NETWORK=mainnet` is set on purpose.

## 2. Install

Python (used by most snippets on the desk):

```bash
python3 --version                                  # 3.9+ required, 3.11+ preferred
python3 -m pip install --user --upgrade "hyperliquid-python-sdk>=0.24,<1" \
  || python3 -m pip install --break-system-packages --upgrade "hyperliquid-python-sdk>=0.24,<1"
python3 -c "import hyperliquid, eth_account; print('ok', hyperliquid.__name__)"
```

Optional TypeScript (if the user prefers TS or wants the WebSocket client from `@nktkas/hyperliquid`):

```bash
node --version                                      # 22.12+ required by @nktkas/hyperliquid (ESM-only)
mkdir -p /workspace/trading-desk/ts && cd /workspace/trading-desk/ts
[ -f package.json ] || npm init -y >/dev/null
npm pkg set type=module >/dev/null                  # so .js files can use import and top-level await
npm i @nktkas/hyperliquid viem
node -e "import('@nktkas/hyperliquid').then(m=>console.log('ok', Object.keys(m).length))"
```

`curl` and `jq` are enough for every read in `hyperliquid-market-data` and `hyperliquid-account`; install `jq` if missing.

## 3. Connectivity check (no key)

```bash
for base in https://api.hyperliquid.xyz https://api.hyperliquid-testnet.xyz; do
  printf '%s -> ' "$base"
  curl -sS -m 10 -X POST "$base/info" -H 'Content-Type: application/json' \
    -d '{"type":"allMids"}' | jq -r 'if type=="object" then "ok, \(length) mids, BTC \(.BTC)" else "unexpected: \(.)" end'
done
```

Both lines should read `ok`. Record the time and result in the desk record. If one network fails, the desk is not blind on the other; say which.

## 4. API wallet (only when the user asks to trade)

An **API wallet** (Hyperliquid also calls it an agent wallet) is a separate key the user authorises to sign trading actions for their account. It can place, modify and cancel orders and change leverage and margin; it cannot withdraw to Arbitrum, cannot send USDC or tokens to another wallet, and cannot approve other agents or builders (those need the main wallet's signature). It *can* still move funds inside the user's own account (perp to spot and across dexs via `agentSendAsset`, into sub-accounts and vaults, and it can spend USDC on `reserveRequestWeight`), all of which the desk forbids by rule. That is the only kind of key that ever reaches the desk computer.

Why: all of the user's Bots share one computer, so anything on it is readable by every Bot. A trade-only key bounds the damage; a seed phrase or main-wallet key would not.

### 4.1 The user creates it in the Hyperliquid app

Guide the user; do not do it for them (it involves their wallet):

1. Open the app for the chosen network (`https://app.hyperliquid.xyz` or `https://app.hyperliquid-testnet.xyz`), connect the main wallet, open the **API** page (`/API`, under **More** in the app's navigation).
2. Generate a new API wallet, give it a name such as `hypergrok-desk`, choose a validity period (a few months is sensible; it can be revoked at any time), and **Authorize**. The app shows the API wallet's private key once. The API wallet's address is shown next to it.
3. On testnet, fund the account from the faucet (`/drip`): it gives 1,000 mock USDC, but only to an address that has deposited on mainnet at some point (email/Privy logins get different addresses per network; export the mainnet wallet into a wallet extension and connect that to testnet). Testnet USDC is not real.

Never ask for the seed phrase or the main wallet's key. If the user offers it, decline and point back to this step.

### 4.2 The user provides the key through the secure secret store

Grok Bot has a secure secret card for exactly this. Ask the user to add a secret named `HYPERLIQUID_PRIVATE_KEY` with the API wallet's private key. Never ask them to paste it in chat and never write it to a file under `/workspace`.

If the desk's Grok Bot setup exposes secrets to the computer as environment variables, scripts read `HYPERLIQUID_PRIVATE_KEY` from the environment. If it does not, the user has two other choices, both made while in control of the computer: a secrets-manager command, or a locked-down file. A Claude Code session, the engine service and a cron line all resolve the key the same way; nothing about the key changes between runtimes.

The loader is `engine/secrets.py`, and every signing path on the desk (`scripts/desk_send.py` and the testnet rehearsal snippets) uses it. Resolution order, first hit wins:

1. `HYPERLIQUID_PRIVATE_KEY` in the environment.
2. `HYPERGROK_KEY_COMMAND`: a command line, run without a shell, whose stdout is the key (for example `op read op://Trading/hyperliquid-api-wallet/private-key`; recipes for 1Password, AWS, GCP, Azure, Vault and Doppler are in `desk-operations` section 1). It gets a 20 second budget and runs with the service's own identity, so the manager's access policy is the boundary.
3. `HYPERGROK_KEY_FILE`, else `~/.hyperliquid/api-wallet.key`: a file the user creates, which must be mode 600 (or 400) and owned by the running user, or it is refused:

```bash
mkdir -p ~/.hyperliquid && chmod 700 ~/.hyperliquid
# the user pastes the key into this file themselves, then:
chmod 600 ~/.hyperliquid/api-wallet.key
```

The key must be a 32-byte hex string; anything else is refused before it reaches the SDK. The loader never prints the key, never puts it in an exception, and reports only which source it used (`desk_send.py --dry-run` shows that line). From Python, `from engine.secrets import load_key, describe` gives the same behaviour to a rehearsal snippet; do not write a private loader of your own.

### 4.3 Non-secret configuration

Set these for the desk computer's shell (for example in `~/.bashrc`, and mirror them in `desk.md`):

```bash
export HYPERLIQUID_NETWORK=testnet                 # or mainnet, deliberately
export HYPERLIQUID_ACCOUNT_ADDRESS=0xYourMainAccount   # the account the API wallet acts for, NOT the API wallet's address
```

The account address is public. Reads use it; `desk_send.py` checks it against the ticket and passes it as `account_address` when signing with the API wallet. No `HYPERGROK_DESK_ROOT` variable is needed: every desk script takes `--desk-root` explicitly.

## 5. Readiness check (before the first send)

Run by the Execution Trader; read-only; proves the key belongs to the account on this network without sending anything.

```python
import os, sys
import eth_account
from hyperliquid.info import Info
from hyperliquid.utils import constants
sys.path.insert(0, "/workspace/hypergrok")
from engine.secrets import load_key, describe          # section 4.2: env, then HYPERGROK_KEY_COMMAND, then the 600 file
print("key source:", describe())                         # the source, never the value

network = os.environ.get("HYPERLIQUID_NETWORK", "testnet")
base = constants.MAINNET_API_URL if network == "mainnet" else constants.TESTNET_API_URL
account = os.environ["HYPERLIQUID_ACCOUNT_ADDRESS"]
agent_addr = eth_account.Account.from_key(load_key()).address   # derived locally, key never printed

info = Info(base, skip_ws=True)
role = info.user_role(agent_addr)                       # {"role": "agent", "data": {"user": "0x..."}} when approved
agents = info.extra_agents(account)                     # named agents: [{"address","name","validUntil"}, ...]
listed = any(a["address"].lower() == agent_addr.lower() for a in agents)
acts_for_account = role.get("role") == "agent" and role.get("data", {}).get("user", "").lower() == account.lower()
approved = acts_for_account or listed                   # an unnamed agent is valid but may not appear in extraAgents
state = info.user_state(account)

print(f"network={network} account={account}")
print(f"api_wallet={agent_addr} role={role.get('role')} approved_for_account={approved}")
for a in agents:
    if a["address"].lower() == agent_addr.lower():
        print(f"valid_until_ms={a.get('validUntil')} name={a.get('name')}")
print(f"account_value={state['marginSummary']['accountValue']} positions={len(state['assetPositions'])}")
```

Ready means: `role=agent`, `approved_for_account=True`, `validUntil` in the future (when the agent is named and listed), and `account_value` is what the user expects on this network. Anything else: stop and report which line disagrees.

## 6. Rotation and revocation

- Revoke: the user removes the API wallet on the app's `/API` page. Sends from the desk fail immediately afterwards.
- Rotate: revoke, create a new API wallet (4.1), replace the secret where it lives (4.2: the secret card, one edit in the secrets manager, or the 600 file), rerun the readiness check. Journal the time.
- Suspected misuse: revoke first, investigate second (`desk-incident-response` playbook G).

## Pitfalls

- Using the API wallet's address as `HYPERLIQUID_ACCOUNT_ADDRESS`. Reads on the agent's address show an empty account; the account is the main wallet's address.
- Signing for mainnet with a testnet key or vice versa. The signature encodes the network; the exchange rejects the mismatch, but the desk should never get that far.
- Installing the SDK into a temporary environment that does not survive a computer refresh. Prefer `--user`; re-run section 2 if imports fail after a restart.
- `Info(...)` performs network calls on construction; pass `skip_ws=True` unless you want the WebSocket thread.
- Printing environment variables while debugging. Redact anything that could be the key.
