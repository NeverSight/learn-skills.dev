---
name: quilium-builder
description: Load when building or restructuring a Quilium CMS site — architecture (page-types, content-types, ItemSets, global fields), YAML schemas, routes and detail pages, Liquid templates, porting an HTML prototype, images, the 404, the CLI loop (init, run, push, dictionary), and content from the shell (bulk imports, long fields edited as files). Triggers on "new Quilium site", "build this site", "design the architecture", "create a content type", "add a page type", "scaffold a template", "port this prototype", "detail page", "the links point to the wrong page", "images are missing", "the 404 doesn't work", "set up the project", "quilium init", "quilium push", "quilium content", "quilium item", "import this into the CMS", "the site doesn't render", "wysiwyg or repeat", "custom wysiwyg styles", "editor style palette". Load quilium-webmaster ALONGSIDE this skill — every build ends with a content phase (step 5). For content work on a site that already runs, quilium-webmaster alone is enough.
---

# Quilium builder

You build Quilium sites: the structure underneath them, the templates that render them, and the local loop
that lets you see your work before anyone else does.

This skill is a **guide, not a manual**. Quilium ships a live skill library through its MCP server, and that
library is the source of truth for every schema, field type and API shape. Your job is to know *what to load
and when*, not to remember what it says.

## The skills-first protocol — non-negotiable

Before any non-trivial CMS operation:

1. Call **`get-skills`** to get the live manifest. Cache it for the session.
2. Load the **smallest set** that covers the task — usually one skill, two when it really spans two areas.
   Never follow `related:` by reflex: load another skill only when a question comes up that the loaded ones
   don't answer. A skill already loaded in this conversation is still in it — don't reload it.
3. Load each with **`get-skill <slug>`**, in parallel when independent.
4. Read what this site actually has with the narrowest call — `get-site-settings` with the one `type` you
   need (not `all`). Never infer structure from another project.
5. Then act.

Everything you read stays in the conversation until it ends, and a conversation has a size limit: a skill
or a settings dump loaded "just in case" costs the user turns. `practices-ops-mcp-batching` is worth
loading for anything over a handful of calls.

When a site is in scope, the manifest may open with a group `site` — the procedures the site's own team wrote
in the CMS (slugs `site:…`). Rare on a site you are building, decisive on one you are restructuring: a
procedure describes how the site works today, read it before changing the structure it relies on.

### The library is smaller than you expect, and that is not an error

**What `get-skills` returns is the whole of what you can load.** The library is gated by profile and by site,
and the set you get may be a fraction of what exists — with whole areas absent: templates, routes, YAML
schema syntax, forms, pagination.

So: if a slug isn't in the manifest, it doesn't exist for you. `get-skill` will refuse it. Don't retry it,
don't work around it by inventing what it probably said, and above all **don't leave the gap unfilled and
improvise the implementation**. That last one is how a detail page ships with routing that returns 200 on
every URL and resolves none of them.

When a skill you wanted isn't there, the bundled references below cover the areas that are most often missing
and most expensive to get wrong. If neither has it, say so plainly and probe the engine (rule zero, in
`references/engine-liquid.md`) instead of guessing.

## The four primitives

