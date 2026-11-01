---
name: carbon
description: IBM Carbon design system aesthetic — gray-layered enterprise UI, IBM Plex type, blue-60 actions, data-dense console components.
---

# Carbon (IBM)

Carbon is IBM's open-source design system for enterprise products. The look:
flat gray layering (no drop shadows), IBM Plex Sans/Mono, sharp square corners,
Blue 60 (`#0f62fe`) as the one true action color, and extreme data density.
If it looks like an IBM Cloud or Red Hat console, you're doing it right.

## Principles

1. **Carbon is open** — everything is public, tokens over hard-coded values. Never
   hard-code a hex; name a token (role-based: `$background`, `$text-primary`).
2. **Carbon is modular** — components are independent, swappable parts; assemble
   pages from a shared kit, don't hand-craft one-offs.
3. **Carbon is consistent** — the same token names/roles across all four themes;
   only values change. Consistency is what makes enterprise UIs learnable.
4. **Carbon is inclusive** — every text/background pairing meets WCAG AA (4.5:1
   small text, 3:1 large). Contrast is a build requirement, not a nice-to-have.
5. **Carbon is efficient** — density first. Data tables, compact rows, inline
   editing: a person uses this tool all day, so respect their time and pixels.
6. **Empathy through restraint** — color is rationed. Gray does the organizing,
   one blue does the acting, support colors appear only to communicate status.

## Color

Gray runs the show; blue acts; everything else signals status. Confidence:
✅ official/documented · 🟡 cross-referenced · ⚠️ community approximation.

**Core palette (IBM Design Language, official steps):**

| Token step | Hex | Role |
|---|---|---|
| White | `#ffffff` ✅ | lightest bg / text on dark |
| Gray 10 | `#f4f4f4` ✅ | light theme bg (g10) |
| Gray 20 | `#e0e0e0` ✅ | hover layer light / borders |
| Gray 30 | `#c6c6c6` ✅ | disabled elements light |
| Gray 40 | `#a8a8a8` ✅ | placeholder text |
| Gray 50 | `#8d8d8d` ✅ | secondary icons |
| Gray 60 | `#6f6f6f` ✅ | secondary text light |
| Gray 70 | `#525252` ✅ | primary icons light |
| Gray 80 | `#393939` ✅ | primary text dark themes |
| Gray 90 | `#262626` ✅ | g90 bg |
| Gray 100 | `#161616` ✅ | g100 bg / primary text light |
| Blue 60 | `#0f62fe` ✅ | **the** interactive/action color |
| Blue 70 | `#0353e9` 🟡 | primary action hover |
| Blue 80 | `#002d9c` 🟡 | primary action active |
| Red 60 | `#da1e28` 🟡 | error / destructive |
| Green 60 | `#24a148` 🟡 | success |
| Yellow 30 | `#f1c21b` 🟡 | warning |
| Blue 40 | `#78a9ff` 🟡 | links/info on dark themes |

**Themes (named after their background):**

| Theme | `$background` | `$layer-01` | `$text-primary` | `$text-secondary` | `$border-subtle` |
|---|---|---|---|---|---|
| White | `#ffffff` ✅ | `#f4f4f4` ✅ | `#161616` ✅ | `#525252` ✅ | `#e0e0e0` ✅ |
| Gray 10 (g10) | `#f4f4f4` ✅ | `#ffffff` ✅ | `#161616` 🟡 | `#525252` 🟡 | `#e0e0e0` 🟡 |
| Gray 90 (g90) | `#262626` ✅ | `#393939` 🟡 | `#f4f4f4` 🟡 | `#c6c6c6` 🟡 | `#525252` 🟡 |
| Gray 100 (g100) | `#161616` ✅ | `#262626` 🟡 | `#f4f4f4` 🟡 | `#c6c6c6` 🟡 | `#393939` 🟡 |

Layering rule ✅: in light themes layers alternate White ↔ Gray 10; in dark
themes each layer goes one step lighter. Never place a component darker than
its background (outside of deliberate high-contrast moments).

