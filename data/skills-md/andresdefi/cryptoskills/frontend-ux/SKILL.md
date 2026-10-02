---
name: frontend-ux
description: "dApp frontend UX patterns and production readiness — wallet connection flows (RainbowKit, multi-state), four-state transaction lifecycle, error handling taxonomy (4001 user rejection, insufficient funds, revert decoding), gas estimation with USD display, network switching, approval patterns (infinite vs exact, Permit2), mobile wallet support (WalletConnect v2, EIP-6963), and production QA checklist."
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: multichain
  category: Frontend
tags:
  - frontend
  - ux
  - wallet-connection
  - transactions
  - error-handling
  - rainbowkit
  - wagmi
  - mobile
---

# frontend-ux

Production UX patterns for dApp frontends. Covers the full user journey from wallet connection through transaction confirmation, with error handling, gas estimation, approval flows, mobile support, and a production QA checklist. Built on wagmi v2, viem, and RainbowKit.

## What You Probably Got Wrong

> Most dApp frontends ship with broken UX because developers treat wallet connection as a button click and transactions as a loading spinner. Both are state machines with multiple failure modes that users encounter constantly.

- **Wallet connection is a four-state machine, not a button** -- The states are `disconnected`, `connecting`, `connected`, and `wrong-network`. Showing a single "Connect Wallet" button that flips to "Connected" misses the `connecting` spinner (important on mobile where WalletConnect takes seconds), the `wrong-network` prompt (users will be on mainnet when your dApp is on Base), and auto-reconnection on page reload (flash of disconnected state).
- **Transactions have four states, not a loading spinner** -- The states are `idle`, `awaiting-signature` (wallet popup open), `pending` (tx submitted, waiting for block inclusion), and `confirmed-or-failed`. Each state needs distinct UI. Users sitting at "Loading..." don't know if they need to open their wallet, wait for the chain, or if something failed.
- **User rejection (code 4001) is NOT an error** -- When a user clicks "Reject" in their wallet, most dApps show a red error toast. This is wrong. The user intentionally cancelled. Silently reset back to the idle state. Reserve error toasts for actual failures.
- **Users don't know what gas is** -- Showing "Gas: 21000 gwei" means nothing to 99% of users. Convert gas cost to USD using a price feed. Show "Network fee: ~$0.42" instead. If you must show technical details, put them behind an expandable "Details" section.
- **Mobile dApp UX is fundamentally different** -- On desktop, browser wallets inject providers. On mobile, the user's wallet IS the browser (MetaMask Mobile, Coinbase Wallet app). Connection happens via deep links and WalletConnect v2. If you haven't tested your dApp inside MetaMask Mobile's in-app browser, your mobile UX is broken.
- **Infinite approvals are a security risk users don't understand** -- Defaulting to `type(uint256).max` approval is convenient but means a compromised spender contract can drain all tokens forever. Offer exact-amount approval as the default with infinite as an opt-in, or use Permit2 for single-transaction approve-and-transfer.
- **Block explorer links should open in a new tab with the correct chain** -- Hardcoding `etherscan.io` breaks on L2s. Use the chain's configured `blockExplorers` from wagmi to construct the correct URL.

## Wallet Connection Flow

### State Machine

```
  disconnected
       |
       | user clicks "Connect"
       v
  connecting  ----(user cancels)---> disconnected
       |
       | wallet responds
       v
  connected  ----(wrong chain detected)---> wrong-network
       |                                         |
       | correct chain                           | user switches chain
       v                                         v
  ready (can transact)  <------------------------+
```

### RainbowKit Setup

RainbowKit provides a production-ready wallet connection modal with built-in support for 30+ wallets, chain switching, ENS resolution, and responsive design.

```bash
npm install @rainbow-me/rainbowkit wagmi viem @tanstack/react-query
```

```tsx
// config.ts
import { getDefaultConfig } from "@rainbow-me/rainbowkit";
import { mainnet, arbitrum, base, optimism, polygon } from "wagmi/chains";

export const config = getDefaultConfig({
  appName: "My dApp",
  projectId: process.env.NEXT_PUBLIC_WC_PROJECT_ID!,
  chains: [mainnet, arbitrum, base, optimism, polygon],
  ssr: true,
});
```

