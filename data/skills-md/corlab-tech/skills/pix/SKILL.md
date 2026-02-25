---
name: pix
description: Launches an autonomous, pixel-perfect UI implementation loop using Figma MCP and Chrome.
allowed-tools: [Bash, Read, Glob, Grep, Edit, Write]
---

# /pix: The Pixel-Perfect Autonomous Loop

> **Note**: This skill requires Figma MCP and Claude Chrome extension. Tool names may vary based on your MCP configuration (e.g., `figma__get_screenshot` or `mcp__figma__get_screenshot`). Run `/mcp` to see available tools.

## Phase 0: Project Discovery

Before anything else, analyze the project to understand its stack:

### 1. Package Manager Detection
Check which lockfile exists: `package-lock.json` (npm), `yarn.lock` (yarn), `pnpm-lock.yaml` (pnpm), `bun.lockb` (bun).
Use the corresponding command for all package operations.

### 2. Dev Server & Port Detection
- Read `package.json` scripts to find the dev command
- Check for port configuration in: `vite.config.*`, `next.config.*`, `nuxt.config.*`, `webpack.config.*`, `.env*`, or the dev script itself
- Common patterns: `--port`, `-p`, `PORT=`, `server.port`
- Default fallback order: 5173 (Vite), 3000 (Next/CRA), 8080 (Vue CLI)

### 3. Design System Detection
Scan `package.json` dependencies for styling approach:
- **Tailwind**: `tailwindcss` → config in `tailwind.config.*`
- **CSS-in-JS**: `styled-components`, `@emotion/*`, `stitches`
- **Component Libraries**: `@chakra-ui/*`, `@mui/*`, `@mantine/*`, `antd`, `@radix-ui/*`
- **CSS Modules**: check for `*.module.css` files
- **Vanilla CSS/SCSS**: check for global stylesheets

### 4. Icon Library Detection
Scan `package.json` and imports for icon libraries:
- `lucide-react` → Lucide
- `@heroicons/react` → Heroicons
- `react-icons` → React Icons (multi-library)
- `@radix-ui/react-icons` → Radix Icons
- `@fortawesome/*` → FontAwesome
- `@phosphor-icons/react` → Phosphor
- `@tabler/icons-react` → Tabler Icons
- If none found, ask user which to install or use inline SVGs

### 5. System Verification
1. **MCP Check**: Verify Figma MCP is connected and authenticated:
    - Call `whoami` to check authentication status
    - If not connected: alert user to configure Figma MCP
    - If not authenticated: guide user to authenticate via Figma OAuth
    - Display the authenticated user info to confirm correct account
2. **Chrome Check**: Ensure Claude Chrome extension is active and connected.
3. **Dev Server**: Using detected port, run `lsof -i :<PORT>` to check if server is already running. If running, leave it alone. If not running, start dev server in background using detected package manager and script.

## Phase 1: Context Gathering

### Chrome Setup

Open Chrome with `localhost:<DETECTED_PORT>`:
- Navigate to the page/route where the component will live
- This tab is used for visual comparison and interaction testing (hover, click, focus states)
- **Zoom in** on the component area for more detailed screenshots

### User Input

**Stop and Ask**:
- "Paste the Figma link to the component you want to build"
- (Use 'Copy link to selection' in Figma)

> **Note**: No need to open Figma in Chrome — Figma MCP handles screenshots via `get_screenshot`.

## Phase 2: The Magic Prompt (Deep Execution)

Once the link is provided, you must execute this EXACT sequence. Do not skip details:

### 1. Hard Data Extraction (Figma MCP)

Use these Figma MCP tools in sequence:

* **Structure**: Use `get_metadata` to understand the component hierarchy and layer structure.
* **Design Context**: Use `get_design_context` to get the full design specification including layout, spacing, and styles.
* **Tokens**: Use `get_variable_defs` to extract hex codes, corner-radius, shadows, and typography tokens.
* **Existing Components**: Use `get_code_connect_map` to check if any Figma components already map to code components in the codebase. Reuse existing components instead of recreating them.
* **Typography**: Get numeric `font-weight` (e.g., 600 vs 700), `line-height`, and `letter-spacing`.
* **Icon Colors**: Extract icon stroke/fill colors separately from text colors. Check `--stroke-0`, `fill`, or style definitions. Never assume icons inherit text color.
* **Container Layout Analysis**: Before implementing, identify:
    - Which elements share a common background vs have distinct backgrounds
    - Where borders/dividers separate sections
    - Whether sections extend edge-to-edge within their parent or are visually inset

### 2. Exhaustive Property Verification

**Rule**: Before writing code for ANY element, call `get_design_context` and verify ALL applicable properties. Never assume inheritance or defaults. Extract each value explicitly.

**Text**:
`font-family`, `font-size`, `font-weight`, `line-height`, `letter-spacing`, `color`, `opacity`, `text-align`, `text-decoration`, `text-transform`

