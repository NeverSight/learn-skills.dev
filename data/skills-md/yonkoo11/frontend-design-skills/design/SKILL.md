---
name: design
description: Design workflow orchestrator. Single entry point for all design work - chains frontend-design proposals into ui-revamp production polish with phase gates. Supports resume, short-circuit flags, and progress tracking.
---

# Design Workflow Orchestrator

Single entry point for all design work. Enforces the correct phase order so nothing gets skipped.

```
/design [project-name] [flags]

Flags:
  --skip-state    Skip Phase 1 (static pages, no app state)
  --polish-only   Jump to Phase 4 (already have a design, just polish)
  --qa-only       Jump to Phase 5 (already polished, final gate)
```

---

## Phase Overview

```
Phase 0: Pre-flight     → Load config, check prerequisites
Phase 1: State Design   → /state-design (data architecture)
Phase 2: Creative        → /frontend-design new|revamp (3 proposals)
Phase 3: Selection       → User picks winner
Phase 4: Production      → /ui-revamp (4-phase audit + polish)
Phase 5: Final QA        → /frontend-design qa (ship gate)
```

---

## EXECUTION

### Phase 0: Pre-flight

Before anything, load context:

1. **Load style config** (personality layer):
   - Check for project-level: `ai/style.config.md`
   - Fall back to user-level: `~/.claude/style.config.md`
   - If neither exists, warn: "No style config found. Designs will use skill defaults. Create ~/.claude/style.config.md for personalized output."
   - Extract: brand words, color preferences, motion philosophy, signature elements, anti-patterns

2. **Decide color mode** (lock this before any design work):
   - **Dark-only**: dev tools, terminals, creative tools, gaming, entertainment, products where dark IS the identity
   - **Both modes**: documentation, reading-heavy apps, productivity apps used 8+ hrs/day, diverse non-technical audience
   - **Light-only**: e-commerce, marketing, editorial, most SaaS dashboards
   - Log decision in `ai/design-progress.md` as `color_mode: dark-only | both | light-only`
   - Do NOT default to "both" -- it doubles the design surface. Only build both if the product type demands it.

