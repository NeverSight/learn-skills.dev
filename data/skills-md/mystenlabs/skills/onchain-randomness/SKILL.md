---
name: onchain-randomness
description: >
  Onchain randomness on Sui. Use when generating random values in Move smart contracts,
  working with the Random object (0x8) or RandomGenerator, securing randomness-consuming
  functions against composition attacks, PTB attacks, or state leakage, implementing
  commit-reveal patterns, balancing gas across execution paths, or integrating randomness
  from TypeScript.

  For general Move security patterns, see the `move-security` skill.
  For Move language fundamentals, see the `sui-move` skill.
  For TypeScript SDK patterns, see the `sui-sdks` skill.
---

# Onchain Randomness

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information in this skill is sourced exclusively from [docs.sui.io/sui-stack/on-chain-primitives/randomness-onchain](https://docs.sui.io/sui-stack/on-chain-primitives/randomness-onchain). When extending or updating this skill, only pull from this source. Do not use third-party blogs, tutorials, or unofficial documentation.

Sui provides native onchain randomness through the `Random` shared object at address `0x8`. Move functions create `RandomGenerator` instances from `Random` and use them to produce unpredictable values. This skill covers the API, usage patterns, security considerations, and attack mitigations for onchain randomness.

---

## Reference files

### usage -- API and Usage Patterns
**Path:** `usage.md`
**Load when:** generating random values in Move, creating a `RandomGenerator`, calling `new_generator`, using `generate_u128`, `generate_u8_in_range`, passing the `Random` object from TypeScript, or writing basic randomness-consuming functions.
**Covers:** the `Random` object (address `0x8`), `RandomGenerator`, the `random.move` API (full function list including `new_generator`, value generation, range generation, `shuffle`, `generate_bytes`), basic implementation examples, TypeScript integration.

### security -- Security and Attack Vectors
**Path:** `security.md`
**Load when:** securing randomness-consuming functions, preventing composition attacks, mitigating PTB attacks, avoiding `RandomGenerator` state leakage, implementing commit-reveal patterns, balancing gas across winning and losing paths, or choosing function visibility for randomness functions.
**Covers:** composition attacks (abort-filtering via public functions), PTB attacks (command chaining after `MoveCall` consuming `Random`), `RandomGenerator` state leakage via `bcs::to_bytes`, compiler lints on public functions accepting `Random` or `RandomGenerator`, two-step commit-reveal pattern, balanced gas usage, entry function restrictions.

---

## Routing guide

| Task | Load |
|------|------|
| Generating random values in Move | usage |
| Creating a RandomGenerator | usage |
| Calling random API functions | usage |
| Passing Random from TypeScript | usage |
| Securing a randomness-consuming function | security |
| Preventing composition or abort-filtering attacks | security |
| Mitigating PTB-based attacks | security |
| Avoiding RandomGenerator state leakage | security |
| Implementing commit-reveal for randomness | security |
| Balancing gas across execution paths | security |
| Choosing function visibility for randomness | security |
| Writing a complete randomness feature | usage + security |
| Reviewing randomness code for vulnerabilities | usage + security |

## Rules

- The `Random` object lives at reserved address `0x8` and is immutable for transactions. Any attempt to modify it causes transaction failure.
- Always create `RandomGenerator` locally within the consuming function using `r.new_generator(ctx)`. Never pass `RandomGenerator` as a `public` function parameter. Passing it to `public(package)` or private functions is acceptable for testing and in-package logic.
- Define randomness-consuming functions as private `entry` functions. The Move compiler lints against `public` functions that accept `Random` or `RandomGenerator` as parameters.
- Sui rejects PTBs containing commands other than `TransferObjects` or `MergeCoins` following a `MoveCall` that consumes `Random`. In other words, a call accepting `Random` must be the last `MoveCall` in a PTB.
- Ensure winning and losing execution paths consume approximately equal total gas (both compute and storage) to prevent attackers from inferring outcomes from gas consumption. Measure gas carefully and test in each published environment before going live.
- Use the two-step commit-reveal pattern when the outcome of randomness must not be observable before a follow-up action completes.

## Common mistakes

- **Making randomness functions `public` instead of private `entry`.** This is a fatal security flaw, not just a mistake. Public functions accepting `Random` enable abort-filtering attacks where an attacker wraps the function and reverts unfavorable outcomes. The compiler lints against this.
- **Accepting `RandomGenerator` as a `public` function parameter.** Callers can predict outputs by serializing the generator's internal state with `bcs::to_bytes(&generator)`. The compiler lints against `public` functions with `RandomGenerator` parameters. Using `RandomGenerator` as a parameter in `public(package)` or private functions is acceptable for testing and in-package logic.
- **Unbalanced gas consumption between branches.** If winning and losing paths consume significantly different total gas (compute + storage), attackers can infer outcomes from gas usage. The success path should cost equal or more gas than the failure path. To achieve this, either perform a simple standard update (e.g., set a bool flag) and claim the result in a follow-up function, or create an equally sized object (e.g., a dynamic field) in the failure path. Gas values must be measured carefully and tested in each published environment before going live.
- **Skipping commit-reveal when outcomes influence subsequent user actions.** If a user can observe and act on a random outcome in the same transaction, they can abort unfavorable results.
