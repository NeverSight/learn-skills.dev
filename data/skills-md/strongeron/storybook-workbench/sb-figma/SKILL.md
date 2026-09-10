---
name: sb-figma
description: "The Figma↔Storybook bridge, both directions, via the native Figma MCP. design→code: map foundation tokens (color/spacing/type) from Figma variables with design↔code parity + drift, and deliver approved Figma components (extract → build → embed), authoring stories via sb-stories' rules. code→design: build Code Connect mappings from components + stories + token parity + usage so Figma Dev Mode shows the real code. Use for 'sync my Figma tokens', 'map Figma variables to my design system', 'deliver this approved Figma design', 'check design↔code token parity', 'connect my components to Figma / code connect'. NOT for prototyping/iterating an undecided design (that's sb-explore)."
compatibility: "Requires bash, python3, Node.js (for the .mjs scripts). The Figma MCP server provides get_variable_defs / get_design_context / get_screenshot; if it's unavailable (headless), the skill degrades to a cached figma-variables.json. Reads project-inventory.json (sb-inventory) when present to cross-check token adoption."
allowed-tools: Bash Read Glob Grep Write Edit
license: MIT
metadata:
  author: strongeron
  version: '0.1.0'
  bundle: storybook-workbench
  vendor:
    scripts: [capture-figma.mjs, pull-figma-variables.mjs, build-token-parity.mjs, build-code-connect.mjs, record-figma-delivery.py]
    wrappers: [TokenMatrix, TokensCanvas, FigmaInventory]
    references: [figma-token-sync.md]
    templates: [figma-inventory.stories.tsx]
---

# sb-figma — Figma → production Storybook delivery

`sb-figma` owns the **DELIVER** stage of the Figma→Storybook lifecycle: an **approved** design becomes
production Storybook. It is Figma-aware (uses the Figma MCP), but it is **not** the exploration skill.

> **The lifecycle line (load this first).** *Undecided / trying options* → **`sb-explore`** (Lab sandbox,
> iterate against a Figma node) → **`sb-ship`** (graduate the Lab experiment). *Already approved in Figma* →
> **`sb-figma`** (deliver direct to prod). Both touch Figma MCP; the difference is **exploration vs delivery**.
> If the user is still deciding, hand off to `sb-explore`. See `references/figma-token-sync.md`.

## Job 0 — capture the MCP output (always, before anything else)

> **Force the NATIVE structured tools — never work from a screenshot.** A screenshot is pixels; it cannot
> give you variables, styles, or component props. The full picture comes ONLY from the native MCP tools, and
> you must pull all three categories before building or connecting:
> - **Variables** → `get_variable_defs` (the token values: color/spacing/type/effect, resolved).
> - **Components + styles** → `get_design_context` (the reference code, applied styles, props/variants).
> - **Structure** → `get_metadata` (the node tree; on truncation, drill to child node-ids — never give up at
>   the parent).
> `get_screenshot` is **visual reference only** — for an eyeball diff after you've built from the structured
> data. NEVER read tokens, props, or layout off a screenshot. If a tool returns "nothing selected" on a page
> id, drill to a concrete component node (a page is not a layer).

Scripts can't call the Figma MCP, and an MCP result lives only in the agent's context — ephemeral, gone
on the next session, absent headless. So **every Figma MCP call you make, persist it** through the universal
store before using it. This is what makes the pipeline reproducible and iterable.

```bash
# any JSON-returning tool — pipe its output straight in:
<get_variable_defs output>  | node scripts/capture-figma.mjs --tool get_variable_defs   --file <FILE> --node <NODE> --from-mcp -
<get_design_context output> | node scripts/capture-figma.mjs --tool get_design_context  --file <FILE> --node <NODE> --from-mcp -
<get_metadata output>       | node scripts/capture-figma.mjs --tool get_metadata        --file <FILE> --node <NODE> --from-mcp -
<get_code_connect_map out>  | node scripts/capture-figma.mjs --tool get_code_connect_map --file <FILE> --node <NODE> --from-mcp -
# get_screenshot returns an image — save it, then register the file:
node scripts/capture-figma.mjs --tool get_screenshot --file <FILE> --node <NODE> --image /tmp/frame.png
# see the whole inventory (degrade / iterate):
node scripts/capture-figma.mjs --list
```

Store layout: `.storybook/figma/manifest.json` + `.storybook/figma/<tool>/<node>.json` (images keep their
ext). Re-capturing a (tool,node) overwrites — diff against git to see what moved in Figma. **Downstream steps
read the store, never re-call MCP.**

## MCP realities (field-verified against the Detections file, 2026-06-22)

