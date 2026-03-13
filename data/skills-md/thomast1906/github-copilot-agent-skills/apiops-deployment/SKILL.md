---
name: apiops-deployment
description: Guides deployment of Azure API Management infrastructure using Infrastructure as Code (Bicep/Terraform), CI/CD pipelines (GitHub Actions/Azure DevOps), and APIOps workflows. Use when deploying APIM, creating pipelines, or implementing dev→test→prod promotion strategies.
license: MIT
metadata:
  author: Azure API Marketplace Team
  version: "1.0"
  last-updated: "2026-01-29"
  azure-services: "api-management, devops, github-actions"
  iac-tools: "bicep, terraform"
---

# APIOps Deployment Skill

Provides Infrastructure as Code (Bicep/Terraform) templates and CI/CD pipeline patterns for deploying Azure API Management following APIOps principles and phased deployment strategies.

## When to Use This Skill

Activate this skill when users need:

- **Infrastructure deployment**: Generate Bicep/Terraform for APIM, Front Door, VNet, supporting services
- **CI/CD pipelines**: Create GitHub Actions or Azure DevOps workflows for APIOps
- **Environment promotion**: Implement dev → test → prod deployment workflows
- **Configuration management**: Environment-specific parameters (dev/test/prod)
- **Disaster recovery**: Backup/restore procedures, blue-green deployments
- **Phased rollout**: Follow deployment planning guide with 7 phases over 17 weeks

---

## Phased Deployment Strategy

**See DEPLOYMENT_PLANNING_GUIDE.md for complete 17-week, 7-phase plan**

### Phase Summary

| Phase | Duration | Focus | Key Deliverables |
|-------|----------|-------|------------------|
| **1** | Week 1-2 | Core Infrastructure | VNet, APIM(dev), Front Door, Key Vault, monitoring |
| **2** | Week 3-4 | Authentication & IAM | Entra ID, Entra External ID, OAuth policies|
| **3** | Week 5-8 | API Onboarding (Dev) | 5 pilot APIs, policies, developer portal |
| **4** | Week 9-10 | Production Infrastructure | APIM(prod) Premium 3u, zone-redundant |
| **5** | Week 11-12 | Production APIs | Migrate 5 pilot APIs, performance testing |
| **6** | Week 13-15 | Governance & Scaling | API Center, additional APIs, APIOps automation |
| **7** | Week 16-17 | Operations Handoff | Runbooks, training, monitoring dashboards |

---

## Important: MCP Tools (ALWAYS Use Before Code Generation)

### 1. Get Azure Verified Modules (AVM)

**BEFORE writing any Bicep**, check for Azure Verified Modules:

```
Tool: azure_bicep-get_azure_verified_module
ResourceType: "Microsoft.ApiManagement/service"
```

**Why**: AVM modules follow Microsoft best practices, reduce code duplication, tested at scale

### 2. Call Deployment Best Practices FIRST

```
Tool: mcp_azure_mcp_get_azure_bestpractices
Intent: "Azure API Management deployment best practices Bicep"
```

### 3. Search Deployment Documentation

```
Tool: mcp_azure_mcp_documentation search
Query: "APIM VNet Internal Bicep deployment"
```

---

## Infrastructure as Code Templates

**See [references/IaC_TEMPLATES.md](references/IaC_TEMPLATES.md) for complete Bicep/Terraform templates**

### Quick Bicep Example: Production APIM

```bicep
param location string = 'uksouth'
param apimName string = 'apim-api-marketplace-prod-uks'
param publisherEmail string = 'admin@example.com'
param publisherName string = 'API Marketplace Team'
param vnetName string = 'vnet-apim-prod-uks'
param subnetName string = 'snet-apim'

resource vnet 'Microsoft.Network/virtualNetworks@2023-04-01' existing = {
  name: vnetName
}

resource apim 'Microsoft.ApiManagement/service@2023-05-01-preview' = {
  name: apimName
  location: location
  sku: {
    name: 'Premium'
    capacity: 3 // Zone-redundant: 3 units across 3 availability zones
  }
  properties: {
    publisherEmail: publisherEmail
    publisherName: publisherName
    virtualNetworkType: 'Internal' // VNet Internal mode
    virtualNetworkConfiguration: {
      subnetResourceId: '${vnet.id}/subnets/${subnetName}'
    }
    customProperties: {
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Protocols.Tls10': 'False'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Protocols.Tls11': 'False'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Protocols.Ssl30': 'False'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Backend.Protocols.Tls10': 'False'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Backend.Protocols.Tls11': 'False'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Backend.Protocols.Ssl30': 'False'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Ciphers.TripleDes168': 'False'
    }
    disableGateway: false
  }
  identity: {
    type: 'SystemAssigned' // Managed Identity for Key Vault access
  }
  zones: [
    '1'
    '2'
    '3'
  ] // Zone redundancy for 99.99% SLA
}

output apimId string = apim.id
output managedIdentityPrincipalId string = apim.identity.principalId
```

