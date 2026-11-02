---
name: atlas-review
description: "Review code against standards and intent, interrogate changes with independent adversarial reviewers, trace downstream blast radius, assess interfaces or motion, and audit animation."
disable-model-invocation: false
---

# Atlas Review

Select methods from the requested outcome and the change's material risks. Combine methods when they answer distinct review questions. An explicitly bounded request such as “Code only” limits selection; an open-ended review leaves selection to you. Ask only when ambiguity changes the method. Read [Scope and ownership](references/ownership.md) and the selected methods.

| Mode | Need | Read and follow |
| --- | --- | --- |
| Code | Assess changes against standards and originating intent | [Code](references/code/code-review.md) |
| Adversarial | Interrogate changes, challenge blind spots or request multimodel review | [Interrogate](references/adversarial/interrogate.md) |
| Impact | Ask what a change could break beyond the diff and prove the facts its safety depends on | [Blast Radius](references/impact/blast-radius.md) |
| Static | Run scoped lint/typecheck checks and judge findings | [Static](references/static/static-review.md) |
| Interface | Assess a screen/flow, or interface problems introduced by a change | Select the interface scope below |
| Motion | Review animation against specialist standards | [Motion](references/motion/review-animations.md) |
| Motion Audit | Survey existing motion and prepare prioritized improvement plans | [Motion Audit](references/motion-audit/index.md) |

For Interface, use [Interface Changes](references/interface/changes/index.md) when the request names a branch, PR, commit range or uncommitted changes. Use [Interface Audit](references/interface/audit/index.md) for a screen, flow or repository audit. Preserve a supplied scope; ask when both interpretations remain materially different. Changes classifies introduced, regressed and pre-existing findings; Audit owns severity, consolidation and coverage. The six interface disciplines are bundled here, independent of a Craft installation.

Requests for `interrogate` or `blast-radius` select the corresponding bundled method. Keep Code's Standards and Spec reports distinct from other selected methods' findings.

Reviewing does not authorize fixes. Impact may run existing checks or owned scratch probes in isolated state; product code remains read-only. Motion Audit may write requested plans under the repository's artifact convention. Construction references bundled for motion judgments do not change that authorization. Follow [Motion ownership](references/motion-ownership.md) when UI polish and motion methods disagree.

Follow each method's evidence limits and independent-context requirements. After an authorized fix, use focused re-check when material uncertainty remains; stop with adequate evidence. Report checks and domains that could not be inspected without implying complete coverage. Atlas Verify is an optional follow-up when behavior checks or recorded QA are requested, or when existing evidence leaves a material behavior uncertainty.
