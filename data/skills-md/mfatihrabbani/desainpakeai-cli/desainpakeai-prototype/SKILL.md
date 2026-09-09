---
name: desainpakeai-prototype
description: Build, inspect, edit, verify, and export dependency-free DesainPakeAI prototype workspaces with the dpai CLI. Use for prototype pages, layouts, components, design tokens, DESIGN.md guidance, visual-review retrieval, canvas working state, or single-HTML export. Do not use for the TanStack host UI or legacy prototype templates.
---

# DesainPakeAI Prototype

Use the globally installed `dpai` CLI. Do not initialize or call a DesainPakeAI
MCP server, and do not use `npx` for each workspace operation.

When this skill is already available, do not run `npx skills add`, `skills
check`, or `skills update` during ordinary tasks. Install the skill only during
initial setup, and check or update it only when the user explicitly requests a
skill synchronization.

## Start a continuous task

Reuse confirmed setup across follow-up edits while the session, target project,
and connection stay unchanged.

1. Run `<prefix> --version` first. If the command is unavailable, run
   `npm install --global desainpakeai-cli@latest`, then check the version again.
   Do not reinstall or update during every ordinary task.
2. Use that binary for the rest of the continuous task.
3. Run `<prefix> auth status --pretty` once. If authentication is missing, ask
   the user to run `<prefix> auth login --api-url <url> --api-key <dpai_key>`,
   then run `<prefix> auth status --pretty` once more to verify the login.
4. Run `<prefix> project current --pretty` and confirm it is the target project.
5. Run `<prefix> context --pretty` and retain its latest revision.
6. Before the first workspace source mutation, run
   `<prefix> guide get --topic workspace-authoring --raw` only when that guide
   is not already retained for the same session, project, and runtime. Reuse it
   across follow-up tasks. Refetch only when that context is lost or changes.
   Skip this step when the task remains read-only.

Treat a successful authenticated CLI command as the connection signal. Creating
or copying an API key alone does not prove that the coding agent is connected.
Do not initialize, call, or wait for an MCP handshake endpoint.

The CLI `workspace-authoring` guide is the source of truth for the minimum
single-HTML authoring contract. This skill only routes when to fetch it; do not
copy or infer a competing CSS, font, component, or JavaScript contract here.
Use `--workspace <path>` only when the user explicitly requests filesystem-local
work. Carry forward the revision returned by every successful mutation.

## Guide catalog and timing

`workspace-authoring` is required once before source mutation and is retained
across follow-up tasks for the same session, project, and runtime. All other
guides are optional task-specific references. Pull one immediately before the
first decision it covers, reuse it for that continuous task, and fetch another
only when a new unresolved risk appears. Never preload all optional guides.

- `workspace-authoring` - required before workspace source mutation.
- `design-quality` - substantive visual design decisions.
- `accessibility` - keyboard, focus, forms, ARIA, or zoom.
- `layout-responsive` - responsive layout, overflow, RTL, or long content.
- `typography` - typography, wrapping, truncation, or bidirectional text.
- `color-system` - tokens, themes, status colors, or contrast.
- `product-writing` - labels, errors, empty states, or localization.
- `ui-polish-motion` - surfaces, icons, motion, or visual states.
- `prototype-interactions` - modals, selects, filters, forms, or stateful UI.
- `evidence-and-reference` - external pages, screenshots, or supplied references.
- `image-to-prototype` - reconstructing a supplied UI image or screenshot.
- `interface-review` - only for a user-requested interface review.
- `component-stress-test` - only for a user-requested stress test.
- `variant-exploration` - only for user-requested design variants.
- `prototype-to-codebase` - only for a user-requested codebase handoff.

Fetch optional guides with `<prefix> guide get --topic <topic> --raw` only when
their trigger matches. Fetch `design-quality` before substantive visual design,
but skip it for non-visual maintenance, canvas positioning, export-only work,
manifest inspection, and narrow fixes. Do not fetch user-gated guides based on
inference.

## Operational invariants

- Before visual UI work, run `<prefix> design context --pretty` and
  `<prefix> token list`. Treat DESIGN.md guidance, registered components, and
  runtime tokens as constraints when present. Keep exploratory values
  page-local when they are absent.
