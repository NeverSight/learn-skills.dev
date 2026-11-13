---
name: create-html-artifact
description: Produce a single portable local HTML file as the final deliverable — a report, doc, dashboard, landing page, demo, tool, or presentation rendered as one .html that opens straight from disk. Use when the user asks for an HTML page/file/artifact saved locally, a visual or interactive deliverable as a standalone web page, or when porting content into one HTML file. Not for publishing or hosting a page online — the deliverable is a local file, never a URL — and not for multi-file web projects or apps with a build step.
---

# Create HTML Artifact

Approach this as the design lead at a small studio known for versatility: every deliverable gets a visual identity pitched at the treatment the task actually calls for — deliberate palette, typography, and layout choices specific to the subject, never a templated design. The deliverable is exactly one `.html` file that renders correctly when opened from disk.

## Output contract

The finished artifact is a single, complete HTML file, produced in two steps: author a body fragment, then build it with the bundled script.

- **Author a fragment, not a document.** Write only the page content — markup plus its own `<style>` and `<script>` blocks. Never hand-write `<!doctype>`, `<html>`, `<head>`, or `<body>`; the build step injects the skeleton and rejects input that contains one.
- **Build with the bundled script.** `python3 scripts/build.py fragment.html -o page.html [--title ...] [--lang ...]` wraps the fragment in the full skeleton (`<!doctype html>`, `<html lang>`, charset, viewport, `<title>` derived from the first `<h1>` when not given) and injects a minimal CSS reset ahead of the page's own styles. The reset sets `color-scheme: light dark`; a deliberately single-theme page overrides it.
- **Mermaid renders out of the box.** Every build injects the mermaid library (a pinned CDN tag) plus a theme-aware init, so `<pre class="mermaid">` blocks render as diagrams; when the CDN is unreachable the diagram source stays visible as plain text.
- **One portable file.** The deliverable must survive being moved, mailed, or shared alone: exactly one `.html`, with local-only assets inline — styles and scripts in the fragment, generated or local images as `data:` URIs. A relative path to a sibling file is the prohibited substitute. Libraries, webfonts, and remote images load from CDN URLs; pin versions so the page doesn't shift under a future release.
- **Delivery is the file path.** Save the file where the user named — otherwise give it a descriptive name in the working directory — and hand back the path. Never upload, host, or publish the page.

Before delivering, verify the contract: scan the built file for `src=`, `href=`, and `url(` values that point at local relative paths — any hit breaks single-file portability and means the artifact is not done.

## Read the request first

Calibrate treatment, not whether to design. A doc deserves the same craft as a landing page — what changes is the treatment that craft is delivered in.

Many requests call for a utilitarian treatment: a plan, a memo, a report, a demo. Make it polished — real typographic hierarchy, considered spacing, a proper palette — but don't over-design. Most pages do not need a flashy hero; keep flourishes tasteful and limited.

Some requests call for an editorial treatment: a landing page, a game, an app or tool the user will keep or share. See "When the request is editorial" below.

When unsure: a well-composed page is never the wrong answer; an over-designed visual identity sometimes is.

## Fundamentals for every artifact

**Honor what's already there.** Look for an existing design system first — CLAUDE.md, a tokens or theme file, existing component styles. When one exists, apply it; everything below fills gaps and never overrides. Precedence: the user's own words, then the project's existing system, then your choices.

**Ground it in the subject.** Pin one concrete subject, its audience, and the page's single job. The subject's own world — its materials, instruments, vernacular — is where distinctive choices come from. Build with real content throughout, never lorem.

**Pair typefaces.** Typography carries the page even when the page isn't about typography. Load webfonts from a CDN — pin the family, weights, and subsets you actually use — and give the stack a considered local fallback so the page still reads well while fonts load or if they fail. Keep running text near 65 characters wide; set a type scale and stay on it; give headings `text-wrap: balance` and uppercase labels a touch of letter-spacing. Tracking and leading are size-specific, never one value for all sizes: large display text tightens (negative letter-spacing, line-height near 1.1) while body stays near zero tracking with roomier leading. Build hierarchy from weight + size + leading as a set, not size alone; set `font-optical-sizing: auto` on variable faces; size spacing in `rem`/`em` so the layout scales with the reader's text-size setting.

**Choose neutrals, don't default to them.** A pure mid-grey reads as unconsidered; a grey with a slight hue bias toward the page's accent reads as chosen. Pure white and near-black are fine grounds when they suit the subject — the point is that the neutral was picked, not inherited.

