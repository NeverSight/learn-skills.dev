---
name: convex-dev-static-hosting
description: A Convex component that enables hosting static React/Vite apps using Convex HTTP actions and file storage. Use this skill whenever working with Static-Hosting or related Convex component functionality.
version: 0.2.1
---

> Agents: read this skill fully before writing code that uses Static-Hosting. Follow the installation and configuration steps exactly.

# Static-Hosting

## Instructions

Static-Hosting enables developers to serve React/Vite apps directly from Convex without external hosting providers. It uses Convex HTTP actions to serve files from Convex storage, with automatic SPA fallback for client-side routing, smart caching for hashed assets, and garbage collection of old deployments. The upload API uses internal functions for security, ensuring only authenticated CLI users can deploy files.

### Installation

```bash
npm install @convex-dev/static-hosting
```

Current npm version: `@convex-dev/static-hosting@0.2.1`

## Use cases

- **Deploy full-stack apps with single backend**: Host your React frontend and Convex backend functions in one deployment, eliminating the need for separate hosting services like Vercel or Netlify
- **Prototype and demo apps quickly**: Skip external hosting setup during development and share working demos directly from your Convex deployment URL
- **Build internal tools and admin dashboards**: Serve company-internal React apps from Convex with built-in authentication integration and no external dependencies
- **Create self-contained SaaS applications**: Package your entire application stack into Convex components that include both backend logic and frontend assets
- **Implement live deployment notifications**: Use the deployment query hooks to show users when new versions are available and prompt for page refreshes

## How it works

The component integrates into your Convex app configuration and HTTP router using `registerStaticRoutes()` to serve files from Convex storage. During deployment, the CLI uploads your built assets to Convex storage via internal functions like `generateUploadUrl()` and `recordAsset()`, which are only accessible through authenticated `npx convex run` commands for security.

The HTTP actions serve files with intelligent caching - hashed assets from bundlers like Vite get long-term cache headers while HTML files use ETags for freshness. The `spaFallback` option automatically serves `index.html` for unmatched routes, enabling client-side routing in single-page applications.

Deployment uses either a one-shot `deploy` command that builds your frontend with the correct production `VITE_CONVEX_URL`, deploys the Convex backend, then uploads static files, or separate `upload` commands for more control. The component automatically garbage collects old deployment files to prevent storage bloat.

## When NOT to use

- When a simpler built-in solution exists for your specific use case
- If you are not using Convex as your backend
- When the functionality provided by Static-Hosting is not needed

## Resources

- [npm package](https://www.npmjs.com/package/%40convex-dev%2Fstatic-hosting)
- [GitHub repository](https://github.com/get-convex/static-hosting)
- [Live demo](https://github.com/get-convex/static-hosting/tree/main/example)
- [Convex Components Directory](https://www.convex.dev/components/static-hosting)
- [Convex documentation](https://docs.convex.dev)