---
name: commitment-and-staleness-watch
description: Find important product or engineering commitments, promises, and target dates that went quiet, remain unfinished, slipped, or became blocked. Use when asked what follow-through is overdue, which commitments need attention, or who must make a decision now. Exclude general project status briefs, backlog grooming, and commitments explicitly dismissed or superseded.
---

# Commitment and Staleness Watch

Review commitments in the requested scope and find the most important promises or target dates that went quiet, remain unfinished, slipped, or became blocked. Connect each finding to current project, story, pull-request, risk, and evidence state, then identify the owner or decision needed now without reviving explicitly dismissed commitments.

Treat a requested start date as the boundary for when a commitment was made or explicitly reaffirmed - not when an older record was reviewed. Exclude earlier promises without an in-window recommitment.

Apply the `devplan-product-context` foundation skill when available. Let it handle retrieval, graph interpretation, evidence quality, and delivery-state checks. If it is unavailable, say so. Do not imply Devplan was checked.

Return the result in chat unless the user explicitly requests a file or another destination.

Use Devplan and connected sources as read-only unless the user asks for a specific change. Do not update work or contact owners without that request.
