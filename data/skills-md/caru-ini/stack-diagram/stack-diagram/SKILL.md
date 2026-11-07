---
name: stack-diagram
description: "Create cloud-architecture-style diagrams of tech stacks, system architectures, infra layouts, and service topologies — with real brand logos, grouped containers, and clean orthogonal arrows — delivered as self-contained HTML, a PNG image, a React/TSX component, or a live artifact. Use this skill whenever the user asks for an architecture / system / stack / infra diagram, a tech-stack overview, a service topology, a cloud-vendor-style diagram, or wants tech logos arranged into a picture of how their services connect — in any language, even if they don't name an output format, and even if the tools involved aren't cloud services."
license: MIT (see LICENSE); bundled fonts are SIL OFL 1.1
compatibility: Python 3.9+ and network access to fetch logos; PNG output also needs Playwright with Chromium
---

# stack-diagram

Produces engineering-drawing-style architecture diagrams: real logos on white tiles, labeled group boxes (like cloud-vendor VPC diagrams), orthogonal arrows with monospace labels, on a cool graph-paper background. One self-contained HTML file is the source of truth; PNG / TSX / artifact are derived from it.

## Requirements

- Python 3.9+ (standard library only for `fetch_icons.py`, `build.py` and `share.py`)
- Network access to the icon sources (svgl.app, raw.githubusercontent.com, cdn.jsdelivr.net, aws.amazon.com and d1.awsstatic.com for AWS icons, plus the brand's own site or repo for `name=URL`) when fetching icons
- Playwright + Chromium for `render_png.py`: `pip install playwright && python3 -m playwright install --with-deps chromium`

## Workflow

1. Settle the content (nodes, groups, edges)
2. Fetch icons — `scripts/fetch_icons.py`
3. Plan coordinates — read `references/geometry.md`
4. Build the HTML from `assets/template.html` — `scripts/build.py`
5. **Render a PNG and look at it** before delivering
6. Deliver in the requested format(s)
7. Optionally share it to the public gallery

## Step 1 — Content

From the user's list of technologies/services, decide:

- **Nodes**: each tech = one node (name + a short lowercase role like `http server`, `sqlite db`)
- **Groups**: draw a box around things that share a runtime, vendor, or repo (e.g. a cloud provider box containing a runtime box; a monorepo box for tooling). Nesting one level deep is fine; deeper gets noisy. Write group labels in the brand's own casing (`GitHub`, `npm`); the template shows them as written.
- **Edges**, three kinds:
  - accent-colored solid = the primary request/data flow (one continuous path reads best)
  - neutral solid = secondary internal connections
  - neutral dashed = dev-time / deploy-time relationships (CI, git hooks, IaC deploy)

If the user gave only a flat list of tools, infer sensible groups and flows from what the tools are — only ask when a tool is ambiguous enough that the diagram would be wrong either way.

## Step 2 — Icons

```bash
python3 scripts/fetch_icons.py <icons-dir> tanstack hono drizzle "betterauth:better-auth" "orpc=https://orpc.unnoq.com/logo.webp"
python3 scripts/fetch_icons.py <icons-dir> "aws:aws/AWS-Cloud-logo" "vpc:aws/vpc" "fargate:aws/fargate" "s3:aws/s3"
```

Spec forms: `name` (name used as slug), `name:slug` (different slug), `name=URL` (explicit URL), `name:aws/<Name>` (official AWS icon). The script tries, in order: **svgl → devicon → gilbarbara/logos**, writes files plus `manifest.json`, and flags icons whose fill is white. svgl (svgl.app) is first because it carries current official marks for modern dev brands (TanStack, Better Auth, Hono...). When a logo has light/dark versions, the light one becomes `<name>` (tiles are white in both themes) and the dark one is saved as `<name>_dark` for group labels. svgl is matched by exact title only, so a miss just falls through. Its API also exposes `wordmark` variants — occasionally useful for a wide group-label, never for tiles.

Rules that matter more than the mechanics:

- **Never recolor a logo.** Users notice. If a logo is white or too light for a white tile, put it on a dark tile (`tile dark` class) instead of touching its fill. The manifest's `white_fill` flag is a heuristic — a white fill can be an inner detail on a colored mark (tRPC, Ubuntu), so glance at the SVG before reaching for the dark tile.
- **Official marks only.** simple-icons is deliberately not a source: its glyphs are monochrome redraws, and users call them wrong on sight. When every source misses (`FAIL`), find the official file and pass it as `name=URL` — look in the project's repo (root `logo*.svg`, `docs/`, `assets/`, `public/`) and on its site (`/logo.svg`, `/favicon.svg`, `/images/logo.svg`). Some marks live only in the repo (Lefthook's is `logo_sign.svg` at the root of `evilmartians/lefthook`).
- **Abstract concepts get pictograms, not text.** A node like "dev environment", "cron", "queue", "cache", or "webhook receiver" has no brand — reach for a Lucide line icon via `name:lucide/<icon>` (e.g. `devenv:lucide/terminal`, `cron:lucide/clock`; browse lucide.dev/icons). No text-in-a-tile, no emoji.
- **Vendor sub-products** (Cloudflare D1/R2/KV...) usually have no distinct logo: just reuse the vendor logo on the tile and let the node name carry the distinction ("Cloudflare D1" / "sqlite db").
- **AWS uses AWS's own icons.** Each service has one: fetch it with `name:aws/<Name>`, read from AWS's official icon package at run time (e.g. `lambda:aws/lambda`, `aws:aws/AWS-Cloud-logo`, `s3:aws/s3`). The `AWS-` / `Amazon-` prefix is optional, common acronyms work (`s3`, `sqs`, `sns`, `ses`, `ecs`, `eks`, `ecr`, `elb`, `alb`, `nlb`, `iam`, `kms`, `msk`, `vpc`), and a miss prints every name. The slugs `aws`, `amazonwebservices` and `aws-*` go to the same package, and what it doesn't carry `FAIL`s instead of falling back to a third-party copy. Always write the `aws/` prefix for a service: a bare `dynamodb` still goes through the third-party chain. Keep the package and loose icon files out of repos: AWS allows the icons in diagrams, and redistribution is unconfirmed.
- **AWS diagrams follow AWS's own drawing rules.** Service icons carry their own square and work on light and dark grounds, so use `tile bare`: a white tile only doubles the frame. People and generic nodes use AWS's general icons (`user:aws/General-User`; also `General-Users`, `General-Client`, `General-Internet`, `General-Server`) in `tile bare res` with the template's `lt`/`dk` pair. Groups use the template's `group aws` for AWS Cloud (with `aws:aws/AWS-Cloud-logo` in the label), plus `region`, `az`, `vpc`, `private` or `public` for the rest: square corners, outline only, label in ink, no vendor tint, and a 30px icon flush in the corner instead of the 14px one. Inside a VPC, show public and private subnets when you know or can safely infer the split (an internet-facing load balancer in public; app servers and databases in private): a flat VPC is the first thing AWS people notice. Edges use one color and an open arrowhead: `<path class="aws" ... marker-end="url(#open)"/>`, `aws dash` for dev/deploy, plain `.el` labels, and no legend. Name nodes `Amazon S3` / `AWS Fargate`, not a bare `S3` / `Fargate`; a short form like `ALB` goes in the role line, under the full name (`Elastic Load Balancing`). Names may take two lines, but `Amazon` / `AWS` must stay on the first word's line: if it would wrap right after the prefix, widen that node (`left:<centerX-76>px; width:152px`).
- **Non-brand nodes** (user, browser, internet, devices, bare-metal server): copy a glyph from `assets/generic/` into the icons dir under the node's name, or use `name:lucide/<icon>` — don't use emoji. These aren't brand logos, so tinting them to the diagram's ink color is fine (the fetch script does it for Lucide automatically).
- **Group-label icons render at 14px** — they need a square glyph mark. Wordmarks and wide lockups turn to mud at that size; if the main icon is a wordmark, fetch the brand's square icon separately for the label (svgl usually has it; otherwise the project's own icon or favicon file).
- **Group labels sit on the group's tint, not on a white tile**, so in the dark theme a mark with black parts vanishes there. If `fetch_icons.py` saved `<name>_dark`, use the template's `lt`/`dk` pair in the label; if there is no dark variant and the mark has black parts, add class `plate` to the label's `<img>` (white backing, dark theme only).
- Raster logos (png/webp) are fine; the build script embeds everything as data URIs, so nothing is loaded at view time.

