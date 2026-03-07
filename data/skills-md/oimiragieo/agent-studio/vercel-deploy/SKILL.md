---
name: vercel-deploy
description: Zero-auth Vercel deployment workflow with automatic framework detection for 20+ frameworks. Use when deploying web applications to Vercel, creating preview deployments, or setting up deployment pipelines. Supports Next.js, Vite, Remix, SvelteKit, Astro, Nuxt, and more.
license: MIT
metadata:
  author: vercel-labs
  version: '1.0.0'
  source: vercel-labs/agent-skills
verified: true
lastVerifiedAt: 2026-02-22T00:00:00.000Z
version: 1.0.0
tools: []
---

# Vercel Deploy

Zero-auth deployment to Vercel with automatic framework detection. Deploy any web application with a single command and receive preview URLs, claim URLs, and deployment metadata.

## When to Apply

Use this skill when:

- Deploying a web application to Vercel for preview or production
- Setting up a deployment pipeline for a new project
- Creating preview deployments for pull request review
- Testing production builds in a live environment
- Demonstrating a prototype or proof of concept

## Supported Frameworks

Vercel auto-detects and configures builds for these frameworks:

| Framework        | Detection                   | Build Command           |
| ---------------- | --------------------------- | ----------------------- |
| Next.js          | `next.config.*`             | `next build`            |
| Vite             | `vite.config.*`             | `vite build`            |
| Remix            | `remix.config.*`            | `remix build`           |
| SvelteKit        | `svelte.config.*`           | `vite build`            |
| Astro            | `astro.config.*`            | `astro build`           |
| Nuxt             | `nuxt.config.*`             | `nuxt build`            |
| Gatsby           | `gatsby-config.*`           | `gatsby build`          |
| Angular          | `angular.json`              | `ng build`              |
| Vue CLI          | `vue.config.*`              | `vue-cli-service build` |
| Create React App | `react-scripts` in deps     | `react-scripts build`   |
| Ember            | `ember-cli-build.js`        | `ember build`           |
| Hugo             | `config.toml` / `hugo.toml` | `hugo`                  |
| Jekyll           | `_config.yml`               | `jekyll build`          |
| Eleventy         | `.eleventy.js`              | `eleventy`              |
| Docusaurus       | `docusaurus.config.*`       | `docusaurus build`      |
| Static HTML      | `index.html` at root        | None                    |

## Deployment Workflow

### Step 1: Prerequisites

Ensure the Vercel CLI is installed:

```bash
# Install globally
npm install -g vercel

# Or use npx (no install needed)
npx vercel
```

### Step 2: Project Setup (First Time Only)

For new projects not yet linked to Vercel:

```bash
# Interactive setup -- creates .vercel/project.json
vercel link

# Or create a new project
vercel --yes
```

### Step 3: Deploy

#### Preview Deployment (Default)

```bash
# Deploy to preview environment
vercel

# Output:
# Vercel CLI 34.x.x
# Linked to username/project-name
# Inspect: https://vercel.com/username/project-name/abcdef
# Preview: https://project-name-abc123.vercel.app
```

#### Production Deployment

```bash
# Deploy to production
vercel --prod

# Output includes production URL:
# Production: https://project-name.vercel.app
```

#### Zero-Auth Deployment (Agent Mode)

For automated deployments without authentication prompts:

```bash
# Using VERCEL_TOKEN environment variable
VERCEL_TOKEN=your-token vercel --yes --token=$VERCEL_TOKEN

# Or with npx for zero-install
VERCEL_TOKEN=your-token npx vercel --yes --token=$VERCEL_TOKEN
```

### Step 4: Deployment Output

Successful deployments return JSON-compatible metadata:

```json
{
  "url": "https://project-name-abc123.vercel.app",
  "inspectUrl": "https://vercel.com/team/project/deployment-id",
  "projectId": "prj_abc123",
  "deploymentId": "dpl_abc123",
  "readyState": "READY"
}
```

Use `--json` flag for machine-readable output:

```bash
vercel --json
```

### Step 5: Post-Deployment Verification

```bash
# Check deployment status
vercel inspect <deployment-url>

# View deployment logs
vercel logs <deployment-url>

# List recent deployments
vercel list
```

## Configuration Options

### Environment Variables

