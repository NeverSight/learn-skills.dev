---
name: gather
description: Collects references from the user's own library, their boards and pattern sites onto one linked board before a design is built.
---

# Gather

This skill collects inspiration before a design is built or reworked. It searches the user's own saves first, then wider sources, and returns one board where every reference links back and names what to take.

## Evidence for a choice, not a style to copy

A reference shows how one part could work. Taking a whole app's look when the user asked for its top bar is a finding. With no number given, gather at least 20 references from at least three sources.

Use it when the user asks for inspiration, references or "inspo", or says a screen looks bad and asks how to improve it. Building variants from the board belongs to `prototype`. Rebuilding one reference value for value belongs to `match`.

## 1. Name the brief

Write one line naming the surface, its platform and what to look for: layout, navigation, density, type, colour, motion or overall taste. A search with no target is `gather-name-the-brief`.

Search on the same platform as the work. A desktop or web app takes web and desktop references. Mobile screens for a desktop app is `gather-same-platform`.

## 2. Start with what the user gave

Open the tabs, screenshots, links and design files already in the thread before searching anywhere. Searching a pattern library while the user's screenshots sit open in the browser is `gather-start-with-given`.

## 3. Search the user's own taste first

Search the user's own library and boards before public sources. Their saves already reflect their taste. Starting from a public library when their own library holds matching saves is `gather-own-library-first`. If none of the user's sources are connected, stop and name each choice: Pond, marked.dev, Are.na, Cosmos, Pinterest and Mobbin. A prompt that drops one of those names is `gather-list-the-sources`. How to reach each source is in [sources.md](sources.md).

## 4. Go wide

Pull from at least three sources. Pattern libraries show flows and screens. Curated galleries show finished sites and brand work, picked by hand. Boards and saves show taste: type, colour, photography and mood. A board drawn from one app is `gather-go-wide`.

Gather the number asked for. When the user asks for more, return new references and leave out those already shown. Repeats under "50 more" is `gather-enough-to-choose`.

## 5. Judge every candidate by eye

A separate agent makes the cut. It gets the candidates, the brief and `.gather/taste/taste.md`, never the queries or sources behind them. The searching agent cutting its own finds is `gather-separate-judge`.

Open each candidate at full resolution, crop to the part the brief names and look at that. A reference kept on its title, metadata or a preview is `gather-look-at-every-image`.

Compare each crop side by side with the closest Yes and No entries, and never give it a score. A win counts only when it holds with the two images swapped. A 1–10 rating, or a win taken in one order, is `gather-compare-not-score`.

Pull about three times the number asked, then cut. Cut what shares a reason under No. A candidate kept against a No reason is `gather-judge-against-taste`.

Cut only clear misses. When two references sit close, both stay on the board and the user decides. A close call settled by the agent is `gather-cut-clear-misses`.

While the taste file holds fewer than 40 entries, show twice the number asked so picks fill it faster. Twenty shown against a six-entry file is `gather-warm-up-taste`.

With no taste file yet, judge against the brief and start the file from the first picks.

## 6. Note the part and the link

Each reference gets one line naming the part to take, such as "the top bar" or "the empty state". A reference with no note is `gather-name-the-part`. Each one keeps its source link, so the user can open the original. An image with no link is `gather-link-every-reference`. Mark each reference `Shipped` or `Concept` in its `details`. A concept shot shown as a shipped product is `gather-concept-or-shipped`.

## 7. Build one board and open it

Copy [board.html](board.html) to `.gather/<brief>/index.html`, an ignored folder and never the source tree. Write `board.js` beside it in the shape its header comment shows, with images in `img/`, then open it. Links pasted in chat instead of a board is `gather-one-board`.

The board's look ships with the skill, so write data only. A page with its own markup or styles is `gather-shipped-board`.

Name each group in two or three words of Title Case, such as "Agent Activity", and put the detail in its note. A group named like a sentence is `gather-short-group-names`.

## 8. Learn from the picks

The user marks picks with Keep on the board and pastes them back with Copy Picks. Add each pick under Yes in `.gather/taste/taste.md`, copying its image into `.gather/taste/img/`. Then ask once what makes the picks right and what the rest got wrong. Write each answer under No beside the references it names. Picks taken with the taste file unchanged is `gather-grow-taste`.

