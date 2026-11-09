---
name: stream-unreal
description: "Build, integrate, and answer how-to questions for Stream Chat in Unreal Engine games and apps. Use for Unreal Engine / UE5 / C++ / Blueprint / UMG project work - plugin install per engine version, StreamChatClientComponent wiring on the HUD, ConnectUser and tokens, channels and messages, the shipped WBP_* chat widgets, theming, cooking, and iOS / Android / desktop packaging. Triggers on unreal, unreal engine, ue5, ue 5.7, ue 5.8, .uproject, .uplugin, Build.cs, umg, blueprint, widget blueprint, StreamChat plugin, UStreamChatClientComponent, UChatChannel, FChannelProperties, WBP_TeamChat, in-game chat, game chat. Chat only - there is no Stream Video or Feeds SDK for Unreal."
license: See LICENSE in repository root
compatibility: Requires an Unreal Engine 5.7 or 5.8 project (C++ or Blueprint) and a local engine install for build/verify work. Docs lookups need only network access. The `getstream` CLI is the default path for credentials (API key + user token); optional if the user pastes them.
metadata:
  author: GetStream
allowed-tools: >-
  Read, Write, Edit, Glob, Grep,
  WebFetch(domain:getstream.io),
  WebFetch(domain:github.com),
  WebFetch(domain:raw.githubusercontent.com),
  WebFetch(domain:getstream.github.io),
  Bash(ls *),
  Bash(grep *),
  Bash(find * *),
  Bash(find . *),
  Bash(cat *.uproject), Bash(cat *.uplugin),
  Bash(jq *),
  Bash(gh release *),
  Bash(unzip *),
  Bash(getstream *)
---

# Stream Unreal - docs orchestrator for Unreal Engine

**Chat only.** There is no Stream Video or Stream Feeds SDK for Unreal (`/video/docs/unreal` and the Feeds Unreal index both 404). If the user asks for calling or feeds in Unreal, say so up front and offer the alternatives (a platform SDK on a companion mobile app, or the REST/server API) rather than inventing an API.

**The SDK is in beta.** `IsBetaVersion: true` in the `.uplugin`; the surface can change between releases, and C++ and Blueprint coverage differ per operation. State this whenever the user pins a version or plans an upgrade.

This skill **orchestrates**: it gates the request against engine support and feature support, routes to the exact docs page, fetches it live, and applies it - while carrying the curated Unreal-specific knowledge the docs do not have (the `ApiKey`/`BeginPlay` ordering trap, the UMG widget layer, cooking, and the per-platform config that decides whether a packaged build is usable).

**Rules (read once per session):** [`RULES.md`](RULES.md) - non-negotiable rules + Unreal pitfalls. Read before writing any code.

---

## Step 0: Three gates, before any code

Resolve all three from the user's words plus a read-only probe. Each one can change the answer from "here is the code" to "that is not possible" - so none of them is optional, and none of them belongs in a compile error later.

### Gate 1: engine version (picks the release asset, or stops the task)

