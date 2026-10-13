---
name: search
description: How to search Mobbin well. Use before every call to search_screens, search_flows or search_sections. Covers the tool and mode, writing an effective query, pulling more results, and what to do when a search falls short.
---

# Searching Mobbin

**Read best practices first.** If the Mobbin `best-practices` skill hasn't been read in this conversation, invoke it before searching, since it says when a search should run at all and when another skill should run it.

A calling skill may set its own search rules, such as how many queries per problem or which mode to use. Where they differ from these, the calling skill's rule wins.

## How search works

- **Search matches meaning, not keywords.** Describe what you would see.
- **Name an app only when the task needs it.** Adding an app name to the query filters results to that app. But not every result is from that app, so check `app_name` and `site_name` before citing.
- **The query also sets a language filter** on screens and flows when it names one ("Japanese banking app"). Name a language only when the task needs it.
- **When results are weak, change the query.** Raising `limit` or resending the query as it was brings back the same matches. To get more results for a query that works, see [A second pull](#a-second-pull).

## Choosing the tool

| Target | Tool |
|---|---|
| A screen or component in an app | `search_screens` with `platform` |
| A section of a marketing site (hero, pricing, feature grid, footer) | `search_sections`, which takes no `platform` |
| A journey, or one screen whose place in a journey matters (the verify-email step of sign-up) | `search_flows` with `platform`. For one screen, pick it from the flow's screens. Only some screens come with a preview; open the `image_url` of any other before citing it |

`platform` is `ios` or `web`, and it is the only filter you set. The tools have no Android, so an Android target searches `ios`. Say the references are iOS wherever you cite them.

## Choosing the mode

`mode` is on `search_screens` only.

- **`deep`** for a query with several parts ("paywall with lifetime option and a discount").
- **`standard`** for a lookup within one named app ("Calm paywall").
- When unsure, `deep`.

`deep` drops matches it scores as weak, so it can return fewer results than `limit`. A short pull means few close matches, not that Mobbin has none. Send a second pull or change the query before you say something is missing.

## Writing the query

**One screen, flow or section per query, with at most three constraints.** Start with the type, then add the state or step and the visible parts the task turns on. The type is the target. Each state, step or part is one constraint: "paywall with plan cards and a free trial button" has two. Length is not the limit. A long query about one target works as well as a short one, but too many constraints blur the results.

Rules:

- **Search at the target's level.** A screen target searches the whole screen ("expense tracker home with no transactions"), never one card of it. A component target searches the screen it lives on.
- **When the task is choosing between options, name the part, not one of the options.** The results need to show more than one way to solve it: "paywall with plan cards and a free trial button", not "paywall with a yearly toggle". Don't join options with "or", and don't put a fix in the query ("with a prompt to add", "placeholder bars"). When the task is finding that exact thing, name it ("banking app search tab with a text label").
- **Say each thing once.** "Empty state", "no transactions yet" and "before any are added" are one state. Keep the shortest.
- **A fourth constraint goes in a second query.** Don't add it to the first.

| Don't | Do |
|---|---|
| "paywall where the trial button is buried below a long table" (the problem in the query) | "paywall with plan cards and a free trial button" |
| "expense tracker home overview in empty state with no transactions yet and prompt to add first expense" (the state said twice, a fix named) | "expense tracker home with no transactions" |
| "spending chart card with no data yet, placeholder bars or empty donut" (one card of a screen target, two options joined by "or") | "spending overview with no transactions" |
| "ios signup screen" (platform in the query) | "signup screen", with `platform` `ios` |
| "clean modern invoice list for Acme" (taste words, the user's product) | "invoice list with filter chips" |
| "login screen without Google sign in" (a negation boosts the thing negated) | "login screen with only email and password fields" |
| "onboarding paywall settings" (several screen types in one query) | one call per screen type |
| "toast" (one ambiguous word) | "toast notification confirming an item was saved" |
| "pricing page with hero, plans and FAQ" (several sections in one query) | "pricing section with three tiers and an annual toggle" |
| "invite teammates screen" (one screen, when the target is a journey) | "inviting teammates during workspace setup", on `search_flows` |

Leave out the user's copy, data and brand, and instructions such as "examples of" or "best". Visual traits Mobbin tags can help when they matter: `dark mode`, `bottom sheet`, `modal`, `full-screen`, `card-based`.

When a pull returns products from outside the task's domain, search again with the domain's noun ("meditation app paywall with plan cards") instead of citing them. If you do cite a product from another domain, say it is there for its structure only.

## A second pull

When a pull doesn't cover what you need, send the same query again with the tool's way of getting more results. That brings new results instead of the first ones reordered. Changing the query makes it a new search, even with exclusions.

- `search_screens`: the same query and `mode`, with every id already seen in `exclude_screen_ids`, up to 100.
- `search_sections` and `search_flows`: the next `page`, dropping results already seen. When `has_next_page` is false, there is no next page, so change the query instead.

## When a search falls short

Handle each case as below. When one still fails, say so in one line, where the calling skill reports a lost search or in the reply when there is none.

**A named product doesn't come up**, meaning it's in no result's `app_name` or `site_name`:

1. If the query spelled the name differently from the product, search again with the product's own spelling.
2. On sections, which have no name filter, ask for the next `page` while `has_next_page` is true. The site may rank past the first page.
3. On screens and flows, when the task isn't tied to one platform, try the other `platform`, since a product can be on Mobbin for iOS or web only. Cite what you find as that platform. Skip this step when the task is for one platform (an iOS redesign has no use for a web screen).

If it's still missing, carry on with the category search. Describe nothing about the product from memory, and don't let another product's screen stand in for it. A screenshot the user shared of it stays their reference.

**Images don't open.** Previews come as `webp`, which not every host can open. Call again with `image_format` set to `jpg`. If they still don't open, cite nothing from that call, since a screen you couldn't see is not a reference.

**The tool refuses the call.** Don't retry it or change the query, since every call will be refused. Stop searching and say so. An error about the input, such as an invalid argument, is different: fix the input and call again.
