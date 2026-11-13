---
name: deployment
description: Deploy the application to production. Guides through Convex and Vercel deployment.
allowed-tools: Bash, Read, WebFetch
user-invocable: true
---

# Deployment Skill

Guide for deploying Vibe Stack to production.

## Pre-Deployment Checklist

- [ ] All tests pass: `pnpm build`
- [ ] Environment variables configured
- [ ] Convex schema deployed: `npx convex deploy`
- [ ] Stripe webhook endpoint configured

## Convex Deployment

```bash
# Deploy Convex functions to production
npx convex deploy

# This will:
# 1. Push schema changes
# 2. Deploy all functions
# 3. Run any migrations
```

## Vercel Deployment

### Required Environment Variables

Set these in Vercel dashboard:

```
NEXT_PUBLIC_CONVEX_URL=https://your-project.convex.cloud
CONVEX_DEPLOY_KEY=prod:your-deploy-key
AUTH_SECRET=your-auth-secret
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

### Build Settings

- Framework Preset: Next.js
- Build Command: `pnpm build`
- Output Directory: `.next`
- Install Command: `pnpm install`

## Post-Deployment

### Stripe Webhook Setup

1. Go to Stripe Dashboard > Developers > Webhooks
2. Add endpoint: `https://your-domain.com/api/stripe/webhook`
3. Select events:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
4. Copy signing secret to `STRIPE_WEBHOOK_SECRET`

### Monitoring

- Check Convex dashboard for function errors
- Monitor Vercel logs for API issues
- Review Stripe webhook delivery status

## Rollback

If issues occur:

1. Convex: Previous deployments available in dashboard
2. Vercel: Use deployment history to rollback
3. Database: Convex maintains data through deployments
