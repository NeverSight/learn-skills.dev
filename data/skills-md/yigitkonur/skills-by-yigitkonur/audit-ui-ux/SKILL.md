---
name: audit-ui-ux
description: "Use if auditing web or mobile UI/UX via vision-first screenshot evaluation across design precision, usability heuristics, and cognitive laws."
disable-model-invocation: true
---

# Unified Vision-First UI & UX Audit (`audit-ui-ux`)

An authoritative, vision-first audit skill that evaluates running Web and Mobile interfaces purely from captured visual pixels. It merges visual design precision (spacing, contrast, typography, tokens) and cognitive human-computer interaction (Nielsen's 10 Heuristics, scientifically grounded Laws of UX) without code inspection bias.

---

## 1. Core Mental Model: Strict Vision-First Air-Gap

The central architectural rule is the **Strict Vision-First Air-Gap** (`references/vision-air-gap.md`):

> **Evaluation agents must NEVER inspect application source code, DOM trees, CSS classes, or internal selectors.**

### Eliminating Omniscience Bias
Human users experience digital products through light emitted from display pixels, not by reading source code. When evaluators read component source files, they suffer from omniscience bias—assuming layout rules work, forgiving poor contrast, and missing visual rendering flaws. The audit evaluates purely from rendered screenshots.

### Visual-Spatial Grounding Framework
To eliminate reliance on internal component names, IDs, or class names, evaluators ground every finding using dual-layer visual-spatial coordinates (`references/vision-air-gap.md`):
1. **Directional Landmark Hierarchy:** `[Screen Region] > [Container Landmark] > [Relative Flow Position] > [Visual Feature Anchor]` (e.g. `Sticky Header > Right Utility Actions > Notification Bell Button`).
2. **Normalized Bounding Coordinates:** Normalized percentage coordinates `[top%, left%, width%, height%]` and 3×3 screen quadrants (`[Top-Right]`, `[Mid-Center]`, etc.).

### Anti-Omniscience Defense Vectors
Evaluation subagents operate under strict environment boundaries forbidding:
- Reading source code or AST files (`.tsx`, `.jsx`, `.vue`, `.svelte`, `.html`, `.css`, `.swift`, `.kt`).
- Grepping or searching the workspace for text strings observed in screenshots.
- Querying DOM trees, computed styles, or Chrome DevTools Protocol (CDP) element inspect APIs.
- Reading design token or configuration files (`tailwind.config.*`).

```
┌────────────────────────────────────────────────────────┐
│                   TARGET APPLICATION                   │
│         (Running Web Dev Server or Mobile App)         │
└───────────────────────────┬────────────────────────────┘
                            │ (Dual-Engine Capture)
                            ▼
┌────────────────────────────────────────────────────────┐
│              DETERMINISTIC SCREENSHOT BUS              │
│       audit-artifacts/<YYYY-MM-DD>/<screen-slug>/      │
└─────────────┬────────────────────────────┬─────────────┘
              │                            │
   (Pixels Only / Air-Gapped)    (Pixels Only / Air-Gapped)
              ▼                            ▼
┌───────────────────────────┐┌───────────────────────────┐
│          UI LENS          ││          UX LENS          │
│ Design Systems & Precision││Usability & Cognitive Laws │
└─────────────┬─────────────┘└─────────────┬─────────────┘
              │                            │
              └─────────────┬──────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│               CONSOLIDATED AUDIT REPORT                │
│       audit-artifacts/<YYYY-MM-DD>/AUDIT-REPORT.md     │
└────────────────────────────────────────────────────────┘
```

---

## 2. When to Use & Execution Modes

### When to Use
- Auditing a running web or mobile application for visual bugs, alignment flaws, or design token inconsistencies.
- Reviewing user flows, onboarding journeys, and complex interfaces against cognitive load and usability heuristics.
- Pre-release visual QA across desktop and mobile screen viewports.
- Verifying WCAG 2.2 contrast and touch target accessibility compliance from real visual output.

### Do NOT Use When
- Functional end-to-end integration testing or headless assertion suites (use `test-by-maestro` or `run-playwright`).
- Automated source code linting or AST static analysis.
- Backend API or non-visual data layer tasks.

### Execution Modes
The audit supports three execution modes, documented in detail in `references/execution-modes.md`:
- **`both` (Default):** Runs UI Lens and UX Lens concurrently over the captured screenshots.
- **`ui`:** Runs the UI Lens only (frontend design systems, visual precision, styling tokens).
- **`ux`:** Runs the UX Lens only (usability heuristics, cognitive ergonomics, user flows).

---

## 3. Dual-Engine Capture Pipeline

Capture visual screenshots before launching evaluation lenses, documented in `references/capture-pipeline.md`:

### Engine 1: Web Capture (`ego-browser`)
- Capture is driven exclusively via `ego-browser`. Headless scrapers and raw Playwright are strictly prohibited.
- **Remote Host Detection & Sync:** When testing on a remote server (e.g., dev host `tugce`), detect the SSH session, trigger capture remotely, and automatically sync screenshots to the local workspace via `scp`:
  ```bash
  scp -r user@remote-host:/path/to/audit-artifacts/<YYYY-MM-DD>/ ./audit-artifacts/<YYYY-MM-DD>/
  ```

### Engine 2: Mobile Capture (`test-by-maestro`)
- Mobile audits require the `skills/test-by-maestro` skill as a prerequisite.
- Operates across iOS Simulators (macOS) and Android emulators/devices (macOS, Linux, Windows) via Maestro's declarative YAML runner and MCP interface (`maestro mcp`).

---

## 4. Screen & State Directory Architecture

Screenshots must be deposited into the deterministic hierarchy defined in `references/screen-state-matrix.md`:

```
audit-artifacts/
  [YYYY-MM-DD]/
    AUDIT-REPORT.md
    [screen-slug]/
      default.png        # Mandatory: Base initial render
      hover.png          # Hover micro-interaction
      active.png         # Input focus / pressed state
      empty-state.png    # 0-item / blank-slate render
      error-state.png    # Validation or network error
      loading.png        # Skeleton or progress state
      modal-open.png     # Overlay / dialog / sheet open
```

### Pre-Evaluation Capture Verification Gate
Before spawning evaluation lenses, execute the capture gate script:
```bash
bash skills/audit-ui-ux/scripts/validate-capture-gate.sh audit-artifacts/<YYYY-MM-DD>/
```
The script validates PNG magic bytes, non-zero file sizes, and verifies that `default.png` exists for every screen.

---

## 5. Parallel Dual-Persona Vision Evaluation

Evaluation lenses are dispatched as concurrent subagents using Antigravity multi-agent orchestration (`invoke_subagent`, `Model: 'inherit'`, `Workspace: 'branch'`).

### Lens 1: UI Lens Persona (Design Systems & Precision)
Detailed in `references/ui-lens-persona.md`. Evaluates pixel-level craft with this embedded persona prompt:

> "Act like a world-class UI engineer with pixel-perfect high precision frontend coding combiend with years of product design and Figma experience and spot the issues and describe it like someone showing this on someone sitting next to you by referring specific component directly and tell UX issues in here (color/spacing/padding/shadow etc) by thinking deep on solely given screenshots."

**Scrutiny Focus:**
- **Spacing & Padding:** Consistent 4px/8px spatial scale, proportional component padding, label clearance.
- **Color & Contrast:** WCAG 2.2 AA (4.5:1 text, 3.0:1 UI components), color independence for accessibility.
- **Typography Scale:** Harmonious modular font scale, line lengths (45–75 chars), readable leading.
- **Elevation & Radii:** Nested border radii ($R_{\text{outer}} = R_{\text{inner}} + \text{padding}$), unified shadow light angles.

### Lens 2: UX Lens Persona (Usability & Cognitive Laws)
Detailed in `references/ux-lens-persona.md`. Evaluates human cognitive flow and ergonomics:
- **Nielsen's 10 Usability Heuristics:** System status visibility, real-world match, user control & escape hatches, consistency, error prevention, recognition over recall, efficiency, minimalist design, error recovery, contextual help.
- **The 30 Laws of UX (Scientifically Grounded):** Detailed in `references/scientific-laws-catalog.md`.

---

## 6. Empirical Grounding & Debunked Myths

The audit enforces scientifically verified standards, eliminating common legacy misconceptions (`references/scientific-laws-catalog.md`):

| Principle | Debunked Legacy Myth | Empirically Grounded Truth |
|---|---|---|
| **Miller's Law** | Arbitrary "7 ± 2" cap on display items / menus. | Nelson Cowan (2001) established working memory capacity is **4 ± 1 chunks**. Display items on screen do NOT consume working memory slots ("recognition over recall"). |
| **Doherty Threshold** | 400ms mainframe threshold treated as modern target. | Modern interaction demands $\le 100\text{ ms}$ for immediate visual feedback, and **Core Web Vitals INP $\le 200\text{ ms}$**. Operations $> 1\text{s}$ require progress indicators. |
| **Fitts's Law** | Linear "primary action > 200px" rule. | Index of Difficulty $ID = \log_2(D/W + 1)$ is **logarithmic**. Desktop screen edges have infinite virtual depth ($W \to \infty$); mobile touch is governed by thumb zones. |
| **Hick's Law** | Capping all choices everywhere. | Strictly models simple stimulus-response reaction time. Choice overload is moderated by task difficulty and filtering (Scheibehenne 2010). |
| **Touch Targets** | Uncited 44px blanket numbers. | **WCAG 2.2 SC 2.5.8 AA:** 24×24 CSS px minimum.<br>**Apple HIG:** 44×44 pt.<br>**Material 3:** 48×48 dp. |
| **Device Viewports** | 375pt labeled as iPhone 13. | Modern base iPhone 13/14 is **390 × 844 pt**; iPhone 14 Pro/15/16 is **393 × 852 pt**. Android standard is **360 × 800 dp**. |
| **Form Patterns** | Unrestricted dropdown usage. | Nielsen Norman Group: Avoid dropdowns for $<5$ options (use radio buttons); group fields in `<fieldset>`; validate on `blur`, not premature `keyup`. |

---

## 7. Synthesis & Reporting Architecture

When evaluation lenses conclude, the orchestrator compiles the findings into the standardized format specified in `references/reporting-format.md`:
1. **Deduplication & Cross-Lens Clustering:** Group findings by screen slug and visual landmark.
2. **Severity Calibration & Priority Mapping:** Catastrophe (P0 Blocker) → Critical (P1 Release Gate) → Major (P2 Sprint Priority) → Minor (P3 Polish).
3. **Standardized 4-Field Findings:** Every finding contains:
   - Visual bounding region and landmark coordinates (`location.landmark`, `location.bounding_box`).
   - Severity level (`Catastrophe`, `Critical`, `Major`, `Minor`) and Priority (`P0`–`P3`).
   - Standardized rule taxonomy ID (`rule.id`, `rule.type`).
   - Deterministic visual fix recommendation (`visual_fix.target_visual_state`, `visual_fix.target_parameters`, `visual_fix.anti_patterns`).
4. **Machine-Parseable Ingestion Schema:** Each finding embeds a ```yaml finding-spec``` code block allowing deterministic parsing by downstream fix agents (`build-frontend`), following the ingestion workflow in `references/reporting-format.md`.
5. **Persist Final Report:** Write to `audit-artifacts/<YYYY-MM-DD>/AUDIT-REPORT.md` including the Executive Dashboard, Screen Inventory, Priority Action Matrix, and machine-parseable finding specifications.
