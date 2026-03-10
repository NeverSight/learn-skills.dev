---
name: orderly-one-dex
description: Create and manage a custom DEX using Orderly One API - deployment, custom domains, graduation, and theming
---

# Orderly Network: Orderly One DEX

**Orderly One** is a white-label DEX platform. Users configure a DEX (name, branding, chains), the API forks a GitHub template repo, and GitHub Actions deploys to GitHub Pages. Graduated DEXs earn fee splits.

## When to Use

- Creating a custom perpetuals DEX
- Managing DEX deployment, domains, or themes
- Handling graduation for fee sharing

## API Base URLs

| Environment | Base URL                                  |
| ----------- | ----------------------------------------- |
| Mainnet     | `https://dex-api.orderly.network`         |
| Testnet     | `https://testnet-dex-api.orderly.network` |

## API Categories

Use `get_orderly_one_api_info` MCP tool for full endpoint details.

| Category        | Description                      | Key Endpoints                                                                               |
| --------------- | -------------------------------- | ------------------------------------------------------------------------------------------- |
| **auth**        | Wallet signature authentication  | `/api/auth/nonce`, `/api/auth/verify`, `/api/auth/validate`                                 |
| **dex**         | DEX CRUD, domains, deployment    | `/api/dex`, `/api/dex/{id}`, `/api/dex/{id}/custom-domain`, `/api/dex/{id}/workflow-status` |
| **theme**       | AI theme generation              | `/api/theme/modify`, `/api/theme/fine-tune`                                                 |
| **graduation**  | Demo → full DEX with fee sharing | `/api/graduation/status`, `/api/graduation/fee-options`, `/api/graduation/verify-tx`        |
| **leaderboard** | Cross-DEX rankings               | `/api/leaderboard`, `/api/leaderboard/broker/{brokerId}`                                    |
| **stats**       | Platform statistics              | `/api/stats`, `/api/stats/swap-fee-config`                                                  |

---

## Create/Update DEX

Both `POST /api/dex` (create) and `PUT /api/dex/{id}` (update) use `multipart/form-data`.

### Required Fields

| Field        | Type   | Constraints                               |
| ------------ | ------ | ----------------------------------------- |
| `brokerName` | string | 3-30 chars, alphanumeric/space/dot/hyphen |

### Optional Fields

**Chains:**
| Field | Type | Notes |
| -------------- | ---------------- | ------------------------ |
| `chainIds` | number[] (JSON) | e.g. `[42161, 10, 8453]` |
| `defaultChain` | number | Default chain ID |

**Branding (files):**
| Field | Type | Max Size |
| --------------- | ---- | -------- |
| `primaryLogo` | File | 250KB |
| `secondaryLogo` | File | 100KB |
| `favicon` | File | 50KB |
| `pnlPoster0..N` | File | 250KB ea |

