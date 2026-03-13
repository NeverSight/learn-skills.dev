---
name: surge-deploy
description: "This skill should be used when the user asks to deploy to surge, publish to surge.sh, or says 'static deploy', 'deploy static', 'deploy to surge', '/static-deploy'. Deploys any static build output - React, Vite, Vue, Next.js static export, Astro, SvelteKit, Hugo, plain HTML, or any framework that produces a build folder. This is specifically for surge.sh deployments, not Vercel or Netlify."
version: 1.1.0
disable-model-invocation: true
---

# Surge Deploy

Deploy any website's build output to the web in seconds using [surge.sh](https://surge.sh). Works with React, Vite, Vue, Next.js (static export), Astro, SvelteKit, Hugo, 11ty, plain HTML - anything that produces a folder of static files after build.

> **Scope**: Surge serves static files. If the project needs server-side rendering, serverless functions, or API routes at runtime, use Vercel/Netlify instead.

## Domain Memory

Surge deploy tracks the domain for each project so re-deploys always go to the same URL.

### How it works

After a successful first deploy, save the domain in a `.surge-domain` file at the project root:

```bash
echo "my-project.surge.sh" > .surge-domain
```

On every subsequent deploy, **always check for this file first**:

```bash
cat .surge-domain 2>/dev/null
```

- If `.surge-domain` exists, use that domain (no need to ask the user)
- If it does not exist, generate or ask for a domain, deploy, then create the file
- Add `.surge-domain` to `.gitignore` if a `.gitignore` exists, to keep it local:

```bash
grep -qxF '.surge-domain' .gitignore 2>/dev/null || echo '.surge-domain' >> .gitignore
```

### Overriding the saved domain

If the user explicitly provides a different domain, use that instead and update `.surge-domain` with the new value.

## Quick Reference

| Action | Command |
|---|---|
| Deploy | `surge ./path name.surge.sh` |
| List projects | `surge list` |
| Tear down | `surge teardown name.surge.sh` |
| Check auth | `surge whoami` |
| View files | `surge files name.surge.sh` |
| Bust cache | `surge bust name.surge.sh` |
| Rollback | `surge rollback name.surge.sh` |

## Pre-Deploy Checklist

Run these checks **in order** before every deployment:

### 1. Check if surge is installed

```bash
which surge
```

If not found, install it:

```bash
npm install -g surge
```

If `npm` is not available, try `npx surge` as a fallback (works without global install).

### 2. Check authentication

```bash
surge whoami
```

**If not authenticated**, do NOT attempt to run `surge login` programmatically - it is interactive and requires the user to type their email and password.

Instead, inform the user:

> Surge requires a one-time login. Run this in your terminal:
> ```
> surge login
> ```
> This takes 30 seconds - enter your email and password (or create a free account). Once done, authentication persists forever until you explicitly log out.

Then **stop and wait** for the user to confirm they've logged in before proceeding.

**For CI/CD or token-based auth**, check for environment variables:
- `SURGE_LOGIN` - email address
- `SURGE_TOKEN` - authentication token (get one via `surge token`)

### 3. Identify the deploy folder

Determine the correct folder to deploy. Common patterns:

| Framework | Build command | Output folder |
|---|---|---|
| Plain HTML/CSS/JS | None needed | Project root or `./` |
| React (CRA) | `npm run build` | `./build` |
| Vite | `npm run build` | `./dist` |
| Next.js (static) | `next build && next export` | `./out` |
| Astro | `npm run build` | `./dist` |
| SvelteKit (static) | `npm run build` | `./build` |
| Hugo | `hugo` | `./public` |
| 11ty | `npx eleventy` | `./docs` or `./_site` |

If the project has a `package.json` with a build script, run the build first:

```bash
npm run build
```

If the folder contains only HTML/CSS/JS files with no build step, deploy the folder directly.

### 4. Verify the folder has an index.html

```bash
ls <deploy-folder>/index.html
```

If missing, check for common issues:
- Wrong folder selected (try `./build`, `./dist`, `./out`, `./public`)
- Build step was skipped
- SPA without an index.html at root

### 5. Handle SPA routing (Single Page Apps)

For SPAs using client-side routing (React Router, Vue Router, etc.), create a `200.html` that is a copy of `index.html`:

```bash
cp <deploy-folder>/index.html <deploy-folder>/200.html
```

This tells surge to serve `index.html` for all routes, preventing 404s on direct URL access or page refresh.

## Deploy

### Resolve the domain

Follow this priority order:

1. **User explicitly provided a domain** → use it
2. **`.surge-domain` file exists in project root** → read and use it (this is a re-deploy)
3. **Neither** → generate a new domain:
   - Use the project folder name or `package.json` name field
   - Sanitize: lowercase, replace spaces/underscores with hyphens, remove special characters
   - Append `.surge.sh`
   - Example: `my-cool-project.surge.sh`
   - If the name is very generic (e.g., `app`, `project`), add a short random suffix:
     ```bash
     echo "my-project-$(head -c 4 /dev/urandom | xxd -p).surge.sh"
     ```

### Run the deploy

```bash
surge <deploy-folder> <domain>.surge.sh
```

### Save the domain (critical)

After a successful deploy, always persist the domain:

```bash
echo "<domain>.surge.sh" > .surge-domain
grep -qxF '.surge-domain' .gitignore 2>/dev/null || echo '.surge-domain' >> .gitignore
```

This ensures the next `/surge` re-deploys to the same URL automatically.

### Verify deployment

After surge completes, confirm the URL is live:

```bash
curl -s -o /dev/null -w "%{http_code}" https://<domain>.surge.sh
```

A `200` status confirms success. Present the live URL to the user prominently:

> Your site is live at: **https://domain.surge.sh**

## Post-Deploy Operations

### List all deployed projects

```bash
surge list
```

### Tear down a deployment

```bash
surge teardown <domain-name>.surge.sh
```

Always confirm with the user before tearing down.

### Update an existing deployment

Re-deploy to the same domain to update:

```bash
surge <deploy-folder> <existing-domain>.surge.sh
```

This overwrites the previous version instantly.

### Rollback to previous version

```bash
surge rollback <domain-name>.surge.sh
```

### Bust CDN cache

If changes aren't showing after re-deploy:

```bash
surge bust <domain-name>.surge.sh
```

## Custom Domains

Surge supports custom domains even on the free plan:

1. Deploy to the custom domain: `surge ./dist mydomain.com`
2. Add a CNAME record pointing to `na-west1.surge.sh` at the DNS provider
3. Wait for DNS propagation (can take up to 48 hours, usually minutes)

Inform the user of the DNS step - the agent cannot configure DNS records.

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| `Not authorized` | Not logged in | Run `surge login` |
| `Domain already taken` | Another user owns that subdomain | Choose a different name |
| `No index.html` | Missing entry point | Check deploy folder path |
| `ENOENT` | Folder doesn't exist | Verify the path |
| `EACCES` | Permission denied | Check folder permissions |

## Additional Resources

### Reference Files

- **`references/custom-domains.md`** - Detailed custom domain and SSL setup guide
- **`references/ci-cd.md`** - CI/CD integration patterns (GitHub Actions, GitLab CI, etc.)

### Example Files

- **`examples/deploy-react.sh`** - Deploy a React/Vite app
- **`examples/deploy-static.sh`** - Deploy plain HTML/CSS/JS
- **`examples/github-action.yml`** - GitHub Actions workflow for auto-deploy

### Scripts

- **`scripts/preflight.sh`** - Run all pre-deploy checks automatically
