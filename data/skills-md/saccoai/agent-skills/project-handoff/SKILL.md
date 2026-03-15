---
name: project-handoff
description: Generate complete client handoff documentation — deployment guide, environment setup, CMS instructions, maintenance checklist, architecture overview, and operational runbook. Use when delivering a finished project to a client or their team.
---

This skill generates all documentation needed to hand off a completed project to a client or their internal team. It reads the codebase, environment config, and deployment setup to produce a comprehensive handoff package.

The user provides: the project directory and optionally the client's technical level (non-technical, developer, DevOps).

## Handoff Package Contents

### 1. Project Overview (`handoff/README.md`)

```markdown
# {Project Name} — Handoff Documentation

## Quick Start
git clone {repo-url}
{package-manager} install
cp .env.example .env.local  # fill in values
{package-manager} dev        # runs on localhost:3000

## Architecture
- Framework: {Next.js 16 / etc.}
- Styling: {Tailwind CSS v4 / etc.}
- Deployment: {Vercel / etc.}
- Domain: {domain.com}

## Repository
- URL: {repo-url}
- Branch strategy: main (production), develop (staging)
- CI/CD: {auto-deploy on push to main via Vercel}
```

### 2. Environment Variables (`handoff/environment.md`)

Auto-generated from `.env.example` and codebase analysis:

```markdown
# Environment Variables

## Required
| Variable | Description | Where to get it | Example |
|----------|------------|-----------------|---------|
| SMTP_HOST | Email server hostname | Your email provider | smtp.gmail.com |
| SMTP_PORT | Email server port | Your email provider | 587 |
| SMTP_USER | Email account username | Your email provider | user@domain.com |
| SMTP_PASS | Email account password | Your email provider | ••••••••••• |

## Optional
| Variable | Description | Default |
|----------|------------|---------|
| NEXT_PUBLIC_GA_ID | Google Analytics ID | (none — analytics disabled) |

## Setting Variables
### Vercel
1. Go to vercel.com → Project → Settings → Environment Variables
2. Add each variable for Production, Preview, and Development
3. Redeploy after adding variables

### .env.local (local development)
Copy .env.example to .env.local and fill in values.
Never commit .env.local to git.
```

### 3. Deployment Guide (`handoff/deployment.md`)

```markdown
# Deployment

## Production (Vercel)
- Auto-deploys when you push to `main` branch
- URL: {production-url}
- Dashboard: vercel.com/team/{team}/project/{project}

## How to Deploy
1. Make changes on a feature branch
2. Create a Pull Request to `main`
3. Vercel creates a preview deployment automatically
4. Review the preview URL
5. Merge the PR → auto-deploys to production

## Manual Deploy
npx vercel --prod

## Rollback
1. Go to Vercel Dashboard → Deployments
2. Find the last working deployment
3. Click ••• → Promote to Production

## Custom Domain
- Domain: {domain.com}
- DNS: {provider}
- Records configured: {A record / CNAME}
- SSL: Automatic via Vercel
```

### 4. Content Management (`handoff/content.md`)

How to update content without a developer:

```markdown
# Updating Content

## Text Content
Content is stored in: src/data/*.ts

### To update text:
1. Open the relevant file in src/data/
2. Find the text you want to change
3. Edit the text between the quotes
4. Commit and push → auto-deploys

### File locations:
| Content | File |
|---------|------|
| Book list | src/data/books.ts |
| Articles | src/data/articles.ts |
| Navigation | src/data/navigation.ts |
| {etc.} | {etc.} |

## Images
- Location: public/images/
- Formats: Use .webp or .jpg (not .png for photos)
- Sizes: Keep under 500KB per image
- After adding: reference in the relevant data file

## Adding a New Page
1. Create src/app/{page-name}/page.tsx
2. Add navigation link in src/data/navigation.ts
3. Update sitemap in src/app/sitemap.ts

## Adding a New Article/Publication
1. Open src/data/{articles|books}.ts
2. Add a new entry following the existing pattern
3. Add any images to public/images/
4. Commit and push
```

### 5. Architecture Overview (`handoff/architecture.md`)

Auto-generated from codebase analysis:

```markdown
# Architecture

## Directory Structure
src/
├── app/                    # Pages (file-based routing)
│   ├── page.tsx           # Homepage (/)
│   ├── about/page.tsx     # About page (/about)
│   ├── api/               # API routes
│   │   └── contact/route.ts  # Contact form endpoint
│   └── layout.tsx         # Root layout (header, footer)
├── components/
│   ├── layout/            # Header, footer, nav
│   ├── sections/          # Reusable page sections
│   └── ui/                # shadcn/ui components
├── data/                  # Content data files
├── lib/                   # Utility functions
└── styles/                # Global CSS

## Key Files
| File | Purpose |
|------|---------|
| src/app/layout.tsx | Root layout — wraps every page |
| src/app/globals.css | Global styles, CSS variables, fonts |
| next.config.ts | Redirects, image domains, config |
| tailwind.config.ts | Theme customization |

## Data Flow
1. Content lives in src/data/*.ts as typed TypeScript objects
2. Pages import data and render it
3. Contact form: client → /api/contact → Nodemailer → SMTP
4. No database — all content is in code

## Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| next | {version} | React framework |
| tailwindcss | {version} | Styling |
| framer-motion | {version} | Animations |
| nodemailer | {version} | Email sending |
| {etc.} | {etc.} | {etc.} |
```

### 6. Maintenance Checklist (`handoff/maintenance.md`)

```markdown
# Maintenance

## Regular Tasks
| Task | Frequency | How |
|------|-----------|-----|
| Update dependencies | Monthly | `npm outdated` then `npm update` |
| Check for security vulns | Monthly | `npm audit` |
| Review Lighthouse scores | Quarterly | Run audit on production |
| Renew SSL certificate | Automatic | Managed by Vercel |
| Check error logs | Weekly | Vercel Dashboard → Logs |
| Backup content | Before major changes | `git tag backup-{date}` |

## Updating Dependencies
npm outdated          # see what's outdated
npm update            # update minor/patch versions
npx npm-check-updates # check for major version updates

## If Something Breaks
1. Check Vercel deployment logs: Dashboard → Deployments → latest
2. Check browser console for errors
3. Rollback to last working deployment (see deployment.md)
4. Contact: {developer contact info}

## Security
- Never commit .env files (they're in .gitignore)
- Rotate SMTP credentials periodically
- Keep dependencies updated (security patches)
- Review Vercel access permissions quarterly
```

### 7. Troubleshooting (`handoff/troubleshooting.md`)

```markdown
# Troubleshooting

## Common Issues

### Build fails after content change
- Check for unclosed quotes or brackets in data files
- TypeScript will show the exact line with the error
- Fix: look at the Vercel build logs for the error message

### Contact form not sending emails
- Verify SMTP environment variables in Vercel
- Check Vercel Function logs for errors
- Test with a simple email first
- Common: SMTP password expired or 2FA blocking

### Images not showing
- Check file exists in public/images/
- Check filename matches exactly (case-sensitive)
- Verify image path in the data file starts with /images/

### Site looks different on mobile
- Clear browser cache (Cmd+Shift+R)
- Check if Vercel preview deployment is stale
- Verify changes are on the `main` branch

### Slow page load
- Run Lighthouse audit
- Check image sizes (should be < 500KB each)
- Look for unoptimized images (use WebP format)
```

## Generation Process

The skill reads the actual codebase to generate accurate documentation:

1. **Scan `package.json`** — detect framework, dependencies, scripts
2. **Scan `.env.example`** — document all environment variables
3. **Scan `src/` directory** — map file structure and data flow
4. **Scan deployment config** — Vercel, Netlify, Docker, etc.
5. **Scan `next.config.*`** — redirects, image domains, etc.
6. **Read git remote** — repository URL and branch info
7. **Generate all handoff documents** with accurate, project-specific content

## Output

All files are saved to `handoff/` directory:

```
handoff/
├── README.md              # Quick start and overview
├── environment.md         # Environment variables guide
├── deployment.md          # How to deploy and rollback
├── content.md             # How to update content
├── architecture.md        # Technical architecture
├── maintenance.md         # Ongoing maintenance checklist
└── troubleshooting.md     # Common issues and fixes
```

## Customization by Audience

| Audience | Focus | Tone |
|----------|-------|------|
| **Non-technical client** | Content updates, what to expect, who to contact | Simple, no jargon |
| **Developer** | Architecture, code patterns, debugging | Technical, concise |
| **DevOps** | Deployment, infra, monitoring, env vars | Operational, specific |

## Agent Team Integration

In the `website-refactor` workflow, this skill runs in Phase 6 after deployment. The Lead generates handoff docs as the final deliverable.