**Key semantic tokens:** `$interactive`/`$link-primary` = Blue 60 ✅;
`$focus` = Blue 60 on light themes, White on dark ✅; focus ring is always
2px solid ✅; `$button-primary` = `#0f62fe`, hover `#0353e9`, disabled = gray
family regardless of base color ✅; `$field-01` input backgrounds sit one
layer up from `$background` ✅.

## Typography

Typeface: **IBM Plex Sans** (UI + prose) and **IBM Plex Mono** (code, data
identifiers, numeric readouts). Both on Google Fonts. No other families —
Plex Serif appears only for pull quotes.

Carbon's type sets are named by intent, not size. Key ones ✅ (size /
line-height / weight):

| Set | px / line-height | Weight | Use |
|---|---|---|---|
| `caption-01` | 12 / 16 | 400, +0.32px tracking | captions, timestamps |
| `label-01` | 12 / 16 | 400, +0.32px tracking | field labels, helper labels |
| `body-short-01` | 14 / 18 | 400 | dense body, table cells |
| `body-01` | 14 / 20 | 400 | default body text |
| `body-02` | 16 / 24 | 400 | long-form reading |
| `productive-heading-01` | 14 / 18 | 600 | section headings, table headers |
| `productive-heading-02` | 16 / 22 | 600 | card/tile headings |
| `productive-heading-03` | 20 / 28 | 400 | page subheads |
| `expressive-heading-01` | 20 / 26 | 600 | marketing-flavored heads 🟡 |
| `display-01` | 54 / 60 | 300 | hero numbers, marketing 🟡 |
| `code-01` | 12 / 16 | 400 mono | code snippet body 🟡 |
| `code-02` | 14 / 20 | 400 mono | code blocks 🟡 |

Rules: 14px is the working body size (not 16) ✅. Uppercase labels get
+0.32px letter-spacing ✅. Headings rarely exceed 600 weight — authority comes
from size and gray, not boldness.

## Layout & spacing

- **Base unit:** the mini-unit is 8px ✅. Spacing tokens:
  `$spacing-01: 2px, -02: 4px, -03: 8px, -04: 12px, -05: 16px, -06: 24px,
  -07: 32px, -08: 40px, -09: 48px, -10: 64px, -11: 80px, -12: 96px,
  -13: 160px` ✅. Everything aligns to this scale — no 10px or 14px gaps.
- **Grid:** 16-column fluid grid ✅, max content width 1584px (99rem) 🟡,
  32px gutters on desktop, 16px on mobile 🟡. Carbon's grid is called the
  "2x grid" — all spacing derives from 2× multiples of the mini-unit ✅.
- **Radius:** components are square — 0px radius on buttons, tiles, inputs,
  notifications ✅. (Expressive contexts may go larger; productive UI does not.)
- **Shadows:** effectively none — depth comes from the gray layering model,
  not elevation ✅.
- **Dividers:** 1px `$border-subtle` rules separate sections; whitespace +
  layer shifts do the rest ✅.
- **UI shell chrome:** 48px (3rem) fixed header ✅; side nav is a 48px icon
  rail when collapsed, 256px (16rem) when expanded 🟡.

## Components

Copy-pasteable HTML/CSS (theme vars switch per theme; shown values = White theme).

### 1. UI shell header (48px, dark gray-100 even on light pages)

