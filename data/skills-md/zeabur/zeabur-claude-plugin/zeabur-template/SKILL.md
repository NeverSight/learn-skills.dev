---
name: zeabur-template
description: Use when creating, editing, validating, or troubleshooting a Zeabur template YAML. Use when converting docker-compose to Zeabur template.
---

# Zeabur Template Knowledge Base

This skill provides comprehensive knowledge for creating, debugging, and publishing Zeabur templates. It combines reference documentation with battle-tested patterns from real template development.

## External Documentation

For the latest schema and detailed docs, fetch from `https://raw.githubusercontent.com/zeabur/zeabur-template-doc/main/`:

| User Need | Document to Fetch | Path |
|-----------|-------------------|------|
| Create a template from scratch | Step-by-step guide | `docs/GUIDE.md` |
| Convert docker-compose.yml | Migration guide | `docs/DOCKER_COMPOSE_MIGRATION.md` |
| Look up YAML fields or built-in variables | Technical reference | `docs/REFERENCE.md` |
| Naming, design patterns, best practices | Best practices | `docs/BEST_PRACTICES.md` |
| Debug template errors | Troubleshooting | `docs/TROUBLESHOOTING.md` |
| Pre-deployment checklist | Checklist | `docs/CHECKLIST.md` |
| Quick all-in-one overview | Comprehensive prompt | `prompt.md` |

The template YAML schema is also available at https://schema.zeabur.app/template.json and the prebuilt service schema at https://schema.zeabur.app/prebuilt.json.

---

## Core Principles

### 0. All services MUST use PREBUILT_V2 with Docker images

**Every service in a template MUST be `template: PREBUILT_V2` with a Docker image as the source.** Never use `template: GIT`, `ARBITRARY_GIT`, or `GITHUB` source — these are NOT supported in templates.

If the project does not have a published Docker image (on Docker Hub, GHCR, etc.), **tell the user they need to build and publish a Docker image first** before a template can be created. Do not attempt to work around this.

If the user asks you to build the image, follow this workflow:
1. Clone the project repo and find its `Dockerfile` (usually at repo root)
2. Study the Dockerfile to understand build stages — use the **production stage** (often named `runner` or `production`)
3. Study `docker-compose.yml` or `docker-compose.fullapp.yml` for the correct startup command, env vars, and volumes — this is the battle-tested production config
4. Build for **amd64** (Zeabur servers are amd64, local Macs are arm64):
   ```bash
   docker buildx build --platform linux/amd64 --target runner -t org/image:tag --push .
   ```
5. After pushing, **verify the Docker Hub repo is public**:
   ```bash
   curl -s "https://hub.docker.com/v2/repositories/ORG/IMAGE/" | grep is_private
   ```
   New repos under org accounts often default to private. If `is_private: true`, the user must make it public on Docker Hub.

### 1. Never start from scratch

When asked to create a template, **always** look for existing configuration first:
- **First check if a Docker image exists** — search Docker Hub, GHCR (`ghcr.io/org/repo`), or the project's CI/CD for published images. If none exists, stop and inform the user.
- Search for the project's `docker-compose.yml`, `docker-compose.yaml`, or `compose.yml`
- Look for Helm charts (`Chart.yaml`, `values.yaml`)
- Check the project's GitHub repo for any deployment YAML files
- Use these as the foundation to build the Zeabur template, not as a loose reference — they contain battle-tested environment variables, port mappings, volume mounts, and service dependencies

### 2. Iterate via runtime logs — never expect one-shot success

Even experienced humans cannot create a working template in one shot. The workflow is an **iterative loop**:

1. Write/update the template YAML
2. Deploy the template
3. It will likely fail — check runtime logs to find the cause
4. Fix the issue in the template
5. Delete the project and redeploy from scratch
6. Repeat until the template achieves **one-click deployment success**

This is the normal process, not a sign of failure. Do not try to get everything perfect before deploying — deploy early, read logs, and iterate.

### 3. Reuse from existing templates — never write common services from scratch

When your template needs a common service (PostgreSQL, Redis, MySQL, MongoDB, etc.), **do not write the service definition yourself**. Instead:

1. Search for existing templates that already use that service:
   ```bash
   npx zeabur@latest template search postgres
   ```
2. Find a template that includes the service you need
3. Get the raw template YAML to see the exact service definition:
   ```bash
   npx zeabur@latest template get -c TEMPLATE_CODE --raw
   ```
4. Copy the service definition directly from that template into yours

