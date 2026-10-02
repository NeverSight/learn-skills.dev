---
name: openzeppelin
description: OpenZeppelin Contracts v5 for building secure smart contracts. Covers ERC-20/721/1155 tokens, access control (Ownable, AccessControl, AccessManager), security utilities (ReentrancyGuard, Pausable, SafeERC20), upgradeable contracts (UUPS, Initializable), and Defender integration. Use when writing Solidity contracts that need battle-tested, audited building blocks.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: Infrastructure
tags:
  - openzeppelin
  - contracts
  - erc20
  - erc721
  - upgrades
  - access-control
---

# OpenZeppelin Contracts

OpenZeppelin Contracts is the standard library for secure smart contract development. Used by Uniswap, Aave, Compound, and most production Solidity projects. The library provides audited, modular building blocks for tokens, access control, security patterns, upgradeability, and governance.

## What You Probably Got Wrong

> OZ v5 shipped breaking changes in late 2023. Most LLM training data reflects v4. Every item below will cause compilation failures if you use the old pattern.

- **Ownable requires a constructor argument** -- `Ownable` no longer has a default owner. You MUST pass the initial owner address: `Ownable(initialOwner)`. Omitting this is the #1 compilation error.
- **Import paths changed** -- v5 uses `@openzeppelin/contracts/token/ERC20/ERC20.sol`, not `@openzeppelin/contracts/ERC20.sol`. Some nested paths also changed. Always import from the full canonical path.
- **`_setupRole` is removed** -- Use `_grantRole(role, account)` in the constructor instead. `_setupRole` does not exist in v5.
- **`_safeMint` internal visibility** -- `_safeMint` is still internal but the override pattern changed. Override `_update` instead of `_beforeTokenTransfer` / `_afterTokenTransfer`.
- **Hook functions renamed** -- `_beforeTokenTransfer` and `_afterTokenTransfer` are gone. Override `_update(from, to, value)` for ERC-20 and `_update(to, tokenId, auth)` for ERC-721.
- **ERC-721 Enumerable override** -- v5 requires overriding `_increaseBalance` in addition to `_update` when combining ERC721Enumerable with other extensions.
- **`SafeMath` is removed** -- Solidity 0.8+ has built-in overflow checks. `SafeMath` was deleted from v5 entirely.
- **`Counters` is removed** -- Use plain `uint256` with `++` instead. The `Counters` library was removed for being unnecessary abstraction.
- **`AccessControl.renounceRole` requires `callerConfirmation`** -- In v5, `renounceRole(role, callerConfirmation)` takes a second parameter to prevent accidental renouncement.

## Quick Start

### Installation

```bash
# Foundry
forge install OpenZeppelin/openzeppelin-contracts

# Hardhat / npm
npm install @openzeppelin/contracts

# Upgradeable variant
npm install @openzeppelin/contracts-upgradeable
```

### Foundry Remappings

```
# remappings.txt
@openzeppelin/contracts/=lib/openzeppelin-contracts/contracts/
```

### Minimum Viable Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MyToken is ERC20 {
    constructor() ERC20("MyToken", "MTK") {
        _mint(msg.sender, 1_000_000 * 10 ** decimals());
    }
}
```

## Token Standards

### ERC-20 with Extensions

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC20Burnable} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import {ERC20Permit} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";
import {ERC20Votes} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Votes.sol";
import {Nonces} from "@openzeppelin/contracts/utils/Nonces.sol";

/// @notice Governance token with gasless approvals (EIP-2612) and vote delegation (EIP-5805).
contract GovernanceToken is ERC20, ERC20Burnable, ERC20Permit, ERC20Votes {
    constructor(address initialHolder)
        ERC20("GovernanceToken", "GOV")
        ERC20Permit("GovernanceToken")
    {
        _mint(initialHolder, 10_000_000 * 10 ** decimals());
    }

    // v5 override resolution: ERC20Votes needs _update, Nonces is shared between Permit and Votes
    function _update(address from, address to, uint256 value)
        internal
        override(ERC20, ERC20Votes)
    {
        super._update(from, to, value);
    }

    function nonces(address owner)
        public
        view
        override(ERC20Permit, Nonces)
        returns (uint256)
    {
        return super.nonces(owner);
    }
}
```

