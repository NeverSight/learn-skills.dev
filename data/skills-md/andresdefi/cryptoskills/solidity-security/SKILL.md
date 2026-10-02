---
name: solidity-security
description: Comprehensive Solidity security patterns, vulnerability prevention, and audit preparation. Covers reentrancy, access control, token decimals, oracle manipulation, vault inflation, proxy safety, EIP-712 signatures, MEV protection, and pre-deploy checklists. Every pattern includes wrong vs correct code.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: Security
tags:
  - solidity
  - security
  - audit
  - reentrancy
  - access-control
---

# Solidity Security

Defensive Solidity patterns that prevent the vulnerabilities behind 90%+ of DeFi exploits. Every section shows the broken pattern first, then the fix. Code is Solidity 0.8.20+ unless noted.

## What You Probably Got Wrong

> LLMs generate plausible but exploitable Solidity. These are the blind spots that cause real losses.

- **USDC/USDT are 6 decimals, not 18** — `1e18` assumptions silently inflate or truncate amounts by 1e12. Always read `IERC20Metadata(token).decimals()` onchain.
- **Solidity has no floating point** — Writing `amount * 0.03` does not compile. Use basis points: `amount * 300 / 10_000`.
- **0.8.x does NOT prevent all overflow** — Checked math covers `+`, `-`, `*`, `/` on standard types. It does NOT protect `unchecked {}` blocks, assembly, bitwise ops, or casting between smaller types (`uint256` to `uint128`).
- **`transfer()` and `send()` are not safe** — They forward only 2300 gas. Since EIP-1884 repriced `SLOAD`, many contracts and multisigs (Gnosis Safe) cannot receive ETH via `transfer()`. Use `call{value:}("")` with reentrancy protection.
- **ERC20 `approve` is not universal** — USDT requires resetting allowance to 0 before setting a new value. Use OpenZeppelin `SafeERC20`.
- **`msg.sender` changes in delegatecall** — In proxy patterns, `msg.sender` in the implementation is the caller, not the proxy. But `address(this)` is the proxy's address. Confusing these causes critical auth bugs.
- **`block.timestamp` is manipulable** — Miners/validators can shift it by ~15 seconds. Never use it as sole entropy or for tight time windows.

## Critical Vulnerabilities

### 1. Token Decimal Mismatch

USDC, USDT, and WBTC use 6 or 8 decimals. Assuming 18 decimals causes catastrophic mispricing.

```solidity
// WRONG: assumes all tokens are 18 decimals
function getValueInUsd(address token, uint256 amount) external view returns (uint256) {
    uint256 price = oracle.getPrice(token);
    return amount * price / 1e18;
}
```

```solidity
// CORRECT: normalize to 18 decimals before math
function getValueInUsd(address token, uint256 amount) external view returns (uint256) {
    uint256 price = oracle.getPrice(token);
    uint8 decimals = IERC20Metadata(token).decimals();
    uint256 normalizedAmount = amount * 10 ** (18 - decimals);
    return normalizedAmount * price / 1e18;
}
```

### 2. No Floating Point — Basis Points Pattern

Solidity has no `float` or `double`. Percentages must use integer math with a denominator.

```solidity
// WRONG: this does not compile
uint256 fee = amount * 0.03;
```

```solidity
// CORRECT: basis points (1 bp = 0.01%, 10_000 bp = 100%)
uint256 constant BPS_DENOMINATOR = 10_000;

function calculateFee(uint256 amount, uint256 feeBps) public pure returns (uint256) {
    return amount * feeBps / BPS_DENOMINATOR;
}

// 3% fee = 300 bps
// 0.3% fee = 30 bps
// 0.01% fee = 1 bp
```

For higher precision (e.g., interest rate models), use WAD math (1e18 denominator):

```solidity
uint256 constant WAD = 1e18;

function wadMul(uint256 a, uint256 b) internal pure returns (uint256) {
    return (a * b + WAD / 2) / WAD; // rounds to nearest
}
```

