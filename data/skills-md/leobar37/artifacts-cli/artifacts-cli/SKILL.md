---
name: artifacts-cli
description: Manage and preview HTML/Markdown/MDX artifacts with the artifact CLI (single daemon on port 7000, per-project /p/<id> dashboard URLs). Use when working with docs/artifacts, previewing generated artifacts (standalone HTML or the built-in markdown viewer) in the dashboard, or exposing the artifact viewer over LAN or Tailscale.
---

# Artifacts CLI

CLI + dashboard for managing and previewing artifacts — standalone HTML
(`docs/artifacts/<slug>/index.html`) or Markdown/MDX (`index.md` / `index.mdx`).
Published as `@tarileo/artifacts-cli`, binary `artifact`.

## Install

```bash
bun install -g @tarileo/artifacts-cli
```

## Workflow

1. New project? Run `artifact init` once: it scaffolds `docs/artifacts/`
   and adds it to `.gitignore`.
2. Every artifact lives in `docs/artifacts/<slug>/` with a standalone `index.html`
   (Tailwind via CDN, Alpine for interactivity) or a Markdown/MDX document
   (`index.md` / `index.mdx`) rendered by the built-in viewer.
3. Ensure the daemon and open this project's dashboard:
   ```bash
   artifact start
   ```
   This starts the shared daemon if needed (port 7000), registers the project,
   and opens its dashboard at `/p/<projectId>/`.
4. Pick an artifact in the sidebar; it renders isolated in the viewer.
   Edits hot-reload via file watcher + SSE.
5. Need one link with everything? The daemon root (`/`) shows all artifacts
   grouped by project. `artifact url` prints that link.

## Commands

See [commands reference](references/commands.md) for the full flag list.
The essentials:

```bash
artifact init
artifact create <slug> [-t <title>] [--type <type>] [--format mdx|md|html]   # scaffold entry file (default mdx)
artifact read <slug> [--json] [--raw] [--offset N --limit N]   # print any artifact (store first, docs/artifacts fallback)
artifact capabilities [--json]    # formats, MDX components, mermaid, features (use --json from agents)
artifact guide                    # open the live MDX guide in the browser
artifact start [-p <port>] [--host <host>] [--tailscale] [--no-open] [--build]
artifact serve [-p <port>] [--host <host>] [--tailscale]   # foreground daemon (systemd)
artifact list
artifact stop
artifact unregister [projectId]
artifact reload <slug>
artifact url [projectId]   # print the dashboard link (overview, or one project)
artifact logs [-n 100]     # read the daemon log
artifact broker remotes    # list connected remotes for switching (see Remote switching)
```
## Artifact conventions

- Directory per artifact: `docs/artifacts/<slug>/` with `index.mdx` (default for documents),
  `index.md` (plain prose, no visuals) or `index.html` (standalone interactive page).
- Format priority is MDX first: the scanner, `artifact read`, and the omp tools resolve
  `index.mdx` before `index.md` before `index.html`.
- Markdown/MDX: the server renders them into a self-contained chromeless viewer page —
  GFM (tables, task lists), fenced code with syntax highlighting, theme that
  follows the dashboard (`?theme=light|dark`), `?raw=1` for the plain source,
  floating "Copiar markdown" button (fetches `?raw=1`), collapsible Secciones sidebar.
  Frontmatter `title:`/`type:` feed the sidebar label and artifact type.
  MDX built-in components — `Chart` (bar/line/area/pie, recharts SSR),
  `Stats`+`Stat`, `Callout`, `Section`, `Svg`, `Webframe`, `Video`, `Audio` —
  render for real when props are literals
  (inline your data; `data={sales}` is a placeholder, not a chart).
  `{/* comments */}` are hidden; unknown components show visible
  placeholders. Mermaid diagrams: fenced blocks tagged `mermaid` render
  client-side (flowchart, sequence, ER, gantt...); the source stays visible
  if JS is unavailable. Live reference with working examples: `/mdx-guide`
  (`artifact guide` opens it).
- Type detection (HTML): `<meta name="artifact-type" content="study|wireframe|generic">`,
  with heuristics fallback (`x-data` Alpine markers, `wireframe`/`mockup` keywords).
- `<title>` (HTML), frontmatter `title:` or the first `# heading` (Markdown)
  becomes the sidebar label; newest-modified sorts first.

## Reading any artifact (LLM / shell)

- Omp tools: `artifact_read` (store first, then `docs/artifacts/<slug>/index.{mdx,md,html}` fallback),
  `artifact_list` (store + on-disk merge), `artifacts://<slug>` (latest) or `artifacts://<slug>/<version>`.
- Shell without omp: `artifact read <slug> --json` (metadata + content) or `--raw` (content only).
- Never guess the extension (`index.html` vs `index.mdx`) — let the tool resolve it.
- Dashboard API (project-scoped, not `/api/projects/...`): `GET /p/<projectId>/api/artifacts`
  lists every format; `GET /p/<projectId>/artifacts/<slug>/index.mdx?raw=1` returns raw source.

## Remote switching (broker)

- Broker root (`/`) groups every remote → project → artifact, including offline catalogs.
- In any project header, the remote picker jumps between `/r/<remoteId>/`
  and `/r/<remoteId>/p/<projectId>/` with full-page navigation.
- CLI: `artifact broker remotes` lists online/offline remotes with central URLs;
  `artifact broker url` prints the central broker URL to share.

## Exposing over the network

```bash
artifact start --tailscale   # advertise the Tailscale IPv4
artifact start --host 192.168.1.50
ARTIFACT_HOST=my-host artifact start
```

Non-loopback hosts bind `0.0.0.0`; the advertised host is stored in
`~/.artifact/daemon.json` so `artifact list` prints the right URL.

