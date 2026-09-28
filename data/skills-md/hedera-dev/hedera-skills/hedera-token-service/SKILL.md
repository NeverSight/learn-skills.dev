---
name: hedera-token-service
description: "How to create, manage, and transfer tokens on Hedera using the Hiero JavaScript SDK (@hiero-ledger/sdk). Use this skill whenever the user wants to work with fungible tokens, NFTs, token creation, minting, burning, transfers, token association, custom fees (fixed, fractional, royalty), airdrops, KYC/freeze/wipe/pause operations, or any HTS (Hedera Token Service) operation in JavaScript or TypeScript. Also trigger when users mention @hashgraph/sdk token operations, ERC-20/ERC-721 equivalents on Hedera, or tokenization on the Hedera network."
---

# Hedera Token Service (HTS) — JavaScript SDK

HTS is Hedera's native token engine. It lets you create and manage fungible tokens and NFTs without writing smart contracts. Tokens created through HTS are first-class network entities with built-in compliance controls (KYC, freeze, wipe, pause) and custom fee schedules.

## Setup

All imports come from `@hiero-ledger/sdk`. Two setup patterns exist:

### Client + setOperator (direct)
```js
import { Client, AccountId, PrivateKey } from "@hiero-ledger/sdk";

const client = Client.forName(process.env.HEDERA_NETWORK)
    .setOperator(
        AccountId.fromString(process.env.OPERATOR_ID),
        PrivateKey.fromStringECDSA(process.env.OPERATOR_KEY),
    );
```

### Wallet + LocalProvider (signer-based)
```js
import { Wallet, LocalProvider } from "@hiero-ledger/sdk";

const provider = new LocalProvider();
const wallet = new Wallet(process.env.OPERATOR_ID, process.env.OPERATOR_KEY, provider);
```

With the signer pattern, use `freezeWithSigner(wallet)`, `signWithSigner(wallet)`, `executeWithSigner(wallet)`, and `getReceiptWithSigner(wallet)` instead of `freezeWith(client)` / `execute(client)`.

## Transaction Lifecycle

Every transaction follows this flow: **configure -> freeze -> sign -> execute -> receipt**.

```js
const tx = await new SomeTransaction()
    .setSomeField(value)
    .freezeWith(client);   // locks the transaction body

await tx.sign(privateKey); // add signatures (call multiple times for multi-sig)

const response = await tx.execute(client);
const receipt = await response.getReceipt(client);
```

When only the operator key is needed, you can skip explicit freeze/sign — `execute(client)` handles it:

```js
const response = await new SomeTransaction()
    .setSomeField(value)
    .execute(client);
const receipt = await response.getReceipt(client);
```

## Creating Tokens

### Fungible Token

```js
import {
    TokenCreateTransaction, TokenType, TokenSupplyType,
    PrivateKey, Hbar,
} from "@hiero-ledger/sdk";

const supplyKey = PrivateKey.generateECDSA();

const { tokenId } = await (
    await new TokenCreateTransaction()
        .setTokenName("My Token")
        .setTokenSymbol("MTK")
        .setDecimals(2)
        .setInitialSupply(10000)
        .setTreasuryAccountId(operatorId)
        .setAdminKey(operatorKey)
        .setSupplyKey(supplyKey)
        .execute(client)
).getReceipt(client);
```

### NFT (Non-Fungible Token)

NFTs require `TokenType.NonFungibleUnique`. They have **no decimals** and **no initial supply** — you mint individual serials after creation.

```js
const { tokenId: nftId } = await (
    await new TokenCreateTransaction()
        .setTokenName("My NFT Collection")
        .setTokenSymbol("MNFT")
        .setTokenType(TokenType.NonFungibleUnique)
        .setSupplyType(TokenSupplyType.Finite)
        .setMaxSupply(1000)
        .setTreasuryAccountId(treasuryId)
        .setAdminKey(adminKey)
        .setSupplyKey(supplyKey)
        .execute(client)
).getReceipt(client);
```

## Minting

