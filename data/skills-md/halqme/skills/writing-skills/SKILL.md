---
name: writing-skills
description: Use this skill when designing, creating, improving, or verifying agent Skills, including editing an existing SKILL.md or bundled references/scripts, evaluating Skill behavior, or improving activation. Do not use it merely to run an existing Skill.
---

# Writing Skills

Treat a Skill as a small, reusable service: a precise trigger, a focused contract, an executable workflow, and clear completion criteria. Add only guidance that the agent would otherwise miss; keep the main file concise and use progressive disclosure for details.

## Workflow

1. **Inspect the target**: read `SKILL.md`, frontmatter, and the contents of `references/`, `scripts/`, `assets/`, and evaluation files when present. Identify the Skill's trigger, non-trigger, inputs, outputs, side effects, failure behavior, and current gaps.
2. **Define the contract and activation**: Write a specific `description` in imperative form—preferably “Use this skill when …”—that states the user intent it serves, when it applies, and meaningful cases where it should not trigger. The `description`, not the `name`, is the primary activation mechanism. Prefer concise, lowercase, hyphen-separated names that state an action on an object, such as `implement-change` or `verify-work`. If naming a Skill this way is difficult, treat that as a signal that it may describe a quality, policy, or implementation technique rather than a well-bounded task. Follow the host’s documented name syntax and length limits; do not rely on the name alone for activation.
3. **Design the smallest useful procedure**: prefer a clear default over a menu of equivalent options. Match specificity to risk: use flexible guidance for judgment-heavy work and exact commands/guardrails for fragile or consequential operations.
4. **Place information deliberately**: keep trigger-critical gotchas and the core workflow in `SKILL.md`; move detailed API knowledge, edge cases, examples, and runbooks to directly linked reference files. Keep references one level deep and state when each one should be read.
5. **Add verification**: require the agent to inspect or validate its output before proceeding. For batch, destructive, or high-stakes work, use an intermediate plan and validate it before execution. For deterministic repeated work, prefer a tested script; document its inputs, outputs, prerequisites, exit codes, and safe defaults.
6. **Evaluate and refine**: test realistic positive, negative, and boundary prompts with a fresh context. Compare against a baseline or previous version when possible, record concrete evidence, then revise only the underlying gap.
7. **Finish safely**: pause to clarify missing or materially ambiguous inputs, failed validation, insufficient permissions, or unclear external effects. Report changed files, checks, failures, and remaining uncertainty.

## Improving an existing Skill

When the request is to improve, review, split, or operationalize an existing Skill, use this focused audit before changing it:

1. Confirm the target directory and inspect its `SKILL.md`, references, scripts, assets, and evals.
2. Compare the declared trigger with the actual workflow. Check the non-trigger boundary, inputs, outputs, side effects, failure handling, and completion criteria.
3. Keep the body focused on the contract and core procedure. Move long API details, examples, and runbooks to references; move deterministic repeated work to scripts.
4. Preserve names and behavior unless the request calls for a change. Explain any changed trigger, interface, or workflow briefly.
5. Validate the result with the repository's available checks and `git diff --check`. For scripts, check both normal and failure inputs.

## Techniques, loops, and patterns

Skills have three complementary building blocks. Choose only those that improve the target Skill; do not add sections mechanically.

### Techniques

A **technique** is a focused instruction for a recurring decision or failure mode. Useful techniques include:

- **Gotchas**: state concrete facts that defeat reasonable assumptions.
- **Defaults**: choose one recommended tool or approach and name a brief escape hatch.
- **Templates**: show the required output shape when format matters.
- **Checklists**: make dependencies and completion criteria visible.

Put high-value gotchas in `SKILL.md`; put lengthy templates or domain details in a directly linked reference.

### Loops

A **loop** is a feedback cycle, not just a sequence of steps. Use the smallest loop that matches the risk:

- **Validation loop**: do the work → validate against a script or checklist → fix → validate again.
- **Evaluation loop**: run representative cases → grade observable assertions → inspect traces/feedback → revise → rerun.
- **Plan–validate–execute loop**: inspect the source of truth → create a structured plan → validate the plan → execute only after it passes → verify the result.

Define what counts as passing and a practical completion threshold. A parser check alone is not enough to establish useful behavior.

### Patterns

A **pattern** is a reusable information or workflow structure:

- **Progressive disclosure**: overview and navigation in `SKILL.md`; conditional detail in one-level-deep references.
- **Conditional workflow**: branch explicitly for materially different cases instead of listing unrelated options.
- **Examples**: pair representative inputs with outputs when quality depends on style or shape.
- **Bundled script**: execute deterministic reusable logic rather than asking the agent to reinvent it each time.

Patterns are means, not requirements. Prefer a short Skill with one coherent workflow over a catalog of generic advice.

## References

Read only the files relevant to the current task:

- [`references/best-practices.md`](references/best-practices.md): detailed authoring guidance, calibration, progressive disclosure, workflows, scripts, and the effective-Skill checklist. It reflects the official Claude Skill best practices.
- [`references/using-scripts.md`](references/using-scripts.md): script interfaces, structured output, errors, exit codes, safe defaults, and dependency handling.
- [`references/evaluating-skills.md`](references/evaluating-skills.md): eval cases, assertions, baselines, grading, comparison, and iteration.
- [`references/optimizing-descriptions.md`](references/optimizing-descriptions.md): trigger evaluation and description optimization.

## When to pause or ask

Clarify the target or desired behavior when ambiguity would change the Skill's scope or behavior. When the ambiguity is minor, choose a conservative default and record the assumption. Treat publication, installation, deletion, overwriting unrelated files, and Git history changes as separate actions that need explicit authorization. If a check fails, either address it or report the failure and its impact; distinguish a partial result from a verified completion.
