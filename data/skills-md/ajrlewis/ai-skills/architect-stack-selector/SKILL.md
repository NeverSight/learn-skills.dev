---
name: architect-stack-selector
description: Use when you want control-plane orchestration to select, scaffold, and validate minimal skills for production-default projects.
---

# Architect: Stack Selector Router

Use this skill when the user describes an app goal but has not chosen a concrete stack or skill set yet.
This is the control plane skill: choose minimal compatible skills, apply them, and run validations.

## Available Skills To Route

Base architect skills:
- `architect-python-uv-batch`
- `architect-python-uv-fastapi-sqlalchemy`
- `architect-nextjs-bun-app`
- `architect-nextjs-vercel-app`
- `architect-next-prisma-bun-vector`

Protocol architect skills:
- `architect-nostr-intent-router`

Add-on skills:
- `addon-decision-justification-ledger`
- `addon-human-pr-review-gate`
- `addon-auth-access-control`
- `addon-observability-telemetry`
- `addon-observability-python-structlog`
- `addon-observability-nextjs-pino`
- `addon-domain-semantic-adaptation`
- `addon-deterministic-eval-suite`
- `addon-llm-judge-evals`
- `addon-rag-ingestion-pipeline`
- `addon-docling-legal-chunk-embed`
- `addon-nostr-client-nextjs`
- `addon-nostr-nip-profile-selector`
- `addon-nostr-nip-sync-lock`
- `addon-nostr-key-custody`
- `addon-nostr-nip23-longform`
- `addon-llm-ancient-greek-translation`
- `addon-llm-translation`
- `addon-direct-llm-sdk`
- `addon-langchain-llm`
- `addon-langgraph-agent`
- `addon-google-agent-dev-kit`
- `addon-vercel-ai-labs`

UI skills:
- `ui-social-feed-shell`
- `ui-editorial-writing-surface`
- `ui-document-intake-dropzone`

## Router Workflow

1. Parse user intent into:
- app surface: `batch` | `api` | `web`
- exposure model: `public` | `internal` (infer `public` by default for `api` and `web` unless the user clearly says internal-only)
- language/runtime preference: `python` | `nextjs` | unspecified
- data/retrieval needs: RAG yes/no, source formats (pdf/markdown/html/csv/text)
- protocol needs: Nostr yes/no
- Nostr protocol intent details: client mode, capability intents, explicit NIP constraints
- persistence needs: relational DB yes/no, vector DB yes/no
- domain language intent: preferred terminology, forbidden terms, tone, and user-facing naming constraints
- execution constraints: network access, available binaries (`uv`, `bun`, `docker`), sandbox restrictions
- delivery mode preference: `production-default` (default) or explicit `NO_DOCKER=yes`
- review gate preference: `required` (default) or explicit opt-out
- decision justification preference: `required` (default, non-optional)
- semantic adaptation preference: `required` (default) or explicit opt-out
- observability preference: `required-for-public-api-web` (default) or explicit opt-out
- observability intensity: `baseline-runtime-default` | `explicit-full-telemetry-push` (infer `explicit-full-telemetry-push` only when observability is a primary user requirement; otherwise keep the baseline default)
- eval preference: deterministic `required` (default), llm-judge `optional` (default)

2. Pick exactly one base architect skill.

3. Add zero or more add-ons.

4. Execute scaffold:
- Apply selected skills in order.
- Produce required artifacts for production-default mode.
- Run selected skills' validation checklists.

5. Return:
- selected skills (ordered)
- one-line reason per skill
- install commands
- short execution order
- execution mode (`full` or degraded fallback mode) when constraints are present
- whether containerization is in-scope (`required` by default unless user explicitly opts out)
- whether human PR review gate is in-scope (`required` by default unless explicitly opted out)
- whether decision justification ledger is in-scope (`required` by default, no opt-out)
- whether semantic adaptation is in-scope (`required` by default unless explicitly opted out)
- whether observability telemetry is in-scope (`required` for public `api`/`web` by default unless explicitly opted out)
- whether observability intensity is baseline runtime-default or explicit full telemetry push
- whether deterministic eval suite is in-scope (`required` by default unless explicitly opted out)
- whether llm-judge evals are in-scope (`optional` by default unless explicitly requested)
- Nostr protocol routing status and selected NIP profile (when applicable)
- scaffold status and validation results

