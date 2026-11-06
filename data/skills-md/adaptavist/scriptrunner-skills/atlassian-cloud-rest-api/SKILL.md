---
name: atlassian-cloud-rest-api
description: Local Atlassian Cloud REST API OpenAPI lookup skill for Confluence Cloud v1/v2, Jira Cloud platform v3, Jira Software Cloud, Jira Service Management Cloud, and Assets Cloud. Use when users ask for REST paths, parameters, request bodies, or response schemas.
metadata:
    author: sms-core
    version: '1.0'
    generated-spec-count: '6'
---

# Atlassian Cloud REST API Skill

Use this skill when you need Atlassian Cloud REST contract details from the local OpenAPI specs bundled into the generated skill.

## Available specs

- `references/specs/assets-cloud-openapi.json` - Assets Cloud REST API (/rest/assets/1.0/...)
- `references/specs/confluence-cloud-v1-openapi.json` - Confluence Cloud REST API v1 (/wiki/rest/api/...)
- `references/specs/confluence-cloud-v2-openapi.json` - Confluence Cloud REST API v2 (/wiki/api/v2/...)
- `references/specs/jira-cloud-platform-v3-openapi.json` - Jira Cloud platform REST API v3 (/rest/api/3/...)
- `references/specs/jira-service-management-cloud-openapi.json` - Jira Service Management Cloud REST API (/rest/servicedeskapi/...)
- `references/specs/jira-software-cloud-openapi.json` - Jira Software Cloud REST API (/rest/agile/1.0/...)

See `references/SPECS.md` for the quick map.

## Workflow

1. Load this skill before answering Atlassian Cloud REST API questions.
2. Resolve the operations you need in one call with `assets/operation.jq` (below). Use `references/SPECS.md`, `rg`, and `jq` only for what it does not answer.
3. Use a subagent only for bounded discovery across a large search space. Ask it for concise findings, spec file paths, HTTP methods, operation paths, schema/component names, and jq selectors or line ranges, not full spec fragments.
4. The parent agent performs any final focused reads and `$ref` resolution needed for accuracy.
5. Read only the smallest matching fragments needed for the answer.
6. Cite the skill file path, HTTP method, operation path, and resolved schema/component names in the final answer.

## CLI guidance

- Resolve operations, `;`-separated, with parameters, request body and success responses fully dereferenced and read-only request properties dropped: `jq -c --arg ops 'POST /rest/api/3/version;GET /rest/api/3/project/{projectIdOrKey}/versions' -f assets/operation.jq references/specs/jira-cloud-platform-v3-openapi.json`
- Find operations by path or summary: `jq -r --arg search 'version' -f assets/operation.jq references/specs/jira-cloud-platform-v3-openapi.json`
- List specs: `ls references/specs`
- Find candidate paths or component names: `rg -n '"/rest/api/3/issue"|IssueBean|CreateIssue' references/specs/*.json`
- Inspect an operation: `jq '.paths["/rest/api/3/issue"].post' references/specs/jira-cloud-platform-v3-openapi.json`
- Inspect a component: `jq '.components.schemas.IssueBean' references/specs/jira-cloud-platform-v3-openapi.json`
- Inspect a Confluence operation: `jq '.paths["/pages"].post' references/specs/confluence-cloud-v2-openapi.json`

## Ref resolution

When generating code or summarizing request/response contracts, do not stop at a raw `$ref`. `assets/operation.jq` does all of this; resolve by hand only what it cuts short (it marks truncated depth with `…`).

1. Resolve both path-level and operation-level `parameters`.
2. Resolve `requestBody` references into `components.requestBodies`, then resolve nested schema refs into `components.schemas`.
3. Resolve response entries in `responses`, including referenced response objects, headers, and nested schema refs.
4. Continue resolving until the effective request/response shape is expanded enough to identify required fields, enums, formats, and nested objects needed for the task.
5. Account for `allOf`, `oneOf`, `anyOf`, and array `items` while resolving.

If a referenced schema is large, resolve only the fields needed for the current code generation task.

## Resource map

- `references/SPECS.md` - human-readable spec index.
- `references/specs/*.json` - raw OpenAPI specs bundled with the skill.
- `assets/specs.json` - machine-readable spec manifest.
- `assets/operation.jq` - operation resolver and search.

## Notes

- Prefer these bundled local OpenAPI specs over memory or web lookups for Atlassian Cloud REST contracts.
- Do not ask subagents to return full spec sections or large excerpts; the parent agent should perform any final focused reads directly.
- Use `scriptrunner-documentation` separately for ScriptRunner behavior; use this skill for Atlassian REST details.
