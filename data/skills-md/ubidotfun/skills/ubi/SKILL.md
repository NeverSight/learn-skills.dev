---
name: ubi
description: Route to the right ubi.fun skill. Use when the user mentions ubi.fun, $UBI, or trading or launching tokens on Arc. ubi.fun is a token launchpad on Arc mainnet (chain 5042, USDC gas) where tokens launched with a creator vault (all since October 4, 2026) pay their holders USDC, the platform's fees pay daily USDC to $UBI holders, and whoever routes a swap earns 5% of its fee on-chain.
---

# ubi.fun

Umbrella skill. Pick the deeper skill that matches the job:

- **Trade tokens, quote prices, discover markets, earn the 5% referrer share, collect dividends, creator earnings and rewards, write or read notes, follow another wallet's note** → `ubi-trading`
- **Launch a token (image, metadata, creator vault, one transaction), USDC-paired, or v3 paired with an asset (gold today)** → `ubi-launch`
- **Let the agent send the transactions itself from a Circle Agent Wallet** → `ubi-circle`

## Facts that apply everywhere

- Chain: Arc mainnet, chain id `5042`. Gas is USDC. The cash side of every pool is USDC (6 decimals); tokens have 18 decimals and a fixed 100 billion supply. v3 tokens (since October 17, 2026) pair with an asset instead, gold (XAUm) today, and have 1 billion supply; you still trade them in USDC, through their route. Fund the wallet with USDC on Arc first (https://ubi.fun/bridge moves USDC from other chains over Circle CCTP).
- MCP server: `https://api.ubi.fun/mcp` (Streamable HTTP, no API key). Connect with:
  - Claude Code: `claude mcp add --transport http ubi https://api.ubi.fun/mcp`
  - Generic config: `{ "mcpServers": { "ubi": { "type": "http", "url": "https://api.ubi.fun/mcp" } } }`
- Trust model: the MCP never requests, stores, or uses wallet keys, and never sends transactions. Tools named `prepare_*` return unsigned `{ chainId, to, data, value }` steps; simulate, sign, and send them with your own wallet tooling.
- Fees: every token launched since October 4, 2026 has a creator vault and a trading fee of 1.5% to 5%, fixed at launch; older tokens pay 1.25%. A referrer named on a swap takes 5% of its fee first, on every token. On vault tokens the rest settles to 77% creator side (the creator, the token's holders, and its buyback), 13% $UBI holders, 10% protocol. v3 tokens set a buy fee and a sell fee (1.5% to 5% each) and pay in their pair asset. Details: https://ubi.fun/docs/creators/creator-vaults and https://ubi.fun/docs/v3/overview
- $UBI (`0xFA3fFdF775CC3f6ac82Cd258Fb948a8a21e1749e`) is the platform token: once a day the holder pool pays USDC to $UBI holders by time-weighted balance, and gold from v3 tokens' fees from the October 18, 2026 round.
- Deeper references: REST API and contracts at https://ubi.fun/docs/integrate/overview. Every docs page also has a `.md` version, e.g. https://ubi.fun/docs/integrate/agents.md
