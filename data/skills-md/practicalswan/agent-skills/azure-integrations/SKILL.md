---
name: azure-integrations
description: Azure deployment for web apps — Static Web Apps, App Service, Blob Storage, Bicep/ARM, GitHub Actions CI/CD. Use when deploying Next.js/Vite to Azure or configuring Azure resources for full-stack apps.
license: Complete terms in LICENSE.txt
---



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`


Deployment and integration patterns for Azure cloud services, focusing on web application hosting, CI/CD automation, and infrastructure as code.

## When to Use This Skill

- Deploying Next.js or Vite/React apps to Azure
- Setting up CI/CD workflows with GitHub Actions
- Configuring Azure Static Web Apps or App Service
- Managing Azure Blob Storage for file uploads
- Using Azure Key Vault for secure secrets management
- Setting up Application Insights for monitoring
- Writing Bicep or ARM templates for infrastructure as code
- Integrating Azure Cosmos DB (MongoDB API) with applications


## Available Deployment Scripts

- **[examples/vite-swa-deployment.md](./examples/vite-swa-deployment.md)** - Vite/React to Static Web Apps
- **[examples/nextjs-app-service-deployment.md](./examples/nextjs-app-service-deployment.md)** - Next.js to App Service with Key Vault, App Insights, Storage
- **[scripts/deploy-swa.ps1](./scripts/deploy-swa.ps1)** - PowerShell deployment script for SWA
- **[scripts/deploy-appservice.ps1](./scripts/deploy-appservice.ps1)** - PowerShell deployment script for App Service

## Reference Documentation

- **[references/bicep-quickref.md](./references/bicep-quickref.md)** - Bicep template patterns and syntax
- **[references/github-actions-azure.md](./references/github-actions-azure.md)** - GitHub Actions patterns for Azure deployments

---

## Azure Static Web Apps

### Deployment Setup
```yaml


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

name: Deploy to Azure Static Web Apps

on:
  push:
    branches: [main]
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches: [main]

jobs:
  build_and_deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build and Deploy
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: "upload"
          app_location: "/"
          api_location: "api"
          output_location: "dist"
```

### Configuration (staticwebapp.config.json)
```json
{
  "routes": [
    { "route": "/api/*", "allowedRoles": ["authenticated"] },
    { "route": "/*", "serve": "/index.html", "statusCode": 200 }
  ],
  "navigationFallback": {
    "rewrite": "/index.html",
    "exclude": ["/api/*", "*.{css,js,png,jpg,svg,ico}"]
  },
  "globalHeaders": {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Content-Security-Policy": "default-src 'self'"
  },
  "responseOverrides": {
    "401": { "redirect": "/login", "statusCode": 302 }
  }
}
```

### Best Practices
- Use staging environments for PR previews
- Configure custom domains with SSL
- Set up authentication providers (Azure AD, GitHub, etc.)
- Use API routes for serverless backend functions

---

## Azure App Service

Full end-to-end deployment guide with **Key Vault integration, Application Insights, and Azure Storage** available in [examples/nextjs-app-service-deployment.md](./examples/nextjs-app-service-deployment.md).

### Quick Reference
| Resource | Purpose |
|-----------|---------|
| **App Service Plan** | Linux hosting for Node.js apps |
| **Web App** | Next.js application instance |
| **Key Vault** | Secure secrets management (MongoDB URI, auth secrets) |
| **Storage Account** | File uploads (recipe images) |
| **Application Insights** | Monitoring and telemetry |
| **Managed Identity** | Service-to-service authentication (no passwords) |

### PowerShell Deployment Script
Automated deployment script: **[scripts/deploy-appservice.ps1](./scripts/deploy-appservice.ps1)**
```powershell
.\deploy-appservice.ps1 -AppName "my-app" -ResourceGroup "rg-my-app" -Sku S1 -EnableAppInsights -EnableStorage
```

### Deployment Workflow
```yaml


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

name: Deploy Next.js to App Service

on:
  push:
    branches: [main]

permissions:
  id-token: write   # Required for OIDC authentication

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install and Build
        run: |
          npm ci
          npm run build

      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Deploy to App Service
        uses: azure/webapps-deploy@v3
        with:
          app-name: kitchen-odyssey
          package: .
```

### Key Features Covered in Full Guide
- ✅ Zero-downtime deployments with deployment slots
- ✅ Key Vault integration for secure secrets
- ✅ Managed Identity authentication (no secrets in app settings)
- ✅ Application Insights for monitoring and telemetry
- ✅ Azure Storage for file uploads with CORS
- ✅ Bicep infrastructure as code templates
- ✅ Production-ready security headers
- ✅ Automated CI/CD with GitHub Actions

### App Settings (Key Vault Pattern)
```bash


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

az webapp config appsettings set --name <app-name> --resource-group <rg> --settings \
  AZURE_KEYVAULT_RESOURCEENDPOINT="https://<vault-name>.vault.azure.net" \
  AZURE_CLIENTID="<Managed-Identity-Client-ID>" \
  NEXTAUTH_URL="https://<app-name>.azurewebsites.net" \
  NODE_ENV="production"
