---
name: api-doc-generator
description: This skill should be used when the user asks to "generate API docs", "create API documentation", "generate curl examples", "create developer docs", or mentions generating documentation, curl examples, or developer guides from OpenAPI/OAS specifications.
metadata: 
  version: 1.0.0
  author: "Mariano de Achaval"
---

# API Doc Generator

Generates markdown documentation from your OpenAPI Specification, creating multiple pages with curl command examples for each endpoint.

## When to Use This Skill

Use this skill when:
- You need to create developer documentation from your API spec
- You want to provide curl examples for each endpoint
- You need human-readable documentation separate from the OAS file
- You're building a documentation website or wiki

## Prerequisites

```bash
pip install pyyaml
```

## Running Documentation Generator

```bash
python3 skills/api-doc-generator/scripts/generate_docs.py path/to/spec.yaml [output-dir]
```

Default output directory is `./docs` if not specified.

## What Gets Generated

The tool creates:

1. **README.md** (Overview page):
   - API title, version, and description
   - List of base URLs/servers
   - Table of contents organized by tags
   - Links to all endpoint pages

2. **Individual endpoint pages** (one per operation):
   - HTTP method and path
   - Description and summary
   - Parameters table (path, query, header)
   - Request body details
   - **Curl command examples** with realistic values
   - Response examples with status codes
   - Response codes table

## Example

```bash
# Generate docs to default ./docs directory
python3 skills/api-doc-generator/scripts/generate_docs.py api-spec.yaml

# Generate docs to custom directory
python3 skills/api-doc-generator/scripts/generate_docs.py api-spec.yaml ./documentation
```

**Output:**
```
Generating API documentation from api-spec.yaml...

Generating overview page: README.md
Generating endpoint page: createUser.md
Generating endpoint page: getUserById.md
Generating endpoint page: listOrders.md

✓ Generated documentation for 3 endpoints
✓ Output directory: ./docs

View the documentation:
  - Overview: ./docs/README.md
```

## Curl Examples

The tool automatically generates curl commands with:
- Correct HTTP method
- Base URL from servers configuration
- Path parameters replaced with example values
- Query parameters included
- Headers included
- Request body with proper JSON formatting
- Multiple examples if the spec provides them

**Example generated curl command:**
```bash
curl -X POST "https://api.example.com/users" \
  -H "Content-Type: application/json" \
  -d '{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "age": 28,
  "role": "developer"
}'
```

## Organizing Documentation

The generated documentation can be:
- Committed to your repository in a `docs/` folder
- Published to GitHub Pages or similar
- Imported into a wiki or documentation platform
- Shared with API consumers as standalone files

Each endpoint gets its own file, making it easy to:
- Link directly to specific endpoints
- Update individual endpoints without touching others
- Organize in folders by tag/category if needed

## Using with Claude

Ask Claude to generate documentation:

```
"Generate markdown documentation from my API spec at path/to/spec.yaml"
"Create API docs with curl examples from specs/my-api.yaml"
"Generate developer documentation for my OpenAPI spec"
```

## Related Skills

- **api-spec-validator** - Validate OAS specs against AI-agent-friendly rules
- **api-schema-inferrer** - Infer and generate schemas from examples in OAS specs