| Target engine | What to do |
|---|---|
| **5.7 or 5.8** | Supported. Download the matching release asset - see [`setup.md`](setup.md) 2. |
| 4.27 / 5.0 / 5.1 | Only [v1.3.0](https://github.com/GetStream/stream-chat-unreal/releases/tag/v1.3.0) (Dec 2022) covers these. Say so: the API predates v2.0.0, `BlockUser`/`UnblockUser`/`GetBlockedUsers` do not exist, and none of this skill's v2 guidance is guaranteed to apply. |
| **5.2 through 5.6** | **Hard stop - no release supports these.** Say it immediately. The options are: upgrade the project to 5.7/5.8, or build the plugin from source against an unsupported engine (unverified, not recommended). Do not download an asset and hope. |

Detect the version from the `.uproject` rather than asking:

```bash
find . -maxdepth 2 -name "*.uproject" -exec sh -c 'echo "== $1"; grep -m1 EngineAssociation "$1"' _ {} \;
```

There is **one release archive per engine version** (`StreamChat-5.7.zip`, `StreamChat-5.8.zip`) and picking the wrong one is a silent mismatch, not a clean error. Resolve the version *first*, then download.

### Gate 2: feature support (say no in the plan, not in a compile error)

Not implemented in the Unreal SDK as of v2.0.0. If the request needs one of these, say so **before** writing code:

- Attachments and file/image uploads
- Sending threaded replies, and the thread list
- Quoted messages, mentions, pinning messages
- Offline persistence and optimistic sending
- Channel archiving and channel pinning
- Polls, draft messages, message reminders, location sharing

Implemented: messaging (send / edit / fetch / full-text search / soft delete, hard delete from C++, C++ pagination both directions), channels (query / watch / create / update / truncate / hide+show / freeze / members), reactions (score + enforce-unique, remove, C++ pagination), read state and unread counts, typing indicators, moderation (ban, shadow ban, mute users, mute channels, **block and unblock users**, flag messages and users, query banned users), slow mode, push device registration, presence + watchers + own-capabilities, real-time events, and preview UI widgets.

> **The docs contradict the SDK here.** The Unreal introduction page still lists "User blocking" as not implemented, but `BlockUser`, `UnblockUser`, and `GetBlockedUsers` all ship on `UStreamChatClientComponent` in v2.0.0. Trust the SDK. The [repo README feature list](https://github.com/GetStream/stream-chat-unreal#feature-support) is the accurate one.

### Gate 3: C++ or Blueprint

Ask only if genuinely unclear; otherwise infer (a `Source/` dir with a `.Build.cs` means C++ is available).

- **C++** is the full surface. Callback-based (`TFunction<void(...)>`), `TOptional<>` parameters, and all pagination.
- **Blueprint** covers the common operations as latent nodes, with `...BP`-suffixed variants where the C++ signature takes `TOptional` (`SendMessageBP`, `BanUserBP`, `ShadowBanUserBP`, `MuteUserBP`, `BanMemberBP`).
- **Pagination and the lower-level APIs are C++ only.** If the user wants a Blueprint-only integration, say up front which parts will need C++ - and note the naming trap: `BanUserBP(User, FTimespan, FString, bool)` takes required args where `BanUser(User, TOptional<FTimespan>, TOptional<FString>, bool)` takes optional ones. A zero `FTimespan` means "unlimited", not "already expired".

---

## The docs convention - and the coverage caveat that matters here

Every Stream docs page has a Markdown twin: **take the page URL, drop the trailing `/`, add `.md`.**

```
https://getstream.io/chat/docs/unreal/query-channels/   ->   https://getstream.io/chat/docs/unreal/query-channels.md
```

Always fetch the `.md` variant - clean Markdown, verbatim code, no page chrome. The live index that lists every Unreal page: `https://getstream.io/cli/docs/chat-unreal.md`.

**Now the caveat, and it is the single most important thing about this docs tree.** The `/chat/docs/unreal/` tree is largely the shared cross-SDK prose. Only about **26 of its 61 pages carry an `Unreal` code tab**; the rest show JavaScript, Node, Kotlin - even a C#/Unity sample on the rate-limits page. Several pages document features the Unreal SDK **does not have at all** (`file-uploads`, `threads`, `pinned-messages`, `polls-api`, `drafts`, `message-reminders`, `location-sharing`, `archiving-channels`, `pinning-channels`) with working JavaScript and no per-page warning. And some pages for features the SDK **does** have carry no Unreal code (`send-reaction`, `moderation`, `search`, `message-delivery-and-read-status`, `freezing-channels`).

So:

1. **Never translate a JavaScript snippet into C++.** `channel.sendReaction(...)` does not tell you the shape of `UChatChannel::SendReaction`. A JS-only page is a page whose *concepts* apply and whose *code* does not.
2. When the page has no Unreal tab, get the API from the **source of truth ladder** below instead, and say where you got it.
3. [`docs-map.md`](docs-map.md) marks per-page Unreal coverage. Use it - it saves a wasted fetch and a wrong signature.

### Source-of-truth ladder

Walk it in order. Stop at the first rung that answers the question, and cite which rung you used.

| Rung | Source | Use for |
|---|---|---|
| 1 | The page's **`Unreal` code tab** ([`docs-map.md`](docs-map.md) says which pages have one) | Anything covered. Copy verbatim. |
| 2 | **Plugin headers** - `Plugins/StreamChat/Source/StreamChat*/Public/**.h` in the user's project, else `raw.githubusercontent.com/GetStream/stream-chat-unreal/<tag>/...` | Exact signatures, defaults, `UFUNCTION` metadata, Blueprint availability. The final authority. |
| 3 | **Doxygen C++ reference** - https://getstream.github.io/stream-chat-unreal/ | Browsing the class surface when you do not know the header name. |
| 4 | **The sample project** - the repo root *is* the sample: `Source/StreamChatSample/`, `Source/DocsSamples/` | Real wiring end to end. `StreamChatSampleHud.cpp` is a working connect + query + show-UI in 40 lines. |

Read the headers from **the version the project actually vendors** (the plugin is copied into `Plugins/`, so it is right there - prefer it over GitHub `main`).

**URL grounding:** only fetch a page URL you got from [`docs-map.md`](docs-map.md) or from a live index fetch in this conversation. Do not invent doc paths from memory.

---

## Step 1: Classify the request

With the gates passed, pick the mode:

- **How-to / reference** ("how do I query channels?", "what does `EChannelFlags::Watch` do?") -> go straight to **Docs lookup**. No setup, no credentials.
- **Integrate** ("add chat to my game", "wire Stream into this project") -> run [`setup.md`](setup.md), then **Docs lookup** per feature.
- **New project** ("build me an Unreal chat app") -> [`setup.md`](setup.md) then **Docs lookup**, scoped to the requested screens. If there is **no** Unreal project, tell the user to create it in the Epic launcher / Unreal Editor first - do not try to scaffold a `.uproject` by hand.
- **Chat UI** ("show a channel list", "put chat on the HUD", "style the message bubbles") -> run [`widgets.md`](widgets.md). This layer has **no official documentation at all**, so the runbook is the source: the `WBP_*` inventory, the `LoadClass`-by-path pattern, the `Setup()`-before-`AddToViewport()` rule, the context-ancestor model, theming, and the cook directive that path-loading requires.
- **Package / ship / run on device** ("build for iOS", "why is it frozen on my phone?", "package for Android") -> run [`platforms.md`](platforms.md). The per-platform config there is load-bearing, not polish: without it a packaged mobile build is variously unreadably small, frozen a few frames in, or deaf to touch.

If the user asks for a chat UI and has not said which, **prefer the shipped `WBP_*` widgets** over hand-built UMG for a first integration - they carry the safe-area handling, theming, and list pagination that is tedious to reproduce.

---

## Step 2: Docs lookup (every request ends here)

1. Open [`docs-map.md`](docs-map.md). Find the row for the feature; it gives the exact `.md` URL **and whether that page has Unreal code**.
2. If the feature is not in the map, fetch the live index (`https://getstream.io/cli/docs/chat-unreal.md`) and pick from it.
3. **Fetch the `.md` page(s)** with WebFetch. At most 3 per request; beyond that, hand the user the index URL.
4. If the page has an Unreal tab, use its code verbatim, adapting only to the project's actor/lifecycle shape. If it does not, drop to rung 2 of the ladder and read the header.
5. **Cite what you used:** `Source: [Title](https://getstream.io/...)`, or `Source: Plugins/StreamChat/Source/StreamChat/Public/Channel/ChatChannel.h` for a header. Never answer SDK specifics from training data - if you did not read it this conversation, read it now or say you could not find it.
6. **Apply best practices** - one `QueryChannels` with a filter, then `Watch` plus WebSocket events; no per-tick queries; connect once. See [`RULES.md`](RULES.md) "Mindful API usage".

---

## What this skill carries

The official docs cover the low-level client well where they have Unreal tabs, so this skill does not restate them. The curated, non-doc content is:

| File | What it is |
|---|---|
| [`RULES.md`](RULES.md) | Non-negotiable rules + the Unreal pitfalls that break builds or fail silently. Every rule is stated once, here. |
| [`setup.md`](setup.md) | Engine-version-aware plugin install, `Build.cs` module deps, CLI credentials, and the verified minimal client wiring. |
| [`widgets.md`](widgets.md) | The UMG widget layer - undocumented upstream. Inventory, path-loading, `Setup` ordering, contexts, theming, cooking. |
| [`platforms.md`](platforms.md) | iOS / Android / desktop config, signing, and the build-vs-package distinction. Includes deploy + log-reading commands. |
| [`docs-map.md`](docs-map.md) | Intent -> exact docs page, annotated with per-page Unreal-code coverage, plus the source-code fallback. |

---

## Support

If the user asks for support or how to contact someone, direct them to [getstream.io/contact](https://getstream.io/contact/). SDK gaps and feature requests go to [the repo issues](https://github.com/GetStream/stream-chat-unreal/issues).
