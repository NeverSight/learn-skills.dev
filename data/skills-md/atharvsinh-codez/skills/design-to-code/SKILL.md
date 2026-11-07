---
name: design-to-code
description: Transforms screenshots, Figma frames, mockups, design images, and live public websites into high-fidelity, responsive, accessible, production-ready frontend code. Use when asked to "recreate this website", "turn this image into code", "match this page exactly", "clone this design", "build this Figma design", "make this responsive", "repair the visual differences", "create an Awwwards-level site", or translate a visual reference into React, Next.js, Vue, Svelte, HTML/CSS, or an existing project's stack. Supports exact reconstruction, greenfield art direction, font identification and selection, hybrid expansion, controlled variants, imagegen-powered assets, responsive inference, interaction and motion, visual-diff validation, and ship-readiness evidence.
---

# Design-to-code

Reconstruct or art-direct a website, then implement it as real, maintainable frontend code.

- **IS:** visual-source selection, design forensics, art direction when needed, responsive implementation, production asset creation, interaction fidelity, and rendered comparison.
- **IS NOT:** a screenshot pasted behind the page, a flattened image UI, an audit-only report when implementation was requested, or permission to redesign an authoritative reference into a preferred house style.

Keep product-behavior decisions, long-form copy strategy, deep SEO work, and standalone motion or typography audits scoped to the request. Implement the necessary parts, but do not silently expand a visual reconstruction into unrelated product strategy.

## Dispatch before acting

Choose one source mode and one surface track. Record both in the working notes.

### Source modes

| Mode | Select when | Source of truth |
|---|---|---|
| **Reference reconstruction** | A screenshot, frame, mockup, or live state defines the target | Observable reference evidence |
| **Greenfield art direction** | No precise composition exists and visual quality is central | Approved brief plus generated design references |
| **Hybrid expansion** | A reference defines the visual language but omits requested sections, routes, states, or breakpoints | Reference invariants plus generated missing surfaces |
| **Variant exploration** | The user asks for options before choosing | Controlled alternatives with identical content and constraints |
| **Retrofit or repair** | The task is responsive repair, dark mode, component cleanup, or visual-regression correction | Existing implementation plus target evidence |
| **Semantic scaffold** | The user explicitly asks only for unstyled structure | Visible content and native semantics |

Never generate a substitute page concept in reference-reconstruction mode. A generated concept may become authoritative only in greenfield or explicitly authorized hybrid work.

### Surface tracks

- **Marketing or brand:** Optimize hierarchy, storytelling, identity, proof, and one clear conversion path.
- **Product or operational:** Optimize task completion, scanability, stable controls, calm density, state coverage, and resilient data interaction.
- **Mixed product:** Treat public acquisition pages as marketing and authenticated work surfaces as product. Do not blend campaign furniture into dashboards.

The reference and explicit user requirements outrank track defaults.

## Load conditional playbooks

Read only the references that apply, each directly from this file:

- Read [art-direction.md](references/art-direction.md) for greenfield art direction, hybrid expansion, variant exploration, or any request for a new Awwwards-level visual direction without an authoritative composition.
- Read [reference-forensics.md](references/reference-forensics.md) for screenshot, Figma, live-site, multi-viewport, or visual-repair work requiring systematic extraction and an evidence ledger.
- Read [typography-and-fonts.md](references/typography-and-fonts.md) for every build that identifies, sources, chooses, substitutes, or loads fonts.
- Read [motion.md](references/motion.md) for any build that adds, matches, tunes, or removes interaction and motion.
- Read [interface-craft.md](references/interface-craft.md) for nontrivial marketing or product surfaces, responsive recomposition, dark mode, component/state design, typography, materials, or complex controls.
- Read [verification.md](references/verification.md) for every nontrivial build and any claim of exact, pixel-close, production-ready, or Awwwards-level output.
- Read [evaluations.md](references/evaluations.md) only when testing or improving this skill, not during normal project execution.

## Progress checklist

Copy and maintain this checklist for nontrivial work:

