---
name: sb-setup
description: "Set up Storybook on a React+Vite app that has none — defer to `npx storybook ai setup`, then align viteFinal/providers/MCP and ask where stories live. Use for 'set up Storybook', 'install Storybook', or NO_STORYBOOK."
compatibility: "Requires Node.js and npx (defers to `npx storybook ai setup`); bash and python3 for the align + runtime-discovery scripts."
allowed-tools: Bash Read Glob Grep Write Edit
license: MIT
metadata:
  author: strongeron
  version: '2.4.0'
  bundle: storybook-workbench
  vendor:
    scripts: [discover-runtime.py]
    wrappers: false
    references: [install-wizard.md, native-ai-setup-prompt.md]
---

# sb-setup — native-first install

This skill is a thin **align+verify** layer. It does NOT re-implement a bootstrap wizard.

## Bootstrap — defer to Storybook

```bash
test -d .storybook && grep -q '"storybook"' package.json 2>/dev/null && echo PRESENT || echo NO_STORYBOOK
# NO_STORYBOOK → defer to Storybook's OWN official onboarding. `storybook` is the official npm
# package (@storybook/cli) — not a URL, not bundled or controlled by this skill; the USER runs it.
# This skill ships ZERO runtime dependencies and makes no network calls of its own. See SECURITY.md.
npx storybook ai setup        # Storybook 10.4 agentic onboarding (the official `storybook` package)
```

## Know what the native flow already does

Before layering anything on top, read `references/native-ai-setup-prompt.md` — the
**captured `storybook ai setup` prompt** (default `optimized-tests` variant), with its 8 rules of
engagement, 8-step plan (discover → shared preview → portals → MSW → write ≤10 colocated stories +
one `CssCheck` → `play` discipline → batch-verify → cleanup), 5 done-when criteria, and verbatim
code examples. Our job is to NOT redo any of that — only add the under-documented align bits below.

## Then align + verify (the under-documented bits)

