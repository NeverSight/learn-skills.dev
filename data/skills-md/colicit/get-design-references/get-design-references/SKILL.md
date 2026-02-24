---
name: get-design-references
description: Search and retrieve highly curated frontend design references for the web. Use this skill when building (1) primitive components like buttons, inputs, and date pickers, (2) compositional patterns like cards, sidebars, and page sections, (3) complete views like hero sections, pricing pages, or analytics dashboards, and (4) design systems with cohesive color palettes, font pairings, and token values.
---

# Get Design References (GDR)

Semantically search Colicit's curated database of frontend design references. Returns grounded React + Tailwind code samples and images that can be adapted to any framework or style system.

## Artifact Types

- **Primitives** — Atomic components (buttons, inputs, toggles, date pickers).
- **Patterns** — Compositions of primitives (cards, sidebars, navbars, page sections).
- **Views** — Complete layouts (hero sections, pricing pages, dashboards).
- **Design Systems** — Cohesive token sets (color palettes, font pairings, spacing scales).

Artifacts from the same source share a `collection_id`. Use the collections endpoint to explore related artifacts.

## Search Modes

1. **Semantic search** — Describe what you need by function and style. Returns the closest matches ranked by similarity.
2. **ID lookup** — Fetch a specific artifact by its UUID.

## Setup

Use the GDR CLI:

```bash
# Install once (fastest repeated usage)
npm install -g @colicit/gdr-cli@latest

# Or run ad-hoc without global install
npx -y -p @colicit/gdr-cli@latest gdr --help
```

## Authentication

The CLI reads API keys in this order:

1. `GET_DESIGN_REFERENCES_API_KEY` in environment
2. `.env.local` in the project directory
3. `.env` in the project directory

For local projects, users typically store the key in `.env.local`:

```
GET_DESIGN_REFERENCES_API_KEY=<your-key>
```

Before any search/get command, verify auth:

```bash
gdr auth doctor --json
gdr auth status --json
```

If auth is unresolved, stop and ask the user to set `GET_DESIGN_REFERENCES_API_KEY` in environment or add it to `.env.local`/`.env`. Do not extract secrets with `grep`/`cut` or print them to logs.

## Workflow

1. Ensure `gdr` CLI is available (`gdr --help` or use `npx -y -p @colicit/gdr-cli@latest gdr ...`).
2. Run from the project root (or pass `--project-dir <path>`), then run `gdr auth status --json`.
3. Read [reference.md](reference.md) for command examples.
4. Identify the artifact type that matches the need (primitive, pattern, view, or design system).
5. Craft a concise `functional_description` (what it does) and `style_description` (how it looks).
6. Run the relevant `gdr ... --json` command. Inspect returned code/images/tokens.
7. Read [interpretation.md](interpretation.md) and apply its fidelity-first approach to reference usage.
8. Optionally, use `gdr collections get --collection-id <uuid> --json` to discover related artifacts from the same collection.