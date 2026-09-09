---
name: technical-plan-with-devplan
description: Create a grounded technical implementation plan using product intent, specifications, acceptance criteria, current architecture and code, related decisions, delivery state, and risks. Use instead of plan-with-devplan when the requested artifact centers on how to build or complete work across architecture, components, data, APIs, migrations, rollout, testing, observability, or technical dependencies. Exclude product discovery plans, status-only briefs, and implementation work without a requested plan.
---

# Technical Plan with Devplan

Create a technical plan for the specified work using its specification, current codebase, product intent, acceptance criteria, and related decisions. Cover architecture, components, data or API changes, migration and rollout, testing, observability, dependencies, and unresolved questions. Distinguish repository facts from proposed design choices.

Apply the `devplan-product-context` foundation skill when available. Let it handle retrieval, graph interpretation, evidence quality, and delivery-state checks. If it is unavailable, say so. Do not imply Devplan was checked.

Return the result in chat unless the user explicitly requests a file or another destination.

Use Devplan and connected sources as read-only unless the user asks for a specific change. Do not implement or update project records without that request.
