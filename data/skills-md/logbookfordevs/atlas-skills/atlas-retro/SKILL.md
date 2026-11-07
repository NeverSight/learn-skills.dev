---
name: atlas-retro
description: "Review a coding session and improve future agent runs: Diagnose proposes environment improvements; Enforce implements explicitly requested prevention of recurring mistakes."
disable-model-invocation: true
---

# Atlas Retro

Plain `atlas-retro` selects Diagnose. Select Enforce only when the user explicitly asks to implement prevention for recurring mistakes; a correction or request for recommendations alone stays advisory. An explicit mode takes precedence.

| Mode | Outcome | Read and follow |
| --- | --- | --- |
| Diagnose — default | Inspect the selected session and propose environment improvements, ordered by severity | [Diagnose](references/diagnose/retro.md) |
| Enforce — explicit | Implement prevention for the authorized recurring mistake classes and prove the guardrails | [Enforce](references/enforce/correct.md) |

For a combined request, use Diagnose to identify candidates, then Enforce only the authorized subset. Reuse supplied findings and evidence rather than repeating adequate diagnosis. Ask only when the requested repair scope remains ambiguous; existing authorization needs no second approval.

Use the current session unless another is named. Read only the selected conversation and directly relevant repository evidence; report inaccessible history as a gap. A proposal, implemented guardrail, local proof, CI run and published change are separate outcomes. Follow the repository's validation and delivery policy.
