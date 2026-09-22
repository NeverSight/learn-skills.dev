---
name: ai-feedback-collector
description: Use this skill when a user wants to report, collect, normalize, classify, or template feedback about problems encountered while using AI tools in any scenario, including coding agents, chatbots, office assistants, search, writing, data analysis, or internal AI systems. The skill converts free-form problem descriptions into a structured feedback report with explicit labels, problem category, severity, scenario, impact, and follow-up questions.
---

# AI Feedback Collector

Use this skill to turn free-form feedback about AI tool usage into a structured, objective issue report.

The goal is collection and normalization, not troubleshooting. Preserve the user's original meaning, avoid over-interpreting sparse descriptions, and make the output easy to paste into an issue tracker, spreadsheet, chat thread, or internal feedback system.

## Workflow

1. Identify whether the user is reporting a problem with an AI tool or AI-assisted workflow.
2. Extract observable facts from the description: tool, task, scenario, failure behavior, impact, business context, and any available environment details.
3. Classify the likely problem category: model capability, environment/tooling, business-context clarity, workflow/process, user-skill/training, data/permission, safety/compliance, or unknown.
4. Separate facts from inferred possibilities. Mark uncertain fields as `unknown` instead of inventing details.
5. Normalize the report into the template below.
6. Add clear labels using the taxonomy in `references/label-taxonomy.md` when needed.
7. Include follow-up questions only as "Suggested additional information"; do not block output unless the user explicitly asks for an interview-style intake.

## Output Template

```markdown
## AI Usage Feedback

### Title
<One concise sentence describing the issue.>

### Summary
<Objective summary of what happened, based only on the user's description.>

### Original Description
<Preserve the user's original wording.>

### Scenario
- Tool: `<tool-name-or-unknown>`
- Scenario: `<scenario-label>`
- Task Type: `<task-label>`
- Workflow Stage: `<stage-label-or-unknown>`
- Affected User/Role: `<role-or-unknown>`

### Problem Category
- Primary Category: `<category-label>`
- Secondary Categories: `<category-label-or-none>`
- Classification Confidence: `<high|medium|low|unknown>`
- Evidence: `<short reason based on the user's description>`

### Labels
- `tool:<value>`
- `category:<value>`
- `scenario:<value>`
- `task:<value>`
- `issue:<value>`
- `capability:<value>`
- `severity:<value>`
- `frequency:<value>`

### Impact
<Describe the likely impact on efficiency, quality, trust, cost, or safety. If unclear, say unknown.>

### Possible Causes
<Optional. List only reasonable hypotheses and make uncertainty clear.>

### Improvement Direction
<How this feedback could help improve AI-assisted R&D, such as model behavior, tool integration, environment setup, prompt/workflow design, business requirement capture, or developer enablement.>

### Suggested Additional Information
- <Specific detail that would help triage the issue.>
- <Specific detail that would help reproduce or understand impact.>

### Suggested Routing
<One or more of: product experience, model capability, tool integration, environment setup, business analysis, prompt/workflow design, permissions/data access, documentation/training, safety/compliance, unknown.>
```

## Labeling Guidance

Use compact machine-readable labels. Prefer lowercase kebab-case values.

Required label families:

- `tool`: the AI product or agent involved.
- `category`: the likely root problem class for statistical analysis and improvement planning.
- `scenario`: the broad usage scenario.
- `task`: the user's intended task.
- `issue`: the observed failure mode.
- `capability`: the likely AI capability area involved.
- `severity`: estimated impact level.
- `frequency`: how often it appears to occur.

If the report spans multiple issue types, include multiple `issue:` labels. If a field is not stated or cannot be safely inferred, use `unknown`.

Read `references/label-taxonomy.md` when you need canonical label values or severity rules.

## Problem Category Rules

Use `category:` to answer "what kind of improvement would most likely prevent this problem from happening again?"

- `category:model-capability`: The AI misunderstood context, reasoned poorly, hallucinated, failed to plan, ignored instructions, used tools incorrectly, or repeated a failing strategy despite adequate task context and environment.
- `category:environment-tooling`: The issue appears caused by local environment, dependencies, build/test setup, IDE/CLI integration, tool permissions, network, unavailable commands, or unreliable tool execution.
- `category:business-context-clarity`: The user, team, or AI did not have a clear enough description of the business goal, product rule, domain concept, acceptance criteria, edge case, or desired behavior.
- `category:workflow-process`: The issue comes from how the AI-assisted R&D workflow is organized, such as missing review gates, unclear handoff, weak task decomposition, no test strategy, or no rollback/checkpoint habit.
- `category:user-skill-training`: The main gap is likely prompt writing, AI usage habits, expectation setting, or knowing how to provide context and verify output.
- `category:data-permission`: The AI could not access required files, repositories, documents, logs, credentials, private data, or knowledge sources.
- `category:safety-compliance`: The issue involves privacy, security, compliance, unsafe code changes, or irreversible actions.
- `category:unknown`: The description is insufficient to classify responsibly.

Prefer one primary category. Add secondary categories only when they are clearly relevant. Set confidence to `low` when the category is mostly inferred.

## Severity Rules

- `severity:low`: Minor inconvenience, easy workaround, little business impact.
- `severity:medium`: Noticeable efficiency or quality impact, but user can recover.
- `severity:high`: Blocks a task, causes significant rework, or affects multiple users.
- `severity:critical`: Causes data loss, security/privacy risk, production impact, compliance exposure, or unsafe irreversible action.

## Style Rules

- Be neutral and concise.
- Do not blame the user or the AI system.
- Do not promise root cause unless evidence is provided.
- Do not solve the original task unless the user explicitly asks.
- Preserve enough original detail for later review.
- Prefer a complete first-pass report over asking many clarifying questions.

## Example

Input:

```text
I was using opencode to modify an API. The model kept editing the wrong files, and after tests failed repeatedly, it did not change its approach.
```

Output:

```markdown
## AI Usage Feedback

### Title
opencode repeatedly edited the wrong files during an API change task

### Summary
The user was using opencode to modify an API, but the AI repeatedly edited incorrect files and kept rerunning failing tests without changing its approach.

### Original Description
I was using opencode to modify an API. The model kept editing the wrong files, and after tests failed repeatedly, it did not change its approach.

### Scenario
- Tool: `opencode`
- Scenario: `coding`
- Task Type: `api-change`
- Workflow Stage: `implementation-and-verification`
- Affected User/Role: `developer`

### Problem Category
- Primary Category: `model-capability`
- Secondary Categories: `workflow-process`
- Classification Confidence: `medium`
- Evidence: The description says the AI repeatedly edited the wrong files and did not change strategy after test failures.

### Labels
- `tool:opencode`
- `category:model-capability`
- `scenario:coding`
- `task:api-change`
- `issue:wrong-file-edit`
- `issue:repeated-failure`
- `capability:planning`
- `capability:context-management`
- `severity:medium`
- `frequency:unknown`

### Impact
The issue likely reduced development efficiency and increased manual review, rollback, and debugging effort.

### Possible Causes
The AI may have failed to build an accurate codebase map, preserve task context, or revise its plan after repeated test failures.

### Improvement Direction
Improve the coding agent's repository understanding, failure recovery behavior, and guardrails for changing files only after confirming the relevant code path.

### Suggested Additional Information
- Which files were expected to change and which files were incorrectly modified.
- The failing test command and error output.
- Whether similar behavior has happened in other tasks.

### Suggested Routing
model capability, prompt/workflow design
```