## Selection Rules

- If user asks for Python data processing or offline ingestion jobs:
  choose `architect-python-uv-batch`.
- If the user explicitly asks for Vercel deployment or a Vercel-optimized Next.js baseline:
  choose `architect-nextjs-vercel-app`.
- If environment is constrained (missing package managers and/or no network):
  keep selected architecture, but explicitly return a degraded fallback mode and what cannot be verified yet.
- Default to `production-default`. Docker is required by default across all runnable base architect skills.
- Default to `addon-human-pr-review-gate`.
- Default to `addon-decision-justification-ledger`.
- Default to `addon-domain-semantic-adaptation`.
- Default `observability intensity` to `baseline-runtime-default`.
- For `baseline-runtime-default`, add only the runtime-specific observability implementation add-on for public `api` and `web` surfaces:
  - Python `api` or worker runtime: `addon-observability-python-structlog`
  - Next.js or TypeScript server runtime: `addon-observability-nextjs-pino`
- Default to `addon-deterministic-eval-suite`.
- Only allow `local-no-docker` when user explicitly sets `NO_DOCKER=yes`.
- Only allow skipping `addon-human-pr-review-gate` when user explicitly requests opt-out.
- Do not allow skipping `addon-decision-justification-ledger` in production-default mode.
- Only allow skipping `addon-domain-semantic-adaptation` when user explicitly requests opt-out.
- Only allow skipping observability add-ons for public `api` and `web` surfaces when user explicitly requests opt-out.
- Only allow skipping `addon-deterministic-eval-suite` when user explicitly requests opt-out.
- If user asks for qualitative scoring, rubric grading, or "LLM as judge":
  add `addon-llm-judge-evals`.
- If user asks for Python API with database/migrations:
  choose `architect-python-uv-fastapi-sqlalchemy`.
- If user asks for a Next.js app without heavy backend DB requirements:
  choose `architect-nextjs-bun-app`.
- If user asks for Next.js + Prisma + Postgres + vector retrieval in one app:
  choose `architect-next-prisma-bun-vector`.
- If user mentions RAG, retrieval, embeddings, or document QA:
  add `addon-rag-ingestion-pipeline`.
- If user mentions legal PDFs/contracts/clauses and wants doc-to-markdown chunking:
  add `addon-docling-legal-chunk-embed` (typically with `addon-rag-ingestion-pipeline`).
- If user mentions Nostr relays/events/signing:
  add `addon-nostr-client-nextjs`.
- If user mentions Nostr and has not provided a complete NIP profile:
  add `architect-nostr-intent-router` before Nostr add-ons.
- For Nostr projects by default:
  add `addon-nostr-nip-profile-selector`.
- If user asks to fetch/update current NIPs or maintain a NIP lockfile:
  add `addon-nostr-nip-sync-lock`.
- If user requires private key handling, signer custody, or non-extension signing fallback:
  add `addon-nostr-key-custody`.
- If user requires NIP-23 long-form posts or Kind `30023`:
  add `addon-nostr-nip23-longform`.
- If user asks for LLM translation to Ancient Greek (`koine`/`attic`):
  add `addon-llm-ancient-greek-translation`.
- If user asks for general LLM translation/localization flows:
  add `addon-llm-translation`.
- If user asks for login, sessions, JWTs, API keys, RBAC, scopes, protected routes, or access control:
  add `addon-auth-access-control`.
- If user makes observability a primary requirement (for example asks for logging, metrics, tracing, health checks, production diagnostics, or telemetry as a named deliverable):
  set `observability intensity` to `explicit-full-telemetry-push`.
