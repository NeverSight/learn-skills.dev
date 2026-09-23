---
name: vercel-monorepo-deploy
description: Best practices, configurations, and automation runbook for deploying monorepo frontends (Next.js, Vite SPAs, React) to Vercel. Covers Vercel CLI GitHub Actions pipelines (free organization bypass), turbo-ignore build skipping, client-side routing rewrites in vercel.json, monorepo root directory setup, NEXT_PUBLIC build-time injection, remote API environment wiring with Cloudflare Tunnels, and Node 22/pnpm 10 compatibility. Use whenever configuring or debugging Vercel deployments from a pnpm/npm monorepo.
---

# Vercel Monorepo Frontend Deployment Runbook

This skill establishes the production standard for deploying frontend applications (`apps/web`) from a pnpm/Turbo monorepo to Vercel, connected to remote backends exposed via Cloudflare Tunnels or custom domains.

---

## 1. Project Configuration in Vercel Dashboard

When importing the monorepo Git repository into Vercel, set these project settings:

| Setting | Value | Why |
| :--- | :--- | :--- |
| **Framework Preset** | *Auto-detected* (Next.js / Vite / Create React App) | Correct build presets |
| **Root Directory** | `apps/web` *(or leave empty if using root build)* | Scopes build context |
| **Include source files outside Root Directory** | **Checked (Enabled)** | Allows Vercel to access `packages/types`, `packages/tsconfig` and root `pnpm-lock.yaml` |
| **Build Command** | `cd ../.. && pnpm turbo run build --filter=web...` (if root is `apps/web`) or override with `pnpm --filter=web build` | Builds dependencies first |
| **Output Directory** | `dist` (for Vite/SPA) or `.next` (for Next.js) | Standard build output |
| **Install Command** | `pnpm install` | Uses workspace root lockfile |

---

## 2. Automated Deployment with Vercel CLI (GitHub Actions)

### Why Vercel CLI over Native Git Integration?
- **Hobby Plan Restriction**: Vercel prohibits direct Git repo connections for repositories that are **both private and owned by a GitHub Organization** (demands upgrade to Pro).
- **Free Workaround**: Deploying via **Vercel CLI in GitHub Actions** compiles the bundle and uploads it directly via the Vercel API without organization paywalls.

### Required Secrets in GitHub (`Settings > Secrets and variables > Actions`):
- `VERCEL_TOKEN`: Personal token from *Vercel Account Settings > Tokens*.
- `VERCEL_PROJECT_ID`: ID from *Vercel Project Settings > General*.
- `VERCEL_ORG_ID`: Account/Team ID from *Vercel Project Settings > General*.
- `NEXT_PUBLIC_API_URL` / `VITE_API_URL`: Cloudflare Tunnel URL (e.g. `https://api.tudominio.com`).

### Production Workflow Step (`.github/workflows/deploy.yml`):
```yaml
deploy-frontend:
  name: Build & Deploy Frontend to Vercel
  runs-on: ubuntu-latest
  steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Setup Node.js (Node 22 required for pnpm 10 / node:sqlite)
      uses: actions/setup-node@v4
      with:
        node-version: 22

    - name: Install pnpm & Vercel CLI
      run: npm install --global pnpm@latest vercel@latest

    - name: Pull Vercel Environment Information
      run: |
        vercel pull --yes --environment=production --token=${{ secrets.VERCEL_TOKEN }}
        if [ -f .vercel/.env.production.local ]; then
          cp .vercel/.env.production.local apps/web/.env.production.local 2>/dev/null || cp .vercel/.env.production.local frontend/.env.production.local 2>/dev/null || true
        fi
      env:
        VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
        VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

    - name: Build Project Artifacts
      run: vercel build --prod --token=${{ secrets.VERCEL_TOKEN }}
      env:
        VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
        VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
        NEXT_PUBLIC_API_URL: ${{ secrets.NEXT_PUBLIC_API_URL }}
        VITE_API_URL: ${{ secrets.VITE_API_URL || secrets.NEXT_PUBLIC_API_URL }}

    - name: Deploy Prebuilt Artifacts to Vercel
      run: vercel deploy --prebuilt --prod --token=${{ secrets.VERCEL_TOKEN }}
      env:
        VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
        VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
        NEXT_PUBLIC_API_URL: ${{ secrets.NEXT_PUBLIC_API_URL }}
        VITE_API_URL: ${{ secrets.VITE_API_URL || secrets.NEXT_PUBLIC_API_URL }}
```

---

## 3. Critical Monorepo Pitfalls & Solutions

