---
name: backlog-reality-groomer
description: Reconcile named backlog items with current delivery reality and classify each as still needed, delivered, partially delivered, superseded, duplicate, stale, or unclear. Use when asked to reality-groom stories, acceptance criteria, or backlog scope against current product and implementation evidence. Exclude general backlog prioritization, new-demand discovery, and verification of one customer-facing claim.
---

# Backlog Reality Groomer

Reality-groom the specified backlog items. Classify each as still needed, delivered, partially delivered, superseded, duplicate, stale, or unclear. Support each classification with current project, change, risk, and code evidence.

Apply the `devplan-product-context` foundation skill when available. Let it handle retrieval, graph interpretation, evidence quality, and delivery-state checks. If it is unavailable, say so. Do not imply Devplan was checked.

Return the result in chat unless the user explicitly requests a file or another destination.

Use Devplan and connected sources as read-only unless the user asks for a specific change. Do not update backlog items without that request.