- If `observability intensity` is `explicit-full-telemetry-push`:
  add `addon-observability-telemetry` plus the runtime-specific observability implementation add-on when the runtime is known.
- If user asks for cross-runtime observability policy, asks for generic observability guidance before choosing a runtime, or the runtime does not have a dedicated implementation add-on:
  set `observability intensity` to `explicit-full-telemetry-push`;
  add `addon-observability-telemetry`.
- If user asks for direct provider SDK usage, explicit provider control, or to avoid LangChain/ADK/Vercel AI abstractions:
  add `addon-direct-llm-sdk`.
- If user asks for LangChain abstractions or LLM provider interactions (chat/completions/RAG chain execution):
  add `addon-langchain-llm`.
- If user asks for LangGraph orchestration or multi-step agent behavior (state machine, tool loops, checkpoints):
  add `addon-langgraph-agent`.
- If user explicitly asks for Google Agent Development Kit (ADK):
  add `addon-google-agent-dev-kit`.
- If user asks for Vercel AI SDK or AI Labs style chat/generation flows:
  add `addon-vercel-ai-labs`.
- If user asks for social timeline/feed UI (including X/Twitter-like structure):
  add `ui-social-feed-shell`.
- If user asks for minimalist/typography-first long-form writing UX:
  add `ui-editorial-writing-surface` (with Next.js + relevant add-ons).
- If user asks for PDF/Markdown upload intake UI:
  add `ui-document-intake-dropzone` (typically with `addon-rag-ingestion-pipeline`).
- If user gives domain-specific terminology or language preferences:
  add `addon-domain-semantic-adaptation`.

## Observability Intensity Examples

- Baseline runtime default:
  `Build a public FastAPI service for customer accounts with auth and Postgres.`
  Route to the Python base stack and include the runtime-specific observability add-on only.
- Explicit full telemetry push:
  `Build a public FastAPI service and add structured logs, metrics, tracing, health checks, and redaction rules.`
  Route to the Python base stack and include `addon-observability-telemetry` plus the runtime-specific observability add-on.
- Cross-runtime observability policy:
  `Define a shared observability policy we can apply across our Python API and Next.js app before we choose implementation details.`
  Add `addon-observability-telemetry` first, then add runtime-specific observability add-ons only after a concrete runtime is selected.

## Default Compositions

For public `api` and `web` flows in `production-default` mode, append the runtime-specific observability add-on as baseline observability unless the user explicitly opts out.

- Python PDF/Markdown RAG worker:
  `architect-python-uv-batch` + `addon-rag-ingestion-pipeline` + `addon-decision-justification-ledger` + `addon-domain-semantic-adaptation` + `addon-deterministic-eval-suite` + `addon-human-pr-review-gate`
- Python legal PDF clause RAG worker:
  `architect-python-uv-batch` + `addon-rag-ingestion-pipeline` + `addon-docling-legal-chunk-embed` + `addon-decision-justification-ledger` + `addon-domain-semantic-adaptation` + `addon-deterministic-eval-suite` + `addon-human-pr-review-gate`
- Python API with RAG endpoints:
  `architect-python-uv-fastapi-sqlalchemy` + `addon-rag-ingestion-pipeline` + `addon-observability-python-structlog` + `addon-decision-justification-ledger` + `addon-domain-semantic-adaptation` + `addon-deterministic-eval-suite` + `addon-human-pr-review-gate`
- FastAPI with auth and access control:
  `architect-python-uv-fastapi-sqlalchemy` + `addon-auth-access-control` + `addon-observability-python-structlog` + `addon-decision-justification-ledger` + `addon-domain-semantic-adaptation` + `addon-deterministic-eval-suite` + `addon-human-pr-review-gate`
