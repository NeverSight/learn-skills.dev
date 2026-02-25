---
name: migrate-to-nextjs
description: Autonomous site migration from any legacy stack to modern Next.js. Visual diffing, best practices enforcement, live progress on localhost.
user-invocable: true
---

# Site Migration Skill

**STOP. READ THIS ENTIRE DOCUMENT BEFORE DOING ANYTHING.**

This skill migrates legacy websites to modern Next.js. You MUST follow every step exactly. Skipping steps will result in failed migrations.

---

## PHASE 1: SETUP

Install all dependencies, ask the user questions, create the Next.js project, and configure MCP. Do not proceed to Phase 2 until everything is verified.

### 1.1 Install Skills

Run each command and verify it succeeds:

```bash
npx skills add https://github.com/vercel-labs/agent-skills --skill vercel-react-best-practices --yes
npx skills add https://github.com/vercel-labs/next-skills --skill next-best-practices --yes
npx skills add https://github.com/vercel-labs/next-skills --skill next-cache-components --yes
npx skills add https://github.com/vercel-labs/agent-skills --skill web-design-guidelines --yes
```

### 1.2 Install Migent

```bash
npm install -g migent
```

**VERIFY**: `migent --version` returns a version number.

### 1.3 Ask User Questions

1. **"Which directory contains your legacy site?"**
   - Scan workspace for `package.json`, `composer.json`, `Gemfile`, `index.html`, `index.php`
   - Offer detected options as choices

2. **"What port is your legacy site running on?"** (or "How do I start it?")
   - Common ports: 3000, 4000, 8000, 8080

3. **"What should I name the Next.js project?"**
   - Suggest: `<legacy-name>-next`

### 1.4 Validate Legacy Site

```bash
ls -la <legacy-directory>
curl -s -o /dev/null -w "%{http_code}" http://localhost:<port>/
```

**MUST PASS**: Directory exists AND curl returns `200`.

**CAPTURE** any observed request patterns. Example: Redirect to /en means the site has localisation — include it in the migration plan.

**IF VALIDATION FAILS**: Return to user with specific error. Do not guess or proceed.

### 1.5 Load All Skills

Load all skill contexts now. They will be used throughout the migration.

```
/next-best-practices
/vercel-react-best-practices
/web-design-guidelines
```

**IMPORTANT**: Always use the latest Next.js and tailwindcss (check versions).

### 1.6 Create Next.js Project

```bash
bunx create-next-app@latest <project-name> \
  --typescript \
  --tailwind \
  --app \
  --src-dir \
  --import-alias "@/*" \
  --use-bun \
  --yes
```

**NOTE**:
- Use `bun`, not `npm`
- Use `bunx`, not `npx`
- ESLint is NOT included — we use Biome

### 1.7 Install Biome

```bash
cd <project-name>
bun add -D @biomejs/biome
```

Create `biome.json`:
```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "organizeImports": { "enabled": true },
  "linter": {
    "enabled": true,
    "rules": { "recommended": true }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2
  }
}
```

### 1.8 Configure MCP

Configure MCP servers in the **workspace root** (NOT inside the Next.js project):

```
workspace/              ← config goes HERE
├── legacy-site/
├── my-next-app/
└── .mcp.json
```

Create `.mcp.json`:
```json
{
  "mcpServers": {
    "migent": {
      "command": "npx",
      "args": ["-y", "migent", "mcp"]
    }
  }
}
```

### 1.9 Verify MCP

Start the Next.js dev server, then test MCP:

```bash
bun run dev
```

```
ir_capture(port: 3000, route: "/")
```

**VERIFY**: Returns JSON with `elementCount > 0`.

### 1.10 Copy Assets

```bash
mkdir -p <next-project>/public
cp -r <legacy-directory>/images/* <next-project>/public/images/ 2>/dev/null || true
cp -r <legacy-directory>/fonts/* <next-project>/public/fonts/ 2>/dev/null || true
cp -r <legacy-directory>/assets/* <next-project>/public/assets/ 2>/dev/null || true
```

### Setup Checkpoint

Before proceeding, confirm ALL of the following:
- [ ] All 4 skills installed
- [ ] Legacy site running and accessible
- [ ] Next.js project created with Biome configured
- [ ] MCP returning captures for both sites
- [ ] Assets copied

**IF ANY FAILS**: Stop and report the error to the user.

---

## PHASE 2: DISCOVERY