```html
<header class="shell">
  <button class="shell-menu" aria-label="Menu">
    <svg viewBox="0 0 16 16" width="20" height="20"><path d="M2 4h12M2 8h12M2 12h12" stroke="currentColor" stroke-width="1.5"/></svg>
  </button>
  <span class="shell-brand">Meridian<strong>Console</strong></span>
  <div class="shell-search"><input type="search" placeholder="Search resources"></div>
  <div class="shell-actions">
    <button class="icon-btn" aria-label="Notifications"><svg viewBox="0 0 16 16" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M8 2a4 4 0 0 0-4 4v2.4L2.8 11h10.4L12 8.4V6a4 4 0 0 0-4-4z"/><path d="M6.6 13a1.4 1.4 0 0 0 2.8 0"/></svg></button>
    <button class="avatar" aria-label="Account">RK</button>
  </div>
</header>
<style>
.shell{display:flex;align-items:center;height:48px;background:#161616;color:#f4f4f4;padding:0 16px;gap:16px}
.shell-brand{font:600 14px/18px 'IBM Plex Sans',sans-serif;letter-spacing:.02em}
.shell-brand strong{font-weight:400}
.shell-search{margin-left:auto}
.shell-search input{width:288px;height:32px;background:#393939;border:0;color:#f4f4f4;padding:0 12px;font:400 14px 'IBM Plex Sans',sans-serif}
.shell-search input::placeholder{color:#a8a8a8}
.icon-btn{background:none;border:0;color:#f4f4f4;cursor:pointer;padding:8px}
.icon-btn:hover{background:#353535}
.avatar{width:32px;height:32px;border-radius:50%;background:#0f62fe;color:#fff;border:0;font:600 12px 'IBM Plex Sans',sans-serif;cursor:pointer}
</style>
```

### 2. Data table (the signature component — 48px normal rows)

```html
<table class="data-table">
  <thead><tr>
    <th><input type="checkbox" aria-label="Select all"></th>
    <th>Name</th><th>Status</th><th class="num">CPU</th><th class="num">Memory</th>
  </tr></thead>
  <tbody>
    <tr><td><input type="checkbox"></td><td>api-gateway-01</td>
      <td><span class="tag tag-green">Running</span></td>
      <td class="num">34%</td><td class="num">7.2 GB</td></tr>
  </tbody>
</table>
<style>
.data-table{width:100%;border-collapse:collapse;font:400 14px/18px 'IBM Plex Sans',sans-serif}
.data-table thead th{background:#e0e0e0;color:#161616;font-weight:600;text-align:left;
  padding:0 16px;height:48px;border-bottom:1px solid #c6c6c6;white-space:nowrap}
.data-table tbody td{padding:0 16px;height:48px;border-bottom:1px solid #e0e0e0;color:#161616}
.data-table tbody tr:hover{background:#f4f4f4}
.data-table .num{text-align:right;font-family:'IBM Plex Mono',monospace}
</style>
```

Row heights by density ✅: tall 64px · normal 48px · short 32px · compact 24px.
Zebra striping is not used; hover is `$layer-hover` gray.

### 3. Tile (clickable card, layer-01, no shadow)

```html
<a class="tile" href="#">
  <p class="tile-label">Clusters</p>
  <p class="tile-value">14</p>
  <p class="tile-sub">3 regions · all healthy</p>
</a>
<style>
.tile{display:block;background:#f4f4f4;padding:16px;text-decoration:none;color:#161616;min-width:0}
.tile:hover{background:#e8e8e8}
.tile-label{font:400 12px/16px 'IBM Plex Sans',sans-serif;letter-spacing:.32px;color:#525252;margin:0 0 8px}
.tile-value{font:400 28px/36px 'IBM Plex Sans',sans-serif;margin:0}
.tile-sub{font:400 12px/16px 'IBM Plex Sans',sans-serif;color:#525252;margin:8px 0 0}
</style>
```

### 4. Tabs (underline style, blue-60 active indicator)

```html
<div class="tabs" role="tablist">
  <button class="tab is-active" role="tab" aria-selected="true">Overview</button>
  <button class="tab" role="tab" aria-selected="false">Activity</button>
  <button class="tab" role="tab" aria-selected="false">Settings</button>
</div>
<style>
.tabs{display:flex;border-bottom:1px solid #e0e0e0;gap:4px}
.tab{background:none;border:0;border-bottom:2px solid transparent;margin-bottom:-1px;
  padding:12px 16px;font:400 14px/18px 'IBM Plex Sans',sans-serif;color:#525252;cursor:pointer}
.tab:hover{color:#161616;border-bottom-color:#c6c6c6}
.tab.is-active{color:#161616;border-bottom-color:#0f62fe;font-weight:600}
</style>
```

### 5. Accordion

