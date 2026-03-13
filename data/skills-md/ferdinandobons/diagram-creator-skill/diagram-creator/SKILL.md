---
name: diagram-creator
description: Generate beautiful, production-ready architecture diagrams as self-contained HTML files from any input. Use this skill whenever the user wants to create a diagram, schema, flowchart, network diagram, system visualization, timeline, org chart, or any visual representation of concepts — technical or non-technical. Trigger when the user mentions "diagram", "schema", "architecture", "flow", "topology", "pipeline", "timeline", "visualize", "graph", or asks to turn a file into a visual diagram. Accepts ANY file type as input (.md, .txt, .json, .yaml, .csv, .pdf, .py, .ts, .toml, .env, .tf, .dockerfile, etc.) — Claude auto-detects the format and extracts relevant structure to diagram. Even a simple sentence like "diagram of how OAuth works" or "visualize this file" triggers this skill.
metadata:
  version: 1.0.0
---

# Diagram Creator

Generate stunning, self-contained HTML diagrams with professional typography, smooth animations, and an infinite canvas you can pan and zoom like Miro. Output is always a single `.html` file that opens directly in any browser — zero dependencies. Supports 5 themes and 8 topology layouts.

## Input Handling

Accept any of these inputs and auto-process them:

| Input type | How to handle |
|---|---|
| **Topic/description** | "Docker networking", "OAuth 2.0 flow" — use directly |
| **Markdown** (.md, .mdx) | Extract structure from headings, lists, tables, relationships |
| **JSON / YAML** (.json, .yaml, .yml, .jsonl) | Parse structure — keys become nodes, nesting becomes layers |
| **Code files** (.py, .ts, .js, .go, .rs, .java, .rb, .php, .swift, .kt, .c, .cpp, .cs, .scala, etc.) | Extract classes, functions, imports, inheritance — diagram the architecture |
| **Config / Infra** (.toml, .ini, .env, .tf, .hcl, Dockerfile, docker-compose.yml, Makefile, nginx.conf) | Map services, variables, dependencies, infrastructure |
| **API specs** (.openapi.yaml, .swagger.json, .graphql, .proto) | Extract endpoints, types, service relationships |
| **Database schemas** (.sql, .prisma, .dbml) | Map tables, columns, foreign keys, relationships |
| **CI/CD pipelines** (.github/workflows/*.yml, .gitlab-ci.yml, Jenkinsfile) | Visualize pipeline stages and deployment flows |
| **Data files** (.csv, .tsv) | Identify columns as entities, rows as relationships |
| **Microsoft Office** (.xlsx, .xls, .docx, .doc, .pptx, .ppt) | Extract tables, headings, slide structure, org charts, SmartArt |
| **Package manifests** (package.json, requirements.txt, Cargo.toml, go.mod, pom.xml) | Map dependency trees |
| **Existing diagrams** (.drawio, .puml, .mermaid) | Read spec and re-render with this design system |
| **PDF / Docs** (.pdf, .txt, .rst, .adoc) | Read content, extract core structure |
| **Notebooks** (.ipynb) | Extract code cells, data flow, library dependencies |

**If it's a file, this skill can diagram it.** For formats not listed, read the content and extract whatever structure exists.

When receiving a file path, read the file, detect the extension, and intelligently extract what matters for the diagram. Don't ask the user to reformat — figure it out.

If the input is genuinely ambiguous (no clear structure to extract), ask clarifying questions before proceeding. See "Pre-generation Questions" below.

## Pre-generation Questions

Always ask these questions before generating, unless the answer is completely obvious from the input. **Ask one question at a time** — wait for the user's answer before moving to the next. Present every question as a **numbered list** so the user can simply reply with a number.

Skip a question ONLY when the answer is unambiguous — e.g., "diagram of Docker bridge networking" makes topology (nested) and detail level (medium) obvious. When in doubt, ask.

**Question flow (one at a time, in this order):**

1. **What to visualize?** (skip only if input is already specific)
   Present 2-3 interpretations of the input as numbered options, plus an "Other" option. Tailor the options to what the user actually asked — don't use generic placeholders.
   ```
   What do you want to visualize?
     1) [interpretation A]
     2) [interpretation B]
     3) Other — describe below
   → Reply with the number:
   ```

2. **Layout?** (skip if only one topology realistically fits — choose automatically in Step 0)
   Only list the 2-3 topologies that could realistically fit, not all 8. Adapt options based on the previous answer.
   ```
   Layout?
     1) Left-to-right — sequential flow
     2) Timeline — vertical step sequence
   → Reply with the number:
   ```

3. **Detail level?**
   ```
   Detail level?
     1) High-level — main entities only, understand in 5 seconds
     2) Medium — entities with key info, labeled connections (default)
     3) Detailed — full technical breakdown, all metadata
   → Reply with the number (default: 2):
   ```

4. **Theme?**
   ```
   Theme?
     1) Dark (default)
     2) Light
     3) Corporate
     4) Neon
     5) Minimal
   → Reply with the number (default: 1):
   ```

Once you have all the answers, proceed autonomously through all remaining steps without further questions.

## Step 0 — Choose the Topology

Pick exactly one topology based on what fits the content best:

| Topology | When to use | Examples |
|---|---|---|
| `nested` | Hierarchical containment, layers wrapping layers | Docker networking, K8s pods, OSI model, VPC subnets |
| `left-to-right` | Sequential flow from A to Z | OAuth flow, CI/CD pipeline, user journey, request lifecycle |
| `hub-and-spoke` | Central node connected to N surrounding nodes | API gateway, microservices, load balancer, team structure |
| `timeline` | Ordered vertical sequence of events/steps | Deploy pipeline, project roadmap, historical events |
| `grid` | Matrix/table comparison, feature grids | Feature comparison, skill map, competitive landscape |
| `tree` | Hierarchical branching, org charts | Org chart, file tree, decision tree, taxonomy |
| `funnel` | Progressive narrowing, conversion stages | Sales funnel, data pipeline, filtering process |
| `comparison` | Side-by-side 2-3 options | Product vs product, technology choices, before/after |

## Step 1 — Plan the Content

Before writing HTML, plan these elements in your thinking:

- **Topic**: one sentence describing what the diagram shows
- **Detail level**: choose one of three levels. Default to **medium** unless context suggests otherwise:
  - **High-level** — Only the main entities of the system. Aggregate similar entities into single boxes (e.g., "Backend Services" instead of listing 10 microservices). No metadata in boxes — just name and role. Minimal connection labels. No callouts, badges, or notes. The viewer should understand the structure in 5 seconds.
  - **Medium** (default) — The entities needed to understand how the system works, without sub-components. Each box gets 1-2 metadata relevant to the domain (infra: port and protocol; org chart: role and team; flow: input/output of each step). Label connections where it adds clarity. Callouts only for non-obvious key concepts. The viewer who knows the domain should understand the diagram without further explanation.
  - **Detailed** — Everything: sub-components, configurations, technical notes. All relevant metadata per box (ports, protocols, versions, env vars, states). Badges, explanatory callouts, side notes. Goal: complete technical reference for people working on the system.
  How to choose: (1) If the user specifies a level explicitly, use it. (2) If context clarifies intent — a presentation implies high-level, a technical doc for the team implies detailed — match it. (3) Otherwise default to medium. (4) If the chosen level produces too many elements for the topology, aggregate entities into groups rather than changing level or topology.
- **Layers/Steps**: each level with name, description, and accent color. For left-to-right topology, count the steps and apply the step count scaling table from `references/topology-layouts.md` to set step max-width and arrow width accordingly
- **Nodes**: each box with emoji, name, and metadata density matching the detail level above
- **Connections**: what each arrow represents (label density matches detail level)
- **Special Components**: callout boxes, badges, info panels (reduce or skip for high-level)
- **Legend Entries**: one per accent color used

## Step 1.5 — Choose the Theme

If the user specifies a theme, use it. Otherwise default to **dark**.

| Theme | Best for | Keywords |
|---|---|---|
| `dark` (default) | Technical diagrams, dev docs | "dark", default |
| `light` | Presentations, documentation sites | "light", "chiaro", "presentation" |
| `corporate` | Business plans, pitch decks | "corporate", "business", "professional" |
| `neon` | Creative, gaming, social media | "neon", "cyberpunk", "vibrant" |
| `minimal` | Clean docs, technical specs | "minimal", "clean", "simple" |

See `references/themes.md` for the exact `:root` values and overrides per theme.

## Step 2 — Build the HTML

Read the reference files for detailed CSS/layout specifications:

- `references/typography-and-colors.md` — fonts, palette, background
- `references/themes.md` — theme system with 5 color schemes
- `references/topology-layouts.md` — layout rules for each of the 8 topologies
- `references/components.md` — node cards, badges, callouts, legend, animations
- `references/safety-rules.md` — mandatory layout constraints for all topologies
- `references/canvas.md` — infinite canvas with pan & zoom (Miro-like navigation)

Follow every rule in those references exactly. The design system is battle-tested — don't improvise fonts, colors, or layout patterns.

**Always include the infinite canvas system** from `references/canvas.md`. This lets users pan (click+drag) and zoom (scroll wheel) the diagram freely, like a whiteboard.

## Step 3 — Output

- Single `.html` file, all CSS in `<style>`, all JS in `<script>`
- No external dependencies except Google Fonts via `@import`
- No CSS frameworks, no JS libraries (vanilla JS for hub-and-spoke coordinates and canvas pan/zoom)
- Valid HTML5 with `<!DOCTYPE html>` as first line
- Must render correctly opened directly in a browser
- Responsive down to 360px viewport width

Save as `diagram-[topic-slug].html` in the current working directory. Open it in the browser with `open` (macOS) or `xdg-open` (Linux). Tell the user where it was saved.
