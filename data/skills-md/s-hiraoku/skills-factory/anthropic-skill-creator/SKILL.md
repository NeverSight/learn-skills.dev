---
name: anthropic-skill-creator
description: Design, review, and improve Claude/Codex skills based on Anthropic's "The Complete Guide to Building Skills for Claude". Use when creating a new skill, rewriting SKILL.md frontmatter and workflows, fixing under-triggering or over-triggering, designing scripts/references/assets, building test cases, or preparing a skill for upload/distribution.
---

# Create Skills

Build skills that trigger correctly, execute reliably, and stay concise.

## Core Principles

- Use progressive disclosure:
  - Frontmatter (`name`, `description`) for trigger selection.
  - `SKILL.md` body for core workflow.
  - `references/` for deep details loaded only when needed.
- Keep skills composable: avoid assumptions that this is the only active skill.
- Prefer deterministic scripts for fragile validation logic.

## Workflow

1. Define 2-3 concrete use cases.
2. Draft trigger-strong frontmatter.
3. Design reusable resources (`scripts/`, `references/`, `assets/`).
4. Write actionable instructions and error handling.
5. Run triggering/functional/performance tests.
6. Iterate based on under-trigger/over-trigger signals.

## 1) Define Use Cases

Capture for each use case:
- User phrasing (what they actually say)
- Intended result
- Multi-step workflow and required tools (built-in and/or MCP)
- Failure points that need guardrails

If use cases are vague, ask targeted follow-up questions before authoring.

## 2) Frontmatter Design (Most Important)

Write only what is needed to trigger correctly.

Required fields:
- `name`: kebab-case, matches folder name
- `description`: include BOTH
  - What the skill does
  - When to use it (trigger phrases/context/file types)

Description formula:
- `[What it does] + [When to use it] + [Key capabilities]`

Good pattern:
- "Processes PDF legal documents for contract review. Use when users ask for clause extraction, risk flags, or redline summaries from .pdf contracts."

Bad pattern:
- "Helps with projects."

Precision controls:
- Add negative triggers to reduce over-triggering.
- Mention relevant file types when applicable.
- Keep wording aligned with real user phrases from use cases.

## 3) Resource Plan

- `scripts/`: deterministic checks/transforms used repeatedly
- `references/`: large docs, domain logic, variant-specific guidance
- `assets/`: templates and artifacts used in outputs

Rules:
- Keep `SKILL.md` compact; link to `references/`.
- Avoid extra docs in skill folder (`README.md`, changelog, etc.).

## 4) Instruction Writing

Write imperative, testable steps.

Include:
- Clear step order and dependencies
- Validation checkpoints
- Common errors with concrete fixes
- Example user inputs and expected outputs

For critical checks, prefer scripts over prose-only checks.

## 5) Test Protocol

Run these three test groups.

### A. Triggering Tests

- Should trigger on obvious requests
- Should trigger on paraphrased requests
- Should NOT trigger on unrelated requests

Target benchmark:
- Trigger on ~90% of relevant prompts in a 10-20 prompt suite

### B. Functional Tests

Validate:
- Correct outputs
- Tool/API call success
- Error handling paths
- Edge cases

### C. Performance Comparison

Compare with vs without skill:
- Number of clarification turns
- Failed tool/API calls
- Token usage
- End-to-end completion quality

## 6) Iteration Rules

Under-triggering signals:
- Skill does not load when expected
- Users keep manually invoking it

Fix:
- Add clearer trigger phrases and technical terms to `description`.

Over-triggering signals:
- Skill loads for unrelated requests

Fix:
- Add negative triggers and tighten scope language.

Execution issues:
- Inconsistent outputs, retries, user corrections

Fix:
- Tighten instructions, add explicit validations, and script critical checks.

## Troubleshooting Quick Guide

- Upload fails with missing `SKILL.md`: file must be exactly `SKILL.md`.
- Invalid frontmatter: verify YAML delimiters `---` and valid syntax.
- Invalid skill name: use lowercase kebab-case.
- Skill not followed: move critical instructions to top and make them concrete.
- Slow behavior: move long content to `references/`; reduce enabled skills.

## Packaging

Validate and package before distribution:

```bash
python3 .agents/skills/skill-creator/scripts/quick_validate.py <skill-dir>
python3 .agents/skills/skill-creator/scripts/package_skill.py <skill-dir>
```

## References

- `references/checklist.md`
- `references/prompt-templates.md`
- `references/patterns.md`
- `references/source.md`: source PDF and extracted principles
- `references/trigger-examples.md`: trigger/non-trigger examples for description tuning
- `references/failure-remedies.md`: failure patterns and minimum effective fixes
