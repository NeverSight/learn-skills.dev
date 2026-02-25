---
name: conductor-setup
description: Set up Conductor (conductor.build) for a repository. Creates conductor.json, setup scripts for .env symlinking, and configures dev server run commands. Use when the user asks to "set up Conductor", "configure Conductor", "add conductor.json", "create conductor config", or mentions Conductor workspaces for a new or existing repo.
---

# Conductor Setup

Configure a repository for Conductor — the macOS app for running parallel Claude Code workspaces.

## Workflow

### 1. Detect project type

Inspect the repo to determine:
- **Package manager**: npm, pnpm, yarn, pip, mix, bundler, cargo
- **Framework**: Next.js, Django, Rails, Phoenix, etc.
- **Dev server command**: The command that starts the development server
- **Env files**: All `.env` and `.env.local` files (check root and subdirectories up to depth 2)
- **Monorepo structure**: Whether the dev server lives in a subdirectory (e.g., `web/`, `apps/frontend/`)

### 2. Create the setup script

Create `scripts/conductor-setup.sh` in the repo root:

```bash
#!/bin/zsh
set -e

echo "==> Conductor workspace setup"

symlink_env() {
  local src="$1"
  local dest="$2"
  if [ ! -f "$src" ]; then
    echo "  WARN: $src not found — skipping (add it via Repository Settings > Open In)"
    return 0
  fi
  ln -sf "$src" "$dest"
  echo "  OK: $dest -> $src"
}

echo "==> Symlinking .env files from CONDUCTOR_ROOT_PATH"
# Add one symlink_env call per .env file discovered:
symlink_env "$CONDUCTOR_ROOT_PATH/.env" ".env"
# symlink_env "$CONDUCTOR_ROOT_PATH/web/.env" "web/.env"        # monorepo example
# symlink_env "$CONDUCTOR_ROOT_PATH/.env.local" ".env.local"    # Next.js example

echo "==> Installing dependencies"
# Add the install command for the detected package manager:
# npm install              # npm
# pnpm install             # pnpm
# pip install -r requirements.txt  # python

echo "==> Conductor workspace ready"
```

Make it executable: `chmod +x scripts/conductor-setup.sh`

Customize the symlink calls and install command for the specific project.

### 3. Create conductor.json

Create `conductor.json` at the repo root:

```json
{
  "scripts": {
    "setup": "zsh scripts/conductor-setup.sh",
    "run": "<dev-server-command> --port $CONDUCTOR_PORT",
    "archive": ""
  },
  "runScriptMode": "nonconcurrent"
}
```

Run command patterns by framework:
- **Next.js (root)**: `"npm run dev -- --port $CONDUCTOR_PORT"`
- **Next.js (monorepo)**: `"npm --prefix web run dev -- --port $CONDUCTOR_PORT"`
- **Django**: `"python manage.py runserver 0.0.0.0:$CONDUCTOR_PORT"`
- **Rails**: `"bin/rails server -p $CONDUCTOR_PORT"`
- **Phoenix**: `"mix phx.server"` (reads PORT env automatically)
- **Python http**: `"python3 -m http.server --port $CONDUCTOR_PORT"`
- **Vite**: `"npx vite --port $CONDUCTOR_PORT"`

Use `nonconcurrent` for dev servers (kills previous before starting new).

### 4. Symlink into existing workspaces

If the repo already has active Conductor workspaces, symlink .env files into them:

```bash
SRC="<repo-root-path>"
for ws in $(ls ~/conductor/workspaces/<repo-name>/); do
  WS_DIR="$HOME/conductor/workspaces/<repo-name>/$ws"
  ln -sf "$SRC/.env" "$WS_DIR/.env"
  # repeat for each .env file
done
```

### 5. Verify

Confirm the setup script symlinks are not broken and conductor.json is valid JSON.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `$CONDUCTOR_ROOT_PATH` | Persistent repo root (where .env files live) |
| `$CONDUCTOR_PORT` | Unique port per workspace |
| `$CONDUCTOR_WORKSPACE_NAME` | Workspace identifier |

## Reference

For full Conductor docs (conductor.json schema, run script modes, workspace locations), see [references/conductor-reference.md](references/conductor-reference.md).
