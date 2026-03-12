---
name: apix
description: Use `apix` to search, browse, and execute API endpoints from local markdown vaults. Use this skill to discover REST API endpoints, inspect request/response schemas, and make HTTP calls directly from the terminal without leaving your environment.
---

# apix — API Explorer for Agents

`apix` is a CLI tool for importing, browsing, searching, and calling API endpoint documents stored as local markdown vaults.

## Prerequisites & Installation

Before using `apix`, verify if it is installed:

```bash
apix --version
```

If it is not installed, install it using Homebrew (macOS/Linux):

```bash
brew tap apix-sh/tap
brew install apix
```

Or via the curl installer:

```bash
curl -fsSL https://apix.sh/install | sh
```

## Agent Workflow Guidelines

When an API task is requested, follow this general workflow:

1. **Discover**: Find the relevant endpoint route.

   ```bash
   apix search "create pet"
   # Or list available APIs: apix ls
   ```

2. **Inspect**: Check the endpoint parameters and schema concisely to save your context window.

   ```bash
   apix peek petstore/v1/pets/{petId}/GET
   ```

   _Note: Only use `apix show <route>` if you need the full, detailed documentation, as it can be long._

3. **Execute**: Make the HTTP call using the route you found.
   ```bash
   apix call demo/v1/items/{id}/POST -p id=item_123 -d '{"name":"item"}'
   ```

## Core Commands

### Search & Discovery

- **Search across all indexed APIs**: `apix search <query>`
- **List namespaces**: `apix ls`
- **List endpoints in a namespace**: `apix ls <namespace>/<version>` (e.g., `apix ls petstore/v1`)
- **Full-text search within a namespace**: `apix grep <namespace> <query>`

### Inspecting Endpoints

Routes follow the format: `<namespace>/<version>/<path segments>/<METHOD>` (e.g., `petstore/v1/pets/GET`).

- **Peek (Recommended for Agents)**: `apix peek <route>` — Outputs the YAML frontmatter and condensed required input fields.
- **Show**: `apix show <route>` — Outputs the full markdown documentation for the route or type.

### Executing HTTP Calls

`apix call` automatically resolves the URL, method, and auth requirements from the route's markdown frontmatter.

- **Basic call with a literal path segment**:

  ```bash
  apix call demo/v1/items/item_123/GET
  ```

  _(apix automatically maps `item_123` to the `{id}` parameter if the defined route is `demo/v1/items/{id}/GET`)_

- **Explicit parameters**:

  ```bash
  apix call demo/v1/items/{id}/POST \
    -p id=item_123 \
    -q expand=full \
    -H "Authorization: Bearer <token>" \
    -d '{"name":"item"}'
  ```

  - `-p <key>=<value>`: Path parameter
  - `-q <key>=<value>`: Query parameter
  - `-H "<Header>: <Value>"`: HTTP Header
  - `-d '<data>'` or `-d @file.json`: Request body

### Importing Custom Specs

If the required API is not in the public registry, you can import an OpenAPI 3.x spec locally:

```bash
apix import /path/to/openapi.json --name myapi
```

## Notes for Agents

- When you execute `apix` commands via the shell, it detects that stdout is piped and will automatically emit **raw markdown**, which is perfectly structured for you to read.
- `apix` routes are standard strings. If a route matches multiple sources, `apix` will throw an ambiguity error. In that case, prefix the route with the source (e.g., `core/petstore/v1/pets/GET`).
- Prioritize `peek` over `show` to avoid flooding your context window with redundant schemas.
