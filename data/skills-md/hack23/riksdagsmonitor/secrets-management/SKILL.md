---
name: secrets-management
description: GitHub secrets and environment variables for MCP servers and CI/CD workflows
license: Apache-2.0
---

# Secrets Management

## Purpose

Secure management of GitHub secrets for MCP servers and CI/CD workflows.

## GitHub Secrets Configuration

### Repository Secrets
```yaml
# Settings → Secrets and variables → Actions → Repository secrets

COPILOT_MCP_GITHUB_PERSONAL_ACCESS_TOKEN
  - Description: GitHub PAT for MCP server with Insiders API
  - Scopes: repo, read:org, read:user
  - Expiration: 90 days (renewal required)
```

### Environment Secrets
```yaml
# Settings → Environments → copilot → Environment secrets

COPILOT_MCP_GITHUB_PERSONAL_ACCESS_TOKEN
  - Description: GitHub PAT for Copilot environment
  - Injected via: COPILOT_AGENT_INJECTED_SECRET_NAMES
```

## Secret Usage in Workflows

### MCP Configuration
```json
// .github/copilot-mcp.json
{
  "mcpServers": {
    "github": {
      "env": {
        "GITHUB_TOKEN": "${{ secrets.COPILOT_MCP_GITHUB_PERSONAL_ACCESS_TOKEN }}",
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${{ secrets.COPILOT_MCP_GITHUB_PERSONAL_ACCESS_TOKEN }}"
      }
    }
  }
}
```

### Workflow Usage
```yaml
# .github/workflows/copilot-setup-steps.yml
env:
  GITHUB_TOKEN: ${{ secrets.COPILOT_MCP_GITHUB_PERSONAL_ACCESS_TOKEN }}
  GITHUB_PERSONAL_ACCESS_TOKEN: ${{ secrets.COPILOT_MCP_GITHUB_PERSONAL_ACCESS_TOKEN }}
```

## Security Best Practices

- ✅ Never commit secrets to repository
- ✅ Use GitHub secret scanning
- ✅ Rotate secrets every 90 days
- ✅ Minimal scope (least privilege)
- ✅ Environment-specific secrets
- ✅ Audit secret access logs

## References

- **GitHub Secrets**: https://docs.github.com/en/actions/security-guides/encrypted-secrets
- **Secret Scanning**: https://docs.github.com/en/code-security/secret-scanning
- **SECURITY.md**: Security policy
