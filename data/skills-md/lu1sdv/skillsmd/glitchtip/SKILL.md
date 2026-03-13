---
name: glitchtip
description: Use when deploying, configuring, integrating, or troubleshooting GlitchTip — including self-hosted installation, SDK setup, source maps, sentry-cli, uptime monitoring, alerting, environment variables, Docker Compose, Helm, social auth, and migration from Sentry
---

# GlitchTip

Open-source, Sentry API-compatible error tracking and uptime monitoring. Django + PostgreSQL backend, Angular frontend. Runs on 256MB RAM (all-in-one) or 512MB (standard).

- Site: https://glitchtip.com
- Docs: https://glitchtip.com/documentation
- API: https://app.glitchtip.com/api/docs
- Repo: https://gitlab.com/glitchtip/glitchtip-backend
- License: MIT

## Quick Reference

| Resource | URL |
|----------|-----|
| Hosted (US) | `app.glitchtip.com` |
| Hosted (EU) | `eu.glitchtip.com` |
| SDK docs | `glitchtip.com/sdkdocs` |
| Install guide | `glitchtip.com/documentation/install` |
| CLI (gtc) | `pip install glitchtip-cli` |

## Deployment

### Docker Compose (recommended)

```bash
# Download sample compose file
curl -sLO https://glitchtip.com/assets/docker-compose.sample.yml
mv docker-compose.sample.yml compose.yml
# Edit environment variables, then:
docker compose up -d
# Upgrade: docker compose pull && docker compose stop && docker compose up -d
```

**Minimal variant**: `compose.minimal.yml` — all-in-one mode, ~256MB RAM.

### Kubernetes (Helm)

```bash
helm repo add glitchtip https://gitlab.com/api/v4/projects/16325141/packages/helm/stable
helm install glitchtip glitchtip/glitchtip
```

Externally managed PostgreSQL recommended. Supports pod disruption budgets and anti-affinity for HA.

### Managed Platforms

PikaPods, Elestio, Nodion, Railway (one-click template), RepoCloud.

## Configuration

All via environment variables. Set in `compose.yml` or Helm values.

### Required

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Random string for Django security |
| `DATABASE_URL` | PostgreSQL 14+ connection string |
| `GLITCHTIP_DOMAIN` | Full URL with scheme (`https://glitchtip.example.com`) |
| `DEFAULT_FROM_EMAIL` | Sender address for notifications |

### Email

| Method | Config |
|--------|--------|
| SMTP | `EMAIL_URL=smtp://user:pass@host:port` |
| Mailgun | `MAILGUN_API_KEY` + `EMAIL_BACKEND=anymail.backends.mailgun.EmailBackend` |
| SendGrid | `SENDGRID_API_KEY` + `EMAIL_BACKEND=anymail.backends.sendgrid.EmailBackend` |
| Console (dev) | `EMAIL_URL=consolemail://` |

Also supports Postmark, Mailjet, Mandrill, SparkPost, Brevo via Anymail.

### Data Retention

| Variable | Default |
|----------|---------|
| `GLITCHTIP_MAX_EVENT_LIFE_DAYS` | 90 |
| `GLITCHTIP_MAX_TRANSACTION_EVENT_LIFE_DAYS` | (inherits above) |
| `GLITCHTIP_MAX_FILE_LIFE_DAYS` | (inherits above) |
| `GLITCHTIP_MAX_UPTIME_CHECK_LIFE_DAYS` | (inherits above) |

### Cache & Workers

| Variable | Default | Purpose |
|----------|---------|---------|
| `VALKEY_URL` | — | `redis://:pass@host:port/db` (Valkey/Redis 7+) |
| `DATABASE_POOL_MAX_SIZE` | 20 | psycopg connection pool |
| `GRANIAN_WORKERS` | 1 | Web server workers (async, rarely needs >1) |
| `VTASKS_CONCURRENCY` | 20 | Background task concurrency |

Set `VALKEY_URL` to empty string to disable and use PostgreSQL as queue.

### Feature Flags & Security

| Variable | Default | Purpose |
|----------|---------|---------|
| `ENABLE_USER_REGISTRATION` | true | Allow self-signup |
| `ENABLE_ORGANIZATION_CREATION` | false | Allow users to create orgs |
| `GLITCHTIP_ENABLE_UPTIME` | true | Uptime monitoring |
| `GLITCHTIP_ENABLE_MCP` | false | Model Context Protocol server |
| `ENABLE_OBSERVABILITY_API` | false | Prometheus metrics |
| `ALLOWED_HOSTS` | `*` | Comma-separated allowed domains |
| `CSRF_TRUSTED_ORIGINS` | — | Reverse proxy origins |
| `BASE_PATH` | — | Subpath hosting (`/glitchtip`) |

