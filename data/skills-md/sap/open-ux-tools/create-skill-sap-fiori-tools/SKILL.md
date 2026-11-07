---
name: create-skill-sap-fiori-tools
description: >
  Author, review, or refactor a skill for the SAP Fiori Tools / open-ux-tools
  ecosystem. Use this skill whenever the user wants to create a new skill,
  rewrite an existing one, add references, split an oversized SKILL.md, enforce the
  `sap-fiori-<feature>` naming convention, validate frontmatter, add CAP/RAP samples,
  declare OData V2 vs V4 requirements, mark a skill as internal (developer-facing) or
  external (public), or produce a verification checklist — even if the user does not
  explicitly say "skill". Enforces host-agnostic tooling, canonical fallbacks, explicit
  scope boundaries, and progressive-disclosure chunking (<500 lines per file).
argument-hint: "Skill name, category (internal|external), backends (CAP/RAP), OData version, target directory"
metadata:
  author: sap-fiori-tools
  version: "0.0.1"
---

# Create Skill — SAP Fiori Tools

Author skills for the `open-ux-tools` ecosystem, regardless of where they live on disk. This skill enforces the conventions that make SAP Fiori Tools skills portable across SAP-approved AI coding assistants (Github Copilot, Claude) and development environments (VS Code, SAP Business Application Studio) — and safe to ship publicly.

> **Skill location is an input, not a convention.** Different hosts and repos use different directories (`.agents/skills/` for contributor skills, `~/.agents/skills/` for user skills, `packages/fiori-mcp-server/skills/` for public skills in this monorepo, etc.). Ask the user *where* the skill should be created (or refactored) and treat that path as the target directory throughout. This SKILL.md never assumes a specific location.

> **Why a dedicated creator?** Generic skill-creator advice is not enough here. Our skills must run in multiple hosts, target two backends (CAP + ABAP RAP), two OData versions (V2 + V4), and two audiences (internal developers vs. public end users). This skill captures those constraints so authors do not have to rediscover them.

---

## Step 0 — Classify the skill (do this first)

Before writing anything, decide **who the skill is for**. This drives every later choice.

| Category | Audience | Examples in this repo | Ships publicly? |
|---|---|---|---|
| **Public** | Developers building SAP Fiori apps (CAP or standalone) | `sap-fiori-app-development`, `sap-fiori-analytical-chart`, `sap-fiori-tree-table`, `sap-fiori-create-cli`, `sap-fiori-eslint-plugin`, `sap-fiori-opa5-test-development`, `sap-fiori-add-visual-filter` | Yes |
| **Contributor** | Engineers working on the `open-ux-tools` monorepo itself | `eslint-rule-development`, `odata-vocabularies-sync` | No — monorepo-only |

### Naming convention (mandatory)

| Category | Pattern | Example |
|---|---|---|
| Public | `sap-fiori-<feature>` (kebab-case, feature-scoped, no product-suffix like `-cli` unless the skill *is* the CLI) | `sap-fiori-tree-table`, `sap-fiori-analytical-chart` |
| Contributor | `<domain>-<action>` (kebab-case; no `sap-fiori-` prefix so it is obvious the skill is not public) | `eslint-rule-development`, `odata-vocabularies-sync` |

**Do not** ship a public skill without the `sap-fiori-` prefix, and **do not** prefix a contributor-only skill with `sap-fiori-` (it will leak into user-facing skill listings).

Ask the user which category applies **if it is not obvious from the request**. Then continue.

### Frontmatter and folder structure validation

When creating the skill, ensure:

- [ ] `name` uses only lowercase letters, numbers, and hyphens (`/^[a-z0-9-]+$/`), between 3–64 characters
- [ ] Folder name matches the `name` field exactly (e.g., `sap-fiori-tree-table/` for `name: sap-fiori-tree-table`)
- [ ] `description` is between 50–1024 characters and includes trigger keywords
- [ ] File is named exactly `SKILL.md` (case-sensitive)
- [ ] Public skills go in `packages/fiori-mcp-server/skills/` (or equivalent public location)
- [ ] Contributor skills go in `.agents/skills/` (or equivalent internal location)

---

## Step 1 — Capture intent and inputs

