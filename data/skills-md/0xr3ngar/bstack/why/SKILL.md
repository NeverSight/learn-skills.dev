---
name: why
description: "Use for \"why does X work this way\", \"why did we pick Y\", \"who is right\", and before a change to something whose reason is not known."
disable-model-invocation: true
license: MIT
compatibility: "Requires Git. Uses the GitHub CLI and T3 Code's thread search when they are present."
---

# Why

Answer from the record, not from the code. The code shows what exists. The record shows why.

- Read the commits and pull requests that introduced the thing, each later change, their review threads, the linked tickets and the design documents. Search the earlier agent threads too, with `t3_thread_search`.
- Quote what the authors wrote, with a link. Mark each inference of your own as an inference.
- Say what the record does not answer, and who can answer it.
- For a dispute, give the evidence of each side and then your verdict.
- Before a plan removes or reverses a decision, find its reason. A reason that no longer holds is the argument for the change.

For how something behaves at run time, read and run the code.
