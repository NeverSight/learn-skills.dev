---
name: build
description: Internal utility skill for regenerating site output. Use after any change to `src/`, `_partials/`, or `site.config.json`, or whenever another skill requires refreshed `dist/` artifacts. Runs `scripts/build.mjs` from the installed skill directory.
---

# Build

## Inputs

- Project root containing `src/`, `_partials/`, and `site.config.json`
- Optional precompiled CSS at `src/css/site.css`
- `SKILL_DIR`: directory containing this `SKILL.md`

## Steps

1. Resolve:
   1. `PROJECT_ROOT`: target user project root
   2. `SKILL_DIR`: directory containing this `SKILL.md`
2. Run:
   ```bash
   node "$SKILL_DIR/scripts/build.mjs" --project-root "$PROJECT_ROOT"
   ```
3. Confirm `dist/` exists and contains built HTML files.
4. If this skill is called by another skill workflow, fail fast on build errors and return the exact error text.

## Output

- `dist/` refreshed from `src/`
- Header/footer partials injected in built HTML files
- SEO/canonical/Open Graph metadata injected from `<!-- meta -->` blocks
- `dist/sitemap.xml` and `dist/robots.txt` regenerated

## Conventions

- Treat this as deterministic infrastructure: do not invent content here.
- Do not assume the user project has `package.json` scripts.
