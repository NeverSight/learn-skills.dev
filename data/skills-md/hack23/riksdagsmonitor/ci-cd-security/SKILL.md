---
name: ci-cd-security
description: Security best practices for GitHub Actions workflows, supply chain security, and secure CI/CD pipelines
license: Apache-2.0
---

# CI/CD Security Skill

## Purpose

Implement security-hardened CI/CD pipelines using GitHub Actions with least privilege, supply chain security, and comprehensive monitoring.

## Core Principles

### 1. Least Privilege Permissions
Always grant minimum necessary permissions:

```yaml
permissions:
  contents: read       # Read repo content
  pull-requests: write # Only if managing PRs
  issues: write        # Only if managing issues
  # Deny everything else by default
```

### 2. Pin Actions to SHA
Never use tags - always pin to commit SHA:

```yaml
# ❌ Bad: Using tag (can be moved)
- uses: actions/checkout@v4

# ✅ Good: Pinned to SHA (immutable)
- uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd
```

### 3. Harden Runner
Use step-security/harden-runner on every job:

```yaml
- name: Harden Runner
  uses: step-security/harden-runner@e3f713f2d8f53843e71c69a996d56f51aa9adfb9
  with:
    egress-policy: audit  # Log all network calls
```

### 4. Secrets Management
```yaml
# ✅ Use GitHub Secrets
- env:
    TOKEN: \${{ secrets.GITHUB_TOKEN }}
  run: |
    # Never echo secrets
    curl -H "Authorization: Bearer \$TOKEN" ...

# ❌ Never hardcode
TOKEN="ghp_hardcoded_token"  # NEVER DO THIS
```

### 5. Supply Chain Security
```yaml
- name: Dependency Review
  uses: actions/dependency-review-action@SHA
  
- name: CodeQL Scanning
  uses: github/codeql-action/analyze@SHA
```

## Security-Hardened Workflow Template

```yaml
name: Secure Workflow

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - name: Harden Runner
        uses: step-security/harden-runner@e3f713f2d8f53843e71c69a996d56f51aa9adfb9
        with:
          egress-policy: audit
          allowed-endpoints: >
            github.com:443
            api.github.com:443
            
      - name: Checkout
        uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd
        
      - name: Setup Node
        uses: actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238
        with:
          node-version: '24'
          cache: 'npm'
          
      - name: Install Dependencies
        run: npm ci
        
      - name: Run Security Checks
        run: |
          npm audit
          npm run lint
          npm test
```

## Supply Chain Security

### Dependency Scanning
```yaml
- name: Run Dependency Review
  uses: actions/dependency-review-action@SHA
  with:
    fail-on-severity: moderate
```

### Code Scanning
```yaml
- name: Initialize CodeQL
  uses: github/codeql-action/init@SHA
  with:
    languages: javascript, python
    
- name: Perform CodeQL Analysis
  uses: github/codeql-action/analyze@SHA
```

### Secret Scanning
Enable in repository settings:
- GitHub secret scanning
- Push protection
- Custom patterns if needed

## Remember

- **Least Privilege**: Grant minimal permissions
- **Pin to SHA**: Immutable action versions
- **Harden Runner**: Audit all network egress
- **Scan Everything**: Dependencies, code, secrets
- **Never Trust**: Validate all inputs
- **Monitor Continuously**: Review audit logs

## References

- [GitHub Actions Security](https://docs.github.com/en/actions/security-guides)
- [Step Security](https://github.com/step-security/harden-runner)
- [SLSA Framework](https://slsa.dev/)
