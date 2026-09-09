---
name: canonical-truth-conflict-resolver
description: Find and reconcile consequential conflicts across product and delivery records, such as completed status paired with unfinished stories, active risks, narrower shipped behavior, or unsupported availability claims. Use when asked which record is trustworthy, why status sources disagree, or what is actually merged, deployed, enabled, visible, incomplete, or unknown. Exclude ordinary backlog grooming and audits that begin with one known plan.
---

# Canonical Truth Conflict Resolver

Find the most consequential conflict in the requested product and delivery scope. Reconcile project status, story progress, active risks, shipped changes, and promised behavior, then state separately what is merged, deployed, enabled, customer-visible, incomplete, or unknown.

Apply the `devplan-product-context` foundation skill when available. Let it handle retrieval, graph interpretation, evidence quality, and delivery-state checks. If it is unavailable, say so. Do not imply Devplan was checked.

Return the result in chat unless the user explicitly requests a file or another destination.

Use Devplan and connected sources as read-only unless the user asks for a specific change. Do not update records or statuses without that request.
