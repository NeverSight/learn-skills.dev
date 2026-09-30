---
name: ev
description: Agent-first home inventory. Use when the user talks about where things are at home (shelves, drawers, boxes, storage, pantry, car), wants to record, find, move, give away, sell or throw out belongings, or mentions `ev`, labels like `K4x4-07-Ü` or `S5-01`, or a lost item.
---

# ev — home inventory for an agent in conversation

The person stands at the shelves and reports; you record through `ev`; either of you asks
`ev` where something is. `ev` prints JSON when piped, so read its stdout as JSON and its
stderr as the error channel.

## Model in one paragraph

Everything is a node in one tree: `home` › `room` (rooms may nest) › `furniture` ›
`container` › `item`. `kind` is only a label — any node can hold other nodes. Codes are
what is printed on the physical labels (`K4x4-07-Ü`, `S5-01`): use them exactly as the
person gives them, never invent one. A node leaves in two steps (`dispose --as` then
`gone`) or one (`gone --as`). A node whose place is unknown is `lost`.

## The conversation loop

1. **Record what the person reports.** Enter a box and its contents in one call with
   `ev add --stdin` (NDJSON; a line with `"key":"b"` can be referenced by later lines as
   `"in":"@b"`). Batches are all or nothing.
2. **Propose, don't assume a move happened.** Plan it with `ev move <x> --to <y> --plan`,
   tell the person where it goes, and only after they say they did it run `ev done <x>`.
   `ev pending` is the checklist. A planned move is also how you park a thing whose right
   place is not settled yet: plan it towards the likeliest holder, and when you later go
   through that holder, bring up everything planned to arrive there so the person decides
   whether it really belongs.
3. **Nothing is finished until the person says so.** A photo of "the current state" is not
   "done". Never mark a bag, drawer or task complete — and never `gone` a record — on your own
   reading; ask. A mistaken `gone` is corrected with `ev restore X --correction "<why>"`.
4. **Leaving the home.** Set aside: `ev dispose <x> --as trash|give|sell`. Actually gone:
   `ev gone <x>` (or `ev gone <x> --as trash` when it is thrown out on the spot). Record
   what the person said about it with `--why "<text>"` ("probably thrown out" is a reason,
   not certainty). A gone node is still reachable by id: `ev show <id> --include-gone`,
   `ev history <id>`, and `ev edit <id> note=…` to annotate it later.
   `ev disposals` lists what is waiting in each pile. A record that was never real (misread
   from a photo, entered twice) is closed with `ev gone <x> --as mistake --why "<what>"`, not
   as trash.
