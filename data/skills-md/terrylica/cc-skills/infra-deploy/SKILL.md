---
name: infra-deploy
description: Cal.com self-hosted deployment to GCP Cloud Run with Supabase PostgreSQL. Docker Compose for local dev. TRIGGERS - deploy calcom, cloud run, self-hosted, docker compose, supabase, gcp deploy, infrastructure, cal.com hosting.
allowed-tools: Read, Bash, Grep, Glob, Write, AskUserQuestion
disable-model-invocation: true
---

# Infrastructure Deployment

Deploy Cal.com self-hosted to GCP Cloud Run with Supabase PostgreSQL, or run locally via Docker Compose.

## Mandatory Preflight

### Step 1: Check GCP Project Configuration

```bash
echo "CALCOM_GCP_PROJECT: ${CALCOM_GCP_PROJECT:-NOT_SET}"
echo "CALCOM_GCP_ACCOUNT: ${CALCOM_GCP_ACCOUNT:-NOT_SET}"
echo "CALCOM_GCP_REGION: ${CALCOM_GCP_REGION:-us-central1}"
```

**If NOT_SET**: These must be configured in `.mise.local.toml`. Run the setup command.

### Step 2: Verify GCP Authentication

```bash
gcloud auth list --filter="status=ACTIVE" --format="value(account)" 2>/dev/null
```

### Step 3: Check Supabase Configuration

```bash
echo "SUPABASE_PROJECT_REF: ${SUPABASE_PROJECT_REF:-NOT_SET}"
echo "SUPABASE_DB_URL_REF: ${SUPABASE_DB_URL_REF:-NOT_SET}"
```

### Step 4: Verify Cal.com Secrets

```bash
echo "CALCOM_NEXTAUTH_SECRET_REF: ${CALCOM_NEXTAUTH_SECRET_REF:-NOT_SET}"
echo "CALCOM_ENCRYPTION_KEY_REF: ${CALCOM_ENCRYPTION_KEY_REF:-NOT_SET}"
echo "CALCOM_CRON_API_KEY_REF: ${CALCOM_CRON_API_KEY_REF:-NOT_SET}"
```

**All 1Password references must be SET.** Secrets are stored in Claude Automation vault.

---

## Deploy Target: GCP Cloud Run

### Step 1: Verify GCP APIs Enabled

```bash
gcloud services list --enabled \
  --project="$CALCOM_GCP_PROJECT" \
  --account="$CALCOM_GCP_ACCOUNT" 2>/dev/null | grep -E "run|artifact|build"
```

Required APIs: Cloud Run, Artifact Registry, Cloud Build.

### Step 2: Build Container

```bash
# From the cal.com fork directory
cd ~/fork-tools/cal.com

# Build Docker image
docker build -t calcom-self-hosted .
```

### Step 3: Push to Artifact Registry

```bash
# Tag for Artifact Registry
docker tag calcom-self-hosted \
  "${CALCOM_GCP_REGION}-docker.pkg.dev/${CALCOM_GCP_PROJECT}/calcom/calcom:latest"

# Push
docker push \
  "${CALCOM_GCP_REGION}-docker.pkg.dev/${CALCOM_GCP_PROJECT}/calcom/calcom:latest"
```

### Step 4: Deploy to Cloud Run

```bash
# Resolve secrets from 1Password
NEXTAUTH_SECRET=$(op read "$CALCOM_NEXTAUTH_SECRET_REF")
ENCRYPTION_KEY=$(op read "$CALCOM_ENCRYPTION_KEY_REF")
CRON_API_KEY=$(op read "$CALCOM_CRON_API_KEY_REF")
DATABASE_URL=$(op read "$SUPABASE_DB_URL_REF")

gcloud run deploy calcom \
  --image="${CALCOM_GCP_REGION}-docker.pkg.dev/${CALCOM_GCP_PROJECT}/calcom/calcom:latest" \
  --region="$CALCOM_GCP_REGION" \
  --project="$CALCOM_GCP_PROJECT" \
  --account="$CALCOM_GCP_ACCOUNT" \
  --platform=managed \
  --allow-unauthenticated \
  --port=3000 \
  --memory=512Mi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=2 \
  --set-env-vars="DATABASE_URL=${DATABASE_URL}" \
  --set-env-vars="NEXTAUTH_SECRET=${NEXTAUTH_SECRET}" \
  --set-env-vars="CALENDSO_ENCRYPTION_KEY=${ENCRYPTION_KEY}" \
  --set-env-vars="CRON_API_KEY=${CRON_API_KEY}" \
  --set-env-vars="NEXT_PUBLIC_WEBAPP_URL=https://calcom-${CALCOM_GCP_PROJECT}.run.app" \
  --set-env-vars="NEXT_PUBLIC_API_V2_URL=https://calcom-${CALCOM_GCP_PROJECT}.run.app/api/v2"
```

---

## Deploy Target: Docker Compose (Local Dev)

### docker-compose.yml Template

