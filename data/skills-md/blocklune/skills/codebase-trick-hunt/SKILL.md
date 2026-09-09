---
name: codebase-trick-hunt
description: Hunt a codebase for language-specific, non-obvious coding tricks and report them as concise tips.
disable-model-invocation: true
---

# Codebase Trick Hunt

Find small, portable coding tricks suggested by a codebase, then report them as concise tips.

## Trick

A trick is a language, standard-library, framework, library, or type-system move that is useful but easy for a newcomer to miss. It should be concrete enough to change code and general enough to reuse outside this repository.

Good trick families include:

- Built-in APIs that replace manual loops or branching.
- Collection, iterator, string, path, async, or error-handling helpers.
- Type-system expressions that derive or constrain useful types.
- Existing project dependencies that provide a sharper helper than plain code.
- Idioms that make a small pattern shorter, safer, or clearer.

Reject generic advice, style opinions, architecture advice, and facts that only matter inside this repository.

## Workflow

1. Map the hunting ground.
   - Inspect metadata, lockfiles, config, and representative source files.
   - Identify the main languages, versions, and major libraries worth checking.
   - Completion: the searched languages and stack areas are named.

2. Hunt for candidates.
   - Look around loops, searches, filters, grouping, indexing, parsing, key/object manipulation, option/result handling, async code, repeated helpers, and type definitions.
   - Include tricks already used in the code and tricks that would simplify nearby code.
   - Completion: each main language or stack area has been checked or explicitly skipped.

3. Keep only real tricks.
   - Confirm the move is available in the project's language version or dependencies.
   - Drop anything too obvious, too broad, too clever without benefit, or too tied to local domain concepts.
   - Completion: every retained trick is locally plausible and portable.

4. Distill the tip.
   - Name the language or library, the move, and the general operation it solves.
   - Replace domain-specific situations with broad operations such as finding an index, keeping matching items, inspecting adjacent values, deriving key unions, or flattening nested values.
   - Completion: each tip can stand alone without knowing the repository.

5. Report the list.
   - Group tips by language or stack area.
   - Keep each tip short; add a tiny example only when a one-line tip would be unclear.
   - Include file paths as optional evidence, not as the subject of the tip.
   - Completion: the user receives a concise list of reusable tips.

## Tip Template

```md
- tip: In <language/library>, use <move> to <general operation> instead of <beginner approach>. Evidence: `path/to/file.ext`.
```

If evidence is unnecessary or unavailable, omit the evidence sentence.
