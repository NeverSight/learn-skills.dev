---
name: project-validator
description: Validates apps-in-toss project configuration and structure for both web and React Native apps. Use when checking if granite.config.ts is properly configured, verifying required files exist, validating package.json has framework dependencies, ensuring project structure follows apps-in-toss conventions, or debugging project setup issues.
---

# Project Validator

Validates apps-in-toss project configuration, structure, and policies for both **web** and **React Native** projects.

**Supported Project Types:**
- Web projects using `@apps-in-toss/web-framework`
- React Native projects using `@apps-in-toss/granite` with Metro bundler
- Unity game projects (WebGL builds using `@apps-in-toss/web-framework`)

## How to Use This Skill

When validating an apps-in-toss project, follow these steps:

1. **Identify the project type** (Web or React Native)
2. **Read and check the relevant files** using the Read tool
3. **Compare against the schema** in the reference documentation
4. **Report findings** to the user with specific issues and solutions

## Validation Checklist

### Project Structure

Check that the project has:
- ✅ `package.json` exists
- ✅ `granite.config.ts` exists
- ⚠️ `src/` directory exists (recommended)
- ⚠️ `tsconfig.json` exists (recommended for TypeScript projects)

### package.json Validation

Check:
- ✅ File is valid JSON
- ✅ Has `@apps-in-toss/framework`, `@apps-in-toss/web-framework`, or `@granite-js/react-native` in dependencies or devDependencies
- ⚠️ **Has TDS (Toss Design System) package** (strongly recommended for consistent Toss UX):
  - For React Native with `@apps-in-toss/framework` < 1.0.0: `@toss-design-system/react-native`
  - For React Native with `@apps-in-toss/framework` >= 1.0.0: `@toss/tds-react-native`
  - For Web with `@apps-in-toss/web-framework` < 1.0.0: `@toss-design-system/mobile`
  - For Web with `@apps-in-toss/web-framework` >= 1.0.0: `@toss/tds-mobile`
- ⚠️ Has `name` field
- ⚠️ Has `version` field
- ⚠️ Has `scripts` field with common scripts (dev, build, etc.)

### granite.config.ts Validation

#### For Web Projects

Check against [web-granite-config-schema.md](references/web-granite-config-schema.md):

**Required checks:**
- ✅ File exists and is readable
- ✅ Imports `defineConfig` from `@apps-in-toss/web-framework/config`
- ✅ Has `export default defineConfig` statement
- ✅ Contains required fields:
  - `appName` (string)
  - `brand` (object with `displayName`, `primaryColor`, `icon`)
  - `permissions` (array)
  - `web.port` (number)
  - `web.commands.dev` (string)
  - `web.commands.build` (string)

**Optional recommended fields:**
- ⚠️ `navigationBar` (object)
- ⚠️ `webViewProps` (object)
- ⚠️ `outdir` (string)

#### For React Native Projects

Check against [react-native-granite-config-schema.md](references/react-native-granite-config-schema.md):

**Required checks:**
- ✅ File exists and is readable
- ✅ Imports `defineConfig` from `@granite-js/react-native/config`
- ✅ Imports `appsInToss` from `@apps-in-toss/framework/plugins`
- ✅ Has `export default defineConfig` statement
- ✅ Contains required fields:
  - `scheme` (string)
  - `appName` (string)
- ✅ Contains `appsInToss` plugin in plugins array with:
  - `brand` (object with `displayName`, `primaryColor`, `icon`)
  - `permissions` (array)

**Optional recommended fields:**
- ⚠️ `navigationBar` (object)
- ⚠️ `entryFile` (string)
- ⚠️ `outdir` (string)

## Validation Workflow

### When Starting a New Project

1. Read `package.json` to identify project type and framework version
2. Read `granite.config.ts` to determine app type (game vs non-game)
3. **Identify configuration schema to use:**
   - Web apps (including Unity games): [web-granite-config-schema.md](references/web-granite-config-schema.md)
   - React Native apps: [react-native-granite-config-schema.md](references/react-native-granite-config-schema.md)
