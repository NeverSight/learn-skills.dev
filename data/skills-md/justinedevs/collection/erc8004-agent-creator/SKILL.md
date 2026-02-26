---
name: erc8004-agent-creator
description: Usage and installation for create-8004-agent (ERC-8004 / 8004 AI agent scaffold). Use when the user asks how to create an ERC-8004 or 8004 agent, how to install or run create-8004-agent, what wizard options mean, which chains are supported, what gets generated, or how to configure and register the generated project (env, npm run register, start:a2a, start:mcp). Covers EVM (Ethereum, Base, Polygon, Monad) and Solana.
license: See repository LICENSE
---

# erc8004-agent-creator

This skill provides usage, installation, and workflow guidance for [create-8004-agent](https://github.com/Eversmile12/create-8004-agent), the CLI that scaffolds ERC-8004 (EVM) and 8004 (Solana) AI agents with optional A2A, MCP, and x402.

## Overview

create-8004-agent is a CLI. No package install; run it once from any directory. The wizard prompts for project directory, agent name, description, image URL, chain, wallet (or leave empty to generate), features (A2A, MCP, x402), A2A streaming, and trust models. Node.js 18+ and npm/pnpm/bun required.

```bash
# Run the CLI (pin version when available for supply-chain safety)
npx create-8004-agent
# Or: npx create-8004-agent@<version>
```

**Security and trust:** This skill is documentation only; it does not execute commands or move funds. Users run `npx create-8004-agent` and any optional patch script themselves. Before running: (1) Verify the CLI source (official repo: [Eversmile12/create-8004-agent](https://github.com/Eversmile12/create-8004-agent)); (2) Prefer a pinned version when available, e.g. `npx create-8004-agent@<version>`; (3) Inspect `scripts/patch_anthropic.py` before use (it only writes under the project dir you pass; no path traversal); (4) Keep `.env` out of version control and use a secrets manager in production. See [SECURITY.md](SECURITY.md) for details.

## Wizard Options (Summary)

| Option | Description |
|--------|-------------|
| Project directory | Where to create the project (default `my-agent`) |
| Agent name / description / image | Metadata for the agent |
| Chain | EVM: eth-sepolia, base-sepolia, polygon-amoy, monad-testnet (+ mainnets). Solana: solana-devnet |
| Agent wallet | EVM or Solana address; leave empty to auto-generate |
| Features | A2A server, MCP server, x402 (x402 only on Base/Polygon) |
| A2A streaming | SSE for streaming responses (when A2A enabled) |
| Trust models | reputation, crypto-economic, tee-attestation |

For full wizard order and chain/feature matrix, see [references/wizard-options.md](references/wizard-options.md).

## What Gets Generated

- `package.json`, `tsconfig.json`, `.env` (with generated key if wallet empty)
- `src/register.ts`, `src/agent.ts` (LLM: OpenAI by default)
- Optional: `src/a2a-server.ts`, `src/a2a-client.ts`, `.well-known/agent-card.json` (if A2A); `src/mcp-server.ts`, `src/tools.ts` (if MCP)

## Usage After Generation

1. **Configure** – `cd <projectDir>`, edit `.env`: `PRIVATE_KEY` (or use generated), `OPENAI_API_KEY`, `PINATA_JWT` (pinata.cloud, pinJSONToIPFS scope). Back up `.env` if wallet was generated.
2. **Fund wallet** – Testnet ETH (Sepolia, Base Sepolia, etc.) or Solana Devnet SOL.
3. **Register on-chain** – `npm run register` (uploads metadata to IPFS, mints Identity Registry NFT). View on [8004scan.io](https://www.8004scan.io/).
4. **Start servers** – If A2A: `npm run start:a2a` (then set public URL in registration and run `npm run register` again if needed). If MCP: `npm run start:mcp`.
5. **Update agent** – Edit `src/register.ts` for name/description/image/skills, then run `npm run register` again.

## Optional: Customize LLM Provider

The generated project uses OpenAI in `src/agent.ts`. To switch to another LLM (e.g. Anthropic Claude), use the optional script: `python scripts/patch_anthropic.py <projectDir>` (projectDir must be a single path segment under the current directory; the script rejects `..` and path traversal). Then add `@anthropic-ai/sdk` in the project. Do not commit `.env`; it may contain API keys. See references for wizard details; the patch is optional.

## Resources

This skill follows the same structure as the skill-creator reference: optional bundled resources below.

### references/

- **wizard-options.md** – Wizard prompt order, chain keys, x402 availability. Read when mapping user choices to wizard answers or explaining chains/features.

### scripts/

- **patch_anthropic.py** – Optional: patches a generated project’s `src/agent.ts` and `.env` for Anthropic. Usage: `python scripts/patch_anthropic.py <projectDir>`.

### assets/

- **agent-anthropic.ts** – Template used by the patch script.
