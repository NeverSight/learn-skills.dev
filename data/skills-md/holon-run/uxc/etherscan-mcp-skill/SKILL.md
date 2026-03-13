---
name: etherscan-mcp-skill
description: Use Etherscan MCP through UXC for address balance checks, token holder analysis, transaction inspection, and contract lookup tasks. Use when tasks need Etherscan MCP tools for onchain investigation with help-first schema inspection, bearer-key auth, and tier-aware read-first handling.
---

# Etherscan MCP Skill

Use this skill to run Etherscan MCP operations through `uxc`.

Reuse the `uxc` skill for shared protocol discovery, output parsing, and generic auth/binding flows.

## Prerequisites

- `uxc` is installed and available in `PATH`.
- Network access to `https://mcp.etherscan.io/mcp`.
- An Etherscan API key is available for authenticated calls.

## Core Workflow

1. Confirm endpoint and protocol with help-first probing:
   - `uxc https://mcp.etherscan.io/mcp -h`
   - expected unauthenticated behavior today: `401 Unauthorized`
2. Configure credential/binding for repeatable auth:
   - `uxc auth credential set etherscan-mcp --auth-type bearer --secret-env ETHERSCAN_API_KEY`
   - `uxc auth credential set etherscan-mcp --auth-type bearer --secret-op op://Engineering/etherscan/api-key`
   - `uxc auth binding add --id etherscan-mcp --host mcp.etherscan.io --path-prefix /mcp --scheme https --credential etherscan-mcp --priority 100`
3. Use fixed link command by default:
   - `command -v etherscan-mcp-cli`
   - If missing, create it: `uxc link etherscan-mcp-cli https://mcp.etherscan.io/mcp`
   - `etherscan-mcp-cli -h`
4. Inspect operation schema before execution:
   - `etherscan-mcp-cli balance -h`
   - `etherscan-mcp-cli tokenTopHolders -h`
   - `etherscan-mcp-cli getContractAbi -h`
   - `etherscan-mcp-cli transaction -h`
5. Prefer read operations first, then any workflow that could trigger heavy data pulls or follow-up automation.

## Capability Map

- Address investigation:
  - `balance`
  - `tokenHoldings`
  - `fundedBy`
  - `getAddressMetadata`
- Token holder analysis:
  - `balanceERC20`
  - `balanceERC20Historical`
  - `tokenTopHolders`
  - `getTokenInfo`
- Transaction investigation:
  - `txList`
  - `internalTxsByAddress`
  - `erc20Transfers`
  - `erc721Transfers`
  - `erc1155Transfers`
  - `transaction`
  - `checkTransaction`
- Contract research:
  - `getContractAbi`
  - `getContractSourceCode`
  - `getContractCreation`
- Verification:
  - `verifySourceCode`
  - `checkVerifyStatus`

Inspect `etherscan-mcp-cli -h` after auth setup for the current full tool list. Etherscan can expand MCP tools independently of this wrapper skill.

## Recommended Usage Pattern

1. Start from a read-only investigation goal:
   - balance or holdings for an address
   - holder concentration for a token
   - transaction inspection for a hash
   - source/metadata lookup for a contract
2. Run `-h` on the specific tool before the first real call.
3. Prefer one chain/address/token at a time before broadening the scope.
4. Parse the JSON envelope first, then inspect `data`.

## Guardrails

- Keep automation on JSON output envelope; do not rely on `--text`.
- Parse stable fields first: `ok`, `kind`, `protocol`, `data`, `error`.
- Use `etherscan-mcp-cli` as default command path.
- `etherscan-mcp-cli <operation> ...` is equivalent to `uxc https://mcp.etherscan.io/mcp <operation> ...`.
- If unauthenticated probe or runtime call returns `401 Unauthorized`:
  - confirm auth binding matches endpoint with `uxc auth binding match https://mcp.etherscan.io/mcp`
  - confirm credential shape with `uxc auth credential info etherscan-mcp`
  - reset credential as bearer if needed: `uxc auth credential set etherscan-mcp --auth-type bearer --secret-env ETHERSCAN_API_KEY`
- Use `key=value` only for simple scalar inputs.
- Prefer positional JSON when an operation accepts nested objects, arrays, or optional flags that may evolve.
- Do not assume tool argument names from memory; inspect `<operation> -h` first because Etherscan may revise MCP schemas independently of this skill.
- Some MCP tools are tier-gated by Etherscan plan. Today `getTokenInfo` can return `NOTOK` with an API Pro upgrade message on non-Pro keys.
- Treat `verifySourceCode` as a write-like action requiring explicit user confirmation.

## References

- Invocation patterns:
  - `references/usage-patterns.md`
