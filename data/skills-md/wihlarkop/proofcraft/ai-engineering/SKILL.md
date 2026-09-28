---
name: ai-engineering
description: >-
  Design, implement, or review AI/LLM features in a provider- and framework-neutral way: model
  contracts, structured output, tool calling, streaming, retrieval/RAG, context management,
  routing/fallback, latency/cost, failure handling, evals, and AI observability. Use when behavior
  depends on model inference or agent decisions. Select provider-specific SDKs only after the
  project has chosen them; verify nondeterministic behavior with appropriate eval evidence.
license: MIT
compatibility: Portable Agent Skills methodology; no runtime dependency.
metadata:
  suite: proofcraft
  suite-version: "0.1.0"
  skill-version: "0.1.0"
---


# AI Engineering

Treat model behavior as an external nondeterministic capability with an explicit contract and evaluation loop.

## Workflow

1. Define the product behavior and model contract before choosing a provider/model: inputs, allowed outputs/actions, latency/cost envelope, and failure behavior.
2. Prefer deterministic schemas/parsers/validators for properties that can be checked deterministically.
3. For tool use, define tool authority, argument validation, side-effect boundaries, retries, and user/approval boundaries where relevant.
4. For retrieval, define source authority, chunk/retrieval/rerank behavior, freshness, citation/provenance needs, and fallback when evidence is absent.
5. Define streaming/cancellation/context-limit behavior and what happens on provider rate limit, timeout, refusal, malformed output, or partial response.
6. Build evals from representative tasks and known failure modes. Compare baseline vs candidate; repeat stochastic cases enough to detect instability.
7. Instrument only the traces needed to debug/evaluate behavior and apply privacy/security constraints to stored prompts/tool data.
8. Use OpenAI/Anthropic/Gemini/local/vLLM/LiteLLM/etc. adapters only when the project already selects them or technology selection is explicitly in scope.

## Stop

Stop when AI behavior has a clear contract, failure/fallback semantics, and evaluation evidence appropriate to its nondeterminism and risk.
## Reference Guide

Load only the references needed for the current task:

- [evals observability](references/evals-observability.md)
- [model contract](references/model-contract.md)
- [retrieval tools](references/retrieval-tools.md)
- [principles](references/_shared/constitution/principles.md)
- [decision lock](references/_shared/constitution/decision-lock.md)
- [concerns](references/_shared/orchestration/concerns.md)
- [provider neutrality](references/_shared/engineering/provider-neutrality.md)
- [evidence](references/_shared/verification/evidence.md)
- [risk depth](references/_shared/verification/risk-depth.md)
