---
name: code-to-figma
description: "CI-anchored code-to-Figma token export pipeline for keeping Figma aligned with the codebase. Use when the user asks to \"sync code to Figma\", \"export design tokens to Figma\", \"set up a Figma sync pipeline\", \"wire up the tokens-sync-to-figma plugin\", \"generate a figma-export.json\", \"create a page walker\", or \"keep Figma up to date with the codebase\"."
license: MIT
compatibility: macOS, Linux, or Windows with Node.js, Git, `jq`, and the GitHub CLI (`gh`)
metadata:
  author: t4sh
  version: "0.2.0"
  tags: figma, design-tokens, code-to-figma, figma-sync, token-export, w3c-dtcg, gist, ci, tailwind, css, design-system
---

# Code to Figma

Generate a project-specific Figma export pipeline: a walker that reads compiled HTML and CSS, resolves class → token bindings, and pushes a structured JSON artifact to a GitHub Gist that the **`tokens-sync-to-figma`** Figma plugin consumes.

The pipeline is intentionally one-directional and CI-anchored. During `setup`, assess the project once, generate scripts, and wire CI. After that, every push that touches tokens or templates automatically updates the Gist — no agent, no Figma API key, no per-sync friction.

## Commands

| Command | Use when | Outcome |
|---|---|---|
| `/code-to-figma setup` | First time; no scripts exist yet | Walker + token scripts generated, Gist created, CI wired, config saved |
| `/code-to-figma sync` | Scripts exist; push current state to Gist | figma-export.json built and patched to Gist |
| `/code-to-figma update` | Stack or token naming changed significantly | Scripts regenerated, CI and config updated |
| `/code-to-figma status` | Check pipeline health | Gist age, CI status, script presence, config validity |

Default to `/code-to-figma setup` when no `figma-sync.config.json` or walker scripts are found.

---

## `/code-to-figma setup`

### 1 — Assess the project

Read in this order before generating anything:

1. **Package manifest** — `package.json`, `pyproject.toml`, etc. Identify the framework (Next.js, Eleventy, SolidJS, plain HTML) and package manager.
2. **CSS / token files** — find the compiled output, not the source. Common paths:
   - Tailwind v4: `out/assets/css/tailwind.css` or equivalent build output
   - Custom CSS: look for a file with `--token-name: value;` custom property declarations
   - Style Dictionary: `tokens.json`, `variables.css`, or generated output in `dist/`
3. **Component CSS** — look for a `components.css` or `utilities.css` alongside the main CSS file
4. **Built HTML** — the compiled output page, not source templates. Common paths: `out/index.html`, `dist/index.html`, `_site/index.html`. **Next.js**: a default build emits no single HTML file; require `output: 'export'` (yields `out/index.html`) before proceeding — see the Next.js note in [`references/walker-patterns.md`](references/walker-patterns.md). If no static HTML artifact can be produced, stop and tell the user rather than guessing a path.
5. **Token naming convention** — read the CSS custom property names, extract the prefix-to-group mapping (e.g. `beige-*` → `palette/beige/`, `fs-*` → `typography/scale/`)
6. **Section structure** — scan the HTML for how sections are delimited: `<section id="...">`, `[data-section]`, `<article>`, header/footer landmarks, etc.

Ask one focused question if two genuinely different walker shapes are possible (e.g. sections identified by ID vs by class). Otherwise infer and state the choice.

### 2 — Generate and verify the scaffold

Create or update the project-specific walker, DTCG 2025.10 token converter, generic Gist pusher, `figma-sync.config.json`, package scripts, GitHub Actions workflow, Gist, secrets, first sync, and Figma plugin connection. Load [references/setup-scaffold.md](references/setup-scaffold.md) for the file specifications and [references/ci-and-gist-setup.md](references/ci-and-gist-setup.md) for the canonical Gist, secret, CI, and plugin setup commands.

Required local checks before relying on CI:

```bash
node scripts/tokens-to-figma/convert-to-dtcg.mjs
git status --short -- scripts/tokens-to-figma/*.w3c.json
node scripts/figma-export/walk-<site>.mjs | jq '.sections | length'
```

Keep the core boundary visible: CI produces `figma-export.json` and `<project>-tokens.w3c.json`; the `tokens-sync-to-figma` plugin consumes those artifacts inside the user-authorized Figma runtime. Do not require a Figma API key in CI.