```bash
# Set environment variables for deployment
vercel env add VARIABLE_NAME production
vercel env add VARIABLE_NAME preview
vercel env add VARIABLE_NAME development

# Or pass inline
vercel -e KEY=value -e KEY2=value2
```

### Build Configuration

Override auto-detected settings in `vercel.json`:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

### Custom Domains

```bash
# Add a custom domain
vercel domains add example.com

# Assign domain to project
vercel alias <deployment-url> example.com
```

## Framework-Specific Patterns

### Next.js

```json
{
  "framework": "nextjs",
  "buildCommand": "next build",
  "outputDirectory": ".next"
}
```

Next.js deployments automatically enable:

- Edge Runtime for middleware
- ISR (Incremental Static Regeneration)
- Image Optimization via `next/image`
- Server Actions

### Vite / React SPA

```json
{
  "framework": "vite",
  "buildCommand": "vite build",
  "outputDirectory": "dist",
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

### SvelteKit

```json
{
  "framework": "sveltekit",
  "buildCommand": "vite build",
  "outputDirectory": ".svelte-kit/output"
}
```

SvelteKit uses the `@sveltejs/adapter-vercel` adapter for optimal deployment.

## Deployment Strategies

### Preview per Pull Request

Configure GitHub integration for automatic preview deployments:

1. Connect repository in Vercel dashboard
2. Every PR gets a unique preview URL
3. Comments added to PR with preview link
4. Preview is torn down when PR is closed

### Staged Rollouts

```bash
# Deploy to staging first
vercel --env ENVIRONMENT=staging

# Promote to production after validation
vercel promote <deployment-url>
```

### Rollback

```bash
# List recent deployments
vercel list

# Rollback to a previous deployment
vercel rollback <deployment-url>
```

## Troubleshooting

### Build Fails

1. Check build logs: `vercel logs <url>`
2. Verify `buildCommand` matches local build
3. Check environment variables are set for the target environment
4. Ensure Node.js version matches (use `engines` in package.json)

### 404 on Client-Side Routes

Add rewrites for SPA frameworks:

```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

### Large Bundle Warnings

1. Enable tree-shaking in bundler config
2. Use dynamic imports for heavy dependencies
3. Check Vercel's bundle analysis: `vercel inspect --logs`

### Timeout Issues

- Serverless functions: Default 10s timeout (configurable up to 300s on Pro)
- Edge functions: 25ms CPU time limit (wall-clock can be longer with I/O)
- Static generation: 45s default timeout

```json
{
  "functions": {
    "api/heavy-route.ts": {
      "maxDuration": 60
    }
  }
}
```

## Security Considerations

- Never commit `VERCEL_TOKEN` to version control
- Use environment variables for secrets (not hardcoded)
- Enable Vercel's DDoS protection for production
- Use `vercel env pull` to sync environment variables locally
- Review deployment protection settings for preview URLs

## References

- [Vercel CLI Documentation](https://vercel.com/docs/cli)
- [Vercel Deployment Documentation](https://vercel.com/docs/deployments)
- [Framework-Specific Guides](https://vercel.com/docs/frameworks)

## Iron Laws

1. **ALWAYS** test the build locally before deploying to ensure the deployment will succeed
2. **NEVER** deploy to production without first creating and validating a preview deployment
3. **ALWAYS** verify environment variables are configured in the Vercel project before deploying
4. **NEVER** store sensitive secrets in deployment commands or public URLs
5. **ALWAYS** check the deployment logs immediately after deployment to confirm the build succeeded

## Anti-Patterns

| Anti-Pattern                         | Why It Fails                                     | Correct Approach                                 |
| ------------------------------------ | ------------------------------------------------ | ------------------------------------------------ |
| Deploying without local build test   | Build fails in Vercel, wasted deployment attempt | Run `build` locally before `vercel deploy`       |
| Skipping preview before production   | Regressions reach users before detection         | Always validate preview URL first                |
| Hardcoded env vars in deploy command | Secrets exposed in shell history and logs        | Configure env vars in Vercel project settings    |
| Ignoring post-deploy build logs      | Silent failures go undetected                    | Always check logs after deployment               |
| No framework detection verification  | Wrong settings cause build failures              | Verify auto-detected framework in project config |

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`
