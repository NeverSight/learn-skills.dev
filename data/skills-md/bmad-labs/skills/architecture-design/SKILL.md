---
name: architecture-design
description: Use when the user asks for a design package, designs folder, detailed design, solution design, or contracts of a system or service before it is built — C4, project structure, module design, ERD or data model, domain events, ingress or egress API (REST, gRPC, Kafka, Pub/Sub, SQL), sequence, class, state, or data pipeline diagrams — at a high, medium, or low level of detail; or asks to review, correct, or update an existing design package against its requirements.
---

# Architecture Design

## Overview

A design package is the **skeleton and the contracts** of a system: its boxes, its data, the shapes that cross
every boundary, and the flows between them. It is a helicopter view. It never holds the body of a function.

Core principle: **one canon, single-source contracts, every protocol file proven by a real tool, one folder at a
time with the user.**

**Follow 70%, create 30%.** The templates in `templates/` (index: `references/templates.md`) are the default
shape (the 70%). Every template has REQUIRED slots — keep them always. The rest (the 30%) you adapt to the use case: add a folder the system needs,
drop one it does not, split a big file, pick the protocol file that fits. Record each adaptation in one line in the
canon's "Folders" table, so the reader knows it was deliberate.

## When to use

- "Create the designs", "design package", "detailed design", "solution design", "API contracts", "data model".
- The user names design kinds: C4, ERD, events, API docs, sequences, class diagrams, pipeline.
- Not for: choosing between options (use `trade-off-analysis` first), a slide deck (use `slide-maker`), an
  architecture decision document only (use `bmad-architecture`), writing code.

## Depth levels

Ask which level the user wants, unless they already said. Each level includes the one above it.

| Level | Designs | Answers |
| --- | --- | --- |
| **High** | C4 context + container, ERD, external contracts (every API and event the system serves, calls, produces, consumes) | "What are the parts, what data, what crosses the border?" |
| **Medium** | + project structure, module design, main logical flow, main data flow (pipeline), entity state design (states + transition table), domain event catalog, error codes, configuration | "How is it organized and how does one unit of work move?" |
| **Low** | + class diagram per module, sequence per workflow, flow diagrams for hard decisions, interfaces between layers and modules (commands, ports, DTOs), code interfaces (signatures only) | "What does each module expose and who calls what?" |

Never at any level: method bodies, algorithms in code, migrations, framework boilerplate. A signature and a
one-line contract ("returns the next order to ship, or none") is the lowest you go.

## Workflow

1. **Load context.** Read the intent, PRD, architecture spine, standards, and the user's reference designs (ERD,
   event sheets, API sheets, C4 images). List them back. Ask for missing ones.
2. **Pick the level and the folder list.** Propose numbered folders from
   [references/templates.md](references/templates.md) §Package layout. Get agreement. Copy `templates/` to the
   target and delete the folders the level does not need.
3. **Write the canon first** (`designs/README.md`): folders, identifiers, topics, event catalog, API list,
   decision register (D1…), open items (DQ-1…). Every later folder uses its names. Guide: `templates/GUIDE.md`.
4. **Build one folder at a time**, in dependency order: project structure → data model → events → ingress →
   egress → integrations → state → sequences → classes → pipeline. For each folder:
   1. Read the folder's `templates/<folder>/GUIDE.md`, then copy its template files. Copy the user's reference
      format (columns, naming, envelope) before inventing one.
   2. Put contracts in a **single source** (catalog JSON/YAML); generate md, schemas, examples, proto with a small
      script when there are more than ~5 items of one kind. Change the source, never the generated file.
   3. **Validate** with the real tool ([references/checklists.md](references/checklists.md) §Validators).
      Add one negative test: a bad message the schema must reject.
   4. Run the folder checklist. Fix. Re-validate.
   5. Report to the user: what is in it, what to check, new open items. **Stop and wait for review.**
   6. Apply feedback. Log each decision (who decided, what) in the canon or the memlog.
5. **Propagate.** A change that touches a name, field, code, or rule:
   1. Update in order: upstream architecture → canon → each folder → generated files (edit the source, re-render).
   2. List every retired name (old field, code, command, config key, file name). `grep -rn` each one across the
      package and upstream docs, history files excluded. Result: zero hits, or each hit fixed.
   3. Render each changed diagram alone (a batch run hides which file failed). Re-run every validator.
   4. Report the sweep list and its result with the validator results.
6. **Close.** Update the upstream architecture document with the decisions. When a decision contradicts the PRD or
   intent, list it as a "PRD correction" and route it to the PRD owner (change proposal), so the two agree. Point the
   PRD's schema line at the package's data-model folder. List open items and assumptions.

Build the package yourself, folder by folder. Parallel builder agents break naming consistency across folders.

## Review or change an existing package

1. Read the package, the upstream architecture, the requirements, and the decision log (who decided what) first.
2. Trace every commit: what if the process dies right after it? Who sends the next command, the event, the timer?
   Read each rule as two builders would; two valid readings is a finding.
