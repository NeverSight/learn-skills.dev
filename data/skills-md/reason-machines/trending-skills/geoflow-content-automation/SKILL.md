---
name: geoflow-content-automation
description: GEOFlow open-source GEO/SEO content production system with AI generation, review workflow, and publishing pipeline built on PHP and PostgreSQL.
triggers:
  - set up GEOFlow content automation
  - configure AI content generation with GEOFlow
  - create content tasks in GEOFlow
  - manage articles with GEOFlow review workflow
  - deploy GEOFlow with Docker
  - integrate GEOFlow API for content publishing
  - troubleshoot GEOFlow worker or scheduler
  - add AI model to GEOFlow
---

# GEOFlow Content Automation

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

GEOFlow is an open-source PHP/PostgreSQL system for automated GEO/SEO content production. It chains model configuration, material management, task scheduling, draft review, and front-end publishing into a single pipeline. It supports any OpenAI-compatible API, runs on Docker Compose, and exposes both a REST API and a CLI.

---

## Installation

### Docker (Recommended)

```bash
git clone https://github.com/yaojingang/GEOFlow.git
cd GEOFlow
cp .env.example .env
# Edit .env — set APP_SECRET_KEY, SITE_URL, and DB credentials
vi .env

# Start web + postgres + scheduler + worker
docker compose --profile scheduler up -d --build

# Front-end
open http://localhost:18080
# Admin panel
open http://localhost:18080/geo_admin/
```

### Local PHP Server

```bash
git clone https://github.com/yaojingang/GEOFlow.git
cd GEOFlow

export DB_DRIVER=pgsql
export DB_HOST=127.0.0.1
export DB_PORT=5432
export DB_NAME=geo_system
export DB_USER=geo_user
export DB_PASSWORD=geo_password
export APP_SECRET_KEY=$(openssl rand -hex 32)
export SITE_URL=http://localhost:8080

php -S localhost:8080 router.php
open http://localhost:8080/geo_admin/
```

**Requirements:** PHP 7.4+, extensions `pdo_pgsql` and `curl`, PostgreSQL instance.

---

## Environment Variables

```dotenv
# .env (copy from .env.example)

HOST_PORT=18080
SITE_URL=http://localhost:18080
APP_SECRET_KEY=$APP_SECRET_KEY          # 32+ char random string — never hardcode
CRON_INTERVAL=60                         # Scheduler poll interval in seconds
TZ=Asia/Shanghai

# Database
DB_DRIVER=pgsql
DB_HOST=postgres
DB_PORT=5432
DB_NAME=geo_system
DB_USER=geo_user
DB_PASSWORD=$DB_PASSWORD                 # Set via environment, not hardcoded
```

Generate a secure key:

```bash
openssl rand -hex 32
# or
php -r "echo bin2hex(random_bytes(32));"
```

---

## Default Credentials

After first boot, log in at `/geo_admin/` with:

- **Username:** `admin`
- **Password:** `admin888`

**Change both immediately** and rotate `APP_SECRET_KEY` before any public deployment.

---

## Docker Services

| Service | Purpose | Profile |
|---|---|---|
| `web` | Front-end + admin HTTP | always |
| `postgres` | PostgreSQL database | always |
| `scheduler` | Scans tasks, writes job queue | `scheduler` |
| `worker` | Calls AI API, generates content | `scheduler` |

```bash
# Web only (no generation)
docker compose up -d

# Full stack
docker compose --profile scheduler up -d

# Logs
docker compose logs -f worker
docker compose logs -f scheduler

# Restart a single service
docker compose restart worker

# Stop everything
docker compose --profile scheduler down
```

---

## Content Generation Pipeline

```
Admin: configure model + prompts + materials
  ↓
Create Task (title library, model, prompt, image library, publish rules)
  ↓
Scheduler (bin/cron.php) → writes to job_queue table
  ↓
Worker (bin/worker.php) → calls AI API → generates article body
  ↓
Optional: insert images, build SEO meta
  ↓
Article enters draft → review → publish states
  ↓
Front-end renders article + SEO/OG tags
```

---

## Admin Workflow

### 1. Add an AI Model

Navigate to **AI配置中心 → AI模型管理** and fill in:

- API Base URL (e.g. `https://api.openai.com/v1`)
- Model ID (e.g. `gpt-4o`)
- API Key (stored encrypted; reference `$AI_API_KEY` in your env)

