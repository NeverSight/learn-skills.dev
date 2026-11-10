---
name: curate
description: Use when the user asks, in a named module, to write or update a knowledge-base page (concept, table, contract, usage flow, or pattern) from a raw artifact, a schema or table export, or code, for example "write a contract page for X", or to mark an artifact processed. Not for answering questions from existing pages or registering modules.
---

# Curate

If `tools/kb/kb.py` is missing but `AGENTS.md` and `modules.md` exist,
the workspace predates the integrity tool: tell the user to run the init
skill, which upgrades it, and stop. Run tool commands from the workspace
root; use `python3` or `py -3` where `python` is
missing or older than 3.9.

## Before writing

1. Resolve the module in `modules.md`. Read its `AGENTS.md`, its
   knowledge-base `INDEX.md`, and its `inventory.md`.
2. Choose the page type and template from `templates/wiki/` in the
   workspace:
   - table: a schema, export, or data structure → `tables/<name>.md`;
   - contract: a function, class, or API that others call →
     `contracts/<name>.md`;
   - usage flow: a user or system flow across steps → `usage/<name>.md`;
   - pattern: one technical shape repeated in two or more places →
     `patterns/<name>.md`. There is no pattern template: use the usage
     flow template and list every place the shape occurs;
   - concept: the module's purpose, boundaries, and terms → `concept.md`.
     If the module has no `concept.md` yet, write it first.
3. Look the subject up first: `python tools/kb/kb.py resolve "<name>"`.
   If a page for it exists, update that page instead of creating a
   second one. Facts that serve several modules go to
   `knowledge-base/shared/`.
4. Large inputs: read a source file over about 50 KB through
   `python tools/kb/kb.py outline <file>` and then only the span you
   need. A table export goes through `python tools/kb/kb.py table <export> --module <module>`
   (the `kb` skill's table procedure covers a layout the tool does not
   know yet). Evidence that is not in `source-artifacts/` yet is
   taken in first with `python tools/kb/kb.py ingest <path> --module <module>`.

## Writing

5. Write the page under `knowledge-base/modules/<module>/`. Every
   non-obvious claim ends with a confidence label:
   - `confirmed`: seen in code, data, or a document you read;
   - `inferred`: concluded from evidence, not stated anywhere;
   - `runtime-unverified`: depends on behavior you could not run;
   - `blocked-by-access`: the evidence exists but you cannot reach it.
   `confirmed` may name its layer: `schema-confirmed` (structure seen in
   an export) or `runtime-confirmed` (observed running).
   Set the page-level `confidence:` to the weakest label on the page.
6. Required sections: a table page has `## Keys`, `## Fields`, and
   `## Relations`; a class or function contract has `## Purpose` and
   `## Signature`.
7. The page's `source:` line names the artifact copy under
   `source-artifacts/` it was written from.
8. Never edit source code while curating.

## After writing

9. In `inventory.md`, end each line the page now covers with
   `-> <page path>`, or with `excluded: <reason>` when it deliberately
   stays out.
10. Add or update one line for the page in the module `INDEX.md`: path
    and the question the page answers.
11. Do not touch the artifact or `source-artifacts/INDEX.md`. Once the
    page names the copy in `source:`, the write hook (or the next
    `python tools/kb/kb.py fix --safe`) records the artifact as processed
    in the registry. Files stay where they are.

Finish with the close-session skill.
