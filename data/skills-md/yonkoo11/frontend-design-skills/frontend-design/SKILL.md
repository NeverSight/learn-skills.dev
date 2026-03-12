---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces. Always generates 3 wildly different worldclass proposals with UX architecture. Use when building web components, pages, dashboards, or applications. Generates creative, polished code that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

# Frontend Design - Unified Design Skill

One skill for all design work. Always produces **3 worldclass proposals** with full UX architecture. No exceptions.

---

## Modes

```
/frontend-design              # Auto-detect mode
/frontend-design new          # Build new UI from scratch
/frontend-design revamp       # Total redesign (throw away existing)
/frontend-design polish       # Production polish pass (no proposals)
/frontend-design qa           # Quality gate check (no proposals)
/frontend-design flow         # UX architecture only (no visuals)
```

### Mode Detection

If no mode specified, detect from context:

| Signal | Mode |
|--------|------|
| No UI files exist | `new` |
| User says "redesign/revamp/redo/start over" | `revamp` |
| User says "polish/refine/improve/fix" | `polish` |
| User says "check/qa/review/audit/ready to ship" | `qa` |
| User says "flow/ux/screens/architecture" | `flow` |
| Ambiguous | Ask user |

---

## THE 3-PROPOSAL RULE (Mandatory for new/revamp)

Every `new` or `revamp` invocation MUST generate **exactly 3 proposals**. Not 1, not 2, not 4. Three. Each proposal must be:
- Structurally different (enforced by DNA system)
- Worldclass professional quality
- Self-contained HTML file with all CSS inline
- Include full UX architecture (flow, states, interactions)

---

## Execution Flow (new/revamp)

### Step 1: Understand Context

Before anything:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Constraints**: Framework, performance, accessibility requirements
- **Existing code**: Read current files if revamp mode

### Step 2: Define UX Architecture (for ALL 3 proposals)

Each proposal includes its own UX architecture:

```markdown
## UX Architecture

**Entry:** [where user starts]
**Exit:** [how user knows done]

**Screens:**
1. [Name] - [Purpose] - [Primary action]
2. [Name] - [Purpose] - [Primary action]

**Happy Path:** Entry > Screen 1 > Screen 2 > Exit

**States:**
- Empty: [what shows with no data]
- Loading: [what shows during fetch]
- Error: [what shows on failure + recovery]

**Kill-Switch Test:**
- Does this flow require explanation? → Simplify
- Could first-time user get stuck? → Add guidance
- Are there screens that exist "just in case"? → Remove
```

### Step 3: Auto-Assign DNA Codes

Read `reference/dna-system.md` and assign unique DNA codes to each proposal.

**Constraint:** No two proposals may share more than 2 DNA genes.

```
DNA Format: DNA-[Layout]-[Navigation]-[Hero]-[Color]-[Typography]

Example:
- Proposal 1: DNA-A-H-I-D-R (Asymmetric, Hidden, Immersive, Duotone, Retro)
- Proposal 2: DNA-B-T-S-V-S (Bento, Top-fixed, Split, Vibrant, Sans)
- Proposal 3: DNA-F-O-F-M-E (Full-bleed, Overlay, Full-viewport, Mono, Serif)
```

### Step 4: Load Constraints

1. Read `reference/banned-defaults.md` - These patterns are FORBIDDEN
2. Read `reference/inspirations.md` - Each proposal must cite at least one inspiration
3. Combine 2-3 inspirations from DIFFERENT categories per proposal

### Step 5: Generate 3 Proposals in Parallel

Launch 3 subagents simultaneously using the Task tool:

```javascript
// For each proposal N (1, 2, 3):
Task({
  subagent_type: "frontend-design",
  prompt: `
    ## Design Proposal ${N}

    **DNA Code:** ${assignedDNA}
    **Target:** ${projectName}
    **Inspiration:** ${citedInspirations}

    ### UX Architecture
    ${uxArchitecture}

    ### Constraints
    - FORBIDDEN patterns (from banned-defaults.md):
      ${bannedPatterns}
    - REQUIRED structural choices (from DNA):
      Layout: ${layoutChoice}
      Navigation: ${navChoice}
      Hero: ${heroChoice}
      Color: ${colorChoice}
      Typography: ${typoChoice}

    ### Hard Rules (48 non-negotiable rules apply - see below)

    ### Output
    Generate a complete, self-contained HTML file with:
    1. All CSS inline or embedded
    2. Responsive design (mobile-first)
    3. DNA badge in top-right corner
    4. Inspiration citation in footer
    5. Full UX architecture documented in HTML comments
    6. All states: loading, empty, error, success
    7. Accessibility: focus states, contrast, semantic HTML

    Save to: ./proposals/proposal-${N}.html
  `
})
```

