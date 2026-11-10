---
name: apple-design
description: Complete Apple Human Interface Guidelines (HIG) and Apple Design System standard. Use when designing, building, or auditing UI/UX for iOS, iPadOS, macOS, watchOS, visionOS, or Apple-styled web and mobile applications.
version: 1.1.0
license: MIT
author: apple-design-skill
tags:
  - design-system
  - apple
  - hig
  - swiftui
  - ios
  - macos
  - visionos
  - web-design
  - ui-ux
  - audit
---

# Apple Design System & Human Interface Guidelines (HIG)

This skill equips AI coding agents with the exact principles, visual specifications, component architectures, typography metrics, color tokens, motion curves, and automated compliance auditing defined by **Apple's Human Interface Guidelines (HIG)** across iOS, iPadOS, macOS, watchOS, visionOS, and modern Apple-grade Web UI.

---

## 🎯 Operational Modes

### Mode 1 — Design & Build from Scratch
When tasked with creating new screens, apps, or web interfaces in Apple style:
1. Choose the platform-native navigation paradigm (e.g. Bottom Tab Bar for iOS, Sidebar for macOS/iPad, Ornaments for visionOS).
2. Establish the 8pt spatial grid and continuous squircle curvature (`G2 continuity`).
3. Apply the SF Pro / New York typography scale with optical tracking rules.
4. Implement semantic Dynamic Colors (Light & OLED Dark mode) and Liquid Frosted Glass materials.
5. Apply Apple spring physics (`cubic-bezier(0.25, 1, 0.5, 1)`) and tactile active feedback (`scale(0.97)`).

### Mode 2 — Apple HIG Compliance Audit & Scoring
When reviewing an existing codebase, mockup, or component:
1. Run the audit tool `node skills/apple-design/scripts/audit-apple-design.mjs` to perform automated static scanning with a **0–100 Scoring Rubric**.
2. Perform exact mathematical WCAG contrast checks and 44×44pt touch-target validations.
3. Fill out the **[Apple HIG Audit Scorecard](skills/apple-design/templates/apple-hig-audit-scorecard.md)** across the 5 core pillars.
4. Deliver prioritized findings with **Confidence Tagging**:
   - 🟢 **Tool-verified**: Statistically measured via CLI tool (e.g., contrast ratio, button dimension, static CSS rules).
   - 🟡 **Needs device test**: Requires hardware interaction (e.g., Dynamic Type at 300%, Reduce Transparency toggle, VoiceOver speech hierarchy).
   - 🔴 **Assumed**: Contextual design trade-off or subjective aesthetic evaluation.

---

## 🛠️ The Apple HIG Compliance CLI Engine

The built-in audit engine (`skills/apple-design/scripts/audit-apple-design.mjs`) provides four subcommands:

```bash
# 1. Full Codebase Static Scan with 0-100 Scorecard (Default)
npm run audit
# or: node skills/apple-design/scripts/audit-apple-design.mjs [path]

# 2. WCAG Relative Luminance Contrast Ratio Check
node skills/apple-design/scripts/audit-apple-design.mjs contrast "#8E8E93" "#FFFFFF"
# -> Contrast Ratio: 3.26:1 [🔴 FAILED - Needs >= 4.5:1]

# 3. Tap Target Sizing Validation (44x44 pt minimum)
node skills/apple-design/scripts/audit-apple-design.mjs target 32 32
# -> Tap Target: 32x32 pt [🔴 FAILED - Minimum 44x44 pt]

# 4. Batch JSON Automated Verification
node skills/apple-design/scripts/audit-apple-design.mjs batch audit.json
```

### Audit Scoring Rubric:
- Base score: **100 points**.
- Point deduction: **-10 points per violation**.
- Scorecard Classification:
  - 🟢 **90 – 100 pts**: **Ship (Sẵn sàng phát hành)** — Đạt chuẩn xuất sắc.
  - 🟡 **70 – 89 pts**: **Cần sửa trước khi release (Fix before release)** — Cần khắc phục trước khi đưa lên App Store / production.
  - 🔴 **< 70 pts**: **Cần thiết kế lại (Systematic redesign required)** — Vi phạm nghiêm trọng kiến trúc hoặc khả năng tiếp cận.

---

## 1. Core Design Philosophy

Apple interfaces are built upon three primary pillars:

1. **Clarity**:
   - Text is legible at every size; icons are precise, distinct, and universally understood.
   - Adornments are subtle and purposeful. Content always takes visual priority over decorative Chrome.
   - Negative space (whitespace) provides breathing room and clarifies visual hierarchy.

2. **Deference**:
   - Fluid motion, translucent materials, and crisp typography elevate content without competing with it.
   - Backgrounds defer to content; chrome recedes when the user is engaged in primary tasks.

3. **Depth**:
   - Distinct visual layers, realistic lighting, specular highlights, and physical spring physics convey spatial hierarchy and tactile realism.
   - Elevations and materials communicate interactive affordances without harsh dropped shadows or abrasive outlines.

---

## 2. Universal Apple Design Tenets & Critical Rules

