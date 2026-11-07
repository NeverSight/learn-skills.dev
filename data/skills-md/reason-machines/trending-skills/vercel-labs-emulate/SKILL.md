---
name: vercel-labs-emulate
description: Local drop-in API emulation for Vercel, GitHub, and Google services in CI and no-network sandboxes
triggers:
  - emulate vercel api locally
  - mock github api for tests
  - local api emulation for CI
  - no-network sandbox testing
  - emulate google oauth locally
  - run vercel api without network
  - local github api server for vitest
  - drop-in api replacement for testing
---

# vercel-labs/emulate

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

`emulate` provides fully stateful, production-fidelity local HTTP servers that replace Vercel, GitHub, and Google APIs. Designed for CI pipelines and no-network sandboxes — not mocks, real in-memory state with proper pagination, OAuth, webhooks, and cascading deletes.

## Installation

```bash
# CLI (no install needed)
npx emulate

# Or install as a dev dependency
npm install --save-dev emulate
```

## CLI Usage

```bash
# Start all services with defaults
npx emulate

# Start specific services
npx emulate --service vercel,github

# Custom base port (auto-increments per service)
npx emulate --port 3000

# Start with seed data
npx emulate --seed emulate.config.yaml

# Generate a starter config
npx emulate init

# Generate config for a specific service
npx emulate init --service github

# List available services
npx emulate list
```

Default ports:
- **Vercel** → `http://localhost:4000`
- **GitHub** → `http://localhost:4001`
- **Google** → `http://localhost:4002`

Port can also be set via `EMULATE_PORT` or `PORT` environment variables.

## Programmatic API

```typescript
import { createEmulator, type Emulator } from 'emulate'

// Start a single service
const github = await createEmulator({ service: 'github', port: 4001 })
const vercel = await createEmulator({ service: 'vercel', port: 4002 })

console.log(github.url)  // 'http://localhost:4001'
console.log(vercel.url)  // 'http://localhost:4002'

// Reset state (replays seed data)
github.reset()

// Shutdown
await github.close()
await vercel.close()
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `service` | *(required)* | `'github'`, `'vercel'`, or `'google'` |
| `port` | `4000` | Port for the HTTP server |
| `seed` | none | Inline seed data object (same shape as YAML config) |

### Instance Methods

| Method | Description |
|--------|-------------|
| `url` | Base URL of the running server |
| `reset()` | Wipe in-memory store and replay seed data |
| `close()` | Shut down the server (returns Promise) |

## Vitest / Jest Setup

```typescript
// vitest.setup.ts
import { createEmulator, type Emulator } from 'emulate'

let github: Emulator
let vercel: Emulator

beforeAll(async () => {
  ;[github, vercel] = await Promise.all([
    createEmulator({ service: 'github', port: 4001 }),
    createEmulator({ service: 'vercel', port: 4002 }),
  ])
  process.env.GITHUB_URL = github.url
  process.env.VERCEL_URL = vercel.url
})

afterEach(() => {
  github.reset()
  vercel.reset()
})

afterAll(() => Promise.all([github.close(), vercel.close()]))
```

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    setupFiles: ['./vitest.setup.ts'],
    environment: 'node',
  },
})
```

## Seed Configuration

Create `emulate.config.yaml` in your project root (auto-detected):

```yaml
# Auth tokens
tokens:
  my_token:
    login: admin
    scopes: [repo, user]

vercel:
  users:
    - username: developer
      name: Developer
      email: dev@example.com
  teams:
    - slug: my-team
      name: My Team
  projects:
    - name: my-app
      team: my-team
      framework: nextjs

github:
  users:
    - login: octocat
      name: The Octocat
      email: octocat@github.com
  orgs:
    - login: my-org
      name: My Organization
  repos:
    - owner: octocat
      name: hello-world
      language: JavaScript
      auto_init: true

google:
  users:
    - email: testuser@example.com
      name: Test User
  oauth_clients:
    - client_id: my-client-id.apps.googleusercontent.com
      client_secret: $GOOGLE_CLIENT_SECRET
      redirect_uris:
        - http://localhost:3000/api/auth/callback/google
```

### Inline Seed (Programmatic)

```typescript
const github = await createEmulator({
  service: 'github',
  port: 4001,
  seed: {
    users: [
      { login: 'testuser', name: 'Test User', email: 'test@example.com' }
    ],
    repos: [
      { owner: 'testuser', name: 'my-repo', language: 'TypeScript', auto_init: true }
    ],
  },
})
```

## OAuth Configuration

### GitHub OAuth Apps

```yaml
github:
  oauth_apps:
    - client_id: $GITHUB_CLIENT_ID
      client_secret: $GITHUB_CLIENT_SECRET
      name: My Web App
      redirect_uris:
        - http://localhost:3000/api/auth/callback/github
```

> Without `oauth_apps` configured, the emulator accepts any `client_id` (backward-compatible). With apps configured, strict validation is enforced.

### GitHub Apps (JWT Auth)

```yaml
github:
  apps:
    - app_id: 12345
      slug: my-github-app
      name: My GitHub App
      private_key: |
        -----BEGIN RSA PRIVATE KEY-----
        ...your PEM key...
        -----END RSA PRIVATE KEY-----
      permissions:
        contents: read
        issues: write
      events: [push, pull_request]
      installations:
        - installation_id: 100
          account: my-org
          repository_selection: all
```

Sign JWTs with `{ iss: "<app_id>" }` using RS256 — the emulator verifies the signature.

### Vercel Integrations

