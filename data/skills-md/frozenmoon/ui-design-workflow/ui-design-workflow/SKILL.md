---
name: ui-design-workflow
description: >
  MUST use when implementing UI components or frontend pages in this project.
  Triggers: designing UI, implement page, develop UI, write component, frontend development,
  create component, build interface, style page,
  button, form, modal, toast, card, input, styling, interface,
  shadcn, ant design, antd, element plus, component library, UI library,
  设计UI, 实现页面, 开发UI, 写组件, 前端开发, 创建组件, 构建界面, 页面样式,
  按钮, 表单, 弹窗, 提示, 卡片, 输入框, 样式, 界面, 组件库, UI组件,
  设计规范, 生成规范, 实现功能, 检查代码, 迭代规范, 切换组件库.
  Before writing any UI code, load this skill to read the project's design spec.
---

# UI Design Workflow

Manage the full UI design workflow: Demo → Spec → Implement → Check → Iterate.
Supports both custom components and component libraries (shadcn/ui, Ant Design, Element Plus, etc.).

## Command Reference

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `demo` | Analyze project + generate UI showcase | Early stage: establish style & component solution |
| `spec` | Generate spec document | After Demo is confirmed |
| `implement` | Build features per spec | Daily development |
| `check` | Audit spec compliance | Before PR, periodic review |
| `iterate` | Update the spec | When gaps are discovered |

---

## Command Details

### demo - Generate UI Components + Showcase Page

**Input**: User's UI style requirements (e.g., "minimal modern", "techy")

**Output**:
- **Real component files** in `src/components/ui/` (reusable across the project)
- **Two showcase pages** (separate pages, NOT tabs):
  - **Landing Page Demo** (`/ui-showcase`) - Complete product page built with the real components
  - **Component Library** (`/ui-components`) - All components rendered in various states, independently iterable

**Flow selection** (auto-detect):
- Project has existing spec → **Flow B** (import existing components, generate demo)
- User specified a library → **Flow C** (use specified library, still confirm style)
- Project has significant existing UI (5+ components or 3+ pages) but no spec → **Flow D** (extract and document, see below)
- Otherwise → **Flow A** (from scratch)

**Flow D: Adopt Existing UI** (for projects with existing UI code but no spec):
1. **Deep scan**: Extract design tokens (colors, fonts, spacing, radius, shadows) and component inventory from existing code
2. **Present extraction results**: Show findings to user via `AskUserQuestion` for confirmation
3. **Gap analysis**: Identify missing tokens, inconsistent values, missing components
4. **User decides**: Fix gaps now or defer to `iterate`
5. **Generate spec**: `doc/ui-design-spec.md` based on extracted data (not invented)
6. **Optional showcase**: Ask if user wants a showcase page for existing components
7. **Update agent config**: Write spec reference to CLAUDE.md / AGENTS.md
- See [references/modes.md](references/modes.md) for detailed steps.

**Flow A (from scratch):**
1. **Project Analysis**:
   - Read `package.json` to identify framework and existing dependencies
   - Scan code directory to identify existing patterns and tech stack
   - Determine project type (landing page, admin panel, SaaS, e-commerce, etc.)
   - **Scan existing components**: Find all components in the project, assess their consistency
2. **Present findings and auto-select component solution**:
   - Show existing component inventory and consistency assessment to user
   - Auto-select a component solution based on analysis (custom / shadcn/ui / Ant Design / other)
   - Auto-detect existing library dependencies and continue with them
   - If user already specified a library in the command, use it directly
   - **Do NOT ask the user to choose** — use the recommended solution by default. Advanced users will override if needed.
3. **⛔ Visual Style Preview (BLOCKING)** — Generate `style-preview.html` (standalone HTML, opens in any browser) with 3 diverse style direction previews. Each preview shows real fonts (Google Fonts), actual color palette, a mini Hero section, and atmosphere effects. User opens in browser, picks A/B/C, asks for a new batch, or describes their own direction. Then ask theme mode (light/dark/toggle). **DO NOT proceed without user's confirmed choice.** See [assets/style-preview-template.md](assets/style-preview-template.md) for the HTML template.
4. **Design Thinking** (read [references/frontend-aesthetics.md](references/frontend-aesthetics.md)):
   - Refine the user's chosen style direction into detailed design tokens
   - Define the memorable element — what makes this design unforgettable?
   - Finalize typography, color palette, atmospheric details — all coherent with the confirmed visual preview
5. **Create real component files** (the single source of truth):
   - Set up design tokens as CSS variables
   - Create each component as a real file in `src/components/ui/`
   - Components support all variants, states, transitions, and accessibility
   - Skip components that already exist in the project
6. **Create two showcase pages** (separate pages, NOT tabs):
   - **Landing Page Demo** (`/ui-showcase`): Product page built with real components.
   - **Component Library** (`/ui-components`): All components in every variant/state.
   - Both pages share a **navigation bar** with links to each other.
   - **Include existing project components** in Component Library page (do not modify them)
   - **Apply motion**: Orchestrate page load animations with staggered reveals
   - **Apply atmosphere**: Add background textures, gradients, or visual depth
7. **Run anti-AI-slop checklist** (see [references/frontend-aesthetics.md](references/frontend-aesthetics.md))
8. Iterate with user

**Existing component handling**:
- Preserve existing components as-is; do not modify during demo phase
- Only suggest fixes for severe issues (accessibility violations, broken layouts)
- Minor inconsistencies are noted for future `iterate` updates

**Output locations**:
- Components: `src/components/ui/*.tsx`
- Landing Page Demo (Next.js): `app/ui-showcase/page.tsx` | (Vite): `src/pages/UIShowcase.tsx`
- Component Library (Next.js): `app/ui-components/page.tsx` | (Vite): `src/pages/UIComponents.tsx`