```text
Design-to-code progress:
- [ ] Select source mode and surface track
- [ ] Confirm scope, rights, routes, states, and target viewports
- [ ] Inspect every reference and the existing project
- [ ] Record observed, inferred, and substituted decisions
- [ ] Lock the visual system, content map, and asset plan
- [ ] Lock the font plan: identify, license, substitute, or use the Geist Serif default
- [ ] Enforce SVG-only iconography and remove every emoji
- [ ] Implement semantic structure and major geometry
- [ ] Integrate final assets, responsive rules, states, and motion
- [ ] Run accessibility, performance, and functional checks
- [ ] Complete rendered comparison and correction passes
- [ ] Run project validation and issue a readiness verdict
```

## Authority and evidence order

Resolve conflicts in this order:

1. Explicit user requirements and corrections.
2. Authorized supplied content and assets.
3. Observable pixels and behavior in the authoritative reference.
4. Additional viewport, state, route, theme, or motion references.
5. Existing product design system, behavior, and repository conventions.
6. Mode and surface-track defaults.
7. The smallest reversible inference.

Label material decisions as:

- **Observed:** directly visible or measured.
- **Inferred:** derived from relationships or conventions where evidence is absent.
- **Substituted:** intentionally replaced because of rights, missing assets, unavailable fonts, accessibility, or technical constraints.

Do not present an inference or substitution as an exact match.

## Establish the assignment

Identify:

- Target route, component, section, or route set.
- Reference files, URLs, viewports, device-pixel ratio, theme, locale, and visible state.
- Required desktop, tablet, mobile, short-height, and ultra-wide behavior.
- Required forms, menus, dialogs, carousels, navigation, data, and scroll behavior.
- Supplied copy, logos, fonts, icons, images, video, data, and design-system primitives.
- Existing framework, delivery environment, browser support, SEO, accessibility, and performance constraints.
- Which elements must be functional rather than visually represented.
- Whether exact third-party branding, copy, imagery, and interaction reproduction is authorized.

Ask one focused question only when an answer changes architecture, rights, core behavior, or the authoritative source. Otherwise choose a conservative reversible default and continue.

For sign-in, checkout, payments, account recovery, identity, or other sensitive flows, implement only authorized behavior. Never create a deceptive credential-capture or impersonation surface. Use inert or clearly mocked submissions unless the user supplied an authorized backend.

## Inspect the project before editing

- Read repository instructions and check the working tree. Preserve unrelated edits.
- Inspect the manifest, lockfile, scripts, framework configuration, routes, layouts, shared components, styling system, tokens, fonts, icons, assets, tests, and build pipeline.
- Reuse established primitives before creating new ones.
- Run the current preview or baseline checks when practical so pre-existing failures remain distinguishable.
- Keep the existing framework, package manager, lockfile, rendering model, and conventions unless change is required.
- Add a dependency only when it solves a real requirement better than existing code or browser primitives.
- Use actual repository commands; do not invent generic validation commands.

If `.openai/hosting.json` exists, read and follow the `sites-building` skill. Use its checkout, preview, checkpoint, and verification lifecycle.

For a new project, honor the requested stack. Without one, choose the smallest maintainable setup that supports the needed routes and interactions.

## Inspect visual sources before coding

Use the available image-viewing capability on every supplied image. Never rely on filenames, OCR, alt text, or a written summary alone.

For a live public reference, read and follow the `control-browser` skill. Capture visible behavior without copying proprietary source code or importing scripts, trackers, cookies, analytics, secrets, or private data. Never bypass authentication, paywalls, anti-bot controls, or access restrictions.

Extract at minimum:

- Viewport, canvas, fold, containers, gutters, columns, section boundaries, alignment anchors, overlaps, clipping, and layer order.
- Font family, real weights and styles, size, line height, tracking, measure, line breaks, optical alignment, and fallback behavior. Identify families with [typography-and-fonts.md](references/typography-and-fonts.md).
- Color roles, gradients, borders, radii, shadows, texture, blur, opacity, material, and depth.
- Image role, aspect ratio, crop, focal point, mask, frame, negative space, and responsive treatment.
- Header, navigation, content hierarchy, controls, forms, cards, lists, footer, sticky regions, and visible states.
- Motion trigger, duration, easing, delay, direction, sequencing, interruption, and reduced-motion behavior.

Treat one screenshot as one sampled route, viewport, state, theme, and scroll position—not a complete specification.

Use [reference-forensics.md](references/reference-forensics.md) to create the evidence ledger and reference manifest for complex work.

## Lock the fidelity contract