3. Each finding: location (`file:line`), the quoted line, a failure scenario, the smallest fix.
4. A fix that reverses a recorded user decision is a question (at most 4, recommended option first). Apply the
   user's pick, even when it is not your recommendation. Apply every other fix.
5. Apply, then run step 5 (Propagate) and step 6 (Close).

## Diagrams: pick the tool

| Condition | Tool | Guide |
| --- | --- | --- |
| A concept, C4 view, pipeline, workflow, or timeline with ≤ ~10 boxes | Hand-written SVG, coordinates computed by a small script | [references/svg-diagrams.md](references/svg-diagrams.md) |
| A sequence, class, state, or ERD diagram, or any graph past ~10 nodes | PlantUML | [references/plantuml-recipes.md](references/plantuml-recipes.md) |
| The user rejected a PlantUML diagram's look twice | Switch to hand SVG | svg-diagrams.md |

## Principles that made the output good

| Principle | Rule |
| --- | --- |
| Reference first | Follow the user's ERD, event sheet, API sheet, and pipeline image as closely as possible. Mark every difference as "NEW" or in a "Delta vs reference" table |
| One fact, one place | Do not store what can be derived (a tab, a display status, a file path built from ids). One writer per field; name it |
| Hot read needs a join | When a list, count, or filter on a hot path would need a join to derive a value, store it as a projection: one named writer, written in the same transaction as its source |
| One rule, one file | A table or rule (status transitions, layer rules, response shape) lives in one file. Other files link to it. A diagram of a table is a picture of it; a script diffs its edges with the table |
| Simplest thing | No outbox, worker, cache, or extra field unless the user asked or a requirement needs it |
| No stranded record | Every after-commit step (next command, event, timer) states what re-runs it if the process dies first: Kafka redelivery with the offset committed last, a re-drive timer, or an idempotent periodic re-check. Pick the cheapest. A record never waits for a message that can be lost |
| One code, one meaning | A status event is a fact, published by the one owner after its own transition. Another system's decision is a request with its own code; the owner answers with the fact |
| `required` = producer guarantee | If the source can omit a field (the customer may not give it), the field is optional in the schema, whatever the business calls it. The rule that needs it (a score, a submit check) handles the absence. Define such a term once in the canon |
| Contract, not code | Show shapes, signatures, owners, and order. No function bodies |
| Owner is explicit | Every command is owned by the module that handles it. Every collection names its writer. Every event names its producer and its consumers |
| Assumptions are visible | Tag unknowns `[ASSUMPTION]`; add a DQ-n open item with the owner who must answer |
| Proof, not claims | "Valid" means a tool said so. Report which checks ran and what they cannot catch |
| Conflicts stop you | Design disagrees with code or requirements: stop, cite both, propose a fix, get agreement |

## Quick reference

- Template file for every document, and a `GUIDE.md` per folder (rules, how to fill, best practices, check):
  [`templates/`](templates/), index in [references/templates.md](references/templates.md)
- Checklist per design kind and validator commands: [references/checklists.md](references/checklists.md)
- JSON Schema + example check: `python3 scripts/validate_json.py <folder> [<design-root>]`
  (needs `jsonschema`, `referencing`; or `uv run --with jsonschema --with referencing python scripts/validate_json.py …`)

## Related skills

- **REQUIRED:** `superpowers:brainstorming` when the problem or the approach is not yet agreed.
- `bmad-architecture` for the decision spine the package details; `trade-off-analysis` before choosing; `context7-mcp` for vendor contracts (Orkes, Kafka, gRPC);
  `superpowers:verification-before-completion` before you say a folder is done.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Inventing a table format when the user has a reference sheet | Copy the sheet's columns. Nested fields get level columns (one column per depth), not `└` |
| Storing derived or speculative fields (status copies, attempt details nobody reads) | Derive at read time or export time; delete the field |
| The sender module owns the command | Move the command into the listener (handler) module |
| An adapter (mail provider, vendor SDK) inside `shared/` | Give it its own adapter module |
| Failed response carries `data` | Failed: `status`, `code`, `message`. Success: the same + `data` |
| Hand-editing a generated md, schema, or proto | Edit the source catalog; re-run the generator |
| Bare `$ref` names; circular `$ref` | Relative file paths; break recursion with a one-level sub-schema |
| Building every folder, then showing the user | Show each folder; wait for review before the next |
| "0 errors, done" | Also say what the checks do not prove (flow correctness, naming across folders) |
| "No outbox, per simplest thing; a sweep is an open item" | Name the cheapest recovery now (offset committed last, re-drive timer, re-check). Simplest thing never means a stuck record |
| The state diagram and a second table "match the canon row for row" | Copies drift. Keep one table; the diagram is checked by an edge diff |
| Validators pass after a rename, so the rename is done | Validators do not see prose. Grep every retired name |
