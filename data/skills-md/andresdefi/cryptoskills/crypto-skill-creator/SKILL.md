---
name: crypto-skill-creator
description: >-
  Step-by-step guide for creating enriched CryptoSkills agent skills.
  Use when building new protocol skills, contributing to the directory,
  or understanding the enriched skill pattern. Covers SKILL.md structure,
  YAML frontmatter, examples, docs, resources, templates, marketplace
  registration, and validation. Triggers: "create a skill", "add a protocol",
  "contribute a skill", "new skill template".
license: Apache-2.0
compatibility: Claude Code, Cursor, Windsurf, Cline, Codex
metadata:
  author: cryptoskills
  version: "1.1"
  chain: multichain
  category: Dev Tools
tags:
  - skill-creation
  - contributing
  - agent-skills
  - developer-tooling
---

# Crypto Skill Creator

The definitive guide for creating agent skills for the CryptoSkills directory. Every skill in this directory follows the same enriched pattern — this skill teaches you exactly how to replicate it.

CryptoSkills follows the [agentskills.io](https://agentskills.io) spec. Skills are agent-agnostic and work with Claude Code, Cursor, Cline, Codex, and any compatible AI coding agent.

## What You Probably Got Wrong

- **"A skill is just a markdown file"** → An enriched skill is 10+ files across 5 directories: SKILL.md, 4 examples, docs, resources, and a starter template. The SKILL.md alone is 300-1500 lines.
- **"Any markdown format works"** → YAML frontmatter with specific required fields is mandatory. Categories and chains are validated against a whitelist — freeform values fail validation.
- **"Examples are optional nice-to-haves"** → Exactly 4 examples per skill, each in its own directory with a README.md. Every code block must be copy-paste ready and independently runnable.
- **"I can organize sections however I want"** → Section order is fixed. "What You Probably Got Wrong" must come before Quick Start. Contract Addresses need "Last verified" dates. The structure is enforced for consistency across 95+ skills.
- **"Just add it to the repo"** → Skills must be registered in `.claude-plugin/marketplace.json` (alphabetical order) and pass `validate-marketplace.ts` with 0 errors before merging.

## Skill Anatomy

Every enriched skill produces exactly this structure:

```
skills/<protocol>/
├── SKILL.md                              # Main skill (300-1500 lines)
├── docs/
│   └── troubleshooting.md                # Common issues + debug checklist (100-300 lines)
├── examples/
│   ├── <use-case-1>/README.md            # 4 examples, each 150-300 lines
│   ├── <use-case-2>/README.md
│   ├── <use-case-3>/README.md
│   └── <use-case-4>/README.md
├── resources/
│   ├── contract-addresses.md             # Multichain address tables
│   └── error-codes.md                    # Error reference with solutions
└── templates/
    └── <protocol>-client.ts              # Starter template (250-350 lines)
```

**Total: 10 files minimum** — 1 SKILL.md, 1 troubleshooting doc, 4 examples, 2 resources, 1 template.

## Step 1: Research the Protocol

Before writing anything, gather authoritative information:

1. **Official docs** — fetch the protocol's documentation site
2. **GitHub repos** — find SDKs, contract ABIs, deployment addresses
3. **Contract addresses** — verify onchain using `cast code <address>` or block explorer
4. **Existing skills** — read 1-2 similar skills in `skills/` for pattern reference

```bash
# Read a reference skill to see the pattern
cat skills/uniswap/SKILL.md | head -50

# Verify a contract address onchain
cast code 0x1F98431c8aD98523631AE4a59f267346ea31F984 --rpc-url $ETH_RPC_URL
```

Store your research — you'll need it for all 10 files.

## Step 2: Create Directory Structure

```bash
PROTOCOL=your-protocol-name
mkdir -p skills/$PROTOCOL/docs \
         skills/$PROTOCOL/examples \
         skills/$PROTOCOL/resources \
         skills/$PROTOCOL/templates
```

### Naming Rules
- **Protocol directory:** kebab-case, no `web3-` prefix (e.g., `uniswap`, `solana-agent-kit`, `account-abstraction`)
- **Example directories:** kebab-case describing the use case (e.g., `swap-exact-input`, `flash-loan`)
- **Resource files:** kebab-case (e.g., `contract-addresses.md`, `error-codes.md`)
- **Template file:** `<protocol>-client.ts` (e.g., `swap-client.ts`, `lending-client.ts`)

## Step 3: Write SKILL.md

The main skill file. 300-1500 lines of production-ready protocol knowledge.

### YAML Frontmatter (Required)

```yaml
---
name: protocol-name
description: >-
  What this skill does and when to use it. Include protocol name,
  key actions (swaps, lending, staking), and supported chains.
  Add trigger phrases so agents auto-activate (e.g., "Use when swapping tokens",
  "Triggers: lending, borrow, flash loan").
  Under 1024 characters total.
license: Apache-2.0
compatibility: Claude Code, Cursor, Windsurf, Cline
metadata:
  author: your-github-username
  version: "1.0"
  chain: ethereum
  category: DeFi
tags:
  - protocol-name
  - relevant-tag
  - another-tag
---
```

### Optional YAML Fields

These fields are not required but improve agent integration:

```yaml
# Declares which tools the skill needs (reduces permission prompts)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - WebFetch

# Declares agent/editor compatibility (1-500 chars)
compatibility: Claude Code, Cursor, Windsurf, Cline

# For skills that expose or depend on MCP servers
mcp-server:
  name: protocol-mcp
  transport: http
  url: https://api.protocol.com/mcp
```

### Allowed Values

**Categories (exact match required):**

| Category | Examples |
|----------|----------|
| DeFi | Uniswap, Aave, Compound, Curve, Lido |
| Infrastructure | The Graph, Account Abstraction, ENS |
| Dev Tools | Foundry, Hardhat, Tenderly, wagmi |
| Trading | DFlow, Hyperliquid, GMX, Polymarket |
| Oracles | Chainlink, Pyth, RedStone |
| Cross-Chain | LayerZero, Wormhole, Hyperlane, Axelar |
| NFT & Tokens | EVM NFTs, OpenZeppelin |
| Security | Slither, Echidna, Mythril, Certora |
| L2 & Alt-L1 | Arbitrum, Base, Optimism, Monad, MegaETH |
| Frontend | Privy, Frontend UX |
| AI Agents | Solana Agent Kit, Eliza, GOAT |
| DevOps | CI/CD, monitoring, deployment tools |

**Chains:**
`ethereum`, `solana`, `arbitrum`, `optimism`, `base`, `monad`, `megaeth`, `starknet`, `zksync`, `polygon`, `sui`, `aptos`, `sei`, `multichain`

### Description Format

Descriptions follow a 3-part pattern: **[What it does] + [When to use it] + [Key capabilities/triggers]**

```yaml
# BAD — too vague, no trigger phrases
description: A skill for Uniswap integration.

# GOOD — specific, includes trigger phrases for agent activation
description: >-
  Integrate Uniswap V3/V4 for token swaps, liquidity provision, and pool
  analytics on Ethereum, Arbitrum, and Base. Use when building DEX integrations,
  executing swaps, or reading pool state. Handles exact-input/output swaps,
  multi-hop routing, flash swaps, and LP position management.
```

Trigger phrases help agents decide when to activate the skill automatically. Include action verbs matching what developers actually ask for.

### Security Restrictions

These rules prevent conflicts with agent system prompts:

| Rule | Reason |
|------|--------|
| No XML angle brackets (`<tag>`) in SKILL.md body | Conflicts with Claude's system prompt parsing — use code blocks or backtick-escaped text instead |
| No `claude` or `anthropic` in the `name` field | Reserved namespace — your skill name cannot contain these strings |
| No `README.md` in skill root directory | Conflicts with SKILL.md as the canonical entry point — use SKILL.md only |
| No system prompt manipulation | Skills must not attempt to override agent behavior or inject system-level instructions |

### Section Order (Mandatory)

Follow this exact order. Do not skip or reorder sections:

### 1. Title (H1)

```markdown
# Protocol Name
```

Just the name. No subtitle or tagline.

### 2. Introduction (1-2 paragraphs)

What the protocol does, why it matters, and what agents can build with it.

### 3. What You Probably Got Wrong (CRITICAL)

**Never skip this section.** Corrects LLM stale training data and common hallucinations.

```markdown
## What You Probably Got Wrong

- **V2 uses `deposit()`** → V3 renamed it to `supply()`. Using `deposit()` will revert on V3 contracts (Aave docs, 2023).
- **Fee is 0.3%** → Fee encoding uses basis points: `3000` = 0.30%, `500` = 0.05%. Not percentages (Uniswap V3 docs).
- **Health factor is a percentage** → It's an 18-decimal fixed-point number. `1e18` = 1.0, not 100% (Aave V3 source).
```

Include 3-8 corrections. Each follows the pattern:
`**Wrong assumption** → Correct fact (source/date)`

What to correct:
- Deprecated function names (version migrations)
- Changed fee structures or parameters
- New contract addresses replacing old ones
- Architecture changes (singleton vs factory, etc.)
- Common hallucinated patterns that don't exist

### 4. Quick Start

```markdown
## Quick Start

### Installation

\`\`\`bash
npm install @protocol/sdk viem
\`\`\`

### Basic Setup

\`\`\`typescript
import { createPublicClient, http } from "viem";
import { mainnet } from "viem/chains";

const client = createPublicClient({
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});
\`\`\`
```

Include installation command, basic client setup, and 2 minimal working code snippets.

### 5. Core Concepts / Patterns (3-5 sections)

Deep-dive subsections with working code. Every code block must be independently runnable.

### 6. Contract Addresses

```markdown
## Contract Addresses

> **Last verified:** March 2026 (verified via `cast code` on mainnet)

| Contract | Ethereum | Arbitrum | Base |
|----------|----------|----------|------|
| Factory | `0x1F98431c8aD98523631AE4a59f267346ea31F984` | `0x1F98...` | `0x33...` |
| Router | `0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45` | `0x68b3...` | `0x2626...` |
```

Requirements:
- All addresses checksummed (mixed case for EVM)
- Include "Last verified" date in blockquote
- Note verification method (`cast code`, `eth_getCode`, block explorer)
- Group by contract type and version

### 7. Common Patterns

Advanced use cases with working code: multi-hop swaps, flash loans, batching, permit flows, etc.

### 8. Error Handling

```markdown
## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `INSUFFICIENT_LIQUIDITY` | Pool has insufficient reserves | Check pool state before swap |
| `SLIPPAGE_EXCEEDED` | Price moved beyond tolerance | Increase slippage or reduce size |
```

### 9. Security / Best Practices

5-10 bullets covering slippage protection, approval patterns, deadline handling, key management.

### 10. Skill Structure

Show the file tree of this skill's directory.

### 11. Guidelines

5-7 actionable rules for using this skill.

### 12. References

Primary sources only — official docs, GitHub repos, governance forums.

## Step 4: Write Examples

Create exactly **4 examples**, each in its own directory.

```
examples/
├── use-case-1/README.md
├── use-case-2/README.md
├── use-case-3/README.md
└── use-case-4/README.md
```

### Example Naming by Category

| Category | Example Names |
|----------|---------------|
| DEX / Swap | `swap-exact-input`, `multi-hop-swap`, `add-liquidity`, `read-pool-state` |
| Lending | `supply-borrow`, `flash-loan`, `read-account-data`, `e-mode` |
| Multisig | `create-safe`, `propose-transaction`, `batch-transactions`, `module-setup` |
| Staking | `stake-lst`, `delegate-stake`, `register-operator`, `create-avs` |
| Bridge | `bridge-eth`, `bridge-erc20`, `check-status`, `estimate-fees` |

### README.md Format

```markdown
# Use Case Title

Brief description of what this example demonstrates.

## Prerequisites

\`\`\`bash
npm install viem @protocol/sdk
\`\`\`

## Setup

\`\`\`typescript
import { createPublicClient, createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { mainnet } from "viem/chains";

const account = privateKeyToAccount(process.env.PRIVATE_KEY as \`0x\${string}\`);
// ... client setup
\`\`\`

## Step 1: Description

\`\`\`typescript
// Working code for step 1
\`\`\`

## Step 2: Description

\`\`\`typescript
// Working code for step 2
\`\`\`

## Complete Example

\`\`\`typescript
// Full working example — copy-paste ready
async function main() {
  // All steps combined into runnable code
}

main().catch(console.error);
\`\`\`
```

**Each README.md should be 150-300 lines.** Each example must be independently runnable — copy, set env vars, execute.

## Step 5: Write Docs

### docs/troubleshooting.md (Required)

100-300 lines covering 5-8 common issues.

```markdown
# Troubleshooting

## Transaction Reverts with No Error Message

**Symptoms:**
- Transaction reverts with empty data or generic "execution reverted"
- No specific error code returned

**Cause:**
- Missing token approval
- Incorrect function parameters
- Contract paused or deprecated

**Solution:**

1. Simulate the transaction first:
\`\`\`typescript
const { request } = await publicClient.simulateContract({
  address: routerAddress,
  abi: routerAbi,
  functionName: "swap",
  args: [params],
  account,
});
\`\`\`

2. Check token approvals:
\`\`\`typescript
const allowance = await publicClient.readContract({
  address: tokenAddress,
  abi: erc20Abi,
  functionName: "allowance",
  args: [account.address, spenderAddress],
});
\`\`\`

## [Next Issue]
...

## Debug Checklist

- [ ] Correct network/chain?
- [ ] Contract addresses verified onchain?
- [ ] Sufficient token balance + approval?
- [ ] Slippage set appropriately?
- [ ] Gas/priority fees adequate?
- [ ] Using latest SDK version?
```

## Step 6: Write Resources

### resources/contract-addresses.md (Required)

```markdown
# Contract Addresses

> **Last verified:** March 2026
> **Verification:** `cast code <address> --rpc-url $RPC_URL`

## Core Contracts

| Contract | Ethereum | Arbitrum | Base |
|----------|----------|----------|------|
| Factory | `0x...` | `0x...` | `0x...` |
| Router | `0x...` | `0x...` | `0x...` |

## Common Tokens

| Token | Mint / Address |
|-------|---------------|
| USDC | `0x...` |
| WETH | `0x...` |

## Deprecated (Do Not Use)

| Contract | Address | Replaced By |
|----------|---------|-------------|
| RouterV1 | `0x...` | RouterV2 `0x...` |
```

### resources/error-codes.md (Required)

```markdown
# Error Codes

| Code | Name | Cause | Fix |
|------|------|-------|-----|
| 1 | `INSUFFICIENT_INPUT` | Input amount too low | Increase amount or check decimals |
| 2 | `SLIPPAGE_EXCEEDED` | Price moved beyond tolerance | Retry with higher slippage |
```

### Additional Resources (as needed)

- `fee-tiers.md` — for DEXes (tick spacing, fee encoding)
- `reserve-config.md` — for lending (LTV, liquidation thresholds)
- `service-urls.md` — for multi-service protocols (API endpoints per chain)
- `token-mints.md` — for Solana protocols (SPL token mints)

## Step 7: Write Template

One starter file: `templates/<protocol>-client.ts` (250-350 lines).

```typescript
/**
 * Protocol Name Client Template
 *
 * Complete starter for [protocol] integration using viem.
 *
 * Features:
 * - Operation A (e.g., swap tokens)
 * - Operation B (e.g., add liquidity)
 * - Operation C (e.g., read pool state)
 *
 * Usage:
 * 1. Copy this file to your project
 * 2. Set RPC_URL and PRIVATE_KEY environment variables
 * 3. Import and use the exported functions/class
 *
 * Dependencies: viem
 */

import {
  createPublicClient,
  createWalletClient,
  http,
  parseAbi,
  type Address,
} from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { mainnet } from "viem/chains";

// ============================================================================
// Configuration
// ============================================================================

const RPC_URL = process.env.RPC_URL;
const PRIVATE_KEY = process.env.PRIVATE_KEY as `0x${string}` | undefined;

if (!RPC_URL) throw new Error("RPC_URL environment variable is required");

// ============================================================================
// Contract Addresses
// ============================================================================

const ADDRESSES = {
  router: "0x..." as Address,
  factory: "0x..." as Address,
} as const;

// ============================================================================
// ABIs
// ============================================================================

const routerAbi = parseAbi([
  "function swap(address tokenIn, address tokenOut, uint256 amountIn, uint256 amountOutMin, address recipient, uint256 deadline) external returns (uint256 amountOut)",
]);

const erc20Abi = parseAbi([
  "function approve(address spender, uint256 amount) external returns (bool)",
  "function balanceOf(address account) external view returns (uint256)",
  "function allowance(address owner, address spender) external view returns (uint256)",
]);

// ============================================================================
// Clients
// ============================================================================

export const publicClient = createPublicClient({
  chain: mainnet,
  transport: http(RPC_URL),
});

const account = PRIVATE_KEY ? privateKeyToAccount(PRIVATE_KEY) : undefined;

export const walletClient = account
  ? createWalletClient({
      account,
      chain: mainnet,
      transport: http(RPC_URL),
    })
  : undefined;

// ============================================================================
// Core Functions
// ============================================================================

export async function operationA(/* params */) {
  // Implementation with simulateContract + writeContract pattern
}

export async function operationB(/* params */) {
  // Implementation
}

// ============================================================================
// Example Usage
// ============================================================================

async function main() {
  // Realistic example showing the template in action
}

main().catch(console.error);
```

The template must be fully functional — copy, set env vars, run.

## Step 8: Register in Marketplace

### 1. Add to marketplace.json

Insert entry in `.claude-plugin/marketplace.json` in **alphabetical order by name**:

```json
{
  "name": "protocol-name",
  "source": "./skills/protocol-name",
  "description": "Same text as SKILL.md frontmatter description",
  "category": "DeFi"
}
```

### 2. Validate

```bash
npx tsx scripts/validate-marketplace.ts
```

Must output: `0 errors, 0 warnings`

The validator checks:
- Required fields present (`name`, `source`, `description`, `category`)
- Description under 1024 characters
- Category in allowed list
- Corresponding `skills/<name>/SKILL.md` exists
- No duplicate names
- Alphabetical ordering

### 3. Build Registry

```bash
npx tsx scripts/build-registry.ts
```

Generates `_registry.json` (gitignored — never commit this file).

## Verify Your Skill

Before submitting, run these 4 test types:

### 1. Triggering Test

Does your skill activate when expected? Ask an agent a question your skill should answer — without mentioning the skill name.

```
# If your skill is "uniswap", try:
"How do I swap USDC for WETH on Arbitrum?"

# The agent should pull in your skill based on description trigger phrases.
# If it doesn't activate, improve your description's trigger phrases.
```

### 2. Functional Test

Install the skill and run through its core use cases:

```bash
npx cryptoskills install your-protocol
```

Then ask the agent to perform 3-5 tasks the skill covers. Verify:
- Code blocks from SKILL.md work when pasted
- Contract addresses resolve onchain
- Error handling matches the documented error table
- Examples produce the expected output

### 3. Accuracy Test

Have the agent answer protocol questions **with** and **without** the skill installed. The skill should:
- Correct at least 1 "What You Probably Got Wrong" item
- Produce working code that fails without the skill's guidance
- Reference correct contract addresses (not hallucinated ones)

### 4. Structure Validation

```bash
# Marketplace validates metadata, categories, descriptions
npx tsx scripts/validate-marketplace.ts

# Build confirms registry generation works
npx tsx scripts/build-registry.ts
```

Both must pass with 0 errors. Fix any issues before submitting.

## Code Quality Rules

These are non-negotiable across all skills:

| Rule | Rationale |
|------|-----------|
| Every code block copy-paste ready | Agents paste code directly — broken snippets break trust |
| TypeScript with explicit types | Type safety prevents runtime errors |
| No `any`, `@ts-ignore`, `@ts-expect-error` | Suppressing types hides real bugs |
| `bigint` for token amounts | JS `number` loses precision above 2^53 |
| `Address` type (`0x${string}`) for addresses | Type-level validation catches wrong strings |
| Check `receipt.status` after transactions | Silent reverts are the #1 missed failure mode |
| Slippage protection on all swaps | `amountOutMinimum = 0n` is a guaranteed sandwich attack |
| Deadlines on time-sensitive ops | Stale transactions can execute at unfavorable prices |
| `simulateContract` before `writeContract` | Catches reverts before spending gas |
| No hardcoded secrets | `process.env` for all keys, URLs, and credentials |
| Addresses checksummed and verified | Wrong address = lost funds |
| Comments explain WHY, not WHAT | Code is self-documenting for what; comments explain business logic |

## Commit Convention

When submitting a skill as a PR, use 4 commits:

```
feat: add <skill-name> skill              # SKILL.md only
feat: add <skill-name> examples           # all examples/
feat: add <skill-name> docs and resources  # docs/ + resources/
feat: add <skill-name> starter template   # templates/
```

Then the marketplace update:
```
chore: update marketplace registry with <skill-name>
```

## Completion Checklist

Before submitting your PR:

- [ ] 10+ files created (SKILL.md, docs, 4 examples, 2+ resources, 1 template)
- [ ] SKILL.md is 300-1500 lines with ALL mandatory sections in correct order
- [ ] "What You Probably Got Wrong" section has 3+ corrections
- [ ] YAML frontmatter valid — category in allowed list, description under 1024 chars
- [ ] Description includes trigger phrases (what + when + capabilities)
- [ ] No XML angle brackets in SKILL.md body, no `README.md` in skill root
- [ ] All code blocks tested and copy-paste ready
- [ ] Contract addresses verified onchain with "Last verified" date
- [ ] No hardcoded secrets anywhere
- [ ] Triggering test passed (agent activates skill from natural question)
- [ ] Functional test passed (code blocks work when pasted)
- [ ] Marketplace entry added in alphabetical order
- [ ] `validate-marketplace.ts` passes (0 errors)
- [ ] `build-registry.ts` succeeds

## Distribution

Once your skill is merged, it's available through multiple channels:

| Channel | How |
|---------|-----|
| **CLI** | `npx cryptoskills install your-protocol` — writes to `.claude/skills/` |
| **Website** | Listed on [cryptoskills.dev](https://cryptoskills.dev) with search, filters, and view counts |
| **GitHub** | Direct install from `github.com/0xinit/cryptoskills/tree/main/skills/your-protocol` |
| **Claude.ai** | Upload SKILL.md directly via the Claude.ai project knowledge feature |
| **Skills API** | Available via Anthropic's `/v1/skills` endpoint and `container.skills` for Agent SDK users |

For maximum reach, ensure your `description` field has strong trigger phrases — this is what agents use to decide whether to activate your skill.

## References

- [CryptoSkills GitHub](https://github.com/0xinit/cryptoskills)
- [Contributing Guide](https://github.com/0xinit/cryptoskills/blob/main/CONTRIBUTING.md)
- [Skill Template](https://github.com/0xinit/cryptoskills/blob/main/template/SKILL.md)
- [Agent Skills Spec](https://agentskills.io)
- [Anthropic Skill Guide](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)
- [cryptoskills.dev](https://cryptoskills.dev)
