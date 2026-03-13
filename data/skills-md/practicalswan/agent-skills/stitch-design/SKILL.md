---
name: stitch-design
description: Google Stitch design toolkit — DESIGN.md generation, screen-to-React conversion, shadcn/ui integration, prompt enhancement, and Remotion walkthroughs. Use when working with Stitch MCP design projects.
license: Complete terms in LICENSE.txt
---



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`


Comprehensive toolkit for Google Stitch projects — combining design system documentation, React component conversion, autonomous build loops, prompt engineering, video walkthroughs, and shadcn/ui component integration. Based on [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills).

## When to Use This Skill

- Analyzing Stitch projects and generating DESIGN.md files
- Converting Stitch screens to modular React/TypeScript components
- Building multi-page websites autonomously via the Stitch build loop
- Enhancing vague UI prompts into Stitch-optimized structured prompts
- Creating walkthrough videos from Stitch projects using Remotion
- Integrating and customizing shadcn/ui components in React apps


---

## Part 1: Design System Documentation (design-md)

Analyze Stitch project screens and synthesize a semantic design system into `DESIGN.md`.

### Prerequisites
- Access to Stitch MCP Server
- A Stitch project with at least one designed screen

### Workflow
1. **Retrieval**: Use Stitch MCP to fetch project screens, HTML code, and metadata
2. **Extraction**: Identify design tokens — colors, typography, spacing, component patterns
3. **Translation**: Convert CSS/Tailwind values into descriptive design language
4. **Synthesis**: Generate comprehensive DESIGN.md

### Analysis Steps
1. **Extract Project Identity** — Title, Project ID from JSON
2. **Define the Atmosphere** — Evocative adjectives for mood (e.g., "Airy", "Minimalist")
3. **Map Color Palette** — Descriptive name + hex code + functional role
4. **Translate Geometry & Shape** — Corner roundness, spacing patterns
5. **Describe Depth & Elevation** — Shadows, layering

### DESIGN.md Output Structure
```markdown


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

**Project ID:** [ID]

## 1. Visual Theme & Atmosphere
## 2. Color Palette & Roles
## 3. Typography Rules
## 4. Component Stylings
## 5. Layout Principles
```

### Guidelines
- Use descriptive design language, not technical jargon
- Include exact hex codes alongside descriptive names
- Explain the "why" behind design decisions

### Pitfalls to Avoid
- Using raw CSS class names without translation
- Omitting color codes or using only descriptive names
- Being too vague in atmosphere descriptions

---

## Part 2: React Component Conversion (react-components)

Convert Stitch screens into modular Vite and React component systems with AST-based validation.

### Retrieval
1. Discover Stitch MCP prefix via `list_tools`
2. Fetch design JSON with `get_screen`
3. Download HTML using system-level curl for reliability
4. Check `screenshot.downloadUrl` for visual verification

### Architectural Rules
- **Modular components**: Independent files, avoid monoliths
- **Logic isolation**: Event handlers in custom hooks (`src/hooks/`)
- **Data decoupling**: Static text/URLs in `src/data/mockData.ts`
- **Type safety**: `Readonly` TypeScript interface for every component
- **Style mapping**: Extract Tailwind config from HTML `<head>`, use theme-mapped classes

### Execution Steps
1. Environment setup: `npm install` if needed
2. Create `src/data/mockData.ts` from design content
3. Draft components using template, replace `StitchComponent` with actual names
4. Wire up in `App.tsx`
5. Quality check: run validation, verify against architecture checklist

### Architecture Checklist
- Logic extracted to custom hooks
- No monolithic files; Atomic/Composite modularity
- Static text/URLs in mockData.ts
- Props use `Readonly<T>` interfaces
- Valid TypeScript (no errors)
- Dark mode (`dark:`) applied to all color classes
- No hardcoded hex values; use theme-mapped Tailwind classes

---

## Part 3: Build Loop (stitch-loop)

Autonomous baton-passing pattern for building complete multi-page websites.

### Execution Protocol
1. **Read the Baton** — `next-prompt.md` contains current task
2. **Consult Context Files** — `DESIGN.md` for visual system, `SITE.md` for site constitution
3. **Generate with Stitch** — Create/edit screens using Stitch MCP
4. **Integrate into Site** — Move from `queue/` to `site/public/`
5. **Update Site Documentation** — Keep SITE.md current
6. **Prepare Next Baton** — Write new `next-prompt.md` for the next iteration

### File Structure
```
project/
├── next-prompt.md      # The baton — current task
├── stitch.json         # Stitch project ID
├── DESIGN.md           # Visual design system
├── SITE.md             # Site vision, sitemap, roadmap
├── queue/              # Staging area for Stitch output
└── site/public/        # Production pages
```

---

## Part 4: Prompt Enhancement (enhance-prompt)

Transform vague UI ideas into polished, Stitch-optimized prompts.

### Enhancement Pipeline

#### Step 1: Assess the Input

| Element | Check for | If missing... |
|---------|-----------|---------------|
| Platform | "web", "mobile", "desktop" | Add based on context |
| Page type | "landing page", "dashboard" | Infer from description |
| Structure | Numbered sections | Create logical structure |
| Visual style | Adjectives, mood, vibe | Add appropriate descriptors |
| Colors | Specific values or roles | Add design system or suggest |
| Components | UI-specific terms | Translate to proper keywords |

#### Step 2: Check for DESIGN.md
- If exists: Extract color palette, typography, component styles
- If missing: Recommend creating one with the design-md workflow

#### Step 3: Apply Enhancements
- **UI/UX Keywords**: Replace vague terms with specific component names
- **Amplify the Vibe**: Add atmospheric adjectives
- **Structure the Page**: Create numbered section layout
- **Format Colors**: Use design system block

#### Step 4: Format the Output
- Stitch-optimized prompt with design system block and numbered structure

---

## Part 5: Remotion Video Walkthroughs (remotion)

Generate walkthrough videos from Stitch projects using Remotion.

### Prerequisites
- Stitch MCP Server and Remotion MCP Server (or CLI)
- Node.js and npm

### Workflow
1. **Gather Screen Assets** — List screens, download screenshots, create manifest
2. **Generate Remotion Components** — ScreenSlide.tsx, WalkthroughComposition.tsx
3. **Preview and Refine** — Open Remotion Studio, adjust timing
4. **Render Video** — Produce final MP4

### Video Architecture
- **ScreenSlide.tsx**: Individual screen with zoom/fade animations (3-5 sec per screen)
- **WalkthroughComposition.tsx**: Sequences slides with transitions
- **config.ts**: Frame rate (30fps), dimensions, duration calculation

### File Structure
```
project/
├── video/
│   ├── src/
│   │   ├── WalkthroughComposition.tsx
│   │   ├── ScreenSlide.tsx
│   │   └── components/
│   ├── public/assets/screens/
│   └── remotion.config.ts
├── screens.json
└── output.mp4
```

### Advanced Features
- Dynamic text extraction from Stitch HTML
- Interactive hotspots for clickable elements
- Voiceover integration
- Multiple video patterns (slideshow, feature highlight, user flow)

---

## Part 6: shadcn/ui Integration (shadcn-ui)

Expert guidance for integrating shadcn/ui components into React applications.

### Core Principles
- **Full ownership**: Components in your codebase, not node_modules
- **Complete customization**: Modify styling, behavior, structure freely
- **No version lock-in**: Update selectively
- **Zero runtime overhead**: Just the code you need

### Setup
```bash


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

