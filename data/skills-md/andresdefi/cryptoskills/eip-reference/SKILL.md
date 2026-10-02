---
name: eip-reference
description: "Ethereum Improvement Proposals and ERC standards reference — ERC-20, ERC-721, ERC-1155, ERC-4626, ERC-2981, EIP-712, EIP-1559, EIP-2612 (Permit), EIP-4337 (Account Abstraction), EIP-4844 (Proto-Danksharding), EIP-7702 (EOA Delegation), ERC-8004 (Agent Identity). Quick lookup, interface signatures, and implementation patterns."
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: ethereum
  category: Infrastructure
tags:
  - eip
  - erc
  - ethereum-standards
  - erc-20
  - erc-721
  - erc-1155
  - eip-712
  - eip-4337
  - eip-7702
---

# EIP / ERC Reference

Canonical reference for Ethereum Improvement Proposals and ERC standards. Covers correct interfaces, behavioral rules, implementation patterns, and the gotchas that trip up humans and LLMs alike. Use this when you need the right function signature, the correct domain separator construction, or the nuance that separates a working implementation from a buggy one.

## What You Probably Got Wrong

> These misconceptions appear in LLM-generated code constantly. Fix your mental model before writing a single line.

- **EIP != ERC** — An EIP (Ethereum Improvement Proposal) covers the entire proposal process. An ERC (Ethereum Request for Comments) is the subset of EIPs defining application-layer standards (tokens, signatures, wallets). ERC-20 started as EIP-20 and became ERC-20 upon acceptance. Chain-level changes like EIP-1559 stay as EIPs — they are never ERCs.
- **ERC-20 `approve` has a race condition** — If Alice approves Bob for 100, then changes to 50, Bob can front-run: spend the original 100, then spend the new 50, totaling 150. Mitigation: approve to 0 first, use `increaseAllowance`/`decreaseAllowance`, or use ERC-2612 `permit`. USDT requires resetting to 0 before setting a new nonzero allowance — it reverts otherwise.
- **ERC-721 `transferFrom` skips receiver checks** — `transferFrom` does NOT call `onERC721Received` on the recipient. Tokens sent to contracts that cannot handle them are permanently locked. Use `safeTransferFrom` unless you have a specific reason not to.
- **EIP-712 domain separator MUST include `chainId`** — Omitting `chainId` from the `EIP712Domain` allows signature replay across chains. A signature valid on mainnet becomes valid on every fork and L2 sharing the contract address. Always include `chainId` and `verifyingContract`.
- **ERC-4337 bundler != relayer** — A bundler packages `UserOperation` objects and submits to the `EntryPoint`. A relayer wraps a signed message and calls a trusted forwarder. Different trust models, different gas accounting, different entry points.
- **EIP-1559 `baseFee` is protocol-controlled** — Users set `maxFeePerGas` and `maxPriorityFeePerGas`. The protocol sets `baseFee` per block. The base fee is burned, the priority fee goes to the validator. Confusing these causes incorrect gas estimation.
- **ERC-4626 share/asset math is rounding-sensitive** — `convertToShares` and `convertToAssets` must round in favor of the vault to prevent share inflation attacks. First-depositor attacks exploit vaults that skip this.
- **EIP-2612 permit signatures can be front-run** — The approval still takes effect, but the original `permit` call reverts. Always check allowance before calling permit.
- **ERC-1155 has no per-token approval** — Only `setApprovalForAll` exists (operator model). There is no `approve(tokenId)` like ERC-721.
- **`decimals()` is OPTIONAL** — Part of `IERC20Metadata`, not `IERC20`. USDC uses 6, WBTC uses 8. Never assume 18.

## How to Look Up Any EIP

When a user asks about ANY EIP or ERC — even ones not covered in this skill — fetch the full spec on demand.

### Step 1: Determine if it's an EIP or ERC

- **ERC** (ERC-20, ERC-721, ERC-1155, ERC-4626, etc.) — application-level standards. Repo: `ethereum/ERCs`
- **EIP** (EIP-1559, EIP-4844, EIP-7702, etc.) — core/networking/interface changes. Repo: `ethereum/EIPs`
- Rule of thumb: token standards and contract interfaces are ERCs. Protocol-level changes are EIPs.
- If unsure, try ERC first (more common in user queries), fall back to EIP.

