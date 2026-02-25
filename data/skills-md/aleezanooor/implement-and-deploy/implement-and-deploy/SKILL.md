---
name: implement-and-deploy
description: Use when implementing a feature and deploying it end-to-end to Azure using GitHub Actions CI/CD, Docker, and Azure Container Apps
---

# Implement and Deploy

## Overview

Full lifecycle: implement feature, containerize, CI/CD pipeline, deploy to Azure, verify live.

**Core principle:** Modular phases with skip-if-done checks and user prompts at decision points.

**Announce at start:** "I'm using the implement-and-deploy skill to build and deploy this feature."

## Phase 1: Repo Setup

**Skip if:** Already in a git repo with remote configured.

1. Ask user: create new repo or use existing?
2. If new: `gh repo create <name> --public --clone` and scaffold project
3. If existing: verify `git remote -v` has a GitHub remote
4. Create feature branch: `git checkout -b feat/<feature-name>`

## Phase 2: Implement Feature

**Skip if:** User confirms feature code is already complete.

1. If frontend work: invoke `frontend-design` skill for UI quality
2. Implement the feature following existing project patterns
3. Write tests if test framework exists
4. Commit work: `git add . && git commit -m "feat: <description>"`

## Phase 3: Local Test

**Skip if:** User confirms local testing passed.

1. Run project test suite if it exists
2. Start app locally and test with `curl` or equivalent
3. If frontend: use `agent-browser` to visually verify the UI
4. Fix any failures before proceeding

## Phase 4: Docker + CI/CD

**Skip if:** Dockerfile and `.github/workflows/deploy.yml` already exist and are correct.

1. Create `Dockerfile` (multi-stage build, minimal final image)
2. Build and test locally: `docker build -t <app> . && docker run -p 8080:8080 <app>`
3. Create `.github/workflows/deploy.yml`:
   - Trigger on push to `main`
   - Build Docker image
   - Push to Azure Container Registry (ACR)
   - Deploy to Azure Container Apps
4. Commit CI/CD files and push branch
5. Open PR: `gh pr create --title "feat: <description>" --body "<summary>"`

## Phase 5: CI/CD Monitor

**Skip if:** PR checks already passing.

1. Delegate to `/aurora`: "Monitor CI/CD pipeline for PR #N in <owner>/<repo>. Report status every 30s until complete."
2. If pipeline fails: read logs, fix issue, push fix, re-monitor
3. Once green: merge PR via `gh pr merge --squash`

## Phase 6: Azure Deploy

**Skip if:** App already deployed and running at expected URL.

1. Ask user for: Azure resource group, ACR name, region (or use defaults)
2. Ensure Azure resources exist (create if needed):
   ```
   az group create --name <rg> --location <region>
   az acr create --name <acr> --resource-group <rg> --sku Basic
   az containerapp env create --name <env> --resource-group <rg>
   ```
3. Build and push image: `az acr build --registry <acr> --image <app>:latest .`
4. Deploy container app:
   ```
   az containerapp create --name <app> --resource-group <rg> \
     --environment <env> --image <acr>.azurecr.io/<app>:latest \
     --target-port 8080 --ingress external
   ```
5. Capture the live URL from output

## Phase 7: Verify Deployment

**Skip if:** Live URL responds correctly.

1. Test live URL with `curl` — check HTTP 200
2. If frontend: use `agent-browser` to visually verify deployed UI
3. Delegate to `/aurora`: "Check logs for <app> in resource group <rg> — report any errors."
4. **If verification fails:** analyze logs, fix, push, wait for CI/CD, redeploy, re-verify (max 3 retries)
5. Present final summary: live URL, resource group, container app name

## When to Stop and Ask

- Azure credentials not configured (`az login` needed)
- User hasn't specified which feature to build
- Deployment target ambiguous (Container Apps vs App Service vs ACI)
- Budget/cost concerns about Azure resources

## Integration

- **frontend-design** — Invoke for any UI work in Phase 2
- **superpowers:verification-before-completion** — Run before declaring done
- **/aurora** — Delegate CI/CD monitoring (Phase 5) and Azure log checks (Phase 7)
- **agent-browser** — Visual testing in Phases 3 and 7