```md
## Yes

- ![](img/4c03063e.jpg) [Linear](https://mobbin.com/screens/4c03063e) - type does the work, no decoration

## No

- ![](img/9f12ab07.jpg) [Acme](https://acme.com) - gradient blob hero, reads as a template
```

Every entry holds the image, its link and the reason in the user's words. An entry with no reason, or the board note in place of the user's words, is `gather-taste-reasons`.

## 9. Save what the user keeps

When the user asks to save the picks, send them where they say: their library, a channel or a board. Read the destination's naming first and match it. A new channel named "FW 26 🔥" beside `fashion / inspiration / 2026 / fall winter` is `gather-match-the-naming`.

Check for each item before adding it. A second copy of a saved item is `gather-no-duplicates`. When a source needs a login or a CAPTCHA, stop and say which one. Working around a login is `gather-ask-at-login`.

## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `gather-name-the-brief` | "Searching settings pages" | "Desktop settings page, looking for grouping and density" |
| `gather-same-platform` | iOS screens for a desktop app | `platform: "web"` and desktop apps |
| `gather-start-with-given` | A pattern-library search while the user's tabs are open | The open tabs read first |
| `gather-own-library-first` | A public library searched first | The user's library searched first, then wider |
| `gather-list-the-sources` | "Connect your accounts, or download Pond" | Pond, marked.dev, Are.na, Cosmos, Pinterest and Mobbin, each named |
| `gather-go-wide` | Twenty screens from one app | Saves, boards and a pattern library |
| `gather-enough-to-choose` | "50 more" returns the first 20 again | 50 new references, earlier ids excluded |
| `gather-separate-judge` | The searching agent cutting its own finds | A second agent cuts from the candidates, the brief and `taste.md` |
| `gather-look-at-every-image` | A screen kept on its title or a preview | The top bar cropped at full resolution and looked at |
| `gather-compare-not-score` | "This one is a 7 out of 10" | Beats the closest Yes entry in both orders |
| `gather-judge-against-taste` | A gradient blob hero kept while No lists one | Cut, it shares "gradient blob hero, reads as a template" |
| `gather-cut-clear-misses` | Two close references, one cut by the agent | Both on the board for the user |
| `gather-warm-up-taste` | 20 shown against a six-entry taste file | 40 shown until the file holds 40 entries |
| `gather-name-the-part` | A screenshot with no note | "Take the grouped list, not the colours" |
| `gather-link-every-reference` | An image with no source | The image linked to its original |
| `gather-concept-or-shipped` | A Dribbble concept shown as a product | `details: { Kind: "Concept" }` |
| `gather-one-board` | Twenty links pasted in chat | `.gather/settings/index.html` opened, grouped by idea |
| `gather-shipped-board` | A board page written from scratch | `board.html` copied, only `board.js` written |
| `gather-short-group-names` | "Activity: thinking, tool calls and steps" | "Agent Activity" |
| `gather-grow-taste` | Picks pasted back, `taste.md` unchanged | Picks under Yes, the user's reasons for the rest under No |
| `gather-taste-reasons` | `- ![](img/4c03063e.jpg)` | `- ![](img/4c03063e.jpg) [Linear](https://mobbin.com/screens/4c03063e) - type does the work` |
| `gather-match-the-naming` | A new channel named "FW 26 🔥" | `fashion / inspiration / 2026 / fall winter` |
| `gather-no-duplicates` | The same pin added twice | Existing items checked and skipped |
| `gather-ask-at-login` | A login worked around | "Pinterest needs you to sign in" |

## Reporting

**Severity.** `HIGH` is a whole look copied when one part was asked for, or items saved twice or under the wrong name. `MEDIUM` is the wrong platform, one source only, a board with no links, a hand-written board or a public search that skipped the ask. It is also a reference kept unseen or against the taste file, a score in place of a comparison or a self-judged cut. So is a close call settled by the agent, a concept shown as shipped or picks left out of the taste file. `LOW` is a reference with no note on what to take, a long group name or a taste entry with no reason. So is a short board while the taste file warms up.

**Format.** One finding per root cause, citing the request when no file applies:

```
file:line - [rule-id] what is wrong
request 2 - [rule-id] what is wrong
```

Then a `Rule | Count | Severity` summary. `Block` when any `HIGH` remains, `Approve` otherwise. Mark every source you could not reach as `Not verified`.
