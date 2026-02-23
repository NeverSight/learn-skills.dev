---
name: dynamic-api-integration
description: Discover, parse, and call external HTTP APIs at runtime using OpenAPI specs, tool templates, and iterative chaining. Adapted from UTCP (Universal Tool Calling Protocol) patterns for Node.js and Claude Code agents.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, WebFetch, WebSearch]
best_practices:
  - Always fetch and validate the OpenAPI spec before constructing requests
  - Use environment variables for all API keys and secrets; never hardcode
  - Apply max_iterations guard to prevent infinite API call loops
  - Truncate or summarize large API responses to stay within context budget
  - Match user intent to API endpoints semantically before calling
  - Handle errors explicitly with retry logic for transient failures
error_handling: strict
streaming: supported
---

**Mode: Cognitive/Prompt-Driven** — No standalone utility script; use via agent context.

# Dynamic API Integration

## Overview

This skill teaches agents how to dynamically discover, parse, and call external HTTP APIs at runtime. It is adapted from the [Universal Tool Calling Protocol (UTCP)](https://www.utcp.io/) patterns, translated into Node.js / Claude Code tool patterns.

**Core workflow (5-phase, inspired by UTCP agent state machine):**

1. **Discover** — Fetch and parse an OpenAPI/Swagger spec (or define a manual tool template).
2. **Match** — Map the user's intent to the right API endpoint semantically.
3. **Construct** — Build the HTTP request with proper method, path, params, headers, body, and auth.
4. **Execute** — Call the API via Bash (curl) or WebFetch and capture the response.
5. **Chain** — If the task is not yet complete, re-analyze and execute another call (up to max_iterations).

## When to Use

**Use this skill when:**

- Agent needs to call an external REST API it has not used before
- User provides an API URL or OpenAPI spec URL and wants data extracted
- Agent must discover available endpoints from a spec before choosing which to call
- Multiple API calls need to be chained iteratively (search -> get details -> filter)
- Agent needs to construct HTTP requests with authentication and parameters

**Do NOT use when:**

- The API is already wrapped as an MCP tool (use the MCP tool directly)
- The integration is a one-time hardcoded call (just use Bash curl directly)
- The API requires OAuth 2.0 authorization code flow with user-interactive redirect
- The API uses WebSocket or streaming-only protocols (not HTTP REST)

## The Iron Law

```
NEVER HARDCODE API KEYS IN REQUESTS — USE ENVIRONMENT VARIABLES ONLY
```

If you find yourself typing an API key in a curl command, STOP. Use `$ENV_VAR` syntax.

---

## Phase 1: Discover — Fetch and Parse the API Spec

### Option A: OpenAPI/Swagger Spec Discovery

When the API provides an OpenAPI spec (most modern APIs do):

```bash
# Step 1: Fetch the OpenAPI spec
WebFetch({
  url: "https://api.example.com/openapi.json",
  prompt: "Extract all API endpoints. For each endpoint, list: HTTP method, path, description, required parameters, optional parameters, authentication requirement. Return as a structured list."
})
```

**What to extract from the spec:**

| Field           | Location in Spec              | Purpose                    |
| --------------- | ----------------------------- | -------------------------- |
| Base URL        | `servers[0].url`              | API root for all requests  |
| Endpoints       | `paths.*`                     | Available operations       |
| Methods         | `paths.*.get/post/put/delete` | HTTP verbs per endpoint    |
| Parameters      | `paths.*.*.parameters[]`      | Query, path, header params |
| Request body    | `paths.*.*.requestBody`       | POST/PUT payload schema    |
| Auth            | `components.securitySchemes`  | API key, Bearer, OAuth     |
| Response schema | `paths.*.*.responses.200`     | Expected response format   |

**Common OpenAPI spec locations:**

- `https://api.example.com/openapi.json`
- `https://api.example.com/swagger.json`
- `https://api.example.com/v3/api-docs`
- `https://api.example.com/.well-known/openapi.json`
- `https://api.example.com/docs` (HTML page may link to spec)

### Option B: Manual Tool Template (No Spec Available)

When no OpenAPI spec exists, define a tool template manually:

```json
{
  "name": "search_books",
  "description": "Search Open Library for books by query",
  "base_url": "https://openlibrary.org/search.json",
  "method": "GET",
  "auth": null,
  "parameters": {
    "q": {
      "type": "string",
      "required": true,
      "in": "query",
      "description": "Search query (title, author, ISBN)"
    },
    "limit": {
      "type": "integer",
      "required": false,
      "in": "query",
      "description": "Max results to return (default 10)"
    },
    "page": {
      "type": "integer",
      "required": false,
      "in": "query",
      "description": "Page number for pagination"
    }
  },
  "response_hint": "Returns { numFound, docs: [{ title, author_name, first_publish_year }] }"
}
```

### Tool Template JSON Schema

The tool template format (inspired by UTCP `manual_call_templates`):

```json
{
  "name": "string (required) — unique tool identifier, lowercase_snake_case",
  "description": "string (required) — what this tool does, used for semantic matching",
  "base_url": "string (required) — full URL including path",
  "method": "string (required) — GET | POST | PUT | PATCH | DELETE",
  "content_type": "string (optional) — default: application/json",
  "auth": {
    "type": "string — api_key | bearer | basic | none",
    "header": "string — header name (e.g., X-Api-Key, Authorization)",
    "env_var": "string — environment variable name holding the secret",
    "prefix": "string (optional) — e.g., 'Bearer ' for bearer auth"
  },
  "parameters": {
    "<param_name>": {
      "type": "string | integer | boolean | array | object",
      "required": "boolean",
      "in": "query | path | header | body",
      "description": "string — what this parameter does",
      "default": "any (optional) — default value if not provided"
    }
  },
  "response_hint": "string (optional) — brief description of response shape"
}
```

---

## Phase 2: Match — Semantic Intent-to-Endpoint Mapping

Before calling an API, match the user's intent to the correct endpoint:

### Step 1: Understand the user's goal

Ask yourself: What data does the user want? What action do they want performed?

### Step 2: Map intent to endpoint

| User Intent                  | Likely HTTP Method | Endpoint Pattern                  |
| ---------------------------- | ------------------ | --------------------------------- |
| "Find / search / list / get" | GET                | `/search`, `/list`, `/{resource}` |
| "Create / add / register"    | POST               | `/{resource}`                     |
| "Update / modify / change"   | PUT or PATCH       | `/{resource}/{id}`                |
| "Delete / remove"            | DELETE             | `/{resource}/{id}`                |
| "Get details about X"        | GET                | `/{resource}/{id}`                |

### Step 3: Select parameters

- **Required parameters:** Must be provided (check `required: true` in spec/template).
- **Optional parameters:** Use only if user specified them or they improve results.
- **Path parameters:** Substitute into URL (e.g., `/repos/{owner}/{repo}`).
- **Query parameters:** Append as `?key=value&key2=value2`.
- **Body parameters:** Send as JSON payload in POST/PUT/PATCH.

---

## Phase 3: Construct — Build the HTTP Request

### Request Construction Checklist

1. **URL:** Base URL + path + path parameter substitution
2. **Method:** GET, POST, PUT, PATCH, DELETE
3. **Headers:** Content-Type, Authorization, Accept, custom headers
4. **Query parameters:** URL-encoded, appended to URL
5. **Body:** JSON payload for POST/PUT/PATCH
6. **Auth:** Injected from environment variable

### Auth Patterns

**API Key (Header):**

```bash
curl -s -X GET "https://api.example.com/data?q=test" \
  -H "X-Api-Key: $API_KEY"
```

**Bearer Token:**

```bash
curl -s -X GET "https://api.example.com/data" \
  -H "Authorization: Bearer $AUTH_TOKEN"
```

**Basic Auth:**

```bash
curl -s -X GET "https://api.example.com/data" \
  -u "$USERNAME:$PASSWORD"
```

**No Auth (Public API):**

```bash
curl -s -X GET "https://api.example.com/data?q=test"
```

### Request Templates by Method

**GET with query parameters:**

```bash
curl -s -X GET "https://api.example.com/search?q=test&limit=10&page=1" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer $TOKEN"
```

**POST with JSON body:**

```bash
curl -s -X POST "https://api.example.com/items" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "New Item", "category": "tools", "price": 29.99}'
```

**PUT with path parameter:**

```bash
curl -s -X PUT "https://api.example.com/items/123" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "Updated Item", "price": 39.99}'
```

**DELETE:**

```bash
curl -s -X DELETE "https://api.example.com/items/123" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Phase 4: Execute — Call the API and Process the Response

### Using Bash (curl) — Primary Method

```bash
# Execute and capture response + HTTP status
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "https://api.example.com/search?q=test" \
  -H "Accept: application/json")
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

