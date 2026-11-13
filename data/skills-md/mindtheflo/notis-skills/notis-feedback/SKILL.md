---
name: notis-feedback
description: Gather passive user feedback on an SDK-powered report or app view through selected-text comments, app-defined annotations and generic chat context pills.
mcp_resource: true
mcp_tool_patterns: []
---

# Notis Feedback

Use the shared [SDK context pattern](../notis-spaces/references/context.md) owned by `notis-spaces`. If the sibling reference is not installed, load the `notis-spaces` skill or its hosted MCP guide by name to access it. Read that reference before authoring feedback interactions; do not maintain a second report renderer or feedback contract.

1. Identify the existing report or app view and the content the user wants reviewed.
2. Enable feedback only on the relevant SDK content region. Add custom questions or controls only when useful; selected-text comments need no executive template.
3. Use the optional nearby comment box or the app’s own UI. Add each chosen response as an explicit context pill with `useAgentContext()`. Apps own annotation storage; the SDK does not store a separate feedback ledger or send messages. Context can include arbitrary JSON and explicit attachments, such as image coordinates and the image being reviewed.
4. Use the owning report or app workflow for building, verification and authorized persistence. Feedback does not authorize executing proposals, deploying an app or publishing a Store listing.

For a new report, use the [reports guidance](../notis-spaces/references/reports.md) in `notis-spaces`. Plain HTML pages saved in Notis Notes do not support this SDK pattern.