**How to judge template trustworthiness:**
- Many templates are created by regular users and may not work correctly
- **Prefer templates with more deployments** — higher deployment count = more battle-tested
- **Prefer official templates over user-submitted ones** — official templates are vetted by Zeabur team

---

## CLI Commands for the Iteration Loop

**Deploy a template:**
```bash
npx zeabur@latest template deploy -f YOUR_TEMPLATE.yaml
```
For non-interactive mode (automation):
```bash
npx zeabur@latest template deploy -i=false \
  -f YOUR_TEMPLATE.yaml \
  --project-id PROJECT_ID \
  --var PUBLIC_DOMAIN=myapp
```

**List services (to get SERVICE_ID):**
```bash
npx zeabur@latest service list --project-id PROJECT_ID
```

**Check runtime logs:**
```bash
npx zeabur@latest deployment log --service-id SERVICE_ID
```

**Execute a command inside a running service** (like `docker exec`):
```bash
npx zeabur@latest service exec --id SERVICE_ID -- SHELL_COMMAND
```
This is extremely useful for debugging — check file paths, env vars, test connectivity, inspect the filesystem, etc. Examples:
```bash
npx zeabur@latest service exec --id SERVICE_ID -- ls /app
npx zeabur@latest service exec --id SERVICE_ID -- env | grep DATABASE
npx zeabur@latest service exec --id SERVICE_ID -- nc -z localhost 5432
```

**Restart a service** (useful to clear ImagePullBackOff or force re-pull):
```bash
npx zeabur@latest service restart --id SERVICE_ID -i=false -y
```

**Delete the project and start over:**
```bash
npx zeabur@latest project delete --id PROJECT_ID
```
> **DANGEROUS OPERATION** — Before deleting a project, you MUST ask the user for explicit confirmation, clearly stating the Project ID, Name, and createdAt timestamp. Never delete without confirmation.

**Publish a new template:**
```bash
npx zeabur@latest template create -f YOUR_TEMPLATE.yaml
```
This returns a template URL like `https://zeabur.com/templates/XXXXXX` with a template code.

**Update an existing template:**
```bash
npx zeabur@latest template update -c TEMPLATE_CODE -f YOUR_TEMPLATE.yaml
```

---

## Quick Reference: Template Skeleton

```yaml
# yaml-language-server: $schema=https://schema.zeabur.app/template.json
apiVersion: zeabur.com/v1
kind: Template
metadata:
  name: ServiceName
spec:
  description: |
    English description (1-3 sentences)
  icon: https://raw.githubusercontent.com/zeabur/service-icons/main/marketplace/service.svg
  coverImage: https://example.com/cover.webp
  tags:
    - Category
  variables: []
  readme: |
    # Service Name
    English documentation...
  services:
    - name: service-name
      icon: https://raw.githubusercontent.com/zeabur/service-icons/main/marketplace/service.svg
      template: PREBUILT_V2
      spec:
        source:
          image: image:tag
          command:              # MUST be inside source, alongside image
            - /bin/sh
            - -c
            - /opt/app/startup.sh
        ports:
          - id: web
            port: 8080
            type: HTTP
        volumes:
          - id: data
            dir: /path/to/data
        configs:
          - path: /opt/app/startup.sh
            permission: 493     # 0755
            envsubst: false
            template: |
              #!/bin/sh
              exec node server.js
        env:
          VAR_NAME:
            default: value
            expose: true
localization:
  zh-TW:
    description: ...
    variables: []
    readme: |
      # ...
  zh-CN:
    description: ...
    variables: []
    readme: |
      # ...
  ja-JP:
    description: ...
    variables: []
    readme: |
      # ...
  es-ES:
    description: ...
    variables: []
    readme: |
      # ...
  id-ID:
    description: ...
    variables: []
    readme: |
      # ...
```

## Quick Reference: Built-in Variables

| Variable | Purpose |
|----------|---------|
| `${PASSWORD}` | Auto-generated secure password |
| `${ZEABUR_WEB_URL}` | Full public URL (e.g. `https://app.zeabur.app`) |
| `${ZEABUR_WEB_DOMAIN}` | Domain only (e.g. `app.zeabur.app`) |
| `${CONTAINER_HOSTNAME}` | Internal hostname for inter-service communication |
| `${[PORTID]_PORT}` | Port value by port ID (e.g. `${DATABASE_PORT}`) |
| `${PORT_FORWARDED_HOSTNAME}` | External hostname (for `instructions`) |
| `${[PORTID]_PORT_FORWARDED_PORT}` | External forwarded port (for `instructions`) |

