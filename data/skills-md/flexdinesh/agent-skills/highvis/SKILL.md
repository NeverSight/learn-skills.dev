---
name: highvis
description: "Explain app or feature architecture with C4, Mermaid/Excalidraw, and an HTML story of ordered events, sync/async flows, URLs, payloads, and responses. Use only when the user explicitly invokes highvis or $highvis; do not auto-invoke from context."
---

# Highvis

Turn repository evidence into architecture people can explore. Deliver an HTML
file, not just Mermaid in chat. Combine architecture maps with a readable HTML
story of what happens, who calls whom, and what crosses each boundary. Support
whole applications, monorepos, services, libraries, and individual features
without inventing runtime boundaries or request contracts.

## Scope

- `$highvis` — architecture of the current app; context and containers first.
- `$highvis <feature, service, package, or path>` — that slice, its owners,
  callers, dependencies, and data flow.
- Honour requested depth, audience, destination, and existing report to update.
  Ask only when ambiguity would select a materially different system or feature;
  otherwise state a concise assumption and proceed.
- Inspect source read-only. Write only report inputs/outputs within the agreed
  scope. Do not refactor the app or start its dependencies to draw it.

## Defaults for app and feature reports

These are Highvis defaults, not additional C4 rules. User requests override them.

| Choice | Entire app | Feature / subsystem |
| --- | --- | --- |
| Audience | Developer joining or navigating the codebase | Developer changing or debugging the feature |
| Opening view | System context | Participating containers and feature boundaries |
| Detail | Context + containers; components only for significant or requested areas | Container orientation, main HTML event story, then components where useful |
| Request/response | Trace representative scenarios when useful or requested | Required for every boundary crossed in the main feature story |
| HTML density | Compact Atlas workspace: navigation, map, inspector | Same workspace, with a full event story and two-column event rows on wide screens |
| Supporting views | Add a scenario only when it explains an important cross-boundary behaviour | Add a failure scenario only when traced handling reveals an important architectural decision |
| Code level | Only when explicitly requested or essential to the question | Same; avoid symbol inventories |

- Order feature views from orientation to event story to supporting detail.
  App views start with context and containers. Titles identify the actual
  subject: “Checkout boundaries”, “Orders API components”, “Place an order”.
- Prefer left-to-right layouts for context, containers, and interaction flows.
  Use top-to-bottom when a component hierarchy is clearer; avoid long chains.
- Aim for 4–9 meaningful nodes per diagram. Above 12, split by responsibility or
  scenario while retaining neighbouring dependencies. Small systems may need fewer.
- Use three concise label lines: name, type / technology, responsibility in 3–7
  words. Put paths, versions, implementation detail, and qualifications in evidence
  or notes. Label edges with specific actions and verified protocols.
- Keep the summary to two sentences: what this scope does and what the report
  covers. Notes explain decisions, unknowns, and omissions; evidence proves wiring.
- Use white backgrounds and colourful, consistent entity roles: pink people,
  indigo systems, blue interfaces, violet services/components, teal storage or
  messaging, and orange external systems. Type labels remain authoritative;
  colour does not replace C4 types or imply a runtime boundary.
- Open diagrams in “Fit view” to show every participant. The inspector and entity
  picker provide readable labels at overview scale; “100%” restores full-size
  diagram text. Preserve manual zoom when the window resizes.

## Atlas HTML by default

Use the bundled Atlas template: view navigation on the left, the diagram and
connections in the centre, and selected entity details on the right. Selecting
an entity shows its incoming/outgoing relationships, qualifications, source
evidence, links to deeper views, and matching story contracts. On narrow screens,
stack these regions and keep the entity picker available. Chronology-only views
use the main reading area without a diagram inspector.

- Use the full available width, 12–20px content gutters, and a small report header.
  Keep title, scope, revision, summary, and view navigation close together.
  Avoid hero layouts, oversized headings, decorative cards, and empty spacer bands.
- Default to 13px body text with approximately 1.4 line height, 24px report titles,
  14–16px section/event titles, and 11–12px contract metadata/code. Gain density
  through layout and spacing first; preserve readable diagram text and zoom.
- On desktop, put each numbered event's title, participants, explanation, and
  prerequisites beside its URL/status and contract disclosure. Keep rows in one
  chronological list; never reorder events into independent columns.
