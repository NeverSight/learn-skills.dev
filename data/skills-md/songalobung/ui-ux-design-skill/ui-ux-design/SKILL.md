---
name: ui-ux-design
description: Human-centered UI/UX design, product discovery, interaction design, accessible interface implementation, and usability validation. Use when researching user needs, designing or improving a website/app flow, building components or design systems, refining visual hierarchy, or reviewing interface quality in any framework.
---

# Human-Centered UI/UX Design

Make the useful thing understandable, accessible, and trustworthy for the people who need it. Visual polish supports a good experience; it cannot compensate for solving the wrong problem, confusing content, inaccessible controls, or an untested workflow.

## Operating principles

1. **Start with people and outcomes.** Understand who is trying to do what, in what context, with what constraints. Do not confuse a stakeholder request, feature, or trend with a validated user need.
2. **Design the whole journey.** Consider the steps, channels, handoffs, outcomes, recovery paths, and support needs before polishing a screen.
3. **Make evidence and assumptions visible.** Separate what users said or research demonstrated from interpretations and hypotheses. Do not fabricate users, research, testing, metrics, testimonials, or product facts.
4. **Include people who are often excluded.** Consider variation in ability, age, language, literacy, culture, device, connectivity, time, confidence, privacy, and environment. Include disabled people in research and evaluation when possible.
5. **Prefer clarity, control, and recovery.** Explain the current state, make the next useful action apparent, prevent foreseeable errors, and provide appropriate ways to back out or recover.
6. **Treat accessibility as a design and implementation requirement.** Use applicable standards precisely, but do not mistake technical conformance for proof of usability.
7. **Use patterns and visual effects in service of the task.** Be coherent and distinctive without making users decode the interface.
8. **Iterate from observed problems.** Prototype early, evaluate with representative people, fix high-impact barriers, and keep learning after launch.
9. **Think about the product before its screens.** Understand verified value, business/service realities, user goals, risk, and lifecycle. Do not make every product look like the same fashionable template.
10. **Use visual storytelling truthfully.** Shape attention, atmosphere, imagery, depth, and rhythm to clarify meaning. Never fabricate evidence or let composition hide consequential information.
11. **Practice design restraint.** Gradients, glass, cards, motion, 3D, and decoration must earn their place. Remove effects that do not improve task clarity, identity, or useful feedback.

## Multidisciplinary operating model

For substantial design work, apply eight complementary lenses in sequence and let them challenge one another: product design checks task and product fit; UX research checks evidence and assumptions; creative direction checks originality and coherence; design systems architecture checks reuse and consistency; frontend engineering checks feasibility and rendered behavior; interaction/motion design checks state, feedback, and purposeful movement; accessibility/usability audit checks operability and inclusion; and a ruthless design critic looks for the clearest reasons the result could still fail. The critic should be rigorous about the work and respectful toward people. Do not claim to be a credentialed human professional or to have conducted research, audits, or testing that did not occur. Detailed responsibilities and the review sequence are in `references/design-capability-playbook.md`.

## Select the right depth

For a small component change, inspect nearby conventions, identify affected states, implement, and run proportionate checks. For a screen or flow, use the full design loop below. For a new product, high-risk workflow, or ambiguous problem, do discovery and validation before committing to a polished solution. Never inflate a small task into a process ceremony; never skip the human and accessibility questions merely because a deliverable is visual.

## End-to-end design loop

### 1. Frame the problem

Identify the intended audience, user task, desired outcome, business or service constraints, environment of use, platform, content, risks, and what is explicitly out of scope. Inspect the existing product and repository before changing them: navigation, analytics or research evidence if available, routes, components, design tokens, copy, dependencies, and platform conventions.

Ask: What does the person need to accomplish? What must they know before acting? What happens if they succeed, fail, stop, or return later? Which assumptions are unverified? What would make this experience unsafe, exclusionary, confusing, or costly?

Do not presume that demographic labels explain behavior. Prefer observable context, goals, barriers, and evidence over stereotypes or fictional personas. If critical context is missing, ask a focused question; otherwise state a conservative assumption and proceed.

### 2. Research needs and context proportionately

