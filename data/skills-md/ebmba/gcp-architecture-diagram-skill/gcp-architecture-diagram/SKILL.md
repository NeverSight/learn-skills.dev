---
name: gcp-architecture-diagram
description: Always use when the user asks to create, generate, or build a Google Cloud (GCP) architecture diagram, cloud infrastructure diagram, or system diagram with Google Cloud services. Also activates for draw.io diagrams mentioning GCP services like Cloud Run, GKE, BigQuery, Pub/Sub, Cloud SQL, Cloud Storage, Dataflow, Vertex AI, etc.
---

# Google Cloud Architecture Diagram Skill

Generate Google Cloud architecture diagrams as native `.drawio` files using the **official Google Cloud
product icons** (https://cloud.google.com/icons), embedded in the file so it opens anywhere. Optionally
export to PNG, SVG or PDF with the diagram XML embedded (exports stay editable in draw.io).

`SCRIPT` = `python3 <this skill's directory>/scripts/gcp_drawio.py`. Use the absolute path: diagrams can be
written anywhere. Other paths below are relative to the skill's directory.

## Workflow

1. **Icons available?** Run `SCRIPT fetch` once (idempotent; downloads Google's icon packs to
   `~/.cache/gcp-architecture-diagram/icons`). The icons are not bundled in the skill.
2. **Clarify** only what you cannot infer: audience (technical vs. executive) and icon mode (see below).
   Default: technical, `modern`.
3. **Pick icon keys** in `references/icons.md` (or `SCRIPT list <query>`). Never invent a key.
4. **Write the source `diagram.src.drawio`** with placeholder styles (`gcpIcon=`, `gcpGroup=`,
   `gcpShape=`), following the layout rules below. Compute every coordinate; don't eyeball.
5. **Build:** `SCRIPT build diagram.src.drawio [--mode legacy]` writes `diagram.drawio` (icons embedded)
   and validates the layout. Fix every `ERROR` and every `WARN` **in the `.src.drawio` file**, then
   rebuild. Never hand-edit the built file: its styles are expanded and merged, so text edits written
   against the source silently miss. (Building a file without `.src` rebuilds it in place, for diagrams
   later edited in draw.io.)
6. **Export** if asked: `SCRIPT export diagram.drawio -f png` (also `svg`, `pdf`). Then **look at the PNG**
   (Read it) and fix anything the validator can't see: cramped labels, unbalanced composition. Export
   needs draw.io desktop (the script finds it in standard locations, or `DRAWIO_BIN`). If it is missing,
   deliver the `.drawio` and tell the user to install it (`brew install --cask drawio` on macOS).
7. **Companion guide:** write `diagram.md` next to it (title, numbered flow, services and their role,
   key design decisions).
8. Open the result (`open` on macOS, `xdg-open` on Linux) or print the path.

## Icon mode

Since 2025 Google uses ~45 icons instead of 250+:
- **19 core products** have a unique 4-color icon (Cloud Run, GKE, BigQuery, Cloud SQL, Spanner, AlloyDB,
  Cloud Storage, Compute Engine, Vertex AI, Apigee, Looker, Anthos…).
- **Every other product uses its category icon** (Pub/Sub, Dataflow and Dataproc all show *Data Analytics*;
  Load Balancing, Cloud Armor and NAT all show *Networking*). **The label carries the product name**, so
  every icon must be labeled.

Modes:
- `modern` (default): Google's current rules, described above. Use unless the user asks otherwise.
- `legacy` (`--mode legacy`): one distinct icon per product, from Google's pre-2025 console set.
  More distinguishable, but Google says these "should not be used as of 2026". Use when the user asks for
  distinct per-product icons or "old"/"classic" GCP icons, and mention the caveat once.
- Per cell override: add `gcpIconMode=legacy` to a single cell's style.
- **Networking-heavy technical diagrams** (hybrid connectivity, hub-and-spoke, security perimeters) end up
  with many identical *Networking* icons in `modern` mode (Load Balancing, Armor, Router, Interconnect,
  VPN, NAT). Offer `legacy` mode in that case when the user hasn't chosen. If you can't ask, keep `modern`
  and say in your reply that `--mode legacy` would make those icons distinct.

## Placeholder styles

The script turns these into full styles. Extra style keys you add (e.g. `fontStyle=1`) are kept.

```xml
<!-- Google Cloud product: 64x64 -->
<mxCell id="run" value="Cloud Run&lt;br&gt;orders-api" style="gcpIcon=cloud_run;" vertex="1" parent="subnet">
  <mxGeometry x="60" y="50" width="64" height="64" as="geometry"/>
</mxCell>

<!-- Actor or non-GCP system: 48x48 -->
<mxCell id="user" value="Customer" style="gcpShape=user;" vertex="1" parent="1">
  <mxGeometry x="80" y="300" width="48" height="48" as="geometry"/>
</mxCell>

<!-- Boundary -->
<mxCell id="project" value="Project: shop-prod" style="gcpGroup=project;" vertex="1" parent="gcp">
  <mxGeometry x="20" y="40" width="1200" height="600" as="geometry"/>
</mxCell>
```

Keys: `references/icons.md`. `gcpIcon` also accepts aliases (`gcs`, `bq`, `pubsub`, `lb`…) and
`category:<name>` to show a category itself. `gcpShape`: `user`, `users`, `browser` (= `laptop`), `mobile`, `server`,
`database`, `internet`, `datacenter`, `external_api`, `other_cloud`, `storage`.

## Boundaries (groups)

Google Cloud's resource model differs from AWS. **Read `references/gcp-hierarchy.md` before drawing any
network or project boundary.** In short:
- Nesting: `google_cloud` → (`organization` → `folder` →) `project` → `vpc` → `region` → `subnet` → `zone`.
- **A VPC is global; subnets are regional.** Draw the VPC around regions, never inside one. Zones only
  matter for zonal resources (VMs, GKE zonal clusters, Filestore); omit them otherwise.
- Serverless and managed services (Cloud Run, Pub/Sub, BigQuery, Cloud Storage…) are **not in a VPC**.
  Put them in the project (optionally in a `region` box), outside the VPC. Show Serverless VPC Access /
  Private Service Connect edges when they reach into the VPC.
- Other kinds: `vpc_sc` (VPC Service Controls perimeter), `cluster` (GKE cluster), `instance_group`,
  `logical` (any functional grouping), `on_premises`, `other_cloud`, `internet`.
- Draw only the boundaries the diagram needs. The `logical` box around an ops lane is optional; drop it
  when vertical space is tight. Single-region diagrams may skip the `region` box (put the region in the
  subnet label).

Container mechanics (critical):
- A group's children set `parent="<group id>"`, and **their coordinates are relative to the group**.
- Leave **40px** at the top of every group for its label and **30px** padding on the other sides.
- Edges between cells in different groups: `parent="1"`.

## Layout rules

- **Left to right**: users and clients on the LEFT, data stores and external systems on the RIGHT.
- Icons 64x64, generic shapes 48x48. Steps are measured **between centers** (works for mixed sizes).
  **Minimum horizontal step: 200px** (room for edge labels). **Minimum vertical step between lanes:
  180px** (icon + 2-line label + gap).
- **Add 30px to a step, horizontal or vertical, for every group border crossed between the two icons**
  (e.g. Cloud Run outside the VPC → Cloud SQL inside VPC + subnet: 2 borders → 260px). Add the height of
  a group title (40px) when a lane starts right under one. Lay out the deepest nesting first, then
  derive group sizes from their content.
- **Size groups including labels.** Estimate ~7px per character at 12px and 16px per line; a 2-line
  label under a 64px icon needs ~100px of height in total. The validator warns when a label sticks out
  of its group.
- Within a flow, use the same step for the same situation. Mixed gaps read as sloppy.
- Secondary services (monitoring, logging, secrets, CI/CD) go in a lane **below** the main flow, or in a
  side `logical` group, not interleaved with the request path.
- Align nodes connected horizontally on the **same center y**; vertically, on the **same center x**:
  `child.x = parent.x + parent.width/2 - child.width/2`. This is what makes edges straight.
- Size each group to its content plus padding, and the canvas to all content plus a 40px margin.
- Title block top-left, outside any group:
```xml
<mxCell id="title" value="&lt;b&gt;Diagram title&lt;/b&gt;&lt;br&gt;Author | Date | Version" style="text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;fontSize=14;spacing=8;fontFamily=Google Sans,Roboto,Arial,sans-serif;" vertex="1" parent="1">
  <mxGeometry x="40" y="20" width="460" height="60" as="geometry"/>
</mxCell>
```
- Labels: product name on line 1, the resource's role or name on line 2 (`Cloud SQL<br>orders-db`). In
  `modern` mode never leave a category-icon node unlabeled. Labels don't wrap: break lines with `<br>`.
- **Labels sit below icons, so an edge leaving or entering an icon's bottom crosses its label.** Move that
  label to a free side or corner. The validator flags every edge that crosses a label.

  | Position | Style to add |
  |---|---|
  | top | `verticalLabelPosition=top;verticalAlign=bottom;` |
  | right | `labelPosition=right;verticalLabelPosition=middle;align=left;verticalAlign=middle;` |
  | left | `labelPosition=left;verticalLabelPosition=middle;align=right;verticalAlign=middle;` |
  | top-right | `labelPosition=right;verticalLabelPosition=top;align=left;verticalAlign=bottom;` |
  | top-left | `labelPosition=left;verticalLabelPosition=top;align=right;verticalAlign=bottom;` |
  | bottom-right | `labelPosition=right;align=left;` |
  | bottom-left | `labelPosition=left;align=right;` |

  A node with edges on all four sides (a hub) gets a corner label. Check that it clears the title of
  the group it sits in.

## Edges

Base style:
```
edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1.5;strokeColor=#5F6368;endArrow=block;endFill=1;fontSize=11;fontColor=#3C4043;labelBackgroundColor=#FFFFFF;
```
- **Always** set `source` and `target` (never a floating edge), and set `exitX/exitY` and `entryX/entryY`:
  right→left for the main flow (`exitX=1;exitY=0.5;entryX=0;entryY=0.5`), bottom→top for lanes below
  (`exitX=0.5;exitY=1;entryX=0.5;entryY=0`). Always include `exitDx=0;exitDy=0;entryDx=0;entryDy=0;`.
- Types: solid = synchronous request/data path; `dashed=1;` = asynchronous / event / optional;
  `dashed=1;strokeColor=#EA4335;` = error or dead-letter path; `strokeColor=#34A853;` may mark replication;
  `dashed=1;endArrow=none;` = association / control plane (e.g. Cloud Router ↔ Interconnect `BGP`).
- Labels: 1–3 words (`HTTPS`, `gRPC`, `publish`, `CDC`). Omit when obvious. No `value` attribute when unlabeled.
- **An edge label is drawn at the middle of the route and must not sit on a group border** (validator
  checks it). Move it along the edge with the edge geometry's `x`, from -1 (source) to 1 (target):
  `<mxGeometry x="-0.6" relative="1" as="geometry"/>` puts it at 20% from the source.
- An edge may start or end on a **group** (e.g. "all workloads in the cluster → Cloud Logging"). To keep it
  straight, set `exitX = (target_center_x - group_x) / group_width` (same idea for `exitY`).
- **At most one bend per edge.** If an edge needs more, move a node; don't add waypoints.
- **Several edges on the same side of an icon** (a hub): spread them with `exitX` (top/bottom side) or
  `exitY` (left/right side) at 0.25 / 0.5 / 0.75, **ordered like their targets** (leftmost target →
  leftmost exit) so they don't cross. Same for two edges sharing a corridor between two lanes.

## Audience

- **Technical**: product names, protocols, ports, CIDR ranges, machine types, regions.
- **Executive / non-technical**: action labels ("Store orders", "Notify customer"), hide network detail
  (no subnets or zones), numbered flow with edge labels `①②③…` (second flow `❶❷❸…`), styled
  `fontSize=13;fontStyle=1;labelBackgroundColor=#FFFFFF;`.

## Self-check before delivering

The build step catches structure and geometry issues. It does **not** check spacing minima, label-to-label
proximity or balance. Check those in the exported image:
1. Every edge is straight or has one clean bend, and none crosses an icon or another edge's path.
2. No label touches an icon, an edge or a group border.
3. Boundaries are correct for GCP (global VPC, regional subnets, serverless outside the VPC).
4. The composition is balanced: no dense half and empty half.

## References

- `references/icons.md`: every icon key, alias, category and group kind (generated, authoritative)
- `references/gcp-hierarchy.md`: resource hierarchy and network boundaries, with placement rules
- `examples/`: worked source diagrams (`*.src.drawio`) with their guide (`*.md`), to copy patterns from:
  `web-app` (Cloud Run, private-IP data services, events, ops lane), `gke-hybrid` (GKE workloads,
  Cloud Armor, Interconnect + Cloud Router, hub node with corner labels, edge from a group) and
  `hub-and-spoke` (multi-project NCC hub, VPC and hybrid spokes, VPC-SC perimeter, PSC, legacy mode)
