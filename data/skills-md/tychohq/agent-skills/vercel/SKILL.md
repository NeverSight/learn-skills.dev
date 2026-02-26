---
name: vercel
slug: vercel-deployment
version: 1.0.0
description: Deploy and manage Vercel projects, including linking repositories, env vars, and domains.
---

# Vercel — Deploy and Manage Projects

## Set Up a New Project

```bash
cd <project-root>   # must be the directory with .git
npx vercel link      # link to Vercel project
npx vercel git connect  # connect GitHub repo for auto-deploys
```

Run `vercel git connect` from the repo root (where `.git` lives), not a subdirectory.

## Set Environment Variables

**NEVER use `echo`** — it adds a trailing `\n`:
```bash
printf 'value' | npx vercel env add VAR_NAME production
```

## Check Domains

```bash
cd any-vercel-project && npx vercel domains ls
```

For the full domain list: see `domains.md` in this folder.
