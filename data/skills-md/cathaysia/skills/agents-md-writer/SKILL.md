---
name: agents-md-writer
description: Create or rewrite AGENTS.md files in strict English policy language. Use this skill whenever the user asks to create AGENTS.md, agents.md, agent instructions, repository policy files, contributor guardrails, or execution rules for coding agents. This skill enforces absolute command language, removes carve-out wording, and validates that the final AGENTS.md uses MUST, NEVER, REQUIRED, and FORBIDDEN instead of softer language.
---

# agents-md-writer

Create an `AGENTS.md` file that reads like a hard policy document for coding agents.

The final `AGENTS.md` output MUST satisfy every rule below:

- The file MUST be written in English only.
- The file MUST use absolute, command-style policy language.
- The file MUST rely on `MUST`, `NEVER`, `REQUIRED`, and `FORBIDDEN`.
- The file MUST NOT use softer modal language.
- The file MUST NOT contain carve-out wording.
- The file MUST NOT use vague scope statements.
- The file MUST NOT use qualitative adjectives without measurable limits.

## Required Style

Every rule in `AGENTS.md` MUST be direct, enforceable, and unambiguous.

Use patterns such as:

- `All new environment variables MUST be documented in .env.example.`
- `Generated files MUST be ignored or committed intentionally.`
- `Debug-only code is forbidden.`
- `Tests that fail locally MUST be fixed before handoff.`

## Forbidden Wording

The final `AGENTS.md` MUST NOT contain any of the following words or phrases:

- `should`
- `should not`
- `recommended`
- `may`
- `optional`
- `except`
- `unless`
- `however`
- `but`

The final `AGENTS.md` MUST NOT contain equivalent escape-hatch phrasing. Rewrite those statements into unconditional rules.

The final `AGENTS.md` MUST NOT use vague language such as:

- `narrow`
- `small`
- `minimal`
- `appropriate`
- `clear`
- `concise`
- `readable`
- `simple`
- `careful`
- `reasonable`

The final `AGENTS.md` MUST NOT use equivalent wording that leaves scope, size, or quality open to interpretation.

Bad pattern:

- `Tests should pass before merge, but small docs changes are fine.`

Required rewrite pattern:

- `All changes MUST keep the test suite green.`
- `Pure documentation changes MUST still pass the required validation commands.`

Bad pattern:

- ``#![allow(...)]` scope MUST stay narrow.`

Required rewrite pattern:

- ``#![allow(...)]` MUST appear only on a single item, a single statement block, or a single function.`

Bad pattern:

- `Function documentation MUST be concise.`

Required rewrite pattern:

- `Function documentation MUST NOT exceed 20 lines.`
- `Function documentation MUST NOT exceed 300 words, excluding code examples.`

## Workflow

1. Inspect repository context before writing.
2. Extract concrete rules from the codebase, tooling, and user request.
3. Rewrite every rule into strict policy language.
4. Replace vague scope statements with explicit targets, file paths, syntactic locations, commands, counts, or limits.
5. Replace qualitative descriptions with measurable thresholds.
6. Remove any sentence that depends on exceptions, caveats, or softened guidance.
7. Produce the final `AGENTS.md` in English only.
8. Run the validation checklist before returning the file.

## Repository Inspection

Read only the files needed to determine real constraints. Prioritize:

- `README*`
- package manifests such as `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`
- lint and format config
- test config
- CI workflows
- existing policy or contribution docs

Convert discovered conventions into hard rules only when the repository actually depends on them.

## Output Contract

When the user asks for a new file, produce `AGENTS.md` content that is ready to write as-is.

When working in a repository, organize the file into short sections such as:

- `Scope`
- `Workflow`
- `Code Quality`
- `Testing`
- `Change Control`

Every bullet or sentence in those sections MUST be a rule, not commentary.

Every scope statement MUST identify the exact target it governs. Valid targets include:

- named files
- named directories
- named commands
- named CI jobs
- named syntax locations
- line counts
- word counts
- byte limits
- time limits
- coverage thresholds

Every quality rule MUST be expressed as a measurable constraint.

## Validation Checklist

Before returning the final result, verify all of the following:

- `AGENTS.md` is entirely in English.
- Every rule is written as a command or prohibition.
- The file uses `MUST`, `NEVER`, `REQUIRED`, or `FORBIDDEN` where normative language is needed.
- The file does not contain `should`, `should not`, `recommended`, `may`, or `optional`.
- The file does not contain `except`, `unless`, `however`, or `but`.
- The file does not contain equivalent carve-out wording.
- The file does not use vague scope terms such as `narrow`, `small`, `minimal`, or equivalent wording.
- The file does not use qualitative adjectives such as `concise`, `clear`, `readable`, or equivalent wording without measurable limits.
- Every scope rule names its exact target or syntactic location.
- Every limit is measurable by count, threshold, path, command, or syntax target.
- The file does not explain policy with soft rationale inside rule bullets.

If any validation check fails, rewrite the file until every check passes.

## Response Pattern

When delivering the result:

1. Present the final `AGENTS.md` content first.
2. State that the file passed the wording validation.
3. List any repository-specific assumptions in plain English outside the file.
