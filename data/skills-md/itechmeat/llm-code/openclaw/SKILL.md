---
name: openclaw
description: "OpenClaw local AI assistant stack. Covers architecture, tools, gateway operations, channels, and onboarding. Keywords: OpenClaw, gateway, tools, channels, agents."
version: "v2026.2.23"
release_date: "2026-02-24"
metadata:
  author: itechmeat
  docs_ingested_at: "2026-02-23"
---

# OpenClaw (Operator Playbook)

This skill is self-contained and includes operational documentation directly in this file.

## Quick Navigation

- Installation / migration: `references/installation.md`
- Architecture & multi-agent routing: `references/architecture.md`
- Extended concepts: `references/concepts.md`
- Tool governance & safety: `references/tools.md`
- Gateway runbook & security: `references/gateway.md`
- Onboarding & first-run: `references/getting-started.md`
- Channels & providers: `references/channels-and-providers.md`
- Nodes & remote execution: `references/nodes.md`
- CLI operations & troubleshooting: `references/operations.md`

## Core Model

- OpenClaw is gateway-centric: one long-lived Gateway per host is the control plane.
- Clients and nodes connect via typed WebSocket API; channels/providers are orchestrated by gateway.
- Session safety depends on deterministic routing + queueing + explicit policy controls.

## Day-1 Setup

1. Run onboarding with daemon install.
2. Verify gateway health/status.
3. Open Control UI/dashboard for first chat.
4. Add channels/providers only after baseline health is stable.

If OpenClaw is not installed, use `references/installation.md`.

## Gateway Operations

- Keep default posture loopback + auth enabled.
- For remote access, prefer Tailscale Serve or SSH tunnel over public bind.
- Non-loopback binds require strict token/password controls.
- Use supervised process mode (launchd/systemd) for reliability.
- For config changes, treat `config.apply` as controlled rollout and `config.patch` as targeted merge.
- Remember patch semantics: objects merge, arrays replace, `null` deletes.

## Release Updates (v2026.2.23)

- Providers: first-class `kilocode` provider support (auth, onboarding, implicit provider detection, and model defaults).
- Tools/web_search: add provider `"kimi"` (Moonshot) and correct the two-step `$web_search` tool flow (echo tool results before synthesis).
- Gateway: optional HSTS via `gateway.http.securityHeaders.strictTransportSecurity` for direct HTTPS deployments.
- Sessions: hardened maintenance via `openclaw sessions cleanup` with disk-budget controls and safer transcript/archive cleanup.
- **Breaking:** browser SSRF policy defaults changed and config key renamed (`browser.ssrfPolicy.allowPrivateNetwork` -> `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork`); use `openclaw doctor --fix` to migrate.

## Architecture and Runtime Concepts

### Agent Loop

- Agent loop is serialized per session (and optionally globally) to avoid tool/history races.
- Run lifecycle emits assistant/tool/lifecycle streams for observability.
- Wait timeout and runtime timeout are different controls.

### System Prompt and Context

- System prompt is OpenClaw-composed per run (not provider default prompt).
- Prompt mode can be `full`, `minimal`, or `none` depending on run context.
- Context includes system prompt, transcript, tools/results, attachments, schemas.
- Bootstrap files are injected into context window and consume budget.

### Workspace and Memory

- Workspace is default execution directory and memory surface, not a hard sandbox.
- Use sandbox settings when strict filesystem isolation is required.
- Memory is markdown-first: daily notes + curated durable memory.
- Compaction persists summary to transcript; pruning trims old tool results in-memory.

### Messaging, Queueing, Presence

- Message processing uses dedupe, optional inbound debounce, queue modes, and channel-aware delivery.
- Queue/streaming/chunking behavior is policy-driven and tunable per channel.
- Presence is best-effort observability; stable `instanceId` is required to avoid duplicate entries.

## Tools Governance

- Start with least-privilege profile, then explicitly allow required tools.
- Deny list overrides allow list.
- Treat `exec`, `sessions_*`, `gateway`, `nodes` as high-impact surfaces.
- Require explicit user consent for media-capture operations.
- Enable loop-detection when tools may form no-progress cycles.

## Channels and Provider Strategy

- Start with fastest stable channel path (commonly Telegram) for baseline verification.
- Add WhatsApp and advanced channels only after pairing/allowlists are proven.
- Keep provider selection explicit via `provider/model` and avoid implicit model drift.
- Isolate auth profiles per agent when separating work/personal contexts.

## Nodes and Remote Execution

- Nodes are capability executors, not gateway replacements.
- Pair nodes explicitly and verify capabilities before invoking actions.
- Keep node exec approvals local to node host and audited.
- Use explicit node binding for deterministic remote execution targeting.

## Security Baseline

- Assume prompt injection is always possible.
- Apply controls in this order: identity (pairing/allowlist) -> scope (tools/sandbox/mentions) -> model policy.
- Keep control UI in secure context (loopback/HTTPS); avoid insecure auth downgrades.
- Use strict filesystem permissions for config/state and redact sensitive logs.

## Troubleshooting Ladder

1. `openclaw status`
2. `openclaw gateway status`
3. `openclaw logs --follow`
4. `openclaw doctor`
5. `openclaw channels status --probe`

Common triage map:

- No replies -> pairing/allowlist/mention policy.
- Connect loop -> auth mode + endpoint + secure context.
- Startup fail -> mode/bind/auth/port conflict.
- Tool failure -> permissions/approvals/foreground constraints.

## Concepts URLs Status (from left navigation)

- Extracted concepts are integrated directly into this skill.
- Some source URLs in docs navigation currently return 404 or empty content.
- Coverage for those pages is consolidated in `references/concepts.md` with fallback guidance.

## When to Use

- You need to design or operate an OpenClaw deployment.
- You need to connect channels, providers, and tools safely.
- You need a practical checklist for onboarding and gateway setup.

## Core Operating Workflow

1. Confirm topology and responsibilities from architecture notes.
2. Choose channels/providers and required tools.
3. Configure gateway access and remote connectivity.
4. Validate onboarding flow and control UI accessibility.
5. Run troubleshooting and hardening checklist.

## Critical Prohibitions

- Do not copy large verbatim chunks from vendor docs into this skill.
- Do not invent defaults or hidden behavior without doc evidence.
- Do not weaken safety controls (pairing, allowlists, auth, sandbox) for convenience in production.

## Links

- [Documentation](https://docs.openclaw.ai/)
- [Releases](https://github.com/openclaw/openclaw/releases)

Key docs pages: [Architecture](https://docs.openclaw.ai/concepts/architecture), [Tools](https://docs.openclaw.ai/tools), [Gateway](https://docs.openclaw.ai/gateway)
