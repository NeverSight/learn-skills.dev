---
name: devplan-product-context
description: Use this foundational Devplan skill to automatically bring ambient product memory into product, customer, roadmap, project, launch, risk, planning, product-writing, coding, or review work that may depend on current evidence, decisions, delivery state, or product intent. Invoke even when the user does not mention Devplan if local context may be insufficient, or whenever a user or skill asks to consult Devplan. Skip generic tasks answerable from local evidence.
---

# Devplan Product Context

Use Devplan as an ambient context layer for the user's actual task. Consult it quietly, apply what matters, and produce the answer, plan, review, draft, or implementation the user requested. Do not turn an ordinary request into a report about Devplan.

## Keep the experience natural

- Think in Devplan's internal model, but speak in the user's language.
- Do not narrate tool selection, searches, graph traversal, hydration, internal object types, or opaque IDs.
- Describe what the information means: customer feedback, a prior decision, planned work, delivered changes, a current risk, or missing evidence.
- Cite readable source names, titles, dates, statuses, and links when evidence matters.
- Mention Devplan only when the user asks, attribution is useful, or its context materially changed the result.
- Explain the underlying graph or MCP only when the user asks how Devplan works, is debugging it, or needs the distinction to understand the answer.

## Consult Devplan effectively

1. Identify what current product, customer, planning, delivery, or organizational context could materially affect the task.
2. Treat the live Devplan MCP tool descriptions as the source of truth for available entities, relationships, retrieval methods, workspace identity, and current query behavior. Discover those capabilities at runtime rather than relying on a copied schema or client-specific tool names.
3. The MCP connection is already scoped to one workspace. Within that workspace, narrow retrieval by the relevant customer, project, product area, team, and time window. Do not blend similarly named but distinct contexts.
4. Retrieve only the context material to the task. Prefer focused evidence over broad summaries, and inspect readable underlying sources when a consequential claim requires them.
5. Reconcile Devplan context with the artifact being changed. Use local code as implementation truth and Devplan for cross-system context about intent, demand, decisions, and observed delivery.
6. Continue the original task using only context that materially improves it.

## Bound the research

- Plan one small evidence pass before retrieving. For focused work, target no more than four searches, two batch hydrations, and two underlying-source fetches. For broad cross-customer synthesis that must establish recurrence across several findings, allow up to six searches, three batch hydrations, and two underlying-source fetches. Exceed the applicable budget only when the user requests an exhaustive audit or consequential uncertainty requires it.
- Combine related intents into query groups when the live tools support it. Shortlist first, then hydrate finalists in batches; do not search or fetch every candidate independently.
- Reuse prior results and avoid equivalent searches, duplicate hydration, or repeated source fetches within the same task.
- Stop retrieving when each material conclusion has enough direct evidence to answer safely. State a focused limitation instead of continuing broad searches to prove absence.
- Exceed the default budget only to close a specific, material evidence gap. Do not expand retrieval merely to make an answer more comprehensive.

## Keep the answer compact

- Follow any user-specified format or length limit. Otherwise, use the smallest structure that answers the question, normally no more than five findings and two decisive citations per finding.
- Prefer a compact table when several findings share the same fields. Do not repeat the same evidence in an introduction, finding, caveat, and summary.
- Omit research narration, redundant conclusions, and generic caveats. Include only limitations that materially change confidence or interpretation.
- Return fewer findings rather than padding the result with weak evidence or additional prose.

## Preserve meaning

- Distinguish source-backed facts, Devplan synthesis, inference, assumptions, missing evidence, and general advice.
- Do not treat an empty result as proof that evidence does not exist.
- Keep planned, written, merged, deployed, enabled, customer-visible, adopted, and generally available states distinct.
- Treat stale, sparse, contradictory, or cross-context evidence as a confidence limitation.
- Say when missing or conflicting context materially limits the answer.

## Compose with task skills

When another skill matches the requested outcome, apply this context inside that workflow. Let the task skill determine the artifact and steps; do not replace it with a generic Devplan summary.

## Handle access and safety

- Use Devplan and connected sources as read-only unless the user asks for a specific change.
- Never send or schedule Slack, email, or customer messages. Draft only.
- Do not expose credentials, raw private customer content, full emails, prompts, or sensitive payloads unless explicitly necessary.
- If Devplan is unavailable, say it could not be checked. Continue with clearly labeled local evidence and assumptions only when safe.
- Stop rather than guess when missing evidence prevents a high-stakes customer, launch, security, or availability claim.
