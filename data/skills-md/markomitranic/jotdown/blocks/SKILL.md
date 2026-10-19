---
name: blocks
description: Use only when working on the docs site. The list of every block a page may use beyond plain markdown, callouts, embeds, figures, fences, tables, layout components, and the styling rules behind them. Read before adding anything richer than markdown to a page, or before touching a project's theme.
---
# Blocks

Anything richer than markdown goes into a page as one of the blocks below. The list belongs to the framework, and a project cannot add to it. If what you want is not here, it must be either a figure or prose. Inventing a new `className` is not the answer; see Styling.

## Callouts

`:::note`, `:::tip`, `:::info`, `:::warning` (`:::warn`, `:::caution`), `:::danger` and our own `:::source`. Plain markdown, no import:

```md
:::warning[Required]

Careful, and *emphatic*.

:::
```

The label in brackets is optional; without one the callout prints its own name. `:::source` is the grey one with a bookmark: where a pattern in the text comes from, book, author, year. The in-page editor draws the same callout, so it looks the same while you write it.

## `<VideoEmbed url="..." />`

A YouTube video, embedded at 16:9. Registered globally, so no import and no ceremony:

```md
<VideoEmbed url="https://www.youtube.com/watch?v=dQw4w9WgXcQ" />
```

## `<LinkEmbed url="..." />`

A link drawn as a card: the page's title, a line of its description, the site's name and icon, and its preview picture on the right. Also global. Reach for it when a link is the point of a paragraph, a tool, a repository or a reference worth opening; a link inside a sentence stays a markdown link.

Only `url` is required. The other props are what the page itself declares, its `og:title`, `og:description`, `og:site_name`, `og:image` and icon, and the studio reads them once when somebody pastes the link onto an empty line. Writing one by hand, copy them from the page's own tags rather than inventing them, and leave out any you cannot read: a card with only `url` shows the address as its title and the host as its site. Never point `image` at a picture you have not seen load.

```md
<LinkEmbed
  url="https://fumadocs.dev/"
  title="Fumadocs"
  description="The React.js documentation framework."
  site="Fumadocs"
  image="https://www.fumadocs.dev/banner.png"
  favicon="https://www.fumadocs.dev/icon.png"
/>
```

## `<FileAttachment ... />`

A file committed to the page and offered as a download card. Also global. Only `href` is required; `size` is a byte count, `uploadedAt` is `YYYY-MM-DD`, `note` runs to 200 characters.

```md
<FileAttachment
  href="/files/docs/9f2c1a8b.zip"
  name="latency-harness.zip"
  size="248193"
  uploadedAt="2026-08-22"
  note="The harness behind the Q3 p99 numbers. Run make bench."
/>
```

## `<DocCardList />`

The grid of child pages that every section landing page ends with. It needs no import: the page binds it to its own place in the tree. It writes its own heading — "Sections" at the site root, "In this section" inside one — so do not put a `##` above it. Pass `title="…"` for different words. The page you are on is never listed, and each card carries the target's `description`, so every page wants one in its front matter and every section wants one in its `meta.json`.

## Tables

A GFM markdown table, and nothing else. The `table` element sits in a horizontally scrolling box, and the prose typography draws the header, the rules and the cell padding, so a wide table scrolls instead of widening the page. A colon in the dashed row sets a column's alignment (`:---:` centres, `---:` right-aligns, which is what a column of numbers wants), and cells take inline markdown, so links, `code` and **bold** all work inside one.

Reach for a chart instead when the cells are mostly numbers you want compared rather than looked up.

## Images

A screenshot or a diagram that ships as a file is plain markdown. The frame, the cap and the caption come from the theme, so there is no wrapper to type:

```md
![The blocks of a page, with one being written in](/img/docs/editor.png "A grip in the left margin moves a block; the bar at the foot commits the page.")
```

- The first bracket is the `alt`: what somebody who cannot see the image needs to know. A sentence about the content, not "screenshot of X".
- An image carrying nothing the prose does not already say is decorative. Write `![](…)` and it is marked as such and skipped by screen readers.
- The quoted string after the path is optional and becomes the caption.
- The image is drawn at its own size up to the width of the text, a little wider on a wide screen, and never taller than `--jd-shot-height`, so a large export cannot take the whole window. Clicking it opens the original file on a dimmed backdrop, and pointing at it shows a toolbar to expand, copy or download the original. Export a screenshot at the size it should be read; a small one is not stretched to fill the column.
- Files live in the project's `docs/_uploads/img/docs/`, which is where the in-page editor puts an upload.
- An SVG follows the colour mode from one file: in dark mode the page draws it again at `#dark`, so a palette set under `svg:target` is its night one. An SVG with one palette looks the same in both.
- An image with no path, `![The team's logo]()`, draws a placeholder saying it could not be downloaded. A page pasted from another site gets one for each picture the browser was not allowed to fetch. Replace it with the real file, never with a link to the other site. An image whose path answers with no picture draws the same placeholder, saying it could not be loaded.

