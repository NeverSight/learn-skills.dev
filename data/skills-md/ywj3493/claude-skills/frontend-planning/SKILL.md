---
name: frontend-planning
description: Generates a 6-step frontend planning document pipeline (requirements → user flows → page spec → use cases → component tree → state/API integration) into docs/en/specifications/<domain>/, with domain analysis, tech stack detection, and user review gates at each step.
---

# frontend-planning

6-step planning document pipeline for frontend projects, organized by domain.

## When to Use

- User says "프론트엔드 기획", "frontend planning", "UI 설계", "화면 설계"
- User says "프론트엔드 문서", "기획 문서 만들어줘", "plan frontend"
- Starting a new frontend project that needs structured design documents
- Adding a major frontend feature that requires multi-page planning

## When NOT to Use

- Backend-only projects (use the backend planning pipeline instead)
- Fixing a single component or small UI tweak
- Editing or updating existing specification documents
- Non-UI work such as CI/CD, infrastructure, or tooling

## Pipeline Overview

```text
Step 0:   Tech stack detection
Step 0.5: Domain analysis & document discovery
Step 1:   Requirements
Step 2:   User Flows
Step 3:   Page Spec
Step 4:   Use Cases
Step 5:   Component Tree
Step 6:   State & API Integration
Step 7:   README (table of contents)
```

For multi-domain projects, Steps 1–6 are completed for each domain before
moving to the next. Step 7 runs once at the end to generate the index.

## Output Structure

```text
docs/en/specifications/
├── architecture.md              # Project folder structure (created by init-docs)
├── config.md                    # Environment variables (created by init-docs)
├── infrastructure.md            # Infrastructure description (created by init-docs)
├── README.md                    # Index of all domains/documents (Step 7)
├── <domain-a>/
│   ├── requirements/
│   │   └── requirements.md      # Step 1
│   └── workflows/
│       ├── user-flows.md        # Step 2
│       ├── page-spec.md         # Step 3
│       ├── use-cases.md         # Step 4
│       ├── component-tree.md    # Step 5
│       └── state-api-integration.md  # Step 6
└── <domain-b>/
    ├── requirements/
    └── workflows/
```

## Step-by-Step Instructions

### Step 0: Detect Tech Stack

Before generating any documents, detect the project's tech stack:

1. Read `package.json` — check for React, Vue, Next.js, Nuxt, Svelte, Angular, etc.
2. Read `tsconfig.json` — check if TypeScript is used
3. Scan directory structure — `src/`, `app/`, `pages/`, `components/`
4. Check for styling solutions — Tailwind, styled-components, CSS Modules, etc.
5. Check for state management — Redux, Zustand, Recoil, Pinia, etc.

Summarize the detected stack and confirm with the user:

> **Detected tech stack:**
> - Framework: Next.js 14 (App Router)
> - Language: TypeScript
> - Styling: Tailwind CSS
> - State: Zustand
>
> I'll generate planning documents based on this stack. Does this look correct?

Wait for confirmation before proceeding.

### Step 0.5: Domain Analysis & Document Discovery

After confirming the tech stack, identify the project's domain structure and discover existing documents:

**Domain Analysis**

1. Ask the user to describe the project's major feature areas
2. Propose domain groupings based on their description (e.g., `auth`, `payment`, `dashboard`)
3. Always create at least one domain directory — even single-domain projects use `specifications/<domain>/`
4. Present the proposed directory structure for confirmation:

> **Proposed domain structure:**
>
> ```
> docs/en/specifications/
> ├── auth/
> │   ├── requirements/
> │   └── workflows/
> └── dashboard/
>     ├── requirements/
>     └── workflows/
> ```
>
> I'll generate the 6 planning documents for each domain in sequence.
> Shall I proceed with this structure?

5. Store the confirmed domain list for subsequent steps

Wait for confirmation before proceeding. If the user requests changes to the
domain groupings, adjust and re-confirm.

**Document Discovery**

