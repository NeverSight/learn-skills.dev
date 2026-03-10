---
name: ui-revamp
description: Transform vibe-coded UIs into production-quality interfaces. Use when revamping, redesigning, polishing, or improving any UI. Applies principles from Emil Kowalski (Linear), Rauno Freiberg (Vercel), Steve Schoger (Refactoring UI), and Sara Soueidan (Accessibility). Executes a four-phase process with automated auditing and enforcement.
---

# UI Revamp Skill

Transform amateur interfaces into production-quality experiences by systematically applying principles from the industry's best design engineers.

## Quick Start: 5-Minute Vibecode Detector

Run these checks first. If 3+ fail, the UI needs a full revamp:

```
[ ] Search CSS for "linear" in transitions → If found: FAIL
[ ] Search for "scale(0)" → If found: FAIL
[ ] Search for "transition: all" → If found: FAIL
[ ] Check button :active states → No feedback? FAIL
[ ] Count border-radius values → More than 2 unique? FAIL
[ ] Check icon set → Mixed filled/outlined? FAIL
[ ] Input font-size < 16px? → FAIL (iOS zoom bug)
[ ] Missing focus states on buttons? → FAIL
```

**Run automated audit**: `node ~/.claude/skills/ui-revamp/scripts/audit.js [path]`

---

## Four-Phase Process

**CRITICAL: Execute phases sequentially. Never skip Phase 2 approval.**

### Phase 1: Deep Audit

Understand before changing.

1. **Run Automated Audit**
   ```bash
   node ~/.claude/skills/ui-revamp/scripts/audit.js ./src
   ```

2. **Heuristic Evaluation**
   - See [reference/06-audit-phases.md](reference/06-audit-phases.md) for Nielsen's 10 heuristics
   - Rate each 0-4 (0=fine, 4=catastrophe)
   - Priority = Severity × Frequency × Impact

3. **Visual Inventory**
   - Document all unique border-radius values
   - Document all unique spacing values
   - List all font sizes in use
   - Note icon style consistency

4. **Document Findings**
   - Use [templates/audit-report.md](templates/audit-report.md)

### Phase 2: Plan & Approve

**STOP. Present findings before proceeding.**

1. Summarize top 10 issues by severity
2. Identify quick wins (high impact, low effort)
3. Propose implementation order

**Ask user**: "Should I proceed with this plan? Any adjustments needed?"

**Do NOT proceed to Phase 3 without explicit user approval.**

### Phase 3: Systematic Implementation

Execute in this order:

1. **Foundation** - Apply CSS reset, establish design tokens
   - See [reference/08-code-snippets.md](reference/08-code-snippets.md)
   - See [reference/04-visual-system.md](reference/04-visual-system.md)

2. **Fix Hard Rule Violations** - Non-negotiable rules
   - See [reference/01-hard-rules.md](reference/01-hard-rules.md)

3. **Apply Conditional Rules** - Context-dependent rules
   - See [reference/02-conditional-rules.md](reference/02-conditional-rules.md)

4. **Implement Animation System**
   - See [reference/03-animation-system.md](reference/03-animation-system.md)

5. **Accessibility Pass**
   - See [reference/05-accessibility.md](reference/05-accessibility.md)

### Phase 4: Quality Validation

1. **Run Automated Check**
   ```bash
   node ~/.claude/skills/ui-revamp/scripts/audit.js ./src
   ```
   All violations should be resolved.

2. **Visual Tests**
   - **Blur Test**: Apply 5-10px blur. Can you identify primary action, hierarchy, sections?
   - **Squint Test**: Clear focal point? Logical grouping? Balanced composition?

3. **Document Changes**
   - Use [templates/before-after.md](templates/before-after.md)

---

## Progress Tracker

**Copy this checklist and update as you work:**

```markdown
## UI Revamp Progress

### Phase 1: Audit
- [ ] Run automated audit script
- [ ] Complete heuristic evaluation (Nielsen's 10)
- [ ] Create visual inventory (radius, spacing, fonts, icons)
- [ ] Document top 10 issues with severity

### Phase 2: Plan (STOP - GET APPROVAL)
- [ ] Present findings summary to user
- [ ] Propose implementation order
- [ ] Get explicit user approval to proceed

### Phase 3: Implement
- [ ] Apply foundation (CSS reset, design tokens)
- [ ] Fix all hard rule violations
- [ ] Apply conditional rules where appropriate
- [ ] Implement animation system
- [ ] Complete accessibility pass
- [ ] Fix Tailwind/shadcn specifics (if applicable)

### Phase 4: Validate
- [ ] Run automated audit (should pass)
- [ ] Pass blur test
- [ ] Pass squint test
- [ ] Document before/after for significant changes
```