**Container/Block**:
`width`, `height`, `min-width`, `max-width`, `padding` (all 4 sides), `margin`, `background-color`, `border-radius`, `border-width`, `border-color`, `border-style`, `box-shadow`, `opacity`, `overflow`

**Icon**:
`size` (width/height), `fill`, `stroke`, `stroke-width`, `color` (independent from parent text)

**Button/Link**:
All text properties + all container properties + `cursor`, `hover-state`, `active-state`, `disabled-state`

**Image**:
`width`, `height`, `object-fit`, `border-radius`, `border`, `aspect-ratio`

**Spacing**:
`gap`, `row-gap`, `column-gap`, space-between elements

**Layout Principle**: Avoid hardcoded sizes (`max-w-[140px]`, `w-[200px]`, etc.). With correct `font-size`, `line-height`, `padding`, and parent container width, elements should naturally render correctly. Hardcoded dimensions are a symptom of incorrect upstream layout — fix the root cause instead.

**Responsive Design**: Keep responsiveness in mind as a big plus. Even if only one breakpoint is provided in Figma, consider how the component should adapt to different screen sizes. When possible, implement both desktop and mobile-friendly styles using the project's responsive approach (Tailwind breakpoints, CSS media queries, container queries).

**Never use approximate Tailwind classes** (like `text-zinc-500`) when exact hex values are available from MCP.

### 3. Design System Sync

NEVER hardcode values. Always sync to the project's design system:

- If **Tailwind**: Check `tailwind.config.*`. If a Figma value is missing, **update the config**. NEVER hardcode arbitrary hex values like `text-[#f3f3f3]` if they should be tokens.
- If **CSS-in-JS**: Add tokens to the theme object/file. NEVER use inline hex values.
- If **Component Library**: Map to existing theme tokens, extend theme if needed. NEVER bypass the theme.
- If **CSS/SCSS**: Add CSS custom properties to `:root`. NEVER scatter magic values.

### 4. Icons

Map Figma layer names to the **project's detected icon library**. Match the `stroke-width` and `size` (px) to the design exactly. If no icon library exists, ask user preference or use inline SVG from Figma.

### 5. Implementation & "Building Brick" QA

Implement the code using the project's existing patterns, then start the **Comparison Loop**:

1. **Screenshot App**: Use Chrome to capture the rendered component at `localhost:<DETECTED_PORT>`.
2. **Screenshot Figma**: Use `get_screenshot` to get the high-res reference from Figma.
3. **The "Brick" Checklist**: Compare the following with 1:1 scrutiny:
    - **Titles**: Is the font boldness and vertical alignment identical?
    - **Icon Shapes**: Does the icon look exactly like the Figma version? Check the stroke thickness.
    - **Icon Colors**: Are icon colors identical to or different from adjacent text?
    - **Distances**: Measure the gaps/margins. If Figma says 24px and the app looks like 20px, refactor.
    - **Borders**: Verify 1px vs 2px lines and the exact curve of `border-radius`.
    - **Edge-to-Edge vs Inset**: Does each section extend to its parent container's edges, or does it appear "floating" with visible gaps?
    - **Background Continuity**: Does the background of a section touch its parent's boundaries, or is there a gap revealing the parent's background?
    - **Padding Ownership**: Is the spacing between content and edges created by the parent container or the child? This affects whether backgrounds extend correctly.

## Phase 3: Recursive Refinement

If you find ANY discrepancy (even 1px):
1. Explain what is wrong.
2. Fix the code.
3. **Repeat Phase 2, Step 5** (Screenshot QA).

**Success Condition**: Only finished when side-by-side screenshots prove local app and Figma design are indistinguishable.

## Phase 4: User Review

Once you're satisfied with the result, **stop and ask**:
- "Here's the final result. Are you happy with it?"
- "If something looks off, paste a Figma 'Link to Selection' for the specific area you'd like me to focus on."

If the user provides a new link, re-run Phase 2 scoped to that specific selection. This allows targeted refinement of individual building blocks without restarting the full component.

**ULTRA-THINK MODE ENABLED**: Take your time. Perfection over speed.

## Examples

**Good invocation:**
```
/pix
> Paste Figma link: https://figma.com/design/abc123/MyApp?node-id=42-100
```

**What Claude does:**
1. Detects: Vite + Tailwind + Lucide icons
2. Extracts: colors, typography, spacing from Figma
3. Updates: `tailwind.config.js` with missing tokens
4. Implements: component with exact values
5. Screenshots: both app and Figma
6. Compares: finds 2px gap difference
7. Fixes: adjusts padding
8. Repeats: until pixel-perfect match

**Bad patterns to avoid:**
- ❌ `text-[#f3f3f3]` — hardcoded hex in Tailwind
- ❌ `w-[247px]` — magic width number
- ❌ Assuming icon color matches text
- ❌ Skipping screenshot comparison