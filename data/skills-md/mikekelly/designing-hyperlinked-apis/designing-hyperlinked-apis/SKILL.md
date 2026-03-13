---
name: designing-hyperlinked-apis
description: "Design principles for building HAL+JSON APIs that agents can explore and distill into deterministic clients. Use when designing, building, reviewing, or improving a hyperlinked API — covers entry points, link relations, CURIEs, versioned relations, relation documentation, deprecation, embedded resources, and progressive disclosure."
---

<objective>
Design HAL+JSON APIs that are self-describing and navigable by AI agents. The API should be explorable from a single entry point through link-following, with each relation documented so an agent can read what a link does, construct the right request, and act — without prior knowledge of the API.

The goal is an API where:
1. An agent starts at the root, follows links, reads relation docs, and completes tasks (exploration)
2. The recorded session can be exported as a deterministic spec that runs without inference (distillation)
</objective>

<quick_start>
A minimal HAL API needs three things:

1. **A root resource** with links to available actions
2. **CURIEs** that map link relation prefixes to documentation URLs
3. **Relation documentation** served as markdown at those URLs

```json
{
  "_links": {
    "curies": [{ "name": "myapi", "href": "https://api.example.com/rels/{rel}", "templated": true }],
    "self": { "href": "/" },
    "myapi:v1:items": { "href": "/items", "title": "All items" },
    "myapi:v1:create-item": { "href": "/items", "title": "Create an item" }
  },
  "title": "My API",
  "description": "A HAL+JSON API"
}
```

When an agent encounters `myapi:v1:items`, the CURIE expands it to `https://api.example.com/rels/v1:items` — a URL serving markdown documentation describing the method, input schema, and response format.
</quick_start>

<essential_principles>
**The API is a graph.** Resources are nodes. Links are edges. The root resource is the entry point. Every resource an agent can reach must be reachable by following links from the root. Never require an agent to construct a URL — it should always come from a link.

**Relation docs are prompt files.** The markdown served at each CURIE-expanded URL is not just documentation — it's a prompt. An agent reads it to learn the HTTP method, input schema, and response shape. Write relation docs as if you're explaining the operation to an agent that has never seen your API before. Include a JSON Schema for the input and an example request.

**Progressive disclosure drives design.** Don't expose everything at the root. The root shows top-level actions. Each response reveals deeper links. An agent navigating from root → collection → item → history discovers capabilities incrementally, loading only what's relevant to its current task.

**Version relations, not the API.** Instead of `/v1/pages` and `/v2/pages`, use versioned relation names: `myapi:v1:pages`. This versions individual transitions rather than the entire API surface. When a relation's contract changes, introduce `myapi:v2:pages` alongside the existing version. The CURIE expansion handles the rest — `v1:pages` and `v2:pages` resolve to different documentation URLs.

**Deprecate through links.** When retiring a relation, add `deprecated: true` and `deprecation: "Use myapi:v2:pages instead"` to the link object. Agents that understand HAL deprecation will warn and adapt. Eventually remove the deprecated link entirely.
</essential_principles>

<entry_point>
The root resource is the only URL an agent needs to know. Design it to surface every top-level capability:

```json
{
  "_links": {
    "curies": [{ "name": "wiki", "href": "https://api.example.com/rels/{rel}", "templated": true }],
    "self": { "href": "/" },
    "wiki:v1:pages": { "href": "/pages", "title": "All wiki pages" },
    "wiki:v1:create-page": { "href": "/pages", "title": "Create a new page" },
    "wiki:v1:categories": { "href": "/categories", "title": "Browse categories" },
    "wiki:v1:search": { "href": "/search{?q}", "templated": true, "title": "Search pages" }
  },
  "title": "Agent Wiki",
  "description": "A HAL+JSON wiki API for AI agent exploration"
}
```

Key points:
- Every link has a `title` — this helps agents understand what the link does before reading the full relation docs
- Templated links (like search) declare `"templated": true` so agents know to substitute variables
- The `self` link is always present
- CURIEs are declared once at the root; agents store them for the session
</entry_point>

<curies>
CURIEs (Compact URIs) namespace your relations and connect them to documentation.

```json
"curies": [{ "name": "wiki", "href": "https://api.example.com/rels/{rel}", "templated": true }]
```

The `{rel}` template variable is replaced with the relation reference. For `wiki:v1:pages`, the prefix is `wiki` and the reference is `v1:pages`, producing `https://api.example.com/rels/v1:pages`.

Choose a short, memorable prefix. One CURIE per API is typical. The prefix appears on every link, so brevity matters.
</curies>

<versioned_relations>
Version the relation name, not the URL path:

| Instead of | Use |
|------------|-----|
| `/v1/pages` | `myapi:v1:pages` with `"href": "/pages"` |
| `/v2/pages` | `myapi:v2:pages` with `"href": "/pages"` |

The version is in the relation name, not the resource URL. This means:
- The same resource can be linked via different relation versions
- Each version has its own documentation URL (via CURIE expansion)
- Clients following `v1:pages` get the v1 contract; clients following `v2:pages` get the v2 contract
- You can deprecate `v1:pages` independently while keeping the resource at `/pages`

