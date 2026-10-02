---
name: ens
description: ENS (Ethereum Name Service) development — name resolution, registration via commit-reveal, text/address records, reverse resolution, avatar retrieval, subdomains, and Name Wrapper integration. Covers viem's built-in ENS actions, resolver patterns, CCIP-Read for offchain data, and contract interactions with the ENS registry on Ethereum mainnet.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: ethereum
  category: Infrastructure
tags:
  - ens
  - naming
  - resolution
  - identity
---

# ENS (Ethereum Name Service)

ENS maps human-readable names (alice.eth) to Ethereum addresses, content hashes, and arbitrary metadata. It is the identity layer for Ethereum — used for wallets, dApps, and onchain profiles. The architecture separates the registry (who owns a name) from resolvers (what data a name points to).

## What You Probably Got Wrong

- **ENS uses `namehash`, not plain strings** -- The registry and resolvers never see "alice.eth" as a string. Names are normalized (UTS-46), then hashed with the recursive `namehash` algorithm (EIP-137). If you pass a raw string to a contract call, it will not work. viem handles this automatically in its ENS actions but you must use `namehash()` and `labelhash()` for direct contract calls.
- **Registry vs Resolver vs Registrar -- three different contracts** -- The Registry tracks name ownership and which resolver to use. The Resolver stores records (address, text, contenthash). The Registrar handles `.eth` name registration and renewal. Confusing these is the most common ENS integration bug.
- **`.eth` registrar uses commit-reveal, not a single transaction** -- Registration requires two transactions separated by at least 60 seconds: first `commit(secret)`, wait, then `register(name, owner, duration, secret, ...)`. This prevents frontrunning. Skipping the wait or reusing a secret will revert.
- **Reverse resolution is opt-in** -- An address only has a "primary name" if the owner explicitly set it via the Reverse Registrar. Do not assume every address has a reverse record. Always handle `null` returns from `getEnsName()`.
- **Name Wrapper changes ownership semantics** -- Since 2023, ENS names can be "wrapped" as ERC-1155 tokens via the Name Wrapper contract. Wrapped names have fuses that permanently restrict operations (cannot unwrap, cannot set resolver, etc.). Check `isWrapped` before assuming standard ownership patterns.
- **CCIP-Read (ERC-3668) enables offchain resolution** -- Resolvers can return an `OffchainLookup` error that instructs the client to fetch data from an offchain gateway and verify it onchain. This powers offchain subdomains, L2 resolution, and gasless record updates. viem handles CCIP-Read automatically.
- **Wildcard resolution (ENSIP-10) is real** -- Resolvers can implement `resolve(bytes name, bytes data)` to handle any subdomain dynamically, even ones not explicitly registered. This is how services like cb.id and lens.xyz work.
- **ENS names expire** -- `.eth` names require annual renewal. Expired names enter a 90-day grace period, then a 21-day premium auction, then become available. Do not cache resolution results indefinitely.
- **`normalize()` before any ENS operation** -- Names must be UTS-46 normalized before hashing. "Alice.ETH" and "alice.eth" produce different hashes. viem normalizes automatically, but if you build raw calldata you must normalize first using `@adraffy/ens-normalize`.

## Quick Start

### Installation

```bash
npm install viem
```

viem has built-in ENS support -- no additional packages needed for resolution.

### Forward Resolution (Name to Address)

```typescript
import { createPublicClient, http } from "viem";
import { mainnet } from "viem/chains";

const client = createPublicClient({
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});

const address = await client.getEnsAddress({
  name: "vitalik.eth",
});
// "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
```

### Reverse Resolution (Address to Name)

```typescript
const name = await client.getEnsName({
  address: "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
});
// "vitalik.eth" (or null if no primary name set)
```

### Get Avatar

```typescript
const avatar = await client.getEnsAvatar({
  name: "vitalik.eth",
});
// HTTPS URL to avatar image, or null
```

## Name Resolution

### Forward Resolution with Coin Types

ENS can store addresses for any blockchain, not just Ethereum. Each chain has a SLIP-44 coin type.

```typescript
const ethAddress = await client.getEnsAddress({
  name: "vitalik.eth",
});

// BTC address (coin type 0)
const btcAddress = await client.getEnsAddress({
  name: "vitalik.eth",
  coinType: 0,
});

// Solana address (coin type 501)
const solAddress = await client.getEnsAddress({
  name: "vitalik.eth",
  coinType: 501,
});
```

