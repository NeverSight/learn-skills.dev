---
name: merkl
description: Activate when the user asks about DeFi rewards, incentives, yield farming campaigns, claiming rewards, or Merkl on Katana Network.
license: MIT
metadata:
  author: katana
  version: '1.0.0'
---

# Merkl Rewards — Katana Network

Discover incentivized DeFi opportunities and claim reward tokens distributed by Merkl on Katana.

## How Merkl Works

Merkl distributes extra reward tokens (KAT, MORPHO, SUSHI, etc.) to users who participate in DeFi on Katana — supplying to Morpho, providing Sushi LP, borrowing, or holding tokens.

- **Campaigns** target specific actions: POOL (Sushi LP), LEND (Morpho supply/vaults), BORROW (Morpho borrow), HOLD (token holding), DROP (airdrops)
- Rewards are computed **offchain every ~2 hours** based on user activity snapshots
- Merkle roots are pushed **onchain every ~8 hours** — only then can users claim
- Claiming submits a merkle proof to the Distributor contract
- No approval needed to claim — the Distributor sends reward tokens directly to the user

## Contract Addresses (Mainnet)

| Contract | Address |
|----------|---------|
| Merkl Distributor | `0x3Ef3D8bA38EBe18DB133cEc108f4D14CE00Dd9Ae` |

## API & Contracts

### Discovering Opportunities

Merkl provides a public REST API for querying incentivized opportunities on Katana:

**Endpoint:** `https://api.merkl.xyz/v4/opportunities?chainId=747474`

Optional query parameters:
- `protocol` — filter by protocol (e.g., `morpho`, `sushi-swap`)
- `action` — filter by action type (`POOL`, `LEND`, `BORROW`, `HOLD`, `DROP`)

Returns LIVE opportunities sorted by TVL: name, total APR (native + reward), daily rewards in USD, reward token details, and protocol.

**APR breakdown:** `totalApr` includes both native protocol yield AND Merkl reward APR. Campaign APRs change as TVL fluctuates — high APRs in low-TVL pools compress as more capital enters.

### Checking User Rewards

**Endpoint:** `https://api.merkl.xyz/v4/users/{userAddress}?chainId=747474`

Returns all pending reward tokens with: total earned, already claimed, unclaimed amount, unclaimed USD value, and proof availability. If proofs are not yet available onchain, the user must wait for the next merkle root update (~8 hour cycle).

### Claiming Rewards

Call `claim` on the Merkl Distributor (`0x3Ef3D8bA38EBe18DB133cEc108f4D14CE00Dd9Ae`):

```
claim(
  address[] users,       // array of user addresses (typically just the one user)
  address[] tokens,      // array of reward token addresses to claim
  uint256[] amounts,     // array of cumulative amounts (from merkle proof)
  bytes32[][] proofs     // array of merkle proofs (one per token)
)
```

**Proof data** comes from the Merkl API. Fetch proofs from:
`https://api.merkl.xyz/v4/users/{userAddress}/claims?chainId=747474`

The response includes the exact `users`, `tokens`, `amounts`, and `proofs` arrays needed for the `claim()` call.

**No approval needed** — the Distributor sends reward tokens directly. Gas-only transaction.

## Workflows

### Discover Best Yield
1. Query `https://api.merkl.xyz/v4/opportunities?chainId=747474` — see all incentivized positions with reward APRs
2. Compare with native yield from Morpho markets (see lending skill) or Sushi pools (see dex skill) — **total yield = native APY + Merkl reward APR**
3. Use dex or lending skills to enter the position

### Check and Claim Rewards
1. Query `https://api.merkl.xyz/v4/users/{address}?chainId=747474` — check unclaimed rewards and USD values
2. Fetch proofs from `https://api.merkl.xyz/v4/users/{address}/claims?chainId=747474`
3. Construct the `claim()` call on the Distributor — no approval needed, gas-only

### Optimize Yield Strategy (Multi-Skill)
1. Query Merkl API with protocol filter — see what's incentivized
2. Check native lending rates on Morpho (see lending skill)
3. Use dex skill to swap into the right tokens or add LP
4. Use lending skill to supply to Morpho markets
5. Periodically query user rewards to track accumulated earnings

## Safety Notes

- **Timing:** New positions won't show rewards immediately. Rewards are computed every ~2 hours.
- **Proof availability:** Merkle roots update every ~8 hours. The API may show unclaimed amounts before proofs are available onchain. Check the `claimable` field before constructing a claim.
- **Dispute period:** After a merkle root update, there's a dispute window before rewards become claimable.
- **Stale proofs:** Proofs are fetched at claim-construction time. If the user waits too long to submit, a new merkle root may invalidate the proofs. Claiming promptly reduces this risk.
- **Reward token liquidity:** Some reward tokens may not have deep on-chain liquidity. Check prices via Sushi V3 pools (see analytics skill) before assuming rewards can be easily sold.

## Common Mistakes

- **Passing token symbols instead of addresses to `claim()`.** The `tokens` parameter requires `0x`-prefixed contract addresses, NOT symbols like `"KAT"` or `"MORPHO"`. Get the correct addresses from the Merkl API response.
- **Trying to claim when proofs aren't available.** The API may show unclaimed amounts but proofs aren't onchain yet (~8 hour cycle). Check the `claimable` field before constructing a claim transaction.
- **Assuming rewards appear instantly.** After entering a new position, rewards won't show for ~2 hours (next offchain computation cycle). Don't query rewards immediately after a deposit and tell the user there are no rewards.

## Cross-References

- **lending**: supply to Morpho markets/vaults to earn LEND rewards
- **dex**: provide Sushi LP to earn POOL rewards
- **analytics**: on-chain price derivation to value reward tokens in USD
- **wallet-manager**: balance checks after claiming to verify reward tokens received
