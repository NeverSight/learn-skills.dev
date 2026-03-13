---
name: marketplace-scaffold
description: Scaffolds a new Sitecore Marketplace app using the official SDK. Use when the user wants to create a new marketplace app, start a new Sitecore project, or initialize a marketplace integration.
argument-hint: "[app-name]"
---

# Scaffold a New Sitecore Marketplace App

You are helping the user scaffold a new Sitecore Marketplace app using the official Sitecore Marketplace SDK (v0.4).

## Step 1: Gather Requirements

Ask the user the following questions (skip any they've already answered):

1. **App name** — What should the app be called? (default: from $ARGUMENTS if provided)
2. **Architecture** — Client-side only or full-stack?
   - **Client-side**: UI runs entirely in the iframe, communicates via SDK client. Simpler, no server needed.
   - **Full-stack**: Includes Next.js API routes/server actions for server-side SDK access. Required for Auth0, server-side mutations, or proxying external APIs.
3. **Authentication** — Built-in (default) or Auth0?
   - **Built-in**: Zero-config, SDK handles auth automatically. Sufficient for most apps.
   - **Auth0**: Required for server-side API access, external service integration, or custom auth flows. Requires Auth0 tenant setup.
4. **Optional packages** — Which additional SDK packages?
   - **XM Cloud (`xmc`)**: Access Sites, Pages, Authoring, Content Transfer, Search, and Agent APIs
   - **AI Skills (`ai`)**: Access Brand Review API for AI-powered content analysis

## Step 2: Run the Scaffold Command

Based on answers, construct and run the appropriate command:

```bash
# Client-side only (built-in auth)
npx shadcn@latest add https://marketplace-sdk.sitecorecloud.io/r/app-client.json

# Client-side + XMC
npx shadcn@latest add https://marketplace-sdk.sitecorecloud.io/r/app-client.json https://marketplace-sdk.sitecorecloud.io/r/xmc.json

# Client-side + AI
npx shadcn@latest add https://marketplace-sdk.sitecorecloud.io/r/app-client.json https://marketplace-sdk.sitecorecloud.io/r/ai.json

# Client-side + XMC + AI
npx shadcn@latest add https://marketplace-sdk.sitecorecloud.io/r/app-client.json https://marketplace-sdk.sitecorecloud.io/r/xmc.json https://marketplace-sdk.sitecorecloud.io/r/ai.json

# Full-stack (Auth0) — adds server-side SDK support
npx shadcn@latest add https://marketplace-sdk.sitecorecloud.io/r/app-auth0.json

# Full-stack + XMC
npx shadcn@latest add https://marketplace-sdk.sitecorecloud.io/r/app-auth0.json https://marketplace-sdk.sitecorecloud.io/r/xmc.json

# Full-stack + AI
npx shadcn@latest add https://marketplace-sdk.sitecorecloud.io/r/app-auth0.json https://marketplace-sdk.sitecorecloud.io/r/ai.json

# Full-stack + XMC + AI
npx shadcn@latest add https://marketplace-sdk.sitecorecloud.io/r/app-auth0.json https://marketplace-sdk.sitecorecloud.io/r/xmc.json https://marketplace-sdk.sitecorecloud.io/r/ai.json
```

**Important**: If the user doesn't have a Next.js project yet, scaffold one first:
```bash
npx create-next-app@latest <app-name> --typescript --tailwind --eslint --app --src-dir
cd <app-name>
```

## Step 3: Post-Scaffold Setup

After scaffolding completes:

1. **Create `.env.local`** — See [env-template.md](references/env-template.md) for the template. Fill in based on architecture choice.

2. **Configure CSP headers** — Add iframe embedding headers to `next.config.ts`:
```typescript
const nextConfig: NextConfig = {
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          {
            key: "Content-Security-Policy",
            value: "frame-ancestors 'self' https://*.sitecorecloud.io",
          },
        ],
      },
    ];
  },
};
```

3. **Install Blok theme** (if not already present):
```bash
npx shadcn@latest add https://marketplace-sdk.sitecorecloud.io/r/blok-theme.json
```

4. **Verify setup** — Run the dev server and confirm no errors:
```bash
npm run dev
```

## Step 4: Explain Next Steps

After successful scaffold, suggest:
- Use `/marketplace-add-extension` to add extension point routes (custom fields, dashboard widgets, etc.)
- Use `/marketplace-sdk-reference` to look up SDK APIs
- Use `/marketplace-build-component` to build UI with the Blok design system
- Use `/marketplace-deploy` when ready to deploy

## Reference Files
- [Architecture Guide](references/architecture-guide.md) — Decision matrix for client-side vs full-stack
- [Environment Template](references/env-template.md) — .env.local templates per architecture
