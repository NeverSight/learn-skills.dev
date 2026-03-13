---
name: design-evaluation-audit
description: Use when systematically evaluating existing designs for cognitive alignment, conducting design reviews or critiques, diagnosing usability issues, quality assurance before launch, or choosing between design alternatives with objective criteria. Invoke when user mentions design review, design critique, evaluate design, audit visualization, checklist, cognitive assessment, or usability evaluation.
---

# Design Evaluation & Audit

## Table of Contents

- [Read This First](#read-this-first)
- [Design Review Workflow](#design-review-workflow)
- [Path Selection Menu](#path-selection-menu)
  - [Path 1: Run Cognitive Design Checklist](#path-1-run-cognitive-design-checklist)
  - [Path 2: Run Visualization Audit](#path-2-run-visualization-audit)
  - [Path 3: Combined Review](#path-3-combined-review)
- [Quick Reference](#quick-reference)
- [Guardrails](#guardrails)

---

## Read This First

### What This Skill Does

This skill provides **systematic evaluation tools** for assessing existing designs against cognitive science principles. It gives you repeatable checklists, scoring rubrics, and prioritized fix recommendations.

**Core principle:** Good evaluation is systematic, not subjective — every dimension gets checked, every finding gets severity-classified, every fix gets prioritized.

### Why It Matters

**Common problems this addresses:**
- Design reviews that miss critical issues because they rely on gut feeling
- Teams disagreeing on what to fix first without objective framework
- Usability problems shipping because no one checked systematically
- Visualizations that mislead because integrity was never audited

**How this helps:**
- Covers all cognitive dimensions (visibility, hierarchy, chunking, memory, feedback, consistency, scanning, simplicity)
- Scores visualizations on 4 independent criteria (Clarity, Efficiency, Integrity, Aesthetics)
- Classifies findings by severity (CRITICAL/HIGH/MEDIUM/LOW)
- Produces actionable fix recommendations with clear priority order

### When to Use This Skill

**Use this skill when:**
- ✓ Conducting design reviews or critiques
- ✓ Evaluating designs for cognitive alignment before iteration
- ✓ Quality assurance before launch or publication
- ✓ Diagnosing why a design "feels off"
- ✓ Choosing between design alternatives with objective criteria
- ✓ Auditing data visualizations for quality

**Do NOT use for:**
- ✗ Creating new designs from scratch (use `cognitive-design`)
- ✗ Learning cognitive theory (use `cognitive-design` Path 1)
- ✗ Detecting misleading visualizations (use `cognitive-fallacies-guard`)
- ✗ Technical implementation (coding, tooling)

---

## Design Review Workflow

**Time:** 30-90 minutes depending on scope

**Copy this checklist and track your progress:**

```
Design Evaluation Progress:
- [ ] Step 1: Systematic Assessment
- [ ] Step 2: Visualization Quality Audit (if applicable)
- [ ] Step 3: Severity Classification & Prioritization
- [ ] Step 4: Fix Recommendations
```

### Step 1: Systematic Assessment

Apply the Cognitive Design Checklist across all 8 dimensions: Visibility, Visual Hierarchy, Chunking, Simplicity, Memory Support, Feedback, Consistency, Scanning Patterns. Check every item. Record pass/fail for each dimension with specific evidence.

**Resource:** [Cognitive Design Checklist](resources/cognitive-checklist.md)

### Step 2: Visualization Quality Audit (if applicable)

If the design includes data visualizations, apply the 4-Criteria Visualization Audit. Score each criterion 1-5: Clarity, Efficiency, Integrity, Aesthetics. Calculate average and identify weakest dimension.

**Resource:** [Visualization Audit Framework](resources/visualization-audit.md)

### Step 3: Severity Classification & Prioritization

Classify every finding by severity:
- **CRITICAL:** Integrity violations, accessibility failures, users cannot complete core tasks. Fix immediately.
- **HIGH:** Clarity/efficiency issues preventing use, missing feedback for critical actions, working memory overload (>10 ungrouped items). Fix before launch.
- **MEDIUM:** Suboptimal patterns, aesthetic issues, minor inconsistencies. Fix in next iteration.
- **LOW:** Minor optimizations, polish items. Fix when convenient.

**Priority rule:** Fix foundation-first — perception before coherence, integrity before aesthetics, critical before high.

### Step 4: Fix Recommendations

For each finding, document:
1. **What is wrong** — specific description with evidence
2. **Why it matters** — which cognitive principle is violated
3. **How to fix** — concrete, actionable recommendation
4. **Expected outcome** — what improves after the fix
5. **Effort estimate** — quick fix (minutes), moderate (hours), significant (days)

Verify fixes don't harm other dimensions.

---

## Path Selection Menu

### Path 1: Run Cognitive Design Checklist

**Choose this when:** Evaluating any interface, layout, content page, form, or general design.

**What you'll get:** Pass/fail across 8 cognitive dimensions, test methods, common failures, severity-classified findings.

**Time:** 20-40 minutes

**→ [Go to Cognitive Design Checklist](resources/cognitive-checklist.md)**

---

### Path 2: Run Visualization Audit

**Choose this when:** Evaluating data visualizations — charts, graphs, dashboards, infographics.

**What you'll get:** 1-5 scores on Clarity, Efficiency, Integrity, Aesthetics with pass/fail threshold.

**Time:** 15-30 minutes per visualization

**→ [Go to Visualization Audit Framework](resources/visualization-audit.md)**

---

### Path 3: Combined Review

**Choose this when:** Comprehensive review covering both interface elements and data visualizations.

**Process:** Run Cognitive Checklist first, then Visualization Audit on each data component, merge findings, produce unified fix list.

**Time:** 45-90 minutes

**→ Start with [Cognitive Checklist](resources/cognitive-checklist.md), then [Visualization Audit](resources/visualization-audit.md)**

---

## Quick Reference

### 3-Question Rapid Check

**1. Attention** — "Is it obvious what to look at first?"
- If NO: hierarchy and visibility issues

**2. Memory** — "Is the user required to remember anything that could be shown?"
- If NO: memory support and chunking issues

**3. Clarity** — "Can someone unfamiliar understand in 5 seconds?"
- If NO: simplicity and comprehension issues

All YES = likely cognitively sound. Any NO = run full checklist on the failing area.

---

## Guardrails

**This skill does NOT:** Create designs, teach theory, provide domain guidance, replace user testing, or cover full accessibility compliance.

**This skill DOES:** Provide systematic evaluation against cognitive principles, classify findings by severity, produce prioritized fix recommendations, and score visualization quality.
