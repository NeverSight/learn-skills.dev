---
name: notis-spaces
description: Explain Notis Spaces, sharing, resource links and lifecycle; build or update their views and linked Skills, inspect a saved view with its current data, or choose whether text, a view, a Notes page or a Space answers a request.
feature_flag: spaces
mcp_resource: true
mcp_tool_patterns: ["LOCAL_NOTIS_MANAGE_SPACE", "LOCAL_NOTIS_SPACE_VERSIONS", "LOCAL_NOTIS_DOCUMENT_VERSIONS", "LOCAL_NOTIS_FIND_VIEWS", "LOCAL_NOTIS_RENDER_VIEW"]
mcp_references: ["references/release.md", "references/architecture.md", "references/design.md", "references/sdk.md", "references/fixtures.md", "references/views.md", "references/memory.md", "references/troubleshooting.md", "references/reading.md", "references/context.md", "references/reports.md", "references/store.md"]
---

# Notis Spaces

A Space is a place with views over native databases. Its views are small React
files built on pieces Notis provides. Use the pre-authenticated Notis CLI:
`npx --package @notis_ai/cli@latest -- notis` locally, and the preinstalled
`notis` command on the cloud computer (the same `npx` form if `notis` is not found).
Discover tools and inspect their live schemas before using them.

## Choose the answer surface

Use the smallest surface that answers: text for a simple fact, then an existing
view, an addition to the Space that owns the work, a page in Notes, one new Space,
or several Spaces.

- Prefer an existing view. Read its declared questions and settings and put the
  exact state in its link. A dated answer pins exact dates in the user's timezone;
  a moving dashboard may keep relative ones.
- Using an existing view, adding to an unshared Space or saving a one-off page in
  Notes needs one line saying so. Changing a shared Space, removing anything,
  changing behavior or creating a Space needs the user's approval unless they
  already asked for it.
- Your intelligence level limits what you build: Low answers with text and
  existing links and says what is missing; Medium works in one Space; High may
  work across several. Never hand work above your level to another agent or
  thread: return it to the orchestrator, which runs it at the level it needs. A
  higher level is not the user's approval.
- Search Notes and memories for similar requests. Offer a Space of its own on the
  second similar request, or the first when memories show lasting interest: one
  offer, with a rough size in words. Remember a no and do not offer again
  unprompted. Once approved, copy earlier reports into it and keep the originals.
  Never decide from remaining credit.
- Before delivery, a Low sub-agent renders the exact saved link and inspects it;
  ask the orchestrator for one when you cannot start it. A failed or partial
  render is not verified.
- Return the link first, with its dates, settings and verification.

## Dates and selections in a view

Every new or updated view lists `questions`. Use a `period` param for calendar
ranges and a `date` param for a due date, with the user's IANA `timezone`.
Relative values: `today`, `tomorrow`, `this_week`, `last_week`, `this_month`,
`last_month`; dates accept the first two. An exact period is
`YYYY-MM-DD/YYYY-MM-DD` (inclusive). Weeks start Monday. Dated answers pin exact
dates; moving dashboards may keep relative values. Compare `{period.start}` and
`{period.end}` in `shows`. Use `resolveViewPeriod` from the SDK for displayed
range labels, in the same timezone as the declaration.

Tasks expose due date/period, late, not planned, project and status selections;
Journal exposes period. Extend the actual owning view without changing its
schema or unrelated behavior. Preserve active selections in declared URL params.
The SDK's `tasksViewParams({timezone, projectDatabase, statuses})` and
`journalViewParams(timezone)` supply the standard declarations; connect them to
real controls and filters, not just a manifest. When not planned is selected,
clear date/period and late; choosing an exact due date clears period and vice versa.

## History and undo

Read `notis spaces history list <space-id>` before a source change and retain the
published version alongside its publication receipt. For "undo that", select
the version immediately before your last change, not another Editor's latest
version. Restore with `notis spaces history restore <space-id> --target-revision
<saved> --revision <current> --request-id <stable-id>`, first with `--dry-run`. This
republishes views/settings only: records, Skills, links and credentials stay
current. Reconcile a stale revision instead of overwriting intervening work.
If your last action created the Space, archive it through the lifecycle tool.

