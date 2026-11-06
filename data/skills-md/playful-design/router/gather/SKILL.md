---
name: gather
description: Collects references from the user's own library, their boards and pattern sites onto one linked board before a design is built.
---

# Gather

This skill collects inspiration before a design is built or reworked. It searches every source at once, fills one board as results land and links every reference back with the part to take.

## Evidence for a choice, not a style to copy

A reference shows how one part could work. Taking a whole app's look when the user asked for its top bar is a finding. With no number given, gather at least 20 references from at least three sources.

Use it when the user asks for inspiration, references or "inspo", or says a screen looks bad and asks how to improve it. Building variants from the board belongs to `prototype`. Rebuilding one reference value for value belongs to `match`.

## 1. Name the brief

Write one line naming the surface, its platform and what to look for: layout, navigation, density, type, colour, motion or overall taste. A search with no target is `gather-name-the-brief`.

Split the brief into its parts, such as "top bar", "empty state" and "row density", and give each part two or three synonyms. Queries come from the parts, two or three words each. One long query carrying the whole brief is `gather-split-the-brief`.

Search on the same platform as the work. A desktop or web app takes web and desktop references. Mobile screens for a desktop app is `gather-same-platform`.

## 2. Start with what the user gave

Open the tabs, screenshots, links and design files already in the thread before searching anywhere. They seed the image searches in step 4. Searching a pattern library while the user's screenshots sit open in the browser is `gather-start-with-given`.

## 3. Offer to connect what is missing

Check which of Pond, marked.dev, Are.na, Cosmos, Pinterest and Mobbin are connected. Ask once, with each missing source as its own option and carrying on as another. A question that drops a missing source, or searching past one without asking, is `gather-offer-to-connect`.

When none are connected, wait for the answer. How to connect each source is in [sources.md](sources.md).

## 4. Search every source at once

