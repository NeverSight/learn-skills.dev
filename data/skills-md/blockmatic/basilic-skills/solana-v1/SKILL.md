---
name: solana-v1
description: Solana dApp UI with kit and web3.js. Use when wallet connect, transactions, or Solana address validation in React/Next.js.
---

# Skill: solana

## Scope

- Solana dApp UI development (React/Next.js) with framework-kit
- Wallet connection and signing flows
- Transaction building, sending, and confirmation UX
- Address validation and transaction patterns

Does NOT cover:
- EVM frontend development (see [wagmi-v3](../wagmi-v3/SKILL.md))
- Address-only backend validation without dApp UI (may use `@solana/web3.js` `PublicKey` only)
- General blockchain concepts

## Assumptions

- `@solana/client` and `@solana/react-hooks` for UI development
- `@solana/kit` for client/RPC/transaction code
- `@solana/web3.js` v1.x for address validation
- React 18+ or Next.js 14+ for UI
- TypeScript v5+ with strict mode
- Node.js 18+

## Principles

- Use Solana Foundation framework-kit (`@solana/client` + `@solana/react-hooks`) for React/Next.js UI
- Use `@solana/kit` for client/RPC/transaction code
- Validate addresses with `PublicKey` from `@solana/web3.js` (including backend-only routes that do not ship wallet UI)
- Use Wallet Standard for wallet discovery and connection
- Isolate `@solana/web3.js` to adapter boundaries when legacy dependencies require it

## Constraints

### MUST

- Validate addresses with `PublicKey.isOnCurve()` before use
- Use `@solana/web3-compat` for legacy adapter boundaries

### SHOULD

- Use `@solana/kit` types (`Address`, `Signer`) over web3.js types
- Prefer `@solana-program/*` instruction builders over hand-rolled instruction data
- Use Wallet Standard for wallet discovery/connect
- Contain `@solana/web3.js` types to adapter modules (don't leak across app)

### AVOID

- Letting `@solana/web3.js` types leak across entire app
- Skipping address validation before use

## Patterns

### Address Validation Pattern

Always validate Solana addresses before use:

```tsx
import { PublicKey } from '@solana/web3.js'

function validateSolanaAddress(address: string): boolean {
  try {
    const publicKey = new PublicKey(address)
    return PublicKey.isOnCurve(publicKey)
  } catch {
    return false
  }
}
```

## Interactions

- Complements wagmi skill for EVM frontend work
- Focuses on Solana-specific dApp development patterns
