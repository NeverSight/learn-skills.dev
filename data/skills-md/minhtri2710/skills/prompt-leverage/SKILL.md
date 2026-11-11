---
name: prompt-leverage
description: Strengthen a raw user prompt into an execution-ready instruction set for Codex or another AI agent. Use when the user wants to improve an existing prompt, build a reusable prompting framework, wrap the current request with better structure, add clearer tool rules, or create a hook that upgrades prompts before execution.
---

# Prompt Leverage

Turn the user's current prompt into a stronger working prompt without changing the underlying intent. Preserve the task, fill in missing execution structure, and add only enough scaffolding to improve reliability.

## Workflow

1. Read the raw prompt and identify the real job to be done.
2. Infer the task type with the script's deterministic whole-word keyword rules; `--task` overrides inference.
3. Rebuild the prompt with the framework blocks in `references/framework.md`.
4. Keep the result proportional: do not over-specify a simple task.
5. Return both the improved prompt and a short explanation of what changed when useful.

## Transformation Rules

- Preserve the user's objective, constraints, and tone unless they conflict.
- Prefer adding missing structure over rewriting everything stylistically.
- Add context requirements only when they improve correctness.
- Add tool rules only when tool use materially affects correctness.
- Add completion criteria for non-trivial tasks, naming the objective checks that decide them.
- Keep prompts compact enough to be practical in repeated use.

## Output Modes

Choose one mode based on the user request.

- `Inline upgrade`: provide the upgraded prompt only.
- `Upgrade + rationale`: provide the prompt plus a brief list of improvements.
- `Template extraction`: convert the prompt into a reusable fill-in-the-blank template.
- `Hook spec`: explain how to apply the framework automatically before execution.

## Hook Pattern

When the user asks for a hook, model it as a pre-processing layer:

1. Accept the current prompt.
2. Classify the task and risk level.
3. Expand the prompt using the framework blocks.
4. Return the upgraded prompt for execution.
5. Optionally keep a diff or summary of injected structure.

Use `scripts/augment_prompt.py` for a first-pass rewrite. It classifies locally, without network access or credentials. Task order and keywords live in its `TASKS` table, the fallback task in `detect_task`; matching is case-insensitive and whole-word. Pass `--task` to override classification and `--intensity` to set the effort level (levels and default are in the script). The rewritten result preserves the prompt text's internal whitespace, including code fences and newlines.

## Quality Bar

An upgraded prompt still matches the original intent, adds no unnecessary
ceremony, names the objective checks the task has, and gives the agent a clear
definition of done.

If the prompt is already strong, say so and make only minimal edits.