### ERC-721 with Extensions

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {ERC721Enumerable} from "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import {ERC721URIStorage} from "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract GameNFT is ERC721, ERC721Enumerable, ERC721URIStorage, Ownable {
    uint256 private _nextTokenId;

    constructor(address initialOwner)
        ERC721("GameNFT", "GNFT")
        Ownable(initialOwner)
    {}

    function safeMint(address to, string calldata uri) external onlyOwner returns (uint256) {
        uint256 tokenId = _nextTokenId++;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
        return tokenId;
    }

    // v5 requires both _update and _increaseBalance overrides for Enumerable
    function _update(address to, uint256 tokenId, address auth)
        internal
        override(ERC721, ERC721Enumerable)
        returns (address)
    {
        return super._update(to, tokenId, auth);
    }

    function _increaseBalance(address account, uint128 value)
        internal
        override(ERC721, ERC721Enumerable)
    {
        super._increaseBalance(account, value);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable, ERC721URIStorage)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
```

### ERC-1155 Multi-Token

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ERC1155} from "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract GameItems is ERC1155, Ownable {
    uint256 public constant GOLD = 0;
    uint256 public constant SILVER = 1;
    uint256 public constant SWORD = 2;

    constructor(address initialOwner)
        ERC1155("https://game.example/api/item/{id}.json")
        Ownable(initialOwner)
    {
        _mint(initialOwner, GOLD, 10 ** 18, "");
        _mint(initialOwner, SILVER, 10 ** 27, "");
        _mint(initialOwner, SWORD, 1, "");
    }

    function mint(address to, uint256 id, uint256 amount, bytes calldata data) external onlyOwner {
        _mint(to, id, amount, data);
    }

    function mintBatch(address to, uint256[] calldata ids, uint256[] calldata amounts, bytes calldata data)
        external
        onlyOwner
    {
        _mintBatch(to, ids, amounts, data);
    }
}
```

## Access Control

### Ownable (Single Admin)

Simplest model: one address has admin privileges. Good for token contracts and simple protocols.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract Vault is Ownable {
    // v5: MUST pass initial owner to constructor
    constructor(address initialOwner) Ownable(initialOwner) {}

    function withdraw() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }

    // Two-step ownership transfer (built into v5 via Ownable2Step)
}
```

For two-step transfers (prevents transferring to a wrong address):

```solidity
import {Ownable2Step, Ownable} from "@openzeppelin/contracts/access/Ownable2Step.sol";

contract SafeVault is Ownable2Step {
    constructor(address initialOwner) Ownable(initialOwner) {}
}
// New owner must call acceptOwnership() to complete the transfer
```

### AccessControl (Role-Based)

Multiple roles with independent permissions. Each role has an admin role that can grant/revoke it.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";

contract Treasury is AccessControl {
    bytes32 public constant TREASURER_ROLE = keccak256("TREASURER_ROLE");
    bytes32 public constant AUDITOR_ROLE = keccak256("AUDITOR_ROLE");

    event Withdrawal(address indexed to, uint256 amount);

    constructor(address admin) {
        // v5: use _grantRole in constructor (not _setupRole, which is removed)
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
        _grantRole(TREASURER_ROLE, admin);
    }

    function withdraw(address payable to, uint256 amount) external onlyRole(TREASURER_ROLE) {
        emit Withdrawal(to, amount);
        to.transfer(amount);
    }

    // v5: renounceRole requires callerConfirmation to prevent accidents
    // renounceRole(TREASURER_ROLE, msg.sender)
}
```