### 2. Create Materials

- **标题库** — Title pool the task draws from
- **图片库** — Image pool for article illustrations
- **知识库** — Reference knowledge injected into prompts
- **提示词模板** — Prompt templates with placeholders

### 3. Create a Task

Navigate to **任务管理 → 新建任务**:

```
Title Library  → selects article titles
Model          → which AI model to call
Prompt         → which prompt template
Image Library  → optional illustration set
Publish Mode   → draft | auto-publish
Schedule       → immediate | cron-based
```

### 4. Monitor Execution

- **任务管理** — Task status, retry controls
- **文章管理** — Draft/review/published states
- **审核中心** — Review queue for human approval

---

## CLI (`bin/geoflow`)

The CLI is the programmatic interface used by automation scripts and the companion skill [`yaojingang/yao-geo-skills`](https://github.com/yaojingang/yao-geo-skills).

```bash
# List available commands
php bin/geoflow help

# Check task status
php bin/geoflow task:status --task-id=<id>

# Create a task
php bin/geoflow task:create \
  --title-library=<id> \
  --model=<id> \
  --prompt=<id> \
  --publish-mode=draft

# Upload an article draft
php bin/geoflow article:create \
  --title="Article Title" \
  --body="<markdown content>" \
  --status=draft

# Review and publish an article
php bin/geoflow article:review --article-id=<id> --action=approve
php bin/geoflow article:publish --article-id=<id>

# Run scheduler manually (one cycle)
php bin/cron.php

# Run worker manually (processes one job then exits)
php bin/worker.php --once
```

---

## REST API (`/api/v1`)

All endpoints require Bearer token authentication.

### Generate an API Token

```bash
php bin/api/create_token.php --name="my-integration"
# Outputs token — store in $GEOFLOW_API_TOKEN
```

### Common Endpoints

```bash
BASE=http://localhost:18080/api/v1
TOKEN=$GEOFLOW_API_TOKEN

# List tasks
curl -H "Authorization: Bearer $TOKEN" "$BASE/tasks"

# Get task detail
curl -H "Authorization: Bearer $TOKEN" "$BASE/tasks/<id>"

# Create task
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title_library_id": 1,
    "model_id": 2,
    "prompt_id": 3,
    "publish_mode": "draft"
  }' \
  "$BASE/tasks"

# List articles
curl -H "Authorization: Bearer $TOKEN" "$BASE/articles"

# Publish article
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE/articles/<id>/publish"

# Check job queue
curl -H "Authorization: Bearer $TOKEN" "$BASE/jobs?status=pending"
```

---

## PHP Code Examples

### Connect to the Database (using GEOFlow's own layer)

```php
<?php
// includes/db_support.php provides the connection helper
require_once __DIR__ . '/includes/db_support.php';

$pdo = get_db_connection(); // Returns a PDO instance

// Always use prepared statements
$stmt = $pdo->prepare("SELECT * FROM articles WHERE status = :status ORDER BY created_at DESC LIMIT 10");
$stmt->execute([':status' => 'published']);
$articles = $stmt->fetchAll(PDO::FETCH_ASSOC);
```

### Call the Article Service

```php
<?php
require_once __DIR__ . '/includes/article_service.php';

// Create a draft
$articleId = create_article([
    'title'       => 'My Article Title',
    'body'        => '## Introduction\n\nContent here...',
    'status'      => 'draft',
    'task_id'     => 42,
    'seo_title'   => 'My Article Title | Site Name',
    'seo_desc'    => 'Short description for search engines.',
]);

// Approve and publish
approve_article($articleId);
publish_article($articleId);
```

### Trigger the AI Engine Directly

```php
<?php
require_once __DIR__ . '/includes/ai_engine.php';

// Execute a single task job (task_id, job_id)
$result = run_task_job(taskId: 5, jobId: 101);

if ($result['success']) {
    echo "Article created: " . $result['article_id'];
} else {
    echo "Error: " . $result['error'];
}
```

### Queue a Job Manually

```php
<?php
require_once __DIR__ . '/includes/job_queue_service.php';

// Claim next available job (used by worker)
$job = claim_next_job();

if ($job) {
    try {
        // ... process the job ...
        complete_job($job['id']);
    } catch (Exception $e) {
        fail_job($job['id'], $e->getMessage());
        // Eligible jobs will be retried by scheduler
    }
}

// Manually enqueue a task
enqueue_task_jobs(taskId: 5);
```

### Custom Prompt Template in PHP

```php
<?php
// Prompt templates support placeholder substitution
$template = "You are an SEO writer. Write a 600-word article about: {{title}}\n\nBackground knowledge:\n{{knowledge}}";

$prompt = str_replace(
    ['{{title}}', '{{knowledge}}'],
    [$articleTitle, $knowledgeBaseContent],
    $template
);

// Pass to AI service
require_once __DIR__ . '/includes/ai_service.php';
$response = call_ai_model(modelId: 2, prompt: $prompt);
echo $response['content'];
```

---

## Directory Reference

```
GEOFlow/
├── index.php                 Front-end article list
├── article.php               Article detail page (SEO + OG)
├── router.php                Local dev router for php -S
├── admin/                    All admin UI pages
├── api/v1/index.php          REST API single entry point
├── bin/
│   ├── geoflow               CLI entrypoint
│   ├── cron.php              Scheduler (run every CRON_INTERVAL seconds)
│   └── worker.php            AI generation worker (long-running)
├── includes/
│   ├── config.php            Global config + constants
│   ├── database.php          Front-end data access
│   ├── ai_engine.php         Core generation orchestration
│   ├── ai_service.php        OpenAI-compatible HTTP client
│   ├── job_queue_service.php Claim / complete / fail / retry
│   ├── task_service.php      Task CRUD
│   ├── article_service.php   Article lifecycle
│   └── api_auth.php          Bearer token auth
└── docs/                     Deployment + API + FAQ docs
```

---

## Common Patterns

### Auto-publish without review

When creating a task, set `publish_mode = auto`. The worker will call `publish_article()` immediately after generation, skipping the review queue.

### Batch retry failed jobs

```bash
# Via CLI
php bin/geoflow job:retry-failed --task-id=<id>

# Via database (emergency)
psql $DATABASE_URL -c "UPDATE job_queue SET status='pending', attempts=0 WHERE status='failed' AND task_id=5;"
```

### Run scheduler outside Docker

```bash
# Add to crontab — runs every minute
* * * * * cd /path/to/GEOFlow && php bin/cron.php >> /var/log/geoflow-cron.log 2>&1

# Or loop manually
while true; do php bin/cron.php; sleep 60; done
```

### Database maintenance

```bash
php bin/db_maintenance.php --vacuum
php bin/db_maintenance.php --clean-old-jobs --days=30
```

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Worker generates nothing | Scheduler not running | Start with `--profile scheduler` or run `cron.php` |
| `pdo_pgsql` not found | Extension missing | Add `extension=pdo_pgsql` to `php.ini` or install `php-pgsql` |
| 500 on admin pages | DB not initialized | Let the web container complete its entrypoint migration on first boot |
| AI calls return 401 | Wrong API key | Re-enter key in **AI模型管理**; check key has no leading/trailing spaces |
| Articles stuck in draft | Auto-publish off | Set `publish_mode=auto` on the task, or manually approve in 审核中心 |
| Jobs pile up in queue | Worker crashed | `docker compose restart worker`; check `docker compose logs worker` |
| CSRF token mismatch | Session expired | Re-login to admin; ensure `APP_SECRET_KEY` is stable across restarts |

### Useful Log Commands

```bash
# All services
docker compose logs -f

# Only errors
docker compose logs worker 2>&1 | grep -i error

# Scheduler activity
docker compose logs scheduler | tail -50

# Check pending jobs in DB
docker compose exec postgres psql -U geo_user -d geo_system \
  -c "SELECT status, COUNT(*) FROM job_queue GROUP BY status;"
```

---

## Security Checklist

- [ ] Change default `admin` / `admin888` credentials immediately
- [ ] Set `APP_SECRET_KEY` to a 32+ character random string via environment variable
- [ ] Never commit `.env` — it is in `.gitignore` by default
- [ ] Use HTTPS in production; set `SITE_URL` to your `https://` domain
- [ ] Restrict `/geo_admin/` and `/api/v1/` with network-level firewall in production
- [ ] Rotate API tokens periodically via `php bin/api/create_token.php`
