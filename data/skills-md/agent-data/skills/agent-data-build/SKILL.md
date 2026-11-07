---
name: agent-data-build
description: >-
  Build an agent-data API when the user wants to turn a website into an API
  or needs website data that existing APIs cannot supply. Describe the intended
  workflow, submit the build, and validate the published API. Use agent-data-extend
  for missing capabilities in an existing API.
metadata:
  version: "0.2.7-draft"
---

# Build an agent-data API

Describe what the user wants to accomplish, request the API, and test it against that goal. Use [agent-data-cli](../agent-data-cli/SKILL.md) for setup and CLI usage.

## 1. Select the source

Reuse any source and catalog findings already established. Otherwise use [agent-data-search](../agent-data-search/SKILL.md) to check for an existing API. Use a suitable API directly, or use [agent-data-extend](../agent-data-extend/SKILL.md) when an existing API needs additional capabilities.

If the user has not selected a website, identify a source for the requested data. Ask the user only when choosing between sources would materially change the result.

## 2. Describe the API

Save the request in `api-task.md`. Include:

- **Goal and source:** the website and what the user wants to accomplish with its data.
- **Required behavior:** what callers need to find, compare, inspect, or track, and the information they need to do it.
- **Example uses:** representative tasks that demonstrate a useful result.

Describe the complete workflow in plain language. For example: “Let shoppers search listings using the marketplace's available filters and sorting, browse further results, inspect selected items, and view seller information before deciding what to buy.”

Use the [API brief examples](references/api-brief.md) for builds and extensions.

## 3. Submit and follow the build

Set `SOURCE_URL` to the website's complete URL:

```bash
agent-data parse "$SOURCE_URL" --task "$(cat api-task.md)" --allow-interrupts required
```

`--allow-interrupts required` enables clarification questions. For unattended execution, use `--allow-interrupts disabled`. Add `--dry-run` to preview without starting the build.

Building is free. When the user's task requires a new API, start the build without a separate approval step.

Save the submission response and returned build ID. If `parse` returns an existing API, inspect its docs and use or extend it. Follow [build status and recovery](references/build-lifecycle.md) until the API is published or a blocker requires attention.

## 4. Validate and use the API

Fetch `agent-data docs LISTING_ID` using the published listing ID. Run the brief's example workflows with real inputs and the documented calls.

Check that the returned data supports the intended task and matches the published contract. Exercise requested filtering, sorting, and pagination. For workflows that move from search results to details, follow a returned item through that flow and confirm its identity.

Retain full requests, responses, and diagnostics. Report the API URL, a working call, demonstrated capabilities, remaining gaps, and checks not performed. Use the API to complete the original task. Carry missing capabilities to [agent-data-extend](../agent-data-extend/SKILL.md); report execution failures with their evidence.