### Step 6: Generate Catalogue

After all proposals complete, generate `./proposals/index.html` using the catalogue template from `reference/catalogue.html`.

### Step 7: Screenshot All Proposals

```javascript
// For each proposal:
mcp__puppeteer__puppeteer_navigate({ url: "file:///path/to/proposal-N.html" })
mcp__puppeteer__puppeteer_screenshot({ name: "proposal-N", width: 1280, height: 800 })
```

### Step 8: Present to User

```markdown
## 3 Design Proposals Generated

| # | DNA | Inspiration | UX Flow |
|---|-----|-------------|---------|
| 1 | DNA-A-H-I-D-R | Brutalist + Bloomberg | Entry > Dashboard > Detail > Action |
| 2 | DNA-B-T-S-V-S | Linear + Stripe | Entry > List > Detail > Action |
| 3 | DNA-F-O-F-M-E | Swiss + Afrofuturism | Entry > Browse > Configure > Confirm |

Browse catalogue: ./proposals/index.html

Next: Pick a winner (or combine elements), then I'll build production code.
```

---

## Design Thinking (for subagents)

Before coding, commit to a BOLD aesthetic direction:
- **Tone**: Pick an extreme - brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

### Frontend Aesthetics

- **Typography**: Choose distinctive fonts. NEVER use Arial, Inter, Roboto, system fonts, Poppins. Pair a distinctive display font with a refined body font.
- **Color**: Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Use CSS variables. 1 brand color + neutrals.
- **Motion**: Focus on high-impact moments: one well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions. Hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements.
- **Backgrounds**: Create atmosphere and depth. Gradient meshes, noise textures, geometric patterns, layered transparencies.

---

## No AI Slop (Zero Tolerance)

**Visual slop - remove on sight:**
- Emojis anywhere in production UI (use SVG icons)
- Gradient text (unless ONE hero element)
- Glassmorphism blur cards stacked on each other
- Neon glow effects on every element
- Decorative SVG blobs/waves that serve no purpose
- Hover animations on non-interactive elements

**Copy slop - rewrite:**
- Fake social proof without real data
- Marketing superlatives ("revolutionary", "cutting-edge")
- Filler text ("Welcome to our platform", "Get started today")
- "Powered by AI" badges

**Layout slop - restructure:**
- 3-column feature grids with icon + title + description
- Oversized hero with stock photo
- "How it works" numbered steps with arrows
- Footer with 4 columns of links to nonexistent pages

**Code slop - clean up:**
- `transition: all` (specify properties)
- Magic numbers (use tokens)
- `!important` overrides (fix specificity)

**The test:** Show the UI to someone. If they say "AI made this" - it has slop. Strip it back.

---

## Hard Rules (48 Non-Negotiable)

### Animation (1-9)

1. **Never linear easing** - Use `ease-out` or `cubic-bezier(0.22, 1, 0.36, 1)`
2. **Never scale from 0** - Minimum scale(0.93)
3. **Never animate keyboard actions** - CMD+K, search, tab switching = instant
4. **Never animate theme toggles** - Theme change is instant
5. **Never animate scroll position** - Let users control scroll
6. **Never exceed 300ms for functional UI** - <100ms instant, 100-300ms responsive
7. **No bounce on serious UI** - Undermines trust
8. **Only animate transform and opacity** - GPU-accelerated only. Never `transition: all`
9. **Always respect prefers-reduced-motion**

### Accessibility (10-21)

10. Contrast >= 4.5:1 for normal text
11. Contrast >= 3:1 for large text (18px+ bold or 24px+)
12. All interactive elements keyboard focusable
13. Focus indicators visible (box-shadow, not outline removal)
14. Color not sole indicator of state (pair with icon + text)
15. Touch targets >= 44x44px
16. Semantic HTML (`<button>` not `<div onclick>`)
17. Escape closes modals/dropdowns
18. Images have alt text
19. Icon-only buttons have aria-label
20. Form inputs have associated labels
21. Error messages associated with inputs via aria-describedby

