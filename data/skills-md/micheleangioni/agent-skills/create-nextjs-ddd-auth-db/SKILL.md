---
name: create-nextjs-ddd-auth-db
description: Create a new fullstack Next.js. Use this skill when the user asks to create a new Next.js project or application.
---

# Objective

Create a brand new Next.js app that satisfies all requested architecture and feature requirements. It includes App Router API endpoints, frontend pages, DDD structure, database integration, Google authentication with better-auth, tests, and linter. Keep the skill itself code-free: generate application code only inside the user-selected target folder.

# Required Workflow

Follow this sequence exactly.

## 1) Ask Initial Questions First

Ask the user:

1. App name
2. Folder where the new app should be created
3. Database to use
4. Library to manage that database. When the user is unsure about the library, propose:
- MongoDB: `mongoose`
- DynamoDB: `dynamoose`
- SQL dialects: `prisma`
5. Whether Jest or Vitest should be used as testing library
6. Whether ESLint or Oxlint should be used as linting library

Confirm the final choices before continuing.

## 2) Present Plan Before Implementation

Create a concrete implementation plan and present it to the user before changing files. Wait for explicit approval.

The plan must include:

- Discovery confirmation
- Version research and documentation review
- Scaffolding
- `instrumentation.ts` file setup to:
  - Log the node version, next.js version and NODE_ENV variable at startup
  - To validate the environment variables and log any critical missing ones at startup
  - To initializate the database connection and log success or failure
  - To log the server startup completion
- Tactical DDD folder setup
- Feature implementation
- Tests
- Linting setup, and Typescript configured in strict mode
- Documentation updates
- Final validation

## 3) Research Latest Versions and Official Docs

Before any installation, verify latest stable versions and usage from official sources:

- Next.js docs: [https://nextjs.org/docs](https://nextjs.org/docs)
- Next.js installation guide: [https://nextjs.org/docs/app/getting-started/installation](https://nextjs.org/docs/app/getting-started/installation)
- better-auth docs
- Chosen database library docs
- Chosen testing library docs (Jest or Vitest)
- Chosen linter library docs (ESLint or Oxlint)

Use the latest stable versions available at execution time. Do not assume versions from memory.

## 4) Scaffold the App with Latest Next.js Features

Create the app in the chosen folder with the chosen name and latest Next.js setup. Use current recommended options from Next.js docs, including App Router and `src/` structure.

Install and configure:

- `better-auth` (Google Auth)
- Selected testing library
- Selected linter library
- Selected database library and required driver packages

## 5) Implement Required Tactical DDD Structure

Create the following structure:

- `<app_name>/src/__tests__`
- `<app_name>/src/app`
- `<app_name>/src/app/api`
- `<app_name>/src/application`
- `<app_name>/src/domain`
- `<app_name>/src/infrastructure`
- `<app_name>/src/shared`
- `<app_name>/src/shared/logger`
- `<app_name>/docs`

## 6) Implement Required Features

Implement all of the following:

- Database connection under `src/infrastructure`, aligned with the selected database and library
- Example `User` entity in domain layer
- `User` repository abstraction + implementation
- Application service for user retrieval
- `GET /users` endpoint in App Router under `src/app/api`
- Homepage page with a Google Auth button powered by better-auth
- Tests for domain/application/infrastructure/API behavior under `src/__tests__`

## 7) Environment and Documentation

Create:

- `.env.example` with every required variable (app URL, auth values, Google OAuth credentials, DB settings, and anything else needed)
- `docs/endpoints.yaml` listing available endpoints with method, path, purpose, and auth requirements in OpenAPI format

Update the app's `README.md` with setup, environment, run, test, lint, and endpoint usage instructions.

## 8) Validate and Iterate Until Complete

Run lint and tests. Fix failures and re-run until passing.

Verify:

- App starts correctly
- Homepage renders and auth button is present
- `/users` endpoint works
- Required structure and docs exist

If any requirement is unmet, iterate until complete.

# Non-Negotiable Constraints

- Keep all packages on latest stable versions at run time.
- Do not embed generated app code in the skill itself.
- Do not stop after scaffolding; continue until all requirements are satisfied and validated.
