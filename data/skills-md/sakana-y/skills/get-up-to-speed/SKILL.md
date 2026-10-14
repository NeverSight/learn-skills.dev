---
name: get-up-to-speed
description: Deliver a complete, self-contained quickstart guide with runnable examples for a library, framework, or developer tool, with implementation depth matched to the learner's goal.
disable-model-invocation: true
---

# Get Up to Speed

Deliver one **Quickstart Guide** with accompanying runnable examples in an independent **Quickstart Workspace**. Make getting started faster by doing the research, selecting a useful path, and explaining it thoroughly. Cover the target's core capabilities and their relationships, using a representative scenario for depth and small supporting examples where needed.

Complete the agreed scope in one delivery. Document sections organize the reading; they are not separate teaching sessions awaiting permission to continue. Follow-up conversation clarifies or extends the guide. Learner exercises, assessments, and learning records are not part of this workflow.

## 1. Establish the Learning Context

Build on the learner's existing language foundations. Programming languages taught from scratch, systematic foundational courses, and long-term study plans fall outside a Library Quickstart. Explain that mismatch before preparing material or creating a workspace, and let the learner choose another direction or narrow the request.

Identify the target, existing experience, and intended use from the request and available context. For a suite, consult its official overview to understand the available paths. Ask only about missing information that materially changes the guide; a stated contribution goal already establishes the need for contribution preparation.

Establish the **Teaching Language**: honor an explicit choice for this quickstart, otherwise ask the learner to select it. Use it for the guide and conversational explanations, keeping code identifiers, commands, and API names in their conventional form. The conversation's language alone is not a selection.

Define what the guide will enable the reader to do and which advanced or alternate paths are outside its scope. Use this outcome to select detail rather than imposing a word count, lesson count, or full-project curriculum.

**Complete when:** the target, intended outcome, relevant prior knowledge, scope, and Teaching Language are clear enough to select a representative scenario.

## 2. Research and Demonstrate the Path

Read the official overview, getting-started material, and guides for the intended use. Select the version from the request or relevant installation; use a current documented release for a fresh setup unless the contribution target calls for a particular source revision. Record the relationship between the demonstrated installation, documentation, and source.

Choose a scenario that exposes the target's characteristic decisions and behavior. Explain the other core capabilities and how they relate to this path; supplement the scenario where it cannot explain a necessary concept. Prepare the entire agreed scope before delivery.

Perform **Source Preparation** even when the documentation appears sufficient. Locate matching source, orient within relevant packages and public entrypoints, and follow the implementation and tests needed to explain key behavior, defaults, precedence, and limits. Stop when the guide's explanations are supported. Distinguish public contracts from behavior at the inspected revision, and tests that were read from tests that were run.

For ordinary onboarding, bring the key mechanisms into the explanation at the depth needed to use the tool and reason about variations. For a contribution goal, also prepare one continuous path from observable behavior through the relevant implementation to a minimal change and regression test:

- Explain how to locate the entrypoint, follow the important calls or data transformations, and identify the branch responsible for the behavior.
- Use a suitable existing problem, historical fix, or explicitly labeled teaching change. Explain the relevant test's setup, trigger, and assertion, why the change belongs at that location, and what the before/after test results establish. A teaching change is not evidence of an upstream bug.
- Rehearse the relevant contribution setup, change, and focused test in an isolated checkout inside the teaching workspace. Retain the base revision, reproducible patch or changed source, and commands needed to repeat it. Connect the contribution example to the guide's main scenario.

Create the workspace at the requested destination, or in a fresh `get-up-to-speed-<target>` directory under the current workspace. Preserve existing contents. Use `README.md` as the complete guide and `examples/` for code and fixtures; place manifests and configuration where the tooling expects them. Keep supporting source checkouts or evidence as needed, with their explanations in the guide. Operational work stays inside this workspace; changing existing projects, provisioning services, or publishing a contribution requires its own authorization.

Run the examples yourself. Inspect actual rendered interfaces for UI examples and command output or generated artifacts for programmatic examples. Preserve runnable before/after states when an example changes, record dependencies with normal manifests and lockfiles, and verify the installed version against the preparation. Resolve disagreements between observed behavior and the planned explanation before writing the affected claim.

If matching source or execution is unavailable, identify the specific limit and distinguish documentation-supported claims, source-derived explanations, observed results, and expected results. An unexecuted walkthrough may support a limited guide, but cannot establish a verified contribution path. If the missing evidence prevents the intended outcome, explain the blocker and let the learner choose a supported narrower outcome or defer; do not silently substitute an incomplete guide.

**Complete when:** every part of the agreed scope has supported explanations and reproducible examples, with execution results or explicit limits that still support the agreed outcome.

## 3. Write the Complete Guide

Write for a reader who has none of the originating conversation. Open with the target's purpose, the reader's intended outcome, assumed background, and a compact map of its core concepts and capabilities. Explain their relationships and where the representative scenario fits. Keep version details and setup instructions easy to find without letting the execution history dominate the introduction.

Organize the body around the scenario's decisions and behavior. For each important concept or step:

- Establish the problem that makes it necessary and connect it to what the reader already knows.
- Show the relevant code in the document, link the runnable file, and explain material commands, configuration choices, and how inputs become results.
- Explain why the result follows. Where a changed condition exposes an important distinction, show a small variation and explain its effect and limits.

For contribution preparation, carry the same explanatory approach through the source path, minimal change, and regression test prepared in step 2. Include the code excerpts and reasoning needed to follow the path in the body; source links provide evidence and further reading rather than replacing the explanation.

Choose sections and diagrams to serve this particular target, without requiring a repeated lesson template. Keep all essential teaching in the primary document. Close with actionable run instructions, a compact command or API reference where useful, scope boundaries, and focused next references. Describe the capabilities covered without claiming the reader has demonstrated mastery.

**Complete when:** the guide covers the agreed outcome from orientation through the worked path, and a reader can follow the reasoning and reproduce the examples without asking for the next installment or searching linked material for essential explanations.

## 4. Check and Deliver

For a guide with multi-step setup, cross-tool operations, contribution rehearsal or environment-sensitive results, use an independent reader replay when available and its value justifies the setup. Read [independent replay](references/independent-replay.md) before assigning it. A small prose correction or concept-only explanation does not automatically need a worker. The author's own execution remains required; independent replay checks whether the delivered material supplies the reader's necessary context.

Read the guide from the learner's stated starting point and correct these gaps before delivery:

- **Understanding:** core concepts have explanations of their relationships and consequences; named features, command tables, and source links alone do not meet this requirement.
- **Reasoning:** important choices and results have a causal explanation, and relevant variations show how to reason beyond the exact example.
- **Outcome:** the worked path reaches the agreed endpoint. A contribution guide includes the source reasoning, minimal change, and regression test rather than postponing them to future lessons.
- **Reproduction:** document snippets agree with retained files, commands identify prerequisites and working directories, and reported outcomes match the evidence. Recheck affected examples after corrections.
- **Completeness:** the primary document contains the necessary explanation for the whole scope, with functioning local links and clearly identified evidence limits.

Return the guide and example links with a brief statement of coverage and material execution limits. Retain the workspace and stop temporary processes created for it, noting any intentionally left running for the learner. If the learner ends the work early, identify the partial material and missing scope explicitly.

**Complete when:** the complete guide and examples are accessible, the checks above are satisfied for the agreed scope, and temporary process ownership is accounted for.