Use MCP tools to capture the legacy site and analyze patterns. **DO NOT USE CURL. DO NOT FETCH HTML MANUALLY.**

### 2.1 Discover Routes

Analyze legacy codebase to find all routes:
- Check `sitemap.xml` if exists
- Check router files (Express routes, Next.js pages, PHP files)
- Check navigation links in captured IR

### 2.2 Capture All Routes (Parallel)

Call `ir_capture` for all discovered routes **in parallel** (batch all calls in a single message). Each `ir_capture` creates a fresh Playwright page — no shared state conflicts.

```
# Call all in one message — they run concurrently:
ir_capture(port: <legacy-port>, route: "/")
ir_capture(port: <legacy-port>, route: "/about")
ir_capture(port: <legacy-port>, route: "/contact")
# ... all discovered routes
```

Collect all results. Write captures to `migration.json`:
```json
{
  "legacy": {
    "directory": "./legacy-site",
    "port": 8000,
    "framework": "php",
    "routes": ["/", "/about", "/contact"]
  },
  "captures": {
    "/": { "elementCount": 150, "animationCount": 12 },
    "/about": { "elementCount": 89, "animationCount": 3 }
  },
  "next": {
    "directory": "./my-next-app",
    "port": 3000
  },
  "routeStatus": {
    "/": "pending",
    "/about": "pending",
    "/contact": "pending"
  },
  "progress": {},
  "skippedIssues": []
}
```

### 2.3 Analyze JavaScript Patterns

**IMPORTANT**: Legacy JavaScript is ANYTHING that is NOT React or Next.js.

Search legacy codebase for patterns that need conversion:

```bash
# Find jQuery
grep -r "jquery\|jQuery\|\\\$(" <legacy-directory> --include="*.js" --include="*.html" --include="*.php"

# Find inline handlers
grep -r "onclick=\|onsubmit=\|onchange=" <legacy-directory> --include="*.html" --include="*.php"
```

Document findings in `migration.json` under `legacy.javascript`.

### 2.4 Detect Locales & Validate Links

Check `ir_capture` results for locale patterns:

1. **Redirect-based detection**: If `ir_capture` returns `redirects` (e.g., `/` → `/en/`), the site uses locale prefixes.
2. **Route-based detection**: If discovered routes have locale prefixes (e.g., `/en/about`, `/fr/about`), locales are in use.

**If locales are detected:**
- Set up Next.js i18n middleware for locale routing
- Create `src/middleware.ts` with locale detection and redirect logic
- Use `next-intl` or Next.js built-in i18n for locale-aware Link components
- Validate all internal links include the correct locale prefix
- Map each locale route to its Next.js equivalent

**Internal link validation**: Check `ir_capture` `internalLinks` against detected locales. Links missing locale prefixes will break in the migrated site.

### 2.5 Install Conditional Dependencies

Based on discovery results:

If animations were detected in any `ir_capture`:
```bash
cd <next-project>
bun add framer-motion
```

---

## PHASE 3: MIGRATE (PER ROUTE)

For EACH route discovered in Phase 2, repeat steps 3.1 through 3.4. Start with `/` to build the shared shell first.

### CRITICAL RULES — VIOLATIONS ARE FAILURES

**FORBIDDEN:**
- `dangerouslySetInnerHTML` — NEVER use to copy legacy HTML
- `onclick="..."` or any inline event handlers
- jQuery or any jQuery patterns
- `<script>` tags with inline JavaScript
- `class=` instead of `className=`

**REQUIRED:**
- Proper JSX with `className`
- React event handlers (`onClick={handler}`)
- Match computed styles visually (Tailwind utilities, CSS modules, or global CSS — see Appendix A)
- `next/image` for images
- Server Components by default
- `'use client'` only when needed

**RECOMMENDED** (enforce in Phase 5):
- `next/font` for fonts (see Appendix C)
- shadcn/ui components for form elements, dialogs, tables (see Appendix D)
- Tailwind utilities over CSS modules/global CSS

### 3.1 Build Page

**For `/` (first route):** also build the shared shell:
1. Create `src/app/layout.tsx` (RootLayout) with HTML structure, metadata
2. Extract shared components: Header, Footer, Nav → `src/components/`
3. Register components in `migration.json` under `components`

**For all routes (including `/`):**

Read captured IR from `migration.json` for this route.

Use `ir_inspect(selector: "...", site: "legacy")` to get full computed styles for specific elements.