Use the lightest method that can answer the decision at hand: review existing research and support feedback; inspect analytics or task outcomes where available; interview or observe users; conduct contextual inquiry; map a journey; or test a prototype. Ask open, non-leading questions about recent real behavior. Observe what people do as well as what they say. Protect privacy, obtain appropriate consent, and do not collect sensitive data without a clear need and safeguards.

Recruit people representative of relevant tasks and contexts, including people with disabilities and people facing access barriers. Avoid treating one participant as representative of a whole population. Record the method, sample limitations, evidence, and unresolved questions. If direct research is unavailable, say so and label any inferred needs as hypotheses for later validation.

### 3. Map the service and information

Map the end-to-end task from trigger to successful outcome, including prerequisites, decisions, errors, interruptions, handoffs, help, and return visits. Mark unnecessary steps, repeated entry, unclear eligibility, dead ends, and points where people need reassurance or human assistance.

Organize content around user questions and actions, not the organization's org chart. Give each page or view a clear purpose. Use descriptive headings, meaningful grouping, and predictable navigation. Keep key information and choices visible when users need them; use progressive disclosure only when it reduces cognitive burden without hiding a consequential choice or next step.

### 4. Prioritize and define success

Prioritize by user impact, frequency, severity of failure, accessibility risk, and uncertainty—not by visual novelty. Define what success looks like in observable terms: completing a task, finding correct information, recovering from an error, or understanding a decision. Use outcome measures only when they can be gathered honestly and interpreted with their limitations. Do not invent conversion improvements or claim causation from a visual redesign alone.

### 5. Explore before committing

Sketch or prototype multiple plausible structures when there is meaningful uncertainty. Start with low-fidelity flow or wireframe decisions before investing in decoration. Compare alternatives against task clarity, user effort, accessibility, feasibility, and product fit. Use a supplied reference to extract principles—not to trace a layout or copy a distinctive identity.

### 6. Specify structure and behavior

Create a proportionate design brief: users and context; task and outcome; content hierarchy; primary and secondary actions; visual direction; critical states; platform constraints; accessibility target; known assumptions; validation plan. Define interaction contracts for controls: purpose, available input methods, state transitions, feedback, error/recovery, keyboard/focus behavior, and what assistive technology should learn.

### 7. Build on the existing system

Inspect and reuse established tokens, components, semantics, layout patterns, and platform behavior. Implement with the repository's native stack. Add dependencies only when they solve a real need and are compatible with performance, maintenance, accessibility, and licensing constraints. Create shared components when repeated use or complex behavior justifies the abstraction; keep one-off elements simple.

### 8. Validate, refine, and report

Test complete tasks at realistic sizes and with realistic content. Review with keyboard, pointer, touch, zoom/text resizing, reduced motion, and relevant assistive technology where available. Conduct usability sessions with representative people for meaningful flows. Record observations as evidence, distinguish severity from frequency, fix the highest-impact barriers, and retest. State what was tested, what was not, remaining uncertainty, and known issues. Never claim conformance, user validation, or a successful browser check without evidence.

## Detailed companion guidance

Load the references relevant to the task instead of relying on memory or this overview alone. The tool catalog is optional: never require a named service, claim access that is unavailable, or use a new library just because it appears in the catalog.

