---
name: exp-build
description: Build or update an MVP from a brief through runnable delivery and acceptance verification.
---

# exp build

Follow [AGENTS.md](../../../AGENTS.md) for workspace conventions, resuming work, current-state records, code quality, and verification. Use the project established by the user or session; ask if the target is ambiguous. A scaffold-only or planning-only request ends at that deliverable.

Choose an approach suited to the intended users, deployment, data needs, existing code, and maintenance constraints. Briefly record the reasons and significant tradeoffs in the specification. When a choice needs user input, explain its practical consequences and recommend an option. Investigate uncertainty that could invalidate the design before committing substantial work; do not require a comparison or experiment for every routine choice.

For a new substantive application, a responsibility or contract boundary change, or an architecture assessment, read [architecture decisions and verification](references/architecture.md). Use it to connect design choices to actual needs and walk through a confirmed next change when one exists. A copy-only change or unrelated narrow repair does not require this reference.

Deliver the complete agreed user flow. Choose the implementation order and tools to suit the task. For architecture or flow exploration, use `exp-brainstorm` when helpful or requested. For new interfaces or substantive UI changes, use [exp-design](../exp-design/SKILL.md) to establish the visual direction and review the interaction; keep small changes proportionate.

For an existing harness project or explicit adoption, read [the harness contract](../../../harness/README.md) for registration and delivery requirements. Use its bounded repair controller only when bounded automatic repair is requested, against established acceptance checks.

Map the agreed completion criteria to appropriate evidence before implementation; include intermediate UI states when the requirement concerns transitions. Reuse the existing specification and tests rather than creating a parallel checklist. Complete the workspace's code review and verification requirements before delivery. Exercise the main user flow, using actual UI interaction for UI behavior when tools permit. Identify required verification that could not be performed as incomplete. For documentation-only or similarly narrow requests, stop at the requested deliverable after appropriate checks.
