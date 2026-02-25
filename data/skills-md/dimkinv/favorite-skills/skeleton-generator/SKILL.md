---
name: skeleton-generator
description: Create minimal TypeScript project skeletons for backend (Node.js), React (Vite), or Next.js with deps, file tree, and AGENTS.md handling.
---

# Skeleton Generator

## Intake

- Confirm the request is to create a new project skeleton.
- If the project type is unclear, ask which type: backend (Node.js), frontend (React with Vite), or Next.js.
- Ask which package manager to use: npm or pnpm.
- Keep the output minimal: only the files needed to run, plus lint/format config and scripts.

## Global rules

- Use TypeScript for all project types.
- Include ESLint and Prettier config.
- Add scripts for dev, build, and run/start in package.json.
- Provide the exact dependency lists and the file tree that will be created.
- Copy the relevant AGENTS file from this skill folder to the project root as AGENTS.md.

## Backend (Node.js, TypeScript)

### Dependencies

Runtime deps: 
- zod
- dotenv

Dev deps:
- typescript
- tsx
- @types/node
- eslint
- @typescript-eslint/parser
- @typescript-eslint/eslint-plugin
- prettier
- eslint-config-prettier

### Scripts

- dev: tsx watch src/index.ts
- build: tsc -p tsconfig.json
- start: node dist/index.js
- lint: eslint .
- format: prettier . --check

### File tree

```
.
├── src/
│   └── index.ts
├── package.json
├── tsconfig.json
├── .gitignore
├── .eslintrc.cjs
├── .prettierrc.cjs
└── .eslintignore
```

### AGENTS

Copy assets/AGENTS-BACKEND.md to the project root as AGENTS.md.

### Gitignore

Add a Node.js TypeScript .gitignore (node_modules, dist, .env, and logs).

## Frontend (React with Vite, TypeScript)

### Dependencies

Runtime deps:
- react
- react-dom

Dev deps:
- typescript
- vite
- @vitejs/plugin-react
- @types/react
- @types/react-dom
- eslint
- @typescript-eslint/parser
- @typescript-eslint/eslint-plugin
- eslint-plugin-react
- eslint-plugin-react-hooks
- prettier
- eslint-config-prettier

### Scripts

- dev: vite
- build: tsc -p tsconfig.json && vite build
- preview: vite preview
- lint: eslint .
- format: prettier . --check

### File tree

```
.
├── src/
│   ├── main.tsx
│   └── App.tsx
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── .gitignore
├── .eslintrc.cjs
├── .prettierrc.cjs
└── .eslintignore
```

### AGENTS

Copy assets/AGENTS-REACT.md to the project root as AGENTS.md.

### Gitignore

Add a Vite React TypeScript .gitignore (node_modules, dist, and logs).

## Next.js (TypeScript)

### Dependencies

Runtime deps:
- next
- react
- react-dom

Dev deps:
- typescript
- @types/node
- @types/react
- @types/react-dom
- eslint
- eslint-config-next
- prettier
- eslint-config-prettier

### Scripts

- dev: next dev
- build: next build
- start: next start
- lint: next lint
- format: prettier . --check

### File tree

```
.
├── app/
│   └── page.tsx
├── package.json
├── tsconfig.json
├── next.config.mjs
├── .gitignore
├── .eslintrc.cjs
├── .prettierrc.cjs
└── .eslintignore
```

### AGENTS

Copy assets/AGENTS-NEXT.md to the project root as AGENTS.md.

### Gitignore

Add a Next.js TypeScript .gitignore (node_modules, .next, out, and logs).
