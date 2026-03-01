---
name: doppler
description: >-
  Manage secrets with Doppler: CLI operations, project/config/environment management,
  secrets injection, CI/CD integrations, and security best practices.
allowed-tools: [Read, Bash, Grep, Glob, WebSearch, WebFetch, Write, Edit]
user-invocable: true
metadata:
  author: rube-de
  version: "1.0.0"
---

# Doppler Secrets Management

Comprehensive assistance for the Doppler secrets management platform: CLI operations, project and config management, secrets injection, integration syncs, and security best practices.

## Triggers

Use this skill when the user mentions: "doppler", "secrets management", "doppler cli", "doppler secrets", "doppler run", "doppler setup", "doppler configs", "doppler projects", "secret injection", "doppler environments", "service tokens".

## Quick Start

### Install CLI

```bash
# macOS
brew install gnupg && brew install dopplerhq/cli/doppler

# Linux (Debian/Ubuntu)
apt-get update && apt-get install -y apt-transport-https ca-certificates curl gnupg
curl -sLf --retry 3 --tlsv1.2 --proto "=https" \
  'https://packages.doppler.com/public/cli/gpg.DE2A7741A397C129.key' | \
  gpg --dearmor -o /usr/share/keyrings/doppler-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/doppler-archive-keyring.gpg] https://packages.doppler.com/public/cli/deb/debian any-version main" | \
  tee /etc/apt/sources.list.d/doppler-cli.list
apt-get update && apt-get install doppler

# Shell script (any OS)
curl -sLf --retry 3 --tlsv1.2 --proto "=https" https://get.doppler.com | sh
```

### Authenticate & Setup

```bash
# Login (opens browser for auth)
doppler login

# Setup project in current directory (interactive)
doppler setup

# Non-interactive setup
doppler setup --project my-app --config dev --no-interactive
```

## Common Tasks by Intent

| Developer wants to... | Action |
|-----------------------|--------|
| List all secrets | `doppler secrets -p <project> -c <config>` |
| Get a single secret | `doppler secrets get SECRET_NAME -p <project> -c <config>` |
| Set a secret | `doppler secrets set KEY=value -p <project> -c <config>` |
| Set multiple secrets | `doppler secrets set KEY1=val1 KEY2=val2` |
| Delete a secret | `doppler secrets delete SECRET_NAME` |
| Run command with secrets | `doppler run -- your-command --flags` |
| Run with specific config | `doppler run -p backend -c dev -- npm start` |
| Download secrets as file | `doppler secrets download --format env --no-file` |
| List projects | `doppler projects` |
| List configs | `doppler configs -p <project>` |
| List environments | `doppler environments -p <project>` |
| Clone a config | `doppler configs clone -p <project> -c <source> --name <new>` |
| View activity logs | `doppler activity` |
| Check current setup | `doppler configure debug` |
| Open dashboard | `doppler open` |
| View who is authenticated | `doppler me` |

## Secrets Injection Patterns

### Environment Variable Injection

```bash
# Inject secrets as env vars for any command
doppler run -- node server.js
doppler run -- docker compose up
doppler run -- terraform apply

# Run a shell command string
doppler run --command "echo $DATABASE_URL && npm start"

# Only inject specific secrets
doppler run --only-secrets DATABASE_URL,API_KEY -- node server.js
```

### Mount Secrets to File

```bash
# Mount as JSON file (ephemeral, cleaned up after process exits)
doppler run --mount secrets.json -- cat secrets.json

# Mount as .env file
doppler run --mount .env --mount-format env -- your-command

# Mount with template
doppler run --mount config.yaml --mount-template template.yaml -- your-command
```

### Template Substitution

```bash
# Substitute secrets into a template file
doppler secrets substitute template.env.tpl > .env
```

### Fallback for Offline/Resilience

```bash
# Run with fallback file (writes encrypted secrets on success, reads on failure)
doppler run --fallback ./fallback.encrypted -- npm start

# Read-only fallback (never update the fallback file)
doppler run --fallback ./fallback.encrypted --fallback-readonly -- npm start

# Offline mode (read directly from fallback, no API contact)
doppler run --fallback-only --fallback ./fallback.encrypted -- npm start
```