Before drafting, confirm the following in one short exchange. Do not guess.

1. **Skill name** — follows the pattern from Step 0.
2. **Target directory** — absolute or workspace-relative path where the skill folder should be created. The skill will live at `<target-directory>/<skill-name>/SKILL.md`. For the open-ux-tools monorepo: public skills default to `packages/fiori-mcp-server/skills/`, contributor skills default to `.agents/skills/`.
3. **Documentation links** — authoritative reference documentation URLs (SAP Help, GitHub docs, API references). Fetch and analyze these first to derive the skill's content, requirements, and implementation steps.
4. **One-sentence purpose** — what does the skill let the model do? Can be derived from the documentation.
5. **Trigger phrases** — 3–4 realistic user prompts that should invoke this skill. They go into the `description` frontmatter.
6. **Scope boundary** — `read-only` or `draft`. Optional; only declare this for complex features like tree tables that have distinct read-only vs editable variants. Most skills default to `draft` (the skill modifies files/configurations). Omit this field unless the distinction matters.
7. **Backend coverage** — CAP only, RAP only, or both. Default to both; if both, samples for each are mandatory. Derive from documentation if the feature is backend-specific.
8. **OData version** — V2, V4, or both. Default to V4 (SAP Fiori elements templates like `FE_FEOP`, `FE_FPM` are V4-only). Check documentation for version requirements or V2 support.
9. **Host requirements** — List which environments the skill targets. SAP-approved hosts: **Github Copilot** (in VS Code/BAS), **Claude** (Claude Code, API, etc.). The skill may also work in other environments (Cursor, Windsurf, etc.) but those are not officially supported. If the feature requires host-specific capabilities (e.g., VS Code extensions for RAP, BAS-specific tooling), document those requirements AND the canonical fallback for other environments. Default: works in all environments unless stated otherwise.
10. **Prerequisite MCP servers / extensions** — Fiori MCP, CDS MCP, ABAP Development Tools, etc. Derive from the implementation requirements. If an MCP server is host-specific, note that.

If anything is missing, ask before drafting.

---

## Step 2 — Draft the SKILL.md

**First, fetch and analyze the documentation links** provided in Step 1. Extract:
- Implementation steps and prerequisites
- Configuration requirements and file changes
- Backend-specific differences (CAP vs RAP)
- OData version constraints
- Code examples and annotation patterns
- Common errors and troubleshooting guidance

Then create the skill folder at `<target-directory>/<skill-name>/` (target directory captured in Step 1) and place `SKILL.md` inside it. Use the canonical template in **[references/skill-template.md](references/skill-template.md)**. It contains ready-to-copy frontmatter for both internal and external skills, plus the standard section order:

1. Title + one-paragraph purpose
2. **Example User Prompts** — 3–4 realistic natural-language requests that invoke this skill (see Step 1, item 5)
3. **Prerequisites** (environment, MCP servers, OData version, backends)
4. **Scope boundary** (read-only / draft) — one sentence, near the top (optional if obvious)
5. **Mandatory inputs** (what to ask the user before doing anything)
6. Implementation steps (numbered, sequential — see Step 3)
6. Verification checklist for the implementation steps (see Step 4)
7. Testing (how to run the app and reach the feature — see Step 5)
8. Common Errors and Solutions (see Step 6)
9. Reference documentation links (see Step 7)

Keep the SKILL.md **under 500 lines**. If you cross that threshold, chunk into `references/` (Step 8).

### Writing style

- Prefer imperative voice: *"Read the manifest.json"*, not *"You should read..."*.
- Explain the **why** for non-obvious rules. LLMs follow reasoning better than they follow shouted `MUST`s. Save all-caps `MUST` / `NEVER` for the two or three genuinely dangerous cases (data loss, credential exposure, wrong OData version).
- Use tables for decision matrices (backend × OData version, host × MCP availability, etc.). They compress well and scan quickly.
- **Host portability.** Skills should work across SAP-approved environments (Github Copilot in VS Code/BAS, Claude) and be usable in other environments (Cursor, Windsurf, etc.) unless a feature genuinely requires host-specific tooling. When a capability is environment-specific (e.g., ABAP Development Tools extension for VS Code), document the requirement AND provide a fallback (e.g., "perform backend changes in your SAP system, then return for UI configuration").
- Show **short** code examples inline. Long snippets belong in `references/`.
- **Product-name capitalization (mandatory).** Write **SAP** in all caps, **Fiori** with a capital F, and **elements** in lowercase. Never write "Fiori" on its own — always **SAP Fiori** (or **SAP Fiori elements**, **SAP Fiori Tools**). Examples: ✅ `SAP Fiori elements`, `SAP Fiori Tools`, `SAP Fiori app` — ❌ `SAPUI5 Fiori`, `Fiori Elements`, `fiori app`, `SAP fiori`.

