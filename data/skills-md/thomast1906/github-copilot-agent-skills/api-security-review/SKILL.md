---
name: api-security-review
description: Reviews Azure API Management configurations for security vulnerabilities, OWASP API Security Top 10 compliance, VNet Internal mode validation, Private Link verification, and Azure Security Benchmark alignment. Use when performing security audits, pre-deployment validation, or compliance reviews.
license: MIT
metadata:
  author: Azure API Marketplace Team
  version: "1.0"
  last-updated: "2026-01-29"
  azure-services: "api-management, security-center"
  compliance-frameworks: "owasp-api-top10,azure-security-benchmark,cis-azure"
---

# API Security Review Skill

Performs comprehensive security reviews of Azure API Management configurations, policies, and network architecture with focus on OWASP API Security Top 10 and Azure Security Benchmark.

## When to Use This Skill

Activate this skill when users need:

- **Security audits**: Comprehensive review of APIM configuration and policies
- **Pre-deployment validation**: Security checklist before production deployment
- **Compliance reviews**: OWASP API Top 10, Azure Security Benchmark, CIS Azure alignment
- **Vulnerability assessments**: Identify security gaps in authentication, network, policies
- **Incident response**: Review configuration after security incident
- **Architecture validation**: Verify VNet Internal mode, Private Link, authentication setup

---

## Security Review Framework

### 1. OWASP API Security Top 10 (2023 RC)

| ID | Threat | APIM Mitigation |
|----|--------|-----------------|
| **API1** | Broken Object Level Authorization | Policy: validate-jwt + check user claims for resource ownership |
| **API2** | Broken Authentication | Policy: OAuth 2.0 (validate-jwt), no plaintext credentials |
| **API3**| Broken Object Property Level Authorization | Policy: Validate input/output schemas, mask sensitive fields |
| **API4** | Unrestricted Resource Consumption | Policy: rate-limit-by-key (per user/subscription), quota enforcement |
| **API5** | Broken Function Level Authorization | Policy: Validate JWT scopes/roles per operation |
| **API6** | Unrestricted Access to Sensitive Business Flows | Policy: Advanced rate limiting, CAPTCHA integration |
| **API7** | Server Side Request Forgery (SSRF) | Network: VNet Internal mode, Private Link to backends |
| **API8** | Security Misconfiguration | Infrastructure: TLS 1.3, disable weak ciphers, NSG rules |
| **API9** | Improper Inventory Management | Governance: Azure API Center, version tracking, deprecation |
| **API10** | Unsafe Consumption of APIs | Policy: Validate backend responses, timeout policies |

---

## Security Controls Checklist

**See [references/SECURITY_CONTROLS.md](references/SECURITY_CONTROLS.md) for complete 60+ control checklist across 9 categories**

### Quick Control Summary

1. **Network Security (NS-)**: VNet Internal, Private Link, NSG, no public IPs
2. **Identity & Access (IA-)**: OAuth 2.0, MFA, PIM, no service accounts
3. **Data Protection (DP-)**: TLS 1.3, Key Vault, no PII in logs
4. **Logging & Threat (LT-)**: App Insights, correlation IDs, SIEM integration
5. **Identity Management (IM-)**: Managed Identity, RBAC, least privilege
6. **Recovery (RA-)**: Backups, zone redundancy, DR plan
7. **Governance (GS-)**: API Center, policy enforcement, compliance
8. **Posture (PS-)**: Azure Policy, Defender for APIs, vulnerability scanning
9. **DevSecOps (DV-)**: APIOps, IaC security, secret scanning

---

## Important: MCP Tools (ALWAYS Use)

### 1. Call Security Best Practices FIRST

```
Tool: mcp_azure_mcp_get_azure_bestpractices
Intent: "Azure API Management security best practices"
```

### 2. Search Security Documentation

```
Tool: mcp_azure_mcp_documentation search
Query: "APIM security best practices OWASP"
```

### 3. Query Existing Resources (If Reviewing Deployed Environment)

```
Tool: azure_resources-query_azure_resource_graph
Intent: "Get API Management instances with network configuration and SKU details"
```

---

## Critical Security Validations

### 1. VNet Internal Mode Validation

**Check**: APIM instances deployed in VNet Internal mode (no public IP)