### Step 2: Fetch the raw spec

**For ERCs** (application-level — tokens, wallets, contract standards):

```
WebFetch: https://raw.githubusercontent.com/ethereum/ERCs/master/ERCS/erc-{number}.md
```

**For EIPs** (core/networking — gas, consensus, transaction types):

```
WebFetch: https://raw.githubusercontent.com/ethereum/EIPs/master/EIPS/eip-{number}.md
```

Examples:
- ERC-20 → `https://raw.githubusercontent.com/ethereum/ERCs/master/ERCS/erc-20.md`
- ERC-4337 → `https://raw.githubusercontent.com/ethereum/ERCs/master/ERCS/erc-4337.md`
- EIP-1559 → `https://raw.githubusercontent.com/ethereum/EIPs/master/EIPS/eip-1559.md`
- EIP-7702 → `https://raw.githubusercontent.com/ethereum/EIPs/master/EIPS/eip-7702.md`

### Step 3: Parse and summarize

The fetched markdown has YAML frontmatter (`eip`, `title`, `status`, `type`, `category`, `author`, `created`, `requires`) followed by sections: Simple Summary, Abstract, Motivation, Specification, Rationale, Backwards Compatibility, Security Considerations, Copyright.

Extract and present: title, status, what it does, key interfaces/types, and security considerations.

### Alternative methods

```bash
# GitHub CLI (requires auth)
gh api repos/ethereum/ERCs/contents/ERCS/erc-{number}.md --jq '.content' | base64 -d
gh api repos/ethereum/EIPs/contents/EIPS/eip-{number}.md --jq '.content' | base64 -d
```

### Sources

| Source | URL | Best for |
|--------|-----|----------|
| EIPs repo | https://github.com/ethereum/EIPs | Core/networking specs, raw markdown |
| ERCs repo | https://github.com/ethereum/ERCs | Token/application standards, raw markdown |
| EIPs website | https://eips.ethereum.org/all | Browsing all EIPs with status filters |

- Raw EIP specs: `https://raw.githubusercontent.com/ethereum/EIPs/master/EIPS/eip-{number}.md`
- Raw ERC specs: `https://raw.githubusercontent.com/ethereum/ERCs/master/ERCS/erc-{number}.md`
- Browse all: https://eips.ethereum.org/all

## EIP vs ERC

| Type | Scope | Examples |
|------|-------|---------|
| **EIP** | Protocol-level changes (consensus, networking, EVM) | EIP-1559, EIP-4844, EIP-7702 |
| **ERC** | Application-level standards (tokens, wallets, signing) | ERC-20, ERC-721, ERC-4337 |

ERCs are a subset of EIPs. "ERC-20" and "EIP-20" refer to the same proposal. The ERC designation applies once the proposal reaches application-layer Final status.

### Status Lifecycle

```
Draft -> Review -> Last Call -> Final
                             -> Stagnant (no activity 6+ months)
                             -> Withdrawn
```

Only **Final** status EIPs should be relied on in production. Draft/Review standards may change without notice.

## Token Standards

### ERC-20 — Fungible Token

The base token standard. Every DeFi protocol depends on this interface.

```solidity
interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
```

**Key rules:**
- `transfer` and `transferFrom` MUST return `true` on success. Some tokens (USDT) do not return a value — use OpenZeppelin `SafeERC20`.
- `decimals()` is OPTIONAL (part of `IERC20Metadata`). USDC/USDT use 6, WBTC uses 8.
- Minting: `Transfer(address(0), to, amount)`. Burning: `Transfer(from, address(0), amount)`.
- Fee-on-transfer tokens deduct on every transfer — always measure `balanceOf` before/after.

```typescript
import { erc20Abi, formatUnits } from 'viem';

const balance = await publicClient.readContract({
  address: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', // USDC
  abi: erc20Abi,
  functionName: 'balanceOf',
  args: ['0xYourAddress...'],
});
// balance is bigint in base units — format with correct decimals
const formatted = formatUnits(balance, 6); // USDC has 6 decimals
```

### ERC-721 — Non-Fungible Token

Each token has a unique `tokenId`. Ownership is 1:1.

