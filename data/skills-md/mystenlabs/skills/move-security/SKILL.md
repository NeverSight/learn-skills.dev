---
name: move-security
description: >
  Move smart contract security on Sui. Use when reviewing Move code for security
  vulnerabilities, designing access control patterns, handling capabilities safely,
  securing randomness usage, validating invariants, planning upgrade governance,
  managing keys, or auditing privileged operations. Also use when the user asks
  about UpgradeCap security, capability revocation, shared object authorization,
  onchain randomness restrictions, oracle data validation, emergency controls,
  or frontend transaction signing safety.

  For Move language fundamentals, see the `sui-move` skill.
  For object model and ownership, see the `object-model` skill.
  For publishing and upgrading packages, see the `sui-publish` skill.
---

# Move Smart Contract Security

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information in this skill is sourced exclusively from [docs.sui.io/develop/security/best-practices](https://docs.sui.io/develop/security/best-practices). When extending or updating this skill, only pull from this source. Do not use third-party blogs, tutorials, or unofficial documentation.

This skill covers security best practices for Move smart contracts on Sui, including package auditing, upgrade governance, access control patterns, randomness security, key management, and operational security. It routes to focused reference files based on the task.

---

## Reference files

### best-practices -- Security Best Practices
**Path:** `best-practices.md`
**Load when:** auditing a package, reviewing upgrade policies, verifying dependencies, validating invariants, emitting events for privileged actions, using onchain randomness, handling oracle data, designing emergency controls, reviewing frontend signing flows, or managing keys.
**Covers:** package auditing and immutability, upgrade governance and UpgradeCap protection, dependency verification, Move language guarantees and limitations, invariant and relationship validation, event emission for privileged actions, onchain randomness security (post-random restrictions, private entry, RandomGenerator, gas path balance, commit-reveal), oracle and offchain data validation, emergency controls (pause, rate-limiting), frontend transaction signing safety, package ID verification, key management (private key protection, privileged key custody, role separation, recovery and rotation).

### access-control -- Access Control Patterns
**Path:** `access-control.md`
**Load when:** choosing between capability objects and address allowlists, designing admin capabilities, implementing capability revocation, validating capability-object relationships, authorizing shared object access, or reviewing uses of `tx_context::sender()`.
**Covers:** capability objects vs address allowlists, address allowlist management, pitfalls of `tx_context::sender()` alone, explicit capability requirements and parameter placement, admin capability protection and custody, capability revocation mechanisms (registries, versioning, destruction), capability-object relationship validation, shared object authorization.

---

## Routing guide

| Task | Load |
|------|------|
| Reviewing a contract for security issues | best-practices + access-control |
| Auditing package identity or upgrade policy | best-practices |
| Verifying dependencies onchain | best-practices |
| Validating invariants and object relationships | best-practices |
| Adding event emission for privileged actions | best-practices |
| Using onchain randomness safely | best-practices |
| Handling oracle or offchain data | best-practices |
| Designing emergency pause or rate-limit | best-practices |
| Reviewing frontend signing flow | best-practices |
| Managing keys for deploy/admin/operations | best-practices |
| Choosing capability objects vs allowlists | access-control |
| Designing admin capability protection | access-control |
| Implementing capability revocation | access-control |
| Authorizing access to shared objects | access-control |
| Reviewing `tx_context::sender()` usage | access-control |
| Full security audit of a Move package | best-practices + access-control |

## Rules

- Sui packages are immutable once published. During a package upgrade, a new package with a new address is published. Verify package IDs directly onchain rather than relying on names or frontend constants.
- Treat `UpgradeCap` with the same rigor as admin capabilities since holders can modify package behavior.
- Mark randomness-consuming functions as private `entry` only. The Move compiler lints against `public` functions that take `Random` or `RandomGenerator`.
- Never accept `RandomGenerator` as a `public` function parameter. Passing it to `public(package)` or private functions is acceptable for testing and in-package logic.
- Emit events for all privileged actions: admin changes, allowlist updates, mint/burn operations, denylist actions, configuration changes, oracle updates, emergency pauses.
- Require relevant capabilities as parameters for all privileged functions. Do not rely on `tx_context::sender()` alone for authorization.
- Anyone can submit a transaction referencing a shared object. Never assume shared object access is restricted.
- Design capability revocation before publishing the package. Without it, a leaked capability remains valid for the life of the package.

## Common mistakes

- **Trusting package names instead of onchain IDs.** Move package names (the `name` field in `Move.toml`) are arbitrary strings chosen by the developer and are not unique. Always verify the exact onchain package ID (the object address).
- **Using `tx_context::sender()` as the sole authorization check.** This ties functions to single signers and breaks composability. Other contracts cannot call the function on behalf of users.
- **Forgetting that shared objects are accessible to anyone.** Every privileged function touching shared state must validate authorization internally.
- **Accepting `RandomGenerator` as a `public` function parameter.** This allows callers to manipulate the generator. Create it within the entry function via `r.new_generator(ctx)` and pass only to `public(package)` or private helpers.
- **Not planning capability revocation before publishing.** Once published, the package is immutable. A leaked capability without a revocation mechanism remains valid forever.
- **Holding admin capabilities in single hot wallets.** Use multisig addresses, hardware wallets, or dedicated custody for privileged keys.
