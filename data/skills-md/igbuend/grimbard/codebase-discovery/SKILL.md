---
name: codebase-discovery
description: Generate security-focused DISCOVERY.md for code review and threat modeling. Use when assessing unfamiliar codebases.
disable-model-invocation: true
aliases:
  - security-discovery
  - codebase-security
  - discovery-doc
---

# Codebase Security Discovery

Generate a security-focused DISCOVERY.md for the codebase at $ARGUMENTS.

## When to Use This Skill

- Security assessment of a new codebase
- Threat modeling preparation
- Security-focused code review
- Compliance audit preparation

## Workflow Steps

1. **Discover** - Run file discovery commands at $ARGUMENTS
2. **Analyze** - Examine auth, crypto, validation patterns
3. **Map** - Identify trust boundaries and entry points
4. **Document** - Generate DISCOVERY.md using template below
5. **Verify** - Complete generation checklist

## Discovery Commands

### Security-Relevant Files

```bash
# Find security-critical files
find $ARGUMENTS -type f \( \
  -name "auth*" -o -name "*login*" -o -name "*session*" -o \
  -name "*crypt*" -o -name "*secret*" -o -name "*key*" -o \
  -name "*token*" -o -name "*password*" -o -name "*credential*" -o \
  -name "*.pem" -o -name "*.key" -o -name "*.cert" -o \
  -name "*security*" -o -name "*permission*" -o -name "*role*" -o \
  -name "*sanitiz*" -o -name "*valid*" -o -name "*filter*" \
\) 2>/dev/null | grep -v node_modules | grep -v __pycache__

# Configuration with potential secrets
find $ARGUMENTS -type f \( -name "*.env*" -o -name "*config*" -o -name "*settings*" \) 2>/dev/null | head -20

# API endpoints
grep -r -l "route\|router\|endpoint\|@app\.\|@api\." --include="*.py" --include="*.js" --include="*.ts" --include="*.go" $ARGUMENTS 2>/dev/null | head -20
```

### Analysis Targets

| Area | What to Examine |
|------|-----------------|
| **Dependencies** | Vulnerable packages, outdated versions, unnecessary deps |
| **Trust Boundaries** | HTTP endpoints, file uploads, CLI args, env vars, DB queries, message queues |
| **Auth Flow** | Identity verification, session management, token handling, permission checks, RBAC |

## Security-Enhanced Structure (Based on Claude.md)

```markdown
# [Project Name] - Security Review Documentation

## Overview
Brief description with security context: what the application does, what sensitive data it handles, and its exposure (internal/external/public).

## Technology Stack
- **Language(s)**: [With versions - check for EOL/vulnerable versions]
- **Framework(s)**: [Note known security features/issues]
- **Database**: [Type, version, connection method]
- **Authentication**: [Mechanism used]
- **Cryptographic Libraries**: [Libraries handling crypto operations]

## Security Posture Summary

| Aspect | Status | Notes |
|--------|--------|-------|
| Authentication | [Mechanism] | [Implementation location] |
| Authorization | [RBAC/ABAC/etc.] | [Where enforced] |
| Input Validation | [Centralized/Distributed] | [Key locations] |
| Output Encoding | [Present/Absent] | [Implementation] |
| Cryptography | [Libraries used] | [Algorithms observed] |
| Logging/Audit | [Present/Absent] | [What's logged] |
| Error Handling | [Secure/Leaky] | [Pattern used] |

## Project Structure (Security View)

```

project-root/
├── src/
│   ├── auth/           # [!] Authentication logic
│   ├── middleware/     # [!] Security middleware, validators
│   ├── controllers/    # [!] Input handling, business logic
│   ├── models/         # [!] Data models, ORM queries
│   ├── services/       # External integrations
│   └── utils/
│       ├── crypto.js   # [!] Cryptographic operations
│       └── sanitize.js # [!] Input sanitization
├── config/             # [!] Configuration, potential secrets
└── tests/
    └── security/       # Security-specific tests (if any)

