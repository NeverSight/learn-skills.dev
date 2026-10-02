---
name: evm-testing
description: Comprehensive testing patterns for EVM smart contracts. Covers unit tests, fuzz testing, invariant testing, fork testing, and gas optimization with Foundry and Hardhat. Focuses on patterns and techniques — not CLI usage or project setup.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: Dev Tools
tags:
  - testing
  - foundry
  - hardhat
  - fuzzing
  - invariants
---

# EVM Testing Patterns

Testing patterns for EVM smart contracts across Foundry (Solidity) and Hardhat (TypeScript). This skill focuses on how to write effective tests — not tool installation or CLI commands. See the `foundry` skill for Foundry setup, commands, and deployment.

## What You Probably Got Wrong

- **Foundry tests are Solidity, not JS** -- Tests in Foundry are `.t.sol` files that extend `forge-std/Test.sol`. There is no Mocha, no Chai, no ethers.js. Every test is a Solidity function starting with `test`.
- **Fuzz != invariant** -- Fuzz tests run one function with random inputs. Invariant tests call random sequences of functions and assert properties that must always hold. They solve different problems.
- **`vm.prank` vs `vm.startPrank`** -- `vm.prank(addr)` only affects the NEXT external call. If your test makes multiple calls as the same address, use `vm.startPrank(addr)` ... `vm.stopPrank()`. This is the #1 source of "why does my test pass when it shouldn't."
- **Hardhat uses Mocha/Chai, not Jest** -- Hardhat tests use `describe`/`it` from Mocha and `expect` from Chai. Jest matchers (`toBe`, `toEqual`) do not exist.
- **Fork tests use real state** -- `vm.createSelectFork` pulls actual mainnet storage. Whale balances change, contracts get upgraded, oracles update. Pin your block number or tests will flake.
- **`deal` cheatcode for token balances** -- `deal(address(token), user, amount)` writes directly to the token's balance mapping. This works for standard ERC20s but can break tokens with rebasing, fee-on-transfer, or non-standard storage layouts. For those, impersonate a whale instead.
- **`expectRevert` must come BEFORE the call** -- `vm.expectRevert()` sets up an expectation for the next call. Placing it after the reverting call does nothing — the test reverts immediately and `expectRevert` is never reached.
- **`expectEmit` order matters** -- Call `vm.expectEmit()`, then emit the expected event shape, THEN execute the function that should emit it. Getting the order wrong silently passes or gives cryptic errors.

## Unit Testing (Foundry)

### Test Structure and Naming

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import {Test, console} from "forge-std/Test.sol";
import {ERC20Token} from "../src/ERC20Token.sol";

contract ERC20TokenTest is Test {
    ERC20Token token;
    address alice;
    address bob;

    // setUp runs before EVERY test function
    function setUp() public {
        alice = makeAddr("alice");
        bob = makeAddr("bob");
        token = new ERC20Token("Test", "TST", 18);
        deal(address(token), alice, 1000e18);
    }

    // Naming: test_<action>_<context> or test_RevertWhen_<condition>
    function test_transfer_updatesBalances() public {
        vm.prank(alice);
        token.transfer(bob, 100e18);

        assertEq(token.balanceOf(alice), 900e18);
        assertEq(token.balanceOf(bob), 100e18);
    }

    function test_transfer_emitsEvent() public {
        vm.expectEmit(true, true, false, true, address(token));
        emit ERC20Token.Transfer(alice, bob, 100e18);

        vm.prank(alice);
        token.transfer(bob, 100e18);
    }

    function test_RevertWhen_transferExceedsBalance() public {
        vm.prank(alice);
        vm.expectRevert(
            abi.encodeWithSelector(
                ERC20Token.InsufficientBalance.selector,
                alice,
                1000e18,
                2000e18
            )
        );
        token.transfer(bob, 2000e18);
    }

    function test_RevertWhen_transferToZeroAddress() public {
        vm.prank(alice);
        vm.expectRevert(ERC20Token.ZeroAddress.selector);
        token.transfer(address(0), 100e18);
    }
}
```

### Testing Custom Errors vs Require Strings

```solidity
// Custom error (preferred — saves gas)
vm.expectRevert(Vault.Unauthorized.selector);