### Text Records

ENS text records store arbitrary key-value metadata. Standard keys are defined in ENSIP-5.

```typescript
const twitter = await client.getEnsText({
  name: "vitalik.eth",
  key: "com.twitter",
});

const github = await client.getEnsText({
  name: "vitalik.eth",
  key: "com.github",
});

const email = await client.getEnsText({
  name: "vitalik.eth",
  key: "email",
});

const url = await client.getEnsText({
  name: "vitalik.eth",
  key: "url",
});

const description = await client.getEnsText({
  name: "vitalik.eth",
  key: "description",
});

// Avatar is also a text record (ENSIP-12 supports NFT references)
const avatarRecord = await client.getEnsText({
  name: "vitalik.eth",
  key: "avatar",
});
// Can be HTTPS URL, IPFS URI, or NFT reference like
// "eip155:1/erc721:0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d/1234"
```

#### Standard Text Record Keys

| Key | Description |
|-----|-------------|
| `email` | Email address |
| `url` | Website URL |
| `avatar` | Avatar image (HTTPS, IPFS, or NFT reference) |
| `description` | Short bio |
| `display` | Display name (may differ from ENS name) |
| `com.twitter` | Twitter/X handle |
| `com.github` | GitHub username |
| `com.discord` | Discord username |
| `org.telegram` | Telegram handle |
| `notice` | Contract notice text |
| `keywords` | Comma-separated keywords |
| `header` | Profile header/banner image |

### Content Hash

```typescript
import { createPublicClient, http, parseAbi } from "viem";
import { mainnet } from "viem/chains";
import { namehash } from "viem/ens";

const client = createPublicClient({
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});

const RESOLVER_ABI = parseAbi([
  "function contenthash(bytes32 node) view returns (bytes)",
]);

const node = namehash("vitalik.eth");

// First get the resolver address
const resolverAddress = await client.getEnsResolver({
  name: "vitalik.eth",
});

const contenthash = await client.readContract({
  address: resolverAddress,
  abi: RESOLVER_ABI,
  functionName: "contenthash",
  args: [node],
});
// Encoded content hash (IPFS, Swarm, Arweave, etc.)
```

### Batch Resolution with Multicall

```typescript
import { createPublicClient, http, parseAbi } from "viem";
import { mainnet } from "viem/chains";
import { namehash } from "viem/ens";

const client = createPublicClient({
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});

const RESOLVER_ABI = parseAbi([
  "function addr(bytes32 node) view returns (address)",
  "function text(bytes32 node, string key) view returns (string)",
]);

const node = namehash("vitalik.eth");

const resolverAddress = await client.getEnsResolver({
  name: "vitalik.eth",
});

const results = await client.multicall({
  contracts: [
    {
      address: resolverAddress,
      abi: RESOLVER_ABI,
      functionName: "addr",
      args: [node],
    },
    {
      address: resolverAddress,
      abi: RESOLVER_ABI,
      functionName: "text",
      args: [node, "com.twitter"],
    },
    {
      address: resolverAddress,
      abi: RESOLVER_ABI,
      functionName: "text",
      args: [node, "com.github"],
    },
    {
      address: resolverAddress,
      abi: RESOLVER_ABI,
      functionName: "text",
      args: [node, "url"],
    },
  ],
});

const [addr, twitter, github, url] = results.map((r) => r.result);
```

## Registration

### Commit-Reveal Process

ENS `.eth` registration uses a two-step commit-reveal to prevent frontrunning. You must wait at least 60 seconds between commit and register.