### AccessManager (v5 Centralized Permission Hub)

New in v5. A single contract that manages permissions across your entire protocol. Contracts delegate their access checks to the AccessManager rather than storing roles internally.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {AccessManaged} from "@openzeppelin/contracts/access/manager/AccessManaged.sol";

/// @notice Any contract that delegates auth to AccessManager.
contract ManagedVault is AccessManaged {
    constructor(address manager) AccessManaged(manager) {}

    // restricted modifier checks with the AccessManager
    function withdraw() external restricted {
        payable(msg.sender).transfer(address(this).balance);
    }
}
```

AccessManager setup (done off-chain or in a deploy script):

```solidity
import {AccessManager} from "@openzeppelin/contracts/access/manager/AccessManager.sol";

// In deploy script:
// 1. Deploy AccessManager with initial admin
// AccessManager manager = new AccessManager(adminAddress);
//
// 2. Label a role
// uint64 WITHDRAWER_ROLE = 1; // role IDs are uint64, 0 is ADMIN_ROLE
//
// 3. Grant role to an address
// manager.grantRole(WITHDRAWER_ROLE, withdrawerAddress, 0); // 0 = no grant delay
//
// 4. Set which role can call which function on the target
// bytes4[] memory selectors = new bytes4[](1);
// selectors[0] = ManagedVault.withdraw.selector;
// manager.setTargetFunctionRole(address(vault), selectors, WITHDRAWER_ROLE);
```

## Security Utilities

### ReentrancyGuard

Prevents reentrant calls to state-changing functions. Apply to any function that makes external calls after state changes.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract LendingPool is ReentrancyGuard {
    mapping(address => uint256) public balances;

    function withdraw(uint256 amount) external nonReentrant {
        // CEI: Checks-Effects-Interactions
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);
    }
}
```

### SafeERC20

Wraps ERC-20 calls to handle tokens that don't return `bool` (like USDT) and tokens that return `false` on failure.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract PaymentSplitter {
    using SafeERC20 for IERC20;

    function collectPayment(IERC20 token, address from, uint256 amount) external {
        // safeTransferFrom reverts on failure and handles non-standard return values
        token.safeTransferFrom(from, address(this), amount);
    }

    function distribute(IERC20 token, address to, uint256 amount) external {
        token.safeTransfer(to, amount);
    }

    function approveSpender(IERC20 token, address spender, uint256 amount) external {
        // forceApprove handles tokens that require approval to be set to 0 first (USDT)
        token.forceApprove(spender, amount);
    }
}
```

### Pausable

Emergency stop mechanism. Commonly used to freeze a protocol during an exploit.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Pausable} from "@openzeppelin/contracts/utils/Pausable.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract Exchange is Ownable, Pausable {
    constructor(address initialOwner) Ownable(initialOwner) {}

    function swap(address tokenIn, address tokenOut, uint256 amount) external whenNotPaused {
        // swap logic only executes when not paused
    }

    function pause() external onlyOwner {
        _pause();
    }

    function unpause() external onlyOwner {
        _unpause();
    }
}
```

### Address Utilities

```solidity
import {Address} from "@openzeppelin/contracts/utils/Address.sol";

contract Sender {
    using Address for address payable;

    function sendETH(address payable to, uint256 amount) external {
        // sendValue reverts if the transfer fails (unlike .transfer which has 2300 gas limit issues)
        to.sendValue(amount);
    }
}
```

## Upgradeable Contracts

### UUPS Pattern

UUPS (Universal Upgradeable Proxy Standard, EIP-1822) places the upgrade logic in the implementation contract. This is the recommended pattern in OZ v5 -- TransparentProxy is still available but UUPS is lighter on gas.

**Install the upgradeable package:**

```bash
npm install @openzeppelin/contracts-upgradeable
```

**Implementation contract:**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Initializable} from "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import {UUPSUpgradeable} from "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import {OwnableUpgradeable} from "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";

