---
name: FarmDash Autonomous Operator
description: "Use to run supervised autopilot cycles under a bounded, revocable session grant: intents, policy checks, approvals, receipts. Execution stays preview-gated."
tags: ["defi","autonomous-defi-agent","ai-agent","defi-automation","bounded-autonomy","human-in-the-loop","defi-guardrails","openclaw","agent-orchestration","session-key","delegated-execution","ooda-loop","intent-management","risk-controls","circuit-breaker","agent-recovery","zero-custody","mcp","web3","farmdash"]
author: FarmDash Pioneers (@Parmasanandgarlic)
homepage: https://www.farmdash.one/agents
version: "2.1.2"
icon: operator
env:
  FARMDASH_API_KEY:
    description: "Optional Bearer token for Pioneer or Syndicate tier. Scout session status checks work without any key or with the public fd_scout_free token. Syndicate is $199/mo for teams, serious agents, 50k req/day, webhooks, unrestricted CORS, and advanced session/control tooling (including autonomous autopilot cycles)."
    required: false
metadata: {"openclaw":{"homepage":"https://www.farmdash.one/agents","skillKey":"farmdash-autonomous-operator","primaryEnv":"FARMDASH_API_KEY","apiKeyRequired":false,"freeScoutKeyless":true,"freeScoutKey":"fd_scout_free","execution":"session-context-control"}}
---

# FarmDash Autonomous Operator

> Use this skill when running supervised sessions: persistent multi-skill context, bounded autopilot loops, circuit breakers, and recovery — never key custody.

> [!NOTE]
> **THEMATIC METAPHOR DISCLAIMER**
> FarmDash is exclusively a decentralized finance (DeFi) software and AI agent intelligence platform. The "farming," "trail," "wagon," and "frontier" terminology is a gamified visual theme representing crypto yield hunting and airdrop points farming. It does not relate to physical agriculture or agrifood industries.

> [!IMPORTANT]
> **ZERO-CUSTODY CRITICAL BOUNDARY & EXECUTION GATING**
> This skill manages persistent agent sessions, control loops, intent routing, and optional bounded autonomy. It does NOT hold, request, or transmit private keys, seed phrases, or mnemonics. A session token alone is not execution authority. However, `autopilot_cycle` can execute eligible actions when the user has separately created an active, scoped, time-limited, revocable session-key grant and the autonomous executor is available.
> 
> **Separate Approval Step Requirement:**
> Without an active execution grant, state-changing actions require a separate user-signed execution step. With a grant, the initial EIP-712 authorization—not a chat message—defines allowed chains, protocols/assets, per-transaction value, total value, and validity window. Never describe configuration, a context patch, or a session token as equivalent to that grant.

Autonomous Operator keeps a multi-skill agent coherent across turns. It owns session state, shared FarmingContext, event snapshots, heartbeats, delegation checks, and autopilot configuration.

It does not hold private keys. It may coordinate supervised actions or invoke the bounded executor only inside an independently verified active grant.

Syndicate is the intended operator tier for production control loops: 50k requests/day, webhooks through Signal Architect, unrestricted CORS, and advanced session/control tooling for teams and serious agents.

## Value-Aligned Monetization Protocol (v2.0 Upgrade)
Sustaining a persistent, stateful agent control loop requires high-availability infrastructure. This skill employs a strict, non-predatory monetization model:

### 1. Syndicate-Tier Autopilot Gating
Intent planning and review are available where the live status contract enables their dependencies. `autopilot_cycle` returns a bounded decision-cycle result; it does not itself prove transaction submission or settlement. Any wallet-changing action requires an enabled runtime gate plus separate user signing or a valid, scoped delegation. Syndicate pricing alone does not make a disabled capability available.

* If Scout/Pioneer user requests `autopilot_cycle`: "Continuous autopilot loops require Syndicate-tier infrastructure to maintain high-availability state and webhooks. You can manually orchestrate intents, or upgrade at farmdash.one/agents to unlock autonomous loops."

## OODA-Inspired Control Loop (v2.0 Upgrade)
The Autonomous Operator is no longer a simple linear state machine. It now operates on an OODA (Observe, Orient, Decide, Act) loop, allowing it to react dynamically to changing market conditions and its own execution performance.