## Project & Config Hierarchy

Doppler organizes secrets in a hierarchy:

```
Workplace
 └── Project (e.g. "backend", "frontend")
      └── Environment (e.g. "development", "staging", "production")
           └── Config (e.g. "dev", "stg", "prd")
                └── Branch Config (e.g. "dev_feature-x")
```

### Config Inheritance

- Root configs (dev, stg, prd) inherit from their environment
- Branch configs inherit from their parent config
- Overrides cascade: Environment → Config → Branch Config
- Personal configs allow individual developer overrides without affecting the team

## Integration Syncs

Doppler can automatically sync secrets to external platforms:

| Platform | Use Case |
|----------|----------|
| AWS Secrets Manager / SSM | ECS, Lambda, EC2 deployments |
| GCP Secret Manager | GKE, Cloud Run, Cloud Functions |
| Azure Key Vault | AKS, App Service, Functions |
| Cloudflare Pages / Workers | Edge & Jamstack deployments |
| Vercel | Frontend/fullstack deployments |
| Firebase Functions / Hosting | Functions config & build-time secrets |
| Serverless Framework | Lambda/serverless function secrets |
| GitHub Actions | CI/CD secrets |
| Docker / Docker Compose | Container environment injection |
| Kubernetes | Secret objects via Doppler Operator |
| Terraform | Infrastructure as Code |
| Webapp.io | CI/CD Layerfile secrets |
| Heroku | PaaS deployments |

## Service Tokens

For CI/CD and production, use service tokens (read-only, scoped to a single config):

```bash
# Generate a service token via dashboard or API
# Use in CI/CD:
DOPPLER_TOKEN=dp.st.xxx doppler run -- your-command

# Or set as environment variable
export DOPPLER_TOKEN=dp.st.xxx
doppler secrets
```

## Security Best Practices

- **Never commit secrets** to version control — use Doppler as the single source of truth
- **Use service tokens** in production (read-only, config-scoped)
- **Use personal configs** for local development overrides
- **Enable change requests** for production configs (requires approval before changes)
- **Rotate secrets regularly** — use Doppler's rotation reminders
- **Use OIDC authentication** where possible for short-lived tokens
- **Audit access** via `doppler activity` and dashboard audit logs
- **Use branch configs** to isolate feature branch secrets
- **Never use `--no-verify-tls`** in production

## Reference Documents

For deep dives, consult these references:

| Reference | Content |
|-----------|---------|
| [CLI.md](references/CLI.md) | Complete CLI command reference with all subcommands and flags |
| [INTEGRATIONS.md](references/INTEGRATIONS.md) | CI/CD, Docker, Kubernetes, cloud platform integration patterns |

## Troubleshooting

### Authentication Issues

1. Run `doppler me` to check current auth status
2. Run `doppler configure debug` to see active configuration
3. Re-authenticate with `doppler login`
4. Check scope: `doppler configure get token --scope /path/to/project`

### Wrong Secrets Loaded

1. Check which project/config is active: `doppler configure debug`
2. Verify scope: `doppler setup` in the project directory
3. Use explicit flags: `doppler secrets -p project -c config`
4. Check for environment variable overrides: `doppler run --preserve-env=false`

### Fallback File Issues

1. Ensure fallback path is writable
2. Check passphrase hasn't changed (config-dependent by default)
3. Use `doppler run clean` to remove old fallback files
4. Regenerate with a fresh `doppler run --fallback ./path -- echo ok`

### Service Token Not Working

1. Verify token is for the correct project and config
2. Service tokens are read-only — cannot set/delete secrets
3. Check token hasn't been revoked in the dashboard
4. Ensure `DOPPLER_TOKEN` env var is set correctly

## Workflow

When helping with Doppler:

1. **Identify the task**: Setup, secret management, injection, integration, or debugging
2. **Check prerequisites**: Is `doppler` CLI installed? Is user authenticated?
3. **Determine scope**: Which project and config are we working with?
4. **Consult references**: Use reference docs for detailed CLI flags and integration patterns
5. **Security first**: Never output secret values in logs; use `--only-names` for listing
