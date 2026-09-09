---
name: explain-with-devplan
description: Explain how a product, feature, project, or workflow works today and trace why it exists back to customer feedback, decisions, and product assumptions. Use when asked both what something does and why it was built, especially when a PRD or current project statement may obscure the earlier origin. Exclude status-only briefs, future plans, and implementation-only technical explanations.
---

# Explain with Devplan

Explain how the specified product, feature, project, or workflow works today and trace why it exists back to the earliest relevant customer feedback, internal decisions, and product assumptions. Do not treat a downstream PRD or objective as the origin. Separate documented demand and decisions from inferred rationale, and call out planned or partial behavior.

Apply the `devplan-product-context` foundation skill when available. Let it handle retrieval, graph interpretation, evidence quality, and delivery-state checks. If it is unavailable, say so. Do not imply Devplan was checked.

Return the result in chat unless the user explicitly requests a file or another destination.

Use Devplan and connected sources as read-only unless the user asks for a specific change. Do not update records or send messages without that request.