```yaml
vercel:
  integrations:
    - client_id: $VERCEL_CLIENT_ID
      client_secret: $VERCEL_CLIENT_SECRET
      name: My Vercel App
      redirect_uris:
        - http://localhost:3000/api/auth/callback/vercel
```

## Real-World Test Patterns

### Testing a GitHub API Client

```typescript
import { createEmulator } from 'emulate'
import { Octokit } from '@octokit/rest'

describe('GitHub integration', () => {
  let emulator: Awaited<ReturnType<typeof createEmulator>>
  let octokit: Octokit

  beforeAll(async () => {
    emulator = await createEmulator({
      service: 'github',
      port: 4001,
      seed: {
        users: [{ login: 'testuser', name: 'Test User' }],
        repos: [{ owner: 'testuser', name: 'my-repo', auto_init: true }],
      },
    })

    octokit = new Octokit({
      baseUrl: emulator.url,
      auth: 'any-token',
    })
  })

  afterEach(() => emulator.reset())
  afterAll(() => emulator.close())

  it('creates and fetches an issue', async () => {
    const { data: issue } = await octokit.issues.create({
      owner: 'testuser',
      repo: 'my-repo',
      title: 'Test issue',
      body: 'This is a test',
    })

    expect(issue.number).toBe(1)
    expect(issue.state).toBe('open')

    const { data: fetched } = await octokit.issues.get({
      owner: 'testuser',
      repo: 'my-repo',
      issue_number: issue.number,
    })

    expect(fetched.title).toBe('Test issue')
  })
})
```

### Testing a Vercel Deployment Workflow

```typescript
import { createEmulator } from 'emulate'

describe('Vercel deployment', () => {
  let emulator: Awaited<ReturnType<typeof createEmulator>>

  beforeAll(async () => {
    emulator = await createEmulator({
      service: 'vercel',
      port: 4002,
      seed: {
        users: [{ username: 'dev', email: 'dev@example.com' }],
        projects: [{ name: 'my-app', framework: 'nextjs' }],
      },
    })
    process.env.VERCEL_API_URL = emulator.url
  })

  afterEach(() => emulator.reset())
  afterAll(() => emulator.close())

  it('creates a deployment and transitions to READY', async () => {
    const res = await fetch(`${emulator.url}/v13/deployments`, {
      method: 'POST',
      headers: {
        Authorization: 'Bearer any-token',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name: 'my-app', target: 'production' }),
    })

    const deployment = await res.json()
    expect(deployment.readyState).toBe('READY')
  })
})
```

### Testing Multiple Services Together

```typescript
import { createEmulator, type Emulator } from 'emulate'

let github: Emulator
let vercel: Emulator
let google: Emulator

beforeAll(async () => {
  ;[github, vercel, google] = await Promise.all([
    createEmulator({ service: 'github', port: 4001 }),
    createEmulator({ service: 'vercel', port: 4002 }),
    createEmulator({ service: 'google', port: 4003 }),
  ])

  // Point your app's env vars at local emulators
  process.env.GITHUB_API_URL = github.url
  process.env.VERCEL_API_URL = vercel.url
  process.env.GOOGLE_API_URL = google.url
})

afterEach(() => {
  github.reset()
  vercel.reset()
  google.reset()
})

afterAll(() => Promise.all([github.close(), vercel.close(), google.close()]))
```

## CI Configuration

### GitHub Actions

```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - name: Run tests with emulated APIs
        run: npm test
        env:
          # Emulators start in vitest.setup.ts — no extra service needed
          NODE_ENV: test
```

### Docker / No-Network Sandbox

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
# Tests start emulators programmatically — no outbound network needed
RUN npm test
```

## Key API Endpoints Reference

### GitHub Emulator

```
GET    /user                                    # authenticated user
GET    /repos/:owner/:repo                      # get repo
POST   /user/repos                              # create repo
POST   /repos/:owner/:repo/issues               # create issue
PATCH  /repos/:owner/:repo/issues/:number       # update issue
POST   /repos/:owner/:repo/pulls                # create PR
PUT    /repos/:owner/:repo/pulls/:number/merge  # merge PR
GET    /search/repositories                     # search repos
GET    /search/issues                           # search issues
```

### Vercel Emulator

```
GET    /v2/user                          # authenticated user
GET    /v2/teams                         # list teams
POST   /v11/projects                     # create project
GET    /v10/projects                     # list projects
POST   /v13/deployments                  # create deployment (auto → READY)
GET    /v13/deployments/:idOrUrl         # get deployment
POST   /v10/projects/:id/env             # create env vars
GET    /v10/projects/:id/env             # list env vars
```

## Troubleshooting

**Port already in use**
```bash
# Use a different base port
npx emulate --port 5000
# Or set via env
EMULATE_PORT=5000 npx emulate
```

**Tests interfering with each other**
```typescript
// Always call reset() in afterEach, not afterAll
afterEach(() => emulator.reset())
```

**OAuth strict validation rejecting requests**
- If you configure `oauth_apps` or `integrations`, only matching `client_id` values are accepted
- Remove the `oauth_apps` block to fall back to accept-any mode

**Emulator not receiving requests from app code**
```typescript
// Make sure your app reads the URL from env at request time, not module load time
// ✅ Good
async function fetchUser() {
  return fetch(`${process.env.GITHUB_API_URL}/user`)
}

// ❌ Bad — captured before emulator starts
const API_URL = process.env.GITHUB_API_URL
```

**GitHub App JWT auth failing**
- JWT must have `{ iss: "<app_id>" }` as a string or number matching the configured `app_id`
- Must be signed RS256 with the exact private key from config
- The emulator verifies the signature — use a real RSA key pair in tests