```tsx
// providers.tsx
"use client";

import { RainbowKitProvider, darkTheme } from "@rainbow-me/rainbowkit";
import { WagmiProvider } from "wagmi";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { config } from "./config";
import { useState, type ReactNode } from "react";
import "@rainbow-me/rainbowkit/styles.css";

export function Providers({ children }: { children: ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        <RainbowKitProvider theme={darkTheme()}>
          {children}
        </RainbowKitProvider>
      </QueryClientProvider>
    </WagmiProvider>
  );
}
```

### Custom Connect Button

RainbowKit's `ConnectButton.Custom` exposes all connection states for full control.

```tsx
import { ConnectButton } from "@rainbow-me/rainbowkit";

function WalletButton() {
  return (
    <ConnectButton.Custom>
      {({
        account,
        chain,
        openAccountModal,
        openChainModal,
        openConnectModal,
        mounted,
      }) => {
        const connected = mounted && account && chain;

        if (!mounted) {
          return <button disabled aria-hidden>Connect Wallet</button>;
        }

        if (!connected) {
          return (
            <button onClick={openConnectModal} type="button">
              Connect Wallet
            </button>
          );
        }

        if (chain.unsupported) {
          return (
            <button onClick={openChainModal} type="button">
              Wrong Network
            </button>
          );
        }

        return (
          <div style={{ display: "flex", gap: 8 }}>
            <button onClick={openChainModal} type="button">
              {chain.name}
            </button>
            <button onClick={openAccountModal} type="button">
              {account.displayName}
            </button>
          </div>
        );
      }}
    </ConnectButton.Custom>
  );
}
```

### EIP-6963 Multi-Injected Provider Detection

Modern wallets announce themselves via EIP-6963 instead of fighting over `window.ethereum`. wagmi v2 discovers these automatically when `multiInjectedProviderDiscovery` is `true` (default).

```tsx
import { useConnect } from "wagmi";

function WalletList() {
  const { connectors, connect, isPending } = useConnect();

  return (
    <ul role="list" aria-label="Available wallets">
      {connectors.map((connector) => (
        <li key={connector.uid}>
          <button
            onClick={() => connect({ connector })}
            disabled={isPending}
            aria-busy={isPending}
          >
            {connector.icon && (
              <img
                src={connector.icon}
                alt=""
                width={24}
                height={24}
              />
            )}
            {connector.name}
          </button>
        </li>
      ))}
    </ul>
  );
}
```

## Transaction Flow

### Four-State Lifecycle

Every transaction passes through four states. Each needs distinct UI.

```
  idle
    |
    | user clicks action button
    v
  awaiting-signature  ----(user rejects: 4001)---> idle (silent reset)
    |
    | wallet signs and broadcasts
    v
  pending  ----(tx dropped/timeout)---> failed
    |
    | block inclusion
    v
  confirmed  ----(receipt.status === "reverted")---> failed
```

### Complete Transaction Component

