---
name: testing
description: Run tests, check builds, and validate the application works correctly. Use after making changes.
allowed-tools: Bash, Read, Grep
user-invocable: true
---

# Testing Skill

Run these checks to validate changes in the Vibe Stack project:

## Build Verification

```bash
# Type check and build
pnpm build
```

## Convex Validation

```bash
# Sync schema and check for errors
npx convex dev --once
```

## Manual Testing Checklist

### Authentication Flow

- [ ] Sign up with new email
- [ ] Log in with existing account
- [ ] Log out clears session
- [ ] Protected routes redirect to login
- [ ] Auth routes redirect authenticated users to dashboard

### Data Operations

- [ ] CRUD operations work correctly
- [ ] Real-time updates reflect immediately
- [ ] Error states display user-friendly messages
- [ ] Loading states show while data fetches

### Stripe Integration

- [ ] Checkout redirects to Stripe
- [ ] Webhook processes subscription events
- [ ] Subscription status updates in database

## Common Issues

### Build Fails

1. Check for TypeScript errors: `pnpm build`
2. Verify Convex schema matches usage
3. Check for missing environment variables

### Auth Not Working

1. Verify `AUTH_SECRET` is set
2. Check Convex dashboard for errors
3. Clear browser cookies and retry

### Stripe Webhook Issues

1. Verify webhook secret matches
2. Check Stripe dashboard for failed events
3. Review webhook logs in Vercel/server