- Python observability-first flow:
  `architect-python-uv-fastapi-sqlalchemy` + `addon-observability-telemetry` + `addon-observability-python-structlog` + `addon-decision-justification-ledger` + `addon-domain-semantic-adaptation` + `addon-deterministic-eval-suite` + `addon-human-pr-review-gate`
- Next.js observability-first flow:
  `architect-nextjs-bun-app` + `addon-observability-telemetry` + `addon-observability-nextjs-pino` + `addon-decision-justification-ledger` + `addon-domain-semantic-adaptation` + `addon-deterministic-eval-suite` + `addon-human-pr-review-gate`
- Next.js on Vercel baseline:
  `architect-nextjs-vercel-app` + `addon-observability-nextjs-pino` + `addon-decision-justification-ledger` + `addon-domain-semantic-adaptation` + `addon-deterministic-eval-suite` + `addon-human-pr-review-gate`
- Next.js Nostr client:
  `architect-nextjs-bun-app` + `architect-nostr-intent-router` + `addon-nostr-client-nextjs` + `addon-nostr-nip-profile-selector` + `addon-decision-justification-ledger` + `addon-domain-semantic-adaptation` + `addon-deterministic-eval-suite` + `addon-human-pr-review-gate`
- Next.js Nostr client with social feed UI:
  `architect-nextjs-bun-app` + `architect-nostr-intent-router` + `addon-nostr-client-nextjs` + `addon-nostr-nip-profile-selector` + `ui-social-feed-shell` + `addon-decision-justification-ledger` + `addon-domain-semantic-adaptation` + `addon-deterministic-eval-suite` + `addon-human-pr-review-gate`
- Next.js typography-first journal with NIP-23 + Ancient Greek translation:
  `architect-nextjs-bun-app` + `architect-nostr-intent-router` + `addon-nostr-client-nextjs` + `addon-nostr-nip-profile-selector` + `addon-nostr-key-custody` + `addon-nostr-nip23-longform` + `addon-llm-ancient-greek-translation` + `ui-editorial-writing-surface` + `addon-decision-justification-ledger` + `addon-domain-semantic-adaptation` + `addon-deterministic-eval-suite` + `addon-human-pr-review-gate`
- Next.js document intake UI for RAG:
  `architect-nextjs-bun-app` + `addon-rag-ingestion-pipeline` + `ui-document-intake-dropzone` + `addon-observability-nextjs-pino` + `addon-decision-justification-ledger` + `addon-domain-semantic-adaptation` + `addon-deterministic-eval-suite` + `addon-human-pr-review-gate`
- Full-stack Next + Prisma + vector search:
  `architect-next-prisma-bun-vector` + `addon-observability-nextjs-pino` + `addon-decision-justification-ledger` + `addon-domain-semantic-adaptation` + `addon-deterministic-eval-suite` + `addon-human-pr-review-gate` (+ `addon-rag-ingestion-pipeline` if ingest/retrieval pipeline needed)
- FastAPI with direct LangChain LLM endpoints:
  `architect-python-uv-fastapi-sqlalchemy` + `addon-langchain-llm` + `addon-decision-justification-ledger` + `addon-domain-semantic-adaptation` + `addon-deterministic-eval-suite` + `addon-human-pr-review-gate`
- FastAPI with LangGraph agent orchestration:
  `architect-python-uv-fastapi-sqlalchemy` + `addon-langgraph-agent` + `addon-decision-justification-ledger` + `addon-domain-semantic-adaptation` + `addon-deterministic-eval-suite` + `addon-human-pr-review-gate`
- Cross-architecture translation flow:
  `architect-nextjs-bun-app` or `architect-python-uv-fastapi-sqlalchemy` + `addon-llm-translation` + `addon-decision-justification-ledger` + `addon-domain-semantic-adaptation` + `addon-deterministic-eval-suite` + `addon-human-pr-review-gate`