contract VaultV1 is Initializable, UUPSUpgradeable, OwnableUpgradeable {
    uint256 public totalDeposits;

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    function initialize(address initialOwner) public initializer {
        __Ownable_init(initialOwner);
        __UUPSUpgradeable_init();
    }

    function deposit() external payable {
        totalDeposits += msg.value;
    }

    // Only owner can authorize upgrades
    function _authorizeUpgrade(address newImplementation) internal override onlyOwner {}
}
```

**Deploy with Foundry:**

```solidity
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";

// In deploy script:
// 1. Deploy implementation
// VaultV1 impl = new VaultV1();
//
// 2. Encode initializer call
// bytes memory data = abi.encodeCall(VaultV1.initialize, (adminAddress));
//
// 3. Deploy proxy pointing to implementation
// ERC1967Proxy proxy = new ERC1967Proxy(address(impl), data);
//
// 4. Interact through proxy
// VaultV1 vault = VaultV1(address(proxy));
```

**Upgrade to V2:**

```solidity
contract VaultV2 is Initializable, UUPSUpgradeable, OwnableUpgradeable {
    uint256 public totalDeposits;
    uint256 public withdrawalFee; // New state variable -- append only, never reorder

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    function initialize(address initialOwner) public initializer {
        __Ownable_init(initialOwner);
        __UUPSUpgradeable_init();
    }

    // New initializer for the upgrade (reinitializer(2) for second version)
    function initializeV2(uint256 fee) public reinitializer(2) {
        withdrawalFee = fee;
    }

    function deposit() external payable {
        totalDeposits += msg.value;
    }

    function _authorizeUpgrade(address newImplementation) internal override onlyOwner {}
}

// Upgrade call:
// VaultV1(proxy).upgradeToAndCall(address(newImpl), abi.encodeCall(VaultV2.initializeV2, (100)));
```

### Upgrade Safety Rules

1. **Never reorder or remove existing state variables** -- only append new ones at the end.
2. **Use `_disableInitializers()` in the constructor** of every implementation contract.
3. **Use `reinitializer(n)` for version-specific init** -- not `initializer` (which can only run once).
4. **No immutable variables that depend on constructor args** in upgradeable contracts (the proxy won't have them).
5. **Storage gaps** -- v5 uses namespaced storage (ERC-7201) instead of `__gap` arrays. If extending OZ upgradeable contracts, the gaps are handled internally.

## Defender Integration

OpenZeppelin Defender provides operational security for deployed contracts: monitoring, automated actions, and secure transaction execution.

### Key Components

| Component | Purpose |
|-----------|---------|
| **Monitor** | Watch on-chain events and trigger alerts |
| **Actions** | Serverless functions that run in response to triggers |
| **Relayers** | Managed EOAs for sending transactions (no key management) |
| **Transaction Proposals** | Multisig-compatible tx submission (Safe, Governor) |
| **Deploy** | Deploy and verify contracts with upgrade safety checks |

### Deploy + Upgrade via Defender

```bash
npm install @openzeppelin/defender-sdk
```

```typescript
import { Defender } from "@openzeppelin/defender-sdk";

const client = new Defender({
  apiKey: process.env.DEFENDER_API_KEY,
  apiSecret: process.env.DEFENDER_API_SECRET,
});