```

**Legacy Pattern (not recommended - secrets exposed in app settings):**
```bash


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

az webapp config appsettings set --name <app-name> --resource-group <rg> --settings \
  MONGODB_URI="mongodb+srv://..." \
  NEXTAUTH_SECRET="..."
```


---

## Azure Blob Storage

### Upload Integration
```javascript
import { BlobServiceClient } from '@azure/storage-blob';

const blobServiceClient = BlobServiceClient.fromConnectionString(
  process.env.AZURE_STORAGE_CONNECTION_STRING
);

export async function uploadFile(containerName, fileName, buffer, contentType) {
  const containerClient = blobServiceClient.getContainerClient(containerName);
  await containerClient.createIfNotExists({ access: 'blob' });

  const blockBlobClient = containerClient.getBlockBlobClient(fileName);
  await blockBlobClient.uploadData(buffer, {
    blobHTTPHeaders: { blobContentType: contentType },
  });

  return blockBlobClient.url;
}

export async function deleteFile(containerName, fileName) {
  const containerClient = blobServiceClient.getContainerClient(containerName);
  const blockBlobClient = containerClient.getBlockBlobClient(fileName);
  await blockBlobClient.deleteIfExists();
}

export async function generateSasUrl(containerName, fileName, expiresInMinutes = 60) {
  const containerClient = blobServiceClient.getContainerClient(containerName);
  const blobClient = containerClient.getBlobClient(fileName);

  const sasUrl = await blobClient.generateSasUrl({
    permissions: BlobSASPermissions.parse('r'),
    expiresOn: new Date(Date.now() + expiresInMinutes * 60 * 1000),
  });

  return sasUrl;
}
```

---

## Bicep Templates

### Web App + Cosmos DB
```bicep
@description('The name of the web app')
param appName string

@description('The location for resources')
param location string = resourceGroup().location

@description('The SKU of the App Service Plan')
param sku string = 'B1'

resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: '${appName}-plan'
  location: location
  sku: {
    name: sku
  }
  properties: {
    reserved: true
  }
  kind: 'linux'
}

resource webApp 'Microsoft.Web/sites@2023-01-01' = {
  name: appName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'NODE|20-lts'
      appSettings: [
        { name: 'MONGODB_URI', value: cosmosDb.listConnectionStrings().connectionStrings[0].connectionString }
        { name: 'NODE_ENV', value: 'production' }
      ]
    }
  }
}

resource cosmosDb 'Microsoft.DocumentDB/databaseAccounts@2023-04-15' = {
  name: '${appName}-db'
  location: location
  kind: 'MongoDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    capabilities: [{ name: 'EnableMongo' }]
    locations: [{ locationName: location, failoverPriority: 0 }]
  }
}

output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
```

### Deployment
```bash
az deployment group create \
  --resource-group myResourceGroup \
  --template-file main.bicep \
  --parameters appName=my-recipe-app
```

---

## GitHub Actions CI/CD Patterns

### Multi-Environment Pipeline
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, staging]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npm run lint
      - run: npm run test

  deploy-staging:
    needs: test
    if: github.ref == 'refs/heads/staging'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - uses: azure/webapps-deploy@v3
        with:
          app-name: ${{ secrets.STAGING_APP_NAME }}
          publish-profile: ${{ secrets.STAGING_PUBLISH_PROFILE }}

  deploy-production:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - uses: azure/webapps-deploy@v3
        with:
          app-name: ${{ secrets.PROD_APP_NAME }}
          publish-profile: ${{ secrets.PROD_PUBLISH_PROFILE }}
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| SWA deployment fails | Check `output_location` matches build output directory |
| App Service 500 errors | Check application logs: `az webapp log tail` |
| Blob upload CORS | Configure CORS rules on storage account |
| Bicep deployment error | Validate: `az bicep build --file main.bicep` |
| Environment variables missing | Check App Settings in Azure Portal |
| Cold start latency | Use Always On for App Service, or premium SWA tier |
```

---

## References & Resources

### Documentation
- [Bicep Quick Reference](./references/bicep-quickref.md) — Bicep template patterns, resource declarations, modules, and common Azure resource examples
- [GitHub Actions for Azure](./references/github-actions-azure.md) — GitHub Actions workflows for Azure deployments, OIDC setup, multi-stage pipelines

### Scripts
- [Deploy to Azure SWA](./scripts/deploy-swa.ps1) — PowerShell script to deploy Vite/React or Next.js apps to Azure Static Web Apps

### Examples
- [Vite SWA Deployment Guide](./examples/vite-swa-deployment.md) — End-to-end walkthrough deploying a Vite+React app to Azure Static Web Apps



---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [microsoft-development](../microsoft-development/SKILL.md) | Look up Azure SDK docs and code samples |
| [devops-tooling](../devops-tooling/SKILL.md) | CI/CD pipelines and GitHub Actions for Azure deployments |
| [vite-development](../vite-development/SKILL.md) | Build Vite apps before deploying to Azure SWA |
| [react-development](../react-development/SKILL.md) | Build React apps for Azure deployment targets |

---