## Widths

A table or an image can stand wider than the article column. Put it alone inside `:::wide` or `:::full`, plain markdown, no import:

```md
:::wide

| Product | Purpose | Business capabilities | Key systems |
| --- | --- | --- | --- |
| Field service | Customers, assets and service delivery in one platform | Case management, work orders | A CRM |

:::
```

- No wrapper is the column, which is right for almost everything. `:::wide` is a step wider, for a table whose columns are cramped or a screenshot whose detail matters. `:::full` runs to the edges of the page, for the one overview a page is built around.
- Both are centred on the column and never narrower than it, so on a small screen they read as an ordinary block.
- A widened image fills its block and drops the screenshot height cap, so only widen an image that was exported large enough to fill it.
- Only a table or a lone image widens, and only as a block of the page itself. Around anything else, or inside a callout, tab or other block, the wrapper is ignored and the content reads at the column's width.
- In the in-page editor the block's grip menu has Width, and a widenable block has a grip on its side to drag it between the three.

## ```mermaid fences

A sequence, flow or state diagram written as code, rendered by Mermaid in the browser. Plain markdown, no import. Inline it shrinks to the page column like an image; clicking it opens a fullscreen stage that pans with the trackpad and zooms with a pinch. Split a long flow at its natural chapters into several fences interwoven with the prose, rather than one tall drawing.

In the in-page editor a fence is the diagram rather than its source: click a node to rename or reshape it, drag from one to another to draw an edge. Every edit is written back as Mermaid source into the fence. `/diagram` inserts a starter flowchart, and an empty fence offers a flowchart, sequence or state diagram to start from.

## Code fences

Shiki highlights every fence, and the meta string after the language is part of the block:

````md
```ts title="lib/cart.ts" lineNumbers
```
````

`title="…"` prints a filename header, `lineNumbers` numbers the lines, and comment annotations mark lines up in place: `// [!code highlight]`, `// [!code ++]` and `// [!code --]` for a diff, `// [!code focus]` to dim the rest, `// [!code word:parseDocument]` to pick out a token. `tab="Server"` on two adjacent fences turns them into one tabbed block, and needs no registration. The in-page editor keeps that meta string as written and prints it back untouched, so a fence with a title opens with the filename in its caption bar and saves with the same header and the same tab it had. A fence you write in is highlighted as you type, by the same Shiki and the same theme the built page uses, and a dropdown in the frame's corner, shown while you point at the fence, names the language.

## `jd-fig` figures

Inline SVG or HTML figures, drawn by the figure skill. Clicking the drawing opens it on the same fullscreen stage a Mermaid diagram gets, with pan, zoom and a minimap; there is nothing to add to the figure for that. An HTML figure, the skill's escape hatch, has no drawing to stage and stays where it is. The figure skill carries a routing table from what a paragraph is about to the form of figure that shows it, a layout reference per form under `references/forms/`, the connector rules every arrow follows, and an index of the Claude Code built-in skills to load for each kind of figure (`artifact-diagramming` for mechanisms, `dataviz` for charts). Any other visual skill you have access to is fair to use too.

## `<Chart />`

A bar, line, area, pie or radar chart of literal data, drawn by shadcn's chart component on Recharts in the brand's `--chart-1` to `--chart-5`, with a tooltip and a legend. `x` names the field that labels each row, `series` maps each plotted field to its label in colour order, and `stacked`, `horizontal`, `unit` and `caption` are optional. The chart skill says which type answers which question. In the in-page editor it is a block that moves and deletes but is edited in the source.

```mdx
<Chart type="bar" x="month" data={[{ month: "Apr", saves: 186 }, { month: "May", saves: 305 }]} series={{ saves: "Studio saves" }} />
```

## Layout components

Five families of layout components are registered by the framework, so a page uses them with no import. Any other tag renders as nothing at all.