```kql
// Azure Resource Graph Query
resources
| where type == 'microsoft.apimanagement/service'
| extend vnetType = properties.virtualNetworkType
| where vnetType != 'Internal'
| project name, resourceGroup, location, vnetType, sku=properties.sku.name
```

**Expected**: `vnetType == 'Internal'` for all production APIM instances

**Risk if External**: Gateway endpoint exposed to public internet, larger attack surface

---

### 2. Private Link Validation

**Check**: Azure Front Door connects to APIM via Private Link (not public origin)

**Validation Steps**:
1. Front Door origin type = `Private Link` (not `Custom` or `Public`)
2. Private Link target = APIM resource ID
3. Private Link status = `Approved` (not `Pending`)
4. APIM has no public DNS record resolving to public IP

**Risk if Public**: Traffic goes over public internet, no zero-trust architecture

---

### 3. Authentication Configuration

**Check**: APIs use OAuth 2.0 (validate-jwt policy) or subscription keys (not both for sensitive APIs)

**Policy Review**:
```xml
<!-- GOOD: OAuth for sensitive APIs -->
<validate-jwt header-name="Authorization">
    <openid-config url="https://login.microsoftonline.com/{tenant}/..." />
    <required-claims>
        <claim name="scp" match="any">
            <value>api.read</value>
        </claim>
    </required-claims>
</validate-jwt>

<!-- BAD: No authentication -->
<policies>
    <inbound>
        <base />
        <!-- No validate-jwt or check-header -->
    </inbound>
</policies>
```

**Risk if Missing**: Unauthenticated access to sensitive data, API abuse

---

### 4. Rate Limiting Configuration

**Check**: All APIs have rate limiting (`rate-limit-by-key` or `quota-by-key`)

**Policy Review**:
```xml
<!-- GOOD: Per-user rate limiting -->
<rate-limit-by-key calls="1000" renewal-period="3600" 
                   counter-key="@((string)context.Variables['userId'])" />

<!-- BAD: No rate limiting -->
<policies>
    <inbound>
        <base />
        <!-- No rate-limit-by-key -->
    </inbound>
</policies>
```

**Risk if Missing**: API4 Unrestricted Resource Consumption, DDoS vulnerability

---

### 5. TLS Configuration

**Check**: TLS 1.2+ only, no SSL 3.0/TLS 1.0/TLS 1.1

**Azure Portal Validation**:
- APIM → Security → Protocols → TLS 1.0 **Disabled**
- APIM → Security → Protocols → TLS 1.1 **Disabled**
- APIM → Security → Protocols → SSL 3.0 **Disabled**
- APIM → Security → Ciphers → Weak ciphers **Disabled**

**Risk if Enabled**: Vulnerable to BEAST, POODLE, CRIME attacks

---

### 6. Secret Management

**Check**: All secrets/certificates stored in Azure Key Vault (not in policies or code)

**Policy Review**:
```xml
<!-- GOOD: Secret from Key Vault -->
<set-header name="X-API-Key">
    <value>{{api-backend-key}}</value> <!-- Named value linked to Key Vault -->
</set-header>

<!-- BAD: Hardcoded secret -->
<set-header name="X-API-Key">
    <value>sk-abc123xyz789</value>
</set-header>
```

**Risk if Hardcoded**: Secret exposure in logs, code repositories, APIM exports

---

### 7. CORS Configuration

**Check**: CORS policies have specific origins (not `*` wildcard for production)

```xml
<!-- GOOD: Specific origins -->
<cors allow-credentials="true">
    <allowed-origins>
        <origin>https://app.example.com</origin>
    </allowed-origins>
</cors>

<!-- Warning: ACCEPTABLE FOR DEV: Wildcard -->
<cors allow-credentials="false">
    <allowed-origins>
        <origin>*</origin>
    </allowed-origins>
</cors>

<!-- BAD: Wildcard with credentials -->
<cors allow-credentials="true">
    <allowed-origins>
        <origin>*</origin> <!-- Security risk! -->
    </allowed-origins>
</cors>
```

**Risk**: CSRF attacks, credential theft if misconfigured

---

### 8. Error Response Validation

**Check**: Error responses don't leak sensitive information (stack traces, internal IPs)

**Policy Review**:
```xml
<!-- GOOD: Generic error -->
<on-error>
    <set-body>@{
        return new JObject(
            new JProperty("error", "Internal server error"),
            new JProperty("correlationId", context.Variables["correlationId"])
        ).ToString();
    }</set-body>
</on-error>

<!-- BAD: Detailed error -->
<on-error>
    <set-body>@{
        return context.LastError.Message; // Might contain stack trace, DB connection strings
    }</set-body>
</on-error>
```