6. **Entry point scan** — read `README.md`, `CLAUDE.md`, `docs/en/specifications/README.md` if they exist
7. **Recursive directory scan** — list all `.md` files under `docs/en/specifications/` (including subdirectories) and `docs/en/policy/`
8. **Document classification** — read the first 30 lines of each discovered file and classify by type:
   `requirements` / `user-stories` / `use-cases` / `api-spec` / `sequence-diagram` /
   `architecture` / `config` / `infrastructure` / `deployment` / `policy` / `other`
9. **User confirmation** — present discovered documents grouped by category using `@`-reference format:

> **Discovered project documents:**
>
> **requirements**
> - [@docs/en/specifications/auth/requirements/requirements.md](docs/en/specifications/auth/requirements/requirements.md)
>
> **api-spec**
> - [@docs/en/specifications/auth/workflows/state-api-integration.md](docs/en/specifications/auth/workflows/state-api-integration.md)
>
> **policy**
> - [@docs/en/policy/naming-conventions.md](docs/en/policy/naming-conventions.md)
>
> Should I use these documents as reference material for the planning pipeline?

10. Carry the confirmed document list as context for all subsequent steps

If no documents are found, record "No project documents found" and proceed.

### Step 1: Requirements

**Output**: `docs/en/specifications/<domain>/requirements/requirements.md`

1. Load the reference template: `references/requirements-template.md`
2. From document discovery results, load all documents classified as `requirements`, `user-stories`, or `architecture` — use them as reference context
3. Ask the user to describe:
   - Project purpose and target users
   - Core features and functionality
   - Non-functional requirements (performance, accessibility, etc.)
4. Generate the document following the template structure
5. Present the document to the user and wait for review

> **Step 1/6 complete**: Requirements document generated.
> Please review and let me know if any changes are needed. Ready to proceed to the next step?

### Step 2: User Flows

**Output**: `docs/en/specifications/<domain>/workflows/user-flows.md`

1. Load the reference template: `references/user-flows-template.md`
2. Load Step 1 output: `<domain>/requirements/requirements.md`
3. From document discovery results, load all documents classified as `use-cases` or `sequence-diagram` — reference existing flows if present
4. For each major feature, create:
   - **Mermaid flowchart** diagram showing the happy path
   - Alternative paths and error/exception flows
   - Entry and exit conditions
5. Generate the document and wait for review

> **Step 2/6 complete**: User flows document generated.
> Please review and let me know if any changes are needed. Ready to proceed?

### Step 3: Page Spec

**Output**: `docs/en/specifications/<domain>/workflows/page-spec.md`

1. Load the reference template: `references/page-spec-template.md`
2. Load previous outputs: Steps 1–2
3. From document discovery results, skim documents classified as `api-spec` or `architecture` — reference any relevant layout or routing information
4. For each page/screen, define:
   - URL / route path
   - Layout structure and sections
   - Key components on the page
   - Responsive behavior (mobile / tablet / desktop)
   - SEO considerations (title, meta, OG tags)
5. Generate the document and wait for review

> **Step 3/6 complete**: Page specification generated.
> Please review and let me know if any changes are needed. Ready to proceed?

### Step 4: Use Cases

**Output**: `docs/en/specifications/<domain>/workflows/use-cases.md`

1. Load the reference template: `references/use-cases-template.md`
2. Load previous outputs: Steps 1–3
3. From document discovery results, load all documents classified as `use-cases` — reference existing actor definitions and flows; also load `architecture` documents for backend interaction mapping
4. For each use case, define:
   - Actor (user role)
   - Preconditions and postconditions
   - Main flow (step-by-step actor-system interaction)
   - Alternative flows
   - Exception flows
5. Generate the document and wait for review

> **Step 4/6 complete**: Use cases document generated.
> Please review and let me know if any changes are needed. Ready to proceed?

### Step 5: Component Tree

**Output**: `docs/en/specifications/<domain>/workflows/component-tree.md`

1. Load the reference template: `references/component-tree-template.md`
2. Load previous outputs: Steps 1–4
3. Define the component hierarchy:
   - **Mermaid graph TD** diagram showing parent-child relationships
   - Separate sections for shared/common components and page-specific components
   - **TypeScript interface** for each component's props
4. Generate the document and wait for review