echo "Status: $HTTP_CODE"
echo "Body: $BODY" | head -c 2000  # Truncate to 2KB for context safety
```

### Using WebFetch — When You Need AI Processing

```javascript
WebFetch({
  url: 'https://api.example.com/search?q=test',
  prompt:
    'Extract the top 5 results with their titles and descriptions. Format as a numbered list.',
});
```

**When to use which:**

| Scenario                             | Tool                   | Reason                              |
| ------------------------------------ | ---------------------- | ----------------------------------- |
| Need raw JSON for further processing | Bash (curl)            | Full control, parseable output      |
| Need summarized/extracted data       | WebFetch               | AI processes response inline        |
| Need to check HTTP status codes      | Bash (curl)            | WebFetch abstracts status away      |
| Large response (>50KB)               | Bash (curl) + truncate | WebFetch may timeout on large pages |
| HTML page (not JSON)                 | WebFetch               | Converts HTML to markdown           |

### Error Handling

**HTTP Status Code Handling:**

| Status  | Meaning      | Action                                          |
| ------- | ------------ | ----------------------------------------------- |
| 200-299 | Success      | Parse response, continue                        |
| 400     | Bad Request  | Check parameters, fix and retry                 |
| 401     | Unauthorized | Check API key/token, re-authenticate            |
| 403     | Forbidden    | Check permissions, report to user               |
| 404     | Not Found    | Check URL/resource ID, try alternative endpoint |
| 429     | Rate Limited | Wait (check Retry-After header), then retry     |
| 500-599 | Server Error | Wait and retry up to 3 times                    |

**Retry with Exponential Backoff:**

```bash
# Retry pattern for transient errors (429, 5xx)
for attempt in 1 2 3; do
  RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$URL" -H "Authorization: Bearer $TOKEN")
  HTTP_CODE=$(echo "$RESPONSE" | tail -1)
  if [ "$HTTP_CODE" -lt 400 ]; then
    break  # Success
  fi
  echo "Attempt $attempt failed ($HTTP_CODE), retrying in $((attempt * 2))s..."
  sleep $((attempt * 2))
