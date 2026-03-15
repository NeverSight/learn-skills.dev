---
name: blockchain-auditor
description: Security audit smart contracts for exploitable vulnerabilities from an unprivileged context. Use when analyzing Solidity contracts, reviewing bytecode, testing exploits on forks, or searching for ways to extract funds without owner access. Covers verified and unverified contracts, bytecode disassembly, vulnerability ranking, and proof-of-concept exploit generation.
---

# Blockchain Security Auditor

Systematically audit smart contracts to identify exploitable vulnerabilities that allow an unprivileged account to extract funds or gain unauthorized access.

## Quick Start

```bash
# For verified contracts (Etherscan source available)
cast etherscan-source <address> --chain mainnet

# For unverified contracts (bytecode only)
cast code <address> --rpc-url $ETH_RPC_URL
cast disassemble <bytecode>

# Fork testing
forge test --fork-url $ETH_RPC_URL -vvv
```

## Audit Methodology

### Phase 1: Reconnaissance

1. **Gather contract information**:
   ```bash
   # Check balance
   cast balance <address> --rpc-url $ETH_RPC_URL

   # Get bytecode
   cast code <address> --rpc-url $ETH_RPC_URL

   # Check if verified on Etherscan
   curl "https://api.etherscan.io/api?module=contract&action=getsourcecode&address=<address>&apikey=$ETHERSCAN_API_KEY"
   ```

2. **Identify contract type**:
   - Multi-sig wallet (addOwner, execute, confirmTransaction)
   - Token contract (transfer, approve, balanceOf)
   - DeFi protocol (deposit, withdraw, swap)
   - Proxy pattern (implementation slot, delegatecall)
   - Custom contract

### Phase 2: Source Code Analysis (Verified Contracts)

1. **Identify high-risk functions**:
   - `selfdestruct` / `suicide` - can drain all ETH
   - `delegatecall` - can execute arbitrary code
   - `call` with user-controlled data - arbitrary calls
   - `transfer` / `send` without checks - reentrancy
   - `withdraw` / `claim` - fund extraction points

2. **Check access control patterns**:
   ```solidity
   // Weak patterns to look for:
   require(tx.origin == owner);     // tx.origin bypass
   require(msg.sender == owner);    // Check if owner is compromised
   // Missing modifier on sensitive function
   function withdraw() public {     // No onlyOwner!
       payable(msg.sender).transfer(address(this).balance);
   }
   ```

3. **Known vulnerability patterns**:
   - Reentrancy (state change after external call)
   - Integer overflow/underflow (Solidity < 0.8.0)
   - Unchecked return values
   - Front-running susceptibility
   - Flash loan attacks
   - Price oracle manipulation

### Phase 3: Bytecode Analysis (Unverified Contracts)

1. **Disassemble bytecode**:
   ```bash
   cast disassemble <bytecode> > contract.asm
   ```

2. **Extract function selectors**:
   ```bash
   # Look for PUSH4 followed by 4 bytes
   grep -oE '63[0-9a-f]{8}' contract.asm | cut -c3-10 | sort -u
   ```

3. **Look up signatures**:
   ```bash
   curl "https://www.4byte.directory/api/v1/signatures/?hex_signature=0x<selector>"
   ```

4. **Identify dangerous opcodes**:
   | Opcode | Hex | Risk |
   |--------|-----|------|
   | SELFDESTRUCT | `ff` | Critical - destroys contract |
   | DELEGATECALL | `f4` | High - arbitrary code execution |
   | CALL | `f1` | Medium - external calls |
   | CALLCODE | `f2` | High - deprecated, dangerous |
   | CREATE2 | `f5` | Medium - deterministic deployment |

5. **Analyze control flow**:
   - Find JUMPDEST locations for function entry points
   - Trace CALLER/ORIGIN checks for access control
   - Look for SLOAD/SSTORE patterns for state access

### Phase 4: Vulnerability Ranking

Rate each finding by exploitation likelihood given current blockchain state:

| Rating | Criteria | Action |
|--------|----------|--------|
| **Critical** | Directly exploitable now, high value | Immediate PoC |
| **High** | Exploitable with specific conditions met | Fork test |
| **Medium** | Requires unlikely conditions | Document |
| **Low** | Theoretical, conditions very unlikely | Note only |

**Factors affecting likelihood**:
- Current blockchain state (owner keys, time locks, balances)
- Required preconditions (deposits, approvals, block numbers)
- Gas costs vs potential gain
- MEV/frontrunning risks

### Phase 5: Fork Validation

1. **Set up Foundry test**:
   ```solidity
   // test/Exploit.t.sol
   pragma solidity ^0.8.20;
   import "forge-std/Test.sol";

   contract ExploitTest is Test {
       address target = 0x<TARGET_ADDRESS>;
       address attacker;

       function setUp() public {
           attacker = makeAddr("attacker");
           vm.deal(attacker, 1 ether);
       }

       function test_exploit() public {
           uint256 balanceBefore = attacker.balance;

           vm.prank(attacker);
           (bool success,) = target.call(abi.encodeWithSelector(0x<SELECTOR>));

           uint256 balanceAfter = attacker.balance;

           // CRITICAL: Verify actual fund extraction
           assertGt(balanceAfter, balanceBefore, "Exploit failed - no funds extracted");
       }
   }
   ```

2. **Run on fork**:
   ```bash
   forge test --fork-url $ETH_RPC_URL -vvvv --match-test "test_exploit"
   ```