Based on captured IR:
1. Create `src/app/<route>/page.tsx`
2. Convert layout structure to JSX
3. Convert captured computed styles to Tailwind (see Appendix A)
4. Convert event handlers to React patterns
5. Import shared components from `src/components/` — do NOT recreate them
6. Recreate animations using captured animation data (see Appendix B)

### 3.2 Code Quality Gate

**BEFORE visual validation**, verify no anti-patterns:

```bash
# Anti-patterns (ALL MUST RETURN no results)
grep -r "dangerouslySetInnerHTML" <next-project>/src/
grep -r 'onclick="' <next-project>/src/
grep -r 'class="' <next-project>/src/ --include="*.tsx" --include="*.jsx"
grep -r 'style={{' <next-project>/src/ --include="*.tsx" --include="*.jsx"
grep -r "from ['\"]jquery['\"]" <next-project>/src/
```

**ALL MUST RETURN**: No results. Fix any violations before proceeding.

### 3.3 Visual Validation Loop

Start watch mode:
```
ir_start(legacyPort: <legacy-port>, nextPort: 3000, legacyRoute: "<route>", nextRoute: "<route>")
→ { status: "watching", match: {...}, totalIssues: N, firstIssue: {...} }
```

Loop until match >= 95%:
```
result = ir_next()

IF result.clsBlocked:
  - CLS score is above 0.1 — ir_next REFUSES to serve other issues
  - Read result.cls.topShifters to identify which elements shifted
  - Fix using result.suggestedFixes:
    1. Font shift → next/font with display: "swap", adjustFontFallback: true
    2. Image shift → next/image with explicit width + height
    3. Dynamic content → min-height or skeleton placeholders
    4. Embeds → fixed aspect-ratio container
  - Save file → watch recaptures → call ir_next again
  - Repeat until clsBlocked is gone

IF result.regressionBlocked:
  - New issues were introduced — fix the regression first
  - Save file → watch recaptures → call ir_next again

IF result.issue exists:
  - Read issue details (selector, styles, position)
  - Fix the specific issue
  - Save file → wait for rebuild → call ir_next again
  - After 3 failed attempts on the same issue: ir_next(skip: true)
  - Document skipped issue in migration.json under skippedIssues

IF result.complete or match >= 95%:
  - Proceed to 3.4
```

**CLS is a hard gate.** `ir_next` will not serve style/content/missing issues until CLS score is "good" (<= 0.1). This is enforced by the tool, not by convention. You cannot skip it.

### 3.4 Mark Route Complete

```
ir_stop()
```

Update `routeStatus` to `"validated"` in `migration.json`. Move to next route.

If only skipped issues remain and match is below 95%: update `routeStatus` to `"failed"`, mark route for human review, and continue.

---

## PHASE 4: COMPLETION

### 4.1 Generate Report

Create `MIGRATION_REPORT.md` with:
- Summary (routes migrated, match percentages)
- Per-route breakdown
- Skipped issues requiring human review
- Components created
- Recommendations

### 4.2 Cleanup

```
ir_stop()
```

---

## PHASE 5: MODERNIZE (OPTIONAL)

Post-migration pass to adopt modern component patterns and tooling. Run this **after all routes pass visual parity** in Phase 4. Each step is independent — skip any that don't apply.

### 5.1 Install shadcn/ui

```bash
cd <next-project>
bunx shadcn@latest init -y
```

### 5.2 Configure shadcn MCP

Add to `.mcp.json`:
```json
{
  "mcpServers": {
    "migent": {
      "command": "npx",
      "args": ["-y", "migent", "mcp"]
    },
    "shadcn": {
      "command": "npx",
      "args": ["shadcn@latest", "mcp"]
    }
  }
}
```

### 5.3 Install Components

Use `ir_capture` `uiPatterns.shadcnComponentsNeeded` data to install the right components:

```bash
# Example: if uiPatterns shows Button, Dialog, Table, NavigationMenu
bunx shadcn@latest add button dialog table navigation-menu -y
```

Also search for **blocks** that match legacy page patterns (e.g., login forms, dashboards, pricing pages).

### 5.4 Convert to shadcn Components

Replace raw HTML elements with shadcn equivalents (see Appendix D):
- `<button>` → `<Button>`
- `<input>` → `<Input>`
- `<table>` → `<Table>`
- `<dialog>` / `.modal` → `<Dialog>`

### 5.5 Convert to Tailwind Utilities

Replace CSS modules and global CSS with Tailwind utilities where possible. Use Appendix A as a mapping reference.

