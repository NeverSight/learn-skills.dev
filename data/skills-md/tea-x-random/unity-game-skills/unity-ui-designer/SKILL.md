---
name: unity-ui-designer
description: "Design verified, screenshot-proven UI for casual iOS games in Unity. Use for HUD, menus, overlays, pause/win/lose/settings/level-select screens, title/menu, buttons, score/coin/lives/timer readouts, store/IAP placeholder, reward popups, responsive portrait layout, safe area/notch and home-indicator handling, touch controls, 44pt touch targets, thumb-reachable zones, typography, TextMeshPro, UI Toolkit (UXML/USS), uGUI Canvas/RectTransform, Canvas Scaler, and mobile portrait UI. Builds UI through the unity-mcp-bridge (manage_ui for UI Toolkit, manage_gameobject + manage_components for uGUI), never raw YAML."
---

# Unity UI Designer

Make casual-iOS game UI intentional, readable, responsive, safe-area-correct, and touch-friendly — and prove it with a phone-resolution screenshot, not a design doc. This is the UI phase under `unity-game-director`; it executes through `unity-mcp-bridge`.

## Doctrine (these override convenience)

1. **Verified, screenshot-proven UI, not docs.** A UI screen is not "done" until a `manage_scene` screenshot at phone resolution shows it laid out, readable, and inside the safe area.
2. **Lean gates.** Decide sensible defaults (stack, reference resolution, font sizes) and proceed; only ask the user at real branch points (art direction, screen set scope).
3. **Build UI through MCP, never raw YAML.** `.unity`/`.prefab`/`.uxml`/`.uss` references are GUID/fileID-linked. Use `manage_ui` for UI Toolkit (UXML/USS), `manage_gameobject` + `manage_components` for uGUI. Enable the group first: `manage_tools(action="enable_group", group="ui")`. C# (SafeArea, juice) goes through the script tools and must compile clean.
4. **Branch on the project's UI stack.** Read `mcpforunity://project/info` and pick UI Toolkit vs uGUI/TMP from what the project already uses.

## Step 0 — Detect the UI stack

Read `mcpforunity://project/info` and check the UI stack flags:

- Project already uses **uGUI / TextMeshPro** (Canvas in scenes, `com.unity.textmeshpro` / `com.unity.ugui`) → build uGUI.
- Project uses / Unity 6 with **UI Toolkit runtime** (`com.unity.ui`, `.uxml`/`.uss` assets, UIDocument) → build UI Toolkit.
- **Greenfield UI on Unity 6 → default to UI Toolkit** (flexbox, percentage units, USS theming scale better across phones). Use uGUI when the project already standardized on it, or for world-space HUD and quick one-off overlays.

Enable the UI tool group before any UI Toolkit work: `manage_tools(action="enable_group", group="ui")` (this exposes `manage_ui`).

## Safe area / notch — MANDATORY for iOS

iPhones have a top notch/Dynamic Island and a bottom home indicator. Never anchor interactive or critical UI to raw screen edges.

- **uGUI:** put a `SafeArea` MonoBehaviour on a full-screen RectTransform that all HUD/menu content parents under, driving anchors from `Screen.safeArea`:

```csharp
using UnityEngine;
[RequireComponent(typeof(RectTransform))]
public class SafeArea : MonoBehaviour {
    RectTransform rt; Rect last; ScreenOrientation lastOri;
    void Awake() { rt = GetComponent<RectTransform>(); Apply(); }
    void Update() { if (Screen.safeArea != last || Screen.orientation != lastOri) Apply(); }
    void Apply() {
        last = Screen.safeArea; lastOri = Screen.orientation;
        Vector2 min = last.position, max = last.position + last.size;
        min.x /= Screen.width;  min.y /= Screen.height;
        max.x /= Screen.width;  max.y /= Screen.height;
        rt.anchorMin = min; rt.anchorMax = max;
        rt.offsetMin = Vector2.zero; rt.offsetMax = Vector2.zero;
    }
}
```

- **UI Toolkit:** apply safe-area padding to the root. Easiest: a small runtime helper that reads `Screen.safeArea` and sets `root.style.paddingTop/Bottom/Left/Right` in px (recompute on orientation/resolution change); keep visual padding in USS so content never touches the notch or home indicator.

## Responsive layout — portrait, many aspect ratios

Phones range ~19.5:9 (modern) to 4:3 (iPad). Never use absolute pixel positions.