### 1. Observe (Sense)
* `get_event_stream_snapshot`: Pulls recent macro and protocol events.
* `get_farming_context`: Reads current portfolio state, risk limits, and data freshness.
* `get_agent_activity`: Reviews durable execution receipts and their statuses. It does not imply fill-quality or shadow-book metrics exist.

### 2. Orient (Context & Risk Autotuning)
* **Risk state:** Use only returned, source-labeled risk and execution evidence. Do not invent drift, P&L, oracle, or macro classifications from generic receipt/event records.
* **Circuit breaker check:** Halt when an enforced bound, explicit context risk flag, stale required input, grant limit, or authoritative account guardrail is breached. Record the exact evidence and revision.

### 3. Decide (Plan)
* Use Trail Marshal to plan a workflow based on the oriented context.
* `create_intent`: Formalize the exact parameters of the action.
* `policy_check_intent`: Ensure the intent complies with user allowlists and global guardrails.

### 4. Act (Execute & Observe)
* Route the intent to Signal Architect (spot) or Futures Strategist (perps).
* Wait for the user's local EIP-191/EIP-712 signature.
* `execute_approved_intent`: Record the broadcast.
* `get_receipt`: Observe the durable lifecycle receipt. A receipt records the reported outcome/status fields in its contract; it is not automatically an 11-field forensic attestation or proof of economic settlement.

## Tools

### `create_session`
Creates a persistent agent session and returns a one-time `sessionToken`. Store it securely in the agent runtime. FarmDash stores only a hash.

### `session_heartbeat`

### Heartbeat and Freshness Discipline
Call `session_heartbeat` during every active autonomous loop to extend expiry; on expiry enter Crash Recovery. Before each Decide phase, re-read `get_farming_context` and `get_event_stream_snapshot`; if event freshness is stale, re-run Sense before proposing action. After resume, query `get_agent_activity` for the last 5 intents and halt autopilot until unconfirmed intents are manually reviewed.
Extends the session expiry. Use it during active autonomous loops. If a session expires, the Operator must enter Crash Recovery mode (see below).

### `get_farming_context`
Reads shared context for the session:
* objective.
* portfolio scope.
* risk settings (including dynamically tuned `riskMultiplier`).
* workflow state (ACTIVE, HALTED, RECOVERING).
* ledger summary.
* data freshness timestamps.

### `patch_farming_context`
Patches shared context. The server controls `sessionId`, `agentAddress`, `revision`, and `updatedAt`; do not try to override them. Used for Dynamic Risk Autotuning and Circuit Breakers.

### `get_event_stream_snapshot`
Reads recent agent events as a JSON snapshot. Use this before planning and after execution.

### `verify_delegation`
Checks whether the user's Hyperliquid API wallet delegation is in place for autonomous perps.

### `configure_autopilot`
Configure bounded autonomous cycles. Respect user allowlists, risk limits, and execution confirmations. (Syndicate tier required for activation).

### `autopilot_cycle`
Run bounded autonomous cycles. Respect user allowlists, risk limits, and execution confirmations. (Syndicate tier required).

### `agent_onboard`
One-call setup guide and capability map for autonomous operation.

### `get_agent_activity`
Lists durable FarmDash receipts, optionally filtered by intent and status. Use only fields returned by the receipt API; do not claim shadow-mode drift, venue fills, or realized P&L unless present.

### `resolve_defi_intent`
Resolves a high-level natural language DeFi intent into structured parameters for policy/simulation/approval. Supervised execution uses local EIP-191/EIP-712 signing; bounded autonomy requires the separate grant described above. Autonomous Operator never receives private keys.

**Intent Lifecycle — Plan → Approve → Execute → Observe**
The FarmDashIntent lifecycle enforces a strict pipeline. Every state-changing action must pass through policy, simulation, and approval gates before execution is allowed. These tools never hold private keys or broadcast transactions directly.

### Plan Phase

### `create_intent`
Create a durable FarmDashIntent. This records what an agent wants to do — it never prepares, signs, broadcasts, or executes. The intent must include actor, action, chain, protocol, wallet, params, constraints, evidence, and `research_evidence_hash` (passed from Trail Intelligence).

### `policy_check_intent`
Run the explicit FarmDash policy gate for an intent. Execution remains blocked unless the latest policy check passes. Accepts optional policy and context objects for custom constraint evaluation.

