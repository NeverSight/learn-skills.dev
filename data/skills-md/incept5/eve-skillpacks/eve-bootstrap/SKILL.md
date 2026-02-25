---
name: eve-bootstrap
description: Full onboarding flow — detects auth state, handles access requests for new users, and sets up project for all users.
triggers:
  - eve bootstrap
  - eve onboard
  - eve get started
  - eve setup
---

# Eve Bootstrap

One skill that handles everything from zero to a working Eve project. It detects whether you're already authenticated and adapts:

- **Already authenticated** → skips to project setup
- **Not authenticated** → creates profile, requests access, waits for admin approval, auto-logs in, then sets up project

## Step 1: Check CLI

```bash
eve --version
```

If this fails, install the CLI first:

```bash
npm install -g @anthropic/eve-cli
```

## Step 2: Create Profile

Check if a profile already exists:

```bash
eve profile list
```

If no `staging` profile exists, create one:

```bash
eve profile create staging --api-url https://api.eh1.incept5.dev
eve profile use staging
```

## Step 3: Check Auth Status

```bash
eve auth status
```

This calls the API — not a local file check. Two outcomes:

### Already authenticated → go to Step 5

If `eve auth status` shows you're logged in, skip ahead to **Step 5: Project Setup**.

### Not authenticated → continue to Step 4

## Step 4: Request Access (New Users Only)

Find an SSH public key to use:

```bash
ls ~/.ssh/*.pub
```

Default: `~/.ssh/id_ed25519.pub`. If no key exists, generate one:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519
```

Ask the user for:
- **Org name** — what they want to call their organisation
- **Email** — optional, for their user account

Submit the access request and wait for approval:

```bash
eve auth request-access \
  --ssh-key ~/.ssh/id_ed25519.pub \
  --org "My Company" \
  --email user@example.com \
  --wait
```

The `--wait` flag:
1. Submits the request (unauthenticated)
2. Prints the request ID (`areq_xxx`)
3. Polls every 5 seconds until an admin approves or rejects
4. On approval: auto-completes SSH challenge login
5. Stores token in `~/.eve/credentials.json`

**Tell the user:** "An admin needs to run `eve admin access-requests approve <id>` to approve your request."

Once approved, you're logged in with your own org (as admin).

## Step 5: Project Setup

Set profile defaults if org/project IDs are known:

```bash
eve profile set --org <org_id> --project <proj_id>
```

If no project exists yet, ask the user for:
- **Project name** and **slug** (slug is immutable, keep it short)
- **Repo URL** (e.g., `git@github.com:org/repo.git`)

```bash
# Option A: Ensure project exists
eve project ensure --name "My App" --slug myapp \
  --repo-url git@github.com:org/repo.git --branch main

# Option B: Bootstrap project + environments in one call
eve project bootstrap --name "My App" --repo-url git@github.com:org/repo.git \
  --environments staging,production
```

**URL impact:** Slugs determine deployment URLs:
`{service}.{orgSlug}-{projectSlug}-{env}.{domain}`

## Step 6: Manifest

If `.eve/manifest.yaml` doesn't exist, create a minimal one:

```yaml
schema: eve/compose/v2
project: myapp

registry: "eve"

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    # image is optional; Eve derives it from the service name when managed registry is used
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
      - name: build
        action: { type: build }
      - name: release
        depends_on: [build]
        action: { type: release }
      - name: deploy
        depends_on: [release]
        action: { type: deploy }
```

Use the `eve-manifest-authoring` skill for detailed manifest guidance.

## Step 7: Learn the Platform

Read the Eve platform reference to understand all capabilities:

```
https://web.incept5-evshow-staging.eh1.incept5.dev/llms
```

This covers CLI commands, manifest syntax, agent harnesses, job lifecycle, and more.

## Step 8: Verify

```bash
eve auth status
eve system health
eve project list
```

## Summary

Print what was set up:
- Profile: name, API URL
- Auth: email, org name, org slug
- Project: name, slug, repo URL
- Next steps: sync manifest (`eve project sync`), deploy (`eve env deploy staging --ref main --repo-dir .`)