// Custom error with arguments
vm.expectRevert(
    abi.encodeWithSelector(Vault.AmountExceeded.selector, 100, 50)
);

// Require string (legacy pattern)
vm.expectRevert("Ownable: caller is not the owner");

// Low-level revert (no data)
vm.expectRevert(bytes(""));

// Arithmetic underflow/overflow (Solidity >=0.8)
vm.expectRevert(abi.encodeWithSignature("Panic(uint256)", 0x11));
```

### Testing Multiple Events in Order

```solidity
function test_batchTransfer_emitsEventsInOrder() public {
    address[] memory recipients = new address[](2);
    recipients[0] = bob;
    recipients[1] = makeAddr("charlie");
    uint256[] memory amounts = new uint256[](2);
    amounts[0] = 50e18;
    amounts[1] = 30e18;

    // Each expectEmit matches the next event in emission order
    vm.expectEmit(true, true, false, true, address(token));
    emit ERC20Token.Transfer(alice, bob, 50e18);

    vm.expectEmit(true, true, false, true, address(token));
    emit ERC20Token.Transfer(alice, recipients[1], 30e18);

    vm.prank(alice);
    token.batchTransfer(recipients, amounts);
}
```

## Fuzz Testing

Foundry generates random inputs for any function parameter. Fuzz tests find edge cases you would never write by hand.

### Basic Fuzz Test

```solidity
function test_fuzz_depositAndWithdraw(uint256 amount) public {
    // bound constrains to a range — better than vm.assume for continuous ranges
    amount = bound(amount, 1, 100 ether);

    vm.deal(alice, amount);
    vm.startPrank(alice);

    vault.deposit{value: amount}();
    assertEq(vault.balanceOf(alice), amount);

    vault.withdraw(amount);
    assertEq(vault.balanceOf(alice), 0);
    assertEq(alice.balance, amount);

    vm.stopPrank();
}
```

### `bound` vs `vm.assume`

```solidity
// PREFER: bound — transforms input to valid range, never discards runs
amount = bound(amount, 1 ether, 100 ether);

// AVOID for ranges: vm.assume — discards the run if condition is false
// Too many rejects (>65536 by default) fails the entire fuzz campaign
vm.assume(amount > 0 && amount < 100 ether);

// vm.assume IS correct for discrete conditions that can't be bounded
vm.assume(addr != address(0));
vm.assume(addr != address(vault));
```

### Fuzz with Multiple Parameters

```solidity
function test_fuzz_swap(
    uint256 amountIn,
    uint256 reserveA,
    uint256 reserveB
) public {
    reserveA = bound(reserveA, 1e18, 1_000_000e18);
    reserveB = bound(reserveB, 1e18, 1_000_000e18);
    amountIn = bound(amountIn, 1e15, reserveA / 10);

    uint256 amountOut = pool.getAmountOut(amountIn, reserveA, reserveB);

    // Constant product invariant: k should not decrease
    uint256 kBefore = reserveA * reserveB;
    uint256 kAfter = (reserveA + amountIn) * (reserveB - amountOut);
    assertGe(kAfter, kBefore, "k decreased after swap");
}
```

### Fuzz Config

In `foundry.toml`:

```toml
[fuzz]
runs = 256              # default, increase to 1000+ for critical paths
max_test_rejects = 65536 # max rejected inputs before failure
seed = "0x1"            # optional: deterministic seed for reproducibility

