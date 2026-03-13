---
name: toml
description: "Universal TOML documentation generator core. Detects repo language/framework, routes to matching reference rules, and maintains an up-to-date toml/ architecture mirror with incremental updates."
version: 1.2.0
category: Documentation, Code Analysis, AI Tools
---

# TOML Generator — Core Skill (Detect → Route → Mirror Updates)

> Design happens during REFACTORING, not during coding.
> See: references/tdd.md

## What this skill MUST do

1) Detect the project language(s) and framework(s).
2) Route to the correct rule references in `references/**`.
3) Generate and maintain a `toml/` folder that mirrors architecture.
4) On changes: incrementally update only impacted TOML files and indexes.

---

## Step 0 — Always start from TOML first (token efficiency)

On follow-ups:
- Read `toml/INDEX.toml` first.
- Then read relevant `toml/**/*.toml`.
  Only open source files if TOML is missing/outdated or user explicitly asks.

---

## Step 1 — Detect language & framework (MANDATORY)

High-confidence signals:
- JS/TS: `package.json` exists and `.js/.jsx/.ts/.tsx` files exist
- TS: `tsconfig.json` OR `typescript` in deps/devDeps
- React: `react` in deps OR `.jsx/.tsx` usage
- Next.js: `next` in deps OR `/app` or `/pages` with Next conventions
- Node server: `express|fastify|koa|hapi|nest` in deps OR server folder patterns

See:
- references/routing.md
- references/javascript/detect.md
- references/typescript/detect.md

---

## Step 2 — Route to ruleset (MANDATORY)

Select exactly one primary ruleset + optional sub-rules:

- If `typescript` + `react`:
  - See: references/typescript/react.md
  - See: references/typescript/extraction.md
- If `javascript` + `react`:
  - See: references/javascript/react.md
  - See: references/javascript/extraction.md

Optional add-ons:
- If `nextjs` detected:
  - See: references/typescript/nextjs.md OR references/javascript/nextjs.md
- If `node` server detected:
  - See: references/typescript/node.md OR references/javascript/node.md

See:
- references/routing.md

---

## Step 3 — Generate/Update TOML mirror (MANDATORY)

Mapping:
`path/to/File.ext` → `toml/path/to/File.toml` (preserve folders exactly)

Every TOML file MUST include:
- `[metadata]`
- `[properties]`
- `[context]`

See:
- references/index-format.md

---

## Step 4 — Incremental updates on code changes (MANDATORY)

Change scenarios:
1) Modified → regenerate that file’s TOML
2) Added → create TOML + update indexes
3) Deleted → remove TOML + update indexes
4) Renamed/moved → move TOML mirror + update indexes

Outdated if:
- TOML missing OR
- `metadata.source.generated_at` older than last known change OR
- `metadata.source.source_hash` mismatches (if used)

See:
- references/diff-update.md

---

## Step 5 — Indexes must stay in sync

Maintain:
- `toml/INDEX.md`
- `toml/INDEX.toml`

See:
- references/index-format.md

---

## Default scope rules

Default scan: `.`. Prioritize `src/` but include other top-level folders:
`shared/ lib/ libs/ packages/ apps/ server/ api/ services/ utils/ scripts/`

Never skip solely because folder is named `api`.

Exclude:
`node_modules/ .git/ dist/ build/ .next/ out/ coverage/`
assets, style-only files, tests.

---

## Non-negotiables

- Never include source code in TOML.
- Never flatten hierarchy.
- Avoid trivial descriptions; focus on WHAT + WHY + interface + architectural role.
- Never skip `[context]`.

> Design happens during REFACTORING, not during coding.
> See: references/tdd.md