```tsx
"use client";

import {
  useWriteContract,
  useWaitForTransactionReceipt,
  useChainId,
} from "wagmi";
import { parseUnits } from "viem";
import { BaseError, UserRejectedRequestError } from "viem";

const erc20Abi = [
  {
    name: "transfer",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "to", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [{ name: "", type: "bool" }],
  },
] as const;

type TxState = "idle" | "awaiting-signature" | "pending" | "confirmed" | "failed";

function getExplorerUrl(chainId: number, hash: string): string {
  const explorers: Record<number, string> = {
    1: "https://etherscan.io",
    10: "https://optimistic.etherscan.io",
    137: "https://polygonscan.com",
    8453: "https://basescan.org",
    42161: "https://arbiscan.io",
  };
  const base = explorers[chainId] ?? "https://etherscan.io";
  return `${base}/tx/${hash}`;
}

function TransferToken({
  token,
  decimals,
  to,
  amount,
}: {
  token: `0x${string}`;
  decimals: number;
  to: `0x${string}`;
  amount: string;
}) {
  const chainId = useChainId();

  const {
    writeContract,
    data: hash,
    isPending: isSigning,
    error: writeError,
    reset,
  } = useWriteContract();

  const {
    isLoading: isConfirming,
    isSuccess,
    data: receipt,
    error: receiptError,
  } = useWaitForTransactionReceipt({ hash });

  function getTxState(): TxState {
    if (isSigning) return "awaiting-signature";
    if (isConfirming) return "pending";
    if (isSuccess && receipt?.status === "success") return "confirmed";
    if (receipt?.status === "reverted" || writeError || receiptError) return "failed";
    return "idle";
  }

  const txState = getTxState();

  function isUserRejection(error: Error): boolean {
    if (error instanceof UserRejectedRequestError) return true;
    const msg = error.message.toLowerCase();
    return msg.includes("user rejected") || msg.includes("user denied");
  }

  function handleSubmit() {
    writeContract({
      address: token,
      abi: erc20Abi,
      functionName: "transfer",
      args: [to, parseUnits(amount, decimals)],
    });
  }

  // 4001 user rejection: silently reset, no error toast
  if (writeError && isUserRejection(writeError)) {
    reset();
    return null;
  }

  const buttonLabels: Record<TxState, string> = {
    idle: "Transfer",
    "awaiting-signature": "Confirm in wallet...",
    pending: "Waiting for confirmation...",
    confirmed: "Transfer complete",
    failed: "Transaction failed",
  };

  return (
    <div>
      <button
        onClick={handleSubmit}
        disabled={txState !== "idle" && txState !== "failed"}
        aria-busy={txState === "awaiting-signature" || txState === "pending"}
      >
        {buttonLabels[txState]}
      </button>

      {txState === "pending" && hash && (
        <p>
          Tx submitted.{" "}
          <a
            href={getExplorerUrl(chainId, hash)}
            target="_blank"
            rel="noopener noreferrer"
          >
            View on explorer
          </a>
        </p>
      )}

      {txState === "confirmed" && hash && (
        <div>
          <p>
            Confirmed in block {receipt?.blockNumber.toString()}.{" "}
            <a
              href={getExplorerUrl(chainId, hash)}
              target="_blank"
              rel="noopener noreferrer"
            >
              View on explorer
            </a>
          </p>
          <button onClick={() => reset()}>Send another</button>
        </div>
      )}

      {txState === "failed" && writeError && !isUserRejection(writeError) && (
        <div role="alert">
          <p>
            {writeError instanceof BaseError
              ? writeError.shortMessage
              : writeError.message}
          </p>
          <button onClick={() => reset()}>Try again</button>
        </div>
      )}

      {txState === "failed" && receipt?.status === "reverted" && (
        <div role="alert">
          <p>Transaction reverted on-chain.</p>
          <button onClick={() => reset()}>Try again</button>
        </div>
      )}
    </div>
  );
}
```

## Error Handling Taxonomy

Not all errors deserve the same UX treatment. Categorize by source and severity.

### Error Classification

| Code | Name | Source | UX Response |
|------|------|--------|-------------|
| 4001 | User Rejected Request | Wallet | Silent reset to idle. Do NOT show an error. |
| 4100 | Unauthorized | Wallet | Prompt reconnection. Wallet may have locked. |
| 4200 | Unsupported Method | Wallet | Fallback to alternative method or show upgrade prompt. |
| 4900 | Disconnected | Wallet | Show reconnect button. |
| 4901 | Chain Disconnected | Wallet | Prompt chain switch. |
| -32700 | Parse Error | RPC | Internal error. Log to monitoring, show generic message. |
| -32600 | Invalid Request | RPC | Internal error. Log to monitoring, show generic message. |
| -32601 | Method Not Found | RPC | RPC does not support this call. Try alternative RPC. |
| -32602 | Invalid Params | RPC | Bug in your code. Fix the parameters. |
| -32603 | Internal Error | RPC | Often means insufficient funds. Parse inner message. |

### Error Parsing Utility