### 3. Reentrancy

The attacker calls back into your contract before state updates complete. CEI (Checks-Effects-Interactions) is the primary defense.

```solidity
// WRONG: state update after external call
function withdraw(uint256 amount) external {
    require(balances[msg.sender] >= amount, "Insufficient");
    (bool ok, ) = msg.sender.call{value: amount}("");
    require(ok, "Transfer failed");
    balances[msg.sender] -= amount; // attacker re-enters before this line
}
```

```solidity
// CORRECT: CEI pattern — update state before external call
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract Vault is ReentrancyGuard {
    mapping(address => uint256) public balances;

    function withdraw(uint256 amount) external nonReentrant {
        // Checks
        require(balances[msg.sender] >= amount, "Insufficient");
        // Effects
        balances[msg.sender] -= amount;
        // Interactions
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "Transfer failed");
    }
}
```

Use BOTH CEI and `nonReentrant`. CEI handles the logic order; `nonReentrant` catches cross-function reentrancy where attacker calls a different function on re-entry.

Read-only reentrancy: an attacker re-enters a `view` function that reads stale state (e.g., Curve LP price during callback). Protect by applying `nonReentrant` to view functions that external protocols depend on.

### 4. SafeERC20 for Non-Standard Tokens

USDT's `approve()` has no return value. BNB's `transfer()` returns nothing. Calling these without SafeERC20 silently fails or reverts.

```solidity
// WRONG: raw ERC20 calls — breaks on USDT, BNB, and other non-standard tokens
IERC20(token).approve(spender, amount); // USDT reverts if allowance != 0
IERC20(token).transfer(to, amount); // BNB returns no bool
```

```solidity
// CORRECT: SafeERC20 handles all edge cases
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract TokenHandler {
    using SafeERC20 for IERC20;

    function doTransfer(IERC20 token, address to, uint256 amount) external {
        token.safeTransfer(to, amount);
    }

    function doApprove(IERC20 token, address spender, uint256 amount) external {
        // forceApprove resets to 0 first, then sets — works with USDT
        token.forceApprove(spender, amount);
    }
}
```

### 5. Oracle Manipulation

DEX spot prices (Uniswap `slot0`, reserves ratio) can be manipulated within a single transaction via flash loans.

```solidity
// WRONG: using instantaneous DEX price — flash-loan manipulable
function getPrice() external view returns (uint256) {
    (uint160 sqrtPriceX96,,,,,,) = pool.slot0();
    return uint256(sqrtPriceX96) ** 2 / (2 ** 192);
}
```

```solidity
// CORRECT: use TWAP or Chainlink with staleness checks
import {AggregatorV3Interface} from "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

function getChainlinkPrice(AggregatorV3Interface feed) public view returns (uint256) {
    (
        uint80 roundId,
        int256 answer,
        ,
        uint256 updatedAt,
        uint80 answeredInRound
    ) = feed.latestRoundData();
    require(answer > 0, "Negative price");
    require(updatedAt > block.timestamp - 3600, "Stale price"); // 1 hour staleness
    require(answeredInRound >= roundId, "Stale round");
    return uint256(answer);
}
```

For onchain TWAP, use Uniswap V3's `observe()` with a window of 30+ minutes. Never use `slot0()` directly for pricing.

### 6. Vault Inflation Attack (ERC4626)

First depositor can inflate share price by donating tokens directly to the vault, causing subsequent depositors to mint 0 shares and lose their entire deposit.

Attack scenario: vault is empty, attacker deposits 1 wei to get 1 share, then transfers 1e18 tokens directly to vault. Next depositor sends 1.99e18 tokens but gets 0 shares due to rounding.

```solidity
// WRONG: naive vault with no inflation protection
function deposit(uint256 assets) external returns (uint256 shares) {
    shares = totalSupply == 0 ? assets : assets * totalSupply / totalAssets();
    _mint(msg.sender, shares);
    token.safeTransferFrom(msg.sender, address(this), assets);
}
```

