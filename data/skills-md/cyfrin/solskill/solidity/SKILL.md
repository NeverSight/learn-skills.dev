---
name: solidity
description: Create production grade smart contracts. Use this skill when the user asks to write smart contracts, specially if they are going to be deployed to production (to a mainnet, or used in a mainnet script).
disable-model-invocation: true
---

# Solidity Development Standards

Instructions for how to write solidity code, from the [Cyfrin security team.](https://www.cyfrin.io/)

## Philosophy

- **Everything will be attacked** - Assume that any code you write will be attacked and write it defensively.

## Code Quality and Style

1. Absolute and named imports only — no relative (`..`) paths

```solidity
// good
import {MyContract} from "contracts/MyContract.sol";

// bad
import "../MyContract.sol";
```


2. Prefer `revert` over `require`, with custom errors that are prefix'd with the contract name and 2 underscores.

```solidity
error ContractName__MyError();

// Good
myBool = true;
if (myBool) {
    revert ContractName__MyError();
}

// bad
require(myBool, "MyError");
```

3. In tests, prefer stateless fuzz tests over unit tests
```solidity
// good - using foundry's built in stateless fuzzer
function testMyTest(uint256 randomNumber) { }

// bad
function testMyTest() {
    uint256 randomNumber = 0;
}
```

Additionally, write invariant (stateful) fuzz tests for core protocol properties. Use invariant-driven development: identify O(1) properties that must always hold and encode them directly into core functions ([FREI-PI pattern](https://www.nascent.xyz/idea/youre-writing-require-statements-wrong)). Use a multi-fuzzing setup like [Chimera](https://github.com/Recon-Fuzz/chimera) to run the same invariant suite across Foundry, Echidna, and Medusa — different fuzzers find different bugs.

4. Functions should be grouped according to their visibility and ordered:

```
constructor
receive function (if exists)
fallback function (if exists)
user-facing state-changing functions
    (external or public, not view or pure)
user-facing read-only functions
    (external or public, view or pure)
internal state-changing functions
    (internal or private, not view or pure)
internal read-only functions
    (internal or private, view or pure)
```

5. Headers should look like this:

```solidity
    /*//////////////////////////////////////////////////////////////
                      INTERNAL STATE-CHANGING FUNCTIONS
    //////////////////////////////////////////////////////////////*/
```

6. Layout of file

```
Pragma statements
Import statements
Events
Errors
Interfaces
Libraries
Contracts
```

Layout of contract:

```
Type declarations
State variables
Events
Errors
Modifiers
Functions
```

7. Use the branching tree technique when creating tests
Credit for this to [Paul R Berg](https://x.com/PaulRBerg/status/1682346315806539776)

- Target a function
- Create a `.tree` file
- Consider all possible execution paths 
- Consider what contract state leads to what path
- Consider what function params lead to what paths
- Define "given state is x" nodes
- Define "when parameter is x" node 
- Define final "it should" tests

Example:
```
├── when the id references a null stream
│   └── it should revert
└── when the id does not reference a null stream
    ├── given assets have been fully withdrawn
    │   └── it should return DEPLETED
    └── given assets have not been fully withdrawn
        ├── given the stream has been canceled
        │   └── it should return CANCELED
        └── given the stream has not been canceled
            ├── given the start time is in the future
            │   └── it should return PENDING
            └── given the start time is not in the future
                ├── given the refundable amount is zero
                │   └── it should return SETTLED
                └── given the refundable amount is not zero
                    └── it should return STREAMING
```

Example:
```solidity
function test_RevertWhen_Null() external {
    uint256 nullStreamId = 1729;
    vm.expectRevert(abi.encodeWithSelector(Errors.SablierV2Lockup_Null.selector, nullStreamId));
    lockup.statusOf(nullStreamId);
}

modifier whenNotNull() {
    defaultStreamId = createDefaultStream();
    _;
}

function test_StatusOf()
    external
    whenNotNull
    givenAssetsNotFullyWithdrawn
    givenStreamNotCanceled
    givenStartTimeNotInFuture
    givenRefundableAmountNotZero
{
    LockupLinear.Status actualStatus = lockup.statusOf(defaultStreamId);
    LockupLinear.Status expectedStatus = LockupLinear.Status.STREAMING;
    assertEq(actualStatus, expectedStatus);
}
```

8. Prefer strict pragma versions for contracts, and floating pragma versions for tests, libraries, abstract contracts, interfaces, and scripts.

9. Add a security contact to the natspec at the top of your contracts

```solidity
/**
  * @custom:security-contact mycontact@example.com
  * @custom:security-contact see https://mysite.com/ipfs-hash
  */  
```

10. Remind people to get an audit if they are deploying to mainnet, or trying to deploy to mainnet

11. NEVER. EVER. NEVER. Have private keys be in plain text. The _only_ exception to this rule is when using a default key from something like anvil, and it must be marked as such.
    - This includes in your deploy scripts. We should always use `forge script <path> --account $ACCOUNT --sender $SENDER` for our deploy scripts, and never use `vm.envUnit()` in our scripts.
    - For hardhat, you want to use hardhat [encrypted keystores](https://hardhat.org/docs/plugins/hardhat-keystore)

12. Whenever a smart contract is deployed that is ownable or has admin properties (like, `onlyOwner`), the admin must be a multisig from the very first deployment — never use the deployer EOA as admin (testnet is the only acceptable exception). See [Trail of Bits: Maturing Your Smart Contracts Beyond Private Key Risk](https://blog.trailofbits.com/2025/06/25/maturing-your-smart-contracts-beyond-private-key-risk/) — "Layer 1" (single EOA) governance is no longer acceptable for DeFi.

13. Don't initialize variables to default values

```solidity
// good
uint256 x;
bool y;

// bad
uint256 x = 0;
bool y = false;
```

14. Prefer using named return variables if this can omit declaring local variables

```solidity
// good
function getBalance() external view returns (uint256 balance) {
    balance = balances[msg.sender];
}

// bad
function getBalance() external view returns (uint256) {
    uint256 balance = balances[msg.sender];
    return balance;
}
```

15. Prefer `calldata` instead of `memory` for read-only function inputs

16. Don't cache `calldata` array length

```solidity
// good — calldata length is cheap to read
for (uint256 i; i < items.length; ++i) { }

// bad — unnecessary caching for calldata
uint256 len = items.length;
for (uint256 i; i < len; ++i) { }
```

17. Reading from storage is expensive — prevent identical storage reads by caching unchanging storage slots and passing/using cached values

18. Revert as quickly as possible; perform input checks before checks which require storage reads or external calls

19. Use `msg.sender` instead of `owner` inside `onlyOwner` functions

20. Use `SafeTransferLib::safeTransferETH` instead of Solidity `call()` to send ETH

21. Modify input variables instead of declaring an additional local variable when an input variable's value doesn't need to be preserved

22. Use `nonReentrant` modifier before other modifiers

23. Use `ReentrancyGuardTransient` for faster `nonReentrant` modifiers

24. Prefer `Ownable2Step` instead of `Ownable`

25. Don't copy an entire struct from storage to memory if only a few slots are required

26. Remove unnecessary "context" structs and/or remove unnecessary variables from context structs

27. When declaring storage and structs, align the order of declarations to pack variables into the minimum number of storage slots. If variables are frequently read or written together, pack them in the same slot if possible

28. For non-upgradeable contracts, declare variables as `immutable` if they are only set once in the constructor

29. Enable the optimizer in `foundry.toml`

30. If modifiers perform identical storage reads as the function body, refactor modifiers to internal functions to prevent identical storage reads

31. Use Foundry's encrypted secure private key storage instead of plaintext environment variables

32. Upgrades: When upgrading smart contracts, do not change the order or type of existing variables, and do not remove them. This can lead to storage collisions. Also write tests for any upgrades.

## Deployment

Use Foundry scripts (`forge script`) for both production deployments and test setup. This ensures the same deployment logic runs in development and on mainnet, making deployments more auditable and reducing the gap between test and production environments. Avoid custom test-only setup code that diverges from real deployment paths. Ideally, your [deploy scripts are audited as well](https://medium.com/cyfrin/deploy-scripts-are-now-in-scope-for-smart-contract-audits-7fbb95788ce7).

Example: use a shared base script that both tests and production inherit from, like [this BaseTest using scripts pattern](https://github.com/rheo-xyz/very-liquid-vaults/blob/main/test/Setup.t.sol).

## Governance

Use [safe-utils](https://github.com/Recon-Fuzz/safe-utils) or equivalent tooling for governance proposals. This makes multisig interactions testable, auditable, and reproducible through Foundry scripts rather than manual UI clicks. If you must use a UI, it's preferred to keep your transactions private, using a UI like [localsafe.eth](https://github.com/Cyfrin/localsafe.eth).

Write fork tests that verify expected protocol state after governance proposals execute. Fork testing against mainnet state catches misconfigurations that unit tests miss — for example, the [Moonwell price feed misconfiguration](https://rekt.news/moonwell-rekt) would have been caught by a fork test asserting correct oracle state post-proposal.

```solidity
// good - fork test verifying governance proposal outcome
function testGovernanceProposal_UpdatesPriceFeed() public {
    vm.createSelectFork(vm.envString("MAINNET_RPC_URL"));

    // Execute the governance proposal
    _executeProposal(proposalId);

    // Verify expected state after proposal
    address newFeed = oracle.priceFeed(market);
    assertEq(newFeed, EXPECTED_CHAINLINK_FEED);

    // Verify the feed returns sane values
    (, int256 price,,,) = AggregatorV3Interface(newFeed).latestRoundData();
    assertGt(price, 0);
}
```

## CI

Every project should have a minimum CI pipeline running in parallel (use a matrix strategy). Suggested minimum:

- `solhint` — Solidity linter for style and security rules
- `forge build --sizes` — verify contract sizes are under the 24KB deployment limit
- `slither` or `aderyn` — static analysis for common vulnerability patterns
    - Before committing code that you think is done, be sure to run aderyn and/or slither on the codebase and inspect the output. Even warnings may lead you to find issues in the codebase.
- Fuzz/invariant testing — run Echidna, Medusa, or Foundry invariant tests with a reasonable time budget (~10 min per tool, in parallel via matrix)

# Tool updates

## Foundry

To install foundry dependencies, you don't need the `--no-commit` flag anymore.