```solidity
interface IERC721 is IERC165 {
    function balanceOf(address owner) external view returns (uint256);
    function ownerOf(uint256 tokenId) external view returns (address);
    function safeTransferFrom(address from, address to, uint256 tokenId, bytes calldata data) external;
    function safeTransferFrom(address from, address to, uint256 tokenId) external;
    function transferFrom(address from, address to, uint256 tokenId) external;
    function approve(address to, uint256 tokenId) external;
    function setApprovalForAll(address operator, bool approved) external;
    function getApproved(uint256 tokenId) external view returns (address);
    function isApprovedForAll(address owner, address operator) external view returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);
    event ApprovalForAll(address indexed owner, address indexed operator, bool approved);
}
```

**Key rules:**
- `safeTransferFrom` calls `IERC721Receiver.onERC721Received` on contract recipients. Reverts if not implemented or wrong selector returned.
- `transferFrom` skips receiver checks — tokens can be permanently lost.
- `approve` clears on transfer — the approved address resets when the token moves.
- `ownerOf` MUST revert for nonexistent tokens (never return `address(0)`).

### ERC-1155 — Multi-Token

Single contract managing multiple token types (fungible and non-fungible) identified by `id`.

```solidity
interface IERC1155 is IERC165 {
    function balanceOf(address account, uint256 id) external view returns (uint256);
    function balanceOfBatch(address[] calldata accounts, uint256[] calldata ids)
        external view returns (uint256[] memory);
    function setApprovalForAll(address operator, bool approved) external;
    function isApprovedForAll(address account, address operator) external view returns (bool);
    function safeTransferFrom(address from, address to, uint256 id, uint256 amount, bytes calldata data) external;
    function safeBatchTransferFrom(
        address from, address to, uint256[] calldata ids, uint256[] calldata amounts, bytes calldata data
    ) external;

    event TransferSingle(address indexed operator, address indexed from, address indexed to, uint256 id, uint256 value);
    event TransferBatch(
        address indexed operator, address indexed from, address indexed to, uint256[] ids, uint256[] values
    );
}
```

**Key rules:**
- ALL transfers are safe — `onERC1155Received` / `onERC1155BatchReceived` is always called.
- No per-token approval — only `setApprovalForAll` (operator model).
- Batch operations save gas on multi-token transfers.

### ERC-4626 — Tokenized Vault

Standard for yield-bearing vaults. The vault itself is an ERC-20 representing shares.

```solidity
interface IERC4626 is IERC20 {
    function asset() external view returns (address);
    function totalAssets() external view returns (uint256);
    function convertToShares(uint256 assets) external view returns (uint256);
    function convertToAssets(uint256 shares) external view returns (uint256);
    function deposit(uint256 assets, address receiver) external returns (uint256 shares);
    function mint(uint256 shares, address receiver) external returns (uint256 assets);
    function withdraw(uint256 assets, address receiver, address owner) external returns (uint256 shares);
    function redeem(uint256 shares, address receiver, address owner) external returns (uint256 assets);
    function maxDeposit(address receiver) external view returns (uint256);
    function maxMint(address receiver) external view returns (uint256);
    function maxWithdraw(address owner) external view returns (uint256);
    function maxRedeem(address owner) external view returns (uint256);
    function previewDeposit(uint256 assets) external view returns (uint256);
    function previewMint(uint256 shares) external view returns (uint256);
    function previewWithdraw(uint256 assets) external view returns (uint256);
    function previewRedeem(uint256 shares) external view returns (uint256);

    event Deposit(address indexed sender, address indexed owner, uint256 assets, uint256 shares);
    event Withdraw(address indexed sender, address indexed receiver, address indexed owner, uint256 assets, uint256 shares);
}
```

**Key rules:**
- `deposit`/`mint` are asset-denominated vs share-denominated entry. `withdraw`/`redeem` are asset-denominated vs share-denominated exit.
- `preview*` functions MUST return exact values (not estimates).
- Rounding: favor the vault. `convertToShares` rounds DOWN, `previewMint`/`previewWithdraw` round UP.
- First-depositor attack: attacker deposits 1 wei, donates tokens to inflate share price. Mitigate with virtual shares/assets offset or minimum deposit.

