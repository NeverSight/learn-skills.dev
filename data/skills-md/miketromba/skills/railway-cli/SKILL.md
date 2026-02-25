---
name: railway-cli
description: Manage Railway cloud deployments via the Railway CLI. Use when the user wants to deploy, manage services, set variables, view logs, link projects, add databases, configure domains, manage volumes, or perform any Railway platform operation from the terminal.
---

# Railway CLI

Operate the [Railway](https://railway.com) platform from the command line. Covers the full lifecycle: authentication, project setup, deployment, services, variables, environments, logs, domains, volumes, functions, and local development.

**Source of truth**: [Railway CLI Docs](https://docs.railway.com/cli.md)

## Handling Missing Installation

Assume `railway` is installed. If a command fails with "command not found" or similar, install it before retrying:

```bash
# macOS (preferred)
brew install railway

# Any OS with Node.js >= 16
npm i -g @railway/cli

# Shell script (macOS / Linux / WSL)
bash <(curl -fsSL cli.new)
```

After install, verify with `railway --version`, then resume the original task.

## Self-Discovery

The Railway CLI evolves across versions. When you encounter an unfamiliar subcommand or need to check current flags:

```bash
railway --help              # Top-level commands
railway <command> --help    # Subcommand flags and usage
```

Always prefer `--help` output over memorized flags when composing complex commands. This keeps behavior correct even as the CLI updates.

## Authentication

```bash
railway login                   # Browser-based login
railway login --browserless     # Token-based login (CI, SSH sessions)
railway logout
railway whoami                  # Verify current identity
```

**CI/CD token auth** (no interactive login):
- `RAILWAY_TOKEN` — project-scoped actions
- `RAILWAY_API_TOKEN` — account/workspace-scoped actions

```bash
RAILWAY_TOKEN=<token> railway up
```

## Project Lifecycle

### Create or link

```bash
railway init                    # Create new project (interactive)
railway link                    # Link cwd to existing project
railway unlink                  # Unlink cwd
```

### Inspect

```bash
railway status                  # Current project/service/environment info
railway list                    # All projects in workspace
railway open                    # Open project in browser
```

## Deployment

```bash
railway up                      # Deploy cwd
railway up --detach             # Deploy without tailing logs
railway deploy --template postgres  # Deploy from a template
railway redeploy                # Redeploy latest deployment
railway restart                 # Restart service (no new build)
railway down                    # Remove latest deployment
```

## Services

```bash
railway add                     # Add service (interactive)
railway add --database postgres # Add a database (postgres, mysql, redis, mongo)
railway add --repo user/repo    # Add service from GitHub repo
railway service                 # Switch linked service (interactive)
railway scale                   # Scale service replicas
railway delete                  # Delete the project
```

## Variables

```bash
railway variable list                   # List all variables
railway variable set KEY=value          # Set a variable
railway variable set K1=v1 K2=v2       # Set multiple at once
railway variable delete KEY             # Remove a variable
```

## Environments

```bash
railway environment                     # Switch environment (interactive)
railway environment new <name>          # Create environment
railway environment delete <name>       # Delete environment
```

## Local Development

```bash
railway run <cmd>               # Run command with Railway env vars injected
railway shell                   # Open shell with Railway env vars
railway dev                     # Run services locally with Docker
```

`railway run` is useful for running migrations, seeds, or scripts that need production/staging credentials without `.env` files.

## Logs & Debugging

```bash
railway logs                    # Stream live deployment logs
railway logs --build            # View build logs
railway logs -n 100             # Last N lines
railway ssh                     # SSH into running service container
railway connect                 # Connect to database shell (psql, mysql, redis-cli, mongosh)
```

## Networking

```bash
railway domain                  # Generate a Railway subdomain
railway domain example.com      # Attach a custom domain
```

## Volumes

```bash
railway volume list
railway volume add
railway volume delete
```

## Functions

```bash
railway functions list
railway functions new
railway functions push
```

## Utilities

```bash
railway completion bash         # Generate shell completions (bash/zsh/fish)
railway docs                    # Open docs in browser
railway upgrade                 # Upgrade CLI to latest version
```

## Global Flags

These flags work across most commands:

| Flag | Description |
|------|-------------|
| `-s, --service <name-or-id>` | Target a specific service |
| `-e, --environment <name-or-id>` | Target a specific environment |
| `--json` | Output as JSON (useful for scripting) |
| `-y, --yes` | Skip confirmation prompts |
| `-h, --help` | Show help |
| `-V, --version` | Show CLI version |

## Common Workflows

### First-time project setup

```bash
railway login
railway init          # or: railway link
railway up
railway domain        # get a public URL
railway logs          # verify deployment
```

### Add a database to an existing project

```bash
railway add --database postgres
railway connect       # verify connectivity
railway variable list # check injected DATABASE_URL
```

### Deploy with environment targeting

```bash
railway environment new staging
railway up -e staging
railway logs -e staging
```

### Run a one-off command with prod vars

```bash
railway run -e production npx prisma migrate deploy
```

## Additional Resources

For the full and most current reference, see [reference.md](reference.md) or consult:

- [Railway CLI Docs](https://docs.railway.com/cli.md)
- `railway --help` / `railway <command> --help`
- [Railway CLI GitHub](https://github.com/railwayapp/cli)