```solidity
// CORRECT: virtual offset (OpenZeppelin ERC4626 default since v4.9)
// Adds virtual assets/shares to prevent first-depositor manipulation
abstract contract SafeVault is ERC4626 {
    // _decimalsOffset() returns 0 by default — override to add protection
    // An offset of 3 means 1e3 virtual shares/assets, preventing
    // attacks below ~1e3 in value
    function _decimalsOffset() internal pure override returns (uint8) {
        return 3;
    }
}
```

The virtual offset makes the cost of an inflation attack `10^(offset)` times more expensive. An offset of 6 makes attacks require $1M+ to steal $1.

### 7. Infinite Approvals

Setting `type(uint256).max` approval is a UX convenience that becomes a liability when the approved contract is exploited.

```solidity
// WRONG: infinite approval persists after use
token.approve(protocol, type(uint256).max);
```

```solidity
// CORRECT: approve only what's needed, when needed
function depositToProtocol(IERC20 token, uint256 amount) external {
    token.safeTransferFrom(msg.sender, address(this), amount);
    token.forceApprove(address(protocol), amount);
    protocol.deposit(amount);
    // Reset approval after use
    token.forceApprove(address(protocol), 0);
}
```

For contracts that interact with routers, use the approve-use-reset pattern in the same transaction.

### 8. Access Control

Bare `onlyOwner` is a single point of failure. Use role-based access for production contracts.

```solidity
// WRONG: single owner controls everything
address public owner;
modifier onlyOwner() {
    require(msg.sender == owner);
    _;
}
function setFee(uint256 fee) external onlyOwner { /* ... */ }
function pause() external onlyOwner { /* ... */ }
function upgradeTo(address impl) external onlyOwner { /* ... */ }
```

```solidity
// CORRECT: granular roles via AccessControl
import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";

contract Protocol is AccessControl {
    bytes32 public constant FEE_MANAGER = keccak256("FEE_MANAGER");
    bytes32 public constant GUARDIAN = keccak256("GUARDIAN");
    bytes32 public constant UPGRADER = keccak256("UPGRADER");

    constructor(address admin) {
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
    }

    function setFee(uint256 fee) external onlyRole(FEE_MANAGER) {
        require(fee <= 1000, "Fee exceeds 10%"); // 1000 bps max
        emit FeeUpdated(fee);
    }

    function pause() external onlyRole(GUARDIAN) { /* ... */ }
}
```

For critical operations (upgrades, large withdrawals), add a timelock:

```solidity
// Queue operation, wait 48 hours, then execute
import {TimelockController} from "@openzeppelin/contracts/governance/TimelockController.sol";
```

### 9. Input Validation

Missing input checks are the most common low-severity finding in audits, but they occasionally enable critical exploits.

```solidity
// WRONG: no validation
function initialize(address _token, address _oracle, uint256 _fee) external {
    token = _token;
    oracle = _oracle;
    fee = _fee;
}
```

```solidity
// CORRECT: validate everything
error ZeroAddress();
error FeeTooHigh(uint256 fee, uint256 max);
error InvalidArray();

function initialize(address _token, address _oracle, uint256 _feeBps) external {
    if (_token == address(0)) revert ZeroAddress();
    if (_oracle == address(0)) revert ZeroAddress();
    if (_feeBps > 1000) revert FeeTooHigh(_feeBps, 1000);

    token = _token;
    oracle = _oracle;
    feeBps = _feeBps;
}

function batchTransfer(address[] calldata recipients, uint256[] calldata amounts) external {
    if (recipients.length != amounts.length) revert InvalidArray();
    if (recipients.length == 0) revert InvalidArray();
    // ...
}
```

Use custom errors instead of require strings — they cost less gas and are easier to decode offchain.

## MEV and Sandwich Attacks