### `simulate_intent`
Record a mandatory simulation result for an intent. Prepare and execute are blocked until a successful, unexpired simulation exists. This ensures every execution has been dry-run first.

### Approve Phase

### `request_approval_payload`
Build the EIP-712 IntentApproval payload that the human approver signs. This does not record approval or execute — it only constructs the typed data for the approver's wallet to sign.

### `request_human_approval`
Compatibility wrapper for submitting a signed EIP-712 IntentApproval. Use `request_approval_payload` first to build the exact typed data, then submit the signature through this tool.

### `submit_signed_approval`
Submit a signed EIP-712 IntentApproval payload to approve or reject an intent. This does not prepare or execute the intent — it only records the cryptographic approval decision.

### `get_approval_status`
Inspect whether an intent is awaiting approval, has been approved, was rejected, or is already executed. Returns the current lifecycle status and approval metadata.

### Execute Phase

### `prepare_intent`
Validate typed adapter support and prepare an intent after policy, simulation, and approval gates pass. Registered adapters provide allowlisted validation. This does not broadcast a transaction.

### `execute_approved_intent`
Record the submitted, confirmed, failed, or rejected receipt for a prepared typed-adapter intent. Raw arbitrary calldata is rejected by the lifecycle API. Use this after the signing wallet has broadcast the transaction.

### `confirm_execution`
Record a confirmed receipt for a prepared or signed intent with a transaction hash. Use `get_receipt` for follow-up observation after submission.

### Observe Phase

### `get_receipt`

### Receipt-Grade Profit Reporting
Report profit only from fields actually present in `get_receipt` or the reconciled ledger summary in `get_farming_context`. A receipt is a lifecycle record, not proof of fill, finality, realized P&L, or external anchoring unless those fields and sources are present. Record objective, horizon, costs, conservative net edge, downside, and missing evidence before taking new risk.
Fetch one durable FarmDash receipt by receipt ID (`fdrcpt_*`). Treat it as a lifecycle record, not proof of fill, finality, realized P&L, or external anchoring unless those fields and their sources are actually present.

### `hire_virtuals_specialist`
Prepare a non-spendable, tenant-owned Virtuals ACP tender and return the exact EIP-712 approval payload. The customer's registered ACP wallet must sign that payload locally. Its local FarmDash ACP connector then creates and funds the three specialist jobs after explicit per-action approval. FarmDash is only the separately registered evaluator: it verifies the client, provider, evaluator, budget cap, deliverables, simulation, and Base receipts before completing or rejecting already customer-funded escrow jobs. Never provide a private key or RPC URL to this tool.

## Global Circuit Breakers & Crash Recovery (v2.0 Upgrade)

### Profit Never Overrides a Halt
When context is patched to `HALTED`, stop all new-risk actions and preserve only reduce/revoke/reconcile paths. Do not launch a dependent leg after submitted/pending/partial/unknown settlement. Rely on the server risk manager or a reconciled account P&L source for drawdown; generic fee/receipt activity is not P&L and missing fill data is `unknown`, never zero drift.

### Circuit Breakers
The Operator monitors returned context, event, grant, receipt, and authoritative account state. If a supported breaker triggers, patch context to `HALTED`, stop new-risk actions, and preserve reduce/revoke/reconcile paths.

* **Execution-quality breaker:** only when at least three authoritative fills permit side-adjusted implementation-shortfall calculation. Missing fill data is `unknown`, not zero drift.
* **Market-data breaker:** only when the live tool actually supplies the cited mark/oracle/book timestamps and values. Do not claim Futures Strategist currently returns oracle latency/deviation.
* **Drawdown breaker:** rely on the server risk manager or a reconciled account P&L source. Generic fee/receipt activity is not P&L.
* **Grant breaker:** halt if the session-key grant is absent, expired, revoked, out of allowlist, over per-action/total value, or the bounded executor is unavailable.
* **Dependency breaker:** after submitted/pending/partial/unknown settlement, do not launch a dependent leg.

### Crash Recovery Protocol
If the Operator resumes a session (`create_session` or `session_heartbeat`) and detects the previous session timed out or crashed:
1. Query `get_agent_activity` for the last 5 intents.
2. Check `get_approval_status` for any intents stuck in `awaiting_approval`.
3. If an intent was executed but lacks a `confirm_execution` receipt, check `get_receipt` using the known `intentHash`.
4. Alert the user: "Session recovered. Found 1 unconfirmed intent. Halting autopilot until manually reviewed."