```typescript
import {
  createPublicClient,
  createWalletClient,
  http,
  parseAbi,
  encodePacked,
  keccak256,
  parseEther,
} from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { mainnet } from "viem/chains";

const ETH_REGISTRAR_CONTROLLER =
  "0x253553366Da8546fC250F225fe3d25d0C782303b" as const;

const CONTROLLER_ABI = parseAbi([
  "function rentPrice(string name, uint256 duration) view returns (tuple(uint256 base, uint256 premium))",
  "function available(string name) view returns (bool)",
  "function makeCommitment(string name, address owner, uint256 duration, bytes32 secret, address resolver, bytes[] data, bool reverseRecord, uint16 ownerControlledFuses) pure returns (bytes32)",
  "function commit(bytes32 commitment) external",
  "function register(string name, address owner, uint256 duration, bytes32 secret, address resolver, bytes[] data, bool reverseRecord, uint16 ownerControlledFuses) payable",
]);

const PUBLIC_RESOLVER = "0x231b0Ee14048e9dCcD1d247744d114a4EB5E8E63" as const;

const account = privateKeyToAccount(
  process.env.PRIVATE_KEY as `0x${string}`
);

const client = createPublicClient({
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});

const walletClient = createWalletClient({
  account,
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});

async function registerName(label: string, durationSeconds: bigint) {
  // 1. Check availability
  const isAvailable = await client.readContract({
    address: ETH_REGISTRAR_CONTROLLER,
    abi: CONTROLLER_ABI,
    functionName: "available",
    args: [label],
  });
  if (!isAvailable) throw new Error(`${label}.eth is not available`);

  // 2. Get price
  const rentPrice = await client.readContract({
    address: ETH_REGISTRAR_CONTROLLER,
    abi: CONTROLLER_ABI,
    functionName: "rentPrice",
    args: [label, durationSeconds],
  });
  // Add 10% buffer for price fluctuation during commit-reveal wait
  const totalPrice =
    ((rentPrice.base + rentPrice.premium) * 110n) / 100n;

  // 3. Generate secret (random 32 bytes)
  const secret = keccak256(
    encodePacked(["address", "uint256"], [account.address, BigInt(Date.now())])
  );

  // 4. Create commitment
  const commitment = await client.readContract({
    address: ETH_REGISTRAR_CONTROLLER,
    abi: CONTROLLER_ABI,
    functionName: "makeCommitment",
    args: [
      label,
      account.address,
      durationSeconds,
      secret,
      PUBLIC_RESOLVER,
      [],              // data (encoded resolver calls to set records at registration)
      true,            // reverseRecord (set as primary name)
      0,               // ownerControlledFuses (0 = no fuses)
    ],
  });

  // 5. Submit commitment
  const commitHash = await walletClient.writeContract({
    address: ETH_REGISTRAR_CONTROLLER,
    abi: CONTROLLER_ABI,
    functionName: "commit",
    args: [commitment],
  });
  await client.waitForTransactionReceipt({ hash: commitHash });
  console.log("Commitment submitted. Waiting 60 seconds...");

  // 6. Wait at least 60 seconds (minCommitmentAge)
  await new Promise((resolve) => setTimeout(resolve, 65_000));

  // 7. Register
  const registerHash = await walletClient.writeContract({
    address: ETH_REGISTRAR_CONTROLLER,
    abi: CONTROLLER_ABI,
    functionName: "register",
    args: [
      label,
      account.address,
      durationSeconds,
      secret,
      PUBLIC_RESOLVER,
      [],
      true,
      0,
    ],
    value: totalPrice,
  });
  const receipt = await client.waitForTransactionReceipt({
    hash: registerHash,
  });

  if (receipt.status !== "success") {
    throw new Error("Registration transaction reverted");
  }

  console.log(`Registered ${label}.eth for ${durationSeconds / 31536000n} year(s)`);
  return receipt;
}

// Register for 1 year (365 days in seconds)
await registerName("myname", 31536000n);
```

### Renewal

```typescript
const CONTROLLER_ABI_RENEW = parseAbi([
  "function rentPrice(string name, uint256 duration) view returns (tuple(uint256 base, uint256 premium))",
  "function renew(string name, uint256 duration) payable",
]);

async function renewName(label: string, durationSeconds: bigint) {
  const rentPrice = await client.readContract({
    address: ETH_REGISTRAR_CONTROLLER,
    abi: CONTROLLER_ABI_RENEW,
    functionName: "rentPrice",
    args: [label, durationSeconds],
  });
  // 5% buffer for price changes
  const totalPrice = ((rentPrice.base + rentPrice.premium) * 105n) / 100n;

  const hash = await walletClient.writeContract({
    address: ETH_REGISTRAR_CONTROLLER,
    abi: CONTROLLER_ABI_RENEW,
    functionName: "renew",
    args: [label, durationSeconds],
    value: totalPrice,
  });
  const receipt = await client.waitForTransactionReceipt({ hash });

  if (receipt.status !== "success") {
    throw new Error("Renewal transaction reverted");
  }

  console.log(`Renewed ${label}.eth for ${durationSeconds / 31536000n} year(s)`);
  return receipt;
}
```

### Check Price Before Registering

