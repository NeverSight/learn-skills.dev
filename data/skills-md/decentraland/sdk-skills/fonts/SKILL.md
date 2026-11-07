---
name: fonts
description: Fonts for text in Decentraland SDK7 scenes — the three built-in faces and custom TTF fonts shipped with the scene (`fontSrc`) on TextShape, UiText, Label, Button, Input and Dropdown. Use when the user wants a custom, branded or themed typeface, wants to change the font of 3D or UI text, wants to ship a .ttf with a scene, or asks why a custom font is not showing. Do NOT use for text layout, sizing or UI structure (see build-ui) or placing 3D text in the world (see advanced-rendering).
---

# Fonts in Decentraland

Every text component has two font fields:

| Field | What it takes | Components |
|---|---|---|
| `font` | A built-in face. On `TextShape` / `UiText`: `Font.F_SANS_SERIF` (default), `Font.F_SERIF`, `Font.F_MONOSPACE`. On React-ECS props: `'sans-serif'` (default), `'serif'`, `'monospace'` | All |
| `fontSrc` | Path to a `.ttf` file in the scene's content, relative to the scene root | `TextShape`, `UiText`, `UiInput`, `UiDropdown`, and the React-ECS `Label`, `Button`, `Input`, `Dropdown` and `UiEntity uiText` |

Those three built-in faces are the only ones. There is no font name list beyond them.

## RULE: Check the SDK version before writing `fontSrc`

