---
name: onepassword-cli-coder
description: This skill guides integrating 1Password CLI (op) for secret management in development workflows. Use when loading secrets for infrastructure, deployments, or local development.
allowed-tools: Read Write Edit Bash Grep Glob
---

## Core Patterns

### Secret Reference Format

```
op://<vault>/<item>/<field>
```

Examples:
```
op://Development/AWS/access_key_id
op://Production/Database/password
op://Shared/Stripe/secret_key
```

### Item Naming Conventions

Format: `{environment}-{service}` with kebab-case. One item per environment.

| Pattern | Example | Bad Alternative |
|---------|---------|-----------------|
| `{env}-{service}` | `production-rails` | `Production Rails` |
| `{env}-{provider}` | `production-dockerhub` | `API Key` |
| `{env}-{provider}-{resource}` | `production-hetzner-s3` | Mixed env items |

### Field Naming

Use semantic field names that describe the credential type:

| Good | Bad | Why |
|------|-----|-----|
| `access_token` | `value` | Self-documenting |
| `master_key` | `secret` | Specific purpose clear |
| `secret_access_key` | `key` | Matches AWS naming |
| `api_token` | `token` | Distinguishes from other tokens |

Field naming rules:
- Match the provider's terminology when possible (AWS uses `access_key_id`, `secret_access_key`)
- Use snake_case for consistency
- Be specific: `database_password` not just `password` when item has multiple credentials

### Environment File (.op.env)

Create `.op.env` in project root:

```bash
AWS_ACCESS_KEY_ID=op://Infrastructure/AWS/access_key_id
AWS_SECRET_ACCESS_KEY=op://Infrastructure/AWS/secret_access_key
DIGITALOCEAN_TOKEN=op://Infrastructure/DigitalOcean/api_token
DATABASE_URL=op://Production/PostgreSQL/connection_string
STRIPE_SECRET_KEY=op://Production/Stripe/secret_key
```

**Critical:** Add to `.gitignore`:
```gitignore
# 1Password - NEVER commit
.op.env
*.op.env
```

### Running Commands with Secrets

```bash
op run --env-file=.op.env -- terraform plan
op run --env-file=.op.env -- rails server
```

## Integration Patterns

### Makefile Integration

```makefile
OP ?= op
OP_ENV_FILE ?= .op.env

# Prefix for all commands needing secrets
CMD = $(OP) run --env-file=$(OP_ENV_FILE) --

deploy:
	$(CMD) kamal deploy

console:
	$(CMD) rails console

migrate:
	$(CMD) rails db:migrate
```

### Docker Compose

```bash
op run --env-file=.op.env -- docker compose up
```

### Kamal Deployment

```yaml
# config/deploy.yml
env:
  secret:
    - RAILS_MASTER_KEY
    - DATABASE_URL
    - REDIS_URL
```

```bash
# .kamal/secrets
RAILS_MASTER_KEY=$(op read "op://Production/Rails/master_key")
DATABASE_URL=$(op read "op://Production/PostgreSQL/url")
REDIS_URL=$(op read "op://Production/Redis/url")
```

### CI/CD (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: 1password/load-secrets-action@v2
        with:
          export-env: true
        env:
          OP_SERVICE_ACCOUNT_TOKEN: ${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}
          AWS_ACCESS_KEY_ID: op://CI/AWS/access_key_id
          AWS_SECRET_ACCESS_KEY: op://CI/AWS/secret_access_key

      - run: terraform apply -auto-approve
```

## CLI Commands

### Reading Secrets

```bash
op read "op://Vault/Item/field"
op read "op://Vault/Item/field" --format json
op read "op://Vault/TLS/private_key" > /tmp/key.pem && chmod 600 /tmp/key.pem
```

### Injecting into Commands

```bash
DATABASE_URL=$(op read "op://Production/DB/url") rails db:migrate
op run --env-file=.op.env -- ./deploy.sh
op run --account my-team --env-file=.op.env -- terraform apply
```

### Managing Items

```bash
op vault list
op item list --vault Infrastructure
op item get "AWS" --vault Infrastructure
op item create --category login --vault Infrastructure \
  --title "New Service" --field username=admin --field password=secret123
```

## Project Setup

### Initial Configuration

```bash
op signin
op vault list

cat > .op.env << 'EOF'
AWS_ACCESS_KEY_ID=op://Infrastructure/AWS/access_key_id
AWS_SECRET_ACCESS_KEY=op://Infrastructure/AWS/secret_access_key
DATABASE_URL=op://Production/Database/url
REDIS_URL=op://Production/Redis/url
EOF

op run --env-file=.op.env -- env | grep -E '^(AWS|DATABASE|REDIS)'
```

### Placeholder Workflow

Create items with placeholder values upfront, populate with real credentials later:

```bash
op item create --vault myproject --category login \
  --title "production-rails" --field master_key="PLACEHOLDER_UPDATE_BEFORE_DEPLOY"

cat > .kamal/secrets << 'EOF'
RAILS_MASTER_KEY=$(op read "op://myproject/production-rails/master_key")
EOF

# Later: update with real value
op item edit "production-rails" --vault myproject \
  master_key="actual_secret_value_here"
```

### Vault Organization

**Single-Vault Approach (Simpler)**

Use one vault with naming conventions for environment separation:

```
Vault: myproject
Items:
  - production-rails
  - production-dockerhub
  - production-hetzner-s3
  - staging-rails
  - staging-dockerhub
  - development-rails
```

**Multi-Vault Approach (Team Scale)** -- use when teams need different access controls:

| Vault | Purpose | Access |
|-------|---------|--------|
| `Infrastructure` | Cloud provider credentials | DevOps team |
| `Production` | Production app secrets | Deploy systems |
| `Staging` | Staging environment | Dev team |
| `Development` | Local dev secrets | Individual devs |

## Security Rules

- Add `.op.env` and `*.op.env` to `.gitignore` -- never commit
- Use service accounts for CI/CD, not personal accounts
- Never pipe `op read` to logs or echo
- Never store session tokens in scripts
- Use variables for vault/item names in automation

## Troubleshooting

```bash
op signin                  # Re-authenticate expired session
op whoami                  # Check current session
op vault list              # Verify vault access
op item list --vault Infrastructure | grep -i aws   # Search for items
op item get "AWS" --vault Infrastructure --format json | jq '.fields[].label'  # Check field names
```

## Multiple Accounts

Always specify account in automation -- never rely on "last signed in":

```bash
op vault list --account acme.1password.com
export OP_ACCOUNT=acme.1password.com
op run --account acme.1password.com --env-file=.op.env -- ./deploy.sh
```

## Multi-Environment Pattern

Use per-environment env files: `.op.env.production`, `.op.env.staging`, `.op.env.development`

```makefile
ENV ?= development
OP_ENV_FILE = .op.env.$(ENV)

deploy:
	op run --env-file=$(OP_ENV_FILE) -- kamal deploy
# Usage: make deploy ENV=production
```

## References

- [references/multiple-accounts.md](references/multiple-accounts.md) - Cross-account workflows and Makefile integration
