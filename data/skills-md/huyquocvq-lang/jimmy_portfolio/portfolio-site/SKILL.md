---
name: portfolio-site
description: >-
  Work on the Jenny Tang React+Vite portfolio: homepage data, routes, per-project
  pages, styles, and mandatory doc sync. Use when editing this repo, adding a project,
  changing Hero/Nav/projects, or when the user mentions AGENTS.md, USAGE_GUIDE, or
  portfolio documentation. Invoke with /portfolio-site.
---

# Portfolio site workflow

## Before coding

1. Read `AGENTS.md`
2. Read `docs/USAGE_GUIDE.md` (doc sync mapping table)
3. Confirm: **React 18 + Vite 5 web SPA** - not React Native

## Mandatory: update docs

After **any** code or config change, update docs per `docs/USAGE_GUIDE.md` §4.2.

List which doc files you updated before finishing.

## Content source (`docs/CONTENT_SOURCE.md`)

- Mapping reference only - not bundled in the app
- On content changes: update `CONTENT_SOURCE.md` and runtime files (`src/data/*`, `src/projects/*`)
- User instructions in chat override `CONTENT_SOURCE.md`

## Edit homepage copy

| Content | File |
|---------|------|
| Profile, contact | `src/data/profile.js` |
| Hero + impact numbers | `src/data/stats.js` |
| About | `src/data/about.js` |
| Skills | `src/data/skills.js`, `src/data/skillIcons.js` |
| Project cards | `src/data/projects.js` |

→ Update `docs/FEATURE_MAP.md` for affected features.

## Edit one project page

- JSX: `src/projects/<Name>Project.jsx`
- CSS: `src/styles/projects/<name>.css`
- Wrap with `ProjectShell` and matching `slug` prop
- **Do not** collapse into a shared generic template

→ Update `docs/FEATURE_MAP.md` for that project.

## Add a new project

1. `src/data/projects.js` - `{ slug, link: '/projects/<slug>', ... }`
2. `src/projects/NewProject.jsx` + `src/styles/projects/new-project.css`
3. `src/App.jsx` - `<Route path="/projects/<slug>" element={<NewProject />} />`
4. `public/images/projects/<slug>.jpg`
5. Update: `FEATURE_MAP.md`, `ARCHITECTURE_OVERVIEW.md`, `AI_AGENT_GUIDE.md`, `FULL_DOCUMENTATION.md`, `API_FLOW.md`, `AGENTS.md` if routes change
6. Verify prev/next pager on `ProjectShell`

## Invariants

```
projects.js slug === App.jsx path segment === ProjectShell slug prop
projects.js link === '/projects/' + slug
getAllProjects() order === prev/next pager order
```

## Commands

```bash
npm install && npm run dev
```

Node 18+.

## Avoid

- `motion.div` (no framer-motion in this repo)
- `href="#work"` on project pages → `href="/#work"` or `<Link to="/#work">`
- Long case study body only in `projects.js` (full copy lives in `src/projects/*.jsx`)

## Reference

- `docs/AI_AGENT_GUIDE.md`
- `docs/ARCHITECTURE_OVERVIEW.md`
