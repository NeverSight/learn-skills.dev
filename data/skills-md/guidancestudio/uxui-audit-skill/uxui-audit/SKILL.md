---
name: uxui-audit
description: Full-spectrum UX/UI audit of a rendered web interface (not its source). Captures screenshots of any app — Playwright, a Playwright MCP, or screenshots you provide — then audits them across thirteen dimensions (Nielsen usability, WCAG accessibility, visual design, content & language/i18n, state coverage, responsive, information architecture, interaction design, user journey, cognitive load & onboarding, trust & credibility, error prevention & recovery, performance perception), assigns a 0–4 severity per finding, and emits a triageable report plus optional regression guards. Use when the user asks to "audit the UX/UI", "UX audit", "UI review", "heuristic evaluation", "design review", "audit the interface/screens", or "check the UX" of a running app. Framework-agnostic. Uses the agent's native image input if the model is multimodal; for non-multimodal agents, route screenshots through an available image-description MCP tool (see workflow.md Analyze phase). Capture needs Node + Playwright, or you supply PNGs.
---

# uxui-audit — Router

This skill audits rendered screenshots across 13 dimensions — Nielsen usability, WCAG accessibility, visual design, content/i18n, states, responsive, IA, interaction, journey, cognitive load, trust, error recovery, and performance perception — assigning 0–4 severity per finding and tying every finding to a screenshot.

## When to invoke

Trigger keywords: "UX audit", "UI audit", "heuristic evaluation", "design review", "review the UI/UX", "audit the interface", "check the UX", "a11y review".

Do **not** use this for source-level audits or for
*building* UI (use a frontend-design skill). This reviews the rendered result.

## The five phases
1. **Scope** — surfaces, viewports, target audience, UI language. See `workflow.md`.
2. **Capture** — screenshots per surface × viewport × state. See `capture.md`.
3. **Analyze** — walk 13 dimensions per screenshot. See `dimensions.md`.
4. **Report** — triageable findings per `report-template.md`.
5. **Guard** *(optional)* — regression guards. See `regression-guards.md`.

## The thirteen dimensions (full catalogue in `dimensions.md`)

| # | Dimension | What it audits |
|---|---|---|
| 1 | **Usability** | Nielsen's 10 heuristics |
| 2 | **Accessibility** | WCAG 2.2 POUR, contrast, target size, semantics |
| 3 | **Visual Design** | hierarchy, spacing, typography, colour semantics, motion |
| 4 | **Content & Language** | i18n consistency, no jargon leak, microcopy, UX writing |
| 5 | **State & Data** | empty/loading/error/first-run/zero-one-many/overflow |
| 6 | **Responsive** | per-breakpoint layout integrity, touch ergonomics |
| 7 | **Information Architecture** | nav structure, labeling, findability, breadcrumbs |
| 8 | **Interaction Design** | affordances, feedback, click-target sizing, gestures, form UX |
| 9 | **User Journey / Flow** | multi-screen coherence, back-navigation, dead ends |
| 10 | **Cognitive Load & Onboarding** | density, chunking, progressive disclosure, first-run guidance |
| 11 | **Trust & Credibility** | social proof, dark patterns, security indicators, transparency |
| 12 | **Error Prevention & Recovery** | confirmations, undo, error message actionability, degradation |
| 13 | **Performance Perception** | skeleton/loading UX, perceived speed, layout shift, optimistic UI |

## Severity (Nielsen 0–4)
`0` not a problem · `1` cosmetic · `2` minor · `3` major · `4` catastrophic. Emoji: 4🔴/3🟡/1-2🟢/0—. Full rubric in `dimensions.md`.

## Honesty rules
Every finding cites a screenshot + concrete fix + includes strengths. Full conventions in `report-template.md`.