The `ZEABUR_<PORT_ID>_URL` pattern: for a port named `web`, it becomes `${ZEABUR_WEB_URL}`; for `console`, it becomes `${ZEABUR_CONSOLE_URL}`.

## Quick Reference: command Placement

**IMPORTANT: `command` MUST be inside `source`, alongside `image`. NOT at `spec` level.**

```yaml
# WRONG -- command at spec level (will be IGNORED, container uses default CMD)
spec:
  source:
    image: python:3.12-slim
  command:
    - /bin/sh
    - -c
    - /opt/app/start.sh

# CORRECT -- command inside source
spec:
  source:
    image: python:3.12-slim
    command:
      - /bin/sh
      - -c
      - /opt/app/start.sh
```

> **Note:** The external docs may show `command` at `spec` level. This is incorrect. Always place `command` inside `source` as confirmed by the JSON schema at `schema.zeabur.app/prebuilt.json`.

## Quick Reference: YAML Gotchas

```yaml
# RISKY -- @ at start of value is a YAML reserved indicator (may cause parse errors)
description: @BotFather token

# SAFE -- quote the value or avoid @ at start
description: "Token from @BotFather for Telegram bot"
description: Telegram bot token from BotFather
```

## Quick Reference: Docker Image ENTRYPOINT

**Some base images have ENTRYPOINT set, which conflicts with `command`.**

| Image | ENTRYPOINT | Problem |
|-------|-----------|---------|
| `ghcr.io/astral-sh/uv:python3.12-*` | `uv` | `command` becomes args to `uv`, container shows `uv help` and exits |
| `node:*` | none | Safe to use |
| `python:*` | none | Safe to use |

If using an image with ENTRYPOINT, switch to a plain base image (e.g. `python:3.12-slim-bookworm`) or one without ENTRYPOINT.

## Quick Reference: Headless Services (no HTTP)

If a service does NOT listen on any HTTP port (502 Bad Gateway), see `zeabur-port-mismatch` skill for the fix.

## Quick Reference: Critical Rules

```yaml
# WRONG -- hardcoded password
POSTGRES_PASSWORD:
  default: mypassword123

# CORRECT -- use ${PASSWORD}
POSTGRES_PASSWORD:
  default: ${PASSWORD}
  expose: true

# WRONG -- PUBLIC_DOMAIN gives incomplete URL
APP_URL:
  default: https://${PUBLIC_DOMAIN}

# CORRECT -- ZEABUR_WEB_URL gives full URL
APP_URL:
  default: ${ZEABUR_WEB_URL}
  readonly: true

# WRONG -- other services can't reference without expose
POSTGRES_HOST:
  default: ${CONTAINER_HOSTNAME}

# CORRECT -- expose + readonly for connection info
POSTGRES_HOST:
  default: ${CONTAINER_HOSTNAME}
  expose: true
  readonly: true

# WRONG -- referencing variables without declaring dependency
- name: app
  spec:
    env:
      DB: ${POSTGRES_HOST}

# CORRECT -- declare dependency first
- name: app
  dependencies:
    - postgresql
  spec:
    env:
      DB: ${POSTGRES_HOST}
```

---

## Domain Binding

Use `domainKey` on the service that needs a public domain. It maps to a variable defined in `spec.variables` with `type: DOMAIN`.

**Single domain:**
```yaml
domainKey: PUBLIC_DOMAIN
```

**Multiple domains (different ports):**
```yaml
domainKey:
    - port: web
      variable: ENDPOINT_DOMAIN
    - port: console
      variable: ADMIN_ENDPOINT_DOMAIN
```

---

## Common Database Configs

### PostgreSQL

```yaml
- name: postgresql
  icon: https://raw.githubusercontent.com/zeabur/service-icons/main/marketplace/postgresql.svg
  template: PREBUILT_V2
  spec:
    source:
      image: postgres:16-alpine
    ports:
      - id: database
        port: 5432
        type: TCP
    volumes:
      - id: data
        dir: /var/lib/postgresql/data
    env:
      POSTGRES_USER:
        default: postgres
        expose: true
      POSTGRES_PASSWORD:
        default: ${PASSWORD}
        expose: true
      POSTGRES_DB:
        default: mydb
        expose: true
      POSTGRES_HOST:
        default: ${CONTAINER_HOSTNAME}
        expose: true
        readonly: true
      POSTGRES_PORT:
        default: ${DATABASE_PORT}
        expose: true
        readonly: true
      POSTGRES_CONNECTION_STRING:
        default: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
        expose: true
        readonly: true
```