MEV (Maximal Extractable Value) bots monitor the mempool and insert transactions before/after yours to extract profit.

**Sandwich attack**: bot sees your swap, front-runs to move the price up, your swap executes at a worse price, bot back-runs to capture the difference.

### Protection Strategies

```solidity
// 1. Enforce slippage limits — the primary defense
function swap(
    address tokenIn,
    address tokenOut,
    uint256 amountIn,
    uint256 amountOutMin // user-specified minimum output
) external returns (uint256 amountOut) {
    amountOut = _executeSwap(tokenIn, tokenOut, amountIn);
    require(amountOut >= amountOutMin, "Slippage exceeded");
}

// 2. Deadline parameter prevents stale transactions from executing
function swapWithDeadline(
    address tokenIn,
    address tokenOut,
    uint256 amountIn,
    uint256 amountOutMin,
    uint256 deadline
) external returns (uint256 amountOut) {
    require(block.timestamp <= deadline, "Transaction expired");
    amountOut = _executeSwap(tokenIn, tokenOut, amountIn);
    require(amountOut >= amountOutMin, "Slippage exceeded");
}
```

**Additional protections**:
- Submit transactions via **Flashbots Protect** RPC (`https://rpc.flashbots.net`) to bypass the public mempool entirely
- Use **private mempools** (MEV Blocker, MEV Share) that auction MEV back to users
- For protocol designers: implement **commit-reveal schemes** for auction-sensitive operations
- Set slippage to the tightest value the user will accept, never leave it open

## Proxy Patterns

Upgradeable contracts split storage (proxy) from logic (implementation). Getting storage layout wrong corrupts all user funds.

### UUPS vs Transparent Proxy

| Feature | UUPS | Transparent |
|---------|------|-------------|
| Upgrade logic location | Implementation contract | Proxy contract |
| Gas per call | Lower (no admin check) | Higher (checks if caller is admin) |
| Risk | Forgetting `_authorizeUpgrade` bricks the contract | Admin can't accidentally call implementation functions |
| Recommendation | Preferred for new projects (ERC-1967) | Legacy, still widely used |

### Storage Layout Rules (Non-Negotiable)

```solidity
// WRONG: changing storage layout between versions
// V1
contract VaultV1 {
    uint256 public totalDeposits; // slot 0
    address public oracle;        // slot 1
}

// V2 — BROKEN: inserting a variable shifts all slots
contract VaultV2 {
    uint256 public totalDeposits; // slot 0
    uint256 public totalShares;   // slot 1 — COLLISION: overwrites oracle
    address public oracle;        // slot 2
}
```

```solidity
// CORRECT: append-only storage, use storage gaps
// V1
contract VaultV1 {
    uint256 public totalDeposits; // slot 0
    address public oracle;        // slot 1
    uint256[48] private __gap;    // reserve 48 slots for future use
}

// V2 — safe: new variable consumes a gap slot
contract VaultV2 {
    uint256 public totalDeposits; // slot 0
    address public oracle;        // slot 1
    uint256 public totalShares;   // slot 2 — uses first gap slot
    uint256[47] private __gap;    // gap shrinks by 1
}
```

### UUPS Implementation

```solidity
import {UUPSUpgradeable} from "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import {AccessControlUpgradeable} from "@openzeppelin/contracts-upgradeable/access/AccessControlUpgradeable.sol";

contract VaultV1 is UUPSUpgradeable, AccessControlUpgradeable {
    bytes32 public constant UPGRADER = keccak256("UPGRADER");

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    function initialize(address admin) public initializer {
        __UUPSUpgradeable_init();
        __AccessControl_init();
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
        _grantRole(UPGRADER, admin);
    }

    // CRITICAL: without this, anyone can upgrade — or nobody can (bricked)
    function _authorizeUpgrade(address newImplementation) internal override onlyRole(UPGRADER) {}
}
```

