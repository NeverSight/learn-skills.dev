---
name: pc-deploy
description: Deploy the current project to Ploi Cloud. Detects project type, creates or updates the app via MCP, deploys, monitors, and auto-fixes failures. Supports both git repos and upload-based deployments.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - mcp__ploi-cloud-mcp__applications_index
  - mcp__ploi-cloud-mcp__applications_store
  - mcp__ploi-cloud-mcp__applications_show
  - mcp__ploi-cloud-mcp__applications_update
  - mcp__ploi-cloud-mcp__applications_status
  - mcp__ploi-cloud-mcp__applications_deploy
  - mcp__ploi-cloud-mcp__applications_destroy
  - mcp__ploi-cloud-mcp__applications_logs
  - mcp__ploi-cloud-mcp__applications_debug_show
  - mcp__ploi-cloud-mcp__applications_debug_summary
  - mcp__ploi-cloud-mcp__applications_build-config_index
  - mcp__ploi-cloud-mcp__applications_build-config_update
  - mcp__ploi-cloud-mcp__applications_settings_update
  - mcp__ploi-cloud-mcp__applications_repository_update
  - mcp__ploi-cloud-mcp__applications_php-config_update
  - mcp__ploi-cloud-mcp__applications_resources_update
  - mcp__ploi-cloud-mcp__applications_deployments_index
  - mcp__ploi-cloud-mcp__applications_deployments_show
  - mcp__ploi-cloud-mcp__applications_deployments_logs
  - mcp__ploi-cloud-mcp__applications_secrets_index
  - mcp__ploi-cloud-mcp__applications_secrets_store
  - mcp__ploi-cloud-mcp__applications_secrets_update
  - mcp__ploi-cloud-mcp__applications_secrets_injected
  - mcp__ploi-cloud-mcp__applications_services_logs
  - mcp__ploi-cloud-mcp__applications_services_restart
  - mcp__ploi-cloud-mcp__v1_applications_services_index
  - mcp__ploi-cloud-mcp__v1_applications_services_store
  - mcp__ploi-cloud-mcp__v1_applications_services_update
  - mcp__ploi-cloud-mcp__applications_volumes_store
  - mcp__ploi-cloud-mcp__applications_domains_store
  - mcp__ploi-cloud-mcp__applications_source_upload_url
---

# Deploy to Ploi Cloud

Deploy the current project to Ploi Cloud directly from your editor. Scans the project, creates or updates the application via MCP, deploys, monitors, and auto-fixes failures. Works with git repositories and projects without a repo (via source upload).

## Prerequisites

The Ploi Cloud MCP server must be connected. If not configured, tell the user to run:

```
claude mcp add --transport http ploi-cloud https://ploi.cloud/mcp
```

## Phase 1: Source validation

Determine the deployment mode: **git** or **upload**.

1. Run `git rev-parse --git-dir` to check if this is a git repo
2. If it is a git repo, run `git remote get-url origin` to check for a remote URL
3. **If both succeed** → **git mode**
   - Parse the remote URL to extract owner and repo name (supports github.com, gitlab.com, bitbucket.org)
   - Run `git branch --show-current` to get the current branch
4. **If either fails** (not a git repo, or no remote URL) → **upload mode**
   - Derive the application name from the current directory name (lowercase, hyphens, 4-32 chars)
   - Inform the user: "No git repository detected — deploying via source upload."

## Phase 2: Project detection

Scan local files to determine the project type and requirements.

**Type detection (first match wins):**
- `composer.json` containing `laravel/framework` → `laravel`
- `composer.json` containing `statamic/cms` → `statamic`
- `composer.json` containing `craftcms/cms` → `craftcms`
- `wp-config.php` exists → `wordpress`
- `composer.json` exists (generic) → `php`
- `package.json` exists → `nodejs`

**Runtime detection:**
- PHP version: read `composer.json` → `require.php` constraint, pick the highest matching version (8.1, 8.2, 8.3, 8.4)
- Node.js version: read `package.json` → `engines.node`, default to `20` if not specified
- PHP extensions: collect all `ext-*` keys from `composer.json` → `require`, exclude built-in (opcache, pcntl, pdo_mysql, pdo_pgsql, redis, sodium, zip)

**Service detection from dependencies:**

| Dependency | Service type |
|---|---|
| `mysql2`, `@prisma/client` with MySQL in schema | `mysql` |
| `pg`, `postgres`, `@prisma/client` with PostgreSQL | `postgresql` |
| `mongodb`, `mongoose`, `mongodb/mongodb` | `mongodb` |
| `predis/predis`, `ext-redis`, `redis`, `ioredis` | `redis` |
| `php-amqplib/php-amqplib`, `amqplib` | `rabbitmq` |

**Build commands by type:**

| Type | Default build command |
|---|---|
| `laravel` | `composer install --no-interaction --prefer-dist --optimize-autoloader --no-dev && npm ci && npm run build` |
| `statamic` | `composer install --no-interaction --prefer-dist --optimize-autoloader --no-dev && npm ci && npm run build` |
| `craftcms` | `composer install --no-interaction --prefer-dist --optimize-autoloader --no-dev` |
| `wordpress` | (none) |
| `php` | `composer install --no-interaction --prefer-dist --optimize-autoloader --no-dev` |
| `nodejs` | `npm ci && npm run build` |

**Init commands:**
- Laravel/Statamic: `php artisan migrate --force`
- Craft CMS: `php craft install/check && php craft migrate/all --no-interaction`
- Others: none

**Secrets:**
- Read `.env.example` if it exists
- Extract variable names that have empty or placeholder values
- Exclude auto-injected variables (see references/service-env-vars.md)
- Exclude `APP_KEY` (auto-generated by Ploi Cloud for Laravel apps)

