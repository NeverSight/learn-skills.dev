---
name: auto-docs
description: Generate and maintain project documentation from the code (README, API reference, architecture notes, setup docs). Re-runnable to keep docs in sync after refactors. Use when a project has no docs, has docs that drifted from the code, or when a new contributor cannot get it running from the existing docs.
license: MIT
---

# Auto Docs

A protocol for generating and maintaining project documentation from the code. Docs rot because they live apart from the code that defines them. This protocol treats docs as derived: generate them from what is actually there, regenerate the parts that drifted, and skip the parts that maintain themselves.

## 1. Analyze project structure

Read the project before writing anything.

- Detect project type from manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`).
- Identify entry points and the public surface: exports, routes, CLI commands, config keys, environment variables.
- Locate existing docs and the install, build, test, and start commands.

Do not document what you have not read. A guessed API reference is worse than none.

## 2. Generate or update the README

Answer four questions in order: what is this, how do I run it, how do I use it, where do I go next. Use the actual install and usage commands. Update the sections that drifted; leave hand-tuned prose alone.

## 3. Generate the API reference

For each public export, route, or command: name and signature, one-sentence purpose, parameters with types and whether required, return or response shape, one usage example reflecting a real call site, and known errors. Document the public surface; skip private helpers.

## 4. Write architecture notes

For any non-trivial system: component responsibilities, data flow from input to output, relationships as a list or a markdown diagram, and the non-obvious design decisions with the constraint behind each.

## 5. Write setup docs

When install is more than one command: prerequisites, step-by-step from clone to running, an environment-variable table (name, controls, required, example, never a real secret), and how to verify the setup worked.

## 6. Keep docs in sync with code

This protocol is meant to be re-run. On re-run, diff the current code surface against what the docs describe. Regenerate the sections whose source changed, leave the rest, and flag docs that reference code that no longer exists. The value is in the second run and every run after.

## What to document vs skip

Document the public API (exports, routes, CLI commands, config keys, environment variables), how to install and run and test, architecture and data flow, and non-obvious design decisions. Skip private helpers, self-evident code, generated files, and prose that restates a function name.

Test for a doc: would a new contributor be slower without it? If not, the doc is noise.

## On committing

Generating docs and committing them are separate steps. Write the files, summarize what changed, and let the human decide when to commit. Do not auto-commit unless explicitly asked.

---

See full content at https://github.com/HermeticOrmus/auto-docs-skills.
