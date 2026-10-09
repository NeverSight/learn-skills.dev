---
name: roblox-text-chat
description: Chat and text safety - TextChatService (channels, SendAsync, ShouldDeliverCallback, OnIncomingMessage, commands, bubbles, custom UI), mandatory TextService filtering of any player-authored text, rate limits, privacy checks, PolicyService restrictions, legacy Chat migration. Use when adding chat features or commands, or any feature that shows one player's text to others (names, signs, notes).
---

# Chat and text safety

## Non-negotiable rules (Roblox Community Standards)

1. Player-to-player conversation must go through **TextChatService** `TextChannel`s (handles filtering,
   privacy/parental settings, and abuse reporting). The legacy `Chat` service/`ChatService` Lua modules
   are gone — `TextChatService` is the only chat system.
2. **Any text authored by one player and shown to another** (pet names, signs, guild names, trade notes,
   custom UI) must be filtered with `TextService:FilterStringAsync` on the server before display — and
   re-filtered when loaded from a DataStore later.
3. Editable text others can see (signs, bulletin boards) needs a rate limit of at least 1 minute.
4. Respect privacy settings with `CanUserChatAsync`/`CanUsersChatAsync`/`CanUsersDirectChatAsync` and mark
   direct-message channels with `TextChannel:SetDirectChatRequester()`.

Not chat (no filtering needed): your own UI text, game status messages, admin announcements you write.

## Filtering player-authored text

```luau
--!strict
local TextService = game:GetService("TextService")

-- Broadcast (e.g. a sign everyone sees). Returns nil if filtering failed: then show nothing.
local function filterForEveryone(text: string, fromUserId: number): string?
	local ok, result = pcall(function()
		local filterResult = TextService:FilterStringAsync(text, fromUserId, Enum.TextFilterContext.PublicChat)
		return filterResult:GetNonChatStringForBroadcastAsync()
	end)
	return if ok then result else nil
end

-- Per-recipient (respects each viewer's age/settings; e.g. a private note).
local function filterForUser(text: string, fromUserId: number, toUserId: number): string?
	local ok, result = pcall(function()
		local filterResult = TextService:FilterStringAsync(text, fromUserId, Enum.TextFilterContext.PrivateChat)
		return filterResult:GetNonChatStringForUserAsync(toUserId)
	end)
	return if ok then result else nil
end

return { forEveryone = filterForEveryone, forUser = filterForUser }
```

- Filter on the **server**, after the player submits (not per keystroke); rate-limit and length-cap first.
- On failure, **fail closed** (show nothing / a placeholder), never the raw text.
- Store the raw text if you must, but always filter at display time (filters and viewer settings change).
- Numbers-only or short strings can still be filtered (hashtags `###`); design UI for that.

## TextChatService essentials

- Defaults: `CreateDefaultTextChannels` creates `RBXGeneral` and `RBXSystem`; `CreateDefaultCommands`
  adds built-ins (`/whisper`, `/team`, `/mute`, ...). Configure look via `ChatWindowConfiguration`,
  `ChatInputBarConfiguration`, `BubbleChatConfiguration` (or disable and build your own UI with
  `TextChannel:SendAsync` and `TextChatService.MessageReceived`).
- Flow: client `TextChannel:SendAsync(text)` → server `TextChannel.ShouldDeliverCallback(message, textSource)`
  per recipient → filtering → clients' `OnIncomingMessage` callbacks → display.
- Callbacks must **not yield**. `ShouldDeliverCallback` is server-only; `TextChatService.OnIncomingMessage`
  and `TextChannel.OnIncomingMessage` are client-only (formatting).
- System messages: `channel:DisplaySystemMessage(text)` on the client (local only).
- Custom channels (team, party, proximity): create `TextChannel`s under `TextChatService` on the server,
  `channel:AddUserAsync(userId)` to add members; check the returned `TextSource`'s `CanSend`.

```luau
--!strict
-- Client: chat tags and colors via OnIncomingMessage (formatting only; never yields).
local Players = game:GetService("Players")
local TextChatService = game:GetService("TextChatService")

TextChatService.OnIncomingMessage = function(message: TextChatMessage)
	local properties = Instance.new("TextChatMessageProperties")
	local source = message.TextSource
	if source then
		local player = Players:GetPlayerByUserId(source.UserId)
		if player and player:GetAttribute("VIP") then
			properties.PrefixText = `<font color="#F5CD30">[VIP]</font> {message.PrefixText}`
		end
	end
	return properties
end
```

```luau
--!strict
-- Server: a /spawn command, restricted to admins.
local Players = game:GetService("Players")
local TextChatService = game:GetService("TextChatService")

local ADMINS: { [number]: boolean } = { [123456] = true }

local command = Instance.new("TextChatCommand")
command.Name = "SpawnCommand"
command.PrimaryAlias = "/spawn"
command.Parent = TextChatService

command.Triggered:Connect(function(source: TextSource, unfilteredText: string)
	if not ADMINS[source.UserId] then
		return
	end
	local player = Players:GetPlayerByUserId(source.UserId)
	print(`{player and player.Name} ran: {unfilteredText}`)
end)
```

More: proximity chat, team channels, custom UI, and migrating from legacy chat:
[references/chat-recipes.md](references/chat-recipes.md).

## PolicyService (per-user restrictions)

`PolicyService:GetPolicyInfoForPlayerAsync(player)` (server, `pcall`) returns flags such as
`ArePaidRandomItemsRestricted`, `IsPaidItemTradingAllowed`, `AreAdsAllowed`, `AllowedExternalLinkReferences`,
`IsSubjectToChinaPolicies`, `IsContentSharingAllowed`. Gate loot boxes, trading, ads, and links to
social media (only show platforms listed in `AllowedExternalLinkReferences`) per player.

## Related skills

`roblox-security` (rate limits, validation), `roblox-ui` (text input UI), `roblox-monetization`
(paid random items), `roblox-data-stores` (storing user text).
