---
name: "gitlab-variable"
description: "GitLab CI/CD variable operations. ALWAYS use this skill when user wants to: (1) list CI/CD variables, (2) set/create variables, (3) update variables, (4) delete variables, (5) manage secrets."
version: "1.0.0"
author: "GitLab-Assistant-Skills"
license: "MIT"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# CI/CD Variable Skill

CI/CD variable management operations for GitLab using the `glab` CLI.

## Quick Reference

| Operation | Command | Risk |
|-----------|---------|:----:|
| List variables | `glab variable list` | - |
| Get variable | `glab variable get <key>` | - |
| Set variable | `glab variable set <key> <value>` | ⚠️ |
| Update variable | `glab variable update <key> <value>` | ⚠️ |
| Delete variable | `glab variable delete <key>` | ⚠️⚠️ |
| Export variables | `glab variable export` | - |

**Risk Legend**: - Safe | ⚠️ Caution | ⚠️⚠️ Warning | ⚠️⚠️⚠️ Danger

## When to Use This Skill

**ALWAYS use when:**
- User wants to manage CI/CD variables
- User mentions "variable", "secret", "env var", "CI variable", "environment variable"
- User wants to configure build/deployment settings

**NEVER use when:**
- User wants to run pipelines (use gitlab-ci)
- User wants to manage .env files locally (use file operations)

## Available Commands

### List Variables

```bash
glab variable list [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-g, --group=<group>` | List group-level variables |
| `-P, --per-page=<n>` | Results per page |

**Examples:**
```bash
# List project variables
glab variable list

# List group variables
glab variable list -g mygroup
```

### Get Variable

```bash
glab variable get <key> [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-g, --group=<group>` | Get from group level |
| `-s, --scope=<scope>` | Variable scope/environment |

**Examples:**
```bash
# Get variable value
glab variable get API_KEY

# Get scoped variable
glab variable get DATABASE_URL --scope=production
```

### Set Variable

```bash
glab variable set <key> <value> [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-g, --group=<group>` | Set at group level |
| `-m, --masked` | Mask value in logs |
| `-p, --protected` | Only available in protected branches |
| `-r, --raw` | Value is raw (no expansion) |
| `-s, --scope=<scope>` | Variable scope/environment |
| `-t, --type=<type>` | Variable type: env_var, file |

**Examples:**
```bash
# Set simple variable
glab variable set API_URL "https://api.example.com"

# Set masked secret
glab variable set API_KEY "secret123" --masked

# Set protected variable (only on protected branches)
glab variable set DEPLOY_KEY "key123" --protected --masked

# Set scoped variable for production
glab variable set DATABASE_URL "postgres://prod..." --scope=production

# Set file type variable
glab variable set CONFIG_FILE "$(cat config.json)" --type=file

# Set group variable
glab variable set SHARED_SECRET "secret" -g mygroup --masked
```

### Update Variable

```bash
glab variable update <key> <value> [options]
```

Same options as `set`. Updates existing variable.

**Examples:**
```bash
# Update variable value
glab variable update API_KEY "new-secret" --masked

# Update and change scope
glab variable update DATABASE_URL "new-url" --scope=staging
```

### Delete Variable

```bash
glab variable delete <key> [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-g, --group=<group>` | Delete from group level |
| `-s, --scope=<scope>` | Variable scope |

**Warning:** This permanently deletes the variable.

**Examples:**
```bash
# Delete variable
glab variable delete OLD_API_KEY

# Delete scoped variable
glab variable delete DATABASE_URL --scope=staging
```

### Export Variables

```bash
glab variable export [options]
```

Export variables in dotenv format.

**Examples:**
```bash
# Export to stdout
glab variable export

# Export to file
glab variable export > .env.ci

# Export and source
eval $(glab variable export)
```

## Variable Types

| Type | Use Case |
|------|----------|
| `env_var` | Environment variable (default) |
| `file` | Write value to file, expose path as variable |

## Variable Flags

| Flag | Effect |
|------|--------|
| `masked` | Value is hidden in job logs |
| `protected` | Only available on protected branches/tags |
| `raw` | No variable expansion (use for JSON, etc.) |

## Common Workflows

### Workflow 1: Set Up Deployment Variables

```bash
# Set production secrets
glab variable set PROD_API_KEY "xxx" --protected --masked --scope=production
glab variable set PROD_DB_URL "postgres://..." --protected --masked --scope=production

# Set staging secrets
glab variable set STAGING_API_KEY "xxx" --masked --scope=staging
glab variable set STAGING_DB_URL "postgres://..." --masked --scope=staging
```

### Workflow 2: Rotate Secrets

```bash
# 1. List current variables
glab variable list

# 2. Update the secret
glab variable update API_KEY "new-secret-value" --masked

# 3. Trigger a new pipeline to use new secret
glab ci run
```

### Workflow 3: Set Up Service Account

```bash
# Store credentials as masked file
glab variable set SERVICE_ACCOUNT_JSON "$(cat service-account.json)" \
  --type=file --protected --masked

# In CI/CD, use $SERVICE_ACCOUNT_JSON as path to the credentials file
```

### Workflow 4: Configure Multi-Environment

```bash
# Production (protected + masked)
glab variable set DATABASE_URL "postgres://prod..." --scope=production --protected --masked
glab variable set API_KEY "prod-key" --scope=production --protected --masked

# Staging
glab variable set DATABASE_URL "postgres://staging..." --scope=staging --masked
glab variable set API_KEY "staging-key" --scope=staging --masked

# Development
glab variable set DATABASE_URL "postgres://dev..." --scope=development
glab variable set API_KEY "dev-key" --scope=development
```

## Security Best Practices

1. **Always mask secrets**: Use `--masked` for any sensitive values
2. **Protect production secrets**: Use `--protected` for production credentials
3. **Use scopes**: Separate variables by environment
4. **Rotate regularly**: Update secrets periodically
5. **Avoid logging**: Never echo variable values in CI scripts
6. **Use file type for complex secrets**: JSON, certificates, etc.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Authentication failed | Invalid/expired token | Run `glab auth login` |
| Variable not found | Wrong key or scope | Check with `glab variable list` |
| Cannot see value | Variable is masked | Masked values cannot be retrieved |
| Permission denied | Not maintainer | Need maintainer+ role for variables |
| Value truncated | Special characters | Use `--raw` flag for complex values |

## Related Documentation

- [Safeguards](../shared/docs/SAFEGUARDS.md)
- [Quick Reference](../shared/docs/QUICK_REFERENCE.md)
