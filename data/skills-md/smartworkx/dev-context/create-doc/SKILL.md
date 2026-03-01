---
name: create-doc
description: >-
  Create documentation following docs-as-code conventions.
  TRIGGER when: user asks to create, write, or draft documentation, diagrams, or technical docs.
  Examples: "create a doc for...", "write architecture documentation", "add a C4 diagram", "document the domain model".
  DO NOT TRIGGER when: user wants an ADR (use create-adr), a spec (use create-spec), or just wants to read existing docs.
allowed-tools: Bash, Read, Write, Glob, Grep, AskUserQuestion
---

Create a new document following docs-as-code conventions.

## Steps

1. Ask the user what type of document to create:
   - **Architecture model** — C4 system/container/component diagram in Mermaid
   - **Domain model** — entities, relationships, ubiquitous language
   - **Technical doc** — how something works, runbooks, guides
   - **General** — any other prose documentation

2. If the user did not provide a document title as an argument, ask them for one

3. Explore the codebase for relevant context:
   - Read `CLAUDE.md` for project conventions
   - Check `doc/` for existing docs and structure
   - Look at related code or config files for accuracy

4. Create the document in the appropriate location:
   - Architecture models → `doc/architecture/`
   - Domain models → `doc/domain-model.md` (or `doc/domain/`)
   - ADRs → use the `create-adr` skill instead
   - Technical docs → `doc/`
   - General → `doc/`

5. Follow these conventions:
   - All docs are Markdown (`.md`)
   - Diagrams use Mermaid fenced code blocks — GitHub renders them natively
   - **Single-use diagrams** — inline in the document that needs them
   - **Shared diagrams** (referenced from multiple docs) — place in `doc/diagrams/` and link from each consumer
   - Architecture diagrams use C4 notation via Mermaid flowcharts
   - Keep prose concise and scannable — use headers, lists, and tables

6. Tell the user the file was created and its path