### File Storage

| Backend | `DEFAULT_FILE_STORAGE` | Key Variables |
|---------|----------------------|---------------|
| AWS S3 / DO Spaces | `storages.backends.s3boto3.S3Boto3Storage` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME` |
| Azure Blob | `storages.backends.azure_storage.AzureStorage` | `AZURE_ACCOUNT_NAME`, `AZURE_ACCOUNT_KEY`, `AZURE_CONTAINER` |
| GCS | `storages.backends.gcloud.GoogleCloudStorage` | `GS_BUCKET_NAME`, `GS_PROJECT_ID`, `GOOGLE_APPLICATION_CREDENTIALS` |

## SDK Integration

GlitchTip uses **Sentry SDKs** — 58 implementations across 18 languages. Configure any Sentry SDK by pointing the DSN to the GlitchTip instance:

```
https://<SENTRY_KEY>@<GLITCHTIP_DOMAIN>/<PROJECT_ID>
```

Find the DSN in **Project Settings > Security Endpoint**.

### Supported Platforms

**JavaScript**: Browser, React, Angular, Vue, Ember, Next.js, Backbone
**Node.js**: Express, Koa, Connect, plain Node
**Python**: Django, Flask, Celery, FastAPI (ASGI), AWS Lambda, WSGI, + 10 more
**PHP**: Laravel, Symfony, Drupal, Monolog
**Ruby**: Rails, Rack
**Java**: Android, Log4j, Logback, App Engine
**Go**: net/http, plain Go
**C#**: ASP.NET Core
**Rust**, **Elixir**, **Flutter**, **React Native**, **Electron**, **Cordova**, **C/C++**, **Objective-C**

### Reduce Event Volume

```python
sentry_sdk.init(
    dsn="...",
    traces_sample_rate=0.01,  # 1% of transactions
    sample_rate=0.5,          # 50% of errors
)
```

## Source Maps (sentry-cli)

GlitchTip is Sentry API-compatible but does **not** support the newer artifact-bundle/debug-ID upload flow. Use **legacy release-based uploads** only.

- SDK docs: https://glitchtip.com/sdkdocs
- Install/storage guide: https://glitchtip.com/documentation/install

**Prerequisites**: File storage must be configured (S3/Azure/GCS or local volume) — source maps are storage-backed, not just metadata.

### Discover Org & Project Slugs

```bash
# Slugs ≠ display names. Query the API to find correct values:
curl -s https://<GLITCHTIP_DOMAIN>/api/0/projects/ \
  -H "Authorization: Bearer <AUTH_TOKEN>" | jq '.[].slug'
```

### Legacy Upload Workflow

```bash
# 1. Set release in your SDK init: release: "<RELEASE_ID>"
# 2. Build with source maps enabled
# 3. Upload (--url is a GLOBAL flag, must precede subcommand):
sentry-cli --url https://<GLITCHTIP_DOMAIN> releases \
  --org <org-slug> --project <project-slug> \
  files "<RELEASE_ID>" upload-sourcemaps ./dist \
  --url-prefix "~/"
