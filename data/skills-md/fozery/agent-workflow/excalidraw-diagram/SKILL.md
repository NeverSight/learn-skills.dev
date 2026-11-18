---
name: excalidraw-diagram
description: "Offer an optional architecture, domain or interaction diagram during design. After user consent, delegate Excalidraw generation and visual checking to a separate subagent."
---

# Excalidraw diagrams

A diagram supports a design conversation; it is not a required workflow phase or a substitute for decisions, contracts or runnable prototypes.
Read applicable project instructions for sources, artifact locations, delegation, network access and permissions. This package can run without the rest of the kit.

## Choose your role

- **Coordinator:** use the offer and handoff steps below. Keep the generation reference, library JSON and render iterations out of the main discussion context.
- **Assigned diagram worker:** if your brief records the user's consent, output scope and source pointers, go directly to **Generate and check**. Do not delegate again.

## Offer and hand off

1. Offer a diagram only when it can clarify relationships, alternatives, boundaries or an interaction that the user is discussing. State what it would explain. An explicit user request for that diagram counts as consent; selecting or installing this package does not.
2. Wait for the user's answer. On refusal or no answer, continue the original work without diagram writes or launching a diagram worker. Do not repeat the same declined offer unless the user reopens it or the scope changes materially.
3. After consent, check that a separate subagent can read the package and agreed sources, write the diagram destination, and perform the permitted render check. Use the project's delegation mechanism, including Orca when selected. If unavailable or forbidden, report the diagram branch as blocked and continue the discussion. Do not draw in the coordinator's context as a fallback.
4. Send one worker a compact brief, not the full conversation:
   - The diagram's question, audience, scope and consent; distinguish current facts, proposals and unresolved choices.
   - Applicable project instructions and readable pointers to the relevant code, ADR, specification or plan. Include only the facts needed to interpret them.
   - The absolute package location and instruction to use this skill as the assigned worker.
   - Exact output paths, ownership and whether an existing diagram may be revised. Put the editable `.excalidraw` and PNG preview with the parent artifact under project conventions. With no convention, agree the destination before dispatch.
   - Relevant library choices, if known; otherwise let the worker select from the bundled index. The coordinator need not inspect library contents.
   - Permission boundaries: diagram files only, no implementation, document decisions, tracker publication, commits or pushes. State the permitted renderer/network setup.
   - Return only the source and preview paths, a short visual-check result, and unresolved questions or blockers.

Consent covers the agreed diagram work, not new architectural decisions or unrelated actions. Changes to scope or authority return to the user.

**Done when:** the offer was declined, the diagram branch has an explicit blocker, or one bounded assignment has been delivered to a separate worker.

## Generate and check

This section is for the assigned worker only.

1. Read the brief and its authoritative sources. Preserve proposed and unresolved status in the diagram. Return missing design decisions to the coordinator rather than inventing them.
2. Read [generation guidance](references/generation.md), then the [library index](references/libraries.md). The generation reference is the retained upstream prompt; this entrypoint owns consent, delegation, paths and permissions. Resolve its `references/...` paths against the package root, not the reference directory. Its restriction on using another coding agent means no nested drawing delegation from this worker.
3. Load only the selected library items. Follow the index's ID and binding rules when combining or repeating components. Keep libraries read-only; the output is a scene, not a modified component collection.
4. Generate the editable scene within the assigned paths. Use the existing renderer with absolute paths:

   ```bash
   cd <absolute-package-directory>/references
   uv run python render_excalidraw.py <absolute-output-path>.excalidraw --output <absolute-preview-path>.png
   ```

   Check [renderer setup](README.md#renderer-setup) if prerequisites are missing. Installation and network use require applicable permission; the renderer loads external code. If rendering is blocked, return the source path as unverified and explain the missing check. Do not claim a completed diagram.
5. View the rendered image. Correct clipped text, overlapping shapes, ambiguous labels and incorrect connections within the agreed scope, then render and inspect again. Verify the diagram against the supplied contracts, not just its appearance. A source change requires a new preview.
6. Return only the two paths, what was checked and any remaining questions. Keep raw scene JSON, library data and iteration logs in the worker context. If the brief is inconsistent, return the blocker instead of a plausible-looking replacement design.

**Done when:** the source and preview are saved at the agreed paths, visually inspected and consistent with the brief, or the incomplete result and blocker are explicit.

## Resume the discussion

The coordinator presents the preview and file links with the worker's short result. A worker report alone is not user acceptance of the design.
Link the diagram from the parent artifact only within its write permissions. The text remains authoritative for decisions, requirements and contracts.
Continue the original design or planning route; diagram generation does not start implementation or publication.
