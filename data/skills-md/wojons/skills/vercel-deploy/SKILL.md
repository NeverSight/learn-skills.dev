---
name: vercel-deploy
description: Deploy applications to Vercel with automatic framework detection
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: deployment
---

# Vercel Deployment Skill

Deploy applications and websites to Vercel with automatic framework detection.

## When to use me

Use this skill when:
- Deploying a web application to production
- Setting up staging/preview deployments
- Migrating from another hosting service
- Testing deployment configuration

## What I do

- Detect framework from project structure (Next.js, Vite, Astro, etc.)
- Validate deployment configuration
- Generate deployment commands
- Provide deployment URLs and settings
- Handle environment variables and build settings

## Examples

```bash
# Deploy current directory to Vercel
agent: Deploy this application to Vercel

# Deploy with specific settings
agent: Deploy to Vercel with production environment variables

# Check deployment configuration
agent: Check if this project is ready for Vercel deployment
```

## Output format

```
## Vercel Deployment

**Project Detected:** Next.js 14 (App Router)
**Framework:** @vercel/nextjs

**Deployment Configuration:**
- Build Command: npm run build
- Output Directory: .next
- Node Version: 18.x

**Deployment Commands:**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

**Environment Variables Required:**
- DATABASE_URL
- API_KEY

**Next Steps:**
1. Set environment variables in Vercel dashboard
2. Run deployment command
3. Access deployment at: https://project-name.vercel.app
```

## Notes

- Requires Vercel CLI or GitHub integration
- Supports automatic framework detection for 40+ frameworks
- Handles both static sites and server-side applications
- Provides claimable deployments for ownership transfer