Rules:
- Never remove or reorder existing storage variables
- Always include `_disableInitializers()` in the constructor
- Always include `_authorizeUpgrade` with proper access control
- Use `@openzeppelin/upgrades-core` to validate storage layout between versions
- Test upgrades with `forge test --fork-url` against the actual proxy

## EIP-712 Typed Data Signatures

EIP-712 creates human-readable signing requests instead of opaque hex blobs. Required for gasless approvals (Permit), meta-transactions, and offchain order books.

```solidity
import {EIP712} from "@openzeppelin/contracts/utils/cryptography/EIP712.sol";
import {ECDSA} from "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

contract GaslessOrders is EIP712 {
    // EIP-712 struct type hash — must match the struct exactly
    bytes32 public constant ORDER_TYPEHASH = keccak256(
        "Order(address maker,address tokenIn,address tokenOut,uint256 amountIn,uint256 amountOutMin,uint256 deadline,uint256 nonce)"
    );

    mapping(address => uint256) public nonces;

    constructor() EIP712("GaslessOrders", "1") {}

    struct Order {
        address maker;
        address tokenIn;
        address tokenOut;
        uint256 amountIn;
        uint256 amountOutMin;
        uint256 deadline;
        uint256 nonce;
    }

    function executeOrder(Order calldata order, bytes calldata signature) external {
        require(block.timestamp <= order.deadline, "Order expired");
        require(order.nonce == nonces[order.maker], "Invalid nonce");

        bytes32 structHash = keccak256(abi.encode(
            ORDER_TYPEHASH,
            order.maker,
            order.tokenIn,
            order.tokenOut,
            order.amountIn,
            order.amountOutMin,
            order.deadline,
            order.nonce
        ));

        bytes32 digest = _hashTypedDataV4(structHash);
        address signer = ECDSA.recover(digest, signature);
        require(signer == order.maker, "Invalid signature");

        nonces[order.maker]++;

        _fillOrder(order);
    }

    function _fillOrder(Order calldata order) internal { /* ... */ }
}
```

Key rules:
- Always include a `nonce` to prevent replay attacks
- Always include a `deadline` for expiry
- The domain separator auto-includes `chainId` — prevents cross-chain replay
- Use `_hashTypedDataV4` from OpenZeppelin, never roll your own domain separator
- For ERC-20 `permit()`, use OpenZeppelin's `ERC20Permit` instead of reimplementing

## Pre-Deploy Security Checklist

Run through every item before deploying to mainnet. Not optional.

### Code Quality
- [ ] All external/public functions have NatSpec (`@notice`, `@param`, `@return`)
- [ ] Custom errors used instead of require strings
- [ ] Events emitted for every state change
- [ ] No `TODO`, `FIXME`, or `HACK` comments remain
- [ ] No hardcoded addresses — use constructor params or immutables

### Access Control
- [ ] Every privileged function has access control
- [ ] Admin roles use multisig, not EOA
- [ ] Upgrade functions protected and tested
- [ ] Timelock on sensitive operations (fee changes, large withdrawals)
- [ ] `renounceOwnership` disabled or confirmed intentional

### Arithmetic and Logic
- [ ] Token decimal handling verified for every token interaction
- [ ] Division before multiplication identified and fixed (precision loss)
- [ ] `unchecked` blocks reviewed for overflow possibility
- [ ] Downcasts (`uint256` to `uint128`) have bounds checks

### External Interactions
- [ ] CEI pattern followed on every external call
- [ ] `ReentrancyGuard` applied to all state-changing functions
- [ ] `SafeERC20` used for all token operations
- [ ] Return values of low-level `call` checked
- [ ] Oracle staleness and negative price checks in place
- [ ] Flash loan attack vectors analyzed

### Proxy Safety (if upgradeable)
- [ ] `_disableInitializers()` in implementation constructor
- [ ] `_authorizeUpgrade` has access control
- [ ] Storage layout validated between versions with OpenZeppelin tooling
- [ ] No `selfdestruct` or `delegatecall` in implementation