### MySQL/MariaDB

```yaml
- name: mariadb
  icon: https://raw.githubusercontent.com/zeabur/service-icons/main/marketplace/mariadb.svg
  template: PREBUILT_V2
  spec:
    source:
      image: mariadb:10.6
    ports:
      - id: database
        port: 3306
        type: TCP
    volumes:
      - id: data
        dir: /var/lib/mysql
    env:
      MYSQL_ROOT_PASSWORD:
        default: ${PASSWORD}
        expose: true
      MYSQL_DATABASE:
        default: mydb
        expose: true
      MYSQL_HOST:
        default: ${CONTAINER_HOSTNAME}
        expose: true
        readonly: true
      MYSQL_PORT:
        default: ${DATABASE_PORT}
        expose: true
        readonly: true
```

### Redis

```yaml
- name: redis
  icon: https://raw.githubusercontent.com/zeabur/service-icons/main/marketplace/redis.svg
  template: PREBUILT_V2
  spec:
    source:
      image: redis:7-alpine
    ports:
      - id: database
        port: 6379
        type: TCP
    volumes:
      - id: data
        dir: /data
    env:
      REDIS_HOST:
        default: ${CONTAINER_HOSTNAME}
        expose: true
        readonly: true
      REDIS_PORT:
        default: ${DATABASE_PORT}
        expose: true
        readonly: true
```

### Standard Volume Paths

| Service | Path |
|---------|------|
| PostgreSQL | `/var/lib/postgresql/data` |
| MySQL/MariaDB | `/var/lib/mysql` |
| MongoDB | `/data/db` |
| Redis | `/data` |
| MinIO | `/data` |

---

## Template Complexity Levels

**Level 1 -- Single prebuilt service** (e.g., Memos, Uptime-Kuma, LobeChat):
- Just one service with image, port, and optionally a volume
- Simplest pattern, no cross-service wiring needed

**Level 2 -- App + database** (e.g., Ghost+MySQL, Linkwarden+PostgreSQL):
- Database service exposes vars, app service references them
- App service uses `dependencies` to ensure DB starts first

**Level 3 -- App + database + init/migrator** (e.g., Teable, Open Mercato):
- First-run initialization or separate migrator service
- Requires wait-for-db pattern and init marker files

**Level 4 -- Multi-service with multiple domains** (e.g., Logto):
- Multiple ports on one service, each bound to a different domain variable

**Level 5 -- Large-scale multi-service platform** (e.g., Dify 12 services, Supabase 11 services):
- **Reverse proxy as entry point**: nginx (Dify) or Kong (Supabase) as the single domain-bound service
- **Same image, different MODE**: e.g., Dify runs `api`, `worker`, `worker-beat` from the same image
- **Internal-only services**: no public domain, communicate via `${CONTAINER_HOSTNAME}`
- **Heavy use of `configs`**: Nginx conf, SQL init scripts, Kong config — all injected via `configs` field
- **PostgreSQL init SQL via configs**: Mount to `/docker-entrypoint-initdb.d/` for auto execution
- **Shared secrets**: Use `${PASSWORD}` for all internal credentials

---

## Writing name, description, readme, icon, and coverImage

**Where to collect information** (in priority order):
1. The project's **GitHub repo README**
2. The project's **official website**
3. Other **public sources** (blog posts, documentation sites, etc.)

**Key rules:**
1. **Do NOT copy-paste the original README.** Write the introduction for **this project's Zeabur template**, not for the project itself. The readme should:
   - Briefly introduce what the project is
   - Focus on how to use this template (deployment steps, configuration, domain binding)
   - Include important caveats and troubleshooting tips specific to Zeabur deployment
2. **Always include licensing and attribution.** If the original project has an MIT, Apache, or other license:
   - Mention the license in the readme
   - Link to the original repo
   - Link to the official website if available
   - This is **legally required** -- never skip it
3. **icon and coverImage**: Find the project's logo from their GitHub repo or official website. Use a direct URL to an image (SVG, PNG, or WebP). **Always verify the URL returns HTTP 200**:
   ```bash
   curl -s -o /dev/null -w "%{http_code}" "URL"
   ```
   Common pitfall: wrong branch name in `raw.githubusercontent.com` URLs (`develop` vs `main` vs `master`).

## Localization Requirements

