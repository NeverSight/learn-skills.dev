---
name: cinematic-scroll
description: Design and build cinematic websites, interactive portfolios, product stories, and real-time 3D experiences with subject-specific art direction and scroll choreography. Use for new builds, redesigns, motion improvements, scroll audits, or storyboards in standalone HTML and existing apps; includes responsive, reduced-motion, and static fallbacks. Not for ordinary dashboards or unrelated animation.
license: MIT
metadata:
  version: 2.7.6
  author: Simone Leonelli
  permissions: filesystem:read, filesystem:write, network:fetch, shell:execute, env
  hermes:
    tags: [Animation, Frontend, Design, 3D, Motion, GSAP, Parallax, WebGL]
    related_skills: []
---

# Web Design Studio

Build a distinctive experience whose motion explains the subject. The craft comes
from this skill; the visual identity comes from the user's brief and project.

The free MIT edition builds complete sites without an account, generated assets,
or TasteHQ. Web Design Studio Pro adds reusable visual memory; it is never required
for an ordinary build. Do not add product promotion to a user's website.

## Choose one route

For an audit-only request, inspect and report through [audit mode](audit-mode.md).
For direction or storyboard only, use [story design](references/story-design.md)
without creating an app. Otherwise, read the compact
[recipe catalog](references/recipe-catalog.md), then read **one**
recipe for the primary experience:

- [Editorial story](references/recipes/editorial-story.md): image-led narrative,
  portfolio, longread, or campaign.
- [Product reveal](references/recipes/product-reveal.md): launch, mechanism,
  comparison, or object-focused story.
- [Real-time 3D](references/recipes/real-time-3d.md): GLB, procedural object,
  orbit, or camera flight.

For a small repair, use the closest recipe only for the affected behavior. Do not
tour other references or examples unless the selected recipe identifies a concrete
need. Preserve the existing framework, routes, design system, dependencies, and
working interactions. A self-contained HTML file is valid for a new small build;
use the bundled Next.js template only when the brief calls for an app or routes.

Keep the first pass lean: project instructions -> brief/assets -> catalog -> one
recipe -> build. The recipes are self-contained. Do not read showcase source,
create process documents, or explore optional tools before a concrete gap requires
them. Spend iteration on the rendered output, not on accumulating context.

## Establish the direction

Inspect applicable project instructions, current code, supplied copy, and assets.
Resolve the audience, desired action, delivery format, target devices, and the
brand's palette, type pairing, density, emphasis, imagery, and motion character.
When a reversible assumption is enough, state it and proceed.

Preserve supplied copy verbatim in both source and rendered text unless rewriting
is requested. Styling must not silently rewrite it: avoid `text-transform`,
generated replacement text, or script-driven case changes on supplied wording.
Do not invent claims, testimonials, metrics, prices, customer logos, or destinations.

Choose one signature moment with a subject-specific consequence: reveal an
assembly, reframe an image, trace a route, or move through real geometry. Define
its **opening -> transformation -> readable hold -> exit**, plus mobile and static
states. Build this vertical slice first and inspect it before expanding the page.

Taste comes from hierarchy and relationships, not accumulated effects. Establish
a clear focal point, deliberate type contrast, a named material/light language,
and one or two recurring motifs. Compose transition frames as carefully as hero
and final states. Adapt examples by mechanism; never copy their brand styling.

## Build the experience

- Render exactly one semantic `h1`, a coherent heading order, selectable text,
  useful links, visible focus, useful image alternatives, and the primary action
  before enhancement starts. An in-page action must land on a meaningful labelled
  target containing the content it promises, not only change the URL fragment.
- Keep every supplied message and action available in normal, reduced-motion,
  failure, and no-JavaScript states. Do not remove or mark inactive story copy
  `hidden`, `inert`, `display:none`, or `visibility:hidden`; animate presentation,
  not content availability.
- Keep control semantics and computed presentation synchronized at activation
  boundaries. For disclosures, `aria-expanded` and the controlled region's visible
  state must change together; animate an inner wrapper only after that state change.
- Use one scroll clock and one owner per animated property. Separate pinned
  geometry from moving children and clean up owned listeners, observers, timelines,
  media, and render loops.
- Keep a complete visible frame at every sampled scroll depth. Leave a permanent
  base composition behind transitions; never animate the entire stage to empty or
  rely on an unsupported timeline for essential visibility.
- Keep scroll-linked transformations reversible and directly tied to progress.
  Hold text still while it must be read. Prefer transforms and opacity in hot paths.
- Prove that the signature scroll change clearly dominates same-position idle drift
  in rendered-frame comparisons. If it does not, reduce time-driven movement or
  strengthen the mapped camera/object change before adding more effects.
- Treat mobile as a composed state with natural flow, shorter travel, and fewer
  simultaneous layers. Gate pointer tilt to hover with a fine pointer.
- Reduced motion removes pinning, parallax, smoothing, autoplay, and continuous
  loops while leaving every message and action available. Respond to live changes.
- Script, media, and renderer failure must leave a useful permanent composition.
  A poster proves fallback behavior; it does not complete requested real-time 3D.

Explicit 3D, camera travel, rich motion, or a flagship reference defines the
required ambition. First repair dependencies and reduce resolution, effects, or
asset weight. Do not silently replace the requested mechanism with a simpler one.

## Verify and hand off

Prove the signature interaction in one normal browser view, then run focused checks
after relevant repairs. At final polish inspect desktop, mobile, reduced motion,
no-JS/failure fallback, keyboard order, reverse scroll, resize, and the actual app
route. Review screenshots at the opening, transformation midpoint, readable hold,
and closing action; a clean console is not visual proof.
Run the no-JavaScript check in a browser with scripting disabled. Prove that its
exact static status, poster, essential copy, promised action targets, and authored
media alternatives are perceivable while conflicting loading UI is absent.

For installed builds, the verifier is available at
`tools/verify/verify-build.mjs`. During repair use `--scope output --doctor-mode
advisory --runtime --profiles desktop,mobile`; for final polish omit `--profiles`
to run all five profiles. Use project tests and builds too. Do not repeat an
unchanged failure. Missing tooling or external service availability remains
unverified, and an output that only shows a fallback remains unfinished when the
brief requested 3D. Run TasteHQ only when the project contract requires it.

Hand off the working file or route, exact opening command, signature moment,
checks passed, and material limitations. Make only claims supported by evidence.