Serve relation docs only for the versioned key. If an agent requests docs for the unversioned form (e.g. `/rels/pages`), return `410 Gone` with a message pointing to the versioned equivalent.
</versioned_relations>

<relation_docs>
Each relation's documentation is a markdown file served at the CURIE-expanded URL. Structure it consistently:

```markdown
# wiki:v1:create-page

Creates a new page in the wiki.

## Method

POST

## Input

```json
{
  "type": "object",
  "properties": {
    "title": { "type": "string", "description": "Page title, must be unique" },
    "body": { "type": "string", "description": "Page content (markdown)" },
    "tags": { "type": "array", "items": { "type": "string" }, "description": "Optional tags" }
  },
  "required": ["title", "body"]
}
```

## Example

```http
POST /pages
Content-Type: application/json

{
  "title": "Agent Communication",
  "body": "# Overview\n\nAgents communicate via...",
  "tags": ["protocols"]
}
```

## Response

Returns the created page as a HAL resource. Status: 201 Created.
```

Key points:
- The Input section is a **JSON Schema** — agents use this to validate their request before sending
- Always include Method, Input (with schema), Example, and Response sections
- Serve with `Content-Type: text/markdown`
- Keep docs concise — an agent needs to understand the operation, not read a tutorial
</relation_docs>

<embedded_resources>
Use `_embedded` for collections and nested resources. The key should be a CURIE-expanded relation:

```json
{
  "_links": {
    "curies": [{ "name": "wiki", "href": "https://api.example.com/rels/{rel}", "templated": true }],
    "self": { "href": "/pages" },
    "wiki:v1:create-page": { "href": "/pages", "title": "Create a new page" }
  },
  "_embedded": {
    "wiki:v1:page": [
      {
        "_links": {
          "self": { "href": "/pages/1" },
          "wiki:v1:history": { "href": "/pages/1/history" }
        },
        "id": "1",
        "title": "Hello World",
        "tags": ["test"]
      }
    ]
  },
  "totalCount": 1
}
```

Embedded items should include their own `_links` so agents can navigate to individual resources. Keep embedded representations minimal (summaries) — the full resource is at the `self` link.
</embedded_resources>

<link_design>
Each response should include links that tell the agent what it can do next:

- **Navigation links**: `self`, `next`, `prev` — where am I, where can I go
- **Action links**: `wiki:v1:edit-page`, `wiki:v1:delete-page` — what can I do here
- **Context links**: `wiki:v1:pages`, `wiki:v1:history` — related resources

Name relations by what they do, not how they work:
- `wiki:v1:create-page` not `wiki:v1:post-to-pages`
- `wiki:v1:edit-page` not `wiki:v1:put-page`
- `wiki:v1:history` not `wiki:v1:get-versions`

Use `title` on links to give agents a quick description without needing to fetch the full relation docs.
</link_design>

<deprecation>
When evolving a relation, keep the old version temporarily with deprecation markers:

```json
{
  "wiki:v1:pages": { "href": "/pages", "title": "All pages" },
  "wiki:pages": { "href": "/pages", "title": "All pages", "deprecated": true, "deprecation": "Use wiki:v1:pages instead" }
}
```

HAL clients that understand deprecation will warn the agent. The `deprecation` string tells them what to use instead.

Lifecycle:
1. Introduce versioned relation (`wiki:v1:pages`)
2. Mark unversioned as deprecated (keep both for a transition period)
3. Remove deprecated relation entirely (clients following old links get no match)

For relation docs: serve full docs only for the versioned key. Return `410 Gone` for deprecated unversioned lookups, pointing to the versioned equivalent.
</deprecation>

<designing_for_distillation>
An API designed for distillation makes it easy for agents to record a workflow and export it as a deterministic spec. This means:

- **Stable relation names** — the spec references relations by name, so names must be stable across requests
- **Self-contained relation docs** — the JSON Schema in the docs becomes the contract in the exported spec
- **Consistent response shapes** — each relation should always return the same structure so the spec is predictable
- **Idempotent navigation** — following the same link from the same state should produce the same result

The exported spec looks like:
```json
[
  { "action": "start", "url": "/" },
  { "action": "follow", "relation": "wiki:v1:pages", "method": "GET" },
  { "action": "follow", "relation": "wiki:v1:create-page", "method": "POST",
    "input": {
      "bodySchema": { "type": "object", "properties": { "title": { "type": "string" }, "body": { "type": "string" } }, "required": ["title", "body"] },
      "body": { "title": "Example", "body": "Content" }
    }
  }
]
```

The `bodySchema` comes directly from your relation docs. If your docs include a clear JSON Schema, the agent preserves it in the export, and a runner can use it to validate inputs without any inference.
</designing_for_distillation>

<success_criteria>
A well-designed HAL API:
- Is fully navigable from the root through link-following alone
- Has CURIEs that expand every relation to a documentation URL
- Serves relation docs with Method, Input (JSON Schema), Example, and Response sections
- Uses versioned relation names (`myapi:v1:*`) rather than versioned URL paths
- Includes `title` on links for quick agent comprehension
- Returns embedded resource summaries with their own `self` links in collections
- Can be explored by an agent with no prior knowledge and distilled into a deterministic spec
</success_criteria>