> **Step 5/6 complete**: Component tree document generated.
> Please review and let me know if any changes are needed. Ready to proceed?

### Step 6: State & API Integration

**Output**: `docs/en/specifications/<domain>/workflows/state-api-integration.md`

1. Load the reference template: `references/state-api-integration-template.md`
2. Load previous outputs: Steps 1–5
3. From document discovery results, load all documents classified as `api-spec` — extract endpoint definitions and use them as the authoritative source for the API table; add a **Source** column to track which discovered document each endpoint originates from
4. Define:
   - State management strategy and rationale
   - **TypeScript interface** for each store/slice
   - API endpoints table with method, path, description
   - **TypeScript interface** for request/response DTOs
   - Caching strategy and error handling patterns
5. Generate the document and wait for review

> **Step 6/6 complete**: State & API integration document generated.
> Please review and let me know if any changes are needed.

### Step 7: Generate README

**Output**: `docs/en/specifications/README.md`

After all domains have completed Steps 1–6, generate a table of contents.

For single-domain projects:

```markdown
# Specifications

## Domains

### <domain>

| Document | Path | Description |
|----------|------|-------------|
| Requirements | [requirements.md](<domain>/requirements/requirements.md) | Feature requirements and constraints |
| User Flows | [user-flows.md](<domain>/workflows/user-flows.md) | User interaction flows with Mermaid diagrams |
| Page Spec | [page-spec.md](<domain>/workflows/page-spec.md) | Page layouts, routes, and responsive behavior |
| Use Cases | [use-cases.md](<domain>/workflows/use-cases.md) | Actor-system interactions |
| Component Tree | [component-tree.md](<domain>/workflows/component-tree.md) | Component hierarchy and props |
| State & API | [state-api-integration.md](<domain>/workflows/state-api-integration.md) | State management and API integration |
```

For multi-domain projects, list each domain in a separate section. Also generate
a per-domain `README.md` at `<domain>/README.md` if there are 2+ domains.

If `docs/en/specifications/README.md` already exists, merge the frontend
planning section rather than overwriting.

If document discovery found any project documents, add a **Related Project Documents**
section at the end of the README listing all discovered documents using `@`-reference format,
grouped by category.

Report completion:

> **Frontend planning complete.** Generated documents for all domains:
> - `docs/en/specifications/<domain>/requirements/requirements.md`
> - `docs/en/specifications/<domain>/workflows/user-flows.md`
> - `docs/en/specifications/<domain>/workflows/page-spec.md`
> - `docs/en/specifications/<domain>/workflows/use-cases.md`
> - `docs/en/specifications/<domain>/workflows/component-tree.md`
> - `docs/en/specifications/<domain>/workflows/state-api-integration.md`
> - `docs/en/specifications/README.md`

## Document Rules

- **Language**: English
- **Meta block**: Every document includes Created date, Last Modified date, Status (Draft/Review/Final), Tech Stack, and Prerequisites
- **Mermaid**: Use `flowchart TD` for user flows, `graph TD` for component trees
- **TypeScript**: Use `interface` declarations for props, store shapes, and API DTOs
- **References**: Each step must load all previous step outputs before generating
- **Review gate**: Never proceed to the next step without user approval

## Document Discovery Rules

- **Scan targets**: `README.md`, `CLAUDE.md`, all `.md` files under `docs/en/specifications/` (recursive) and `docs/en/policy/`
- **Classification types**: `requirements`, `user-stories`, `use-cases`, `api-spec`, `sequence-diagram`, `architecture`, `config`, `infrastructure`, `deployment`, `policy`, `other`
- **Classification method**: Read the first 30 lines of each file and classify based on content, headings, and filename
- **Reference format**: Use `@`-reference links for all discovered documents per [@docs/en/policy/reference-convention.md](docs/en/policy/reference-convention.md)
- **docs/reference/ exclusion**: Never apply `@`-prefix to files in `docs/reference/` — cite them with standard backtick paths only
- **No-documents fallback**: If no project documents are found, record "No project documents found" and proceed without references
- **Carry forward**: The confirmed document list from Step 0.5 must be available as context to every subsequent step
