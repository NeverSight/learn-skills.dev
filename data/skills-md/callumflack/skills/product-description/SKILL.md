---
name: product-description
description: Build a "product description" repo for a software product — a set of prose documents describing, from the outside in, what the user sees, what they can do, and exactly what happens when they do it, written from the code and tests, then verified against the running product and triaged into a bug list. Works for any product with a user (canvas editors, web apps, CLIs, chat products, mobile apps). Use when the user asks to "write a product description for X", "describe the user experience of X", "document how X behaves for the user", "make a behavior-spec repo", or wants a feature-by-feature, event-by-event account of an app's behavior rather than API docs. Also use to resume or extend an existing product description repo.
---

# Product description repo

A product description treats the product as a large state chart the user moves through with input. The repo describes that state chart feature by feature, in plain language, from the user's point of view, with the same skeleton for every document so that gaps and inconsistencies show up by comparison. Documents are drafted from the source code and its tests, then verified by hand against the running product, and everything that looks like a defect is collected into one triage file.

The files under `references/`:

| File | What it is |
| --- | --- |
| `product-kinds.md` | How to map the template onto a canvas editor, a web app, a CLI, or a chat product. Read in Phase 0. |
| `README-template.md`, `goal-template.md`, `glossary-guide.md` | Skeletons for the three files that steer the whole build. |
| `document-template.md` | The eight-section skeleton every feature document follows. |
| `verification-template.md`, `bug-triage-template.md` | Skeletons for the checking half. |
| `check-links.py` | Link and anchor checker for the consistency pass. `python3 check-links.py {repo}`. |

## Outputs

```
README.md            purpose, conventions, document template, method, structure, coverage table
goal.md              the standing instructions for whoever drafts (you, subagents, a future session)
glossary.md          the vocabulary; the source of truth for every term of art
AGENTS.md            "Read README.md, then goal.md. The coverage table in README.md is the work list."
CLAUDE.md            "Read @AGENTS.md."
{area}/{feature}.md  one document per feature, all on the same skeleton
verification/        README.md (protocol) + one checklist file per cluster of documents
bug-triage.md        every suspected defect, deduplicated, with repro, cause, severity, decision needed
```

## Phase 0: scope

Settle these before writing a file. Ask only for what you cannot infer from the conversation or the source repo; record the answers in the README's "Scope decisions" section.

1. **Product and surface.** What exactly is being described: which app, which route, role, or configuration, with what customization (usually "the defaults, nothing customized"). One surface per repo.
2. **Source of truth.** The path to the source repo (read-only reference) and the commit. Every document footer cites `git rev-parse --short HEAD` of that repo.
3. **Where to run it.** The command and URL, binary, or account that brings up the surface for verification.
4. **Out of scope.** Name what is excluded and why, so later readers do not think it was forgotten.
5. **Where the repo goes.** A new directory, `git init`, first commit `Initial commit`.
6. **The product's shape.** Read `references/product-kinds.md` and decide, once: the unit of interaction and the names of its five phases; the variant axis (modifiers, flags, roles); the fixed interrupt list; the cross-cutting concerns and their order. These go into the README's "Document template" section and the glossary before the pilot is written, and they do not change afterwards without revisiting every document.

Then do a reconnaissance pass over the source repo to find: where interaction state lives (state machines, reducers, controllers, route handlers, command definitions), where behavior tests are (the ones that read as executable specs of edge cases), where the UI is, and where defaults and thresholds are defined (options, constants, config schemas). These go into the README's "Reference" section and goal.md's reading order.

## Phase 1: scaffold

Write, in this order, adapting the templates in `references/`:

