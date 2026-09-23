---
name: zklogin
description: >
  zkLogin on Sui — architecture, protocol flow, integration, and security.
  Use when explaining how zkLogin works, integrating zkLogin into a Sui
  application, choosing an OpenID provider, understanding the address derivation
  scheme, debugging session lifetime or proof issues, or answering questions
  about zkLogin security properties (salt, ephemeral keys, JWT privacy).
  Also use when the user asks about OAuth-based wallet-less login on Sui.
---

# zkLogin Skill

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information in this skill is sourced exclusively from [docs.sui.io/concepts/cryptography/zklogin](https://docs.sui.io/concepts/cryptography/zklogin). When extending or updating this skill, only pull from this source. Do not use third-party blogs, tutorials, or unofficial documentation.

zkLogin is a Sui primitive that lets users log in with their existing OAuth credentials (Google, Facebook, Apple, etc.) instead of managing a traditional crypto wallet. It uses zero-knowledge proofs to link an OAuth identity to a Sui address without revealing the OAuth identifier onchain. Common AI-coding mistakes include confusing the roles of the salt, ephemeral key, and ZK proof in the security model, assuming a leaked JWT means compromised funds, and not understanding that addresses are permanent but sessions are ephemeral.

This skill routes to focused reference files. Load only the ones relevant to the current task.

All patterns in this skill are derived from:
  https://docs.sui.io/concepts/cryptography/zklogin

If unsure about any detail, fetch the relevant page before answering.
Do not guess or extrapolate from other authentication systems.

---

## Reference files

### architecture -- Architecture and Protocol Flow
**Path:** `architecture.md`
**Load when:** the user asks how zkLogin works internally, about the three key entities (frontend, salt service, proving service), the 10-step protocol flow, address derivation, session lifetime, the Groth16 ceremony, or the role of JWTs and nonces.
**Covers:** three key entities, JWT structure, protocol flow (10 steps), address derivation formula, session lifetime and ephemeral key expiry, key notations, Groth16 ceremony.

### integration -- Integration Guide
**Path:** `integration.md`
**Load when:** the user needs to integrate zkLogin into an application, choose a supported OpenID provider, verify signatures offchain, understand security tradeoffs, or troubleshoot common issues.
**Covers:** supported OpenID providers by network, implementation steps, offchain signature verification methods, security considerations, FAQ.

---

## Routing guide

| Task | Load |
|------|------|
| Explaining what zkLogin is | SKILL.md only |
| Understanding the protocol flow | architecture |
| Understanding address derivation | architecture |
| Understanding session lifetime and ephemeral keys | architecture |
| Choosing an OpenID provider | integration |
| Integrating zkLogin into an app | integration |
| Verifying zkLogin signatures offchain | integration |
| Understanding security properties | integration |
| Answering zkLogin FAQ | integration |
| Full deep dive on zkLogin | **all reference files** |

---

## Skill Content

### Key concepts

- **Wallet-less login.** zkLogin lets users transact on Sui using OAuth credentials (Google, Facebook, Apple, etc.) instead of managing seed phrases or private keys. The user's OAuth identity maps to a deterministic Sui address.

- **Three key entities.** The system involves three components: (1) the application frontend that manages ephemeral keys and OAuth flow, (2) a salt service that returns a consistent unique salt per user, and (3) a proving service that generates zero-knowledge proofs.

- **Ephemeral key pairs.** Each session uses a short-lived key pair. The ephemeral public key, a max epoch, and randomness are embedded in the OAuth nonce. When the epoch passes max_epoch, the user logs in again and generates a new key pair and ZK proof but continues using the same Sui address.

- **Zero-knowledge proofs.** A Groth16 zkSNARK proof validates that the nonce was derived correctly, the key claim value matches the JWT, the RSA signature is valid, and the address is consistent with the key claim and salt -- all without revealing the OAuth subject identifier onchain.

- **Permanent addresses.** The Sui address derived from zkLogin is permanent. It does not change unless the sub, iss, aud, or user_salt changes. Different providers or applications produce different addresses for the same user.

### Rules

1. **Never conflate JWT leaks with fund compromise.** A leaked JWT can compromise privacy but cannot steal funds as long as the ephemeral private key is safe.
2. **Never assume the ZK proof alone authorizes transactions.** Both the ephemeral signature and the ZK proof are required; neither is sufficient on its own.
3. **Always explain that the salt is critical for both privacy and access.** The salt unlinks the OAuth identifier from the onchain address. Losing the salt means permanent loss of access.
4. **Always note that iss, aud, and kid are revealed onchain.** The JWT itself is not published onchain, but these three fields are visible.
5. **Never suggest converting a traditional wallet to a zkLogin address.** They use different address derivation schemes and are not interchangeable.

### Common mistakes

- **Assuming a leaked JWT means stolen funds.** The JWT alone is not enough. An attacker also needs the ephemeral private key and salt to create valid transactions.
- **Forgetting that proofs are session-scoped.** A ZK proof is valid only until the ephemeral key expires (max_epoch). Proofs cannot be reused across sessions, but can be cached and reused within a session.
- **Ignoring the salt's role in privacy.** Without the salt, there is no link between the OAuth subject and the Sui address. If the salt leaks, the link becomes visible, though funds remain safe.
- **Assuming all providers work on all networks.** Some providers (Slack, Kakao, Microsoft) are available on Devnet and Testnet only — not Mainnet. Others (RedBull, Amazon, WeChat, Auth0, Okta) are under review.
