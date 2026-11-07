---
name: codedvisuals
description: Add CodedVisuals visual compositions to a React marketing or landing page. Use when the user wants an animated coded visual (charts, hero, bento, feature block, dashboard, chat, code editor, avatars, integrations, and more) in their project, when picking which visual fits a section, or when installing, importing, and customizing one. This is the entry point; each visual also has a reference file at visuals/{category}/{file}.md.
---

# Using CodedVisuals

CodedVisuals is a library of marketing visuals built as self-contained React components. Each visual is a single `.tsx` file with no shared dependencies between visuals, styled with shadcn/ui design tokens and animated with Motion. They are decorative illustrations for marketing and landing pages (heroes, bento grids, feature blocks, product explainers), not interactive app UI.

**CodedVisuals is a paid library.** The catalog below ships from a private registry that needs a license: [codedvisuals.com/pricing](https://codedvisuals.com/pricing). If the user has no license yet, tell them the visual they want is part of the paid library and link them to pricing. Do not quietly hand-build a substitute instead, unless they ask you to.

This is the entry point. It covers how to pick a visual, get it into the project, and use it. Every visual also has a reference file bundled with this skill at `visuals/{category}/{file}.md` (for example `visuals/charts/line.md`), with that visual's exact props, default content, and copy-ready examples. Read that file once you know which visual you want.

## How to work with a visual

1. **Pick a visual** from the catalog at the end of this file. Each entry has a registry name, a description, and the reference file to open next.
2. **Open the visual's reference file** (`visuals/{category}/{file}.md`) for its props, defaults, and examples.
3. **Make sure it is installed** in the project (next section). This skill is not tied to what is installed, so a visual you pick may not be in the project yet.
4. **Import and use it** inside a sized container (see "Use it on a page").

## Install a visual if it is not in the project

The project may have this skill without having every visual installed. Before using a visual, check whether its file already exists under the project's source root:

```
components/codedvisuals/{category}/{file}.tsx
```

The exact root varies by project (for example `src/` in a Vite app, `resources/js/` in a Laravel app). If the file is there, just import it. If it is not, add it one of two ways.

Both ways need a license, so before starting either one, check whether the project already has the registry configured (a `@codedvisuals` entry in `components.json`) and a token available. If it does not, this is a purchase step only the user can complete: point them at [codedvisuals.com/pricing](https://codedvisuals.com/pricing) and stop there. Never reimplement a catalog visual from its description in this skill as a workaround for a missing license.

### Install with the shadcn CLI (recommended)

CodedVisuals ships a private shadcn registry. After a one time setup (below), install any visual by its registry name, which is `{category}-{file}`:

```bash
npx shadcn@latest add @codedvisuals/charts-line
```

The CLI drops the file into `components/codedvisuals/` and installs Motion and lucide-react if they are missing. Other package managers work the same way: `pnpm dlx shadcn@latest add ...`, `yarn shadcn@latest add ...`, `bunx --bun shadcn@latest add ...`.

#### Set up the private registry (one time)

The registry is private, so it needs a CodedVisuals account with an active license and a personal registry token. This is configured once per project, and it requires actions only the user can take (purchasing, signing in, copying a secret), so guide the user through these steps rather than attempting them yourself.

1. **Get a license and issue a token.** Buy a license at [codedvisuals.com/pricing](https://codedvisuals.com/pricing) if the user does not have one, then sign in, open Settings, Registry token, and issue a token. It is shown only once, so copy it right away.
2. **Add the registry to `components.json`** with a `registries` entry that reads the token from an environment variable:

   ```json
   "registries": {
     "@codedvisuals": {
       "url": "https://codedvisuals.com/r/{name}.json",
       "headers": { "Authorization": "Bearer ${CODEDVISUALS_TOKEN}" }
     }
   }
   ```

3. **Expose the token** in the project's `.env` (or shell environment):

   ```bash
   CODEDVISUALS_TOKEN=your-token-here
   ```

After this, `npx shadcn@latest add @codedvisuals/{category}-{file}` works for any visual in the catalog. The Settings, Registry token page also shows these exact `components.json` and `.env` snippets prefilled, and is the authoritative source if the registry URL ever differs from the above.

### Copy and paste

Licensed members can copy a visual's source or download its file from its preview page, then drop it into `components/codedvisuals/{category}/`. On this path you install the dependencies yourself: Motion and lucide-react. Members only: a visual's source is not public, so if the user is not signed in with a license, send them to [codedvisuals.com/pricing](https://codedvisuals.com/pricing).

### Projects without shadcn/ui

Visuals expect four things from the host project: the `cn` class-merging utility, a `cn()` helper at `@/lib/utils`, the shadcn/ui design-token CSS variables, and an `@` import alias pointing at the source root. A shadcn/ui project already has these. For a plain React + Tailwind CSS v4 project, follow `manual-setup.md` in this skill, then copied files work unchanged.

## Use it on a page

A visual brings its own height, so it always renders, but it looks best inside a box that gives it room: set an exact height or a `min-h-*`. `h-96` is a good default for most cases. Without a defined height the visual sits edge to edge, top and bottom, with no room to breathe.

```tsx
import ChartsLine from "@/components/codedvisuals/charts/line";

export default function LandingPage() {
  return (
    <div className="h-96 rounded-2xl border bg-card">
      <ChartsLine animated />
    </div>
  );
}
```

Keep the container padding-free. Each visual already clips its own content, so it fills the frame to the rounded corners and tucks its edges out of sight when space is tight; padding would shrink it and leave gaps.

Alternatively, for a more subtle visual container, you can use the following classes:

```tsx
<div className="h-96 rounded-2xl border border-border/50 bg-muted/20 dark:bg-muted/15">
  <ChartsLine animated />
</div>
```

For a soft vignette, pass mask utilities straight to the visual:

```tsx
<div className="h-96 rounded-2xl border bg-card">
  <ChartsLine
    animated
    className="mask-t-from-85% mask-r-from-85% mask-b-from-85% mask-l-from-85%"
  />
</div>
```

The default import name is the consumer's choice; `{Category}{File}` in PascalCase (for example `ChartsLine`) is a safe convention.

If the host project already has its own grid, card, or feature-section layouts, drop the visual into those. If it does not, open `layout-patterns.md` in this skill for ready-to-paste containers, feature cards, bento grids, and split rows. Note that without an existing layout it's a good approach to give the container an explicit height or minimum height to give vertical room for the visual to breathe.

## Animation

Animation is opt-in through three props:

- `animated` turns motion on. Without it the visual renders in its final, static state.
- `trigger` decides when the entrance plays:
  - `mount`: animate as soon as the visual renders.
  - `inView` (default): animate once when it scrolls into view.
  - `inViewRepeat`: replay every time it scrolls back into view.
- `hover` enables hover micro-interactions on visuals that support them.

```tsx
<ChartsLine animated trigger="mount" />
<ChartsLine animated trigger="inViewRepeat" hover />
```

Omit `animated` entirely for a completely still illustration.

## Presentation modifiers

Most visuals accept marketing-ready modifiers. They are optional:

- `gradient` (default `true` when supported): a soft brand glow behind the visual.
- `fadeOut` (default `false`): fade the bottom edge into the background.
- `isometric` (default `false`): a subtle 3D tilt.

```tsx
<ChartsLine animated isometric fadeOut />
```

## Data props and defaults

Visuals are data-driven. Beyond the shared props above, each visual takes its own typed props (copy, values, icons, counts) to customize appearance and content. Every prop is optional and falls back to a sensible default, so pass only what you want to override. The exact props, their types, defaults, and examples live in each visual's reference file under `visuals/`. When in doubt, the installed `.tsx` file is the source of truth: its props `interface` and `DEFAULT_*` values show the full API.

## Theming and accessibility

Visuals read the project's shadcn/ui tokens, so they match the brand with zero configuration. Change the `--primary` token and every visual updates; toggle the `.dark` class and they switch to dark mode. The Tailwind palette is only used for small supportive accents, never the core brand surfaces.

Visuals are decorative: the outer container is `aria-hidden`, so do not rely on them to convey information to assistive tech. Pair a visual with real text content in the surrounding section.

## Visual catalog

Pick by category. Each entry is `registry-name` (**Name**): description, plus the reference file to open next.

<!-- CATALOG:START -->

### Activity

- `@codedvisuals/activity-feed` (**Feed**): A live activity feed with avatars, actions, and relative timestamps. Details: `visuals/activity/feed.md`.
- `@codedvisuals/activity-timeline` (**Timeline**): A vertical activity timeline of grouped events and status changes. Details: `visuals/activity/timeline.md`.

### AI

- `@codedvisuals/ai-agent-flow` (**Agent Flow**): An agent pipeline of stacked isometric cubes that light up in sequence, revealing each step label as it runs. Details: `visuals/ai/agent-flow.md`.
- `@codedvisuals/ai-model-picker` (**Model Picker**): A model switcher that cycles through AI models and streams each one's answer with its speed, latency, and cost. Details: `visuals/ai/model-picker.md`.
- `@codedvisuals/ai-neural-net` (**Neural Net**): A layered network where pulses travel node to node and light up the winning output with its confidence. Details: `visuals/ai/neural-net.md`.
- `@codedvisuals/ai-presence` (**Presence**): Live multiplayer cursors roaming a shared canvas, one carrying your avatar and the rest labeled AI agents, over an ambient glow and particle field. Details: `visuals/ai/presence.md`.
- `@codedvisuals/ai-prompt-box` (**Prompt Box**): A wide prompt composer with a typing prompt, model picker, token count, and send, over an ambient glow and particle field. Details: `visuals/ai/prompt-box.md`.
- `@codedvisuals/ai-retrieval` (**Retrieval**): A query fanning out to ranked source cards that light up as each pulse lands, then converging into a streamed answer, over an ambient glow and particle field. Details: `visuals/ai/retrieval.md`.
- `@codedvisuals/ai-thinking` (**Thinking**): A reasoning panel that streams its thinking steps, collapses into a summary, then streams the final answer. Details: `visuals/ai/thinking.md`.
- `@codedvisuals/ai-tools` (**Tools**): An agent working through its tool calls one at a time, each row running with a spinner then settling into a result and a duration. Details: `visuals/ai/tools.md`.
- `@codedvisuals/ai-voice` (**Voice**): A realtime voice assistant orb that cycles through listening, thinking, and speaking states, with pulsing rings, a live equalizer, a status pill, and a transcript, over an ambient glow and particle field. Details: `visuals/ai/voice.md`.
- `@codedvisuals/ai-writer` (**Writer**): A document where an AI rewrites a selection, autocompletes ghost text, or answers a slash command inline behind a labeled AI caret, over an ambient glow and particle field. Details: `visuals/ai/writer.md`.

### API

- `@codedvisuals/api-logs` (**Logs**): Service nodes streaming into a log console along connected paths, with severity-colored level chips and rows that tail in. Details: `visuals/api/logs.md`.
- `@codedvisuals/api-request` (**Request**): A request arcing from client to server and a response arcing back, with a method pill, a status code, and a JSON response card. Details: `visuals/api/request.md`.
- `@codedvisuals/api-webhook` (**Webhook**): A webhook event fanning retry arcs at your endpoint, where failed attempts fall short and the successful one delivers. Details: `visuals/api/webhook.md`.

### Automations

- `@codedvisuals/automations-workflow-builder` (**Workflow Builder**): A workflow where a trigger runs into a condition that branches to one of two actions, with a run pulse lighting the path taken. Details: `visuals/automations/workflow-builder.md`.

### Avatars

- `@codedvisuals/avatars-grid` (**Grid**): A grid of user avatars with subtle staggered reveals. Details: `visuals/avatars/grid.md`.
- `@codedvisuals/avatars-stack` (**Stack**): An overlapping avatar stack with a remaining count badge. Details: `visuals/avatars/stack.md`.
- `@codedvisuals/avatars-profile-card` (**Profile Card**): A compact profile card with avatar, name, and key stats. Details: `visuals/avatars/profile-card.md`.

### Branding

- `@codedvisuals/branding-spotlight` (**Spotlight**): An app icon spotlit over a fading dock of placeholder apps, with ambient glow and a particle field. Details: `visuals/branding/spotlight.md`.

### Browser

- `@codedvisuals/browser-loading` (**Loading**): A browser window mockup with an animated page loading state. Details: `visuals/browser/loading.md`.
- `@codedvisuals/browser-simple` (**Simple**): A clean browser window frame for showcasing any screenshot or UI. Details: `visuals/browser/simple.md`.
- `@codedvisuals/browser-tabs` (**Tabs**): A browser window with switching tabs and an address bar. Details: `visuals/browser/tabs.md`.

### Calendar

- `@codedvisuals/calendar-date-picker` (**Date Picker**): A calendar date picker with a selected day and range highlight. Details: `visuals/calendar/date-picker.md`.
- `@codedvisuals/calendar-event-list` (**Event List**): An agenda style list of upcoming calendar events. Details: `visuals/calendar/event-list.md`.
- `@codedvisuals/calendar-month-view` (**Month View**): A full month calendar grid with events placed on days. Details: `visuals/calendar/month-view.md`.

### Charts

- `@codedvisuals/charts-bar` (**Bar**): An animated bar chart with a value, trend badge, and grid. Details: `visuals/charts/bar.md`.
- `@codedvisuals/charts-donut` (**Donut**): An animated donut chart with a center total and legend. Details: `visuals/charts/donut.md`.
- `@codedvisuals/charts-funnel` (**Funnel**): A conversion funnel of tapering stage slabs that pour in one by one, with per stage counts and conversion rates. Details: `visuals/charts/funnel.md`.
- `@codedvisuals/charts-gauge` (**Gauge**): A semicircular gauge whose arc sweeps to its value, with an optional zoned track, a center reading, and range labels. Details: `visuals/charts/gauge.md`.
- `@codedvisuals/charts-heatmap` (**Heatmap**): A grid heatmap of labeled rows and columns whose cells light up in a diagonal sweep, with an intensity legend. Details: `visuals/charts/heatmap.md`.
- `@codedvisuals/charts-line` (**Line**): An animated line chart with a value, trend badge, and gradient fill. Details: `visuals/charts/line.md`.
- `@codedvisuals/charts-sparkline` (**Sparkline**): A compact inline sparkline for tight spaces and stat cards. Details: `visuals/charts/sparkline.md`.

### Chat

- `@codedvisuals/chat-ai-chat` (**AI Chat**): An AI chat interface with streaming responses and a prompt box. Details: `visuals/chat/ai-chat.md`.
- `@codedvisuals/chat-bubbles` (**Bubbles**): A conversation of chat bubbles between two people. Details: `visuals/chat/bubbles.md`.
- `@codedvisuals/chat-thread` (**Thread**): A threaded message view with replies and reactions. Details: `visuals/chat/thread.md`.

### Code

- `@codedvisuals/code-editor` (**Editor**): A code editor mockup with syntax highlighting and a file tab. Details: `visuals/code/editor.md`.
- `@codedvisuals/code-snippet` (**Snippet**): A copyable code snippet card with a language label. Details: `visuals/code/snippet.md`.
- `@codedvisuals/code-terminal` (**Terminal**): A terminal window with a typing command and output. Details: `visuals/code/terminal.md`.

### Connections

- `@codedvisuals/connections-converge` (**Converge**): Multiple sources converging into a single destination node. Details: `visuals/connections/converge.md`.
- `@codedvisuals/connections-flow` (**Flow**): An animated flow of nodes connected by data paths. Details: `visuals/connections/flow.md`.
- `@codedvisuals/connections-pipeline` (**Pipeline**): A linear pipeline of stages with moving progress. Details: `visuals/connections/pipeline.md`.
- `@codedvisuals/connections-sync` (**Sync**): Two systems syncing with data moving back and forth. Details: `visuals/connections/sync.md`.

### Data

- `@codedvisuals/data-filters` (**Filters**): A filter builder where each rule lands in turn and narrows a running result count and progress bar. Details: `visuals/data/filters.md`.
- `@codedvisuals/data-import` (**Import**): A CSV import mapper where each source column connects across to its destination field, leaving unmapped columns skipped. Details: `visuals/data/import.md`.
- `@codedvisuals/data-query` (**Query**): A visual query builder that assembles its conditions, sweeps as it runs, then streams the matching rows with a timing readout. Details: `visuals/data/query.md`.
- `@codedvisuals/data-table` (**Table**): A data table with sortable columns, rows, and status pills. Details: `visuals/data/table.md`.

### Dashboard

- `@codedvisuals/dashboard-mini-panel` (**Mini Panel**): A compact dashboard panel with a metric and mini chart. Details: `visuals/dashboard/mini-panel.md`.
- `@codedvisuals/dashboard-widget-grid` (**Widget Grid**): A grid of dashboard widgets and summary cards. Details: `visuals/dashboard/widget-grid.md`.

### Devices

- `@codedvisuals/devices-laptop` (**Laptop**): A laptop device frame for presenting a screenshot or UI. Details: `visuals/devices/laptop.md`.
- `@codedvisuals/devices-phone` (**Phone**): A phone device frame for showcasing a mobile screen. Details: `visuals/devices/phone.md`.
- `@codedvisuals/devices-tablet` (**Tablet**): A tablet device frame for showcasing an app or page. Details: `visuals/devices/tablet.md`.

### Email

- `@codedvisuals/email-compose` (**Compose**): An email compose window with recipient, subject, and body. Details: `visuals/email/compose.md`.
- `@codedvisuals/email-inbox` (**Inbox**): An email inbox list with senders, previews, and unread states. Details: `visuals/email/inbox.md`.

### Files

- `@codedvisuals/files-explorer` (**Explorer**): A file explorer with a folder tree and file list. Details: `visuals/files/explorer.md`.
- `@codedvisuals/files-simple` (**Simple**): A simple file card with name, type, and size. Details: `visuals/files/simple.md`.
- `@codedvisuals/files-stacked` (**Stacked**): A stack of overlapping file cards with depth. Details: `visuals/files/stacked.md`.
- `@codedvisuals/files-upload` (**Upload**): A file upload area with progress and drag and drop. Details: `visuals/files/upload.md`.

### Geo

- `@codedvisuals/geo-edge-network` (**Edge Network**): A dotted world map where a request hops to the nearest edge node, with latency chips comparing the edge to a distant origin server. Details: `visuals/geo/edge-network.md`.
- `@codedvisuals/geo-geofence` (**Geofence**): A softly faded street map with a drawn zone, tracked devices driving its irregular roads, and a toast that pops each time one enters the zone. Details: `visuals/geo/geofence.md`.
- `@codedvisuals/geo-globe` (**Globe**): A rotating globe of dotted continents with location markers and connection arcs that draw in. Details: `visuals/geo/globe.md`.
- `@codedvisuals/geo-pin-drop` (**Pin Drop**): Location pins dropping onto an abstract radar field with concentric ripple pings. Details: `visuals/geo/pin-drop.md`.
- `@codedvisuals/geo-world-map` (**World Map**): A dotted world map that blooms outward from a chosen city, with pinging location markers, tinted coverage regions, and connection arcs that draw between cities. Details: `visuals/geo/world-map.md`.

### Git

- `@codedvisuals/git-branch-graph` (**Branch Graph**): A commit rail where feature branches fork off, run their own commits, and merge back, with pulses traveling every path. Details: `visuals/git/branch-graph.md`.
- `@codedvisuals/git-diff` (**Diff**): A file diff with added and removed lines, in unified or side by side view, swept line by line as the change counters climb. Details: `visuals/git/diff.md`.
- `@codedvisuals/git-pull-request` (**Pull Request**): A pull request card whose CI checks run one by one, then settle into an approval and a merge button that lights up. Details: `visuals/git/pull-request.md`.

### Images

- `@codedvisuals/images-carousel` (**Carousel**): An image carousel with slides and navigation controls. Details: `visuals/images/carousel.md`.
- `@codedvisuals/images-gallery` (**Gallery**): A responsive image gallery grid with hover states. Details: `visuals/images/gallery.md`.

### Integrations

- `@codedvisuals/integrations-hub` (**Hub**): A central app connected to surrounding integration logos. Details: `visuals/integrations/hub.md`.
- `@codedvisuals/integrations-logo-orbit` (**Logo Orbit**): Integration logos orbiting a central brand mark. Details: `visuals/integrations/logo-orbit.md`.
- `@codedvisuals/integrations-logo-marquee` (**Logo Marquee**): Rows of integration logos scrolling in alternating directions, fading out at both edges. Details: `visuals/integrations/logo-marquee.md`.
- `@codedvisuals/integrations-logo-reel` (**Logo Reel**): A row of integration logos sliding one by one into a center spotlight, blurring out as they pass. Details: `visuals/integrations/logo-reel.md`.
- `@codedvisuals/integrations-plugin-slot` (**Plugin Slot**): An isometric board of integration cubes where new logos drop into open slots and connect. Details: `visuals/integrations/plugin-slot.md`.

### Keyboard

- `@codedvisuals/keyboard-half` (**Half**): A half keyboard showing a key combination press. Details: `visuals/keyboard/half.md`.
- `@codedvisuals/keyboard-shortcut` (**Shortcut**): A keyboard shortcut rendered as labeled keycaps. Details: `visuals/keyboard/shortcut.md`.

### Media

- `@codedvisuals/media-audio-waveform` (**Audio Waveform**): An audio player with an animated waveform and controls. Details: `visuals/media/audio-waveform.md`.
- `@codedvisuals/media-video-player` (**Video Player**): A video player frame with controls and a progress bar. Details: `visuals/media/video-player.md`.

### Metrics

- `@codedvisuals/metrics-comparison` (**Comparison**): A before and after metric comparison with deltas. Details: `visuals/metrics/comparison.md`.
- `@codedvisuals/metrics-stat-card` (**Stat Card**): A single stat card with a value, label, and trend. Details: `visuals/metrics/stat-card.md`.
- `@codedvisuals/metrics-trend` (**Trend**): A metric with a trend line and period over period change. Details: `visuals/metrics/trend.md`.

### Notifications

- `@codedvisuals/notifications-bell` (**Bell**): A notification bell with an unread badge and pop. Details: `visuals/notifications/bell.md`.
- `@codedvisuals/notifications-list` (**List**): A list of notifications with icons and timestamps. Details: `visuals/notifications/list.md`.
- `@codedvisuals/notifications-toast` (**Toast**): An animated toast notification that slides in. Details: `visuals/notifications/toast.md`.

### Payments

- `@codedvisuals/payments-checkout` (**Checkout**): A checkout summary with line items and a pay button. Details: `visuals/payments/checkout.md`.
- `@codedvisuals/payments-credit-card` (**Credit Card**): A credit card visual with brand, number, and chip. Details: `visuals/payments/credit-card.md`.
- `@codedvisuals/payments-usage-meter` (**Usage Meter**): A metered billing summary with a usage bar against quota, itemized metered charges, and an estimated total. Details: `visuals/payments/usage-meter.md`.

### Search

- `@codedvisuals/search-command-palette` (**Command Palette**): A command palette with a typed query, grouped commands, keyboard hints, and a selection that walks the list. Details: `visuals/search/command-palette.md`.
- `@codedvisuals/search-results` (**Results**): A search results panel with filter chips, a result count, and matched terms highlighted in place. Details: `visuals/search/results.md`.
- `@codedvisuals/search-semantic` (**Semantic**): A query landing in an embedding space, where a radius sweep lights up its nearest matches with similarity scores. Details: `visuals/search/semantic.md`.

### Sections

- `@codedvisuals/sections-auth` (**Auth**): A login section with social buttons, fields, and a sign-in button. Details: `visuals/sections/auth.md`.
- `@codedvisuals/sections-backgrounds` (**Backgrounds**): A section preview that cycles through background styles (mesh, grid, dots, rays) with a picker to switch between them. Details: `visuals/sections/backgrounds.md`.
- `@codedvisuals/sections-bento` (**Bento**): A bento grid section with a featured tile and mixed-size cards. Details: `visuals/sections/bento.md`.
- `@codedvisuals/sections-blog` (**Blog**): A blog index section with article cards and metadata. Details: `visuals/sections/blog.md`.
- `@codedvisuals/sections-blog-post` (**Blog Post**): A blog post layout with title, meta, and content. Details: `visuals/sections/blog-post.md`.
- `@codedvisuals/sections-comments` (**Comments**): A comments thread with avatars, replies, and votes. Details: `visuals/sections/comments.md`.
- `@codedvisuals/sections-components` (**Components**): A showcase grid of UI components and building blocks. Details: `visuals/sections/components.md`.
- `@codedvisuals/sections-contact` (**Contact**): A contact section with a form and details. Details: `visuals/sections/contact.md`.
- `@codedvisuals/sections-cta` (**CTA**): A call to action section with heading and buttons. Details: `visuals/sections/cta.md`.
- `@codedvisuals/sections-error` (**Error**): An error state section with code, message, and action. Details: `visuals/sections/error.md`.
- `@codedvisuals/sections-faq` (**FAQ**): A frequently asked questions section with expandable items. Details: `visuals/sections/faq.md`.
- `@codedvisuals/sections-features` (**Features**): A features section with icons, titles, and descriptions. Details: `visuals/sections/features.md`.
- `@codedvisuals/sections-footers` (**Footers**): A marketing footer with brand, links, and socials. Details: `visuals/sections/footers.md`.
- `@codedvisuals/sections-headers` (**Headers**): A marketing header with navigation and actions. Details: `visuals/sections/headers.md`.
- `@codedvisuals/sections-hero` (**Hero**): A marketing hero section with heading, copy, and buttons. Details: `visuals/sections/hero.md`.
- `@codedvisuals/sections-logos` (**Logos**): A logo cloud of customer or partner brands. Details: `visuals/sections/logos.md`.
- `@codedvisuals/sections-newsletter` (**Newsletter**): A newsletter signup section with an email input. Details: `visuals/sections/newsletter.md`.
- `@codedvisuals/sections-pricing` (**Pricing**): A pricing section with plan cards and features. Details: `visuals/sections/pricing.md`.
- `@codedvisuals/sections-process` (**Process**): A step by step process section with numbered stages. Details: `visuals/sections/process.md`.
- `@codedvisuals/sections-stats` (**Stats**): A stats section highlighting key numbers. Details: `visuals/sections/stats.md`.
- `@codedvisuals/sections-team` (**Team**): A team section with member cards and roles. Details: `visuals/sections/team.md`.
- `@codedvisuals/sections-testimonials` (**Testimonials**): A testimonials section with quotes and authors. Details: `visuals/sections/testimonials.md`.
- `@codedvisuals/sections-timeline` (**Timeline**): A timeline section of milestones and dates. Details: `visuals/sections/timeline.md`.

### Security

- `@codedvisuals/security-fingerprint` (**Fingerprint**): An animated fingerprint scan with a success state. Details: `visuals/security/fingerprint.md`.
- `@codedvisuals/security-lock` (**Lock**): A lock visual conveying security and access control. Details: `visuals/security/lock.md`.
- `@codedvisuals/security-shield` (**Shield**): A shield visual conveying protection and trust. Details: `visuals/security/shield.md`.

### States

- `@codedvisuals/states-empty` (**Empty**): An empty grid of dashed placeholder slots where an add action ripples out and one slot briefly materializes before dissolving back. Details: `visuals/states/empty.md`.
- `@codedvisuals/states-error` (**Error**): A request pulse traveling into a service card and breaking it, cascading its service tiles to a fault state under an alert badge. Details: `visuals/states/error.md`.
- `@codedvisuals/states-maintenance` (**Maintenance**): A stack of service tiles with one lifted out and being worked on, hovering over its empty slot while a progress sweep runs underneath. Details: `visuals/states/maintenance.md`.
- `@codedvisuals/states-not-found` (**Not Found**): A request spike traveling a route into a barrier at a large status code, ringing out concentric pulses, with the missing page left as a dashed ghost tile. Details: `visuals/states/not-found.md`.

### Status

- `@codedvisuals/status-health-check` (**Health Check**): A service health check with status indicators. Details: `visuals/status/health-check.md`.
- `@codedvisuals/status-resource-monitor` (**Resource Monitor**): A live resource monitor streaming CPU and memory usage across a gridded plot, with a legend showing the current reading for each series. Details: `visuals/status/resource-monitor.md`.
- `@codedvisuals/status-uptime-bar` (**Uptime Bar**): An uptime bar showing daily operational status. Details: `visuals/status/uptime-bar.md`.

### Tasks

- `@codedvisuals/tasks-checklist` (**Checklist**): A checklist with items completing one by one. Details: `visuals/tasks/checklist.md`.
- `@codedvisuals/tasks-kanban` (**Kanban**): A kanban board with columns and draggable cards. Details: `visuals/tasks/kanban.md`.

<!-- CATALOG:END -->