Start one agent per connected source, or run their searches as parallel calls where agents are unavailable. Each writes `candidates/<source>.json` in the shape [sources.md](sources.md#candidates) shows. Searching one source after another is `gather-parallel-sources`.

When Mobbin answers that monthly usage is high, stop calling it, tell the user and carry on with the other sources. Search Mobbin again only when the user asks for it by name. Another Mobbin call after that warning is `gather-stop-at-usage-limit`.

The user's own saves lead each group. A board with nothing from Pond or marked.dev while either holds matches is `gather-own-library-first`.

Pull from at least three sources. Pattern libraries show flows and screens, curated galleries show finished work and boards show taste. A board drawn from one app is `gather-go-wide`.

Seed image searches from what the user gave and from their closest saves, through Pond `visual` and Cosmos. Text queries alone when the user shared screenshots is `gather-search-by-image`.

When the best reference is a shipped product, open its live page and screenshot the part. A gallery thumbnail of a site that is one click away is `gather-capture-live`.

Pull about twice the number asked, then cut. When the user asks for more, leave out every url already on the board. Repeats under "50 more" is `gather-enough-to-choose`.

## 5. Collect into one board

Run the collector once the first candidates land and open the board straight away. It copies the board page, downloads every image and video and fills the board live as agents finish.

```sh
node <skill>/collect.mjs .gather/<brief> --serve
```

`.gather/` stays out of version control. Write the title, brief and group order to `.gather/<brief>/board.json` as [sources.md](sources.md#board) shows. Links pasted in chat instead of a board is `gather-one-board`.

The collector and the board ship with the skill, so a run writes data only. A hand-written board page, or a per-run script that downloads or builds, is `gather-shipped-collector`.

## 6. Look at every reference

Open each downloaded file and look at the part the brief names. A reference kept on its title, metadata or a preview is `gather-look-at-every-image`.

Cut only clear misses, by adding their url to `cut` in `board.json`. When two references sit close, both stay and the user decides. A close call settled by the agent is `gather-cut-clear-misses`.

Each reference gets one note naming the part to take, such as "the top bar". A reference with no note is `gather-name-the-part`. Each keeps its source link. An image with no link is `gather-link-every-reference`.

Mark each reference `Shipped` or `Concept` under `Kind` in its `details`. A concept shot shown as a shipped product is `gather-concept-or-shipped`.

Name each group in two or three words of Title Case, such as "Agent Activity", and put the detail in its description. A group named like a sentence is `gather-short-group-names`.

When the cut is done, run the collector once more with `--done` so the board stops reloading.

## 7. Act on what comes back

The board copies three prompts. Copy Picks returns the picks with the user's notes, which become the brief for the next step. More Like This returns one reference. Save Picks returns the picks to save.

For More Like This, seed an image search from that reference and keep to its group, with every url on the board left out. A text search on its title is `gather-more-from-the-pick`.

## 8. Save what the user keeps

Send picks where the user says: their library, a channel or a board. Read the destination's naming first and match it. A new channel named "FW 26 🔥" beside `fashion / inspiration / 2026 / fall winter` is `gather-match-the-naming`.

Check for each item before adding it. A second copy of a saved item is `gather-no-duplicates`. When a source needs a login or a CAPTCHA, stop and say which one. Working around a login is `gather-ask-at-login`.

## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `gather-name-the-brief` | "Searching settings pages" | "Desktop settings page, looking for grouping and density" |
| `gather-split-the-brief` | `query: "desktop settings page with grouped dense options"` | `"settings groups"`, `"preferences list"`, `"dense settings"` |
| `gather-same-platform` | iOS screens for a desktop app | `platform: "web"` and desktop apps |
| `gather-start-with-given` | A pattern-library search while the user's tabs are open | The open tabs read first |
| `gather-offer-to-connect` | Pond searched alone while marked.dev and Mobbin sit unconnected | "Connect marked.dev or Mobbin, or carry on with Pond?" |
| `gather-parallel-sources` | Pond, then Mobbin, then Cosmos, one after another | One agent per source, started together |
| `gather-stop-at-usage-limit` | Mobbin searched again after "your monthly usage is high" | "Mobbin says monthly usage is high, so I've stopped searching it" |
| `gather-own-library-first` | A board of Mobbin screens while Pond holds matches | The user's saves first in each group |
| `gather-go-wide` | Twenty screens from one app | Saves, boards and a pattern library |
| `gather-search-by-image` | Text queries while the user's screenshot sits in the thread | `search_library` with `visual` seeded from it |
| `gather-capture-live` | A Land-book thumbnail of linear.app | A screenshot of the live top bar, linked to linear.app |
| `gather-enough-to-choose` | "50 more" returns the first 20 again | 50 new references, earlier urls left out |
| `gather-one-board` | Twenty links pasted in chat | `.gather/settings/` served and opened, grouped by idea |
| `gather-shipped-collector` | A `build.mjs` written for this run | `node collect.mjs .gather/settings --serve` |
| `gather-look-at-every-image` | A screen kept on its title or a preview | The downloaded file opened and the top bar looked at |
| `gather-cut-clear-misses` | Two close references, one cut by the agent | Both on the board for the user |
| `gather-name-the-part` | A screenshot with no note | "Take the grouped list, not the colours" |
| `gather-link-every-reference` | An image with no source | The image linked to its original |
| `gather-concept-or-shipped` | A Dribbble concept shown as a product | `details: { Kind: "Concept" }` |
| `gather-short-group-names` | "Activity: thinking, tool calls and steps" | "Agent Activity" |
| `gather-more-from-the-pick` | More Like This searched as "Linear settings" | An image search seeded from the picked screen |
| `gather-match-the-naming` | A new channel named "FW 26 🔥" | `fashion / inspiration / 2026 / fall winter` |
| `gather-no-duplicates` | The same pin added twice | Existing items checked and skipped |
| `gather-ask-at-login` | A login worked around | "Pinterest needs you to sign in" |

## Reporting

**Severity.** `HIGH` is a whole look copied when one part was asked for, or items saved twice or under the wrong name.

`MEDIUM` is the wrong platform, one source only, sources searched in turn, a board with no links or a hand-written board or build script. It is also a search that skipped the connect question or the user's own saves. So is a reference kept unseen, a close call settled by the agent or a concept shown as shipped. So is a Mobbin call after its usage warning.

`LOW` is one long query, text search where an image search fits or a gallery thumbnail of a live site. So is a reference with no note, a long group name, repeats under "more" or More Like This searched by title.

**Format.** One finding per root cause, citing the request when no file applies:

```
file:line - [rule-id] what is wrong
request 2 - [rule-id] what is wrong
```

Then a `Rule | Count | Severity` summary. `Block` when any `HIGH` remains, `Approve` otherwise. Mark every source you could not reach as `Not verified`.