npx shadcn@latest create



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

npx shadcn@latest init



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

npx shadcn@latest add button card dialog
```

### Component Architecture
```
src/
├── components/
│   ├── ui/              # shadcn components (don't modify directly)
│   └── [custom]/        # your composed components
├── lib/
│   └── utils.ts         # cn() utility
└── app/
    └── page.tsx
```

### The cn() Utility
```typescript
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### Customization
- **Theme**: Edit CSS variables in `globals.css`
- **Variants**: Use `class-variance-authority` (cva)
- **Extending**: Create wrapper components in `components/` (not `components/ui/`)

### Available Components (50+)
- **Layout**: Accordion, Card, Separator, Tabs, Collapsible
- **Forms**: Button, Input, Label, Checkbox, Radio Group, Select, Textarea
- **Data Display**: Table, Badge, Avatar, Progress, Skeleton
- **Overlays**: Dialog, Sheet, Popover, Tooltip, Dropdown Menu
- **Navigation**: Navigation Menu, Breadcrumb, Pagination
- **Feedback**: Alert, Alert Dialog, Toast, Command

### Best Practices
1. Keep `ui/` pure — don't modify originals directly
2. Compose, don't fork — create wrapper components
3. Use the CLI for installation
4. Maintain `cn()` for all class merging
5. Preserve ARIA attributes and keyboard handlers
6. Test in light and dark modes

### Troubleshooting
- **Import errors**: Check `components.json` aliases and `tsconfig.json` paths
- **Style conflicts**: Ensure Tailwind config includes component paths
- **Missing deps**: Run CLI installation to auto-install dependencies

---

## References & Resources

### Documentation
- [Stitch MCP Commands](./references/stitch-mcp-commands.md) — All 5 Stitch MCP commands with parameters and workflow patterns
- [shadcn/ui Components](./references/shadcn-components.md) — 40+ components with CSS variable theming and composite patterns

### Scripts
- [Stitch to React](./scripts/stitch-to-react.ps1) — PowerShell script to set up Vite+React+TypeScript+Tailwind+shadcn projects

### Examples
- [Design System Example](./examples/design-system-example.md) — Complete DESIGN.md example generated from Stitch screen data

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [react-development](../react-development/SKILL.md) | Implement Stitch screens as React code |
| [frontend-design](../frontend-design/SKILL.md) | Design system and UI principles |
| [canvas-design](../canvas-design/SKILL.md) | Design philosophy and visual aesthetics |
