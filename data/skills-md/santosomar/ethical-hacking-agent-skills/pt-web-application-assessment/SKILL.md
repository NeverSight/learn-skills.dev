---
name: pt-web-application-assessment
description: Performs authorized web application and API penetration testing with focus on OWASP-style risks and business logic flaws. Use when assessing websites, web APIs, authentication flows, session handling, and input validation.
---

# Web Application Assessment

## Authorized Use Only

Test only approved applications, domains, and endpoints. Respect rate limits and data handling constraints. Use non-destructive proofs and avoid unauthorized data extraction.

## Objectives

1. Identify exploitable weaknesses in web apps and APIs.
2. Validate authentication, authorization, session, and input controls.
3. Prioritize findings by exploitability and business impact.

## Workflow

1. Map attack surface:
   - Endpoints, parameters, methods, auth requirements, role boundaries
   - Hidden/admin routes, API schema, and third-party integrations
2. Test control families:
   - Authentication and session management
   - Authorization and access control (horizontal/vertical)
   - Input handling and output encoding
   - Business logic and workflow abuse
3. Validate high-impact classes:
   - Injection paths, XSS, access control failures, insecure object access
   - Sensitive data exposure, misconfiguration, weak secrets handling
4. Confirm exploitability:
   - Use constrained PoCs and reproducible steps
   - Document bypass conditions and security control failures
5. Produce remediation guidance:
   - Secure coding fixes plus operational controls
   - Regression test cases to prevent reintroduction

## Output Template

```markdown
# Web App Assessment Output

## Coverage
- Application/API in scope:
- Roles tested:
- Key workflows:

## Findings
- Finding:
  - Endpoint/feature:
  - Preconditions:
  - Evidence:
  - Impact:
  - Fix recommendation:
  - Regression test idea:

## Attack Path Summary
- Initial condition:
- Exploit chain:
- Business consequence:
```

## Quality Checks

- Findings include exact endpoint/workflow context.
- PoCs remain non-destructive and reproducible.
- Recommendations include both code and configuration controls.
