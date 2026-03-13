---
name: marketplace-deploy
description: Deploys a Sitecore Marketplace app to Vercel with correct CSP headers and configuration.
disable-model-invocation: true
---

# Deploy to Vercel

You are helping the user deploy their Sitecore Marketplace app to Vercel.

**Important**: This skill has real side effects (deploying to production). Confirm each step with the user before executing.

## Pre-Deploy Checklist

Before deploying, verify:

1. **Build succeeds locally**:
```bash
npm run build
```

2. **CSP headers are configured** — Check `next.config.ts` for `frame-ancestors`:
```typescript
// next.config.ts must include:
headers: [
  {
    source: "/(.*)",
    headers: [
      {
        key: "Content-Security-Policy",
        value: "frame-ancestors 'self' https://*.sitecorecloud.io",
      },
    ],
  },
]
```

3. **Environment variables are set** — Check that `.env.local` exists and has required values

4. **Extension points are registered** — All routes defined in the app should be registered in the Developer Portal

## Deploy Steps

### Step 1: Install Vercel CLI (if needed)
```bash
npm i -g vercel
```

### Step 2: Link to Vercel project
```bash
vercel link
```

### Step 3: Set environment variables
```bash
# For client-side apps
vercel env add NEXT_PUBLIC_SITECORE_APP_ID

# For full-stack (Auth0) apps — add all Auth0 vars too
vercel env add AUTH0_SECRET
vercel env add AUTH0_BASE_URL
vercel env add AUTH0_ISSUER_BASE_URL
vercel env add AUTH0_CLIENT_ID
vercel env add AUTH0_CLIENT_SECRET
vercel env add AUTH0_AUDIENCE
vercel env add AUTH0_SCOPE
```

### Step 4: Deploy
```bash
# Preview deployment
vercel

# Production deployment
vercel --prod
```

### Step 5: Post-Deploy Configuration

After deploying:
1. Copy the production URL from Vercel
2. Go to Sitecore Developer Portal → Your App → Settings
3. Set the **App URL** to the Vercel production URL
4. Update `AUTH0_BASE_URL` env var in Vercel to match the production URL (if using Auth0)

## Reference Files
- [Vercel Config](references/vercel-config.md) — vercel.json and next.config.ts templates
