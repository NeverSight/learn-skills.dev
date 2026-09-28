---
name: flow-docs
description: "Human-facing documentation grounded in current code. Use when writing or updating a README, contributing guide, usage docs, API reference or architecture docs. Feeds `flow-review` or `flow-ship`."
metadata:
  stage: build
---

# Document

Start from the reader's question. Docs earn space by letting someone use, change or reason
about the system without rediscovering its constraints.

## Process

1. Identify the reader and the doc's job: tutorial, task guide, reference or explanation.
   Inspect existing docs and the actual API, behavior, config and examples.
2. Ground claims in source, tests, history, ADRs or issues. Explain invariants and tradeoffs;
   label inferred rationale as inference and never invent historical intent.
3. Colocate docs with what they explain when the repo supports it. Keep one source of truth
   and link with stable anchors instead of maintaining contradictory copies. Generate
   repetitive reference material when existing tooling does it reliably.
4. Give readers the procedure or contract: prerequisites, working commands, inputs, outputs,
   failure cases and limits. Keep consumer-facing signatures, parameters and examples even
   when they also appear in source.
5. Run examples or check them against the installed API. Validate links and anchors,
   regenerate owned docs and inspect the output. Mark unrun or access-dependent examples as such.
6. Prune obsolete or duplicated material with no reader value. Keep legal notices, tool
   directives, supported compatibility notes and still-needed rationale.

## Anti-patterns

- Paraphrasing source without answering a reader question.
- Deleting useful reference material only because code also contains it.
- Stale commands from memory or invented reasons for an old design.
- Hand-editing generated pages instead of their generator or source.

## Done when

- The reader can perform the task or understand the stated contract.
- Claims, examples and links match current source, with verification limits visible.
- Generated artifacts and their sources agree.

Use `flow-review` for correctness review or `flow-ship` when the docs are part of delivery.