### Input & Interaction (22-26)

22. Input font-size >= 16px (prevents iOS zoom)
23. Hover states only on hover-capable devices (`@media (hover: hover)`)
24. Disabled buttons have no tooltips, use cursor: not-allowed
25. No auto-focus on touch devices
26. Customize iOS tap highlight (`-webkit-tap-highlight-color: transparent`)

### Typography (27-30)

27. Apply font smoothing (antialiased)
28. Tabular numbers for data (`font-variant-numeric: tabular-nums`)
29. Max 3-4 font sizes per view
30. Line height 1.4-1.6 for body, 1.1-1.25 for headings

### Visual Design (31-37)

31. Max 2 border-radius values
32. Consistent icon style (all outlined or all filled, never mixed)
33. Clear button hierarchy (1 primary per view)
34. Shadows follow consistent light source (top-down)
35. Consistent spacing scale (4px base)
36. Limited color palette (1 brand + neutrals + semantic)
37. z-index scale from tokens

### State Handling (38-42)

38. Loading states exist (skeleton loaders)
39. Empty states guide users forward (CTA, not blank)
40. Error states show recovery path (retry action)
41. No dead-end screens
42. Destructive actions require confirmation

### Design System (43-48)

43. Zero hardcoded values (all from CSS variables)
44. One token file (single source of truth)
45. Modular CSS (each component owns its styles)
46. No inline styles for repeated patterns (3+ = make a class)
47. Font discipline (display for headings, body for text, mono for code)
48. Semantic class names (describe purpose, not appearance)

---

## Mode: polish

Production polish pass. No proposals - direct fixes.

### Quick Checklist

- [ ] No overlapping/cut-off elements
- [ ] Consistent spacing from design tokens
- [ ] Readable contrast (4.5:1+)
- [ ] Empty, loading, error states designed
- [ ] Hover/focus/active states consistent
- [ ] Mobile (375px) no horizontal scroll
- [ ] Desktop (1920px) not stretched
- [ ] Typography hierarchy clear
- [ ] All buttons have feedback states

### Output

```markdown
## Polish Report
Issues Found: X | Fixed: X | Remaining: [list]
Ready for /frontend-design qa: Yes/No
```

---

## Mode: qa

Quality gate before shipping.

### Automated Checks

```bash
# Emoji detection (should find 0)
grep -rE "[\x{1F300}-\x{1F9FF}]" src/

# transition: all (should be 0)
grep -r "transition: all" src/ | wc -l

# !important overrides (minimal)
grep -r "!important" src/ --include="*.css" | wc -l

# Hardcoded colors outside tokens
grep -rn "#[0-9a-fA-F]\{3,8\}" src/ --include="*.css" | grep -v tokens

# Inline styles count
grep -rn "style={{" src/ --include="*.tsx" | wc -l
```

### Manual Review

- [ ] Zero emojis in production UI
- [ ] No childish animations (bounce, wiggle, shake, pulse)
- [ ] No fake social proof
- [ ] No 3-column icon+title+description grid
- [ ] No decorative SVG blobs
- [ ] No gradient text (except 1 hero element max)
- [ ] All colors from design tokens
- [ ] All spacing from design tokens

### Senior Designer Test

1. Would this look professional in 5 years?
2. Is every element necessary?
3. Could you explain every design decision?
4. Does it look like a human designer made deliberate choices?

### Output

```
DESIGN QA REPORT
================
Automated: PASS/FAIL
Manual: PASS/FAIL
Senior Test: PASS/FAIL
Status: APPROVED / NEEDS REVISION
```

---

## Mode: flow

UX architecture only. No visuals, no code.

### Core Questions

1. **Entry:** Where does user start?
2. **Exit:** How do they know they're done?
3. **Screens:** List essential screens (3-7 max)
4. **Happy path:** Entry > A > B > Exit
5. **Decisions:** What must user decide? (keep <5)
6. **States:** Empty, loading, error for each screen

### Kill-Switch Test

- Does this flow require explanation? -> Simplify
- Could first-time user get stuck? -> Add guidance
- Are there screens that exist "just in case"? -> Remove

---

## Screenshot Protocol

For ANY design change:

