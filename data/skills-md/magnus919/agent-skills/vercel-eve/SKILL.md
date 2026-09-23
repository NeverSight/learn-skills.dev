---
name: vercel-eve
description: >-
  Build, develop, deploy, self-host, secure, and troubleshoot durable backend AI agents with Vercel Eve. Use when creating an Eve agent, adding tools, skills, subagents, channels, schedules, sandboxing, durable sessions, observability, or deploying Eve on Vercel or a Node host. Do not use for the separate Vercel AI SDK Agent APIs such as ToolLoopAgent or WorkflowAgent; use an AI SDK-specific skill for those.
license: MIT
compatibility: Requires Node.js 24+ for the current Eve package. Deployment requires an LLM provider credential or Vercel AI Gateway access; self-hosted durable execution requires persistent workflow storage.
metadata:
  source: https://github.com/vercel/eve
  research_checked: "2026-07-15"
---

# Vercel Eve

Eve is a filesystem-first framework for durable backend agents. Treat the `agent/` directory as the application boundary and the deployment as a composition of independently replaceable HTTP, workflow, sandbox, model, credential, and observability layers.

## Operating contract

1. Start with the generated project structure. Put agent behavior in `agent/instructions.md`, runtime choices in `agent/agent.ts`, and one typed capability per file under its relevant directory.
2. Keep authority outside the model prompt. Use typed tools, connections, sandbox boundaries, and route authentication instead of placing credentials or policy in instructions.
3. Treat a durable session as a workflow, not an in-memory chat. Define persistence, idempotency, callback reachability, and recovery before relying on long-running or side-effecting work.
4. On self-hosted deployments, replace every Vercel service deliberately. A Node process that starts is not evidence that workflow callbacks, persisted state, schedules, sandbox isolation, authentication, and telemetry work.
5. Verify with a health request and a real authenticated session that exercises the workflow path. Never treat an HTTP 200 alone as a production readiness signal.

## When not to use

Do not load this for the separate `ai` package’s `ToolLoopAgent`, `WorkflowAgent`, or `HarnessAgent` APIs. Do not use it for generic Next.js deployment without an Eve agent. For vendor-neutral workflow orchestration, use the relevant workflow or agent-framework skill instead.

When such a request appears, say that Eve does not apply and route to current AI SDK documentation or an AI SDK-specific skill. Do not write AI SDK API code, model configuration, or deployment guidance from this skill.

## Project model

| Need | Default location |
|---|---|
| Always-on behavior | `agent/instructions.md` |
| Model and runtime options | `agent/agent.ts` |
| Typed actions | `agent/tools/*.ts` |
| On-demand procedures | `agent/skills/` |
| Narrower child agents | `agent/subagents/` |
| HTTP, Slack, or other entry points | `agent/channels/` |
| Typed external integrations | `agent/connections/` |
| Isolated compute | `agent/sandbox/` |
| OpenTelemetry setup | `agent/instrumentation.ts` |
| Recurring work | `agent/schedules/` |

Read [development and architecture](references/development-and-architecture.md) before creating or restructuring an agent.

## Quick start

```sh
npx eve@latest init my-agent
cd my-agent
npm run dev
```

Use the generated README and package scripts as the local source of truth. A minimal runtime configuration selects a model:

```ts
import { defineAgent } from "eve";

export default defineAgent({
  model: "anthropic/claude-opus-4.8",
});
```

On Vercel, a string model ID routes through AI Gateway and can use project OIDC. Outside Vercel, either configure `AI_GATEWAY_API_KEY` or use an AI SDK provider object with the provider’s normal credential. Do not assume that BYOK means the Gateway is bypassed.

## Build capabilities deliberately

### Tools

A tool is a typed boundary between model reasoning and an external action. Give it a narrow schema and a description that makes the authorization and side-effect boundary clear. A tool declares typed inputs, outputs, and side effects. It does not hold credentials or grant authority: keep integration credentials in connections and enforce authorization server-side before the effect occurs.

```ts
import { defineTool } from "eve/tools";
import { z } from "zod";

export default defineTool({
  description: "Look up a city’s current weather.",
  inputSchema: z.object({ city: z.string().min(1) }),
  async execute({ city }) {
    return { city, condition: "Sunny" };
  },
});
```

Use a skill for larger procedures that should load only when relevant. Use a subagent when the work needs a fresh history, narrower toolset, or isolated intermediate state.

### Credentials and execution

Use `agent/connections/` for typed service integrations. Use `agent/sandbox/` for generated code or shell work. Never place provider keys, OAuth tokens, or route-auth secrets in instructions, tool source, generated artifacts, or logs.

For sandbox design and lifecycle choices, read [development and architecture](references/development-and-architecture.md). For self-hosting backends and routing, read [deployment and self-hosting](references/deployment-and-self-hosting.md).

## Deploy

### Vercel

Use a Git-connected project or `vercel deploy`. Eve emits Vercel Build Output, uses Vercel Workflows for durable sessions, and normally selects Vercel Sandbox. Replace scaffolded placeholder authentication before exposing a browser-facing route.

### Self-hosted Node service

```sh
eve build
PORT=3000 eve start --host 0.0.0.0
```

This uses the normal Nitro Node output under `.output/`. Before production traffic, read [deployment and self-hosting](references/deployment-and-self-hosting.md) and explicitly verify persistent workflow storage, sandbox backend, model credential path, authentication, the `/eve/` and `/.well-known/workflow/` proxy prefixes, schedule execution, and telemetry.

Treat host paths, reverse-proxy product configuration, storage product, and scheduler implementation as target-specific evidence. If the target topology is not supplied or inspected, name the required contract and the missing evidence rather than inventing a configuration.

## Security and observability

- Replace placeholder authentication with a real policy before any production browser request. Outside Vercel, do not rely on `vercelOidc()` as the sole authenticator.
- Give sandboxes the minimum network and credential access required. A sandbox does not protect secrets that are deliberately injected into it.
- Vercel Agent Runs is convenient, but treat OpenTelemetry as the portable operational evidence path. Set `recordInputs` or `recordOutputs` to `false` when traces would contain sensitive data.
- For personal, sensitive, or regulated data, assess what model inputs, tool arguments, outputs, and traces are retained and disclose collection where required.

## Verification gate

1. Build the deployed artifact.
2. Confirm the health endpoint: `GET /eve/v1/health`.
3. Start one authenticated session: `POST /eve/v1/session`.
4. Attach to its stream and verify a real turn completes.
5. For self-hosting, exercise a durable workflow callback or resume path, not only a stateless reply.
6. Inspect the trace and ensure secrets and sensitive payloads are absent or intentionally redacted.

## Exit criteria

The task is complete only when the requested agent capability is implemented, its route and authorization boundary are explicit, and the relevant local or deployed session path has been exercised with evidence. See [source index](references/source-index.md) when validating version-sensitive behavior.