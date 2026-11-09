---
name: roblox-ui-hud
description: Use when building or fixing Roblox game UI/HUD in Luau — responsive layout across phone/tablet/desktop, ScreenGui panels, progress bars/meters, wallet/nav chrome, and the layout gotchas that bite (UIScale vs position, horizontal UIListLayout order, boolean-visibility bug, font glyphs, click-outside-close). Also the copy/clarity rules that make a HUD read well.
---

# Roblox game UI / HUD patterns

Hand-built HUDs (not auto-scaled templates) that hold up across devices and read clearly.

## Responsive layout across devices
- **`UIScale` (e.g. a `fitScale` helper) scales an element's SIZE about its anchor — NOT its position.** So scaling alone doesn't reposition; recompute positions per device where it matters. Don't nest two UIScales on one element (parent + child) — it double-scales.
- **Device gate by MIN dimension, not by `TouchEnabled` alone** — `math.min(vp.X, vp.Y)` is orientation-proof: phone short side ≈ ≤430, tablet ≥ ~744. Branch desktop / phone (`isMobile and min < 600`) / tablet (`isMobile and min >= 600`) so a rotated tablet isn't treated as a phone.
- **Anchor stacked HUD elements to LIVE panel heights, not hardcoded pixel offsets.** Classic bug: a boost/pill row hardcodes "panel is 104px" but the panel above it GROWS with content (`clamp(base + n*rowH, …)`), so they overlap once the panel expands. Read the neighbor's actual `AbsoluteSize.Y` (or its formula) and position off that.
- **Leave room for Roblox's own mobile controls:** the DynamicThumbstick capture area reaches up to ~0.75·`vp.Y` on the bottom-left, and the Jump button sits bottom-right; lift bottom-anchored HUD off the edge enough to clear them WITH and WITHOUT the safe-area inset. Verify on a small phone (iPhone SE) and a large one (Pro Max) — the two worst cases.

## ScreenGui panels
- Convention that tests well: **one `ScreenGui` per screen/panel, `Enabled = false`, content pre-built.** Toggle `.Enabled = true` to open. (For MCP testing, enabling reveals CENTERED panels; SLIDE-IN panels sit off-screen in their closed position, so toggling shows nothing — animate them in instead.)
- **Only one panel open at a time:** a `closeAll()` that closes/​hides every panel before opening the next.
- **Click-outside-to-close:** `.Active = true` does NOT reliably sink clicks that fall through a child ScrollingFrame. Bounds-check the backdrop's `InputBegan` — close only when the click is OUTSIDE the panel's `AbsolutePosition`/`AbsoluteSize`.

## Progress bars / meters (the reusable recipe)
**Don't resize a rounded fill.** A rounded fill narrower than its own height shrinks to a dot that grows, then
stretches sideways (players saw it on every bar at low values). Instead the fill is the **full size of its rounded
track** (same UICorner) and a `UIGradient` named `Mask` on it cuts it at the fraction (opaque up to the cut,
transparent after, ~1 px soft edge): 2% is a sliver of the track's own round end and the edge is a straight cut.
```lua
-- The Mask's transparency along the bar: opaque on the kept side of `cut` (0..1), see-through on the other,
-- blended over `soft` (one pixel's width as a fraction of the bar) so the edge doesn't shimmer as it moves.
local function maskSequence(cut: number, soft: number, keepLow: boolean): NumberSequence
	local function value(t: number): number
		local v = math.clamp((t - (cut - soft / 2)) / soft, 0, 1)
		return if keepLow then v else 1 - v
	end
	local points = { NumberSequenceKeypoint.new(0, value(0)) }
	for _, t in { cut - soft / 2, cut + soft / 2 } do
		if t > points[#points].Time + 1e-4 and t < 1 - 1e-4 then
			table.insert(points, NumberSequenceKeypoint.new(t, value(t)))
		end
	end
	table.insert(points, NumberSequenceKeypoint.new(1, value(1)))
	return NumberSequence.new(points)
end
-- One shared helper owns every bar; nothing else writes a fill's Size or its Mask:
-- Bars.set(fill, fraction, axis?) (does nothing when unchanged: many callers set every frame),
-- Bars.tween(fill, fraction, TweenInfo), Bars.setColor(fill, colorOrSequence), Bars.get(fill)
```
- Shading moves to a child `Shade` ImageLabel (a top-to-bottom alpha image tinted the top colour over the fill's
  bottom colour), because the Mask gradient owns Transparency. Shine / checker children get their own Mask cut where
  the fill's cut falls on them.
- Grows from the right / bottom when the fill's AnchorPoint is 1. Redraw on `AbsoluteSize` changes.
- A Studio command script adds Mask + Shade to every bar so new bars are made the same way; a fill without a Mask
  warns once and shows full.
- Typical layout: the helper in `src/shared/Bars.luau`, the Studio command script in `tools/ui/bar_masks.luau`.
- Status colour still reads at a glance (`Bars.setColor(fill, good and GREEN or AMBER)`); text overlay centred.
**⚠️ Boolean-visibility bug (bit me):** in Luau, `local show = a and b and season.teams` returns the **last operand** (a table), NOT `true` — so `frame.Visible = show` errors or `show == true` is always false. Make the condition a real boolean: end it with a comparison (`… and season.teams ~= nil`), or wrap it. Reserve the bar's slot even when hidden so the layout doesn't jump.

## Layout gotchas (waste hours)
- **Horizontal auto-size `UIListLayout` ignores `LayoutOrder` by default** — set `SortOrder = Enum.SortOrder.LayoutOrder` or chips render in reversed/creation order.
- **`UDim2.new(0,0,1,0)` (single pair set)** trips a selene "use fromScale" warning — use `UDim2.fromScale`/`fromOffset`.
- **Font glyphs:** Gotham renders `✕ ↻ ✦` as boxes — use `X`, `★`, `◆`, `$`. Emoji are fine (🍀 👑 ⚡ ⚔️ 🏆) EXCEPT flag emoji (show as 2 letters) — draw flags with frames.

## Copy & clarity (small rules, big readability)
- **Prefer ICONS/glyphs over jargon words** in the HUD — e.g. show currency as its icon, not "Cash/Shards/Gems"; names belong only where the reward is described (shop). Same spirit: avoid internal-system nouns in player-facing text (say the action/outcome, not "level up the X board"; say "team", not "XI").
- Keep it **plain-language** — read every string as a brand-new player would.

## Verifying UI (MCP)
Screenshots can lie for UI — a freecam capture can leave ScreenGuis hidden, and distant SurfaceGui close-ups render blank. Cross-check by walking `PlayerGui:GetDescendants()` and asserting on `.Text` / `.Visible` / `ImageLabel.Image` / accessory counts. The MCP tools + gotchas (clicking by `AbsolutePosition`, the cross-VM rule, capture artifacts) are in the **roblox-studio-mcp** skill; the dev/test loop is in **roblox-studio-workflow**.

Phone-first scaling, safe areas, ScreenInsets, touch buttons and gamepad menus are in **roblox-cross-device-ui**; verifying in Studio is **roblox-studio-verification**.