### 5.6 Convert to next/font

Replace `@font-face` declarations with `next/font` (see Appendix C).

### 5.7 Verify No Visual Regressions

Run `ir_start` again after modernization to confirm no regressions:
```
ir_start(legacyPort: <legacy-port>, nextPort: 3000, legacyRoute: "<route>", nextRoute: "<route>")
```

Check that match percentages are unchanged or improved.

### 5.8 Code Quality Checks

```bash
# shadcn enforcement — raw HTML elements should be replaced
grep -rn '<button' <next-project>/src/ --include="*.tsx" --include="*.jsx" | grep -v 'components/ui/'
grep -rn '<input' <next-project>/src/ --include="*.tsx" --include="*.jsx" | grep -v 'components/ui/'
grep -rn '<textarea' <next-project>/src/ --include="*.tsx" --include="*.jsx" | grep -v 'components/ui/'
grep -rn '<select' <next-project>/src/ --include="*.tsx" --include="*.jsx" | grep -v 'components/ui/'
grep -rn '<table' <next-project>/src/ --include="*.tsx" --include="*.jsx" | grep -v 'components/ui/'
grep -rn '<dialog' <next-project>/src/ --include="*.tsx" --include="*.jsx" | grep -v 'components/ui/'

# Font enforcement — no raw @font-face
grep -r "@font-face" <next-project>/src/

# Verify shadcn IS being used
grep -rn "from ['\"]@/components/ui/" <next-project>/src/ --include="*.tsx"

# Legacy CSS class names should be converted to Tailwind
grep -rE 'className="[^"]*[a-z]+_[a-z]+' <next-project>/src/ --include="*.tsx"
```

---

## ERROR HANDLING

### MCP tool fails
Stop and report to user. Do not attempt workarounds.

### Site unreachable
Stop and ask user to restart the server.

---

## RESUMABILITY

`migration.json` tracks per-route status in `routeStatus`:

| Status | Meaning |
|---|---|
| `pending` | Not yet migrated |
| `validated` | Passed visual validation (match >= 95%) |
| `failed` | Below 95% after exhausting fixes, needs human review |

If `migration.json` exists when `/migration` is invoked:
1. Read existing state
2. Skip `validated` routes entirely
3. Resume from first `pending` route
4. Retry `failed` routes if user requests it

---

## APPENDIX A: Captured Styles → Tailwind Mapping

Use `ir_inspect(selector: "...", site: "legacy")` to get computed styles, then convert:

**Colors** (backgroundColor, color, borderColor):
```
rgb(196, 30, 58) → bg-[#c41e3a] or bg-red-600 (if close match)
rgb(255, 255, 255) → bg-white
rgb(0, 0, 0) → bg-black
rgba(0,0,0,0.5) → bg-black/50
```

**Spacing** (padding, margin):
```
padding: "16px" → p-4
padding: "15px 20px" → py-[15px] px-5
margin: "0 auto" → mx-auto
margin: "24px 0 0 0" → mt-6
```

**Typography**:
```
fontSize: "14px" → text-sm
fontSize: "18px" → text-lg
fontSize: "32px" → text-3xl
fontWeight: "700" → font-bold
fontWeight: "600" → font-semibold
lineHeight: "1.5" → leading-normal
textAlign: "center" → text-center
```

**Layout**:
```
display: "flex" → flex
display: "grid" → grid
flexDirection: "column" → flex-col
justifyContent: "center" → justify-center
alignItems: "center" → items-center
gap: "16px" → gap-4
```

**Sizing**:
```
width: "100%" → w-full
maxWidth: "1280px" → max-w-7xl
height: "auto" → h-auto
minHeight: "100vh" → min-h-screen
```

**Position**:
```
position: "absolute" → absolute
position: "relative" → relative
position: "fixed" → fixed
top: "0px" → top-0
left: "50%" → left-1/2
```

**Borders**:
```
borderRadius: "8px" → rounded-lg
borderRadius: "9999px" → rounded-full
borderWidth: "1px" → border
borderColor: "rgb(229,231,235)" → border-gray-200
```

**Font Style**:
```
fontStyle: "italic" → italic
fontStyle: "normal" → not-italic
```

**Text Transform**:
```
textTransform: "uppercase" → uppercase
textTransform: "lowercase" → lowercase
textTransform: "capitalize" → capitalize
textTransform: "none" → normal-case
```

**Text Decoration**:
```
textDecoration: "underline" → underline
textDecoration: "line-through" → line-through
textDecoration: "none" → no-underline
```