1. Before: `mcp__puppeteer__puppeteer_screenshot({ name: "before-YYYY-MM-DD", width: 1280, height: 800 })`
2. Make changes
3. After: `mcp__puppeteer__puppeteer_screenshot({ name: "after-YYYY-MM-DD", width: 1280, height: 800 })`

---

## Design System Reference (New Projects)

### Dark Mode (Crypto/Trading)

```css
--bg-base: #09090b;
--bg-surface: #18181b;
--bg-elevated: #27272a;
--text-primary: #fafafa;
--text-secondary: #a1a1aa;
--text-muted: #71717a;
--accent: [pick ONE color];
--success: #10b981;
--warning: #f59e0b;
--error: #ef4444;
--border: rgba(255, 255, 255, 0.06);

/* Motion */
--ease-out: cubic-bezier(0.22, 1, 0.36, 1);
--duration-fast: 150ms;
--duration-normal: 200ms;
--duration-slow: 300ms;

/* Spacing: 4px base */
--space-1: 4px; --space-2: 8px; --space-3: 12px;
--space-4: 16px; --space-5: 20px; --space-6: 24px;
--space-8: 32px; --space-10: 40px; --space-12: 48px;
```

---

## Knowledge Base (Optional)

If the user has a design knowledge base (e.g. `~/System/guides/DESIGN_MASTERY.md` or similar), read targeted sections before generating:

| Phase | Topics to Load |
|-------|---------------|
| Proposals (new/revamp) | Typography, Color, Spacing & Layout, Motion & Animation, Personality Factor |
| Polish mode | Shadows & Depth, Motion & Animation, Dark Mode, Quick Reference |
| QA mode | Quick Reference (condensed rules only) |

Don't read an entire guide. Load only the sections relevant to the current mode. The skill works without external guides but produces better results with them.

---

## Personal Style (style.config.md)

Before generating proposals, check for a style config:
1. Project-level: `ai/style.config.md` (takes priority)
2. User-level: `~/.claude/style.config.md`

If found, apply:
- **Brand words** set the tone for all proposals
- **Color preferences** override defaults (respect anti-colors)
- **Motion philosophy** guides animation choices
- **Signature elements** must appear in proposals
- **Anti-patterns** are banned on top of `banned-defaults.md`

Style config is a preference layer, not hard constraints. If a DNA code conflicts with style preferences, DNA wins (structural variety matters more).

---

## Relationship to /design Orchestrator

This skill is Phase 2 (Creative) and Phase 5 (QA) of the `/design` workflow.
- When called via `/design`, the orchestrator handles knowledge loading and style config
- When called standalone, this skill loads them itself
- Polish mode overlaps with `/ui-revamp` but is lighter: quick pass vs full 4-phase audit

---

## Reference Files

- `reference/dna-system.md` - 5-gene DNA for structural variety
- `reference/banned-defaults.md` - Forbidden AI patterns
- `reference/inspirations.md` - Curated design reference library
- `reference/catalogue.html` - Proposal catalogue template

---

## Proposal Quality Checklist

Each proposal MUST:
- [ ] Have unique DNA (max 2 shared genes with others)
- [ ] Cite at least one inspiration (from different categories)
- [ ] Avoid ALL banned defaults
- [ ] Be self-contained (no external dependencies except fonts)
- [ ] Include DNA badge in top-right corner
- [ ] Include inspiration citation in footer
- [ ] Be responsive (mobile-first)
- [ ] Include full UX architecture in HTML comments
- [ ] Handle all states (loading, empty, error, success)
- [ ] Pass all 48 hard rules
- [ ] Look genuinely DIFFERENT from other proposals

---

## Wild Mode (Optional)

Add `--wild [theme]` to enable convention-breaking designs:

| Theme | Rules |
|-------|-------|
| `90s-web` | Tiled backgrounds, marquee, hit counters, garish colors |
| `y2k` | Chrome effects, bubble text, optimism gradients |
| `rave` | Acid colors, distorted text, neon on black |
| `brutalist` | Monospace, harsh borders, raw HTML |
| `afrofuturism` | Ankara patterns, gold accents, cosmic imagery |
| `newspaper` | Column layouts, drop caps, serif, B&W + accent |
| `vaporwave` | Pastel gradients, glitch, Japanese text |

When wild mode active: IGNORE usability conventions, PRIORITIZE visual impact, BREAK grid systems, EMBRACE the theme fully.

---

*"The details are not the details. They make the design." -- Charles Eames*
