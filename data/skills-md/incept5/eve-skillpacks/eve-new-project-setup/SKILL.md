---
name: eve-new-project-setup
description: Configure a new Eve Horizon project after running eve init (profile, auth, manifest, and repo linkage).
triggers:
  - new project setup
  - initialize eve project
  - get started with eve
  - configure eve manifest
  - run eve-new-project-setup
---

# Eve New Project Setup

Use this after a developer has run `eve init` and needs to configure the project for Eve Horizon.

## Context

The user has already run:
```bash
npm install -g @eve-horizon/cli
eve init my-project
cd my-project
```

This skill handles the remaining setup: profile, authentication, org/project registration, manifest customization, and git remote configuration.

## Step 1: Verify CLI

```bash
eve --version
```

If this fails, the CLI wasn't installed. Have them run:
```bash
npm install -g @eve-horizon/cli
```

## Step 2: Profile Setup

Create a profile for the staging environment:

```bash
eve profile create staging --api-url https://api.eh1.incept5.dev
eve profile use staging
```

Ask the user for their email and set defaults:

```bash
eve profile set --default-email user@example.com
```

## Step 3: Authentication

Check current auth status:

```bash
eve auth status
```

If not authenticated, log in:

```bash
eve auth login
```

The CLI will guide them through SSH key discovery (can fetch from GitHub if needed).

We'll set harness credentials after project creation.

## Step 4: Org + Project

Ask the user for:
- **Organization name** (e.g., "my-company")
- **Project name** (e.g., "My App")
- **Project slug** (e.g., "my-app")
- **Repo URL** (e.g., "git@github.com:me/my-app.git")

Create or ensure they exist:

```bash
eve org ensure my-company --slug myco
eve project ensure --name "My App" --slug my-app --repo-url git@github.com:me/my-app.git --branch main
```

**URL impact:** The org and project slugs directly form deployment URLs and K8s namespaces:
- URL: `{service}.{orgSlug}-{projectSlug}-{env}.{domain}` (e.g., `api.myco-my-app-staging.eh1.incept5.dev`)
- Namespace: `eve-{orgSlug}-{projectSlug}-{env}` (e.g., `eve-myco-my-app-staging`)
- `${ORG_SLUG}` is available for interpolation in manifest values

Slugs are immutable — choose short, meaningful values.

Set as defaults in the profile:

```bash
eve profile set --org org_xxx --project proj_xxx
```

## Step 5: Choose Harness + Set API Keys

Ask which harness they want to target (can be more than one):
- **mclaude / claude** (Anthropic)
- **code / codex** (OpenAI)
- **zai** (Z.ai)
- **gemini** (Google)

Map harnesses to required secrets:
- **mclaude/claude**: `ANTHROPIC_API_KEY` (preferred) or Claude OAuth via `eve auth sync`
- **code/codex**: `OPENAI_API_KEY` (preferred) or `CODEX_AUTH_JSON_B64`
- **zai**: `Z_AI_API_KEY`
- **gemini**: `GEMINI_API_KEY` (or `GOOGLE_API_KEY`)

Decide where to store secrets:
- **Org** (recommended) for shared keys across projects
- **Project** for app-specific keys
- **User** for personal keys

Use a secrets file for batch setup (starter repo includes `secrets.env.example`):

```bash
cp secrets.env.example secrets.env
eve secrets import --org org_xxx --file ./secrets.env
```

For Claude/Codex OAuth tokens on the host:

```bash
# Store OAuth tokens in the project scope (or add --system if admin)
eve auth sync --project proj_xxx
```

## Step 6: Manifest Configuration

The starter template includes `.eve/manifest.yaml`. Update it with the project details:

```yaml
schema: eve/compose/v2
project: my-app

services:
  api:
    build:
      context: apps/api
    ports: [3000]
    x-eve:
      ingress:
        public: true
        port: 3000

environments:
  staging:
    pipeline: deploy

pipelines:
  deploy:
    steps:
      - name: deploy
        action: { type: deploy }
```

Key fields to customize:
- `project`: Match the project slug
- `services`: Define your app's services
- `x-eve.ingress`: Configure public access

## Step 7: Git Remote

The project starts with no remote. Help set one up:

```bash
git remote -v
git remote add origin git@github.com:user/my-app.git
git push -u origin main
```

## Step 8: Verification

Run these checks to confirm setup:

```bash
eve system health
eve auth status
eve profile show
```

## Next Steps

After setup is complete, suggest:

1. **Run locally**: `docker compose up --build`
2. **Set secrets**: `eve secrets set MY_KEY "value"` or `eve secrets import --file ./secrets.env`
3. **Deploy to staging**: `eve env deploy staging --ref main --repo-dir .`
4. **Create a job**: `eve job create --prompt "Review the codebase"`

Note: If the environment has a `pipeline` configured in the manifest, `eve env deploy <env> --ref <sha>` will trigger that pipeline. Use `--direct` to bypass the pipeline and do a direct deploy. `--ref` must be a 40-character SHA, or a ref resolved against `--repo-dir`/cwd.

## Troubleshooting

### "eve: command not found"
```bash
npm install -g @eve-horizon/cli
```

### "Not authenticated"
```bash
eve auth login
```

### "No profile"
```bash
eve profile create staging --api-url https://api.eh1.incept5.dev
```
