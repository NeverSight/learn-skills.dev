---
name: pixel-perfect-ui
description: "Autonomous pixel-perfect UI implementation loop for Next.js/React using Figma MCP and Playwright. Converts Figma designs to production-ready components with iterative visual validation. **AUTO-TRIGGERS** on ANY request to implement Figma designs including: 'implement this Figma', 'build this page/component from Figma', 'create from Figma design', 'implement design', 'build this block', 'create component from design'. Use for: (1) Building pages/components from Figma, (2) Pixel-perfect accuracy, (3) Responsive layouts, (4) Design token conversion."
---

# Pixel-Perfect UI Implementation

Autonomous workflow for converting Figma designs to **production-ready**, pixel-perfect React/Next.js implementations with visual validation.

## 🚀 AUTO-TRIGGER CONDITIONS

This skill **MUST be invoked automatically** when the user requests ANY of:
- "implement this Figma design"
- "build this page/component from Figma"
- "create from Figma"
- "implement the design"
- "build this block/section"
- "create component matching design"
- Any request involving Figma URL or node ID
- Any request to implement a page, block, or component from a design

## Prerequisites

- Figma MCP server connected (for design extraction)
- Playwright MCP server connected (for visual validation)  
- Next.js or React project initialized

---

## 📋 PHASE 0: MANDATORY CHECKLIST CREATION (ALWAYS FIRST)

**CRITICAL**: Before ANY implementation, you MUST:

### Step 0.1: Analyze Design & Identify Sections

First, get the full page/component from Figma and identify ALL sections:
```bash
mcp0_get_design_context --nodeId <page-node-id>
mcp0_get_metadata --nodeId <page-node-id>
```

List all sections/blocks in the design (e.g., Header, Hero, Features, CTA, Footer).

### Step 0.2: Create Implementation Checklist File

Create a markdown checklist file at `.windsurf/implementation-checklist.md`:

```markdown
# Implementation Checklist: [Component/Page Name]

**Created**: [Date]
**Figma Source**: [URL or Node ID]
**Target Path**: [e.g., src/app/page.tsx or src/components/MyComponent.tsx]
**Status**: 🟡 Pending Approval

---

## 📋 Sections to Implement

[List each section identified from Figma]

1. **Section Name 1** (node-id: xxx)
2. **Section Name 2** (node-id: xxx)
3. **Section Name 3** (node-id: xxx)
...

---

## 🔄 SECTION-BY-SECTION IMPLEMENTATION

> ⚠️ **CRITICAL RULE**: For EACH section below:
> 1. First EXTRACT fresh Figma data for that specific section
> 2. Then IMPLEMENT based on that fresh extraction
> 3. Mark section complete
> 4. Move to next section
> 
> **NEVER rely on old/cached Figma data. Always re-extract before implementing!**

---

### Section 1: [Section Name]
**Node ID**: [figma-node-id]
**Status**: ⬜ Not Started

#### 1.1 Extract from Figma
- [ ] mcp0_get_design_context for this section
- [ ] mcp0_get_screenshot for visual reference
- [ ] Export any images/assets needed
- [ ] Note typography, colors, spacing

#### 1.2 Implement
- [ ] Create/update component structure
- [ ] Implement desktop layout (1440px)
- [ ] Implement tablet layout (768px)
- [ ] Implement mobile layout (375px)
- [ ] Add images with Next.js Image
- [ ] Apply styles (typography, colors, spacing)

#### 1.3 Validate
- [ ] Visual check matches Figma
- [ ] Responsive on all viewports
- [ ] No horizontal scroll

✅ **Section 1 Complete**: [ ]

---

### Section 2: [Section Name]
**Node ID**: [figma-node-id]
**Status**: ⬜ Not Started

#### 2.1 Extract from Figma
- [ ] mcp0_get_design_context for this section
- [ ] mcp0_get_screenshot for visual reference
- [ ] Export any images/assets needed
- [ ] Note typography, colors, spacing

#### 2.2 Implement
- [ ] Create/update component structure
- [ ] Implement desktop layout (1440px)
- [ ] Implement tablet layout (768px)
- [ ] Implement mobile layout (375px)
- [ ] Add images with Next.js Image
- [ ] Apply styles (typography, colors, spacing)

#### 2.3 Validate
- [ ] Visual check matches Figma
- [ ] Responsive on all viewports
- [ ] No horizontal scroll

✅ **Section 2 Complete**: [ ]

---

[Repeat for each section...]

---

## 🏁 Final Validation

- [ ] All sections implemented
- [ ] Full page visual comparison
- [ ] Resource validation passed (no broken links/images)
- [ ] Production checklist complete

---

## 📝 Notes

[Add any specific notes here]

---

## ✅ Completion Summary

**Completed**: [Date when finished]
**Final Status**: [Pending/Complete]
```