```typescript
async function getRegistrationCost(
  label: string,
  durationSeconds: bigint
): Promise<{ base: bigint; premium: bigint; total: bigint }> {
  const rentPrice = await client.readContract({
    address: ETH_REGISTRAR_CONTROLLER,
    abi: CONTROLLER_ABI,
    functionName: "rentPrice",
    args: [label, durationSeconds],
  });
  return {
    base: rentPrice.base,
    premium: rentPrice.premium,
    total: rentPrice.base + rentPrice.premium,
  };
}
```

## Working with Resolvers

### Setting Text Records

```typescript
import {
  createPublicClient,
  createWalletClient,
  http,
  parseAbi,
} from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { mainnet } from "viem/chains";
import { namehash } from "viem/ens";

const PUBLIC_RESOLVER = "0x231b0Ee14048e9dCcD1d247744d114a4EB5E8E63" as const;

const RESOLVER_ABI = parseAbi([
  "function setText(bytes32 node, string key, string value) external",
  "function setAddr(bytes32 node, address addr) external",
  "function setAddr(bytes32 node, uint256 coinType, bytes value) external",
  "function setContenthash(bytes32 node, bytes hash) external",
  "function multicall(bytes[] data) external returns (bytes[])",
]);

const account = privateKeyToAccount(
  process.env.PRIVATE_KEY as `0x${string}`
);

const client = createPublicClient({
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});

const walletClient = createWalletClient({
  account,
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});

const node = namehash("myname.eth");

// Set a single text record
const hash = await walletClient.writeContract({
  address: PUBLIC_RESOLVER,
  abi: RESOLVER_ABI,
  functionName: "setText",
  args: [node, "com.twitter", "myhandle"],
});
await client.waitForTransactionReceipt({ hash });
```

### Batch Update Records with Multicall

Setting multiple records in a single transaction using the resolver's built-in multicall.

```typescript
import { encodeFunctionData } from "viem";

const node = namehash("myname.eth");

const calls = [
  encodeFunctionData({
    abi: RESOLVER_ABI,
    functionName: "setText",
    args: [node, "com.twitter", "myhandle"],
  }),
  encodeFunctionData({
    abi: RESOLVER_ABI,
    functionName: "setText",
    args: [node, "com.github", "mygithub"],
  }),
  encodeFunctionData({
    abi: RESOLVER_ABI,
    functionName: "setText",
    args: [node, "url", "https://mysite.com"],
  }),
  encodeFunctionData({
    abi: RESOLVER_ABI,
    functionName: "setText",
    args: [node, "email", "me@mysite.com"],
  }),
  encodeFunctionData({
    abi: RESOLVER_ABI,
    functionName: "setText",
    args: [node, "avatar", "https://mysite.com/avatar.png"],
  }),
];

const hash = await walletClient.writeContract({
  address: PUBLIC_RESOLVER,
  abi: RESOLVER_ABI,
  functionName: "multicall",
  args: [calls],
});
const receipt = await client.waitForTransactionReceipt({ hash });

if (receipt.status !== "success") {
  throw new Error("Multicall record update reverted");
}
```

### Setting the Primary Name (Reverse Record)

```typescript
const REVERSE_REGISTRAR = "0xa58E81fe9b61B5c3fE2AFD33CF304c454AbFc7Cb" as const;

const REVERSE_ABI = parseAbi([
  "function setName(string name) external returns (bytes32)",
]);

const hash = await walletClient.writeContract({
  address: REVERSE_REGISTRAR,
  abi: REVERSE_ABI,
  functionName: "setName",
  args: ["myname.eth"],
});
await client.waitForTransactionReceipt({ hash });
```

## Subdomains

### Creating an Onchain Subdomain

```typescript
import { parseAbi } from "viem";
import { namehash, labelhash } from "viem/ens";

const ENS_REGISTRY = "0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e" as const;

const REGISTRY_ABI = parseAbi([
  "function setSubnodeRecord(bytes32 node, bytes32 label, address owner, address resolver, uint64 ttl) external",
  "function owner(bytes32 node) view returns (address)",
  "function resolver(bytes32 node) view returns (address)",
]);

const parentNode = namehash("myname.eth");
const subLabel = labelhash("sub");

const hash = await walletClient.writeContract({
  address: ENS_REGISTRY,
  abi: REGISTRY_ABI,
  functionName: "setSubnodeRecord",
  args: [
    parentNode,
    subLabel,
    account.address,       // owner of sub.myname.eth
    PUBLIC_RESOLVER,       // resolver
    0n,                    // TTL
  ],
});
await client.waitForTransactionReceipt({ hash });
// sub.myname.eth now exists and points to PUBLIC_RESOLVER
```

