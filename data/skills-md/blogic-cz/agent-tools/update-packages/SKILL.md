---
name: update-packages
description: "LOAD THIS SKILL when: updating npm packages, user mentions 'update packages', 'update-packages', 'outdated', 'dependency updates'. Covers autonomous npm package updates with breaking change handling, Bun updates, Playwright Docker sync, and package group coordination."
---

# Update Packages

## First Step: Create Branch (MANDATORY)

Before touching any packages, create a dedicated branch:

```bash
but branch new chore/update-packages-$(date +%y%m%d-%H%M)
```

**Rules:**

- Never reuse an existing update-packages branch
- Always create a fresh branch with the current timestamp
- All package update commits go to this branch

## Definition of Done

- `bun upgrade` shows all packages at latest versions
- No packages remain to select or update
- All checks pass (`bun run check`)
- All relevant tests pass

## If Bun Updates

When the Bun runtime itself has a new version:

1. Update `packageManager` field in root `package.json`:

   ```json
   "packageManager": "bun@X.Y.Z"
   ```

2. Update all Dockerfiles that reference `BUN_VERSION`:

   ```dockerfile
   ARG BUN_VERSION=X.Y.Z
   ```

3. Update CI pipeline `BUN_VERSION` environment variable in all relevant pipeline files.

4. Run checks to confirm nothing broke:

   ```bash
   bun run check
   ```

5. Commit message format:
   ```
   chore: update bun to vX.Y.Z
   ```

## If Playwright Updates

When `@playwright/test` or `playwright` npm version changes:

1. The Docker image version **must match** the npm package version exactly.

2. Find all references to the Playwright Docker image across:
   - `Dockerfile` files
   - CI/CD pipeline YAML files
   - Kubernetes Helm values files
   - Any other infrastructure files

3. Update all references to use the matching image tag:

   ```
   mcr.microsoft.com/playwright:vX.Y.Z-noble
   ```

4. Run E2E tests to confirm compatibility:

   ```bash
   bun run test:e2e
   ```

5. Commit message format:
   ```
   chore: update playwright to vX.Y.Z
   ```

## Catalog Packages

Some packages are managed via Bun's catalog and require manual version checking:

```bash
# Check latest version of a catalog package
npm view <package-name> version

# Check all versions available
npm view <package-name> versions --json
```

Update catalog entries in `package.json` or `bun.lockb` manually after confirming the latest version.

## Package Groups (Update Together)

These packages must always be updated as a group — mismatched versions cause type errors or runtime failures:

| Group               | Packages                                                                                            |
| ------------------- | --------------------------------------------------------------------------------------------------- |
| **tanstack-router** | `@tanstack/react-router`, `@tanstack/router-devtools`, `@tanstack/router-plugin`, `@tanstack/start` |
| **tanstack-query**  | `@tanstack/react-query`, `@tanstack/react-query-devtools`, `@tanstack/query-core`                   |
| **trpc**            | `@trpc/server`, `@trpc/client`, `@trpc/react-query`, `@trpc/tanstack-react-query`                   |
| **effect**          | `effect`, `@effect/schema`, `@effect/platform`, `@effect/language-service`                          |
| **drizzle**         | `drizzle-orm`, `drizzle-kit`, `drizzle-zod`                                                         |
| **pino**            | `pino`, `pino-pretty`, `@types/pino`                                                                |
| **playwright**      | `@playwright/test`, `playwright` (+ Docker image sync — see above)                                  |

## Update Strategy

**For regular packages:**

1. Run `bun upgrade` to update all packages interactively
2. Select packages to update (prefer updating all unless a known breaking change exists)
3. Run `bun run check` after each group update
4. Fix any breaking changes before proceeding to the next group

**For catalog packages:**

1. Manually check latest version with `npm view <package> version`
2. Update the version in the catalog configuration
3. Run `bun install` to apply
4. Run `bun run check`

## Testing Requirements

| Update Type                                    | Required Tests                                        |
| ---------------------------------------------- | ----------------------------------------------------- |
| UI/component packages (`@base-ui/react`, etc.) | `bun run check` + visual review in browser            |
| TRPC / TanStack Router                         | `bun run check` + `bun run test`                      |
| Drizzle ORM                                    | `bun run check` + `bun run test`                      |
| Effect packages                                | `bun run check` + `bun run test`                      |
| Playwright                                     | `bun run check` + `bun run test:e2e`                  |
| Bun runtime                                    | `bun run check` + `bun run test` + `bun run test:e2e` |
| All others                                     | `bun run check`                                       |

## Cache Recovery (Bun)

If packages fail to install or you see stale cache errors after updating:

```bash
bun clean:packages && bun install
```

This clears the local package cache and performs a fresh install.

## Common Breaking Changes

| Package                    | Common Issue                                                          | Fix                                                                         |
| -------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `@effect/language-service` | Version must match `effect` core exactly                              | Always update together with `effect`                                        |
| `@types/react`             | React 19 types changed significantly; some third-party types conflict | Check peer deps, may need `--legacy-peer-deps` workaround or type overrides |
| `@base-ui/react`           | API surface changes frequently in pre-stable releases                 | Review changelog, update component usage accordingly                        |

## Guardrails

- **DO NOT** update packages with `workspace:*` version specifiers — these are internal monorepo packages managed separately
- **DO NOT** skip `@typescript/native-preview` updates — this package affects TypeScript LSP performance and should stay current
- **DO NOT** use `bun outdated` to check for updates — it misses packages that are in the catalog or have non-standard version specifiers; use `bun upgrade` interactively instead
