---
name: writing-bicep-templates
description: Provides Bicep coding standards for Azure infrastructure in this repository. Use when writing or modifying Bicep files, configuring Container Apps, setting up RBAC, or working with Azure resources.
---

# Bicep Coding Standards

**Goal**: Create consistent, secure Azure infrastructure

## Naming Convention

Use `resourceToken` from `uniqueString()`:

```bicep
var token = toLower(uniqueString(subscription().id, environmentName, location))
name: '${abbrs.appContainerApps}web-${token}'  // ca-web-abc123
```

**Exception**: ACR requires alphanumeric only: `cr${resourceToken}`

## Parameters

Always add `@description()` and use `@allowed()` for constrained values:

```bicep
@description('Environment (dev, prod)')
param environmentName string

@description('Azure region')
@allowed(['eastus2', 'westus2'])
param location string = 'eastus2'
```

## Outputs

Expose key identifiers for `azd` and other modules:

```bicep
output containerAppName string = containerApp.name
output webEndpoint string = 'https://${containerApp.properties.configuration.ingress.fqdn}'
output identityPrincipalId string = containerApp.identity.principalId
```

## Managed Identity

Always use system-assigned identity + output `principalId`:

```bicep
identity: { type: 'SystemAssigned' }
output identityPrincipalId string = resource.identity.principalId
```

## RBAC Assignments

Use `guid()` for names + specify `principalType`:

```bicep
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resource.id, principalId, roleId)
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleId)
    principalId: principalId
    principalType: 'ServicePrincipal'
  }
}
```

## Container Apps

Key settings: System identity + scale-to-zero + HTTPS only:

```bicep
resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  identity: { type: 'SystemAssigned' }
  properties: {
    configuration: {
      ingress: {
        external: true
        targetPort: 8080
        allowInsecure: false
      }
    }
    template: {
      scale: { minReplicas: 0, maxReplicas: 3 }
    }
  }
}
```

## Secrets Pattern

Use Container App secrets + `listCredentials()`:

```bicep
secrets: [{
  name: 'registry-password'
  value: containerRegistry.listCredentials().passwords[0].value
}]
```

## Validation

```powershell
az bicep build --file main.bicep
az deployment group what-if --template-file main.bicep
```

---

## Project-Specific: Module Hierarchy

```
main.bicep (subscription scope)
├─ Resource group
├─ main-infrastructure.bicep (ACR + Container Apps Env + Log Analytics)
├─ main-app.bicep (Container App)
└─ RBAC (Cognitive Services User role)
```

## Project-Specific: Container App Configuration

```bicep
resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  identity: { type: 'SystemAssigned' }
  properties: {
    managedEnvironmentId: containerAppsEnvironmentId
    configuration: {
      ingress: {
        external: true
        targetPort: 8080
        allowInsecure: false
      }
      secrets: [{
        name: 'registry-password'
        value: containerRegistry.listCredentials().passwords[0].value
      }]
    }
    template: {
      containers: [{
        name: 'web'
        image: containerImage
        env: [
          { name: 'ENTRA_SPA_CLIENT_ID', value: entraSpaClientId }
          { name: 'AI_AGENT_ENDPOINT', value: aiAgentEndpoint }
          { name: 'AI_AGENT_ID', value: aiAgentId }
        ]
        resources: { cpu: json('0.5'), memory: '1Gi' }
      }]
      scale: { minReplicas: 0, maxReplicas: 3 }
    }
  }
}

output fqdn string = containerApp.properties.configuration.ingress.fqdn
output identityPrincipalId string = containerApp.identity.principalId
```

## Related Skills

- **deploying-to-azure** - Deployment commands and hook workflow
- **writing-csharp-code** - Backend configuration for Container Apps
- **troubleshooting-authentication** - RBAC and managed identity debugging