`fontSrc` needs the **first `@dcl/sdk` release after 7.30.1** (decentraland/js-sdk-toolchain#1656). On 7.30.1 and earlier the field does not exist: it is a TypeScript error, and even forced past the types the SDK never sends it to the explorer.

Read the installed version from `node_modules/@dcl/sdk/package.json` (or `package.json`) before writing it. If the scene is older, either upgrade `@dcl/sdk` or stay with a built-in `font`. Never patch the SDK's generated serializers in `node_modules`. The QA scene did that as a temporary bridge, and it breaks on the next install.

## RULE: Always set `font` next to `fontSrc`

`font` is the fallback whenever the custom font cannot be used: on mobile always, on desktop until the font's asset bundle is ready (see Testing). Pick the closest built-in face, so the fallback still looks intended: `'serif'` for a serif or display face, `'monospace'` for a code or terminal face, `'sans-serif'` otherwise.

## RULE: The mobile app ignores `fontSrc`

The Decentraland mobile app does not support custom fonts: it always renders the `font` fallback (decentraland/godot-explorer#3092, no ETA). Every scene that uses `fontSrc` must still look right and fit with its fallback:

- Choose the fallback deliberately (previous rule), not as an afterthought.
- Never rely on the custom font's width to make text fit a fixed box. Size the box so the fallback fits too.
- Never put meaning only in the custom font's look (an icon font, a symbol font, a "handwritten" clue). On mobile it becomes plain text.

When the user adds a custom font, tell them it won't show on mobile.

## RULE: A custom font is a `.ttf` file in the scene

`fontSrc` is a file path, not a font name. Custom fonts are available, but a font the user names ("use Playfair Display") only works once its `.ttf` file sits in the scene's folder and `fontSrc` points at it. When the user wants a custom font and the scene has no `.ttf` for it yet, tell them custom fonts are supported and ask them to provide the `.ttf` file (and its licence). Do not fetch one yourself.

The Unity explorer supports nothing else. Every other value silently falls back to `font` there:

| `fontSrc` value | Unity explorer | Bevy explorer |
|---|---|---|
| `.ttf` in the scene content | Yes, once its asset bundle exists (deployed, or preview with optimized assets) | Yes |
| OpenType with CFF outlines (usually `.otf`), collections (`.ttc`), web fonts (`.woff`, `.woff2`) | Falls back | Not documented — do not rely on it |
| `.ttf` over 16 MB, or with extremely complex glyph outlines | Falls back (refused by the converter) | Not documented |
| URL to a `.ttf` | Falls back | Yes |
| Font family name (`'Playfair Display'`) | Falls back | Yes |
| Missing file, invalid file, empty string | Falls back | Falls back |

The protocol's doc comment, which shows up in editor tooltips, says a font family name works. That is Bevy only: Unity dropped external fonts on purpose (security, code size, runtime glyph rasterising). Never write a family name or a URL in `fontSrc`.

When the desktop client rejects a font it logs an `SDK_FONTS` warning in the console saying why (for a URL: `font_src "…" cannot be an external URL`). Check the console before anything else when a font falls back.

## Adding a font to a scene

1. Put the `.ttf` under `assets/fonts/`, for example `assets/fonts/BungeeShade-Regular.ttf`. Use a static `.ttf`. If a family ships only as a variable font, use its static instances.
2. Put the font's licence next to it (`assets/fonts/BungeeShade-OFL.txt`). Deploying publishes the file on public content servers, so the licence must allow redistribution and embedding. OFL and Apache fonts allow it. Most commercial desktop licences do not.
3. Reference it by its path from the scene root, the same way as a texture `src`: `fontSrc: 'assets/fonts/BungeeShade-Regular.ttf'`.

One file is one face. For a bold title and regular body text, ship both weights and point each text at its own file.

Cost: every text entity using the same `fontSrc` shares one loaded copy, so reusing a font across the scene costs no more than using it once. Each distinct font file becomes its own asset bundle of about 700 KB (two texture atlases), plus its own textures in memory. Keep a scene to one or two font files.

## 3D text (`TextShape`)

```typescript
import { engine, Transform, TextShape, Font } from '@dcl/sdk/ecs'
import { Vector3, Color4, Color3 } from '@dcl/sdk/math'

const sign = engine.addEntity()
Transform.create(sign, { position: Vector3.create(8, 3, 8) })

TextShape.create(sign, {
  text: 'OPEN',
  fontSize: 6,
  textColor: Color4.White(),
  outlineColor: Color3.Black(),
  outlineWidth: 0.1,
  font: Font.F_SERIF,
  fontSrc: 'assets/fonts/AbrilFatface-Regular.ttf'
})

// Switching font at runtime is a plain field write
TextShape.getMutable(sign).fontSrc = 'assets/fonts/BungeeShade-Regular.ttf'
```

## UI text (React-ECS)

```tsx
<Label
  value="Score: 100"
  fontSize={24}
  font="sans-serif"
  fontSrc="assets/fonts/BungeeShade-Regular.ttf"
  uiTransform={{ width: 240, height: 40 }}
/>

<Button value="Play" variant="primary" font="sans-serif" fontSrc="assets/fonts/BungeeShade-Regular.ttf" />

<Input placeholder="Your name" font="serif" fontSrc="assets/fonts/PTSerif-Regular.ttf" />

<Dropdown options={['Easy', 'Hard']} font="serif" fontSrc="assets/fonts/PTSerif-Regular.ttf" />

<UiEntity uiText={{ value: 'Coded-only text bag', font: 'monospace', fontSrc: 'assets/fonts/AzeretMono-Medium.ttf' }} />
```

Editable UI (**build-ui**): the Creator Hub UI Designer does not know `fontSrc`. Its property panel neither shows nor edits it, and whether a hand-written `fontSrc` survives an editor save has not been verified. Prefer `fontSrc` in coded UI and on `TextShape`. In an editable file, open the component in the editor after writing it and check that the prop is still there after a save.

## Testing a custom font

The desktop client (Unity explorer) loads scene fonts only from asset bundles, never from the raw `.ttf`. So the custom font shows only where bundles exist:

- **Local preview with optimized assets:** in the Creator Hub, **Play Options → Desktop Client → Compress Assets**; from the CLI, `npm run start -- --asset-bundles`. The Desktop Explorer converts the scene's assets, fonts included, itself. This needs a Desktop Explorer release newer than v0.189.0: older releases convert with a version that builds no font bundles, so preview shows the fallback even with Compress Assets on.
- **Plain local preview** (no optimized assets): always the `font` fallback. That is expected, not a bug.
- **Deployed scene:** the font appears once the server's asset-bundle conversion finishes. Until then the fallback shows. Scenes deployed before font conversion existed get font bundles only when they are deployed again.
- **Bevy explorer** loads the `.ttf` directly, so its preview shows the font without conversion.
- **Mobile app:** always the fallback (see the mobile rule).
- Tell the user which of these applies before they report "my font isn't working".
- The reference scene for expected behaviour is `scenes/84,-6-font-src` in decentraland/sdk7-test-scenes (realm `sdk7testscenes.dcl.eth` on zone). It covers each fallback case, fonts shared between components, recreating components and the scene boundary.

## Glyphs and legibility

- A custom font only draws the characters it contains. Characters it lacks are drawn with the built-in sans-serif, mid-word, which looks broken. For accented letters, Cyrillic, CJK and so on, pick a font that includes those scripts.
- The font's bundle comes with ASCII, smart punctuation (quotes, dashes, ellipsis, bullet), € and the common Latin-1 letters already rendered. Any other character the font includes (Cyrillic, Greek, CJK…) is rendered the first time it appears, which causes a brief hitch. For text in those scripts, show it early (a loading or intro screen) rather than at a critical moment.
- No emoji in any text value, whatever the font. The Unity explorer has no emoji glyphs (see **build-ui**).
- Keep decorative and display faces for short titles and signs. Body text and anything read while moving needs a plain face at the sizes in **build-ui** (UI) and **advanced-rendering** (3D).
- A monospace face, built-in or custom, does not make spaces line up columns in a `TextShape`. Use one `TextShape` per column (see **advanced-rendering**).

## Cross-references

- **build-ui**: Label, Button, Input and Dropdown props, sizing and the no-emoji rule.
- **advanced-rendering**: `TextShape` placement, orientation, outline and alignment.
- **migrate-sdk6-to-sdk7**: SDK6 `font` names map to the built-in `Font` enum, and custom SDK6 fonts map to `fontSrc`.
- **deploy-worlds** / **deploy-scene**: deploying so the server converts the font.
- **optimize-scene**: asset-bundle conversion and why it matters for load time.