A site is built from four things: **page-types** (a page's structure and its own fields), **content-types**
(reusable blocks dropped onto pages), **ItemSets** (managed collections), and **global-fields** (site-wide
singletons).

Choosing between them is the highest-leverage decision in the project and the most expensive one to get
wrong. It also already has a dedicated decision matrix, with a five-question flowchart and a worked list of
anti-patterns:

**Load `practices-conventions-architecture` before you commit to a shape**, along with anything the manifest
offers next to it. Not after. It will tell you things that contradict your instinct — that most pages need no
page-type of their own, that a list you were about to model as a `repeat` is one rich-text field, and that
almost nothing belongs in global fields.

Don't take a compressed version of that matrix from here or anywhere else. Read it live.

### Rich text is the option before the four

The first question the matrix asks isn't which primitive — it's whether the editor needs one at all. **Ask it
out loud, per block, before writing its schema**, and write the answer into your architecture note next to the
shape you chose. Skipping it is how a hero ends up with four rigid `text` fields.

**The test — is each item just standard HTML the editor could type?** A bullet list, a link list, a paragraph
followed by a button, numbered prose steps, short Q/A: **yes → one `wysiwyg` field. Stop.** Not a `repeat`, not
four `text` fields.

**When it doesn't apply**, and you keep the typed shape:

- The item is a **mini-record whose shape rich text cannot express** — icon + title + image + link, repeated.
  That's a `repeat`.
- The value **lands in an attribute, a URL, a slug, an anchor or a CSS class.** A `wysiwyg` wraps its output in
  `<p>`, which breaks attribute injection. Those stay `text`.
- The editor needs to **filter, search or reorder items individually** — that's a collection, and the matrix
  takes over.

The signature of getting it wrong: a `repeat` whose sub-fields are all `text` or `wysiwyg`. That's a `wysiwyg`
in disguise — collapse it.

What makes the "yes" branch hold in practice is the site-wide **style palette** — buttons, styled lists,
callouts, coloured spans, available to the editor from the toolbar. Without it, every visual variant the design
needs pushes you back into typed fields, and you get the rigid schema the matrix warns against. The palette is
what turns "the editor can type this" from a hope into a fact. So the second question is **when the palette
needs a new variant**: the answer is *whenever a block would otherwise be forked into typed fields for a
button, a styled list or a callout* — add the variant once, site-wide, and every editor on the site gains it.

**Load `reference-wysiwyg-config` before writing schemas, alongside
`practices-conventions-architecture`.** It carries the palette configuration and a starter pack. Two reasons
it belongs early rather than whenever rich text next comes up:

- **It changes the YAML you write.** Each variant the palette covers is a field you don't declare. Deciding it
  after the schemas exist means rewriting them.
- **The palette is site-wide settings, not per-type.** One decision for the whole site, and a settings write
  replaces its target wholesale — read, merge, write back complete.

Retrofitting this onto a site whose content is already authored is a migration: schema edits plus re-authoring
every block that was split across typed fields. Decide it in step 1.

## Building a new site

Five steps, in this order. The order encodes dependencies — see `references/process-new-site.md` for the
detail and the reasoning.

1. **Architecture** — decide the shape, write it down before writing YAML.
2. **CMS base** — ItemSets, content-types, page-types, global fields, then routes.
3. **Base layout** — one `layout.liquid` that renders, with header, footer and nav — and the 404, registered
   in the settings.
4. **Templates** — one per content-type and page-type.
5. **Media, then content** — uploads first, since content references them by uuid. In draft. With the CLI
   installed, bulk rows and long fields go through it (`references/cli-content.md`) — your call.

Templates come **before** content: you want to see a block render before you author fifty of them.

## Absolute rules

These aren't preferences. Each one, broken, produces a failure that looks like something else.

- **Templates are `.liquid`**, full path always (`elements/hero.liquid`, never `hero.liquid`). It is the only
  loadable extension: any other value in a `template:` is ENOENT → **500**, never a fallback. That covers mail
  bodies too (`sendmail`'s `config.template`). A value with no extension does resolve — `.liquid` is appended.
- **Every key you write in YAML is English `camelCase`.** Types, fields, tabsets, ItemSets, `select` option
  values, image versions, routes — the identifiers, all of them, whatever language the site or the client
  speaks. Only the editor-facing strings (`label:` and friends) follow the site's language. Keys are code: a
  template reaches them by dot access, so `titre-principal` or `libellé` stops being reachable as
  `page.custom.<field>` — a hyphen parses as a minus, an accent isn't a word character — and you're into
  bracket lookups, when it works at all. Mixed languages cost more slowly: `articles` next to `evenements`,
  and every template read after that is a guess.
- **YAML is block style, always.** Indented mappings, 2 spaces, one key per line — the way every example in
  the docs is written. Never flow/JSON-like mappings (`col1: { name: Horaires, width: 50 }`): the parser takes
  them, the webdesigner who maintains the file by hand does not. Form layout lives INSIDE a tabset:
  `tabsets.<tab>.fieldsets.<key>` with an optional `name` (the heading shown above the group — a fieldset
  without `name` is a bare column) and a `width` from 25/30/33/40/50/60/66/70/75/100; a field only carries
  `fieldset: <key>`. Group what is read together and name the groups that mean something (« Horaires »,
  « Lieu », « Publication ») — never after the single field they hold.
- **Never write a URL path or a page UUID in a template.** Both are CMS identifiers; a template that hardcodes
  one breaks the day a slug is translated or a locale is added. The indirection is a **named route**, consumed
  as `{{ 'routename' | url }}`. See `references/engine-liquid.md`.
- **Every wrong way to call the `url` filter returns 200.** A typo'd route name points at the current page; a
  mis-shaped argument dumps the whole record into the query string. Detail pages are the sharp edge —
  `references/detail-pages.md` before you wire one.
- **Images are uploaded, not pushed.** `quilium push` carries `public/`; content images live in the media
  library and reach it only by an upload (MCP, or `quilium media upload`). An image you never uploaded renders
  `src=""` and warns nobody.
- **Register the 404 in the settings.** A `404.liquid` that exists on disk but isn't declared in
  `miscellaneous.rendering.404` is not the site's 404 — every unknown URL errors instead.
- **Define page-types before creating pages.** A page freezes its template at creation; changing the page-type
  afterwards does not propagate, and the page 500s while the settings still look correct.
- **Create pages `state: active`.** `state` means routable, not published. An `inactive` page 404s everywhere,
  including locally. "Leave it in draft" means don't publish a live revision — never deactivate.
- **A settings write replaces its target wholesale.** `update-settings-partial` replaces the whole block you
  aim at, and `update-setting` replaces the entire file. Always read the current value, merge your change into
  it, and write the result back complete — including the parts you have no opinion about.
- **Nothing publishes itself.** Publishing is a human decision, page by page.
- **Probe before building logic on a filter.** Drop `<!--DBG x=[{{ … }}]-->` into a shared partial, `curl | grep
  DBG`, remove it. Some filters return empty without erroring; a wrong assumption here costs an afternoon.

## Where to look — intent to source

Build this table from `get-skills` at the start of the session; the slugs below are the ones commonly
present, not a guarantee. **If the manifest doesn't offer it, use the fallback column** — don't wait for a
skill that isn't coming.

| You're about to… | Load if offered | Otherwise |
|---|---|---|
| Decide the shape of a feature | `practices-conventions-architecture` | ask the wysiwyg question first: a bullet list or a paragraph-with-CTA is one field, not a `repeat` |
| Give the editor rich text that matches the design | `reference-wysiwyg-config` | read the site's existing `wysiwyg` settings and mirror that shape — never invent the palette syntax |
| Choose a field type | `reference-fields-catalog` | probe one in the back-office before committing a schema to it |
| Name anything | `practices-conventions-naming` | English camelCase keys, consistent site-wide, full template path, `.liquid` |
| Design the editor's experience | `practices-conventions-cms-ux` | — |
| Write a template | — | `references/engine-liquid.md` |
| Wire a listing and its detail pages | — | `references/detail-pages.md` |
| Upload and render images | `tasks-media-crud` (library ops) | `references/media.md` (schema + template side) |
| Port an approved HTML prototype | — | `references/from-a-prototype.md` |
| Set up the 404 | — | `references/process-new-site.md`, step 3 |
| Move a page in the tree | `reference-navigation` | `reorder-navigation`, never `update-page` |
| Batch more than a handful of MCP calls | `practices-ops-mcp-batching` | serialise and read each response |
| SEO metadata | `practices-compliance-seo-basics` | — |
| Run the CLI | — | `references/local-dev.md` |
| Import rows, or edit a long field as a file | — | `references/cli-content.md` (if the CLI is installed; otherwise MCP) |

## Bundled references

- `references/process-new-site.md` — the five steps in full, with the dependency order and why it holds.
- `references/engine-liquid.md` — the template layer: globals, filters, and what fails silently.
- `references/detail-pages.md` — the listing → detail chain: route, query field, hidden page, links.
- `references/media.md` — images end to end: upload, reference, schema versions, render.
- `references/from-a-prototype.md` — porting an approved HTML prototype without redesigning it.
- `references/local-dev.md` — `init`, `run`, `push`, `dictionary`, and the debugging loop.
- `references/cli-content.md` — content from the shell: blocks, collection rows, media, and when to prefer
  the CLI over the MCP.

## What this skill is not

Not a schema reference — that's the MCP library, and it's more current than any copy.
Not a content-authoring guide — that's `quilium-webmaster`, loaded alongside this one: a build is not
structure alone, it ends with media and content (step 5), and that phase follows the webmaster's discipline.
Not site-specific — per-site conventions belong in the project's own `CLAUDE.md`, and what a site does its
own way lives in its procedures (the `site` group of `get-skills`).
