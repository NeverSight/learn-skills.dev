---
name: ask-astra
description: Consults Astra on a bounded question while the calling agent retains task ownership.
---

# Ask Astra

Spawn a read-only advisor using `model: "gpt-6-astra"` and `fork_turns: "none"`.

Provide the question, relevant files or evidence, constraints, and what remains uncertain. Include prior decisions needed to understand the problem.

Ask for a recommendation, supporting evidence, tradeoffs, and uncertainty. The advisor must not edit files or delegate further.

Assess the advice against the task and available evidence, then continue the work. Consult again only when a material unresolved question warrants it.