### 🚫 Forbidden Anti-Patterns (Never Do These)
- **NO Purple/Violet On Dark Themes**: Never use purple fonts or violet accent buttons on dark backgrounds. Use Apple System Blue (`#0A84FF`) or semantic system tints.
- **NO Harsh Drop Shadows**: Never use dense black un-diffused box shadows (`box-shadow: 0 4px 10px rgba(0,0,0,0.5)`). Use multi-layered ambient diffusion (`box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04)`).
- **NO Sharp / Geometric Corners**: Never leave interactive controls, cards, or inputs with 0px radius or arbitrary non-continuous corners.
- **NO Untracked Large Typography**: Never render large headings (>24px) without tight letter-spacing (-0.02em to -0.03em / -0.5px to -1.2px).
- **NO Non-Standard Touch Targets**: Never create clickable elements smaller than 44×44 pt (iOS standard) or 28×28 pt (macOS compact pointer).
- **NO Plain Static CSS Transitions**: Never use `ease-in-out` for physical UI interactions; always use fluid spring physics or Apple easing curves.

---

## 3. Visual Foundations

### A. Typography System (San Francisco & New York)
- **Primary Interface Font**: SF Pro (`-apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", sans-serif`)
- **Monospace Font**: SF Mono (`ui-monospace, "SF Mono", Menlo, Monaco, Consolas, monospace`)
- **Serif Font**: New York (`"New York", ui-serif, Georgia, Cambria, serif`)

#### Typographic Scale & Optical Sizing Rules:
| Style | Size (pt/px) | Weight | Line Height | Tracking / Letter Spacing |
| :--- | :--- | :--- | :--- | :--- |
| **Large Title** | 34px | Bold (700) | 41px | `-0.022em (-0.75px)` |
| **Title 1** | 28px | Bold / SemiBold | 34px | `-0.020em (-0.56px)` |
| **Title 2** | 22px | Bold / SemiBold | 28px | `-0.018em (-0.40px)` |
| **Title 3** | 20px | SemiBold (600) | 25px | `-0.015em (-0.30px)` |
| **Headline** | 17px | SemiBold (600) | 22px | `-0.012em (-0.20px)` |
| **Body** | 17px | Regular (400) | 22px | `-0.010em (-0.17px)` |
| **Callout** | 16px | Regular (400) | 21px | `-0.008em (-0.13px)` |
| **Subheadline** | 15px | Regular (400) | 20px | `-0.005em (-0.08px)` |
| **Footnote** | 13px | Regular (400) | 18px | `0.000em (0.00px)` |
| **Caption 1** | 12px | Regular (400) | 16px | `0.005em (+0.06px)` |
| **Caption 2** | 11px | Regular / Medium | 13px | `0.010em (+0.11px)` |

---

## 4. Materials, Translucency & Specular Glass

Apple materials blur underlying content to create visual grounding while maintaining vibrancy:

```css
/* Authentic Apple Ultra-Thin Frosted Glass Material */
.apple-material-ultrathin {
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(20px) saturate(190%);
  -webkit-backdrop-filter: blur(20px) saturate(190%);
  border: 1px solid rgba(255, 255, 255, 0.45);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.02);
}

@media (prefers-color-scheme: dark), [data-theme="dark"] {
  .apple-material-ultrathin {
    background: rgba(28, 28, 30, 0.75);
    backdrop-filter: blur(25px) saturate(190%);
    -webkit-backdrop-filter: blur(25px) saturate(190%);
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35), 0 1px 3px rgba(255, 255, 255, 0.05) inset;
  }
}
```

---

## 5. Animation Physics (Apple Spring Curves)

Never use linear or standard ease curves for interactive UI. Use authentic Apple spring physics:

### Spring Parameters Reference:
- **Interactive / Tap feedback**: `mass: 1, stiffness: 350, damping: 35` (CSS approx: `cubic-bezier(0.25, 1, 0.5, 1)`)
- **Sheet Presentation / Modal Slide**: `mass: 1.2, stiffness: 280, damping: 28` (CSS approx: `cubic-bezier(0.32, 0.72, 0, 1)`)
- **Snappy Switch / Toggle**: `mass: 0.8, stiffness: 450, damping: 30`

```css
/* Apple Native Motion Classes */
.apple-spring-interactive {
  transition: transform 0.35s cubic-bezier(0.25, 1, 0.5, 1),
              opacity 0.25s ease;
}

.apple-spring-interactive:active {
  transform: scale(0.965);
}
```

---

## 6. Bundled Resources & Full Apple HIG Library

- **[Master HIG Documentation Catalog (skills/apple-design/references/INDEX.md)](skills/apple-design/references/INDEX.md)**: Full searchable index of all 172 guideline topics.
- **[Apple HIG Audit Scorecard Template](skills/apple-design/templates/apple-hig-audit-scorecard.md)**: Standard 5-pillar evaluation scorecard.
- **Assets & Presets**:
  - `skills/apple-design/assets/apple-tokens.css`: Complete CSS variable design token stylesheet.
  - `skills/apple-design/assets/apple-components.css`: Ready-to-use CSS components (Buttons, Glass cards, Segmented, Sheets).
  - `skills/apple-design/assets/tailwind.preset.apple.js`: Tailwind configuration preset.
  - `skills/apple-design/assets/swiftui-cheat-sheet.md`: Idiomatic SwiftUI patterns.
- **CLI Automation Tools**:
  - `npm run audit`: Scans codebases for Apple HIG violations and generates a 0–100 score.
  - `npm run fetch-hig`: Fetches/updates the entire Apple HIG documentation and illustrations from Apple CDN.
