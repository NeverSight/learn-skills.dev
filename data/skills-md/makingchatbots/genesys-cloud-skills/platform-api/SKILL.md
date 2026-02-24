---
name: platform-api
description: Queries the Genesys Cloud Platform API schema for endpoint details,
  permissions, parameters, and response formats. Use when user asks about Genesys
  Cloud API endpoints (e.g., "/api/v2/assistants/queues"), API documentation, API
  permissions, schemas, capabilities, or when implementing Genesys Cloud operations.
allowed-tools: Bash(jq:*), Bash(SCHEMA="*/schema.json" && jq **), Bash(SCHEMA="*/schema.json" jq **)
---

# Platform API Extraction Skill

## Overview

This skill provides jq query patterns for extracting API endpoint information from the Genesys Cloud Platform API Swagger 2.0 schema. The schema contains over 1,900 endpoints and 4,305 definitions in a 19MB+ file.

**Schema**: `schema.json` must be downloaded before first use. Run the download script from this skill's directory:

```bash
./scripts/download-schema.sh
```

See the [download script](scripts/download-schema.sh) for region options and usage details.

Before running any queries, determine the absolute path to this SKILL.md file's parent directory and set the schema path variable:

```bash
SCHEMA="<resolved-skill-directory>/schema.json"
```

All examples below use `"$SCHEMA"` to reference this file.

---

## MANDATORY WORKFLOW

**CRITICAL: NEVER recommend endpoints without verification!**

When asked about an endpoint or API operation, you MUST follow this 4-step workflow:

### PERFORMANCE REQUIREMENT: Execute Queries in PARALLEL

**Steps 1-3 are INDEPENDENT queries. Execute them in a SINGLE message using multiple Bash tool calls in parallel.**

### Step 1: Search & Verify

**Search for matching endpoints** (ALWAYS limit to 15-20 results):

```bash
jq -r '.paths | keys | map(select(test("KEYWORD"; "i"))) | .[0:15] | .[]' "$SCHEMA"
```

Common patterns: "find all X" -> `/api/v2/X$`, "get specific X" -> `/api/v2/X/\{id\}`

See `references/search-operations.md` for detailed search patterns.

### Step 2: Confirm Exact Endpoint Exists

```bash
jq '.paths["/api/v2/exact/path"] | keys' "$SCHEMA"
```

If this returns `null`, the endpoint **does not exist**. Do NOT proceed.

### Step 3: Extract Full Operation Details

```bash
jq '.paths["/api/v2/exact/path"]["METHOD"] | {
  operationId,
  summary,
  description,
  permissions: ."x-inin-requires-permissions",
  parameters: [.parameters[]? | {name, in, required, type, description}]
}' "$SCHEMA"
```

Replace `METHOD` with: get, post, put, patch, or delete.

See `references/jq-query-patterns.md` for complete extraction patterns and `references/schema-resolution.md` for resolving `$ref` references.

### Step 4: Format and Respond to User

After completing steps 1-3 with **actual results from the schema**, respond using this structure:

```
## Recommended Endpoint

**Endpoint:** `[METHOD] /api/v2/path`
**Operation ID:** `operationId`
**Summary:** Brief description

### Permissions
- Type: ALL/ANY (or "No special permissions required" if null)
- Required: permission list

### Key Parameters
- List path/query/body parameters with required status

### Usage Notes
- Brief guidance on how to use this endpoint
- Any important caveats or considerations
```

---

## FORBIDDEN BEHAVIORS

- Assuming endpoints exist based on REST patterns
- Guessing endpoint paths without verification
- Recommending endpoints before running verification queries
- Providing information based on typical API conventions
- Executing queries sequentially when they can run in parallel
- Returning unlimited search results (always limit to 15-20)

## REQUIRED BEHAVIORS

- Always run verification queries before every recommendation
- Execute independent queries in PARALLEL using multiple Bash tool calls in a single message
- Use actual schema data in your responses
- Limit search results with `.[0:15]` or similar
- Show uncertainty if verification fails ("The endpoint does not exist in the schema")
- Provide alternatives if searched endpoint is not found
- Format responses using the structured template

---

## COMPLETE WORKFLOW EXAMPLE

**User asks:** "What API endpoint can be used to find all the users?"

**Execute Steps 1-3 in PARALLEL** (single message with 3 Bash tool calls):

```bash
# Tool Call 1: Search for user endpoints
jq -r '.paths | keys | map(select(test("user"; "i"))) | .[0:15] | .[]' "$SCHEMA"

# Tool Call 2: Verify /api/v2/users exists
jq '.paths["/api/v2/users"] | keys' "$SCHEMA"

# Tool Call 3: Get full details for GET /api/v2/users
jq '.paths["/api/v2/users"]["get"] | {
  operationId,
  summary,
  description,
  permissions: ."x-inin-requires-permissions",
  parameters: [.parameters[]? | {name, in, required, type, description}]
}' "$SCHEMA"
```

**Step 4: Respond with structured format**

```
## Recommended Endpoint

**Endpoint:** `GET /api/v2/users`
**Operation ID:** `getUsers`
**Summary:** Get the list of available users.

### Permissions
- Type: No special permissions required (permissions is null)

### Key Parameters
- `pageSize` (query, optional): Page size
- `pageNumber` (query, optional): Page number
- `id` (query, optional): A list of user IDs to fetch by bulk
- `sortOrder` (query, optional): Ascending or descending sort order
- `state` (query, optional): Only list users of this state

### Usage Notes
- This endpoint supports pagination via pageSize and pageNumber
- You can fetch specific users by providing an array of IDs in the id parameter
- Use expand parameter to include additional user information
```

---

## Resources

**Reference Documentation**:
- `references/jq-query-patterns.md` - Comprehensive jq syntax, advanced filtering, variable chaining
- `references/search-operations.md` - All search techniques, count-before-fetch patterns
- `references/schema-resolution.md` - Definition resolution, nested references, property extraction
- `references/complete-examples.md` - Step-by-step workflow examples for common tasks

**External Resources**:
- Swagger 2.0 Spec: https://swagger.io/specification/v2/
- jq Manual: https://jqlang.github.io/jq/manual/
