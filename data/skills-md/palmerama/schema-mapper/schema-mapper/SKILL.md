---
name: schema-mapper
description: Set up, configure, and update Schema Mapper — a visual Sanity org/schema explorer using App SDK and React Flow.
---

# Schema Mapper

Visual Sanity org/schema explorer. A Sanity App SDK app using React Flow. Shows projects, datasets, and document types as nodes, references as edges. Connects to the Sanity API, discovers all projects in an org, samples documents to infer schemas, and renders an interactive node graph.

## Setup

Follow these steps when a user says "install schema mapper" or "set up schema mapper".

### 1. Check for Studio in root

Before choosing an install location, check if the user's project root contains a Sanity Studio (`sanity.cli.ts` and `sanity.config.ts` in the root directory).

If a Studio is in the root:

> ⚠️ **Schema Mapper is a separate Sanity App SDK app — it can't run inside a Studio project.** The Sanity CLI can only detect one app per directory, so having both a Studio and an App SDK app in the same root won't work (the CLI will try to run the Studio instead of Schema Mapper).
>
> The fix is simple: move your Studio into a `/studio` subfolder and put Schema Mapper in `/apps/schema-mapper` alongside it. This makes **zero difference** to how your Studio works — you can still run it with `cd studio && npx sanity dev` and deploy with `cd studio && npx sanity deploy`. Everything stays exactly the same, it's just in a subfolder.

Offer to do this for the user:
1. Create a `studio/` folder
2. Move all Studio files into it (sanity.cli.ts, sanity.config.ts, schemas/, src/, etc.)
3. Create `apps/schema-mapper` for Schema Mapper
4. If there's a `pnpm-workspace.yaml` or similar, leave it in the root — don't add `packages:` entries, each app runs independently

If the user declines, warn them that Schema Mapper probably won't work from the same root as the Studio.

### 2. Check Studio version

Check the user's installed Sanity version:

```bash
npx sanity --version
```

Or check `package.json` for the `sanity` dependency version.

Flag any issues:

- **Below v4.9.0**: Deployed schema is not available (live manifests require v4.9.0+). Schema Mapper will still work but will use **inferred schema** (sampling documents to guess the schema). Recommend upgrading to get accurate deployed schema support. The user can deploy their schema without redeploying their Studio by running `npx sanity schema deploy`.
- **v4.9.0+**: Full support — deployed schema via live manifests and Dashboard both work. Recommend `@latest` for best experience.

### 3. Choose install location

- Check if an `apps/` directory exists in the current project
- If yes: suggest `apps/schema-mapper` as the default location
- If no: ask the user where they want to install it
- Confirm the path with the user before proceeding

### 4. Clone the repository

```bash
git clone --depth 1 https://github.com/sanity-labs/schema-mapper.git <chosen-path>
rm -rf <chosen-path>/.git
rm -rf <chosen-path>/scripts
```

### 5. Choose Sanity project

```bash
npx sanity projects list
```

- Present the list to the user with project names and IDs
- Ask the user to choose which project to use
- If the Sanity CLI isn't available or the command fails, ask the user for their project ID manually

### 6. Get organization ID

```bash
npx sanity projects get <projectId>
```

- Look for the org ID in the output
- If that fails, ask the user for their organization ID
- Org IDs look like `oXxXxXxXx` (starts with `o`, alphanumeric)

### 7. Configure the app

In `<path>/sanity.cli.ts`: replace `YOUR_PROJECT_ID` with the chosen project ID, replace `YOUR_ORG_ID` with the org ID.

In `<path>/src/App.tsx`: replace `YOUR_PROJECT_ID` with the chosen project ID, and replace `YOUR_ORG_ID` with the org ID.

### 8. Install dependencies

- Check for `pnpm-lock.yaml` → use `pnpm install`
- Check for `yarn.lock` → use `yarn install`
- Otherwise → use `npm install`

Run the install command inside the app directory.

### 9. Done

Tell the user: "Schema Mapper is installed. Run `npx sanity dev` from `<path>` to start. Then open your Sanity dashboard in the browser — the app runs inside the dashboard as a local app, not directly at localhost."

## Update

Follow these steps when a user says "update schema mapper".

### 1. Find the installation

Look for the schema-mapper directory. Check `apps/schema-mapper` first, then ask the user.

### 2. Backup config lines

These two files contain the user's project and org IDs (often with commented-out alternatives). Read and save the **exact lines** containing these IDs:

- `<path>/sanity.cli.ts` — find the `organizationId:` line (e.g. `organizationId: 'abc123', // my org`)
- `<path>/src/App.tsx` — find the `organizationId` line AND the `projectId:` line in the config array

Save the **complete lines** including any inline comments — the user may have other IDs commented alongside. You will reinstate these exact lines after the update.

### 3. Download latest

