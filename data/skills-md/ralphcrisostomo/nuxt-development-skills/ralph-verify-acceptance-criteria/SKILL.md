---
name: ralph-verify-acceptance-criteria
description: "Verify Ralph user story implementations against acceptance criteria in prd.json. Use this skill whenever you need to verify a completed user story, test Ralph's implementation, check if acceptance criteria pass, validate admin dashboard features, or audit PRD completion status. Triggers on: verify story, check implementation, ralph verify, test acceptance criteria, validate prd, check user story, verify US-XXX, audit ralph progress, does this story pass."
model: opus
---

# Ralph Verify Acceptance Criteria Skill

Verify that a user story implementation satisfies every acceptance criterion in `scripts/ralph/prd.json`. Produces a structured pass/fail report and optionally updates the PRD.

## When to Use

- After Ralph completes a user story — verify before marking `passes: true`
- When the user asks to audit or re-verify existing implementations
- To check if a specific acceptance criterion is met
- To generate a verification report across all stories

## Workflow

### 1. Load the PRD

Read `scripts/ralph/prd.json` from the project root. Parse the `userStories` array.

If the user specifies a story ID (e.g., "verify US-005"), target that story. If no story is specified, find the highest-priority story where `passes: true` that hasn't been verified yet, or ask the user which story to verify.

### 2. Detect UI Story

Before classifying individual criteria, determine if this story involves UI. Scan the story title, description, and acceptance criteria for any of these signals:

- **UI keywords:** page, component, layout, modal, form, card, table, badge, button, tab, drawer, sidebar, header, nav, dialog, toast, skeleton, avatar, dropdown, menu, list, grid
- **File paths:** `.vue` files, `app/pages/`, `app/components/`, `app/layouts/`
- **Nuxt UI components:** UCard, UButton, UBadge, UTable, USkeleton, UModal, UInput, UForm, UDropdown, UTabs, UAvatar, etc.
- **Behavioral language:** renders, displays, shows, visible, clicks, navigates, responsive, mobile, dark mode, screenshot

If **any** signal matches, mark the story as a UI story. Browser verification is mandatory for UI stories — it cannot be skipped or deferred.

### 3. Classify Each Acceptance Criterion

For each acceptance criterion, determine the verification strategy:

| Pattern in criterion | Strategy | Tool |
|---|---|---|
| "Create file", "Add file" | **File exists** | Glob/Read |
| "middleware", "composable", "component", "page", "layout" | **File exists + content check** | Read + Grep |
| "Typecheck passes" | **Typecheck** | `bun run lint` via Bash |
| "tf:plan", "terraform", "Terraform module" | **Terraform plan** | `bun run tf:plan:staging` |
| "GraphQL schema", "Add query", "Add mutation", "Add type" | **Schema check** | Grep on `schema.graphql` |
| "resolver", "function module", "pipeline resolver" | **Terraform config check** | Grep on `main.tf` and `terraform/functions/` |
| "Wire up", "datasource" | **Terraform wiring** | Grep on `main.tf` |
| "UCard", "UButton", "UBadge", "USkeleton" etc. | **Component usage** | Grep in target Vue file |
| General behavior descriptions | **Code review** | Read the relevant file and verify logic |

Browser verification is not a per-criterion classification — it is driven by the UI story detection in Step 2.

### 4. Execute Verifications

Run checks in this order. Browser verification runs first because it catches the most impactful issues (broken renders, missing elements, runtime errors) that static checks miss.

#### A. Browser Verification (UI Stories)

Run this phase first for any story detected as UI in Step 2. Use the `/dev-browser` skill:

1. Start the dev server if not running: `bun run dev &`
2. Start the browser: `./skills/dev-browser/server.sh &`
3. **Auth setup:**
   - Regular pages: set `auth-role=user` cookie + `?dev-bypass` query param
   - Admin pages: use demo account (`.env` → `DEV_DEMO_EMAIL` / `DEV_DEMO_PASSWORD`)