```
[!] = Security-critical directories

## Trust Boundaries

### External Entry Points
| Entry Point | Location | Input Type | Validation |
|-------------|----------|------------|------------|
| REST API | `src/routes/api/` | JSON | [Describe] |
| File Upload | `src/controllers/upload.js` | Multipart | [Describe] |
| WebSocket | `src/ws/handler.js` | Messages | [Describe] |
| GraphQL | `src/graphql/resolvers/` | Queries | [Describe] |

### Internal Trust Boundaries
- **Service-to-Service**: How internal services authenticate
- **Database Access**: Connection handling, query construction
- **Cache Layer**: What's cached, cache poisoning risks
- **Message Queue**: Message validation, serialization

## Attack Surface

### Network Exposure
- **Public Endpoints**: Unauthenticated routes
- **Authenticated Endpoints**: Routes requiring auth
- **Admin Endpoints**: Privileged routes
- **Internal APIs**: Service-to-service communication

### Data Input Vectors
1. **User Input**: Forms, query params, headers
2. **File Input**: Uploads, imports
3. **API Input**: Third-party webhooks, callbacks
4. **Scheduled Input**: Cron jobs, background tasks

## Authentication Flow

### Primary Authentication
```

[Diagram or step-by-step flow]

1. User submits credentials to POST /auth/login
2. Server validates against [user store]
3. [Session/Token] created and returned
4. Subsequent requests authenticated via [header/cookie]

```

**Implementation Files:**
- Login handler: `src/auth/login.js`
- Session management: `src/auth/session.js`
- Auth middleware: `src/middleware/authenticate.js`

### Session Management
- **Type**: [Cookie/JWT/Session ID]
- **Storage**: [Server-side/Client-side]
- **Expiration**: [Duration, renewal policy]
- **Invalidation**: [Logout handling]

### Multi-Factor Authentication
- **Supported**: [Yes/No]
- **Implementation**: [Location if present]

## Authorization Model

### Access Control Type
[RBAC/ABAC/ACL/Custom] implemented in `path/to/authz`

### Roles & Permissions
| Role | Permissions | Definition Location |
|------|-------------|---------------------|
| admin | Full access | `src/config/roles.js` |
| user | Read, write own | `src/config/roles.js` |
| guest | Read public | `src/config/roles.js` |

### Authorization Enforcement Points
- **Route level**: `src/middleware/authorize.js`
- **Controller level**: [If present]
- **Data level**: [Row-level security if present]

## Sensitive Data Handling

### Data Classification
| Data Type | Classification | Storage | Encryption |
|-----------|---------------|---------|------------|
| Passwords | Critical | DB (hashed) | [Algorithm] |
| PII | Sensitive | DB | [At-rest encryption] |
| API Keys | Critical | Env/Vault | [Method] |
| Session Tokens | Sensitive | [Redis/Memory] | [Method] |

### Data Flow
```

