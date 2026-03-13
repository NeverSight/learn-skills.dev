---
name: deploying-to-azure
description: Provides deployment commands and troubleshooting for Azure Container Apps. Use when running azd commands, deploying containers, debugging deployment failures, or updating infrastructure in this repository.
---

# Deploying to Azure

## Subagent Delegation for Deployment Analysis

**Container logs and deployment output can be massive** (1000+ lines). Delegate to subagent for:
- Analyzing full deployment logs
- Debugging container startup failures
- RBAC permission troubleshooting
- Multi-resource status checks

### Delegation Pattern

```text
runSubagent(
  prompt: "ANALYSIS task - analyze deployment issue.
    
    **Problem**: [describe the deployment failure]
    
    **Run these commands**:
    1. az containerapp logs show --name <app> --resource-group <rg> --tail 200
    2. az containerapp show --name <app> --resource-group <rg> --query 'properties.provisioningState'
    
    **Find**:
    - Error messages or stack traces
    - Resource provisioning failures
    - Configuration mismatches
    
    **Return** (max 15 lines):
    - Root cause (1-2 sentences)
    - Key error lines only (max 5)
    - Suggested fix command
    
    Do NOT include full log output.",
  description: "Debug: [deployment issue]"
)
```

### When to Delegate vs Inline

| Delegate to Subagent | Keep Inline |
|----------------------|-------------|
| Full log analysis (100+ lines) | Quick status check |
| Multi-resource debugging | Single az command |
| RBAC permission audit | Container image query |
| Startup failure diagnosis | Provisioning state check |

## Quick Commands

| Command | Purpose | Time |
|---------|---------|------|
| `azd up` | Full deployment (Entra app + infrastructure + container) | 10-12 min |
| `azd deploy` | Code-only deployment (Docker rebuild + push) | 3-5 min |
| `azd provision` | Re-run infrastructure + AI Foundry discovery | 5-7 min |

## Deployment Phases

1. **preprovision** → AI Foundry auto-discovery + tenant detection. For CI: `azd env set ENTRA_SERVICE_MANAGEMENT_REFERENCE "<guid>"`
2. **provision** → Deploy Azure resources via Bicep (infrastructure + Entra app via Microsoft Graph Bicep extension + placeholder container image)
3. **postprovision** → Sets `identifierUri` on Entra app + updates redirect URIs + assigns RBAC to AI Foundry + generates local dev config
4. **predeploy** → Builds container (local Docker or ACR cloud build)

**Implementation**: 
- `infra/entra-app.bicep` (Entra app registration via Microsoft Graph Bicep extension)
- `deployment/hooks/preprovision.ps1` (AI Foundry discovery)
- `deployment/hooks/postprovision.ps1` (Entra config + RBAC + local config generation)
- `deployment/hooks/predeploy.ps1` (container build + push)
- `deployment/hooks/modules/Get-AIFoundryAgents.ps1` (agent discovery via REST)

## Docker Multi-Stage Build

Build order: React → .NET → Runtime

- Frontend: `deployment/docker/frontend.Dockerfile`
- Backend: `deployment/docker/backend.Dockerfile`
- Custom npm registries: Add `.npmrc` to `frontend/` directory

## AI Foundry Resource Configuration

**Auto-discovery** (`azd up`): Searches subscription for AI Foundry resources → prompts to select if multiple → discovers agents via REST API → configures RBAC.

**Change resource**: Run `azd provision` to re-run discovery, or:
```powershell
azd env set AI_FOUNDRY_RESOURCE_GROUP <rg>
azd provision
```

## Container Infrastructure

- **Health Probes**: Liveness (`GET /api/health` every 30s) and startup (`GET /api/health` every 10s, 5s initial delay) probes configured on the Container App
- **ACR Pull**: Uses a user-assigned managed identity with `AcrPull` role — no admin credentials or secrets. The MI is created in `main-infrastructure.bicep` before the Container App, avoiding the chicken-and-egg problem.
- **Resource Defaults**: 0.5 vCPU, 1GB RAM, 0-3 replicas (all parameterized in `container-app.bicep`)

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `VITE_ENTRA_SPA_CLIENT_ID not set` | Run `azd up` to generate `.env` files |
| `AI_AGENT_ENDPOINT not configured` | Run `azd provision` to re-discover AI Foundry |
| No AI Foundry resources found | Create at https://ai.azure.com |
| Multiple AI Foundry resources | Run `azd provision` to select different resource |
| Container not updating | Check `az containerapp logs show --name $app --resource-group $rg` |
| Container fails health check | Verify `/api/health` endpoint returns 200 — check container logs for startup errors |

## Useful Commands

```powershell
# Check current container image
az containerapp show --name $app --resource-group $rg `
    --query "properties.template.containers[0].image"