5. **What the person tells you about a thing goes into its `note`** — what it is for, where it
   came from, why they keep it ("a wrench that came with the kitchen tap, kept because it is
   often needed"). That knowledge is what makes a later decision possible; record it the moment
   they say it, in their words, with the date.
6. **Uncertainty goes into `note`**, never guessed into a field. If you are not sure what
   something is, ask the person, then record the answer.
7. **Lost:** `ev lost <x>` keeps the last seen place; `ev lost` lists them; `ev found <x>`
   clears it in place; any move clears it too.

## The plan: start every session with `ev next`

`ev` keeps the work list, so no session starts from memory. Run `ev next` first and tell the
person, in one short paragraph, what today's task is and why, what is planned to arrive at its
places, and how far the whole home is (`progress`). Then:

- **Ask the goal once.** If `goal` is null, ask whether they want to put things in order
  (`ev goal organize`) or only keep the records right (`ev goal track`). Under `track`, never
  propose tidy-up tasks, moves or disposals of your own; record what they report, answer where
  things are, and keep only the tasks they ask for. Under `organize`, a place they want left
  alone is `ev review <place> --as kept` — respect it and drop it from proposals.
- **Build the plan from what you see.** When looking at a place's photo, write what you notice
  as `ev observe <place> "<text>" --photo n` (a bag of mixed screws, a box that does not match
  the drawer's theme, things that belong elsewhere). **The records are the current state; a
  photo is the moment it was taken.** Before writing an observation from a photo, compare it
  with `ev show <place>` — things may have been moved out, thrown away or sorted since — and
  say which one you describe. Turn it into tasks with
  `ev task add "<title>" --why "<reason>" --on <place> --at <n>`. The reason is what makes the
  order defensible: mess, uncertainty (records guessed from a photo), blocking (a planned move
  waits on it), payoff (space freed, things to give or sell). Show proposed orderings as a
  numbered table and let the person reorder; `unplanned` in `ev next` lists raw places no task
  covers yet.
- **Work one task.** `ev task start <id>`, go through its places box by box, bring up
  everything under `arriving`, and add new tasks when you find work elsewhere.
- **Close only on the person's word.** When they say the place is done: `ev review <place>
  --as toured` and `ev task done <id>`; then run `ev next` again and say what comes next.
  A toured place that changed later shows in `progress` as `changed_since`; mention it.

## Everything waiting: `ev todo`

When the person asks what is left, or a session starts with no clear task, run `ev todo` and
summarise by kind with counts ("19 tasks, 8 moves, 2 things to return to Mahmutlar, 8 things
leaving, 1 thing to buy"). Most of it is state on the records — never copy it into tasks; it
leaves the list when you record the thing itself (`done`, `gone`, `back`, `found`, …).
Record the kinds that have their own verbs as you meet them:

- **A code you set** needs a label: after adding or re-coding a holder, say it goes on the
  label list (`ev label` prints it for the label maker); `ev label <ref>` only when the person
  says the label is on.
- **Something to buy or make** (a box ran out, a battery is low, a gridfinity bin to print):
  `ev need add "<what>" [--qty n] [--make] [--for <place>]`; `ev need got <id>` when it
  arrived, then record it in the tree.
- **Broken:** `ev broken <x> --note "<what is wrong>"`; `ev fixed <x>`; if it will not be fixed,
  propose `ev dispose`.
- **A use-by date** seen on a package or photo: `ev expires <x> 2026-07`.
- **Selling:** after `ev dispose <x> --as sell`, `ev sale <x> --listed --price n --where …`,
  then `--reserved`; when it is sold, `ev gone <x>`.
- **Photo of the current state:** every place should have a photo of how it is now — its own
  photo, or a crop cut for it from a wider one (a box out of a drawer photo).
  `photos` in `ev todo` lists the places without one or changed since; after a move or a
  tour, ask for a fresh photo of each place it touched and attach it (see **Photos**) with
  `--note "son hali, <date>"`. Older photos stay as history.
- **Gridfinity drawers:** give the drawer a grid once (`ev grid <drawer> --cols 6 --rows 7`,
  row 1 at the back) and place each box with `ev cell <box>=A3-B3`. Then `ev grid <drawer>`
  draws the map and lists free cells — propose places for new boxes from it, and name them by
  cell. When boxes trade places, give all of them their new cells in one
  `ev cell A=A3-B3 B=A4 C=B4 --recode` once the person has moved them: overlaps are checked
  against the final layout, and `--recode` renames each box after its back-left cell.
- **Unclear records** are names still guessed ("belirsiz", "muhtemelen"): ask about them when
  the person is at that place, then rename.

## Proposals the person can answer by number

Every table or list of proposed actions starts each row with a number (`#` column), so the
person can answer "did 1 and 3". Act only on the numbers they name; ask about the rest.

## Where should this go?

Never answer from memory. The decision is `ev suggest`'s ranking plus your judgement over it,
in this order:

1. **Describe it the way the inventory is written.** Name + part code + what kind of thing it
   is, in Turkish and English when both are used here: `ev suggest "KY-018 LDR ışık sensörü
   modülü"`, not just `KY-018`. The category words are what find the family box. For a thing
   already recorded use `ev suggest --for <ref>`: its own name, tags and note are the query.
2. **Read the ranking with its reasons.** `similar` is best first; each entry says which words
   matched, from which field or thing, and how many points. A match on a `specific` word
   (marked `*` in text output) says what the thing is; a match only on common words ("sensör",
   "modül") says only its family.
3. **If `new_group_likely` is true, nothing here is this kind of thing.** Do not squeeze it into
   the least bad box: propose a new group — an empty box or free cell first (`ev find kutu
   --tag "boş kap"`, the drawer's `grid.free`), or a mixed box if it is one of a kind.
4. **Check the rules and the room.** Every rule in `rules` applies. `room` comes from `fill`:
   `none` means the best box is full — say so and offer the next one or a bigger box; `unknown`
   or `stale` means estimate the fill from the photo (0/25/50/75/100) and record it with
   `ev edit <box> fill=N` before you rely on it.
5. **Say what you weighed**: "best: F2 (ışık*, ldr*; 69% of the description), room yes; rule 6
   applies; next was C5". The person can then disagree with a reason, not a guess.
6. **Turn corrections into data.** When the person picks another place, record why: a `theme`
   on the box, a rule (`ev rule add`), or a synonym (`ev synonym add "fotosel, ldr"`) when the
   miss was two words for one thing. Give boxes a `size` (`1x2x0.5`) and tag empty ones
   `boş kap`, so regrouping can offer them.

At the end of a drawer's tour, run `ev regroup <drawer>` and bring its findings as numbered
proposals: things better off elsewhere, mixed boxes, full boxes and the bigger spare box with
the cells it fits, nearly empty boxes to merge, unknown fills. `alone` lists things that share
no word with anything in their box: the other box there is only a guess (often wrong for
keepsakes and one-off tools, sometimes right, like a 9V battery among wires) — judge each one
yourself before proposing it. It only reports; nothing moves until the person says so. The same
suggestions show in `ev ui` when the person selects the drawer or a box. Run `ev audit` now and
then for alike things split across the house.

**Keep kinds apart with facets, not with prose rules.** When a drawer keeps two kinds of
things apart that share words (modules and bare parts, novels and technical books), a rule in
plain words is not read by `suggest` or `regroup`. Make it a facet: `ev facet add modül --words
"modül, kart"`, `ev facet add çıplak`, and tag each holder with its facet (`ev edit <box>
tags=+modül`). Things inherit their holder's facet and new things take it from their words;
holders of another facet are listed apart under `other_facet`, never proposed.
**Give every place a theme.** A theme is the summary every placement answer leans on: places
without one are where suggestions go wrong. While touring, run `ev themes <drawer>` (the
details in `ev ui` show the same): for each place it lists the words its contents share and the
themed place they read most like. Write a short theme in the person's words from that and from
what you see ("Antenler ve anten kabloları"), say it, and record it with
`ev edit <place> theme="…"` once they agree. Do not theme a place that has not been toured.
**Work you cannot do yet goes into the plan, not the records.** A move worked out before the
place is toured, a tag to add, a theme to decide: write it as `ev observe <place> "<text>"` so
`ev next` brings it up when that place's turn comes. Do not edit the records of a place that
has not been toured on the strength of the conversation alone; ask first. **Close the plan with
the work:** when you record what an observation asked for (the parts it said were waiting are
placed, the theme is set), remove it in the same step with `ev unobserve <id>` — the history
keeps both. Before you call a place done, read its `observations` in `ev show <place>`; one
left behind keeps coming back in `ev next` as work still to do.

## Photos

**Name every part by where it is in the photo, every time.** "The transistors" or "the
temperature sensors" is not enough, and neither is having described the position once further
up: the person matches your words to the picture, so each mention carries its place in that
photo — "left, the two on paper tape", "bottom row, all three", "top right, the big black
one", "2nd from the left in the middle row" — in tables, proposals and questions alike. A
proposal that says what goes where names both ends by position: the part in the photo and the
cell or box it goes to.

**Show a placement proposal, don't only write it.** When you propose where the things in a
photo go, mark both ends and put them on the person's screen together: the parts photo with a
numbered frame on each part (`ev photo mark <file> "1 → A6"=x,y,w,h …`), the destination with
the same numbers on its cells (`ev photo mark <drawer> 1=A6 2=B6 …`; `--grid <corners>` for a
photo cut before corners were kept), then both in one request, `ev focus --file <parts> --file
<drawer> --note "<what this is>"` (sent one after the other, the second would replace the
first). The person steps between them with `[` `]`, closes them with Esc and reopens them with
`m`; no need to send again. Open each marked file and check every frame sits on its part before
sending — the coordinates are your estimate. The marked copies are temporary (not stored, not
attached, no history); nothing needs undoing after the move. The text still names each part by
position, for a person reading without the screen.

**Don't ask for a drawer photo after every batch.** When parts go into a drawer batch by batch,
record each move as the person confirms it and ask for one photo of the drawer when the batches
are done; `ev todo` keeps the drawer on its photo list until then (a box added or changed after
the drawer's photo puts it back there, with `grid: true`).

**Every photo of a place is attached the moment it arrives** — including one the person sends
only to confirm a state ("son hali bu mu?"). A photo that confirmed something and was not
attached leaves the place's current photo older than the place, which is the exact slip this
rule exists for. The newest photo is the current one; older photos stay as history, never
replaced or removed.

When the person sends a photo of a drawer or box, first confirm its contents against the
records. Then attach it in one step. **A drawer with a grid is cut by its corners**:
`ev photo cut <photo> --place <drawer> --grid blx,bly,brx,bry,frx,fry,flx,fly` takes the grid's
four corners as fractions of the upright photo — back-left, back-right, front-right, front-left
— and cuts a crop for every placed box from the grid, with the photo's perspective, so no box is
left on an older photo. The corners are your estimate: run the same command with `--preview`
first (nothing is cut; every box is drawn framed on its cells) and look before cutting.
Otherwise `ev photo cut <photo> --place <holder> <box>=x,y,w,h
<item>=x,y,w,h …` puts the whole view on the holder and a crop on each box or item named
(`ev photo add <node> <photo> --crop x,y,w,h` does one); a crop named by hand wins over the
grid's for the same box. **Look at every crop you cut** (open the stored file) and redo it if
it shows the wrong thing — the coordinates are your estimate, the check is what makes them right.
**A group photo goes whole on one node only — the place — and every thing in it gets its own
crop.** `ev photo add` refuses a whole photo that is already attached whole elsewhere; when it
does, cut the crop — do not reach for `--whole` to get past it. `shared_photos` in `ev todo`
lists any slip of this kind. A photo of what is inside a bag or box goes on the things in it once
they are recorded, not on the bag. Close-ups the person sends later (screw heads, labels) go to
the item, cropped to the thing itself, and a photo of an empty holder goes to the holder. Photos
are copied into `~/.ev/photos`; the original may then be deleted.

**A tour is not finished on an old photo.** `ev review <place> --as toured` is refused while
the place or any placed box in its grid has no photo or one older than its last change
(`details.stale`); attach a current photo, or say an old one still holds with
`ev photo current <ref>`.

## Going somewhere

Whenever the person says they are going somewhere or meeting someone ("yarın Mahmutlara
gidiyorum", "Ayşe gelecek"), run `ev for <place>` with the Turkish case suffix removed
(`Mahmutlara` → `Mahmutlar`) and tell them what to take, return and collect, with where each
thing is. Record new intentions as they come up: `ev edit X to=<place>` (take it there),
`ev edit X owner=<place>` (it is theirs), `ev lend X --to <place>` / `ev back X` (lent out).
Different names for the same household are aliases of one place (`ev place alias`); if two
places turn out to be the same, `ev place merge`.

## Show, don't describe

When the person asks which thing you mean, or you name something they may not recognise, run
`ev focus <x>` (add `--photo n` for a particular photo): their open `ev ui` jumps to it and
shows its photo full screen — usually the crop you cut. Say you did it.

## Let the person watch

Suggest `ev ui` in a second terminal at the start of a session: it is read-only and
refreshes on its own, highlighting whatever you just changed, so the person sees each
record land as you make it. To look at a photo they press `o` (full screen, `[` `]` to step
through the node's photos) or `O` (system viewer); on the search tab `x` clears the search;
`J`/`K` scroll the details and `H`/`L` switch their tabs (summary, photos, grid, contents, suggestions,
history); the panes resize by dragging their dividers or with `<` `>` `{` `}`. The details start
with the node's `#id`: when the person says "#534", run commands on `#534` as it is. When they
ask what happened to a place, its History tab shows the same as `ev history <x> --contents`.

## Exit codes

| Exit | Meaning | What you do |
|---|---|---|
| 0 | success | continue |
| 2 | malformed input | fix the command |
| 3 | no node matches | `ev find <text>`, then retry with the id |
| 4 | several nodes match | pick from `error.candidates` and retry with the id |
| 5 | a rule refused the change | read `error.message` / `error.details`; tell the person |
| 6 | database is newer than this `ev` | stop; ask the person to upgrade `ev` |

A partial name never resolves (`flipper` does not find "Flipper Zero"): search first,
then act by id. Codes and names compare case- and diacritic-insensitively, so `k4x4-07-u`
finds `K4x4-07-Ü`.

## Useful reads

- `ev find <text> [--tag t] [--kind k]` — where is it? `ev find --tag t` alone lists all tagged
  t: tag things that belong together but are scattered (`3d yazıcı`) so they can be gathered.
- `ev show <ref>` — one node, its path, children, pending move, disposition.
- `ev tree [<ref>] [--depth n]` — the whole picture.
- `ev history <ref> [--contents]` — what happened to it; `--contents` adds what came in, went out
  or was added there.

Field reference and payload shapes: `REFERENCE.md` in the ev repository.

## Language and appearance

`ev ui` and the readable output are English or Turkish; JSON is always English. When the person
asks for the other language, or for a fixed light or dark look, change it for them with
`ev settings language tr|en|auto` or `ev settings theme dark|light|auto` — an open `ev ui`
follows within a second. `auto` is the default for both: the computer's language, and the
terminal's own light or dark background, followed live. `ev ui` reopens where the person left
the tree; `ev settings resume off` if they would rather start at the top.