// Propose an upgrade through a multisig
const proposal = await client.upgrade.proposeUpgrade({
  contract: { address: "0xPROXY", network: "mainnet" },
  newImplementation: "0xNEW_IMPL",
  via: "0xMULTISIG", // Safe address
  viaType: "Gnosis Safe",
});
```

### Monitor Setup

```typescript
const monitor = await client.monitor.create({
  type: "BLOCK",
  name: "Large Transfers",
  network: "mainnet",
  addresses: ["0xTOKEN_ADDRESS"],
  abi: '[{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]',
  eventConditions: [{ eventSignature: "Transfer(address,address,uint256)", expression: "value > 1000000000000000000000" }],
  alertThreshold: { amount: 1, windowSeconds: 3600 },
  notificationChannels: ["email-channel-id"],
});
```

## Common Patterns

### Combining Extensions

When multiple OZ contracts override the same function, you must resolve the diamond. The pattern is always the same: override the conflicting function and call `super`.

```solidity
// Multiple inheritance resolution example
function _update(address from, address to, uint256 value)
    internal
    override(ERC20, ERC20Votes, ERC20Pausable)
{
    super._update(from, to, value);
}
```

The `super` call invokes the rightmost parent first (C3 linearization). Order your inheritance from most base to most derived:

```solidity
// Correct: base -> extensions
contract Token is ERC20, ERC20Burnable, ERC20Pausable, ERC20Votes { ... }
```

### Governor (On-Chain Governance)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Governor} from "@openzeppelin/contracts/governance/Governor.sol";
import {GovernorCountingSimple} from "@openzeppelin/contracts/governance/extensions/GovernorCountingSimple.sol";
import {GovernorVotes} from "@openzeppelin/contracts/governance/extensions/GovernorVotes.sol";
import {GovernorVotesQuorumFraction} from "@openzeppelin/contracts/governance/extensions/GovernorVotesQuorumFraction.sol";
import {GovernorTimelockControl} from "@openzeppelin/contracts/governance/extensions/GovernorTimelockControl.sol";
import {IVotes} from "@openzeppelin/contracts/governance/utils/IVotes.sol";
import {TimelockController} from "@openzeppelin/contracts/governance/TimelockController.sol";

contract MyGovernor is
    Governor,
    GovernorCountingSimple,
    GovernorVotes,
    GovernorVotesQuorumFraction,
    GovernorTimelockControl
{
    constructor(IVotes token, TimelockController timelock)
        Governor("MyGovernor")
        GovernorVotes(token)
        GovernorVotesQuorumFraction(4) // 4% quorum
        GovernorTimelockControl(timelock)
    {}

    function votingDelay() public pure override returns (uint256) {
        return 7200; // ~1 day at 12s blocks
    }

    function votingPeriod() public pure override returns (uint256) {
        return 50400; // ~1 week at 12s blocks
    }

    function proposalThreshold() public pure override returns (uint256) {
        return 100_000 * 10 ** 18; // 100k tokens to propose
    }

    // Required overrides for diamond resolution
    function state(uint256 proposalId)
        public
        view
        override(Governor, GovernorTimelockControl)
        returns (ProposalState)
    {
        return super.state(proposalId);
    }

    function proposalNeedsQueuing(uint256 proposalId)
        public
        view
        override(Governor, GovernorTimelockControl)
        returns (bool)
    {
        return super.proposalNeedsQueuing(proposalId);
    }

    function _queueOperations(
        uint256 proposalId,
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        bytes32 descriptionHash
    ) internal override(Governor, GovernorTimelockControl) returns (uint48) {
        return super._queueOperations(proposalId, targets, values, calldatas, descriptionHash);
    }

    function _executeOperations(
        uint256 proposalId,
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        bytes32 descriptionHash
    ) internal override(Governor, GovernorTimelockControl) {
        super._executeOperations(proposalId, targets, values, calldatas, descriptionHash);
    }

    function _cancel(
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        bytes32 descriptionHash
    ) internal override(Governor, GovernorTimelockControl) returns (uint256) {
        return super._cancel(targets, values, calldatas, descriptionHash);
    }

    function _executor() internal view override(Governor, GovernorTimelockControl) returns (address) {
        return super._executor();
    }
}
```

