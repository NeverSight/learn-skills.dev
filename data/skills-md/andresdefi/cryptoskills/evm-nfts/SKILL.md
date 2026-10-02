---
name: evm-nfts
description: "ERC-721 and ERC-1155 NFT development patterns for EVM chains. Covers minting, metadata, royalties, marketplace integration with Seaport, and security pitfalls. Uses OpenZeppelin v5.6.1."
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: multichain
  category: NFT & Tokens
tags:
  - erc-721
  - erc-1155
  - nft
  - evm
  - solidity
  - metadata
  - royalties
  - erc-2981
  - seaport
  - openzeppelin
  - minting
  - token
---

# EVM NFTs

ERC-721 and ERC-1155 are the two NFT standards on EVM chains. ERC-721 represents unique tokens (1-of-1 art, PFPs, deeds), while ERC-1155 represents semi-fungible tokens (game items, editions, tickets). This skill covers secure minting patterns, metadata standards, royalty implementation, and marketplace integration using OpenZeppelin v5.6.1 and Seaport 1.6.

## What You Probably Got Wrong

- **`_safeMint` calls `onERC721Received` on the receiver -- reentrancy vector.** The `_safeMint` function makes an external call to the receiver if it is a contract. A malicious receiver contract can re-enter your mint function and mint more tokens than allowed. Use `ReentrancyGuard` on ALL mint functions, without exception.

- **Allowlist signatures without EIP-712 domain separators are replayed across chains and contracts.** Always include `block.chainid` and `address(this)` in the domain separator. Signatures MUST include a per-address nonce (tracked onchain in a mapping) and a deadline (`block.timestamp` expiry). Without nonces, a single valid signature can be replayed indefinitely.

- **`transferFrom` does NOT check `onERC721Received` -- only `safeTransferFrom` does.** If you send an ERC-721 token to a contract using `transferFrom`, the contract has no way to react or reject the transfer. The token can be permanently locked. Always use `safeTransferFrom` when the recipient might be a contract.