**Overflow**:
```
overflow: "hidden" → overflow-hidden
overflow: "auto" → overflow-auto
overflow: "scroll" → overflow-scroll
overflowX: "auto" → overflow-x-auto
overflowY: "hidden" → overflow-y-hidden
```

**Grid**:
```
gridTemplateColumns: "repeat(3, 1fr)" → grid-cols-3
gridTemplateColumns: "repeat(4, minmax(0, 1fr))" → grid-cols-4
gridTemplateColumns: "200px 1fr" → grid-cols-[200px_1fr]
```

**Transform**:
```
transform: "translateX(-50%)" → -translate-x-1/2
transform: "rotate(45deg)" → rotate-45
transform: "scale(1.1)" → scale-110
```

**Effects**:
```
opacity: "0.5" → opacity-50
boxShadow: "0 1px 3px rgba(0,0,0,0.1)" → shadow-sm
boxShadow: "0 10px 15px rgba(0,0,0,0.1)" → shadow-lg
```

**Arbitrary values** (when no Tailwind match):
```
padding: "13px" → p-[13px]
backgroundColor: "#c41e3a" → bg-[#c41e3a]
fontSize: "17px" → text-[17px]
maxWidth: "1140px" → max-w-[1140px]
```

---

## APPENDIX B: Recreating Animations

From captured `animations` data in `ir_capture`:

**CSS @keyframes → Framer Motion:**
```tsx
// Captured: { name: "fadeInUp", duration: "0.6s", timingFunction: "ease-out" }

import { motion } from 'framer-motion';

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.6, ease: "easeOut" }}
>
```

**CSS @keyframes → Tailwind animation:**
```css
/* Add to globals.css — copy the captured keyframes rule */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
```
```tsx
<div className="animate-[fadeInUp_0.6s_ease-out]">
```

**Transitions:**
```tsx
// Captured: { property: "background-color", duration: "0.2s", timingFunction: "ease" }

<button className="transition-colors duration-200 ease-in-out hover:bg-red-700">
```

**jQuery animations → Framer Motion:**
```tsx
// Captured: jQueryAnimations: [".fadeIn(300)"]

import { AnimatePresence, motion } from 'framer-motion';

<AnimatePresence>
  {isVisible && (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
    >
  )}
</AnimatePresence>
```

---

## APPENDIX C: Font Migration

Read font data from `ir_capture` response (`fonts` section). For each detected font family:

**Google Fonts → `next/font/google`:**
```tsx
import { Inter, Roboto } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  weight: ['400', '700'],  // from fonts[].weight
  style: ['normal', 'italic'],  // from fonts[].style
  display: 'swap',  // from fonts[].display or default to 'swap'
  variable: '--font-inter',
});
```

**Custom Fonts → `next/font/local`:**
```tsx
import localFont from 'next/font/local';

const customFont = localFont({
  src: [
    { path: './fonts/custom-regular.woff2', weight: '400', style: 'normal' },
    { path: './fonts/custom-bold.woff2', weight: '700', style: 'normal' },
  ],
  variable: '--font-custom',
  display: 'swap',
});
```

**Apply in `layout.tsx`:**
```tsx
export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${inter.variable} ${customFont.variable}`}>
      <body>{children}</body>
    </html>
  );
}
```

**Configure in `tailwind.config.ts`:**
```ts
fontFamily: {
  sans: ['var(--font-inter)', ...defaultTheme.fontFamily.sans],
  custom: ['var(--font-custom)'],
},
```

**Download font files**: If `ir_capture` `fonts[].src` contains URLs, download .woff2 files to `public/fonts/` for `next/font/local`.

---

## APPENDIX D: shadcn Component Mapping (Phase 5)

Use shadcn components instead of raw HTML. Reference this during Phase 5 (Modernize). Map legacy elements:

| Legacy HTML | shadcn Component | Import |
|---|---|---|
| `<button>`, `<input type="submit">` | `<Button>` | `@/components/ui/button` |
| `<input type="text\|email\|password">` | `<Input>` | `@/components/ui/input` |
| `<textarea>` | `<Textarea>` | `@/components/ui/textarea` |
| `<select>` | `<Select>` | `@/components/ui/select` |
| `<table>` | `<Table>` | `@/components/ui/table` |
| `<dialog>`, `.modal` | `<Dialog>` | `@/components/ui/dialog` |
| `<nav>` | `<NavigationMenu>` | `@/components/ui/navigation-menu` |
| `.card`, `<article>` | `<Card>` | `@/components/ui/card` |
| `<input type="checkbox">` | `<Checkbox>` | `@/components/ui/checkbox` |
| `<input type="radio">` | `<RadioGroup>` | `@/components/ui/radio-group` |
| `.tabs`, `[role="tablist"]` | `<Tabs>` | `@/components/ui/tabs` |
| `.accordion`, `<details>` | `<Accordion>` | `@/components/ui/accordion` |
| `.breadcrumb` | `<Breadcrumb>` | `@/components/ui/breadcrumb` |
| `.pagination` | `<Pagination>` | `@/components/ui/pagination` |

**Example conversion:**
```tsx
// WRONG - raw HTML
<button className="bg-red-600 text-white px-4 py-2 rounded">Submit</button>

