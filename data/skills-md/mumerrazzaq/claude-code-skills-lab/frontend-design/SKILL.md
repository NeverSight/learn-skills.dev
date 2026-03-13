---
name: frontend-design
description: Create production-grade frontend interfaces with systematic UI/UX design. Use when building web components, pages, or applications. Covers design systems, component states, accessibility (WCAG 2.2), responsive design, and industry conventions. Evaluates existing UI against best practices. Forces design thinking before implementation. Generates distinctive code avoiding generic AI aesthetics while following UX principles.
license: Complete terms in LICENSE.txt
---

# Frontend Design Skill

Create distinctive, production-grade frontend interfaces using systematic UI/UX principles.

## Quick Answers

| Question | Answer |
|----------|--------|
| **What matters here?** | User needs FIRST, then accessibility, conventions, visual hierarchy |
| **What can go wrong?** | Designing without understanding users, poor accessibility, inconsistent states |
| **Fastest correct path?** | Think (understand) → Plan (decide) → Build (implement) → Validate (test) |
| **How do I know I'm done?** | User problem solved, WCAG compliant, conventions followed, states complete |

---

## PHASE 1: THINK (Mandatory Discovery)

**STOP. Do NOT write any code until these questions are answered.**

### 1.1 User Understanding

Ask or determine these BEFORE designing:

```
WHO is the user?
├── Demographics (age, tech proficiency, device usage)
├── Goals (what are they trying to accomplish?)
├── Context (where/when will they use this?)
└── Pain points (what frustrates them currently?)

WHAT problem does this solve?
├── Primary user task (the main job-to-be-done)
├── Secondary tasks (supporting actions)
├── Success criteria (how does user know they succeeded?)
└── Failure modes (what happens when things go wrong?)

WHY would users choose this over alternatives?
├── Unique value proposition
├── Competitive advantage
└── User motivation (convenience, speed, trust, delight?)
```

### 1.2 Technical Context

```
CONSTRAINTS:
├── Framework: React / Vue / Vanilla / Other?
├── Existing design system: Yes / No / Partial?
├── Performance budget: Critical / Normal / Flexible?
├── Browser support: Modern only / Legacy required?
└── Accessibility level: WCAG A / AA / AAA?

INTEGRATION:
├── Does this fit into existing UI?
├── What patterns already exist in the codebase?
├── What components can be reused?
└── What's the deployment target?
```

### 1.3 User Psychology Checkpoint

Before proceeding, consider:

| Mental Model | Question |
|--------------|----------|
| **Expectations** | What does the user expect to see based on similar products? |
| **Cognitive Load** | How much information can they process at once? |
| **Decision Fatigue** | How many choices are we asking them to make? |
| **Trust Signals** | What makes them feel safe/confident? |
| **Error Recovery** | How do they fix mistakes? |

**Output from Phase 1:** Document answers to these questions. If answers are unknown, ASK THE USER before proceeding.

### 1.4 If User Cannot Answer Discovery Questions

When user lacks context for Phase 1 questions:

```
FALLBACK APPROACH:
1. Document assumptions explicitly in component plan
2. Default to conservative choices:
   ├── WCAG 2.2 AA compliance
   ├── Mobile-first approach
   ├── Standard industry conventions
   └── 44px touch targets (exceeds WCAG 2.2 AA minimum)
3. Mark assumptions for later validation
4. Proceed with clearly stated caveats
```

---

## PHASE 2: PLAN (Design Decisions)

### 2.1 Information Architecture

Before visual design, structure the information:

```
CONTENT HIERARCHY:
├── What's the #1 thing users must see/do? → Make it PRIMARY
├── What supports the primary action? → Make it SECONDARY
├── What's rarely needed? → Make it TERTIARY or hide
└── What can be removed entirely? → DELETE IT

NAVIGATION MENTAL MODEL:
├── How does user expect to move through this?
├── What's the mental map they'll build?
├── Where might they get lost?
└── How do they return to safety?
```

### 2.2 Aesthetic Direction Selection

Choose ONE direction based on user psychology:

| Direction | Best For | User Psychology |
|-----------|----------|-----------------|
| **Brutally Minimal** | Pro tools, dashboards | Users value efficiency, hate clutter |
| **Maximalist** | Creative, entertainment | Users seek inspiration, exploration |
| **Retro-Futuristic** | Tech products, gaming | Users want to feel cutting-edge |
| **Organic/Natural** | Wellness, sustainability | Users value calm, authenticity |
| **Luxury/Refined** | Premium products | Users expect exclusivity, quality |
| **Editorial/Magazine** | Content-heavy, media | Users want to browse, discover |
| **Brutalist/Raw** | Dev tools, tech-forward | Users appreciate honesty, function |
| **Playful/Toy-like** | Consumer apps, games | Users want delight, fun |