```html
<details class="accordion">
  <summary>Network configuration <span class="chev">▾</span></summary>
  <div class="accordion-body">VPC <code>meridian-prod</code>, subnets in 3 zones, egress via NAT gateway.</div>
</details>
<style>
.accordion{border-top:1px solid #e0e0e0;border-bottom:1px solid #e0e0e0}
.accordion summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;
  padding:16px;font:600 14px/18px 'IBM Plex Sans',sans-serif;color:#161616}
.accordion summary::-webkit-details-marker{display:none}
.accordion[open] .chev{transform:rotate(180deg)}
.accordion-body{padding:0 16px 16px;font:400 14px/20px 'IBM Plex Sans',sans-serif;color:#525252}
</style>
```

### 6. Notifications (inline + toast)

```html
<div class="notification notification-info" role="status">
  <strong>Deployment queued.</strong> api-gateway-01 will restart with zero downtime.
  <button aria-label="Dismiss">✕</button>
</div>
<style>
.notification{display:flex;gap:12px;align-items:flex-start;border-left:3px solid #0f62fe;
  background:#f4f4f4;padding:12px 16px;font:400 14px/20px 'IBM Plex Sans',sans-serif;color:#161616}
.notification-error{border-color:#da1e28}.notification-success{border-color:#24a148}.notification-warning{border-color:#f1c21b}
.notification button{margin-left:auto;background:none;border:0;cursor:pointer;color:#525252;font-size:14px}
</style>
```

Toasts slide in bottom-right, same structure, `$layer-01` bg.

### 7. Tag (status pill — the system's one rounded control)

```html
<span class="tag tag-red">Failed</span>
<span class="tag tag-blue">Provisioning</span>
<style>
.tag{display:inline-flex;align-items:center;min-height:24px;padding:0 8px;
  font:400 12px/16px 'IBM Plex Sans',sans-serif;letter-spacing:.32px;border-radius:16px}
.tag-red{background:#ffd7d9;color:#750e13}.tag-magenta{background:#ffd6e8;color:#740937}
.tag-purple{background:#e8daff;color:#491d8b}.tag-blue{background:#d0e2ff;color:#002d9c}
.tag-cyan{background:#bae6ff;color:#003a6d}.tag-teal{background:#9ef0f0;color:#004144}
.tag-green{background:#defbe6;color:#044317}.tag-gray{background:#e0e0e0;color:#161616}
.tag-coolgray{background:#dde1e6;color:#121619}.tag-warmgray{background:#e5e0df;color:#171414}
.tag-hc{background:#393939;color:#f4f4f4}
</style>
```

✅ sizes sm 18 / md 24 (default) / lg 32px; inline padding `$spacing-03` (8px).
The 16px radius is a fixed token — on short labels it reads as a pill, but it
is not a dynamic capsule. Dark themes swap bg/text per the tag token pairs
(e.g. dark red: `#a2191f` / `#ffd7d9`). Carbon v11 has no amber/yellow tag —
use red/magenta/purple/blue/cyan/teal/green/grays only. 🟡 exact dark-theme
tints: verify against `@carbon/styles` before shipping a theme.

### 8. Code snippet (Plex Mono, layer-01, copy button)

```html
<div class="code-snippet">
  <pre><code>kubectl get pods -n meridian-prod</code></pre>
  <button class="copy-btn" aria-label="Copy"><svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="6" y="6" width="7.5" height="7.5"/><path d="M10 6V2.5H2.5V10H6"/></svg></button>
</div>
<style>
.code-snippet{display:flex;align-items:center;background:#f4f4f4;padding:12px 16px;gap:12px}
.code-snippet pre{margin:0;flex:1;font:400 12px/16px 'IBM Plex Mono',monospace;color:#161616;white-space:pre-wrap}
.copy-btn{background:none;border:0;cursor:pointer;color:#525252;font-size:16px}
.copy-btn:hover{color:#161616;background:#e0e0e0}
</style>
```

### 9. Buttons