- Keep event padding around 8px, gaps 4–16px, and copy to one or two short
  sentences per event. Keep method/URL, status, execution mode, and request/reply
  links visible. Put full payloads, headers, qualifications, and source in native
  disclosures; show payload and headers side by side when space allows.
- On narrow screens stack each row and wrap long URLs/JSON inside the viewport.
  Keep compact spacing; increase touch targets for coarse pointers rather than
  globally inflating desktop controls. Preserve focus, contrast, and keyboard access.
- Use a bounded diagram viewport, roughly 280–560px tall; scroll/zoom rather than
  shrinking labels. Keep legends, evidence, and source sections tight and usable.
- Verify density with real content: count fully visible collapsed events at the
  same desktop viewport before and after layout changes. Check expanded contracts,
  narrow layout, and overflow. Compact must retain the complete event story.

## Trace the architecture

1. Read applicable instructions, repository docs, manifests, deployment config,
   and relevant entry points. Exclude generated/vendor/build files.
2. For app scope, identify actors, external systems, runtime units, storage,
   messaging, and independently runnable applications. For feature scope, trace
   from the real trigger through its owner to storage or external effects;
   include the caller and adjacent owners that explain the slice.
3. Follow imports, route/handler registration, service calls, schema ownership,
   events, workers, and deployment wiring. A directory tree alone is not evidence
   of architecture. Distinguish runtime communication from build dependencies.
   Follow each request from call site to handler/adapter and response consumer;
   an input schema alone does not prove the outbound payload or returned response.
4. Keep a compact evidence map: entity/relationship, source path and line range,
   what it proves. Mark inference and unknowns explicitly. Never fill missing
   code with a conventional frontend/API/database design.
5. Choose the fewest useful views using [C4 conventions](references/c4.md).
   Separate levels; do not label a mixed graph “C4 containers”. Do not force all
   four levels. A library may need context and components, with no container view.

## Tell the feature story

Read [event and contract conventions](references/flows.md). Feature reports must
include an HTML chronology from the actual trigger to the observable result,
including local decisions that explain why the next interaction happens. Use
plain paragraphs and numbered events; do not make readers reconstruct the story
from an architecture graph. A `Dynamic` view may contain `events` without Mermaid.

- Explain the action, reason, sender, recipient, and next consequence for each
  event. Keep full URLs and contracts in HTML, with expandable payload/header/source
  details; diagrams stay concise and optional for behaviour.
- Show requests and replies as separate events, paired by `exchange`. Include
  method, exact route/query template, symbolic environment base URL, relevant
  headers, actual payload shape, status, response shape, and consumer handling.
  Show SDK arguments/return values when the underlying HTTP contract is unavailable.
- Distinguish sync request/reply (caller waits), async publication/delivery or
  callbacks, redirects, and local execution. JavaScript `async`/`await` does not
  make a request an independent background workflow. Never invent async work;
  explicitly state when a traced feature has none.
- Record causal prerequisites using `after`; use `parallelGroup` for concurrent
  branches and explain the join. Numbering is reading order, not an invented
  total ordering of concurrent completions. Preserve nested call chronology:
  request → downstream request → downstream reply → caller reply.
- Separate materially different branches (email/social, success/recovery, etc.).
  Explain timeouts, cancellations, retries, side effects, and unknown outcomes
  where they affect continuation. Show only behaviour established by source.
- Mark provisional contracts and unavailable downstream implementation at the
  event itself. Redact credentials, tokens, personal data, and signed URLs;
  retain field names, types, and placeholders. Never call live feature endpoints
  to obtain examples. Use representative payloads clearly labelled as examples.

## Draw with C4 + Mermaid

Read [C4 conventions](references/c4.md) before authoring diagrams. Use
`flowchart LR` or `flowchart TB` for every diagram, with typed labels and subgraph
boundaries. C4 is the abstraction model; Mermaid is the notation. Avoid Mermaid's
experimental `C4Context`/`C4Container` syntax: this renderer's shape conversion is
designed for flowcharts.

- Labels say **name, C4 type / technology, responsibility**. Give each edge a
  concrete verb; include protocol/event/contract where verified.
- Keep IDs stable across views. Apply the node budget above; split crowded graphs
  into focused views instead of shrinking text.