- `references/human-centered-process.md` — discovery, research ethics, journey mapping, content structure, prioritization, and practical usability testing.
- `references/accessibility-inclusive-design.md` — disability-inclusive design, WCAG 2.2 boundaries, semantic implementation, keyboard/focus, forms, media, motion, and assistive-technology checks.
- `references/interaction-patterns.md` — action feedback, navigation, forms, search, tables, dialogs, destructive actions, errors, empty/loading states, and responsive interaction decisions.
- `references/visual-design-systems.md` — hierarchy, typography, color, spacing, layout, content, tokens, theming, imagery, motion, and coherent visual direction.
- `references/design-capability-playbook.md` — explicit step-by-step selection methods for design intelligence, creative direction, research, layout, typography, color, architecture, UX psychology, interaction, motion, responsive design, and rendered QA. Read this for new screens, design systems, visual refreshes, or detailed user requests.
- `references/design-intelligence-architecture.md` — design reasoning records, visual critique, alternative simulation, screenshot interpretation, design-to-code comparison, visual regression, behavioral UX, responsive/performance intelligence, governance, project memory, benchmarks, and controlled improvement. Read for advanced product work or when the user asks for design-intelligence systems.
- `references/tool-selection-and-workflow.md` — optional discovery-to-delivery workflow and selection guide for the user's named color, type, research, component, motion, 3D, icon, illustration, photo, and QA tools. Read when choosing or using external references, assets, or implementation libraries. Always verify current docs, compatibility, pricing, and rights.
- `references/tool-source-notes.md` — dated primary-source verification notes for a subset of those tools; use as link pointers, not a substitute for checking current source terms.
- `references/curated-source-research.md` — the user's additional books, UX articles, research overviews, and Apple/Meta source links, with verified takeaways, provenance, evidence scope, and limitations. Load when consulting those sources or choosing platform/e-commerce references.
- `references/knowledge-library.md` — map of the complete curated reference library and task-based loading recipes. Read this when planning substantial work or selecting references.
- `references/design-philosophy.md` — product thinking, visual storytelling, ethical persuasion, and restraint.
- `references/design-styles.md`, `references/typography.md`, `references/color-theory.md`, and `references/layout-patterns.md` — detailed design knowledge for visual direction and composition.
- `references/ux-patterns.md`, `references/motion-design.md`, and `references/design-systems.md` — task patterns, purposeful motion, and reusable systems.
- `references/accessibility.md` and `references/platform-guidelines.md` — quick accessibility routing and platform-specific adaptation. Verify volatile platform details in current official documentation.
- `references/anti-ai-slop.md` and `references/visual-qa.md` — critique generic design decisions and inspect/correct the rendered product.
- `references/quality-assurance.md` — design review, usability evaluation, implementation QA, severity, iteration, and honest handoff.
- `references/standards-and-sources.md` — authoritative references and which are normative, informative, platform-specific, or heuristic.
- `references/source-patterns.md` — patterns observed on the twelve UI libraries supplied by the user, plus item-specific reuse cautions.
- `templates/design-brief.md` and `templates/usability-test-plan.md` — adaptable working templates. Use only fields relevant to the scope.
- `templates/design-decision-log.md` and `templates/design-evaluation.md` — reusable records for rationale, alternatives, evidence, implementation, testing scope, and remaining uncertainty.

## Implementation acceptance bar

Before calling an interface complete, confirm the applicable points below or explicitly note why an item could not be evaluated:

- **Purpose:** The view has a clear job, the content answers the user's likely questions, and the main action is understandable.
- **Behavior:** Every apparent control does what it promises; state changes are visible; errors have a recovery path; no dead or fake controls remain.
- **Accessibility:** Semantics and names are correct; keyboard users can complete the task; focus is visible and predictable; content is not conveyed by color alone; contrast, zoom, motion, and target-size requirements have been checked against the applicable criteria.
- **Content:** Labels are specific and plain; validation is helpful; empty, loading, success, and failure states are designed where relevant; claims and content are accurate.
- **Responsive use:** Layout and controls work across target widths, touch/pointer input, text expansion, and realistic content without clipping or overflow.
- **Craft:** Type, spacing, alignment, density, imagery, and component states form a coherent system; decoration does not compete with task completion.
- **Quality:** Relevant automated checks pass; rendered pages have been inspected where possible; remaining limitations are disclosed.

This acceptance bar is a practical review checklist, not itself a conformance standard. For a compliance claim, use the exact normative specification and full conformance requirements. See `references/accessibility-inclusive-design.md` and `references/standards-and-sources.md`.

## Portability across assistants and frameworks

The canonical instructions are plain Markdown with YAML frontmatter. The skill is framework-neutral: first identify the project's native framework and conventions, then translate design intent into its idioms. Do not assume React, Tailwind, shadcn, a component catalog, a particular browser tool, or a specific coding-agent feature. To use this content in Claude, Gemini, Codex, Manus, or another assistant, adapt the package's filename, folder, frontmatter, and activation mechanism to that assistant's current rules/skill format. Preserve the references alongside the core file or bring the relevant reference into context; a core file that points to missing references loses essential detail.

## Completion report

Summarize the user need addressed, what changed, important design decisions, validation actually performed, and remaining issues or assumptions. Keep the report proportionate. Never say “accessible,” “WCAG-compliant,” “validated with users,” or “production-ready” as an unqualified claim when the evidence does not support it.
