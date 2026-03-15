---
name: kairos-development
description: Use when an AI agent should run protocols or workflow tests against kairos-dev (KAIROS MCP in this repo's dev environment). Covers AI–MCP integration and workflow-test flows; MCP-only, reports/ output.
---

# KAIROS development — agent instructions for kairos-dev MCP

Use this skill when an AI agent should run protocols or workflow tests against **kairos-dev** (the KAIROS MCP in this repo’s dev environment). All instructions assume MCP-only usage: no shell, no filesystem except writing to `reports/`.

## When to use which flow

| Flow | File | Use when |
|------|------|----------|
| **AI–MCP integration** | [ai-mcp-integration.md](ai-mcp-integration.md) | Agent runs protocols **one by one** from a real-user perspective: import each protocol from `docs/examples/`, run it to completion, write **one report per protocol** under `reports/<run-id>/<protocol-folder>/report.md` with inline pretty-printed JSON. Tighter scope (no README, one report per protocol). |
| **Workflow test** | [workflow-test.md](workflow-test.md) | Agent runs the **four scenarios** (imports; search + workflows; update step; update chain). Single summary report at `reports/<run-id>/report.md` plus per-call JSON under `reports/<run-id>/calls/`. Use for dev/qa workflow validation. |

- For **one-by-one protocol runs** (e.g. scripted or “run each example as a user”): use **ai-mcp-integration.md**.
- For **full workflow test** (four scenarios, one run): use **workflow-test.md**.

## Related

- Mintable protocol examples: `docs/examples/protocol-example-*.md` (do not read `docs/examples/README.md` when under ai-mcp-integration constraints).
- Test harness and automated import test: `tests/workflow-test/` and `npm run dev:ai-mcp-integration` / `npm run dev:test -- tests/integration/kairos-mint-docs-examples.test.ts`.
- MCP payload (tools, prompts, resources) is in `src/embed-docs/` and served by the server at runtime.