### ERC-2981 — NFT Royalties

```solidity
interface IERC2981 is IERC165 {
    function royaltyInfo(uint256 tokenId, uint256 salePrice)
        external view returns (address receiver, uint256 royaltyAmount);
}
```

Returns royalty recipient and amount for a given sale price. Enforcement is voluntary — marketplaces query this but the standard cannot force payment.

## Signature & Auth Standards

### EIP-712 — Typed Structured Data Signing

Structured, human-readable signing. Users see the data they sign in their wallet.

```solidity
bytes32 DOMAIN_SEPARATOR = keccak256(abi.encode(
    keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"),
    keccak256(bytes("MyProtocol")),
    keccak256(bytes("1")),
    block.chainid,
    address(this)
));

bytes32 constant PERMIT_TYPEHASH = keccak256(
    "Permit(address owner,address spender,uint256 value,uint256 nonce,uint256 deadline)"
);

bytes32 digest = keccak256(abi.encodePacked(
    "\x19\x01",
    DOMAIN_SEPARATOR,
    keccak256(abi.encode(PERMIT_TYPEHASH, owner, spender, value, nonce, deadline))
));
```

```typescript
const signature = await walletClient.signTypedData({
  domain: {
    name: 'MyProtocol',
    version: '1',
    chainId: 1,
    verifyingContract: '0xContractAddress...',
  },
  types: {
    Permit: [
      { name: 'owner', type: 'address' },
      { name: 'spender', type: 'address' },
      { name: 'value', type: 'uint256' },
      { name: 'nonce', type: 'uint256' },
      { name: 'deadline', type: 'uint256' },
    ],
  },
  primaryType: 'Permit',
  message: {
    owner: '0xOwner...',
    spender: '0xSpender...',
    value: 1000000n,
    nonce: 0n,
    deadline: BigInt(Math.floor(Date.now() / 1000) + 3600),
  },
});
```

**Key rules:**
- Domain separator MUST be recomputed if `block.chainid` changes (fork protection).
- Nested structs: referenced types appended alphabetically after the primary type.
- `bytes` and `string` fields are `keccak256`-ed before encoding.
- Do NOT list `EIP712Domain` in the `types` object — viem derives it from the `domain` field.

### ERC-2612 — Permit (Gasless Approval)

EIP-712 signed approvals for ERC-20 tokens. Eliminates the separate `approve` transaction.

```solidity
interface IERC20Permit {
    function permit(
        address owner, address spender, uint256 value,
        uint256 deadline, uint8 v, bytes32 r, bytes32 s
    ) external;
    function nonces(address owner) external view returns (uint256);
    function DOMAIN_SEPARATOR() external view returns (bytes32);
}
```

**Key rules:**
- `deadline` is a Unix timestamp. Always check `block.timestamp <= deadline`.
- Nonces are sequential per-owner. Cannot skip or reorder.
- Not all ERC-20 tokens support permit. DAI uses a non-standard permit with `allowed` (bool) instead of `value` (uint256).
- Permit signatures can be front-run — check allowance before calling permit.

### EIP-4361 — Sign-In With Ethereum (SIWE)

Standard message format for using an Ethereum address to authenticate with off-chain services.

```
example.com wants you to sign in with your Ethereum account:
0xAddress...

I accept the Terms of Service: https://example.com/tos

URI: https://example.com
Version: 1
Chain ID: 1
Nonce: abc123
Issued At: 2026-03-04T12:00:00.000Z
```

Used by dApps for wallet-based authentication. The message is human-readable, domain-bound (prevents phishing), and includes a server-issued nonce for replay protection.

### ERC-1271 — Contract Signature Verification

Allows smart contracts (multisigs, smart accounts) to validate signatures.

```solidity
interface IERC1271 {
    function isValidSignature(bytes32 hash, bytes memory signature)
        external view returns (bytes4 magicValue);
}
// MUST return 0x1626ba7e if valid
```

**Dual verification pattern (EOA + contract):**

```solidity
function _isValidSignature(address signer, bytes32 hash, bytes memory signature) internal view returns (bool) {
    if (signer.code.length > 0) {
        try IERC1271(signer).isValidSignature(hash, signature) returns (bytes4 magicValue) {
            return magicValue == 0x1626ba7e;
        } catch {
            return false;
        }
    } else {
        return ECDSA.recover(hash, signature) == signer;
    }
}
```