- **Royalties (ERC-2981) are NOT enforced onchain.** ERC-2981 is a read-only interface. Marketplaces query `royaltyInfo()` and can choose to ignore it. For practical enforcement, use ERC-721C (Limit Break's transfer validator pattern) which hooks into transfer functions to enforce payment.

- **ERC-721 has TWO independent approval mechanisms.** `approve(to, tokenId)` grants approval for a single token. `setApprovalForAll(operator, true)` grants blanket approval for all tokens. These are independent -- revoking one does not affect the other. Users commonly forget `setApprovalForAll` remains active after individual approvals are cleared.

- **`tokenURI` returns a URI that resolves to JSON metadata, not a URL to an image.** The URI points to a JSON document with `name`, `description`, `image`, and optional `attributes`. The `image` field inside that JSON is the actual image URL.

- **ERC-1155 has no `name()` or `symbol()` in the standard.** Use `uri(id)` to get the metadata URI for a specific token ID. OpenZeppelin's ERC1155 implementation does not expose name/symbol by default.

- **`{id}` substitution in ERC-1155 URIs is client-side.** The `uri()` function returns a template like `https://api.example.com/token/{id}.json`. The `{id}` placeholder must be replaced by the client with the hex token ID, zero-padded to 64 characters, lowercase, no `0x` prefix. Example: token ID 1 becomes `0000000000000000000000000000000000000000000000000000000000000001`.

- **`balanceOf` returns a count, not token IDs.** For ERC-721, getting the list of owned token IDs requires `tokenOfOwnerByIndex` (only available if the contract extends ERC721Enumerable). Without enumeration, you must index Transfer events off-chain.

- **`tokenURI` returns empty string for non-existent tokens in some implementations.** OpenZeppelin v5.6.1's ERC721URIStorage returns empty string if the token has not been minted. It does NOT revert. Always check `_ownerOf(tokenId) != address(0)` before returning metadata if you want to revert for non-existent tokens.

- **Seaport 1.6 is the current marketplace protocol.** Same deterministic address on all EVM chains: `0x0000000000000068F116A894984e2DB1123eB395`. Do not use Seaport 1.4 or 1.5 -- they have known issues.

- **Reservoir is DEPRECATED.** Reservoir shut down in October 2025. Use Seaport directly or the OpenSea API for marketplace integration.

## OpenZeppelin v5.6.1 Patterns

OpenZeppelin v5 introduced breaking changes from v4. All code in this skill targets v5.6.1.

| v4 Pattern (BROKEN) | v5.6.1 Pattern (CORRECT) |
|---------------------|-------------------------|
| `using Counters for Counters.Counter` | Use `uint256 private _nextTokenId` directly |
| `_beforeTokenTransfer` / `_afterTokenTransfer` | Override `_update(to, tokenId, auth)` |
| `Ownable()` (no args) | `Ownable(initialOwner)` -- owner is required in constructor |
| `ERC721("Name", "Symbol")` only | Same, but URI storage auto-returns from `tokenURI()` |
| `_safeMint(to, tokenId)` then `_setTokenURI` | Same pattern, but `_update` is the hook point |
| `_exists(tokenId)` | `_ownerOf(tokenId) != address(0)` |

```bash
forge install OpenZeppelin/openzeppelin-contracts@v5.6.1
```

## ERC-721

### Interface

```solidity
interface IERC721 {
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);
    event ApprovalForAll(address indexed owner, address indexed operator, bool approved);

    function balanceOf(address owner) external view returns (uint256);
    function ownerOf(uint256 tokenId) external view returns (address);
    function safeTransferFrom(address from, address to, uint256 tokenId, bytes calldata data) external;
    function safeTransferFrom(address from, address to, uint256 tokenId) external;
    function transferFrom(address from, address to, uint256 tokenId) external;
    function approve(address to, uint256 tokenId) external;
    function setApprovalForAll(address operator, bool approved) external;
    function getApproved(uint256 tokenId) external view returns (address);
    function isApprovedForAll(address owner, address operator) external view returns (bool);
}
```

### Minimal ERC-721 with Mint (OpenZeppelin v5.6.1)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract SimpleNFT is ERC721, Ownable, ReentrancyGuard {
    uint256 private _nextTokenId;
    uint256 public constant MAX_SUPPLY = 10_000;

    error MaxSupplyReached();

    constructor(address initialOwner)
        ERC721("SimpleNFT", "SNFT")
        Ownable(initialOwner)
    {}

    function mint(address to) external onlyOwner nonReentrant {
        uint256 tokenId = _nextTokenId++;
        if (tokenId >= MAX_SUPPLY) revert MaxSupplyReached();
        _safeMint(to, tokenId);
    }

    function totalSupply() external view returns (uint256) {
        return _nextTokenId;
    }
}
```

### ERC721Enumerable

Adds `tokenOfOwnerByIndex` and `tokenByIndex` for on-chain enumeration. Increases gas cost for transfers by ~50%. Only use when on-chain enumeration is a hard requirement.

```solidity
import {ERC721Enumerable} from "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";