```typescript
import {
  BaseError,
  ContractFunctionRevertedError,
  UserRejectedRequestError,
  InsufficientFundsError,
} from "viem";

function parseTransactionError(error: Error): {
  message: string;
  shouldToast: boolean;
} {
  if (error instanceof UserRejectedRequestError) {
    return { message: "Transaction cancelled", shouldToast: false };
  }

  if (error instanceof BaseError) {
    if (error.walk((e) => e instanceof InsufficientFundsError)) {
      return { message: "Insufficient funds for gas + value", shouldToast: true };
    }

    const revert = error.walk(
      (e) => e instanceof ContractFunctionRevertedError
    );
    if (revert instanceof ContractFunctionRevertedError) {
      const reason = revert.data?.errorName ?? revert.reason ?? "Unknown revert";
      return { message: `Contract error: ${reason}`, shouldToast: true };
    }

    return { message: error.shortMessage, shouldToast: true };
  }

  return { message: error.message, shouldToast: true };
}
```

See `resources/error-codes.md` for the complete error code table with detection patterns.

### Toast vs Inline Error Display

| Error Type | Display Method | Reason |
|------------|---------------|--------|
| User rejection | None (silent reset) | User chose to cancel |
| Insufficient funds | Inline, near balance display | User needs to see their balance |
| Contract revert | Inline, near action button | Contextual to the failed action |
| Network error | Toast | Global issue, not action-specific |
| RPC rate limit | Toast with retry | Transient, affects all operations |

## Gas Estimation UI

Users should see transaction cost in their local currency, not in gwei.

### Fetching Gas Estimate with USD Conversion

```tsx
import { useEstimateGas, useGasPrice } from "wagmi";
import { formatEther, formatGwei, parseEther } from "viem";

// ETH price from any oracle or API (Chainlink, CoinGecko, etc.)
function useEthPrice(): number | undefined {
  // In production, fetch from a price API or read Chainlink on-chain
  // This is a placeholder -- replace with your price source
  return 2500;
}

function GasEstimate({
  to,
  value,
}: {
  to: `0x${string}`;
  value: bigint;
}) {
  const { data: gasLimit } = useEstimateGas({ to, value });
  const { data: gasPrice } = useGasPrice();
  const ethPrice = useEthPrice();

  if (!gasLimit || !gasPrice || !ethPrice) {
    return <span>Estimating fee...</span>;
  }

  // 10% safety margin on gas limit
  const safeGasLimit = gasLimit + gasLimit / 10n;
  const gasCostWei = safeGasLimit * gasPrice;
  const gasCostEth = Number(formatEther(gasCostWei));
  const gasCostUsd = gasCostEth * ethPrice;

  return (
    <div>
      <p>Network fee: ~${gasCostUsd.toFixed(2)}</p>
      <details>
        <summary>Details</summary>
        <dl>
          <dt>Gas limit</dt>
          <dd>{safeGasLimit.toString()}</dd>
          <dt>Gas price</dt>
          <dd>{formatGwei(gasPrice)} gwei</dd>
          <dt>Cost in ETH</dt>
          <dd>{gasCostEth.toFixed(6)} ETH</dd>
        </dl>
      </details>
    </div>
  );
}
```

### EIP-1559 Fee Tiers

Use `useFeeHistory` to compute slow/normal/fast gas tiers:

```typescript
import { useFeeHistory } from "wagmi";

function useFeeTiers() {
  const { data } = useFeeHistory({
    blockCount: 5,
    rewardPercentiles: [10, 50, 90],
  });

  if (!data?.reward || !data.baseFeePerGas) return undefined;

  const latestBaseFee = data.baseFeePerGas[data.baseFeePerGas.length - 1];
  if (!latestBaseFee) return undefined;

  // Average priority fees at each percentile across recent blocks
  const avgAt = (idx: number) =>
    data.reward!.reduce((sum, r) => sum + (r[idx] ?? 0n), 0n) /
    BigInt(data.reward!.length);

  return [
    { label: "Slow", maxFeePerGas: latestBaseFee + avgAt(0) },
    { label: "Normal", maxFeePerGas: latestBaseFee * 2n + avgAt(1) },
    { label: "Fast", maxFeePerGas: latestBaseFee * 3n + avgAt(2) },
  ];
}
```

## Network Switching

### Auto-Prompt Chain Switch

When a user connects on the wrong chain, prompt them immediately instead of letting them discover the error on their first transaction.

