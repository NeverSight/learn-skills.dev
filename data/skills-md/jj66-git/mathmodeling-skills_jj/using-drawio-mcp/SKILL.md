---
name: using-drawio-mcp
description: Use when a mathematical modeling project needs a complex editable Draw.io flowchart, architecture, swimlane, state, ER, network, or multi-page diagram through Draw.io MCP, including incremental edits, language-locked labels, or MCP-failure fallback handling.
---

# Using Draw.io MCP

## Overview

Turn an approved figure contract into an editable, verified Draw.io artifact through the installed Draw.io MCP tools. Treat MCP output as an intermediate artifact: inspect structure and rendering before promotion, and leave an explicit blocked fallback when MCP cannot be verified.

## Ownership

- Let `modeling-figure-orchestrator` choose the visual backend and maintain the figure manifest.
- Let `4drawio` own the mathematical-modeling non-data-diagram stage and `DRAWIO_REPORT.md`.
- Own the complex Draw.io MCP call, page-safe editing, retries, visual QA, and failure artifacts here.
- Do not use this skill for statistical plots, scientific charts, or tables.

## Route by Observable Complexity

Set `drawio_mcp_required: true` when any condition holds:

- More than eight nodes.
- At least two decision nodes, or any feedback loop.
- At least two swimlanes, nested groups, or containers.
- A multi-layer architecture.
- Specialized editable geometry or stencils.
- Any edit to an existing `.drawio` file.
- An explicit request to use Draw.io MCP.

For a simpler new diagram, permit Mermaid or direct Draw.io XML only when the orchestrator's figure contract allows it. A Mermaid or TikZ image used because MCP failed is a placeholder, never a final substitute.

## Execute the Workflow

1. **Read the figure contract.** Require `figure_id`, purpose, paper language, diagram type, nodes, edges, branch labels, groups or lanes, target paper width, editable-source path, export path, and acceptance criteria. Stop with a concrete missing-artifact blocker instead of inventing content.
2. **Lock the language.** Use the paper language for every visible label. For Chinese papers use Chinese labels and `是` / `否`; for English papers use English labels and `Yes` / `No`. Keep identifiers and file names ASCII where practical. Do not silently translate terminology.
3. **Choose the installed operation.** Use Mermaid input for supported standard structures and XML input for precise layout, containers, layers, specialized shapes, or exact routing. Search shapes only when a specialized stencil is necessary. For existing files, always run `list_pages -> get_page -> set_page`; never rebuild or splice the whole multi-page file.
4. **Build before calling.** Resolve the node and edge inventory, stable ids, parent/container rules, layout direction, decision branches, feedback paths, and paper-scale typography. Escape XML text and keep ids unique.
5. **Call MCP.** Use only the installed operations documented in [references/drawio-mcp-protocol.md](references/drawio-mcp-protocol.md). Treat the browser/editor opening as an intermediate result, not proof that a source file was saved.
6. **Verify.** Check semantic completeness, page preservation, parseable Draw.io/XML structure, correct language, readable export, geometry, edge routing, clipping, overlap, and target-width text size. Record the evidence in the figure QA log.
7. **Repair deliberately.** Make at most three render attempts total. Each retry must name the observed defect and change only the relevant structure or layout. Do not loop blindly.
8. **Promote or fall back.** Promote only after the editable source exists and visual QA is `PASS`. Otherwise create the complete fallback set and keep G5/G6 blocked.

## Existing-File Mutation Rule

For every existing `.drawio` edit:

1. List pages from the requested file path.
2. Select the intended page by returned page identity.
3. Read that page.
4. Modify only its returned page content.
5. Write only that page back.
6. Re-read the page list and affected page; verify untouched pages retain their identities and content.

Never replace an existing file merely because page inspection or mutation failed. Report the blocker and preserve the original.

## Status and Artifact Contract

Use exactly these non-promotable states when applicable:

| State | Meaning | Gate effect |
|---|---|---|
| `PLACEHOLDER` | Mermaid/TikZ render temporarily occupies the paper slot | Block G5 and G6 |
| `AWAITING_SAVE` | MCP opened an editor but the required editable source is not confirmed on disk | Block G5 and G6 |
| `UNVERIFIED_MCP_FALLBACK` | Legal Draw.io/XML fallback exists but was not verified through MCP rendering | Block G5 and G6 |

On MCP failure, timeout, unavailable tool, save uncertainty, or failed visual QA after three attempts, produce all of the following:

- `paper/figures/placeholders/<figure_id>.mmd` or `<figure_id>.tex`.
- A rendered placeholder image used only to maintain draft layout.
- A legal `<figure_id>.drawio` file and a separate `<figure_id>.xml` copy marked `UNVERIFIED_MCP_FALLBACK` in file metadata or a non-visible diagram attribute.
- `paper/issues/drawio-mcp/<figure_id>/issue.md` with failure reason, attempted operations, affected paper location, artifact paths, current state, and required recovery action.
- Supporting call or validation logs in the same issue folder when available.
- An `OPEN` or `BLOCKING` row in `paper/issues/issue_register.md`.

Keep the issue register internal. Do not cite production failures in the contest paper. The writer may include the rendered placeholder during drafting but must not describe it as final or allow it through G5/G6.

## Quality Red Lines

Reject promotion when any of these occurs:

- A required node, relation, lane, layer, or decision branch is missing.
- Visible labels use the wrong language or inconsistent branch words.
- XML is malformed, ids collide, or a child has the wrong parent.
- An existing-file edit changes an untargeted page.
- Text overlaps, clips, or becomes unreadable at the declared paper width.
- Connectors obscure nodes, become ambiguous, or cross excessively without semantic need.
- The editable source, export, manifest entry, QA evidence, or issue closure is missing.

## Common Rationalizations

| Rationalization | Required response |
|---|---|
| "The XML looks plausible." | Parse it and verify the rendered result before promotion. |
| "The editor opened, so the file is saved." | Use `AWAITING_SAVE` until the source exists at the required path. |
| "Regenerating is easier than editing page 2." | Use page-safe inspection and mutation; preserve every untargeted page. |
| "A placeholder is good enough for the deadline." | Keep layout moving, but block G5/G6 and register the open issue. |
| "English technical labels are universal." | Match every visible label to the paper language. |

## Handoff

Return to `4drawio` with the editable source path, export path, backend, language, render-attempt count, QA result, and issue state. Return to `modeling-figure-orchestrator` to update `figure_manifest.json` and `figure_qa_log.md`. Route an unresolved Draw.io issue back to this skill; never route it directly to final assembly.

Read [references/drawio-mcp-protocol.md](references/drawio-mcp-protocol.md) before making MCP calls or generating fallback files.
