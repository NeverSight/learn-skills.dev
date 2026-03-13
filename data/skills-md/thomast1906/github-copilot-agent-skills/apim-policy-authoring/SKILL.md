---
name: apim-policy-authoring
description: Creates production-ready Azure API Management policy XML for authentication (OAuth 2.0, JWT validation, subscription keys), rate limiting, CORS configuration, error handling, and API transformations. Use when implementing API security, access control, or request/response processing logic.
license: MIT
metadata:
  author: Azure API Marketplace Team
  version: "1.0"
  last-updated: "2026-01-29"
  azure-services: "api-management"
---

# APIM Policy Authoring Skill

Generates production-ready Azure API Management policy XML with authentication, rate limiting, CORS, error handling, correlation IDs, and security headers.

## When to Use This Skill

Activate this skill when users need:

- **Authentication policies**: OAuth 2.0, JWT validation, hybrid auth with subscription keys
- **Rate limiting**: Per-user or per-subscription throttling
- **CORS configuration**: Cross-origin access for browser-based clients
- **Error handling**: Standardized error responses with correlation IDs
- **Request/response transformation**: Header manipulation, body transformations
- **Security headers**: X-Content-Type-Options, X-Frame-Options, etc.

---

## Policy Templates

**See [references/POLICY_TEMPLATES.md](references/POLICY_TEMPLATES.md) for complete production-ready XML templates:**

1. **Hybrid Authentication** - OAuth + subscription key fallback for public APIs
2. **OAuth Only** - Internal corporate APIs with Entra ID
3. **Subscription Key Only** - Simple public read-only APIs

---

## Policy Execution Flow

```
INBOUND → BACKEND → OUTBOUND → ON-ERROR

1. INBOUND: Authentication, rate limiting, CORS, headers
2. BACKEND: Forwarding, retry, circuit breaker
3. OUTBOUND: Response transform, security headers, cleanup
4. ON-ERROR: Structured errors, logging, correlation ID
```

---

## Important: MCP Tools (ALWAYS Use Before Writing Policies)

### 1. Call Best Practices FIRST

**Before ANY policy generation**, call:

```
Tool: mcp_azure_mcp_get_azure_bestpractices
Intent: "Azure API Management policy best practices for [authentication|rate-limiting|CORS|error-handling]"
```

### 2. Search Documentation

For specific policy elements:

```
Tool: mcp_azure_mcp_documentation search
Query: "APIM validate-jwt policy reference"
```



### 1. JWT Validation with Entra ID
```xml
<validate-jwt header-name="Authorization">
    <openid-config url="https://login.microsoftonline.com/{tenant}/v2.0/.well-known/openid-configuration" />
    <audiences>
        <audience>api://{client-id}</audience>
    </audiences>
</validate-jwt>
```

### 2. Per-User Rate Limiting
```xml
<set-variable name="userId" value="@(context.Request.Headers.GetValueOrDefault('Authorization','').AsJwt()?.Subject)" />
<rate-limit-by-key calls="1000" renewal-period="3600" counter-key="@((string)context.Variables['userId'])" />
```

### 3. Correlation ID Generation
```xml
<set-variable name="correlationId" value="@(Guid.NewGuid().ToString())" />
<set-header name="X-Correlation-ID" exists-action="override">
    <value>@((string)context.Variables["correlationId"])</value>
</set-header>
```

### 4. Standardized Error Response
```xml
<on-error>
    <set-body>@{
        return new JObject(
            new JProperty("error", new JObject(
                new JProperty("code", context.LastError.Source),
                new JProperty("message", context.LastError.Message),
                new JProperty("correlationId", context.Variables["correlationId"]),
                new JProperty("timestamp", DateTime.UtcNow.ToString("o"))
            ))
        ).ToString();
    }</set-body>
</on-error>
```

### 5. Security Headers
```xml
<set-header name="X-Content-Type-Options" exists-action="override">
    <value>nosniff</value>
</set-header>
<set-header name="X-Frame-Options" exists-action="override">
    <value>DENY</value>
</set-header>
<set-header name="Strict-Transport-Security" exists-action="override">
    <value>max-age=31536000; includeSubDomains</value>
</set-header>
```

---

## Authentication Decision Matrix

| API Type | Authentication | Rate Limit | Use Case |
|----------|----------------|------------|----------|
| **Public Read-Only** | Subscription Keys | 500 req/hour | Weather API, Public Holidays |
| **Internal Corporate** | OAuth (Entra ID) | 10,000 req/hour | Employee Directory, HR Systems |
| **Sensitive Public** | OAuth (Entra External ID) | 1,000 req/hour | Payment, Health Records |
| **Hybrid** | OAuth + Keys Fallback | 1,000/500 req/hour | APIs with free/premium tiers |

---

## Policy Validation Checklist

Before deploying, verify:

- **Correlation ID**: Generated in `<inbound>`, included in response + error
- **Authentication**: JWT validation or subscription key check
- **Rate limiting**: Configured with appropriate limits
- **Error handling**: `<on-error>` block with structured JSON
- **Security headers**: X-Content-Type-Options, X-Frame-Options, HSTS
- **Backend cleanup**: Remove `X-Powered-By`, `Server` in `<outbound>`
- **XML validity**: Well-formed, no unclosed tags
- **Testing**: Valid/invalid tokens, rate limit exceeded

---

## Related Skills

- **azure-apim-architecture** - Understand architecture before policy authoring
- **api-security-review** - Validate security after policy creation

---

## Microsoft Documentation

- [Policy Reference](https://learn.microsoft.com/azure/api-management/api-management-policies)
- [validate-jwt](https://learn.microsoft.com/azure/api-management/validate-jwt-policy)
- [rate-limit-by-key](https://learn.microsoft.com/azure/api-management/rate-limit-by-key-policy)
- [CORS](https://learn.microsoft.com/azure/api-management/cors-policy)
- [Policy Expressions](https://learn.microsoft.com/azure/api-management/api-management-policy-expressions)

---

**Skill Version**: 1.0  
**Last Updated**: 29 January 2026  
**Primary Knowledge**: APIM_PLATFORM_BASELINE_POLICIES.md, [references/POLICY_TEMPLATES.md](references/POLICY_TEMPLATES.md)