### Testing
- [ ] Line coverage above 90%
- [ ] Fuzz tests on all math-heavy functions
- [ ] Invariant tests on core protocol properties
- [ ] Fork tests against mainnet state
- [ ] Upgrade path tested (V1 -> V2 with real state)

## Automated Security Tools

### Slither (Static Analysis)

```bash
# Install
pip3 install slither-analyzer

# Run on project
slither . --filter-paths "node_modules|lib"

# Common high-confidence detectors
slither . --detect reentrancy-eth,reentrancy-no-eth,arbitrary-send-eth,suicidal,uninitialized-state
```

### Foundry Fuzz Testing

```solidity
// Fuzz test: Foundry generates random inputs automatically
function testFuzz_depositWithdrawInvariant(uint256 amount) public {
    amount = bound(amount, 1, 1e30); // constrain to reasonable range

    token.mint(address(this), amount);
    token.approve(address(vault), amount);

    uint256 sharesBefore = vault.totalSupply();
    vault.deposit(amount, address(this));

    uint256 sharesReceived = vault.totalSupply() - sharesBefore;
    vault.redeem(sharesReceived, address(this), address(this));

    // Invariant: user gets back at most what they deposited (minus rounding)
    assertLe(token.balanceOf(address(this)), amount);
    // Invariant: rounding loss is at most 1 wei
    assertGe(token.balanceOf(address(this)), amount - 1);
}
```

### Foundry Invariant Testing

```solidity
// Define invariants that must ALWAYS hold
function invariant_totalAssetsBacksShares() public view {
    if (vault.totalSupply() > 0) {
        assertGt(vault.totalAssets(), 0, "Shares exist without backing assets");
    }
}

function invariant_solvency() public view {
    assertGe(
        token.balanceOf(address(vault)),
        vault.totalAssets(),
        "Vault is insolvent"
    );
}
```

### Mythril (Symbolic Execution)

```bash
# Install
pip3 install mythril

# Analyze a single contract
myth analyze src/Vault.sol --solc-json mythril.config.json

# Quick scan (faster, fewer detectors)
myth analyze src/Vault.sol --execution-timeout 300
```

### Tool Comparison

| Tool | Type | Strengths | Limitations |
|------|------|-----------|-------------|
| Slither | Static analysis | Fast, low false positives, CI-friendly | Misses runtime/state-dependent bugs |
| Mythril | Symbolic execution | Finds deep logic bugs | Slow on large contracts |
| Foundry fuzz | Property testing | Tests with real EVM, fast | Only as good as your properties |
| Echidna | Fuzzer | Stateful fuzzing, coverage-guided | Requires property definitions |
| Certora | Formal verification | Mathematical proofs | Expensive, steep learning curve |

Run Slither in CI on every PR. Run Foundry fuzz tests with 10,000+ runs before deployment. Use Mythril for high-value contracts. Commission a professional audit for anything holding significant user funds.

## References

- [SWC Registry](https://swcregistry.io/) — Smart Contract Weakness Classification
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/) — Battle-tested implementations
- [Solidity Security Considerations](https://docs.soliditylang.org/en/latest/security-considerations.html)
- [Consensys Smart Contract Best Practices](https://consensys.github.io/smart-contract-best-practices/)
- [EIP-712: Typed Structured Data Hashing and Signing](https://eips.ethereum.org/EIPS/eip-712)
- [EIP-4626: Tokenized Vaults](https://eips.ethereum.org/EIPS/eip-4626)
- [Flashbots Protect](https://docs.flashbots.net/flashbots-protect/overview)
- [Trail of Bits Building Secure Contracts](https://secure-contracts.com/)
- [Slither Documentation](https://github.com/crytic/slither)
- [Foundry Book — Fuzz Testing](https://book.getfoundry.sh/forge/fuzz-testing)