- Feature diagrams show their parent container and relevant cross-container
  boundaries. Optional dynamic diagrams number interactions to match the HTML
  story and remain supporting views, not a C4 abstraction level.
- Use the provided palette consistently. Do not rely on colour alone: put types
  in node labels. Use quoted labels, simple rectangles/rounded rectangles,
  `subgraph`, labelled arrows, and `classDef`/`class`.
- Put full URLs in HTML event contracts; diagrams may use short relative routes.
  Do not include click directives, absolute URLs, Mermaid init directives, icons,
  embedded images, scripts, or untrusted HTML. `<br/>` label breaks are sufficient.

## Build the HTML

Resolve this skill's directory from the loaded `SKILL.md`, regardless of cwd.
Use its bundled generator and template; do not recreate the renderer from memory.

1. Write a JSON report matching [examples/app.json](examples/app.json) or
   [examples/feature.json](examples/feature.json). Replace illustrative content
   with traced facts. Each view needs `id`, `title`, `level`, `description`,
   `notes`, and `evidence`. Architecture views need `mermaid`; `Dynamic` views
   can instead supply a non-empty `events` array, or combine both. Events follow
   [the chronology schema](references/flows.md) and carry their own evidence.
   Evidence items contain `path` and `detail`;
   optional `lines` is a source line number/range. Notes record assumptions and
   limits, not invented findings. Supply a real revision when available.
   Add optional `entities` metadata to architecture views as described in
   [C4 conventions](references/c4.md#entity-inspection). Reuse Mermaid node IDs;
   record each role, entity evidence/notes, and an optional deeper-view ID. Names,
   types, responsibilities, and connections come from the rendered Mermaid graph,
   not a duplicated or independently invented inventory. Existing reports without
   metadata remain supported; supply metadata for intentional role colours and
   entity-specific evidence.
2. Default destination: `docs/architecture/highvis/<scope-slug>.html` with a
   neighbouring JSON input. Follow an explicit user path or repository convention.
3. Run, substituting absolute paths:

   ```sh
   python3 <skill-dir>/scripts/build_report.py <report.json> --output <report.html>
   ```

The output is one portable HTML file with inline report data, CSS, and UI code.
It loads pinned Excalidraw/Mermaid libraries from esm.sh and jsDelivr, so rendering
requires network access; Python needs no extra packages. Preview the generated
HTML, not the unfilled `assets/report.html` template. Serve locally if the browser
restricts `file://` module imports:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory <report-directory>
```

The pipeline is `parseMermaidToExcalidraw` → `convertToExcalidrawElements` →
`exportToSvg`. Keep this pipeline; Mermaid's SVG or hand-drawn mode alone does
not fulfil the Excalidraw requirement. Preserve view switching, zoom/fit, source
inspection, evidence, `.mmd`/SVG/`.excalidraw` downloads, responsive layout, and
visible loading/error states. Keep white backgrounds, clear typography,
consistent role colours, and readable HTML stories. Avoid dashboard filler.

If fully offline output is requested, bundle verified dependencies or embed
Excalidraw-rendered SVGs at generation time while retaining Mermaid sources and
evidence. Explicitly report the chosen approach; do not claim the CDN template is
offline. Never silently fall back to a different renderer on failure.

## Verify and deliver

- Cross-check every visible entity, arrow, boundary, and C4 level against source.
  Compare all app entry points for broad scope; report omitted areas explicitly.
- Verify request URLs, serialization, response status/body, request/reply pairing,
  causal order, parallel joins, and consumer behaviour against both ends of each
  interaction. Trace failures separately; do not present a provisional path as live.
- Open the generated HTML in an available browser. Render **every** view; inspect
  desktop and narrow layouts for clipped labels, overlaps, and overflow. Exercise
  switching, fit/zoom, source inspection, downloads, event links, contract disclosures,
  and chronology-only views. Confirm HTML story sections remain readable when CDN
  rendering fails. Fix malformed Mermaid or broken rendering before handing it
  over. Generator success is not render proof.
- If browser verification is unavailable, say so. Never claim it rendered from
  static validation alone. Retain source and show recoverable dependency errors.
- Return a clickable HTML file link, scope/views, and any material uncertainty.
  Keep the response concise. Include the JSON link when useful for later updates.