1. **README.md** from `README-template.md`. The structure section is the plan: list every document you expect to write with a one-line gloss, grouped by how the user meets the feature (foundations, then the areas of the product, then cross-cutting concerns), never by package or module. The coverage table lists every document as `not started`. Getting the structure right up front is most of the planning; expect to revise it as you learn, and update the table whenever you do.
2. **glossary.md** from `glossary-guide.md`. Start with the terms the foundations will need and the interrupt words from Phase 0; grow it as documents demand new words. A term used in a document that is not in the glossary is a consistency bug.
3. **goal.md** from `goal-template.md`. This is the prompt that drives all drafting. Its "Things already established" section is empty at first and fills in as the foundations are written.
4. **AGENTS.md** and **CLAUDE.md** with the one-line contents shown under Outputs. Do not leave AGENTS.md empty; it is what a fresh session reads first.

Commit: `docs: add README, glossary, goal`.

## Phase 2: pilot, foundations, the hard part

Do these yourself, in sequence, not in parallel. They fix the template, tone, depth, and vocabulary that everything else copies.

1. **Pilot.** One small, self-contained feature with a real interaction in it (`product-kinds.md` names one per product kind). Write it on the full eight-section template (`document-template.md`). Iterate on it until it is right; every later document copies it. A small feature done properly runs around 150–200 lines, with every phase narrated, every variant and interrupt cell filled, and the cross-cutting list walked in full; if a section is thin, the feature has not been read closely enough yet.
2. **Foundations.** The documents everything else links to: the input or invocation model (events, thresholds, what cancels, completes, and interrupts), the core object or data model, the mode, tool, or navigation model, the viewport or session model. These *own* the facts other documents link to instead of restating. As each is written, add its load-bearing facts (numbers, defaults, rules) to goal.md's "Things already established" so no later document re-derives or contradicts them.
3. **The hardest area.** The bulk of the experience (the selection tool, the main editor, the `build` command, the composer plus the streaming response). Read all of its state handling before writing any of its documents, because the states hand off to each other and the documents must agree on where one ends and the next begins. Decide which document owns each state and write that down in goal.md.

Commit after each document or coherent group: `docs: add {path}`.

## Phase 3: draft the rest in parallel

Once the exemplars exist, the remaining documents are independent. Fan out with subagents, one document or small cluster per agent. Each agent's prompt is:

> Read `goal.md`, `README.md`, `glossary.md`, `{pilot}`, and `{the foundation document this feature depends on}`. Write `{area}/{feature}.md` on the same skeleton, at the same depth. Use the glossary's words; if you need a term it lacks, add it to `glossary.md` in the right section with a full definition rather than coining a synonym. Do not edit any other existing document. Do not modify the source repo. End with "## Open questions and verification" and the footer. Report what you could not determine from code and tests.

Review every result yourself before accepting it. Check: glossary words used correctly, established facts not contradicted, relative links resolve, footer present, interrupt table complete (every row, even if the answer is "no effect"), suspected bugs stated plainly in "Open questions" rather than smoothed over.

Update the coverage table to `drafted` as each lands. Commit in groups: `docs: add {paths}`.

## Phase 4: consistency pass

Over the whole set:

- Same term for the same thing everywhere; every term of art defined in the glossary; glossary definitions agree with the documents.
- No two documents describe the same behavior differently. Where two documents touch, one owns the behavior and the other links.
- Every relative link and heading anchor resolves: `python3 {skill dir}/references/check-links.py {repo}` (exit 1 and a list of `file:line: missing file|anchor` if not).
- Every document has the footer and an "Open questions and verification" section.
- The interrupt table has the same rows in the same order in every document; the cross-cutting concerns appear in the same order.
- The README structure and coverage table match the files on disk exactly.

Commit: `docs: revise the set after the consistency review`. Then go back through the documents whose open questions were thinnest and deepen them; expect a second revision pass on a handful of documents.

## Phase 5: verification checklists

Drafting reads the code; verification watches the product. From `verification-template.md`:

- `verification/README.md`: how to bring up the surface, confirm the commit, run a pass, record results, file failures, and when a document moves from `drafted` to `verified`.
- One checklist file per cluster of documents, one table per document, one row per observable claim: stable ID (`AREA-NN`), priority (P1 established fact or suspected bug, P2 ordinary claim, P3 a number, color, or timing), what it needs (device, role, network condition), the claim with a link to the section, setup, numbered steps, expected result, Result column (`—` until run). Claims that cannot be checked by hand go under "Not checkable by hand".