- Cross-architecture direct LLM SDK flow:
  `architect-nextjs-bun-app` or `architect-python-uv-fastapi-sqlalchemy` + `addon-direct-llm-sdk` + `addon-decision-justification-ledger` + `addon-domain-semantic-adaptation` + `addon-deterministic-eval-suite` + `addon-human-pr-review-gate`
- Cross-architecture LangChain LLM flow:
  `architect-nextjs-bun-app` or `architect-python-uv-fastapi-sqlalchemy` + `addon-langchain-llm` + `addon-decision-justification-ledger` + `addon-domain-semantic-adaptation` + `addon-deterministic-eval-suite` + `addon-human-pr-review-gate`
- Cross-architecture LangGraph agent flow:
  `architect-nextjs-bun-app` or `architect-python-uv-fastapi-sqlalchemy` + `addon-langgraph-agent` + `addon-decision-justification-ledger` + `addon-domain-semantic-adaptation` + `addon-deterministic-eval-suite` + `addon-human-pr-review-gate`
- Google ADK agent flow:
  `architect-nextjs-bun-app` or `architect-python-uv-fastapi-sqlalchemy` + `addon-google-agent-dev-kit` + `addon-decision-justification-ledger` + `addon-domain-semantic-adaptation` + `addon-deterministic-eval-suite` + `addon-human-pr-review-gate`
- Next.js Vercel AI Labs flow:
  `architect-nextjs-bun-app` + `addon-vercel-ai-labs` + `addon-decision-justification-ledger` + `addon-domain-semantic-adaptation` + `addon-deterministic-eval-suite` + `addon-human-pr-review-gate`

## Output Template

Use this response shape:

```text
Selected skills (in order):
1) <skill-name> - <reason>
2) <skill-name> - <reason>

Install:
npx skills add ajrlewis/ai-skills --skill <skill-name>
npx skills add ajrlewis/ai-skills --skill <skill-name>

Execution order:
1) Apply base architect skill.
2) Apply add-ons.
3) Run each skill's validation checklist.
4) Summarize generated artifacts and any blockers.

Execution mode:
- full | offline-smoke | limited-by-sandbox

Containerization:
- required across runnable base architect skills (default) | explicit-no-docker (user requested)

Human review gate:
- required (default) | explicit-opt-out (user requested)

Decision justification ledger:
- required (default) | non-optional policy

Semantic adaptation:
- required (default) | explicit-opt-out (user requested)

Observability telemetry:
- required-for-public-api-web (default) | explicit-opt-out (user requested)

Observability intensity:
- baseline-runtime-default (default) | explicit-full-telemetry-push (user requested or clearly primary requirement)

Deterministic eval suite:
- required (default) | explicit-opt-out (user requested)

LLM judge evals:
- optional (default) | explicit-required (user requested)
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Prefer the smallest skill set that satisfies requirements.
- Do not select multiple base architects unless user explicitly requests a multi-repo architecture.
- `architect-nostr-intent-router` is a protocol control-plane architect and may be combined with one base architect.
- If a requirement conflicts with a selected skill, call it out and suggest the nearest valid composition.
- Surface blockers early (missing `uv`/`bun`, no network, restricted Docker) and include an actionable fallback.
- Never silently downgrade from production-default to no-docker behavior.
- Do not invent prompt-specific one-off skills during normal routing; compose generic `architect-*`, `addon-*`, and reusable `ui-*` skills.
- Prefer generic UI skills (`ui-social-feed-shell`, `ui-editorial-writing-surface`) with style inputs over brand-locked UI skill creation.
- Default to `addon-human-pr-review-gate` for production scaffolds.
- Default to `addon-decision-justification-ledger` for production scaffolds.
- Default to `addon-domain-semantic-adaptation` so user/domain language is reflected in output copy and docs.
- Default to `addon-deterministic-eval-suite` for hard pass/fail gating.
- Treat `addon-llm-judge-evals` as secondary quality scoring unless user explicitly makes it blocking.
- No skill decision should be returned without a concrete justification and trace entry.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