## Phase 3: Check existing app

1. Call `applications_index` to list all apps
2. **Git mode:** search for an app whose repository URL matches the current project's remote URL
3. **Upload mode:** search for an app whose name matches the derived directory name AND has `source_type` = `upload`
4. If found → go to Phase 4b (update)
5. If not found → go to Phase 4a (create)

## Phase 4a: Create application

**Git mode:**
1. `applications_store` — create with name (repo name), type, repository URL, owner, name, branch

**Upload mode:**
1. `applications_store` — create with name (directory name), type, and `source_type: "upload"`. Do NOT pass repository fields.

**Both modes (continue):**
2. `applications_build-config_update` — set build commands and init commands
3. `applications_settings_update` — set health_check_path (/ for most types, /up for Statamic)
4. `applications_php-config_update` — set PHP version and extensions (PHP apps only)
5. `v1_applications_services_store` — create each detected service (memory: 512Mi, volume_size: 5Gi)
6. `applications_secrets_store` — add required secrets only
7. Go to Phase 4c (upload mode) or Phase 5 (git mode)

## Phase 4b: Update existing application

**Git mode:**
1. `applications_repository_update` — update repo URL and branch if changed

**Both modes (continue):**
2. `applications_build-config_update` — update build commands if needed
3. `v1_applications_services_index` — check existing services, add any missing via `v1_applications_services_store`
4. Go to Phase 4c (upload mode) or Phase 5 (git mode)

## Phase 4c: Upload source archive (upload mode only)

Skip this phase entirely in git mode.

1. Determine which ignore file to use:
   - Use `.dockerignore` if it exists
   - Otherwise use `.gitignore` if it exists
   - Otherwise no exclusions
2. Create a tar.gz archive of the project directory:
   ```
   tar czf /tmp/ploi-source-upload.tar.gz --exclude='.git' --exclude='node_modules' --exclude='.DS_Store' -X <ignore-file> -C <project-dir> .
   ```
   If no ignore file exists, omit the `-X` flag. Always exclude `.git`, `node_modules`, and `.DS_Store`.
3. Call `applications_source_upload_url` with the application ID to get a signed upload URL
4. Upload the archive directly using curl:
   ```
   curl -s -X POST -F 'source=@/tmp/ploi-source-upload.tar.gz' '<upload_url>'
   ```
   Verify the response contains `"success": true`.
5. Clean up the temp file: `rm /tmp/ploi-source-upload.tar.gz`
6. Go to Phase 5

## Phase 5: Deploy

1. Call `applications_deploy` to trigger a deployment
2. Note the deployment ID from the response
3. Go to Phase 6

## Phase 6: Monitor

Poll every 15 seconds for up to 10 minutes.

1. Call `applications_deployments_logs` with `tail: 100` to check build progress
2. Call `applications_status` to check if the app is live
3. If deployment status is `failed` or `cancelled` → go to Phase 7 (Auto-fix)
4. If application status is `active` → go to Phase 8 (Success)
5. If still building (deployment status `running` or app status `deploying`) → wait 15 seconds and repeat

## Phase 7: Auto-fix

Maximum 5 retry attempts. Diagnose the failure and apply a fix.

**Diagnosis:**
1. Read deployment logs (`applications_deployments_logs` with `tail: 2000`)
2. Read application logs (`applications_logs`)
3. Check debug summary (`applications_debug_summary`)

**Fix patterns:**

| Error | Fix |
|---|---|
| OOMKilled / exit code 137 | `applications_resources_update` — increase memory (1Gi → 2Gi → 4Gi) |
| Missing PHP extension | `applications_php-config_update` — add the extension |
| Build failure (composer/npm) | `applications_build-config_update` — adjust commands |
| Health check failure | `applications_settings_update` — change health_check_path |
| Missing environment variable | `applications_secrets_store` — add the variable |
| Database connection error | Check service exists, verify env var injection |

After applying a fix:
1. **Upload mode:** re-run Phase 4c to re-upload source if build commands changed local output
2. Call `applications_deploy` to redeploy
3. Return to Phase 6 (Monitor)

## Phase 8: Success

1. Call `applications_show` to get the auto-assigned domain
2. Confirm with `applications_debug_summary` that pods are healthy
3. Report to the user:
   - Application name
   - Deployment mode (git or upload)
   - Live URL (the auto-assigned domain)
   - Application ID
   - Services created
   - Any fixes that were applied

## Critical rules

- NEVER add domains — the platform auto-assigns a preview domain
- NEVER add `APP_KEY` to secrets — Ploi Cloud generates it for Laravel apps
- NEVER hardcode database credentials in secrets — services auto-inject them via ConfigMap
- Default memory is `1Gi`. Use `applications_resources_update` with the `memory_request` parameter to change it
- Service volume_size must be `"5Gi"` (Kubernetes quantity format with unit suffix)
- Each build command entry becomes a separate `RUN` in the Dockerfile — chain dependent commands with `&&`
- `${VAR}` interpolation in secrets only resolves other user secrets, NOT service-injected vars
- Build commands run as root, but the application runtime runs as www-data (non-root). Build-time operations like `npm install -g` work fine
- Application status values: `starting`, `active`, `deploying`, `stopping`, `stopped`, `destroying`, `failed`. Use `active` to confirm the app is live
- Deployment status values: `pending`, `running`, `success`, `failed`, `cancelled`. Note that `running` means the build is in progress, not that the app is live
- Upload-type applications do NOT support `skip_build` (redeploy) — every deployment runs a full build
- When creating the tar.gz for upload, always exclude `.git`, `node_modules`, and `.DS_Store` at minimum