---

## `/code-to-figma sync`

1. Confirm `figma-sync.config.json` exists and the walker path is valid.
2. Run: `node <walker> > figma-export.tmp.json`
3. Validate: `jq '.sections | length' figma-export.tmp.json`
4. Confirm `GIST_TOKEN` is exported or prefix the pusher command with it.
5. Push: `node scripts/tokens-to-figma/push-to-figma.mjs < figma-export.tmp.json`
6. Delete `figma-export.tmp.json` when done, then report sections and nodes exported and the Gist URL.

---

## `/code-to-figma update`

Use this when the framework output, token naming convention, section selectors, or CSS build paths changed enough that the existing walker may be stale.

1. Re-run the setup assessment against current compiled HTML/CSS and token files.
2. Update `walk-<site>.mjs`, `convert-to-dtcg.mjs`, `figma-sync.config.json`, and CI paths together so `tokenPath()`, explicit token types, and file paths stay aligned.
3. Regenerate the DTCG token artifact: `node scripts/tokens-to-figma/convert-to-dtcg.mjs`.
4. Validate the walker output: `node <walker> > figma-export.tmp.json && jq -e '.sections | type == "array"' figma-export.tmp.json`.
5. Push through `/code-to-figma sync` or CI after reviewing the script and `.w3c.json` diffs.

---

## `/code-to-figma status`

Report:

| Check | How |
|---|---|
| Walker script | Does `figma-sync.config.json` exist? Does the walker file exist? |
| Gist freshness | `gh api gists/<id> --jq '.updated_at'` — report how old the Gist is |
| CI wiring | Does `figma-sync.yml` exist? Does it have `workflow_dispatch`? |
| Secrets | `gh secret list --repo <org>/<repo>` — confirm `GIST_TOKEN` and `FIGMA_EXPORT_GIST_ID` are present |
| Last run | `gh run list --workflow=figma-sync.yml --limit=1` |

---

## Skill Boundaries

| User intent | Use |
|---|---|
| Export code tokens and page structure → Figma | This skill |
| Import a Figma design → code | **`figma-to-code`** skill |
| Edit Figma variables or components directly | The project's configured Figma write/design workflow (outside this skill) |
| Sync an existing Gist manually | `/code-to-figma sync` |

This skill does not edit Figma files. The plugin (`tokens-sync-to-figma`) is the Figma-side consumer — this skill produces the artifact it reads.

## Reference Files

| File | Load when |
|------|-----------|
| [references/walker-patterns.md](references/walker-patterns.md) | Generating or updating the walker, DTCG converter, or generic Gist pusher; adapting `tokenPath()`, explicit token taxonomy, section detection, or Next.js static-export constraints |
| [references/setup-scaffold.md](references/setup-scaffold.md) | Generating setup files, package scripts, Gist commands, GitHub secrets, first sync, or plugin-side contract details |
| [references/figma-export-contract.md](references/figma-export-contract.md) | Validating walker JSON output shape (`meta`, `sections`, nodes, token references) |
| [references/ci-and-gist-setup.md](references/ci-and-gist-setup.md) | Wiring `figma-sync.yml`, GitHub secrets, first Gist push, or `tokens-sync-to-figma` plugin setup |
| [references/benchmarks.md](references/benchmarks.md) | Comparing peer skills on [skills.sh](https://skills.sh) or positioning this pipeline vs alternatives |

## Operating Principles

- **Read the compiled output, not the source.** Token bindings only become resolvable in built HTML+CSS. Source templates may use variables that haven't been substituted yet.
- **`tokenPath()` and explicit `$type` mappings are the contract.** The walker and DTCG converter must use the same path function, and every exported token must have an intentional DTCG type. Never infer `$type` from the raw CSS value; fail on unknown taxonomy or non-conforming values.
- **Walker is project-specific; pusher is generic.** The walker understands the project's HTML shape; the pusher only knows the Gist API. Keep them separate.
- **Commit the DTCG JSON.** The `.w3c.json` file is the human-readable diff surface for token changes. It belongs in the repo, not in `.gitignore`.
- **`node` not `pnpm` in CI.** pnpm writes a script header to stdout when running a lifecycle script, which corrupts a `> file.json` redirect. Always invoke the walker with `node` directly in CI steps.
