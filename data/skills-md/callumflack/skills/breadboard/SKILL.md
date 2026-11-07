---
name: breadboard
description: Creates and maintains interactive product breadboards with selectable stories, requirements, workflow wiring and links into code. Use to map a workflow, connect several workflows, shape a proposed change or reconcile a map with implementation.
---

# Breadboard

Create an inspectable map of how a product workflow works. Let the reader enter through a story or requirement, follow the relevant actions and handoffs, and find the responsible code and proof.

Use the repository's existing breadboard owner and renderer when present. Otherwise use the bundled viewer, derived from Unity Surfaces #1957. Read [the format](references/format.md) before authoring its JSON and [the viewer contract](references/viewer-contract.md) before rendering. The bundled viewer needs Node.js 22 or newer and no installed packages or Unity checkout.

## Establish the map

Identify the actor, starting situation, goal and observable outcome. Bound the workflow by that outcome. Read the owning instructions, accepted requirements and any supplied description, walkthrough, sketch or recording. Ask only for material product intent that those sources cannot establish.

Before reading implementation to discover, check or clarify behavior, complete this prerequisite. It applies to new maps, review fixes, added stories and requirements, and maintenance after a change.

1. Load [product-description](../product-description/SKILL.md). In Claude Code, invoke the `Skill` tool with `{"skill":"product-description"}`. In a host without a skill loader, read the complete linked `SKILL.md` through the filesystem. A name, catalogue description or link in this file does not load the method. If the skill cannot be loaded or read, report that dependency as blocked before investigating behavior.
2. Read that skill's `references/product-kinds.md` and `references/document-template.md`, then apply its discovery method to the requested workflow. Use an existing product description where available and investigate missing or uncertain behavior from the owning code and tests.
3. Carry the findings into the map's stories, requirements and gaps, retaining links to the description, sources and verification. Keep source-derived findings distinct from runtime observations.

This loads the behavioral method for the current breadboard task. It does not require a full description repo or authorize additional commits, delegation or product execution. Layout-only changes that preserve behavioral claims do not require this discovery pass.

Choose the representation the task needs. An existing-behavior map follows code. A proposed map follows stated intent and labels unimplemented parts. A comparison keeps both visible. Code establishes implemented behavior; accepted requirements establish intended behavior. Preserve a discrepancy instead of silently changing either authority.

Keep the main map in the product's enduring roles. Use specific providers or demonstration apps when the scope is explicitly that example. Keep example results and proof history attached to the behavior they establish.

## Draw the working parts

Identify places, UI affordances, runtime operations and actual state or data. Name what a person can do, what the runtime does and what the next part receives. Distinguish control or navigation wires from data or result wires. Include authority boundaries, interruptions and recovery where they change the experience.

Trace code until the next meaningful product boundary. Keep internal detail in inspection or a more detailed view when it obscures the story. A dependency box without the action or handoff it enables is insufficient.

A breadboard describes working parts and their relationships. Its boxes are not mutually exclusive machine states, and its wires are not all state transitions. Use a statechart for legal state changes, events, guards and concurrency when those questions matter. Both can cover a whole workflow. Formal checking establishes properties of a model; verification of the implementation remains separate.

## Connect stories and requirements

Write each story as a situation, an attempt and an outcome. Select the actual wires it traverses. Include meaningful alternatives such as already-complete work, cancellation, failure or retry. Choose stories that reveal different behavior rather than enumerating every permutation.

For every story except All wiring, author a short numbered path in everyday language. Selecting the story must reveal who acts, what happens next, and the outcome. Connect each step to the wires it explains; distinguish alternative branches from successive events. Put its exact executable check beside the story when one exists and state any proof gap. Provide each check’s exact name, link and coverage. State the specific gap wherever a branch, outcome or runtime is unproved. The generator rejects missing steps and stories with neither a named check nor a gap. Existing definitions must meet this contract when regenerated.

Write requirements as obligations the product must satisfy. Link each to the responsible connected blocks and explain the action, owner and recovery. Requirements can span stories and workflows. Keep unmet obligations and unknown behavior visible in framing or supporting decisions. Do not invent wiring to make an obligation look satisfied.

Keep stable block, wire, story and requirement IDs. Preserve IDs when behavior changes in place. Remove an ID when its subject disappears and explain consequential removals in the change notes. Keep the explanation in the same decomposition as the map, using the same IDs.

