---
name: gpui-style
description: >-
  Style GPUI applications with semantic color pairs, region surfaces, consistent
  typography and radii, and interaction states. Use when adding or reviewing GPUI
  styling, themes, dark mode, palettes, or design systems, including requests to
  style a panel, button, or sidebar. Adapt to the app's existing theme and the
  requested scope; the supplied shadcn-inspired Theme scaffold is optional.
---

# GPUI theming with semantic design tokens

The supplied scaffold adapts shadcn/ui's token model to GPUI: render code names
semantic roles, and the `Theme` global supplies their values. Use those roles
with the app's existing design system, or adopt this scaffold when a new theme
system fits the request.

## Prefer semantic tokens

Use the app's existing theme for shared colors, radii, and typography. The supplied
system exposes these through `cx.theme()`; another system may use different names
or accessors. Preserve those conventions and the user's requested design.

When using this scaffold, prefer tokens over repeated `rgb(...)`, `.rounded_md()`,
or `.text_sm()` values in render code. Fixed GPUI helpers do not follow the theme's
radius or type scale. A local styling change does not require introducing a full
theme system or migrating unrelated components.

## Workflow

1. **Check for an existing theme.** Inspect imports, style helpers, and globals (`rg -n 'impl.*Global for|trait.*Theme' src/`). If one exists, use it and match its naming.
2. **If none exists**, match the task's scope. For a new theme system, use [theme-module.md](references/theme-module.md) as a starting point. For a local change, follow nearby styles or introduce only the shared tokens needed.
3. **Identify the region** you are rendering into. For the supplied scaffold, pick its surface from §3; otherwise use the app's equivalent roles.
4. **Reuse theme values**, following the pairing, state, and shape/type guidance in §2, §4, and §5 as applicable.
5. **Self-check** against §7 before finishing.

## 1. The supplied token set

The names below match the reference module. Keep its examples consistent when
adopting it; map the roles onto existing names when working in another system.

Colors are `gpui::Hsla`. Tokens divide into **per-surface** tokens (they differ by region) and **global** tokens (identical everywhere).

**Per-surface** — the `Surface` struct, one instance per region:

| Field | Role |
|---|---|
| `bg` | the surface itself |
| `fg` | primary text and icons on it |
| `muted_fg` | secondary text on it: captions, placeholders, help text, timestamps |
| `border` | separating lines drawn on it: edges, dividers, rules |
| `accent` / `accent_fg` | hover / selected background for rows and ghost controls on it |
| `primary` / `primary_fg` | the emphasis action as it appears on it |
| `ring` | focus indicator on it |

**Global** — the `Theme` struct:

| Field | Role |
|---|---|
| `secondary` / `secondary_fg` | filled but non-committal control (secondary button) |
| `muted` | inert tinted fill: table headers, code blocks, skeletons, wells |
| `destructive` / `destructive_fg` | danger: delete actions, error state |
| `input` | border color of form controls (usually `border`, split out so fields can be more or less prominent than dividers) |
| `chart[5]` | ordered categorical series for data viz |
| `radius` | one base length; the whole scale derives from it |
| `font` | family + size scale |

**Derived state fields** (`primary_hover`, `primary_active`, `ring_focus`, `destructive_subtle`, …) are computed by `ThemeSpec::resolve()` in this scaffold. Keep that policy in the resolver instead of recomputing it in each component. See §4.

Notes on the roles that are easy to get wrong:

- `muted_fg` is the second-most-used token in a real app. Every caption, placeholder, and secondary label. There is no third gray — if text is not `fg` it is `muted_fg`.
- `secondary` is *a variant you choose*; `accent` is *a state that happens to you* (hover, selection). They often have similar values; they are not interchangeable in code.
- `ring` is separate from `primary` so focus visibility survives any brand color change.
- There is deliberately no `success`/`warning`/`info`. Add them only if the app needs them, and add them as full `(color, fg, subtle)` triples matching `destructive`.

## 2. The pairing convention (the load-bearing rule)

