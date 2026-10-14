---
name: work-with-design-systems
description: >
  Inspect, build, or extend Figma design systems — and optionally sync them to
  code. Two modes in one skill: inspect mode (read-only audits with WCAG checks,
  component scoring, detached instance detection, handoff docs) and build mode
  (creating components with variable bindings, slot-based composition, structured
  descriptions, validation, and optional export of tokens.css + AI rules to
  the user's codebase).
  Use when the user says 'audit my design system', 'check component quality',
  'create design system', 'build DS in Figma', 'generate component library',
  'add slots to my components', 'sync design tokens from code', 'find detached
  instances', 'check WCAG compliance', 'export tokens to code', 'generate
  CLAUDE.md for design system', or wants to push a design system from code to
  Figma or back. The skill auto-detects the mode from request, or asks if unclear.
  After inspect, ALWAYS pauses and waits for explicit user decision before any
  build action. Phase 6 (sync to code) is OFF by default — only triggers on
  explicit user request.
  Does NOT implement Figma designs as code — use figma-implement-design for that.
  Does NOT create individual screens — use figma-generate-design for that.
compatibility: >
  Requires the figma-use skill to be installed. Requires Figma MCP server (remote)
  connected. Phase 6 (sync to code) requires file write access to the user's
  project — available in Claude Code, Cursor, Codex, and similar MCP clients.
  Not available when running in Claude.ai web/mobile chat (in that case Phase 6
  outputs file contents inline for the user to copy).
metadata:
  mcp-server: figma
  version: 2.1.1
---

# Work with design systems in Figma

Two modes in one skill: **inspect** (read-only quality audits with reports) and **build** (creating, fixing, extending components and tokens). Inspect produces structured reports. Build produces working Figma files. Build mode optionally extends to **Phase 6 (sync to code)** — generates `tokens.css`, an audit script, and AI rules file for the user's codebase. Phase 6 is off by default and only triggers on explicit user request.

Between inspect and build, the skill always pauses for the user to decide what to do with the report.

**Always pass `skillNames: "work-with-design-systems"` when calling `use_figma` as part of this skill.** This is a logging parameter — it does not affect execution.

## Prerequisites

**You MUST invoke the `figma-use` skill (Skill tool: `skill: "figma-use"`) before every `use_figma` call.** It contains critical Plugin API rules, gotchas, and script templates. Never call `use_figma` without it.

IMPORTANT: Before working with design systems in Figma, load the `working-with-design-systems/wwds.md` reference from the figma-use skill to understand key concepts and guidelines.

## Critical rules

These apply to BOTH modes — inspect and build.

1. **Work incrementally.** One component (or one variant set) per `use_figma` call. Validate after each step. This is the single most important practice for avoiding bugs.
2. **Never build on unvalidated work — match validation depth to change type.**
   - **Structural change** (new variant, restructured auto-layout, new property, `swapComponent`): `get_metadata` + `get_screenshot` before next step. Visual properties may have shifted invisibly.
   - **Binding / description / codeSyntax / scope / rename change**: verify INSIDE the same script via `node.boundVariables` / `node.description` / `variable.description` / `variable.codeSyntax` / `variable.scopes` reads, return as part of the result. No external `get_screenshot` needed — Figma is deterministic on these.
   - **End of batch**: one `get_screenshot` of the parent CS for visual sanity.
   Why: `get_screenshot` is the heaviest call, and Figma MCP rate-limits its read tools per plan and seat — **Professional Full/Dev seat: 10 calls/min and 200/day**; Organization: 15/min, 200/day; Enterprise: 20/min, 600/day; Starter: 20/month; View/Collab seats: 6/month (Figma's `rate-limits-access` doc, 2026-08). Only `whoami`, `create_new_file`, `add_code_connect_map` are exempt. The **daily** cap is the one that bites: a per-component inspect pass with a screenshot each can spend a whole day's budget on one mid-size file. Matching depth to risk frees that budget for the structural changes that actually need visual verification. Run `whoami` when unsure which tier applies.
3. **Bind visual properties to variables when a scale value exists.** Fills, strokes, padding, itemSpacing, corner radius. For component-specific dimensions that don't match any scale value (e.g., 3px internal padding on a toggle track, 1px divider offset), hardcoded values are acceptable — document these exceptions in the component description. **A tint of an existing colour is a token too:** a colour variable can alias another colour variable and carry its own opacity (`{ color: <alias>, opacity: <percent> }`), so a disabled, ghost, overlay or scrim value is an alias-with-opacity token — never a bound fill with a raw opacity typed on the paint, which no export and no audit can read. See `references/build/token-taxonomy.md`, "Alpha tokens".
4. **lineHeight variables must store pixel values, not percentages.** Figma variables are unitless. When bound to lineHeight, the value is interpreted as pixels. If your DS defines line heights as percentages (e.g., 150%), convert before storing: fontSize × (percentage / 100). Text styles can store {unit: "PERCENT", value: 150} — variables cannot.
5. **Set codeSyntax.WEB on every variable — one unique token name per variable.** Without it, agents using `get_design_context` get raw Figma variable names instead of code token names. Set during creation, not as a separate pass. Presence is not enough: a semantic token gets its **own** name (`--color-text-link`), never the name of the primitive it aliases (six roles sharing `--color-primary-500` cannot be told apart in a stylesheet), and never a **value** (`1.25rem`, `9999px`, `#fff`, `400` — Phase 6 would emit `--1rem: 1rem`). Spell it in the codebase's convention: a CSS custom property as `--name` or `var(--name)` (Figma's own examples use the `var()` form) is what Phase 6 `tokens.css` consumes; an SCSS `$token` or a bare `token-name` is valid when the project's documentation prescribes it, but Phase 6 cannot consume it. The validator reports values and duplicates as errors and non-CSS conventions as info. The dash form (`--group-leaf` or `--group--leaf`) is one project convention, confirmed in Phase 1e and never mixed; two names that become one after dash collapse and lowercasing are an error too, because a tool that normalizes names keeps only one of them.
6. **Set explicit variable scopes.** Never leave ALL_SCOPES. Background colors get FRAME_FILL + SHAPE_FILL. Text colors get TEXT_FILL. Spacing gets GAP + WIDTH_HEIGHT. Radius gets CORNER_RADIUS. Font size gets FONT_SIZE. **Empty `scopes` (`[]`) is the opposite failure and worse:** the variable is invisible in every property picker, so designers hand-paste hex into frames (seen in practice: 46 primitives, all `[]`, and hex pasted by hand). The validator reports both.
7. **TEXT properties with the same name merge across variants.** If two variants both define `addComponentProperty("Label", "TEXT", ...)`, they become ONE shared property on the component set with one default value. For different defaults per variant: use different property names, leave text as direct content with instance text overrides, or accept the shared default.
8. **TEXT component properties on every customizable text node.** Without them, label overrides ("Label" → "Submit") revert on component update. Every customizable text node needs `componentPropertyReferences = { characters: key }`.
9. **Use slots for compound components.** Compound components (Card, Modal, Dialog, ListItem, ReviewCard) that contain variable inner content MUST use named slots instead of detach patterns or text-only props. Without slots, agents and users detach the component to edit inner content, which breaks maintenance and the agent's ability to reason about composition. Slots are available in Figma as of March 2026. See `references/build/slots-guide.md`.
10. **Every public component MUST have a structured description.** Figma MCP reads component descriptions and passes them to agents as context. Missing descriptions force the agent to guess purpose, behavior, and composition. Use the template in `references/build/component-description-template.md`. **Use plain-text formatting (UPPERCASE section headers, no markdown bold or `##` — `get_design_context` escapes them) — see template's "MCP delivery format" section.** Private base components (prefixed with `.` or `_`) may use a one-line note. **A description is the spec, not a changelog:** no dates, people's names, decision history ("approved", "decided", "previous version"), node ids, repo or file paths, scan notes or instance counts. That history belongs in the project's decision records and work logs. A note this skill asks for (a Rule #3 exception, a slot decision) is written as the current rule. A **variable** description follows `references/build/variable-description-template.md` (PURPOSE / USAGE / CONSTRAINT) under the same format rules and the same exclusion.
11. **Never detach a component.** If you need to vary inner content, use: variant, boolean property, instance swap, or named slot. Detaching breaks the design-to-code bridge — the detached frame becomes structurally invisible to agents and to inspect mode.

---

## Mode selection

The skill operates in one of two modes. The first thing to do in any session is determine the mode.

**Inspect mode** triggers when the user says:
- "audit my design system" / "check component quality" / "review my DS"
- "find detached instances" / "check WCAG" / "score my components"
- "generate handoff docs" / "export component specs"
- "is this design system ready" / "what's broken in my file"
- Any request that asks for a report or evaluation without explicit "build" or "fix"

**Build mode** triggers when the user says:
- "create design system" / "build DS in Figma" / "generate component library"
- "set up tokens" / "add components" / "sync from code"
- "fix ALL_SCOPES" / "add codeSyntax" / "rebuild Variables"
- "add slots to my components" / "write descriptions"
- "export tokens.css" / "generate CLAUDE.md" / "sync to code" (these enter build mode and proceed directly to Phase 6 if rest of system is in good shape)
- Any request that asks for changes to the file or codebase

**Ambiguous requests** like "I have a Figma file with some issues — help me with my design system" — ASK the user explicitly:

> Should I run a quality audit first (read-only report with scores and issues), or go straight to building/fixing? If you want both, I'll do inspect first, show you the report, then wait for your decision before changing anything.

**Default behavior when explicitly mixed** ("audit and fix"): start with inspect mode, produce report, pause, wait for user direction.

---

## Inspect mode

Read-only. Never modifies the file. Produces structured reports.

Read `references/inspect/overview.md` before starting. It documents which modules to run for which user requests, the execution order, and the readiness scoring formula.

### Inspect workflow

1. **Scope.** Ask the user: full file or specific components? Which audit modules? Default is all six. Export format — markdown (default), JSON, both, or AI prompt.
2. **Inventory.** Run `scripts/inspect/inventory.js` to list all component sets with variant counts and page locations. Present as a table for user confirmation.
3. **Run modules** for each component set in this order:
   - Module 1 — Token compliance (`scripts/inspect/audit-tokens.js`) — outputs errors and warnings separately
   - Module 2 — Interactive states (`scripts/inspect/audit-states.js`)
   - Module 3 — Accessibility (`scripts/inspect/audit-accessibility.js`)
   - Module 4 — Detached instances (`scripts/inspect/audit-detached.js`) — runs once, file-wide
   - Module 5 — Naming quality (`scripts/inspect/audit-naming.js`)
   - Module 6 — Component descriptions (no script — uses Claude reasoning, read `references/inspect/component-descriptions.md`)
4. **Compile report** using templates from `references/inspect/report-templates.md`. Calculate weighted readiness score per component using the formula in `references/inspect/readiness-scoring.md` (errors weighted 1.0, warnings weighted 0.3).
5. **Export** report to `/mnt/user-data/outputs/audit-report.md` (and `.json` if requested).
6. **STOP.** Present report summary. Wait for user decision.

### Inspect → build handoff

After inspect, the skill MUST pause and present:

> Audit complete. Report saved to `audit-report.md`. Overall score: {score}/100.
>
> Top issues:
> 1. {highest_impact_issue}
> 2. {second_highest_impact_issue}
> 3. {third_highest_impact_issue}
>
> What would you like to do next?
> - **Fix issues** — switch to build mode and address findings (I'll work through the priority list)
> - **Fix specific issues** — tell me which to address (e.g., "fix only the ALL_SCOPES violations")
> - **Build new components** — switch to build mode for new work, leaving issues for later
> - **Stop** — keep the report for later, do nothing

DO NOT proceed to any build action without explicit user confirmation. This pause is the core guarantee of inspect mode.

---

## Build mode

Read/write. Creates, modifies, validates.

Read `references/build/component-spec.md` and `references/build/token-taxonomy.md` before starting Phase 2 (foundations) or Phase 4 (components). Read `references/build/slots-guide.md` before building any compound component. Read `references/build/auto-fix-guide.md` before running fuzzy auto-fix on existing components. Read `references/build/code-export.md` before entering Phase 6.

### Build workflow paths

**Full build** (no existing file): Phase 1 → 2 → 3 → 4 → 5 → (optional 6)

**Extend** (variables/styles exist, need components): Phase 1c (health check) → fix foundation issues → Phase 3 (file structure, if needed) → Phase 4 → Phase 5 → (optional 6)

**Fix foundations only**: Phase 1c → fix ALL_SCOPES/codeSyntax/unbound → stop

**Add slots to existing compound components**: Phase 1c → identify detach-prone components → Phase 4c (slot decision) → Phase 4 (build or update) → Phase 5

**Apply audit fixes — manual** (entry from inspect mode): user reviews report → confirms scope → enter build mode → execute fixes per priority list → Phase 5 verification → (optional 6)

**Apply audit fixes — fuzzy auto-fix** (entry from inspect mode, user opts in): user reviews report → requests "auto-fix the token issues" → Phase 1c health check (foundations must be valid) → run `scripts/build/fixHardcodedToTokens.js` with issues from inspect → review applied/skipped report with user → handle skipped items manually → Phase 5 verification → (optional 6)

**Code export only** (Figma file is solid, just need files in repo): Phase 1c (verify foundations OK) → skip 2/3/4/5 → Phase 6

### Phase 1: Discovery

#### 1a. Determine the source

Ask the user:
- **From scratch:** What's the product? Brand colors, typography, spacing? Reference (Figma file, website, brand guidelines)?
- **From codebase:** Where are tokens defined? (`tailwind.config.js`, `tokens.css`, `theme.ts`, design-tokens JSON). Where are components? (`src/components/ui/`)

Supported inputs for from-scratch builds:
- `.md` file with brand guidelines
- `.json` design tokens (W3C DTCG format, Tokens Studio format)
- Screenshots or URLs as visual references
- Verbal description of brand, colors, typography

#### 1b. If syncing from code — analyze the codebase

Scan for:
- Token files: CSS variables, Tailwind config, JSON token files, styled-components theme
- Component inventory: list all UI components, their props/variants, file paths
- Naming conventions: PascalCase vs kebab-case, variant naming patterns
- Framework: React, Vue, Svelte, Angular, or other
- **Storybook stories (if present):** Read `*.stories.{ts,tsx,js,jsx,mdx}` files. Each story = one Figma variant. Use story inventory to validate variant coverage in Phase 4. Missing variants on Figma side are as much a gap as missing stories on code side.

Read `references/build/framework-mappings.md` for framework-specific extraction patterns.

#### 1c. If a Figma file already exists — quick health check

Fast sanity check to build a state ledger and decide how to proceed. NOT a full audit — for that, switch to inspect mode.

Run `scripts/build/validate-design-system.js` via `use_figma`. Then targeted checks:
- Variable scopes (flag ALL_SCOPES **and empty** scopes)
- codeSyntax quality — present on every variable, **unique** (also after dash collapse and lowercasing), and a CSS *name* (`--color-brand-primary`), not a value (`1.25rem`) and not the aliased primitive's name reused on a semantic role
- Duplicate variables
- Bindings sample via `get_metadata` on a few components, check `boundVariables` coverage
- Generic layer names (if >20% of layers in components are auto-named like `Frame 47`, suggest Figma's AI rename in Actions panel as a first pass)
- Detach patterns in compound components (flag for Phase 4c slot decision)

Recommend a path:
- **Build in place** — file has solid variables, components need fixes
- **New file, old as reference** — no variables, naming chaos, start fresh
- **Hybrid** — foundations solid, components need rebuild
- **Switch to inspect mode** — if user wants comprehensive audit before deciding
- **Code export only** — if Figma is solid and user just wants Phase 6 outputs

If foundations are complete, skip Phase 2.

#### 1d. Check for project overrides

Look for project-specific design system rules and load them as overrides on top of the skill's defaults. In priority order, check:

1. `<projectRoot>/.claude/rules/design-system.md` — Claude Code convention for DS rules
2. `<projectRoot>/.claude/rules/component-build-rules.md` — alternative name some projects use
3. `<projectRoot>/CLAUDE.md` — if it contains a "Components — Build Rules" or "Design System" section, load that section

If any of these exist, read them and treat the rules as **extensions**, not replacements, of this skill's Critical Rules and Phase requirements. Surface what you loaded to the user in one line: "Loaded project overrides from `<path>` — N additional rules will be applied."

Why: every team's DS has conventions the generic skill can't predict — component numbering schemes (`C{section}.{number}`), required registry fields (e.g. CMS element identifiers), brand-specific tokens (sharp buttons vs pill, scrim opacity values), description templates (a project-defined marker line first). Hardcoding these in the generic skill would over-specialize it; ignoring them forces the team to re-explain conventions every session. Loading them as overrides keeps the skill general while letting it act project-aware.

If no override file exists, proceed normally — do not block on absence.

#### 1e. Confirm scope

Present summary:
- Token categories (colors, spacing, radius, typography, shadows)
- Number of modes (Light/Dark, brands, Desktop/Mobile, platform modes such as web and presentation) and each collection's default mode
- Component list (prioritized — core first)
- Naming convention
- Component numbering convention (`C{section}.{number} {Name}`)
- CSS token naming for codeSyntax.WEB, including the dash form: single (`--color-bg-primary`) or double (`--color-bg--primary`), one form for the whole project
- If code export is in scope: the CSS strategy for every mode that is not a collection's default. Theme modes: `[data-theme]`, `prefers-color-scheme`, both, or one mode only. Platform modes: an attribute, a file per mode, or one mode exported and the other out of scope (`references/build/code-export.md`)

**Do not proceed until user confirms.**

### Phase 2: Foundations

**Skip if Phase 1c confirmed all needed tokens exist and pass quality checks.**

Read `references/build/token-taxonomy.md` before starting.

#### 2a. Variable Collections

**Recommended:** 3-tier (Primitives → Semantic → Component). Best for multi-brand or new builds.

**Alternative:** flat domain-based (Colors, Spacing, Radius, Typography). Valid for single-brand or rebuilds where this structure exists.

Match what's in the file or codebase. The requirement is not depth — it's that every variable has explicit scopes and codeSyntax.WEB.

When a variable gets a description, write it from `references/build/variable-description-template.md` and read `variable.description` back in the same script (Critical Rule #2).

#### 2b. Text Styles and Effect Styles

Create text styles with proper variable bindings (font-size, line-height, font-weight, letter-spacing all bound to variables). Apply lineHeight gotcha (Critical Rule #4).

**Text wrap (Figma, Aug 2026):** text layers, text styles and individual paragraphs now carry a wrap mode — default, `Balance` (even line lengths) or `Pretty` (no orphan word on the last line). Decide it per text style, not per layer: `Pretty` for body/paragraph styles, `Balance` for headings and pull quotes, default for UI labels. The Plugin API property is not documented in `figma-use` yet — set it in the UI, or grep `plugin-api-standalone.d.ts` for the property name before scripting it. It does not survive export to PPTX / Figma Slides, so a system that also feeds presentations must not rely on it for line breaks.

**Responsive / fluid type:** model it with collection **modes**, not by hardcoding one size. Give the Typography collection a `Desktop` (default) and a `Mobile` mode; every `font-size` / `line-height` token carries a value per mode. A frame previews mobile via `setExplicitVariableModeForCollection(typographyCollection, mobileModeId)` while reusing the same text styles, and on code export the Mobile mode takes a media-query target (the formatter does not emit `clamp()`; `code-export.md`, "Not covered"). Keep `Desktop` the default so styles preview at full size. (Line-height stays in pixels — Critical Rule #4.)

Create effect styles for shadows, blurs.

#### 2c. Semantic layer completeness — cover every role, never skip status

When building the Semantic tier, verify it covers the full role surface, not just the obvious ones:

- **background** (canvas / surface / subtle / inverse) · **text** (primary / secondary / muted / inverse / on-brand) · **border** (default / strong / focus) · **interactive** (primary / secondary / disabled, + hover) · **status** (success / warning / error / info — each as solid / bg / text) · **accent** (optional)

**Status is the most-missed group — treat it as mandatory for any app UI.** Without it there is no token to show an error, a validation message, or a success toast.

**If the source / brand palette has no status hues (especially no red for `error`):** do NOT silently omit them and do NOT force a brand colour into a status role (a brown "error" reads as wrong and breaks the convention). Surface the gap to the user and propose a small functional status ramp (`error | warning | success | info` × `{bg, solid, text}`) tuned to harmonise with the palette, with every text-on-bg pair checked for WCAG AA (≥ 4.5:1). Status colour is functional infrastructure, not brand expression. See `references/build/token-taxonomy.md`.

### Phase 3: File structure

**Skip if documentation pages aren't required.**

Standard pages: Cover, Getting Started, Foundations, one page per component group, Patterns (if applicable), Utilities.

Foundations page contains: rendered swatches for each color variable, type specimens for each text style, spacing scale visualization, effect previews.

**Colour swatch card (recommended anatomy):** group swatches by role (PRIMARY / SECONDARY / NEUTRALS / STATUS …) under uppercase section titles — uppercase via the text style's `textCase = 'UPPER'`, **never by typing capitals into `characters`** (source text stays sentence-case; a restyle then needs no retyping). Each card = a large swatch bound to the variable, then three text lines: human name (bold), the code token (`--token-name`, from codeSyntax.WEB), and `HEX CODE : #RRGGBB`. Add a 1px neutral border to swatches whose luminance is high (≈ > 0.82) so white / light-tint swatches stay visible on a white page. **Type specimen:** one row per text style; if the scale is responsive, show a `Desktop` column and a fixed-width `Mobile` column (mode-switched) side by side so the fluid behaviour is visible.

Component pages use fixed-width (996px) wrapper structure:
- Wrapper: 996px wide, AUTO height
- Specs container: FILL width, AUTO height, padL/R=96, itemSpacing=64

Patterns page (if patterns documented) follows the same wrapper structure. Read `references/build/patterns-guide.md` for pattern frame conventions.

Create a reusable Page Title component on Utilities page. Each component page uses an instance, not a manual frame.

### Phase 4: Components

#### 4a. Confirm component list

Suggest defaults (Button, Input, Select, Checkbox, Radio, Toggle, Card, Modal, Badge, Avatar, Toast). User confirms based on actual inventory. Add or remove freely.

Read `references/build/component-spec.md` for default specs.

#### 4b. Build each component

One component per `use_figma` call. Validate after each.

Sequence per component:
1. Create base structure (component frame, variants, Auto Layout) via `use_figma` — patterns in `figma-use` skill's `working-with-design-systems/wwds.md` reference
2. Bind variables to fills, strokes, padding, item spacing, corner radius via `use_figma` — same reference
3. Add component properties (variants, booleans, instance swaps, TEXT properties)
4. Set spec wrapper frame (state labels as column headers, size labels as row labels)
5. **Write structured description** using `references/build/component-description-template.md` (Critical Rule #10)
6. Validate with `get_metadata` + `get_screenshot`

#### 4c. Slot decision (for compound components)

Before building Card, Modal, Dialog, ListItem, ReviewCard, or any component that hosts variable inner content — read `references/build/slots-guide.md` and decide:

1. **Variant** — for fixed appearance changes (size, type, state)
2. **Boolean property** — for visibility toggles (has icon, show divider)
3. **Instance swap** — for single predictable element changes (icon, avatar)
4. **Named slot** — for arbitrary user-provided content (card body, modal content)

When in doubt for compound components, prefer slots. Document the decision in the component description.

#### 4d. Patterns (optional)

If user wants composition patterns documented, read `references/build/patterns-guide.md`. Build pattern frames on the Patterns page using actual component instances arranged according to layout rules. Number patterns as `P{section}.{number} {Name}`.

### Phase 5: QA

Run `scripts/build/validate-design-system.js` for full file audit (variables and styles are file-level; the component-tree walk covers one page per call — pass `PAGE_ID` and fan out one call per component page, see `references/inspect/overview.md`):
- All collections present
- No ALL_SCOPES or empty-scope variables
- Every variable has a unique, name-shaped codeSyntax.WEB, still unique after dash collapse
- No hardcoded fills in components
- All components have Auto Layout
- Light/Dark modes tested
- All public components have descriptions
- All compound components have slot decision documented

Build a test page assembling several components together to verify composability.

**If you edit any script in `scripts/`, run the fixed set before and after the edit:** `npm test` (no dependencies, Node only) runs the scripts against the JSON fixtures in `tests/fixtures/` through a mock `figma`, compares them to the hand-written answer keys in `tests/expected/`, and prints a fixture × check grid with a score line. A red row before the edit is what the edit must turn green; a green row that goes red is the regression. A fixture is cheap — add one for the shape you are fixing rather than checking the change by hand on a live file.

If the file is a **published library**, remind the user to click **Publish** — consumer files keep the old scopes, names and bindings until they accept the library update, so a fix that validates here is invisible downstream until then.

After QA passes, present this prompt to the user:

> Build complete. {N} components, {M} tokens, all validated.
>
> Want to sync to code? I can generate up to four files in your project:
> - `tokens.css` — design tokens with three-layer indirection (handles Light/Dark modes)
> - AI rules file — design system rules for the AI agent in this repo (Claude Code / Cursor / Codex)
> - `scripts/token-audit.js` — CI-ready audit script that catches hardcoded values
> - `specs/patterns/*.md` — optional composition spec files (Hardik Pandya-style)
>
> Reply with "yes, sync to code" to enter Phase 6, or "done" to stop here.

Do NOT enter Phase 6 unless user explicitly requests it.

### Phase 6: Sync to code (optional, OFF by default)

**Pre-condition:** This phase requires file write access to the user's project root. Available in Claude Code, Cursor, and other MCP clients with file write tools. NOT available when skill runs in Claude.ai web/mobile chat — in that case, output the file contents inline for the user to copy manually.

**When to enter Phase 6:**
- User explicitly asks: "and generate tokens.css", "create CLAUDE.md for this DS", "set up the audit script", "sync to code"
- User accepts the Phase 5 closing prompt with "yes, sync to code"
- User starts session with explicit Phase 6 intent (e.g., "my Figma DS is solid, just generate tokens.css and CLAUDE.md") — skill runs Phase 1c health check then jumps directly to Phase 6
- DO NOT enter Phase 6 automatically. Retrofit scenarios (slot retrofit, partial fixes, foundation-only fixes) should never trigger Phase 6.

Read `references/build/code-export.md` before starting Phase 6.

#### 6a. Format detection

Determine which AI agent client the project uses by checking the project root:
- `.claude/` directory or `CLAUDE.md` file exists → Claude Code
- `.cursor/` directory exists → Cursor
- `AGENTS.md` file exists → Codex
- None of the above → ask the user, or skip AI rules generation

If multiple are present, ask which the user wants. Skill can generate for multiple at once.

#### 6b. Output path resolution

**Important:** never overwrite an existing top-level `CLAUDE.md`, `AGENTS.md`, or full `.cursor/rules`. The skill writes to scoped locations:
- Claude Code → `.claude/rules/design-system.md`
- Cursor → `.cursor/rules/design-system.mdc`
- Codex → append a `## Design system` section to `AGENTS.md` between explicit start/end markers (`<!-- design-system-rules-start -->` / `<!-- design-system-rules-end -->`) for safe future updates

If the scoped path already has a file from a previous Phase 6 run, ask user: overwrite, append, or skip.

#### 6c. tokens.css strategy

Ask the user how Light/Dark modes should resolve in CSS:
- `[data-theme="dark"]` attribute on root — most flexible, requires JS to set
- `@media (prefers-color-scheme: dark)` — automatic, follows OS preference
- Both — explicit attribute wins, falls back to media query
- Single mode only — skip dark export

Multi-brand modes: use the same attribute pattern with brand-specific values (`[data-brand="acme"]`).

Platform modes (a collection whose modes are output platforms, not themes): use the strategy chosen in Phase 1e. See `code-export.md`, "Collections with platform modes". Every mode that is not its collection's default needs a target; the formatter refuses a mode without one.

Read `references/build/code-export.md` for full structure with examples for each strategy.

#### 6d. Generate files

For each file, use Claude's file write tools (NOT `use_figma`). Generate:

1. **`tokens.css`**: call `scripts/build/exportTokensToCSS.js` via `use_figma` and save the JSON it returns to a file. Write the strategy from 6c as a targets map (`references/build/code-export.md`, "Formatting tokens.css"), then, from the project root, run `node <skill folder>/scripts/export/formatTokensCSS.js <export.json> <targets.json> > <path>/tokens.css`. The CSS comes from that formatter and is never written or patched by the model from prose: when a value is wrong, fix the variable, its codeSyntax or the targets map, and run it again. When the formatter refuses, its errors name what to fix.

2. **AI rules file** — read template from `references/build/code-export.md` "AI rules templates" section. Fill in component list (from current build), token reference list, audit script reference. Write to scoped path determined in 6b.

3. **`scripts/token-audit.js`** — read template from `references/build/code-export.md` "Audit script template" section. Fill in TOKENS object with token names and raw values from current build. Write to project's scripts directory (create if missing).

4. **(Optional) `specs/patterns/*.md`** — only if user explicitly asks ("also generate spec files for patterns"). One markdown file per pattern documented in Phase 4d. Use template from `references/build/code-export.md`.

If running in Claude.ai web (no file write tools), output each file's contents in fenced code blocks with clear "save as: {path}" headers. Where Node cannot run either, `tokens.css` is the exception: output the exporter JSON, the targets map and the formatter command, never a hand-formatted `tokens.css`.

#### 6e. Verify

After writing files:
- If Node is available in the environment, run `node scripts/token-audit.js` and report results
- Note: if the project's existing CSS has hardcoded values, audit will flag them — that's expected on first run and tells the user where to apply tokens
- Confirm AI rules file is at correct scoped path (not overwriting top-level files)

Report file paths to user. Phase 6 complete.

---

## Other design surfaces

Build mode and Phase 6 sync are Figma-only: variables ↔ code. Some teams draw screens in a second canvas tool that keeps its own token store. In that case the source of truth stays the tokens file (or the design-system document that holds the same values), and the tool's tokens are a **projection** of it:

- Create the tool's tokens from the file through its token API, never by hand from memory.
- **Names must survive the import.** A second tool may normalize names on import: collapse a double dash, lowercase, strip characters it does not allow. Before the push, run the collision check over that normalization. The validator's dash-collapse check (`codeSyntaxCollisions`) covers collapse and lowercase; for any other rule the tool applies, apply it to every name and look for two that become one. After the push, read the tool's tokens back and diff the names 1:1 against the file, not only the values. A name that changed on import is a drift: resolve it by renaming at the source (the variable or its codeSyntax), never by a hand fix in the tool. With a tool that collapses dashes, a double-dash form cannot survive the import; weigh that when the dash form is chosen in Phase 1e.
- Before any hand-off (exports into the repo, a task for a builder), read the tool's token list back and diff it against the file. Colors, spacing and radius must match 1:1. Line-height may drift where the tool approximates it in px; record the drift, don't fix it.
- A token that exists in the tool and not in the file is an invented rule. Report it for a decision, then add it to the file first and to the tool second.
- Inspect mode's semantic-role coverage (the mandatory status group, AA pairs, code-ready names) applies to a design-system document exactly as it applies to a Figma library. Run it on the file.

This skill does not draw screens in any tool. Tool mechanics belong to that tool's own skill or guide.

## Example (inline reference)

**Inspect mode — quality report on someone else's file**

User: "Audit this Figma file — I'm reviewing it for a client engagement."

Mode: Inspect.

1. Scope: full file, all six modules, markdown export
2. Inventory: 23 component sets across 5 pages
3. Run all modules per component
4. Compile report with scores
5. Export to audit-report.md
6. STOP. Present summary, wait for user decision.

For 8 more examples (full build, inspect → build paired flow, slot retrofit, narrow-scope inspect, end-to-end Phase 6, code-export-only, touch-up description pass) see `references/examples.md`. Load it when the request doesn't clearly match the inline example above.

For unusual situations (mode unclear, Phase 6 in Claude.ai web, missing fonts, token conflicts, rate limits, conflicting project overrides) see `references/edge-cases.md`. Load it when you hit one.

---

## Error recovery

On any `use_figma` error:
1. Stop. Do not retry immediately.
2. Read the error message.
3. Call `get_metadata` to understand current file state.
4. Fix the root cause in the script.
5. Retry.

For full error recovery workflow, load `figma-use` skill.

On Phase 6 file write errors:
1. Stop. Report which file failed and why (permission, missing directory, conflict).
2. Do not partially write — leave already-written files in place but stop generation.
3. Present error to user with options (fix permissions, skip file, retry, abort Phase 6).