### Offchain Subdomains (CCIP-Read / ERC-3668)

Offchain subdomains let you issue unlimited subdomains without gas costs. The resolver responds with an `OffchainLookup` error that directs the client to a gateway URL. The gateway returns signed data that is verified onchain.

This is how services like cb.id (Coinbase), uni.eth (Uniswap), and lens.xyz work.

For offchain resolution, viem handles CCIP-Read transparently -- no client-side changes needed:

```typescript
// Resolving an offchain subdomain works identically to onchain names
const address = await client.getEnsAddress({
  name: "myuser.cb.id",
});
// viem automatically:
// 1. Calls resolver.resolve(...)
// 2. Catches OffchainLookup revert
// 3. Fetches from the gateway URL
// 4. Calls resolver with the gateway proof
// 5. Returns the verified address

const avatar = await client.getEnsAvatar({
  name: "myuser.cb.id",
});
```

To build your own offchain resolver, implement ERC-3668:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IExtendedResolver} from "@ensdomains/ens-contracts/contracts/resolvers/profiles/IExtendedResolver.sol";

/// @notice Offchain resolver that delegates lookups to a gateway
/// @dev Implements ERC-3668 (CCIP-Read) and ENSIP-10 (wildcard resolution)
contract OffchainResolver is IExtendedResolver {
    string public url;
    address public signer;

    error OffchainLookup(
        address sender,
        string[] urls,
        bytes callData,
        bytes4 callbackFunction,
        bytes extraData
    );

    constructor(string memory _url, address _signer) {
        url = _url;
        signer = _signer;
    }

    /// @notice ENSIP-10 wildcard resolve entry point
    function resolve(
        bytes calldata name,
        bytes calldata data
    ) external view returns (bytes memory) {
        string[] memory urls = new string[](1);
        urls[0] = url;

        revert OffchainLookup(
            address(this),
            urls,
            data,
            this.resolveWithProof.selector,
            abi.encode(name, data)
        );
    }

    /// @notice Callback that verifies the gateway signature
    function resolveWithProof(
        bytes calldata response,
        bytes calldata extraData
    ) external view returns (bytes memory) {
        // Verify signature from gateway matches expected signer
        // Return decoded result
        // Implementation depends on your signing scheme
    }
}
```

## Contract Addresses

Ethereum Mainnet. Last verified: 2025-03-01.

| Contract | Address | Purpose |
|----------|---------|---------|
| ENS Registry | `0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e` | Core registry -- maps names to owners and resolvers |
| Public Resolver | `0x231b0Ee14048e9dCcD1d247744d114a4EB5E8E63` | Default resolver for address, text, contenthash, and ABI records |
| ETH Registrar Controller | `0x253553366Da8546fC250F225fe3d25d0C782303b` | Handles .eth name registration and renewal (commit-reveal) |
| Name Wrapper | `0xD4416b13d2b3a9aBae7AcD5D6C2BbDBE25686401` | Wraps names as ERC-1155 tokens with permission fuses |
| Reverse Registrar | `0xa58E81fe9b61B5c3fE2AFD33CF304c454AbFc7Cb` | Manages reverse records (address-to-name mapping) |
| Base Registrar (NFT) | `0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85` | ERC-721 NFT for .eth second-level names |
| Universal Resolver | `0xce01f8eee7E30F8E3BfC1C22bCBc01faBc8680E4` | Batch resolution with CCIP-Read support |

### Address Constants for TypeScript

```typescript
const ENS_ADDRESSES = {
  registry: "0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e",
  publicResolver: "0x231b0Ee14048e9dCcD1d247744d114a4EB5E8E63",
  ethRegistrarController: "0x253553366Da8546fC250F225fe3d25d0C782303b",
  nameWrapper: "0xD4416b13d2b3a9aBae7AcD5D6C2BbDBE25686401",
  reverseRegistrar: "0xa58E81fe9b61B5c3fE2AFD33CF304c454AbFc7Cb",
  baseRegistrar: "0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85",
  universalResolver: "0xce01f8eee7E30F8E3BfC1C22bCBc01faBc8680E4",
} as const satisfies Record<string, `0x${string}`>;
```

### Sepolia Testnet

Last verified: 2025-03-01.

| Contract | Address |
|----------|---------|
| ENS Registry | `0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e` |
| Public Resolver | `0x8FADE66B79cC9f707aB26799354482EB93a5B7dD` |
| ETH Registrar Controller | `0xFED6a969AaA60E4961FCD3EBF1A2e8913DeBe6c7` |
| Name Wrapper | `0x0635513f179D50A207757E05759CbD106d7dFcE8` |
| Reverse Registrar | `0xA0a1AbcDAe1a2a4A2EF8e9113Ff0e02DD81DC0C6` |

## Error Handling

### Common Resolution Errors

```typescript
async function safeResolve(name: string) {
  try {
    const address = await client.getEnsAddress({ name });
    if (!address) {
      console.log(`${name} has no address record set`);
      return null;
    }
    return address;
  } catch (error) {
    if (error instanceof Error) {
      // Name does not exist or is malformed
      if (error.message.includes("Could not find resolver")) {
        console.log(`${name} is not registered or has no resolver`);
        return null;
      }
      // CCIP-Read gateway failure
      if (error.message.includes("OffchainLookup")) {
        console.log(`Offchain resolution failed for ${name}`);
        return null;
      }
    }
    throw error;
  }
}
```

### Common Registration Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `CommitmentTooNew` | Called `register()` less than 60s after `commit()` | Wait at least 60 seconds between commit and register |
| `CommitmentTooOld` | Commitment expired (older than 24 hours) | Submit a new commitment |
| `NameNotAvailable` | Name is registered or in grace period | Check `available()` first |
| `DurationTooShort` | Duration under minimum (28 days) | Use at least 2419200 seconds |
| `InsufficientValue` | Sent less ETH than `rentPrice()` requires | Add a 5-10% buffer to `rentPrice()` result |
| `Unauthorised` | Caller is not the name owner | Verify ownership via registry before writing records |

### Validating ENS Names

```typescript
import { normalize } from "viem/ens";