### 1. `NEXT_PUBLIC_*` Build-Time Ingestion (Error 404 on Auth/API)
- **Problem**: In Next.js, `NEXT_PUBLIC_*` variables are baked into the static browser bundle at **build time**. If omitted during `vercel build`, client API requests default to relative paths on the Vercel domain (`https://app.vercel.app/auth/login` -> 404).
- **Solution**: Pass `NEXT_PUBLIC_API_URL` directly in the `env` blocks of `vercel build` and `vercel deploy`, and copy `.vercel/.env.production.local` to `apps/web/.env.production.local`.

### 2. Monorepo Root Duplication (`apps/web/apps/web/package.json ENOENT`)
- **Problem**: `Error: ENOENT: no such file or directory, open '.../apps/web/apps/web/package.json'`.
- **Causa**: Vercel project already configured `Root Directory: apps/web`. Adding `working-directory: ./apps/web` in GitHub Actions causes the CLI to duplicate the path.
- **Solution**: Run all Vercel CLI commands strictly from the **monorepo root** without `working-directory`.

### 3. Node.js 22 & pnpm 10 Compatibility (`node:sqlite`)
- **Problem**: `ERR_UNKNOWN_BUILTIN_MODULE: No such built-in module: node:sqlite` during CI build.
- **Causa**: pnpm v10+ uses `node:sqlite`, which requires Node.js v22.13+.
- **Solution**: Always configure `actions/setup-node@v4` with `node-version: 22`.

---

## 4. Preventing Unnecessary Builds (`turbo-ignore`)

To avoid wasting Vercel build minutes when only backend or docker files change:

### In Vercel Project Settings > Git > Ignored Build Step:
Select **Custom** and enter:
```bash
npx turbo-ignore web
```

- If changes only affected `apps/api` or unrelated files, the build exits with code `0` (canceled) with zero cost.
- If changes touched `apps/web`, `packages/types`, or `packages/tsconfig`, Vercel proceeds with the deployment.

---

## 5. SPA Client-Side Routing (`vercel.json`)

For Single Page Applications (**Vite**, React Router, Vue Router, Svelte) to prevent 404 errors on browser page refreshes:

Create `apps/web/vercel.json`:
```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-XSS-Protection", "value": "1; mode=block" }
      ]
    }
  ]
}
```

> [!NOTE]
> For **Next.js** applications, `vercel.json` is not required as Next.js handles server-side and client-side routing natively.

---

## 6. Environment Variables Wiring

Connect the Vercel frontend to the backend running on Raspberry Pi / Cloudflare Tunnel:

### For Vite SPAs:
In Vercel **Environment Variables**:
- `VITE_API_URL`: `https://api.tudominio.com` (Production)
- `VITE_API_URL`: `https://dev-api.tudominio.com` (Preview / Staging)

In Frontend Code:
```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3004';
export const apiClient = axios.create({ baseURL: API_URL, withCredentials: true });
```

### For Next.js:
In Vercel **Environment Variables**:
- `NEXT_PUBLIC_API_URL`: `https://api.tudominio.com`

In Frontend Code:
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3004';
```

---

## 7. Just-In-Time (JIT) Monorepo Package Transpilation

To consume shared packages (`@repo/types`, `@repo/ui`) directly without needing a separate compilation step (`tsup`/`tsc`) during Vercel builds:

### In Next.js (`apps/web/next.config.js`):
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ['@repo/types'],
  output: 'standalone', // Needed for Docker, ignored safely by Vercel
};

module.exports = nextConfig;
```

### In Vite (`apps/web/vite.config.ts`):
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@repo/types': path.resolve(__dirname, '../../packages/types/src'),
    },
  },
});
```

---

## 8. Deployment Checklist

- [ ] Vercel Root Directory set to `apps/web` with "Include files outside Root" checked.
- [ ] Vercel CLI secrets configured in GitHub (`VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`).
- [ ] Node.js version set to `22` in CI workflow (`actions/setup-node@v4`).
- [ ] `NEXT_PUBLIC_API_URL` or `VITE_API_URL` passed in `vercel build` and `vercel deploy` steps.
- [ ] Vercel CLI executed from monorepo root without `working-directory` duplicate flag.
- [ ] Ignored Build Step configured with `npx turbo-ignore web`.
- [ ] `vercel.json` created in `apps/web` (for Vite/SPA apps).
- [ ] Backend CORS configured to accept `https://*.vercel.app` and custom domain.

---

## 9. Deep-Dive Reference Guides

- [Vercel Preview Deployments, Environment Matrix & Troubleshooting](./references/preview-deployments-and-troubleshooting.md) (Automated PR preview workflows via GitHub Actions and Vercel CLI, root cause troubleshooting matrix).