**Decision Documentation:**
```
AESTHETIC CHOICE: [Selected Direction]
RATIONALE: [Why this fits the user/context]
KEY CHARACTERISTICS: [3-5 specific traits to implement]
```

### 2.3 Component Planning

For each component, decide BEFORE building:

```
COMPONENT: [Name]
├── PURPOSE: What job does this do?
├── USER EXPECTATION: What do they expect it to look like/behave?
├── STATES NEEDED: [default, hover, focus, active, disabled, loading, error, success]
├── RESPONSIVE BEHAVIOR: How does it adapt?
├── ACCESSIBILITY: How do screen readers announce it?
└── CONVENTION CHECK: What do GitHub/Stripe/Google do?
```

**Output from Phase 2:** Component plan with rationale for each decision.

---

## PHASE 3: BUILD (Implementation)

### 3.1 Design Tokens First

Before writing component code, establish tokens for:

| Category | Examples | Count |
|----------|----------|-------|
| **Typography** | `--font-size-xs` to `--font-size-3xl`, line heights | ~12 tokens |
| **Spacing** | 8-point grid: 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px | ~8 tokens |
| **Colors** | Primary, secondary, success, warning, error, text, background, border | ~15 tokens |
| **Effects** | `--focus-ring`, `--transition-fast`, shadows | ~6 tokens |

**For complete token system with examples: See references/design-system.md**

### 3.2 Component States Implementation

**EVERY interactive element MUST have these states:**

| State | CSS Selector | Visual Change | Purpose |
|-------|--------------|---------------|---------|
| Default | `.btn` | Base appearance | Normal state |
| Hover | `.btn:hover` | Lighten/darken 10% | Mouse feedback |
| Focus | `.btn:focus-visible` | Focus ring (REQUIRED) | Keyboard navigation |
| Active | `.btn:active` | Scale down slightly | Click feedback |
| Disabled | `.btn:disabled` | 50% opacity, no pointer | Unavailable |
| Loading | `.btn.loading` | Spinner, disabled | Processing |

**Key implementation points:**
- `min-height: 44px; min-width: 44px` for touch targets
- `:focus-visible` with `box-shadow: var(--focus-ring)` for accessibility
- `transition: var(--transition-fast)` for smooth state changes

**For complete CSS implementations: See references/component-states.md**

### 3.3 Layout Conventions

**Button Order (CRITICAL - Industry Standard):** Secondary LEFT, Primary RIGHT

Evidence: GitHub, Stripe, Google, Notion, Figma all follow this pattern.

**For complete conventions with evidence: See references/industry-conventions.md**

### 3.4 Responsive Implementation

**Breakpoints (mobile-first):** 640px (sm) → 768px (md) → 1024px (lg) → 1280px (xl) → 1536px (2xl)

**Touch Targets (MANDATORY):** 44×44px minimum on all interactive elements (exceeds WCAG 2.2 AA 24px requirement)

**For complete responsive patterns: See references/mobile-responsive.md**

---

## PHASE 4: VALIDATE (Quality Assurance)

### 4.1 Accessibility Checklist

| Check | Standard | How to Test |
|-------|----------|-------------|
| Color contrast | 4.5:1 normal, 3:1 large | Browser DevTools or WebAIM checker |
| Focus visible | All interactive elements | Tab through entire page |
| Labels present | All inputs have labels | Inspect form elements |
| Alt text | All meaningful images | Check img tags |
| Keyboard navigation | Everything accessible | Unplug mouse, use only keyboard |
| Screen reader | Logical reading order | Use VoiceOver/NVDA |

For complete accessibility guide: See references/accessibility.md

### 4.2 3-Dimension UI Evaluation

For ANY component, evaluate:

| Dimension | What to Check | Pass Criteria |
|-----------|---------------|---------------|
| **Position** | Location relative to other elements | Follows conventions, discoverable |
| **Visual Weight** | Prominence vs other elements | Clear hierarchy, primary stands out |
| **Spacing** | Gap from adjacent elements | Consistent, adequate separation |

**Evaluation Output Format:**
```markdown
## [Component] Evaluation

### Current State
- Position: [Description]
- Visual Weight: [Description]
- Spacing: [Measurements]

### Verdict: [CORRECT / NEEDS CHANGES]

### Issues (if any)
| Priority | Issue | Fix |
|----------|-------|-----|
| P1 | [Critical UX break] | [Specific fix] |
| P2 | [Suboptimal] | [Specific fix] |
| P3 | [Polish] | [Specific fix] |
```

