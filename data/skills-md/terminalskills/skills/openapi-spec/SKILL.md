---
name: openapi-spec
description: >-
  OpenAPI is the standard format for describing HTTP APIs in YAML or JSON, from which docs, typed clients and mock servers can be generated. Use this skill to write an OpenAPI 3.1 spec, lint it with Redocly CLI, generate TypeScript types and a typed fetch client, build HTML docs, and keep a spec valid. Use when someone says "write an OpenAPI spec", "document my REST API", "generate a client from openapi.yaml" or "lint my swagger file".
license: Apache-2.0
compatibility: 'Node.js 20.19+ or 22.12+ for the Redocly CLI (2.x), Node.js 20+ for openapi-typescript; spec is language-agnostic'
metadata:
  author: terminal-skills
  version: 1.1.0
  category: development
  repository: https://github.com/OAI/OpenAPI-Specification
  tags: "openapi, swagger, api-design, documentation, rest"
---

# OpenAPI Specification

## Overview

An OpenAPI document describes an HTTP API: paths, operations, parameters, request and response bodies, and security. This skill targets OpenAPI 3.1 (JSON Schema 2020-12 compatible). Versions 3.2.0 and 3.2.1 also exist; 3.1 is still the version most tooling supports fully, so check your tools before moving. Design-first means the spec is written and reviewed before code, and later drives docs, SDKs and contract tests.

Tool versions checked in October 2026: `@redocly/cli` 2.71, `openapi-typescript` 7.13, `openapi-fetch` 0.17.

## Instructions

### Step 1: Write the spec
Save as `openapi.yaml`. Notes on what the example does:
- `security` at the root applies to every operation; the two public GET operations opt out with `security: []`.
- In 3.1, "may be null" is written `type: [string, 'null']`. The 3.0 keyword `nullable: true` is invalid in 3.1 and Redocly rejects it.
- `examples` (a list) replaces the old singular `example` on schemas.
- Every operation has at least one 4XX response, and shared errors live in `components/responses`.

```yaml
openapi: 3.1.0
info:
  title: Project Management API
  version: 1.0.0
  description: API for managing projects and tasks
  license:
    name: Apache-2.0
    identifier: Apache-2.0

servers:
  - url: https://api.acmeprojects.dev/v1
    description: Production

security:
  - bearerAuth: []

paths:
  /projects:
    get:
      summary: List projects
      operationId: listProjects
      tags: [Projects]
      security: []
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [active, archived, all]
            default: active
        - name: limit
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: cursor
          in: query
          description: Pagination cursor from the previous response
          schema:
            type: string
      responses:
        '200':
          description: List of projects
          content:
            application/json:
              schema:
                type: object
                required: [data, nextCursor]
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Project'
                  nextCursor:
                    type: [string, 'null']
        '400':
          $ref: '#/components/responses/ValidationError'

    post:
      summary: Create a project
      operationId: createProject
      tags: [Projects]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateProjectInput'
      responses:
        '201':
          description: Project created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Project'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '422':
          $ref: '#/components/responses/ValidationError'

  /projects/{projectId}:
    get:
      summary: Get a project by ID
      operationId: getProject
      tags: [Projects]
      security: []
      parameters:
        - name: projectId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Project details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Project'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    Project:
      type: object
      required: [id, name, status, createdAt]
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
          examples: ["Website Redesign"]
        description:
          type: [string, 'null']
        status:
          type: string
          enum: [active, archived]
        taskCount:
          type: integer
        createdAt:
          type: string
          format: date-time

    CreateProjectInput:
      type: object
      required: [name]
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        description:
          type: string
          maxLength: 500

    Error:
      type: object
      required: [error]
      properties:
        error:
          type: string
        details:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
              message:
                type: string

  responses:
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    ValidationError:
      description: Validation error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Unauthorized:
      description: Missing or invalid bearer token
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### Step 2: Lint

```bash
npx @redocly/cli lint openapi.yaml
```

Exit code is non-zero on errors, so this works as a CI gate. Rules are configured in `redocly.yaml` (`extends: [recommended]`, then per-rule `error`/`warn`/`off`). Redocly CLI 2.x no longer has `preview-docs`; build static docs instead:

```bash
npx @redocly/cli build-docs openapi.yaml -o docs/index.html
```

For specs split over several files, `npx @redocly/cli bundle openapi.yaml -o dist/openapi.yaml` resolves all `$ref`s into one file.

### Step 3: Generate TypeScript types and a typed client

```bash
npm install --save-dev openapi-typescript typescript
npm install openapi-fetch
npx openapi-typescript openapi.yaml -o src/api/schema.d.ts
```

```typescript
import createClient from "openapi-fetch";
import type { paths, components } from "./schema";

type Project = components["schemas"]["Project"];

const client = createClient<paths>({ baseUrl: "https://api.acmeprojects.dev/v1" });

const { data, error } = await client.GET("/projects", {
  params: { query: { status: "active", limit: 20 } },
});
if (error) throw new Error(error.error);          // typed as the Error schema
const projects: Project[] = data.data;

const created = await client.POST("/projects", {
  body: { name: "Website Redesign" },
  headers: { Authorization: `Bearer ${process.env.PROJECTS_API_TOKEN}` },
});
```

Path, query and body types are checked at compile time against the spec; rerun `openapi-typescript` whenever it changes. Add `--check` in CI to fail if the committed file is stale.

## Examples

### Example 1: "Add an endpoint to archive a project"
Add `/projects/{projectId}/archive` with `post`, `operationId: archiveProject`, path parameter `projectId`, a `200` returning `Project`, plus `401` and `404` via `$ref`. Run `npx @redocly/cli lint openapi.yaml`; the output ends with `Woohoo! Your API description is valid.` Regenerate types and `client.POST("/projects/{projectId}/archive", { params: { path: { projectId } } })` becomes available.

### Example 2: "The linter says `Property nullable is not expected here`"
The spec declares `openapi: 3.1.0` but uses 3.0 syntax. Replace `type: string` + `nullable: true` with `type: [string, 'null']`, and `example:` with `examples: [...]`. Re-run lint; the errors disappear.

## Guidelines

- Design-first: agree the spec in review before implementing; it is cheaper to change YAML than code.
- Give every operation a unique `operationId`; generators use it for method names.
- Reuse with `$ref` for schemas, error responses and parameters.
- Declare security once at the root and opt out per operation, so a new endpoint is protected by default.
- Match the `openapi:` version to the syntax you use (3.0 and 3.1 differ in nullability, `exclusiveMinimum`, `example` and `webhooks`).
- Version breaking changes in the URL (`/v1`) and keep `info.version` for the spec's own revisions; diff specs in CI before releasing.
- Treat example values in the spec as public documentation: no real tokens or customer data.