[profile.ci.fuzz]
runs = 10000            # more runs in CI
```

## Invariant Testing

Invariant tests are stateful: Foundry calls random functions in random order across multiple contracts, then checks that your invariant assertions still hold. This is the most powerful testing technique for finding complex bugs.

### Handler Pattern

The handler wraps your contract with bounded inputs and tracks ghost variables for invariant assertions.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import {Test} from "forge-std/Test.sol";
import {StdInvariant} from "forge-std/StdInvariant.sol";
import {LendingPool} from "../src/LendingPool.sol";

contract LendingPoolHandler is Test {
    LendingPool pool;
    address[] public actors;
    uint256 public ghost_totalDeposited;
    uint256 public ghost_totalBorrowed;
    uint256 public ghost_totalRepaid;
    uint256 public ghost_totalWithdrawn;

    constructor(LendingPool _pool) {
        pool = _pool;
        for (uint256 i; i < 3; i++) {
            actors.push(makeAddr(string(abi.encodePacked("actor", i))));
        }
    }

    modifier useActor(uint256 seed) {
        vm.startPrank(actors[bound(seed, 0, actors.length - 1)]);
        _;
        vm.stopPrank();
    }

    function deposit(uint256 actorSeed, uint256 amount) public useActor(actorSeed) {
        amount = bound(amount, 0.01 ether, 50 ether);
        vm.deal(msg.sender, amount);
        pool.deposit{value: amount}();
        ghost_totalDeposited += amount;
    }

    function borrow(uint256 actorSeed, uint256 amount) public useActor(actorSeed) {
        uint256 max = pool.maxBorrow(msg.sender);
        if (max == 0) return;
        amount = bound(amount, 1, max);
        pool.borrow(amount);
        ghost_totalBorrowed += amount;
    }

    function repay(uint256 actorSeed, uint256 amount) public useActor(actorSeed) {
        uint256 debt = pool.debtOf(msg.sender);
        if (debt == 0) return;
        amount = bound(amount, 1, debt);
        vm.deal(msg.sender, amount);
        pool.repay{value: amount}();
        ghost_totalRepaid += amount;
    }

    function withdraw(uint256 actorSeed, uint256 amount) public useActor(actorSeed) {
        uint256 bal = pool.balanceOf(msg.sender);
        if (bal == 0) return;
        amount = bound(amount, 1, bal);
        pool.withdraw(amount);
        ghost_totalWithdrawn += amount;
    }
}

contract LendingPoolInvariantTest is StdInvariant, Test {
    LendingPool pool;
    LendingPoolHandler handler;

    function setUp() public {
        pool = new LendingPool();
        handler = new LendingPoolHandler(pool);
        targetContract(address(handler));
    }

    function invariant_solvency() public view {
        assertEq(
            address(pool).balance,
            handler.ghost_totalDeposited() - handler.ghost_totalWithdrawn()
                - handler.ghost_totalBorrowed() + handler.ghost_totalRepaid()
        );
    }

    function invariant_borrowsNeverExceedDeposits() public view {
        uint256 netDeposits = handler.ghost_totalDeposited() - handler.ghost_totalWithdrawn();
        uint256 netBorrows = handler.ghost_totalBorrowed() - handler.ghost_totalRepaid();
        assertGe(netDeposits, netBorrows);
    }
}
```

### Invariant Config

```toml
[invariant]
runs = 256          # number of test sequences
depth = 50          # calls per sequence (increase for deeper state exploration)
fail_on_revert = false  # false = skip reverting calls, true = fail on revert
shrink_run_limit = 5000 # attempts to minimize failing sequence
```

## Fork Testing

Test against real mainnet state. Pin a block number to avoid flaky tests.

### Basic Fork Test

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import {Test} from "forge-std/Test.sol";
import {IERC20} from "forge-std/interfaces/IERC20.sol";