done
```

### Response Processing

**Parse JSON response (Bash):**

```bash
# Extract specific fields from JSON response
echo "$BODY" | node -e "
  const data = JSON.parse(require('fs').readFileSync('/dev/stdin', 'utf8'));
  console.log('Total:', data.totalResults);
  data.items?.slice(0, 5).forEach((item, i) => {
    console.log(\`\${i+1}. \${item.title} — \${item.description?.substring(0, 80)}\`);
  });
"
```

**Truncate large responses:**

```bash
# Safety: never pass >10KB of API response into context
BODY_TRUNCATED=$(echo "$BODY" | head -c 10000)
if [ ${#BODY} -gt 10000 ]; then
  echo "[TRUNCATED: Response was $(echo "$BODY" | wc -c) bytes, showing first 10KB]"
fi
```

---

## Phase 5: Chain — Iterative Multi-Call Workflow

Many tasks require multiple API calls chained together. Use the UTCP-inspired iterative pattern:

### Chaining Pattern

```
Iteration 1: Search -> Get list of results
Iteration 2: Get details for top result
Iteration 3: Perform action on result
(max_iterations guard: stop at 5)
```

### The Iteration Guard (MANDATORY)

```
MAX_ITERATIONS = 5

Before each API call:
  IF iteration_count >= MAX_ITERATIONS:
    STOP. Summarize what was gathered so far and respond.
  ELSE:
    Execute the call, increment counter, re-analyze task.
```

**Why this matters:** Without an iteration guard, an agent could loop indefinitely calling APIs. UTCP uses a default of 3; we recommend 5 for more complex multi-step workflows.

### Chaining Examples

**Example 1: Search and Get Details**

```
User: "Find information about the book '1984' by George Orwell"

Iteration 1:
  Call: GET https://openlibrary.org/search.json?q=1984+george+orwell&limit=5
  Result: Found 5 matches, top result has key "/works/OL1168083W"

Iteration 2:
  Call: GET https://openlibrary.org/works/OL1168083W.json
  Result: Full book details (title, description, subjects, covers)

Task complete: Return summarized book information.
```

**Example 2: GitHub — Find and Analyze a Repository**

```
User: "What are the most recent issues in the react repository?"

Iteration 1:
  Call: GET https://api.github.com/repos/facebook/react/issues?state=open&per_page=10&sort=created
  Headers: Authorization: Bearer $GITHUB_TOKEN
  Result: 10 most recent open issues

Task complete: Summarize issue titles, labels, and dates.
```

**Example 3: Multi-API Chain**

```
User: "Find news about AI safety and summarize the top article"

Iteration 1:
  Call: GET https://newsapi.org/v2/everything?q=AI+safety&sortBy=publishedAt&pageSize=5
  Headers: X-Api-Key: $NEWS_API_KEY
  Result: 5 articles with titles, URLs

Iteration 2:
  Call: WebFetch({ url: articles[0].url, prompt: "Summarize this article in 3 bullet points" })
  Result: Article summary

Task complete: Return article title + summary.
```

---

## Real-World API Examples

### GitHub API (Bearer Token Auth)

```bash
# List repositories for a user
curl -s -X GET "https://api.github.com/users/octocat/repos?sort=updated&per_page=5" \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN"
```

**Tool Template:**

```json
{
  "name": "github_list_repos",
  "description": "List repositories for a GitHub user, sorted by most recently updated",
  "base_url": "https://api.github.com/users/{username}/repos",
  "method": "GET",
  "auth": {
    "type": "bearer",
    "header": "Authorization",
    "env_var": "GITHUB_TOKEN",
    "prefix": "Bearer "
  },
  "parameters": {
    "username": {
      "type": "string",
      "required": true,
      "in": "path",
      "description": "GitHub username"
    },
    "sort": {
      "type": "string",
      "required": false,
      "in": "query",
      "description": "Sort field: created, updated, pushed, full_name",
      "default": "updated"
    },
    "per_page": {
      "type": "integer",
      "required": false,
      "in": "query",
      "description": "Results per page (max 100)",
      "default": 10
    }
  }
}
```

### Open Library API (No Auth)

```bash
# Search for books
curl -s -X GET "https://openlibrary.org/search.json?q=george+orwell&limit=5" \
  -H "Accept: application/json"
```

### JSONPlaceholder (Testing/Prototyping)

```bash
# GET all posts
curl -s https://jsonplaceholder.typicode.com/posts?_limit=5

# POST new item
curl -s -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Post", "body": "Hello world", "userId": 1}'
```

### Weather API (API Key Auth)

```bash
# Get current weather
curl -s "https://api.open-meteo.com/v1/forecast?latitude=51.5074&longitude=-0.1278&current_weather=true"
```

---

## Context Management for Large Responses

API responses can be very large. Apply these rules to prevent context overflow:

### Response Size Limits

| Response Size | Action                                  |
| ------------- | --------------------------------------- |
| < 5 KB        | Use full response                       |
| 5-20 KB       | Extract relevant fields only            |
| 20-50 KB      | Summarize via WebFetch or node script   |
| > 50 KB       | Truncate to first 5KB + count remaining |

### Extraction Pattern (Recommended for Large Responses)

```bash
# Instead of dumping full response, extract what you need
curl -s "https://api.example.com/search?q=test" | node -e "
  const data = JSON.parse(require('fs').readFileSync('/dev/stdin', 'utf8'));
  // Extract only what the user asked for
  const results = data.results.slice(0, 5).map(r => ({
    id: r.id,
    title: r.title,
    summary: r.description?.substring(0, 200)
  }));
  console.log(JSON.stringify(results, null, 2));
"
```

---

## Security Checklist

- [ ] All API keys stored in environment variables (never in code/commands)
- [ ] HTTPS used for all API calls (never HTTP for authenticated requests)
- [ ] Response data validated before use (check status codes)
- [ ] No user secrets logged or written to files
- [ ] Rate limits respected (check headers: X-RateLimit-Remaining)
- [ ] Sensitive response data (PII, tokens) not stored in memory files
- [ ] Timeout set on all requests (`curl --max-time 30`)

---

## Verification Checklist

Before completing a dynamic API integration task:

- [ ] API spec was fetched and endpoints were identified
- [ ] User intent was mapped to the correct endpoint and method
- [ ] Request includes proper authentication (if required)
- [ ] Request parameters match the API schema (required params present)
- [ ] HTTP status code was checked and errors handled
- [ ] Response was truncated/summarized if > 5KB
- [ ] Iteration count did not exceed max_iterations (5)
- [ ] No API keys were hardcoded in any command or file

---

## Anti-Patterns (AVOID)

| Anti-Pattern                           | Why It Fails                                | Correct Approach                   |
| -------------------------------------- | ------------------------------------------- | ---------------------------------- |
| Hardcoding API keys                    | Security risk, breaks when rotated          | Use `$ENV_VAR` in all commands     |
| Calling API without reading spec first | Wrong endpoint, wrong parameters            | Discover first (Phase 1)           |
| Passing full 100KB response to context | Context overflow, degraded performance      | Truncate/extract (Phase 4)         |
| No iteration guard on chained calls    | Infinite loops burning tokens               | Always enforce max_iterations      |
| Guessing parameter names               | 400 errors, wasted calls                    | Read spec/docs before constructing |
| Ignoring HTTP error codes              | Silent failures, wrong results              | Check status, handle 4xx/5xx       |
| Using POST when GET is correct         | API rejects or creates unintended resources | Match method to intent (Phase 2)   |

---

## Quick Reference Card

```
DISCOVER  → WebFetch(spec_url) or define manual tool template
MATCH     → Map user intent to endpoint + method + params
CONSTRUCT → Build curl command with URL, headers, auth, body
EXECUTE   → Bash(curl) for JSON, WebFetch for HTML/summarize
CHAIN     → Re-analyze task, call again (max 5 iterations)
```

**Auth Quick Reference:**

```
API Key:  -H "X-Api-Key: $KEY"
Bearer:   -H "Authorization: Bearer $TOKEN"
Basic:    -u "$USER:$PASS"
None:     (no auth header needed)
```

**Tool Template Quick Create:**

```json
{
  "name": "...",
  "description": "...",
  "base_url": "...",
  "method": "GET",
  "auth": { "type": "api_key", "header": "...", "env_var": "..." },
  "parameters": { "q": { "type": "string", "required": true, "in": "query" } }
}
```

---

## Research Basis

This skill is adapted from:

- [Universal Tool Calling Protocol (UTCP)](https://www.utcp.io/) — open standard for AI agent tool calling
- [UTCP Agent](https://github.com/universal-tool-calling-protocol/utcp-agent) — LangGraph-based reference implementation
- [UTCP Specification](https://github.com/universal-tool-calling-protocol/utcp-specification) — RFC and protocol definition
- [OpenAPI Specification 3.1](https://spec.openapis.org/oas/v3.1.0.html) — API description standard
- [OpenAPI Best Practices](https://learn.openapis.org/best-practices.html) — community guidelines
- [agents.json Specification](https://github.com/wild-card-ai/agents-json) — API-agent contract standard
- [API Integration Patterns (2026)](https://composio.dev/blog/apis-ai-agents-integration-patterns) — pattern taxonomy

## Related Skills

- `auth-security-expert` — OAuth 2.1, JWT, encryption patterns
- `nodejs-expert` — Node.js HTTP patterns
- `debugging` — API call failure investigation
- `research-synthesis` — Researching new APIs before integration

## Memory Protocol

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New API pattern discovered -> `.claude/context/memory/learnings.md`
- API issue/limitation found -> `.claude/context/memory/issues.md`
- API design decision made -> `.claude/context/memory/decisions.md`
- Reusable tool template created -> save to `.claude/context/memory/named/api-templates.md`

Assume interruption: if it is not in memory, it did not happen.