### Step 0.3: Present Plan to User

After creating the checklist, **ALWAYS**:

1. **Display the plan** to the user in chat (show all identified sections)
2. **Ask for confirmation**: "I've created the implementation checklist at `.windsurf/implementation-checklist.md` with X sections. Should I proceed?"
3. **WAIT for user approval** before proceeding

### Step 0.4: Execute Section-by-Section

**FOR EACH SECTION** (in order):

```
┌─────────────────────────────────────────────────────┐
│  SECTION WORKFLOW (repeat for each section)         │
├─────────────────────────────────────────────────────┤
│  1. 📥 EXTRACT: Get fresh Figma data for section    │
│     - mcp0_get_design_context --nodeId <section-id> │
│     - mcp0_get_screenshot --nodeId <section-id>     │
│     - Export images if needed                       │
│                                                     │
│  2. 🔨 IMPLEMENT: Build based on fresh extraction   │
│     - Use the data you JUST extracted               │
│     - Do NOT use old/cached data                    │
│     - Implement responsive (desktop→tablet→mobile)  │
│                                                     │
│  3. ✅ VALIDATE: Check section matches Figma        │
│                                                     │
│  4. 📝 UPDATE CHECKLIST: Mark items [x] complete    │
│                                                     │
│  5. ➡️ MOVE TO NEXT SECTION                         │
└─────────────────────────────────────────────────────┘
```

**CRITICAL**: 
- Do NOT batch extract all sections at once
- Do NOT implement from memory or old data
- ALWAYS re-extract Figma data immediately before implementing each section
- Update checklist after completing each section

### Step 0.5: Track Progress

As you complete each section:
1. **Update the checklist file** - Change `- [ ]` to `- [x]` for completed items
2. **Update section status**: ⬜ Not Started → 🔵 In Progress → ✅ Complete
3. **Update overall Status** field:
   - 🟡 Pending Approval
   - 🔵 In Progress - Section X of Y
   - 🟢 Complete
   - 🔴 Blocked (with reason)

---

## 🚨 CRITICAL PRODUCTION RULES

### Mobile-First Responsive Design (MANDATORY)
- **NEVER use hardcoded pixel widths** (e.g., `w-[1728px]`, `width: 1728px`)
- **ALWAYS use responsive units**: `max-w-7xl`, percentages, or viewport units
- **ALWAYS test on mobile viewports** (375px, 768px, 1024px, 1440px)
- **NO horizontal scroll** - Use `overflow-x-hidden` on body if needed
- **Container pattern**: Use `max-w-[size] mx-auto px-4 sm:px-6 lg:px-8`

### Image Requirements (MANDATORY)
- **EXPORT all images from Figma** - Never use placeholder paths
- **CHECK image existence** before referencing
- **USE Next.js Image component** with proper dimensions
- **PROVIDE fallbacks** for missing images
- **OPTIMIZE images** - WebP format preferred

### Production Checklist (MUST COMPLETE)
- [ ] All viewports tested (mobile, tablet, desktop)
- [ ] No horizontal scroll on any device
- [ ] All images exported and accessible
- [ ] Touch targets minimum 44x44px on mobile
- [ ] Text readable without zooming
- [ ] Interactive elements have hover/focus states
- [ ] Loading states implemented
- [ ] Error boundaries added
- [ ] **Resource validation passed** (no broken links/images)

## Core Workflow

> ⚠️ **REMINDER**: Always complete Phase 0 (Checklist Creation) before starting these steps!

### 1. Design Extraction

Extract comprehensive design data from Figma:

```bash
# Get design context and code
mcp0_get_design_context --nodeId <node-id>
mcp0_get_variable_defs --nodeId <node-id>
mcp0_get_screenshot --nodeId <node-id>
```

Parse extracted data for:
- Typography (font-family, size, weight, line-height, letter-spacing)
- Colors (hex values, opacity)
- Spacing (padding, margin, gap)
- Layout (flexbox/grid properties, alignment)
- Borders, shadows, radius values
- Asset URLs and SVG exports

### 2. Project Analysis

