---
name: compose
description: 'Use when deploying or starting a common service with Docker Compose on a server or VPS, such as Caddy, Nginx, MySQL, PostgreSQL, Redis, n8n, New API, Open WebUI, or Verdaccio. Lists the tlyboy compose-starter templates and how to pull one with giget.'
---

# Compose

`tlyboy/compose-starter` holds one Docker Compose template per service. Pull only the directory you need.

## Templates

| Service             | Template     | Notes                                                                                             |
| ------------------- | ------------ | ------------------------------------------------------------------------------------------------- |
| Caddy               | `caddy`      | Config in `conf/Caddyfile`, static files in `site/`                                               |
| Caddy + Alibaba DNS | `caddy-ali`  | Custom build with `caddy-dns/alidns`; needs `ALIYUN_ACCESS_KEY_ID` and `ALIYUN_ACCESS_KEY_SECRET` |
| Caddy + Cloudflare  | `caddy-cf`   | Custom build with `caddy-dns/cloudflare`; needs `CF_API_TOKEN`                                    |
| Nginx               | `nginx`      |                                                                                                   |
| MySQL               | `mysql`      |                                                                                                   |
| PostgreSQL          | `postgres`   |                                                                                                   |
| Redis               | `redis`      |                                                                                                   |
| n8n                 | `n8n`        |                                                                                                   |
| New API             | `new-api`    |                                                                                                   |
| Open WebUI          | `open-webui` | Use `open-webui-cuda` on NVIDIA GPU hosts                                                         |
| Verdaccio           | `verdaccio`  |                                                                                                   |

Check `https://github.com/tlyboy/compose-starter` for templates added after this list.

## Usage

```bash
npx giget gh:tlyboy/compose-starter/<template> <dir>
cd <dir>
docker compose up -d
```

Servers often have no Node.js. Pull a single template with git sparse checkout instead:

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/tlyboy/compose-starter.git /tmp/compose-starter
git -C /tmp/compose-starter sparse-checkout set <template>
cp -r /tmp/compose-starter/<template> <dir>
rm -rf /tmp/compose-starter
cd <dir>
docker compose up -d
```

- Templates ship with placeholder credentials (for example `POSTGRES_PASSWORD`). Change them before exposing a service.
- Put secrets such as DNS API tokens in a `.env` file next to `compose.yaml`; do not commit it.
- Data lives in bind mounts under the template directory or in named Docker volumes. Keep both when upgrading: `docker compose pull && docker compose up -d`, or `docker compose build --pull && docker compose up -d` for the custom-built `caddy-ali` and `caddy-cf`.

## Missing Tools

Templates need Docker with the Compose plugin, plus `npx` or git to pull them. When one is missing, do not install anything silently. Tell the user what is missing and let them pick:

1. **Recommended**: Docker Engine from Docker's apt repository, with an optional Alibaba Cloud mirror and a pull proxy. Follow [docker.md](docker.md) (Ubuntu); git from the system package manager.
2. **Simplest**: Docker's convenience script, `curl -fsSL https://get.docker.com | sh` (add `-s -- --mirror Aliyun` for servers in mainland China). It installs the latest release without prompts and is not meant for upgrades or production.
3. **Their own way**: the distribution's `docker.io` package, Docker Desktop, OrbStack, Podman, or anything else they prefer.
