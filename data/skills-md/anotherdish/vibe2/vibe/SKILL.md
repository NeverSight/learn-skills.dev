---
name: vibe
description: Convert Vibe pseudocode in .vibe files, startvibe/endvibe source blocks, and source comments containing "vibe:" into working code. Use when the user invokes /vibe, asks to implement or resolve Vibe code, supplies a .vibe file, or references actual Vibe markers. Do not activate for incidental prose or documentation that merely discusses the word 'vibe'.
---

Vibe is a pseudocode framework for expressing implementation intent inside a codebase. Its contents may be valid target-language code, malformed approximations, prose, omissions, or any mixture of them. Treat Vibe syntax as evidence of intent, not as a literal implementation contract.

Transform the Vibe artifacts in the requested scope into working target-language code, then remove only the artifacts whose intent has been fully implemented.

## Scope

- Default to the entire repository.
- If the user explicitly names a path or component, limit the run to that scope and name the scope in the final result.
- Search tracked and unignored working-tree source, including untracked non-ignored files.
- If available, use the current git diff to understand vibe-scoped modifications to code for futher clarity of user intent
- Exclude generated output, dependencies, vendor code, caches, submodule internals, and similar derived or third-party content from vibe parsing
- If the declared scope contains no Vibe artifacts, make no changes and report that none were found.

## Recognizing Vibe

There are three artifact types:

1. Any file whose name ends in `.vibe`. One file may describe one target file or an entire component spanning source, tests, migrations, and configuration. The file's existence and location are themselves intent: they may signal the code structure the user wants (for example, an intended folder layout, module placement, or component boundary), so keep in mind the location and of the `.vibe` files when converting into real source files.
2. An inline region in a plausible target-language source file, delimited by `startvibe` and `endvibe`.
3. A single-line comment in a plausible target-language source file containing the literal marker `vibe:`. This comment draws attention to a specific line or nearby section of code. Treat its remaining text as the complete statement of intent and use its location to identify the code it targets.

Inline delimiters should:

- be standalone comment tokens valid for the containing file's language;
- match case-insensitively;
- allow whitespace around the token; and
- contain no trailing prose.

For example, `# startvibe`, `// STARTVIBE`, and `/* endvibe */` are markers when valid for the containing language

Multiple non-overlapping inline blocks in one file are valid. Nested, unmatched, or reversed markers are malformed. Report malformed markers with their locations and do not edit that file until their boundaries are clarified or corrected.

A single-line Vibe comment must be a valid comment for the containing language and may appear on its own line or after code. For example, `// vibe: handle an expired session here` and `value = load() # vibe: avoid doing this twice` are artifacts.
Do not treat `vibe:` in source language strings, documentation, data files, or multi-line comments as an artifact unless the user explicitly includes them.

## Workflow

### 1. Discover the complete inventory

Find every in-scope `.vibe` file, valid inline block, and single-line Vibe comment before editing. Bring the full inventory and enough surrounding repository context into the analysis so related artifacts are considered together.

For each artifact, identify:

- the behavior or structure it requests;
- its likely target language and destination;
- affected contracts, callers, tests, data, configuration, and external effects;
- dependencies on other Vibe artifacts or existing code; and
- ambiguities or contradictions that could materially change the result.

For `.vibe` files, infer the file's target from:

1. an explicit header or user instruction;
2. its path and filename;
3. nearby modules, imports, symbols, and tests; and
4. build manifests and repository conventions.

Build a lightweight dependency graph and plan to implement foundations before consumers.

- Treat an entire inline Vibe region as provisional intent, including lines that already look like valid production code.
- Treat a single-line Vibe comment as an instruction about the line or nearby section it identifies. Use the comment text and local code context to determine its target without requiring a larger Vibe block.


### 2. Establish sufficient clarity

Do not begin a target implementation unless you are sufficiently clear on the users intent for changes/additions. In the event of ambiguity, clarify with the user before editing rather than guessing.

### 3. Implement in dependency order

- Replace each understood artifact with a complete implementation that follows the repository's existing patterns and types.
- A `.vibe` file may require creating or updating multiple real files.
- Keep inline marker lines, single-line Vibe comments, and each `.vibe` file in place until their corresponding implementation is ready to validate.

### 4. Validate before removing vibe artifacts

Use the smallest existing syntax, formatting, type-check, build, or test commands that cover each changed component. 

If applicable validation fails, fix the implementation and rerun it. If failure exposes unresolved intent or correctness cannot be established, preserve the Vibe artifact and clarify the ambiguity with the user before proceeding.

When no applicable automated validation exists, strong contextual and structural confidence may suffice. 

Only after all outputs represented by an artifact are complete and sufficiently validated:

- remove the `startvibe` and `endvibe` marker lines from a successfully implemented inline block; or
- remove the entire successfully implemented single-line Vibe comment while preserving any code on the same line; or
- delete the successfully implemented `.vibe` file.

Never delete unresolved intent.

## Final response

Report concisely:

- the components implemented;
- the `.vibe` files deleted, inline blocks removed, and single-line Vibe comments removed;
- the validation performed
- any residual artifacts and why they remain.