**Theming:**
| Field | Type | Notes |
| --------------- | ------ | -------------------------------- |
| `themeCSS` | string | CSS variables to override [default theme](https://raw.githubusercontent.com/OrderlyNetworkDexCreator/dex-creator-template/refs/heads/main/app/styles/theme.css) |
| `tradingViewColorConfig` | string | JSON for chart colors |

**Social:**
| Field | Type | Notes |
| -------------- | ------ | ------------------ |
| `telegramLink` | string | URL |
| `discordLink` | string | URL |
| `xLink` | string | URL |

**Auth/Wallet:**
| Field | Type | Notes |
| ------------------------ | -------- | -------------------------- |
| `walletConnectProjectId` | string | WalletConnect project ID |
| `privyAppId` | string | Privy app ID |
| `privyTermsOfUse` | string | URL to terms |
| `privyLoginMethods` | string | Comma-separated |
| `enableAbstractWallet` | boolean | Enable Abstract wallet |
| `disableEvmWallets` | boolean | Disable EVM wallets |
| `disableSolanaWallets` | boolean | Disable Solana wallets |

**Network:**
| Field | Type | Notes |
| ------------------ | ------- | -------------------- |
| `disableMainnet` | boolean | Disable mainnet |
| `disableTestnet` | boolean | Disable testnet |

**Trading:**
| Field | Type | Notes |
| ------------ | -------------- | ------------------------------- |
| `swapFeeBps` | number (0-100) | Swap fee in basis points (requires "Swap" in enabledMenus) |
| `symbolList` | string | Comma-separated (PERP_ETH_USDC) |

**Menus:**
| Field | Type | Notes |
| -------------- | ------ | ----------------------------- |
| `enabledMenus` | string | Comma-separated. Options: Trading, Portfolio, Markets, Leaderboard (defaults), Swap, Rewards, Vaults, Points |
| `customMenus` | string | Format: "Name,URL;Name2,URL2" |

**SEO:**
| Field | Type | Constraints |
| ------------------- | ------ | --------------------- |
| `seoSiteName` | string | max 100 chars |
| `seoSiteDescription`| string | max 300 chars |
| `seoSiteLanguage` | string | "en" or "en-US" |
| `seoSiteLocale` | string | "en_US" |
| `seoTwitterHandle` | string | "@handle" |
| `seoThemeColor` | string | "#1a1b23" |
| `seoKeywords` | string | max 500 chars |

**Other:**
| Field | Type | Notes |
| -------------------------- | ------- | ------------------------ |
| `availableLanguages` | string | JSON array. Options: en, zh, tc, ja, es, ko, vi, de, fr, ru, id, tr, it, pt, uk, pl, nl |
| `analyticsScript` | string | Base64 encoded |
| `enableServiceDisclaimerDialog` | boolean | Show disclaimer |
| `enableCampaigns` | boolean | Enable ORDER token campaigns and Points menu |
| `restrictedRegions` | string | Comma-separated country names (e.g., "United States,China") |
| `whitelistedIps` | string | IP whitelist |

### Response

**Create (201):** `{ id, brokerId, brokerName, repoUrl, userId, createdAt }`

**Update (200):** Full DEX object with all fields

---

## Key Workflows

### Authentication

1. `POST /api/auth/nonce` with `{ address }` → get message to sign
2. Sign: `"Sign this message to authenticate with Orderly One: {nonce}"`
3. `POST /api/auth/verify` with `{ address, signature }` → get JWT
4. Use `Authorization: Bearer {token}` for all requests

### Create DEX Flow

1. Build `multipart/form-data` with fields above
2. `POST /api/dex` → returns `{ id, brokerId, repoUrl }`
3. Poll `GET /api/dex/{id}/workflow-status` until `conclusion: "success"`

### Graduation (Fee Sharing)

1. `GET /api/graduation/fee-options` → USDC/ORDER amounts + `receiverAddress`
2. Transfer tokens on **Ethereum, Arbitrum, or Base** to `receiverAddress`
3. `POST /api/graduation/verify-tx` with `{ txHash, chain, chainId, chainType: "EVM", brokerId, makerFee, takerFee, rwaMakerFee, rwaTakerFee, paymentType }` → creates broker ID

**After broker ID created, finalize admin wallet:**

**EVM Wallet:** 4. Register with Orderly Network API:

- `GET https://api.orderly.org/v1/registration_nonce`
- Sign EIP-712 typed data: `{ brokerId, chainId, timestamp, registrationNonce }`
- `POST https://api.orderly.org/v1/register_account` with `{ message, signature, userAddress, chainType: "EVM" }`

5. `POST /api/graduation/finalize-admin-wallet` (empty body)

**Solana Wallet:** 4. Register with Orderly Network API:

- `GET https://api.orderly.org/v1/registration_nonce`
- Sign message with Solana wallet: `{ brokerId, chainId: 900900900, timestamp, registrationNonce }`
- `POST https://api.orderly.org/v1/register_account` with `{ message, signature, userAddress, chainType: "SOL" }`

5. `POST /api/graduation/finalize-admin-wallet` (empty body)

**EVM Multisig/Gnosis Safe:** 4. In Safe Wallet → Transaction Builder → create batch:

- **To:** Orderly Vault contract (chain-specific)
- **Method:** `delegateSigner`
- **Data:** `[keccak256(brokerId), userAddress]`

5. Execute on Safe with required signer approvals
6. `POST /api/graduation/finalize-admin-wallet` with `{ multisigAddress, multisigChainId }`

---

## Orderly MCP

This skill references the Orderly MCP server. If not installed, see **orderly-onboarding** skill for setup.

**Tool:** `get_orderly_one_api_info`

- `{ endpoint: "/api/dex" }` - Specific endpoint details
- `{ category: "graduation" }` - All endpoints in a category
- `{}` - Full API overview

---

## Common Issues

| Issue                   | Solution                                                     |
| ----------------------- | ------------------------------------------------------------ |
| DEX stuck deploying     | Check `/api/dex/{id}/workflow-runs/{runId}` for job failures |
| Domain not working      | CNAME to `{org}.github.io`, wait for DNS propagation         |
| Graduation verify fails | Confirm tx to `receiverAddress`, wait for confirmations      |
| Logo upload fails       | Check file size limits (250KB primary, 100KB secondary)      |
| Invalid CSS             | Validate `themeCSS` syntax before submitting                 |

---

## Related Skills

- **orderly-onboarding** - Account setup
- **orderly-trading-orders** - Trading functionality