Load `references/install-wizard.md` for the full align layer (load it **only when you're actually
aligning a fresh `storybook ai setup`** — **Do NOT load it** to answer a one-off "is my Storybook
configured right?" question; the checklist below is enough for that):

- **runtime discovery FIRST** — `${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/scripts/discover-runtime.py` →
  `.storybook/runtime.json`: the native Step-1 facts as ground truth (provider tree + `from`, root-CSS
  mechanism (JS import vs `index.html` `<link>`), portal target ids, network/MSW surface). The three
  bullets below come **from** it — verify against it, don't re-derive by reading the entry by hand.
- **viteFinal** — strip plugins Storybook can't use; keep aliases.
- **provider decorators** — wrap stories in the app's Router/Theme/Query providers (from `runtime.json.providers`).
  For a **class-based dark theme** (toggling `.dark` on `<html>`, colors from CSS vars), the decorator alone
  isn't enough: also theme the canvas root in `.storybook/preview-head.html` (`html, body, .sb-show-main {
  background: var(--color-background) }` + `html.dark { color-scheme: dark }`), or `centered` stories render a
  dark sliver in a white field and `padded`/`fullscreen` ones a white frame. (Snippet in `install-wizard.md` item 9.)
- **bare-OKLCH / shadcn-channel token bridge** — for a project whose `:root` declares **bare channel
  triplets** (`--background: 0.99 0.003 234`, no `oklch()` wrapper) under shadcn's `--background`/`--card`/…
  names with **no `--color-*` namespace** reaching the iframe, the wrappers' `--color-*` chrome refs resolve
  to nothing and every surface renders unstyled (the #1 "first run looked broken" gap on OKLCH design
  systems). Detect it (dominant `css-vars`, channel-triplet values, no `--color-background`) and
  **auto-generate the `--color-* → oklch(var(--bare))` bridge** into `.storybook/preview-head.html` for both
  modes — same place/mechanism as the canvas-root theming above. Recipe + detection in `install-wizard.md` item 11.
- **MCP wiring** — detect `@storybook/addon-mcp` + `.mcp.json`; wire if present.
- **panel-visible default** — write `.storybook/manager.ts` with
  `addons.setConfig({ showPanel: true, panelPosition: 'bottom' })` so the Controls / Actions /
  Accessibility panel shows by default. Storybook ships no `manager.ts`; without it an accidental `A`
  keypress (or a dragged-closed divider) persists a "panel hidden" state in localStorage and
  reviewers/agents conclude the stories have no Controls. The Controls panel is where `sb-stories`'
  `argTypes` surface, so this is what makes that authoring work visible. (Snippet in `install-wizard.md`.)
- **theme switching (themed projects) — wire `@storybook/addon-themes`, don't hand-roll a `globalTypes.theme`.**
  If runtime discovery finds a theme mechanism (`next-themes`, a class-based `.dark`, or `data-theme`),
  register `withThemeByClassName` so the toolbar toggles the **same `.dark` class** the canvas-root theming
  (item 9) and the bare-OKLCH `--color-*` bridge (item 11) already key off — one switch re-skins every
  surface, and the wrappers' live `getComputedStyle` re-read fires on the flip. Without it a themed app
  opens with **no theme control at all** (the reviewer ends up hand-adding one — the gap this closes). Add
  `@storybook/addon-backgrounds` only if you need surface-on-surface checks. Snippet in `install-wizard.md` item 12.
- **accessibility is already installed — confirm, don't re-add.** Native `storybook init` bundles
  `@storybook/addon-a11y` (axe per story, incl. contrast); the panel-visible default above surfaces its
  Accessibility panel. Verify it's in `package.json` and the panel shows — runtime a11y/contrast is axe's
  job, so `DesignSystemHealth`'s checks stay **static** (raw-hex / undefined / orphan / scale-gap),
  complementary to axe, not a re-implementation of it.
- **docs-page composition** — set `parameters.docs.page` in `preview.tsx` to the standard autodocs blocks
  with the `UsageSection` block **near the top**, so every component's (and `Foundations/Colors` /
  `Typography`'s) Docs opens with a "Real usage in this app" status band before the playground. It reads
  the usage JSONs lazily (renders nothing until they exist), so it's safe to wire at setup. (Recipe +
  ordering in `install-wizard.md` Phase 4.)
- **adopt existing structure** — scan-and-match `storySort.order`, title taxonomy, file placement;
  don't impose new conventions on an established repo.
- **adopt the native prompt's preview doctrine** (`install-wizard.md` items 7–9): pin determinism
  the app itself reads in a global `beforeEach` (`MockDate` + only the `localStorage` keys it reads);
  `Edit` the init-generated `preview.tsx`, never overwrite it; emit **exactly one `CssCheck`**
  story (a `getComputedStyle` proof the CSS actually loaded — the #1 silent failure otherwise); and
  theme the **canvas root** for class-based dark themes (item 9 above).

> **On discovery:** the native prompt says "discover with Glob/Grep/Read, not shell." Our
> `inventory-project.sh`/`extract-*.sh`/`discover-runtime.py` chain *is* that cached discovery — it
> runs **once** and writes JSON (`project-inventory` · `flows` · `component-states` · `prop-shapes` ·
> `page-patterns` · `runtime`) you then Read, rather than re-grepping per call. **Never re-derive by
> shell scan what a script already wrote to `.storybook/*.json`** — cite the JSON field.

## Decide where everything lands (ASK — don't scatter the repo)

Everything the bundle writes goes under `.storybook/` (CONTEXT.md STORAGE MAP) so a client repo stays
clean. The **one** choice is **where stories live** — and you must **ask the user**, because writing
`Foo.stories.tsx` next to every component scatters files through a `src/` you may not own (a real demo
miss). Use `AskUserQuestion` (Claude) / `request_user_input` (Codex), or a numbered list if no blocking
tool exists — never silently pick:

> **Where should I save the stories? (everything else already lives under `.storybook/`.)**
> 1. **`.storybook/stories/`** *(default — recommended for an audit / client / messy repo)* — keeps
>    `src/` untouched; the whole audit is one removable folder.
> 2. **Co-located — `src/**/<Name>.stories.tsx`** *(opt in — for a project you own long-term)* —
>    Storybook's general convention; stories move with components.
> 3. **A custom folder** *(you name it — still one place; configured into `main.ts`)*.

**`.storybook/stories/` is the default**: if the user doesn't pick, or it's clearly a client/messy
repo, choose it — **never co-locate silently** (that's the scatter we're avoiding). Then **configure
`main.ts` `stories` to match** (`.storybook/stories/` → add `'./stories/**/*.stories.@(tsx|ts)'`
relative to `.storybook/`; a custom path → add its glob; keep the `@/` alias so stories import cleanly),
and **record the choice** in `.storybook/audit/status.md` as `storiesLocation: isolated|colocated|PATH`.
`sb-stories` and `sb-hub` read that and never re-ask.

> **Already had Storybook?** This ask still has to happen — if `sb-setup` is skipped because Storybook
> is present, the first `sb-stories` run asks instead (it refuses to write a story to an unconfirmed
> location). Decide it once, up front, so nothing scatters.

## Next

Once Storybook is present, run **`sb-inventory`** to discover real-vs-slop before authoring.
