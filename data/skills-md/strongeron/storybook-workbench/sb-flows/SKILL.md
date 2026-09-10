---
name: sb-flows
description: "Map the whole app — routes, navigation edges, and persistent nav chrome, not just a screen list. Use for 'map the app', 'show the flow', 'app map', 'audit navigation', or 'how do screens connect'."
compatibility: "Requires bash and python3 (router/flow extraction writes flows.json)."
allowed-tools: Bash Read Glob Grep Write
license: MIT
metadata:
  author: strongeron
  version: '2.3.0'
  bundle: storybook-workbench
  vendor:
    scripts: [extract-flows.sh, scaffold-wrapper.sh]
    templates: [extract-app-graph.mjs]
    wrappers: [AppFlowGraph, JourneyGraph]
    references: [flow-capture.md]
---

# sb-flows — the connection half of an audit

A route list can't prove coverage; a flow graph needs **edges** and **persistent nav sources**
(sidebar/header/footer link from every screen and are invisible to a page-body sweep — the #1
audit miss). Load `references/flow-capture.md` before mapping.

## Run it

```bash
SKILL=${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}
CORE=${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}
"$SKILL/scripts/extract-flows.sh"      # 1. generic first pass → .storybook/flows.json (routes + edges + navSources)
"$CORE/scripts/scaffold-wrapper.sh" --flow   # 2. AppFlowGraph + JourneyGraph (+ icons.tsx)

# 3. The app-graph the wrappers actually render (edges with ACTION labels, deep store/service
#    tracing, role lanes, component lists). Copy the reference template, ADAPT its 3 marked blocks
#    to this repo's router/nav/role-gate, then run it. It writes app-graph.json + component-pages.json.
cp "$SKILL/templates/extract-app-graph.mjs" .storybook/scripts/extract-app-graph.mjs   # then edit ADAPT-1/2/3
node .storybook/scripts/extract-app-graph.mjs
```

Act on the **sweep reminder** the extractor prints when nav chrome exists. And if it prints
**`⚠ LIKELY UNDER-EXTRACTION`**, treat `flows.json` as a draft — the app navigates via an idiom
the script doesn't parse yet (the nanostores-class miss). Don't trust `edgeCount`: read the
unmatched call sites it lists, recover the real edges (a repo-local source-aware resolver beats more
regex), and fold general idioms back into `extract-flows.sh`. Full loop: `references/flow-capture.md`
→ **"When extraction under-reports."**

**Deep edges (don't stop at the shallow pass).** A nav fired from a store/service action (or a
deeply-nested feature component) has no screen of its own — its real origin is *whoever calls it*.
The template's `moduleOrigins` traces that **re-export-aware** (it follows barrels: a service
re-exported through a store is found via the store's import token), up the import graph to the routed
pages. This recovered real `switchToHotel → scheduler` edges that the shallow pass dropped. Verify in
`references/flow-capture.md` → **"Deep-edge tracing"**.

**VALIDATE — never hallucinate an empty edge.** The contract: every edge has file:line provenance;
anything unattributable is recorded in `unresolvedEdges`/`dynamicCallSites`, not invented. After
running, check `node -e` the JSON: `unresolvedEdges` should be small and each reason honest (a 404
with no route, a genuinely dynamic dispatch), and spot-check a couple of `module-trace` edges against
the source. See `references/flow-capture.md` → **"Validate the graph."**

## Model it

- **`<AppFlowGraph graph={...}>`** — whole-app route map: role swimlanes, typed/colored edges,
  coverage colouring, click-to-story. Feed an `AppGraph` derived from `flows.json`.
- **`<JourneyGraph journey={...}>`** — one flow's journey map (the `Flows/*` Docs index); each step
  links to its per-state story by `storyId`. Ships a collapsed "how to add a flow" authoring hint by
  default (suppress with `hideAuthoringHint`); the "what is this?" provenance banner is **off by
  default** — reachable on demand via `setProvenance()` / `__SB_WB_PROVENANCE__`, and `hideIntro`
  hard-suppresses it. The
  `journey` is a CURATED narrative — one persona's path across the captured graph — not a field in
  `flows.json` (which holds the route nodes + edges `AppFlowGraph` draws).
- Both take an injectable `icons` prop (pass lucide/project icons) — **no emoji** (CONTEXT.md
  §wrapper-view-design).
- **Theme via the app's tokens, not a fixed palette.** Chrome (panels, text, borders, lane stripes)
  reads `var(--color-foreground|surface|border-subtle|muted-foreground, <fallback>)`, so one `.dark`
  flip re-skins the whole map light↔dark and the fallback keeps it rendering in a token-less app.
  Only the *data* encodings stay literal — coverage dots and the per-`EdgeKind` hues are categorical,
  not chrome. Don't replace the `var()` chrome with hardcoded colors.

## The rules that matter

- Sweep **every** navigation source — `flows.json.navSources[]`, not just page bodies.
- Capture **edges**, not just routes — `flows.json.edges[]`.
- Explore **roles** — the same app is a different graph per persona. `flows.json` gives each route an
  `access` (public/user/admin, a path heuristic) + `roleSignals[]` (the real guards). Verify access
  against the guards, lay the graph out in role lanes (`node.role = route.access`), and audit the
  crossings: can an anon reach a user route? a user reach an admin route? See flow-capture.md
  → **"Step — explore roles."**
- Render pages/flows at **real width** — `layout: 'fullscreen'` + a desktop viewport AND a mobile
  view; never the narrow centered canvas. Each documented state = its own full-width story.
- Numbered-name convention `N · label`, linked by `storyId` (see flow-capture.md).

## Next

Append a finding, then `sb-stories` for each screen's states, or `sb-audit` to check coverage.