6 languages required: en-US (in `spec`), zh-TW, zh-CN, ja-JP, es-ES, id-ID.

**Translate:** `description`, `variables[].name`, `variables[].description`, `readme`

**Do NOT translate:** `key`, `type`, `${VARIABLE_NAMES}`, URLs

---

## Hard-Won Lessons (from real template challenges)

### Wait for database readiness
Zeabur's `dependencies` field only ensures services are **deployed**, not that they're **ready to accept connections**. A database container can take 5-15 seconds to initialize. Always add a wait loop before running migrations or init:
```yaml
args:
    - -c
    - |
        echo "Waiting for PostgreSQL..."
        while ! nc -z ${POSTGRES_HOST} ${POSTGRES_PORT} 2>/dev/null; do sleep 2; done
        echo "PostgreSQL is ready!"
        echo "Waiting for Redis..."
        while ! nc -z ${REDIS_HOST} ${REDIS_PORT} 2>/dev/null; do sleep 2; done
        echo "Redis is ready!"
        # ... then run migrations/init
```
Note: `nc` (netcat) is available on most Alpine-based images. If not, use `wget --spider` or a node one-liner.

### Study the project's own Dockerfile and docker-compose
**Never guess startup commands.** Instead:
1. Read the project's `Dockerfile` to understand the build stages and the final `CMD`/`ENTRYPOINT`
2. Read `docker-compose.yml` and especially `docker-compose.fullapp.yml` (or `docker-compose.prod.yml`) for the production startup command -- these often override the Dockerfile's CMD with init/migrate logic
3. Check the app's `package.json` scripts to understand what `yarn start` or `npm start` actually runs
4. The startup command in docker-compose is battle-tested -- copy it, don't reinvent it

### Memory-heavy apps need lighter startup
Apps that spawn workers, schedulers, and the web server all in one process may OOM on Zeabur's default allocation. Signs of OOM:
- Container starts, runs for 1-2 minutes, then crashes with no error logs (just `BackOff: Back-off restarting failed container`)
- No application-level crash message -- the kernel kills the process silently

Solutions:
- Run the web server directly (e.g., `next start` or `node server.js`) instead of a CLI wrapper that spawns workers + scheduler + server
- Disable non-essential background processes via env vars (e.g., `AUTO_SPAWN_WORKERS=false`)
- If workers are needed, consider splitting them into a separate service

### First-run init with persistent marker
For apps that need first-time initialization (DB schema, seed data, admin users), use a marker file in a persistent volume:
```yaml
args:
    - -c
    - |
        if [ ! -f /app/storage/.initialized ]; then
          echo "First run: initializing..."
          run-init-command && touch /app/storage/.initialized
        else
          echo "Subsequent run: migrations only..."
          run-migrate-command
        fi
        exec start-server-command
```
Key points:
- The marker file MUST be in a **persistent volume**, not `/tmp/` (which is ephemeral)
- Use `&&` after init so the marker is only created if init succeeds
- Use `exec` for the final server process so it becomes PID 1 and receives signals properly
- Read init logs carefully for the **actual default credentials** -- don't assume from docs

### Working directory matters
When overriding `command`/`args`, be aware of the Dockerfile's `WORKDIR`. In monorepo apps, different commands need to run from different directories:
```yaml
args:
    - -c
    - |
        cd /app              # root workspace for yarn workspace commands
        yarn mercato init    # CLI from root package.json
        cd /app/apps/myapp   # app directory for next start
        exec next start -p 3000
```

### ImagePullBackOff recovery
When a pod is stuck in `ImagePullBackOff` (e.g., after making a Docker Hub repo public), the Kubernetes backoff timer prevents immediate retries. Fix by restarting the service:
```bash
npx zeabur@latest service restart --id SERVICE_ID -i=false -y
```

### Disable unused monitoring agents
Many production images ship with New Relic, Datadog, or similar APM agents. These require license keys and consume memory. Add `NEW_RELIC_ENABLED=false` or equivalent env vars to disable them cleanly. Check if the `start` script injects agents via `NODE_OPTIONS='-r newrelic'` -- these still run even if the agent errors out.

### Verify all URLs before publishing
Before publishing a template, verify that ALL URLs return HTTP 200:
- `icon` URL
- `coverImage` URL
- Links in `readme`

Common pitfall: `raw.githubusercontent.com` URLs with wrong branch name (`develop` vs `main` vs `master`). Always check:
```bash
curl -s -o /dev/null -w "%{http_code}" "https://raw.githubusercontent.com/..."
```