Before deep implementation, record:

- One-sentence visual thesis.
- Canonical copy and content hierarchy.
- Semantic region and component map.
- Container, grid, breakpoint, and section-rhythm rules.
- Type scale, font plan, spacing grid, radii, borders, depth, and semantic color roles.
- Asset inventory, rights, production paths, crops, and generation needs.
- Responsive transformations per section.
- Interaction, state, and motion requirements.
- Observed facts, inferred behavior, substitutions, risks, and blockers.

In exact reconstruction, derive this contract from evidence. In greenfield work, establish it deliberately using [art-direction.md](references/art-direction.md).

Create tokens early for repeated colors, typography, spacing, containers, radii, borders, shadows, layers, and motion. Preserve intentional one-off art-direction values instead of forcing every measurement into a generic scale.

## Use imagegen in two distinct roles

Read and follow the `imagegen` skill whenever missing custom raster imagery materially carries the design.

- **Art-direction reference:** A temporary, large, readable composition used to decide or inspect layout, hierarchy, typography relationships, spacing, media treatment, and rhythm.
- **Production asset:** A standalone image intended to ship, such as hero art, photography, illustration, texture, product render, atmospheric background, or transparent cutout.

Art-direction references may depict a full section but must never ship as the page, a flattened UI, or a full-page background. Production assets must exclude page copy, buttons, navigation, interface chrome, browser/device frames, logos, and watermarks unless those elements genuinely belong inside the artwork.

In greenfield mode, establish canonical copy before generation. Treat generated text only as spatial evidence; render approved wording as real HTML.

For every generated production asset:

- Define role, aspect ratio, largest rendered size, crop, focal point, negative space, palette, and responsive variants.
- Inspect the result and iterate one targeted mismatch at a time.
- Save the selected asset inside the project under a stable descriptive name before referencing it.
- Optimize delivery and reserve intrinsic dimensions.
- Record source or generation status, rights, dimensions, focal point, crops, and alternative-text decision.

Use existing authorized assets first. Keep ordinary icons, logos, diagrams, simple geometry, and repo-native SVG systems code-native. Never counterfeit protected marks or use generated imagery as a false depiction of a real person, product, location, event, or result.

For greenfield section-reference generation and consistency rules, follow [art-direction.md](references/art-direction.md).

## Enforce SVG-only iconography and zero emoji

This is a strict requirement for every website implementation, including exact-reference work:

- Every designed interface icon must render as SVG. Prefer the project’s existing SVG icon library; otherwise create a matching inline SVG, imported `.svg`, sprite symbol, or SVG component.
- Do not use emojis anywhere in website output—including copy, navigation, buttons, headings, bullets, labels, badges, statuses, alerts, empty states, placeholders, cursors, metadata, or decoration.
- Do not use Unicode pictographs or symbols, icon fonts, text glyphs, CSS pseudo-element glyphs, PNG/JPG/WebP icons, or image-generated raster art as icon substitutes.
- If the authoritative reference or supplied copy contains an emoji, replace it with the closest semantically correct SVG icon or clear plain text. Record this as a required substitution even when it creates a small visual difference from the reference.
- Do not use `imagegen` for icons. Keep icon geometry code-native, crisp, themeable, and reusable.
- Match one icon family’s view box, optical size, stroke/fill language, weight, caps, joins, and directionality. Use `currentColor` where the icon should inherit state or theme color.
- Hide decorative SVGs from assistive technology. Give icon-only controls an accessible name on the control, and do not treat an SVG `<title>` as the sole label.
- Verify that no emoji, Unicode icon substitute, icon font, or raster icon remains in rendered routes before declaring readiness.

The rule applies to icons, not ordinary photography or approved non-icon brand imagery.

## Implement from macro to micro

1. Establish the route, semantic landmarks, document order, background, page shell, containers, grid, and major section geometry.
2. Match the header, first viewport, dominant visual, content hierarchy, and primary action.
3. Match fonts, type metrics, content widths, and line wrapping.
4. Build repeated components and functional states using existing primitives.
5. Integrate final assets and tune crop, focal point, masks, and frames.
6. Add surfaces, borders, depth, icons, details, and intentional decorations.
7. Add responsive transformations, interactions, and motion.
8. Complete below-the-fold content, secondary states, validation, and cleanup.