**Templates**: See [assets/website.md](assets/website.md) and [assets/components.md](assets/components.md)
**Library guide**: See [assets/library-guide.md](assets/library-guide.md)

---

### spec - Generate Spec Document

**Prerequisite**: Confirmed Demo exists (component files + showcase page)

**Output**:
1. Spec document: `doc/ui-design-spec.md` (includes Component Registry)
2. Project integration: Update CLAUDE.md with spec reference

**Flow**:
1. Read component files and showcase code, extract design decisions
2. **Build Component Registry**: Scan all component files, record name → path → variants → states
3. **Record component solution**: Document the chosen solution in the spec
   - Solution type (custom / library name)
   - Library version (if applicable)
   - Theme configuration method and file path
4. Generate structured spec document (design tokens + registry, NOT code examples)
5. Update CLAUDE.md with spec reference

---

### implement - Build Features Per Spec

**Prerequisite**: Project has a UI spec with Component Registry

**Flow**:
1. **Must** read the project's UI spec document first
2. **Check Component Registry**: Find existing components that can be reused
   - If a needed component exists → read its source file, import and use it
   - If a needed component does NOT exist → create it following the spec's design tokens, then notify user to run `iterate` to register it
3. Implement the user's requested feature per spec
4. Ensure colors, spacing, and component styles comply with the spec

**Key**: Always check the Component Registry before creating any UI element. Reuse existing components — do not duplicate.

---

### check - Audit Spec Compliance

**Input**: File or directory to check

**Flow**:
1. Read the project's UI spec (including Component Registry)
2. Scan the specified code
3. Check for:
   - **Component reuse**: Are registry components being imported and used, or duplicated inline?
   - **Design tokens**: Are CSS variables used instead of hardcoded values?
   - **Spacing/radius**: Do values conform to the spec's grid system?
   - **Library compliance** (if applicable): Are library components used correctly?
4. Output violation report with component reuse rate

---

### iterate - Update the Spec

**Trigger**: New component created during `implement`, missing registry entry, design token change, or switching component solution

**Flow**:
1. Confirm with user what needs to be added/modified
2. If adding a new component: verify the file exists, add to Component Registry, add to showcase
3. If switching component solution, flag components that need migration
4. Update spec document (registry / tokens)
5. Update Demo showcase page (if needed)
6. Sync related implementation code (if needed)

---

## Design Principles (General)

> **Full details**: [assets/design-principles.md](assets/design-principles.md) — Must read before demo phase.
> **Aesthetics guide**: [references/frontend-aesthetics.md](references/frontend-aesthetics.md) — Core creative reference for all design work.

### Intentional Design (Core Principle)
- Every design must have a clear aesthetic direction and point of view
- Choose a bold tone: brutally minimal, luxury refined, editorial, organic, retro-futuristic, etc.
- Define the memorable element — the ONE thing someone will remember
- **NEVER produce generic AI aesthetics**: no Inter/Roboto fonts, no purple-on-white gradients, no cookie-cutter layouts

### Less is More (Token Principle)
- Default to the minimum viable set of design tokens
- Fewer named levels: border-radius 3, spacing 4, shadows 3, font weights 2
- Minimal tokens ≠ minimal aesthetics — a small set of well-chosen tokens creates more cohesion

### Component Solution
- **Custom components**: Hand-write all UI components, full control
- **Component library**: Use an existing library (shadcn/ui, Ant Design, Element Plus, etc.)
- Choice is made during demo stage, recorded in the spec document
- All subsequent stages automatically follow this choice

### Typography
- Choose **distinctive, characterful fonts** — never generic defaults
- Pair a display/heading font with a refined body font for contrast
- Vary font choices across different projects — never converge on the same "safe" pick
- Clear type scale hierarchy (Display → H1 → H2 → Body → Small)

### Color System
- **Dominant + accent model**: One dominant color for mood, sharp accents for focal points
- Build palettes that evoke an emotion — if you can't name the feeling, it's too generic
- **Avoid**: purple-blue gradients, teal/coral combos, unmodified Tailwind gray scales
- **System feedback**: Success, Error, Warning, Info

### Motion & Atmosphere
- Orchestrate page load with staggered reveals (highest impact)
- Add scroll-triggered reveals, surprising hover states
- Create atmospheric depth: gradient meshes, noise textures, radial highlights
- Avoid: solid white/dark backgrounds with no visual interest

### Responsive
- Mobile-first design
- Key breakpoints: sm(640px), md(768px), lg(1024px)

---

## File Structure

```
ui-design-workflow/
├── SKILL.md              # This file (overview)
├── README.md             # User documentation
├── assets/
│   ├── website.md        # Landing page template structure
│   ├── components.md     # Component library template
│   ├── design-principles.md  # UI design principles (references aesthetics guide)
│   ├── spec-template.md  # Spec document template
│   └── library-guide.md  # Component library integration guide
└── references/
    ├── modes.md          # Detailed mode specifications
    └── frontend-aesthetics.md  # ⭐ Core creative aesthetics guide (anti-AI-slop)
```

---

## Quick Decision Guide

**User says "design UI"** → Use `demo` (analyze project, recommend component solution)
**User says "use shadcn/ui"** → Use `demo` (skip recommendation, use specified library)
**User says "generate spec"** → Use `spec`
**User says "implement feature"** → Use `implement` (read spec first, identify component solution)
**User says "check code"** → Use `check`
**User says "add component spec"** → Use `iterate`
**User says "switch to Ant Design"** → Use `iterate` (switch component solution)