- Reuse a registered component when available. Create or register a component
  only when the user explicitly requests it or asks for reusable extraction;
  otherwise keep the implementation page-owned.
- Work on one page at a time. A page-create command only creates its skeleton
  and Canvas frame. Add one visual or workflow group per initial file edit and
  never run page mutations in parallel.
- Create or change persistent tokens only after the user selects a direction or
  explicitly asks to save them.
- Preserve stable `data-node-id`, `data-component`, `data-part`, `data-action`,
  bridge attributes, and public props. Prefer an existing token over a
  hardcoded reusable value.
- Use `<iconify-icon icon="collection:name">` directly without adding a loader
  or wrapper. Give icon-only controls an `aria-label` and mark decorative icons
  `aria-hidden="true"`.
- After completing a page, run `<prefix> preview verify --page <page-id>`, fix
  applicable diagnostics, verify again if needed, perform the rendered checks
  required by `workspace-authoring`, then run `<prefix> work finish --page
  <page-id>`.

## Prefer native commands

Do not handwrite inline JSON. Use native flags for normal work; the CLI builds
and validates the operation payload and reads the latest revision automatically.
For `page create`, pass routes without a leading slash, such as
`--route activity`; the CLI adds the slash. This form avoids Git Bash/MSYS path
conversion on Windows.

```text
<prefix> design context --detail compact --section Overview,Components --pretty
<prefix> token list --type color,spacing --format css
<prefix> token create --name --color-accent --type color --value "#635bff"
<prefix> token set --name --color-accent --value "#574ee8"
<prefix> token delete --name --color-legacy
<prefix> design set-section --heading Overview --content-file overview.md
<prefix> component create --id status-pill --tag x-status-pill --prop tone="Visual tone" --default tone=neutral
<prefix> review get --review <uuid> --output review.png
<prefix> work status --pretty
<prefix> preview verify --page <page-id>
<prefix> work finish --page <page-id>
```

For long HTML, CSS, JavaScript, or Markdown, pipe raw text through stdin. Use a
short, shell-safe `--before`, `--after`, or `--replace` value only as the unique
anchor. For exact multiline replacement, pipe a standard unified diff into
`dpai file patch --path <path>`; one diff may contain several related hunks and
is applied atomically. This is the default agent workflow and does not require
creating temporary old/new files.

Use `--content-file`, `--replace-file`, or `--patch-file` only when the shell
cannot preserve the payload exactly, when the artifact is useful for debugging,
or when Windows PowerShell 5.1 may corrupt non-ASCII stdin. Keep those files
UTF-8.

When fallback files are necessary, resolve the Git repository root and place
them only in `<git-root>/.desainpakeai/tmp/<task-slug>/` with descriptive names.
Before writing the first file, ensure the root `.gitignore` contains the exact
root-relative entry `/.desainpakeai/tmp/`; append only that line when missing
and preserve the rest of the file. If the current directory is not in a Git
repository, use `<cwd>/.desainpakeai/tmp/<task-slug>/` and do not create a
`.gitignore` solely for it. Never put temporary inputs beside prototype source
files. Delete a fallback file as soon as the command consuming it succeeds. If
the command fails, keep it only while recovering, then delete it. Before
`work finish` or handoff, verify that the task-specific temporary directory no
longer exists; never leave task-only files behind after the work is complete.

## Show page progress section by section

For a new page, expose real Canvas progress with two sequential commands per
section. First insert only one visible section shell before
`<!-- agent:page-sections -->`. Give it the final semantic element, stable
`data-node-id`, outer inline layout or surface, enough block size to render, and
a unique nested `<!-- agent:<page>.<section>-content -->` anchor. Then insert
that section's content before its nested anchor and keep the anchor for future
partial edits.

Finish one section before creating the next, carry forward the revision from
every command, and never run page mutations in parallel. Each successful edit
is persisted and becomes a Canvas progress update. Run `preview verify` only
after the page is complete unless a mutation reports a problem.

Repeat list flags or pass comma-separated values. Use `--input @payload.json`
only for an atomic batch that mixes edit modes, an atomic multi-token batch,
component recipes, the complete omissions list, or low-level integration
debugging. Generate the file programmatically and never compose JSON inline in
the shell.

Run every DesainPakeAI operation through `<prefix>` and use command output for
verification, completion, revision conflicts, and recovery.