# View container logs
az containerapp logs show --name $app --resource-group $rg --tail 100

# Check RBAC assignments
$principalId = az containerapp show --name $app --resource-group $rg `
    --query "identity.principalId" -o tsv
az role assignment list --assignee $principalId
```

---

## Preprovision Hook Details

**File**: `deployment/hooks/preprovision.ps1`

**What it does**:
1. Discovers AI Foundry resources in subscription (prompts if multiple)
2. Discovers agents via REST API using `Get-AIFoundryAgents.ps1`
3. Auto-detects tenant ID
4. Sets azd environment variables

**Note**: Entra app registration is handled by Bicep (`infra/entra-app.bicep`), not this hook.

## Postprovision Hook Details

**File**: `deployment/hooks/postprovision.ps1`

**What it does**:
1. Sets `identifierUri` (`api://{clientId}`) on Entra app — can't be done in Bicep because it references the auto-generated `appId`
2. Updates Entra app redirect URIs (localhost + Container App FQDN)
3. Assigns Cognitive Services User role to Container App's managed identity on AI Foundry resource (via Azure CLI, not Bicep)
4. Generates local dev config files (`.env.local` for frontend, `.env` for backend)

**Why RBAC via CLI?**: Using Azure CLI for role assignment prevents azd from tracking the external AI Foundry resource group, avoiding accidental deletion on `azd down`.

## Predeploy Hook Details

**File**: `deployment/hooks/predeploy.ps1`

**What it does**:
1. Detects if Docker is available and running
2. Uses local Docker build + push if available (~2 min)
3. Falls back to ACR cloud build if Docker unavailable (~4-5 min)
4. Updates Container App with new image (if it exists)
5. Sets `SERVICE_WEB_IMAGE_NAME` env var for Bicep

## Dockerfile Example

**File**: `deployment/docker/frontend.Dockerfile` (production build)

```dockerfile
# Stage 1: Build React Frontend
FROM node:22-alpine AS frontend-builder
ARG ENTRA_SPA_CLIENT_ID
ARG ENTRA_TENANT_ID
WORKDIR /app/frontend
COPY frontend/ ./
RUN npm ci
# Remove local .env files to prevent localhost config
RUN rm -f .env.local .env.development .env
ENV NODE_ENV=production
ENV VITE_ENTRA_SPA_CLIENT_ID=$ENTRA_SPA_CLIENT_ID
ENV VITE_ENTRA_TENANT_ID=$ENTRA_TENANT_ID
RUN npm run build

# Stage 2: Build .NET Backend
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS backend-builder
WORKDIR /app
COPY backend/WebApp.sln ./
COPY backend/WebApp.Api/WebApp.Api.csproj ./backend/WebApp.Api/
COPY backend/WebApp.ServiceDefaults/WebApp.ServiceDefaults.csproj ./backend/WebApp.ServiceDefaults/
RUN dotnet restore backend/WebApp.Api/WebApp.Api.csproj
COPY backend/ ./backend/
RUN dotnet publish backend/WebApp.Api/WebApp.Api.csproj -c Release -o /app/publish

# Stage 3: Runtime - Single container serving API + static files
FROM mcr.microsoft.com/dotnet/aspnet:9.0-alpine
WORKDIR /app
COPY --from=backend-builder /app/publish ./
COPY --from=frontend-builder /app/frontend/dist ./wwwroot
EXPOSE 8080
ENV ASPNETCORE_URLS=http://+:8080
ENV ASPNETCORE_ENVIRONMENT=Production
ENTRYPOINT ["dotnet", "WebApp.Api.dll"]
```

## Related Skills

- **writing-csharp-code** - Backend coding patterns for Container App configuration
- **writing-bicep-templates** - Infrastructure templates for Azure resources
- **troubleshooting-authentication** - Entra ID and RBAC debugging

## Official Documentation

| Topic | URL |
|-------|-----|
| **Azure Container Apps** | https://learn.microsoft.com/azure/container-apps/overview |
| **Container Apps quickstart** | https://learn.microsoft.com/azure/container-apps/quickstart-portal |
| **Azure Developer CLI (azd)** | https://learn.microsoft.com/azure/developer/azure-developer-cli/overview |
| **azd templates** | https://learn.microsoft.com/azure/developer/azure-developer-cli/azd-templates |
| **Azure AI Foundry overview** | https://learn.microsoft.com/azure/ai-foundry/what-is-ai-foundry |
| **AI Foundry Agent Service** | https://learn.microsoft.com/azure/ai-foundry/agents/overview |
| **Managed Identity** | https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/overview |
| **Cognitive Services RBAC** | https://learn.microsoft.com/azure/ai-services/authentication |