> Every token that paints a **surface** ships with the foreground that sits **on** it. Set both, from the same pair, in the same builder chain.

```rust
let t = cx.theme();
let s = t.surface(surface_kind); // surface_kind: SurfaceKind

// correct — pair set together
div().bg(s.primary).text_color(s.primary_fg)

// wrong — foreground from a different pair, contrast not guaranteed
div().bg(s.primary).text_color(s.fg)

// wrong — a surface color used as text
div().text_color(s.primary)
```

Pairing preserves the palette's intended contrast without components knowing its
colors. Validate the authored pairs in both modes; pairing alone does not ensure
that the chosen colors have sufficient contrast.

`border`, `input`, and `ring` have no foreground pair — they are line colors, never surfaces.

`.text_color()` cascades to text children, so set it on the container that owns the surface.
**SVG icons are an exception:** set `.text_color(...)` directly on every `svg()` using the appropriate
theme foreground token. Without its own color, the SVG renderer skips drawing the icon, even when
the asset is bundled correctly. Parent hover colors do not recolor SVGs either; apply the hover token
on the SVG via `.group_hover(...)` (see the [icon-button recipe](references/component-recipes.md#icon-button)).

## 3. Regions → surfaces (GPUI has no CSS cascade, so this is explicit)

CSS gets region-scoped theming free from the cascade. GPUI does not, so a surface is passed explicitly. `Theme::surface(SurfaceKind)` returns the right one.

| What you are rendering | `SurfaceKind` | Also apply |
|---|---|---|
| Window root, main content area, editor pane | `App` | — |
| Panel, settings group, list container, dialog body, card | `Card` | `border_1` + `border_color(s.border)`, `rounded(t.radius.lg())` |
| Dropdown, context menu, tooltip, popover, command palette, autocomplete | `Popover` | `border_1`, `rounded(t.radius.md())`, `shadow_lg()` |
| Left nav rail, activity bar, file tree, project panel, tab strip | `Sidebar` | `border_r_1` + `border_color(s.border)` |
| Titlebar, toolbar, status bar | `Sidebar` | chrome shares the nav palette by default |
| Modal scrim | — | `hsla(0., 0., 0., 0.5)` — the one allowed literal, or `t.scrim` |

The supplied palette expresses elevation through surface color and reserves
shadows for floating layers such as popovers and modals. Preserve an existing
app's elevation conventions when they differ; a card restyle need not redesign
the rest of the application.

Component signature convention: stateless components take the surface they render onto.

```rust
#[derive(IntoElement)]
struct Button { label: SharedString, variant: ButtonVariant, on: SurfaceKind }

impl Button {
    fn new(label: impl Into<SharedString>) -> Self {
        Self { label: label.into(), variant: ButtonVariant::Secondary, on: SurfaceKind::App }
    }
    fn on(mut self, kind: SurfaceKind) -> Self { self.on = kind; self }
}
```

Default to `SurfaceKind::App`; a container that owns a non-default surface passes it down. This replaces shadcn's flat `--sidebar-*` prefix hack with one structure that works for any region.

## 4. Derived states in the supplied scaffold

`resolve()` computes interaction states from base tokens. Adjust the shared
derivation policy when adopting this scaffold; use the existing state tokens
when working in another theme system.

Base `primary`/`primary_fg` tokens live on `Surface` (`s`). The supplied module's
derived `primary_hover`/`primary_active` tokens live on `Theme` (`t`) and are shared
across regions: `resolve()` derives them using `app.bg`. If a design requires
distinct primary colors or state derivation per region, extend `Surface` and the
resolver together instead of mixing region-specific bases with global states.

| State | Rule |
|---|---|
| **Hover, filled** | `state_shift(base, app.bg, d.hover_shift)` → `t.primary_hover`, `t.secondary_hover`, `t.destructive_hover`; default HSL lightness shift is `0.05` |
| **Hover, transparent** (ghost button, menu row, list item) | paint `s.accent` behind it; text becomes `s.accent_fg` |
| **Active / pressed** | `state_shift(base, app.bg, d.active_shift)` → `t.primary_active`, `t.secondary_active`; default shift is `0.09`. The destructive recipe reuses `t.destructive_hover`. |
| **Selected** | `s.accent` + `s.accent_fg`, persistent (not a hover style) |
| **Focus** | `s.ring` at 50% alpha as a 3px spread box-shadow — `t.ring_focus`; apply while focused |
| **Disabled** | `.opacity(0.5)` on the whole element + drop the click handler + `.cursor_default()`. One rule for every component; no disabled color tokens. |
| **Invalid** | `.border_color(t.destructive)` + focus ring becomes `t.destructive_ring` |
| **Subtle status fill** | `t.destructive_subtle` (destructive at ~10–15% alpha) for error banners |

In GPUI these are style closures on a stateful `div()`:

```rust
let t = cx.theme();
let s = t.surface(SurfaceKind::App);

div()
    .id("save")
    .px_3().py_1p5()
    .rounded(t.radius.md())
    .bg(s.primary).text_color(s.primary_fg)
    .hover(|st| st.bg(t.primary_hover))
    .active(|st| st.bg(t.primary_active))
    .cursor_pointer()
```

`.hover()` needs no id; `.active()` and `.focus()` require `.id(...)` (it turns `Div` into `Stateful<Div>`).

Focus styling does not itself establish keyboard navigation. Preserve or provide
the intended focus handle (`.track_focus(&handle)`), tab order (`.tab_index(...)`),
and Tab/Shift-Tab routing through the app's navigation policy.
On revisions that provide it, `.focus_visible(...)` restricts a style to focus
from keyboard navigation; `.focus(...)` also applies after pointer focus.

Focus ring recipe — GPUI has no CSS `outline`, so use a zero-blur spread shadow, which does not affect layout:

```rust
use gpui::{BoxShadow, point, px};
.focus(|st| st.shadow(smallvec::smallvec![BoxShadow {
    color: t.ring_focus,
    offset: point(px(0.), px(0.)),
    blur_radius: px(0.),
    spread_radius: px(3.),
}]).border_color(t.app.ring))
```

`state_shift` moves toward the background for strongly contrasting fills and away
for low-contrast fills, keeping the state change visible. Deriving once in
`resolve()` keeps that policy in one place and makes it tunable (see §6).

## 5. Shape and type

**Radius is one number.** The scale derives from it by fixed multipliers, so `radius: px(0.)` makes the whole app sharp and `px(16.)` softens it, proportionally, in one edit.

```rust
t.radius.sm()   // base * 0.6
t.radius.md()   // base * 0.8
t.radius.lg()   // base       ← the default for cards and panels
t.radius.xl()   // base * 1.4
```

With this scaffold, use `.rounded(t.radius.md())`; `.rounded_md()` and
`.rounded_lg()` are fixed constants that ignore its radius setting. Keep fixed
helpers when they are an intentional convention of the existing design.

Rough assignment: badges/inputs/buttons `md`, cards/panels/popovers `lg`, small chips `sm`, avatars `.rounded_full()`.

**Type.** GPUI's `.text_sm()`/`.text_base()` constants are usable but do not follow the theme's font settings, so route sizes through the theme too:

```rust
.font_family(t.font.sans.clone())
.text_size(t.font.sm)
.line_height(t.font.line_height_normal)
```

Weight comes from `FontWeight::{NORMAL, MEDIUM, SEMIBOLD}` directly — not a token. Monospace content uses `t.font.mono`.

**Spacing is not tokenized.** Use GPUI's numeric scale (`.p_2()`, `.gap_3()`, `.px_4()`) — it is already Tailwind's 0.25rem step and is consistent by construction. Adding spacing tokens buys nothing and enlarges the authoring surface.

## 6. Scaffold conventions and configuration

| Supplied scaffold conventions | Configured by the developer |
|---|---|
| Token names and roles (§1) | The ~24 base color values |
| Surface/foreground pairing (§2) | `radius` base length |
| Region → surface mapping defaults (§3) | Font families and size scale |
| States are derived, not authored (§4) | Derivation constants (`hover_shift`, `active_shift`, `ring_alpha`, `disabled_opacity`) via `Derivation` |
| Radius derives from one base (§5) | Extra semantic colors (`success`/`warning`/`info`) |
| No literals in render code | Which surfaces diverge (sidebar can just clone `app`) |

**Two-layer design.** `ThemeSpec` is the small, `serde`-friendly authoring struct (base values only). `Theme` is the resolved struct held in the global (all tokens + derived states). `ThemeSpec::resolve(&Derivation) -> Theme` is the single place the design rules live.

That split is what makes both stories work:

- **Built-in presets** — ship `ThemeSpec::light()` / `ThemeSpec::dark()` constructors without exposing user configuration; these are ordinary functions, not const values.
- **Configurable at runtime** — deserialize `ThemeSpec` from a TOML/JSON settings file, `resolve()`, `cx.set_global(theme)`.

Either way components are identical, because they only ever see the resolved `Theme`.

**Light and dark are two independently authored `ThemeSpec`s, not one spec plus an invert.** A chroma that reads as confident on white vibrates on near-black: dark themes raise the brand's lightness and *lower* its chroma, and compress the whole lightness range. Never generate dark mode by flipping lightness.

## 7. Self-check before finishing

Apply these checks to the changed components and the theme system in use. The
field names and strict token conventions below describe the supplied scaffold;
they do not require an app-wide migration for a local fix.

- [ ] Shared visual values reuse the theme; intentional local exceptions follow the project's conventions.
- [ ] Every `.bg()` on a surface has a matching `.text_color()` from the same pair.
- [ ] Every `svg()` has its own theme-based `.text_color(...)`; any hover recoloring is applied directly to the SVG too.
- [ ] Radius and text sizes follow the chosen theme or existing design conventions.
- [ ] Secondary text uses the appropriate semantic role (`s.muted_fg` in this scaffold).
- [ ] The region uses the surface from §3's table, and its border comes from that surface.
- [ ] Interactive elements have hover, active, focus, and disabled handled per §4 — not just hover.
- [ ] Elevation follows the app's conventions; the supplied scaffold uses color + border for cards.
- [ ] The view redraws on theme change (`cx.observe_global::<Theme>(|_, cx| cx.notify()).detach()` in the root view's constructor).

**Auditing an existing codebase:**

```bash
rg -n 'rgb\(0x|rgba\(0x|hsla\(' src/ --glob '!**/theme*'
rg -n '\.rounded_(sm|md|lg|xl|2xl|3xl)\(\)' src/
rg -n '\.text_(xs|sm|base|lg|xl)\(\)' src/
```

## References

Load these as needed — do not read all three up front.

| File | Read when |
|---|---|
| `references/theme-module.md` | Scaffolding the theme: complete `theme.rs` with `Theme`/`ThemeSpec`/`Surface`/`Derivation`, the `Global` impl, the `ActiveTheme` extension trait, OKLCH→`Hsla` conversion, contrast validation, and light/dark switching. |
| `references/component-recipes.md` | Building or restyling a specific widget: button variants, input, card, list row, menu, sidebar, badge, table, modal, tooltip — each as correct token usage. |
| `references/authoring-themes.md` | Choosing actual color values: the decision checklist in dependency order, the OKLCH lightness ladder, dark-mode adjustment rules, and a worked light/dark pair. |

## Ground truth

GPUI is pre-1.0 and its APIs move between commits. Before relying on any nontrivial signature (`Hsla` helpers, `BoxShadow` fields, `refresh_windows`, `WindowAppearance`), verify against the pinned revision — the vendored checkout under `~/.cargo/git/checkouts/zed-*/<rev>/crates/gpui/src/` is authoritative. The reference implementation defines its own `alpha`/`state_shift` helpers to reduce dependence on `Hsla`'s inherent methods; compile-check the module and representative consumers against the project's pin.
