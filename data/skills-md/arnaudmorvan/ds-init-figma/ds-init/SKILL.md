---
name: ds-init
description: "Create a Design System in Figma. USE WHEN: project kickoff, Figma DS creation, setting up variables/tokens, creating Figma components, structuring pages. Also supports partial execution: adding a single component, generating a specific page, or running a specific phase on an existing DS file."
argument-hint: "Project name OR Figma link + task (e.g. 'MyApp DS', 'add a Tabs component to <figma-link>', 'generate examples page on <figma-link>')"
---

# DS Init — Create a Design System in Figma

## Goal

Create a complete Design System in Figma through a **modular and verified** execution.
Each phase is self-contained, verified by screenshot, and can be re-run without breaking things.

**This skill supports both full and partial execution** — see Execution Modes below.

**References**:
- [DS Knowledge Base](copilot-skill:/ds-audit/references/ds-knowledge-base.md) — patterns from audits
- [Figma Components Documentation](copilot-skill:/ds-audit/references/figma-components-doc.md) — SlotNode, Auto Layout, inheritance

**MCP Tools**:
- `mcp_figma_create_new_file` — Create the DS file
- `mcp_figma_use_figma` — Execute Figma Plugin API code
- `mcp_figma_get_screenshot` — Verify visual output

> **⚠️** `mcp_figma_generate_figma_design` is high-level. For precise control, use `mcp_figma_use_figma`.

---

## Execution Modes

Detect the user's intent and select the appropriate mode:

### Mode 1: `full` — Create a complete DS from scratch
**Trigger**: "Create a design system", "Initialize a DS", project name without Figma link
**Flow**: Phase 0 (questions) → Phase 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9
**Requires**: Nothing (creates a new file)

### Mode 2: `component` — Add a single component to an existing DS
**Trigger**: "Add a Tabs component", "Create a Modal component", "Build the Alert component"
**Flow**: Discover existing DS (variables, page structure) → Phase 5 for the specific component → Phase 7 for its showcase
**Requires**: Figma link to an existing DS file (or ask for it)

| Example prompts | Component | Phases |
|---|---|---|
| "Add a Tabs component" | Tabs | 5 (Tabs only) → 7 (Tabs showcase) |
| "Create Card, Badge, Avatar" | Card, Badge, Avatar | 5 (each) → 7 (each showcase) |
| "Add all Tier 2 components" | Card, Modal, Tabs, Alert, Badge | 5 (each) → 7 (each showcase) |

### Mode 3: `page` — Generate a specific page
**Trigger**: "Generate the examples page", "Create the welcome page", "Build foundations"
**Flow**: Discover existing DS → Run only the relevant phase
**Requires**: Figma link to an existing DS file with components already created

| Example prompts | Phase |
|---|---|
| "Generate the Welcome page" | Phase 8 |
| "Create the Foundations page" | Phase 6 |
| "Build example pages" | Phase 9 |
| "Create the Showcase page" | Phase 7 |
| "Generate the Icons page" | Phase 4 |
| "Build layouts and templates" | Phase 3 |

### Mode 4: `phase` — Run a specific phase by number
**Trigger**: "Run phase 6", "Execute phase 3"
**Flow**: Run exactly one phase file
**Requires**: All prerequisites for that phase must exist in the file

### Discovery step (Modes 2, 3, 4)

For partial execution on an existing file, **always start with a discovery step**:

```
1. get_screenshot of ALL pages to understand current state
2. Read existing variables (Color, Typography, Size collections)
3. Read existing Component Sets on 🔒 _Components
4. Identify what already exists vs what needs to be created
5. Proceed with the requested phase(s) only
```

> **⚠️ NEVER re-create** variables, doc components, or Component Sets that already exist.
> Use `getLocalVariablesAsync()` and `findAll()` to retrieve existing nodes.

---

## Golden Rule: Verify after EVERY call

```
AFTER every mcp_figma_use_figma:
1. get_screenshot of the modified page
2. Check: elements visible? overlaps? collapsed heights?
3. If problem → fix BEFORE moving to the next step
```

Read [references/rules.md](copilot-skill:/ds-init/references/rules.md) **before the first MCP call**.
Use patterns from [references/plugin-api-patterns.md](copilot-skill:/ds-init/references/plugin-api-patterns.md).
Follow visual conventions from [references/style-guide.md](copilot-skill:/ds-init/references/style-guide.md).

---

## Phase 0 — Information Gathering (BLOCKING)

> **⛔ BLOCKING**: DO NOT proceed to Phase 1 until the user has answered the questions.
> If the user says "defaults" or "don't care", use the default values.
> But ALWAYS ask the questions first — NEVER start silently.

**If the user already provides a Figma link + specs** → extract info from the message and confirm.
**If the user just says "run an init"** → ask the questions below BEFORE creating anything.

### Method: Ask the user the following questions

Present these questions to the user **before starting any phase**. Use whatever method your environment supports (interactive form, chat questions, etc.). Collect all answers before proceeding.

