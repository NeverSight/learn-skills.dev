---
name: generate-api-collection
type: atomic
license: MIT
description: >
  Use when creating or updating a REST API collection for Rails endpoints.
  Do not use for GraphQL. Trigger words: Postman, API collection, endpoint,
  API route, request collection.
metadata:
  version: 1.0.0
  user-invocable: "true"
---

# Generate API Collection


**Core principle:** Every API surface (Rails app or engine) has a single API collection file that stays in sync with its endpoints.

## Rules at a Glance

| Aspect | Rule |
|--------|------|
| When | Create or update collection when creating or modifying any REST API endpoint (route + controller action) |
| Format | Postman Collection JSON v2.1 (`schema` or `info.schema` references v2.1) |
| Location | One file per app or engine — `docs/api-collections/<app-or-engine-name>.json` or `spec/fixtures/api-collections/`; if a collection folder already exists, update the existing file |
| Language | All request names, descriptions, and variable names must be in **English** |
| Variables | Use `{{base_url}}` for the base URL so the collection works across environments |
| Per request | method, URL, headers, body, **description**, and **test scripts** (e.g. `pm.response.to.have.status(200)`) |
| Folders | Group related endpoints into folders using nested `item` arrays |
| Exception | GraphQL endpoints — use **implement-graphql** instead |

## HARD-GATE

```text
When you create or modify a REST API endpoint (new or changed route and controller action),
you MUST also create or update the corresponding API collection file so the
flow can be tested. Do not leave the collection missing or outdated.

Each request MUST include a description and at least one basic test script (e.g. status code check).

EXCEPTION: GraphQL endpoints — use implement-graphql instead.
```

## Core Process

1. Create or open the corresponding API collection JSON file.
2. Group related endpoints into folders using nested `item` arrays.
3. Use `{{base_url}}` for the base URL.
4. Add method, URL, headers, body, description, and test scripts for each request.
5. Validate the JSON is syntactically correct:
   - Run `python -m json.tool collection.json` or `jq . collection.json` — both print errors on invalid JSON.
   - If invalid: fix the reported error, then re-run the command until it exits cleanly.
6. Verify the collection can be imported into a compatible API client (e.g. Postman) without errors.
7. Confirm all new or changed endpoints are represented and that `{{base_url}}` is used consistently.

## Collection Structure (Postman v2.1)

Ensure the collection includes the `info` block, folders (nested `item` arrays), and `event` scripts:

```json
{
  "info": {
    "name": "Products API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Products",
      "item": [
        {
          "name": "List products",
          "request": {
            "method": "GET",
            "header": [],
            "url": "{{base_url}}/api/v1/products",
            "description": "Returns a list of all products in the catalog."
          },
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": ["pm.test('Status code is 200', () => { pm.response.to.have.status(200); });"],
                "type": "text/javascript"
              }
            }
          ]
        }
      ]
    }
  ],
  "variable": [
    { "key": "base_url", "value": "http://localhost:3000" }
  ]
}
```

## Common Mistakes

| Mistake | Reality |
|---------|----------|
| Missing Content-Type or body for POST/PUT | Include headers and example body so the request works out of the box |
| Skipping validation after generation | Run `jq .` or `python -m json.tool` and fix any errors before committing (see HARD-GATE) |

## Extended Resources

Load only when a concrete collection example is needed:

- [EXAMPLES.md](./EXAMPLES.md) — Postman v2.1 multi-endpoint collection example.

## Integration

| Skill | When to chain |
|-------|---------------|
| **create-engine** | When the engine exposes HTTP endpoints |
| **version-api** | When a new version requires a collection update |
