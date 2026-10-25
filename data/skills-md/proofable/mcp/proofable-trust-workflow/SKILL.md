---
name: proofable-trust-workflow
description: Verifies identity, permissions, and reusable proofs before sensitive assistant actions. Use when confirming authority, loading a trusted agent, scoping what it may do, or when the user asks for Proofable.
license: Apache-2.0
compatibility: Requires a client that supports remote HTTP MCP servers and hosted OAuth.
metadata:
  author: Proofable
  version: "0.1.7"
  homepage: https://docs.proofable.me/mcp/setup
---

# Proofable Trust Workflow

Reuse existing proofs first. Verify again only when needed. Summarize as **Proofable**: Passed, Action needed, or Blocked. Never dump raw tool JSON.

Use this before an assistant runs sensitive tools or takes another verification-sensitive step. Answer simple questions directly.

## When to use

- Before sensitive tools, spend, publish, secrets, or agent actions
- When the user asks for Proofable, proofs, agent permissions, or trusted-agent setup
- When acting as a registered profile agent in a project

## Workflow

1. **`proofable_context`** once per session. Prefer signed-in profile context; omit wallet fields on check/verify tools.
2. **Profile agent:** **`proofable_agent_mount`** (or `proofable mount <agentId> --apply <host>`) for identity, permissions, skills, and context.
3. **Trust before action:** use **`proofable_verify_or_guide`** directly. It reuses qualifying proofs or returns the next secure step. Use **`proofable_proofs_check`** only for an explicit yes/no eligibility, gate, or access question; never use it for memory, context, or content retrieval. When signed in, ownership checks continue with **`proofable_verify`**. For another signer, prepare with **`proofable_verify_prepare`** and submit with **`proofable_verify_submit`**. Share a browser link only when a tool returns one.
4. **Agent:** **`proofable_agent_link`**. If missing, **`proofable_agent_create`** (a dedicated account needs a key you create and hold; pass only its public address). Then **`proofable_agent_mount`**.
5. **Proofs and context:** use the `proofable_context` context index first, then **`proofable_proofs_get`** with a known proof ID and `include=content` for an exact body.
6. **Saved keys:** a credential belongs on the profile in Proofable, never in a conversation and never through a tool. Do not offer to store one from here.
7. Reuse existing proofs via **`proofable_verify_or_guide`** before creating new ones. When signed in, `proofable_context` returns the current profile context; re-call it only after a profile change.
8. Summarize as **Proofable**.

## Proofable format

Use the Passed / Action needed / Blocked guidance from `proofable_context`. Never invent proof IDs, verifier IDs, or statuses.

```txt
Proofable: Passed. Requirement satisfied. Proof on file. Next: Continue.
Proofable: Action needed. Missing: <step>. Next: Complete the secure step, then retry.
Proofable: Blocked. A required trust condition was not satisfied. Next: Do not continue until it passes.
```

## Hard rules

- Proofs stay off the chain unless the user asks for a blockchain record. Do not prompt for a wallet otherwise.
- Use proof IDs only from tool responses. Prefer “proof ID” / “portable proof” in user text.
- Never ask for a credential and never accept one. A key is saved on the profile in Proofable, where a run uses it without the value reaching a model or an app. This connection carries no tool that stores a secret; a call to one answers `platform_only`.
- Use live verifier IDs from **`proofable_context`** / **`proofable_verifiers_catalog`**. Do not hardcode a second catalog.

## Setup and mount

Install, OAuth, access keys, and project mount: [references/setup.md](references/setup.md)

Docs: [docs.proofable.me](https://docs.proofable.me). Setup: [docs.proofable.me/mcp/setup](https://docs.proofable.me/mcp/setup)
