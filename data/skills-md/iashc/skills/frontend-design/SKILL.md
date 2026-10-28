---
name: frontend-design
description: >-
  Design, implement, redesign, or visually review frontend experiences when a
  task materially concerns visual hierarchy, layout, responsive behavior, or
  interaction design. Do not use for backend, API, infrastructure, or
  frontend logic work without a material design impact.
license: MIT
metadata:
  author: Ash Li
  version: '2026-08-23'
---

# Frontend Design

Create frontend experiences that fit their users, domain, and actual work. Use
a deliberate visual direction without replacing an established product
language or expanding the user's request.

## Choose the Mode

- For design, implementation, or redesign, read and follow applicable project
  instructions. Check the user's requirements, `DESIGN.md`, and the existing
  design system and conventions before changing the interface. Preserve the
  current product language unless the user requests a new direction.
- For review-only work, report concrete defects and their user impact without
  changing the implementation. Separate usability, responsive, accessibility,
  and consistency problems from subjective preferences.
- Infer missing details from the request and repository when one direction is
  clearly supported. Ask only when plausible choices would materially change
  the result.

## Fit the Product

- Identify the audience, primary task, content hierarchy, product domain, and
  usage frequency before choosing the layout and visual language.
- Put the usable experience first for applications, tools, and games. Build a
  marketing landing page only when the request calls for one. Favor scanning,
  comparison, and predictable repeated actions in operational products; allow
  more expression where atmosphere is part of the experience.
- Complete only the requested, reachable workflows and their meaningful
  interaction and system states. Do not invent backend behavior or unrelated
  flows.
- Keep copy focused on the user's task. Include onboarding, shortcut guidance,
  or contextual help when it genuinely improves use; omit filler that narrates
  obvious controls, implementation details, or decorative choices.

## Design the Interface

- Use semantic, accessible controls that match the action. Use swatches for a
  finite color set, a color picker for arbitrary colors, and a text value when
  precise entry is required. Prefer familiar controls and label ambiguous
  icons.
- Reuse existing components, tokens, icons, and assets. Add or obtain resources
  only when necessary for the requested design and within the task scope; do
  not add a dependency that duplicates an adequate existing capability.
- Give every visual boundary a purpose. Avoid nested cards, floating-card page
  sections, or oversized headings that weaken hierarchy. Do not substitute
  decorative gradients, excessive rounding, or card grids for useful content
  and structure.
- Choose a deliberate palette with clear roles, sufficient contrast, and brand
  fit instead of applying a familiar generated-UI style without a reason.
- On subject-led pages, make the subject clear early. If a hero has a primary
  next step, make it clear using the composition that best serves the content.
  Use relevant media when it improves understanding, and keep the subject
  recognizable when users need to inspect it. Preserve aspect ratio,
  legibility, and fallback behavior.
- Reuse user-provided or project-authorized brand assets. From other
  references, extract design principles without copying protected identity.
- Do not make a page appear finished or non-scrollable while essential content
  continues below.

## Support Responsive and Accessible Use

- Use layout constraints, aspect ratios, and bounded sizing to keep controls,
  media, and text stable across supported viewports. Allow text to wrap and
  preserve long words without clipping or unbounded viewport-based type.
- Prevent overflow, overlap, clipped controls, unexpected layout shifts, and
  unusable touch targets, including with dynamic content and longer text.
- Ensure semantic structure, keyboard access, visible focus, readable contrast,
  text zoom, and reduced-motion support. Visual polish must not weaken
  accessibility.
- For canvas, games, 3D, or animation, prioritize the actual experience and
  reuse mature project capabilities. Do not add an engine or reimplement a
  domain system solely for visual work, and do not confine the primary
  experience to an ornamental preview card.

## Validate Proportionately

- Reuse the project's running service and documented workflow. When the user
  needs access, verify and provide a working URL and leave the server running.
  Otherwise stop temporary servers after validation. Use another port when
  necessary; for a self-contained static page, provide a file link instead.
- For a small component change, render and visually inspect the affected
  component, interaction, and a representative viewport. For page-level or
  responsive work, render and inspect desktop, mobile, and relevant boundary
  sizes.
- Exercise the primary flow and important in-scope non-happy states. Confirm
  that assets load, text fits, controls work, and content does not overflow,
  overlap, or shift unexpectedly.
- For canvas, 3D, and animation, also confirm nonblank rendering, expected frame
  changes, and real interaction.
- Use visual or browser tooling when available; otherwise inspect manually and
  disclose unverified behavior. Fix and recheck in-scope findings only for
  design, implementation, or redesign; leave review-only work unchanged.