[Input] → [Validation] → [Processing] → [Storage]
                ↓
         [Logging - what's logged?]

```

### Secrets Management
- **Location**: Environment variables / Vault / Config files
- **Rotation**: [Policy if any]
- **Access**: [Who/what can access]

## Cryptographic Implementation

### Algorithms in Use
| Purpose | Algorithm | Location | Assessment |
|---------|-----------|----------|------------|
| Password Hashing | [bcrypt/argon2/etc.] | `src/auth/password.js` | [Adequate/Weak] |
| Token Signing | [HS256/RS256/etc.] | `src/auth/jwt.js` | [Adequate/Weak] |
| Data Encryption | [AES-256-GCM/etc.] | `src/utils/crypto.js` | [Adequate/Weak] |
| TLS | [Version] | Server config | [Adequate/Weak] |

### Key Management
- **Storage**: [HSM/Vault/Environment/Hardcoded(!)]
- **Rotation**: [Automated/Manual/None]
- **Derivation**: [KDF used if any]

### Cryptographic Concerns
- [ ] Hardcoded keys or IVs
- [ ] Weak algorithms (MD5, SHA1 for security, DES, RC4)
- [ ] ECB mode usage
- [ ] Predictable random number generation
- [ ] Missing integrity checks (encryption without MAC)

## Input Validation & Output Encoding

### Input Validation
| Input Source | Validation Method | Location |
|--------------|-------------------|----------|
| Query params | [Schema/Manual] | `src/middleware/validate.js` |
| Request body | [Schema/Manual] | `src/middleware/validate.js` |
| File uploads | [Type/Size/Content] | `src/controllers/upload.js` |
| Headers | [Allowlist/None] | [Location] |

### Output Encoding
| Context | Encoding Method | Location |
|---------|-----------------|----------|
| HTML | [Escaped/Template auto-escape] | `src/views/` |
| JSON | [Serializer] | [Framework default] |
| SQL | [Parameterized/ORM] | `src/models/` |
| Shell | [Escaped/Avoided] | [If applicable] |

## Security Controls

### Existing Controls
- [ ] CSRF protection: [Implementation]
- [ ] Rate limiting: [Implementation]
- [ ] CORS policy: [Configuration location]
- [ ] Security headers: [Helmet/manual]
- [ ] SQL injection prevention: [ORM/parameterized]
- [ ] XSS prevention: [CSP/encoding]
- [ ] Path traversal prevention: [Method]

### Logging & Monitoring
- **Security Events Logged**: [Auth failures, access denied, etc.]
- **Log Location**: `path/to/logs` or [external service]
- **Sensitive Data in Logs**: [Yes/No - check for PII leakage]
- **Audit Trail**: [Present/Absent]

### Error Handling
- **Error Response Pattern**: [Generic/Detailed]
- **Stack Traces Exposed**: [Yes/No]
- **Error Logging**: [Implementation]

## External Integrations

| Service | Purpose | Auth Method | Data Exchanged |
|---------|---------|-------------|----------------|
| [Service] | [Purpose] | [API Key/OAuth] | [Data types] |

### Third-Party Risks
- Dependency on external services for security functions
- Data sent to third parties
- Callback/webhook handling

## Dependencies Security

### Critical Dependencies
| Package | Version | Purpose | Known Issues |
|---------|---------|---------|--------------|
| [package] | [version] | [auth/crypto/etc.] | [CVEs if any] |

### Dependency Analysis Commands
```bash
# Node.js
npm audit

# Python
pip-audit / safety check

# Go
govulncheck ./...

# Ruby
bundle audit
```

## Security Testing

### Existing Security Tests

- Location: `tests/security/` or integrated
- Coverage: [Auth, authz, injection, etc.]
- Automation: [CI/CD integration]

### Recommended Test Areas

1. Authentication bypass attempts
2. Authorization boundary testing
3. Input validation fuzzing
4. Session management testing
5. Cryptographic implementation review

## Configuration Security

### Security-Relevant Configuration

| Setting | Location | Current Value | Recommendation |
|---------|----------|---------------|----------------|
| Debug mode | `config/app.js` | [true/false] | false in prod |
| Session timeout | `config/auth.js` | [value] | [recommendation] |
| Password policy | `config/auth.js` | [policy] | [recommendation] |

### Environment Variables

| Variable | Purpose | Sensitivity |
|----------|---------|-------------|
| `DATABASE_URL` | DB connection | High |
| `JWT_SECRET` | Token signing | Critical |
| `API_KEY` | External service | High |

## High-Risk Areas

### Priority Review Targets

1. **[Component]**: [Reason for concern]
2. **[Component]**: [Reason for concern]
3. **[Component]**: [Reason for concern]

### Known Security Debt

- [Issue 1]: [Location, severity, notes]
- [Issue 2]: [Location, severity, notes]

## Quick Reference

### Security-Critical Files

| File | Contains |
|------|----------|
| `src/auth/login.js` | Authentication logic |
| `src/middleware/auth.js` | Auth middleware |
| `src/utils/crypto.js` | Crypto operations |
| `config/security.js` | Security configuration |

### Common Vulnerability Locations

- **SQLi**: `src/models/`, raw query usage
- **XSS**: `src/views/`, dynamic content
- **SSRF**: `src/services/`, URL handling
- **Path Traversal**: `src/controllers/`, file operations
- **Deserialization**: `src/utils/`, object parsing

## Compliance Considerations

If applicable:

- **GDPR**: Data subject rights implementation
- **PCI-DSS**: Cardholder data handling
- **HIPAA**: PHI protection measures
- **SOC 2**: Security controls mapping

```

## Generation Checklist

Before finalizing, verify:
- [ ] All entry points identified
- [ ] Authentication flow fully traced
- [ ] Authorization enforcement points mapped
- [ ] Sensitive data flows documented
- [ ] Cryptographic usage catalogued
- [ ] External integrations listed
- [ ] High-risk areas highlighted
- [ ] Security controls inventory complete

## Success Criteria

A complete DISCOVERY.md enables a security reviewer to:
- Understand the application's security posture in <30 minutes
- Identify all trust boundaries and entry points
- Locate security-critical code files directly
- Know what authentication/authorization mechanisms exist
- Find cryptographic implementations for review

## Output

Save as `DISCOVERY.md` in the repository root at $ARGUMENTS.
