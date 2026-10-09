---
name: ak-render
description: Show a plan, report, recap, diff review, dashboard, explainer, or comparison as one polished offline HTML page. Write a short YAML Page Spec and compile it with the ak-render CLI (npm package @bestagentkits/render) instead of hand-writing HTML, CSS, or JavaScript. Use when the user asks for an HTML report, a visual or shareable page, a status update, a code-review summary, a KPI dashboard, a timeline, a checklist, or a risk review, or when a long result reads better as a page than as terminal text.
---

# AK Render

AK Render compiles a short YAML or JSON **Page Spec** into one deterministic,
self-contained HTML file. The page opens from `file://` and makes no network
request. You describe what the page says. The compiler owns layout, colour,
typography, motion, accessibility, and security.

## Run the CLI

Use `ak-render` if it is on `PATH`. Otherwise prefix every command with
`npx -y @bestagentkits/render`. Node.js 20.11 or later is required. Reading the
spec from stdin (`-`) and the `mcp` command need version 0.2.0 or later, and
`search-catalog`, `describe --compact`, `catalog --category` and recipes need
0.3.0 or later, so check `npx -y @bestagentkits/render --version` first. Every command accepts
`--json` and never prompts.

## The loop

1. **Find the blocks.** Search by intent, or list one category. The full
   catalog of 83 block types and every action is about 7 kB:

   ```bash
   npx -y @bestagentkits/render search-catalog sortable table
   npx -y @bestagentkits/render catalog --category data
   npx -y @bestagentkits/render catalog
   ```

2. **Describe only the blocks you use.** `--compact` gives one line per prop
   for up to 12 types. Use `--json` on one type for its full contract:

   ```bash
   npx -y @bestagentkits/render describe steps data-table chart --compact
   npx -y @bestagentkits/render describe steps --json
   ```

3. **Write the spec** to a `.yaml` file, or pipe it on stdin with `-`. For a
   common page, start from a recipe and replace every placeholder:

   ```bash
   npx -y @bestagentkits/render recipes
   npx -y @bestagentkits/render recipe incident-report > page.yaml
   ```

4. **Validate and fix.** Exit code 1 means fix and retry:

   ```bash
   npx -y @bestagentkits/render validate page.yaml --json
   cat page.yaml | npx -y @bestagentkits/render validate - --json
   ```

   The result is `{ ok, diagnostics[] }`. Each diagnostic has a stable `code`
   and a JSON `path` to fix, such as `$.blocks[0].titl`. For an unknown prop,
   `details.allowed` lists the valid props. Fix every diagnostic by its path,
   then validate again.

5. **Compile** to an `.html` file. The first argument is the spec path, or
   `-` for stdin. `--theme` overrides the spec's preset:

   ```bash
   npx -y @bestagentkits/render page.yaml --out page.html --json
   npx -y @bestagentkits/render - --out page.html --theme swiss-clean < page.yaml
   ```

   The JSON summary reports `out`, `bytes`, `hash`, `theme`, `features`, and
   `warnings`. Don't read the HTML back into context, because the summary is
   enough.

6. **Open it** with the platform opener: `open page.html` on macOS,
   `xdg-open page.html` on Linux, or `start page.html` on Windows. Then tell the
   user the path.

## Minimal spec

```yaml
version: 1
meta:
  title: Migration plan
  description: How we move the API to the new gateway.
theme:
  preset: editorial # optional; see `themes`
blocks:
  - type: hero
    eyebrow: Plan
    title: Migration plan
    description: Move the public API to the new gateway without downtime.
  - type: section
    title: Steps
    blocks:
      - type: steps
        items:
          - title: Mirror traffic
            text: Send a copy of production requests to the new gateway.
          - title: Switch reads
            text: Route read endpoints once error rates match.
  - type: callout
    tone: info
    title: Rollback
    text: Point DNS back to the old gateway; no data migrates.
```

## Pick blocks by intent

Prefer semantic blocks, because they carry the design for you. Confirm each
block with `describe` before you use it.

| Page | Start with |
| --- | --- |
| Plan or roadmap | `hero`, `steps`, `timeline`, `risk-matrix`, `checklist`, `callout` |
| Recap or status | `hero`, `stats`, `timeline`, `checklist`, `list` |
| Diff or code review | `diff-summary`, `code-review`, `file-tree`, `code` |
| Dashboard | `kpi`, `chart`, `data-table`, `filter-bar`, `grid-item`, `main-aside` |
| Benchmark or evidence report | `benchmark-comparison`, `metric-breakdown`, `chart`, `references` |
| Incident or engineering status | `timeline`, `log-viewer`, `test-results`, `api-endpoint`, `kanban`, `roadmap` |
| Product page | `hero`, `pricing`, `feature-matrix`, `testimonial`, `logo-cloud`, `people` |
| Explainer | `hero`, `card-grid`, `tabs`, `accordion`, `code`, `callout` |
| Comparison or decision | `comparison`, `table`, `before-after`, `callout` |

Group blocks with `section`. Tabs, accordion sections, carousel slides, and
bento tiles can hold blocks in `items[i].blocks`. Use `grid`, `split`, and
`stack` only when the semantic blocks can't express the structure.

Put numbers that several blocks show in top-level `datasets` and bind each
block with `dataRef`. Native controls write page `state`, and `visibleWhen`
switches views from it. `percent` takes `87` for "87%".

## Themes

List the presets and set one with `theme.preset` in the spec or `--theme` on
the compile command:

```bash
npx -y @bestagentkits/render themes
```

The eleven built-in presets are `blueprint`, `crimson-press`, `data-console`,
`editorial`, `executive-report`, `paper-ink`, `product-studio`,
`research-notebook`, `swiss-clean`, `terminal-mono`, and `warm-signal`, and `themes` also lists any
project or user presets it finds. Use only a name it lists. Don't try to restyle the page.

## Rules

- **No raw HTML, CSS, or JS.** The spec has no field for them, and keys such
  as `rawHTML`, `iframe`, `srcdoc`, or `script` are rejected. Don't look for
  an escape hatch, and don't post-process the emitted file. Links accept
  `https`, `http`, `mailto`, and relative paths, and `javascript:` is rejected.
- **Backticks and double asterisks are the only inline markup.** In prose text
  (a `text`, a step or list item's `text`, a `description`, a `caption`), a
  pair of backticks renders as inline code, so write `` `ak-render validate` ``
  for a command, path or URL, and `**key phrase**` renders as bold. Use bold
  sparingly. Titles, `code` blocks, and `terminal` lines stay literal.
- **Never invent data.** Every number, date, name, path, and finding must come
  from the conversation, the repository, or tool output. If a value is
  unknown, leave the block out or ask. Don't fill it with a plausible guess.
- **Keep the page offline.** `policy.network` defaults to `deny`, so a remote
  image or video renders as a labelled fallback, and a remote video `poster`
  fails validation. Opt in only when the user asks for remote media:

  ```yaml
  policy:
    network:
      allow:
        - images
  ```

## MCP alternative

`npx -y @bestagentkits/render mcp` serves the same loop over stdio as the tools
`catalog` (optional `category`), `search-catalog` (`query`), `describe`
(`type`, or `types` with optional `compact`), `recipes`, `recipe` (`name`),
`validate` (`spec`), `render` (`spec`, `out`, optional `theme`), and `themes`. `spec` may be YAML or JSON text, or the parsed
object. `render` writes the file to `out` and returns only the summary. When
these tools are available, use them instead of the shell commands.

```json
{
  "mcpServers": {
    "ak-render": { "command": "npx", "args": ["-y", "@bestagentkits/render", "mcp"] }
  }
}
```