```tsx
import { useAccount, useChainId, useSwitchChain } from "wagmi";
import type { ReactNode } from "react";

function RequireChain({
  chainId: requiredChainId,
  chainName,
  children,
}: {
  chainId: number;
  chainName: string;
  children: ReactNode;
}) {
  const { isConnected } = useAccount();
  const currentChainId = useChainId();
  const { switchChain, isPending, error } = useSwitchChain();

  if (!isConnected) return <>{children}</>;

  if (currentChainId !== requiredChainId) {
    return (
      <div role="alert">
        <p>This dApp requires {chainName}.</p>
        <button
          onClick={() => switchChain({ chainId: requiredChainId })}
          disabled={isPending}
          aria-busy={isPending}
        >
          {isPending ? "Switching..." : `Switch to ${chainName}`}
        </button>
        {error && <p>Failed to switch: {error.message}</p>}
      </div>
    );
  }

  return <>{children}</>;
}
```

### Adding Unknown Networks

When `switchChain` fails because the wallet doesn't know the chain, wagmi automatically calls `wallet_addEthereumChain` with the chain parameters from your config. The chain definition in wagmi already includes `rpcUrls`, `blockExplorers`, and `nativeCurrency` -- no extra configuration needed.

```typescript
import { defineChain } from "viem";

// Custom chain definition with all required wallet_addEthereumChain fields
const myChain = defineChain({
  id: 999999,
  name: "My Network",
  nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 },
  rpcUrls: {
    default: { http: ["https://rpc.mynetwork.com"] },
  },
  blockExplorers: {
    default: { name: "MyExplorer", url: "https://explorer.mynetwork.com" },
  },
});
```

## Approval Patterns

### Approval Strategy Comparison

| Strategy | Approval Txs | Risk | UX |
|----------|:---:|------|-----|
| Infinite approval (`type(uint256).max`) | 1 (once ever) | High: compromised spender drains all | Best: no future approvals needed |
| Exact amount | 1 per interaction | Low: only approved amount at risk | Worst: approval tx before every interaction |
| Permit2 (Uniswap) | 1 (once per token to Permit2) | Medium: time-limited permits | Good: off-chain signature per interaction |

### Approval Flow Pattern

The approval flow checks current allowance, then approves if needed:

```typescript
import { useReadContract, useWriteContract, useAccount } from "wagmi";

const MAX_UINT256 = 2n ** 256n - 1n;

function useApprovalState(
  token: `0x${string}`,
  spender: `0x${string}`,
  requiredAmount: bigint
) {
  const { address } = useAccount();

  const { data: allowance, refetch } = useReadContract({
    address: token,
    abi: erc20Abi,
    functionName: "allowance",
    args: address ? [address, spender] : undefined,
    query: { enabled: !!address },
  });

  const needsApproval = allowance !== undefined && allowance < requiredAmount;

  return { needsApproval, allowance, refetch };
}
```

Default to exact-amount approval (safer). Offer infinite approval (`MAX_UINT256`) as an opt-in with a warning about the risk. See `examples/approval-flow/README.md` for a complete component with Permit2 integration.

### Permit2 Flow

