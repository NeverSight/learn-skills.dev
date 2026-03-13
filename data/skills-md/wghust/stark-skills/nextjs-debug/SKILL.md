---
name: nextjs-debug
description: Diagnose and fix Next.js project startup, compilation, and runtime errors by analyzing logs and project source code. Use when the user reports a Next.js startup error, compilation failure, hydration mismatch, module not found, Server/Client boundary violation, environment variable issue, or port conflict. Also triggers on "next dev fails", "next build error", "Turbopack error", "use client missing", "module not found", "Cannot find module", "hydration failed". 诊断并修复 Next.js 项目启动、编译和运行时错误。当用户粘贴启动日志、描述 Next.js 报错、询问"启动失败"、"编译报错"、"模块找不到"、"Server Component 报错"、"hydration 错误"、"环境变量不生效"时使用。
---

# Next.js Debug

> **Language**: Respond in the same language as the user (中文提问则中文回答).

---

## Execution Flow

Run all steps in order. Steps marked **[if project detected]** are skipped when no Next.js project is found.

### Step 0 · Receive Input

Accept one of:
- **Log**: raw terminal output pasted by user
- **Description**: natural-language problem description
- **Both**: prioritize log for classification; use description to disambiguate

Output one line before starting:
```
Diagnosing Next.js issue — analyzing [log / description / both]...
```

---

### Step 1 · Gather Context (run in parallel)

#### 1A · Version Stack [if project detected]

Read `package.json` and extract:
```
VersionStack = { next, react, reactDom, typescript, nodeEngine }
```
Also run `node -v` or read `.nvmrc` / `.node-version` for the active Node.js version.

**Compatibility checks** (flag as `VERSION_COMPAT` warning if triggered):
| Condition | Warning |
|---|---|
| `next` ≥ 15 and Node.js < 18.18 | Node.js too old |
| `next` ≥ 14 and Node.js < 18.17 | Node.js too old |
| `next` ≥ 15 and `react` < 19 | React/Next.js version mismatch |
| `next` ≤ 14 and `react` ≥ 19 | React/Next.js version mismatch |

**Deprecated API scan** (run with `rg`, conditional on Next.js version):
- `next` ≥ 13: grep `app/` for `getServerSideProps|getStaticProps` → flag as Pages Router API in App Router
- `next` ≥ 13: grep source for `<Image layout=|<Image objectFit=` → flag as removed `next/image` props
- `next` ≥ 15: check `next.config.*` for `webpack:` callback → note Turbopack doesn't run it

#### 1B · Dependency Audit [if project detected]

1. **Package manager**: check for `pnpm-lock.yaml` → pnpm; `yarn.lock` → yarn; `package-lock.json` → npm
2. **node_modules check**: if `node_modules/` is absent → output install command and **stop** (no further diagnosis needed)
3. **Duplicate React**: scan lockfile for multiple resolved `react` versions → list them and note `overrides`/`resolutions` fix
4. **.next cache**: if user description contains "worked yesterday" / "no code changes" → prepend `rm -rf .next && <pm> run dev` as first fix step

#### 1C · Git Context [if `.git` directory exists]

1. `git log --oneline -10` → record as `RecentCommits`
2. `git status --porcelain` → if any modified/untracked file overlaps with affected files → **flag as top suspect**, run `git diff -- <file>`
3. `git log --oneline -3 -- package.json` → if commits found → run `git diff HEAD~N HEAD -- package.json` and correlate with error class

---

### Step 2 · Project Detection

Check for `next.config.js`, `next.config.ts`, `next.config.mjs` at workspace root, or `"next"` in `package.json` dependencies.

- **Monorepo**: if not found at root, search one level deeper (`apps/*/`, `packages/*/`)
- **Detected** → set `PROJECT_ROOT`, activate code-location steps
- **Not detected** → note "No Next.js project detected — code-level location unavailable", proceed with log-only diagnosis

---

### Step 3 · Classify Error

Parse log / description and assign each error to one class:

| Class | Recognition Keywords |
|---|---|
| `COMPILE_ERROR` | `SyntaxError`, `Type error`, `Failed to compile`, `TS\d+:` |
| `MODULE_ERROR` | `Module not found`, `Cannot find module`, `Cannot resolve` |
| `BOUNDARY_ERROR` | `You're importing a component that needs`, `Event handlers cannot be passed to Client Component`, `Hooks can only be called inside of the body`, `async/await is not yet supported in Client Components` |
| `ENV_ERROR` | `Missing required environment variable`, `process.env.* is undefined`, `NEXT_PUBLIC_` in error |
| `CONFIG_ERROR` | `Invalid next.config`, `Unrecognized key(s) in object`, webpack/turbopack plugin error from config file |
| `RUNTIME_ERROR` | `Hydration failed`, `Text content did not match`, `EADDRINUSE`, uncaught exception in stack trace |

If multiple classes detected → list all, order by severity (blocking first).

---

### Step 4 · Extract Identifiers & Search Code [if project detected]

Extract from log before searching:

| Type | Pattern Example | Search Action |
|---|---|---|
| `FileRef` | `./src/app/page.tsx:34:12` or `app/layout.tsx(18,5)` | Read file at line, extract `[line-5, line+5]` snippet |
| `SymbolName` | `'UserCard'`, `Cannot find name 'fetchData'` | `rg -n "export.*(function\|const\|class\|default) SymbolName" app/ src/ lib/ components/` |
| `ModulePath` | `@/utils/api`, `./hooks/useAuth` | Glob `**/useAuth.{tsx,ts,jsx,js}` + `rg "from.*useAuth"` for all import sites |
| `StackFrame` | `at fn (filepath:line:col)` | Filter out `node_modules` frames, Read each project-owned file at indicated line |

**Code snippet format** (use `▶` for error line):
```
`src/app/dashboard/page.tsx` line 34
  33 | export default function Dashboard() {
▶ 34 |   const data = await fetchUserData()
  35 |   return <div>{data.name}</div>
```

**File too large** (>500 lines): read only `[line-10, line+20]`, note range in header.

**BOUNDARY_ERROR without file path**: glob `app/**/*.{tsx,jsx}`, check each file for client-only APIs (`useState`, `useEffect`, `onClick`, `window.`, `document.`) without `"use client"` on line 1.

---

### Step 5 · Deep Trace [if project detected]

#### MODULE_ERROR — Import Chain Tracing

1. Run `rg -n "from.*<missingPath>"` across project source to find all importers
2. For each importer, check if it is itself imported: `rg -n "from.*<importerFile>"` (max 2 levels up)
3. **tsconfig alias resolution**: read `tsconfig.json` → `compilerOptions.paths`, resolve `@/xxx` to real path, re-run search

#### RUNTIME_ERROR — Stack Trace Mapping

1. Parse each non-`node_modules` stack frame → `{file, line}`
2. If frame path is `.next/server/...` → map to source file by matching page segment name
3. Read each source file at `[line-5, line+5]`, include snippets innermost-first

#### COMPILE_ERROR — Type Error Scope

If `Type error` with `TS2307` (cannot find module) → treat as `MODULE_ERROR` and also run import chain tracing.

---

### Step 6 · Generate Diagnostic Report

Output the report using this template. Omit sections that have no findings.

```markdown
## Version Stack
- Next.js: X.Y.Z | React: X.Y.Z | Node.js: X.Y.Z | TypeScript: X.Y.Z
- [VERSION_COMPAT warnings if any]

## Likely Regression
[git-context findings: uncommitted changes / recent commits / package.json diff]

---

## Error 1: <CLASS> · <severity: blocking | warning>

### Root Cause
One sentence describing the root cause.

### Affected Files
- `path/to/file.tsx` line N
    N-1 | ...context...
  ▶ N   | ...error line...
    N+1 | ...context...

### Fix Steps
1. Step one (include code diff or exact command)
2. Step two

### Verify Fix
Run: `<command>`
Expected: `<expected output>`

### References
- [Title](https://nextjs.org/docs/...)
```

Repeat `## Error N` block for each error found, ordered blocking → warning.

If no fix can be determined → replace Fix Steps with:
```markdown
### Next Steps
- Additional info needed: [full log / Next.js version / Node.js version]
- Search: https://github.com/vercel/next.js/issues?q=<error-keywords>
- Community: https://github.com/vercel/next.js/discussions
```

---

## Examples

### Example A — Module not found (with project context)

**Input log:**
```
Module not found: Can't resolve './components/UserCard'
./src/app/dashboard/page.tsx
```

**Actions:**
1. Class: `MODULE_ERROR`
2. FileRef: `src/app/dashboard/page.tsx` — read import line
3. Glob: `**/UserCard.{tsx,ts,jsx,js}` — not found
4. tsconfig paths: check for alias → none

**Report excerpt:**
```markdown
## Error 1: MODULE_ERROR · blocking

### Root Cause
`UserCard` component file does not exist at the imported path.

### Affected Files
- `src/app/dashboard/page.tsx` line 3
  2 | import { useState } from 'react'
▶ 3 | import UserCard from './components/UserCard'

### Fix Steps
1. Create `src/app/dashboard/components/UserCard.tsx` or correct the import path
2. Check for casing mismatch (e.g., `userCard.tsx` vs `UserCard.tsx`)

### Verify Fix
Run: `npm run build`
Expected: `✓ Compiled successfully`

### References
- [Resolving Modules](https://nextjs.org/docs/app/api-reference/config/typescript)
```

---

### Example B — Missing "use client"

**Input log:**
```
You're importing a component that needs useState. It only works in a Client Component but none of its parents are marked with "use client".
```

**Actions:**
1. Class: `BOUNDARY_ERROR`
2. No file path → glob `app/**/*.{tsx,jsx}`, grep for `useState` without `"use client"` on line 1
3. Find offending file

**Fix step:** Add `"use client";` as line 1 of the offending file.

**Verify:** Run `next dev` → no `You're importing a component...` error in terminal.

---

### Example C — ENV_ERROR (NEXT_PUBLIC_ prefix missing)

**Input log:**
```
process.env.API_URL is undefined
```

**Actions:**
1. Class: `ENV_ERROR`
2. Grep source for `process.env.API_URL` → find usage in a client component
3. Check `.env.local` → variable exists as `API_URL` without `NEXT_PUBLIC_`

**Fix step:** Rename `.env.local` entry to `NEXT_PUBLIC_API_URL`, update all references.

**Verify:** Run `next build` → no `undefined` reference.

---

## Additional Resources

- For error patterns, version matrix, and code search templates → see [reference.md](reference.md)
