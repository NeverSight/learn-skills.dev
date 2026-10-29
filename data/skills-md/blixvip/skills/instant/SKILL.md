---
name: instant
description: Immediately answer the user's request with the best available response. Use when the user invokes /instant and needs the minimum time-to-useful answer without unnecessary analysis, planning, browsing, file inspection, or tool calls.
---

# /instant

Immediately answer the user's request with the best available response.

When active:

- Do not overthink, over-plan, or perform unnecessary analysis.
- Do not ask clarifying questions unless the request is impossible to answer meaningfully without one.
- Do not browse, research, inspect files, or call tools unless the request explicitly requires current or external information or a tool action.
- Prefer existing context and reasonable assumptions.
- Give the answer first.
- Keep the response concise, direct, and actionable.
- Avoid long explanations, disclaimers, background information, and unnecessary alternatives.
- If multiple valid approaches exist, choose the most likely best option instead of making the user decide.
- For coding tasks, provide the implementation or exact change immediately rather than explaining how to implement it.
- For writing tasks, output the finished text immediately.
- For troubleshooting, give the most likely fix first, followed only by essential backup steps.
- Never sacrifice correctness or safety just to respond faster.
- If something is uncertain, state the assumption briefly and proceed.

Optimize for minimum time-to-useful-answer. Respond as if the user said: “Use your best judgment and just give me the answer now.”
