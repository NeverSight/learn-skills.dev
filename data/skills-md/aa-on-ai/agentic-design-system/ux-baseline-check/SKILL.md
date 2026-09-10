---
name: ux-baseline-check
description: >
  Core pack — always active for visual work. Enforces UX quality standards on any
  screen, flow, form, or dashboard. Ensures nothing ships with missing states.
  Auto-activates alongside design-review for all frontend work.
---

# UX Baseline Check

## Core Pack — Always Active
This is a core skill. Apply it on ALL visual and frontend work alongside design-review.

Every screen ships with ALL states covered. No exceptions. This is the minimum bar.

## The State Inventory

Before any page or component is "done", verify each applicable state exists:

### 1. Data States
- [ ] **Empty** — no data yet. Helpful message + clear CTA, not a blank screen
- [ ] **Loading** — skeleton, spinner, or shimmer. Never a white flash
- [ ] **Loaded** — the happy path, obviously
- [ ] **Error** — API failure, network issue. User-friendly message + retry action
- [ ] **Partial** — some data loaded, some failed. Don't hide what works
- [ ] **Long content** — what happens with 200 items? 2000-character names? Test it

### 2. Interaction States
- [ ] **Hover** — every clickable element has a hover state
- [ ] **Focus** — keyboard navigation works, focus rings visible
- [ ] **Active/pressed** — buttons respond to clicks visually
- [ ] **Disabled** — grayed out with clear reason why (tooltip or helper text)
- [ ] **Selected** — multi-select, current tab, active filter all visually distinct
- [ ] **Adjacent-action consistency** — when a state is read-only, disabled, offline,
  permission-limited, or destructive, inspect every nearby primary, secondary, toolbar, and inline
  action. Remove, relabel, or visibly explain contradictions; use native `disabled` semantics when
  an inactive control remains visible, and preserve active actions in unaffected states.

### 3. Form States
- [ ] **Validation** — inline errors on blur, not just on submit
- [ ] **Required fields** — clearly marked
- [ ] **Success feedback** — user knows their action worked (toast, inline, redirect)
- [ ] **Destructive confirmation** — delete/remove actions require confirmation
- [ ] **Autofill** — doesn't break layout when browser autofills

### 4. Responsive
- [ ] **Mobile (375px)** — usable, not just visible. Touch targets ≥48px with ≥8px spacing between them
- [ ] **Tablet (768px)** — layout adapts, not just shrinks
- [ ] **Desktop (1280px)** — the primary target, looks intentional
- [ ] **Wide (1800px+)** — content doesn't stretch absurdly. Max-width or centered

### 5. Accessibility
- [ ] **Keyboard nav** — can reach all interactive elements with Tab
- [ ] **Screen reader** — semantic HTML, aria-labels on icons, alt text on images
- [ ] **Color contrast** — 4.5:1 minimum for text (use WebAIM checker)
- [ ] **No color-only indicators** — don't rely solely on red/green for status

### 6. Edge Cases
- [ ] **First-time user** — onboarding or empty state guides them
- [ ] **Permission denied** — user sees why they can't access, not a broken page
- [ ] **Stale data** — timestamps or refresh indicators when data might be outdated
- [ ] **Concurrent edits** — what happens if two people edit the same thing?

## How to Use

Run this checklist AFTER the feature works but BEFORE design review. For each missing state, either:
1. **Implement it** (preferred)
2. **Document it as a known gap** and tell the user explicitly

Never silently skip a state. If it's intentionally deferred, say so.

## Quick Pass vs Full Pass

**Quick pass** (components, small features): States 1-2 only
**Full pass** (pages, flows, shipping features): All 6 sections

## The Test

Ask yourself: "What happens if the network is slow, the data is weird, the user is on a phone, or they're using a keyboard?" If you don't know, you haven't finished.