```html
<button class="btn btn-primary">Deploy cluster</button>
<button class="btn btn-secondary">Save draft</button>
<button class="btn btn-danger">Delete</button>
<style>
.btn{height:48px;padding:0 32px;border:1px solid transparent;cursor:pointer;
  font:400 14px/18px 'IBM Plex Sans',sans-serif}
.btn-primary{background:#0f62fe;color:#fff}
.btn-primary:hover{background:#0353e9}
.btn-primary:active{background:#002d9c}
.btn-secondary{background:transparent;border-color:#0f62fe;color:#0f62fe}
.btn-secondary:hover{background:#0f62fe;color:#fff}
.btn-danger{background:#da1e28;color:#fff}
.btn-danger:hover{background:#ba1b23}
.btn:disabled{background:#c6c6c6;color:#8d8d8d;cursor:not-allowed}
</style>
```

Buttons are 48px tall with 16px horizontal padding for primary actions (small
variant: 32px) 🟡. Tertiary/ghost buttons are text-only with blue-60 text.

### 10. Form field

```html
<label class="field"><span>Cluster name</span>
  <input type="text" value="meridian-prod" placeholder="e.g. meridian-prod">
  <em>Lowercase letters, numbers and hyphens only.</em>
</label>
<style>
.field span{display:block;font:400 12px/16px 'IBM Plex Sans',sans-serif;letter-spacing:.32px;color:#525252;margin-bottom:8px}
.field input{width:100%;height:40px;background:#f4f4f4;border:0;border-bottom:1px solid #8d8d8d;
  padding:0 16px;font:400 14px/18px 'IBM Plex Sans',sans-serif;color:#161616}
.field input:focus{outline:2px solid #0f62fe;outline-offset:-2px}
.field em{display:block;font-style:normal;font:400 12px/16px 'IBM Plex Sans',sans-serif;color:#525252;margin-top:8px}
</style>
```

Inputs are square with a 1px bottom border (`$border-strong`); focus is the
2px `$focus` outline ✅.

### 11. Overflow menu (row actions)

```html
<div class="ovf">
  <button class="icon-btn-row" aria-label="Open actions menu" aria-expanded="false">
    <svg viewBox="0 0 16 16" width="16" height="16"><circle cx="8" cy="3" r="1.3" fill="currentColor"/><circle cx="8" cy="8" r="1.3" fill="currentColor"/><circle cx="8" cy="13" r="1.3" fill="currentColor"/></svg>
  </button>
  <div class="ovf-menu" hidden>
    <button>View details</button>
    <button>Upgrade cluster</button>
    <button>Restart worker nodes</button>
    <hr>
    <button class="danger">Delete cluster</button>
  </div>
</div>
<style>
.ovf{position:relative;display:inline-flex}
.ovf-menu{position:absolute;right:0;top:36px;min-width:208px;background:#ffffff;
  border:1px solid #e0e0e0;z-index:40;padding:4px 0}
.ovf-menu button{display:flex;width:100%;background:none;border:0;height:40px;padding:0 16px;
  font:400 14px/18px 'IBM Plex Sans',sans-serif;color:#161616;cursor:pointer;text-align:left}
.ovf-menu button:hover{background:#f4f4f4}
.ovf-menu button.danger{color:#da1e28}
.ovf-menu hr{border:0;border-top:1px solid #e0e0e0;margin:4px 0}
</style>
```

Menu floats on `$layer-01` with a 1px `$border-subtle` edge — no shadow ✅.
Danger actions sit below a divider, in `$support-error` text. One menu open
at a time; Escape and outside-click close it.

### 12. Modal (dialog)