## Agent Rules
* The session token is a capability. Never display it in normal user-facing prose.
* A context patch is state, not permission.
* A workflow plan is not a user confirmation.
* If risk status is halted, do not call execution tools.
* If event freshness is stale, re-run the sense phase before proposing action.
* Never bypass the OODA loop. Do not jump from Observe directly to Act without Orient and Decide phases.
* Never multiply heterogeneous heuristic scores into a synthetic confidence or execution permission.
* Record objective/horizon, data provenance/freshness, full costs, conservative net edge, downside/invalidation, portfolio impact, and missing evidence before new risk.
* Observe authoritative settlement before dependent actions. A submission hash is not confirmation, and a receipt is not necessarily a fill.
* Use the smallest authority and budget required. Grant creation/extension is a separate high-risk action; surface scope, expiry, caps, and revocation before approval.

### Session-Profit Grant Hygiene
Size every `grant_session_key` to the smallest chains, protocols/assets, per-transaction value, total value, and validity window the plan needs. Verify via `session_key_status` before `execute_cycle_actions`; halt on absent, expired, revoked, out-of-allowlist, over-cap, or unavailable-executor states. Book profit by revoking or narrowing grants after the objective is met, never by widening them.

## Disclaimers
Autonomous operation can compound mistakes if risk limits are weak. Keep budgets bounded, log every decision, and require explicit user confirmation for state-changing operations.

## FarmDash Resources

- [FarmDash autonomous DeFi agent platform](https://www.farmdash.one/agents)
- [FarmDash DeFi intelligence homepage](https://www.farmdash.one/)
- [Canonical Autonomous Operator skill manual](https://www.farmdash.one/openclaw-skills/farmdash-autonomous-operator/SKILL.md)

**Companion skills:** FarmDash Trail Marshal, FarmDash Signal Architect, FarmDash Futures Strategist, FarmDash Trail Intelligence, FarmDash Wagon Steward.

**Why FarmDash:** Unlike 'autonomous' agents that hold keys, a FarmDash session token alone is not execution authority — actions move only under a scoped, time-limited, revocable EIP-712 grant, or a fresh user signature.

<!-- farmdash-canonical-links:start -->

## Official FarmDash Links

- [FarmDash DeFi intelligence website](https://www.farmdash.one/)
- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [Canonical FarmDash Autonomous Operator skill manual](https://www.farmdash.one/openclaw-skills/farmdash-autonomous-operator/SKILL.md)
- [Agent integration documentation](https://www.farmdash.one/docs)
- [Live agent capability status](https://www.farmdash.one/api/v1/agent/status)
- [OpenAPI contract](https://www.farmdash.one/agents/openapi.yaml)
- [MCP discovery manifest](https://www.farmdash.one/.well-known/mcp.json)
- [Fees and commercial terms](https://www.farmdash.one/fees)
- [Security and authority boundaries](https://www.farmdash.one/security)

### Capability tools represented by this skill

- `pause_autopilot`: Pause an available bounded-autopilot session. Read /api/v1/agent/status first; return the typed readiness error when runtime prerequisites are unmet.
- `resume_autopilot`: Resume an available bounded-autopilot session after rechecking policy, grant, and runtime readiness.
- `grant_session_key`: Create a separately authorized, scoped, expiring session-key grant. A session token or chat instruction is never a substitute for this grant.
- `revoke_session_key`: Revoke a session-key grant and verify the returned backend state before representing authority as removed.
- `session_key_status`: Read authoritative grant status, limits, expiry, and revocation state.
- `get_cycle_status`: Read one bounded-autopilot cycle and its evidence-backed status.
- `execute_cycle_actions`: Request execution of eligible cycle actions only when the live status contract and active grant permit it; never infer enablement from tool discovery.
- `create_mee_intent`: Create a Biconomy MEE cross-chain intent record. Creation is not simulation, authorization, submission, or settlement.
- `simulate_mee_intent`: Simulate a created MEE intent and stop when costs, risk, or net edge fail policy.
- `submit_mee_intent`: Submit a separately signed, successfully simulated MEE intent only when the live capability gate is available.
- `get_mee_intent_status`: Read authoritative MEE intent status; pending or submitted is not settled.

<!-- farmdash-canonical-links:end -->