- `<Tabs items={['npm','bun']}><Tab value="npm">…</Tab></Tabs>`. One instruction, several environments, without three near-identical sections.
- `<Steps><Step>…</Step></Steps>`. A numbered procedure with a rail down the left. Better than `1.` `2.` `3.` when each step carries a code block.
- `<Files><Folder name="docs"><File name="index.mdx" /></Folder></Files>`. A directory tree, which is otherwise an ASCII drawing inside a fence.
- `<Cards><Card title="ADR 0015" href="/decision-records/0015-hosted-studio-and-static-publishing" /></Cards>`. A hand-picked set of links, where `<DocCardList />` gives you every child.
- `<Accordions><Accordion title="…">…</Accordion></Accordions>`. Answers most readers will skip, folded away. `type="multiple"` lets several stand open at once, `defaultValue` is the title of the one that starts open, and an `id` on a panel gives it a copy-link button plus an anchor that opens it.

Some components other docs frameworks ship are deliberately left out:

| Component | Why not |
| --- | --- |
| `Callout` | `:::note` and friends are the same thing in markdown, and the in-page editor draws them. |
| `ImageZoom` | A markdown `![](…)` renders `DocImage`, which frames, caps and zooms already. |
| `CodeBlockTabs` | Two adjacent fences with `tab="…"` do the same thing in markdown. |
| `DynamicCodeBlock` | Highlights at runtime, for code that is not in the file. Every fence here is. |
| `Banner`, `GitHubInfo` | Site chrome rather than page content. |
| `InlineTOC` | Takes a `TOCItemType[]` array, which nobody can write by hand. Pages get the sidebar TOC regardless. |
| `TypeTable`, `AutoTypeTable` | A markdown table with a column for the type and one for whether it is required says the same. |
| `GraphView` | A site this size navigates from the sidebar. |


# Styling

The site's typography is the framework's own: the heading scale, the line length, the
spacing between blocks, the table and code frames. A page does not restyle any
of it. Article prose under `docs/` is plain markdown, full stop.

A project's look lives in one place, never a page: the `theme` in
`.jotdown/config.json`. Shadcn token names once per mode, `background`,
`foreground`, `primary`, `destructive` and `chart-1` to `chart-5`, paint every
block, figure and chart, so both colour modes follow without a page knowing.
`sections` gives a section its colour by naming a token, `radius` rounds the
corners, and `fonts` names the `sans`, `serif` and `mono` faces.

## className in a document

If a passage needs emphasis, markdown already has it: a blockquote (`>`), bold,
a callout (`:::note`, `:::warning`, `:::source` for citations).

One className is allowed in `docs/`, and no others: `jd-fig`, on an inline SVG
or HTML figure drawn by the figure skill. That is a picture, not prose.

Anything else is unwritable by humans, invisible to the in-page editor, and
becomes a permanent stain in the repo. Do not invent a `className` for prose,
and do not reach for Tailwind utilities inside a document: only the classes the
framework's own components use are compiled, so any other renders as an
unstyled element.

## Rules of thumb

- Don't hard-code colours or fonts in a page. A figure paints with the
  `--jd-fig-*` tokens, a chart with the brand's chart colours, and the one
  exception is an editorial illustration, an SVG file with its own palette.
- Don't restyle the article. If a heading, a paragraph or a table looks wrong,
  leave it, and say so to whoever maintains the framework.
- Unless the user asks for Mermaid, diagrams are inline SVG/HTML figures drawn
  with the figure skill. Mermaid is for complex, deeply technical,
  deterministic reference diagrams; everything else is an illustrative figure
  aiming to lower cognitive load.

The same rules as a table, for the cases people actually hit:

| Want | Don't | Do |
| --- | --- | --- |
| Emphasise a passage | a `<div className="…">` around prose | `>` blockquote, bold, or a `:::note` / `:::warning` callout |
| A coloured or boxed paragraph | a new class, or Tailwind utilities in the document | plain markdown; if it is a picture, a `jd-fig` figure |
| A colour for the project | a hex value in a page | a shadcn token in the `theme` of its `.jotdown/config.json` |
| A typeface for the project | a `<style>` in a page | a face in the theme's `fonts` |
| A process or state diagram in official reference docs | a hand-drawn figure | a ```mermaid fence |
| An illustration next to prose | a ```mermaid fence | a `jd-fig` figure drawn by the figure skill |
| A picture that opens a story, magazine-style | a diagram with its boxes renamed, or an SVG pasted into the page | an SVG file from the editorial-illustration skill, shown as a markdown image inside `:::wide` |
| A number, trend or comparison | boxes and arrows, or a paragraph of figures | a `<Chart />` block, per the chart skill |
