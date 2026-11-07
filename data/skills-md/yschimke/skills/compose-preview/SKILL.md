---
name: compose-preview
description: Render a Jetpack Compose or Compose Multiplatform @Preview to PNG in one call (MCP render_preview, or the compose-preview CLI) and look at it. Use whenever someone asks to render, show, or see what a composable, @Preview or Compose component looks like (including library components such as Material 3 or Wear M3 EdgeButton, which come from the hosted catalog), after editing Compose UI to verify it, to compare before/after, or to review previews against catalog design guidelines.
---

# Compose Preview

Render `@Preview` composables to PNG without Android Studio (Android via
Robolectric, CMP Desktop via Skia). CLI, Gradle plugin and renderers ship from
[compose-ai-tools](https://github.com/yschimke/compose-ai-tools); the MCP server
from [compose-preview-server](https://github.com/yschimke/compose-preview-server).

## Render first

For a request to render or show a preview, follow the short loop below. For a
requested guidelines review, use
[the review checklist](./references/design-guidelines.md) to choose the local,
hosted or UI Builder lane before invoking tools. Published catalogs and
server-homed designs use hosted tools first; a missing local checkout does not
require cloning, Gradle or a cloud environment. If tools are unavailable,
report blocked evidence and follow the integration's setup guidance.

With the local MCP server attached (compose-preview-server 3.78.0+), its
`initialize` instructions say how to call it: `render_preview
preview=<FunctionName>`, no exploring or registering first, no hand-built
mocks. Follow them. This skill adds the budget: a routine render is at most
three tool calls, with no base64 in the reply and images only when you need to
see them.

Your first call is the render. Don't grep for the preview or read its source
first: the server finds it by function name. Look things up only if the render
fails.

1. **Render.** If your client reads local files (Claude Code, Codex, Gemini
   CLI, OpenCode, Antigravity), pass `inline=false`. The result is `pngPath`,
   `sha256`, dimensions and `changed`, with no image tokens. If it lists
   `otherMatches`, render one only if the person asked about it.
   **If it carries a `variantChoice` whose `message` says to ask** (several
   previews matched and the host showed no chooser), the person picks, not
   you: reply with the rendered match and every entry in `choices` as a
   numbered list, ask which one they meant, and stop. Don't pick one or
   shorten the list to "other variants are available". A grid result or a
   declined choice needs no question.
2. **Look only when you need to.** Read `pngPath` with your file reader
   before you describe or judge the UI; that is what the person sees. Skip the
   read when `changed` or `sha256` already answers the question, such as
   "did my edit land?". Describe only what you saw. If you can't view images
   here, say so plainly.
3. **Reply** briefly, with `pngPath` so the person can open the same image.
   Don't write "the image above": in a terminal or print-mode harness the
   person doesn't see images your tools return. Point at `pngPath` instead.

**Library components come from the catalog.** When the person names a
library component (Material 3, Wear M3 `EdgeButton`, …) rather than one of
their own previews, use the hosted catalog (`compose-catalogs`):
`catalog_list_previews`, then read the published snapshot with
`resources/read`. Request `live` access only to change knobs with
`catalog_render_preview`. **Never** add preview files to the person's project
to show a library component unless they ask for one. See
[catalog-mcp.md](./references/catalog-mcp.md#resourcesread-before-catalog_render_preview).

**Sweeps use hashes.** For more than one render (variants, devices, font
scales, locales, a before/after check), pass `observe=hash` or use
`render_matrix` with `contactSheet: false`, which returns per-cell hashes
only. Fetch pixels only for the final screen or the cells whose hash moved,
or that you must judge by eye: one `render_preview` per such cell (its
`overrides` or `uri`, `inline=false`) and one read of its `pngPath`.

**Design guidelines review.** When asked to review a preview or catalog design
against Android design guidance, read
[design-guidelines.md](./references/design-guidelines.md). It covers keyless
agent review, published results and the CLI's `compose-preview review` loop,
including explicit surface selection, required pictures and incomplete
coverage. It is in the default
skill bundle; the optional PR-review bundle is not required.

**Hand multi-render reviews to `design-reviewer`.** If a `design-reviewer`
subagent is available (the compose-agent-plugins plugins ship one), delegate
accessibility, font-scale, round-device and other matrix checks to it so the
images stay out of your context, and relay its verdict and paths. Give it the
subject, home/revision, catalog rules and requested coverage. Without one, run
the same checklist yourself and report that delegation was unavailable.
For a routine hash sweep, keep `contactSheet: false`. A requested visual
guidelines comparison needs pixels: inspect its required frames even in your
own context when no reviewer exists. Prefer only the relevant individual
images or a bounded comparison sheet, and never claim visual coverage from
hashes alone.

**After a source edit**, call `render_preview` again. `notify_file_changed` is
optional. **If the result says it is stale**, make exactly one more call with
`force: {"reason": "<why>"}`. **Never** run `./gradlew`, `clean`, or delete
`build/` dirs to chase a render; if a forced render is still wrong, read
[mcp.md § Troubleshooting](./references/mcp.md#troubleshooting-first--when-not-to-act)
(start with `compose-preview mcp doctor`).

**Details on request.** Add `details: ["a11y", "layout"]` only when the
person asks about accessibility or layout. `observe=png` returns inline pixels
for clients that can't read files.

**No MCP tool?** Use the CLI: `compose-preview show --json --filter <Name>`,
then read the entry's `pngPath`. Stale: `--force=<reason>`, once. See
[cli.md](./references/cli.md). On either path, only output from the render
tools is a render: never a hand-built HTML, CSS or SVG mock. Report a failed
render with its error.

**Not previewable** (takes a ViewModel or injected service)? Propose extracting
a stateless inner composable and preview that
([state-hoisting.md](./references/state-hoisting.md)).

## Install / update (only if missing)

Check with `compose-preview --version`. If it's missing, run this skill's stub,
`bash <this skill's dir>/scripts/compose-preview --version`: its first run
installs the CLI and puts it on `PATH`. Every other route, updating, and the
Gradle plugin are in [setup.md](./references/setup.md); MCP wiring (the local
server and the one hosted URL) is in [mcp.md](./references/mcp.md).

## Working with platform skills

An official platform skill, such as Android's
[Wear Compose Material 3 skill](https://developer.android.com/agents/skills/wear/wear-compose-m3/skill),
owns API, dependency and migration choices. This skill only renders and
verifies:

- **Defer.** Follow the platform skill for which component, API or version to
  use. Don't treat this skill's references as a second API guide.
- **Changes are expected.** During a migration a changed hash or image is
  information, not a regression. Only a render failure or a new accessibility
  error blocks. Don't restore old screenshots or tune the UI to match them.
- **Mind the catalog version.** A hosted catalog renders one fixed library
  version, which may differ from the project's `libs.versions.toml`. See
  [catalog-mcp.md § Choosing a component](./references/catalog-mcp.md#choosing-a-component-with-a-platform-skill).

**Migration workflow.** Before editing, `find_previews_for_file` for each file
and record a baseline with `render_preview observe=hash`. Make the platform
skill's edits, re-render, and report failures and new accessibility errors
(`get_preview_data kind=a11y/atf`) as blockers. Show a before/after for one to
three key screens, and check a small round device and the largest font scale
on Wear. Details:
[wear-ui.md § Verification workflow](./references/wear-ui.md#verification-workflow).

## Reference index

Read only what the task needs.

| Topic | Read |
|---|---|
| Install, update, which skills, apply the Gradle plugin, zero-code init script | [setup.md](./references/setup.md) |
| CLI commands, `--filter`/`--id`/`--force`, `counts` buckets, render filenames, SVG output, Gradle tasks, `build-brief` for non-preview builds | [cli.md](./references/cli.md) |
| **Which MCP server** (local vs hosted `https://preview.coo.ee/mcp`); local server setup, tools, history, multi-workspace, **troubleshooting** | [mcp.md](./references/mcp.md) |
| Interaction loop: semantic refs, `observe` modes, `diff_semantics`, crop, `render_matrix` (variants/matrix), record → test, failure `kind`s | [agent-loop.md](./references/agent-loop.md) |
| Accessibility (ATF, `compose-preview a11y`) | [a11y.md](./references/a11y.md) |
| Per-render data (a11y, layout, recomposition, SVG) | [data-products.md](./references/data-products.md) |
| Multi-preview, GIFs, `@SettledPreview`, scrolling captures | [capture-modes.md](./references/capture-modes.md) |
| Wear Compose UI / Wear Tiles | [wear-ui.md](./references/wear-ui.md), [wear-tiles.md](./references/wear-tiles.md) |
| CMP `:shared` modules | [cmp-shared.md](./references/cmp-shared.md) |
| Android XML drawables / icons | [resource-previews.md](./references/resource-previews.md) |
| Runtime permissions per render | [runtime-permissions.md](./references/runtime-permissions.md) |
| Editable override knobs | [override-knobs.md](./references/override-knobs.md) |
| Display filters | [display-filters.md](./references/display-filters.md) |
| Remote Compose, `compose-preview rc` | [remote-compose.md](./references/remote-compose.md) |
| Hosted catalog MCP tools and grant flow (`serve`, no checkout) | [catalog-mcp.md](./references/catalog-mcp.md) |
| Gated server access (`compose-preview auth request`) | [server-access.md](./references/server-access.md) |
| Agent allowlists, staging PNGs | [permissions.md](./references/permissions.md) |
| Cloud sandboxes | [agent-cloud.md](./references/agent-cloud.md) |
| VS Code extension (humans) | [vscode.md](./references/vscode.md) |

**CI and PR review** live in opt-in sibling skills:
[compose-preview-ci](../compose-preview-ci/SKILL.md) (baselines, PR-comment
Actions) and [compose-preview-review](../compose-preview-review/SKILL.md)
(base vs. head render and diff). To add one, see
[setup.md § Which skills](./references/setup.md#which-skills).
