---
name: design-critique
description: Produces a structured critique of a screenshot, URL, Figma frame or UI code, covering visual hierarchy, alignment, spacing rhythm, contrast, consistency, affordances and the Nielsen usability heuristics, and returns prioritized P0, P1 and P2 fixes with exact values and the reason for each. Use when asked to review, critique or give feedback on a design, or to explain what feels off about a screen. Not for a full WCAG audit; use accessibility-audit.
---

# Design Critique

Turns a screen into a ranked, implementable list of fixes. Every finding names the element, the exact change (values, not adjectives) and the principle behind it, so it can be built without a follow-up conversation.

## When to use
- A screenshot, URL, Figma frame or component code arrives with "review this", "what do you think" or "why does this look off"
- A landing page, dashboard or flow is about to ship and needs a second pass
- Two variants need comparing with reasons beyond taste
- A design feels busy, flat or amateur and the cause is unclear
- A redesign was implemented and needs checking against its original intent

## Workflow
1. Establish context: what the screen is for, its primary action, platform and viewport. If the primary action is unknown and not inferable, ask one question; otherwise state the assumption and continue.
2. First-glance pass: list what the eye hits 1st, 2nd and 3rd. Blur the image or zoom out to 25% and check whether that order matches the intended priority.
3. Structure pass: count distinct left edges per section, check grid adherence, extract spacing values and test them against a 4/8 scale, check grouping by proximity.
4. Type and color pass: count font sizes and weights, estimate line length, compute contrast ratios for text and key UI, note how often the accent appears.
5. Interaction pass: affordances (do clickable things look clickable), target sizes, and presence of hover, focus, disabled, loading, empty and error states.
6. Heuristic pass: check Nielsen's 10 (listed below) and record only violations, each with evidence.
7. Prioritize, write each fix with values, cluster duplicates, and list 2–3 strengths to preserve.
8. If code was provided, offer a patch for P0 and P1 items.

## Rules
**Priority**
- P0: blocks or derails the primary task, invites likely errors, makes interactive elements unrecognizable, or fails WCAG AA contrast (text under 4.5:1; large text, ≥24px regular or ≥18.66px bold, under 3:1).
- P1: weakens hierarchy, comprehension or trust; visible inconsistency across the screen.
- P2: polish such as rhythm, optical alignment, icon weight and micro-copy.

**Hierarchy and layout**
- One primary action per view, and it is the highest-contrast interactive element. Two equally loud buttons is a P1: demote one to secondary or ghost.
- More than 6 font sizes or 3 weights on one screen is an inconsistency finding.
- Spacing inside a group must be smaller than spacing between groups; off-scale values (13px, 27px) get normalized to the 4/8 scale.
- Body text ≥16px on web; line length 45–75 characters.
- Each unintended extra alignment edge in a section is a finding.

**Interaction**
- Targets ≥24×24 CSS px (WCAG 2.5.8); recommend 44×44 for touch.
- Input borders, meaningful icons and focus indicators need ≥3:1 against adjacent colors.
- Every interactive element needs a visible focus state.

**Writing fixes**
- A fix states element, problem, change with values, and rationale. "Improve contrast" is not a fix; "Body text #9CA3AF on #FFFFFF is 2.5:1; change to #6B7280 (4.8:1)" is.
- Cite heuristics by number and name. Critique the work, not the person; no taste-only statements.
- Cap at 15 findings; cluster repeats ("all 6 pricing cards").

**Nielsen's 10 heuristics**
- H1 Visibility of system status · H2 Match between system and the real world · H3 User control and freedom · H4 Consistency and standards · H5 Error prevention
- H6 Recognition rather than recall · H7 Flexibility and efficiency of use · H8 Aesthetic and minimalist design · H9 Help users recognize, diagnose and recover from errors · H10 Help and documentation

## Output
- Verdict: 2–3 sentences naming the overall state and the single biggest lever.
- Findings grouped under P0, P1 and P2 as a table: # | Element | Issue | Fix (exact values) | Why (principle or heuristic).
- Keep: 2–3 strengths that must survive the revision.
- Optional patch for P0 and P1 in the project's stack: semantic HTML + CSS custom properties, or React + Tailwind if already used. No new dependencies.
- When only code or only an image was available, mark which findings are inferred rather than observed.

## Avoid
- Generic statements without location and values ("spacing feels off")
- Reciting all 10 heuristics with "passes" filler
- Redesigning from scratch when targeted fixes solve it; if a new direction is truly needed, hand off to distinctive-ui
- Ranking a 2px misalignment alongside an unreadable call to action
- Contrast claims without computed ratios
- Recommending trend effects (gradients, glassmorphism) as fixes for hierarchy problems

## Final check
- [ ] Primary action identified and the hierarchy judged against it
- [ ] Every finding has element, value-level fix and rationale
- [ ] P0 items genuinely block tasks or fail AA
- [ ] Contrast findings include the measured ratio and a passing replacement
- [ ] Duplicates clustered; 15 findings or fewer
- [ ] Strengths listed
- [ ] Deeper issues routed: accessibility-audit for WCAG, ui-states for missing states, layout-spacing for spacing systems, typography-system for the type scale