If you can drive the product (browser tools, a console handle on the app, a shell for a CLI, a test harness), run a first pass yourself on what can be observed that way, record the results in the Result columns, and say plainly in `verification/README.md` what that pass did and did not cover (for example: a scripted pass checks output, exit codes, and stored state but not what was shown on screen or how long it took to appear). Do not mark a document `verified` on the strength of an automated pass alone. A failed item is not automatically a product bug; sometimes the document is wrong, and the Status line says which.

## Phase 6: bug triage

From `bug-triage-template.md`: collect every suspected defect from every document's body and open questions, merge duplicates (the same root cause raised by many documents is one entry with many "Raised by" links), and write each up with where the user meets it, what happens vs. what was expected, reproduction steps, the cause in the code with file and line, a severity, and the decision the product team needs (`fix` or `product call`). Summary table at the top sorted by severity. Entries confirmed by a verification pass carry a **Status** line.

**Filing upstream is a separate, outward-facing step.** Offer it; do not do it unasked. If the user wants the entries filed as issues, confirm the repo and the format first, file them, then add an Issue line to each entry and a link column to the summary table (`docs: revise bug-triage.md with links to the filed issues`).

## Resuming and extending an existing repo

A later session, or a request to add a feature that was out of scope, starts here rather than at Phase 0.

1. Read `AGENTS.md`, `README.md` (structure, coverage table, scope decisions), `goal.md` (established facts), and `glossary.md`. Read the pilot to recalibrate depth.
2. Confirm the source repo's commit. If it has moved, decide with the user whether new documents cite the new commit (and say so in their footer) or the repo pins the old one. Do not silently mix.
3. To add a document: add it to the README structure and coverage table first, write it, add its checklist table to the right `verification/` file (new ID prefix, numbered from 01), add any new triage entries to `bug-triage.md` with the next `B-NN`, and commit each step: `docs: add {path}`, `docs: add the {name} checklist ({PREFIX}-01 to {PREFIX}-NN) to verification/{cluster}.md`, `docs: add B-NN to B-MM to bug-triage.md from the {name} work`.
4. To revise a document after a verification pass: change the document, update the checklist row's Result and note, update the triage entry's Status, and commit as `docs: revise {path}`.
5. Never renumber checklist IDs or triage IDs once a pass or an issue has used them.

## Writing rules (carry into goal.md verbatim or adapted)

- Describe the experience, not the code. "The form stays disabled until the server answers", not "the mutation sets isPending". "The file is written only after every check passes", not "validate() runs before write()".
- Technical detail only in `> Technical note:` block quotes, and only when the mechanism changes what the user would expect.
- Sentence case for headings. Direct, concrete, no hedging, no marketing.
- Surprising behavior is stated plainly, with the reason if the code or a comment gives one. If it looks like a bug, say so in "Open questions".
- Variants and interrupts go in tables, split by phase ("at the start" / "during"). Every cell filled, even with "no effect".
- Cross-reference with relative links instead of repeating. The foundation documents own thresholds and definitions.
- One Mermaid `stateDiagram-v2` per interaction, limited to the states the user passes through.
- Footer: `## Open questions and verification`, a bullet list, then `Verified against {repo} commit \`{sha}\``.
- Commits: `docs: add {path}` / `docs: revise {path}`. Follow whatever the user's repo does about AI attribution in commit messages.
- Never modify the source repo. It is read-only reference material.
- When a behavior cannot be determined from code and tests, write what can be determined, put the rest in "Open questions", move on. Do not guess, do not block.

## What never changes, whatever the product

The outside-in stance; one skeleton for every document; the interrupt list asked of every feature in the same order; a glossary that owns the words; foundations written first so they own the numbers; a pilot that sets the depth; drafting from code and tests, then verifying against the running product, then triaging what looks wrong. `product-kinds.md` is about what to rename; this list is what not to.