4. Navigate to the target page
5. **Verify checklist:**
   - Page renders without console errors
   - Expected UI elements are visible (cards, tables, buttons, badges, forms)
   - Key interactions work (clicks, navigation, form submission)
   - Responsive layout if criteria mention mobile
6. Take screenshots as evidence

#### B. File Existence Checks
For criteria mentioning file creation, use Glob to confirm files exist. Read key files to verify they contain expected patterns (component names, function signatures, imports).

#### C. Code Content Checks
For behavioral criteria, Read the relevant source files and verify:
- Expected functions/methods exist
- Required imports or composable calls are present
- Correct patterns are used (e.g., `definePageMeta({ layout: 'admin', middleware: ['admin'] })`)
- GraphQL query strings are defined
- Resolver functions contain expected DynamoDB operations

#### D. GraphQL Schema Checks
For schema-related criteria, Grep `terraform/envs/staging/schema.graphql` for:
- Type definitions (`type AdminStats`)
- Query/mutation declarations (`getAdminStats`, `adminDeleteUser`)
- Field definitions with correct types
- Input arguments

#### E. Terraform Infrastructure Checks
For infrastructure criteria:
- Grep `terraform/envs/staging/main.tf` for module declarations
- Grep `terraform/envs/staging/lambda_function.tf` for Lambda resources
- Check `terraform/functions/` for resolver JS files
- Check `terraform/lambda/src/` for Lambda handler code
- If the user wants a full terraform validation, run `bun run tf:plan:staging` (requires AWS credentials)

#### F. TypeScript / Lint Check
For "Typecheck passes" criteria, run:
```bash
bun run lint 2>&1 | tail -20
```
Check exit code. If it fails, capture and report the errors.

### 5. Generate Verification Report

Output a structured report. Browser verification appears first to reflect execution priority:

```
## Verification Report: US-XXX — [Story Title]

### Acceptance Criteria Results

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Browser verification | PASS | Screenshot: page renders, elements visible |
| 2 | Create middleware file | PASS | File exists at `app/middleware/admin.ts` |
| 3 | Non-admin redirect | PASS | Line 8: `navigateTo('/')` with toast |
| 4 | Typecheck passes | PASS | `bun run lint` exit code 0 |

### Summary
- **Passed:** 4/4
- **Failed:** 0/4
- **Overall:** PASS
```

For failed criteria, include specific details about what's missing or incorrect, with file paths and line numbers.

### 6. Update PRD (Optional)

If all criteria pass and the user confirms, update `scripts/ralph/prd.json`: set `"passes": true` and add `"verifiedAt": "<ISO timestamp>"`. If any criteria fail, do NOT update — list remediation steps instead.

## Batch Verification Mode

When asked to "verify all stories" or "audit the PRD":

1. Load all stories from prd.json
2. Filter to stories where `passes: true` (already claimed complete)
3. Run verification on each story sequentially
4. Output a summary table:

```
| Story | Title | Claimed | Verified | Issues |
|-------|-------|---------|----------|--------|
| US-001 | Admin middleware | PASS | PASS | - |
| US-003 | Admin layout | PASS | FAIL | Missing mobile drawer test |
```

## Quick Check Mode

When the user says "quick verify" or "verify without browser", static checks (file existence, code patterns, schema, terraform, typecheck) run immediately. For UI stories, browser verification is marked as **DEFERRED** in the report — the story cannot be marked `passes: true` until browser verification completes. Run deferred browser checks later with "verify browser US-XXX".

## Key Project Paths

| Area | Path |
|---|---|
| Pages | `app/pages/` |
| Components | `app/components/` |
| Middleware | `app/middleware/` |
| Composables | `app/composables/` |
| Layouts | `app/layouts/` |
| GraphQL queries | `app/graphql/` |
| Schema | `terraform/envs/staging/schema.graphql` |
| Resolver functions | `terraform/functions/` |
| Lambda handlers | `terraform/lambda/src/` |
| Terraform config | `terraform/envs/staging/main.tf` |
| Lambda TF config | `terraform/envs/staging/lambda_function.tf` |
| Types / PRD | `types/`, `scripts/ralph/prd.json` |
