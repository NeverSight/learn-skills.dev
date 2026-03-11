---
name: ssh-remote-connection
description: SSH connection to remote servers. Use when you need to execute commands on a remote server, check logs, restart services, or manage Docker containers.
---

# SSH Remote Connection

Universal skill for connecting to remote servers via SSH.

## Usage

```bash
# Interactive shell
scripts/connect.sh

# Run command directly
scripts/connect.sh "docker compose logs backend --tail 50"
```

## Setup

### For Claude Code (local)

1. Copy config template:
   ```bash
   cp config/.env.example config/.env
   ```

2. Fill in `config/.env` with actual values

3. Make script executable:
   ```bash
   chmod +x scripts/connect.sh
   ```

### For Cloud Runtime

Set environment variables in your cloud configuration:
- `SSH_HOST` — server hostname or IP
- `SSH_USER` — SSH username
- `SSH_KEY_PATH` — path to private key
- `SSH_KEY_PASSWORD` — key passphrase (optional)
- `SERVER_PROJECT_PATH` — project directory on server

## Important Notes

- **Git operations**: Do NOT run `git pull` on the server. User will handle git sync manually.
- **Code location**: Code is in a private repo, changes must be pushed first then pulled by user.
- **Docker**: Use `docker compose` (not `docker-compose`) on the server.

## Example Commands

```bash
# View logs
scripts/connect.sh "docker compose logs backend --tail 100"

# Restart service
scripts/connect.sh "docker compose restart backend"

# Rebuild and restart
scripts/connect.sh "docker compose build backend && docker compose up -d backend"

# Check status
scripts/connect.sh "docker compose ps"
```
