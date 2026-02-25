---
name: growth-design-review
description: Review UI designs and code against Product Psychology & Growth Design frameworks (Psych, B.I.A.S., C.L.E.A.R., UI Rules of Thumb, Psychological Triggers). Use when asked to "review my design", "audit growth UX", "check conversion optimization", "review onboarding flow", "audit landing page", or "propose a development plan for my UI".
license: MIT
---

# 🧠 Growth Design Review Skill

Review UI designs or code against **Product Psychology & Growth Design frameworks**. Propose a prioritized development plan following each framework's best practices to maximize the Net Perceived Value.

---

## 📚 Frameworks Overview

This skill applies five core frameworks. **CRITICAL:** You must read the full definitions in `reference/frameworks.md` before performing any review.

1. **Psych Framework** — Maximize Net Perceived Value (Motivation - Friction).
2. **B.I.A.S. Framework** — Behavioral audit: Block, Interpret, Act, Store.
3. **C.L.E.A.R. Scorecard** — Copywriting, Layout, Emphasis, Accessibility, Reward.
4. **UI Rules of Thumb** — Page-type specific patterns (e.g., Landing, Dashboard, Onboarding).
5. **Psychological Triggers** — Utilization of the IKEA Effect, Zeigarnik Effect, and Loss Aversion.

---

## 🛠 Review Process

Whenever a user requests a review, strictly follow these steps:

1. **Diagnostic Routing:** Determine if the interface involves AI (LLMs, generative UI, or autonomous agents).
   - *If standard SaaS/Web:* Apply the Psych Framework, B.I.A.S. Audit, and C.L.E.A.R. Scorecard.
   - *If AI-Native:* Read `reference/shape-of-ai.md`. Apply standard frameworks to diagnose friction, but you MUST propose solutions using specific Shape of AI patterns.
2. **Load Context:** Read the `reference/frameworks.md` file from this skill's directory.
3. **Understand the Target:** Read the target UI files (components, pages, styles) the user wants reviewed. If none are provided, ask the user which files to evaluate.
4. **Systematic Audit:** Evaluate the UI against *all* applicable frameworks systematically.
5. **Scoring:** Rate each C.L.E.A.R. dimension (Copy, Layout, Emphasis, Accessibility, Reward) on a strict **1–5 scale**.
6. **Actionable Output:** Generate the output exactly matching the format below.
7. **Next Steps:** Offer to implement the Priority 1 (Critical) items immediately for the user.

---

## 📋 Required Output Format

You must format your response exactly as follows:

```markdown
## 📈 Growth Design Audit

### 1. Psych Framework Analysis
**Net Perceived Value Assessment:**
- **Motivation signals found:** [List any]
- **Friction points found:** [List any]
- **Psych Additions present:** [Rewards, progress markers, delighters]
- **Psych Subtractions to fix:** [Redundant fields, cognitive load, jargon]
- **Labor Illusion usage:** [Present/missing, recommendation]

### 2. B.I.A.S. Behavioral Audit
| Dimension | Status | Finding |
| :--- | :---: | :--- |
| **Block** (Visual Hierarchy & Trust) | [Pass/Fail] | [Brief explanation] |
| **Interpret** (Clarity over Cleverness) | [Pass/Fail] | [Brief explanation] |
| **Act** (Decision Simplicity) | [Pass/Fail] | [Brief explanation] |
| **Store** (Peak-End Rule) | [Pass/Fail] | [Brief explanation] |

### 3. C.L.E.A.R. Scorecard
| Dimension | Score (1-5) | Finding |
| :--- | :---: | :--- |
| **C** - Copywriting | X/5 | [Brief explanation] |
| **L** - Layout | X/5 | [Brief explanation] |
| **E** - Emphasis | X/5 | [Brief explanation] |
| **A** - Accessibility | X/5 | [Brief explanation] |
| **R** - Reward | X/5 | [Brief explanation] |
| **Total Score** | **XX/25** | |

### 4. UI Rules of Thumb
- **Page Type Identified:** [Landing / Dashboard / Onboarding / Component / Other]
- **Compliance Analysis:** [Findings per applicable rule based on the page type]

### 5. Psychological Triggers
- **IKEA Effect:** [Present / Missed Opportunity] - [Explanation]
- **Zeigarnik Effect:** [Present / Missed Opportunity] - [Explanation]
- **Loss Aversion:** [Present / Missed Opportunity] - [Explanation]

### 6. Shape of AI Analysis (If AI-Native)
| Dimension | Friction Point | NPV Impact | Recommended Shape of AI Pattern |
| :--- | :--- | :--- | :--- |
| [Category] | [Brief Description] | [Impact] | **[Pattern Name]:** [Execution suggestion] |

---

## 🏗 Development Plan

### 🔴 Priority 1 — Critical (High Impact, Low Effort)
| # | Action | Framework | File(s) | Rationale |
|---|--------|-----------|---------|-----------|
| 1 | [Action] | [Framework] | [File path] | [Why this matters] |

### 🟡 Priority 2 — Important (High Impact, Higher Effort)
| # | Action | Framework | File(s) | Rationale |
|---|--------|-----------|---------|-----------|
| 1 | [Action] | [Framework] | [File path] | [Why this matters] |

### 🟢 Priority 3 — Nice to Have (Lower Impact)
| # | Action | Framework | File(s) | Rationale |
|---|--------|-----------|---------|-----------|
| 1 | [Action] | [Framework] | [File path] | [Why this matters] |
```
