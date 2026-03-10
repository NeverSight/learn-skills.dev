---
name: scaffold-nextjs-app
description: >
  Scaffold a new Next.js application with App Router, TypeScript,
  and modern defaults. Covers project creation, directory structure,
  routing setup, and initial configuration. Use when starting a new web
  application project, creating a React-based frontend with server-side
  rendering, building a full-stack application with API routes, or setting
  up a TypeScript web project from scratch.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: web-dev
  complexity: basic
  language: TypeScript
  tags: nextjs, react, typescript, app-router, scaffold
---

# Scaffold Next.js App

Create a new Next.js application with App Router, TypeScript, and production-ready defaults.

## When to Use

- Starting a new web application project
- Creating a React-based frontend with server-side rendering
- Building a full-stack application with API routes
- Setting up a TypeScript web project

## Inputs

- **Required**: Application name
- **Required**: Package manager preference (npm, yarn, pnpm)
- **Optional**: Whether to include Tailwind CSS (default: yes)
- **Optional**: Whether to include ESLint (default: yes)
- **Optional**: src/ directory structure (default: yes)

## Procedure

### Step 1: Create Project

```bash
npx create-next-app@latest my-app \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*"
```

Answer prompts or use flags to set all options non-interactively.

**Expected:** Project directory created with all dependencies installed.

**On failure:** Check Node.js version (`node --version`, must be >= 18.17). Ensure `npx` is available. If the command hangs on prompts, add the `--use-npm` flag (or `--use-pnpm`/`--use-yarn`) to skip the package manager prompt.

### Step 2: Verify Project Structure

```
my-app/
├── src/
│   ├── app/
│   │   ├── layout.tsx        # Root layout
│   │   ├── page.tsx          # Home page
│   │   ├── globals.css       # Global styles
│   │   └── favicon.ico
│   └── lib/                  # Shared utilities (create manually)
├── public/                   # Static assets
├── next.config.ts            # Next.js configuration
├── tailwind.config.ts        # Tailwind configuration
├── tsconfig.json             # TypeScript configuration
├── package.json
└── .eslintrc.json
```

**Expected:** All listed directories and files are present.

**On failure:** If `src/` directory is missing, the `--src-dir` flag was not passed. Re-run `create-next-app` with the flag, or move files manually into `src/app/`.

### Step 3: Configure Next.js

Edit `next.config.ts` for project needs:

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable React strict mode
  reactStrictMode: true,

  // Image optimization domains
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "example.com",
      },
    ],
  },
};

export default nextConfig;
```

**Expected:** `next.config.ts` saved without TypeScript errors.

**On failure:** If the file uses `.js` extension instead of `.ts`, rename it. Ensure `NextConfig` type is imported from `"next"`.

### Step 4: Set Up Directory Conventions

Create common directories:

```bash
mkdir -p src/app/api
mkdir -p src/components
mkdir -p src/lib
mkdir -p src/types
```

**Expected:** All four directories created under `src/`.

**On failure:** If `src/` does not exist, create it first or adjust paths to match the project structure (non-src layout uses `app/` at the root).

### Step 5: Create Base Layout

Edit `src/app/layout.tsx`:

```tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "My Application",
  description: "Application description",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
```

**Expected:** Layout renders with the Inter font and wraps all pages.

**On failure:** If font fails to load, check network access. Replace `Inter` with a system font fallback as a temporary workaround.

### Step 6: Add Example API Route

Create `src/app/api/health/route.ts`:

```typescript
import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({ status: "ok", timestamp: new Date().toISOString() });
}
```

**Expected:** File created at `src/app/api/health/route.ts`.

**On failure:** Ensure the `api/health/` directory exists. The file must export named HTTP method handlers (`GET`, `POST`, etc.), not a default export.

### Step 7: Run Development Server

```bash
cd my-app
npm run dev
```

**Expected:** Application running at http://localhost:3000.

**On failure:** Check Node.js version (>= 18.17). Run `npm install` if dependencies are missing.

## Validation

- [ ] `npm run dev` starts without errors
- [ ] Home page loads at localhost:3000
- [ ] TypeScript compilation succeeds
- [ ] Tailwind CSS classes are applied
- [ ] API route responds at /api/health
- [ ] ESLint runs without errors (`npm run lint`)

## Common Pitfalls

- **Node.js version**: Next.js requires Node.js >= 18.17. Check with `node --version`.
- **Port conflicts**: Default port 3000 may be in use. Use `npm run dev -- -p 3001`.
- **Import alias confusion**: `@/*` maps to `src/*`. Don't confuse with node_modules imports.
- **Pages vs App Router**: Ensure you're using App Router (`src/app/`) not Pages Router (`src/pages/`).

## Related Skills

- `setup-tailwind-typescript` - detailed Tailwind and TypeScript configuration
- `deploy-to-vercel` - deploy the scaffolded app
- `configure-git-repository` - version control setup
