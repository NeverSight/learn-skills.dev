---
name: tonweb
description: TonWeb JavaScript SDK for TON. Wallets, BOC, HttpProvider, NFT, Jetton, DNS.
metadata:
  author: Hairy
  version: "2026.2.25"
  source: Generated from sources/tonweb (toncenter/tonweb)
---

> Based on tonweb v0.0.66, generated 2026-02-25.

TonWeb is the JavaScript API for the TON blockchain: wallet contracts, BOC/Cell, TonCenter HttpProvider, NFT/Jetton, DNS, payments, block subscription.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overview | Installation, provider, root API | [core-overview](references/core-overview.md) |
| TonWeb instance | Root class, getTransactions, getBalance, sendBoc, call | [core-tonweb-instance](references/core-tonweb-instance.md) |
| Address and utils | Address, toNano/fromNano, bytes/hex/base64, BN, nacl | [core-address-utils](references/core-address-utils.md) |
| BOC | Cell, BitString, fromBoc/oneFromBoc | [core-boc](references/core-boc.md) |
| Slice | Parsing BOC: beginParse, loadBit, loadUint, loadAddress, loadRef | [core-slice](references/core-slice.md) |
| Contract base | deploy, methods, getQuery/send/estimateFee, createStateInit | [core-contract](references/core-contract.md) |
| HttpProvider | getAddressInfo, getWalletInfo, sendBoc, call/call2 | [core-http-provider](references/core-http-provider.md) |
| HttpProviderUtils | parseResponse, parseObject — parse get-method stack to BN/Cell | [core-http-provider-utils](references/core-http-provider-utils.md) |
| Transfer URL | parseTransferUrl, formatTransferUrl (ton://transfer/...) | [core-transfer-url](references/core-transfer-url.md) |
| Workchain | WorkchainId Master/Basic, wc for addresses and contracts | [core-workchain](references/core-workchain.md) |
| Utils extra | AdnlAddress, StorageBagId; keyPairFromSeed, newKeyPair, newSeed | [core-utils-extra](references/core-utils-extra.md) |
| Estimate fee | estimateFee on methods, getEstimateFee(boc) on provider | [core-estimate-fee](references/core-estimate-fee.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Wallet | create, deploy, transfer, seqno, V2/V3/V4 | [features-wallet](references/features-wallet.md) |
| Highload wallet | HighloadWalletContractV3, HighloadQueryId | [features-highload-wallet](references/features-highload-wallet.md) |
| Lockup wallet | liquid/locked/restricted balances | [features-lockup-wallet](references/features-lockup-wallet.md) |
| Lockup vesting | VestingWalletV1: vesting schedule, getLockedAmount, getVestingData | [features-lockup-vesting](references/features-lockup-vesting.md) |
| NFT | NftCollection, NftItem, NftMarketplace, NftSale | [features-nft](references/features-nft.md) |
| Jetton | JettonMinter, JettonWallet, transfer, burn | [features-jetton](references/features-jetton.md) |
| NFT content & royalty | NftUtils: offchain URI cell, parseOffchainUriCell, getRoyaltyParams | [features-nft-content-royalty](references/features-nft-content-royalty.md) |
| DNS | resolve, getWalletAddress, getSiteAddress | [features-dns](references/features-dns.md) |
| Ledger | AppTon, getPublicKey, getAddress, sign, transfer; TransportWebUSB/HID/BLE | [features-ledger](references/features-ledger.md) |
| Payments | PaymentChannel, createChannel | [features-payments](references/features-payments.md) |
| Block subscription | BlockSubscription, InMemoryBlockStorage | [features-block-subscription](references/features-block-subscription.md) |
| Subscription contract | Recurring payments: pay, getSubscriptionData | [features-subscription](references/features-subscription.md) |
| Wallet parsing | parseTransferQuery, parseTransferBody (V3/V4 transfer BOC) | [features-wallet-parsing](references/features-wallet-parsing.md) |

## Best practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Custom contract | Extend Contract, createDataCell, message builders | [best-practices-custom-contract](references/best-practices-custom-contract.md) |
| Error handling | exit_code, parseResponse throws, provider/send errors | [best-practices-error-handling](references/best-practices-error-handling.md) |