### Content quality checklist

Before finalizing SKILL.md, verify:

- [ ] All product names use proper capitalization throughout
- [ ] Implementation steps are numbered and sequential with clear objectives
- [ ] Each step includes preconditions and verification cues
- [ ] Verification Checklist section maps to implementation steps
- [ ] Testing section explains how to start the project (CAP vs standalone vs mock)
- [ ] Common Errors and Solutions section includes concrete error messages and fixes
- [ ] References section lists all authoritative documentation links
- [ ] ALL-CAPS warnings used sparingly (≤3 per skill)
- [ ] No duplication of content from other skills (use cross-references)
- [ ] All links checked and working
- [ ] For public skills: Prerequisites declare backends (CAP/RAP) and OData version (V2/V4)
- [ ] For public skills: If both backends supported, examples included for each

---

## Step 3 — Write steps that execute sequentially

Structure the implementation as **numbered, self-contained steps** that a model can execute one at a time without re-reading the whole file.

Each step should:

- Start with a clear objective ("Add the `@Aggregation.ApplySupported` annotation").
- List preconditions ("The entity must have at least one numeric property").
- Give a runnable snippet or an exact MCP call.
- End with a verification cue ("You should now see the aggregation function in `$metadata`").

**Why:** the model executes skills like a checklist. Steps that mix concerns force it to re-read and re-plan, which wastes tokens and produces inconsistent output.

Also: apply DRY. If two backends share 80% of the flow, put the shared part in the SKILL.md and split only the deltas into per-backend files under `references/` (for example `references/cap/implementation.md` and `references/rap/implementation.md`).

---

## Step 4 — Verification checklist for the implementation steps

Directly after the numbered implementation steps, add a **Verification Checklist** that lets the model (and the user) confirm every step from Step 3 was executed correctly on the target project. This is the feature-level check — not a skill-authoring check.

Use the `## Verification Checklist` block already present in **[references/skill-template.md](references/skill-template.md)** as the starting point, then adapt the `**After Step N — ...**` groups to the actual steps in your skill.

---

## Step 5 — Testing (how to run the app and reach the feature)

After the Verification Checklist, add a **Testing** section that tells the user exactly how to start their project so they can walk the Runtime and Regression groups of the checklist. Do not assume the user knows which script to run — CAP, standalone with a live backend, and standalone with mock data all use different commands.

Refer to `sap-fiori-app-development` (section *Application Preview Guidelines*) for anything environment-related (Node install, npm workspace, mock server details). Never re-explain generic project startup in every feature skill.
---

## Step 6 — Common Errors and Solutions section

Every skill ends with a **Common Errors and Solutions** section. This is the section users jump to when the happy path fails — it lists concrete error messages and the exact fix for each. Look at the `sap-fiori-tree-table` skill for a well-shaped example.

Use the `## Common Errors and Solutions` block already present in **[references/skill-template.md](references/skill-template.md)** as the starting point — it ships with a `<!-- TODO -->` placeholder ready to be filled in.

---

## Step 7 — Reference documentation links

Every **public skill** ends with a `## References` section that links out to the authoritative source. This is what users click when the skill's summary is not enough.

**Contributor skills** (internal to the monorepo) may omit this section if there are no specific references — most monorepo tasks reference AGENTS.md or package READMEs which contributors already know.

Do not paste raw URLs into the middle of the skill — link them from the References section and reference by name in prose. Broken links here are user-visible; check them before packaging.

---

## Step 8 — Chunking (the 500-line rule)

Skill files load into context. Long ones crowd out everything else and slow the model down. Follow progressive disclosure:

