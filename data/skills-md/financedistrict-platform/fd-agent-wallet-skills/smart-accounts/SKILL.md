---
name: smart-accounts
description: Deploy and manage multi-signature smart accounts. Use when you or the user want to create a smart wallet, deploy a multi-sig, add or remove owners, change threshold, set up shared wallets, or manage account ownership. Covers "create a multi-sig", "add an owner to my account", "deploy a smart wallet", "change signing threshold".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(fdx status*)", "Bash(fdx call deploySmartAccount*)", "Bash(fdx call manageSmartAccountOwnership*)", "Bash(fdx call getWalletOverview*)"]
---

# Smart Account Management

Deploy multi-signature smart accounts on any supported EVM chain and manage their ownership (add/remove owners, change signing threshold).

## Confirm wallet is authenticated

```bash
fdx status
```

If the wallet is not authenticated, refer to the `authenticate` skill.

## Deploying a Smart Account

Create a new smart account on a specific chain:

```bash
fdx call deploySmartAccount \
  --chainKey <chain>
```

### deploySmartAccount Parameters

| Parameter         | Required | Description                                                              |
| ----------------- | -------- | ------------------------------------------------------------------------ |
| `--chainKey`      | Yes      | Blockchain to deploy on (e.g. `ethereum`, `polygon`, `base`, `arbitrum`) |
| `--initialOwners` | No       | Comma-separated list of owner addresses                                  |
| `--threshold`     | No       | Number of signatures required to execute transactions                    |

### Examples

```bash
# Deploy a simple smart account on Ethereum
fdx call deploySmartAccount --chainKey ethereum

# Deploy a 2-of-3 multi-sig
fdx call deploySmartAccount \
  --chainKey ethereum \
  --initialOwners 0xOwner1...,0xOwner2...,0xOwner3... \
  --threshold 2
```

## Managing Ownership

Add owners, remove owners, or change the signing threshold on an existing smart account:

```bash
fdx call manageSmartAccountOwnership \
  --chainKey <chain> \
  --accountAddress <smartAccountAddress> \
  --action <action>
```

### manageSmartAccountOwnership Parameters

| Parameter          | Required | Description                                                            |
| ------------------ | -------- | ---------------------------------------------------------------------- |
| `--chainKey`       | Yes      | Blockchain of the smart account                                        |
| `--accountAddress` | Yes      | Smart account address to manage                                        |
| `--action`         | Yes      | Action to perform (e.g. `addOwner`, `removeOwner`, `changeThreshold`)  |
| `--ownerAddress`   | No       | Owner address to add or remove (required for `addOwner`/`removeOwner`) |
| `--newThreshold`   | No       | New signing threshold (required for `changeThreshold`)                 |

### Examples

```bash
# Add a new owner
fdx call manageSmartAccountOwnership \
  --chainKey ethereum \
  --accountAddress 0xSmartAccount... \
  --action addOwner \
  --ownerAddress 0xNewOwner...

# Remove an owner
fdx call manageSmartAccountOwnership \
  --chainKey ethereum \
  --accountAddress 0xSmartAccount... \
  --action removeOwner \
  --ownerAddress 0xOldOwner...

# Change the threshold to 3-of-5
fdx call manageSmartAccountOwnership \
  --chainKey ethereum \
  --accountAddress 0xSmartAccount... \
  --action changeThreshold \
  --newThreshold 3
```

## Viewing Smart Account Details

Check the smart account's holdings and activity:

```bash
fdx call getWalletOverview \
  --chainKey <chain> \
  --accountAddress <smartAccountAddress>
```

## Flow

1. Check authentication with `fdx status`
2. Deploy a smart account with `fdx call deploySmartAccount`
3. Note the returned smart account address
4. Manage ownership as needed with `fdx call manageSmartAccountOwnership`
5. Use the smart account address in `send-tokens` or `swap-tokens` skills via `--fromAccountAddress`

**Important:** Ownership changes on multi-sig accounts are sensitive operations. Always confirm the action, addresses, and new threshold with your human before executing. Removing too many owners or setting the threshold too high can lock the account.

## Prerequisites

- Must be authenticated (`fdx status` to check, see `authenticate` skill)
- Smart accounts are deployed on EVM chains only (not Solana)

## Error Handling

- "Not authenticated" — Run `fdx setup` first, or see `authenticate` skill
- "Invalid account address" — Verify the smart account address exists on the specified chain
- "Threshold exceeds owner count" — Threshold must be ≤ number of owners
