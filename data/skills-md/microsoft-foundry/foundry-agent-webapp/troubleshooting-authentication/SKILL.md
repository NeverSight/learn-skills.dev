---
name: troubleshooting-authentication
description: Provides authentication troubleshooting for MSAL, JWT, and Entra ID. Use when debugging 401 errors, token issues, MSAL configuration problems, or credential failures in this repository.
---

# Authentication Troubleshooting

## Architecture

1. Browser → MSAL.js (PKCE flow) → JWT with `Chat.ReadWrite` scope
2. Frontend → Backend (JWT Bearer token)
3. Backend → Foundry Agent Service (ManagedIdentityCredential)

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| 401 on `/api/*` | Token missing scope | Verify `Chat.ReadWrite` scope in token |
| `ManagedIdentityCredential` error locally | Wrong environment | Set `ASPNETCORE_ENVIRONMENT=Development` |
| Token popup blocked | Browser settings | Allow popups for localhost |
| Silent token fails | No cached token | Fallback to popup (handled by useAuth) |

## Backend: JWT Validation

Accepts both audience formats:

```csharp
options.TokenValidationParameters.ValidAudiences = new[]
{
    builder.Configuration["AzureAd:ClientId"],
    $"api://{builder.Configuration["AzureAd:ClientId"]}"
};
```

## Backend: Credential Strategy

```csharp
TokenCredential credential = env.IsDevelopment()
    ? new ChainedTokenCredential(
        new AzureCliCredential(),
        new AzureDeveloperCliCredential())  // Supports 'azd auth login'
    : new ManagedIdentityCredential();
```

**Local development**: Requires `az login` or `azd auth login` to work.

**Why ChainedTokenCredential**: Avoids `DefaultAzureCredential`'s unpredictable "fail fast" mode. Provides explicit, debuggable credential chain.

## Frontend: MSAL Pattern

```typescript
// Always try silent first
try {
  const { accessToken } = await instance.acquireTokenSilent({
    ...tokenRequest,
    account: accounts[0]
  });
  return accessToken;
} catch {
  // Fallback to popup
  const { accessToken } = await instance.acquireTokenPopup(tokenRequest);
  return accessToken;
}
```

## Debugging Steps

1. **Check token contents**: https://jwt.ms
2. **Verify scope**: Token should have `Chat.ReadWrite`
3. **Check audience**: Should match client ID or `api://{clientId}`
4. **Verify Entra app**: Check redirect URIs in Azure Portal

## Environment Variables

**Frontend** (`.env.local`):
```ini
VITE_ENTRA_SPA_CLIENT_ID=...
VITE_ENTRA_TENANT_ID=...
```

**Backend** (`.env`):
```ini
AzureAd__ClientId=...
AzureAd__TenantId=...
```

**Regenerate**: Run `azd up` to recreate Entra app and `.env` files.

## Related Skills

- **writing-csharp-code** - Backend JWT validation and credential patterns
- **writing-typescript-code** - Frontend MSAL integration and useAuth hook
- **deploying-to-azure** - Entra app provisioning and RBAC configuration