```

### Bundler Plugin (Vite/Webpack/esbuild/Rollup)

```javascript
// Use uploadLegacySourcemaps — the default artifact-bundle mode
// triggers 404 on GlitchTip's /artifactbundle/assemble/ endpoint
sentryPlugin({
  url: "https://<GLITCHTIP_DOMAIN>",  // REQUIRED — defaults to sentry.io
  authToken: process.env.SENTRY_AUTH_TOKEN,
  org: "<org-slug>",
  project: "<project-slug>",
  release: { uploadLegacySourcemaps: "./dist" },
})
```

### Next.js Specifics

- Set `productionBrowserSourceMaps: true` in `next.config.js`
- Pass `sentryUrl` (not `url`) into `withSentryConfig`
- Watch for trailing slashes in the instance URL — they can break uploads

### Gotchas

| Gotcha | Detail |
|--------|--------|
| `.sentryclirc` ignored | Bundler plugin v2 no longer reads `.sentryclirc` — pass config via plugin options or env vars (`SENTRY_URL`, `SENTRY_AUTH_TOKEN`, `SENTRY_ORG`, `SENTRY_PROJECT`) |
| CLI calls sentry.io | `--url` is a global flag — must come before the subcommand, not after |
| Auth token vs DSN | DSN = SDK event ingestion. Auth token = CLI/API operations (Profile > Auth Tokens). Do not mix them |
| Upload succeeds, UI empty | CLI output can be decoupled from server persistence — always check server logs for 500s |
| `releases finalize` fails | Not fully supported on GlitchTip — skip finalize, rely on release creation + artifact upload |
| Proxy/TLS false 401 | Corporate proxies cause "Invalid token" errors — enable `sentry-cli --log-level debug`, verify proxy env vars are full URLs |

## Uptime Monitoring

Four monitor types:

| Type | Behavior |
|------|----------|
| **Ping** | HTTP HEAD request (most common) |
| **GET** | HTTP GET, validates expected status code |
| **POST** | HTTP POST, validates expected status code |
| **Heartbeat** | Awaits inbound requests from your app at a generated URL |

Link monitors to a project with email alerts configured for status change notifications.

## Integrations

### Alerting

Configure in **Projects > Alert Recipients**:
- **Email**: Team member notifications on error frequency thresholds
- **Webhooks**: POST to any URL on alert trigger

### External Tools

| Tool | Setup |
|------|-------|
| **GitLab** | Settings > Monitor > Error Tracking > Sentry provider > GlitchTip URL + Auth Token |
| **Grafana** | Data source > Sentry type > GlitchTip URL + org + Auth Token |

Auth tokens: **Profile > Auth Tokens** (scope: read-only or full).

### Social Auth (OAuth)

Configure via Django Admin (`/admin/socialaccount/socialapp/`):

GitHub, GitLab, Google, Microsoft, Gitea, DigitalOcean, NextCloud, Okta, OpenID Connect (Keycloak, etc.)

Callback URL: `https://example.com/accounts/<provider>/login/callback/`

OpenID Connect settings:
```json
{ "server_url": "https://idp.example.com/auth/realms/realm/.well-known/openid-configuration" }
```

## CLI Tool (gtc)

```bash
pip install glitchtip-cli
gtc list      # list organizations
gtc create    # create organization
gtc delete    # delete organization
gtc members   # show org membership
```

First run prompts for API token and instance URL. Config saved to `.env`.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Events not appearing | Verify DSN, check SDK `sampleRate`, confirm `GLITCHTIP_DOMAIN` matches |
| High event volume | Lower `traces_sample_rate` / `sample_rate` in SDK config |
| Email not sending | Check `EMAIL_URL` or provider API key, try `consolemail://` for debugging |
| 401 on API/integration | Regenerate Auth Token in Profile > Auth Tokens |
| Worker not processing | Check `VALKEY_URL`, ensure worker container running, verify `VTASKS_CONCURRENCY` |
| Out of memory | Use all-in-one mode (`compose.minimal.yml`) or increase RAM to 512MB+ |
| Uptime checks failing | Verify monitor URL accessible from GlitchTip server, check expected status code |
| Social auth not working | Verify callback URL, check Django Admin socialaccount config |
| Search not working | Check PostgreSQL `text_search_config` for non-English languages |
| Disk growing fast | Lower `GLITCHTIP_MAX_EVENT_LIFE_DAYS`, check source map / file retention |
| 404 on `/artifactbundle/assemble/` | GlitchTip doesn't support artifact-bundle flow — switch to `uploadLegacySourcemaps` or `releases files upload-sourcemaps` |
| "Nothing to upload" but UI empty | Check file storage config (S3/volume), inspect server logs for 500s on assemble endpoint |
| `debug_id_or_release_required` | Upload only `.js` + `.map` pairs, not entire `dist/` — remove files without matching maps |
| `files_fileblob_checksum_key` duplicate | Clean release artifacts before re-uploading identical builds; upload is not idempotent |
| `releases finalize` → "version required" | Skip finalize — not fully supported on GlitchTip. Use release creation + artifact upload only |
| CLI sends to sentry.io unexpectedly | `--url` must precede subcommand; check `.sentryclirc` `defaults.url`; bundler plugin v2 ignores `.sentryclirc` |
| Stack traces stay minified | Verify: (1) storage has files, (2) release value matches SDK init, (3) `--url-prefix` matches runtime paths |
