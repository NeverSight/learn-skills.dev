---
name: agent-data-extend
description: >-
  Extend an existing agent-data API when it lacks capabilities needed for the
  user's task. Inspect the current API, describe the missing behavior, submit
  an extension or owner revision, and validate the published result.
metadata:
  version: "0.2.7-draft"
---

# Extend an agent-data API

Describe what the user needs to accomplish and what the current API is missing. Use [agent-data-cli](../agent-data-cli/SKILL.md) for setup and CLI usage.

## 1. Establish the gap

Reuse the API selected for the task, or use [agent-data-search](../agent-data-search/SKILL.md) to find it. Read `agent-data docs LISTING_ID` and check whether the current API already supports the workflow.

Use a real call when the gap depends on runtime behavior. Retain the request, response, and missing capability. Authentication failures, allowance errors, and timeouts require troubleshooting rather than additional API capabilities.

## 2. Describe the desired result

Write an [API brief](../agent-data-build/references/api-brief.md) covering the user's goal, what the API already enables, the missing behavior, and example uses that demonstrate the improvement. Include relevant real requests and results from the current API.

Choose the supported submission path:

| Change | Path |
|---|---|
| Additional capabilities exposed through new public endpoints | Saved extension request: step 3. |
| Changes to a live API the user owns | Owner revision: step 4. |
| Data from a different source with no suitable API | [agent-data-build](../agent-data-build/SKILL.md). |

Public extensions add endpoints; they cannot replace existing routes. Extending is free. Submit the work needed for the user's task without a separate approval step.

## 3. Submit a public extension

Inspect the target using its handle or listing UUID:

```bash
agent-data parse extension target API_REFERENCE
```

Save the response. If `canStart` is false, report the returned blocker. Otherwise create `extension-request.json` using the [saved request format](references/saved-request.md). Copy the returned `listingId` and `contractVersion`, describe the requested capabilities in prose, and save the request's UUIDs before submission.

```bash
agent-data parse extension submit extension-request.json --dry-run
agent-data parse extension submit extension-request.json
agent-data parse extension status REQUEST_ID
```

The preview validates the payload without submitting a build. After a timeout, check status with the saved `requestId`. Retry the **same complete payload unchanged** when recovering that submission.

On `contract_changed`, refresh the docs and target, reassess the gap, and save a new request for the revised proposal. Preserve the rejected request. For other failures, use the returned error and status to determine the next action.

Follow a returned `buildId` through [build status and recovery](../agent-data-build/references/build-lifecycle.md). Validate the API after the extension reaches `published`.

## 4. Revise an owned live API

Use `agent-data parse list` and `agent-data parse status PARSE_JOB_ID` to identify the user's current live build. Save the requested changes and example uses in `extension-task.md`:

```bash
agent-data parse revise PARSE_JOB_ID "$(cat extension-task.md)"
```

Save the returned build ID and follow [build status and recovery](../agent-data-build/references/build-lifecycle.md). If the submission response is lost, recover the build's identity before submitting again.

## 5. Validate the improvement

Read the published docs and run the requested workflows with real data, following [agent-data-build](../agent-data-build/SKILL.md) step 4. Confirm that the capability motivating the extension is usable.

Repeat representative existing calls affected by the change. Compare their documented behavior and record identity; live source values can change between calls.

Retain full requests, responses, and diagnostics. Report the request/build ID, publication state, working calls, remaining gaps, and checks not performed. Use the improved API to complete the user's task.