## Gas & Transaction Standards

### EIP-1559 — Fee Market

Base fee + priority fee model. The base fee is burned.

| Field | Set by | Description |
|-------|--------|-------------|
| `baseFeePerGas` | Protocol | Adjusts per block based on utilization. Burned. |
| `maxPriorityFeePerGas` | User | Tip to the validator. |
| `maxFeePerGas` | User | Maximum total fee per gas unit. |

```
effectiveGasPrice = min(baseFeePerGas + maxPriorityFeePerGas, maxFeePerGas)
```

Base fee increases up to 12.5% per block when utilization exceeds 50% target (15M gas of 30M limit).

### EIP-4844 — Blob Transactions (Proto-Danksharding)

Type 3 transactions carrying blobs for L2 data availability.

- Blobs are ~128 KB each, target 6 per block (post-Pectra), max 9.
- Blob data is NOT accessible from the EVM — only the versioned hash.
- Blobs are pruned after ~18 days.
- Separate fee market with independently adjusting `blobBaseFee`.
- Used by Arbitrum, Optimism, Base, and Scroll for data posting.

### EIP-2930 — Access Lists

Pre-declare which addresses and storage keys will be accessed.

```typescript
const accessList = await publicClient.createAccessList({
  account: '0xSender...',
  to: '0xContract...',
  data: encodedCalldata,
});
```

Pre-warming costs 2,400 gas per slot (vs 2,600 cold access). Useful for cross-contract calls accessing known storage.

## Account Abstraction

### ERC-4337 — Account Abstraction via Entry Point

Smart contract wallets with `UserOperation` objects processed by bundlers.

**Core flow:**
```
User creates UserOperation
  -> Bundler collects and simulates
    -> Bundler calls EntryPoint.handleOps(userOps, beneficiary)
      -> EntryPoint calls account.validateUserOp(...)
        -> If paymaster: validates sponsorship
          -> EntryPoint executes the operation
```

**PackedUserOperation (v0.7):**

```solidity
struct PackedUserOperation {
    address sender;
    uint256 nonce;               // 192-bit key + 64-bit sequence for parallel channels
    bytes initCode;              // factory address + calldata (first-time only)
    bytes callData;
    bytes32 accountGasLimits;    // verificationGasLimit (16 bytes) + callGasLimit (16 bytes)
    uint256 preVerificationGas;
    bytes32 gasFees;             // maxPriorityFeePerGas (16 bytes) + maxFeePerGas (16 bytes)
    bytes paymasterAndData;      // paymaster address + gas limits + custom data
    bytes signature;
}
```

**EntryPoint v0.7:** `0x0000000071727De22E5E9d8BAf0edAc6f37da032`

**Key rules:**
- `validateUserOp` MUST return `SIG_VALIDATION_FAILED` (1) on bad signatures, NOT revert.
- Banned opcodes during validation: `GASPRICE`, `TIMESTAMP`, `BLOCKHASH`, `CREATE`, etc.
- Paymasters pre-deposit ETH to EntryPoint and can sponsor gas or accept ERC-20 payment.

### EIP-7702 — EOA Delegation

EOAs temporarily or persistently delegate execution to smart contract code. Type `0x04` transactions include an `authorizationList`.

```
authorization_tuple = (chain_id, address, nonce, y_parity, r, s)
```

When processed, the EOA's code is set to `0xef0100 || address`. Calls execute the delegated contract's code in the EOA's context (like delegatecall).

```typescript
import { walletClient } from './config';

const authorization = await walletClient.signAuthorization({
  contractAddress: '0xBatchExecutor...',
});

const hash = await walletClient.writeContract({
  address: walletClient.account.address,
  abi: batchExecutorAbi,
  functionName: 'executeBatch',
  args: [[
    { target: '0xTokenA...', value: 0n, data: approveCalldata },
    { target: '0xRouter...', value: 0n, data: swapCalldata },
  ]],
  authorizationList: [authorization],
});
```

**EIP-7702 + ERC-4337**: Complementary. Bundlers accept `eip7702Auth` on UserOperations, letting EOAs participate in AA without migrating addresses.

