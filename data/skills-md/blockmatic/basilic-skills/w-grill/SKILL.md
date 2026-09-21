---
name: w-grill
description: Relentless design-tree interview until the frontier is empty.
disable-model-invocation: true
---

Stress-test a plan or decision. Blocking gaps only use [clarify](../w-clarify/SKILL.md). Do not implement until the user confirms shared understanding. Do not write a glossary or a second ADR tree.

1. Inspect matching MDX, ADRs, README, and `DESIGN.md` for facts already recorded. Follow [council](../w-council/SKILL.md) steps 1–3 for filesystem or code facts. Do not ask the user for anything you can look up.
2. Map the work as a **design tree**: every decision branches into the decisions that hang off it. The **frontier** is every decision whose prerequisites are already settled.
3. Ask the whole frontier in one round. Follow [round format](references/round-format.md). Then wait.
4. Each round of answers reshapes the tree. Recompute the frontier. A running exploration is an unsettled prerequisite: ask the rest of the frontier now; questions downstream of it wait.
5. Stop when the frontier is empty. Confirm shared understanding. Do not act on it until the user says to.
