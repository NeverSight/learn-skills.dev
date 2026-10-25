---
name: ai-system-architecture
description: How to architect AI/LLM PRODUCTS, not just call a model. Use when building agents, RAG, memory hierarchies, tool calling, MCP, model routing, prompt caching, guardrails, evaluation, sandboxing, human-in-the-loop, AI observability.
when_to_use: |
  - building AI agents, RAG, memory hierarchies
  - tool calling, MCP, model routing
  - guardrails, evaluation, sandboxing, human-in-the-loop, AI observability
license: MIT
metadata:
  version: "0.11"
  category: system-design
compatibility: OpenCode, Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, Windsurf, Cline
---

# AI System Architecture

An LLM is **one component**, not the application. The application owns the workflow; the LLM
performs reasoning. **Design deterministic systems around probabilistic models** — the system
provides reliability, the model provides intelligence.

## Golden rule

Never ask *"What model should I use?"* Ask *"What capability do I need?"* — reasoning, extraction,
classification, coding, vision, embeddings, planning, tool use. Different capabilities need
different models.

## AI pipeline & components

```
User → Intent → Planner → Context Builder → Retriever → Memory → Prompt Builder
     → LLM → Tool Calls → Verification → Post-processing → Response
```

Components: Interface → Orchestrator → Memory → Retriever → LLM → Tool Executor → Storage →
Observability. Never put all logic inside prompts.

## Agent loop: Planner → Executor → Critic

- **Planner:** breaks goals, prioritizes, selects tools. Never executes.
- **Executor:** tool calls, API/DB/files/browser/code. No planning.
- **Critic:** verification, validation, policy enforcement, output quality. Every complex workflow
  needs one.

## Memory hierarchy (never store everything)

1. **Working** — conversation, current task (short-lived)
2. **Session** — current session, preferences, files, intermediate state
3. **Long-term** — persistent knowledge, user prefs, projects, docs, embeddings
4. **Knowledge base** — company docs, specs, API docs, source (not conversation)
5. **External systems** — CRM, GitHub, Slack, Jira, DBs. The agent *retrieves*, never memorizes.

## Context engineering

Tokens are expensive; every token must justify itself. Priority: system rules → goal → relevant
memory → relevant files → retrieved knowledge → history → examples. **Context quality > quantity** —
never dump the whole repo; retrieve relevant/recent/necessary.

## RAG & retrieval

Retrieve **before** generation. Pipeline: Query → Rewrite → Embedding → Search → Rank → Filter →
Compress → Prompt → LLM. Prefer **hybrid search** (keyword + semantic). Embeddings are *indexes*,
not memory — original data stays the source of truth. **Chunk** by section/heading/function/semantic
boundary; poor chunking destroys RAG quality.

## Tools, MCP, routing

- **Tool calling** over hallucination: DB, GitHub, FS, search, browser, calculator, payments.
- **MCP:** reuse existing servers (GitHub, Slack, browser, DB, cloud) — don't rebuild.
- **Orchestrator** owns planning/retries/timeouts/tool execution/memory/model selection/state.
- **Model router:** coding→coding model, vision→vision model, classification→small, reasoning→large.
  Don't use the largest model for everything.

## Cost, caching, evaluation

- Estimate prompt/completion/embedding/retrieval/storage/tool/inference/latency cost — every
  workflow has a budget.
- **Prompt caching** (system prompts, retrieved context, tool outputs) + **semantic cache** (reuse
  similar solutions).
- **Observability:** prompt, model, latency, cost, retrieved docs, tool calls, errors, retries,
  feedback. **Evaluation:** accuracy, latency, cost, tool success, retrieval quality, groundedness,
  hallucination rate, task success.

## Guardrails, durability, safety

- **Human-in-the-loop** for payments/deploys/deletes/emails/publishing/code/infra.
- **Guardrails** validate input/output/tool calls/permissions/safety. Verify via tools, not
  confidence. **Sandbox** generated code (containers/MicroVMs/Firecracker/E2B). **Failure recovery:**
  retry → fallback model → human escalation. **AI security:** least privilege; never expose secrets/
  PII/internal architecture.
- **Multi-agent** only when distinct expertise exists (Planner→Researcher→Coder→Reviewer→Tester);
  agents exchange goals/state/artifacts/events, never whole conversations.

## Architecture decision tree

```
Need an AI feature?
  ↓
What capability? (reasoning / extraction / vision / embeddings)
Complex multi-step? → Planner → Executor → Critic + durable workflow
Need external data? → Tools / MCP (reuse)
Need knowledge? → RAG (hybrid search)
Long-lived agent? → Memory hierarchy + durable workflow
Generated code? → Sandbox
Irreversible action? → Human-in-the-loop
```

## Anti-patterns

- ❌ Putting all logic inside prompts
- ❌ Dumping the entire repo into context
- ❌ Trusting LLM output without verification
- ❌ Using one model for every task
- ❌ Executing generated code on production
- ❌ No evaluation / observability · fully automating irreversible actions

## Architecture prompts

- What capability do I need (not which model)?
- Is the context relevant / recent / necessary?
- Can a tool verify this instead of guessing?
- What is the fallback if the model fails?
- Where does state live outside the model?