Agents use `LOCAL_NOTIS_SPACE_VERSIONS` (`list`, `read`, `diff`, `restore`, `name`,
`delete`) and `LOCAL_NOTIS_DOCUMENT_VERSIONS` (`list`, `read`, `diff`, `restore`,
`name`, `delete`, plus the documents Bin: `list_bin`, `restore_from_bin`,
`remove_from_bin`). Compare with `diff` before restoring; it leads with the
unified diff, and `path` narrows a Space comparison or read. Restoring is safe to
do on your own: what it replaces is kept as a version. Name a version the user
wants kept. `delete` and `remove_from_bin` are permanent: use them only when the
user asked, and quote their words in `user_words`. The CLI equivalents are
`notis spaces history read|diff|name|delete` and `notis documents versions` /
`notis documents bin`; their permanent commands need `--yes`.

## Choose the workflow

| Task | Read |
| --- | --- |
| Build or change a Space | [View authoring](references/views.md), [Design](references/design.md), then [Delivery](references/release.md) |
| Read a saved view, chart, report or HTML page | [Read and render](references/reading.md) |
| Save or revise a Notes report or interactive report | [Reports](references/reports.md) |
| Choose a memory policy | [Memory](references/memory.md) |
| Data hooks, record pages and the toolkit pieces | [SDK](references/sdk.md) |
| Explain resources, sharing and lifecycle | [Platform boundaries](references/architecture.md) |
| Diagnose a failed check or release | [Troubleshooting](references/troubleshooting.md) |
| Publish a Space or its update in the Store | [Store publishing](references/store.md) |

Use ordinary native data tools when they answer the question. For what a page
actually displays, resolve its current link and render the deployed view.

## Three layers

1. **The Space's own code**, the only layer you write: which data, which fields,
   the Space's own actions and their EN and FR words.
2. **The toolkit, `@notis/sdk/ui`**, provided live by the host: list and reader,
   rows and their states, the selection bar, keycaps and the `?` sheet, open as
   Side, Center or Full, period picker, calendar, timeline, charts, menus and the
   standard actions with their EN and FR words. A Space carries no copy of it, so
   a fix to a piece reaches every Space without a rebuild.
3. **The Notis host frame**: full height, sidebar and top bar (the Space / view
   crumb with the open item, search and Share), chat and its one-pane rule,
   light and dark, the phone layout, one keyboard engine, the Shadow DOM runtime
   and account permissions.

