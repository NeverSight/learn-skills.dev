---
name: wow-api-framexml
description: "Complete documentation for World of Warcraft FrameXML functions — global Lua functions, mixins, object pools, SharedXML utilities, and game utility modules. Use this for UI helpers (StaticPopup_Show, EasyMenu), formatting (SecondsToTime, FormatLargeNumber), table/math utils (tContains, Lerp), mixin/pool patterns, chat frame filters, tooltip helpers, bag functions, texture/atlas markup, and all FrameXML game utility modules."
---

# FrameXML Functions API

This skill documents the **FrameXML** layer of the WoW API — global Lua functions defined by Blizzard's interface code, shared XML utility modules, mixin system, object pools, and game utility modules. These are distinct from the C-based Widget API.

> **Source of truth:** https://warcraft.wiki.gg/wiki/FrameXML_functions
> **FrameXML source:** https://github.com/Gethe/wow-ui-source/tree/live/Interface/FrameXML
> **SharedXML source:** https://github.com/Gethe/wow-ui-source/tree/live/Interface/SharedXML
> **Current as of:** Patch 12.0.0 — Retail only.

## When to Use This Skill

Use this skill when you need to:
- Toggle standard UI panels (`ToggleCharacter`, `ShowUIPanel`, `ToggleSpellBook`)
- Use standard UI dialogs (`StaticPopup_Show`) or context menus (`EasyMenu`)
- Use the Mixin / Object Pool system (`CreateFromMixins`, `CreateFramePool`)
- Filter or extend chat messages (`ChatFrame_AddMessageEventFilter`)
- Format numbers, money, or time (`SecondsToTime`, `FormatLargeNumber`, `GetMoneyString`)
- Use table utilities (`tContains`, `tDeleteItem`, `tInvert`, `CopyTable`)
- Use math utilities (`Lerp`, `Clamp`, `Round`, `CalculateDistance`)
- Create texture/atlas markup for FontStrings (`CreateAtlasMarkup`, `CreateTextureMarkup`)
- Build tooltips with helpers (`GameTooltip_AddNormalLine`, `GameTooltip_SetTitle`)
- Handle pixel-perfect UI (`PixelUtil.SetSize`, `PixelUtil.SetPoint`)
- Use event convenience functions (`EventUtil.ContinueOnAddOnLoaded`)
- Register/animate frames (`UIFrameFadeIn`, `ScriptAnimationUtil.ShakeFrameRandom`)
- Manage bags (`OpenAllBags`, `ToggleBag`, `IsBagOpen`)
- Preview items/mounts in dressing room (`DressUpItemLink`)
- Query player/class/spec info (`PlayerUtil.GetCurrentSpecID`, `GetClassColor`)
- Work with quest icons, map utils, communities, transmog, or other game utilities

## References

| Reference | Contents |
|-----------|----------|
| [UIPARENT.md](references/UIPARENT.md) | UI panel toggles, `ShowUIPanel`, `CloseSpecialWindows`, `MouseIsOver`, number abbreviation |
| [MIXINS-AND-POOLS.md](references/MIXINS-AND-POOLS.md) | Mixin system, `CreateFromMixins`, `CreateColor`, object/frame/texture pools |
| [SHAREDXML-DATA-UTILS.md](references/SHAREDXML-DATA-UTILS.md) | TableUtil, MathUtil, TimeUtil, FormattingUtil, ColorUtil, CvarUtil, EasingUtil, EventUtil, EventRegistry, FunctionUtil, LinkUtil, Flags, AuraUtil, UnitUtil |
| [SHAREDXML-UI-UTILS.md](references/SHAREDXML-UI-UTILS.md) | FrameUtil, TextureUtil, PixelUtil, AnchorUtil, NineSlice, RegionUtil, ScriptAnimationUtil, GameTooltipTemplate, TooltipUtil, `UIFrameFadeIn/Out` |
| [FRAMEXML-GAME-UTILS.md](references/FRAMEXML-GAME-UTILS.md) | AchievementUtil, ActionButtonUtil, AzeriteUtil, CalendarUtil, CampaignUtil, CommunitiesUtil, DifficultyUtil, ItemRef/ItemUtil, MapUtil, PlayerUtil, PVPUtil, PartyUtil, QuestUtils, TransmogUtil, and more |
| [CHATFRAME-CONTAINERS.md](references/CHATFRAME-CONTAINERS.md) | ChatFrame functions, bag open/close/toggle, DressUpFrames, StaticPopup_Show, EasyMenu |