**Risk**: Information disclosure (API3, API8)

---

## Security Review Output Format

When performing security review, structure findings as:

### Finding: [Title]
- **Severity**: Critical | High | Medium | Low
- **OWASP Mapping**: API1, API4, API8, etc.
- **Azure Security Benchmark**: NS-1, DP-2, IA-3, etc.
- **Current State**: What was found
- **Risk**: Impact if not fixed
- **Remediation**: Step-by-step fix with code examples
- **Microsoft Docs**: Link to official guidance
- **Priority**: Immediate | Before Production | Post-Launch

**Example**:

### Finding: VNet External Mode Detected

- **Severity**: **Critical**
- **OWASP Mapping**: API7 (SSRF), API8 (Security Misconfiguration)
- **Azure Security Benchmark**: NS-1 (Network Segmentation)
- **Current State**: APIM instance `apim-api-marketplace-prod-uks` deployed in VNet External mode with gateway endpoint `10.2.1.4` exposed via public IP
- **Risk**: Gateway endpoint accessible from public internet, no network isolation, vulnerable to DDoS bypassing Front Door
- **Remediation**:
  1. Redeploy APIM in VNet Internal mode:
     ```bash
     az apim update --name apim-api-marketplace-prod-uks --resource-group rg-apim-prod-uks \
       --virtual-network-type Internal
     ```
  2. Update Front Door origin to use Private Link (not public IP)
  3. Verify no public DNS resolution: `nslookup apim-api-marketplace-prod-uks.azure-api.net` should return internal IP only
- **Microsoft Docs**: [APIM VNet Internal Mode](https://learn.microsoft.com/azure/api-management/api-management-using-with-vnet?tabs=stv2#virtual-network-modes)
- **Priority**: **Immediate** (block production deployment)

---

## Azure Security Benchmark Quick Reference

| Control ID | Category | Requirement | APIM Implementation |
|------------|----------|-------------|---------------------|
| **NS-1** | Network Segmentation | Isolate workloads | VNet Internal mode |
| **NS-2** | Private Connectivity | Private Link/Endpoints | Front Door → APIM Private Link |
| **NS-4** | DDoS Protection | Enable DDoS Standard or ingress with DDoS | Front Door Premium (DDoS included) |
| **IA-2** | Secure Authentication | OAuth/MFA | validate-jwt with Entra ID |
| **IA-5** | MFA Enforcement | Require MFA | Entra ID Conditional Access |
| **DP-1** | Data at Rest Encryption | Encrypt sensitive data | Azure Managed Disks encryption |
| **DP-3** | Data in Transit Encryption | TLS 1.2+ | APIM TLS 1.3, disable weak protocols |
| **DP-4** | Encryption Key Management | Azure Key Vault | All secrets in Key Vault |
| **LT-1** | Centralized Logging | Log all security events | App Insights, Azure Monitor |
| **LT-4** | Audit Logging | Tamper-proof audit trail | Azure Activity Log, diagnostic logs |
| **IM-1** | Managed Identities | Avoid service accounts | APIM Managed Identity |
| **IM-3** | Least Privilege | RBAC | Custom roles per environment |
| **GS-1** | Policy Enforcement | Azure Policy | Require VNet Internal, TLS 1.2+ |

---

## Related Skills

- **apim-policy-authoring** - Review policies created by this skill for security
- **azure-apim-architecture** - Understand architecture security decisions
- **apiops-deployment** - Integrate security checks into CI/CD pipeline

---

## Microsoft Documentation

- [APIM Security Best Practices](https://learn.microsoft.com/azure/api-management/security-controls-policy)
- [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x00-header/)
- [Azure Security Benchmark](https://learn.microsoft.com/security/benchmark/azure/overview)
- [Private Link Security](https://learn.microsoft.com/azure/private-link/private-link-overview)
- [APIM VNet Integration](https://learn.microsoft.com/azure/api-management/api-management-using-with-vnet)

---

**Skill Version**: 1.0  
**Last Updated**: 29 January 2026  
**Primary Knowledge**: SECURITY_CONTROLS_CHECKLIST.md, [references/SECURITY_CONTROLS.md](references/SECURITY_CONTROLS.md)