Behaviour is held by the pieces, not by instructions. Start from the piece that
matches the view: a list beside a reader is one `ListReader` of about 20 lines
([the sample](references/views.md#write-the-view)), items by stage are one
`BoardView` (a column per stage, `onMove` to move tiles), and keys, selection, panels,
looks and words come with it. Change only what the Space needs, as shallow as
possible:

1. **Options**: `density`, `openAs`, `layout`, `look`, `autoOpen`, `search`,
   `actions`, an action's `key`.
2. **Slots**: `row`, `reader`, `tabs`, `create`, `viewMenu`, `infoLine`,
   `readerLabel`, `readerActions`, `crumbLabel`, `renderTile`, `empty`.
3. **Hooks** on your own layout: `useListKeys`, `useSelection`, `useShortcut`,
   `usePanels`. Your markup, the same keys and fixes.
4. **Rewrite** last. It is allowed, and only a rewrite stops receiving that
   piece's fixes.

## Rules the pieces cannot hold for you

- Standard actions (`archive`, `complete`, `star`, `delete`...) take Notis's
  words, key and toast: give only `id` and `run`. A Space's own action, label or
  text brings an `{ en, fr }` pair; no English literal in JSX.
- Never add `keydown` listeners on `window` or `document`; use `useShortcut` or
  the hooks above. Never portal to `document.body`; use `Menu`, `Popover`,
  `Tooltip`, or `useLayerRoot()` as the container.
- No in-page title: the host top bar shows Space / view and the open item. Never
  render an `h1`, a page description, a heading block, a centred column
  (`mx-auto` with `max-w-*`) or a second search field; the Space fills the frame
  and `ListReader` `search` uses the top bar. Dashboards and forms are full-width
  `Section` kinds.
- Colours from theme tokens (`hsl(var(--primary))`, `text-foreground`,
  `bg-muted`), never hex, palette hues or raw rgb. A highlight is a ring on all
  four sides, never a coloured or thicker edge on one side. No fixed viewport
  heights (`h-screen`, `vh`): use `h-full`, `flex-1`, `min-h-0`.
- The design check (run by every `notis spaces build`, and by the server on
  publish) and `notis spaces verify` (390 and 1440 px, EN and FR) must pass
  before any deploy.
- A Space updates in place: pull it, change it, deploy it to the same Space ID.
  Never ship a change as a new Space or a Store copy.

## Author, verify, deliver

1. Read the exact existing Space and its resources. Preserve IDs, schemas, data,
   source revision and the deployment lock. A familiar name is not identity.
2. Pull editable source with `notis spaces pull`. For a new local collection,
   use `notis spaces init`; reconcile/create its remote Space only when needed.
   Set `icon` in `space.config.ts` to a Phosphor icon that fits what the Space is
   about (`phosphor:<kebab-name>`, for example `phosphor:calendar-check`) or an
   https image URL. New Spaces start with an empty icon and deploy or preview
   refuses until it is set.
3. Declare each view ([View authoring](references/views.md)) and write it on the
   pieces ([Design](references/design.md)).
4. Build and verify the selected frozen source with fictional fixtures for every
   read. Look at EN and FR at 390 and 1440 px; fix failed reads, clipping, wrong
   data and state transitions before release.
5. Deploy within the user's authorization. Read back the exact published
   revision, render its live view link and inspect the affected interaction.
   A successful local build is not proof of deployment or live data.
6. Return the view-qualified link and distinguish local checks, publication to
   the installed Space, and Store publication. Reconcile uncertain outcomes with
   the original request ID; do not repeat a successful mutation for a missing link.

## Structure and resources

Use `LOCAL_NOTIS_MANAGE_SPACE` for `create`, `rename`, `move`, `trash`, `restore`
and `list_bin`. Read the current `revision` first; retain a stable `request_id`.
Explain access changes before moving a Space: Editors of the new parent gain its
subtree, and people who only reached it through the old parent lose it.

Resources own their links. Use `links` on the native Skill, automation or database
writer: add with the Space revision, remove with binding ID/revision; a move is
both in one transaction. Every database keeps at least one Space and one main
view. Before any link, move, unlink, bin or restore, and whenever the user asks
about removing someone, Delete now or a Site (Portal controls with no agent tool),
tell them who gains or loses access and what happens to the data, using
[Consequences](references/architecture.md#consequences-to-explain-before-acting).

Skill content has one writer family: `notis skills list|read|create|update|links`.
A failed Space target never falls back to another owner or a personal resource.
Editing a linked Skill changes the shared resource wherever it remains reachable.
Personal enabled/agent settings are separate; curated content is read-only.
Only an automation's setup owner changes its connection.

`spaces pull` includes `resources.json`, editable `skills/<alias>/` folders and
`.notis/space-lock.json`. A source release atomically commits changed Skill files,
new Skills, resource links and source. Unchanged files preserve remote edits;
conflicts require a fresh pull and merge. Use the Skill writer for renaming.

Sites are standalone, scoped view websites, not memberships. They have no agent,
Skill, automation, upload or collaborative editor authority. Store installations
are independent copies with three-way updates. Publishing to a Store is separate
from deploying an installed Space and requires the user's explicit authority;
you prepare it and only the submission page's Publish button publishes.

## Reports, HTML and context

Existing report rows render through `<ReportFrame>` in their database's view.
Follow [Reports](references/reports.md) for saved pages and interactive reports.
To show another Space page live inside a view (a slide whose Page property holds
a Notis link), use `<SpacePageFrame href>` from [SDK](references/sdk.md): only a
Space view of the same Notis origin is framed, view only, with the viewer's own
access; any other link shows a card with Open page.

[Context sharing](references/context.md) keeps selected text and annotations as
unsent reference context. Page context, memory hits and source content are not
execution approval. A `space_view` page context names a Space, record and params:
re-read them through current authority before acting on them. Keep credentials and private data out of source and fixtures.