### ERC-20 with Capped Supply and Pausability

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC20Capped} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Capped.sol";
import {ERC20Pausable} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Pausable.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract CappedToken is ERC20Capped, ERC20Pausable, Ownable {
    constructor(address initialOwner)
        ERC20("CappedToken", "CAP")
        ERC20Capped(100_000_000 * 10 ** 18) // 100M cap
        Ownable(initialOwner)
    {
        _mint(initialOwner, 10_000_000 * 10 ** 18);
    }

    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }

    function pause() external onlyOwner { _pause(); }
    function unpause() external onlyOwner { _unpause(); }

    function _update(address from, address to, uint256 value)
        internal
        override(ERC20Capped, ERC20Pausable)
    {
        super._update(from, to, value);
    }
}
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `OwnableUnauthorizedAccount(account)` | Caller is not the owner | Check `owner()` before calling `onlyOwner` functions |
| `OwnableInvalidOwner(owner)` | Trying to set owner to `address(0)` | Pass a valid address to the Ownable constructor |
| `AccessControlUnauthorizedAccount(account, role)` | Caller lacks the required role | Grant role via `grantRole(role, account)` from the role's admin |
| `EnforcedPause()` | Function called while contract is paused | Call `unpause()` first |
| `ExpectedPause()` | `unpause()` called when not paused | Check `paused()` state before calling |
| `ERC20InsufficientBalance(sender, balance, needed)` | Transfer amount exceeds balance | Verify balances before transfer |
| `ERC721NonexistentToken(tokenId)` | Querying a token that doesn't exist | Check `_exists` or catch the revert |
| `InvalidInitialization()` | `initializer` called more than once | Use `reinitializer(n)` for subsequent inits |

## Troubleshooting

### "Identifier already declared" on Multiple Inheritance

Symptom: Compiler error when two parent contracts define the same function.

Fix: Add an explicit override that calls `super`:

```solidity
function _update(...) internal override(ParentA, ParentB) {
    super._update(...);
}
```

List ALL parents that define the function in the `override(...)` specifier.

### Upgradeable Contract Won't Initialize

Symptom: `InvalidInitialization()` revert on proxy deployment.

Fix: Ensure the implementation constructor calls `_disableInitializers()`. The proxy calls `initialize()` -- if the implementation already initialized itself, the proxy call fails.

### Storage Collision After Upgrade

Symptom: State variables return garbage after upgrading.

Fix: Never reorder, rename, or remove state variables. Only append new variables at the end. In v5, OZ uses ERC-7201 namespaced storage internally, but your custom variables must still follow append-only ordering.

## Security Considerations

- Always use `SafeERC20` when interacting with arbitrary ERC-20 tokens -- many don't follow the standard return value convention.
- Apply `ReentrancyGuard` to functions that transfer ETH or call external contracts after state changes, even with CEI pattern as defense-in-depth.
- Use `Ownable2Step` over `Ownable` for any contract where losing ownership is catastrophic. The two-step process prevents transferring to a typo address.
- For upgradeable contracts, use the `@openzeppelin/upgrades` Hardhat/Foundry plugin to validate storage layout compatibility before deploying upgrades.
- Never leave `_authorizeUpgrade` unprotected. Always gate it with `onlyOwner` or a role check.

## References

- [OpenZeppelin Contracts v5 Docs](https://docs.openzeppelin.com/contracts/5.x/)
- [GitHub: openzeppelin-contracts](https://github.com/OpenZeppelin/openzeppelin-contracts)
- [OpenZeppelin Contracts Wizard](https://wizard.openzeppelin.com/) -- generates contract code with selected extensions
- [v5 Migration Guide](https://docs.openzeppelin.com/contracts/5.x/upgradeable)
- [OpenZeppelin Defender](https://docs.openzeppelin.com/defender/v2/)
- [ERC-7201: Namespaced Storage Layout](https://eips.ethereum.org/EIPS/eip-7201)
- [EIP-1822: UUPS](https://eips.ethereum.org/EIPS/eip-1822)
- [EIP-2612: Permit](https://eips.ethereum.org/EIPS/eip-2612)
