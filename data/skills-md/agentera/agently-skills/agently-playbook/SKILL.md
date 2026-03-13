---
name: agently-playbook
description: Use when the user wants to build, validate, optimize, or refactor a model-powered assistant, internal tool, automation, evaluator, or workflow from a business scenario or common problem statement, including project-structure refactors that may separate model setup, prompt config, and orchestration, even if the request also mentions a UI, app shell, or local model service such as Ollama, and it is still unclear whether the solution should stay a single request, add supporting capabilities, or become orchestration. The user does not need to mention Agently explicitly.
---

# Agently Playbook

Use this skill first when the request still starts from business goals, refactor goals, product behavior, or broad model-app language.

The user does not need to say Agently, TriggerFlow, or any other framework term. Generic asks such as "build an assistant", "help me design an internal tool", or "create a validator for common problems" should still start here when the owner layer is unresolved.

Requests that also mention a UI, a web page, a desktop shell, or a local model service such as Ollama should still start here when the request is fundamentally about shaping a model-powered tool rather than only wiring one narrow capability.

## Workflow

1. Reduce the request into scenario and atomic goals.
2. Choose the narrowest native Agently capability path.
3. Name the concrete operations or primitives that should be used.
4. Name the validation rule that proves the design stayed native-first.

## Capability Routing

- model provider setup or settings-file-based model separation -> `agently-model-setup`
- request-side prompt design or config-file prompt bridge -> `agently-prompt-management`
- output schema and reliability -> `agently-output-control`
- response reuse, metadata, or streaming consumption -> `agently-model-response`
- session continuity or restore -> `agently-session-memory`
- tools, MCP, FastAPIHelper, `auto_func`, or `KeyWaiter` -> `agently-agent-extensions`
- embeddings, KB, or retrieval-to-answer -> `agently-knowledge-base`
- branching, concurrency, waiting/resume, mixed sync/async orchestration, event-driven fan-out, process-clarity refactors, runtime stream, or explicit multi-stage quality loops -> `agently-triggerflow`
- migration choice between LangChain and LangGraph -> `agently-migration-playbook`

## Anti-Patterns

- do not skip this playbook when the owner layer is unresolved
- do not invent custom output parsers, retry loops, or orchestration first
- do not treat multi-agent, judge, or review flows as separate framework surfaces before checking native Agently capabilities

## Read Next

- `references/capability-map.md`
