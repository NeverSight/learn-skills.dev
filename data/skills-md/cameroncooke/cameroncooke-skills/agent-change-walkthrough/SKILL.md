---
name: agent-change-walkthrough
description: Produces a single-story walkthrough of AI-authored code changes from runtime trigger to final behavior, weaving changed and unchanged code into one narrative with annotated diffs, trade-offs, alternatives, and risk analysis. Use when asked to "explain what changed", "walk me through this diff", "summarize agent edits", "show how this feature works", or "explain this implementation step by step".
allowed-tools: Read, Grep, Glob, Bash
---

Generate one coherent implementation story that explains how the code works end-to-end after the change.

## Step 1: Capture implementation intent

Restate the requested change in plain language.

Include:
- User problem being solved
- Scope boundaries
- Explicit non-goals

If requirements are ambiguous, state assumptions before proceeding.

## Step 2: Build evidence from conversation + git

Collect both sources before writing:

1. Conversation context (planning input only)
   - Requested outcome
   - Constraints and acceptance criteria
   - Domain context needed to interpret the code correctly

2. Git-based evidence (source of truth for output)
   - Changed file list
   - Diff per changed file (analyze full diffs locally, but only quote the minimum needed hunks in output)
   - Relevant unchanged context needed to explain behavior

Use commands such as:

```bash
git status --short
git diff --name-only
git diff -- <file>
git show -- <file>
```

Use history only when needed to disambiguate intent:

```bash
git log --oneline -- <file>
```

Never include conversation process, investigation history, or request negotiation as walkthrough steps. The walkthrough must describe implementation behavior only.
Never include full file dumps, raw secrets, credentials, tokens, private keys, or copied production payloads in the final output.

## Step 3: Build the story stack

Order story steps by **dependency-first causality**:
1. Introduce contracts/types/schemas/interfaces before showing call sites that use them
2. Introduce function/class definitions before showing new call paths that invoke them
3. Then continue in runtime flow order from trigger to final behavior

If runtime order and dependency order conflict, prefer dependency order and add one short transition sentence that reconnects to runtime flow.

Skip non-essential detail while preserving causal clarity.

## Step 4: Write each step as natural developer narrative

For each story step:
- Use a clear step title that describes behavior (no file path in the heading)
- Mark the step as `UNCHANGED CONTEXT` or `CHANGED`
- Place `Filename: `<relative/path/to/file.ext:start_line>`` immediately above each snippet
- Optionally place `Symbol: `<function/method/class>`` above each snippet when useful
- Show a short code snippet
- For data-shape/model/API changes, include concrete example data (input/output or before/after payload) using sanitized, representative values
- Explain the step in natural prose as a developer-to-developer walkthrough
- Explain what this step causes next in the flow
- Avoid forward references: do not use a field/type/function in a step before showing where it is defined or introduced

Avoid rigid template labels such as `Why this step exists:` or `Impact:`. Write readable, connected prose instead. Keep headings and narrative readable; put precise location in the snippet header.

When code changed, prefer mini-diff snippets:

```diff
- old behavior
+ new behavior
```

When the change affects data shape or behavior, add a small `Example input/output` block after the code snippet to show representative (synthetic) values flowing through the updated code.
Do not copy verbatim payloads from logs, production data, or repository fixtures that may contain sensitive information.

Call out semantic effect per changed hunk.
## Step 5: Integrate analysis inline

Embed analysis at the relevant story step:
- Trade-offs chosen at that step
- Viable alternatives and why not chosen
- Performance implications
- Failure modes and compatibility risk

Use natural language callouts in prose; keep them concise and specific.

## Step 6: End with concise close-out

After the final story step, add a short close-out with:
- What changed overall
- Why behavior is now different
- What to monitor or validate next

## Output contract

Return this structure:

1. `# Implementation Walkthrough`
2. One brief setup paragraph (intent + scope)
3. Numbered story steps (`## Step 1`, `## Step 2`, ...)
4. `## Final Outcome`

## Output example

Use this structure:

````markdown
# Implementation Walkthrough

This change adds source-aware feature behavior for a new UI path while preserving the existing invocation flow.

## Step 1 — User click enters the feature entrypoint [UNCHANGED CONTEXT]
The runtime trigger is still the button click. That handler forwards the input into the existing feature path, so the change does not alter how execution begins.

Filename: `src/ui/button.ts:42`
Symbol: `onClick`
```ts
button.onClick = () => startFeature(input)
```

From here, control moves into `startFeature()`.

## Step 2 — Entrypoint forwards to service [UNCHANGED CONTEXT]
The orchestration layer remains unchanged and continues to delegate work to `run()`. This is important context because it means the new behavior is introduced deeper in the service layer, not at the boundary.

Filename: `src/feature/entry.ts:10`
Symbol: `startFeature`
```ts
export function startFeature(input: Input) {
  return run(input)
}
```

That keeps the original control flow intact and localizes the behavior change.

## Step 3 — Service return payload updated [CHANGED]
This is the functional change: the service now includes source metadata in its return payload so downstream consumers can render source-specific UI behavior.

Filename: `src/feature/service.ts:88`
Symbol: `run`
```diff
- return { state: "pending" }
+ return { state: "ready", source: "agent" }
```

Example input/output:
```json
{
  "input": { "taskId": "t_123", "state": "pending" },
  "output_before": { "state": "pending" },
  "output_after": { "state": "ready", "source": "agent" }
}
```

The team chose to enrich the existing payload instead of creating a second metadata endpoint, which avoids an extra network hop and synchronization complexity. Performance impact here is negligible because no additional I/O is introduced, but there is a compatibility risk for legacy consumers that assume the old payload shape.

## Step 4 — UI consumes enriched payload [CHANGED]
Rendering now branches on the new `source` field, which is what makes the feature visible to users. This step is where the service-layer change becomes observable behavior.

Filename: `src/ui/render.ts:120`
Symbol: `renderState`
```ts
if (data.source === "agent") {
  showAgentState()
}
```

At this point the flow reaches the updated UI outcome.

## Final Outcome
The feature still starts at the same runtime trigger and follows the same orchestration path, but the changed service payload now drives source-aware rendering. Next validation should confirm that legacy consumers handle the added `source` field safely.
````

## Validation and exit criteria

Complete only when all checks pass:

- Story begins at runtime trigger and ends at final observable behavior.
- Every changed file appears in at least one `CHANGED` story step.
- Every snippet header uses `Filename: relative/path/to/file.ext:start_line` format.
- No forward references: definitions/contracts appear before usages that depend on them.
- Unchanged-but-critical context appears in `UNCHANGED CONTEXT` steps.
- Each changed hunk includes reason + behavioral effect.
- Data-shape/model/API changes include concrete example input/output with sanitized representative values.
- Trade-offs, alternatives, performance notes, and risk notes appear at relevant steps.
- Facts are distinguished from inference.
- Unknowns are explicitly labeled.
- Conversation process/history does not appear as a walkthrough step.
- No claim of validation is made unless validation was actually performed.
- Snippets and examples contain no credentials, keys, tokens, or other sensitive values.

If any criterion fails, state what is missing and continue refining before finalizing.
