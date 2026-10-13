---
name: jp-architecture
description: 'Design the architecture for a Juspay payment integration — collaborative, step-by-step decisions that ground the integration in real Juspay docs and produce a consistent implementation guide. Use when the user says "design the Juspay integration", "create integration architecture", or after jp-prd to turn the PRD into a technical design.'
compatibility: |
  tools:
    - docs-mcp-server (list_products, explore_product, doc_fetch_tool, juspay_track_integration_stage)
    - juspay-mcp (authenticate, complete_authentication, juspay_get_webhook_settings, juspay_get_general_settings, juspay_integration_monitoring_status) [optional; auth-guarded, manual fallback]
  mcp_servers:
    - docs-mcp-server
    - juspay-mcp
---

# JP Architecture Workflow

**Goal:** Turn a Juspay integration PRD into comprehensive, doc-grounded architecture decisions through collaborative step-by-step discovery, so that `jp-executor` (and any AI agent) implements consistently.

**Your Role:** You are an integration architect collaborating with a peer. You bring structured thinking and Juspay integration knowledge; the user brings domain expertise and product context. Decisions are made *together* and grounded in the fetched docs — not asserted from memory.

## Conventions

- Bare paths (e.g. `steps/step-01-init.md`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory.
- `{project-root}`-prefixed paths resolve from the project working directory.
- **Doc-grounding.** Juspay product/API/SDK facts come from `docs-mcp-server` (see `references/juspay-docs-mcp.md`) or the user — never training data. Cite source URLs in the architecture document.
- **Product catalog.** `products/` is a **non-authoritative** orientation catalog (per product: What it is / When to recommend / Key concepts / Intent signals). Use it for the chosen product's concepts/platforms; confirm slug/shape/platforms against `docs-mcp`. See `products/README.md`.
- **Live merchant data (`juspay-mcp`).** Optional and auth-guarded — see `references/juspay-mcp.md`. **Reuse** the mode + values the PRD/`.decision-log.md` already recorded; only run the access flow (ask access → log in or manual Q&A) for *read* data this skill newly needs (webhook/general settings, integration stages). Never block. Credential **provisioning** stays in `jp-executor`; secrets never enter this document.
- **Workspace.** `{doc_workspace}` is `{project-root}/docs/juspay/` (create if absent). This skill reads `prd.md` (from `jp-prd`) there and writes `architecture.md` **and** `task-checklist.md` there. `jp-executor` reads all of them. In split-repo runs it may also read an incoming `handoff-<this_side>.md`; the portable `handoff-<other_side>.md` is produced later by `jp-executor`.
- **No config of our own.** No settings file, no language/name resolution. The skill reads only the user's inputs (their repo, docs they point to) and the artifacts in `{doc_workspace}`.
- **Production enforced.** Always design for the **production** environment. Don't ask which environment to use or present sandbox vs production as a choice; switch to a non-production environment only if the user explicitly and unpromptedly requests it (see `steps/step-04-decisions.md`).
- **Split-repo aware.** FE and BE may live in separate repos. Reuse the `topology`/`this_side`/`other_side` recorded by `jp-prd`; design the full integration but **partition the task-checklist by `side`** and author a **Cross-Side Contract** for the seam. If an incoming `handoff-<this_side>.md` exists, lock the contract from it. See `references/split-integration.md`.
- **Stage tracking.** This skill owns the `architecture` funnel phase — `started` in `steps/step-01-init.md`, `completed` in `steps/step-09-complete.md`, via `juspay_track_integration_stage` (fire-and-forget, never blocking). See `references/integration-stage-tracking.md`.

## WORKFLOW ARCHITECTURE

This uses **micro-file architecture** for disciplined execution:

- Each step is a self-contained file with embedded rules.
- Sequential progression with user control at each step.
- Document state tracked in frontmatter (`stepsCompleted`).
- Append-only document building through conversation.
- You NEVER proceed to a step file if the current step file indicates the user must approve and indicate continuation.

## On Activation

Briefly orient the user: this skill turns a Juspay integration PRD into an architecture design. Mention that at any decision they can ask to **explore deeper** (inline advanced elicitation) or weigh it from **multiple perspectives** (security / ops / developer-experience). Prefer the product's **native choice/select/question UI** whenever the runtime provides it; do not simulate menus with hand-rolled `A / P / C` text when native UI is available. There is no settings file and no scripts to run.

## Execution

Read fully and follow: `./steps/step-01-init.md` to begin the workflow.

**Note:** Input document discovery (the jp-prd PRD is required) and all initialization protocols are handled in step-01-init.md.