contract EnumerableNFT is ERC721Enumerable, Ownable, ReentrancyGuard {
    uint256 private _nextTokenId;

    constructor(address initialOwner)
        ERC721("EnumerableNFT", "ENFT")
        Ownable(initialOwner)
    {}

    function _update(address to, uint256 tokenId, address auth)
        internal
        override(ERC721Enumerable)
        returns (address)
    {
        return super._update(to, tokenId, auth);
    }

    function _increaseBalance(address account, uint128 value)
        internal
        override(ERC721Enumerable)
    {
        super._increaseBalance(account, value);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721Enumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
```

## ERC-1155

### Interface

```solidity
interface IERC1155 {
    event TransferSingle(address indexed operator, address indexed from, address indexed to, uint256 id, uint256 value);
    event TransferBatch(address indexed operator, address indexed from, address indexed to, uint256[] ids, uint256[] values);
    event ApprovalForAll(address indexed account, address indexed operator, bool approved);
    event URI(string value, uint256 indexed id);

    function balanceOf(address account, uint256 id) external view returns (uint256);
    function balanceOfBatch(address[] calldata accounts, uint256[] calldata ids) external view returns (uint256[] memory);
    function setApprovalForAll(address operator, bool approved) external;
    function isApprovedForAll(address account, address operator) external view returns (bool);
    function safeTransferFrom(address from, address to, uint256 id, uint256 amount, bytes calldata data) external;
    function safeBatchTransferFrom(address from, address to, uint256[] calldata ids, uint256[] calldata amounts, bytes calldata data) external;
}
```

### ERC-1155 with Supply Tracking

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC1155} from "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import {ERC1155Supply} from "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155Supply.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract GameItems is ERC1155, ERC1155Supply, Ownable, ReentrancyGuard {
    uint256 public constant SWORD = 0;
    uint256 public constant SHIELD = 1;
    uint256 public constant POTION = 2;

    mapping(uint256 id => uint256 cap) public maxSupply;

    error ExceedsMaxSupply(uint256 id);

    constructor(address initialOwner)
        ERC1155("https://api.example.com/items/{id}.json")
        Ownable(initialOwner)
    {
        maxSupply[SWORD] = 1_000;
        maxSupply[SHIELD] = 5_000;
        maxSupply[POTION] = 100_000;
    }

    function mint(address to, uint256 id, uint256 amount) external onlyOwner nonReentrant {
        if (totalSupply(id) + amount > maxSupply[id]) revert ExceedsMaxSupply(id);
        _mint(to, id, amount, "");
    }

    function mintBatch(address to, uint256[] calldata ids, uint256[] calldata amounts)
        external
        onlyOwner
        nonReentrant
    {
        for (uint256 i = 0; i < ids.length; i++) {
            if (totalSupply(ids[i]) + amounts[i] > maxSupply[ids[i]]) revert ExceedsMaxSupply(ids[i]);
        }
        _mintBatch(to, ids, amounts, "");
    }

    function _update(address from, address to, uint256[] memory ids, uint256[] memory values)
        internal
        override(ERC1155, ERC1155Supply)
    {
        super._update(from, to, ids, values);
    }
}
```

## Metadata Standards

### Metadata JSON Schema (ERC-721)

```json
{
  "name": "Token #1",
  "description": "Description of the token",
  "image": "ipfs://Qm.../1.png",
  "external_url": "https://example.com/token/1",
  "attributes": [
    { "trait_type": "Color", "value": "Red" },
    { "trait_type": "Level", "value": 5, "display_type": "number" },
    { "trait_type": "Power", "value": 85, "max_value": 100 }
  ]
}
```

### Metadata Storage Comparison

| Storage | Cost | Immutability | Speed | Best For |
|---------|------|-------------|-------|----------|
| IPFS (pinned) | Low (~$5/GB/year via Pinata/nft.storage) | Content-addressed, immutable if pinned | Moderate (gateway dependent) | Most collections, art, PFPs |
| Arweave | One-time (~$5/GB permanent) | Permanent, truly immutable | Moderate | Archival, high-value art |
| Onchain SVG | High (~50k-200k gas per token) | Fully onchain, chain-immutable | Instant (no external dependency) | Generative art, dynamic NFTs |
| Centralized API | Cheapest | Mutable, server-dependent | Fast | Game items, evolving metadata |

### Contract-Level Metadata (contractURI)

OpenSea and other marketplaces read `contractURI()` for collection-level metadata:

```solidity
function contractURI() external pure returns (string memory) {
    return "ipfs://QmCollectionMetadataHash";
}
```

The JSON at that URI:

```json
{
  "name": "Collection Name",
  "description": "Collection description",
  "image": "ipfs://QmCollectionImage",
  "external_link": "https://example.com",
  "seller_fee_basis_points": 500,
  "fee_recipient": "0xRoyaltyRecipient..."
}
```

### ERC-4906: Metadata Update Events

Signal marketplaces to refresh metadata for specific tokens or ranges:

```solidity
import {IERC4906} from "@openzeppelin/contracts/interfaces/IERC4906.sol";

contract UpdatableNFT is ERC721, IERC4906 {
    function updateMetadata(uint256 tokenId) external onlyOwner {
        emit MetadataUpdate(tokenId);
    }

    function updateAllMetadata() external onlyOwner {
        emit BatchMetadataUpdate(0, type(uint256).max);
    }
}
```

## Royalties (ERC-2981)

ERC-2981 defines a standard `royaltyInfo(tokenId, salePrice)` function that returns the royalty recipient and amount. Marketplaces query this but are NOT required to enforce it.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {ERC2981} from "@openzeppelin/contracts/token/common/ERC2981.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract RoyaltyNFT is ERC721, ERC2981, Ownable, ReentrancyGuard {
    uint256 private _nextTokenId;

    constructor(address initialOwner, address royaltyReceiver)
        ERC721("RoyaltyNFT", "RNFT")
        Ownable(initialOwner)
    {
        // 5% royalty (500 basis points) on all tokens by default
        _setDefaultRoyalty(royaltyReceiver, 500);
    }

    function mint(address to) external onlyOwner nonReentrant {
        _safeMint(to, _nextTokenId++);
    }

    /// @notice Override for specific token royalty
    function setTokenRoyalty(uint256 tokenId, address receiver, uint96 feeNumerator)
        external
        onlyOwner
    {
        _setTokenRoyalty(tokenId, receiver, feeNumerator);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC2981)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
```

## Common Minting Patterns

### Allowlist with Merkle Proof

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {MerkleProof} from "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract MerkleAllowlistNFT is ERC721, Ownable, ReentrancyGuard {
    uint256 private _nextTokenId;
    bytes32 public merkleRoot;
    mapping(address minter => bool claimed) public hasClaimed;

    error AlreadyClaimed();
    error InvalidProof();

    constructor(address initialOwner, bytes32 _merkleRoot)
        ERC721("AllowlistNFT", "ANFT")
        Ownable(initialOwner)
    {
        merkleRoot = _merkleRoot;
    }

    function allowlistMint(bytes32[] calldata proof) external nonReentrant {
        if (hasClaimed[msg.sender]) revert AlreadyClaimed();

        bytes32 leaf = keccak256(abi.encodePacked(msg.sender));
        if (!MerkleProof.verify(proof, merkleRoot, leaf)) revert InvalidProof();

        hasClaimed[msg.sender] = true;
        _safeMint(msg.sender, _nextTokenId++);
    }
}
```

### Allowlist with EIP-712 Signature (Nonce + Deadline)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {EIP712} from "@openzeppelin/contracts/utils/cryptography/EIP712.sol";
import {ECDSA} from "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/// @notice EIP-712 signed allowlist with per-address nonce and deadline to prevent replay
contract SignedAllowlistNFT is ERC721, EIP712, Ownable, ReentrancyGuard {
    using ECDSA for bytes32;

    uint256 private _nextTokenId;
    address public signer;
    mapping(address minter => uint256 nonce) public nonces;

    // EIP-712 domain includes contract address and chainId automatically via EIP712 base
    bytes32 private constant MINT_TYPEHASH =
        keccak256("Mint(address minter,uint256 nonce,uint256 deadline)");

    error InvalidSignature();
    error SignatureExpired();

    constructor(address initialOwner, address _signer)
        ERC721("SignedNFT", "SGNFT")
        EIP712("SignedAllowlistNFT", "1")
        Ownable(initialOwner)
    {
        signer = _signer;
    }

    function allowlistMint(uint256 deadline, bytes calldata signature) external nonReentrant {
        if (block.timestamp > deadline) revert SignatureExpired();

        uint256 currentNonce = nonces[msg.sender];

        bytes32 structHash = keccak256(
            abi.encode(MINT_TYPEHASH, msg.sender, currentNonce, deadline)
        );
        bytes32 digest = _hashTypedDataV4(structHash);
        address recovered = digest.recover(signature);

        if (recovered != signer) revert InvalidSignature();

        // Increment nonce BEFORE external call (_safeMint) -- CEI pattern
        nonces[msg.sender] = currentNonce + 1;
        _safeMint(msg.sender, _nextTokenId++);
    }
}
```

### Dutch Auction

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/// @notice Price decreases linearly from startPrice to endPrice over the auction duration
contract DutchAuctionNFT is ERC721, Ownable, ReentrancyGuard {
    uint256 private _nextTokenId;
    uint256 public constant MAX_SUPPLY = 10_000;

    uint256 public immutable auctionStart;
    uint256 public immutable auctionDuration;
    uint256 public immutable startPrice;
    uint256 public immutable endPrice;

    error AuctionNotStarted();
    error MaxSupplyReached();
    error InsufficientPayment();

    constructor(
        address initialOwner,
        uint256 _auctionStart,
        uint256 _auctionDuration,
        uint256 _startPrice,
        uint256 _endPrice
    )
        ERC721("DutchAuctionNFT", "DANFT")
        Ownable(initialOwner)
    {
        auctionStart = _auctionStart;
        auctionDuration = _auctionDuration;
        startPrice = _startPrice;
        endPrice = _endPrice;
    }

    function currentPrice() public view returns (uint256) {
        if (block.timestamp < auctionStart) revert AuctionNotStarted();
        uint256 elapsed = block.timestamp - auctionStart;
        if (elapsed >= auctionDuration) return endPrice;

        uint256 priceDrop = ((startPrice - endPrice) * elapsed) / auctionDuration;
        return startPrice - priceDrop;
    }

    function mint() external payable nonReentrant {
        uint256 price = currentPrice();
        if (msg.value < price) revert InsufficientPayment();
        uint256 tokenId = _nextTokenId++;
        if (tokenId >= MAX_SUPPLY) revert MaxSupplyReached();

        _safeMint(msg.sender, tokenId);

        uint256 refund = msg.value - price;
        if (refund > 0) {
            (bool sent, ) = payable(msg.sender).call{value: refund}("");
            require(sent);
        }
    }

    function withdraw() external onlyOwner {
        (bool sent, ) = payable(owner()).call{value: address(this).balance}("");
        require(sent);
    }
}
```

### Commit-Reveal for High-Value Mints

Prevents front-running and sniping by splitting mint into two transactions: commit (hash of intent) then reveal (actual mint after delay).

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/// @notice Two-phase mint: commit a hash, then reveal after a delay to prevent front-running
contract CommitRevealNFT is ERC721, Ownable, ReentrancyGuard {
    uint256 private _nextTokenId;
    uint256 public constant REVEAL_DELAY = 2;
    uint256 public constant REVEAL_WINDOW = 256;

    struct Commitment {
        uint64 blockNumber;
        bool revealed;
    }

    mapping(bytes32 commitHash => Commitment) public commitments;

    error CommitmentAlreadyExists();
    error CommitmentNotFound();
    error RevealTooEarly();
    error RevealWindowExpired();
    error AlreadyRevealed();

    constructor(address initialOwner)
        ERC721("CommitRevealNFT", "CRNFT")
        Ownable(initialOwner)
    {}

    /// @notice Phase 1: submit keccak256(abi.encodePacked(msg.sender, salt))
    function commit(bytes32 commitHash) external {
        if (commitments[commitHash].blockNumber != 0) revert CommitmentAlreadyExists();
        commitments[commitHash] = Commitment({
            blockNumber: uint64(block.number),
            revealed: false
        });
    }

    /// @notice Phase 2: reveal with original salt after REVEAL_DELAY blocks
    function reveal(bytes32 salt) external nonReentrant {
        bytes32 commitHash = keccak256(abi.encodePacked(msg.sender, salt));
        Commitment storage c = commitments[commitHash];

        if (c.blockNumber == 0) revert CommitmentNotFound();
        if (c.revealed) revert AlreadyRevealed();
        if (block.number < c.blockNumber + REVEAL_DELAY) revert RevealTooEarly();
        // blockhash only available for last 256 blocks
        if (block.number > c.blockNumber + REVEAL_WINDOW) revert RevealWindowExpired();

        c.revealed = true;
        _safeMint(msg.sender, _nextTokenId++);
    }
}
```

### Free Claim (One Per Address)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract FreeClaimNFT is ERC721, Ownable, ReentrancyGuard {
    uint256 private _nextTokenId;
    uint256 public constant MAX_SUPPLY = 5_000;
    bool public claimActive;

    mapping(address claimer => bool claimed) public hasClaimed;

    error ClaimNotActive();
    error AlreadyClaimed();
    error MaxSupplyReached();

    constructor(address initialOwner)
        ERC721("FreeClaimNFT", "FREE")
        Ownable(initialOwner)
    {}

    function setClaimActive(bool active) external onlyOwner {
        claimActive = active;
    }

    function claim() external nonReentrant {
        if (!claimActive) revert ClaimNotActive();
        if (hasClaimed[msg.sender]) revert AlreadyClaimed();
        uint256 tokenId = _nextTokenId++;
        if (tokenId >= MAX_SUPPLY) revert MaxSupplyReached();

        hasClaimed[msg.sender] = true;
        _safeMint(msg.sender, tokenId);
    }
}
```

## Marketplace Integration (Seaport 1.6)

> **Last verified:** March 2026

Seaport 1.6 is OpenSea's marketplace protocol, deployed at the same deterministic address on all EVM chains: `0x0000000000000068F116A894984e2DB1123eB395`.

### Approving Seaport

Before listing, the NFT owner must approve Seaport as an operator:

```solidity
nftContract.setApprovalForAll(0x0000000000000068F116A894984e2DB1123eB395, true);
```

### Creating a Listing (TypeScript with viem)

```typescript
import { createWalletClient, http, type Address } from "viem";
import { mainnet } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";

const SEAPORT = "0x0000000000000068F116A894984e2DB1123eB395" as const;

// Seaport order components -- ERC-721 listing for ETH
interface OrderParameters {
  offerer: Address;
  zone: Address;
  offer: Array<{
    itemType: number;    // 2 = ERC721, 3 = ERC1155
    token: Address;
    identifierOrCriteria: bigint;
    startAmount: bigint;
    endAmount: bigint;
  }>;
  consideration: Array<{
    itemType: number;    // 0 = ETH, 1 = ERC20
    token: Address;
    identifierOrCriteria: bigint;
    startAmount: bigint;
    endAmount: bigint;
    recipient: Address;
  }>;
  orderType: number;     // 0 = FULL_OPEN
  startTime: bigint;
  endTime: bigint;
  zoneHash: `0x${string}`;
  salt: bigint;
  conduitKey: `0x${string}`;
  totalOriginalConsiderationItems: bigint;
}
```

See `examples/marketplace-listing/` for a complete working example with order signing and fulfillment.

### Seaport Item Types

| Value | Type | Description |
|-------|------|-------------|
| 0 | NATIVE | ETH (or native token) |
| 1 | ERC20 | ERC-20 token |
| 2 | ERC721 | ERC-721 NFT |
| 3 | ERC1155 | ERC-1155 token |
| 4 | ERC721_WITH_CRITERIA | ERC-721 with trait-based criteria |
| 5 | ERC1155_WITH_CRITERIA | ERC-1155 with criteria |

## Security Checklist for NFT Contracts

- [ ] `ReentrancyGuard` on ALL mint functions (`_safeMint` makes external calls)
- [ ] Supply cap enforced with `require(tokenId < MAX_SUPPLY)` or equivalent
- [ ] Per-wallet mint limit to prevent single-wallet hoarding
- [ ] Commit-reveal for high-value mints to prevent front-running/sniping
- [ ] Metadata freeze function (`emit BatchMetadataUpdate` then disable further changes)
- [ ] Never use `tx.origin` for authorization -- always `msg.sender`
- [ ] EIP-712 domain separators on all signature-based allowlists
- [ ] Nonce tracking for signature-based mints to prevent replay
- [ ] Deadline/expiry on all signed messages
- [ ] `Ownable` with explicit initial owner (OZ v5 requires constructor arg)
- [ ] `supportsInterface` correctly overridden when combining ERC721 + ERC2981 + ERC4906
- [ ] Withdrawal function for ETH from paid mints (owner-only, pull pattern)
- [ ] No hardcoded royalty recipient if it needs to be updatable

## Related Skills

- **openzeppelin** -- contract library used for all implementations in this skill
- **solidity-security** -- comprehensive Solidity security patterns and audit checklist
- **eip-reference** -- detailed EIP specifications including ERC-721, ERC-1155, ERC-2981
- **foundry** -- testing and deployment framework for Solidity contracts
- **viem** -- TypeScript library for EVM interaction used in marketplace examples

## References

- [ERC-721: Non-Fungible Token Standard](https://eips.ethereum.org/EIPS/eip-721)
- [ERC-1155: Multi Token Standard](https://eips.ethereum.org/EIPS/eip-1155)
- [ERC-2981: NFT Royalty Standard](https://eips.ethereum.org/EIPS/eip-2981)
- [ERC-4906: EIP-721 Metadata Update Extension](https://eips.ethereum.org/EIPS/eip-4906)
- [ERC-6551: Non-fungible Token Bound Accounts](https://eips.ethereum.org/EIPS/eip-6551)
- [OpenZeppelin Contracts v5 Docs](https://docs.openzeppelin.com/contracts/5.x/)
- [OpenZeppelin v5 Migration Guide](https://docs.openzeppelin.com/contracts/5.x/upgradeable#migration)
- [Seaport Protocol Documentation](https://docs.opensea.io/reference/seaport-overview)
- [Seaport 1.6 Source (ProjectOpenSea)](https://github.com/ProjectOpenSea/seaport)
- [OpenSea Metadata Standards](https://docs.opensea.io/docs/metadata-standards)
- [Limit Break ERC-721C](https://github.com/limitbreakinc/creator-token-standards)