| # | Question | Options (★ = recommended default) | Free input? |
|---|----------|-----------------------------------|-------------|
| 1 | **DS Name** — What name for the Design System? | — | Yes |
| 2 | **Platform** — What target platform? | ★ Web · Mobile · Desktop · Multi | No |
| 3 | **Font** — What primary font? | ★ Inter · DM Sans · Plus Jakarta Sans | Yes (custom font) |
| 4 | **Primary color** — Primary color (hex)? e.g. #2563EB | — | Yes |
| 5 | **Secondary color** — Secondary color (hex)? e.g. #7C3AED | — | Yes |
| 6 | **Border radius** — Radius style? | Sharp (0-2px) · ★ Soft (4-8px) · Round (12-24px) · Full (999px) | No |
| 7 | **Shadows** — Shadow style? | ★ Subtle · Bold · Glow | No |
| 8 | **Dark mode** — Dark mode support? | ★ Yes · No · Later | No |
| 9 | **Spacing base** — Base spacing unit? | ★ 4px · 8px | No |
| 10 | **Components** — Which component tiers? | ★ Tier 1 (Button, Input, Select, Checkbox, Radio) · Tier 2 (+Card, Modal, Tabs, Alert, Badge) · Tier 3+ (all advanced) | No |
| 11 | **SaaS Templates** (multi-select) — Which SaaS templates? | ★ Dashboard · Settings · List/Detail · Table · Profile · Onboarding | No |
| 12 | **Landing Templates** (multi-select) — Which Landing templates? | ★ Hero · Features · Pricing · Testimonials · CTA Banner · Footer | No |
| 13 | **Doc header** — Include Doc Header components on pages? | ★ Yes · No | No |

> If the user cancels or doesn't respond → ask again in chat as a last resort.

**Silent defaults** (not asked):
- Type scale: Minor third 1.2
- Grid: 12 columns, 24px gutter, max-width 1280px
- Breakpoints: 640 / 768 / 1024 / 1280 / 1536
- Icons: Flaticon UIcons Regular Rounded

---

## Execution Phases

### Overview

| Phase | File | MCP Calls | Output |
|---|---|---|---|
| 1. Setup | [phases/01-setup.md](copilot-skill:/ds-init/phases/01-setup.md) | 1 create + 4 use | File + pages + 8 variable collections |
| 2. Doc Components | [phases/02-doc-components.md](copilot-skill:/ds-init/phases/02-doc-components.md) | 1 use | Header, Footer, Metadata, Divider |
| 3. Layouts & Templates | [phases/03-layouts-templates.md](copilot-skill:/ds-init/phases/03-layouts-templates.md) | 2 use | PageLayout, GridLayout, SaaS/Landing Templates |
| 4. Icons | [phases/04-icons.md](copilot-skill:/ds-init/phases/04-icons.md) | 2 use | Icon Component Set + Icons Page |
| 5. Components | [phases/05-components.md](copilot-skill:/ds-init/phases/05-components.md) | 1 per component | Button, TextField, Select, Checkbox, Radio |
| 6. Foundations | [phases/06-foundations.md](copilot-skill:/ds-init/phases/06-foundations.md) | 1 per section | Foundations Page (Colors, Typo, Size…) |
| 7. Showcase | [phases/07-showcase.md](copilot-skill:/ds-init/phases/07-showcase.md) | 1 per component | Components Page (Light + Dark) |
| 8. Welcome | [phases/08-welcome.md](copilot-skill:/ds-init/phases/08-welcome.md) | 1-2 use | Welcome Page |
| 9. Examples | [phases/09-examples.md](copilot-skill:/ds-init/phases/09-examples.md) | 4 use | Examples Page (Login, Dashboard, Settings, User List) |

### Execution Workflow

```
For each phase:
  1. Read the phase file (copilot-skill:/ds-init/phases/XX-*.md)
  2. Execute the described MCP calls
  3. Screenshot + visual verification
  4. If OK → next phase
  5. If problem → fix within the same phase BEFORE continuing
```

**Key principle**: one MCP call = one verifiable work unit.
NEVER chain 3+ calls without an intermediate screenshot.

### Dependency Order

```
Phase 1 (Setup) ─────────┬──→ Phase 2 (Doc Components)
                          │         │
                          ├──→ Phase 4 (Icons)
                          │         │
                          │         ▼
                          ├──→ Phase 5 (Components) ←── Phase 4
                          │         │
                          ├──→ Phase 3 (Layouts & Templates)
                          │
                          ├──→ Phase 6 (Foundations) ←── Phase 2
                          │
                          ├──→ Phase 7 (Showcase) ←── Phase 2 + 4 + 5
                          │
                          ├──→ Phase 8 (Welcome) ←── Phase 2 + 5
                          │
                          └──→ Phase 9 (Examples) ←── Phase 2 + 5
```

**Parallelizable**: Phases 3 and 4 can run independently after Phase 1+2.
**Sequential**: Phase 5 → Phase 7 (showcases instantiate the Component Sets).

---

## Page Separation — Architecture

> Main Components and presentation pages are **physically separated**.

| Page | Content |
|---|---|
| `🔒 _Components` | ALL Main Components (Component Sets, doc components, layouts, templates) |
| `📄 👋 Welcome` | DS showcase page |
| `🧱 Foundations` | Visual content: swatches, type scale, spacing scale… |
| `⚙️ Icons` | Categorized icon grid |
| `🏗️ Layouts` | Layout/template presentation with colored slots |
| `Components` | Showcase instances Light + Dark |
| `📐 Examples` | Composed example pages (Login, Dashboard, Settings, User List) |

---

## Summary (end of execution)

Produce a summary:

```markdown
## Figma DS initialized: [Name]

### Configuration
- Font: [font] | Primary: [hex] | Secondary: [hex]
- Radius: [style] | Dark mode: [yes/no]

### Created content
- [X] pages | [X] Variable Collections | [X] variables
- [X] Component Sets | [X] templates (SaaS + Landing)
- [X] icons imported

### Next steps
1. Validate colors/typography with stakeholders
2. Add Tier 2+ components
3. Test in a prototype
```