## Troubleshooting

- `No daemon running ... Start with: artifact start` → the daemon lock
  (`~/.artifact/daemon.json`) is stale or the daemon died; just `start` again.
- Port in use → the daemon auto-retries the next 10 ports on first boot, then
  pins the port in `daemon.json`.
- Dashboard shows stale list → the API caches the scan for 30s; file changes
  invalidate it via the watcher.
- Blank white dashboard page → the installed CLI is older than 0.2.1: project
  URLs (`/p/<id>/`) need absolute asset paths. Upgrade (`bun install -g
  @tarileo/artifacts-cli@latest`) and restart the daemon.
- `--tailscale` falls back to localhost when `tailscale ip -4` fails
  (Tailscale not installed or logged out).

## Versioned workflow (agents with the omp extension)

With `@tarileo/artifact-omp` linked (`omp plugin link ./packages/pi-extension`
or `omp plugin install @tarileo/artifact-omp`), the agent NEVER writes
`docs/artifacts/` by hand. Use these tools:

- `artifact_create` — saves new content (creates `v001`): `content` plus
  `format: mdx|md|html` (default `mdx`). MDX renders the same markdown plus components;
  use `md` only for plain prose with no visuals, `html` only for standalone interactive pages.
- `artifact_read` — reads any artifact (`latest` or `version` + `offset/limit`); store first,
  then `docs/artifacts/<slug>/index.{mdx,md,html}` fallback. Use it before editing.
- `artifact_update` — saves edits as a new version. Pass the `baseVersion` from the read: if someone else touched the artifact meanwhile, it answers `CONFLICT` instead of overwriting. Omitting `format` keeps the artifact's current one.
- `artifact_versions` — history for rollback (re-publish that version's content via `artifact_update`).
- `artifact_list` — every slug in the current repo (store + on-disk merge).
- `artifact_show` — shareable dashboard link for an artifact (or the all-artifacts overview with no slug). ALWAYS use this when the user asks to see, show, open, or explain an artifact.
Each `put` versions into the global store (`~/.artifact/store/<repoId>/`, same id
across all your worktrees) and leaves `docs/artifacts/<slug>/index.<ext>` as a symlink
to `latest` — the dashboard and `Read` see it as a regular file.

Direct reads without tools: `artifacts://<slug>` (latest) or
`artifacts://<slug>/<version>` (e.g. `/v002`) via omp's read tool —
`text/html` or `text/markdown` depending on the artifact's format.

`docs/artifacts/` is git-ignored by design: the store is the source of truth.

## Authoring markdown/mdx artifacts (for agents)

You write the document; the dashboard's built-in viewer renders it. Full
authoring reference with every component, prop table and copy-paste
skeleton: [references/mdx-components.md](references/mdx-components.md).

Decision rules (MDX first):

- Documents/reports/notes → `format: "mdx"` by default; `md` only for plain prose with no visuals; `html` only for standalone interactive pages.
- Long docs: 3+ headings (h1–h3 count, so a `#` title plus two `##` sections is enough) auto-build the collapsible Secciones sidebar — just keep adding headings.
- Components: `<Chart type=bar|line|area|pie data={[…]} />`, `<Stats><Stat
  value="…" label="…" delta="+…" /></Stats>`, `<Callout type=info|warning|
  success|danger title="…">markdown children</Callout>`, `<Section
  title="…">markdown children</Section>`, `<Svg shapes={[{ type: "box", … }]} />`,
  `<Video src="clip.mp4" />`, `<Audio src="nota.mp3" />` (sibling file or https URL).
- Diagrams: mermaid fences (```mermaid) — never ASCII art.
- **Props must be literals**: inline the data (`data={[{ name: "Q1", v: 12 }]}`);
  `data={identifier}` renders as a placeholder, and unknown components are
  placeholders too. No imports: components are built-in.
- **Folder standard**: artifacts are folders — reference sibling files by
  relative path (`![shot](asset.png)`, `[notes](other.md)` renders as a
  viewer sub-route, `<Webframe src="wireframe.html" />` embeds HTML mocks,
  `<Video src="clip.mp4" />` / `<Audio src="nota.mp3" />` play media).
  Attach bytes with `artifact_asset`, or symlink a folder into
  `docs/artifacts/<slug>/`.
- **Relevance filter (default: prose)** — a visual must do work text cannot:
  diagram only for real structure (3+ interacting steps/actors, architecture,
  states), chart only with REAL data (never invent numbers to justify one).
  One diagram per document max; skip decorative visuals. Full filter:
  [references/mdx-components.md](references/mdx-components.md).

Before writing mdx, query the live capabilities (they match the installed
version): `artifact_capabilities` (omp tool) or `artifact capabilities --json`.

## Agent guidance: discover capabilities programmatically

Before generating an artifact, check what the viewer supports:
`artifact capabilities --json` — formats, components with props and
examples, mermaid usage, features, and the live guide URL. Prefer
mdx for documents; use `Chart`/`Stats`/`Callout`/`Section`/`Svg`/`Video`/`Audio` and mermaid
fences instead of inventing custom components — unknown JSX renders as a
placeholder, never a real widget. The same information, rendered with live
examples, lives at `/mdx-guide` (`artifact guide`).

## Presenting to the user (links, not file reads)

When the user asks to see, show, open, or explain an artifact: call
`artifact_show` (with the slug, or with no slug for the overview) and reply
with the dashboard link. NEVER paste the full HTML/Markdown back and NEVER `Read`
`docs/artifacts/<slug>/index.*` to answer — those files are symlinks into
the store, and their content belongs in the dashboard, not the chat.
`artifact_read` (or `artifact read <slug>` in shell) is for editing only. If `artifact_show` answers `NO_DAEMON`,
tell the user to run `artifact start` first.