- **SKILL.md — always in context.** Keep it ≤ 500 lines. Use it as an index that points to `references/` for depth.
- **`references/*.md` — pulled in on demand.** Detailed CAP flows, RAP flows, error catalogues, long CDS templates, historical migration notes.

### Critical rule: Keep references one level deep

**All reference files must link directly from SKILL.md.** Never create references that link to other references — Claude may use preview commands like `head -100` when encountering nested references, resulting in incomplete information.

**✅ Correct — one level deep:**
```
SKILL.md → references/cap-implementation.md
SKILL.md → references/rap-implementation.md
SKILL.md → references/rap-read-only.md
SKILL.md → references/shared-implementation.md
```

**❌ Wrong — nested references:**
```
SKILL.md → references/index.md → references/cap-implementation.md
SKILL.md → references/rap-implementation.md → references/detailed-guides/1-read-only.md
```

If a reference file needs to point to related content, link back to another reference that is **also directly linked from SKILL.md**, not to a file buried deeper.

### When to split

Count lines with `wc -l SKILL.md`. If the file is:

- **< 300 lines** — keep flat.
- **300–500 lines** — consider splitting the largest section (usually the RAP implementation) into a file under `references/` (e.g. `references/rap-implementation.md`).
- **> 500 lines** — split now. Model performance drops sharply.

### Bundled assets validation

If the skill includes `references/`, `scripts/`, or `assets/` folders:

- [ ] Every reference file is directly linked from SKILL.md (no nested references)
- [ ] Reference files use descriptive names (`cap-implementation.md`, not `1.md`)
- [ ] No reference file exceeds 500 lines
- [ ] Each bundled file serves a clear purpose (helper scripts, code templates, reference data)
- [ ] No single asset exceeds 5MB
- [ ] No build output directories (`node_modules/`, `dist/`, `bin/`, `obj/`)
- [ ] Scripts include help documentation and error handling

Layout patterns that work well (paths shown relative to `<target-directory>/<skill-name>/`):

```
<skill-name>/
├── SKILL.md                        # ~200-400 lines: purpose, prerequisites, decision matrix, quick summaries
└── references/
    ├── cap-implementation.md       # Full CAP flow (linked from SKILL.md)
    ├── rap-implementation.md       # Full RAP flow (linked from SKILL.md)
    ├── rap-read-only.md            # RAP variant 1 (linked from SKILL.md)
    ├── rap-editable.md             # RAP variant 2 (linked from SKILL.md)
    └── shared-implementation.md    # Shared code (linked from SKILL.md)
```

**Note the flat structure under `references/`** — subdirectories like `cap/` and `rap/` are allowed for organization, but every `.md` file inside them must still be directly linked from SKILL.md, not from another reference file.

See existing skills such as `sap-fiori-tree-table/` and `sap-fiori-eslint-plugin/` (wherever your host stores them) for concrete examples.

---

## Step 9 — Don't Repeat Yourself (DRY)

Skills in this repo repeatedly discover the same patterns. Bake reusable content into shared references rather than restating it in every skill.

Signals you are repeating yourself:

- Two skills both explain "how to run `cds watch` for a CAP project" → link to `sap-fiori-app-development` instead.
- Every RAP skill re-explains "install ABAP Development Tools for VS Code" → put it once in a shared `references/` file and link.
- Three skills copy the same CDS snippet → move it to `references/shared-implementation.md` and link.

**Do not** duplicate content just to keep a skill "self-contained". Cross-references cost one line; duplication costs maintenance forever.

The one exception: **the Prerequisites section**. Repeat it in every skill even if it is nearly identical elsewhere. It is the first thing users read, and a link there is a bad user experience.

---

## Final validation

Before committing, run these commands to verify the skill structure:

```bash
# Count lines (must be ≤500)
wc -l <skill-name>/SKILL.md

# List all files (check for unexpected content)
find <skill-name> -type f

# Verify frontmatter parsing (should output name and description)
head -20 <skill-name>/SKILL.md | grep -E '^(name|description):'
```

Review the checklists in Steps 0, 2, and 8 to confirm all validation criteria are met. Remember: **SAP Fiori Tools** (capital 'T' in Tools).
