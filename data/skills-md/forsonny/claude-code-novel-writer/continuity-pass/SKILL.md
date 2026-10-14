---
name: continuity-pass
description: Audit a chapter range or current manuscript for contradictions, timeline errors, knowledge leaks, rule violations, and unresolved continuity risks.
---

# Continuity Pass

Use any chapter range or priorities supplied with the invocation.

1. Resolve the requested scope. If none is supplied, use the most recent three completed chapters plus earlier chapters they directly depend on.
2. Read `.agents/roles/continuity-editor.md`.
3. If the harness exposes a named `continuity-editor` specialist, delegate the bounded audit to it. Otherwise perform that role directly.
4. Check findings against manuscript prose, character state, world state, and the accepted outline.
5. Group findings as critical contradiction, likely inconsistency, possible concern, and intentional or ambiguous.
6. Require exact manuscript file references for every finding.
7. Do not edit prose unless the user requested fixes.
8. If fixes are requested, make the smallest changes that restore continuity, then recheck the affected scope.
9. Clear `planning/continuity-flag.txt` only after the requested review has actually been completed.
10. Report what was checked, findings, fixes made, and remaining uncertainty.