**Key Configuration**:
- VNet Internal mode (`virtualNetworkType: 'Internal'`)
- Premium SKU with 3 units (zone-redundant)
- TLS 1.2+ only (disable weak protocols)
- Managed Identity (no service accounts)
- Zones `[1, 2, 3]` for 99.99% SLA

---

## APIOps CI/CD Pipeline Pattern

### GitHub Actions Workflow (Recommended)

```yaml
name: APIOps - Deploy APIM Infrastructure

on:
  workflow_dispatch:
  push:
    branches: [main]
    paths:
      - 'infra/**'
      - '.github/workflows/deploy-infra.yml'

env:
  AZURE_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
  AZURE_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
  
jobs:
  # ===== Dev Environment =====
  deploy-dev:
    runs-on: ubuntu-latest
    environment: development
    steps:
      - uses: actions/checkout@v4
      
      - name: Azure Login
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ env.AZURE_TENANT_ID }}
          subscription-id: ${{ env.AZURE_SUBSCRIPTION_ID }}
      
      - name: Deploy Bicep
        uses: azure/arm-deploy@v2
        with:
          scope: resourcegroup
          resourceGroupName: rg-apim-dev-uks
          template: ./infra/main.bicep
          parameters: ./infra/params/dev.bicepparam
          failOnStdErr: false
      
      - name: Smoke Test
        run: |
          # Verify APIM health endpoint
          curl -f https://management.azure.com/subscriptions/${{ env.AZURE_SUBSCRIPTION_ID }}/resourceGroups/rg-apim-dev-uks/providers/Microsoft.ApiManagement/service/apim-api-marketplace-dev-uks?api-version=2023-05-01-preview \
            -H "Authorization: Bearer $(az account get-access-token --query accessToken -o tsv)"
  
  # ===== Test Environment (After Dev) =====
  deploy-test:
    needs: deploy-dev
    runs-on: ubuntu-latest
    environment: test
    steps:
      # Same steps as dev, use test.bicepparam
      - uses: actions/checkout@v4
      - uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ env.AZURE_TENANT_ID }}
          subscription-id: ${{ env.AZURE_SUBSCRIPTION_ID }}
      - uses: azure/arm-deploy@v2
        with:
          scope: resourcegroup
          resourceGroupName: rg-apim-test-uks
          template: ./infra/main.bicep
          parameters: ./infra/params/test.bicepparam
          failOnStdErr: false
  
  # ===== Production (Manual Approval Required) =====
  deploy-prod:
    needs: deploy-test
    runs-on: ubuntu-latest
    environment:
      name: production
      # GitHub environment protection rule: Require manual approval
    steps:
      - uses: actions/checkout@v4
      - uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ env.AZURE_TENANT_ID }}
          subscription-id: ${{ env.AZURE_SUBSCRIPTION_ID }}
      
      - name: Deploy Production APIM
        uses: azure/arm-deploy@v2
        with:
          scope: resourcegroup
          resourceGroupName: rg-apim-prod-uks
          template: ./infra/main.bicep
          parameters: ./infra/params/prod.bicepparam
          failOnStdErr: false
      
      - name: Production Smoke Test
        run: |
          # Verify Front Door → APIM connectivity
          curl -f https://api.yourdomain.com/health
      
      - name: Tag Release
        run: |
          git tag -a "apim-prod-$(date +%Y%m%d-%H%M%S)" -m "Production deployment"
          git push origin --tags
```

**Key Features**:
- Dev → Test → Prod progression (serial jobs with `needs`)
- Manual approval for production (`environment: production` with protection rules)
- Smoke tests after each deployment
- Git tags for production releases (audit trail)
- Federated credential authentication (no secrets in code)

---

## Environment-Specific Parameters

### dev.bicepparam
```bicep
using './main.bicep'

param location = 'uksouth'
param environment = 'dev'
param apimSku = 'Developer' // £45/month
param apimCapacity = 1
param virtualNetworkType = 'Internal'
param enableFrontDoor = false // Dev: Direct APIM access
param tags = {
  Environment: 'Development'
  ManagedBy: 'IaC'
  CostCenter: 'Engineering'
}
```

### prod.bicepparam
```bicep
using './main.bicep'

param location = 'uksouth'
param environment = 'prod'
param apimSku = 'Premium' // £1,944/month (3 units)
param apimCapacity = 3 // Zone-redundant
param virtualNetworkType = 'Internal'
param enableFrontDoor = true // Prod: Front Door + Private Link
param enableApiCenter = true // £135/month
param tags = {
  Environment: 'Production'
  ManagedBy: 'IaC'
  CostCenter: 'Operations'
  Criticality: 'High'
}
```

**Pattern**: Single `main.bicep` template, environment-specific `.bicepparam` files for configuration

---

## Backup & Restore Procedures

### APIM Backup (Automated)