---

## Reference Files

**Rules & Requirements:**
- [01-hard-rules.md](reference/01-hard-rules.md) - 42 non-negotiable rules (MUST follow)
- [02-conditional-rules.md](reference/02-conditional-rules.md) - 37 context-dependent rules
- [05-accessibility.md](reference/05-accessibility.md) - WCAG requirements

**Systems & Patterns:**
- [03-animation-system.md](reference/03-animation-system.md) - Timing, easing, springs
- [04-visual-system.md](reference/04-visual-system.md) - Typography, colors, spacing
- [08-code-snippets.md](reference/08-code-snippets.md) - Copy-paste CSS/JS patterns

**Checklists & Frameworks:**
- [06-audit-phases.md](reference/06-audit-phases.md) - All 5 audit phase checklists
- [07-decision-frameworks.md](reference/07-decision-frameworks.md) - When to animate, etc.

**Tech-Specific:**
- [09-tailwind-patterns.md](reference/09-tailwind-patterns.md) - Tailwind class mappings
- [10-shadcn-guide.md](reference/10-shadcn-guide.md) - shadcn/ui modifications

---

## Decision Quick Reference

### Should I Animate This?

```
Keyboard-triggered? → NO animation
Used 100+ times/day? → NO animation
Used hourly? → MINIMAL (100-150ms)
Used daily? → PURPOSEFUL (150-200ms)
Used rarely? → DELIGHTFUL (300ms+)
```

### Animation Durations

| Element | Duration | Easing |
|---------|----------|--------|
| Button press | 150ms | ease-out |
| Modal open | 200ms | ease-out or spring |
| Modal close | 150ms | ease-in or instant |
| Dropdown | 180ms | ease-out |
| Tooltip | 150ms | ease-out |
| Page transition | 250ms | ease-out |

### Never Do

1. Linear easing on UI elements
2. Scale from 0 (use 0.93+ minimum)
3. Animate keyboard actions
4. Animate theme toggles
5. Duration >300ms for functional UI
6. Bounce on serious UI
7. Multiple primary button styles per view

---

## Success Criteria

The revamp is complete when:

- [ ] Automated audit passes with 0 violations
- [ ] Blur test passes (hierarchy visible)
- [ ] No linear easing anywhere
- [ ] No scale(0) animations
- [ ] Max 2 border-radius values
- [ ] Spacing uses consistent scale
- [ ] Touch targets ≥44px
- [ ] Focus states visible on all interactive elements
- [ ] Loading, empty, and error states exist

---

## Knowledge Base (Optional)

If the user has a design knowledge base (e.g. `~/System/guides/DESIGN_MASTERY.md` or similar), read targeted sections:

| Phase | Topics to Load |
|-------|---------------|
| Phase 1: Audit | Quick Reference (use as audit checklist) |
| Phase 3: Implementation | Shadows & Depth, Motion & Animation, Dark Mode (if applicable) |
| Phase 4: Validation | Quick Reference (final check) |

Don't read an entire guide. Load only the sections relevant to the current phase. The skill works without external guides but produces better results with them.

---

## Personal Style (style.config.md)

Before auditing, check for a style config:
1. Project-level: `ai/style.config.md` (takes priority)
2. User-level: `~/.claude/style.config.md`

If found, respect the user's intentional choices during audit:
- **Signature elements** are intentional, not bugs. Don't "fix" personality.
- **Brand words** tell you the intended tone. Don't push toward generic.
- **Anti-patterns** flag things the user hates. Treat as hard rules.
- If something looks like a violation but matches the style config, leave it alone.

---

## Relationship to /design Orchestrator

This skill is Phase 4 (Production Polish) of the `/design` workflow.
- When called via `/design`, the orchestrator handles knowledge loading and style config
- When called standalone, this skill loads them itself
- This is the full 4-phase audit. For a lighter pass, use `/frontend-design polish`

---

## Attribution

Principles from:
- **Emil Kowalski** (Linear) - Animation & Motion
- **Rauno Freiberg** (Vercel) - Interaction Design & Craft
- **Steve Schoger** (Refactoring UI) - Visual Design Tactics
- **Sara Soueidan** - Accessibility
- **Dan Saffer** - Microinteractions

*"The details are not the details. They make the design." -- Charles Eames*
