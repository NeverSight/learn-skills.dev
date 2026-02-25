---
name: security
description: '[Review & Quality] ⚡⚡ Perform security review'
argument-hint: [target]
---

# Security Review: $ARGUMENTS

Perform security review on: $ARGUMENTS

## Summary

**Goal:** Perform a structured security audit on a target codebase area and present findings with severity ratings.

| Step | Action                 | Key Notes                                                                     |
| ---- | ---------------------- | ----------------------------------------------------------------------------- |
| 1    | Scope identification   | Parse target, identify API endpoints, handlers, forms, integrations           |
| 2    | Security checklist     | Input validation, authorization, sensitive data, API security, frontend, auth |
| 3    | Vulnerability patterns | Scan for common anti-patterns (missing auth, injection, XSS, logging secrets) |
| 4    | Report                 | Severity-rated findings with file:line refs, fixes, OWASP references          |
| 5    | Wait for approval      | Present findings before implementing any fixes                                |

**Key Principles:**

- Every finding must have severity rating (Critical/High/Medium/Low/Informational) and code location
- Never implement fixes without explicit user approval
- Check both backend (C#) and frontend (TypeScript) security vectors

## Phase 1: Scope Identification

1. **Parse target** from: $ARGUMENTS
2. **Identify components:**
    - API endpoints (Controllers)
    - Command/Query handlers
    - Frontend forms and inputs
    - Data handling and storage
    - External integrations

## Phase 2: Security Checklist

### Input Validation

- [ ] All user inputs validated in Commands/Queries `Validate()` method
- [ ] XSS protection - no raw HTML rendering of user content
- [ ] SQL/NoSQL injection prevention (parameterized via EF Core/MongoDB driver)
- [ ] File upload validation (type whitelist, size limits, content scanning)
- [ ] URL validation for redirects (prevent open redirect)

### Authorization

- [ ] `[PlatformAuthorize]` attribute on sensitive endpoints
- [ ] Entity-level access checks (company ownership, user permissions)
- [ ] Role-based permissions verified in handlers:
    ```csharp
    RequestContext.HasRole(PlatformRoles.Admin)
    RequestContext.HasRequestAdminRoleInCompany()
    ```
- [ ] Multi-tenancy boundaries respected (CompanyId filtering)
- [ ] Resource ownership validation before modification

### Sensitive Data Protection

- [ ] No secrets in logs or error messages
- [ ] PII properly encrypted at rest
- [ ] Sensitive fields excluded from DTOs/responses
- [ ] Audit logging for sensitive operations
- [ ] No credentials in source code or config files

### API Security

- [ ] CORS properly configured (not `*` in production)
- [ ] Rate limiting on public endpoints
- [ ] Request size limits configured
- [ ] Timeout handling to prevent DoS
- [ ] HTTPS enforced

### Frontend Security

- [ ] No sensitive data in localStorage (use sessionStorage or memory)
- [ ] XSS-safe rendering (no `innerHTML` with user data, use `[textContent]`)
- [ ] CSRF tokens for state-changing operations
- [ ] Proper error messages (no stack traces exposed to users)
- [ ] Secure cookie flags (HttpOnly, Secure, SameSite)

### Authentication

- [ ] Strong password requirements enforced
- [ ] Account lockout after failed attempts
- [ ] Session timeout configured
- [ ] Secure token storage and transmission
- [ ] Password reset flow secure (time-limited tokens)

## Phase 3: Common Vulnerability Patterns

### Look for these anti-patterns:

```csharp
// ❌ Missing authorization
[HttpPost]
public async Task<IActionResult> DeleteUser(string userId) // No [PlatformAuthorize]

// ❌ Missing ownership check
await repository.DeleteAsync(request.Id); // Should verify ownership first

// ❌ Logging sensitive data
logger.LogInformation($"User {email} logged in with password {password}");

// ❌ SQL injection (rare with EF but check raw queries)
context.Database.ExecuteSqlRaw($"SELECT * FROM Users WHERE Id = '{id}'");
```

```typescript
// ❌ XSS vulnerability
element.innerHTML = userInput; // Use textContent instead

// ❌ Sensitive data in localStorage
localStorage.setItem('authToken', token); // Use memory or secure storage
```

## Phase 4: Report

Present findings with:

- **Severity rating:** Critical / High / Medium / Low / Informational
- **Affected code locations** with file:line references
- **Recommended fixes** with code examples
- **OWASP reference** if applicable

### Severity Guidelines:

- **Critical:** Direct data breach, authentication bypass, RCE
- **High:** Privilege escalation, sensitive data exposure
- **Medium:** Missing security controls, information disclosure
- **Low:** Security best practice violations
- **Informational:** Suggestions for defense-in-depth

## Phase 5: Wait for Approval

**CRITICAL:** Present your security findings. Wait for explicit user approval before implementing fixes.

---

Use `/security` skill for comprehensive analysis.

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
