---
name: lucian-uxui
description: Builds sites, pages and components from Lucian UX/UI Prompt (lucianlabs.dev/uxui-prompt), a growing library of polished, dependency-free interactive UI elements with light and dark themes, keyboard and touch support and reduced motion. It covers buttons, toggles, inputs, menus and tabs, cards, sign-in and sign-up, toasts, loaders, empty and error states, charts, and app-level tools like editors, dashboards, schedulers and kanban boards. Searches the library, fetches only the chosen elements and ports them into the project's framework and theme. Use when the user names lucian-uxui, Lucian UX/UI or lucianlabs elements, or asks to build UI that should use them, e.g. "build a landing page with lucian-uxui", "lucian-uxui 스킬로 사이트 만들어줘", "루샨 UX/UI 요소로 로그인 화면 만들어줘". Not for backend work or for editing the library itself.
---

# Lucian UX/UI

Lucian UX/UI Prompt is a library of interactive UI elements. Each element is one self-contained snippet: a `<style>` block scoped to `.uNNN`, a root `<div class="ux uNNN">`, and a `<script>`. Every element reads its colors from `--ux-*` theme tokens. The library keeps growing (200 elements now, thousands later), so never assume what it contains. Search it every time.

All access goes through the bundled CLI. It caches on disk and falls back to a GitHub mirror when lucianlabs.dev is unreachable. `<skill-dir>` is the folder that contains this SKILL.md:

```sh
node <skill-dir>/scripts/lucian-uxui.mjs <command>
```

| Command | Use |
|---|---|
| `search <words...>` | Best matches for one UI part, such as `search pricing toggle` or `search 로그인`. Add `--category <slug>` or `--limit 20` to narrow or widen. |
| `list` | Categories with counts. `list --category <slug>` lists every element in one category. |
| `get <id> [<id>...]` | Full code for up to 8 elements. Fetch only the ones you will port. |
| `tokens` | The `--ux-*` light and dark tokens plus the `.ux` base rules that every element needs. |
| `info` | Data source, catalog version and cache folder, for troubleshooting. |

Add `--lang ko` for Korean copy. The default is `--lang en`. Use `--out <path>` with `get` or `tokens` to write files instead of printing them.

## Workflow

1. **Read the project.** Find the framework (React, Next, Vue, Svelte, Astro, plain HTML), the styling approach (CSS modules, Tailwind, global CSS), the theming approach (`data-theme`, a `.dark` class, CSS variables) and the language of the site's copy. If there is no project yet, use what the user asked for. If they named nothing, use plain HTML, CSS and JS.
2. **Break the request into UI parts**, for example: header nav, hero call-to-action button, monthly/yearly pricing toggle, sign-up form, FAQ, success toast, empty state. You build the page layout and sections (hero, pricing grid, footer) yourself. Lucian supplies the interactive parts inside them.
3. **Search once per part.** If the user names specific elements by number or gallery link (`#055`, `55`, `lucianlabs.dev/uxui-prompt/#055`), skip the search for them and `get` those exact elements. English keywords match best, and Korean also works. Read the one-line summaries and pick the element whose behavior fits the part. **Prefer a Lucian element whenever a reasonable match exists**, rather than writing your own. Build from scratch only when nothing fits, and match the Lucian look with the same tokens.
4. **Fetch what you picked**: `get <ids>`, at most a few at a time. Also run `tokens` once per project.
5. **Port each element** following [references/porting.md](references/porting.md). Read it before your first port.
6. **Check** both themes, a narrow mobile width (375px), keyboard use and `prefers-reduced-motion`.
7. **Report.** End your reply with a list of the elements you used. Give one line per element in the form `#ID title: where it is used, what you adapted, https://lucianlabs.dev/uxui-prompt/#ID`, and then list anything you could not check.

## Language

Use the language of the site's copy: `--lang ko` for a Korean site and `--lang en` for everything else. When the language is unclear, use English. Element text is sample copy either way. Replace it with the project's real content.

## Rules

- Use only code returned by `get`. Never invent element IDs or reconstruct an element from memory or from its summary.
- Keep the first line of each element, the `<!-- Lucian UX/UI Prompt #ID · MIT License ... -->` comment, at the top of the component file you create from it. The license requires it.
- Do not dump the whole catalog into context or download every element. Use `search`, and use `list --category` to browse.
- Port an element's structure, shapes and motion values (durations, curves, delays) as they are. Adapt the framework, data and colors, not the design.

## When the CLI cannot run

- **Network blocked** (exit code 3, common in sandboxes such as Codex): the CLI needs HTTPS access to `lucianlabs.dev` or, as a fallback, `raw.githubusercontent.com`. Request network permission for the command and rerun it. If the network stays unavailable and nothing is cached, tell the user. Do not substitute invented elements.
- **No Node.js**: use curl with the same data:
  ```sh
  curl -fsSL https://lucianlabs.dev/uxui-prompt/api/v1/en/catalog.tsv | grep -i "toggle"   # columns: id, cat, category, title, tags, shape, hash, summary
  curl -fsSL https://lucianlabs.dev/uxui-prompt/api/v1/en/e/056.txt                      # one element
  curl -fsSL https://lucianlabs.dev/uxui-prompt/api/v1/en/tokens.css                     # tokens
  ```
