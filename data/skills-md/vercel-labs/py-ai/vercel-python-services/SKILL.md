---
name: vercel-python-services
description: Building Python backend services using Vercel's experimentalServices API. Use when creating Python backends, or multi-service projects with a Python backend and JavaScript frontend.
---

# Python Services with Vercel

Build multi-service projects using Vercel's `experimentalServices` API with a Python backend and (optional) JavaScript frontend.

## Setup

1. Create the project files (see references for the minimal working example). Choose frameworks for each service according to user's requests.
2. Define backend routes without the `/api` prefix (e.g. `@app.get("/health")`). Vercel strips the prefix before forwarding to the backend.
3. Validate services in `vercel.json` have `entrypoint` and `routePrefix`, but no extra unknown fields, otherwise that will cause preview to crash

Only `vercel.json` lives at the root. Each service manages its own dependencies independently.

## Usage

- Use `vercel dev -L` from the project root to run all services as one application. The CLI will handle each individual service's routing and dev server and put the application on port 3000.
- Frontend calls `/api/...` — Vercel routes these to the backend, which sees only the path after the prefix. No localhost URLs, no proxy needed.