What the live Figma MCP actually returns — the scripts already handle these; know them so you don't fight the output:
- **`get_variable_defs` is a FLAT `{ "name": "value" }` map** (not nested DTCG, not an array). Colors come **already
  resolved to hex** (`"semantic/background":"#fbfcfc"`), incl. 8-digit alpha (`"#e4e5e580"`). Numbers are bare
  strings (`"spacing-2":"8"`, `"wght/semibold":"650"`). **Typography is an opaque `Font(family: …, size: …)`
  string** — `pull-figma-variables` parses it to `{family,size,weight,lineHeight,…}` (a field may itself be a
  var-name ref like `size/text-lg`). Shadows are `Effect(…)` → the `effect` family. `classify()` buckets by VALUE.
- **`get_metadata` returns XML and TRUNCATES on large frames** (a table view blew past the token limit). When it
  truncates: read the child node ids from the partial XML and `get_design_context`/`get_metadata` the **sub-node**,
  not the parent. Capture each sub-node to the store so you never re-fetch.
- **Node-ids: the URL uses `1-6965`, the API uses `1:6965`.** `capture-figma` canonicalizes to dash form, so a
  capture is found whichever way it's passed next. Always pass the node from the URL as-is.
- **Persistence + screenshot↔node linking are solved by Job 0** — the store keeps every output with its node-id in
  the manifest, so you don't hand-cross-reference screenshots or re-call MCP (both were real friction before).

## Two jobs (both consume the Job-0 store)

### Job 1 — foundation tokens → `Foundations/Colors|Tokens|Type` (sb-figma writes these directly)

No other skill maps Figma *variables* to code tokens, so sb-figma owns the foundation parity end to end.

1. **Normalize the captured variables** — after Job 0 stored `get_variable_defs`, point the normalizer at the
   stored file: `node scripts/pull-figma-variables.mjs --from-mcp .storybook/figma/get_variable_defs/<NODE>.json --out .storybook/figma-variables.json`
   (with no `--from-mcp`, it reuses the last `--out` cache — the headless degrade path). Captures **colors,
   spacing, and type** (`wght`/`text`/`leading`).
2. **Build parity** — `node scripts/build-token-parity.mjs --variables .storybook/figma-variables.json --css <token-css-glob> --out .storybook/figma-token-parity.json`.
   Resolves OKLCH channel triplets → hex, maps each Figma `semantic/*` → the project's `--token`
   (following `var()` alias chains), and emits a `{ token: { figmaVar, figmaHex, mapsTo, drift } }` map for all
   three families.
   Pass `figmaParity` to `TokenMatrix` (it reads `figma-token-parity.json` itself) to surface **drift**
   right in the color table's issue column — `figma Δ` with `code #X vs figma #Y` on hover — so design↔code
   parity lives next to the token, not only in `docs/figma-token-parity.md`.
3. **Wire** the foundation stories — `Colors.stories.tsx` / `Tokens.stories.tsx` (+ a `Type` group) read
   `figma-token-parity.json` and pass `figmaVar`/`figmaHex` into `TokenMatrix` rows (and the spacing/type
   sections). The fields are optional — a project with no Figma file renders exactly as before.
4. **Drift** — the parity map flags Figma-value ≠ code-computed-value (OKLCH→hex tolerance for color, exact
   for spacing/type) and lists **app-only roles** (`--popover`, `--ring`, …) as *expected*, not failures.
   Report in the sb-health shape.

### Job 2 — approved Figma component → production (sb-figma delivers; sb-stories authors)

1. **Extract (via Job 0 store)** — capture `get_design_context` for the node (fall back to `get_metadata` then
   a sub-node fetch if truncated) + `get_screenshot`, then read them back from `.storybook/figma/`. The
   variant list + node-id come from the stored design-context, so re-runs don't re-hit MCP.
2. **Audit before adding** — grep for an existing component covering the same concept; extend it rather than
   duplicate (mirrors guardrails §8 step 3).
3. **Build** the component with approved tokens/primitives only — **tokens, not magic numbers**; if a Figma
   value has no token, **stop and ask** (it's a missing-token task, route to Job 1 or the user).
4. **Author the story by following `sb-stories`' conventions** — materially-different states only (no
   Cartesian), a factory when 3+ stories share a shape. Do **not** reinvent CSF3 rules; load `sb-stories`.
5. **Stamp + embed** — node-id in a top-of-file comment, and `parameters.design` (see Shared plumbing).
6. **Validate** — light / dark / mobile, screenshot-vs-implementation parity.
0. **Size the delivery FIRST — chunk a big board into parts.** A multi-artboard feature (a whole flow,
   a screen with many sections) blows past the MCP token budget and produces a "too long, what's the
   status?" mega-pass. Split by **artboard / section**: deliver + validate + record one part, then the
   next. The Figma Inventory (step 7) accretes stories across parts (union by id), so an incremental
   delivery is first-class, not a workaround. Don't attempt the whole board in one turn.