```bash
#!/bin/bash
# backup-apim.sh - Schedule daily via Azure Automation or GitHub Actions

APIM_NAME="apim-api-marketplace-prod-uks"
RESOURCE_GROUP="rg-apim-prod-uks"
STORAGE_ACCOUNT="stapimproduksbkp"
CONTAINER="apim-backups"
BACKUP_NAME="apim-backup-$(date +%Y%m%d-%H%M%S)"

# Trigger APIM backup to Storage Account
az apim backup create \
  --name "$APIM_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --storage-account-name "$STORAGE_ACCOUNT" \
  --storage-account-container "$CONTAINER" \
  --backup-name "$BACKUP_NAME"

echo "Backup created: $BACKUP_NAME"
```

### APIM Restore (Disaster Recovery)

```bash
#!/bin/bash
# restore-apim.sh - Run during DR scenario

APIM_NAME="apim-api-marketplace-prod-uks"
RESOURCE_GROUP="rg-apim-prod-uks"
STORAGE_ACCOUNT="stapimproduksbkp"
CONTAINER="apim-backups"
BACKUP_NAME="apim-backup-20260128-120000" # Latest successful backup

# Restore APIM from backup
az apim backup restore \
  --name "$APIM_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --storage-account-name "$STORAGE_ACCOUNT" \
  --storage-account-container "$CONTAINER" \
  --backup-name "$BACKUP_NAME"

echo "APIM restored from backup: $BACKUP_NAME"
```

**Backup Retention**:
- Daily backups for 30 days (Azure Storage lifecycle policy)
- Weekly backups for 12 weeks
- Monthly backups for 12 months
- Geo-redundant storage (GRS) to UK West

---

## Deployment Validation Checklist

Before production deployment, verify:

- **Infrastructure Code**: Bicep/Terraform linted and validated (`az bicep build`, `terraform validate`)
- **Network Configuration**: VNet Internal mode, Private Link configured
- **Security**: TLS 1.2+, weak protocols disabled, Key Vault integration
- **Authentication**: OAuth policies deployed, Entra ID/External ID configured
- **Rate Limiting**: All APIs have rate-limit-by-key policies
- **Monitoring**: Application Insights, diagnostic logs, alerts configured
- **Backups**: Automated daily backups to GRS storage
- **Smoke Tests**: Health endpoints responding, Front Door → APIM connectivity verified
- **Manual Approval**: Production deployment requires human approval (GitHub environment protection)
- **Rollback Plan**: Previous Bicep/Terraform state in Git, APIM backup available

---

## Common Deployment Issues & Solutions

### Issue: APIM VNet Integration Fails

**Error**: `The subnet is not valid for API Management instance`

**Solution**:
1. Ensure subnet size ≥ /27 (32 IPs minimum)
2. Subnet must not have any other resources
3. Delegate subnet to `Microsoft.ApiManagement/service`:
   ```bicep
   delegations: [
     {
       name: 'delegation'
       properties: {
         serviceName: 'Microsoft.ApiManagement/service'
       }
     }
   ]
   ```

---

### Issue: Private Link Connection Pending

**Error**: Front Door → APIM Private Link status `Pending Approval`

**Solution**:
1. Approve Private Endpoint connection in APIM:
   ```bash
   az network private-endpoint-connection approve \
     --resource-name apim-api-marketplace-prod-uks \
     --resource-group rg-apim-prod-uks \
     --name <connection-name> \
     --type Microsoft.ApiManagement/service
   ```
2. Verify status:
   ```bash
   az network private-endpoint-connection list \
     --name apim-api-marketplace-prod-uks \
     --resource-group rg-apim-prod-uks \
     --type Microsoft.ApiManagement/service
   ```

---

### Issue: Deployment Takes 45+ Minutes

**Cause**: APIM Premium with zone redundancy takes 30-60 minutes to deploy

**Solution**: Expected behavior. Use incremental deployments:
- Day 1: Deploy APIM infrastructure (wait 45 min)
- Day 2+: Deploy API configurations (fast, minutes)

**Optimization**: Use `--what-if` flag to preview changes without deploying

---

## Related Skills

- **azure-apim-architecture** - Understand architecture before deploying
- **apim-policy-authoring** - Deploy policies as part of APIOps workflow
- **api-security-review** - Validate security before production deployment

---

## Microsoft Documentation

- [APIOps Guide](https://learn.microsoft.com/azure/architecture/example-scenario/devops/automated-api-deployments-apiops)
- [APIM Bicep Reference](https://learn.microsoft.com/azure/templates/microsoft.apimanagement/service)
- [APIM Backup/Restore](https://learn.microsoft.com/azure/api-management/api-management-howto-disaster-recovery-backup-restore)
- [Azure Verified Modules](https://aka.ms/avm)
- [GitHub Actions for Azure](https://learn.microsoft.com/azure/developer/github/github-actions)

---

**Skill Version**: 1.0  
**Last Updated**: 29 January 2026  
**Primary Knowledge**: DEPLOYMENT_PLANNING_GUIDE.md, [references/IaC_TEMPLATES.md](references/IaC_TEMPLATES.md)