contract ForkTest is Test {
    address constant USDC = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    address constant WHALE = 0x47ac0Fb4F2D84898e4D9E7b4DaB3C24507a6D503;

    function setUp() public {
        // Pin block number to prevent flaky tests from state changes
        vm.createSelectFork("mainnet", 19_000_000);
    }

    function test_whaleHasUSDC() public view {
        assertGt(IERC20(USDC).balanceOf(WHALE), 1_000_000e6);
    }

    function test_impersonateAndTransfer() public {
        address recipient = makeAddr("recipient");
        vm.prank(WHALE);
        IERC20(USDC).transfer(recipient, 1_000e6);
        assertEq(IERC20(USDC).balanceOf(recipient), 1_000e6);
    }
}
```

### Multi-Fork Testing

```solidity
function test_crossChainState() public {
    uint256 mainnetFork = vm.createFork("mainnet", 19_000_000);
    uint256 arbitrumFork = vm.createFork("arbitrum", 180_000_000);

    vm.selectFork(mainnetFork);
    uint256 mainnetSupply = IERC20(USDC).totalSupply();

    vm.selectFork(arbitrumFork);
    address ARB_USDC = 0xaf88d065e77c8cC2239327C5EDb3A432268e5831;
    assertGt(mainnetSupply, IERC20(ARB_USDC).totalSupply());
}
```

## Gas Optimization

### Forge Snapshot for Regression Tracking

```bash
forge snapshot                  # writes .gas-snapshot
forge snapshot --check          # fails if gas increased vs snapshot
forge snapshot --diff           # shows per-test gas diff
```

### Inline Gas Tracking in Tests

```solidity
function test_gasComparison_mappingVsArray() public {
    uint256 gasBefore = gasleft();
    storageContract.writeMapping(1, 42);
    uint256 mappingGas = gasBefore - gasleft();

    gasBefore = gasleft();
    storageContract.pushArray(42);
    uint256 arrayGas = gasBefore - gasleft();

    console.log("Mapping write:", mappingGas);
    console.log("Array push:   ", arrayGas);
    assertLt(mappingGas, arrayGas);
}
```

### Gas Report Per Function

```bash
forge test --gas-report --match-contract VaultTest
```

Output shows min/avg/median/max gas per function call — use this to identify expensive paths.

## Hardhat Testing

### Basic Test Setup

```typescript
import { expect } from "chai";
import { ethers } from "hardhat";
import { loadFixture } from "@nomicfoundation/hardhat-toolbox/network-helpers";

describe("Vault", function () {
  async function deployVaultFixture() {
    const [owner, alice, bob] = await ethers.getSigners();
    const Vault = await ethers.getContractFactory("Vault");
    const vault = await Vault.deploy();

    return { vault, owner, alice, bob };
  }

  it("should accept deposits", async function () {
    const { vault, alice } = await loadFixture(deployVaultFixture);

    await vault.connect(alice).deposit({ value: ethers.parseEther("1.0") });

    expect(await vault.balanceOf(alice.address)).to.equal(
      ethers.parseEther("1.0")
    );
  });

  it("should revert on zero deposit", async function () {
    const { vault, alice } = await loadFixture(deployVaultFixture);

    await expect(
      vault.connect(alice).deposit({ value: 0n })
    ).to.be.revertedWithCustomError(vault, "ZeroAmount");
  });

  it("should emit Deposit event", async function () {
    const { vault, alice } = await loadFixture(deployVaultFixture);

    await expect(
      vault.connect(alice).deposit({ value: ethers.parseEther("1.0") })
    )
      .to.emit(vault, "Deposit")
      .withArgs(alice.address, ethers.parseEther("1.0"));
  });
});
```

### Time Manipulation (Hardhat)

```typescript
import { time } from "@nomicfoundation/hardhat-network-helpers";

it("should unlock after timelock period", async function () {
  const { vault, alice } = await loadFixture(deployVaultFixture);
  await vault.connect(alice).deposit({ value: ethers.parseEther("1.0") });

  await time.increase(7 * 24 * 60 * 60); // fast-forward 7 days

  await expect(vault.connect(alice).withdraw(ethers.parseEther("1.0"))).to.not
    .be.reverted;
});