4. For **non-game apps**: Check if TDS package is installed (recommended for better UX)
5. For **Unity game apps**: Check for Unity SDK installation or WebGL build artifacts (see [unity-game-validation.md](references/unity-game-validation.md))
6. Check all required fields against the appropriate schema
7. Report any missing or incorrect configuration
8. Provide specific solutions from the schema documentation

### When Debugging Configuration Issues

1. Ask the user what issues they're experiencing
2. Read the relevant configuration files
3. Compare against schema requirements
4. Identify the root cause
5. Provide the solution from [Common Issues and Solutions](#common-issues-and-solutions)

### When Reviewing Project Setup

1. Systematically check all validation points
2. Report critical errors (❌) first
3. Then report warnings (⚠️)
4. Suggest improvements based on best practices

## Reporting Validation Results

When reporting validation results to the user:

### ✅ Success
All required checks passed. The project configuration is valid.

### ❌ Critical Error
Required configuration is missing or invalid. The project may not work correctly.
- Report these with high priority
- Provide specific file location (e.g., `granite.config.ts:15`)
- Include the exact fix from the schema documentation

### ⚠️ Warning
Non-critical issue detected. The project may work, but best practices recommend addressing these.
- Report these after critical errors
- Explain why the recommendation matters
- Provide optional improvement suggestions

## Common Issues and Solutions

### Missing Framework Dependencies

**Issue:** `package.json` doesn't have required framework packages

**Solution for Web:**
```bash
npm install @apps-in-toss/web-framework
```

**Solution for React Native:**
```bash
npm install @granite-js/react-native @apps-in-toss/framework
```

### Missing Required Field: appName

**Issue:** `granite.config.ts` is missing the `appName` field

**Solution:** Add `appName` to granite.config.ts:
```typescript
export default defineConfig({
  appName: 'my-app',
  // ...
});
```

### Missing Required Field: brand

**Issue:** `granite.config.ts` is missing the `brand` configuration

**Solution:** Add complete `brand` object:
```typescript
export default defineConfig({
  brand: {
    displayName: 'My App',
    primaryColor: '#3182F6',
    icon: 'https://static.toss.im/icons/app-icon.png',
  },
  // ...
});
```

### Missing Required Field: permissions

**Issue:** `granite.config.ts` is missing the `permissions` array

**Solution:** Add `permissions` array (can be empty):
```typescript
export default defineConfig({
  permissions: [],
  // or with specific permissions:
  permissions: [
    { name: 'clipboard', access: 'read' },
    { name: 'camera', access: 'access' },
  ],
  // ...
});
```

### Missing appsInToss Plugin (React Native)

**Issue:** React Native project doesn't have `appsInToss` plugin

**Solution:** Add the plugin to the plugins array:
```typescript
import { appsInToss } from '@apps-in-toss/framework/plugins';

export default defineConfig({
  plugins: [
    appsInToss({
      brand: {
        displayName: 'My App',
        primaryColor: '#3182F6',
        icon: 'https://static.toss.im/icons/app-icon.png',
      },
      permissions: [],
    }),
  ],
});
```

### Incorrect Import Path

**Issue:** Using wrong import path for `defineConfig`

**Solution for Web:**
```typescript
import { defineConfig } from '@apps-in-toss/web-framework/config';
```

**Solution for React Native:**
```typescript
import { defineConfig } from '@granite-js/react-native/config';
```

### Required File Missing: granite.config.ts

**Issue:** Project doesn't have a `granite.config.ts` file

**Solution:** Create the file using the appropriate template:
- Web projects: See [web-granite-config-schema.md](references/web-granite-config-schema.md)
- React Native projects: See [react-native-granite-config-schema.md](references/react-native-granite-config-schema.md)

### Missing Export Statement

**Issue:** `granite.config.ts` doesn't export the configuration

**Solution:** Add export statement:
```typescript
export default defineConfig({ /* config */ });
```

### Missing TDS (Toss Design System) Package

**Issue:** Mini-app doesn't have TDS package in `package.json`

**Important:** TDS is **strongly recommended** for consistent Toss UX and better review approval chances.

**Solution for React Native:**

Check framework version in `package.json`:

If `@apps-in-toss/framework` < 1.0.0:
```bash
npm install @toss-design-system/react-native
```

If `@apps-in-toss/framework` >= 1.0.0:
```bash
npm install @toss/tds-react-native
```

**Solution for Web:**

Check framework version in `package.json`:

If `@apps-in-toss/web-framework` < 1.0.0:
```bash
npm install @toss-design-system/mobile
```

If `@apps-in-toss/web-framework` >= 1.0.0:
```bash
npm install @toss/tds-mobile
```

**TDS Documentation:**
- React Native: https://tossmini-docs.toss.im/tds-react-native
- Web: https://tossmini-docs.toss.im/tds-mobile

**Note:** Game apps (appType: 'game') may be exempt from TDS requirement

## Reference Documentation

**Always consult these references when validating:**

- **[web-granite-config-schema.md](references/web-granite-config-schema.md)** — Full schema and examples for web `granite.config.ts`
- **[react-native-granite-config-schema.md](references/react-native-granite-config-schema.md)** — Full schema and examples for React Native `granite.config.ts`
- **[unity-game-validation.md](references/unity-game-validation.md)** — Validation guide for Unity WebGL game projects
- **Apps-in-Toss Unity official docs (key takeaways for validation):**
  - Platform model & precheck (overview, runtime-structure, precheck): WebGL/WASM + JS bridge; no native plugins; mobile/touch targets; file I/O and sockets limited; AR/XR/Compute constrained.
  - Engine versions (recommend-engine): Prefer Unity 2023.3 LTS; 2022.3 stable; 2021.3 legacy; avoid 2024.2 beta for production.
  - Migration flow (migration-guide): Precheck → WebGL conversion → Apps-in-Toss SDK integration → UX/perf optimization → `.ait` packaging/monitoring.
  - Performance goals (perf-optimization, perf-measure): Startup <3s target (<5s max), avg FPS ≥30 on mobile, memory <200MB (critical >300MB), first frame <5s, battery ~90–110% of native.
  - Runtime/startup/loading (runtime/performance, startup-speed, loading): Adaptive frame/quality, batching/instancing/LOD/culling, pooled updates; avoid heavy first-frame work; progressive/prioritized loading with unload paths and cache limits; scene transitions near 2s when possible.
  - Debugging (debug-exception): Centralized logging to web/Apps-in-Toss, global exception handler with recovery, in-app profiler/console hooks for WebGL.

## Best Practices for Validation

1. **Be Specific**: When reporting issues, include exact file paths and line numbers if possible
2. **Provide Context**: Explain why a field is required or recommended
3. **Offer Solutions**: Always provide the exact code fix from the schema documentation
4. **Prioritize**: Report critical errors before warnings
5. **Be Thorough**: Check all required fields, not just the obvious ones
6. **Check TDS Usage**: Verify if TDS package is installed and recommend it for consistent Toss UX
7. **Provide Documentation Links**: Include relevant TDS documentation links when suggesting TDS

## Example Validation Report

```
Validating apps-in-toss project...

✅ package.json found and valid
✅ granite.config.ts found

Project Type: Web (detected @apps-in-toss/web-framework v1.2.0)
App Type: general (non-game)

❌ Critical Errors:
1. Missing required field: brand
   Location: granite.config.ts
   Fix: Add brand configuration with displayName, primaryColor, and icon

2. Missing required field: permissions
   Location: granite.config.ts
   Fix: Add permissions array (can be empty: permissions: [])

⚠️ Warnings:
1. Missing recommended field: navigationBar
   Suggestion: Add navigationBar for better UX

2. TDS package not found
   Recommendation: Install @toss/tds-mobile (for @apps-in-toss/web-framework >= 1.0.0)
   Command: npm install @toss/tds-mobile
   Benefit: Provides consistent Toss UX and improves review approval chances
   Documentation: https://tossmini-docs.toss.im/tds-mobile

Consult: references/web-granite-config-schema.md for complete examples
```
