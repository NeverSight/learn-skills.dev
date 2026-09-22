---
name: experience-design-validate
description: "Use this skill to run a visual-craft audit of a rendered UI and produce an evidence-grounded Craft Report across Useful, Usable, Reliable, Coherent, and Well-Crafted. Invoke it for craft audits, visual critiques, design comparisons, felt-quality reviews, or visual-craft readiness checks on screenshots (.png, .jpg, .jpeg, .webp, .gif), Figma frames, rendered prototypes, and live URLs. Do not use it for source-code review, SLDS compliance (use design-systems-slds-validate), or accessibility compliance (use experience-accessibility-validate)."
metadata:
  version: "1.0"
  domains: ["Experience"]
  relatedSkills:
    - "design-systems-slds-validate"
    - "experience-accessibility-validate"
    - "experience-lwc-generate"
    - "experience-lwc-security-validate"
---

# Experience Design Validate

Evaluate the visual craft of rendered software: what the eye sees and the felt quality those visible decisions create. Judge relationships, hierarchy, restraint, consistency, and care rather than CSS, tokens, or implementation technique.

This is a **visual-craft-only** audit. It does not establish WCAG conformance, keyboard or screen-reader support, behavioral usability, implementation quality, or production release readiness. Route accessibility compliance to `experience-accessibility-validate` and SLDS compliance to `design-systems-slds-validate`.

## Use and boundaries

Use this skill to:

- Critique visual craft at a design checkpoint.
- Explain why a rendered design feels considered, cramped, calm, fragmented, or delightful.
- Compare the craft of two or more designs solving the same brief.
- Identify design moves that would lift a visible experience from good to great.

Do not use this skill for:

- Implementation or code review. For LWC generation or security review, use `experience-lwc-generate` or `experience-lwc-security-validate` as appropriate.
- Accessibility compliance, including WCAG, screen-reader, keyboard, or focus-order validation. Use `experience-accessibility-validate`.
- SLDS design-token compliance. Use `design-systems-slds-validate`.
- Claims about real-user behavior. Recommend a usability study when impact depends on behavior rather than visible evidence.

## Visual evidence contract

Rendered pixels are mandatory. Prefer screenshots because they preserve the exact evidence reviewed.

1. **Screenshots:** use supplied full-page or region captures directly.
2. **Live URL:** if browser capability is available, open the URL, exercise only the relevant paths, capture screenshots, and retain the URL and viewport as evidence. Otherwise ask for screenshots.
3. **Figma:** if Figma capability is available, fetch or export the named rendered frames. Treat a frame as static unless prototype behavior is actually exercised. Otherwise ask for frame exports or screenshots.
4. **Screen recording or interactive prototype:** inspect observable transitions and capture representative frames when tooling supports it.
5. **Source code, design descriptions, or inaccessible links:** do not infer the rendered result. Render with available capability; otherwise request screenshots.

If no rendered pixels are available:

- **Interactive run:** ask the user for screenshots or another rendered artifact and pause the audit.
- **Non-interactive run:** return status `INSUFFICIENT_VISUAL_EVIDENCE` with a short statement of the missing artifact. Do not score, assign a verdict, create findings, or imply readiness.

### Evidence modes

Declare one mode before analysis:

| Mode | What it can support | What it cannot support |
|---|---|---|
| `STATIC_VISUAL` | Visible hierarchy, spacing, typography, color, density, composition, consistency, and the visible treatment of the captured moment | Interaction behavior, transitions between states, responsive adaptation beyond captured viewports, latency, runtime performance, or unseen states |
| `MULTI_VIEW_STATIC` | Static visual evidence across supplied screens, states, or viewport captures, including cross-screen coherence | The behavior connecting captures, timing, input response, runtime performance, or states not shown |
| `DYNAMIC_VISUAL` | Static qualities plus behavior directly exercised or recorded: interaction feedback, transitions, state changes, and perceived performance | Unexercised paths, unrecorded states, accessibility compliance, or measured performance beyond what was observed |

A static screenshot of a loading, error, or empty state supports critique of that state's **visible treatment only**. It does not substantiate state coverage, transition behavior, or performance. Never lower a score because an unobserved state or behavior was not supplied; mark that coverage `INSUFFICIENT_EVIDENCE` instead.

## Five dimensions

| Dimension | Felt question |
|---|---|
| **Useful** | Does the visible content earn the space and attention it occupies? |
| **Usable** | Does the visible hierarchy and affordance make the intended path feel obvious? |
| **Reliable** | Do the observed states and feedback make the experience feel predictable? |
| **Coherent** | Does the visible experience feel made by one team with one taste? |
| **Well-Crafted** | Does the visible design feel precise, considered, and delightful? |

Use a 1-10 score only when the available evidence adequately covers a dimension. Use `INSUFFICIENT_EVIDENCE` when an applicable dimension cannot be supported. Use `N/A` only when the dimension or topic genuinely does not apply, never merely because evidence is missing.

Read `references/scoring-rubric.md` for scoring anchors, verdict rules, severity definitions, and the complete report contract.

## Craft lens

Ask whether the rendered experience feels:

- **Breathable:** space structures the composition and gives the eye room.
- **Approachable:** the intended path is visually obvious without explanation.
- **Inviting:** visible states encourage exploration rather than present dead ends.
- **Considered:** repeated decisions form a system rather than an accumulation.
- **Quiet:** hierarchy is calm; few elements compete to be primary.
- **Delightful:** detail and personality are purposeful, not ornamental noise.
- **Confident:** the design has a point of view and avoids unnecessary hedging.

## Audit workflow

Follow this order:

1. Establish the evidence mode and inventory every supplied or captured artifact.
2. If no rendered pixels exist, follow the insufficient-visual-evidence behavior and stop.
3. Look before consulting rules. Record up to three honest first impressions for each design.
4. Build the coverage and relevance ledger. For every dimension and reference topic, record `SCORED`, `N/A`, or `INSUFFICIENT_EVIDENCE`, the evidence mode, and a concise reason.
5. Load `references/craft.md`, `references/scoring-rubric.md`, and `references/visual-system.md`. Load only conditional references whose topic is both relevant and observable in the evidence mode.
6. Score only supported dimensions. Select the **highest anchor whose applicable, observable criteria are fully supported**; use an odd score only when evidence clearly exceeds that anchor without fully supporting the next.
7. Write findings. Cap findings at five per dimension and deduplicate cross-dimensional root causes.
8. Write the Craft Report, including the ledger and evidence limitations.

## Progressive disclosure

Always load:

- `references/scoring-rubric.md`: scoring, coverage, severity, verdict, and report schema.
- `references/craft.md`: felt qualities of considered work.
- `references/visual-system.md`: visible layout, typography, color, and surfaces.

Load only when relevant **and observable**:

| Reference | Evidence needed |
|---|---|
| `references/components.md` | Visible buttons, inputs, modals, lists, tables, or feedback components |
| `references/navigation.md` | Visible navigation, tabs, breadcrumbs, search, or wayfinding |
| `references/responsive.md` | Captures from multiple viewports or directly exercised resizing |
| `references/forms-flows.md` | Multiple visible steps or directly exercised form behavior |
| `references/data.md` | Visible charts, dashboards, metrics, filters, results, or tables |
| `references/records.md` | Visible records, detail pages, status, metadata, or collaboration |
| `references/ai.md` | Visible AI, agent, chat, citations, or model output |
| `references/trust.md` | Visible auth, privacy, consent, permissions, or destructive settings |
| `references/usability.md` | Visible task structure; do not infer behavioral usability |
| `references/interaction.md` | `DYNAMIC_VISUAL` evidence of interaction or motion |
| `references/state.md` | `DYNAMIC_VISUAL` state transitions; static state captures support appearance only |
| `references/performance.md` | `DYNAMIC_VISUAL` evidence of timing, latency, or layout stability |

## Finding voice

Speak at the felt level and anchor claims to visible evidence.

Good: "The toolbar feels overworked; too many controls compete for attention, so the eye cannot find the primary action."

Wrong scope: "Three button classes use inconsistent spacing tokens." That belongs in implementation or SLDS review.

Each finding must include `severity`, `primary_dimension`, optional `related_dimensions`, `location`, `problem`, `why_it_weakens_craft`, `what_better_looks_like`, and `fix`. When one problem appears in three or more places, create one finding with a count and representative location.

## Comparative audits

Audit each design independently with the same evidence requirements and rubric. The report must include:

- Per-design evidence mode, coverage ledger, first impressions, dimension scores, evidence, and gap to the next supported level.
- A side-by-side comparison table that preserves `N/A` and `INSUFFICIENT_EVIDENCE` rather than forcing numeric comparisons.
- A result of `A_HIGHER_CRAFT`, `B_HIGHER_CRAFT`, `TIE`, or `MIXED`. Use `MIXED` when leadership varies by dimension or evidence coverage prevents an overall ranking.
- Differentiating dimensions, concrete craft moves each design makes better, and improvements each could borrow without copying.

Do not crown a winner when the evidence supports a tie or mixed outcome.

## Output

If the user explicitly supplies an output path, write there exactly; that path overrides the naming convention. Otherwise use `YYYY-MM-DD-<target-slug>-craft-audit-<VERDICT>.md`, with uppercase `PASS`, `WARN`, `FAIL`, or `LIMITED`.

The report must make its scope explicit: verdicts and readiness implications cover **visual craft only**, not accessibility, functional correctness, measured performance, or production release approval.

Recommendations and cross-cutting patterns each contain **zero to five** items. Include only evidence-backed, useful entries; never add filler to reach a quota. End with the fix prompt defined in `references/scoring-rubric.md` only when at least one actionable recommendation exists.

## Core principles

1. **Pixels first.** No rendered evidence means no visual-craft audit.
2. **Eye first, rules second.** Record first impressions before rubric analysis.
3. **Evidence bounds claims.** Unobserved behavior is unknown, not defective.
4. **Felt level, not implementation level.** Describe visual experience, not code.
5. **Teach while auditing.** Explain why each finding matters and what better feels like.
6. **Severity over volume.** A few sharp findings beat a padded checklist.
