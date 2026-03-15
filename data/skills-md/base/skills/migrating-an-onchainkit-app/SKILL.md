---
name: migrating-an-onchainkit-app
description: >
  Migrates apps from @coinbase/onchainkit to standalone wagmi/viem components.
  Handles provider replacement (OnchainKitProvider to WagmiProvider),
  wallet component replacement (Wallet/ConnectWallet to custom WalletConnect),
  and transaction component replacement. Use when the user says "migrate my
  onchainkit", "replace onchainkit provider", "migrate my wallet component",
  "replace my onchainkit wallet", "migrate my transaction component",
  "remove onchainkit dependency", or "move off onchainkit".
---

# OnchainKit Migration Skill

Migrate apps from `@coinbase/onchainkit` to standalone `wagmi`/`viem` components with zero OnchainKit dependency.

## Before Starting

Create a `mistakes.md` file in the project root:

```markdown
# Migration Mistakes & Learnings

Track errors, fixes, and lessons learned during OnchainKit migration.

## Errors

## Lessons Learned
```

Append every error, fix, and lesson to this file throughout the migration. This file improves the skill over time.

## Migration Workflow

Migrations MUST happen in this order. Do not skip steps.

### Step 1: Detection

Scan the project to understand current OnchainKit usage:

1. Search all files for `@coinbase/onchainkit` imports
2. Identify which components are used:
   - **Provider**: `OnchainKitProvider` (always present if using OnchainKit)
   - **Wallet**: `Wallet`, `ConnectWallet`, `WalletDropdown`, `WalletModal`, `Connected`
   - **Transaction**: `Transaction`, `TransactionButton`, `TransactionStatus`
   - **Other**: `Identity`, `Avatar`, `Name`, `Address`, `Swap`, `Checkout`, etc.
3. Check `package.json` for existing `wagmi`, `viem`, `@tanstack/react-query` dependencies
4. Identify the project's styling approach (Tailwind, CSS Modules, styled-components, etc.)
5. Report findings to the user before proceeding

### Step 2: Provider Migration (always first)

Read [references/provider-migration.md](references/provider-migration.md) for detailed instructions and code.

Summary:
1. Ensure `wagmi`, `viem`, and `@tanstack/react-query` are installed
2. Create `wagmi-config.ts` with chain and connector configuration
3. Replace `OnchainKitProvider` with `WagmiProvider` + `QueryClientProvider`
4. Remove `@coinbase/onchainkit/styles.css` import
5. Remove any `SafeArea` or MiniKit imports from layout files

**Validation gate**: Run `npm run build` (or the project's build command). Must pass before continuing. If it fails, fix errors and document them in `mistakes.md`.

### Step 3: Wallet Migration (after provider)

Read [references/wallet-migration.md](references/wallet-migration.md) for detailed instructions and code.

Summary:
1. Create a `WalletConnect` component using wagmi hooks (`useAccount`, `useConnect`, `useDisconnect`)
2. Component includes a modal with wallet options: Base Account, Coinbase Wallet, MetaMask
3. Shows truncated address + disconnect button when connected
4. Replace all OnchainKit wallet imports and component usage

**Validation gate**: Run `npm run build`. Must pass before continuing. Document any errors in `mistakes.md`.

### Step 4: Transaction Migration (after wallet)

Read [references/transaction-migration.md](references/transaction-migration.md) for detailed instructions and code.

Summary:
1. Check the `chainId` prop on existing `<Transaction />` components -- add any missing chains to `wagmi-config.ts`
2. Create a `TransactionForm` component using wagmi hooks (`useWriteContract`, `useWaitForTransactionReceipt`, `useSwitchChain`)
3. Component handles the full lifecycle: idle, pending wallet confirmation, confirming on-chain, success, error
4. Replace all OnchainKit transaction imports (`Transaction`, `TransactionButton`, `TransactionStatus`, `TransactionSponsor`, etc.)
5. Update the `calls` array format -- use `address`, `abi`, `functionName`, `args` with proper `as const` typing
6. Map `onStatus` callback to the new lifecycle status names (init, pending, confirmed, success, error)

**Validation gate**: Run `npm run build`. Must pass before continuing. Document any errors in `mistakes.md`.

### Step 5: Cleanup

1. Search for any remaining `@coinbase/onchainkit` imports -- there should be none
2. Optionally remove `@coinbase/onchainkit` from `package.json` dependencies
3. Run final `npm run build` to verify everything works
4. Update `mistakes.md` with final lessons learned

## Troubleshooting

### Build fails after provider migration
- **Missing dependencies**: Ensure `wagmi`, `viem`, `@tanstack/react-query` are installed
- **Type errors with wagmi config**: Check that `chains` array has at least one chain and `transports` has a matching entry
- **"use client" missing**: Both the provider and wallet components must have `"use client"` directive

### MetaMask SDK react-native warning
- The warning `Can't resolve '@react-native-async-storage/async-storage'` is harmless in web builds. It comes from MetaMask SDK and does not affect functionality.

### Wallet won't connect
- Verify the wagmi config has the correct connectors configured
- Check that `WagmiProvider` wraps the component tree before any wallet hooks are used
- Ensure `QueryClientProvider` is inside `WagmiProvider`

### Transaction receipt stuck in pending
- **Symptom**: Transaction hash appears, tx confirms on-chain, but UI stays stuck on "Transaction in progress..." forever
- **Cause**: `useWaitForTransactionReceipt` has no RPC to poll because the transaction's chain is missing from the wagmi config's `chains` + `transports`
- **Fix**: (1) Add the target chain to `wagmi-config.ts` chains array AND transports object. (2) Always pass `chainId` to `useWaitForTransactionReceipt({ hash, chainId })` so it polls the correct chain

### Transaction targets wrong chain
- The `TransactionForm` auto-switches chains, but the target chain must exist in the wagmi config's `chains` array and `transports` object
- Common: add `baseSepolia` for testnet transactions (chainId 84532)

### Next.js page export restrictions
- Next.js only allows specific named exports from page files. Exporting contract call arrays or ABI constants from a page file will cause a build error
- Fix: make them non-exported `const` declarations or move them to a separate module

### ABI type errors after transaction migration
- When defining ABIs inline, use `as const` on the array for proper type inference
- Mark individual fields like `type: 'function' as const` and `stateMutability: 'nonpayable' as const`

### Existing wagmi setup detected
- If the project already wraps with `WagmiProvider`, do NOT add another one
- Instead, just update the existing wagmi config to include the needed connectors
- OnchainKit's provider detects and defers to existing wagmi providers -- the standalone setup should too

## Important Notes

- Always use `wagmi` and `viem` directly. Never import from `@coinbase/onchainkit`.
- The `baseAccount` connector comes from `wagmi/connectors`, not from a separate package.
- `wagmi-config.ts` must include every chain the app transacts on. If the original OnchainKit `<Transaction chainId={X} />` used a specific chain, that chain must be in both `chains` and `transports`. Without it, `useWaitForTransactionReceipt` will hang forever.
- If the project uses Tailwind, use Tailwind classes for the components. If not, adapt to inline styles or the project's existing styling approach (e.g., CSS Modules).
- Do not export contract call arrays, ABI constants, or other non-page values from Next.js page files. Use non-exported constants or a separate module.
- Inspect the OnchainKit source code in `node_modules/@coinbase/onchainkit/src/` if you need to understand how a specific component works internally.