## Step 3 — Layout

Read `references/geometry.md` for the coordinate system, spacing constants, and — most importantly — the **edge anchoring rules that prevent arrows from running through label text**. The one-line version: a node is its tile *plus* the text under it; vertical arrows connect node-box boundaries, never tile-to-tile through text.

## Step 4 — Build

Copy `assets/template.html`, replace the sample GROUPS / EDGES / NODES / header sections with yours (the template's markup doubles as format documentation), then inline the assets. Set `lang` on `<html>` to the language of the diagram's labels (`en` by default; use `ja` for Japanese so browsers pick Japanese glyph variants). Two options the template already carries: a **dark variant** (set `data-theme="dark"` on `<html>`; tiles stay white so logos survive, group-label icons follow the Step 2 rule, and arrowheads and legend swatches follow the tokens automatically), and a "deploy to platform X" edge where X is a group, not a node — point the arrow at the most representative node *inside* the group and label the edge (`deploy`), which reads correctly.

```bash
python3 scripts/build.py my-diagram.html <icons-dir> out.html --fonts <skill>/assets/fonts
```

Icons are referenced in markup as `%%ICON_<name>%%`; fonts as `%%FONT_DISPLAY%%` (Geist) / `%%FONT_JBM%%` (JetBrains Mono). The build fails loudly on unresolved tokens. Keep every color and font behind the CSS custom properties already in the template — tweak the tokens, not scattered values.

## Step 5 — Verify by looking

Render and actually read the image:

```bash
python3 scripts/render_png.py out.html check.png --selector .canvas --scale 2
```

If the diagram contains Japanese text, the render host needs a Japanese font, or CJK characters silently come out in Chinese glyph variants (users notice immediately). The script warns and prints a fix; the template's font stack already names the Noto JP faces.

Checklist while looking at it:
- No arrow crosses label text; no arrowhead lands inside text
- Edge labels readable (they have a paper-colored halo — confirm it's working)
- Every icon visible (white-on-white is the classic failure → dark tile), including group-label icons in the dark render
- Group labels sit in their group's top-left corner, clear of nodes and edges; each group's left and right padding match
- Nothing sticks out of its group box; nothing clipped at canvas edge

Fix and re-render until clean. This loop is cheap; shipping a diagram with overlapping text is not.

## Step 6 — Deliver

- **HTML** (default): the built file itself. Self-contained, works offline.
- **PNG**: always produced by screenshotting the built HTML with headless Chromium (`render_png.py`, `--scale 2` for crisp text) — never by drawing a separate image with matplotlib/PIL/standalone SVG rasterizers; the HTML is the single source of truth and the browser's text/SVG rendering is what makes it look right. By default the script emits BOTH themes (`out.png` light + `out-dark.png`) with square corners (radius is stripped for the screenshot only) — deliver both unless the user asked for one; `--single` captures the document as-authored. Target `.canvas` for just the diagram, `--full-page` for the whole page.
- **TSX**: convert per `references/tsx.md` (self-contained React component, no deps).
- **Artifact** (where the environment offers an artifact or page-publishing tool): publish the built HTML with the environment's artifact tool. Everything is already inlined as data URIs, so the artifact's blocked-network sandbox is a non-issue. Prefer this when the user will iterate on the diagram in conversation; pair it with a PNG when they need something to paste elsewhere.

If several formats are requested, build the HTML once and derive the rest from it.

In the footer, credit the icon sources actually used — the `source` field of each entry in the icons dir's `manifest.json` (e.g. `icons: svgl / devicon / Lucide`; source `aws` reads `AWS Architecture Icons`). Brand logos remain the trademarks of their owners. Keep the template's "made with stack-diagram" link after the credits unless the user asks to remove it; a default PNG captures only the canvas, so the link stays out of it.

## Step 7 — Share to the gallery (optional)

Offer this only where you can run shell commands with network access; otherwise skip the step. After delivering, add one line in the user's language offering to share it, with the gallery link so they can look first. For example: "If you'd like to share this diagram, I can post it to the public gallery: https://stacks.caru.moe". Say it once per conversation and never raise it again; never submit without the user's explicit yes.

On a yes, ask for a display name (don't fill it in from `gh` or git) and whether to add a GitHub login. The login is optional and never shown publicly; it only lets them delete the post later by signing in to the gallery with that account. If `gh` is signed in, offer the result of `gh api user -q .login`; include it only if they agree.

Then show exactly what will be sent before sending anything:

- the light and dark PNGs — the `.canvas` pair `render_png.py` writes (`out.png` / `out-dark.png`) — with their paths and every label in them
- a title, in plain English even when the conversation isn't. It describes the diagram, not the request. The diagram's own labels stay as they are.
- the stack: the technologies in the diagram, by their official names
- the display name
- the GitHub login, if any, marked as not public

Point out anything that looks internal — hostnames, IPs, customer or company names, internal service names — and suggest re-rendering without it first. Ask them to confirm it is their own system or one they may show publicly, and send only after a second explicit yes on that exact content.

```bash
python3 scripts/share.py submit out.png out-dark.png --title "..." --stack "..." --name "..." [--github LOGIN] [--icons DIR]
```

`--stack` lists the technologies, comma-separated, by their official names. Write `Name=key` to show a technology's logo beside it in the gallery: `key` is its entry in the icons dir's `manifest.json`, and `--icons` takes that dir (`<icons-dir>` from Step 2). A name without `=` goes without a logo, for example `--stack "Next.js=nextjs,Hono=hono,Neon" --icons <icons-dir>`. The gallery shows only logos from svgl, gilbarbara/logos and devicon; AWS, Lucide and logos from a brand's own site or repo go without one.

If `share.py` rejects a PNG as too large, re-render with a lower `--scale` and show the new pair before sending.

Tell the user the URL, that a held post appears only after a manual review, and the path where `share.py` says it saved the delete key. To delete later: `python3 scripts/share.py delete <id>` (`list` shows saved posts). If the gallery could confirm the GitHub login they gave, signing in with that account on the gallery deletes it too.
