---
name: power-apps-code-apps
description: >
  Use when building, scaffolding, debugging, or deploying Microsoft Power Apps Code Apps
  using React, Vue, or TypeScript in VS Code. Handles project initialization via pac CLI,
  Dataverse and connector data access via the @microsoft/power-apps SDK, power.config.json
  configuration, Vite build pipelines, and deployment to Power Platform environments.
  Triggers on: "power apps", "code app", "pac code", "dataverse", "power platform app",
  "vibe coding", "scaffold power app", "deploy code app".
license: MIT
compatibility: "Requires Node.js LTS, npm, Power Platform CLI (pac), VS Code"
metadata:
  author: custom
  version: "1.0.0"
  platform: "Microsoft Power Platform"
  sdk-version: "@microsoft/power-apps ^1.0.3"
---

# Power Apps Code Apps Developer Skill

You are an expert Power Apps Code Apps developer. Code Apps are standalone web applications
built with React/Vue/TypeScript that run as first-class citizens on the Power Platform.

## CRITICAL RULES -- Read These First

1. **NEVER write authentication code.** The Power Apps Host manages all Entra ID auth.
   Do not use MSAL.js, do not implement OAuth flows, do not create login pages.
   The user is already authenticated when the app loads.

2. **`initialize()` was REMOVED in SDK v1.0.** Do NOT call `initialize()`.
   Data calls and context retrieval can be made immediately. Any code calling
   `initialize()` is outdated and wrong.

3. **This is NOT PCF.** Do not use `context.webAPI`, `context.parameters`, or
   `Xrm.WebApi`. Code Apps use `getContext()` and generated service classes.
   Read `resources/sdk-api.md` for correct method signatures.

4. **SDK v1.0.0 is deprecated.** Always use `@microsoft/power-apps` version `^1.0.3`.

5. **No mobile support.** Code Apps do not run on Power Apps mobile or Power Apps for Windows.

6. **Environment admin must enable Code Apps.** `pac code push` fails with "does not allow
   this operation for this Code app" until an environment admin enables Code App operations.
   This is NOT enabled by default. If blocked, deploy as a web resource instead (see below).

7. **Code Apps CANNOT be embedded inside MDAs.** Code Apps are standalone Power Apps. They
   cannot be used as Custom Pages, iframed, or embedded inline in a Model-Driven App. The
   only ways to embed custom UI inside an MDA are: Web Resources, Custom Pages (canvas apps
   built specifically as custom pages), or PCF controls. See `resources/mda-integration.md`.

## Workflow: Building a New Code App

### Step 1 -- Plan (Act as Plan Designer)

Before writing code, propose a plan to the user:
- **User personas** -- Who uses this app?
- **Data entities** -- What Dataverse tables or connectors are needed?
- **Key screens/flows** -- What does the user navigate through?
- **Components** -- What reusable UI components are needed?

Do NOT generate code until the plan is approved.

### Step 2 -- Scaffold

Use the starter template (includes React, Tailwind, TanStack Query, React Router, Zustand, Radix UI):

```bash
npx degit github:microsoft/PowerAppsCodeApps/templates/starter my-app
cd my-app
npm install
pac auth create
pac env select --environment <environment-id>
pac code init --displayname "App Name"
```

Or use the minimal Vite template:
```bash
npx degit github:microsoft/PowerAppsCodeApps/templates/vite my-app
```

For full CLI reference, read `resources/cli-ref.md`.

### Step 3 -- Configure Vite

The `vite.config.ts` must include the Power Apps plugin:

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { powerApps } from "@microsoft/power-apps-vite/plugin";

export default defineConfig({
  plugins: [react(), powerApps()],
});
```

Key packages in `package.json`:
- `@microsoft/power-apps` (^1.0.3) -- runtime SDK
- `@microsoft/power-apps-vite` (^1.0.2) -- Vite plugin (devDependency)

### Step 4 -- Access Context

```typescript
import { getContext } from "@microsoft/power-apps/app";

const context = await getContext(); // Returns Promise<IContext> -- must await!
// context.app.appId        -- string
// context.app.environmentId -- string
// context.app.queryParams  -- Record<string, string>
// context.user.fullName    -- string
// context.user.objectId    -- string
// context.user.tenantId    -- string
// context.user.userPrincipalName -- string
// context.host.sessionId   -- string
```

For complete interface definitions, read `resources/sdk-api.md`.

### Step 5 -- Add Data Sources

```bash
pac code add-data-source --dataset <dataset-name>
```

This generates typed service and model files:
- `generated/services/<Name>Service.ts` -- CRUD methods
- `generated/models/<Name>Model.ts` -- TypeScript types

**Tabular services expose:** `create()`, `get()`, `getAll()`, `update()`, `delete()`
**Dataverse services additionally expose:** `getMetadata()`

Query example:
```typescript
import { ContactService } from "./generated/services/ContactService";

