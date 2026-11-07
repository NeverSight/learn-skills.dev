---
name: btp-diagram-generator
description: "Generate SAP BTP (Business Technology Platform) solution architecture diagrams as native draw.io (.drawio) files following the official SAP BTP Solution Diagram guidelines (Fiori Horizon design system) and open them via a configured draw.io MCP server. USE WHEN: user asks to create/draw/design/sketch a BTP diagram, BTP architecture, BTP landscape, BTP solution diagram, BTP reference architecture, SAP Business Technology Platform diagram, or wants to visualize SAP BTP services (CAP, Build, Integration Suite, SAC, AI Core, HANA Cloud, Cloud Foundry, Kyma, Workzone, etc.) and their interdependencies in draw.io / drawio / diagrams.net. DO NOT USE FOR: non-BTP architecture diagrams, generic flowcharts, sequence/UML diagrams, or diagrams that should remain in Mermaid/PlantUML."
---

# BTP Solution Diagram Generator

Produces a `.drawio` file in the workspace that conforms to the [SAP BTP Solution Diagram guidelines](https://sap.github.io/btp-solution-diagrams/) and opens it through whichever [draw.io MCP server](https://www.drawio.com/doc/faq/ai-drawio-generation) is configured.

Its validation and delivery discipline is informed by [Archify](https://github.com/tt-a1i/archify): deterministic artifacts, machine-readable repair receipts, explicit quality gates, last-good preservation, and separate automated versus perceptual review claims.

## ⚡ Quick Path (use this first)

For the vast majority of diagrams, **do not hand-write XML**. Use the `btp_builder` Python package — it owns icon lookup, SAP palette, port pinning, label HTML, A4 sizing, SVG upscaling, and validation. A typical L1 diagram is ~20 lines.

```python
# scripts/examples/task_center_arch.py — runnable end-to-end
import sys
from pathlib import Path
# Add the skill's scripts/ dir to sys.path so `btp_builder` imports work
# regardless of where the skill is installed
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from btp_builder import BtpDiagram

d = BtpDiagram(level="L1", title="Task Center Reference Architecture")

btp = d.btp_container(x=260, y=80, w=560, h=440)
sub = d.subaccount(parent=btp, label="Subaccount",
                   x=btp.x + 24, y=btp.y + 110, w=520, h=170)

wz = d.service("work zone",   in_=sub, x=sub.x + 60, y=sub.y + 60)
tc = d.service("task center", right_of=wz)
ci = d.service("cloud identity", below=tc)

eu = d.user("End User", x=60, y=btp.y + 100)
ac = d.app_client("Application Clients\n(Mobile or Desktop)", below=eu)

s4    = d.external("SAP S/4HANA\nOn-Premise Solutions",
                   x=btp.right_edge() + 40, y=btp.y + 70, kind="sap")
third = d.external("3rd Party\nApplications", below=s4, kind="non-sap")
cloud = d.external("SAP Cloud\nApplications", below=third, kind="sap")
idp   = d.idp("3rd-party Identity Provider",
              x=ci.center_x() - 140, y=btp.bottom_edge() + 60)

d.connect(eu, ac, direction="down")
d.connect(ac, wz, direction="right")
d.connect(wz, tc, kind="dblhd")
d.connect(tc, ci, kind="dblhd", direction="down")
d.connect(tc, s4); d.connect(tc, third); d.connect(tc, cloud)
d.connect(idp, ci, kind="dashed", direction="up")

d.save("btp-task-center-architecture.drawio")  # validates, then atomically commits
```

Run via `uv run python <script>.py` from the repository root. `save()` validates first and raises `ValueError` with the full error list if anything is off; warnings are printed.
Builder output is deterministic: the same authored diagram produces identical XML bytes and a stable diagram ID. `save()` writes a same-directory candidate and atomically replaces the target only after validation, so a failed commit preserves any prior artifact.

### Quick-Path API surface

| Call                                                        | Returns   | Notes                                                                                                                                                       |
| ----------------------------------------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `BtpDiagram(level, title)`                                  | builder   | level ∈ `L0`/`L1`/`L2`. Drives icon size + label weight.                                                                                                    |
| `.btp_container(x,y,w,h, sub_label, env_label, with_logo)`  | `NodeRef` | Light-blue outer frame + SAP corner logo + Subaccount/Multi-Cloud labels.                                                                                   |
| `.subaccount(parent, label, ...)`                           | `NodeRef` | White card inside the BTP container.                                                                                                                        |
| `.inner_card(parent, label, ...)`                           | `NodeRef` | Generic white sub-card (e.g. CIS service group).                                                                                                            |
| `.service(name, in_=, right_of=, left_of=, below=, above=)` | `NodeRef` | `name` is fuzzy-matched via [references/icon-aliases.json](references/icon-aliases.json) (e.g. `"task center"`, `"cpi"`, `"hana cloud"`).                     |
| `.user(label, kind="sap")`                                  | `NodeRef` | kind ∈ `sap` / `non-sap` / `highlight`.                                                                                                                     |
| `.app_client(label, ...)`                                   | `NodeRef` | Generic mobile/desktop tile.                                                                                                                                |
| `.external(label, kind="sap"/"non-sap", ...)`               | `NodeRef` | Right-side external system tile.                                                                                                                            |
| `.idp(label, ...)`                                          | `NodeRef` | 3rd-party Identity Provider tile.                                                                                                                           |
| `.connect(src, tgt, kind, direction)`                       | edge id   | `kind` ∈ `std`/`dblhd`/`dashed`/`optional`/`auth`/`scim`/`trust`/`neutral`. `direction` auto-pins ports — override with `"right"`/`"left"`/`"up"`/`"down"`. |
| `.save(path, validate=True)`                                | `Path`    | Validates, then atomically commits deterministic XML (raises on errors).                                                                                    |

Positional kwargs (`right_of`, `left_of`, `below`, `above`, `in_`) auto-place nodes — only set explicit `x,y` for the first anchor in each row/column.

### Icon name discovery

```python
from btp_builder import list_aliases, list_icons, lookup_icon
print(list(list_aliases())[:30])     # short names → canonical keys
print(lookup_icon("integration suite", "L1")["key"])
```

If `lookup_icon` raises `IconNotFound`, fall back to a styled tile (`external(label, kind="sap")`) and call it out in the final response.

### Open the diagram

```sh
uv run python skills/btp-diagram-generator/scripts/open_diagram.py btp-task-center-architecture.drawio
```

Falls back to printing a `https://app.diagrams.net/?…#create=...` URL if no system opener is found. If a draw.io MCP tool is available in the runtime, prefer that — only call MCP tools that actually appear in the tool list.

---

## Manual XML path (advanced / niche cases only)

Use this only when the Quick Path doesn't cover what you need (e.g. exotic legend variants, custom flow-protocol pills, novel layouts not yet supported by the builder). Everything below documents the underlying XML primitives the builder generates for you.

## When to use

Trigger on requests like:

- "Draw a BTP architecture for …"
- "Generate a BTP solution diagram showing CAP + HANA Cloud + Build Workzone"
- "Create a draw.io of our SAP BTP integration landscape"
- "L0 / L1 / L2 BTP diagram for <use case>"

If the request is a generic flowchart, sequence diagram, or non-SAP architecture, do not use this skill — generate Mermaid or use a plain draw.io workflow instead.

## Inputs to gather (ask once, concisely)

Before generating, confirm what is missing. Default to L1 if unspecified.

| Input                    | Default              | Notes                                                                                                                                                                  |
| ------------------------ | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Audience level           | L1                   | L0 = business overview (no legend, neutral connectors); L1 = technical (services + main flows); L2 = detailed (data flows, protocols, components)                      |
| BTP services / SaaS apps | (must ask)           | e.g. CAP, Build Code, Integration Suite (CPI/Event Mesh/API Mgmt), HANA Cloud, SAC, AI Core, Joule, Build Workzone, Identity Authentication, Destination, Connectivity |
| Non-BTP systems          | (optional)           | e.g. S/4HANA Cloud, SuccessFactors, Ariba, third-party SaaS, on-prem systems, end users                                                                                |
| Environment / runtime    | Cloud Foundry        | Cloud Foundry, Kyma, ABAP Environment                                                                                                                                  |
| Region / multi-region?   | single               | Affects grouping containers                                                                                                                                            |
| Primary flows            | (must ask)           | What connects to what, direction, purpose                                                                                                                              |
| Output format            | `.drawio` + PNG      | `.drawio` always; optionally export PNG (`-s 2`), SVG, or PDF via draw.io CLI                                                                                          |
| Output filename          | `btp-diagram.drawio` | Saved to workspace root unless user specifies                                                                                                                          |

If the user gives a one-line prompt with enough services and a clear flow, proceed without asking — surface assumptions in the final response.

## Component allowlist discipline

Before layout, create an explicit **component allowlist** from the request:

1. List requested actors, clients, services, targets, and any architecturally required supporting services (e.g. CIS for authentication flows).
2. **Do not add familiar products as decoration.** SAP Build Work Zone, SuccessFactors, or extra posting targets appear only when explicitly requested or required by a described flow.
3. **Preserve the requested sequence** as an ordered edge list. E.g. `Outlook → Document AI → Integration Suite → S/4HANA Cloud` means exactly those adjacent edges — do not insert intermediary steps or additional targets.

## Workflow

### 1. Map requirements to BTP icons

> **There is no `mxgraph.sap.*` stencil family.** SAP BTP icons in draw.io are SVGs embedded as base64 inside `shape=image;image=data:image/svg+xml,<base64>;…` style strings, distributed via the [SAP draw.io shape library XML files](https://github.com/SAP/btp-solution-diagrams/tree/main/assets/shape-libraries-and-editable-presets/draw.io). Generating `shape=mxgraph.sap.foo` produces an empty square in the canvas — you have seen this fail.

For every requested service, obtain its real `style` string by looking it up in [references/icon-index.json](references/icon-index.json):

1. **Preferred:** Load [references/icon-index.json](references/icon-index.json) (~660 KB, 100 icons). It maps each icon title (e.g. `31068-sap-build-work-zone_sd`) to its `style` string and library cell `width`/`height`. Match by substring against the requested service name.
2. **Source XML libraries** (if you need a non-default size or a metadata field the index doesn't carry) live in [references/libraries/](references/libraries/) — one size-M `mxlibrary` per icon set (foundational, integration suite, app-dev, AI, data-analytics, BTP-SaaS, all-in-one).
3. **Style donors:** for compound patterns (subaccount cards, NETWORK boundaries, pill labels, legend cards), consult the curated [references/examples/](references/examples/) — 11 official editable diagrams (Task Center L0/L1/L2, Build Work Zone L2, Process Automation L2, Cloud Identity Services L1/L2, Private Link L2, SAP Start L2). Open any of them and copy the exact style string.
4. If a service is genuinely missing from the library, use the styled fallback tile (see §3 below) and **list it in the final response** so the user can replace it.

Default icon geometry by audience level (matches the official examples — see [references/example-patterns.md §5](references/example-patterns.md)):

> **SVG intrinsic size warning:** Every icon in the SAP shape library has `width="16" height="16"` on its root `<svg>` element, even in the size-M set. draw.io rasterizes at that intrinsic size then upscales, producing a blurry icon. After extracting a base64 SVG, patch the root `<svg width>` and `<svg height>` to match the target cell size (e.g. 48 for L1) before re-encoding. Keep `viewBox` unchanged. See [references/example-patterns.md §11](references/example-patterns.md) for the Python helper.

| Level | Icon size | Label            |
| ----- | --------- | ---------------- |
| L0    | 50×50     | Arial 14 bold    |
| L1    | 48×48     | Arial 14 bold    |
| L2    | 32×32     | Arial 12 regular |

The label goes in the cell's `value=` attribute and renders below the icon (the library style already sets `verticalLabelPosition=bottom`). Always keep the `points=[[0,0,0,0,0],…]` 12-anchor array from the library style so connectors snap cleanly.

### 2. Apply the SAP Fiori Horizon palette

Always use these colors only (never pick arbitrary fills). Source: SAP BTP Solution Diagram guideline — _Foundation (Atoms)_ and _Areas_:

| Token                      | Hex                      | Use                                                           |
| -------------------------- | ------------------------ | ------------------------------------------------------------- |
| SAP/BTP border (Primary)   | `#0070F2`                | BTP container stroke, accent fills, sub-card stroke           |
| SAP/BTP fill               | `#EBF8FF`                | BTP container background                                      |
| Non-SAP border             | `#475E75`                | Non-SAP / external area strokes, generic data-flow connectors |
| Non-SAP fill / Subtle bg   | `#F5F6F7`                | Non-SAP areas, page background, generic pill fill             |
| Title text                 | `#1D2D3E`                | Headings, primary labels                                      |
| Secondary text             | `#556B82`                | Sub-labels, descriptions, footnotes                           |
| Positive (Auth, green)     | `#188918` / bg `#F5FAE5` | Authentication flows (SAML, OIDC) — per guideline             |
| Critical (Warning, orange) | `#C35500` / bg `#FFF8D6` | Warnings                                                      |
| Negative (Error, red)      | `#D20A0A` / bg `#FFEAF4` | Errors                                                        |
| Teal accent                | `#07838F` / bg `#DAFDF5` | Highlight areas                                               |
| Indigo (Authorization)     | `#5D36FF` / bg `#F1ECFF` | Authorization / provisioning (SCIM) flows — per guideline     |
| Pink (Trust)               | `#CC00DC` / bg `#FFF0FA` | Trust flows (mutual trust, federation) — per guideline        |

Font: `Arial` (or `Arial Black` for headings), size 12 for body labels, 14 for service labels, 16 for group titles.

### 3. Apply the atomic structure

Per the SAP atomic design system (Atoms → Molecules → Organisms). The exact style strings, sizes and HTML label patterns to copy live in [references/example-patterns.md](references/example-patterns.md) — match those rather than inventing variants.

- **Document title** (every diagram): a floating text cell above the BTP container, blue `#0070F2` bold Arial 16, format `"{Scenario} - SAP BTP Solution Diagram"`.
- **Outer container** (Subaccount / Multi-Cloud): `rounded=1;strokeColor=#0070F2;fillColor=#EBF8FF;arcSize=32;absoluteArcSize=1;strokeWidth=1.5;`. Carries the SAP-logo image tile in the top-left and two stacked labels: bold `Subaccount` (Arial 16) + smaller `Multi-Cloud` (Arial 12).
- **Sub-containers** (white cards inside the BTP boundary — e.g. Cloud Identity Services group): same `#0070F2` stroke, `#FFFFFF` fill, `arcSize=16`. **Always blue stroke, never slate**, when the card sits inside the BTP container. Per the guideline _Areas / Nesting_: alternate fill vs. no-fill between parent and child to keep visual contrast (BTP container has fill `#EBF8FF`, so inner cards use white).
- **Service nodes**: BTP icons (§1) wrapped in a `style="group" connectable="0"` cell whenever they need a separate text label or are co-positioned with another shape. Children use coordinates relative to the group origin.
- **External-system tiles** (e.g. `SAP S/4HANA On-Premise`): a group of (white card `arcSize=14` + ~28×28 icon top-left + bold `font-size:16px` label on the right). Sit outside the BTP container.
- **Users / actors**: a `group` containing the user SVG image and a centered `End User` text label below.
- **Connectors** — copy the right variant from the example patterns reference. Per the guideline _Connectors_ section, line _style_ encodes flow nature and line _color_ encodes flow semantic:
  - **Line style:** solid = direct synchronous request/response · `dashed=1` = indirect / asynchronous · `dashed=1;dashPattern=1 4;` (dotted) = optional · `strokeWidth=3` = **firewalls / network barriers only**.
  - **Semantic color:** Authentication = green `#188918` · Authorization / Provisioning (SCIM) = indigo `#5D36FF` · Mutual trust / federation = pink `#CC00DC` · Generic data = slate `#475E75`.
  - Standard data flow: `endArrow=blockThin;strokeColor=#475E75;endFill=1;endSize=4;startSize=4;strokeWidth=1.5;`
  - Orthogonal: prefix with `edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;`
  - Authentication (SAML/OIDC): same shape, `strokeColor=#188918`
  - Authorization / Provisioning (SCIM): same shape, `strokeColor=#5D36FF`
  - Mutual trust: add `startArrow=blockThin;startFill=1` and `strokeColor=#CC00DC`
  - Async / indirect: use `edgeStyle=entityRelationEdgeStyle;rounded=0;html=1;strokeColor=#475E75;strokeWidth=1.5;endArrow=blockThin;endFill=1;endSize=4;startArrow=none;startFill=0;startSize=4;jumpStyle=none;jumpSize=0;targetPerimeterSpacing=15;dashed=1;` (the official SAP indirect connector style — `entityRelationEdgeStyle` + `targetPerimeterSpacing=15`)
  - Optional: add `dashed=1;dashPattern=1 4;` (dotted) to the async style above
  - Network / firewall boundary line: thick grey vertical separator `strokeColor=#475E75;strokeWidth=3;jumpStyle=gap;` with a small uppercase `NETWORK` label (`#475E75`) beside it. **Reserve `strokeWidth=3` for firewalls/network barriers only** — do not use it for normal data flows.
  - **Always pin exit/entry ports** to avoid diagonal auto-routing: add `exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;` (adjust X/Y for the direction). For vertical connectors use `exitY=1` / `entryY=0`. **Remove manual `<mxPoint>` waypoints** unless a deliberate detour is needed — leave `<Array as="points"/>` empty. See [references/example-patterns.md §8](references/example-patterns.md) for the full port-pinning reference.
- **Edge labels** are _separate vertex pills_, not inline edge text — small rounded rectangles `arcSize=50`, ~16 px tall, color-matched to the connector (generic `#475E75`/`#F5F6F7`, auth `#188918`/`#F5FAE5`, authz/SCIM `#5D36FF`/`#F1ECFF`, trust `#CC00DC`/`#FFF0FA`).
- **L0**: no legend, no protocol pills, neutral `endArrow=block` or `endArrow=none` connectors.
- **L1**: directional `endArrow=blockThin` connectors, optionally a few colored auth/provisioning flows and pill labels.
- **L2**: add a description block + `Diagram Level: L2` under the title, pill tags on every meaningful edge, and a **legend card** in the top-right (white card, `strokeColor=#eaecee`, with colored 16×16 ellipse swatches for each flow type and a sample arrow per arrow style).

### 4. Generate the draw.io XML

Follow the [draw.io AI generation rules](https://www.drawio.com/doc/faq/ai-drawio-generation):

- Use **uncompressed** XML, full `<mxfile>` wrapper (so file-level vars are usable).
- Always include `<mxCell id="0"/>` and `<mxCell id="1" parent="0"/>`.
- Vertices: `vertex="1"`. Edges: `edge="1"` with `source`/`target`. Mutually exclusive.
- Unique IDs across the diagram.
- Coordinates: top-left `(0,0)`, x→right, y→down. Children inside a group use coordinates _relative_ to the group.
- Match perimeter to shape (e.g. `perimeter=ellipsePerimeter` for ellipses).
- XML-escape labels (`&amp;`, `&lt;`, `&gt;`, `&quot;`). HTML markup inside `value=` is allowed and is the standard way to bold/size text — see the official examples.
- **HTML label escaping:** Build the full HTML string first (tags + text, with plain `<`/`>`/`"`), then apply **one** complete escape pass (`&`→`&amp;`, `<`→`&lt;`, `>`→`&gt;`, `"`→`&quot;`) before inserting into the `value="…"` attribute. When using `xml.etree.ElementTree`, pass the unescaped value and let the serializer escape it. Parse the written file with a real XML parser and reject any visible label containing `<font`, `&lt;font`, or `<div`.
- Use `container=0;` on area shapes (BTP boundary, subaccount cards) — not draw.io container behavior — so connectors route correctly through them.
- Keep grid spacing on multiples of 10 px (`gridSize="10"`); leave ≥20 px gaps between siblings; sub-containers padded by ~18–24 px.
- It is normal and expected for diagrams to be authored in **negative** coordinate space (e.g. `x="-2200"`); draw.io centers on content.
- Every edge `mxCell` MUST contain `<mxGeometry relative="1" as="geometry" />` — self-closing edge cells are invalid and will not render.

Page size: **always A4 landscape** — `pageWidth="1169" pageHeight="827"`, even for dense L2. Larger virtual canvas comes from spreading groups across negative coordinates, not from changing the page size. L2 additionally sets `background="none"` on `<mxGraphModel>`.

### 5. Write the file

Save to the path the user requested (default: workspace root, `btp-diagram.drawio`). Do not overwrite an existing file without confirming.

### 6. Open via the MCP server

Detect which draw.io MCP integration is available, in this order — use the first that is configured:

1. **MCP Tool Server** (`@drawio/mcp` / `npx @drawio/mcp`): call its "open diagram" tool with the generated XML to launch the editor in the browser.
2. **MCP App Server** (`mcp.draw.io/mcp` remote): call its render tool to embed the interactive viewer inline in chat.
3. **Neither configured**: skip silently and instead print a `https://app.diagrams.net/?pv=0&grid=0#create=...` URL built per the FAQ (URI-encode JSON `{"type":"xml","compressed":true,"data":"<base64-deflate-raw>"}`). If you cannot compress in-context, print the file path and instruct the user to open it in their installed draw.io.

Never invent an MCP tool name — only call tools that actually appear in the available tool list.

### 7. Validate before delivering

Validate after every candidate edit. Use `standard` while iterating; it accepts warnings but reports them. Use `showcase` for final delivery; every warning becomes a blocking error.

```sh
python3 skills/btp-diagram-generator/scripts/validate_diagram.py \
  <file.drawio> --quality standard --json

python3 skills/btp-diagram-generator/scripts/validate_diagram.py \
  <file.drawio> --quality showcase --json
```

The JSON receipt includes stable diagnostic codes, the exact local subject, supported fixes, per-check status, and the artifact byte count and SHA-256. On failure, change only the diagnosed subject and rerun validation. If two consecutive repairs do not reduce the error count, stop and report the unresolved diagnostics rather than rewriting the whole diagram.

A passing final `showcase` receipt freezes the artifact: do not edit it afterward. Only open or export the exact file that passed. If validation or save fails and an older output exists, that file is the last-good artifact, not the rejected candidate.

If it warns about blurry icons (SVG intrinsic size smaller than cell), fix in place:

```sh
python3 skills/btp-diagram-generator/scripts/upscale_svg_icons.py <file.drawio> --size 48 --in-place
```

Automated validation proves XML structure, connector/style contracts, and byte identity. It does not prove perceptual polish. Separately verify these remaining items by eye:

- [ ] All labels XML-escaped (no raw `<font>` visible).
- [ ] No overlapping shapes (≥20px gap).
- [ ] BTP container visually encloses all BTP services; external systems sit outside it.
- [ ] L0 diagrams have no legend and neutral connectors; L2 includes a legend card top-right and a description block under the title.
- [ ] Edge labels are pill _vertex_ cells, not inline `value=` text on the `edge="1"` cell.
- [ ] Connectors do not cross through unrelated containers.
- [ ] No unrequested components present (check against the allowlist).
- [ ] Service sequence matches the user's requested order.
- [ ] CIS is outside the Subaccount but inside BTP.
- [ ] Legend (if present) does not overlap any connector.

The validator covers everything else: root cells, unique IDs, vertex/edge exclusivity, no `mxgraph.sap.*`, edge source/target validity, port pinning, manual waypoints, SVG intrinsic size vs cell geometry, palette colors, and A4 landscape page size.

For deeper validation, reference [`mxfile.xsd`](https://github.com/jgraph/drawio-mcp/blob/main/shared/mxfile.xsd) and the [style reference checklist](https://github.com/jgraph/drawio-mcp/blob/main/shared/style-reference.md#15-validation-checklist-for-ai-generated-files).

## Final response template

When done, respond with:

1. The saved file path as a workspace-relative markdown link.
2. Whether the diagram was opened in the MCP editor (and how), or the fallback URL/instructions.
3. The final quality profile, check count, error/warning totals, artifact SHA-256, and byte count from the JSON receipt.
4. The visual-review status, stated separately from automated validation.
5. A short bullet list of **assumptions made** and any **icons that fell back** to generic tiles, so the user can correct them.
6. If the diagram opened in a draw.io workspace using **dark theme**, mention that SAP labels (`#1D2D3E`) are intentionally dark per the Fiori Horizon spec and will appear faint on dark canvas — switch draw.io to light theme or export to PNG/SVG to verify.
7. One sentence on how to iterate (e.g. "ask me to add X service or change the audience level to L2").

## Bundled assets

- [references/icon-index.json](references/icon-index.json) — flat `{title → {style, width, height}}` map of all 100 BTP service icons + 3 generic user icons (`generic:user-sap` / `-non-sap` / `-highlight`). **Primary lookup source for icon styles.** The Quick-Path builder reads this for you.
- [references/icon-aliases.json](references/icon-aliases.json) — short-name → canonical-key map (132 aliases like `"task center"`, `"cpi"`, `"hana cloud"`, `"end user"`). Drives the fuzzy lookup in `BtpDiagram.service()`.
- [references/styles.json](references/styles.json) — named SAP style strings (`container_btp`, `card_subaccount`, `tile_external_sap`, `arrow_dblhd`, `pill_auth`, …) + port-pin fragments + per-level icon sizes. Loaded by the builder; useful as a copy-paste reference when hand-authoring XML.
- [references/templates/](references/templates/) — empty L0/L1/L2 mxfile skeletons, ready to fill in.
- [references/sap-logo.b64.txt](references/sap-logo.b64.txt) — base64 of the SAP corner logo SVG, embedded by `btp_container(with_logo=True)`.
- [references/libraries/](references/libraries/) — the 7 official SAP draw.io `mxlibrary` XML files (foundational, integration-suite, app-dev-automation, data-analytics, AI, BTP-SaaS, and the all-in-one size-M set). Use when you need raw library data the index doesn't expose.
- [references/svg/](references/svg/) — 129 raw `.svg` source files for every BTP service icon. Use when you need to edit/recolor an icon, export to non-draw.io targets, or embed an icon outside a draw.io style string.
- [references/examples/](references/examples/) — the 11 official editable example diagrams (Task Center L0/L1/L2, Build Work Zone L2, Process Automation L2, Cloud Identity Services L1/L2, Private Link L2, SAP Start L2). **Primary source for compound style patterns** (subaccount card, network boundary, pill labels, legend card).
- [references/sap-btp-palette.json](references/sap-btp-palette.json) — the exact color tokens above, ready to paste into draw.io `Extras → Configuration` `customColorSchemes`.
- [references/example-patterns.md](references/example-patterns.md) — ready-to-copy style strings, sizes, label HTML and connector/pill recipes extracted from the example diagrams. **Consult this whenever you need the exact style of a container, icon, edge or pill — do not improvise.**

## Bundled scripts

In `scripts/`, runnable with `uv run python` (no third-party dependencies):

- [scripts/btp_builder/](scripts/btp_builder/) — **the Quick-Path package**. `BtpDiagram` DSL, icon lookup with alias resolution, palette constants, port-pin helpers, SVG upscaling, named styles. Import as `from btp_builder import BtpDiagram`.
- [scripts/examples/task_center_arch.py](scripts/examples/task_center_arch.py) — runnable canonical example reproducing the Task Center reference architecture end-to-end.
- [scripts/open_diagram.py](scripts/open_diagram.py) — opens a `.drawio` file via the OS opener (macOS `open`, Linux `xdg-open`, Windows `start`); falls back to printing an `app.diagrams.net` URL.
- [scripts/validate_diagram.py](scripts/validate_diagram.py) — enforces the §7 checklist. Catches `mxgraph.sap.*` typos, duplicate IDs, edges with broken source/target, missing port pins, manual waypoints, off-palette colors, and SVG intrinsic-size blur. Use `--quality showcase --json` for a zero-warning final gate and machine-readable receipt. The legacy `--strict-palette` and `--strict-waypoints` flags remain available. Also exposes `validate_xml(xml)` / `validate_path(path)` for reuse from Python.
- [scripts/upscale_svg_icons.py](scripts/upscale_svg_icons.py) — fixes blurry icons by patching the root `<svg>` `width`/`height` to match the cell geometry (keeps `viewBox` unchanged). Default target 48 px; pass `--size 32` for L2, `--size 50` for L0. Use `--in-place` to overwrite. (The Quick-Path builder applies this automatically; only run manually on hand-authored XML.)

## Layout tips

### Avoiding overlapping connectors

When generating diagrams with many connections:

1. **Pin exit/entry points** — always set explicit `exitX`, `exitY`, `entryX`, `entryY` on connectors to control exactly where they leave/arrive at shapes.
2. **Distribute across perimeter** — for N connections from one shape, distribute exit points: e.g. 3 on bottom → `exitX=0.25`, `0.5`, `0.75` (never all at `exitX=0.5`).
3. **Use waypoints** — for complex routing, add `<mxPoint>` waypoints inside `<Array as="points">` to force edges through specific corridors.
4. **Stagger vertical spacing** — place elements with many connections at different Y-levels so connectors have room.
5. **Separate flow types visually** — use different sides of shapes for different flow types (data flows exit right, auth flows exit bottom).
6. **Prefer one connector to a shared destination area** — if S/4HANA and SuccessFactors sit inside one "SAP Cloud Solutions" area, use a single connector to the area boundary rather than fanning out.
7. **Place external targets in a side column** — align the external area horizontally with the integration hub, as in SAP reference diagrams.

### Connectors must NOT cross through containers

Lines must never visually pass through a container they are not connecting to.

1. Trace the full path (all segments) and verify it doesn't intersect any unrelated container's bounding box.
2. Position containers to avoid line corridors.
3. Verify each orthogonal segment independently: vertical at X=V must not cross a container spanning that X; horizontal at Y=H must not cross a container spanning that Y.

### Straight & uniform lines (minimize bends)

Zero bends is preferred; one 90° bend is the normal maximum. Two or more bends only when an obstacle makes them unavoidable.

1. **Align elements by center coordinates** — if two elements should have a straight connector, ensure they share the same X center (vertical lines) or Y center (horizontal lines).
2. **Design layout around connector geometry** — decide straight-line constraints first, then position elements.
3. **Enforce a bend budget:** 0 bends = shared center axis; 1 bend = pin one `mxPoint`; 2+ = reject and reposition unless obstacle-forced.
4. **Do not trust automatic orthogonal routing** for offset elements — it creates unwanted doglegs. Pin explicit waypoints.

### Connector label clearance

A connector must never pass through an icon label, product name, or area title:

1. Prefer an icon cell with `value=""` plus a **separate text cell** below it.
2. If a vertical connector must continue below an icon, start it from the bottom edge of the label cell, not the icon.
3. Keep horizontal connectors on the icon centerline and labels below (`exitY=0.5`, `entryY=0.5`).
4. Leave at least 20px of straight line before an arrowhead. Never place a bend immediately beside an icon.

### SAP Cloud Identity Services placement

CIS must be **outside the Subaccount but inside BTP** (identity services are provisioned at BTP level, not within a subaccount):

1. Position CIS **below the Subaccount** but within the BTP boundary.
2. Place CIS to the **left** side of BTP so vertical connectors from Integration Suite (right side) don't cross it.
3. CIS container: **white fill** (`#ffffff`) with **grey border** (`#475E75`) — alternating fill pattern (BTP blue → CIS white).
4. CIS → Subaccount: green dashed **bidirectional** OIDC trust connector. SAML 2.0 is NOT used for modern BTP trust — SAML only applies to upstream corporate IdP federation.
5. Show SCIM 2.0 (indigo `#5D36FF`) separately only when identity provisioning is requested.

### Application Clients presentation

Application Clients should be a standalone icon+label, NOT wrapped in a container:

1. Use the App Clients icon from the `"Application and User"` component group.
2. Set icon `value=""` and add a separate text cell below with `value="Application Clients&#xa;Mobile / Desktop"`.
3. Connect horizontal data flows from the icon's side (`exitY=0.5`), not through its label.
4. Do NOT add a container area around it.

### Area nesting fill pattern

Always alternate fill when nesting: `blue → white → blue → white`.

```
L0: BTP Platform   (border #0070F2, fill #EBF8FF)
  L1: Subaccount   (border #475E75, fill #ffffff)
    L2: Service group (border #0070F2, fill #EBF8FF)
  L1: CIS          (border #475E75, fill #ffffff)
```

A direct child of a blue-filled container MUST have white fill (not blue-on-blue).

### Legend placement

The legend MUST NOT overlap any connector or element:

1. Place in an empty corner — bottom-right preferred (flows go L→R, T→B).
2. Trace all connector routes; the legend must not intersect any.
3. Never place between source and target where connectors route.

### Diagram title placement

The title must not be blocked by any container border:

1. Place **above** the BTP container top edge (e.g. title y=10, BTP y=50).
2. OR **inside** BTP with ≥10px padding from the border.
3. Reserve a 45-60px title band at the top of every area.

## Export workflow (draw.io CLI)

### Prerequisites

```bash
# macOS (Homebrew installs as `drawio`, no dot)
drawio --version

# macOS (full path fallback)
/Applications/draw.io.app/Contents/MacOS/draw.io --version

# Linux
draw.io --version

# Windows
"C:\Program Files\draw.io\draw.io.exe" --version
```

Install from [jgraph/drawio-desktop/releases](https://github.com/jgraph/drawio-desktop/releases) if missing.

### Step 1 — Export preview PNG (no `-e`)

```bash
drawio -x -f png -s 2 -o diagram.png diagram.drawio
```

### Step 2 — Self-check

Use vision (if available) to verify the exported PNG:

| Check                  | What to look for                                         |
| ---------------------- | -------------------------------------------------------- |
| Correct SAP colors     | Blue `#0070F2` for SAP, Grey `#475E75` for non-SAP       |
| Area nesting           | Alternating blue/white fill                              |
| Overlapping shapes     | ≥20px gap between all siblings                           |
| Clipped labels         | Text cut off → increase shape dimensions                 |
| Missing connections    | Disconnected arrows → verify source/target ids           |
| Line style             | Solid=sync, Dashed=async                                 |
| Unrequested components | Products not in the allowlist → remove                   |
| Wrong service order    | Edge order differs from requested sequence → fix         |
| Title collision        | Icon/label touches area title → move below reserved band |
| Raw HTML text          | `<font>` markup visible → fix escaping                   |

Also run: `python3 scripts/validate_diagram.py diagram.drawio --strict-palette`

Max 2 self-check rounds.

### Step 3 — Review loop

Show the preview to the user. Apply targeted XML edits per feedback. Loop until approved. **Safety valve:** after 5 rounds, suggest opening `.drawio` in draw.io desktop for manual fine-tuning.

### Step 4 — Final export (with `-e` for embedded diagram)

```bash
# PNG with embedded diagram XML (editable in draw.io)
drawio -x -f png -e -s 2 -o diagram.drawio.png diagram.drawio

# SVG with embedded diagram
drawio -x -f svg -e -o diagram.drawio.svg diagram.drawio

# PDF
drawio -x -f pdf -o diagram.pdf diagram.drawio
```

Key flags: `-x` export mode · `-f` format · `-e` embed diagram XML · `-s` scale (2 recommended for PNG) · `-o` output path · `-b 10` border.

### Known issue: truncated IEND in `-e` PNGs

draw.io CLI emits `-e` PNGs with an 8-byte truncation at IEND, causing some viewers/APIs to reject the file. Export SVG/PDF is unaffected. If the final PNG won't open, re-export without `-e` for the user-facing image.

### Fallback chain

| Scenario                              | Behavior                                                               |
| ------------------------------------- | ---------------------------------------------------------------------- |
| draw.io CLI missing, Python available | Generate `.drawio` + print a `https://app.diagrams.net/?…` browser URL |
| draw.io CLI missing, Python missing   | Generate `.drawio` XML only; instruct user to open manually            |
| CLI unavailable in sandbox (macOS)    | Use browser fallback; ask user to export in non-sandboxed terminal     |
| Vision unavailable for self-check     | Skip visual verification; proceed to showing user the file             |
| Linux headless export fails           | Try `xvfb-run -a drawio …`; add `--disable-gpu` if EGL errors          |

### WSL2 specifics

```bash
# CLI path on WSL2
"/mnt/c/Program Files/draw.io/draw.io.exe" --version

# Open exported file (convert path first)
cmd.exe /c start "" "$(wslpath -w diagram.drawio.png)"
```

## Common mistakes

| Mistake                                                | Fix                                                                                                                      |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| Missing `id="0"` / `id="1"` root cells                 | Always include both at top of `<root>`                                                                                   |
| Self-closing edge `mxCell` (`<mxCell ... edge="1" />`) | Use expanded form with `<mxGeometry relative="1" as="geometry" />` child                                                 |
| `--` inside XML comments                               | Illegal per XML spec — rephrase                                                                                          |
| `shape=mxgraph.sap.*` style                            | Does not exist; use `shape=image;image=data:image/svg+xml,...` from icon-index.json                                      |
| Literal `\n` in label                                  | Use `&#xa;` for line breaks in `value` attributes                                                                        |
| HTML label double-escaping                             | Build HTML string first, then one full escape pass (`&amp;`, `&lt;`, `&gt;`, `&quot;`) before inserting into `value="…"` |
| Raw `<font>` markup visible in diagram                 | Verify with XML parser after generating; use `xml.etree.ElementTree.fromstring()`                                        |
| Blurry icons                                           | Patch SVG `width`/`height` to cell size before encoding; run `upscale_svg_icons.py`                                      |
| Edges crossing through unrelated containers            | Reposition containers or add waypoints                                                                                   |
| All connectors exit same point                         | Distribute exit/entry across perimeter (`exitX=0.25`, `0.5`, `0.75`)                                                     |
| Auto-routing creates doglegs                           | Pin explicit waypoints; align centers for straight lines                                                                 |
| `strokeWidth=3` on data flow                           | Reserve thick grey for firewalls/network barriers only                                                                   |
| `command not found: draw.io` (macOS)                   | Homebrew installs as `drawio` (no dot)                                                                                   |
| Vision "dimensions exceed 2576×2576px"                 | Re-export with `--width 2000` instead of `-s 2`                                                                          |