```yaml
version: "3.9"
services:
  calcom:
    image: calcom/cal.com:latest
    restart: unless-stopped
    ports:
      - "3000:3000"
    env_file:
      - .env
    depends_on:
      database:
        condition: service_healthy

  database:
    image: postgres:15
    restart: unless-stopped
    volumes:
      - calcom-db:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: calcom
      POSTGRES_PASSWORD: calcom
      POSTGRES_DB: calcom
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U calcom"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  calcom-db:
```

### Local .env Template

```bash
DATABASE_URL=postgresql://calcom:calcom@database:5432/calcom
NEXTAUTH_SECRET=<generate-with-openssl>
CALENDSO_ENCRYPTION_KEY=<generate-with-openssl>
CRON_API_KEY=<generate-with-openssl>
NEXT_PUBLIC_WEBAPP_URL=http://localhost:3000
NEXT_PUBLIC_API_V2_URL=http://localhost:3000/api/v2
```

---

## Deploy Target: Webhook Relay (Pushover Notifications)

Lightweight Cloud Run service bridging Cal.com webhooks to Pushover emergency alerts. Zero dependencies (Python stdlib only).

### Step 1: Verify Pushover Credentials

```bash
echo "PUSHOVER_APP_TOKEN: ${PUSHOVER_APP_TOKEN:+SET}"
echo "PUSHOVER_USER_KEY: ${PUSHOVER_USER_KEY:+SET}"
echo "PUSHOVER_SOUND: ${PUSHOVER_SOUND:-dune}"
```

**All must be SET.** See [pushover-setup.md](../booking-notify/references/pushover-setup.md) for credential setup.

### Step 2: Deploy Webhook Relay to Cloud Run

```bash
RELAY_SOURCE="$HOME/.claude/plugins/marketplaces/cc-skills/plugins/calcom-commander/scripts/webhook-relay"

gcloud run deploy calcom-pushover-webhook \
  --source "$RELAY_SOURCE" \
  --project="$CALCOM_GCP_PROJECT" \
  --account="$CALCOM_GCP_ACCOUNT" \
  --region="$CALCOM_GCP_REGION" \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars="PUSHOVER_TOKEN=$PUSHOVER_APP_TOKEN,PUSHOVER_USER=$PUSHOVER_USER_KEY,PUSHOVER_SOUND=${PUSHOVER_SOUND:-dune}" \
  --memory=128Mi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=1 \
  --timeout=30 \
  --quiet
```

Note the **Service URL** from the output. Store in `.mise.local.toml` as `WEBHOOK_RELAY_URL`.

### Step 3: Verify Health

```bash
curl -s "$WEBHOOK_RELAY_URL" | python3 -m json.tool
# Expected: {"status": "healthy", "service": "calcom-pushover-webhook"}
```

### Step 4: Register Cal.com Webhook

```bash
CALCOM_API_KEY=$(op item get "$CALCOM_OP_UUID" --vault "Claude Automation" --fields password --reveal)

curl -s -X POST "https://api.cal.com/v1/webhooks?apiKey=$CALCOM_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"subscriberUrl\":\"$WEBHOOK_RELAY_URL\",\"eventTriggers\":[\"BOOKING_CREATED\",\"BOOKING_RESCHEDULED\",\"BOOKING_CANCELLED\"],\"active\":true}"
```

### Step 5: Test with Simulated Booking

```bash
curl -s -X POST "$WEBHOOK_RELAY_URL" \
  -H "Content-Type: application/json" \
  -d '{"triggerEvent":"BOOKING_CREATED","payload":{"title":"Test Meeting","attendees":[{"name":"Test User"}],"startTime":"2026-01-01T10:00:00Z","endTime":"2026-01-01T10:30:00Z"}}'
```

Expected: Pushover emergency alert with "dune" sound on your device.

---

## Supabase Database Management

### Check Connection

```bash
DATABASE_URL=$(op read "$SUPABASE_DB_URL_REF")
psql "$DATABASE_URL" -c "SELECT version();"
```

### Run Migrations

```bash
cd ~/fork-tools/cal.com
DATABASE_URL=$(op read "$SUPABASE_DB_URL_REF") npx prisma migrate deploy
```

## 1Password Secret References

All secrets in Claude Automation vault (biometric-free access):

| Secret                    | 1Password Reference                                        |
| ------------------------- | ---------------------------------------------------------- |
| `NEXTAUTH_SECRET`         | `op://Claude Automation/<item-id>/NEXTAUTH_SECRET`         |
| `CALENDSO_ENCRYPTION_KEY` | `op://Claude Automation/<item-id>/CALENDSO_ENCRYPTION_KEY` |
| `CRON_API_KEY`            | `op://Claude Automation/<item-id>/CRON_API_KEY`            |
| `DATABASE_URL`            | `op://Claude Automation/<item-id>/DATABASE_URL`            |
| `DATABASE_DIRECT_URL`     | `op://Claude Automation/<item-id>/DATABASE_DIRECT_URL`     |

## Post-Change Checklist

- [ ] YAML frontmatter valid (no colons in description)
- [ ] Trigger keywords current
- [ ] Path patterns use $HOME not hardcoded paths
- [ ] 1Password references are agnostic (no hardcoded UUIDs)