```js
import { TokenMintTransaction } from "@hiero-ledger/sdk";

// Fungible — specify amount
await new TokenMintTransaction()
    .setTokenId(tokenId)
    .setAmount(500)
    .execute(client);

// NFT — specify metadata per serial
const { serials } = await (
    await new TokenMintTransaction()
        .setTokenId(nftId)
        .addMetadata(Buffer.from("ipfs://QmFirst..."))
        .addMetadata(Buffer.from("ipfs://QmSecond..."))
        .execute(client)
).getReceipt(client);
// serials = [Long(1), Long(2)]
```

## Token Association

Hedera accounts must **associate** with a token before they can receive it (unless the account has automatic token associations enabled via `setMaxAutomaticTokenAssociations`).

```js
import { TokenAssociateTransaction } from "@hiero-ledger/sdk";

await (
    await (
        await new TokenAssociateTransaction()
            .setAccountId(recipientId)
            .setTokenIds([tokenId])
            .freezeWith(client)
    ).sign(recipientKey)      // account owner must sign
).execute(client);
```

Alternatively, set `setMaxAutomaticTokenAssociations(-1)` on account creation to allow unlimited auto-association.

## Transfers

Use `TransferTransaction` for both fungible tokens and NFTs. Amounts are **signed**: negative debits, positive credits. They must net to zero per token.

```js
import { TransferTransaction } from "@hiero-ledger/sdk";

// Fungible transfer
await new TransferTransaction()
    .addTokenTransfer(tokenId, senderId, -100)
    .addTokenTransfer(tokenId, receiverId, 100)
    .execute(client);

// NFT transfer (tokenId, serial, sender, receiver)
await new TransferTransaction()
    .addNftTransfer(nftId, 1, senderId, receiverId)
    .execute(client);

// Mix Hbar + token transfers in one transaction
await new TransferTransaction()
    .addHbarTransfer(senderId, new Hbar(-5))
    .addHbarTransfer(receiverId, new Hbar(5))
    .addTokenTransfer(tokenId, senderId, -50)
    .addTokenTransfer(tokenId, receiverId, 50)
    .execute(client);
```

## Key Roles

Each key is optional. If omitted at creation, that capability is permanently disabled.

| Key | Purpose |
|-----|---------|
| `adminKey` | Update/delete the token; rotate other keys |
| `supplyKey` | Mint and burn |
| `freezeKey` | Freeze/unfreeze accounts from transferring this token |
| `kycKey` | Grant/revoke KYC status on accounts |
| `wipeKey` | Wipe token balance from an account |
| `pauseKey` | Pause/unpause all token operations globally |
| `feeScheduleKey` | Update the custom fee schedule |
| `metadataKey` | Update token or NFT metadata |

## Compliance Operations

```js
// Grant KYC (required when token has kycKey)
await new TokenGrantKycTransaction()
    .setTokenId(tokenId).setAccountId(accountId).execute(client);

// Freeze an account
await new TokenFreezeTransaction()
    .setTokenId(tokenId).setAccountId(accountId).execute(client);

// Unfreeze
await new TokenUnfreezeTransaction()
    .setTokenId(tokenId).setAccountId(accountId).execute(client);

// Wipe tokens from an account
await new TokenWipeTransaction()
    .setTokenId(tokenId).setAccountId(accountId).setAmount(10).execute(client);

// Pause all transfers
await new TokenPauseTransaction().setTokenId(tokenId).execute(client);

// Unpause
await new TokenUnpauseTransaction().setTokenId(tokenId).execute(client);
```

## Burning & Deleting

```js
import { TokenBurnTransaction, TokenDeleteTransaction } from "@hiero-ledger/sdk";

// Burn fungible
await new TokenBurnTransaction()
    .setTokenId(tokenId).setAmount(100).execute(client);

// Burn NFT serials
await new TokenBurnTransaction()
    .setTokenId(nftId).setSerials([1, 2]).execute(client);

// Delete entire token (requires adminKey)
await new TokenDeleteTransaction()
    .setTokenId(tokenId).execute(client);
```

## Querying Token Info

