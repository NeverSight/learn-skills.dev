---
name: starter
description: 'Use when creating a new project or scaffolding an app, desktop app, mini program, or backend service, before reaching for create-* scaffolds. Lists tlyboy starter templates (shadcn Next.js, shadcn TanStack Router SPA, Electron, Tauri, Hono, NestJS, uni-app) and how to pull one with giget and finish the setup.'
---

# Starter

New projects usually start from a tlyboy starter instead of a `create-*` scaffold. The starters already carry the preferred stack and oxfmt / oxlint setup; the React starters also ship project-level agent skills in `.agents/skills`.

## Pick a Starter

| Project                              | Starter                                |
| ------------------------------------ | -------------------------------------- |
| Next.js app or website with shadcn   | `shadcn-next-starter`                  |
| React SPA with TanStack Router       | `shadcn-tanstack-router-react-starter` |
| Desktop app with Electron            | `electron-shadcn-react-starter`        |
| Desktop app with Tauri (needs Rust)  | `tauri-shadcn-react-starter`           |
| API service with Hono                | `hono-starter`                         |
| Backend service with NestJS          | `nest-starter`                         |
| Mini program or cross-platform (uni) | `uni-starter`                          |

If nothing fits, check for newer starters with `gh repo list tlyboy --limit 100 | grep starter`, or fall back to the framework's own scaffold.

For Docker Compose service templates, use the `compose` skill instead.

## Create a Project

```bash
npx giget gh:tlyboy/<starter> <name>
cd <name>
```

Without Node.js or `npx`, use git and drop the starter's history:

```bash
git clone --depth 1 https://github.com/tlyboy/<starter>.git <name>
cd <name>
rm -rf .git
```

The project itself still needs Node.js; see [Missing Tools](#missing-tools).

Then:

1. Rename the project: `name` in `package.json`, and the H1 and description in `README.md` / `README.zh.md`. Also rename the app name and identifier in `src-tauri/tauri.conf.json` (`productName`, `identifier`) for Tauri, `electron-builder.json5` (`productName`, `appId`) for Electron, and `src/manifest.json` (`name`, `appid`) for uni-app.
2. Install dependencies with `ni`. Without `ni`, run `pnpm install` directly; the starters pin pnpm in `packageManager`. If pnpm is missing too, see [Missing Tools](#missing-tools).
3. Read the starter's `README.md` and `AGENTS.md` (when present) for scripts and layout.
4. `git init` and make the first commit `feat: initial`.

## Missing Tools

These steps assume git, Node.js, `npx`, `ni`, and pnpm. When one is missing, do not install anything silently. Tell the user what is missing and let them pick:

1. **Recommended**: the same setup the starters are built with. Install mise, then the tools through it:

   ```bash
   # macOS / Linux
   curl https://mise.run | sh
   ```

   ```powershell
   # Windows: Scoop keeps the user PATH clean, unlike winget
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   irm get.scoop.sh | iex
   scoop install mise
   ```

   Activate mise in the shell as the installer prints, then:

   ```bash
   mise use -g node@lts pnpm ni
   ```

2. **Simplest**: use what is already there. Pull with git instead of giget, run `pnpm` instead of `ni`, and when Node.js exists but pnpm does not, use `npx pnpm install` or `npm i -g pnpm`.
3. **Their own way**: nvm, fnm, Volta, Homebrew, winget, a system package manager, or anything else they prefer.