```html
<div class="modal-overlay">
  <div class="modal" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
    <div class="modal-head">
      <div><h2 id="modalTitle">Create cluster</h2>
      <p class="modal-sub">Billing starts when the first worker node is ready.</p></div>
      <button class="n-close" aria-label="Close dialog"><svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 4l8 8M12 4l-8 8"/></svg></button>
    </div>
    <div class="modal-body"><!-- form fields go here --></div>
    <div class="modal-foot">
      <button class="btn btn-secondary">Cancel</button>
      <button class="btn btn-primary">Create cluster</button>
    </div>
  </div>
</div>
<style>
.modal-overlay{position:fixed;inset:0;background:rgba(22,22,22,.5);z-index:100;
  display:flex;align-items:flex-start;justify-content:center;padding:64px 16px 16px}
.modal{background:#ffffff;width:640px;max-width:100%;color:#161616}
.modal-head{display:flex;justify-content:space-between;gap:16px;padding:24px 24px 0}
.modal-head h2{font:400 20px/28px 'IBM Plex Sans',sans-serif;margin:0 0 8px}
.modal-sub{font:400 14px/20px 'IBM Plex Sans',sans-serif;color:#525252;margin:0}
.modal-body{padding:24px}
.modal-foot{display:flex;justify-content:flex-end;gap:8px;padding:16px 24px 24px}
</style>
```

Sizes: sm 448 / md 640 / lg 960px 🟡. Overlay is flat 50% gray-100 — never a
blur or gradient. Focus the first field on open; Escape and overlay-click
close. Footer buttons are right-aligned, primary last.

## Motion

Two modes, never bouncy ✅. **Productive** = fast, functional, default for
everything. **Expressive** = slower, reserved for rare important moments.

| Curve | Productive ✅ | Expressive ✅ |
|---|---|---|
| Standard (visible start→end) | `cubic-bezier(0.2, 0, 0.38, 0.9)` | `cubic-bezier(0.4, 0.14, 0.3, 1)` |
| Entrance (appearing) | `cubic-bezier(0, 0, 0.38, 0.9)` | `cubic-bezier(0, 0, 0.3, 1)` |
| Exit (leaving) | `cubic-bezier(0.2, 0, 1, 0.9)` | `cubic-bezier(0.4, 0.14, 1, 1)` |

Durations ✅: `fast-01: 70ms` (micro-interactions, hover) · `fast-02: 110ms`
(small reveals) · `moderate-01: 150ms` (standard transitions) ·
`moderate-02: 240ms` (larger expansions) · `slow-01: 400ms` (large expansions,
important moments) · `slow-02: 700ms` (background dimming, page-level).

Rules: entrance decelerates into place; exit accelerates away (a leaving
element doesn't need watching) ✅. Duration scales with distance — a tall
panel gets more time than a short one so both feel equally quick ✅.
Never `linear`, generic `ease`, or anything suggesting bounce/stretch ✅.

```css
.tile{transition:max-height 240ms cubic-bezier(0.2, 0, 0.38, 0.9)}
.notification{animation:slide-in 110ms cubic-bezier(0, 0, 0.38, 0.9)}
```

## Do / Don't

- ✅ Do layer surfaces: white page → gray-10 tiles → white nested panels.
  ❌ Don't add drop shadows to fake depth — gray steps are the depth system.
- ✅ Do use one Blue 60 for every action (buttons, links, active tab
  indicators, focus). ❌ Don't introduce a second accent color for "variety".
- ✅ Do keep corners square (0px) on productive components.
  ❌ Don't round buttons/inputs "to feel friendly" — that breaks the system.
- ✅ Do write labels in sentence case, 12px, +0.32px tracking, gray-70.
  ❌ Don't use all-caps bold labels at 11px like a marketing site.
- ✅ Do use the data table for everything tabular with 48/32/24px density
  rows. ❌ Don't build "cards with stats" when a table answers the question.
- ✅ Do show status with tags + support colors only on the status element.
  ❌ Don't tint whole rows/panels green or red.
- ✅ Do make disabled states gray-on-gray with no hover.
  ❌ Don't keep the blue and lower opacity — disabled is always the gray family.
- ✅ Do animate state changes with productive standard/entrance curves.
  ❌ Don't spring, bounce, or fade-slow anything in a tool used all day.

## Copy voice

One line: Carbon copy is plain, precise, and instructional — it tells the
operator exactly what will happen, no marketing adjectives. Example strings:
"Deploying restarts each node with zero downtime." / "3 of 14 clusters need
attention." / "Enter the cluster name. It can't be changed later."