it("should revert before timelock expires", async function () {
  const { vault, alice } = await loadFixture(deployVaultFixture);
  await vault.connect(alice).deposit({ value: ethers.parseEther("1.0") });

  await time.increase(1 * 24 * 60 * 60); // only 1 day (lock is 7)

  await expect(
    vault.connect(alice).withdraw(ethers.parseEther("1.0"))
  ).to.be.revertedWithCustomError(vault, "TimelockNotExpired");
});
```

`loadFixture` snapshots EVM state after the first call and reverts to that snapshot for subsequent tests. This is faster than redeploying contracts in every test -- the Hardhat equivalent of Foundry's `setUp`.

## Common Cheatcodes Reference

| Cheatcode | Purpose | Scope |
|-----------|---------|-------|
| `vm.prank(addr)` | Next call as `addr` | Single call |
| `vm.startPrank(addr)` / `vm.stopPrank()` | All calls as `addr` until stopped | Multi-call |
| `vm.deal(addr, amount)` | Set ETH balance | Permanent |
| `deal(token, addr, amount)` | Set ERC20 balance (stdcheats) | Permanent |
| `vm.warp(timestamp)` | Set `block.timestamp` | Permanent |
| `vm.roll(blockNum)` | Set `block.number` | Permanent |
| `skip(seconds)` / `rewind(seconds)` | Advance / rewind timestamp | Permanent |
| `vm.expectRevert(...)` | Assert next call reverts | Next call |
| `vm.expectEmit(t1,t2,t3,d)` | Assert next event matches | Next emit |
| `vm.snapshotState()` / `vm.revertToState(id)` | Save / restore EVM state | -- |
| `vm.createSelectFork(rpc)` / `vm.selectFork(id)` | Fork chain / switch forks | Permanent |
| `vm.label(addr, name)` | Label address in traces | Traces |
| `makeAddr(name)` | Deterministic address from label | Pure |
| `vm.store(addr, slot, val)` / `vm.load(addr, slot)` | Write / read storage slot | Permanent |
| `vm.etch(addr, code)` | Set bytecode at address | Permanent |
| `vm.record()` / `vm.accesses(addr)` | Record and get storage access | -- |

## Testing Patterns

### Reentrancy Attack Test

```solidity
contract ReentrancyAttack {
    Vault target;
    uint256 attackCount;

    constructor(address _target) {
        target = Vault(payable(_target));
    }

    function attack() external payable {
        target.deposit{value: msg.value}();
        target.withdraw(msg.value);
    }

    receive() external payable {
        if (attackCount < 3) {
            attackCount++;
            target.withdraw(msg.value);
        }
    }
}

contract ReentrancyTest is Test {
    Vault vault;
    ReentrancyAttack attacker;

    function setUp() public {
        vault = new Vault();
        attacker = new ReentrancyAttack(address(vault));

        // Seed the vault with funds from legitimate depositors
        address depositor = makeAddr("depositor");
        vm.deal(depositor, 10 ether);
        vm.prank(depositor);
        vault.deposit{value: 10 ether}();
    }

    function test_RevertWhen_reentrancyAttempted() public {
        vm.deal(address(attacker), 1 ether);
        vm.expectRevert();
        attacker.attack{value: 1 ether}();
    }
}
```

### Access Control Test

```solidity
contract AccessControlTest is Test {
    ManagedVault vault;
    address owner = makeAddr("owner");
    address admin = makeAddr("admin");
    address user = makeAddr("user");

    function setUp() public {
        vm.startPrank(owner);
        vault = new ManagedVault();
        vault.grantRole(vault.ADMIN_ROLE(), admin);
        vm.stopPrank();
    }

    function test_ownerCanPause() public {
        vm.prank(owner);
        vault.pause();
        assertTrue(vault.paused());
    }

    function test_RevertWhen_userTriesToPause() public {
        vm.prank(user);
        vm.expectRevert();
        vault.pause();
    }

    function test_RevertWhen_adminTriesToUpgrade() public {
        vm.prank(admin);
        vm.expectRevert();
        vault.upgradeTo(address(0xdead));
    }
}
```

### UUPS Upgrade Test

```solidity
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";