function isValidEnsName(name: string): boolean {
  try {
    normalize(name);
    return true;
  } catch {
    return false;
  }
}

// normalize() throws on invalid names
// Valid: "alice.eth", "sub.alice.eth", "alice.xyz"
// Invalid: names with zero-width characters, confusable Unicode, etc.
```

## Key Constants

| Constant | Value | Notes |
|----------|-------|-------|
| Min commitment age | 60 seconds | Wait between commit and register |
| Max commitment age | 86400 seconds (24h) | Commitment expires after this |
| Min registration duration | 2419200 seconds (28 days) | Shortest allowed registration |
| Grace period | 90 days | After expiry, owner can still renew |
| Premium auction | 21 days | After grace period, decaying price auction |
| Namehash of `eth` | `0x93cdeb708b7545dc668eb9280176169d1c33cfd8ed6f04690a0bcc88a93fc4ae` | Used as parent node for .eth names |

## References

- [ENS Documentation](https://docs.ens.domains/) -- official docs covering architecture, resolution, registration, and CCIP-Read
- [EIP-137: ENS](https://eips.ethereum.org/EIPS/eip-137) -- core ENS specification (registry, namehash, resolvers)
- [EIP-181: Reverse Resolution](https://eips.ethereum.org/EIPS/eip-181) -- reverse registrar and addr.reverse namespace
- [EIP-2304: Multichain Address Resolution](https://eips.ethereum.org/EIPS/eip-2304) -- SLIP-44 coin type support in resolvers
- [ERC-3668: CCIP-Read](https://eips.ethereum.org/EIPS/eip-3668) -- offchain data retrieval standard
- [ENSIP-5: Text Records](https://docs.ens.domains/ensip/5) -- standardized text record keys
- [ENSIP-10: Wildcard Resolution](https://docs.ens.domains/ensip/10) -- dynamic subdomain resolution
- [ENSIP-12: Avatar Text Records](https://docs.ens.domains/ensip/12) -- NFT and IPFS avatar specification
- [ENS Deployments](https://docs.ens.domains/learn/deployments) -- official contract addresses per network
- [viem ENS Actions](https://viem.sh/docs/ens/getting-started) -- built-in ENS resolution in viem
- [@adraffy/ens-normalize](https://github.com/adraffy/ens-normalize.js) -- reference UTS-46 normalization library used by viem