7. **Record the delivery in the Figma Inventory** — so the stories this feature created don't just scatter
   across the taxonomy. Run the recorder (idempotent; re-run per delivery, stories union by id):
   ```bash
   "${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/scripts/record-figma-delivery.py" . \
     --figma-url "<board url>" [--feature "<Name>"] --spec-url "<spec node url>" --node-ids 101-9717 \
     --description "<one line>" \
     --story "Hunts/Hunt Packs:hunts-hunt-packs--default:component"   # repeat per story you created
   ```
   Then ensure the root surface exists: scaffold once with `scaffold-wrapper.sh --figma`, drop the
   `figma-inventory.stories.tsx` template (title `Figma Inventory`), add **one export per feature**
   (`export const Hunts = { args: { feature: 'Hunts' } }`), and pin it to the top in `.storybook/preview`
   via `options.storySort.order: ['Figma Inventory', '*']`. The `FigmaInventory` wrapper reads
   `figma-inventory.json` and renders the index + each feature's board link + the stories it brought in.
   (Spec: `docs/specs/2026-06-23-figma-feature-inventory.md`.)

### Job 3 — Connect: Storybook → Figma (the reverse direction, code→design)

The reverse of Jobs 1–2: push the code's truth back to Figma so Dev Mode shows your real components. Driven
from the Storybook side, fed by context the bundle already has — **no new scanners**.

1. **Gather** — for each component that has a story AND a Figma node (the `parameters.design` node-id from
   deliverable #8): its used tokens (from `figma-token-parity.json`), real prop values (from
   `component-usage.json`), variants (from the CSF3 stories), and — from `get_metadata` — its **Figma variant
   properties** (`{type:[root,nest-1,nest-2,nest-3]}`) and **modes** (`[Light,Dark]`). Assemble a `comps.json`
   (`variantProperties` + `modes` + optional `propAliases` to rename a Figma prop, e.g. `type→depth`).
   `build-code-connect` maps each variant property → a code prop with its value enum, and carries the modes as
   the theme dimension — so the Code Connect mapping drives a variant-rich component from Figma's variant picker.
2. **Build the payload** — `build-code-connect.mjs --components comps.json --parity .storybook/figma-token-parity.json
   [--usage .storybook/component-usage.json] --out .storybook/code-connect.json`. It enriches each token with its
   `figmaVar` + value, canonicalizes node-ids, and emits a **reverse-parity report**: components with no Figma
   node, drifted tokens, tokens not in the parity map.
3. **Push (the agent, via MCP)** — `send_code_connect_mappings` / `add_code_connect_map` with the
   `mappings[]` from `code-connect.json`. This is the **primary, low-risk** path — it makes Figma Dev Mode
   show the real code/props/tokens. **Gate the push** (it writes to Figma): confirm before sending.
4. **Generate (opt-in, OFF by default)** — for a component in `componentsWithoutNode`, `generate_figma_design`
   from the code + story (foundation tokens supplying real values). It *creates* design artifacts, so only on
   explicit user intent.

The loop closes: the `parameters.design` node-id added when *delivering* (Jobs 1–2) is what Job 3 reads to
*connect back*. Capture any `get_code_connect_map` / suggestions to the Job-0 store like every MCP call.

## Shared plumbing — the Figma design embed (Docs)

Every story sb-figma touches gets the design source preserved on its catalog page:

```ts
parameters: { design: { type: 'figma', url: 'https://figma.com/file/<FILE_ID>?node-id=<NODE_ID>' } }
```

This is `@storybook/addon-designs` (the "Design" tab — the same mechanism `sb-explore` uses for frames). Plus
a node-id stamp + link in `parameters.docs.description`. `sb-explore` and `sb-stories` can reuse this snippet
whenever the node-id is known.

## Boundaries — never duplicate a sibling's verb

- **Exploration / "try a v2" / undecided** → `sb-explore` (Lab). sb-figma is for *approved* designs only.
- **Graduating a Lab experiment** → `sb-ship` (preserve `cp`, rewrite callsites). sb-figma delivers from
  *Figma*, not from a `/explore/` experiment.
- **Documenting an existing code component (no Figma)** → `sb-stories`. sb-figma *calls* sb-stories' rules to
  author; it never reimplements them.
- **Code-internal token health / orphans** → `sb-health` / `sb-inventory` (Figma-free). sb-figma adds the
  *design↔code* parity those can't see.

## Inputs the agent must resolve first

- **Figma file id** + **variables node id** (the variables/styles spec frame) — ask if not pasted.
- **Token CSS path(s)** — where `--token: <value>` declarations live (e.g. `src/styles/**/*.css`).
- **Is the design approved?** If the user is still iterating → stop, route to `sb-explore`.

## Next

Run Job 1 (tokens) first so components built in Job 2 consume real, parity-checked tokens. Append progress to
`.storybook/audit/status.md` for clean resume. Full call sequence + the OKLCH→hex notes:
`references/figma-token-sync.md`.