**Design both themes.** `prefers-color-scheme` carries the viewer's preference. The robust pattern is token-level: define the palette as custom properties on `:root`, redefine only the tokens under `@media (prefers-color-scheme: dark)`, and style components through the tokens — never directly inside the media query. If the page ships its own theme toggle, have it stamp `data-theme="dark"` / `data-theme="light"` on the root element and redefine the tokens again under those selectors so the toggle overrides the media query in both directions. Give the second theme the same care as the first — don't naively invert; keep contrast legible and the accent working on both grounds. A design that deliberately commits to one visual world (a neon arcade screen, a letterpress invitation) may stay single-theme — make it a choice, not an omission.

**Let layout do the spacing.** Lay out sibling groups with flex or grid and `gap`, not per-element margins that silently collapse or double. Wide content — tables, code, diagrams — gets `overflow-x: auto` on its own container so the page body never scrolls sideways. Use relative units and `max-width: 100%` on images so the page holds up at any width. Reach for `font-variant-numeric: tabular-nums` wherever digits line up in columns.

**Avoid AI-generated design.** AI-generated design clusters around a few looks: warm cream (#F4F1EA) with a serif display and terracotta accent; near-black with a lone acid-green or vermilion pop; broadsheet hairline rules with dense columns; a purple-to-blue gradient hero on white; Inter or Space Grotesk as the "safe" face; emoji as section markers; everything centered; `rounded-lg` everywhere; accent bar/rail on rounded cards. Where the user pins down a visual direction, follow it exactly — their words always win, including when they ask for one of these looks. Where nothing is specified, don't spend that freedom on one of these defaults.

**Build cleanly.** Be cognizant of overlapping elements, cascade collisions, silent font fallbacks; visual bugs hide in the gap between source and output. Close every non-void element, double-quote attributes, give keyboard focus a visible state, respect `prefers-reduced-motion`. For generative or decorative graphics, reach for Canvas or WebGL rather than hand-authoring long SVG path data.

**Watch selector specificity.** It is easy to generate classes that cancel each other out — a type-based selector like `.section` fighting an element-based one like `.cta` over padding and margins. Structure the cascade so it doesn't silently undo your spacing.

**Write the copy as design material.** Write from the user's side of the screen — name things by what people recognize, not how the system is built (a person manages *notifications*, not *webhook config*). Active voice; a control says exactly what happens ("Publish", then a toast that says "Published"). Errors explain what went wrong and how to fix it — no apologies, no vagueness. Specific beats clever.

**Structure is information.** Structural devices — numbering, eyebrows, dividers, labels — should encode something true about the content, not decorate it. Numbered markers (01 / 02 / 03) are only appropriate when the content actually is a sequence. Question such choices before incorporating them.

**When it moves or responds to touch.** Before writing any gesture-driven or animated interaction — drags, swipes, sheets, carousels, springs, page transitions — read `references/motion.md`: response and latency, interruptibility, spring parameters with concrete values, velocity handoff, momentum projection, and reduced-motion equivalents. Static pages skip it.

**When it's a UI, not a document.** A dashboard or tool is scanned and operated, not read top-to-bottom, so the craft shifts from typography to information design. Surface the summary before the detail; encode state in form as well as number — a pill, a chip, a severity stripe — so what needs attention reads at a glance. Semantic color (good / warning / critical) is separate from the accent hue and doesn't count as your accent. Give sparklines and charts the same care as type: an area fill, a faint grid, an emphasized endpoint. What's interactive should look interactive.

## Process

Before writing code, sketch a short design plan — a compact token system:

- **Color**: the palette as 4–6 named hex values.
- **Type**: typefaces for 2+ roles — a characterful display face used with restraint, a complementary body face, and a utility face for captions or data if needed.
- **Layout**: a layout concept in one or two sentences.

Then build, deriving every color and type decision from the plan.

## When the request is editorial

The stance shifts: the client has already rejected proposals that felt templated and is paying for a distinctive point of view. Make opinionated calls, and take one real aesthetic risk where it serves the work.

Review the design plan against the subject before building: if any part reads like the generic default you would produce for any similar page, revise that part and note what changed and why. Only then write the code, following the revised plan exactly.

- The hero is a thesis: open with the most characteristic thing in the subject's world — headline, image, live demo, interactive moment.
- Typography carries the personality of the page. Pair the display and body faces deliberately — not the families you would reach for on any other project — and make the type treatment itself memorable, not a neutral delivery vehicle.
- Leverage motion deliberately: a page-load sequence, a scroll-triggered reveal, hover micro-interactions, ambient atmosphere. One orchestrated moment usually lands harder than scattered effects — and sometimes less is more; extra animation is itself an AI-generated tell.
- Match complexity to the vision. Maximalist directions need elaborate execution; minimal directions need precision in spacing, type, and detail. Elegance is executing the chosen vision well.
- Spend your boldness in one place; keep everything around it quiet. If the accent fights the ground, shift it toward analogous or drop saturation rather than replacing it.
