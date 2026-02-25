---
name: loom-nodejs
description: Develop BACKEND Node.js services, APIs, routes, and models for Link Loom. Handles database interactions, business logic, and server-side operations using `loom-sdk`.
license: Apache 2.0
author: Blackwood Stone Holdings, Inc.
compatibility: Requires Node.js v18+, Link Loom SDK
allowed-tools: Bash(git:*) Bash(jq:*) Read
---

# Link Loom Node.js Service Development Skill

This skill allows you to develop backend services for the Link Loom ecosystem, adhering to strict architectural, stylistic, and documentation standards.

## Table of Contents

1.  [Coding Standards](#1-coding-standards)
2.  [Architecture & Concepts](#2-architecture--concepts)
3.  [Naming Conventions](#3-naming-conventions)
4.  [Directory Structure](#4-directory-structure)
5.  [Component Guidelines](#5-component-guidelines)
    - [Models](#models)
    - [Services](#services)
    - [Routes](#routes)
6.  [Registration & Indexing](#6-registration--indexing)
7.  [General Best Practices](#7-general-best-practices)
8.  [Resources & Documentation](#8-resources--documentation)
9.  [Instructions](#9-instructions)
10. [Examples](#10-examples)
11. [Edge Cases](#11-edge-cases)

---

## 1. Coding Standards

### **Flat-Style & Defensive Coding (Critical)**

- **No Nested If-Else**: Avoid deep nesting.
- **Guard Clauses**: Validate inputs at the beginning of the function.
- **Negative Check First**: Check for failure conditions (missing params, falsy values) immediately and return errors.
- **Happy Path Last**: The successful execution logic should remain at the end of the function.

**Bad:**

```javascript
async myFunc(params) {
  if (params) {
    if (params.id) {
       // logic...
       return success;
    } else {
       return error;
    }
  } else {
    return error;
  }
}
```

**Good (Required):**

```javascript
async myFunc({ params }) {
  // 1. Defensive Checks
  if (!params) return this._utilities.io.response.error('Missing params');
  if (!params.id) return this._utilities.io.response.error('Missing ID');

  // 2. Logic
  const result = await this._doWork(params.id);

  // 3. Negative Check on Result
  if (!result) return this._utilities.io.response.error('Work failed');

  // 4. Happy Path Return
  return this._utilities.io.response.success(result);
}
```

---

## 2. Architecture & Concepts

### Domain Driven Design (DDD) parity

**CRITICAL**: The backend structure dictates the frontend structure.

- Ensure that modules are organized by domain (e.g., `workflow-orchestration/control-plane/...`).
- Changes in this structure must be reflected in the frontend to maintain 1:1 parity.

Understanding what to build is as important as how to build it.

| Concept      | Usage                                                                                                                                          |
| :----------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| **Service**  | **Default choice.** Contains business logic, database interactions, and complex operations. Extends `BaseModel` patterns usually.              |
| **Function** | Single-purpose, often stateless utility or cloud function logic (e.g., `timed`, `startup`). Do not make a Function if it manages entity state. |
| **App**      | A long-running app, self-contained module or mini-application logic.                                                                           |
| **Model**    | Data definition and schema. **Must** extend `BaseModel`.                                                                                       |

---

## 3. Naming Conventions

**Strictly** adhere to these naming conventions.

| Type        | File Pattern            | Class Name Pattern        | Example                                                                           |
| :---------- | :---------------------- | :------------------------ | :-------------------------------------------------------------------------------- |
| **Service** | `kebab-case.service.js` | `[Domain][Entity]Service` | `WorkflowOrchestrationFlowDefinitionService` (File: `flow-definition.service.js`) |
| **Route**   | `kebab-case.route.js`   | `[Domain][Entity]Route`   | `WorkflowOrchestrationFlowDefinitionRoute` (File: `flow-definition.route.js`)     |
| **Model**   | `kebab-case.model.js`   | `[Domain][Entity]Model`   | `WorkflowOrchestrationFlowDefinitionModel` (File: `flow-definition.model.js`)     |
| **Utility** | `kebab-case.util.js`    | `camelCase` (func)        | `dateFormatter`                                                                   |

**Rule**: Class names MUST be the concatenation of the Full Domain Path + Entity Name.

- Path: `src/models/workflow-orchestration/control-plane/flow-design/flow-definition/`
- Entity: `FlowDefinition`
- Class: `WorkflowOrchestrationFlowDefinitionModel`

**Rule**: Class names MUST be the concatenation of the Full Domain Path + Entity Name.

- Path: `src/models/workflow-orchestration/control-plane/flow-design/flow-definition/`
- Entity: `FlowDefinition`
- Class: `WorkflowOrchestrationFlowDefinitionModel`

---

## 4. Directory Structure

Place files in the correct location based on their responsibility.

```text
src/
├── routes/
│   ├── router.js                    # Main router aggregator
│   └── api/
│       └── <module-name>/
│           ├── <module>.routes.js   # Module-specific router (e.g., chat.routes.js)
│           └── <feature>.route.js   # Route handler class
├── services/
│   ├── index.js                     # Main service exporter
│   └── <module-name>/
│       └── <feature>.service.js     # Logic
├── models/
│   ├── index.js                     # Main model exporter
│   └── <model-name>.model.js        # Schema
```

---

## 5. Component Guidelines

### Models

- **Inheritance**: MUST extend `BaseModel` (from `@link-loom/sdk`).
- **Statuses**: `entityStatuses` MUST always include a `color` property (hex code) for UI consistency.
- **Structure**: Sub-models/Sub-entities MUST be placed in a `sub-entities/` folder within the model's directory.
- **Strict Definitions**: NO "black box" properties. All properties must be explicitly defined in `initializeEntityProperties`. This prepares for TypeScript migration.
- **Synchronization**: Every property MUST be present in 4 places:
  1.  **Class Declaration**: Top of the class (e.g., `name;`).
  2.  **Initialization**: Inside `initializeEntityProperties` (e.g., `this.name = ...`).
  3.  **Getter**: Inside `get get()` (e.g., `name: this.name?.value`).
  4.  **Swagger**: Inside `@swagger` definition.
- **No Redundant Props**: Do **not** define `id`, `created`, `modified`, or `status` manually. These are inherited.
- **Swagger**: MUST include full Swagger `@swagger` documentation for the schema.
- **Initialization**: Implement explicit `initializeEntityProperties(args)` method.
- **Getters**: Implement `sanitized` and `get` accessors.

### Services

- **Constructor Order**:
  1.  Base Properties (`dependencies`)
  2.  Custom Properties (private vars)
  3.  Assignments
- **Get Method**: Must use a `switch(params.queryselector)` to handle variants (`id`, `all`, etc.).
- **Private Methods**: Use private methods (`#getById`, `#getAll`) for specific logic, called by the main public methods.
- **Validation**: Every public method must start with input validation (defensive coding).

### Routes

- **Micro-Routers**: Do not add routes directly to `src/routes/router.js`. Add them to `src/routes/api/<module>/<module>.routes.js`, then import that file in the main router.
- **Classes**: Route handlers are classes.
- **Swagger**: Every route method must have full Swagger documentation defining inputs/outputs.
- **CRUD Mapping**: Typically map `get`, `create`, `update`, `delete` handlers, unless it is a command route (e.g., `execute`).

---

## 6. Registration & Indexing

- **Services**: Must be exported in `src/services/index.js`.
- **Models**: Must be exported in `src/models/index.js`.
- **Routes**: Must be defined in the module's `*.routes.js` file (e.g., `chat.routes.js`) using the standard configuration object (httpRoute, route, handler, method).

---

## 7. General Best Practices

- **Language**: **English ONLY** for code and static text, unless explicitly requested otherwise by the user.
- **Documentation**: Avoid excessive comments. Document only complex algorithms. Code should be self-documenting.
- **KISS Principle**: keep it simple, stupid. Avoid overengineering. If a process is simple, keep the code simple.
- **Naming**: Use semantic variable names. **NEVER** use single-letter names like `x`, `ac`, `t`. Names must indicate intent.
- **Clean Code**: Remove unused imports, dependencies, and functions. No dead code.
- **Git**: Use **Conventional Commits** if asked to generate commit messages.
- **Design Patterns**: Act as an experienced architect. Use patterns (Factory, Singleton, Proxy, etc) **only** when necessary to solve a specific problem. Do not force patterns where simple logic suffices.
- **Context**: Do not infer if unsure. Always ask the user for clarification if requirements are not clear. Challenge user requests that lead to "garbage code" or antipatterns.
- **Backend Specifics**:
  - **Reuse**: ALWAYS check `link-loom`/`loom-sdk` docs. Do not reinvent utilities or base classes that already exist.
  - **Model Awareness**: Understand existing backend models before creating any functionality to deeply understand the domain.
- **Strictness**: Since you are the expert, do not let the user start to write bad code patterns, warn him.
- **Linting**: **MANDATORY**. Code must be written adhering to the project's linter configuration (e.g., `.prettierrc`, `.eslintrc.js`).

---

## 8. Resources & Documentation

**CRITICAL**: Before inventing new utilities or patterns, check the local documentation.

- **Link Loom SDK Docs**: `link-loom/github/loom-sdk/docs`
  - **Core Utilities**: `link-loom/github/loom-sdk/docs/core/utilities.module.md`
  - **Infrastructure**: `link-loom/github/loom-sdk/docs/infrastructure/` (Email, Storage, Database)
  - **Data Types**: `link-loom/github/loom-sdk/docs/core/data-types.module.md`

Use `view_file` on these paths to understand available tools before coding.

---

## 9. Instructions

1.  **Read Context**: Before creating a file, check the `index.js` or `router.js` to see where it fits.
2.  **Use Assets**: Copy the base structure from the `assets/` templates.
3.  **Apply Standards**: Refactor the template code to match the "Flat-Style" and specific logic requirements (switch cases, defensive checks).
4.  **Document**: Add Swagger JSDoc immediately.
5.  **Register**: Update the corresponding `index.js` or `routes.js` file to register the new component.

---

## 10. Examples

### Service Implementation

See `assets/service.js`.

### Route Implementation

See `assets/route.js`.

### App Implementation

See `assets/app.js`.

### Model Implementation

See `assets/model.js`.

---

## 11. Edge Cases

- **Missing Organization ID**: Almost all create methods require `organization_id`. Fail if missing.
- **Transaction Safety**: If using database transactions, ensure errors are caught and logged properly before returning the error response.
- **Legacy Code**: If you see code that doesn't follow "Flat-Style", do not copy it. Upgrade it to the new standard.
