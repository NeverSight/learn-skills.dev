---
name: infra-security-review
description: Security patterns and checklists for reviewing Infrastructure-as-Code. Covers Terraform/OpenTofu state, secrets, network, compute, database, and storage security.
---

# Infrastructure Security Review Patterns

Security checklists and grep patterns for reviewing IaC code. Use these patterns when verifying infrastructure security.

## Security Checklists

### State Backend Security

| Check | Severity | Pattern |
|-------|----------|---------|
| S3 bucket without encryption | Critical | `encrypt = false` or missing |
| Missing state locking | High | No DynamoDB table configured |
| Public bucket policy | Critical | `block_public_*` not all true |
| Missing versioning | Medium | `versioning` not enabled |

### Secret Exposure

| Check | Severity | Pattern |
|-------|----------|---------|
| Hardcoded AWS keys | Critical | `AKIA[0-9A-Z]{16}` |
| Hardcoded passwords | Critical | `password\s*=\s*"[^"]+[^}]"` |
| Database credentials in code | Critical | `DATABASE_URL` with password |
| API keys in variables | High | `api_key`, `secret_key` defaults |

### Network Security

| Check | Severity | Pattern |
|-------|----------|---------|
| SSH open to world | Critical | `0.0.0.0/0` on port 22 |
| Database publicly accessible | Critical | Missing `private_network_uuid` |
| Wide CIDR ranges | Medium | `/8`, `/16` on public resources |
| Missing firewall | High | Droplet without firewall resource |

### Compute Security

| Check | Severity | Pattern |
|-------|----------|---------|
| Root login enabled | High | `PermitRootLogin yes` in cloud-init |
| Password auth enabled | Medium | `PasswordAuthentication yes` |
| Missing SSH hardening | Low | No `ClientAliveInterval` config |
| No monitoring | Low | `monitoring = false` |

### Database Security

| Check | Severity | Pattern |
|-------|----------|---------|
| Public database access | Critical | No database firewall rules |
| No VPC attachment | High | Missing `private_network_uuid` |
| Weak version | Medium | Old database engine versions |
| Single node for production | Low | `node_count = 1` in prod |

### Storage Security

| Check | Severity | Pattern |
|-------|----------|---------|
| Public S3 buckets | Critical | `acl = "public-read"` |
| Missing encryption | High | No SSE configuration |
| No access logging | Medium | Missing access log bucket |

## Grep Patterns

```bash
# Hardcoded secrets
grep -rE 'AKIA[0-9A-Z]{16}' *.tf
grep -rE 'password\s*=\s*"[^$\{][^"]*"' *.tf
grep -rE 'secret.*=\s*"[^$\{][^"]*"' *.tf
grep -rE 'api_key\s*=\s*"' *.tf

# Network exposure
grep -rE '0\.0\.0\.0/0.*22' *.tf
grep -rE 'cidr_blocks.*0\.0\.0\.0/0' *.tf
grep -rE 'publicly_accessible\s*=\s*true' *.tf

# State security
grep -rE 'encrypt\s*=\s*false' *.tf
grep -rE 'block_public_acls\s*=\s*false' *.tf

# Cloud-init issues
grep -rE 'PermitRootLogin\s+yes' *.tf *.yaml
grep -rE 'PasswordAuthentication\s+yes' *.tf *.yaml
```

## Report Template

```markdown
# Infrastructure Security Review

**Repository:** [name]
**Date:** [date]
**Files Reviewed:** [count]

## Summary

| Severity | Count |
|----------|-------|
| Critical | X |
| High | X |
| Medium | X |
| Low | X |

## Findings

### [SEVERITY-001] Title

**File:** `path/to/file.tf:line`
**Resource:** `resource_type.name`

**Issue:**
Description of the security issue.

**Current:**
```hcl
[current code]
```

**Remediation:**
```hcl
[fixed code]
```

## Compliance Notes

- [ ] State encryption enabled (SOC 2)
- [ ] No hardcoded credentials (PCI-DSS)
- [ ] Network segmentation in place (HIPAA)
- [ ] Access logging enabled (all frameworks)
```

## Severity Guide

| Severity | Definition | Action |
|----------|------------|--------|
| Critical | Direct security exposure, data breach risk | Block deployment |
| High | Significant risk, exploitable weakness | Fix before production |
| Medium | Best practice violation, indirect risk | Fix within 30 days |
| Low | Minor hardening opportunity | Address when convenient |