3. **Verify fund extraction** (not just call success):
   - Check attacker balance increased
   - Verify target balance decreased
   - Confirm contract state changed as expected
   - **Call success does NOT mean exploit success**

### Phase 6: Report Generation

For confirmed vulnerabilities, create a report:

```markdown
# Vulnerability Report: [Contract Address]

## Summary
- **Severity**: Critical/High/Medium/Low
- **Type**: [Reentrancy/Access Control/etc.]
- **Impact**: [Amount at risk, what attacker gains]
- **Exploitable**: Yes/No (with current blockchain state)

## Vulnerable Function
\`\`\`solidity
function vulnerableFunction() public {
    // Vulnerable code
}
\`\`\`

## Attack Vector
1. Attacker calls function X with parameter Y
2. Contract fails to check Z
3. Funds transferred to attacker

## Proof of Concept
\`\`\`solidity
// Foundry test that demonstrates the exploit
function test_exploit() public {
    // Setup and exploit code
}
\`\`\`

## Execution Script (if confirmed)
\`\`\`bash
cast send <target> "vulnerableFunction()" --rpc-url $ETH_RPC_URL --private-key $PRIVATE_KEY
\`\`\`

## Remediation
- Add access control modifier
- Implement checks-effects-interactions pattern
- Use SafeMath for arithmetic
```

## Common Vulnerability Checklist

### Access Control
- [ ] All sensitive functions have proper modifiers
- [ ] Owner/admin addresses are not compromised
- [ ] Multi-sig requires sufficient confirmations
- [ ] Time locks are enforced
- [ ] No tx.origin authentication

### Reentrancy
- [ ] State changes before external calls
- [ ] ReentrancyGuard used on fund transfers
- [ ] No callbacks to untrusted contracts

### Arithmetic (Solidity < 0.8.0)
- [ ] SafeMath used for all operations
- [ ] No unchecked blocks with user input
- [ ] Proper bounds checking
- [ ] **Check for 0.5.x - 0.6.x overflow vulnerabilities**

### External Calls
- [ ] Return values checked
- [ ] Gas limits set appropriately
- [ ] Fallback/receive functions handled

### Oracle/Price Manipulation
- [ ] Multiple price sources used
- [ ] TWAP instead of spot price
- [ ] Flash loan protection

### Solidity Version-Specific Issues

| Version | Issue | Check |
|---------|-------|-------|
| < 0.8.0 | Integer overflow/underflow | SafeMath usage |
| < 0.6.0 | Constructor name confusion | `constructor()` keyword |
| < 0.5.0 | Uninitialized storage pointers | Variable declarations |
| Any | tx.origin authentication | Access control patterns |

## False Positive Indicators

Be aware of patterns that look exploitable but aren't:

1. **Multi-sig pending transactions**: `kill()` succeeds but requires N-of-M confirmations
2. **User-specific balances**: `withdraw()` only returns caller's deposited amount
3. **Time-locked releases**: Funds go to hardcoded address, not caller
4. **Proxy patterns**: Implementation has checks even if proxy doesn't
5. **Call success without transfer**: Function completes but no ETH moves

**ALWAYS verify actual fund movement on fork before concluding exploitability.**

## Tools Reference

| Tool | Purpose | Command |
|------|---------|---------|
| cast | RPC calls, disassembly | `cast code/call/send/disassemble` |
| forge | Fork testing | `forge test --fork-url` |
| 4byte.directory | Selector lookup | API or web |
| Etherscan | Source code, ABI | API or web |
| Slither | Static analysis | `slither .` |
| Mythril | Symbolic execution | `myth analyze` |

## Environment Setup

Required environment variables:
```bash
export ETH_RPC_URL="https://eth-mainnet.g.alchemy.com/v2/<KEY>"
export ETHERSCAN_API_KEY="<KEY>"
```

Required tools:
```bash
# Foundry (forge, cast, anvil)
curl -L https://foundry.paradigm.xyz | bash
foundryup

# Node.js (for Hardhat if needed)
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox
```

## Example Workflow

```bash
# 1. Check contract value and code
cast balance 0x<address> --rpc-url $ETH_RPC_URL
cast code 0x<address> --rpc-url $ETH_RPC_URL > bytecode.hex

# 2. Disassemble if unverified
cast disassemble $(cat bytecode.hex) > contract.asm

# 3. Extract and lookup selectors
grep -oE '63[0-9a-f]{8}' contract.asm | cut -c3-10 | sort -u | while read sel; do
  sig=$(curl -s "https://www.4byte.directory/api/v1/signatures/?hex_signature=0x$sel" | jq -r '.results[0].text_signature // "unknown"')
  echo "0x$sel: $sig"
done

# 4. Create and run fork test
forge test --fork-url $ETH_RPC_URL -vvvv

# 5. Verify fund extraction (not just call success!)

# 6. Generate report if confirmed exploitable
```

## Database Integration

When auditing multiple contracts, track findings in SQLite:

```sql
CREATE TABLE contracts (
  address TEXT PRIMARY KEY,
  balance_usd REAL,
  is_verified INTEGER,
  exploitable INTEGER DEFAULT 0,
  notes TEXT
);

-- Update after analysis
UPDATE contracts SET
  exploitable = 0,
  notes = 'Multi-sig wallet. kill() requires confirmations. NOT exploitable.'
WHERE address = '0x...';
```

## Security & Legal Notes

- Only test on forks, never mainnet without explicit authorization
- Document all findings, including false positives
- Consider responsible disclosure for live vulnerabilities
- Be aware of legal implications of exploit execution
- This skill is for authorized security research only
