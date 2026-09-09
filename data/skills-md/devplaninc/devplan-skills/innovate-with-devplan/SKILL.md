---
name: innovate-with-devplan
description: Propose the single highest-impact feasible product addition after examining the current product, codebase, roadmap, customer evidence, and existing work. Use when asked what new feature or product bet should be built next for a specified area. Exclude ordinary prioritization among known work, unmet-demand ranking, and open-ended brainstorming without selecting one winner.
---

# Innovate with Devplan

Propose the single highest-impact feasible new feature for the specified product area. Use the current product, codebase, roadmap, customer evidence, and existing work so the idea is specific and non-duplicative. Score the winner on leverage, surprise, feasibility, fit, defensibility, and compounding value, then briefly name the strongest runners-up.

Apply the `devplan-product-context` foundation skill when available. Let it handle retrieval, graph interpretation, evidence quality, and delivery-state checks. If it is unavailable, say so. Do not imply Devplan was checked.

Return the result in chat unless the user explicitly requests a file or another destination.

Use Devplan and connected sources as read-only unless the user asks for a specific change. Do not create a project or begin implementation without that request.