3. **Check prerequisites**:
   - Does project exist? Is there a working directory?
   - For Phase 1: Does a scope/requirements doc exist? (warn if not, don't block)
   - For Phase 2+: Has Phase 1 been completed or explicitly skipped?

4. **Read design progress** (resume support):
   - Check `ai/design-progress.md` for prior state
   - If exists, report current phase and offer to continue

5. **Initialize tracking**:
   - Create `ai/design-progress.md` if it doesn't exist
   - Log start time and project name

6. **Load design knowledge** (optional, enhances output):
   - If you have design reference guides available, load them for typography, color, spacing, motion, and accessibility knowledge
   - The skill works without external guides but produces better results with them

**Output after Phase 0:**
```
Design Workflow: [project-name]
Style Config: [loaded from X | not found]
Color Mode: [dark-only | both | light-only] — [reason]
Current Phase: [starting fresh | resuming Phase N]
Flags: [--skip-state | none]

Ready to begin Phase 1: State Design
(Use --skip-state if this is a static page with no app state)
```

---

### Phase 1: State Design

**Gate:** None (first phase)
**Skip condition:** `--skip-state` flag or user confirms no app state needed

Execute `/state-design [project-name]`

When complete:
- Verify output exists at `ai/state-design.md` or equivalent
- Update `ai/design-progress.md`:
  ```
  phase_1: completed | skipped
  state_design_output: [path or "skipped - static page"]
  ```
- Proceed to Phase 2

---

### Phase 2: Creative (3 Proposals)

**Gate:** Phase 1 must be completed or skipped. Check `ai/design-progress.md`.
**If gate fails:** "Phase 1 (State Design) hasn't been completed. Run /state-design first or use --skip-state."

Before generating proposals, apply knowledge of:
- Typography: font scales, weight pairing, line height rules
- Color: palette construction, contrast, semantic color
- Spacing & Layout: spacing scale, layout patterns
- Motion & Animation: timing, easing, what to animate
- Personality: what makes designs feel human, not generic

Also load from style config:
- Brand words (set the tone for all 3 proposals)
- Color preferences (respect preferred/anti colors)
- Motion philosophy (match motion style)
- Signature elements (incorporate into proposals)
- Anti-patterns (avoid these on top of banned defaults)

Execute `/frontend-design new` (or `revamp` if redesigning existing UI)

The skill handles 3-proposal generation, DNA codes, banned defaults, etc.

When complete:
- Verify 3 proposal files exist in `./proposals/`
- Update `ai/design-progress.md`:
  ```
  phase_2: completed
  proposals: [proposal-1.html, proposal-2.html, proposal-3.html]
  dna_codes: [DNA-X-X-X-X-X, DNA-Y-Y-Y-Y-Y, DNA-Z-Z-Z-Z-Z]
  ```
- Present proposals to user

---

### Phase 3: Selection

**Gate:** Phase 2 must be completed. 3 proposals must exist.

Present the choice:
```
3 proposals generated. Pick your direction:

1. Proposal 1 (DNA-X-X-X-X-X) - [brief description]
2. Proposal 2 (DNA-Y-Y-Y-Y-Y) - [brief description]
3. Proposal 3 (DNA-Z-Z-Z-Z-Z) - [brief description]
4. Hybrid - combine elements from multiple proposals

Which direction? (pick a number or describe what you want)
```

When user selects:
- Update `ai/design-progress.md`:
  ```
  phase_3: completed
  selected: [proposal number or "hybrid: details"]
  ```
- If hybrid: document which elements from which proposals
- Build the selected/hybrid design as the production codebase
- Proceed to Phase 4

---

### Phase 4: Production Polish

**Gate:** Phase 3 must be completed. Selected design must be built.
**Skip condition:** `--polish-only` flag bypasses Phases 1-3 (assumes design already exists)

Apply knowledge of:
- Shadows & Depth: shadow values, layering, elevation
- Motion & Animation: spring physics, timing functions
- Dark Mode: if applicable
- Interactive Elements: state layers, animation timing, easing curves

Execute `/ui-revamp` (full 4-phase: audit, plan, implement, validate)

When complete:
- Verify audit passes
- Update `ai/design-progress.md`:
  ```
  phase_4: completed
  audit_result: [pass/fail]
  issues_fixed: [count]
  ```
- Proceed to Phase 5

---

### Phase 5: Final QA

**Gate:** Phase 4 must be completed.
**Skip condition:** `--qa-only` flag bypasses Phases 1-4 (assumes polished design exists)

Run full QA checklist covering:
- Typography (font sizes, weights, line heights, hierarchy)
- Contrast (WCAG AA minimum, text over backgrounds)
- Spacing (consistent scale, no magic numbers)
- Interactive (hover/focus/active states, transitions)
- Dark Mode (if applicable)
- Accessibility (focus management, ARIA, keyboard nav)

Execute `/frontend-design qa`

When complete:
- Update `ai/design-progress.md`:
  ```
  phase_5: completed
  qa_result: [APPROVED | NEEDS REVISION]
  ```
- If APPROVED: "Design complete. Ready to ship."
- If NEEDS REVISION: List remaining issues, loop back to Phase 4

---

## Progress File Format

`ai/design-progress.md`:
```markdown
# Design Progress: [project-name]

Started: [date]
Style Config: [path loaded]
Flags: [any flags used]

## Phase 1: State Design
Status: pending | completed | skipped
Output: [path]

## Phase 2: Creative (3 Proposals)
Status: pending | completed
Proposals: [list]
DNA Codes: [list]

## Phase 3: Selection
Status: pending | completed
Selected: [choice]

## Phase 4: Production Polish
Status: pending | completed
Audit Result: [pass/fail]

## Phase 5: Final QA
Status: pending | completed
QA Result: [APPROVED | NEEDS REVISION]
```

---

## Short-Circuit Flags

**`--skip-state`**: Skips Phase 1. Use for:
- Static marketing pages
- Simple landing pages
- Pages with no dynamic state

**`--polish-only`**: Jumps to Phase 4. Use when:
- You already have a design you like
- Skipping creative phase, just need production polish
- Coming back to polish after a break

**`--qa-only`**: Jumps to Phase 5. Use when:
- Polish is done, just need the final gate check
- Quick verification before shipping

---

## Resume Support

The orchestrator reads `ai/design-progress.md` on every run. If a phase is already completed, it skips ahead to the next pending phase. You never lose progress between sessions.

To restart from scratch: delete `ai/design-progress.md`.