### ERC-8004 — Agent Identity Registry

Onchain identity for AI agents — three registries for discovery, reputation, and validation.

```solidity
interface IAgentIdentityRegistry {
    struct AgentIdentity {
        string name;
        string[] skills;
        string endpoint;
        bytes metadata;
    }

    function registerAgent(AgentIdentity calldata identity) external returns (uint256 agentId);
    function getAgent(uint256 agentId) external view returns (AgentIdentity memory);
    function resolveByName(string calldata name) external view returns (uint256 agentId);

    event AgentRegistered(uint256 indexed agentId, address indexed owner, string name);
}
```

Reputation registry provides immutable feedback (append-only, no edits). Validation registry enables third-party verification of agent capabilities. Integrates with x402 for payment authentication.

## Proxy & Upgrade Patterns

### EIP-1967 — Proxy Storage Slots

```solidity
// Implementation: bytes32(uint256(keccak256("eip1967.proxy.implementation")) - 1)
bytes32 constant IMPLEMENTATION_SLOT = 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;

// Admin: bytes32(uint256(keccak256("eip1967.proxy.admin")) - 1)
bytes32 constant ADMIN_SLOT = 0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103;

// Beacon: bytes32(uint256(keccak256("eip1967.proxy.beacon")) - 1)
bytes32 constant BEACON_SLOT = 0xa3f0ad74e5423aebfd80d3ef4346578335a9a72aeaee59ff6cb3582b35133d50;
```

### EIP-1822 — UUPS Proxy

Upgrade logic in the implementation, not the proxy. Smaller proxy, cheaper deploys. **Risk**: if you deploy an implementation without `upgradeTo`, the proxy is permanently bricked.

### EIP-7201 — Namespaced Storage

Deterministic storage locations for upgradeable contracts. Prevents slot collisions across inheritance. OpenZeppelin v5+ uses this by default.

```solidity
/// @custom:storage-location erc7201:myprotocol.storage.Counter
struct CounterStorage {
    uint256 count;
    mapping(address => uint256) perUser;
}
```

## Interface Detection

### ERC-165 — Standard Interface Detection

```solidity
function supportsInterface(bytes4 interfaceId) external view returns (bool);
```

**Common interface IDs:**

| Interface | ID |
|-----------|-----|
| IERC165 | `0x01ffc9a7` |
| IERC721 | `0x80ac58cd` |
| IERC721Metadata | `0x5b5e139f` |
| IERC1155 | `0xd9b67a26` |
| IERC2981 | `0x2a55205a` |

ERC-20 predates ERC-165 — do not rely on `supportsInterface` to detect ERC-20 tokens.

### EIP-6963 — Multi-Wallet Discovery

Replaces the `window.ethereum` single-provider model. Wallets announce themselves via DOM events, eliminating the provider collision problem.

```typescript
window.addEventListener('eip6963:announceProvider', (event) => {
  const { info, provider } = event.detail;
  // info.name, info.icon, info.rdns, info.uuid
});
window.dispatchEvent(new Event('eip6963:requestProvider'));
```

## Chain & Network

### EIP-155 — Replay Protection

Chain ID in transaction signatures prevents cross-chain replay. Common IDs:

| Chain | ID | Chain | ID |
|-------|----|-------|----|
| Ethereum Mainnet | 1 | Polygon | 137 |
| Sepolia | 11155111 | Arbitrum One | 42161 |
| Base | 8453 | Optimism | 10 |

### EIP-1193 — Provider API

Standard JavaScript API for Ethereum providers (`window.ethereum`).

```typescript
interface EIP1193Provider {
  request(args: { method: string; params?: unknown[] }): Promise<unknown>;
  on(event: string, listener: (...args: unknown[]) => void): void;
  removeListener(event: string, listener: (...args: unknown[]) => void): void;
}
```

## Quick Lookup Table

