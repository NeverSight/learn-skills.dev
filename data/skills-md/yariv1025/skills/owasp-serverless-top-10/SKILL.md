---
name: owasp-serverless-top-10
description: "OWASP Serverless Top 10 - prevention, detection, and remediation for serverless (Lambda, Functions) security. Use when building or reviewing serverless apps - event injection, over-permissioned functions, insecure deps, secrets, config, and other serverless-specific interpretations of the Web Top 10."
---

# OWASP Serverless Top 10

This skill encodes the OWASP Top 10 Serverless Interpretation for secure serverless design and review. References are loaded per risk. Based on OWASP Top 10 Serverless Interpretation 2018. See the [official PDF](https://github.com/OWASP/Serverless-Top-10-Project/raw/master/OWASP-Top-10-Serverless-Interpretation-en.pdf) for the exact 10 categories.

## When to Read Which Reference

| Risk | Read |
|------|------|
| SL1 Injection (Serverless) | [references/sl01-injection.md](references/sl01-injection.md) |
| SL2 Broken Authentication (Serverless) | [references/sl02-broken-auth.md](references/sl02-broken-auth.md) |
| SL3 Sensitive Data Exposure (Serverless) | [references/sl03-sensitive-data-exposure.md](references/sl03-sensitive-data-exposure.md) |
| SL4 XML External Entities (Serverless) | [references/sl04-xxe.md](references/sl04-xxe.md) |
| SL5 Broken Access Control (Serverless) | [references/sl05-broken-access-control.md](references/sl05-broken-access-control.md) |
| SL6 Security Misconfiguration (Serverless) | [references/sl06-misconfiguration.md](references/sl06-misconfiguration.md) |
| SL7 XSS (Serverless) | [references/sl07-xss.md](references/sl07-xss.md) |
| SL8 Insecure Deserialization (Serverless) | [references/sl08-insecure-deserialization.md](references/sl08-insecure-deserialization.md) |
| SL9 Using Components with Known Vulnerabilities (Serverless) | [references/sl09-vulnerable-components.md](references/sl09-vulnerable-components.md) |
| SL10 Insufficient Logging and Monitoring (Serverless) | [references/sl10-logging-monitoring.md](references/sl10-logging-monitoring.md) |

## Quick Patterns

- Validate and sanitize event input (injection); use least privilege for function IAM; avoid hardcoded secrets; secure config and dependencies; enable logging and monitoring.

## Quick Reference / Examples

| Task | Approach |
|------|----------|
| Prevent event injection | Validate/sanitize all event data (API Gateway, S3, SNS). See [SL1](references/sl01-injection.md). |
| Least privilege IAM | Scope function roles to exact resources needed. See [SL5](references/sl05-broken-access-control.md). |
| Manage secrets | Use Secrets Manager/Parameter Store, not env vars. See [SL3](references/sl03-sensitive-data-exposure.md). |
| Secure dependencies | Pin versions, scan for vulnerabilities. See [SL9](references/sl09-vulnerable-components.md). |
| Enable logging | CloudWatch/X-Ray for all functions. See [SL10](references/sl10-logging-monitoring.md). |

**Safe - input validation in Lambda:**
```python
import json
def handler(event, context):
    body = json.loads(event.get("body", "{}"))
    user_id = body.get("user_id", "")
    if not user_id.isalnum() or len(user_id) > 36:
        return {"statusCode": 400, "body": "Invalid user_id"}
    # Proceed with validated input
```

**Safe - least privilege IAM policy:**
```yaml
# serverless.yml
provider:
  iam:
    role:
      statements:
        - Effect: Allow
          Action: dynamodb:GetItem
          Resource: arn:aws:dynamodb:*:*:table/users
```

**Unsafe - overly permissive IAM:**
```yaml
# NEVER do this
statements:
  - Effect: Allow
    Action: "*"
    Resource: "*"
```

## Workflow

Load the reference for the risk you are addressing. Confirm exact risk names from the official OWASP Serverless Top 10 PDF.