Use semantic HTML, native elements, natural document flow, grid, flexbox, and intrinsic sizing. Reserve absolute positioning for genuine overlays and art-directed layers. Never implement the whole page as a coordinate map, giant SVG trace, canvas bitmap, or pile of absolutely positioned elements.

Treat typography as geometry. Identify or choose fonts with [typography-and-fonts.md](references/typography-and-fonts.md); when no relevant font is found, use Geist Serif (or Geist Sans/Mono for clear sans or mono roles) instead of a framework default. Fix font family, real weight/style availability, variable axes, fallback metrics, width, line height, and tracking before adding offsets or brittle `<br>` elements. Use tabular numerals for changing counters, prices, and metrics when visual jitter matters.

Treat embedded product screenshots, device frames, browser mockups, charts, and dashboards inside a marketing reference as media unless the requested target scope explicitly includes rebuilding their internal interface.

## Preserve component and state integrity

- Extract components for repeated structure, behavior owners, or stable visual primitives—not every wrapper.
- Keep external margins and page placement at call sites.
- Accept the project's normal class or style override mechanism on reusable visual components.
- Keep dimensions stable when labels, counts, hover styles, validation, or loading copy change.
- Preserve input values through recoverable errors.
- Prevent accidental double submission and stale asynchronous updates.
- Restore focus after dialogs and destructive confirmations.
- Provide rollback or clear recovery for optimistic and destructive actions.
- Cover default, hover, focus, pressed, selected, disabled, loading, empty, error, success, permission, offline, destructive, long-content, localization, and RTL states when applicable.

Use [interface-craft.md](references/interface-craft.md) for detailed marketing/product, surface, typography, responsive, state, and feature-specific rules.

## Recompose responsively

Treat mobile as a deliberate composition, not a proportionally shrunken desktop.

- Choose breakpoints where content or composition fails.
- Define each section's transformation as preserve, reflow, collapse, reorder, crop, simplify, or hide.
- Prefer one logical DOM; do not duplicate desktop and mobile trees without a semantic reason.
- Use fluid containers, `clamp()`, intrinsic sizing, and component-level container queries where appropriate.
- Collapse sidebars and dense navigation into accessible mobile patterns rather than squeezing columns.
- Preserve focal points, content priority, logical reading order, and practical touch targets.
- Test immediately above and below each breakpoint and eliminate unintended horizontal overflow.
- Apply the mobile platform layer from [interface-craft.md](references/interface-craft.md): viewport meta, `svh`/`dvh`, safe areas, 16px inputs, gated hover, and no tap flash.

Validate exact supplied widths first, then representative narrow, tablet, desktop, intermediate, short-height, and ultra-wide views. Follow the detailed engineering rules in [interface-craft.md](references/interface-craft.md).

## Match interaction and motion

Read [motion.md](references/motion.md) for any build that adds, matches, tunes, or removes motion.

- Match observed behavior before inventing effects. Defaults apply only where evidence is silent.
- Decide whether it should animate at all: never animate keyboard-initiated or 100+ per-day actions, and name a purpose for every animation.
- Use the cheapest tool: CSS transitions for states, `@starting-style` for entry, CSS or WAAPI for motion during busy page work, a spring library only for gestures, layout, and exit animation.
- Animate `transform` and `opacity`. Never use `transition: all` or `scale(0)` entrances.
- Use ease-out for enter and exit, never ease-in on UI. Keep product UI motion under 300ms, and make exits faster than entrances.
- Set `transform-origin` at the trigger for popovers and menus; keep modals centered.
- Gate hover motion to `(hover: hover) and (pointer: fine)` and give touch `:active` feedback.
- Keep initial content visible when animation setup or JavaScript fails.
- Ship a reduced-motion path that is gentler, not empty.

Add custom cursors, parallax, smooth scrolling, WebGL, magnetic controls, and page transitions only when supported by the reference or visual thesis and justified by the performance budget.
## Protect accessibility, performance, and SEO foundations

