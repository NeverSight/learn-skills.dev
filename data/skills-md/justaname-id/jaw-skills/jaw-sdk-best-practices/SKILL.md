---
name: jaw-sdk-best-practices
description: Best practices and usage guide for the JAW SDK (@jaw.id/core, @jaw.id/wagmi, @jaw.id/ui). Use this skill when writing code that uses jaw-sdk or @jaw.id packages, integrating JAW smart accounts into an application, configuring JAW SDK features (passkeys, permissions, gas sponsoring, ENS), building with JAW wagmi hooks, implementing headless/server-side smart account operations, debugging JAW SDK issues, or when asked about JAW SDK patterns, APIs, or best practices.
---

# JAW SDK Best Practices

Guide for building applications with the JAW SDK passkey-authenticated smart accounts on EVM chains with programmable permissions.

## When to use

Reference these guidelines when:

- Installing or setting up `@jaw.id/wagmi`, `@jaw.id/core`, or `@jaw.id/ui`
- Configuring the JAW connector or provider (API key, modes, paymasters, ENS)
- Connecting/disconnecting wallets with passkey authentication
- Sending transactions (single or batched) through JAW smart accounts
- Signing messages or typed data (EIP-191, EIP-712, ERC-7871)
- Granting, querying, or revoking permissions (ERC-7715)
- Implementing subscription payments or recurring charges
- Setting up gas sponsoring with paymasters (ERC-7677)
- Issuing ENS subnames to users during onboarding
- Implementing Sign-In With Ethereum (SIWE)
- Building headless integrations, server-side operations, or AI agent wallets
- Using the Account class directly (no UI)
- Building stablecoin payment flows (USDC gas, batch payouts)
- Choosing between CrossPlatform and AppSpecific authentication modes
- Implementing a custom UI handler for app-specific mode
- Reviewing or debugging code that uses JAW SDK

## Key facts

- **Packages:** `@jaw.id/wagmi` (React), `@jaw.id/core` (vanilla JS / server), `@jaw.id/ui` (app-specific mode UI)
- **API Key:** Required. Get one at [https://dashboard.jaw.id](https://dashboard.jaw.id)
- **EIP-1193 compatible:** Drop-in replacement for MetaMask or any wallet
- **Smart accounts:** ERC-4337 with passkey signers, gasless tx, batch ops, permissions
- **EntryPoint:** v0.8 only (for paymasters)

## Rule index

### 1. Setup & Configuration

- <rules/installation.md> - Package installation, peer dependencies, choosing wagmi vs core
- <rules/configuration.md> - All config options: apiKey, appName, ens, mode, paymasters, preference
- <rules/auth-modes.md> - CrossPlatform vs AppSpecific modes and when to use each

### 2. Wagmi Integration (React)

- <rules/wagmi-setup.md> - Wagmi connector setup, providers, using standard wagmi hooks with JAW
- <rules/connect-disconnect.md> - useConnect, useDisconnect, connection with capabilities

### 3. Core Operations

- <rules/transactions.md> - Sending transactions, batch calls, gas estimation, checking status
- <rules/signing.md> - Personal sign, typed data, unified wallet_sign, cross-chain signing

### 4. Permissions & Payments

- <rules/permissions.md> - Granting, querying, revoking permissions (ERC-7715)
- <rules/subscription-payments.md> - Recurring subscription payments using permissions
- <rules/stablecoin-payments.md> - Headless USDC payments, batch payouts, ERC-20 gas

### 5. Identity & Auth

- <rules/ens-identity.md> - ENS subname issuance, profile resolution, text records
- <rules/siwe.md> - Sign-In With Ethereum (SIWE) implementation
- <rules/gas-sponsoring.md> - Paymaster setup, sponsorship policies, multi-chain config

### 6. Advanced

- <rules/account-api.md> - Headless Account class for AI agents, server-side, embedded wallets
- <rules/custom-ui-handler.md> - Building a custom UIHandler for app-specific mode
- <rules/provider-api.md> - Direct provider RPC methods reference and patterns

### 7. Reference

- <rules/error-handling.md> - EIP-1193 error codes, common errors, debugging
- <rules/typescript-types.md> - Key TypeScript interfaces and type patterns

## How to use

Read individual rule files for detailed guidance. Each contains:
correct usage examples, common mistakes to avoid, and critical requirements.