```js
import { TokenInfoQuery, TokenNftInfoQuery, NftId } from "@hiero-ledger/sdk";

const info = await new TokenInfoQuery().setTokenId(tokenId).execute(client);
console.log(info.name, info.symbol, info.totalSupply.toString());

const nftInfo = await new TokenNftInfoQuery()
    .setNftId(new NftId(nftId, 1))
    .execute(client);
console.log(nftInfo.accountId.toString()); // current owner
```

## Airdrops

Airdrops distribute tokens to multiple recipients. If a recipient can't auto-associate, the airdrop becomes **pending** and must be claimed.

```js
import {
    TokenAirdropTransaction, TokenClaimAirdropTransaction,
    TokenCancelAirdropTransaction, TokenRejectTransaction, NftId,
} from "@hiero-ledger/sdk";

// Send airdrop
const record = await (
    await (
        await new TokenAirdropTransaction()
            .addTokenTransfer(tokenId, treasuryId, -300)
            .addTokenTransfer(tokenId, recipient1, 100)
            .addTokenTransfer(tokenId, recipient2, 100)
            .addTokenTransfer(tokenId, recipient3, 100)
            .addNftTransfer(nftId, 1, treasuryId, recipient1)
            .freezeWith(client)
            .sign(treasuryKey)
    ).execute(client)
).getRecord(client);

// Check pending airdrops
const { newPendingAirdrops } = record;

// Recipient claims a pending airdrop
await (
    await new TokenClaimAirdropTransaction()
        .addPendingAirdropId(newPendingAirdrops[0].airdropId)
        .freezeWith(client)
        .sign(recipientKey)
).execute(client);

// Sender cancels a pending airdrop
await new TokenCancelAirdropTransaction()
    .addPendingAirdropId(newPendingAirdrops[1].airdropId)
    .execute(client);

// Recipient rejects tokens they already received
await (
    await new TokenRejectTransaction()
        .setOwnerId(recipientId)
        .addTokenId(tokenId)           // reject fungible
        .addNftId(new NftId(nftId, 1)) // reject NFT
        .freezeWith(client)
        .sign(recipientKey)
).execute(client);
```

## Custom Fees

HTS supports three fee types. See `references/custom-fees.md` for full details.

```js
import {
    CustomFixedFee, CustomFractionalFee, CustomRoyaltyFee, Hbar,
} from "@hiero-ledger/sdk";

const fixedFee = new CustomFixedFee()
    .setFeeCollectorAccountId(collectorId)
    .setHbarAmount(new Hbar(1));

const fractionalFee = new CustomFractionalFee()
    .setFeeCollectorAccountId(collectorId)
    .setNumerator(1).setDenominator(100)  // 1%
    .setMin(1).setMax(1000);

const royaltyFee = new CustomRoyaltyFee()
    .setFeeCollectorAccountId(collectorId)
    .setNumerator(5).setDenominator(100)  // 5%
    .setFallbackFee(
        new CustomFixedFee().setHbarAmount(new Hbar(2))
    );

await new TokenCreateTransaction()
    .setCustomFees([fixedFee, fractionalFee])
    // ... other fields
    .execute(client);
```

## Common Gotchas

1. **Association before transfer**: Recipients must associate with the token or have auto-association slots. Without it, transfers fail with `TOKEN_NOT_ASSOCIATED_TO_ACCOUNT`.

2. **Signed amounts**: `addTokenTransfer` uses signed amounts. Sender gets negative, receiver gets positive. They must net to zero.

3. **NFTs have no decimals or initial supply**: Set `TokenType.NonFungibleUnique` and mint serials individually.

4. **Keys are permanent if no adminKey**: Without an admin key, you cannot update or delete the token, and cannot change any other keys.

5. **KYC gate**: If a token has a `kycKey`, accounts must receive KYC approval before they can transact with that token.

6. **Supply key for mint/burn**: You need a supply key set at creation to later mint or burn.

7. **Treasury auto-association**: The treasury account is automatically associated with the token.

8. **Freeze before multi-sig**: When multiple parties need to sign, call `freezeWith(client)` first, then chain `.sign(key)` calls.

## Reference Files

- `references/api-reference.md` — Complete list of all HTS transaction and query classes with their methods
- `references/custom-fees.md` — Detailed guide to fixed, fractional, and royalty fees