- **uGUI Canvas Scaler:** `UI Scale Mode = Scale With Screen Size`, `Reference Resolution = 1080 x 1920`, `Screen Match Mode = Match Width Or Height`, `Match = 0.5` (start there; bias toward width for portrait-critical layouts). Anchor elements to corners/edges, not center-with-fixed-offset.
- **UI Toolkit:** flexbox (`flex-grow`, `flex-direction`, `justify-content`, `align-items`) + percentage / `vw`/`vh`-style sizing in USS. Let containers flex; avoid fixed px on layout containers (px is fine for borders/icons). Set the PanelSettings scale mode to scale-with-screen, reference resolution 1080x1920.

## Touch targets & thumb reach

- Minimum tappable size **~44x44 pt** (`>= ~88 px` at 1080-wide reference / 2x). Pad the hit area even if the icon is smaller.
- Spacing between adjacent buttons so a thumb does not hit two.
- Put primary actions in the **bottom thumb-reachable zone** for one-handed portrait play; reserve the top (under the notch) for passive readouts (score, coins, timer).

## Typography

- **uGUI: use TextMeshPro**, not legacy `Text` — it stays crisp when scaled. Generate SDF font assets for the chosen font.
- Legible body sizes; avoid tiny labels. Enable Auto Size within a sane min/max for numbers that grow (score, coins). Strong contrast (text vs panel vs world).
- One display font + one UI font max; consistent sizing scale across screens.
- **Type the scale, never the size.** Don't pass raw point sizes (`28`, `44`, `64`) into label factories — that's how typography drifts. Pick from a small *named* scale (Title/Heading/Body/Caption…) defined once. See "Design tokens" below — this is the #1 source of text inconsistency.

## Design tokens — one source of truth for a runtime-built UI (do this FIRST)

A casual game's look drifts when every screen sets its own font sizes, colors, paddings, and radii as magic numbers. The fix from established design-system practice ([USWDS design tokens](https://designsystem.digital.gov/design-tokens/), [Adobe Spectrum](https://spectrum.adobe.com/page/design-tokens/), [Material 3]): define a **token layer** — a curated palette of named values that *everything* references — instead of hard-coding values per widget. Tokens are "the smallest unit of a design decision… a single source of truth" ([UXPin](https://www.uxpin.com/studio/blog/what-are-design-tokens/)); the win is that restyling becomes a **one-place change** that updates every screen at once.

**Explicit input — when the project has an `art-spec.yaml`, the token PALETTE is derived from it, never invented here.** Read the spec's `palette.roles` (`ground`, `panel`, `ink`, `accent_primary`, `accent_secondary`) + palette arrays (canonical path + legacy roots: `docs/PIPELINE_CONVENTIONS.md`) and map them onto the theme's semantic color roles. `GameTheme.cs` color hexes MUST equal the art-spec hexes exactly — **colors only**; typography, spacing, and radii are GameTheme-native (no art-spec source) and stay owned here. No art-spec (exploratory/prototype): pick a deliberate palette, flag it as unlocked, and reconcile when the spec lands.

For a runtime-constructed Unity UI (no prefabs/UXML to centralize), the token layer is a **theme object** (a `GameTheme` ScriptableObject) referenced by the runtime builder (`AppRoot`). Put **all five token families** there, named, and reference them everywhere:

1. **Typography scale** — a small set of named sizes (NOT per-call literals). e.g. `Display=78, Title=56, Heading=44, Subhead=32, Body=30, Label=26, Caption=22`. Add weight roles if the font has them. Every label picks a role, never a number.
2. **Spacing scale** — a stepped rhythm (`xs=4, s=8, m=16, l=24, xl=32, xxl=48`) for padding/margins/gaps. Lay out from the scale so vertical rhythm is consistent across screens ([USWDS units](https://designsystem.digital.gov/design-tokens/)).
3. **Color roles (semantic, not raw)** — name by *role* not hue: `background`, `panel`, `textPrimary`, `textMuted`, `textOnColor`, `accent`, `danger`/`conflict`, `success`. Region/decorative palettes stay separate. Semantic naming means a re-skin changes the role's value once and every widget follows ([USWDS color](https://designsystem.digital.gov/design-tokens/), [Spectrum 3 token levels: global → alias → component](https://spectrum.adobe.com/page/design-tokens/)).
4. **Corner radii** — `radiusS / radiusM / radiusL / pill`. One rounded-rect language across cards, buttons, chips.
5. **Icon sizes** — `iconS / iconM / iconL` + the **44pt minimum touch target** (~88px @2x) as a named constant.

Express it as fields on the theme (the example game already does this for colors — extend it to sizes/spacing/radii):

```csharp
public sealed class GameTheme : ScriptableObject {
  // Typography scale (point sizes) — labels reference these, never literals
  public float typeDisplay = 78, typeTitle = 56, typeHeading = 44,
               typeSubhead = 32, typeBody = 30, typeLabel = 26, typeCaption = 22;
  // Spacing scale
  public float spaceXs = 4, spaceS = 8, spaceM = 16, spaceL = 24, spaceXl = 32, spaceXxl = 48;
  // Radii + touch target
  public float radiusS = 12, radiusM = 20, radiusL = 32, touchMin = 88; // 88px @2x = 44pt
  // ... existing semantic color roles (textDark/textMuted/panelCream/cellConflict/...)
}
```

**Real-world example:** the build leaked **16 distinct magic font-size literals** (24/26/28/30/31/32/38/40/42/44/56/60/64/72/76/78) across `AppRoot`, `LeaderboardView`, and `CubeApp` — three separate `Label(...)` factories each taking a raw `size`. That is exactly the "the menu looks cheap / text drifts" churn. A typography token set + one shared `Label` collapses those to ~7 named roles. **Self-heal note:** keep the theme usable from `CreateInstance` (default field values = the real values) so a null/headless asset ref still renders — and delete any `Resources/GameTheme.asset` that would shadow the `.cs` defaults with stale serialized values (the `.cs` is the **runtime source read by AppRoot** — itself a derived view of `art-spec.yaml`, the only style SSOT, whose palette hexes it must equal exactly, colors only).

## Shared component library — consistent by construction (atomic design)

Menus drift when each screen builds its widgets ad hoc. The fix is [atomic design](https://www.justinmind.com/ui-design/atomic-design) (Brad Frost): build from a small set of reusable components — atoms (Label, Icon, Button) compose into molecules (IconButton, Pill, Card) — so "a button looks the same on every page… modifying an atom updates every place that uses it" ([LogRocket](https://blog.logrocket.com/ux-design/atomic-design-components-ui-design/)). In a runtime UI this is a set of **factory functions**, ONE per widget, all reading tokens from the theme:

- `Label(parent, text, TypeRole role, ColorRole color, align)` — the *only* way text is created. No call site passes a raw size; it passes a role that maps to the typography token.
- `Button(...)`, `IconButton(...)`, `Card(...)`, `Pill(...)`, `Toggle(...)` — each applies the theme's radius/spacing/color-role/touch-min internally.

Rules that keep it consistent:

- **One factory per widget, used by EVERY screen.** No screen news up a raw `TextMeshProUGUI`/`Image`/`Button` and styles it inline. Restyling glossy→flat or recoloring a button becomes a one-function edit instead of a hunt across screens (the example game restyled buttons glossy→flat repeatedly *because* the styling lived in N places).
- **Don't fork the factory per screen.** The example game ended up with three `Label` implementations (app/leaderboard/cube) → guaranteed drift. Put shared factories in ONE static UI-kit class that every builder calls.
- **Compose, don't copy.** A Card is panel + radius + padding from tokens; an IconButton is Button + Icon + Label. Build molecules from atoms, not from scratch.

## User-facing strings — single source of truth (no literal drift, enables CJK)

Every user-visible string is **defined once and referenced**, never duplicated as a literal across screens. Hard-coded strings are "expensive technical debt… every hard-coded string [is] a localization failure point" ([SimpleLocalize](https://simplelocalize.io/blog/posts/best-practices-in-software-localization/)); the i18n rule is **externalize all user-facing strings, never concatenate** ([Microsoft Globalization](https://learn.microsoft.com/en-us/globalization/methodology/software-internationalization)).

- **Route labels through ONE provider.** The example game's difficulty names were duplicated as string literals across the menu, overlays, and HUD until they were funneled through `DifficultyRules.DisplayName(d)` — a single static source. Do this for *every* repeated label (button captions, screen titles, result lines): one method/table returns the string; screens call it.
- **No string literals at call sites for anything shown twice.** If two screens show the same word, that word lives in one place.
- This is also what makes **localization/CJK feasible later** — a string table swaps per locale; scattered literals can't. Build the seam now even if you ship one language: one provider today = drop-in `.json`/`.strings` table tomorrow ([best practice: store text in external resource files so translators never touch code](https://simplelocalize.io/blog/posts/best-practices-in-software-localization/)).

## TMP fonts for international text — decide glyph coverage UP FRONT

A CJK (or any non-Latin) requirement that surfaces *late* forces a font swap and re-layout. Decide required scripts before building text, because the default TMP font (LiberationSans) lacks CJK → **tofu (□)** boxes.

1. **Pick a font that covers the required scripts.** If your game needs glyphs outside the default font's coverage (CJK, Cyrillic, Arabic, etc.), LiberationSans won't have them → switch to a font that covers the required script (e.g. an OFL-licensed Noto family font). Verify coverage before committing — a font that can't render the script just yields tofu.
2. **Build a dynamic-atlas `TMP_FontAsset` for crisp SDF.** Use `AtlasPopulationMode.Dynamic` so arbitrary glyphs (any glyph a locale needs) are added at runtime, with **multi-atlas fallback** when one atlas fills ([Unity Learn](https://learn.unity.com/tutorial/textmesh-pro-font-asset-creation-1)). Concrete crispness settings that worked for a real project (regenerated as "<DisplayFont> SDF HD"): **samplingPointSize 110, atlas 2048², padding 11, Render Mode SDFAA**. Unity's general guidance: SDF render mode, sampling 50–70 for plain Latin, **cap atlas at 2048² for mobile**, padding ~1:10 of sampling ([Unity Learn](https://learn.unity.com/tutorial/textmesh-pro-font-asset-creation-1)) — the project went higher on sampling for large display type to stay crisp. *Blurry text = sampling/atlas too low for the display size.*
3. **Set it as the project TMP default** so all runtime text inherits it (no per-label font assignment): `TMP_Settings.instance.m_defaultFontAsset` (via `SerializedObject`), or `TMP Settings ▸ Default Font Asset`. One default = no font drift.
4. **Fallbacks for mixed scripts.** If the display font lacks some glyphs, add fallbacks in priority order (Latin → CJK → Symbols) on the primary asset's Fallback Font Asset list — TMP walks the list until a glyph matches ([Bugnet](https://bugnet.io/blog/fix-unity-ui-text-mesh-pro-falling-back-default-font)). Pre-warm with `TryAddCharacters()` on a loading screen if you render many unique CJK glyphs at once, to avoid runtime atlas-build hitches ([Unity Learn](https://learn.unity.com/tutorial/textmesh-pro-font-asset-creation-1)).
5. **No tofu check.** After wiring, screenshot a screen showing the required script and confirm real glyphs, not boxes. The project had to regenerate the TMP asset multiple times for crispness *and* re-verify the script rendered — do it once, deliberately, up front.

## The casual screen set

Title/menu, HUD (score / coins / lives or timer), pause, win, lose / game-over, settings, level-select, store / IAP placeholder, reward popup. Wire each to game state, not duplicated rules.

**Compact recipe — one screen end-to-end via MCP:**
1. `manage_tools(action="enable_group", group="ui")` and confirm `mcpforunity://editor/state` is ready.
2. **UI Toolkit:** `manage_ui` to author the UXML (structure) + USS (style); add a `UIDocument` to a GameObject referencing the asset. **uGUI:** `manage_gameobject(action="create")` the Canvas, then children; `manage_components` to add CanvasScaler, SafeArea, TMP_Text, Button, Image.
3. Apply safe area (above) and responsive config.
4. Bind to a controller script (show/hide, set score) via the script tools; compile clean (`read_console(types=["error"])`).
5. Enter Play Mode, trigger the state, `manage_scene(action="screenshot")` at phone resolution.

**Stacked overlays (one runtime overlay over another).** When an overlay opens on top of another shown/hidden panel — e.g. a leaderboard over the start menu — call `transform.SetAsLastSibling()` on it **right before `SetActive(true)`**. Sibling/creation order alone isn't enough once panels are toggled dynamically, so the new panel can render *behind* the one it's meant to cover. Give each overlay **its own dim** so the panel underneath is visually suppressed.

Full ordered calls + UXML/USS and uGUI examples: load `references/ui-recipes.md`.

## Constraint / peer highlight (grid & constraint puzzles)

In Sudoku/Queens-style boards, when a cell is selected, subtly brighten every cell that shares its row, column, or region — `Color.Lerp(regionColor, Color.white, ~0.22f)` — so the player can *see* the active constraints at a glance. Big intuitive-UX win: it teaches the rules without text. Layer by priority: selected cell brightest, peers subtle, conflict color overrides peer highlighting so errors stay readable.

## Count badge + disabled state (consumable buttons)

For limited-use actions (hints, undos), pin a small **circular count badge** to the button's top-right corner (`anchorMin = anchorMax = (1,1)`, offset inward) showing remaining uses. When the count hits 0: set `Button.interactable = false`, dim the whole button via a `CanvasGroup` (alpha ~0.5), hide the badge, **and** disable the separate `PressFeedback` component — otherwise a disabled button still fires tap SFX/scale-punch and feels broken. The badge + dim communicate "spent" at a glance.

## Premium menu patterns (beat flat colored pills)

A title/menu reads as "made by a studio" with these instead of a column of full-width colored pills:

- A **mascot circle header** (the game's character in a circular frame) anchoring the top.
- Small **glossy circular icon-buttons in the header corners** (settings gear, leaderboard) instead of full-width pills in the option list — declutters and reads premium.
- **Wide buttons = layered:** rounded base + top-gloss strip + drop shadow + label (see `unity-graphics` layered-button recipe).
- Small difficulty **"pips"** (filled vs faint dots) to convey difficulty at a glance without text.
- Move secondary settings into a **gear popover** to keep the main menu uncluttered.

## Juice

- Button press: scale-down on press / scale-up on release, optional tap SFX (pair with `unity-audio-generator`).
- Score count-up (tween the displayed number, not the model).
- Popups scale-in from 0 with ease-out + slight overshoot; dim background.
- Screen transitions (fade / slide) instead of hard cuts.
- **Reveal-animation gotcha:** if you add a drop shadow by inserting a `CardShadow` sibling at the card's index, the shadow becomes child 0 — so a spring/scale reveal driven by `transform.GetChild(0)` animates the SHADOW, not the card. Target `transform.Find("Card")` (by name), not by index.

## World-to-UI cohesion

Match the game's art direction — palette, corner radius, icon family. When `art-spec.yaml` exists, UI colors come from its `palette.roles` (see the Design-tokens input rule) and UI art prompts reuse the spec's verbatim style tokens. Use a single consistent icon set; generate logos/icons/panels/title art with `unity-image-generator` rather than mismatched placeholders.

## Verify (a screen is done only with evidence)

- Screenshot at a real phone resolution (e.g. 1170x2532 / 1080x1920 portrait) shows the screen.
- Content inside safe area: nothing under the notch or behind the home indicator.
- Re-screenshot a tall (19.5:9) and a short (4:3) aspect to confirm no clipping/overlap.
- Touch targets visibly >= ~44pt; primary actions thumb-reachable.
- Text fits, no clipping, legible, good contrast.

Before claiming UI work complete, load `references/checklists/ui-readability.md`, `references/checklists/responsive-safe-area.md`, AND `references/checklists/ui-consistency.md`, and pass all three.

## UI consistency audit — run before calling UI "done"

A separate pass from readability/responsiveness: catches *drift* between screens (the menu-rework / text-drift churn). Run it once the screens exist; load `references/checklists/ui-consistency.md` for the full list. The core gates:

- **Token discipline** — grep the UI code for raw font-size literals, color literals, and magic paddings/radii at call sites. There should be ~none: everything references the theme/token layer. (The example game had 16 orphan font sizes — that's a fail.)
- **Hexes equal art-spec** — when `art-spec.yaml` exists, every theme color hex equals an art-spec palette hex (`palette.roles` + arrays) exactly; no invented UI colors (colors only — type/spacing/radii are theme-native).
- **One factory per widget** — every Label/Button/Card/IconButton comes from the shared UI-kit; no screen news up and styles a `TextMeshProUGUI`/`Image`/`Button` inline; no forked per-screen copies of a factory.
- **No string-literal drift** — every label shown on 2+ screens routes through one provider (e.g. `DifficultyRules.DisplayName`); no duplicated user-facing literals.
- **Font default + no tofu** — the project TMP default font is set; a screenshot of any required non-Latin script (CJK) shows real glyphs, not boxes.
- **Cross-screen visual match** — buttons, cards, headers, radii, and type roles look identical across menu / HUD / overlays in side-by-side screenshots. Restyling one widget would propagate everywhere (proof the library is shared, not copied).
- **Safe-area + touch targets** still hold on every screen, not just the first one built.

## Final response

Report: detected UI stack and why; screens built and that they went through `manage_ui` / `manage_gameobject`+`manage_components` (not raw YAML); safe-area + responsive config applied; touch-target/typography evidence; phone-resolution screenshots (and the multi-aspect check); both checklists passed; remaining risks.

## Field notes & lessons

- Added stacked-overlay rule — `SetAsLastSibling()` right before `SetActive(true)` so a runtime overlay opened over another panel renders on top (creation order isn't enough once panels toggle dynamically); give each its own dim.
- Added constraint/peer highlight for grid puzzles (Lerp region color toward white ~0.22 on row/col/region peers; selected brightest, conflict overrides) and consumable-button count badge + disabled state (top-right circular badge; at 0 set interactable=false, dim via CanvasGroup, hide badge, AND disable PressFeedback so a dead button gives no tap SFX/scale).
- Added premium menu patterns (mascot circle header, glossy circular corner icon-buttons + gear popover instead of full-width pills, layered wide buttons, difficulty pips) and the reveal-animation gotcha (a `CardShadow` sibling at the card index makes the shadow child 0, so `GetChild(0)` spring-reveals the shadow — target `transform.Find("Card")` by name).
- Root-caused the recurring menu/text-consistency churn and encoded the systemic fixes. Added four sections — (1) **Design tokens**: a single source of truth for typography scale (named sizes, not literals), spacing scale, semantic color roles, radii, and icon/touch-target sizes, expressed as fields on the runtime theme object (`GameTheme`) read by the builder (`AppRoot`); grounded in the real bug (16 orphan magic font-size literals across 3 screens, three forked `Label` factories). (2) **Shared component library** (atomic design): one factory per widget (Label/Button/Card/IconButton) used by EVERY screen so restyling glossy→flat is a one-place change; don't fork the factory per screen. (3) **User-facing strings: single source of truth** — route every repeated label through one provider (`DifficultyRules.DisplayName`), no duplicated literals; this is what makes CJK/localization feasible. (4) **TMP fonts for international text** — decide glyph coverage UP FRONT to avoid tofu; dynamic-atlas `TMP_FontAsset` (a script-appropriate display font, samplingPointSize 110 / atlas 2048² / padding 11 / SDFAA) set as the project TMP default; fallback lists + `TryAddCharacters` pre-warm. Plus a new **UI consistency audit** section + `references/checklists/ui-consistency.md`. Sources cited inline: USWDS/Adobe Spectrum/UXPin design tokens, Brad-Frost atomic design (Justinmind/LogRocket), Apple HIG typography + 44pt, Unity Learn TMP font-asset creation + CJK dynamic atlas, SimpleLocalize/Microsoft i18n single-source-of-truth.

## State-driven panel visibility (hard rules)

- Every full-screen or center panel maps 1:1 to game states (Ready/Running/GameOver/Pause).
  Toggle the PANEL ROOT GameObject, never just its text/children — a panel Image left enabled
  with cleared text is an invisible-in-code, glaring-in-game overlay (field bug: a #1B1F3A@0.85
  center panel covered the screen all game because HideCenter() only disabled the label).
- REQUIRED PlayMode assertion: in the Running state, no enabled UI `Image` covers ≥50% of the
  canvas rect. One line of insurance against the whole class. A legitimate full-screen board/
  background Image (card games, boards) is exempted BY NAME and must sit at sibling index 0.
- uGUI flash feedback: `Image.color` is multiplicative — white does NOTHING (same trap as
  SpriteRenderer.color). Flash = a white overlay Image animating alpha, or a material swap.
- Headless screenshot evidence MUST include the UI: batch mode has no game view, so overlay
  canvases are invisible to camera RT captures — switch the canvas to Screen-Space-Camera for
  the capture (then restore), or the evidence is UI-blind and overlay bugs ship.
- Safe area: HUD content lives under a SafeAreaFitter container (anchors from Screen.safeArea),
  not raw canvas corners.
- **Transient-view lifecycle (drag ghosts, stale FX):** any rebuild/re-render sweep must clear
  EVERY container that can own transient views (drag layers, FX layers, tooltip layers) — not
  just the primary list container. Views moved out of their owner (reparented for z-order) are
  exactly the ones a naive children-sweep misses. Ban ordering assumptions ("the end-drag
  handler will destroy it"); enforce with a count assertion: live views == model count.
