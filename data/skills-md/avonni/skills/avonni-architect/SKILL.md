---
name: avonni-architect
description: Design and orchestrate multi-artifact Avonni solutions. MUST activate when a request spans more than one Avonni artifact type (Dynamic Component, Flow Screen Components, Experience site components) or describes a business use case rather than a single named artifact — e.g. a component plus the flow it launches. Do NOT use for a single artifact of a known type — use its skill directly.
license: MIT
compatibility: Requires Node.js >=18, the Avonni MCP server (with the toolsets of the artifact skills being orchestrated), and Salesforce CLI.
metadata:
    version: '1.0.0'
---

# avonni-architect

## Role

This skill designs the architecture of a multi-artifact Avonni solution and dispatches the build work. It never builds an artifact itself — every artifact is built by exactly one of the three Avonni artifact skills, invoked through the Skill tool:

| Artifact type                                  | Owning skill                   |
| ---------------------------------------------- | ------------------------------ |
| Avonni Dynamic Component                       | `avonni-dynamic-components`    |
| Avonni Flow Screen Components (screen flow)    | `avonni-flow-components`       |
| Avonni components in a Digital Experience site | `avonni-experience-components` |

## Toolset

Unlike the artifact skills, this skill is not bound to a single toolset. It may call only the read-only discovery tools — `list_components` and `list_interactions` — using the toolset that matches the artifact being planned (`dynamic`, `flow`, or `experience`). Never call `get_component_docs`, or `get_component_styles` from this skill: component-level detail belongs to the artifact skills.

## Prerequisites

These enforce the requirements listed in this skill's `compatibility` frontmatter. Check items 1 and 2 before Step 1; items 3 and 4 depend on the architecture plan and are checked during Step 2, at the point indicated below.

1. **Node.js >= 18** — before Step 1, run `node --version`. If the command fails or the major version is below 18, stop and ask the user to install Node.js 18 or newer. Do not proceed.
2. **Salesforce CLI** — before Step 1, run `sf --version`. If it fails, do NOT stop: warn the user once that the Salesforce CLI is not installed and that some artifact skills will have reduced capabilities, then continue.
3. **Avonni MCP server** — before Step 1, verify the Avonni MCP tools are available in the session; if they are not, stop and ask the user to configure the Avonni MCP server. Reachability is confirmed by the first MCP call of the workflow (`list_components` with the first planned toolset, in Step 2): if that call fails after one retry, stop the same way. Never continue without the MCP.
4. **Sub-skill availability** — once the plan names its artifact skills (Step 2), verify each one is available in the session's skill list. Match by exact name first; if no skill has that name, look for an available skill whose description covers building that artifact type and use it instead. If none exists, flag the artifact in the plan ("cannot be built in this session — install with `npx skills avonni/skills`") and exclude it from dispatch, together with any artifact that depends on it.

## Execution Workflow

To produce your output, you MUST follow the steps below in order — you cannot skip a step. If you go back to a previous step, all subsequent steps have to be executed again in order.

### Step 1 — Understand the Use Case

Decompose the user's request into user-facing surfaces (record page, screen flow, Experience site page, dynamic component, etc.) and the actions connecting them (launch a flow, open a component, navigate, create or update records).

-   If the decomposition yields **one** artifact, do not produce an architecture plan: invoke that artifact's owning skill through the Skill tool with the user's request and stop.
-   If the request is ambiguous about which surfaces are involved, ask the user to clarify before proceeding.

### Step 2 — Plan the Architecture

Read `references/plan-architecture.md`. Then make an architecture plan strictly following the instructions in that file.

### Step 3 — Validate the Plan

Ask the user to validate your plan.

-   If the plan is accepted as is, continue to step 4.
-   If the user asks for changes, go back to step 2.

### Step 4 — Dispatch

Invoke each artifact skill through the Skill tool, one invocation per artifact, in the build order fixed by the plan. Build the dispatch brief for each invocation as described in `references/plan-architecture.md`.

Each artifact skill runs its own plan → validate → build loop, scoped to its artifact. Do not suppress it — the user validates each artifact's detailed plan even though the overall architecture is already validated.

A sub-skill's final summary is NOT the end of the task. Dispatching continues until every artifact in the build order is built: after a sub-skill summarizes its artifact, run Step 5 and immediately dispatch the next artifact in the same turn, without waiting for the user to prompt you. State the progress each time (e.g. "Artifact 1 of 2 built — continuing with the Case Kanban component"). Stop between dispatches only for the sub-skill's own plan validation or a failure (Step 5).

### Step 5 — Verify and Continue

After each sub-build, before dispatching the next artifact:

-   Confirm the expected output file exists on disk (Dynamic Component metadata record file, `.flow-meta.xml`, modified `content.json`). This is a read-only check.
-   Capture the identifiers downstream artifacts need (flow API name, dynamic component name, file paths) and include them in the next dispatch brief.
-   If the file is missing or the sub-skill reported failure: stop the dispatch sequence, report which artifacts were built and which remain, and ask the user whether to retry that artifact or continue without it. Never build an artifact whose dependency failed.

### Step 6 — Summarize

-   List every artifact that was built, its file path, and the wiring between artifacts (which interaction connects what to what), in natural language.
-   Tell the user that nothing was deployed.
-   If any artifact was excluded (missing skill, failed dependency), restate it and what is needed to complete it.

## Authority

-   The MCP is the single source of truth for Avonni component and interaction APIs.
-   `references/composition-matrix.md` tells you where to look for cross-artifact links, but the existence of any specific interaction must be confirmed by `list_interactions` on the calling artifact's toolset before it appears in the plan. If the MCP disagrees with the matrix, the MCP wins.
-   Never rely on prior knowledge or assumptions about components or interactions.
-   If required information is missing, do not guess — request it.
-   **Never invent artifacts, components, interactions, or capabilities.** Only plan links the MCP explicitly documents.

## Global Tool Usage Rules

-   Never request the same docs twice — cache results.
-   Always use the tools result directly as returned by the MCP, even if the output is large. Never use Bash commands, file reads, or any other tool to shorten, parse, or reprocess the MCP result.

### Global Output Rules

When referring to components or interactions, use their label, not their name.
**Examples:**
ExecuteFlow → Execute Flow
OpenDynamicComponentDialog → Open Dynamic Component Dialog

## Unknown or Ambiguous Requests

If you need more information from the user:

-   Stop generation.
-   Respond in plain text explaining what is unknown or ambiguous.
-   Ask the user to clarify the use case, the surfaces involved, or the connections between them.

## Failure Handling

If an MCP tool call fails:

-   retry once

If it still fails:

-   inform the user that this skill cannot run without the Avonni MCP server and stop
-   never generate output without MCP data

If a needed artifact skill is not available in the session:

-   flag the artifact in the plan and exclude it from dispatch (see Prerequisites)
-   never build the artifact yourself as a substitute

If a dispatched sub-build fails or its output file is missing:

-   stop the dispatch sequence and follow Step 5