```bash
cd <path> && curl -sL https://github.com/sanity-labs/schema-mapper/archive/main.tar.gz | tar xz
```

### 4. Overwrite ALL source files

Copy **everything** from the extracted `schema-mapper-main/` directory into `<path>`, including any new files that didn't exist before. The only exceptions are `sanity.cli.ts` and `src/App.tsx` — these contain the user's project and org IDs and MUST NOT be overwritten. Use `rsync` or `cp -r` to ensure new files are added and deleted files are removed:

```bash
rsync -a --exclude='sanity.cli.ts' --exclude='src/App.tsx' <path>/schema-mapper-main/ <path>/
```

### 5. Restore config lines

In the updated `sanity.cli.ts` and `src/App.tsx`, find the placeholder lines (`YOUR_ORG_ID`, `YOUR_PROJECT_ID`) and replace them with the **exact lines** you saved in step 2. This preserves the user's IDs and any commented-out alternatives on the same lines.

### 6. Clean up

```bash
rm -rf <path>/schema-mapper-main
```

### 7. Install dependencies

Run install in case `package.json` changed (use the same package manager detection as setup).

### 8. Done

Tell the user the update is complete.

## Architecture

### App SDK App (not a Studio plugin)

Schema Mapper is a standalone Sanity App SDK app. It uses:
- `sanity.cli.ts` with `app: { organizationId, entry }` config
- `SanityApp` provider from `@sanity/sdk-react` with explicit `config` prop
- `useProjects()`, `useDatasets()`, `useClient()` hooks for data fetching
- `ResourceProvider` to scope hooks to specific project/dataset contexts

### Data Flow

1. `LiveOrgOverview` → `useProjects()` gets all org projects
2. Per project: `ProjectDatasetsWrapper` → `useDatasets()` inside `ResourceProvider`
3. Per dataset: `DatasetDiscoveryWrapper` → `useSchemaDiscovery()` samples documents
4. Results flow up via callbacks → assembled into `ProjectInfo[]`
5. `OrgOverview` renders navigation and graph as data arrives progressively

### Key Files

| File | Purpose |
|------|---------|
| `sanity.cli.ts` | CLI config — org ID, Vite config, CORS headers |
| `src/App.tsx` | Root — SanityApp provider, theme, routing |
| `src/components/LiveOrgOverview.tsx` | Data orchestrator — progressive loading |
| `src/components/OrgOverview.tsx` | UI shell — tabs, graph container, export |
| `src/components/SchemaGraph.tsx` | React Flow graph — 4 layout algorithms, edge styles |
| `src/components/SchemaNode.tsx` | Custom node — field list with type badges and handles |
| `src/hooks/useSchemaDiscovery.ts` | Schema inference from document sampling |

## Known Gotchas

1. **Sanity CLI detection in monorepos** — CLI needs both `sanity.cli.ts` in the project root AND `sanity` in `devDependencies` of `package.json`. Missing either = CLI won't find the app.

2. **Chrome LNA headers** — Chrome requires `Access-Control-Allow-Private-Network: true` for localhost. Without it, Sanity auth flow fails. Configured in `sanity.cli.ts` under `vite.server.headers`.

3. **useDatasets() per-project error handling** — `useDatasets()` throws for projects where the user isn't a member. Each call is wrapped in an `ErrorBoundary` that falls back to assuming a `production` dataset.

4. **SanityApp needs explicit config prop** — `SanityApp` from `@sanity/sdk-react` requires `config` with at least one `{ projectId, dataset }` entry. Without it, hooks like `useProjects()` won't work.

5. **ResourceProvider needs fallback={null}** — Without `fallback={null}`, `ResourceProvider` shows a loading flash. Always pass it for background data fetching.

6. **Hook ordering in React Flow** — `useCallback` functions referencing `setEdges` (from `useEdgesState`) must be defined AFTER the `useEdgesState` call. JavaScript's temporal dead zone causes "Cannot access before initialization" errors otherwise.

7. **Edge/node types must be module-level** — `nodeTypes` and `edgeTypes` objects must be defined outside the component. If defined inside, React Flow recreates them every render causing infinite loops.

## Customization

### Layout Algorithms
- `dagre` — Directed graph (LR)
- `layered` — ELK layered with crossing minimization
- `force` — ELK force-directed
- `stress` — ELK stress with manual component separation

### Edge Styles
- `bezier` — Custom gentle bezier with adjustable curvature
- `smoothstep` — Right-angle stepped edges
- `straight` — Direct lines

### Adding a New Layout
Add the layout function in `SchemaGraph.tsx`, add it to the layout selector dropdown, and define default spacing in the spacing map.

### Changing Node Appearance
Edit `SchemaNode.tsx`. The node renders field names, type badges, and source/target handles for references.

### Export Formats
`ExportDropdown.tsx` supports PNG, SVG, and PDF with smart cropping. Add new formats there.