For complete evaluation framework: See references/evaluation-framework.md

### 4.3 Final Quality Gate

**Before delivery, verify ALL items:**

```
ACCESSIBILITY (WCAG 2.2)
[ ] Color contrast meets WCAG AA (4.5:1 text, 3:1 large)
[ ] All focus states visible and not obscured by other content
[ ] Focus indicators meet WCAG 2.2 requirements
[ ] All inputs have associated labels
[ ] Keyboard navigation works end-to-end
[ ] Touch targets: 44px+ (exceeds WCAG 2.2 AA 24px minimum)
[ ] Dragging actions have single-pointer alternative
[ ] Help mechanisms in consistent location across pages
[ ] Don't re-request previously entered information
[ ] Authentication without cognitive function tests

CONVENTIONS
[ ] Button order: Secondary LEFT, Primary RIGHT
[ ] Navigation: Logo LEFT, Primary nav CENTER/LEFT, Utilities RIGHT
[ ] Forms: Labels above inputs, error messages below

STATES
[ ] All buttons have: default, hover, focus, active, disabled
[ ] All inputs have: default, focus, filled, error, disabled
[ ] Loading states for async operations
[ ] Error states with clear messages
[ ] Empty states for no-data scenarios

RESPONSIVE
[ ] Mobile breakpoint (320px) tested
[ ] Tablet breakpoint (768px) tested
[ ] Desktop breakpoint (1024px+) tested
[ ] No horizontal scroll on mobile

AESTHETICS
[ ] Typography is distinctive (not Inter/Roboto/Arial)
[ ] Color palette is cohesive
[ ] Spacing uses consistent system
[ ] Visual hierarchy is clear
```

---

## Reference Files

Load based on current task:

| File | When to Use |
|------|-------------|
| [design-system.md](references/design-system.md) | Creating tokens, atomic design, component library |
| [component-states.md](references/component-states.md) | Implementing interactive elements, state machines |
| [accessibility.md](references/accessibility.md) | WCAG compliance, screen readers, keyboard nav, security patterns |
| [industry-conventions.md](references/industry-conventions.md) | Button order, navigation, standard patterns |
| [evaluation-framework.md](references/evaluation-framework.md) | Auditing existing UI, producing verdicts |
| [typography-color.md](references/typography-color.md) | Font pairing, color psychology, visual design |
| [forms-inputs.md](references/forms-inputs.md) | Form design, validation, input patterns |
| [mobile-responsive.md](references/mobile-responsive.md) | Breakpoints, touch, responsive patterns |
| [anti-patterns.md](references/anti-patterns.md) | What to avoid, common mistakes |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why Bad | Fix |
|--------------|---------|-----|
| Designing before understanding users | Solves wrong problem | Complete Phase 1 first |
| Icon-only buttons | Not understandable | Add labels |
| Primary LEFT, Secondary RIGHT | Breaks convention | Reverse order |
| Touch targets < 44px | Unusable on mobile | Increase size |
| No focus states | Fails accessibility | Add focus-visible |
| Placeholder as label | Disappears on input | Use real labels |
| Same styling primary/secondary | No hierarchy | Differentiate visually |
| Generic fonts (Inter/Roboto) | AI slop aesthetic | Choose distinctive fonts |

For complete anti-patterns: See references/anti-patterns.md

---

## External Resources

| Resource | URL | Use For |
|----------|-----|---------|
| WCAG 2.2 Quick Reference | https://www.w3.org/WAI/WCAG22/quickref/ | Current accessibility standard |
| What's New in WCAG 2.2 | https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/ | 9 new criteria |
| MDN Accessibility | https://developer.mozilla.org/en-US/docs/Web/Accessibility | Implementation patterns |
| WebAIM Contrast Checker | https://webaim.org/resources/contrastchecker/ | Testing contrast |
| Material Design 3 | https://m3.material.io/ | Component patterns |

## When Patterns Aren't Covered

For patterns not in this skill:

1. Fetch docs from official sources (MDN, WCAG, framework docs)
2. Reference established design systems (Material, Carbon, Spectrum)
3. Use Context7 MCP for library-specific documentation
4. Default to conservative choices when uncertain

---

**Standards Note**: This skill follows **WCAG 2.2** (ISO/IEC 40500:2025, current as of December 2025).
WCAG 3.0 is in development. Check https://www.w3.org/WAI/ for updates.