Permit2 (Uniswap's universal approval contract) replaces per-spender approvals with a single on-chain approval to the Permit2 contract (`0x000000000022D473030F116dDEE9F6B43aC78BA3`, same on all EVM chains -- last verified February 2026), then off-chain EIP-712 signatures for each subsequent interaction. The flow is:

1. One-time: approve token to Permit2 contract (`token.approve(PERMIT2, maxUint256)`)
2. Per interaction: sign an EIP-712 `PermitTransferFrom` message with `useSignTypedData`
3. Protocol calls `permit2.permitTransferFrom()` with the signature

See `examples/approval-flow/README.md` for a complete Permit2 implementation.

### Approval Revocation

Revoke by calling `approve(spender, 0n)`. Always provide a revocation UI so users can remove approvals they no longer need. See `examples/approval-flow/README.md` for the full component.

## Mobile Wallet Support

### WalletConnect v2

WalletConnect v2 is the standard for connecting mobile wallets. It uses a relay server and requires a project ID from cloud.walletconnect.com.

```typescript
import { walletConnect } from "wagmi/connectors";

walletConnect({
  projectId: process.env.NEXT_PUBLIC_WC_PROJECT_ID!,
  showQrModal: true,
  metadata: {
    name: "My dApp",
    description: "Decentralized application",
    url: "https://mydapp.com",
    icons: ["https://mydapp.com/icon.png"],
  },
})
```

### Mobile Detection

Check `navigator.userAgent` for mobile wallet in-app browsers (`metamask`, `coinbase`, `trust`, `rainbow`). In-app browsers already have a provider injected and don't need WalletConnect. Regular mobile browsers require WalletConnect QR or deep links. Always guard with `typeof window === "undefined"` for SSR safety.

### Responsive Design Rules

- Touch targets: minimum 44x44px (WCAG 2.5.5)
- Font size: minimum 16px on mobile (prevents iOS zoom on input focus)
- Buttons: full-width on mobile (`width: 100%`)
- Transaction states: must be readable on 320px viewport width
- `aria-busy` on buttons during `awaiting-signature` and `pending` states

## Production QA Checklist

Run through every item before shipping. A missed state means a broken user experience.

### Wallet Connection States

- [ ] Disconnected state shows connect button
- [ ] Connecting state shows spinner or "Connecting..."
- [ ] Connected state shows address (truncated) and chain name
- [ ] Wrong network state shows switch prompt with correct chain name
- [ ] Auto-reconnect works on page reload without flash of disconnected state
- [ ] Disconnect fully clears state (no stale address displayed)

### Transaction States

- [ ] Idle state shows action button enabled
- [ ] Awaiting-signature state disables button, shows "Confirm in wallet..."
- [ ] Pending state shows "Waiting for confirmation..." with explorer link
- [ ] Confirmed state shows success with explorer link and option to send another
- [ ] Failed state shows error message with retry button
- [ ] User rejection (4001) silently resets to idle, no error toast
- [ ] On-chain revert shows distinct message from pre-flight failure

### Error Handling

- [ ] Insufficient funds shows balance and required amount
- [ ] Contract revert shows decoded error name when ABI is available
- [ ] Network errors show retry option
- [ ] RPC timeouts show fallback RPC or retry
- [ ] All error messages are human-readable, not raw hex/stack traces

### Token Display

- [ ] Token amounts use correct decimals (6 for USDC, 18 for ETH)
- [ ] Large numbers formatted with commas or abbreviations (1.5M, not 1500000)
- [ ] USD equivalents shown where possible
- [ ] Never use JavaScript `number` for token amounts -- always `bigint`

### Mobile

- [ ] Tested in MetaMask Mobile in-app browser
- [ ] Tested in Coinbase Wallet in-app browser
- [ ] WalletConnect QR code scans correctly
- [ ] Touch targets at least 44x44px
- [ ] No horizontal scroll on small screens
- [ ] Transaction states readable on 320px width

### Accessibility

- [ ] All interactive elements keyboard-navigable
- [ ] Transaction state changes announced to screen readers (aria-live or role="alert")
- [ ] Color is not the only indicator of state (use icons or text alongside)
- [ ] Modal focus trapped and restored on close
- [ ] Sufficient color contrast (4.5:1 for text, 3:1 for large text)

## Deployment Notes

- **Environment variables**: All `NEXT_PUBLIC_` variables are exposed to the browser bundle. Never put private RPC keys with billing in `NEXT_PUBLIC_` variables -- use a proxy or rate-limited public endpoint.
- **IPFS hosting**: Deploy to IPFS via Fleek or Pinata for censorship-resistant hosting. Limitations: no SSR, no API routes, no dynamic routing.
- **ENS website**: Point an ENS name's `contenthash` to your IPFS deployment. Users access via `yourname.eth.limo`.

## References

- RainbowKit docs: https://rainbowkit.com
- wagmi v2 docs: https://wagmi.sh
- viem docs: https://viem.sh
- WalletConnect v2: https://docs.walletconnect.com/2.0
- EIP-1193 (Provider API): https://eips.ethereum.org/EIPS/eip-1193
- EIP-6963 (Multi-Injected Provider): https://eips.ethereum.org/EIPS/eip-6963
- EIP-2612 (Permit): https://eips.ethereum.org/EIPS/eip-2612
- Permit2 (Uniswap): https://docs.uniswap.org/contracts/permit2/overview
- WCAG 2.1 Touch Target Size: https://www.w3.org/WAI/WCAG21/Understanding/target-size.html
- Fleek (IPFS hosting): https://fleek.co