- Target WCAG 2.2 AA where applicable: landmarks, headings, native controls, labels, accessible names, logical focus, visible focus, contrast, zoom/reflow, touch, reduced motion, and meaningful alternatives.
- Preserve information without color, hover, animation, or imagery alone.
- Reserve media dimensions, minimize layout shift, optimize responsive images, and prioritize the likely largest-contentful-paint asset.
- Load only required font families, real weights, styles, and subsets; prevent faux bold/italic and disruptive font swapping.
- Avoid unnecessary client hydration, blocking scripts, giant media, and permanent expensive effects.
- Preserve titles, metadata, headings, links, crawlable content, deep links, and error-page resilience for public routes.
- Keep the console free of new runtime errors, hydration warnings, missing keys, and failed local assets.

## Run mandatory rendered verification

Do not declare success from a compiling build.

For every authoritative target:

1. Stabilize route, viewport, device-pixel ratio, browser, zoom, fonts, locale, theme, data, state, scroll position, and animation.
2. Capture the implementation at the same conditions as the reference.
3. Compare full-page and important component crops side by side.
4. Use overlay, blink, or image-diff evidence when available.
5. Fix mismatches in this order: content/state, geometry, typography, dominant assets, spacing, color/material, details, interaction, motion.
6. Fix root causes before local symptoms, then capture again.
7. Complete at least two deliberate correction passes for every nontrivial reconstruction.
8. Validate responsive interpolation, states, keyboard, touch, reduced motion, console/network, and the production build.

Read [verification.md](references/verification.md) for the comparison manifest, feature gates, browser matrix, readiness verdict, and evidence requirements.

## Anti-rationalization gates

| Shortcut thought | Required response |
|---|---|
| "The screenshot is obvious" | Inspect it at full useful detail and record evidence before editing. |
| "Image generation will make it premium" | Generate concepts only in greenfield/hybrid mode; never replace an authoritative reference. |
| "One full-page board is faster" | Split into large section references when text, controls, or spacing become unreadable. |
| "The crop is good enough" | Use crops for inspection; freshly render an unclear section before making it authoritative. |
| "The build passes" | Render, compare, correct, and capture evidence. |
| "Mobile can just stack" | Define and test intentional transformations for every section. |
| "This card makes grouping easy" | Use the lightest sufficient boundary; justify every card. |
| "This font is close enough" | Compare wrap points at the reference viewport and record the substitution. |
| "Motion makes it feel premium" | Pass the frequency and purpose gate first; remove motion that cannot name a purpose. |
| "It looks fine in device emulation" | Report hardware-only behavior as unverified unless tested on a real device. |
| "The asset is decorative" | Still verify performance, contrast, responsive crop, motion, and accessible treatment. |

## Reject common failures

- Screenshot-as-page, flattened text, full-page raster, coordinate-map layout, or hidden overflow used to conceal defects.
- Generic templates, repeated section formulas, card piles, nested boxes, giant rounded wrappers, decorative pills, and fake system labels.
- Default blue-purple glow styling, indiscriminate glassmorphism, fake metrics, fabricated testimonials, partner logos, or product claims.
- Placeholder copy, generic transformation language, unrelated stock imagery, any emoji in website output, non-SVG icon substitutes, and dead controls.
- Font files copied from a live site without a license, framework-default fonts chosen without a decision, motion on keyboard actions, and fade-in-on-scroll on every section.
- Silent font substitution, arbitrary line breaks, random breakpoints, missing states, inaccessible hover-only behavior, and motion with no reduced path.
- Replacing generous reference rhythm with cramped implementation or simplifying distinctive sections into generic rows.

Apply these anti-generic rules only where the user or authoritative reference does not require the pattern.

## Readiness verdict

Finish with exactly one verdict:

- **READY:** Required fidelity, behavior, responsiveness, accessibility, checks, and evidence pass.
- **READY WITH SUBSTITUTIONS:** All gates pass, but documented authorized substitutions remain.
- **NOT READY:** A required route, state, interaction, check, or material visual mismatch remains.
- **UNVERIFIED:** Implementation exists, but browser comparison or another mandatory evidence source was unavailable.

Never call an unverified result pixel-perfect or exact.

## Handoff

Lead with the working result. Report:

- Source mode, surface track, routes, and major components.
- Visual system and responsive transformations implemented.
- Generated or edited assets, their project paths, and substitutions.
- Reference targets, viewports, states, and browsers compared.
- Validation commands actually run and their outcomes.
- Readiness verdict and precise remaining deltas.

Keep the handoff concise. Let the implementation and evidence carry the detail.