contract UpgradeTest is Test {
    VaultV1 implV1;
    ERC1967Proxy proxy;
    address owner = makeAddr("owner");

    function setUp() public {
        vm.startPrank(owner);
        implV1 = new VaultV1();
        proxy = new ERC1967Proxy(
            address(implV1), abi.encodeCall(VaultV1.initialize, (owner))
        );
        vm.stopPrank();
    }

    function test_upgradePreservesState() public {
        vm.prank(owner);
        VaultV1(address(proxy)).setValue(42);

        vm.startPrank(owner);
        VaultV2 implV2 = new VaultV2();
        VaultV1(address(proxy)).upgradeToAndCall(address(implV2), "");
        vm.stopPrank();

        assertEq(VaultV2(address(proxy)).getValue(), 42);
    }

    function test_RevertWhen_nonOwnerUpgrades() public {
        vm.prank(makeAddr("attacker"));
        vm.expectRevert();
        VaultV1(address(proxy)).upgradeToAndCall(address(new VaultV2()), "");
    }
}
```

### Oracle Mock Pattern

```solidity
contract MockPriceFeed {
    int256 public price;
    uint256 public updatedAt;

    function setPrice(int256 _price) external {
        price = _price;
        updatedAt = block.timestamp;
    }

    function setStalePrice(int256 _price, uint256 staleness) external {
        price = _price;
        updatedAt = block.timestamp - staleness;
    }

    function latestRoundData()
        external
        view
        returns (uint80, int256, uint256, uint256, uint80)
    {
        return (0, price, 0, updatedAt, 0);
    }

    function decimals() external pure returns (uint8) { return 8; }
}

contract OracleDependentTest is Test {
    MockPriceFeed priceFeed;
    LiquidationEngine engine;

    function setUp() public {
        priceFeed = new MockPriceFeed();
        engine = new LiquidationEngine(address(priceFeed));
    }

    function test_liquidatesUnderwater() public {
        priceFeed.setPrice(1500e8);

        address borrower = makeAddr("borrower");
        vm.deal(borrower, 10 ether);
        vm.prank(borrower);
        engine.depositAndBorrow{value: 1 ether}(1000e6);

        priceFeed.setPrice(800e8);

        vm.prank(makeAddr("liquidator"));
        engine.liquidate(borrower);
        assertEq(engine.debtOf(borrower), 0);
    }

    function test_RevertWhen_oracleStale() public {
        priceFeed.setStalePrice(1500e8, 7200);
        vm.expectRevert(LiquidationEngine.StaleOracle.selector);
        engine.getPrice();
    }
}
```

## References

- [Foundry Book - Testing](https://book.getfoundry.sh/forge/tests) -- unit, fuzz, invariant, and fork testing
- [Foundry Cheatcodes](https://book.getfoundry.sh/cheatcodes/) -- full `vm.*` reference
- [Hardhat Testing Guide](https://hardhat.org/tutorial/testing-contracts) -- official Hardhat testing tutorial
- [hardhat-network-helpers](https://hardhat.org/hardhat-network-helpers/docs/overview) -- time, mine, snapshot, loadFixture
- [Chai Matchers for Hardhat](https://hardhat.org/hardhat-chai-matchers/docs/overview) -- revertedWith, emit, changeEtherBalance
- [Trail of Bits - Building Secure Contracts](https://secure-contracts.com/) -- invariant testing methodology
- [Foundry Invariant Testing Guide](https://book.getfoundry.sh/forge/invariant-testing) -- handler patterns, ghost variables
