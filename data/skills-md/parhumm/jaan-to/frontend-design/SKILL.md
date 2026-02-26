---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with bold design choices and working code. Use when designing UI components.
allowed-tools: Read, Glob, Grep, Write($JAAN_OUTPUTS_DIR/frontend/**), Task, WebSearch, AskUserQuestion, Edit(jaan-to/config/settings.yaml)
argument-hint: [component-description-or-requirements]
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Requires jaan-init setup.
---

# frontend-design

> Create distinctive, production-grade frontend interfaces.

## Context Files

- `$JAAN_CONTEXT_DIR/tech.md` - Tech stack context (optional, auto-imported if exists)
  - Uses sections: `#current-stack`, `#frameworks`, `#constraints`
- `$JAAN_CONTEXT_DIR/design.md` - Design system guidelines (optional)
- `$JAAN_CONTEXT_DIR/brand.md` - Brand guidelines (optional)
- `$JAAN_TEMPLATES_DIR/jaan-to-frontend-design.template.md` - Output template
- `$JAAN_LEARN_DIR/jaan-to-frontend-design.learn.md` - Past lessons (loaded in Pre-Execution)
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol

## Input

**Component Request**: $ARGUMENTS

Accepts any of:
- **Component description** — "Create a hero section for SaaS landing page"
- **Detailed requirements** — "Build a pricing card component with 3 tiers, hover effects, CTA buttons"
- **PRD reference** — Path to PRD file with frontend requirements
- **Empty** — Start interactive wizard

If no input provided, ask: "What component should I design and build?"

---

## Pre-Execution Protocol
**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `frontend-design`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)

Also read context files if available:
- `$JAAN_CONTEXT_DIR/tech.md` - Know the tech stack for framework-specific code generation
- `$JAAN_CONTEXT_DIR/design.md` - Know the design system patterns
- `$JAAN_CONTEXT_DIR/brand.md` - Know brand colors, fonts, tone

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_frontend-design`

> **Language exception**: Generated code output (variable names, code blocks, schemas, SQL, API specs) is NOT affected by this setting and remains in the project's programming language.

---

# PHASE 1: Analysis (Read-Only)

## Thinking Mode

ultrathink

Use extended reasoning for:
- Analyzing component requirements and purpose
- Planning bold design approaches
- Considering accessibility and responsive patterns
- Balancing creativity with usability
- Architecting component structure

## Step 1: Parse Component Request

Analyze the provided input to extract:

**Build initial understanding:**
```
COMPONENT REQUEST
─────────────────
Type:         {hero/card/form/modal/button/etc}
Purpose:      {what it does}
Context:      {where it's used}
Constraints:  {technical or design constraints}
Unknown:      {areas needing clarification}
```

**If PRD reference:**
1. Read the PRD file
2. Extract frontend-relevant requirements
3. Identify component needs from user stories
4. Note technical constraints mentioned

## Step 2: Detect Tech Stack

Read `$JAAN_CONTEXT_DIR/tech.md` if available:

1. Extract frontend framework from `#current-stack` or `#frameworks` sections
2. Determine: React, Vue, Svelte, vanilla JS, etc.
3. Note framework version for API compatibility
4. Identify styling approach from tech.md:
   - Tailwind CSS, CSS Modules, styled-components, Sass, vanilla CSS, etc.

**If tech.md missing or incomplete:**
- Ask: "Which framework? (React/Vue/Svelte/Vanilla JS)"
- Ask: "Styling approach? (Tailwind/CSS Modules/styled-components/vanilla CSS)"

## Step 3: Gather Design Requirements

Ask up to 7 smart questions based on what's unclear from Steps 1-2. Skip questions already answered by the input or context files.

### Design Direction (check settings first)

1. **Check settings.yaml** (if exists at `jaan-to/config/settings.yaml`):
   - Look for: `design.default_direction`, `design.palette`, `design.typography`
   - If found, use as baseline

2. **Ask user to fill gaps or override** (use AskUserQuestion):
   - Question: "What design direction should this take?"
   - Header: "Design Direction"
   - Options:
     - "Bold & Distinctive" — Modern, opinionated, memorable (recommended)
     - "Professional & Clean" — Conservative, trustworthy, subtle
     - "Playful & Creative" — Expressive, fun, unconventional
     - "Minimal & Elegant" — Refined, spacious, sophisticated
     - "Keep Settings Default" — (if settings exist)

3. **Infer from context** (if still unclear after above):
   - Landing page hero → Bold & Distinctive
   - Dashboard widget → Professional & Clean
   - Marketing page → Playful & Creative
   - Admin form → Minimal & Elegant

### Additional Questions (as needed)

4. "Any specific colors, typography, or brand elements to incorporate?" — only if not in brand.md
5. "Any accessibility requirements? (WCAG level, screen reader support)" — only if unclear
6. "Responsive breakpoints needed? (mobile-first assumed)" — only if special requirements
7. "Dark mode support needed?" — only if not specified in design.md

## Step 4: Design System Check

Check for existing patterns to maintain consistency:

1. **Glob** for `$JAAN_OUTPUTS_DIR/frontend/design/*` to see existing components
2. **Read** `$JAAN_CONTEXT_DIR/design.md` (if exists) for:
   - Color palette and usage guidelines
   - Typography scale and hierarchy
   - Spacing system (e.g., 4px, 8px grid)
   - Component patterns and conventions
   - Motion/animation guidelines
3. **Grep** for similar component patterns (buttons, cards, forms) in codebase

**Decision:**
- If patterns exist → Note them for consistency
- If no patterns → Create opinionated defaults that establish new standards

## Step 5: Plan Component Structure

Based on requirements, tech stack, and design direction, outline the component:

**For React:**
- Component structure (functional component with hooks)
- Props interface (TypeScript if project uses it)
- State management (if needed - useState, useReducer)
- Styling approach (based on tech.md)
- Accessibility attributes (ARIA labels, roles, keyboard handlers)

**For Vue:**
- Single File Component structure
- Props definition with TypeScript (if applicable)
- Composition API or Options API (based on project version)
- Scoped styles
- Accessibility attributes

**For Vanilla JS/HTML:**
- Semantic HTML structure
- Progressive enhancement approach
- CSS organization (BEM methodology, utility classes, or custom properties)
- Minimal JS (if needed for interactivity)

**Design Elements to Plan:**
- **Layout system**: Grid, Flexbox, Container Queries
- **Typography hierarchy**: Display, heading, body, caption levels
- **Color usage**: Primary, accent, neutral, semantic (success/error/warning)
- **Interactive states**: hover, focus, active, disabled, loading, error
- **Micro-interactions**: transitions, animations, scroll-triggered effects
- **Responsive behavior**: mobile-first breakpoints (e.g., 640px, 1024px, 1280px)

**Present component plan:**
```
COMPONENT DESIGN PLAN
─────────────────────
Name:         {ComponentName}
Framework:    {React/Vue/Vanilla}
Type:         {hero/card/form/etc}
Styling:      {Tailwind/CSS Modules/etc}
Scope:        Component + Preview (default)

Key Features:
- {feature_1}
- {feature_2}
- {feature_3}

Design Choices:
- Layout: {grid/flex/hybrid with rationale}
- Typography: {font families, scale, hierarchy}
- Colors: {palette with purpose and meaning}
- Motion: {animation approach and timing}
- Responsive: {breakpoint strategy and behavior}

Accessibility:
- ARIA labels: {yes/no, which ones}
- Keyboard nav: {tab order, focus management}
- Screen reader: {SR-only text, descriptions}
- Color contrast: {WCAG AA/AAA ratios}

Differentiation:
- What makes this distinctive: {unique design choice}
- How it avoids AI slop: {specific anti-patterns avoided}
```

---

# HARD STOP — Review Design Plan

Present complete design summary to user.

Use AskUserQuestion:
- Question: "Proceed with generating the component code?"
- Header: "Generate Component"
- Options:
  - "Yes" — Generate the component
  - "No" — Cancel
  - "Edit" — Let me revise the design direction first

**Do NOT proceed to Phase 2 without explicit approval.**

---

# PHASE 2: Generation (Write Phase)

## Step 6: Generate Component Code

Create production-grade, framework-specific component code:

### For All Frameworks:

1. **Semantic structure** — Use proper HTML5 elements (header, section, article, nav, button, etc.)
2. **Accessibility** — ARIA attributes, roles, keyboard handlers, focus management
3. **Modern CSS** — Grid, Custom Properties, Container Queries, modern selectors
4. **Bold design** — Distinctive typography, purposeful colors, unexpected layouts
5. **Responsive** — Mobile-first approach with fluid scaling
6. **Comments** — Inline documentation explaining non-obvious design choices

### React Example Structure:
```jsx
// Component with TypeScript props (if applicable)
// Clear prop documentation
// State management (if needed)
// Accessibility attributes
// Inline style comments explaining design choices
```

### Vue Example Structure:
```vue
<!-- Template with semantic HTML -->
<!-- Props with TypeScript (if applicable) -->
<!-- Scoped styles with design tokens -->
<!-- Accessibility attributes -->
```

### Vanilla HTML/CSS/JS Structure:
```html
<!-- Semantic HTML structure -->
<!-- Progressive enhancement -->
<!-- CSS with custom properties -->
<!-- Minimal JS for interactivity -->
```

### CSS Guidelines (All Frameworks):
- Use CSS custom properties for theming: `--color-primary`, `--spacing-unit`
- Modern features: `clamp()` for fluid typography, `min()`, `max()`
- Container queries for component-level responsiveness
- Smooth transitions: `transition: all 0.2s ease-in-out`
- Dark mode support (if needed): `@media (prefers-color-scheme: dark)`
- Reduced motion support: `@media (prefers-reduced-motion: reduce)`

### Design Differentiation:
- **Typography**: Avoid Inter, Roboto, Arial — choose distinctive fonts
- **Colors**: Avoid generic purple gradients — use purpose-driven palette
- **Layout**: Avoid predictable grid — try asymmetry, overlap, diagonal flow
- **Motion**: Avoid scattered micro-interactions — focus on high-impact moments

## Step 7: Generate Preview File

Create standalone HTML preview showing the component in action:

**Preview File Structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{ComponentName} Preview</title>
  <!-- Import framework (CDN) if React/Vue -->
  <!-- Import component styles -->
</head>
<body>
  <!-- Component demonstration -->
  <!-- Multiple states if applicable (default, hover, active, disabled, etc.) -->
  <!-- Responsive preview at different viewport widths -->
</body>
</html>
```

**Variants to show:**
- Default state
- Interactive states (hover, focus, active)
- Different props/configurations (if applicable)
- Error/loading states (if applicable)
- Dark mode (if supported)

## Step 8: Generate Documentation

Read template: `$JAAN_TEMPLATES_DIR/jaan-to-frontend-design.template.md`

Fill all sections:
- **Executive Summary**: 1-2 sentence overview (component type, framework, key design characteristic)
- **Overview**: Component metadata table
- **Design Rationale**: Why these aesthetic and technical choices? How does it avoid generic patterns?
- **Usage**: Installation, imports, basic example, props API
- **Code**: Reference to code file with key highlights
- **Accessibility**: WCAG compliance details, keyboard nav, screen reader support
- **Responsive Behavior**: Breakpoint behavior table
- **Customization**: CSS variables for theming
- **Metadata**: Generated date, skill version, output path

## Step 9: Quality Check

Before preview, verify all items:

- [ ] Code is syntactically valid (no syntax errors)
- [ ] Semantic HTML used (proper elements, not div soup)
- [ ] Accessibility attributes present (ARIA labels, roles, keyboard handlers)
- [ ] Responsive design implemented (mobile-first, fluid scaling)
- [ ] Design choices are bold and distinctive (not generic)
- [ ] Color contrast meets WCAG AA (4.5:1 for text, 3:1 for UI elements)
- [ ] Focus indicators visible (not `outline: none` without replacement)
- [ ] Inline comments explain non-obvious choices
- [ ] No hardcoded values that should be design tokens
- [ ] Documentation is complete with all required sections

If any check fails, fix before proceeding.

## Step 10: Preview & Approval

Show complete output to user:
- Component code (first 50 lines or full if short)
- Key design choices highlighted
- Documentation structure
- Preview file path

Use AskUserQuestion:
- Question: "Write component files to output?"
- Header: "Write Files"
- Options:
  - "Yes" — Write the files
  - "No" — Cancel
  - "Refine" — Make adjustments first

## Step 10.5: Generate ID and Folder Structure

```bash
# Source ID generator utility
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/id-generator.sh"

# Define subdomain directory
SUBDOMAIN_DIR="$JAAN_OUTPUTS_DIR/frontend/design"
mkdir -p "$SUBDOMAIN_DIR"

# Generate next sequential ID
NEXT_ID=$(generate_next_id "$SUBDOMAIN_DIR")

# Create slug from component name (lowercase-kebab-case, max 50 chars)
slug="{component-name-slug}"

# Generate paths
OUTPUT_FOLDER="${SUBDOMAIN_DIR}/${NEXT_ID}-${slug}"
MAIN_FILE="${OUTPUT_FOLDER}/${NEXT_ID}-${slug}.md"
CODE_FILE="${OUTPUT_FOLDER}/${NEXT_ID}-${slug}-code.{jsx|vue|html}"
PREVIEW_FILE="${OUTPUT_FOLDER}/${NEXT_ID}-${slug}-preview.html"
```

**Preview output configuration:**
> **Output Configuration**
> - ID: {NEXT_ID}
> - Folder: $JAAN_OUTPUTS_DIR/frontend/design/{NEXT_ID}-{slug}/
> - Files:
>   - {NEXT_ID}-{slug}.md (documentation)
>   - {NEXT_ID}-{slug}-code.{ext} (code)
>   - {NEXT_ID}-{slug}-preview.html (preview)

## Step 11: Write Output

1. **Create output folder:**
   ```bash
   mkdir -p "$OUTPUT_FOLDER"
   ```

2. **Write documentation file:**
   Write filled template to `$MAIN_FILE`

3. **Write component code file:**
   Write generated code to `$CODE_FILE`

4. **Write preview file:**
   Write standalone preview to `$PREVIEW_FILE`

5. **Update subdomain index:**
   ```bash
   source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/index-updater.sh"
   add_to_index \
     "$SUBDOMAIN_DIR/README.md" \
     "$NEXT_ID" \
     "${NEXT_ID}-${slug}" \
     "{ComponentName}" \
     "{Executive summary — 1-2 sentences}"
   ```

6. **Confirm to user:**
   > ✓ Component written to: $JAAN_OUTPUTS_DIR/frontend/design/{NEXT_ID}-{slug}/
   > ✓ Files created:
   >   - {NEXT_ID}-{slug}.md
   >   - {NEXT_ID}-{slug}-code.{ext}
   >   - {NEXT_ID}-{slug}-preview.html
   > ✓ Index updated: $JAAN_OUTPUTS_DIR/frontend/design/README.md

## Step 12: Suggest Next Actions

Present follow-up workflow options:

> **Component generated successfully!**
>
> **Next Steps:**
> - Copy code from `{CODE_FILE}` to your project
> - Open `{PREVIEW_FILE}` in browser to see live preview
> - Run `/jaan-to:qa-test-cases "{MAIN_FILE}"` to generate test cases
> - Run `/jaan-to:frontend-task-breakdown` if you need integration tasks for larger feature

## Step 13: Capture Feedback

Use AskUserQuestion:
- Question: "How did the component turn out?"
- Header: "Feedback"
- Options:
  - "Perfect!" — Done
  - "Needs fixes" — What should I improve?
  - "Learn from this" — Capture a lesson for future runs

If "Learn from this":
- Run `/jaan-to:learn-add frontend-design "{feedback}"`

---

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Framework-agnostic with `tech.md` detection
- Template-driven output structure
- Output to standardized `$JAAN_OUTPUTS_DIR` path

## Definition of Done

- [ ] Valid, working code generated
- [ ] Bold design choices implemented and documented
- [ ] WCAG AA accessibility met
- [ ] Responsive design (mobile-first) implemented
- [ ] Framework matches tech.md (or user choice)
- [ ] Documentation complete with all required sections
- [ ] Preview file works (if scope includes preview)
- [ ] Output follows v3.0.0 structure (ID, folder, index)
- [ ] Index updated with executive summary
- [ ] User approved final result