Detect project configuration:
- Framework: Next.js App Router vs Pages Router
- Styling: Tailwind, CSS Modules, styled-components
- Component library: shadcn/ui, MUI, Radix
- Design tokens location: tailwind.config, theme.ts

Map Figma tokens to existing project tokens.

### 3. Implementation

Generate component with extracted values:

```typescript
// For complex layouts, use references/layout-patterns.md
// For component patterns, use references/component-patterns.md
// For responsive patterns, use references/responsive-patterns.md
```

**STRICT Implementation Rules**:
- ❌ **FORBIDDEN**: Hardcoded widths like `w-[1728px]`, `width: 1728px`
- ✅ **REQUIRED**: Responsive containers `max-w-7xl mx-auto px-4`
- ✅ **REQUIRED**: Mobile-first breakpoints `sm:`, `md:`, `lg:`, `xl:`
- ✅ **REQUIRED**: Export and validate all images from Figma
- ✅ **REQUIRED**: Flexible layouts using Flexbox/Grid
- ✅ **REQUIRED**: Test on 375px, 768px, 1024px, 1440px viewports

**Image Handling**:
```typescript
// 1. Export from Figma
mcp0_get_screenshot --nodeId <id> --filename "hero-image.png"

// 2. Save to public/assets/
// 3. Use with Next Image
<Image src="/assets/hero-image.png" alt="..." width={...} height={...} />
```

### 4. Multi-Device Validation Loop

**Mandatory**: Run validation on ALL viewports:

```bash
# Desktop validation
python scripts/visual-compare.py --viewport 1440x900

# Tablet validation  
python scripts/visual-compare.py --viewport 768x1024

# Mobile validation (CRITICAL)
python scripts/visual-compare.py --viewport 375x667

# Responsive issues check
python scripts/responsive-validation.py --url <url>

# Resource validation (CRITICAL - Run before deployment)
python scripts/resource-validator.py --directory src/app --strict
```

**Validation Requirements**:
- ✅ No horizontal scroll on any viewport
- ✅ All images loading correctly (verified by resource-validator.py)
- ✅ No broken links or missing resources
- ✅ No placeholder content (lorem ipsum, temp images)
- ✅ Touch targets ≥ 44x44px on mobile
- ✅ Text legible without zooming
- ✅ Proper stacking on mobile (no overlaps)
- ✅ Interactive elements accessible

**Common Failures to Fix**:
- ❌ Hardcoded widths causing overflow
- ❌ Missing or broken images (detected by resource-validator.py)
- ❌ Broken internal/external links
- ❌ Placeholder content (lorem ipsum, temp images)
- ❌ External dependencies not cached locally
- ❌ Text too small on mobile (<14px)
- ❌ Elements overlapping on small screens
- ❌ Fixed positioning breaking on mobile

### 5. Responsive Implementation

Extract breakpoint variations from Figma:
- Desktop (1440px)
- Tablet (768px)
- Mobile (375px)

Apply responsive rules using project's breakpoint system.

## Quick Commands

### Full page implementation:
```bash
python scripts/extract-and-implement.py --figma-url <url> --output-path <path>
```

### Component extraction:
```bash
python scripts/extract-component.py --node-id <id> --component-name <name>
```

### Visual validation:
```bash
python scripts/visual-compare.py --implementation-url <url> --figma-node <id>
```

### Resource validation (broken links, missing images):
```bash
# Validate single file
python scripts/resource-validator.py --file src/app/page.tsx

# Validate entire app (REQUIRED before production)
python scripts/resource-validator.py --directory src/app --strict --report validation-report.txt
```

## File Organization

- **Pages**: Follow project routing convention
  - App Router: `app/[route]/page.tsx`
  - Pages Router: `pages/[route].tsx`
- **Components**: `components/ui/[component].tsx`
- **Assets**: `public/assets/` or `src/assets/`
- **Styles**: Co-located or in `styles/`

## Token Mapping

See `references/token-mapping.md` for:
- Figma → Tailwind mapping
- Figma → CSS variables mapping
- Shadow and gradient conversion
- Typography scale mapping

## Component Patterns

See `references/component-patterns.md` for:
- Card layouts
- Navigation patterns
- Form components
- Modal implementations
- Grid systems

## Validation Thresholds

Acceptable differences:
- Font kerning: ±2px
- Line height: ±1px
- Anti-aliasing variations

Must match exactly:
- Colors (hex values)
- Border radius
- Spacing values
- Component dimensions
- Shadow properties
