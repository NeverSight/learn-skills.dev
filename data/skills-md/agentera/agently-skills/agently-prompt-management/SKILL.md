---
name: agently-prompt-management
description: Use when the user is shaping how one model request or request family should be instructed or templated, including prompt slots, input/instruct/info layering, mappings, recursive placeholder injection, prompt config, YAML or config-file-driven prompt behavior, and reusable prompt structure.
---

# Agently Prompt Management

Use this skill when the core problem is how prompt state should be structured before one request or request family runs.

## Native-First Rules

- prefer `input(...)`, `instruct(...)`, `info(...)`, and `output(...)` over concatenated prompt strings
- move reusable prompt structure into prompt config or YAML instead of ad hoc literals
- keep runtime variables as `${...}` placeholders in prompt files and inject them through mappings at load time
- keep task-specific request contracts in prompt config, and keep only widely reused persona setup in small code-side factories
- keep prompt composition separate from transport and orchestration
- use config files as an editable bridge when UI or product teams need to adjust prompt-driven behavior without rewriting workflow code

## Anti-Patterns

- do not flatten business context into one opaque string unless the task is trivial
- do not rebuild prompt templates through ad hoc `.format(...)` or string concatenation when prompt mappings already fit
- do not use prompt config files as a substitute for workflow state

## Read Next

- `references/overview.md`
