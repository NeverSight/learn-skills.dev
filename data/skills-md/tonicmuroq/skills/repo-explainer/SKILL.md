---
name: repo-explainer
description: Analyze a local repository and explain its purpose, architecture, implementation approach, and notable design/code decisions. Optionally include ASCII request/data-flow diagrams and minimal integration examples only when they are meaningful for the repository. Use when asked to read a repo, summarize how it works, review implementation quality, or extract practical usage patterns.
---

# Repo Architecture Explainer

## Objective

Read the current repository and produce an evidence-based architecture report with three required sections and two conditional sections:
1. What the repo does
2. Design ideas and implementation approach
3. Notable implementation/design decisions worth learning
4. ASCII flow diagram for request flow and data flow (conditional)
5. Minimal usable example (conditional)

Match the selected output language and keep claims grounded in repository files.

## Invocation Parameters

This skill uses text parameters in the invocation string. No separate typed argument system is required.

- `/repo-explainer` or `$repo-explainer`: output in English by default.
- `/repo-explainer chinese` or `$repo-explainer chinese`: output in Chinese.
- Also accept aliases:
  - Chinese: `chinese`, `zh`, `zh-cn`, `中文`
  - English: `english`, `en`, `英文`
- If the user explicitly asks for a language in the request body, that explicit request overrides invocation defaults.

## Workflow

### 1) Discover scope and entry points

- Confirm analysis scope as the current repository root.
- Build a fast inventory with `rg --files`.
- Prioritize these files first when present:
  - `README*`, `docs/**`
  - dependency and build manifests such as `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`
  - primary entry points such as `main.*`, `index.*`, `app.*`, framework boot files
  - public API surfaces for libraries, such as `src/index.*`, exported modules, `__init__.py`
  - examples/tests that reveal expected usage

### 2) Infer architecture from code

- Identify major runtime roles: client, API, worker, background jobs, storage, and external services.
- Trace request flow end-to-end: entry -> handlers/services -> storage/external dependencies -> response.
- Trace data flow: source -> validation/transform -> persistence/cache -> output.
- Anchor every major conclusion to concrete files.

### 3) Evaluate notable decisions

- Select 2-5 strong implementation/design decisions with concrete evidence.
- Prefer decisions such as:
  - clear module boundaries or layering
  - robust error handling and retries
  - typed interfaces/contracts
  - test strategy and coverage focus
  - configuration/secrets separation
  - migration/versioning strategy
- Explain why each selected decision is worth learning.

### 4) Decide whether the repo is a reusable library

- Treat the repo as a library only when most signals exist:
  - explicit exported API
  - usage instructions for consumers
  - versioning/release intent
  - examples that show external consumption
- If signals are weak, state that it is application-oriented and skip library example output.

### 5) Decide whether a flow diagram is meaningful

- Add section 4 only when non-trivial flow exists, such as:
  - network request lifecycle (client/server/API)
  - multi-step domain/data pipeline
  - async jobs, queues, cache, or storage boundaries
- Skip section 4 for trivial repositories where a diagram adds no explanatory value.
- For trivial libraries (for example a single pure function such as `return a + b`), prefer a one-line note: `No meaningful request/data flow to diagram.`

### 6) Produce final output

- Follow `references/report-template.md` by default.
- Keep the report concise but concrete.
- Include file paths as evidence in each section.
- Mark assumptions clearly when information is missing.
- Avoid inventing functionality not visible in repo files.
- Keep sections 1-3 always present.
- Include sections 4-5 only when they provide practical value; otherwise explicitly mark them `Skipped` with a short reason.

## Output quality rules

- Label key claims as `Confirmed` or `Likely`.
- Use plain ASCII only for diagrams.
- Include at least one request path and one data path when a diagram is included.
- Keep direction explicit with arrows such as `->`.
- If runnable examples are incomplete, provide a minimal skeleton and call out missing pieces.
- Do not force low-value artifacts. Prefer omission with reason over filler output.

## Reference files

- `references/report-template.md` for report structure and formatting