## Support different resolutions

Use related views or linked boards when a product overview needs to expand into a workflow or mechanism. Give each expansion an entry condition, inputs, possible outcomes and an owning boundary. Name the parent block and corresponding detailed parts in the frame. Reuse a shared workflow by reference when several workflows depend on it.

The bundled viewer has view navigation through `?flow=...`; it does not implement a nested state machine or automatic semantic zoom. Add an explicit link in the frame when useful. Check that the entry and outcomes retain their meaning across the views. Keep the reader's route back to the overview visible.

## Ground the claims

Attach source references to the blocks they support. For local material, record its repository-relative path, role, symbol or line when useful, and reviewed content hash. Keep the real revision when known. Do not construct a remote URL from an assumed repository or branch.

Use source roles to distinguish implementation, intent, verification instructions, models and evidence. Link an existing verifier or statechart when relevant. If none exists, state the missing proof or model without generating another tool unless requested. A requirement can connect to several blocks, statechart properties and verification steps.

Keep source inspection, observed runtime behavior and deployment distinct. Keep the frame concise so stories remain easy to reach. Put detailed provenance, discrepancy reasoning and proof history in collapsed Sources, with a short consequential limit in the frame. The runtime canvas contains actions, operations and state or data. Hash checks detect changes in mapped bytes; they establish neither semantic accuracy nor runtime success.

## Render and inspect

Keep the editable `breadboard.json` and its generated HTML together at the repository's document owner. Keep local proof artifacts outside current product documentation unless the task gives them a durable owner. Use paths relative to the repository, not paths to this machine.

Resolve `SKILL_DIR` to this skill's actual directory. Run commands from the target repository root. After reading the local sources, record only the references you reviewed:

```sh
node "$SKILL_DIR/scripts/breadboard.mjs" record-sources docs/system/example/breadboard.json --root .
node "$SKILL_DIR/scripts/breadboard.mjs" render docs/system/example/breadboard.json --root .
node "$SKILL_DIR/scripts/breadboard.mjs" check docs/system/example/breadboard.json --root .
```

Use `--out PATH` when the generated HTML has another name. A render can write a draft and exit nonzero because sources remain changed or unknown. Read its report. `check` writes nothing. Exit 0 means the mapped local bytes and generated artifacts match. Exit 1 means invalid content, changed source or stale output. Exit 2 means some references remain unavailable or unreviewed. Neither successful generation nor a matching hash proves the product works.

Cold-read an ordinary story and a recovery or failure story when the workflow has one. Start at the story in the rendered board without source hints. Identify the actor, order, alternatives, visible outcome, and exact check or stated gap. Follow the links and repair any missing handoff or misleading claim. When reporting counts, name the view that contains the entries.

Open the generated board in a browser. Exercise a story, close and reopen its details using the same story heading, then check a requirement, block inspection, source links, All wiring, Fit selection and Fit all. Inspect the full selected path and its lane headings. For related views, follow the expansion and return links. Check readable text, visible inactive context and useful framing. Preserve screenshots and the observations that support the result.

For local source inspection, run `node "$SKILL_DIR/scripts/serve.mjs" .` from the selected root. It prints a loopback URL with an available port. Open the map's relative path at that URL. The server displays code as text, avoiding browser downloads for TypeScript files. Stop the owned process after inspection. This serves files and executes no product code.

Report the map location, represented revision or source state, consequential gaps and proof limits. The HTML embeds the interactive viewer. Its adjacent contract and local source files remain part of the bundle; remote links still need network access.

## Maintain after a change

Start with the changed code or accepted decision and the current map. Run `check` before changing baselines. Follow the affected block and requirement IDs through the stories, wires, walkthroughs, framing and linked views. Update only the affected meaning and preserve useful manual explanations.

Read the changed source and compare the requirement before recording its new hash. Use `record-sources ... --source relative/path` to refresh only reviewed references. A missing runtime proof remains missing after the code hash changes. Regenerate and inspect the affected views, then run `check` again. Summarize behavior changes and unresolved discrepancies without turning implementation into an automatic approval of intent.

Authoring a map authorizes no product changes, credential access, dependency installation, publication, commits or autonomous delegation. Follow the current task's authority for those actions. Viewer provenance and local distribution limits are in [NOTICE.md](NOTICE.md).