| Number | Name | Type | Status |
|--------|------|------|--------|
| ERC-20 | Token Standard | ERC | Final |
| ERC-165 | Interface Detection | ERC | Final |
| EIP-155 | Replay Protection (Chain ID) | EIP | Final |
| EIP-191 | Signed Data Standard | EIP | Final |
| ERC-721 | Non-Fungible Token | ERC | Final |
| ERC-1155 | Multi-Token | ERC | Final |
| ERC-1271 | Contract Signature Verification | ERC | Final |
| EIP-712 | Typed Structured Data Signing | EIP | Final |
| EIP-1014 | CREATE2 Deterministic Addresses | EIP | Final |
| EIP-1193 | JavaScript Provider API | EIP | Final |
| EIP-1559 | Fee Market (Base + Priority Fee) | EIP | Final |
| EIP-1822 | UUPS Proxy | EIP | Final |
| EIP-1967 | Proxy Storage Slots | EIP | Final |
| EIP-2098 | Compact 64-byte Signatures | EIP | Final |
| ERC-2612 | ERC-20 Permit (Gasless Approval) | ERC | Final |
| EIP-2718 | Typed Transaction Envelope | EIP | Final |
| EIP-2930 | Access Lists (Type 1 Tx) | EIP | Final |
| ERC-2981 | NFT Royalty Standard | ERC | Final |
| ERC-3009 | Transfer With Authorization | ERC | Final |
| EIP-3156 | Flash Loan Standard | EIP | Final |
| ERC-4337 | Account Abstraction (EntryPoint) | ERC | Final |
| EIP-4361 | Sign-In With Ethereum | EIP | Final |
| ERC-4626 | Tokenized Vault | ERC | Final |
| EIP-4844 | Blob Transactions (Proto-Danksharding) | EIP | Final |
| EIP-6093 | Custom Errors for Tokens | EIP | Final |
| EIP-6963 | Multi-Wallet Discovery | EIP | Final |
| EIP-7201 | Namespaced Storage Layout | EIP | Final |
| ERC-7579 | Modular Smart Accounts | ERC | Draft |
| EIP-7702 | EOA Delegation (Set Account Code) | EIP | Final |
| EIP-7951 | secp256r1 Precompile (Passkeys) | EIP | Final |
| ERC-8004 | Agent Identity Registry | ERC | Draft |

Last verified: March 2026

## Related Skills

- **eth-concepts** — EVM internals, gas mechanics, storage layout, transaction types
- **account-abstraction** — Full ERC-4337/EIP-7702/ERC-7579 implementation patterns
- **solidity-security** — Security patterns, CEI, reentrancy guards, access control
- **evm-nfts** — NFT minting, metadata, marketplace integration patterns
- **x402** — Agent payment protocol (integrates with ERC-8004)

## References

- [EIPs Repository](https://eips.ethereum.org) — Canonical source for all EIP/ERC text
- [ERC-20](https://eips.ethereum.org/EIPS/eip-20) — Token Standard
- [ERC-721](https://eips.ethereum.org/EIPS/eip-721) — Non-Fungible Token
- [ERC-1155](https://eips.ethereum.org/EIPS/eip-1155) — Multi-Token
- [ERC-4626](https://eips.ethereum.org/EIPS/eip-4626) — Tokenized Vault
- [ERC-2981](https://eips.ethereum.org/EIPS/eip-2981) — NFT Royalty Standard
- [EIP-712](https://eips.ethereum.org/EIPS/eip-712) — Typed Structured Data
- [ERC-2612](https://eips.ethereum.org/EIPS/eip-2612) — Permit Extension
- [ERC-4337](https://eips.ethereum.org/EIPS/eip-4337) — Account Abstraction
- [EIP-1559](https://eips.ethereum.org/EIPS/eip-1559) — Fee Market Change
- [EIP-4844](https://eips.ethereum.org/EIPS/eip-4844) — Shard Blob Transactions
- [EIP-7702](https://eips.ethereum.org/EIPS/eip-7702) — Set EOA Account Code
- [ERC-8004](https://eips.ethereum.org/EIPS/eip-8004) — Agent Identity Registry
- [EIP-6963](https://eips.ethereum.org/EIPS/eip-6963) — Multi-Wallet Discovery
- [EIP-7951](https://eips.ethereum.org/EIPS/eip-7951) — secp256r1 Precompile
- [OpenZeppelin Contracts v5](https://docs.openzeppelin.com/contracts/5.x/) — Reference implementations
- [Viem Documentation](https://viem.sh/) — TypeScript Ethereum library