const contacts = await ContactService.getAll({
  select: ["fullname", "emailaddress1"],
  filter: "contains(fullname, 'Smith')",
  orderBy: "fullname asc",
  top: 50,
  maxPageSize: 100,
});
```

For complete data access patterns, read `resources/sdk-api.md`.

### Step 6 -- Configure Telemetry (Optional)

```typescript
import { setConfig } from "@microsoft/power-apps/app";

setConfig({
  logger: {
    logMetric: (value) => {
      appInsights.trackEvent({ name: value.type }, value.data);
    },
  },
});
```

### Step 7 -- Build and Deploy

```bash
npm run build | pac code push
```

The build script in package.json should be: `"build": "tsc -b && vite build"`

For solution-targeted deployment:
```bash
npm run build | pac code push --solutionName MySolution
```

For full deployment and ALM patterns, read `resources/cli-ref.md`.

## Known Limitations

Read `resources/overview.md` for the full list. Key ones:
- No mobile (Power Apps mobile / Windows app)
- No Power BI `PowerBIIntegration` function
- No SharePoint Forms integration
- No FetchXML for Dataverse queries (use OData $filter)
- No polymorphic lookups
- No Dataverse actions/functions
- No alternate key support
- No option set metadata retrieval
- No environment variables access
- No Solution Packager
- No Git integration for ALM (yet)
- Excel Online connectors (Business and OneDrive) unsupported

## When Debugging

1. Check that `@microsoft/power-apps` is version `^1.0.3` (not 1.0.0)
2. Verify `power.config.json` exists and has valid `appId` -- read `resources/config-schema.md`
3. Ensure the Vite config includes `powerApps()` plugin
4. Check browser compatibility (Chrome/Edge may block local network access since Dec 2025)
5. Verify `pac auth` is connected to the correct environment
6. Do NOT add authentication code -- the host handles it

## When Migrating from Canvas Apps

If the user wants to port Canvas App logic to a Code App:
1. Read `resources/yaml-syntax.md` for the `.pa.yaml` source format
2. Identify Power Fx formulas and translate to TypeScript equivalents
3. Map Canvas App data sources to Code App generated services
4. Recreate the UI using React components

## Vibe Coding Mode

When the user gives a high-level natural language description:
1. Act as the Plan Designer -- decompose into data model + user flows
2. Propose Dataverse table structure
3. Generate component hierarchy
4. Scaffold the project
5. Implement iteratively, screen by screen

Read `resources/vibe-coding.md` for prompt patterns and AI integration.

## Web Resource Fallback Deployment

When `pac code push` is blocked (environment permissions) or when you need the React app
embedded inside an MDA (which Code Apps cannot do), deploy as a web resource instead.

### Setup

```bash
npm install -D vite-plugin-singlefile
```

### Vite Config

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { viteSingleFile } from "vite-plugin-singlefile";

export default defineConfig({
  plugins: [react(), viteSingleFile()],
  build: {
    assetsInlineLimit: 100000000,
    cssCodeSplit: false,
  },
});
```

### Build and Deploy

```bash
npm run build
# Produces a single index.html with all JS/CSS inlined
```

Then upload via the Dataverse Web API:
```powershell
$html = Get-Content -Path "dist/index.html" -Raw
$b64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($html))

$body = @{
    name = "prefix_/html/myapp.html"
    displayname = "My React App"
    webresourcetype = 1
    content = $b64
} | ConvertTo-Json

$headers["MSCRM.SolutionUniqueName"] = "MySolution"
Invoke-WebRequest -Uri "$baseUrl/webresourceset" -Headers $headers -Method POST `
    -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) `
    -ContentType "application/json; charset=utf-8" -UseBasicParsing
```

Add to MDA sitemap:
```xml
<SubArea Id="Home" Title="My App" Url="/WebResources/prefix_/html/myapp.html" Client="All" />
```

### Context Differences

When running as a web resource instead of a Code App:
- `@microsoft/power-apps` SDK is NOT available — use `Xrm.WebApi` or direct fetch instead
- `Xrm` may not be injected — try `parent.Xrm` or fall back to WhoAmI API for user identity
- Authentication is still handled by the host (MDA session)
- Use relative URLs (`/api/data/v9.2/...`) for Dataverse calls
