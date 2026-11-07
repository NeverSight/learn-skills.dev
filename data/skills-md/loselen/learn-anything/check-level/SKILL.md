---
name: check-level
description: Find what someone can and can't do in a topic, and why each failure happens. Use for placement or diagnostic tests, "what should I learn next", finding gaps or misconceptions, or when someone keeps getting something wrong. Normally called by map-topic.
license: MIT
---

# Check level

Based on knowledge space theory (Doignon & Falmagne), think-aloud research (Ericsson & Simon) and procedural bug research (Brown & Burton).

## Probe

- Open with an easy item, one the learner can likely pass, so the check starts with a win. Never open with the hardest item.
- Climb toward the goal on the graph, one step harder each time. After a pass, spot-check one prerequisite only if the next item is a stretch. After a fail, move one level down and probe again.
- Keep the tone light: say it's a check of the material, not a test of them, and don't stack more than two fails in a row. Follow a fail with an item they can pass.
- Give two items per node, with different surfaces, before concluding.
- Match each item to the kind of knowledge:

  | Kind | Item |
  |---|---|
  | procedure | Do it on a new case |
  | principle | Predict an outcome, or find a bug |
  | concept | Classify an example |
  | structure | Label the parts |
  | facts | Recall them |

- Ask the learner to "keep saying what you're thinking." Don't ask them to explain their reasoning during the task, because that changes how they think. Ask why afterwards.

## Classify each failure

| Type | Signal | Fix |
|---|---|---|
| Missing prerequisite | Also fails a node below | Teach that node first |
| Bug | Same wrong move every time | Name and correct the rule they follow |
| Slip | Inconsistent, and fixed on a recheck | Nothing to teach |
| Needs support | Succeeds with a hint | Note which hint worked |
| No transfer | Passes only the familiar form | Vary the practice |

## Report

- **Solid**: passed.
- **Shaky**: the most recently learned solid nodes. Review these first.
- **Ready next**: failed, with all prerequisites solid.
- **Not yet**: everything else.
- Each failure with its type, plus any missing prerequisites found.

Hand the report back to map-topic.

## With a learning vault

If the user has a learning vault (a folder whose root `AGENTS.md` starts with `# Learning vault rules`), follow its rules and append a dated entry to `## Level checks` in each lesson note you probed: result, failure type, and the hint that worked.
