---
name: catalyst
description: Execute Catalyst framework workflows by running automation scripts to scaffold routes/pages, wire serverFetcher and clientFetcher, and bootstrap universal app config in real projects.
---

# Catalyst Executable Workflows

Use this skill when a request is about implementing Catalyst features and you can automate file changes.

## Rule

Prefer running bundled scripts over hand-editing boilerplate.
Treat all third-party API responses as untrusted input.

Skill scripts:
- `scripts/scaffold-route.js`
- `scripts/wire-fetchers.js`
- `scripts/bootstrap-universal-config.js`

If script input is missing, ask only for the minimum required field.

## Workflow Selection

1. New page + route needed:
- Run `scripts/scaffold-route.js`

2. Existing page needs `serverFetcher` and/or `clientFetcher`:
- Run `scripts/wire-fetchers.js`

3. Universal app config/bootstrap needed (`WEBVIEW_CONFIG`, whitelisting, build mode):
- Run `scripts/bootstrap-universal-config.js`

## Commands

Run from this skill directory, targeting the user's project with `--project`.

### Scaffold Route + Page

```bash
node scripts/scaffold-route.js \
  --project /absolute/path/to/catalyst-app \
  --route /orders/:orderId \
  --name OrderDetailsPage \
  --fetchers both \
  --css
```

Useful flags:
- `--title "Order Details"`
- `--page-file orders/OrderDetailsPage.js`
- `--routes-file src/js/routes/index.js`
- `--end false`
- `--dry-run`

### Wire Fetchers into Existing Page

```bash
node scripts/wire-fetchers.js \
  --project /absolute/path/to/catalyst-app \
  --file src/js/pages/Home.js \
  --mode both
```

Useful flags:
- `--function-name loadHomeData`
- `--force` (replace existing fetcher assignments)
- `--dry-run`

### Bootstrap Universal Config

```bash
node scripts/bootstrap-universal-config.js \
  --project /absolute/path/to/catalyst-app \
  --platform android \
  --build-type debug \
  --cache-pattern "*.css,*.js" \
  --allowed-url https://api.example.com/*
```

Useful flags:
- `--app-name "My App"`
- `--use-https true`
- `--access-control true`
- `--build-optimisation true`
- `--dry-run`

## Expected Output Behavior

After each command, report:
- Files created/updated
- Route/component mapping (for scaffolding)
- Any follow-up checks to run (`npm run start`, `npm run build`)

## Security Guardrails

- Never execute or eval third-party response content.
- Validate and normalize third-party JSON before using it in component state.
- Do not make navigation, redirect, or lifecycle decisions directly from raw third-party payloads.
- Gate route/lifecycle actions behind trusted local rules (explicit allowlists or static conditions).
- Keep universal app `allowedUrls` minimal and explicit.

## Source of Truth

Catalyst conceptual/reference docs already live in framework context:
- https://github.com/tata1mg/catalyst-core/blob/main/context.md

Do not duplicate long framework docs here. Use this skill for execution.