// CORRECT - shadcn Button
import { Button } from "@/components/ui/button";
<Button className="bg-red-600 text-white">Submit</Button>
```

```tsx
// WRONG - raw HTML table
<table><tr><td>Name</td></tr></table>

// CORRECT - shadcn Table
import { Table, TableBody, TableCell, TableRow } from "@/components/ui/table";
<Table>
  <TableBody>
    <TableRow>
      <TableCell>Name</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

**Raw HTML elements (`<button>`, `<input>`, `<table>`, `<dialog>`) should be replaced in Phase 5.**

**Code quality checks (run during Phase 5):**
```bash
# No raw @font-face in CSS (must use next/font)
grep -r "@font-face" <next-project>/src/

# No raw <button> outside components/ui/ (must use shadcn Button)
grep -rn '<button' <next-project>/src/ --include="*.tsx" --include="*.jsx" | grep -v 'components/ui/'

# No raw <input> outside components/ui/ (must use shadcn Input)
grep -rn '<input' <next-project>/src/ --include="*.tsx" --include="*.jsx" | grep -v 'components/ui/'

# No raw <table> outside components/ui/ (must use shadcn Table)
grep -rn '<table' <next-project>/src/ --include="*.tsx" --include="*.jsx" | grep -v 'components/ui/'

# Verify shadcn components ARE being used
grep -rn "from ['\"]@/components/ui/" <next-project>/src/ --include="*.tsx"
```
**ALL MUST RETURN**: No results (except shadcn verification which SHOULD return matches). These checks are enforced in Phase 5, not during Phase 3 migration.

---

## APPENDIX E: MCP Tools Reference

### ir_capture
Capture a page's DOM tree, computed styles, animation metadata, and CLS score.

```
ir_capture(port: number, route?: string, width?: number, height?: number)
```

Deterministic capture sequence:
1. Waits for network idle
2. Forces all lazy images to load
3. Waits for all images and fonts
4. Extracts animation metadata (BEFORE finishing animations)
5. Forces all animations to END STATE
6. Waits for DOM stability

**Returns:**
- Layout patterns (header, nav, footer, sidebar, main)
- Component hierarchy
- Top-level elements with computed styles
- **Animation data:** keyframes, animatedElements, transitionElements, jQueryAnimations
- **CLS data:** score, rating, top shifters
- **Font data** (`fonts`): totalFontFaces, fontFaces, uniqueFamilies
- **UI patterns** (`uiPatterns`): patterns with shadcnComponentsNeeded
- **Redirects** (`redirects`): Array of { from, to, statusCode } — useful for locale detection
- **Internal links** (`internalLinks`): { total, links[] } — for route validation

### ir_start
Start migration watch mode. Captures both sites, diffs, starts file watcher, returns first issue.
```
ir_start(legacyPort, nextPort, legacyRoute?, nextRoute?, watchPaths?)
```
Returns: `{ status: "watching", match: {...}, totalIssues: N, firstIssue: {...} }`.

### ir_next
Get next issue to fix. Blocks on CLS gate and regressions.
```
ir_next(skip?: boolean)
```
- `skip: true` — skip current issue after failed attempts, advance to next
- Returns: Issue with selector, position, styles, and fix suggestion.

### ir_status
Migration progress: match percentages, issue counts by severity, CLS score, regression state.

### ir_inspect
Inspect element by selector or text.
```
ir_inspect(selector: string, site?: "legacy" | "next" | "both")
```
- `site="legacy"` or `"next"`: full styles, rect, snippet for one side
- `site="both"` (default): side-by-side comparison with style diffs

### ir_stop
Stop watch mode and close browser.
