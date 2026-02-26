---
name: deploy-preview
description: |
  Deploy Vercel preview environments, check status, view build logs, and run Lighthouse audits — all from chat. 

  Use when:
  - User wants to deploy a preview or production build
  - User asks to check a deployment's status or logs
  - User wants a performance/accessibility audit on a preview URL
  - User wants to list recent deployments
---

# Deploy Preview

Deploy Vercel previews, check status, view logs, and run Lighthouse audits from your agent.

## Setup

Requires `VERCEL_TOKEN` environment variable. Create one at [vercel.com/account/tokens](https://vercel.com/account/tokens).

Optional: `VERCEL_SCOPE` for team deployments.

## Usage

```bash
VERCEL_TOKEN="$VERCEL_TOKEN" ./scripts/deploy-preview.sh <command> [args]
```

## Commands

| Command | Description |
|---------|-------------|
| `deploy [path] [--prod]` | Deploy preview (or production) and return URL |
| `deploy-branch <path> <branch>` | Checkout branch and deploy preview |
| `status <url-or-id>` | Check deployment state (QUEUED/BUILDING/READY/ERROR) |
| `logs <url-or-id>` | View build logs |
| `audit <preview-url>` | Run Lighthouse audit (performance, a11y, SEO, best practices) |
| `list [project-id]` | Recent deployments |

## Examples

```bash
# Deploy a preview from current directory
deploy-preview.sh deploy

# Deploy a specific branch
deploy-preview.sh deploy-branch ./my-app feature/new-ui

# Check if it's ready
deploy-preview.sh status dpl_abc123

# Run a performance audit
deploy-preview.sh audit https://my-app-abc123.vercel.app

# View build logs
deploy-preview.sh logs dpl_abc123

# List recent deploys
deploy-preview.sh list
```

## Audit Output

The `audit` command uses Google PageSpeed Insights API (free, no extra key needed) and returns:

```json
{
  "performance": 0.94,
  "accessibility": 0.98,
  "bestPractices": 1.0,
  "seo": 0.91,
  "fcp": "1.2 s",
  "lcp": "2.1 s",
  "cls": "0.003",
  "tbt": "120 ms"
}
```

## Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `VERCEL_TOKEN` | Vercel API token | Yes |
| `VERCEL_SCOPE` | Team slug for team deployments | No |

## Requirements

- [Vercel CLI](https://vercel.com/docs/cli) (`npm i -g vercel`)
- `curl`, `jq`
