---
name: vercel-deployment
description: |
  Vercel deployment configuration, preview environments, and edge functions. Covers vercel.json and vercel.ts configuration, rewrites, redirects, headers, environment variables across production/preview/development, custom domains, DNS setup, edge and serverless functions, Vercel CLI, GitHub Actions CI/CD, and monorepo deployments.

  Use when deploying to Vercel, configuring builds, setting up preview branches, managing environment variables, configuring custom domains, or using edge/serverless functions. Use for vercel, deploy, preview, edge-function, serverless, vercel-json, environment-variables, domains, monorepo.
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: 'https://vercel.com/docs'
user-invocable: false
---

# Vercel Deployment

## Overview

Vercel is a cloud platform for deploying frontend frameworks and serverless functions with automatic CI/CD, preview deployments, and edge infrastructure. Projects are configured via `vercel.json` (or programmatic `vercel.ts`), the Vercel dashboard, or the Vercel CLI.

**When to use:** Static sites, SSR frameworks (Next.js, SvelteKit, Nuxt), serverless API routes, edge functions, preview environments per pull request, monorepo deployments.

**When NOT to use:** Long-running backend processes (use containers), WebSocket servers (use dedicated infrastructure), heavy compute workloads (use cloud VMs), applications requiring persistent file system access.

## Quick Reference

| Pattern              | Tool / API                           | Key Points                                         |
| -------------------- | ------------------------------------ | -------------------------------------------------- |
| Project config       | `vercel.json` or `vercel.ts`         | Root of project, controls builds/routing/functions |
| Rewrites             | `rewrites` array                     | Routes request to destination, URL unchanged       |
| Redirects            | `redirects` array                    | Changes URL, `permanent: true` for 301             |
| Headers              | `headers` array                      | Custom response headers per path pattern           |
| Clean URLs           | `cleanUrls: true`                    | Strips `.html` extensions                          |
| Trailing slash       | `trailingSlash: false`               | Consistent URL format                              |
| Environment vars     | Dashboard or `vercel env`            | Scoped to production, preview, development         |
| Custom domains       | Project Settings > Domains           | A record for apex, CNAME for subdomains            |
| Preview deploys      | Automatic per PR                     | Each push gets unique URL                          |
| Edge functions       | `export const runtime = 'edge'`      | V8 isolates, low latency, limited Node.js APIs     |
| Serverless functions | `api/` directory or framework routes | Node.js runtime, full API access                   |
| Deploy via CLI       | `vercel` or `vercel --prod`          | Preview by default, `--prod` for production        |
| Promote deploy       | `vercel promote <url>`               | Promote existing preview to production             |
| Monorepo             | Root directory setting per project   | One repo, multiple Vercel projects                 |
| GitHub integration   | Automatic on push                    | Zero-config CI/CD with preview per branch          |
| Programmatic config  | `vercel.ts` with `@vercel/config`    | Typed, dynamic configuration alternative           |
| Fluid compute        | Enabled by default for new projects  | Multi-request workers, 300s default duration       |
| Rolling releases     | Incremental rollout with monitoring  | Gradual traffic shift with auto-rollback triggers  |
| Firewall rules       | `vercel.json` WAF configuration      | Block threats via dashboard, API, or config file   |

## Common Mistakes

| Mistake                                                    | Correct Pattern                                                                            |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Using `.env.production` for preview-specific values        | Use Vercel environment variables scoped to preview environment                             |
| Expecting `VERCEL_URL` to include protocol                 | Prepend `https://` manually; use `VERCEL_PROJECT_PRODUCTION_URL` for stable production URL |
| Adding only apex domain without `www`                      | Add both `yourdomain.com` and `www.yourdomain.com` to avoid 404 on one                     |
| Using Node.js APIs in edge functions                       | Edge runtime uses V8 only; `fs`, `path`, `process` are unavailable                         |
| Exceeding 1024 static redirects                            | Use `bulkRedirects` property for large redirect sets (CSV/JSON/JSONL)                      |
| Creating QueryClient or fetching in edge without streaming | Use streaming responses for long operations in edge functions                              |
| Setting `maxDuration` above plan limit                     | Fluid compute default: 300s; Hobby: 60s, Pro: 300s, Enterprise: 900s max                   |
| Conflicting DNS records for custom domain                  | Remove duplicate A records; keep only the Vercel-pointing record                           |
| Not awaiting build in CI before deploy                     | Use `vercel build` then `vercel deploy --prebuilt` for reliable CI deploys                 |
| Ignoring monorepo root directory setting                   | Set root directory per project in Vercel dashboard for correct builds                      |

## Delegation

- **Infrastructure review**: Use `Task` agent to audit deployment configuration
- **Environment debugging**: Use `Explore` agent to trace environment variable issues
- **CI/CD pipeline review**: Use `code-reviewer` agent for GitHub Actions workflow review

## References

- [Configuration: vercel.json, builds, rewrites, redirects, headers](references/configuration.md)
- [Environment variables and custom domains](references/environment-and-domains.md)
- [Edge and serverless functions](references/edge-and-serverless.md)
- [CLI commands and CI/CD integration](references/cli-and-ci.md)
